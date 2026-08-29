#!/usr/bin/env python3
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
BASE = ROOT.parent / "dephasing_d_availability_v01" / "dephasing_d_availability_v01.py"
EXPECTED_BASE_SHA256 = "d49778d7f07865d0bbf8530b0bc8430664589fb3cd8e4eaab45df453f0763fa0"
REPLICATION_SEED = 2026082922


def main():
    base_bytes = BASE.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != EXPECTED_BASE_SHA256:
        raise SystemExit(f"base H11 code SHA mismatch: {base_sha}")

    spec = importlib.util.spec_from_file_location("h11_stageA_engine", BASE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    mod.SEED = REPLICATION_SEED
    mod.ROOT = ROOT
    mod.RESULTS = RESULTS
    mod.OUT = RESULTS / "dephasing_d_replication_stageA_v01.json"
    mod.SELECTION = RESULTS / "stageA_dephasing_d_replication_selection.json"
    mod.SELECTION_SHA = RESULTS / "stageA_dephasing_d_replication_selection.sha256"

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod.execute()

    result = json.loads(mod.OUT.read_text(encoding="utf-8"))
    if result["status"] == "READY_FOR_BLIND_REVEAL_H11":
        result["status"] = "READY_FOR_BLIND_REVEAL_H12"
    elif result["status"] == "SELECTION_HOLD_H11":
        result["status"] = "SELECTION_HOLD_H12"
    result["replication_seed"] = REPLICATION_SEED
    result["base_h11_code_sha256"] = base_sha
    result["same_family_replication"] = True
    mod.OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
