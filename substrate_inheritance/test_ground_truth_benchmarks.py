import numpy as np

from substrate_inheritance.ground_truth_benchmarks import run_ground_truth_benchmarks


def _cases_by_id():
    result = run_ground_truth_benchmarks()
    return result, {case["case_id"]: case for case in result["cases"]}


def test_benchmark_suite_is_explicitly_synthetic_and_complete():
    result, cases = _cases_by_id()
    assert result["scope"] == "synthetic_ground_truth_benchmark_only"
    assert result["case_count"] == 10
    assert result["physical_thresholds_frozen"] is False
    assert result["real_system_evidence"] is False
    assert len(cases) == 10


def test_no_coupling_does_not_create_false_influence():
    _, cases = _cases_by_id()
    case = cases["C01_NO_COUPLING"]
    assert case["evidence_label"] == "UNRESOLVED"
    assert case["observations"]["max_abs_substrate_self_energy"] == 0.0


def test_influence_only_is_not_promoted_to_inheritance():
    _, cases = _cases_by_id()
    case = cases["C02_INFLUENCE_ONLY"]
    assert case["evidence_label"] == "SUBSTRATE_INFLUENCE"
    assert case["observations"]["transfer_norm"] > 0.0


def test_scalar_mapping_without_intervention_stays_conditional():
    _, cases = _cases_by_id()
    case = cases["C03_SCALAR_CONDITIONAL"]
    assert case["evidence_label"] == "CONDITIONAL_INHERITANCE"
    assert case["observations"]["absolute_prediction_error"] == 0.0


def test_modal_inheritance_does_not_require_scalar_equality():
    _, cases = _cases_by_id()
    case = cases["C04_MODAL_INHERITANCE_SCALAR_CHANGED"]
    assert case["evidence_label"] == "SUBSTRATE_INHERITANCE"
    assert case["observations"]["scalar_values_preserved"] is False
    assert case["observations"]["known_basis_map_residual"] < 1e-12


def test_equal_frequencies_do_not_fake_modal_inheritance():
    _, cases = _cases_by_id()
    case = cases["C05_FREQUENCY_FALSE_FRIEND"]
    assert case["observations"]["max_eigenvalue_difference"] < 1e-12
    assert case["observations"]["identity_overlap_error"] > 1e-3
    assert case["evidence_label"] == "UNRESOLVED"


def test_mode_splitting_is_detected_at_subspace_level():
    _, cases = _cases_by_id()
    case = cases["C06_MODE_SPLITTING"]
    assert np.isclose(case["observations"]["max_individual_overlap"], 0.5, atol=1e-12)
    assert np.allclose(case["observations"]["principal_angle_cosines"], [1.0], atol=1e-12)


def test_degenerate_basis_rotation_is_not_false_loss():
    _, cases = _cases_by_id()
    case = cases["C07_DEGENERATE_SUBSPACE"]
    assert np.allclose(case["observations"]["principal_angle_cosines"], [1.0, 1.0], atol=1e-12)


def test_coupling_rewiring_changes_conglomerated_response():
    _, cases = _cases_by_id()
    case = cases["C08_COUPLING_REWIRE"]
    assert case["observations"]["rewire_gap"] > 1e-6


def test_finite_bath_retains_recurrence_and_is_not_called_friction():
    _, cases = _cases_by_id()
    case = cases["C09_FINITE_BATH_RECURRENCE"]
    assert case["evidence_label"] == "NON_MARKOVIAN_OR_FINITE_BATH_HOLD"
    assert case["observations"]["late_max_abs_kernel"] > 0.1
    assert case["observations"]["late_rms_kernel"] > 0.01


def test_full_ground_truth_case_passes_all_synthetic_gates():
    _, cases = _cases_by_id()
    case = cases["C10_FULL_PROSPECTIVE_INHERITANCE"]
    assert case["evidence_label"] == "SUBSTRATE_INHERITANCE"
    assert case["observations"]["prediction_error"] < 1e-12
    assert case["observations"]["transfer_norm"] > 0.0
    assert case["observations"]["eigenvalue_preserving_scramble_gap"] > 1e-6
