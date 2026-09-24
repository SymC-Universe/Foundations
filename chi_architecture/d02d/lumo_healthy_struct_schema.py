from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np
import requests
from scipy.io import loadmat


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "results" / "d02d_schema"
OUT = ROOT / "results" / "D02D_LUMO_HEALTHY_STRUCT_SCHEMA_v0.1.json"
ZIP_URL = "https://data.uni-hannover.de/dataset/93b52576-6a5a-4ce9-8c27-a0372590f7b0/resource/37be937f-8e16-414e-9fd4-92d59196417c/download/exemplary_datasets_dam3_010.zip"
HEADERS = {"User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}


def fetch(path: Path) -> None:
    if path.exists():
        return
    with requests.get(ZIP_URL, headers=HEADERS, stream=True, timeout=900) as r:
        r.raise_for_status()
        with path.open("wb") as f:
            for chunk in r.iter_content(chunk_size=8 * 1024 * 1024):
                if chunk:
                    f.write(chunk)


def summarize(obj, depth=0):
    if depth > 5:
        return {"type": type(obj).__name__, "depth_limit": True}

    if isinstance(obj, np.ndarray):
        out = {
            "type": "ndarray",
            "shape": list(obj.shape),
            "dtype": str(obj.dtype),
        }
        if obj.dtype.kind in {"U", "S"} and obj.size <= 200:
            out["string_values"] = [str(x) for x in obj.reshape(-1).tolist()]
        elif obj.dtype == object and obj.size <= 200:
            out["elements"] = [summarize(x, depth + 1) for x in obj.reshape(-1).tolist()]
        return out

    if hasattr(obj, "_fieldnames"):
        return {
            "type": type(obj).__name__,
            "fields": {
                name: summarize(getattr(obj, name), depth + 1)
                for name in obj._fieldnames
            },
        }

    if isinstance(obj, (str, bytes)):
        return {"type": type(obj).__name__, "value": str(obj)[:500]}

    if np.isscalar(obj):
        # Numeric scalar values are deliberately withheld.
        return {"type": type(obj).__name__, "numeric_scalar_withheld": True}

    return {"type": type(obj).__name__}


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    zpath = CACHE / "exemplary_datasets_dam3_010.zip"
    fetch(zpath)

    with zipfile.ZipFile(zpath) as zf:
        healthy = sorted(
            x for x in zf.namelist()
            if x.startswith("11_Healthy/") and x.lower().endswith(".mat")
        )
        if len(healthy) != 5:
            raise RuntimeError(f"expected five healthy MAT files, got {len(healthy)}")
        member = healthy[0]
        raw = zf.read(member)

    mat = loadmat(io.BytesIO(raw), variable_names=["Dat"], squeeze_me=True, struct_as_record=False)
    if "Dat" not in mat:
        raise RuntimeError("Dat struct missing")

    result = {
        "schema": "d02d-lumo-healthy-struct-schema-v0.1",
        "status": "HEALTHY_SCHEMA_ONLY_NUMERIC_VALUES_WITHHELD",
        "source_member": member,
        "source_member_sha256": hashlib.sha256(raw).hexdigest(),
        "dat_schema": summarize(mat["Dat"]),
        "guard": "Only the first healthy MAT member was loaded. Numeric scalar and array values are not emitted. No damaged MAT member was opened.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "source_member": member,
        "output": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
