from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "results" / "d02b_raw"
ARCHIVE = CACHE / "00_raw_exports.zip"
OUT = ROOT / "results" / "D02B_RAW_ARCHIVE_MANIFEST_v0.1.json"
URL = "https://zenodo.org/records/20038951/files/00_raw_exports.zip?download=1"
EXPECTED_MD5 = "68450ff0f1c25492ee243b8adba29991"
HEADERS = {"User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}


def file_hash(path: Path, name: str) -> str:
    h = hashlib.new(name)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    if ARCHIVE.exists() and file_hash(ARCHIVE, "md5") == EXPECTED_MD5:
        return
    with requests.get(URL, headers=HEADERS, stream=True, timeout=600) as r:
        r.raise_for_status()
        with ARCHIVE.open("wb") as f:
            for chunk in r.iter_content(chunk_size=8 * 1024 * 1024):
                if chunk:
                    f.write(chunk)


def main() -> None:
    download()
    actual_md5 = file_hash(ARCHIVE, "md5")
    if actual_md5 != EXPECTED_MD5:
        raise RuntimeError(f"raw archive MD5 mismatch: {actual_md5}")

    entries = []
    with zipfile.ZipFile(ARCHIVE) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            entries.append({
                "path": info.filename,
                "size_bytes": info.file_size,
                "compressed_size_bytes": info.compress_size,
                "crc32": f"{info.CRC:08x}",
            })

    amplitude = [x for x in entries if "/Amplitude/" in x["path"].replace("\\","/")]
    phase = [x for x in entries if "/Phase/" in x["path"].replace("\\","/")]

    result = {
        "schema": "d02b-raw-archive-manifest-v0.1",
        "status": "RAW_ARCHIVE_PATHS_ONLY_NO_FRF_VALUES_READ",
        "source": {
            "url": URL,
            "size_bytes": ARCHIVE.stat().st_size,
            "md5": actual_md5,
            "sha256": file_hash(ARCHIVE, "sha256"),
        },
        "counts": {
            "all_files": len(entries),
            "amplitude_files": len(amplitude),
            "phase_files": len(phase),
        },
        "entries": entries,
        "guard": "ZIP directory metadata only; no raw export member was opened.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "counts": result["counts"],
        "sha256": result["source"]["sha256"],
        "output": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
