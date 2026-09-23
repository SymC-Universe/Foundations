from __future__ import annotations

import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "results" / "d02b_stage_a"
OUT = ROOT / "results" / "D02B_STAGE_A_SCHEMA_v0.1.json"
CACHE.mkdir(parents=True, exist_ok=True)

BASE = "https://zenodo.org/records/20038951/files/"
ASSETS = {
    "documentation": ("01_documentation.zip", "3eb96c388b4811380ab86af9bb4be1ad"),
    "processed_tables": ("02_processed_tables.zip", "a8261869e61e2c41b799360f344b4394"),
    "scripts": ("04_scripts.zip", "f7dc41fcf2ee9b2da491e289e045eeb9"),
}
HEADERS = {"User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}


def digest(data: bytes, kind: str) -> str:
    h = hashlib.new(kind)
    h.update(data)
    return h.hexdigest()


def download(name: str) -> bytes:
    url = BASE + name + "?download=1"
    r = requests.get(url, headers=HEADERS, timeout=180)
    r.raise_for_status()
    return r.content


def csv_schema(raw: bytes, filename: str) -> dict:
    text = raw.decode("utf-8-sig", errors="replace")
    reader = csv.reader(io.StringIO(text))
    header = next(reader, [])
    row_count = 0
    for _ in reader:
        row_count += 1
    return {
        "path": filename,
        "header": header,
        "data_row_count": row_count,
        "guard": "No CSV data values emitted.",
    }


def zip_schema(data: bytes) -> dict:
    zf = zipfile.ZipFile(io.BytesIO(data))
    files = []
    for info in zf.infolist():
        if info.is_dir():
            continue
        item = {
            "path": info.filename,
            "size_bytes": info.file_size,
            "crc32": f"{info.CRC:08x}",
        }
        if info.filename.lower().endswith(".csv"):
            item["csv_schema"] = csv_schema(zf.read(info.filename), info.filename)
        files.append(item)
    return {"file_count": len(files), "files": files}


def main() -> None:
    result = {
        "schema": "d02b-stage-a-schema-v0.1",
        "status": "STAGE_A_SCHEMA_ONLY_NO_SCIENTIFIC_DATA_VALUES_EMITTED",
        "record": "10.5281/zenodo.20038951",
        "assets": {},
    }

    for role, (name, expected_md5) in ASSETS.items():
        data = download(name)
        actual_md5 = digest(data, "md5")
        if actual_md5 != expected_md5:
            raise RuntimeError(f"MD5 mismatch for {name}: {actual_md5} != {expected_md5}")
        path = CACHE / name
        path.write_bytes(data)
        result["assets"][role] = {
            "filename": name,
            "url": BASE + name + "?download=1",
            "size_bytes": len(data),
            "md5": actual_md5,
            "sha256": digest(data, "sha256"),
            "zip_schema": zip_schema(data),
        }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "asset_count": len(result["assets"]),
        "output": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
