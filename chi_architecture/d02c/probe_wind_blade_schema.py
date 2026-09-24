from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "results" / "d02c_wind_probe"
OUT = ROOT / "results" / "D02C_WIND_BLADE_SCHEMA_v0.1.json"
BASE = "https://zenodo.org/records/18427836/files/"
HEADERS = {"User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}

FILES = {
    "climate_main": ("ClimateChamber_20221115.csv", "7afea2377fb14ca576516c39201a6aac"),
    "modal_x": ("MO04_mpe_X_20221115.csv", "0a08eb30f4361d3ebfd1a6ecfb4ff332"),
    "modal_z": ("MO04_mpe_Z_20221115.csv", "3e1ceb71d0fae2901c9256eb472d021a"),
    "raw_midnight": ("MO04_acceleration_20221115_000000.zip", "dc1bd7d724264e1a37ffdc58865f6304"),
    "raw_1300": ("MO04_acceleration_20221115_130000.zip", "50e32f0e7e711b89128a895d5c0c9481"),
    "climate_dry": ("ClimateChamber_20220927.csv", "aa3dccbefeb1644e5c8cbc030801b146"),
    "raw_dry": ("MO04_acceleration_20220927.zip", "83d9f4030346d6a3538627320a03437e"),
}


def digest_bytes(data: bytes, alg: str) -> str:
    h = hashlib.new(alg); h.update(data); return h.hexdigest()


def fetch(role: str) -> tuple[str, bytes]:
    name, expected = FILES[role]
    r = requests.get(BASE + name + "?download=1", headers=HEADERS, timeout=600)
    r.raise_for_status()
    data = r.content
    actual = digest_bytes(data, "md5")
    if actual != expected:
        raise RuntimeError(f"MD5 mismatch for {name}: {actual}")
    return name, data


def csv_schema(data: bytes) -> dict:
    text = data.decode("utf-8-sig", errors="replace")
    reader = csv.reader(io.StringIO(text))
    header = next(reader, [])
    rows = list(reader)
    # Only emit first/last timestamp-like field where it is lexical metadata, not measurement values.
    timestamp_tokens = []
    for row in rows:
        if not row:
            continue
        for value in row[:2]:
            if re.search(r"\d{4}[-/]\d{2}[-/]\d{2}", value) or re.search(r"\d{2}:\d{2}:\d{2}", value):
                timestamp_tokens.append(value)
                break
    return {
        "header": header,
        "data_row_count": len(rows),
        "first_timestamp_token": timestamp_tokens[0] if timestamp_tokens else None,
        "last_timestamp_token": timestamp_tokens[-1] if timestamp_tokens else None,
        "guard": "No measurement values emitted.",
    }


def zip_schema(data: bytes) -> dict:
    z = zipfile.ZipFile(io.BytesIO(data))
    files = []
    for info in z.infolist():
        if info.is_dir():
            continue
        item = {"path": info.filename, "size_bytes": info.file_size}
        # File names are permitted because they encode timestamps/stage availability, not outcomes.
        if info.filename.lower().endswith(".csv") and info.file_size < 20_000_000 and len(files) < 3:
            raw = z.read(info.filename)
            text = raw.decode("utf-8-sig", errors="replace")
            header = next(csv.reader(io.StringIO(text)), [])
            item["csv_header_only"] = header
        files.append(item)
    return {"file_count": len(files), "files": files}


def main() -> None:
    result = {
        "schema": "d02c-wind-blade-schema-v0.1",
        "status": "SCHEMA_AND_TIMESTAMP_AVAILABILITY_ONLY_NO_OUTCOME_INSPECTION",
        "record": "10.5281/zenodo.18427836",
        "assets": {},
    }

    for role in FILES:
        name, data = fetch(role)
        item = {
            "filename": name,
            "size_bytes": len(data),
            "md5": digest_bytes(data, "md5"),
            "sha256": digest_bytes(data, "sha256"),
        }
        if name.lower().endswith(".csv"):
            item["csv_schema"] = csv_schema(data)
        else:
            item["zip_schema"] = zip_schema(data)
        result["assets"][role] = item

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "assets": {k: v["filename"] for k,v in result["assets"].items()},
        "output": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
