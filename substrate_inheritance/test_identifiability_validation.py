import numpy as np

from substrate_inheritance.identifiability_validation import (
    SCOPE,
    equivalent_single_frequency_couplings,
    run_identifiability_validation,
)


def test_distinct_couplings_can_match_one_scalar_self_energy():
    k_diag = np.array([2.5, 3.5, 5.0])
    c1 = np.array([[1.0], [0.0], [0.0]])
    direction = np.array([[0.0], [1.0], [1.0]])
    c2, target, matched = equivalent_single_frequency_couplings(k_diag, c1, direction, 0.4)
    assert abs(target - matched) < 1e-12
    cosine = abs(float(np.dot(c1.reshape(-1), c2.reshape(-1)))) / (
        np.linalg.norm(c1) * np.linalg.norm(c2)
    )
    assert cosine < 1e-12


def test_single_frequency_match_does_not_imply_multifrequency_identity():
    result = run_identifiability_validation(trials=64, dimension=5, seed=20260833)
    assert result["scope"] == SCOPE
    assert result["single_scalar_response_identifies_unique_coupling"] is False
    assert result["matched_frequency_self_energy_error"]["maximum"] < 1e-12
    assert result["second_frequency_relative_response_gap"]["mean"] > 0.0
    assert result["second_frequency_relative_response_gap"]["fraction_nonzero_above_machine_scale"] > 0.5


def test_identifiability_output_is_not_physical_evidence():
    result = run_identifiability_validation(trials=32, dimension=5, seed=20260833)
    assert result["physical_thresholds_frozen"] is False
    assert result["real_system_evidence"] is False
