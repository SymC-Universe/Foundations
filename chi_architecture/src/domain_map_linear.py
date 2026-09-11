from __future__ import annotations

import itertools
import math
from typing import Any

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import linear_sum_assignment
from scipy.sparse.linalg import expm_multiply


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


def mechanical_2dof_matrices(
    *,
    k1: float,
    k2: float,
    c1: float,
    c2: float,
    kc: float,
    cc: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    values = np.asarray([k1, k2, c1, c2, kc, cc], dtype=float)
    if not np.all(np.isfinite(values)):
        raise DomainMapRefusal("D01B parameters must be finite")
    if k1 <= 0.0 or k2 <= 0.0:
        raise DomainMapRefusal("D01B grounded stiffnesses must be positive")
    if c1 < 0.0 or c2 < 0.0 or kc < 0.0 or cc < 0.0:
        raise DomainMapRefusal("D01B passive damping/coupling parameters must be nonnegative")

    m = np.eye(2, dtype=float)
    k = np.array([[k1 + kc, -kc], [-kc, k2 + kc]], dtype=float)
    c = np.array([[c1 + cc, -cc], [-cc, c2 + cc]], dtype=float)
    a = np.block([[np.zeros((2, 2)), np.eye(2)], [-k, -c]])
    return m, c, k, a


def _sorted_eigenstructure(a: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eig(a)
    order = np.lexsort((np.imag(values), np.real(values)))
    return values[order], vectors[:, order]


def _complex_value(z: complex) -> dict[str, float]:
    return {"real": float(np.real(z)), "imag": float(np.imag(z))}


def _minimum_normalized_eigenvalue_separation(values: np.ndarray) -> float:
    vals = np.asarray(values, dtype=complex)
    if vals.size < 2:
        return float("nan")
    scale = max(1.0, float(np.max(np.abs(vals))))
    distances = [abs(vals[i] - vals[j]) for i in range(vals.size) for j in range(i + 1, vals.size)]
    return float(min(distances) / scale)


def _matched_spectral_displacement(values: np.ndarray, reference: np.ndarray) -> float:
    cost = np.abs(values[:, None] - reference[None, :])
    rows, cols = linear_sum_assignment(cost)
    matched = cost[rows, cols]
    return float(np.sqrt(np.mean(matched * matched)))


def _modal_participation(values: np.ndarray, vectors: np.ndarray) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for value, vector in zip(values, vectors.T):
        q = np.asarray(vector[:2], dtype=complex)
        weights = np.abs(q) ** 2
        denom = float(np.sum(weights))
        fractions = [None, None] if denom <= 1e-30 else [float(v / denom) for v in weights]
        out.append({
            "pole": _complex_value(complex(value)),
            "displacement_participation": fractions,
        })
    return out


def _complex_pair_damping_ratios(values: np.ndarray, imag_tol: float = 1e-10) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for value in values:
        if float(np.imag(value)) <= imag_tol:
            continue
        mag = abs(value)
        if mag <= 0.0:
            continue
        out.append({
            "positive_imaginary_pole": _complex_value(complex(value)),
            "complex_pair_damping_ratio": float(-np.real(value) / mag),
            "status": "COMPLEX_PAIR_DAMPING_RATIO_NOT_MASTER_CHI",
        })
    return out


def _exact_real_modal_scalarization(c: np.ndarray, k: np.ndarray) -> dict[str, Any]:
    commutator = c @ k - k @ c
    denom = max(1.0, float(np.linalg.norm(c, ord="fro") * np.linalg.norm(k, ord="fro")))
    commutator_norm = float(np.linalg.norm(commutator, ord="fro") / denom)
    if commutator_norm > 1e-12:
        return {
            "status": "NO_EXACT_REAL_MODAL_SCALARIZATION",
            "normalized_commutator_norm": commutator_norm,
            "modal_chi": [],
        }

    # For real symmetric commuting C and K, a generic real linear combination
    # supplies a common orthonormal eigenbasis except for unresolved numerical
    # degeneracy. The result is verified explicitly before any scalar is emitted.
    _, q = np.linalg.eigh(k + math.sqrt(2.0) * c)
    kt = q.T @ k @ q
    ct = q.T @ c @ q
    offdiag = float(
        max(
            np.linalg.norm(kt - np.diag(np.diag(kt)), ord="fro"),
            np.linalg.norm(ct - np.diag(np.diag(ct)), ord="fro"),
        )
    )
    if offdiag > 1e-10:
        return {
            "status": "COMMUTING_BUT_SIMULTANEOUS_DIAGONALIZATION_UNRESOLVED",
            "normalized_commutator_norm": commutator_norm,
            "offdiagonal_verification_norm": offdiag,
            "modal_chi": [],
        }

    km = np.real(np.diag(kt))
    cm = np.real(np.diag(ct))
    if np.any(km <= 0.0):
        return {
            "status": "INVALID_MODAL_STIFFNESS_REFUSAL",
            "normalized_commutator_norm": commutator_norm,
            "offdiagonal_verification_norm": offdiag,
            "modal_chi": [],
        }
    modal = [
        {
            "k_modal": float(kv),
            "c_modal": float(cv),
            "omega_n": float(math.sqrt(kv)),
            "chi_modal": float(cv / (2.0 * math.sqrt(kv))),
        }
        for kv, cv in zip(km, cm)
    ]
    return {
        "status": "EXACT_REAL_MODAL_SCALARIZATION_ADMISSIBLE",
        "normalized_commutator_norm": commutator_norm,
        "offdiagonal_verification_norm": offdiag,
        "modal_chi": modal,
    }


def _d01b_time_grid(execution: dict[str, Any]) -> np.ndarray:
    grid = execution.get("observation_grid", {})
    start = float(grid.get("time_start", 0.0))
    stop = float(grid.get("time_stop", 0.0))
    points = int(grid.get("time_points", 0))
    if start != 0.0 or stop <= start or points < 2:
        raise DomainMapRefusal("invalid D01B frozen observation grid")
    return np.linspace(start, stop, points)


def _response_energy_metrics(
    trajectory: np.ndarray,
    time: np.ndarray,
    *,
    k1: float,
    k2: float,
    c1: float,
    c2: float,
    kc: float,
    cc: float,
    perturbed_component: int,
) -> dict[str, Any]:
    q1 = trajectory[:, 0]
    q2 = trajectory[:, 1]
    v1 = trajectory[:, 2]
    v2 = trajectory[:, 3]

    e1 = 0.5 * v1 * v1 + 0.5 * k1 * q1 * q1
    e2 = 0.5 * v2 * v2 + 0.5 * k2 * q2 * q2
    ec = 0.5 * kc * (q1 - q2) ** 2
    et = e1 + e2 + ec
    e0 = float(et[0])
    if not math.isfinite(e0) or e0 <= 1e-15:
        raise DomainMapRefusal("declared D01B perturbation must have positive initial energy")

    local_diss = c1 * v1 * v1 + c2 * v2 * v2
    coupling_diss = cc * (v1 - v2) ** 2
    total_diss = local_diss + coupling_diss
    cumulative = np.concatenate(([0.0], cumulative_trapezoid(total_diss, time)))
    residual = np.abs(et + cumulative - e0) / e0
    norm = np.sqrt(np.maximum(et, 0.0) / e0)
    settling = _settling_tau(time, norm, fraction=0.02)

    receiver = e2 if perturbed_component == 1 else e1
    receiver_index = 2 if perturbed_component == 1 else 1
    peak_receiver_idx = int(np.argmax(receiver))
    peak_gain_idx = int(np.argmax(et / e0))

    return {
        "initial_total_energy": e0,
        "final_total_energy_fraction": float(et[-1] / e0),
        "max_transient_energy_gain": float(np.max(et / e0)),
        "max_transient_energy_gain_time": float(time[peak_gain_idx]),
        "settling_time_2pct": settling,
        "settling_status": "SETTLED_WITHIN_FIXED_WINDOW" if settling is not None else "NOT_SETTLED_WITHIN_FIXED_WINDOW",
        "state_norm_integral": float(np.trapezoid(norm, time)),
        "receiving_component": receiver_index,
        "receiving_component_peak_energy_fraction": float(receiver[peak_receiver_idx] / e0),
        "receiving_component_peak_time": float(time[peak_receiver_idx]),
        "coupling_spring_peak_energy_fraction": float(np.max(ec) / e0),
        "coupling_dissipation_fraction": float(np.trapezoid(coupling_diss, time) / e0),
        "local_dissipation_fraction": float(np.trapezoid(local_diss, time) / e0),
        "maximum_energy_balance_residual_fraction": float(np.max(residual)),
    }


def iter_d01b_parameter_cases(plan: dict[str, Any]) -> list[dict[str, float]]:
    if plan.get("schema") != "domain-chi-map-plan-v0.1" or plan.get("domain_id") != "D01_LINEAR_DYNAMICS":
        raise DomainMapRefusal("D01B requires the frozen D01 domain plan v0.1")
    phase = next((p for p in plan.get("phases", []) if p.get("id") == "D01B_COUPLED_2DOF"), None)
    if phase is None:
        raise DomainMapRefusal("missing D01B phase")
    grid = phase["parameter_grid"]
    names = ["k1", "k2", "local_damping_c1", "local_damping_c2", "coupling_stiffness_kc", "coupling_damping_cc"]
    values = [grid[name] for name in names]
    cases: list[dict[str, float]] = []
    for combo in itertools.product(*values):
        cases.append({name: float(value) for name, value in zip(names, combo)})
    return cases


def evaluate_d01b_case(
    params: dict[str, float],
    perturbations: list[dict[str, Any]],
    execution: dict[str, Any],
) -> dict[str, Any]:
    k1 = float(params["k1"])
    k2 = float(params["k2"])
    c1 = float(params["local_damping_c1"])
    c2 = float(params["local_damping_c2"])
    kc = float(params["coupling_stiffness_kc"])
    cc = float(params["coupling_damping_cc"])

    _, c, k, a = mechanical_2dof_matrices(k1=k1, k2=k2, c1=c1, c2=c2, kc=kc, cc=cc)
    values, vectors = _sorted_eigenstructure(a)
    _, _, _, a0 = mechanical_2dof_matrices(k1=k1, k2=k2, c1=c1, c2=c2, kc=0.0, cc=0.0)
    reference_values, _ = _sorted_eigenstructure(a0)

    spectral_abscissa = float(np.max(np.real(values)))
    stable = bool(spectral_abscissa < -1e-10)
    local_chi1 = float(c1 / (2.0 * math.sqrt(k1)))
    local_chi2 = float(c2 / (2.0 * math.sqrt(k2)))

    time = _d01b_time_grid(execution)
    initial_columns: list[np.ndarray] = []
    perturbed_components: list[int] = []
    for perturbation in perturbations:
        q0 = np.asarray(perturbation["q0"], dtype=float)
        v0 = np.asarray(perturbation["qdot0"], dtype=float)
        if q0.shape != (2,) or v0.shape != (2,) or not np.all(np.isfinite(np.r_[q0, v0])):
            raise DomainMapRefusal("invalid D01B perturbation")
        initial_columns.append(np.r_[q0, v0])
        if perturbation.get("meaning") == "perturb_component_1":
            perturbed_components.append(1)
        elif perturbation.get("meaning") == "perturb_component_2":
            perturbed_components.append(2)
        else:
            raise DomainMapRefusal("D01B perturbation meaning must identify the perturbed component")

    b = np.column_stack(initial_columns)
    trajectories = expm_multiply(
        a,
        b,
        start=float(time[0]),
        stop=float(time[-1]),
        num=int(time.size),
        endpoint=True,
        traceA=float(np.trace(a)),
    )

    response_records = []
    for index, perturbation in enumerate(perturbations):
        trajectory = np.asarray(np.real_if_close(trajectories[:, :, index]), dtype=float)
        metrics = _response_energy_metrics(
            trajectory,
            time,
            k1=k1,
            k2=k2,
            c1=c1,
            c2=c2,
            kc=kc,
            cc=cc,
            perturbed_component=perturbed_components[index],
        )
        response_records.append({
            "perturbation_index": index,
            "meaning": perturbation["meaning"],
            **metrics,
        })

    return {
        "parameters": {
            "k1": k1,
            "k2": k2,
            "c1": c1,
            "c2": c2,
            "kc": kc,
            "cc": cc,
        },
        "isolated_component_coordinates": {
            "chi1": local_chi1,
            "chi2": local_chi2,
            "status": "ISOLATED_COMPONENT_CHI_NOT_SYSTEM_CHI",
        },
        "asymptotic_stability": stable,
        "spectral_abscissa": spectral_abscissa,
        "poles": [_complex_value(complex(v)) for v in values],
        "minimum_normalized_eigenvalue_separation": _minimum_normalized_eigenvalue_separation(values),
        "state_eigenvector_condition_number": float(np.linalg.cond(vectors)),
        "spectral_displacement_from_uncoupled_rms": _matched_spectral_displacement(values, reference_values),
        "modal_participation": _modal_participation(values, vectors),
        "complex_pair_damping_ratios": _complex_pair_damping_ratios(values),
        "exact_real_modal_scalarization": _exact_real_modal_scalarization(c, k),
        "responses": response_records,
    }


def run_d01b(plan: dict[str, Any], execution: dict[str, Any]) -> dict[str, Any]:
    if execution.get("schema") != "d01b-execution-freeze-v0.1":
        raise DomainMapRefusal("D01B requires execution freeze v0.1")
    if execution.get("parent_plan") != "D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json":
        raise DomainMapRefusal("D01B execution freeze does not point to the expected parent plan")
    if execution.get("scientific_parameter_source") != "parent_plan_only" or execution.get("parameter_overrides") is not False:
        raise DomainMapRefusal("D01B execution freeze may not override the parent scientific grid")

    phase = next((p for p in plan.get("phases", []) if p.get("id") == "D01B_COUPLED_2DOF"), None)
    if phase is None:
        raise DomainMapRefusal("missing D01B phase")
    perturbations = phase["perturbations"]
    cases = iter_d01b_parameter_cases(plan)
    records = [evaluate_d01b_case(params, perturbations, execution) for params in cases]

    return {
        "domain_id": "D01_LINEAR_DYNAMICS",
        "phase_id": "D01B_COUPLED_2DOF",
        "status": "P0_DOMAIN_MAP_COUPLED_MECHANICAL",
        "atlas_blind": True,
        "cross_domain_confirmation": False,
        "known_context_before_execution": ["NSD_P0D14", "NSD_P0D15", "NSD_P0D16", "NSD_P0D17", "NSD_P0D19"],
        "scientific_parameter_source": "D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json",
        "execution_freeze": "D01B_EXECUTION_FREEZE_v0.1.json",
        "master_scalar_predeclared": False,
        "parameter_case_count": len(cases),
        "perturbation_count_per_case": len(perturbations),
        "records": records,
        "interpretation_ceiling": (
            "Within-domain P0 mechanical Function/Limit mapping only. Already-viewed NSD feedback results are known context, "
            "not independent confirmation. Any compression proposed after this output is discovery-only."
        ),
    }
