from pathlib import Path

import numpy as np
import pytest

from substrate_inheritance.coupling_response_landscape import (
    CouplingResponseRefusal,
    assemble_coupled_system,
    clean_parent_system,
    generalized_modes,
    load_plan,
    projected_carrier_overlap,
    rotated_substrate_stiffness,
    run_fm1,
    self_energy_curve,
)


PLAN = Path("substrate_inheritance/SI_FM1_COUPLING_RESPONSE_PLAN_v0.1.json")


def _model():
    return load_plan(PLAN)["model"]


def test_plan_is_p0d_and_has_36_cases():
    plan = load_plan(PLAN)
    model = plan["model"]
    assert plan["status"] == "P0_D_EXPLORATORY_FUNCTION_AND_LIMIT_MAPPING"
    assert plan["mfr14_activated"] is False
    assert plan["physical_inheritance_claim"] is False
    assert len(model["coupling_scale_values"]) * len(model["carrier_geometry_angle_values_radians"]) == 36
    assert plan["reporting"]["binary_physical_pass_threshold"] is False


def test_geometry_rotation_preserves_clean_substrate_spectrum():
    model = _model()
    reference = np.asarray(model["parent_stiffness_eigenvalues"], dtype=float)
    for theta in model["carrier_geometry_angle_values_radians"]:
        rotated = rotated_substrate_stiffness(reference, theta)
        assert np.max(np.abs(np.linalg.eigvalsh(rotated) - reference)) < 1e-12


def test_zero_coupling_has_zero_embedding_rewire_and_intervention_response():
    result = run_fm1(PLAN)
    controls = result["zero_coupling_controls"]
    assert controls["maximum_embedded_response_curve_norm"] < 1e-14
    assert controls["maximum_coupling_rewire_relative_curve_change"] < 1e-14
    assert controls["maximum_intervention_derivative_magnitude"] < 1e-12


def test_origin_recovers_parent_carrier_basis_and_frequency_assignment():
    result = run_fm1(PLAN)
    origin = result["origin_control"]
    assert abs(origin["carrier_assignment_mean_overlap"] - 1.0) < 1e-12
    assert abs(origin["carrier_assignment_mean_substrate_participation"] - 1.0) < 1e-12
    assert origin["frequency_only_total_absolute_frequency_error"] < 1e-12
    assert abs(origin["frequency_only_assignment_mean_carrier_overlap"] - 1.0) < 1e-12


def test_same_spectrum_geometry_change_can_reduce_carrier_overlap_without_frequency_change():
    result = run_fm1(PLAN)
    target = next(
        r
        for r in result["records"]
        if r["coupling_scale"] == 0.0 and np.isclose(r["carrier_geometry_angle_radians"], 0.70)
    )
    assert target["same_spectrum_substrate_eigenvalue_max_error_before_coupling"] < 1e-12
    assert target["frequency_only_total_absolute_frequency_error"] < 1e-12
    assert target["carrier_assignment_mean_overlap"] < 0.95


def test_positive_coupling_produces_nonzero_embedded_response_and_intervention():
    result = run_fm1(PLAN)
    positives = [r for r in result["records"] if r["coupling_scale"] > 0.0]
    assert max(r["embedded_response_curve_norm"] for r in positives) > 0.0
    assert max(r["intervention_derivative_magnitude"] for r in positives) > 0.0


def test_coupling_rewire_changes_response_in_at_least_one_positive_case():
    result = run_fm1(PLAN)
    positives = [r for r in result["records"] if r["coupling_scale"] > 0.0]
    assert max(r["coupling_rewire_relative_curve_change"] for r in positives) > 1e-6


def test_overlap_and_participation_are_separate_outputs():
    model = _model()
    _, _, _, parent_modes = clean_parent_system(model["parent_stiffness_eigenvalues"], model["parent_masses"])
    substrate = rotated_substrate_stiffness(model["parent_stiffness_eigenvalues"], 0.2)
    mass, _, stiffness = assemble_coupled_system(
        substrate_stiffness=substrate,
        parent_masses=model["parent_masses"],
        child_local_mass=model["child_local_mass"],
        child_local_stiffness=model["child_local_stiffness"],
        coupling_scale=0.35,
        coupling_weights=model["base_coupling_weights"],
        rayleigh_alpha=model["rayleigh_damping_alpha"],
        rayleigh_beta=model["rayleigh_damping_beta"],
    )
    _, child_modes = generalized_modes(mass, stiffness)
    overlap, participation = projected_carrier_overlap(parent_modes, child_modes, np.asarray(model["parent_masses"]))
    assert overlap.shape == (4, 5)
    assert participation.shape == (5,)
    assert np.all(participation >= 0.0)
    assert np.all(participation <= 1.0 + 1e-12)


def test_negative_coupling_is_known_bad_and_refused():
    model = _model()
    substrate = rotated_substrate_stiffness(model["parent_stiffness_eigenvalues"], 0.0)
    with pytest.raises(CouplingResponseRefusal, match="INVALID_PARAMETER"):
        assemble_coupled_system(
            substrate_stiffness=substrate,
            parent_masses=model["parent_masses"],
            child_local_mass=model["child_local_mass"],
            child_local_stiffness=model["child_local_stiffness"],
            coupling_scale=-0.1,
            coupling_weights=model["base_coupling_weights"],
            rayleigh_alpha=model["rayleigh_damping_alpha"],
            rayleigh_beta=model["rayleigh_damping_beta"],
        )


def test_coupling_weights_must_preserve_declared_total_scale():
    model = _model()
    substrate = rotated_substrate_stiffness(model["parent_stiffness_eigenvalues"], 0.0)
    with pytest.raises(CouplingResponseRefusal, match="INVALID_COUPLING_WEIGHTS"):
        assemble_coupled_system(
            substrate_stiffness=substrate,
            parent_masses=model["parent_masses"],
            child_local_mass=model["child_local_mass"],
            child_local_stiffness=model["child_local_stiffness"],
            coupling_scale=0.2,
            coupling_weights=[0.2, 0.2, 0.2, 0.2],
            rayleigh_alpha=model["rayleigh_damping_alpha"],
            rayleigh_beta=model["rayleigh_damping_beta"],
        )


def test_response_curve_is_finite_for_frozen_probe_grid():
    plan = load_plan(PLAN)
    model = plan["model"]
    substrate = rotated_substrate_stiffness(model["parent_stiffness_eigenvalues"], 1.0)
    mass, damping, stiffness = assemble_coupled_system(
        substrate_stiffness=substrate,
        parent_masses=model["parent_masses"],
        child_local_mass=model["child_local_mass"],
        child_local_stiffness=model["child_local_stiffness"],
        coupling_scale=1.2,
        coupling_weights=model["base_coupling_weights"],
        rayleigh_alpha=model["rayleigh_damping_alpha"],
        rayleigh_beta=model["rayleigh_damping_beta"],
    )
    curve, condition = self_energy_curve(mass, damping, stiffness, np.asarray(plan["probe_frequencies"]))
    assert np.all(np.isfinite(curve.real))
    assert np.all(np.isfinite(curve.imag))
    assert np.isfinite(condition)


def test_full_fm1_retains_every_case_and_builds_no_master_or_system_chi():
    result = run_fm1(PLAN)
    assert result["case_count"] == 36
    assert len(result["records"]) == 36
    assert len(result["summary_by_coupling"]) == 6
    assert len(result["summary_by_geometry_angle"]) == 6
    assert result["system_scalar_chi_constructed"] is False
    assert result["master_relationship_score_constructed"] is False
    assert result["atlas_used_for_parameter_selection"] is False
    assert result["reporting_firewall"]["binary_physical_pass_threshold_applied"] is False
    assert result["real_system_evidence"] is False
    assert result["physical_inheritance_claim"] is False
