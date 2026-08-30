from __future__ import annotations

import json
from pathlib import Path

from substrate_inheritance.real_system_adapter import (
    CORRESPONDENCE_PROTOCOL,
    SCHEMA,
    analyze_real_system_record,
    canonical_record_sha256,
)


SCOPE = "synthetic_real_system_adapter_validation_only"


def synthetic_adapter_record() -> dict:
    return {
        "schema": SCHEMA,
        "system_id": "SYNTHETIC/REAL-SYSTEM-ADAPTER-VALIDATION",
        "system_role": "development_only",
        "channel": "mechanical_harmonic",
        "correspondence_protocol": CORRESPONDENCE_PROTOCOL,
        "parent": {
            "object_id": "synthetic-clean-parent",
            "object_kind": "mass_weightable_hessian",
            "coordinate_ids": ["S1:x", "S2:x"],
            "masses": [10.0, 12.0],
            "stiffness_matrix": [[4.0, -0.6], [-0.6, 3.1]],
            "matrix_units": "synthetic_energy_per_length2",
            "mass_units": "synthetic_mass",
            "symmetry_absolute_tolerance": 1e-12,
            "source_artifact_sha256": "a" * 64,
        },
        "child": {
            "object_id": "synthetic-parent-plus-child",
            "object_kind": "mass_weightable_hessian",
            "coordinate_ids": ["S1:x", "S2:x", "A:x"],
            "masses": [10.0, 12.0, 5.0],
            "stiffness_matrix": [
                [4.1, -0.55, 0.35],
                [-0.55, 3.25, -0.25],
                [0.35, -0.25, 2.4],
            ],
            "matrix_units": "synthetic_energy_per_length2",
            "mass_units": "synthetic_mass",
            "symmetry_absolute_tolerance": 1e-12,
            "source_artifact_sha256": "b" * 64,
        },
        "shared_coordinate_map": [
            {"parent_coordinate_id": "S1:x", "child_coordinate_id": "S1:x"},
            {"parent_coordinate_id": "S2:x", "child_coordinate_id": "S2:x"},
        ],
        "provenance": {
            "source_repository": "synthetic/adapter-validation",
            "source_ref": "synthetic",
            "source_commit": "0" * 40,
            "mapping_frozen_before_target_carrier_inspection": True,
            "target_kinetics_used_to_choose_mapping": False,
            "chi_used_to_choose_mapping": False,
        },
    }


def run_adapter_validation() -> dict:
    record = synthetic_adapter_record()
    analysis = analyze_real_system_record(record)
    return {
        "scope": SCOPE,
        "physical_thresholds_frozen": False,
        "real_system_evidence": False,
        "synthetic_input_record_canonical_sha256": canonical_record_sha256(record),
        "analysis": analysis,
        "interpretation": (
            "Validates the exact machine-readable output shape that will be used for a future provenance-complete mechanical parent/child record. "
            "The record is synthetic and the adapter assigns neither a physical inheritance threshold nor an inheritance promotion label."
        ),
    }


def write_adapter_validation(path: str | Path) -> dict:
    result = run_adapter_validation()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    output = write_adapter_validation("substrate_inheritance/results/adapter_validation.json")
    print(json.dumps(output, indent=2, sort_keys=True))
