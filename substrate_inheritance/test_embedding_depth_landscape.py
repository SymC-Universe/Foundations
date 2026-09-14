import json
from pathlib import Path

import numpy as np

from substrate_inheritance.embedding_depth_landscape import (
    _effective_depth,
    evaluate_case,
    run_fm2,
)


PLAN_PATH = Path("substrate_inheritance/SI_FM2_EMBEDDING_DEPTH_PLAN_v0.1.json")
FREEZE_PATH = Path("substrate_inheritance/SI_FM2_EXECUTION_FREEZE_v0.1.json")


def load_plan():
    return json.loads(PLAN_PATH.read_text(encoding="utf-8"))


def load_freeze():
    return json.loads(FREEZE_PATH.read_text(encoding="utf-8"))


def test_effective_depth_requires_all_deeper_records_to_stay_within_tolerance():
    records = [
        {"retained_depth_dof": 1, "relative_error_to_semi_infinite": 0.2},
        {"retained_depth_dof": 2, "relative_error_to_semi_infinite": 0.05},
        {"retained_depth_dof": 4, "relative_error_to_semi_infinite": 0.12},
        {"retained_depth_dof": 8, "relative_error_to_semi_infinite": 0.02},
        {"retained_depth_dof": 16, "relative_error_to_semi_infinite": 0.01},
    ]
    result = _effective_depth(records, 0.1)
    assert result["status"] == "REACHED_WITHIN_GRID"
    assert result["retained_depth_dof"] == 8


def test_fm2_single_case_preserves_direct_recursive_crosscheck():
    result = evaluate_case(
        depths=[1, 2, 4, 8, 16],
        hopping=0.65,
        real_frequency=0.7,
        imaginary_regularizer=0.15,
        onsite_stiffness=4.0,
        child_coupling=0.6,
        tolerances=[0.1, 0.01],
    )
    assert len(result["depth_records"]) == 5
    assert max(
        row["matrix_vs_recursive_surface_green_absolute_residual"]
        for row in result["depth_records"]
    ) < 1e-9
    assert all(np.isfinite(row["finite_dynamic_matrix_condition_number_2norm"]) for row in result["depth_records"])
    assert result["finite_bath_recurrence_status"] == "NOT_EVALUATED_FREQUENCY_DOMAIN_MAP"


def test_fm2_full_frozen_grid_is_complete_and_nonphysical():
    result = run_fm2(load_plan(), load_freeze())
    assert result["scope"] == "synthetic_fm2_embedding_depth_function_limit_map_only"
    assert result["status"] == "P0_D_DESCRIPTIVE_STRUCTURAL"
    assert result["physical_inheritance_claim"] is False
    assert result["physical_thresholds_frozen"] is False
    assert result["atlas_target_used"] is False
    assert result["chi_used"] is False
    assert result["imaginary_probe_is_damping"] is False
    assert result["numerical_effective_depth_is_physical_inheritance_length"] is False
    assert result["case_count"] == 48
    assert result["depth_record_count"] == 384
    assert len(result["cases"]) == 48
    assert all(len(case["depth_records"]) == 8 for case in result["cases"])
    assert result["numerical_verification"]["status"] == "FINITE_METHODS_AGREE_WITHIN_FROZEN_TOLERANCE"


def test_fm2_tolerance_keys_are_exactly_the_frozen_task_tolerances():
    plan = load_plan()
    result = run_fm2(plan, load_freeze())
    expected = {str(float(x)) for x in plan["declared_numerical_task_tolerances"]}
    assert set(result["summary"]["effective_depth_by_declared_numerical_tolerance"]) == expected
    for case in result["cases"]:
        assert set(case["effective_depth_by_declared_numerical_tolerance"]) == expected


def test_fm2_zero_or_invalid_science_is_not_introduced_by_execution_freeze():
    freeze = load_freeze()
    assert freeze["parameter_overrides"] is False
    assert freeze["conditioning"]["condition_number_is_physical_failure_threshold"] is False
    assert freeze["conditioning"]["automatic_case_deletion_from_condition_number"] is False
    assert freeze["firewalls"]["imaginary_probe_is_damping"] is False
    assert freeze["firewalls"]["numerical_effective_depth_is_physical_inheritance_length"] is False
    assert freeze["firewalls"]["physical_inheritance_claim"] is False
