from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import zipfile

import requests
from scipy.io import whosmat


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "results" / "d02d_schema"
OUT = ROOT / "results" / "D02D_LUMO_SCHEMA_PROBE_v0.1.json"
ZIP_URL = "https://data.uni-hannover.de/dataset/93b52576-6a5a-4ce9-8c27-a0372590f7b0/resource/37be937f-8e16-414e-9fd4-92d59196417c/download/exemplary_datasets_dam3_010.zip"
README_URL = "https://data.uni-hannover.de/dataset/93b52576-6a5a-4ce9-8c27-a0372590f7b0/resource/bd0a6d0a-3ff3-4780-91cc-1d816ab39fb9/download/readme.pdf"
HEADERS = {"User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str, path: Path) -> None:
    if path.exists():
        return
    with requests.get(url, headers=HEADERS, stream=True, timeout=900) as r:
        r.raise_for_status()
        with path.open("wb") as f:
            for chunk in r.iter_content(chunk_size=8 * 1024 * 1024):
                if chunk:
                    f.write(chunk)


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    zpath = CACHE / "exemplary_datasets_dam3_010.zip"
    rpath = CACHE / "readme.pdf"
    fetch(ZIP_URL, zpath)
    fetch(README_URL, rpath)

    members = []
    mat_members = []
    with zipfile.ZipFile(zpath) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            item = {
                "path": info.filename,
                "size_bytes": info.file_size,
                "compressed_size_bytes": info.compress_size,
                "crc32": f"{info.CRC:08x}",
            }
            members.append(item)
            if info.filename.lower().endswith(".mat"):
                mat_members.append(info.filename)

        mat_schema = []
        for name in mat_members[:8]:
            raw = zf.read(name)
            try:
                variables = [
                    {"name": n, "shape": list(shape), "class": cls}
                    for n, shape, cls in whosmat(io.BytesIO(raw))
                ]
                mat_schema.append({"path": name, "variables": variables})
            except Exception as exc:
                mat_schema.append({
                    "path": name,
                    "schema_error": type(exc).__name__ + ": " + str(exc),
                })

    result = {
        "schema": "d02d-lumo-schema-probe-v0.1",
        "status": "SCHEMA_ONLY_NO_SCIENTIFIC_ARRAY_VALUES_EMITTED",
        "selection_basis": "DAM3_010 is the smallest decisive ZIP by CKAN metadata.",
        "source": {
            "zip_url": ZIP_URL,
            "zip_size_bytes": zpath.stat().st_size,
            "zip_sha256": sha256(zpath),
            "readme_url": README_URL,
            "readme_size_bytes": rpath.stat().st_size,
            "readme_sha256": sha256(rpath),
        },
        "archive": {
            "member_count": len(members),
            "mat_member_count": len(mat_members),
            "members": members,
            "mat_schema_first_eight": mat_schema,
        },
        "guard": "ZIP directory metadata and scipy.io.whosmat variable schemas only. No MATLAB scientific array values were loaded or emitted.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "member_count": len(members),
        "mat_member_count": len(mat_members),
        "zip_sha256": result["source"]["zip_sha256"],
        "output": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
