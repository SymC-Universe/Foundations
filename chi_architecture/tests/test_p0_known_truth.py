import json
import math
from pathlib import Path

import numpy as np
import pytest

from p0_known_truth import (
    ArchitectureRefusal,
    asymptotic_stability,
    diagonal_state_norm,
    eigensystem,
    exact_degenerate_mode_status,
    max_transient_gain_upper,
    run_f0_f8,
    second_order_chi,
    simulate_noise_entry,
    single_pole_chi,
    two_state_hurwitz,
    upper_triangular_transition,
)


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def plan():
    return json.loads((ROOT / "P0_EXPERIMENT_PLAN_v0.2.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def results(plan):
    return run_f0_f8(plan)


def _family(plan, family_id):
    return next(x for x in plan["families"] if x["id"] == family_id)


def test_v02_plan_is_explicitly_fixture_only(plan):
    assert plan["status"] == "P0_EXPLORATORY_NOT_CONFIRMATORY"
    assert plan["anti_circularity"]["fixture_to_evidence_prohibition"]
    assert plan["future_evaluative_experiment_requirements"]["status"] == "NOT_YET_RUN"
    assert plan["future_evaluative_experiment_requirements"]["must_define_independent_outcome"] is True
    assert plan["future_evaluative_experiment_requirements"]["must_have_a_result_that_counts_against_the_hypothesis"] is True


def test_f0_normal_decoupled_is_plain_stable_baseline(results):
    assert results["F0"]["stability"] == "STABLE"
    assert results["F0"]["normality_defect_fro"] == pytest.approx(0.0, abs=1e-14)


def test_exact_upper_triangular_transition_matches_closed_form_entries():
    k = 3.25
    t = 0.7
    et = upper_triangular_transition(k, t)
    e1 = math.exp(-t)
    e2 = math.exp(-2.0 * t)
    expected = np.array([[e1, k * (e1 - e2)], [0.0, e2]])
    assert et == pytest.approx(expected, rel=1e-14, abs=1e-14)


def test_f1_same_spectrum_can_have_different_transient_behavior(results):
    cases = results["F1"]["cases"]
    eigs = [sorted((round(v[0], 12), round(v[1], 12)) for v in c["eigenvalues"]) for c in cases]
    assert all(e == eigs[0] for e in eigs)
    g0 = next(c["max_gain"] for c in cases if c["k"] == 0.0)
    g8 = next(c["max_gain"] for c in cases if c["k"] == 8.0)
    assert g0 == pytest.approx(1.0)
    assert g8 > 1.0


def test_f1_and_f6_parameters_match_their_own_plan_entries(plan, results):
    expected_f1 = [float(x) for x in _family(plan, "F1")["parameter_values"]["k"]]
    expected_f6 = [float(x) for x in _family(plan, "F6")["parameter_values"]["k"]]
    observed_f1 = [c["k"] for c in results["F1"]["cases"]]
    observed_f6 = [c["k"] for c in results["F6"]["cases"]]
    assert observed_f1 == expected_f1
    assert observed_f6 == expected_f6
    assert expected_f6[1] == 2.0


def test_f2_same_modal_basis_different_scalar_decay_changes_response(results):
    norms = [c["norm_at_evaluation_time"] for c in results["F2"]["cases"]]
    assert norms[0] > norms[-1]
    assert norms[0] == pytest.approx(math.exp(-1.0))


def test_f3_coupling_can_change_stability_with_local_terms_fixed(results):
    cases = {c["label"]: c for c in results["F3"]["cases"]}
    assert cases["zero"]["stability"] == "STABLE"
    assert cases["symmetric_destabilizing"]["stability"] == "UNSTABLE"
    assert results["F3"]["fixed_local_terms"] == {"a11": -1.0, "a22": -2.0}


def test_f4_recovers_native_hurwitz_fixture_without_calling_it_compensation(plan, results):
    f4_plan = _family(plan, "F4")
    assert f4_plan["role"] == "DESIGNED_FIXTURE_NOT_COMPENSATION_EVIDENCE"
    cases = {c["label"]: c for c in results["F4"]["cases"]}
    assert cases["insufficient_feedback"]["hurwitz_stable"] is False
    assert cases["stabilizing_feedback"]["hurwitz_stable"] is True
    assert cases["strong_stabilizing_feedback"]["hurwitz_stable"] is True
    assert cases["sign_reversed_feedback"]["hurwitz_stable"] is False


def test_f5_observer_only_noise_preserves_no_noise_physical_trajectory_for_every_seed(results):
    base = results["F5"]["cases"]["NO_NOISE"]
    observer = results["F5"]["cases"]["OBSERVER_ONLY_NOISE"]
    assert [x["seed"] for x in base] == [x["seed"] for x in observer]
    for b, o in zip(base, observer):
        assert o["final_state"] == pytest.approx(b["final_state"], rel=0.0, abs=0.0)
        assert o["state_rms"] == pytest.approx(b["state_rms"], rel=0.0, abs=0.0)
        assert o["observation_rms"] != pytest.approx(b["observation_rms"], rel=1e-12, abs=1e-12)


def test_f5_process_and_sensor_noise_enter_physical_state(results):
    base = results["F5"]["cases"]["NO_NOISE"]
    process = results["F5"]["cases"]["PROCESS_NOISE"]
    sensor = results["F5"]["cases"]["FEEDBACK_OR_SENSOR_NOISE"]
    process_deltas = [np.linalg.norm(np.asarray(p["final_state"]) - np.asarray(b["final_state"])) for b, p in zip(base, process)]
    sensor_deltas = [np.linalg.norm(np.asarray(s["final_state"]) - np.asarray(b["final_state"])) for b, s in zip(base, sensor)]
    assert all(d > 1e-8 for d in process_deltas)
    assert all(d > 1e-8 for d in sensor_deltas)


def test_f6_is_standard_fixed_spectrum_nonnormal_fixture(results):
    cases = results["F6"]["cases"]
    eigs = [sorted((round(v[0], 12), round(v[1], 12)) for v in c["eigenvalues"]) for c in cases]
    assert all(e == eigs[0] for e in eigs)
    assert cases[-1]["max_gain"] > cases[0]["max_gain"]


def test_f7_exact_degeneracy_refuses_unique_individual_modes(results):
    status = results["F7"]
    assert status["status"] == "SUBSPACE_ONLY"
    assert status["individual_mode_identity"] == "NONIDENTIFIABLE"


def test_f8_spans_licensed_under_critical_over_and_undamped_cases(results):
    cases = results["F8"]["cases"]
    assert cases["underdamped"]["status"] == "ADMISSIBLE_SECOND_ORDER_CHI"
    assert cases["underdamped"]["regime"] == "UNDERDAMPED"
    assert cases["critical"]["chi"] == pytest.approx(1.0)
    assert cases["critical"]["regime"] == "CRITICAL"
    assert cases["overdamped"]["regime"] == "OVERDAMPED"
    assert cases["undamped"]["chi"] == pytest.approx(0.0)
    assert cases["undamped"]["regime"] == "UNDERDAMPED"


def test_f8_refuses_active_antidamping_antirestoring_and_single_pole(results):
    cases = results["F8"]["cases"]
    assert cases["active_antidamping"]["status"] == "NO_ADMISSIBLE_CHI"
    assert cases["anti_restoring"]["status"] == "NO_ADMISSIBLE_CHI"
    assert cases["single_real_pole"]["status"] == "NO_ADMISSIBLE_CHI"


def test_raw_f0_to_f6_results_do_not_embed_interpretive_state_labels(results):
    for family_id in [f"F{i}" for i in range(7)]:
        assert "state" not in results[family_id]


def test_direct_hurwitz_helper_matches_known_trace_determinant_rule():
    weak = np.array([[0.3, -0.4], [0.4, -1.0]])
    good = np.array([[0.3, -0.6], [0.6, -1.0]])
    assert two_state_hurwitz(weak)["hurwitz_stable"] is False
    assert two_state_hurwitz(good)["hurwitz_stable"] is True


def test_direct_negative_gamma_is_not_admitted_as_passive_damping_chi():
    out = second_order_chi(-2.0, 1.0)
    assert out["status"] == "NO_ADMISSIBLE_CHI"


# Known-bad inputs demonstrate that checks can fail rather than merely pass good cases.
def test_known_bad_non_square_generator_is_refused():
    with pytest.raises(ArchitectureRefusal):
        asymptotic_stability([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])


def test_known_bad_nonfinite_generator_is_refused():
    with pytest.raises(ArchitectureRefusal):
        eigensystem([[1.0, float("nan")], [0.0, -1.0]])


def test_known_bad_empty_time_grid_is_refused():
    with pytest.raises(ArchitectureRefusal):
        max_transient_gain_upper(2.0, [])


def test_known_bad_noise_label_is_refused(plan):
    f5 = _family(plan, "F5")
    sim = f5["simulation"]
    with pytest.raises(ArchitectureRefusal):
        simulate_noise_entry(
            "MAGIC_NOISE",
            seed=1729,
            x0=f5["x0"],
            dt=sim["dt"],
            steps=sim["steps"],
            sigma=sim["sigma"],
            feedback_k=sim["feedback_k"],
            feedback_h=sim["feedback_h"],
        )


def test_known_bad_nonfinite_single_pole_is_refused():
    with pytest.raises(ArchitectureRefusal):
        single_pole_chi(float("nan"))


def test_known_bad_old_plan_version_is_refused():
    with pytest.raises(ArchitectureRefusal):
        run_f0_f8({"schema": "chi-architecture-p0-experiment-plan-v0.1", "families": []})
