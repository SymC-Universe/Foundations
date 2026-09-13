import json
import math
from pathlib import Path

import numpy as np

from substrate_inheritance.lineage_flow_landscape import (
    carrier_overlap,
    exact_case,
    exact_generation_bases,
    operator_from_basis,
    perturbation_ensemble_case,
    run_fm3,
)


PLAN_PATH = Path("substrate_inheritance/SI_FM3_LINEAGE_FLOW_PLAN_v0.1.json")


def load_plan():
    return json.loads(PLAN_PATH.read_text(encoding="utf-8"))


def test_fm3_same_spectrum_is_preserved_exactly_before_perturbation():
    gap = 0.1
    expected = np.array([1.0, 1.1, 3.0])
    for basis in exact_generation_bases(0.6):
        operator = operator_from_basis(basis, gap)
        assert np.allclose(np.linalg.eigvalsh(operator), expected, atol=1e-12, rtol=0.0)


def test_fm3_zero_transformation_is_identity_flow_and_direct_reconvergence():
    result = exact_case(theta=0.0, spectral_gap=0.3)
    identity = np.eye(3)
    for matrix in result["transition_correspondence"]:
        assert np.allclose(np.asarray(matrix), identity, atol=1e-12, rtol=0.0)
    assert np.allclose(
        np.asarray(result["direct_generation0_to_generation3_correspondence"]),
        identity,
        atol=1e-12,
        rtol=0.0,
    )
    assert result["flow_vs_direct_reconvergence_l1"] < 1e-12
    assert result["relative_flow_threshold_applied"] is False


def test_fm3_pi_over_four_creates_exact_first_step_split_without_forced_descendant():
    result = exact_case(theta=math.pi / 4.0, spectral_gap=0.3)
    first = np.asarray(result["transition_correspondence"][0])
    assert first[0, 0] == np.testing.assert_allclose(first[0, 0], 0.5, atol=1e-12) or True
    assert np.isclose(first[0, 2], 0.5, atol=1e-12)
    dominant = result["transition_dominant_lineage"][0][0]
    assert dominant["unique_dominant"] is False
    assert dominant["child_index"] is None
    dispersion = result["transition_dispersion"][0][0]
    assert np.isclose(dispersion["effective_child_count"], 2.0, atol=1e-12)


def test_fm3_direct_reconvergence_can_be_lost_by_sequential_weight_propagation():
    result = exact_case(theta=0.6, spectral_gap=0.3)
    direct = np.asarray(result["direct_generation0_to_generation3_correspondence"])
    assert np.allclose(direct, np.eye(3), atol=1e-12, rtol=0.0)
    assert result["direct_reconvergence_error_from_identity_fro"] < 1e-12
    assert result["flow_vs_direct_reconvergence_l1"] > 0.0


def test_fm3_crowded_perturbed_case_keeps_seed_complete_envelope_and_can_refuse_identity():
    seeds = load_plan()["parameter_grid"]["perturbation_seeds"]
    result = perturbation_ensemble_case(
        theta=0.0,
        spectral_gap=0.01,
        relative_frobenius=0.01,
        seeds=seeds,
    )
    assert result["seed_count"] == len(seeds)
    assert [item["seed"] for item in result["seed_records"]] == seeds
    assert result["envelope_semantics"].endswith("not_confidence_interval")
    # The two-dimensional low-eigenvalue sector remains much better preserved
    # than individual carrier identity under near-degenerate perturbations.
    assert min(result["minimum_subspace_cosine_by_transition"]) > 0.98
    assert any(
        not step["identifiable"]
        for transition in result["transition_interval_identifiability"]
        for step in transition[:2]
    )


def test_fm3_full_plan_retains_every_grid_case_and_no_promotion_semantics():
    result = run_fm3(load_plan())
    assert result["scope"] == "synthetic_fm3_lineage_function_limit_map_only"
    assert result["status"] == "P0_D_DESCRIPTIVE_STRUCTURAL"
    assert result["physical_inheritance_claim"] is False
    assert result["physical_thresholds_frozen"] is False
    assert result["atlas_target_used"] is False
    assert result["master_score_computed"] is False
    assert result["relative_flow_is_probability"] is False
    assert result["relative_flow_is_causal_fraction"] is False
    assert result["relative_flow_is_inheritance_percentage"] is False
    assert result["relative_flow_is_promotion_score"] is False
    assert result["summary"]["case_count"] == 125
    assert result["summary"]["seed_count_per_case"] == 32
    assert result["summary"]["seed_expanded_evaluations"] == 4000
    assert result["summary"]["extinction_constructed"] is False
    assert len(result["records"]) == 125
