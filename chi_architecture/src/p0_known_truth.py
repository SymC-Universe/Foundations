from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Iterable

import numpy as np


class ArchitectureRefusal(ValueError):
    """Fail-closed refusal for a mathematically unlicensed interpretation."""


def _matrix(a: Any) -> np.ndarray:
    arr = np.asarray(a, dtype=float)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ArchitectureRefusal("generator must be a finite square matrix")
    if not np.all(np.isfinite(arr)):
        raise ArchitectureRefusal("generator contains non-finite values")
    return arr


def eigensystem(a: Any) -> dict[str, Any]:
    arr = _matrix(a)
    values, vectors = np.linalg.eig(arr)
    cond = float(np.linalg.cond(vectors))
    defect = float(np.linalg.norm(arr.T @ arr - arr @ arr.T, ord="fro"))
    return {
        "eigenvalues": values,
        "right_eigenvectors": vectors,
        "eigenvector_condition_number": cond,
        "normality_defect_fro": defect,
    }


def asymptotic_stability(a: Any, tol: float = 1e-12) -> str:
    vals = np.linalg.eigvals(_matrix(a))
    m = float(np.max(np.real(vals)))
    if m < -tol:
        return "STABLE"
    if m > tol:
        return "UNSTABLE"
    return "MARGINAL_OR_INDETERMINATE"


def upper_triangular_transition(k: float, t: float) -> np.ndarray:
    """Exact exp(A t) for A=[[-1,k],[0,-2]]."""
    if t < 0 or not math.isfinite(t) or not math.isfinite(k):
        raise ArchitectureRefusal("k and t must be finite; t must be nonnegative")
    e1 = math.exp(-t)
    e2 = math.exp(-2.0 * t)
    return np.array([[e1, k * (e1 - e2)], [0.0, e2]], dtype=float)


def max_transient_gain_upper(k: float, times: Iterable[float]) -> dict[str, float]:
    best_gain = -math.inf
    best_t = math.nan
    seen = False
    for t in times:
        seen = True
        et = upper_triangular_transition(float(k), float(t))
        gain = float(np.linalg.svd(et, compute_uv=False)[0])
        if gain > best_gain:
            best_gain = gain
            best_t = float(t)
    if not seen:
        raise ArchitectureRefusal("time grid is empty")
    return {"max_gain": best_gain, "time_of_max_gain": best_t}


def diagonal_state_norm(rates: Iterable[float], t: float, x0: Iterable[float]) -> float:
    rates_arr = np.asarray(list(rates), dtype=float)
    x = np.asarray(list(x0), dtype=float)
    if rates_arr.shape != x.shape or rates_arr.ndim != 1:
        raise ArchitectureRefusal("rates and x0 must be equal-length vectors")
    if t < 0 or not np.all(np.isfinite(rates_arr)) or not np.all(np.isfinite(x)):
        raise ArchitectureRefusal("invalid decay input")
    xt = np.exp(rates_arr * t) * x
    return float(np.linalg.norm(xt))


def two_state_hurwitz(a: Any, tol: float = 1e-12) -> dict[str, Any]:
    arr = _matrix(a)
    if arr.shape != (2, 2):
        raise ArchitectureRefusal("Hurwitz trace-determinant helper is 2x2 only")
    tr = float(np.trace(arr))
    det = float(np.linalg.det(arr))
    stable = tr < -tol and det > tol
    return {"trace": tr, "determinant": det, "hurwitz_stable": bool(stable)}


def second_order_chi(gamma: float, kappa: float) -> dict[str, Any]:
    """License chi only for x'' + gamma x' + kappa x = 0 with kappa>0."""
    if not math.isfinite(gamma) or not math.isfinite(kappa):
        raise ArchitectureRefusal("gamma and kappa must be finite")
    discriminant = gamma * gamma / 4.0 - kappa
    if kappa <= 0.0:
        return {
            "status": "NO_ADMISSIBLE_CHI",
            "reason": "restoring term is not positive; critical-damping boundary is not licensed",
            "discriminant": discriminant,
        }
    omega0 = math.sqrt(kappa)
    chi = gamma / (2.0 * omega0)
    return {
        "status": "ADMISSIBLE_SECOND_ORDER_CHI",
        "omega0": omega0,
        "chi": chi,
        "discriminant": discriminant,
        "critical_boundary": bool(abs(discriminant) <= 1e-12),
    }


def single_pole_chi(_: float) -> dict[str, str]:
    return {
        "status": "NO_ADMISSIBLE_CHI",
        "reason": "a single real pole does not identify a licensed second-order factor",
    }


def exact_degenerate_mode_status(a: Any, tol: float = 1e-12) -> dict[str, Any]:
    arr = _matrix(a)
    vals = np.linalg.eigvals(arr)
    if arr.shape == (2, 2) and abs(vals[0] - vals[1]) <= tol:
        lam = complex(vals[0])
        residual = np.linalg.norm(arr - np.eye(2) * lam, ord="fro")
        if residual <= tol:
            return {
                "status": "SUBSPACE_ONLY",
                "eigenspace_dimension": 2,
                "individual_mode_identity": "NONIDENTIFIABLE",
            }
    return {"status": "INDIVIDUAL_MODE_ANALYSIS_NOT_REFUSED_BY_THIS_EXACT_TEST"}


@dataclass(frozen=True)
class NoiseExperimentResult:
    state_rms: float
    observation_rms: float
    final_state_norm: float


def _rms(arr: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(arr))))


def simulate_noise_entry(
    kind: str,
    *,
    seed: int = 20260910,
    dt: float = 0.002,
    steps: int = 5000,
    sigma: float = 0.35,
    feedback_k: float = 0.8,
    feedback_h: float = 0.8,
) -> NoiseExperimentResult:
    """Separate process, feedback-sensor, and observer-only noise paths.

    State is [x,y]. The nominal closed-loop generator is
    [[0.3, -k], [h, -1]]. Sensor noise enters the y feedback equation via h*(x+eta).
    Observer-only noise is added after the physical update and never enters the state.
    """
    if kind not in {"PROCESS_NOISE", "FEEDBACK_OR_SENSOR_NOISE", "OBSERVER_ONLY_NOISE"}:
        raise ArchitectureRefusal(f"unsupported noise entry kind: {kind}")
    if dt <= 0 or steps <= 0 or sigma < 0:
        raise ArchitectureRefusal("invalid simulation controls")

    rng = np.random.default_rng(seed)
    x = np.zeros(2, dtype=float)
    states = np.zeros((steps, 2), dtype=float)
    obs = np.zeros((steps, 2), dtype=float)

    for i in range(steps):
        z = float(rng.normal())
        dx = 0.3 * x[0] - feedback_k * x[1]
        dy = feedback_h * x[0] - x[1]

        if kind == "PROCESS_NOISE":
            x[0] += dt * dx + sigma * math.sqrt(dt) * z
            x[1] += dt * dy
        elif kind == "FEEDBACK_OR_SENSOR_NOISE":
            x[0] += dt * dx
            x[1] += dt * dy + feedback_h * sigma * math.sqrt(dt) * z
        else:
            x[0] += dt * dx
            x[1] += dt * dy

        states[i] = x
        obs[i] = x
        if kind == "OBSERVER_ONLY_NOISE":
            obs[i, 0] += sigma * z

    return NoiseExperimentResult(
        state_rms=_rms(states),
        observation_rms=_rms(obs),
        final_state_norm=float(np.linalg.norm(states[-1])),
    )


def run_f0_f8() -> dict[str, Any]:
    results: dict[str, Any] = {}

    a0 = np.diag([-1.0, -2.0])
    results["F0"] = {
        "stability": asymptotic_stability(a0),
        "normality_defect_fro": eigensystem(a0)["normality_defect_fro"],
        "state": "STANDARD_TOOLKIT_EQUIVALENT",
    }

    times = np.linspace(0.0, 8.0, 4001)
    f1_cases = []
    for k in [0.0, 1.0, 4.0, 8.0, 12.0]:
        a = np.array([[-1.0, k], [0.0, -2.0]])
        es = eigensystem(a)
        tg = max_transient_gain_upper(k, times)
        f1_cases.append({
            "k": k,
            "eigenvalues": [float(v.real) for v in np.linalg.eigvals(a)],
            "normality_defect_fro": es["normality_defect_fro"],
            **tg,
        })
    results["F1"] = {
        "cases": f1_cases[:4],
        "state": "SCALAR_SPECTRUM_INSUFFICIENT_FOR_TRANSIENT_TASK",
    }
    results["F6"] = {
        "cases": f1_cases,
        "state": "STANDARD_NONNORMAL_ANALYSIS_EXPLAINS_EFFECT_UNLESS_ARCHITECTURE_ADDS_A_SEPARATE_VALUE_AXIS",
    }

    f2 = []
    for rate in [-0.25, -1.0, -1.75]:
        f2.append({
            "rates": [rate, -2.0],
            "norm_t4": diagonal_state_norm([rate, -2.0], 4.0, [1.0, 0.0]),
        })
    results["F2"] = {
        "cases": f2,
        "state": "MODAL_GEOMETRY_INSUFFICIENT_FOR_DECAY_TASK",
    }

    f3 = []
    for label, b, c in [
        ("zero", 0.0, 0.0),
        ("symmetric_mild", 0.5, 0.5),
        ("antisymmetric", 2.0, -2.0),
        ("symmetric_destabilizing", 2.0, 2.0),
    ]:
        a = np.array([[-1.0, b], [c, -2.0]])
        f3.append({
            "label": label,
            "b": b,
            "c": c,
            "stability": asymptotic_stability(a),
            **two_state_hurwitz(a),
        })
    results["F3"] = {"cases": f3, "state": "COUPLING_SPECIFIC_SYSTEM_RESPONSE"}

    f4 = []
    for label, k, h in [
        ("feedback_absent", 0.0, 0.0),
        ("insufficient_feedback", 0.4, 0.4),
        ("stabilizing_feedback", 0.6, 0.6),
        ("strong_stabilizing_feedback", 1.0, 1.0),
        ("sign_reversed_feedback", -0.6, 0.6),
    ]:
        a = np.array([[0.3, -k], [h, -1.0]])
        f4.append({
            "label": label,
            "k": k,
            "h": h,
            "feedback_product": k * h,
            "stability": asymptotic_stability(a),
            **two_state_hurwitz(a),
        })
    results["F4"] = {
        "cases": f4,
        "state": "COMPENSATION_REQUIRES_COUPLING_SPECIFICITY",
    }

    f5 = {}
    for kind in ["PROCESS_NOISE", "FEEDBACK_OR_SENSOR_NOISE", "OBSERVER_ONLY_NOISE"]:
        r = simulate_noise_entry(kind)
        f5[kind] = {
            "state_rms": r.state_rms,
            "observation_rms": r.observation_rms,
            "final_state_norm": r.final_state_norm,
        }
    results["F5"] = {"cases": f5, "state": "NOISE_ENTRY_POINT_MUST_CHANGE_INTERPRETATION"}

    results["F7"] = exact_degenerate_mode_status(-np.eye(2))

    results["F8"] = {
        "restoring_second_order": second_order_chi(2.0, 1.0),
        "anti_restoring_second_order": second_order_chi(2.0, -1.0),
        "single_real_pole": single_pole_chi(-1.0),
    }

    return results
