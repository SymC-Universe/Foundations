#!/usr/bin/env python3
"""Fail-closed readiness guard for GFSA external numerical admission.

This tool does not encode scientific thresholds or scoring rules. It only verifies
that the already-frozen external-candidate contract has been recovered and hashed
before any candidate response values are inspected.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REQUIRED_RULE_KEYS = (
    "file_provenance",
    "channel_mapping",
    "numerical_quality",
    "uncertainty_handling",
    "bandwidth",
    "observer_surrogate_order",
    "decision_logic",
    "exclusions_stop_conditions",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def emit(status: str, reason: str, **extra: object) -> None:
    payload = {"status": status, "reason": reason, **extra}
    print(json.dumps(payload, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--contract",
        default="stability_arc/gfsa_v0.7.2/external_admission/v0.7/CONTRACT_RECOVERED.json",
        help="Recovery record for the exact frozen v0.7 external-candidate contract.",
    )
    args = parser.parse_args()
    contract_path = Path(args.contract)

    if not contract_path.is_file():
        emit("PROVENANCE_HOLD", "missing_recovered_contract", contract=str(contract_path))
        return 2

    try:
        record = json.loads(contract_path.read_text(encoding="utf-8"))
    except Exception as exc:
        emit("PROVENANCE_HOLD", "invalid_contract_recovery_json", error=str(exc))
        return 2

    if record.get("candidate_values_inspected") is not False:
        emit("PROVENANCE_HOLD", "freeze_before_view_not_certified")
        return 2

    if record.get("contract_status") != "RECOVERED_EXACT_FROZEN_V0.7":
        emit("PROVENANCE_HOLD", "contract_not_exactly_recovered")
        return 2

    rules = record.get("rule_sources")
    if not isinstance(rules, dict):
        emit("PROVENANCE_HOLD", "rule_sources_missing")
        return 2

    missing = [key for key in REQUIRED_RULE_KEYS if not rules.get(key)]
    if missing:
        emit("PROVENANCE_HOLD", "required_rule_source_missing", missing=missing)
        return 2

    hashed_files = record.get("hashed_files")
    if not isinstance(hashed_files, list) or not hashed_files:
        emit("PROVENANCE_HOLD", "hashed_files_missing")
        return 2

    checked = 0
    for item in hashed_files:
        if not isinstance(item, dict):
            emit("PROVENANCE_HOLD", "malformed_hash_record")
            return 2
        path = Path(str(item.get("path", "")))
        expected = str(item.get("sha256", "")).lower()
        if not path.is_file() or len(expected) != 64:
            emit("PROVENANCE_HOLD", "hash_target_missing_or_invalid", path=str(path))
            return 2
        actual = sha256(path)
        if actual != expected:
            emit(
                "PROVENANCE_HOLD",
                "hash_mismatch",
                path=str(path),
                expected=expected,
                actual=actual,
            )
            return 3
        checked += 1

    emit("READY_FOR_FROZEN_EXTERNAL_ADMISSION", "all_pre_view_provenance_gates_present", checked_hashes=checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())
