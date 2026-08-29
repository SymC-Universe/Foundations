#!/usr/bin/env python3
import json
import math
import platform
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "conditional_tangent_audit_v01.json"

ETA = 0.73
KAPPA = 0.41
OMEGA = 1.17
GAMMA = 0.23
DTS = [1e-4, 3e-5, 1e-5]
DW_COEFFS = [0.37, -0.61]
EPSILONS = [1e-4, 1e-5]
FD_GATE = 1e-7
TRACE_GATE = 5e-12
CHI_GATE = 1e-14

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
ident = np.eye(2, dtype=complex)
sm = np.array([[0, 1], [0, 0]], dtype=complex)

xop = 0.5 * sz
hamiltonian = 0.5 * OMEGA * sy
collapse = math.sqrt(GAMMA) * sm

rho = 0.5 * (ident + 0.20 * sx - 0.25 * sy + 0.30 * sz)
delta = 0.5 * (-0.13 * sx + 0.21 * sy + 0.17 * sz)


def comm(a, b):
    return a @ b - b @ a


def dissipator(c, state):
    cd = c.conj().T
    cdc = cd @ c
    return c @ state @ cd - 0.5 * (cdc @ state + state @ cdc)


def liouvillian(state):
    return (
        -1j * comm(hamiltonian, state)
        + dissipator(collapse, state)
        + 2.0 * KAPPA * dissipator(xop, state)
    )


def mu(state):
    return float(np.trace(xop @ state).real)


def h_super(state):
    m = mu(state)
    return xop @ state + state @ xop - 2.0 * m * state


def delta_h(state, perturbation):
    dm = float(np.trace(xop @ perturbation).real)
    return (
        xop @ perturbation
        + perturbation @ xop
        - 2.0 * mu(state) * perturbation
        - 2.0 * dm * state
    )


def fro(a):
    return float(np.linalg.norm(a, ord="fro"))


def same_noise_map(state, dt, dw):
    amp = math.sqrt(2.0 * ETA * KAPPA)
    return state + liouvillian(state) * dt + amp * h_super(state) * dw


def same_record_map(state, dt, dy):
    amp = math.sqrt(2.0 * ETA * KAPPA)
    obs = math.sqrt(8.0 * ETA * KAPPA)
    innovation = dy - obs * mu(state) * dt
    return state + liouvillian(state) * dt + amp * h_super(state) * innovation


def block_chi(a):
    a = np.asarray(a)
    if a.shape != (2, 2) or np.max(np.abs(a.imag)) > 1e-14:
        return None
    ar = a.real
    tr = float(np.trace(ar))
    det = float(np.linalg.det(ar))
    if tr >= 0.0 or det <= 0.0:
        return None
    return -tr / (2.0 * math.sqrt(det))


criteria = {}

# T0: trace preservation and valid base state.
trace_items = {
    "initial_delta_trace": abs(complex(np.trace(delta))),
    "L_delta_trace": abs(complex(np.trace(liouvillian(delta)))),
    "deltaH_trace": abs(complex(np.trace(delta_h(rho, delta)))),
    "H_rho_trace": abs(complex(np.trace(h_super(rho)))),
}
base_eigs = np.linalg.eigvalsh(rho)
t0_pass = (
    trace_items["initial_delta_trace"] <= 1e-14
    and max(trace_items.values()) <= TRACE_GATE
    and float(np.min(base_eigs)) > 0.0
)
criteria["T0"] = {
    "status": "PASS" if t0_pass else "FAIL",
    "trace_residuals": {k: float(v) for k, v in trace_items.items()},
    "base_rho_eigenvalues": [float(v) for v in base_eigs],
}

# T1/T2: finite-difference checks of the registered first variations.
amp = math.sqrt(2.0 * ETA * KAPPA)
obs = math.sqrt(8.0 * ETA * KAPPA)
dm = float(np.trace(xop @ delta).real)

same_noise_rows = []
same_record_rows = []
for dt in DTS:
    for coeff in DW_COEFFS:
        dw = coeff * math.sqrt(dt)
        analytic_noise = delta + liouvillian(delta) * dt + amp * delta_h(rho, delta) * dw

        dy = obs * mu(rho) * dt + dw
        analytic_record = (
            delta
            + liouvillian(delta) * dt
            + amp * delta_h(rho, delta) * dw
            - 4.0 * ETA * KAPPA * dm * h_super(rho) * dt
        )

        noise_errors = {}
        record_errors = {}
        for eps in EPSILONS:
            fd_noise = (same_noise_map(rho + eps * delta, dt, dw) - same_noise_map(rho, dt, dw)) / eps
            fd_record = (same_record_map(rho + eps * delta, dt, dy) - same_record_map(rho, dt, dy)) / eps
            noise_errors[f"{eps:.0e}"] = fro(fd_noise - analytic_noise)
            record_errors[f"{eps:.0e}"] = fro(fd_record - analytic_record)

        same_noise_rows.append({
            "dt": dt,
            "dw_over_sqrt_dt": coeff,
            "errors": noise_errors,
            "fine_below_gate": noise_errors["1e-05"] <= FD_GATE,
            "improves_with_epsilon": noise_errors["1e-05"] < noise_errors["1e-04"],
        })
        same_record_rows.append({
            "dt": dt,
            "dw_over_sqrt_dt": coeff,
            "errors": record_errors,
            "fine_below_gate": record_errors["1e-05"] <= FD_GATE,
            "improves_with_epsilon": record_errors["1e-05"] < record_errors["1e-04"],
        })


t1_pass = all(r["fine_below_gate"] and r["improves_with_epsilon"] for r in same_noise_rows)
t2_pass = all(r["fine_below_gate"] and r["improves_with_epsilon"] for r in same_record_rows)
criteria["T1"] = {
    "status": "PASS" if t1_pass else "FAIL",
    "max_fine_error": max(r["errors"]["1e-05"] for r in same_noise_rows),
    "rows": same_noise_rows,
}
criteria["T2"] = {
    "status": "PASS" if t2_pass else "FAIL",
    "max_fine_error": max(r["errors"]["1e-05"] for r in same_record_rows),
    "rows": same_record_rows,
}

# T3: exact reduction to ordinary second-order damping ratio.
oscillator_cases = [(1.0, 1.0, 0.6), (2.3, 0.7, 1.4), (0.4, 2.1, 5.0)]
chi_rows = []
for mass, omega, gamma in oscillator_cases:
    a = np.array([[0.0, 1.0 / mass], [-mass * omega * omega, -gamma]], dtype=float)
    measured = block_chi(a)
    expected = gamma / (2.0 * omega)
    err = abs(measured - expected) if measured is not None else float("inf")
    chi_rows.append({
        "m": mass,
        "Omega": omega,
        "Gamma": gamma,
        "chi_block": measured,
        "chi_expected": expected,
        "abs_error": err,
    })
t3_pass = all(r["abs_error"] <= CHI_GATE for r in chi_rows)
criteria["T3"] = {
    "status": "PASS" if t3_pass else "FAIL",
    "max_abs_error": max(r["abs_error"] for r in chi_rows),
    "rows": chi_rows,
}

# T4: registered refusal controls.
refusal_controls = [
    np.diag([1.0, -2.0]),
    np.array([[0.0, 1.0], [1.0, -1.0]], dtype=float),
]
refusal_rows = []
for idx, a in enumerate(refusal_controls, start=1):
    val = block_chi(a)
    refusal_rows.append({
        "control": idx,
        "trace": float(np.trace(a)),
        "determinant": float(np.linalg.det(a)),
        "result": "REFUSE" if val is None else float(val),
    })
t4_pass = all(r["result"] == "REFUSE" for r in refusal_rows)
criteria["T4"] = {
    "status": "PASS" if t4_pass else "FAIL",
    "rows": refusal_rows,
}

overall = all(v["status"] == "PASS" for v in criteria.values())
payload = {
    "schema": "stability-arc-conditional-tangent-audit-v0.1",
    "overall_status": "PASS" if overall else "FAIL",
    "interpretation": "DERIVATION_AUDIT_ONLY",
    "parameters": {
        "eta": ETA,
        "kappa": KAPPA,
        "omega": OMEGA,
        "gamma": GAMMA,
        "dt": DTS,
        "dw_over_sqrt_dt": DW_COEFFS,
        "finite_difference_epsilons": EPSILONS,
    },
    "criteria": criteria,
    "environment": {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "platform": platform.platform(),
    },
}
OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(payload, indent=2, sort_keys=True))
raise SystemExit(0 if overall else 1)
