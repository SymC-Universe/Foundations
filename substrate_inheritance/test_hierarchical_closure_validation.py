import copy
import json
from pathlib import Path

import numpy as np
import pytest

from substrate_inheritance.hierarchical_closure_validation import (
    HierarchicalClosureRefusal,
    assemble_four_dof_chain,
    direct_outer_reduction,
    full_outer_compliance,
    guyuan_boundary_reduction,
    load_plan,
    nested_exact_outer_reduction,
    one_mode_internal_resolvent_reduction,
    run_fm4,
)
from substrate_inheritance.inheritance_engine import dynamic_stiffness


PLAN = Path("substrate_inheritance/SI_FM4_HIERARCHICAL_CLOSURE_PLAN_v0.1.json")


def _system(k_internal=0.5, k_outer=0.8):
    return assemble_four_dof_chain(
        masses=np.array([1.0, 1.3, 0.9, 1.1]),
        ground_stiffness=np.array([2.4, 1.9, 1.5, 1.1]),
        inner1_boundary_coupling=0.75,
        internal_coupling=k_internal,
        boundary_outer_coupling=k_outer,
        rayleigh_alpha=0.03,
        rayleigh_beta=0.015,
    )


def test_plan_loads_as_exploratory_p0d():
    plan = load_plan(PLAN)
    assert plan["status"] == "P0_D_EXPLORATORY_FUNCTION_AND_LIMIT_MAPPING"
    assert plan["mfr14_activated"] is False
    assert plan["physical_inheritance_claim"] is False
    assert plan["expected_method_truth"]["approximation_ordering_predeclared"] is False


def test_assembled_system_is_positive_definite():
    mass, damping, stiffness = _system()
    assert np.min(np.linalg.eigvalsh(mass)) > 0.0
    assert np.min(np.linalg.eigvalsh(stiffness)) > 0.0
    assert np.min(np.linalg.eigvalsh(damping)) > 0.0


def test_direct_and_nested_schur_match_full_outer_compliance():
    mass, damping, stiffness = _system()
    for omega in [0.0, 0.4, 1.0, 1.8, 2.6]:
        d = dynamic_stiffness(stiffness, mass, omega, damping)
        full = full_outer_compliance(d)
        direct = direct_outer_reduction(d)
        nested = nested_exact_outer_reduction(d)
        assert abs(full - direct["compliance"]) < 1e-11
        assert abs(direct["compliance"] - nested["compliance"]) < 1e-11
        assert abs(direct["return"] - nested["return"]) < 1e-11


def test_zero_outer_coupling_removes_group_return_path():
    mass, damping, stiffness = _system(k_outer=0.0)
    for omega in [0.0, 0.7, 1.4, 2.4]:
        d = dynamic_stiffness(stiffness, mass, omega, damping)
        direct = direct_outer_reduction(d)
        nested = nested_exact_outer_reduction(d)
        assert abs(direct["return"]) < 1e-14
        assert abs(nested["return"]) < 1e-14


def test_guyan_static_condensation_matches_exact_outer_response_at_zero_frequency():
    mass, damping, stiffness = _system()
    d = dynamic_stiffness(stiffness, mass, 0.0, damping)
    exact = direct_outer_reduction(d)
    reduced = guyuan_boundary_reduction(mass, damping, stiffness, 0.0)
    assert abs(exact["compliance"] - reduced["compliance"]) < 1e-11
    assert abs(exact["return"] - reduced["return"]) < 1e-11


def test_approximate_reductions_return_finite_response_away_from_singularities():
    mass, damping, stiffness = _system(k_internal=1.0, k_outer=1.6)
    for omega in [0.2, 0.9, 1.7, 2.9]:
        guyuan = guyuan_boundary_reduction(mass, damping, stiffness, omega)
        one_mode = one_mode_internal_resolvent_reduction(mass, damping, stiffness, omega)
        assert np.isfinite(guyuan["compliance"].real)
        assert np.isfinite(guyuan["compliance"].imag)
        assert np.isfinite(one_mode["compliance"].real)
        assert np.isfinite(one_mode["compliance"].imag)


def test_nonpositive_mass_is_known_bad_and_refused():
    with pytest.raises(HierarchicalClosureRefusal, match="INVALID_PARAMETER"):
        assemble_four_dof_chain(
            masses=np.array([1.0, 0.0, 0.9, 1.1]),
            ground_stiffness=np.array([2.4, 1.9, 1.5, 1.1]),
            inner1_boundary_coupling=0.75,
            internal_coupling=0.5,
            boundary_outer_coupling=0.8,
            rayleigh_alpha=0.03,
            rayleigh_beta=0.015,
        )


def test_negative_coupling_is_known_bad_and_refused():
    with pytest.raises(HierarchicalClosureRefusal, match="INVALID_PARAMETER"):
        _system(k_internal=-0.1)


def test_wrong_plan_scope_is_known_bad_and_refused(tmp_path):
    plan = json.loads(PLAN.read_text())
    plan["mfr14_activated"] = True
    path = tmp_path / "bad_plan.json"
    path.write_text(json.dumps(plan))
    with pytest.raises(HierarchicalClosureRefusal, match="P0_SCOPE_VIOLATION"):
        load_plan(path)


def test_full_fm4_retains_all_planned_grid_cases_and_no_system_chi():
    plan = load_plan(PLAN)
    result = run_fm4(PLAN)
    expected_cases = len(plan["model"]["internal_coupling_values"]) * len(plan["model"]["boundary_outer_coupling_values"])
    expected_records = expected_cases * plan["frequency_grid"]["points"]
    assert result["parameter_case_count"] == expected_cases
    assert result["record_count"] == expected_records
    assert result["system_scalar_chi_constructed"] is False
    assert result["atlas_used_for_parameter_selection"] is False
    assert result["real_system_evidence"] is False
    assert result["physical_inheritance_claim"] is False
    assert result["approximation_surfaces"]["binary_physical_pass_threshold_applied"] is False


def test_full_fm4_exact_closure_passes_only_mathematical_identity_tolerance():
    result = run_fm4(PLAN)
    exact = result["exact_closure"]
    assert exact["status"] == "HIERARCHICAL_REDUCTION_SUPPORTED_IN_REGIME"
    assert exact["maximum_exact_identity_error"] <= exact["numerical_tolerance"]
    assert "not a physical inheritance threshold" in exact["tolerance_role"]


def test_full_fm4_zero_coupling_control_is_exactly_near_zero_return():
    result = run_fm4(PLAN)
    assert result["zero_outer_coupling_control"]["record_count"] > 0
    assert result["zero_outer_coupling_control"]["maximum_absolute_group_return"] < 1e-13
