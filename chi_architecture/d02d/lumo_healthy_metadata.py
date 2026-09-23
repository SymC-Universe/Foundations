from __future__ import annotations

import io
import json
from pathlib import Path
import zipfile

import requests
from scipy.io import loadmat


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "results" / "d02d_schema"
OUT = ROOT / "results" / "D02D_LUMO_HEALTHY_METADATA_v0.1.json"
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


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    zpath = CACHE / "exemplary_datasets_dam3_010.zip"
    fetch(zpath)
    with zipfile.ZipFile(zpath) as zf:
        healthy = sorted(x for x in zf.namelist() if x.startswith("11_Healthy/") and x.lower().endswith(".mat"))
        if len(healthy) != 5:
            raise RuntimeError(f"expected five healthy MAT files, got {len(healthy)}")
        raw = zf.read(healthy[0])

    mat = loadmat(io.BytesIO(raw), variable_names=["Dat"], squeeze_me=True, struct_as_record=False)
    dat = mat["Dat"]
    fs = float(dat.Fs)
    if not (fs > 0):
        raise RuntimeError("invalid sampling rate")

    result = {
        "schema": "d02d-lumo-healthy-metadata-v0.1",
        "status": "HEALTHY_METADATA_ONLY",
        "source_member": healthy[0],
        "sampling_rate_hz": fs,
        "sample_count": int(dat.Data.shape[0]),
        "channel_count": int(dat.Data.shape[1]),
        "duration_seconds_from_shape": float(dat.Data.shape[0] / fs),
        "channel_names": [str(x) for x in dat.ChannelNames.tolist()],
        "channel_units": [str(x) for x in dat.ChannelUnits.tolist()],
        "guard": "Only healthy metadata and array shape were emitted. No acceleration, strain, temperature, or damaged-state values were emitted.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
