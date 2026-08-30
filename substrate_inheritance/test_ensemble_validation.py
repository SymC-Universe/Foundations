import numpy as np

from substrate_inheritance.ensemble_validation import (
    SCOPE,
    auc_probability,
    best_assignment_score,
    coupling_rewire_ensemble,
    modal_same_spectrum_ensemble,
    run_ensemble_validation,
    transfer_consistency_ensemble,
)


def test_assignment_score_is_permutation_invariant_for_permuted_identity():
    overlap = np.array(
        [
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
        ]
    )
    assert np.isclose(best_assignment_score(overlap), 1.0, atol=1e-12)


def test_auc_probability_handles_complete_separation_and_ties():
    assert auc_probability(np.array([2.0, 3.0]), np.array([0.0, 1.0])) == 1.0
    assert auc_probability(np.array([1.0]), np.array([1.0])) == 0.5


def test_same_spectrum_ensemble_preserves_scalar_spectrum_and_separates_carriers():
    result = modal_same_spectrum_ensemble(trials=64, dimension=5, seed=20260830)
    assert result["same_scalar_spectrum_null"] is True
    assert result["max_same_spectrum_numerical_error"] < 1e-10
    assert result["planted_assignment_score"]["mean"] > result["same_spectrum_scrambled_assignment_score"]["mean"]
    assert result["threshold_free_auc_probability"] > 0.5


def test_coupling_rewire_changes_response_without_changing_substrate_spectrum():
    result = coupling_rewire_ensemble(trials=64, dimension=5, seed=20260831)
    assert result["substrate_spectrum_changed_by_rewire"] is False
    assert result["relative_self_energy_change"]["mean"] > 0.0
    assert result["relative_self_energy_change"]["fraction_nonzero_above_machine_scale"] > 0.5


def test_finite_difference_transfer_matches_analytic_sensitivity():
    result = transfer_consistency_ensemble(trials=64, dimension=5, seed=20260832)
    assert result["relative_transfer_error"]["maximum"] < 1e-6


def test_ensemble_output_cannot_be_mislabeled_as_physical_evidence():
    result = run_ensemble_validation()
    assert result["scope"] == SCOPE
    assert result["physical_thresholds_frozen"] is False
    assert result["real_system_evidence"] is False
    assert result["modal_same_spectrum_ensemble"]["threshold_free_auc_probability"] > 0.5
