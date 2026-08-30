import copy

import numpy as np
import pytest

from substrate_inheritance.real_system_adapter import (
    CORRESPONDENCE_PROTOCOL,
    SCHEMA,
    IngestionRefusal,
    analyze_real_system_record,
    canonical_record_sha256,
    validate_real_system_record,
)


HASH_A = "a" * 64
HASH_B = "b" * 64


def valid_record():
    return {
        "schema": SCHEMA,
        "system_id": "SYNTHETIC/ADAPTER-ONLY",
        "system_role": "development_only",
        "channel": "mechanical_harmonic",
        "correspondence_protocol": CORRESPONDENCE_PROTOCOL,
        "parent": {
            "object_id": "parent-clean-substrate",
            "object_kind": "mass_weightable_hessian",
            "coordinate_ids": ["Cu1:x", "Cu2:x"],
            "masses": [63.546, 63.546],
            "stiffness_matrix": [[4.0, -0.5], [-0.5, 3.0]],
            "matrix_units": "synthetic_energy_per_length2",
            "mass_units": "synthetic_mass",
            "symmetry_absolute_tolerance": 1e-12,
            "source_artifact_sha256": HASH_A,
        },
        "child": {
            "object_id": "child-substrate-plus-adsorbate",
            "object_kind": "mass_weightable_hessian",
            "coordinate_ids": ["Cu1:x", "Cu2:x", "A:x"],
            "masses": [63.546, 63.546, 22.99],
            "stiffness_matrix": [
                [4.1, -0.45, 0.30],
                [-0.45, 3.2, -0.20],
                [0.30, -0.20, 2.2],
            ],
            "matrix_units": "synthetic_energy_per_length2",
            "mass_units": "synthetic_mass",
            "symmetry_absolute_tolerance": 1e-12,
            "source_artifact_sha256": HASH_B,
        },
        "shared_coordinate_map": [
            {"parent_coordinate_id": "Cu1:x", "child_coordinate_id": "Cu1:x"},
            {"parent_coordinate_id": "Cu2:x", "child_coordinate_id": "Cu2:x"},
        ],
        "provenance": {
            "source_repository": "synthetic/adapter-test",
            "source_ref": "synthetic",
            "source_commit": "0" * 40,
            "mapping_frozen_before_target_carrier_inspection": True,
            "target_kinetics_used_to_choose_mapping": False,
            "chi_used_to_choose_mapping": False,
        },
    }


def refusal_code(record):
    with pytest.raises(IngestionRefusal) as exc:
        validate_real_system_record(record)
    return exc.value.code


def test_valid_record_passes_and_produces_carrier_preprocessing_only():
    record = valid_record()
    result = analyze_real_system_record(record)
    overlap = np.asarray(result["parent_to_child_projected_modal_overlap_matrix"])
    participation = np.asarray(result["child_substrate_participation_weights"])

    assert result["software_admissibility_status"] == "PASS_INPUT_CONTRACT"
    assert overlap.shape == (2, 3)
    assert participation.shape == (3,)
    assert np.all(participation >= 0.0)
    assert np.all(participation <= 1.0 + 1e-12)
    assert result["physical_inheritance_threshold_applied"] is False
    assert result["inheritance_promotion_label_assigned"] is False
    assert result["chi_computed"] is False
    assert result["damping_computed"] is False


def test_projected_overlap_columns_are_normalized_directions_not_participation():
    result = analyze_real_system_record(valid_record())
    overlap = np.asarray(result["parent_to_child_projected_modal_overlap_matrix"])
    participation = np.asarray(result["child_substrate_participation_weights"])
    assert np.allclose(np.sum(overlap, axis=0), 1.0, atol=1e-12)
    assert not np.allclose(participation, np.ones_like(participation))


def test_mapping_must_cover_every_parent_coordinate_exactly_once():
    record = valid_record()
    record["shared_coordinate_map"] = record["shared_coordinate_map"][:1]
    assert refusal_code(record) == "INCOMPLETE_PARENT_MAPPING"


def test_duplicate_child_mapping_is_refused():
    record = valid_record()
    record["shared_coordinate_map"][1]["child_coordinate_id"] = "Cu1:x"
    assert refusal_code(record) == "DUPLICATE_CHILD_MAPPING"


def test_mapping_must_be_frozen_before_target_carrier_inspection():
    record = valid_record()
    record["provenance"]["mapping_frozen_before_target_carrier_inspection"] = False
    assert refusal_code(record) == "MAPPING_NOT_PROSPECTIVE"


def test_target_kinetic_leakage_is_refused():
    record = valid_record()
    record["provenance"]["target_kinetics_used_to_choose_mapping"] = True
    assert refusal_code(record) == "TARGET_LEAKAGE"


def test_chi_based_mode_mapping_is_refused():
    record = valid_record()
    record["provenance"]["chi_used_to_choose_mapping"] = True
    assert refusal_code(record) == "TARGET_LEAKAGE"


def test_unit_mismatch_is_refused_upstream_of_analysis():
    record = valid_record()
    record["child"]["matrix_units"] = "different_units"
    assert refusal_code(record) == "MATRIX_UNIT_MISMATCH"


def test_invalid_source_hash_is_refused():
    record = valid_record()
    record["parent"]["source_artifact_sha256"] = "not-a-hash"
    assert refusal_code(record) == "INVALID_SHA256"


def test_asymmetry_beyond_declared_tolerance_is_refused():
    record = valid_record()
    record["child"]["stiffness_matrix"][0][1] = -0.40
    assert refusal_code(record) == "ASYMMETRIC_MATRIX"


def test_tiny_asymmetry_inside_declared_tolerance_is_only_numerically_cleaned():
    record = valid_record()
    record["child"]["symmetry_absolute_tolerance"] = 1e-8
    record["child"]["stiffness_matrix"][0][1] += 1e-10
    result = analyze_real_system_record(record)
    assert result["software_admissibility_status"] == "PASS_INPUT_CONTRACT"


def test_nonpositive_mass_is_refused():
    record = valid_record()
    record["parent"]["masses"][0] = 0.0
    assert refusal_code(record) == "NONPOSITIVE_MASS"


def test_schema_or_protocol_drift_is_refused():
    record = valid_record()
    record["correspondence_protocol"] = "old-protocol.json"
    assert refusal_code(record) == "PROTOCOL_MISMATCH"


def test_canonical_record_hash_is_stable_to_dictionary_key_order():
    record = valid_record()
    reordered = copy.deepcopy(record)
    reordered = dict(reversed(list(reordered.items())))
    assert canonical_record_sha256(record) == canonical_record_sha256(reordered)
