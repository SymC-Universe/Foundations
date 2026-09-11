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


def _family(plan: dict[str, Any], family_id: str) -> dict[str, Any]:
    matches = [x for x in plan.get("families", []) if x.get("id") == family_id]
    if len(matches) != 1:
        raise ArchitectureRefusal(f"plan must contain exactly one {family_id} family")
    return matches[0]


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


def second_order_chi(gamma: float, kappa: float, tol: float = 1e-12) -> dict[str, Any]:
    """License damping-ratio chi only for x'' + gamma x' + kappa x = 0.

    This demo requires a positive restoring term and nonnegative dissipative
    coefficient. Negative gamma is active antidamping and requires a separate
    construction rather than inheriting passive damping semantics.
    """
    if not math.isfinite(gamma) or not math.isfinite(kappa):
        raise ArchitectureRefusal("gamma and kappa must be finite")
    discriminant = gamma * gamma / 4.0 - kappa
    if kappa <= 0.0:
        return {
            "status": "NO_ADMISSIBLE_CHI",
            "reason": "restoring term is not positive; passive critical-damping interpretation is not licensed",
            "discriminant": discriminant,
        }
    if gamma < 0.0:
        return {
            "status": "NO_ADMISSIBLE_CHI",
            "reason": "negative gamma is active antidamping; passive damping-ratio chi is not licensed by this demo",
            "discriminant": discriminant,
        }
    omega0 = math.sqrt(kappa)
    chi = gamma / (2.0 * omega0)
    scale = max(1.0, abs(kappa), abs(gamma * gamma / 4.0))
    critical = abs(discriminant) <= tol * scale
    if critical:
        regime = "CRITICAL"
    elif discriminant < 0.0:
        regime = "UNDERDAMPED"
    else:
        regime = "OVERDAMPED"
    return {
        "status": "ADMISSIBLE_SECOND_ORDER_CHI",
        "omega0": omega0,
        "chi": chi,
        "discriminant": discriminant,
        "regime": regime,
        "critical_boundary": bool(critical),
    }


def single_pole_chi(pole: float) -> dict[str, str]:
    if not math.isfinite(pole):
        raise ArchitectureRefusal("pole must be finite")
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
    final_state: tuple[float, float]


def _rms(arr: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(arr))))


def simulate_noise_entry(
    kind: str,
    *,
    seed: int,
    x0: Iterable[float],
    dt: float,
    steps: int,
    sigma: float,
    feedback_k: float,
    feedback_h: float,
) -> NoiseExperimentResult:
    """Separate no-noise, process, feedback-sensor, and observer-only paths."""
    allowed = {"NO_NOISE", "PROCESS_NOISE", "FEEDBACK_OR_SENSOR_NOISE", "OBSERVER_ONLY_NOISE"}
    if kind not in allowed:
        raise ArchitectureRefusal(f"unsupported noise entry kind: {kind}")
    if dt <= 0 or steps <= 0 or sigma < 0:
        raise ArchitectureRefusal("invalid simulation controls")
    if not all(math.isfinite(v) for v in (dt, sigma, feedback_k, feedback_h)):
        raise ArchitectureRefusal("simulation controls must be finite")

    initial = np.asarray(list(x0), dtype=float)
    if initial.shape != (2,) or not np.all(np.isfinite(initial)):
        raise ArchitectureRefusal("x0 must be a finite length-2 vector")

    rng = np.random.default_rng(int(seed))
    x = initial.copy()
    states = np.zeros((steps, 2), dtype=float)
    obs = np.zeros((steps, 2), dtype=float)

    for i in range(steps):
        z = float(rng.normal())
        dx = 0.3 * x[0] - feedback_k * x[1]
        dy = feedback_h * x[0] - x[1]

        x[0] += dt * dx
        x[1] += dt * dy

        if kind == "PROCESS_NOISE":
            x[0] += sigma * math.sqrt(dt) * z
        elif kind == "FEEDBACK_OR_SENSOR_NOISE":
            x[1] += feedback_h * sigma * math.sqrt(dt) * z

        states[i] = x
        obs[i] = x
        if kind == "OBSERVER_ONLY_NOISE":
            obs[i, 0] += sigma * z

    return NoiseExperimentResult(
        state_rms=_rms(states),
        observation_rms=_rms(obs),
        final_state_norm=float(np.linalg.norm(states[-1])),
        final_state=(float(states[-1, 0]), float(states[-1, 1])),
    )


def _time_grid(spec: dict[str, Any]) -> np.ndarray:
    start = float(spec["start"])
    stop = float(spec["stop"])
    points = int(spec["points"])
    if start < 0.0 or stop < start or points < 2:
        raise ArchitectureRefusal("invalid time grid in plan")
    return np.linspace(start, stop, points)


def run_f0_f8(plan: dict[str, Any]) -> dict[str, Any]:
    """Run v0.2 plan-driven designed fixtures and emit raw/native metrics.

    F0-F8 are method fixtures. Their outputs must not contain prewritten
    architecture-success labels. Exact refusal/admission statuses remain
    permitted because they are returned by the mathematical guard itself.
    """
    if plan.get("schema") != "chi-architecture-p0-experiment-plan-v0.2":
        raise ArchitectureRefusal("runner requires P0 experiment plan v0.2")

    results: dict[str, Any] = {}

    f0 = _family(plan, "F0")
    a0 = _matrix(f0["matrix"])
    results["F0"] = {
        "stability": asymptotic_stability(a0),
        "eigenvalues": [[float(v.real), float(v.imag)] for v in np.linalg.eigvals(a0)],
        "normality_defect_fro": eigensystem(a0)["normality_defect_fro"],
    }

    f1 = _family(plan, "F1")
    times1 = _time_grid(f1["time_grid"])
    f1_cases = []
    for k in f1["parameter_values"]["k"]:
        kf = float(k)
        a = np.array([[-1.0, kf], [0.0, -2.0]])
        es = eigensystem(a)
        tg = max_transient_gain_upper(kf, times1)
        f1_cases.append({
            "k": kf,
            "eigenvalues": [[float(v.real), float(v.imag)] for v in np.linalg.eigvals(a)],
            "normality_defect_fro": es["normality_defect_fro"],
            **tg,
        })
    results["F1"] = {"cases": f1_cases}

    f2 = _family(plan, "F2")
    f2_cases = []
    x0 = [float(x) for x in f2["x0"]]
    eval_time = float(f2["evaluation_time"])
    for matrix in f2["matrices"]:
        arr = _matrix(matrix)
        if not np.allclose(arr, np.diag(np.diag(arr)), atol=0.0, rtol=0.0):
            raise ArchitectureRefusal("F2 matrices must be exactly diagonal")
        rates = np.diag(arr)
        f2_cases.append({
            "rates": [float(v) for v in rates],
            "norm_at_evaluation_time": diagonal_state_norm(rates, eval_time, x0),
        })
    results["F2"] = {"evaluation_time": eval_time, "x0": x0, "cases": f2_cases}

    f3 = _family(plan, "F3")
    a11 = float(f3["fixed_local_terms"]["a11"])
    a22 = float(f3["fixed_local_terms"]["a22"])
    f3_cases = []
    for case in f3["coupling_cases"]:
        b = float(case["b"])
        c = float(case["c"])
        a = np.array([[a11, b], [c, a22]])
        f3_cases.append({
            "label": case["label"],
            "b": b,
            "c": c,
            "eigenvalues": [[float(v.real), float(v.imag)] for v in np.linalg.eigvals(a)],
            "stability": asymptotic_stability(a),
            **two_state_hurwitz(a),
        })
    results["F3"] = {"fixed_local_terms": {"a11": a11, "a22": a22}, "cases": f3_cases}

    f4 = _family(plan, "F4")
    plant = float(f4["fixed_local_terms"]["plant_rate"])
    feedback_rate = float(f4["fixed_local_terms"]["feedback_state_rate"])
    f4_cases = []
    for case in f4["cases"]:
        k = float(case["k"])
        h = float(case["h"])
        a = np.array([[plant, -k], [h, feedback_rate]])
        f4_cases.append({
            "label": case["label"],
            "k": k,
            "h": h,
            "feedback_product": k * h,
            "eigenvalues": [[float(v.real), float(v.imag)] for v in np.linalg.eigvals(a)],
            "stability": asymptotic_stability(a),
            **two_state_hurwitz(a),
        })
    results["F4"] = {
        "fixed_local_terms": {"plant_rate": plant, "feedback_state_rate": feedback_rate},
        "cases": f4_cases,
    }

    f5 = _family(plan, "F5")
    sim = f5["simulation"]
    f5_cases: dict[str, list[dict[str, Any]]] = {}
    for kind in f5["noise_cases"]:
        seed_records = []
        for seed in f5["seeds"]:
            r = simulate_noise_entry(
                kind,
                seed=int(seed),
                x0=f5["x0"],
                dt=float(sim["dt"]),
                steps=int(sim["steps"]),
                sigma=float(sim["sigma"]),
                feedback_k=float(sim["feedback_k"]),
                feedback_h=float(sim["feedback_h"]),
            )
            seed_records.append({
                "seed": int(seed),
                "state_rms": r.state_rms,
                "observation_rms": r.observation_rms,
                "final_state_norm": r.final_state_norm,
                "final_state": list(r.final_state),
            })
        f5_cases[kind] = seed_records
    results["F5"] = {"cases": f5_cases}

    f6 = _family(plan, "F6")
    times6 = _time_grid(f6["time_grid"])
    f6_cases = []
    for k in f6["parameter_values"]["k"]:
        kf = float(k)
        a = np.array([[-1.0, kf], [0.0, -2.0]])
        es = eigensystem(a)
        tg = max_transient_gain_upper(kf, times6)
        f6_cases.append({
            "k": kf,
            "eigenvalues": [[float(v.real), float(v.imag)] for v in np.linalg.eigvals(a)],
            "normality_defect_fro": es["normality_defect_fro"],
            **tg,
        })
    results["F6"] = {"cases": f6_cases}

    f7 = _family(plan, "F7")
    results["F7"] = exact_degenerate_mode_status(f7["matrix"])

    f8 = _family(plan, "F8")
    f8_cases: dict[str, Any] = {}
    for case in f8["cases"]:
        label = case["label"]
        if "pole" in case:
            f8_cases[label] = single_pole_chi(float(case["pole"]))
        else:
            f8_cases[label] = second_order_chi(float(case["gamma"]), float(case["kappa"]))
    results["F8"] = {"cases": f8_cases}

    return results
