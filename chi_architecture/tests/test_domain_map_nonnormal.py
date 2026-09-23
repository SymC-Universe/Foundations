import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm

from domain_map_nonnormal import (
    construct_generator,
    exact_propagators,
    evaluate_case,
    load_freeze,
    run_d01c,
)


FREEZE = Path("chi_architecture/D01C_PREEXECUTION_FREEZE_v0.1.json")


def freeze():
    return load_freeze(FREEZE)


def test_freeze_scientific_surface_is_predeclared_and_no_master_scalar_is_enabled():
    f = freeze()
    assert f["schema"] == "d01c-nonnormal-preexecution-freeze-v0.1"
    assert f["status"] == "P0_D_PREEXECUTION_FROZEN_BEFORE_D01C_OUTPUT"
    assert f["scalar_policy"]["master_scalar_search"] is False
    assert f["anti_circularity"]["no_D01B_outcome_tuning"] is True
    assert f["anti_circularity"]["no_Atlas_target_used"] is True
    assert f["anti_circularity"]["all_frozen_cases_retained"] is True
    assert len(f["generator_family"]["spectral_families"]) == 2
    assert len(f["generator_family"]["theta_degrees"]) == 13


def test_constructed_family_preserves_spectrum_across_nonorthogonality():
    for theta in [90.0, 30.0, 5.0, 0.5]:
        a, _ = construct_generator(-1.0, -2.0, theta)
        actual = np.sort(np.linalg.eigvals(a).real)
        assert np.allclose(actual, [-2.0, -1.0], atol=1e-12, rtol=0.0)


def test_normal_limit_is_diagonal_and_has_no_transient_operator_gain():
    f = freeze()
    r = evaluate_case("N1", [-1.0, -2.0], 90.0, f)
    a = np.asarray(r["generator"])
    assert np.allclose(a, np.diag([-1.0, -2.0]), atol=1e-12)
    assert r["max_operator_state_gain"] == 1.0
    assert r["right_eigenvector_condition_number"] == 1.0


def test_carrier_conditioning_increases_as_angle_closes():
    values = []
    for theta in [90.0, 30.0, 5.0, 0.5]:
        _, v = construct_generator(-1.0, -2.0, theta)
        values.append(np.linalg.cond(v))
    assert values == sorted(values)
    assert values[-1] > 100.0


def test_exact_propagator_matches_scipy_matrix_exponential():
    a, _ = construct_generator(-0.25, -2.0, 7.5)
    t = np.asarray([0.0, 0.3, 1.7, 4.0])
    p = exact_propagators(-0.25, -2.0, 7.5, t)
    for i, ti in enumerate(t):
        assert np.allclose(p[i], expm(a * ti), atol=1e-12, rtol=1e-12)


def test_fixed_spectrum_can_change_finite_time_behavior_without_emitting_master_chi():
    f = freeze()
    normal = evaluate_case("N1", [-1.0, -2.0], 90.0, f)
    nonnormal = evaluate_case("N1", [-1.0, -2.0], 1.0, f)
    assert normal["eigenvalues"] == nonnormal["eigenvalues"]
    assert normal["spectral_abscissa"] == nonnormal["spectral_abscissa"]
    assert nonnormal["max_operator_state_gain"] > normal["max_operator_state_gain"]
    assert nonnormal["resolvent_peak_2norm"] > normal["resolvent_peak_2norm"]
    assert normal["scalar_status"] == "NO_MASTER_SCALAR_SEARCHED"
    assert nonnormal["scalar_status"] == "NO_MASTER_SCALAR_SEARCHED"


def test_full_frozen_map_has_expected_case_count_and_retains_every_case():
    r = run_d01c(freeze())
    assert r["case_count"] == 26
    assert r["expected_case_count"] == 26
    assert len(r["records"]) == 26
    assert len(r["family_summaries"]) == 2
    assert r["max_spectral_residual"] < 1e-10
    assert r["master_scalar_searched"] is False
