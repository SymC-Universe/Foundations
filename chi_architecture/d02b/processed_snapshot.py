from __future__ import annotations

import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "D02B_PROCESSED_SNAPSHOT_v0.1.json"
BASE = "https://zenodo.org/records/20038951/files/"
HEADERS = {"User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}
ASSETS = {
    "documentation": ("01_documentation.zip", "3eb96c388b4811380ab86af9bb4be1ad"),
    "processed": ("02_processed_tables.zip", "a8261869e61e2c41b799360f344b4394"),
}


def fetch(name: str, expected_md5: str) -> bytes:
    r = requests.get(BASE + name + "?download=1", headers=HEADERS, timeout=180)
    r.raise_for_status()
    data = r.content
    actual = hashlib.md5(data).hexdigest()
    if actual != expected_md5:
        raise RuntimeError(f"MD5 mismatch for {name}")
    return data


def read_csv(zf: zipfile.ZipFile, path: str) -> list[dict[str, str]]:
    raw = zf.read(path).decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(raw)))


def main() -> None:
    doc_data = fetch(*ASSETS["documentation"])
    proc_data = fetch(*ASSETS["processed"])
    doc = zipfile.ZipFile(io.BytesIO(doc_data))
    proc = zipfile.ZipFile(io.BytesIO(proc_data))

    torque = read_csv(doc, "01_documentation/torque_states.csv")
    audit = read_csv(proc, "02_processed_tables/resonance_group_selection_audit.csv")
    windows = read_csv(proc, "02_processed_tables/adaptive_tracking_windows.csv")
    tracked = read_csv(proc, "02_processed_tables/tracked_frequencies.csv")
    per_case = read_csv(proc, "02_processed_tables/per_case_metrics.csv")
    dose = read_csv(proc, "02_processed_tables/dose_response.csv")

    retained = [r for r in audit if str(r["retained"]).strip().lower() in {"true","1","yes"}]
    if len(retained) != len(windows):
        raise RuntimeError(f"retained/window mismatch: {len(retained)} vs {len(windows)}")

    result = {
        "schema": "d02b-processed-snapshot-v0.1",
        "status": "PROCESSED_VALUES_ARCHIVED_BEFORE_RAW_FRF_INSPECTION",
        "source_record": "10.5281/zenodo.20038951",
        "torque_states": torque,
        "retained_resonance_audit_rows": retained,
        "tracking_windows": windows,
        "tracked_frequencies": tracked,
        "per_case_metrics": per_case,
        "dose_response": dose,
        "counts": {
            "torque_states": len(torque),
            "retained_families": len(retained),
            "tracked_frequency_rows": len(tracked),
            "per_case_rows": len(per_case),
            "dose_response_rows": len(dose),
        },
        "guard": "Raw FRF archive was not downloaded or opened by this script.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["counts"], indent=2))


if __name__ == "__main__":
    main()
