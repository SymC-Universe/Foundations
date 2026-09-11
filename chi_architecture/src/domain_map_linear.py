from __future__ import annotations

import math
from typing import Any

import numpy as np


class DomainMapRefusal(ValueError):
    """Fail-closed refusal for invalid domain-map inputs."""


def _validate_grid(tau: np.ndarray) -> np.ndarray:
    arr = np.asarray(tau, dtype=float)
    if arr.ndim != 1 or arr.size < 2:
        raise DomainMapRefusal("tau must be a one-dimensional grid with at least two points")
    if not np.all(np.isfinite(arr)) or np.any(arr < 0.0) or np.any(np.diff(arr) <= 0.0):
        raise DomainMapRefusal("tau must be finite, nonnegative, and strictly increasing")
    return arr


def normalized_sdof_trajectory(
    chi: float,
    tau: np.ndarray,
    *,
    x0: float,
    u0: float,
    critical_tol: float = 1e-12,
) -> tuple[np.ndarray, np.ndarray]:
    """Exact solution of x'' + 2 chi x' + x = 0 in normalized time tau.

    u is dx/dtau. This function is intentionally expressed in normalized
    coordinates so the coordinate-sufficiency test can compare physical
    omega0/gamma pairs at fixed chi without smuggling omega0 into the shape.
    """
    if not math.isfinite(chi) or chi < 0.0:
        raise DomainMapRefusal("D01A passive anchor requires finite chi >= 0")
    if not math.isfinite(x0) or not math.isfinite(u0):
        raise DomainMapRefusal("initial conditions must be finite")
    t = _validate_grid(tau)

    if abs(chi - 1.0) <= critical_tol:
        a = float(x0)
        b = float(u0 + x0)
        e = np.exp(-t)
        x = (a + b * t) * e
        u = (b - a - b * t) * e
        return x, u

    if chi < 1.0:
        wd = math.sqrt(1.0 - chi * chi)
        a = float(x0)
        b = float((u0 + chi * x0) / wd)
        c = np.cos(wd * t)
        s = np.sin(wd * t)
        e = np.exp(-chi * t)
        core = a * c + b * s
        core_dot = -a * wd * s + b * wd * c
        x = e * core
        u = e * (core_dot - chi * core)
        return x, u

    root = math.sqrt(chi * chi - 1.0)
    r1 = -chi + root
    r2 = -chi - root
    denom = r1 - r2
    a = (u0 - r2 * x0) / denom
    b = (r1 * x0 - u0) / denom
    e1 = np.exp(r1 * t)
    e2 = np.exp(r2 * t)
    x = a * e1 + b * e2
    u = a * r1 * e1 + b * r2 * e2
    return x, u


def physical_sdof_from_chi(
    omega0: float,
    chi: float,
    tau: np.ndarray,
    *,
    x0: float,
    normalized_u0: float,
) -> dict[str, Any]:
    """Construct the physical parameter pair and map it back to normalized form."""
    if not math.isfinite(omega0) or omega0 <= 0.0:
        raise DomainMapRefusal("omega0 must be finite and positive")
    if not math.isfinite(chi) or chi < 0.0:
        raise DomainMapRefusal("chi must be finite and nonnegative")
    tnorm = _validate_grid(tau)
    gamma = 2.0 * chi * omega0
    physical_t = tnorm / omega0
    x, u = normalized_sdof_trajectory(chi, tnorm, x0=x0, u0=normalized_u0)
    physical_v = omega0 * u
    return {
        "omega0": float(omega0),
        "gamma": float(gamma),
        "chi": float(chi),
        "physical_time": physical_t,
        "x": x,
        "physical_velocity": physical_v,
        "normalized_velocity": physical_v / omega0,
    }


def _first_zero_crossing(tau: np.ndarray, x: np.ndarray) -> float | None:
    eps = 1e-14
    for i in range(1, x.size):
        a = float(x[i - 1])
        b = float(x[i])
        if abs(a) <= eps and i - 1 > 0:
            return float(tau[i - 1])
        if a * b < 0.0:
            frac = abs(a) / (abs(a) + abs(b))
            return float(tau[i - 1] + frac * (tau[i] - tau[i - 1]))
    return None


def _zero_crossing_count(x: np.ndarray) -> int:
    eps = 1e-12
    signs = np.sign(np.where(np.abs(x) <= eps, 0.0, x))
    last = 0.0
    count = 0
    for s in signs:
        if s == 0.0:
            continue
        if last != 0.0 and s != last:
            count += 1
        last = s
    return count


def _settling_tau(tau: np.ndarray, state_norm: np.ndarray, fraction: float = 0.02) -> float | None:
    initial = float(state_norm[0])
    if initial <= 0.0:
        return 0.0
    threshold = fraction * initial
    above = np.flatnonzero(state_norm > threshold)
    if above.size == 0:
        return float(tau[0])
    last = int(above[-1])
    if last >= tau.size - 1:
        return None
    return float(tau[last + 1])


def normalized_sdof_metrics(
    chi: float,
    tau: np.ndarray,
    *,
    x0: float,
    u0: float,
) -> dict[str, Any]:
    t = _validate_grid(tau)
    x, u = normalized_sdof_trajectory(chi, t, x0=x0, u0=u0)
    energy = 0.5 * (x * x + u * u)
    state_norm = np.sqrt(x * x + u * u)
    disc = chi * chi - 1.0
    if abs(disc) <= 1e-12:
        regime = "CRITICAL"
        slow_decay = 1.0
    elif disc < 0.0:
        regime = "UNDERDAMPED"
        slow_decay = chi
    else:
        regime = "OVERDAMPED"
        slow_decay = chi - math.sqrt(chi * chi - 1.0)

    return {
        "chi": float(chi),
        "regime": regime,
        "root_discriminant": float(disc),
        "slowest_dimensionless_decay_rate": float(slow_decay),
        "zero_crossing_count": _zero_crossing_count(x),
        "first_zero_crossing_tau": _first_zero_crossing(t, x),
        "settling_tau_2pct": _settling_tau(t, state_norm),
        "integral_abs_x_dtau": float(np.trapezoid(np.abs(x), t)),
        "integral_x2_dtau": float(np.trapezoid(x * x, t)),
        "integral_energy_dtau": float(np.trapezoid(energy, t)),
        "max_abs_u": float(np.max(np.abs(u))),
        "final_state_norm": float(state_norm[-1]),
    }


def run_d01a(plan: dict[str, Any]) -> dict[str, Any]:
    if plan.get("schema") != "domain-chi-map-plan-v0.1":
        raise DomainMapRefusal("D01 runner requires domain map plan v0.1")
    if plan.get("domain_id") != "D01_LINEAR_DYNAMICS":
        raise DomainMapRefusal("unexpected domain id")

    phase = next((p for p in plan.get("phases", []) if p.get("id") == "D01A_SDOF_SCALE_COLLAPSE"), None)
    if phase is None:
        raise DomainMapRefusal("missing D01A phase")
    grid = phase["parameter_grid"]
    start = float(grid["chi_start"])
    stop = float(grid["chi_stop"])
    step = float(grid["chi_step"])
    if step <= 0.0 or stop < start:
        raise DomainMapRefusal("invalid chi grid")
    n = int(round((stop - start) / step))
    chi_values = np.round(start + step * np.arange(n + 1), 12)
    if abs(float(chi_values[-1]) - stop) > 1e-9:
        raise DomainMapRefusal("chi grid does not land on declared stop")

    tau = np.linspace(float(grid["tau_start"]), float(grid["tau_stop"]), int(grid["tau_points"]))
    omega_values = [float(v) for v in grid["omega0"]]

    records: list[dict[str, Any]] = []
    collapse: list[dict[str, Any]] = []

    for ic_index, ic in enumerate(grid["normalized_initial_conditions"]):
        x0 = float(ic["x0"])
        u0 = float(ic["u0"])
        for chi in chi_values:
            metrics = normalized_sdof_metrics(float(chi), tau, x0=x0, u0=u0)
            traces = []
            for omega0 in omega_values:
                physical = physical_sdof_from_chi(omega0, float(chi), tau, x0=x0, normalized_u0=u0)
                traces.append((physical["x"], physical["normalized_velocity"]))
            ref_x, ref_u = traces[0]
            max_dx = max(float(np.max(np.abs(x - ref_x))) for x, _ in traces[1:]) if len(traces) > 1 else 0.0
            max_du = max(float(np.max(np.abs(u - ref_u))) for _, u in traces[1:]) if len(traces) > 1 else 0.0
            collapse.append({
                "initial_condition_index": ic_index,
                "chi": float(chi),
                "max_abs_normalized_x_difference_across_omega0": max_dx,
                "max_abs_normalized_u_difference_across_omega0": max_du,
            })
            records.append({
                "initial_condition_index": ic_index,
                **metrics,
            })

    return {
        "domain_id": "D01_LINEAR_DYNAMICS",
        "phase_id": "D01A_SDOF_SCALE_COLLAPSE",
        "status": "P0_DOMAIN_MAP_EXACT_ANCHOR",
        "atlas_blind": True,
        "cross_domain_confirmation": False,
        "chi_grid": [float(v) for v in chi_values],
        "omega0_values": omega_values,
        "normalized_initial_conditions": grid["normalized_initial_conditions"],
        "records": records,
        "scale_collapse": collapse,
    }
