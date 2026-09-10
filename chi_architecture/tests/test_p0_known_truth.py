import math

import numpy as np
import pytest

from p0_known_truth import (
    ArchitectureRefusal,
    asymptotic_stability,
    diagonal_state_norm,
    eigensystem,
    exact_degenerate_mode_status,
    max_transient_gain_upper,
    second_order_chi,
    simulate_noise_entry,
    single_pole_chi,
    two_state_hurwitz,
)


def test_f0_normal_decoupled_is_plain_stable_baseline():
    a = np.diag([-1.0, -2.0])
    assert asymptotic_stability(a) == "STABLE"
    assert eigensystem(a)["normality_defect_fro"] == pytest.approx(0.0, abs=1e-14)


def test_f1_same_spectrum_can_have_different_transient_behavior():
    times = np.linspace(0.0, 8.0, 4001)
    g0 = max_transient_gain_upper(0.0, times)["max_gain"]
    g8 = max_transient_gain_upper(8.0, times)["max_gain"]
    a0 = np.array([[-1.0, 0.0], [0.0, -2.0]])
    a8 = np.array([[-1.0, 8.0], [0.0, -2.0]])
    assert np.sort(np.linalg.eigvals(a0)) == pytest.approx(np.sort(np.linalg.eigvals(a8)))
    assert g0 == pytest.approx(1.0)
    assert g8 > 1.0


def test_f2_same_modal_basis_different_scalar_decay_changes_response():
    slow = diagonal_state_norm([-0.25, -2.0], 4.0, [1.0, 0.0])
    fast = diagonal_state_norm([-1.75, -2.0], 4.0, [1.0, 0.0])
    assert slow > fast
    assert slow == pytest.approx(math.exp(-1.0))


def test_f3_coupling_can_change_stability_with_local_terms_fixed():
    zero = np.array([[-1.0, 0.0], [0.0, -2.0]])
    bad = np.array([[-1.0, 2.0], [2.0, -2.0]])
    assert asymptotic_stability(zero) == "STABLE"
    assert asymptotic_stability(bad) == "UNSTABLE"
    assert np.diag(zero) == pytest.approx(np.diag(bad))


def test_f4_feedback_stability_requires_correct_strength_and_sign():
    weak = np.array([[0.3, -0.4], [0.4, -1.0]])
    good = np.array([[0.3, -0.6], [0.6, -1.0]])
    reversed_sign = np.array([[0.3, 0.6], [0.6, -1.0]])
    assert two_state_hurwitz(weak)["hurwitz_stable"] is False
    assert two_state_hurwitz(good)["hurwitz_stable"] is True
    assert two_state_hurwitz(reversed_sign)["hurwitz_stable"] is False


def test_f5_observer_noise_does_not_change_true_state_but_process_noise_does():
    observer = simulate_noise_entry("OBSERVER_ONLY_NOISE")
    process = simulate_noise_entry("PROCESS_NOISE")
    sensor = simulate_noise_entry("FEEDBACK_OR_SENSOR_NOISE")
    assert observer.state_rms == pytest.approx(0.0, abs=1e-15)
    assert observer.observation_rms > 0.0
    assert process.state_rms > 0.0
    assert sensor.state_rms > 0.0


def test_f7_exact_degeneracy_refuses_unique_individual_modes():
    status = exact_degenerate_mode_status(-np.eye(2))
    assert status["status"] == "SUBSPACE_ONLY"
    assert status["individual_mode_identity"] == "NONIDENTIFIABLE"


def test_f8_restoring_second_order_admits_chi_and_exact_boundary():
    out = second_order_chi(2.0, 1.0)
    assert out["status"] == "ADMISSIBLE_SECOND_ORDER_CHI"
    assert out["chi"] == pytest.approx(1.0)
    assert out["critical_boundary"] is True


def test_f8_antirestoring_refuses_chi_critical_boundary_interpretation():
    out = second_order_chi(2.0, -1.0)
    assert out["status"] == "NO_ADMISSIBLE_CHI"
    assert out["discriminant"] > 0.0


def test_f8_single_pole_refuses_second_order_chi():
    assert single_pole_chi(-1.0)["status"] == "NO_ADMISSIBLE_CHI"


# These known-bad inputs demonstrate that checks can fail rather than merely pass good cases.
def test_known_bad_non_square_generator_is_refused():
    with pytest.raises(ArchitectureRefusal):
        asymptotic_stability([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])


def test_known_bad_nonfinite_generator_is_refused():
    with pytest.raises(ArchitectureRefusal):
        eigensystem([[1.0, float("nan")], [0.0, -1.0]])


def test_known_bad_empty_time_grid_is_refused():
    with pytest.raises(ArchitectureRefusal):
        max_transient_gain_upper(2.0, [])


def test_known_bad_noise_label_is_refused():
    with pytest.raises(ArchitectureRefusal):
        simulate_noise_entry("MAGIC_NOISE")
