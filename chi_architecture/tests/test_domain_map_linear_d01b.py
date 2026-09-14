import json
from pathlib import Path

import numpy as np
import pytest

from domain_map_linear import (
    DomainMapRefusal,
    evaluate_d01b_case,
    iter_d01b_parameter_cases,
    mechanical_2dof_matrices,
)


PLAN_PATH = Path("chi_architecture/D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json")
FREEZE_PATH = Path("chi_architecture/D01B_EXECUTION_FREEZE_v0.1.json")


def load_plan():
    return json.loads(PLAN_PATH.read_text(encoding="utf-8"))


def load_freeze():
    return json.loads(FREEZE_PATH.read_text(encoding="utf-8"))


def perturbations():
    plan = load_plan()
    phase = next(p for p in plan["phases"] if p["id"] == "D01B_COUPLED_2DOF")
    return phase["perturbations"]


def test_d01b_parent_grid_has_exact_declared_case_count_and_no_hidden_parameters():
    cases = iter_d01b_parameter_cases(load_plan())
    assert len(cases) == 1 * 3 * 4 * 4 * 6 * 4
    assert set(cases[0]) == {
        "k1",
        "k2",
        "local_damping_c1",
        "local_damping_c2",
        "coupling_stiffness_kc",
        "coupling_damping_cc",
    }


def test_d01b_execution_freeze_cannot_override_scientific_grid():
    freeze = load_freeze()
    assert freeze["scientific_parameter_source"] == "parent_plan_only"
    assert freeze["parameter_overrides"] is False
    assert freeze["anti_circularity"]["no_nsdp0d16_17_19_parameter_tuning"] is True
    assert freeze["anti_circularity"]["no_atlas_target_or_range_used"] is True
    assert freeze["anti_circularity"]["no_master_scalar_predeclared"] is True


def test_zero_coupling_state_matrix_is_block_equivalent_to_two_isolated_components():
    _, _, _, a = mechanical_2dof_matrices(k1=1.0, k2=2.0, c1=0.5, c2=1.0, kc=0.0, cc=0.0)
    vals = np.linalg.eigvals(a)
    r1 = np.roots([1.0, 0.5, 1.0])
    r2 = np.roots([1.0, 1.0, 2.0])
    expected = np.r_[r1, r2]
    unmatched = list(vals)
    for target in expected:
        idx = int(np.argmin([abs(v - target) for v in unmatched]))
        assert abs(unmatched.pop(idx) - target) < 1e-10


def test_local_component_chi_is_unchanged_when_only_coupling_changes():
    base = {
        "k1": 1.0,
        "k2": 2.0,
        "local_damping_c1": 0.5,
        "local_damping_c2": 1.0,
        "coupling_stiffness_kc": 0.0,
        "coupling_damping_cc": 0.0,
    }
    coupled = dict(base, coupling_stiffness_kc=1.0, coupling_damping_cc=0.5)
    r0 = evaluate_d01b_case(base, perturbations(), load_freeze())
    r1 = evaluate_d01b_case(coupled, perturbations(), load_freeze())
    assert r0["isolated_component_coordinates"]["chi1"] == pytest.approx(r1["isolated_component_coordinates"]["chi1"])
    assert r0["isolated_component_coordinates"]["chi2"] == pytest.approx(r1["isolated_component_coordinates"]["chi2"])
    assert r0["spectral_displacement_from_uncoupled_rms"] == pytest.approx(0.0, abs=1e-12)
    assert r1["spectral_displacement_from_uncoupled_rms"] > 0.0


def test_exact_modal_scalarization_is_admitted_only_when_commuting_structure_earns_it():
    uncoupled = {
        "k1": 1.0,
        "k2": 2.0,
        "local_damping_c1": 0.5,
        "local_damping_c2": 1.0,
        "coupling_stiffness_kc": 0.0,
        "coupling_damping_cc": 0.0,
    }
    nonproportional = dict(uncoupled, coupling_stiffness_kc=1.0, coupling_damping_cc=0.0)
    r0 = evaluate_d01b_case(uncoupled, perturbations(), load_freeze())
    r1 = evaluate_d01b_case(nonproportional, perturbations(), load_freeze())
    assert r0["exact_real_modal_scalarization"]["status"] == "EXACT_REAL_MODAL_SCALARIZATION_ADMISSIBLE"
    assert len(r0["exact_real_modal_scalarization"]["modal_chi"]) == 2
    assert r1["exact_real_modal_scalarization"]["status"] == "NO_EXACT_REAL_MODAL_SCALARIZATION"
    assert r1["exact_real_modal_scalarization"]["modal_chi"] == []


def test_passive_mechanical_response_respects_energy_accounting_and_no_master_system_chi_is_emitted():
    params = {
        "k1": 1.0,
        "k2": 0.5,
        "local_damping_c1": 0.5,
        "local_damping_c2": 0.1,
        "coupling_stiffness_kc": 0.5,
        "coupling_damping_cc": 0.1,
    }
    result = evaluate_d01b_case(params, perturbations(), load_freeze())
    assert result["asymptotic_stability"] is True
    assert "system_chi" not in result
    assert "master_chi" not in result
    assert len(result["responses"]) == 2
    for response in result["responses"]:
        assert response["max_transient_energy_gain"] <= 1.0 + 1e-10
        assert response["maximum_energy_balance_residual_fraction"] < 5e-3
        assert 0.0 <= response["receiving_component_peak_energy_fraction"] <= 1.0 + 1e-10
        assert 0.0 <= response["coupling_spring_peak_energy_fraction"] <= 1.0 + 1e-10


def test_invalid_active_or_negative_coupling_refuses_passive_d01b_construction():
    with pytest.raises(DomainMapRefusal):
        mechanical_2dof_matrices(k1=1.0, k2=1.0, c1=-0.1, c2=0.5, kc=0.2, cc=0.1)
    with pytest.raises(DomainMapRefusal):
        mechanical_2dof_matrices(k1=1.0, k2=1.0, c1=0.1, c2=0.5, kc=-0.2, cc=0.1)
