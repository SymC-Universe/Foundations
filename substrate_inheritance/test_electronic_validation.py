from substrate_inheritance.electronic_validation import (
    SCOPE,
    basis_invariance_case,
    run_electronic_validation,
    same_spectrum_carrier_scramble_ensemble,
    schur_identity_case,
)


def test_electronic_full_and_reduced_green_functions_agree():
    result = schur_identity_case()
    assert result["maximum_full_vs_reduced_green_residual"] < 1e-10


def test_electronic_self_energy_is_basis_invariant_when_coupling_cotransforms():
    result = basis_invariance_case()
    assert result["maximum_curve_residual"] < 1e-10


def test_same_electronic_spectrum_does_not_fix_interface_response():
    result = same_spectrum_carrier_scramble_ensemble(trials=64, dimension=5, seed=20260851)
    assert result["maximum_same_spectrum_numerical_error"] < 1e-10
    assert result["relative_self_energy_curve_gap"]["mean"] > 0.0
    assert result["relative_self_energy_curve_gap"]["fraction_nonzero_above_machine_scale"] > 0.5


def test_electronic_channel_is_not_reclassified_as_mechanical_damping():
    result = run_electronic_validation()
    assert result["scope"] == SCOPE
    assert result["physical_thresholds_frozen"] is False
    assert result["real_system_evidence"] is False
    assert result["mechanical_damping_inferred"] is False
    assert result["electronic_hybridization_identified_with_mechanical_gamma"] is False
