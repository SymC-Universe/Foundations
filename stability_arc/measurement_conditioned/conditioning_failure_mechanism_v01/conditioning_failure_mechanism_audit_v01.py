#!/usr/bin/env python3
import json
import math
import platform
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "conditioning_failure_mechanism_audit_v01.json"

SEED = 2026082903
ETA_LEVELS = [1e-3, 1e-4, 1e-5]
N_PER_SIGN = 64
MAX_CANDIDATES = 100000
S_CUT = 0.10
DARK_TOL = 5e-10
LIFT_TOL = 5e-12
FINE_RESID_TOL = 0.01
FINE_MEDIAN_TOL = 1e-3
NULL_TOL = 1e-10

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
ident2 = np.eye(2, dtype=complex)
sm = np.array([[0, 1], [0, 0]], dtype=complex)
xop = 0.5 * sz
BASIS = [0.5 * sx, 0.5 * sy, 0.5 * sz]
PAULI = [sx, sy, sz]

DUP = np.array(
    [[1.0, 0.0, 0.0],
     [0.0, 1.0, 0.0],
     [0.0, 1.0, 0.0],
     [0.0, 0.0, 1.0]], dtype=float)
ELIM = np.array(
    [[1.0, 0.0, 0.0, 0.0],
     [0.0, 0.5, 0.5, 0.0],
     [0.0, 0.0, 0.0, 1.0]], dtype=float)
SYM_BASIS = [
    np.array([[1.0, 0.0], [0.0, 0.0]], dtype=float),
    np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float),
    np.array([[0.0, 0.0], [0.0, 1.0]], dtype=float),
]


def max_abs(x):
    a = np.asarray(x)
    return 0.0 if a.size == 0 else float(np.max(np.abs(a)))


def comm(a, b):
    return a @ b - b @ a


def dissipator(c, state):
    cd = c.conj().T
    cdc = cd @ c
    return c @ state @ cd - 0.5 * (cdc @ state + state @ cdc)


def rho_from_bloch(v):
    return 0.5 * (ident2 + v[0] * sx + v[1] * sy + v[2] * sz)


def mu(state):
    return float(np.trace(xop @ state).real)


def h_super(state):
    return xop @ state + state @ xop - 2.0 * mu(state) * state


def delta_h(state, perturbation):
    dm = float(np.trace(xop @ perturbation).real)
    return xop @ perturbation + perturbation @ xop - 2.0 * mu(state) * perturbation - 2.0 * dm * state


def liouvillian(state, gamma, kappa, omega):
    H = 0.5 * omega * sy
    c = math.sqrt(gamma) * sm
    return -1j * comm(H, state) + dissipator(c, state) + 2.0 * kappa * dissipator(xop, state)


def coords(operator):
    vals = [complex(np.trace(p @ operator)) for p in PAULI]
    if max(abs(v.imag) for v in vals) > 1e-11:
        raise ValueError("non-real Bloch coordinate")
    return np.array([v.real for v in vals], dtype=float)


def linear_matrix(action):
    return np.column_stack([coords(action(e)) for e in BASIS])


def reconstruct(f, eta):
    state = rho_from_bloch(f["base"])
    Aphys = linear_matrix(lambda e: liouvillian(e, f["gamma"], f["kappa"], f["omega"]))
    amp = math.sqrt(2.0 * eta * f["kappa"])
    B = amp * linear_matrix(lambda e: delta_h(state, e))
    h = coords(h_super(state))
    Vt = np.array([[float(np.trace(xop @ e).real) for e in BASIS]], dtype=float)
    U = -4.0 * eta * f["kappa"] * h.reshape(-1, 1)
    Arec = Aphys + U @ Vt
    return state, Aphys, Arec, B, Vt


def observability_dark(A, Vt):
    O = np.vstack([Vt, Vt @ A, Vt @ A @ A])
    _, s, vh = np.linalg.svd(O, full_matrices=True)
    rank = int(np.sum(s > NULL_TOL))
    D = vh[rank:].T.copy()
    if D.size:
        D, _ = np.linalg.qr(D)
    return s, D


def orth_complement(D, n):
    if D.shape[1] == 0:
        return np.eye(n)
    _, _, vh = np.linalg.svd(D.T, full_matrices=True)
    return vh[D.shape[1]:].T.copy()


def moment_action(A, B, P):
    return A @ P + P @ A.T + B @ P @ B.T


def sym_coords(P):
    return np.array([P[0, 0], 0.5 * (P[0, 1] + P[1, 0]), P[1, 1]], dtype=float)


def sym_generator(A, B):
    return np.column_stack([sym_coords(moment_action(A, B, E)) for E in SYM_BASIS])


def sym_generator_kron(A, B):
    K = np.kron(np.eye(2), A) + np.kron(A, np.eye(2)) + np.kron(B, B)
    return ELIM @ K @ DUP


def alpha(G):
    return float(np.max(np.real(np.linalg.eigvals(G))))


def predictor_S(gamma, kappa, omega, x, z):
    delta = gamma / 2.0 - kappa
    D = delta * delta - 4.0 * omega * omega
    if not (delta > 0.0 and D > 0.0):
        raise ValueError("fixture outside registered perturbative branch")
    c = 1.0 - z * z
    return -c + (c * delta - 2.0 * omega * x * z) / math.sqrt(D)


def generate_panel():
    rng = np.random.default_rng(SEED)
    positive = []
    negative = []
    rejected_near_zero = 0
    n_candidates = 0
    while (len(positive) < N_PER_SIGN or len(negative) < N_PER_SIGN) and n_candidates < MAX_CANDIDATES:
        n_candidates += 1
        gamma = float(10.0 ** rng.uniform(-1.0, 0.5))
        rk = float(rng.uniform(0.02, 0.35))
        kappa = rk * gamma
        delta = gamma * (0.5 - rk)
        rho = float(rng.uniform(0.20, 0.80))
        omega = rho * delta / 2.0
        direction = rng.normal(size=3)
        direction = direction / np.linalg.norm(direction)
        radius = float(rng.uniform(0.20, 0.95))
        base = radius * direction
        S = predictor_S(gamma, kappa, omega, float(base[0]), float(base[2]))
        raw = {
            "candidate_index": n_candidates,
            "gamma": gamma,
            "kappa": kappa,
            "omega": omega,
            "rk": rk,
            "rho": rho,
            "base": [float(v) for v in base],
            "S": S,
            "predictor_2S": 2.0 * S,
        }
        if S >= S_CUT and len(positive) < N_PER_SIGN:
            raw["id"] = f"P{len(positive)+1:03d}"
            raw["sign_group"] = "POSITIVE_S"
            positive.append(raw)
        elif S <= -S_CUT and len(negative) < N_PER_SIGN:
            raw["id"] = f"N{len(negative)+1:03d}"
            raw["sign_group"] = "NEGATIVE_S"
            negative.append(raw)
        else:
            rejected_near_zero += 1
    return positive + negative, n_candidates, rejected_near_zero


def panel_signature(panel):
    return json.dumps(panel, sort_keys=True, separators=(",", ":"))


panel_a, candidates_a, rejected_a = generate_panel()
panel_b, candidates_b, rejected_b = generate_panel()
F0 = (
    len(panel_a) == 2 * N_PER_SIGN
    and sum(f["sign_group"] == "POSITIVE_S" for f in panel_a) == N_PER_SIGN
    and sum(f["sign_group"] == "NEGATIVE_S" for f in panel_a) == N_PER_SIGN
    and panel_signature(panel_a) == panel_signature(panel_b)
    and candidates_a == candidates_b
    and rejected_a == rejected_b
)

records = []
quotient_ok = True
lift_ok = True
for f in panel_a:
    level_records = []
    for eta in ETA_LEVELS:
        state, Aphys, Arec, B, Vt = reconstruct(f, eta)
        rho_min = float(np.min(np.linalg.eigvalsh(state)))
        svals, D = observability_dark(Aphys, Vt)
        reasons = []
        if rho_min <= 0.0:
            reasons.append("NONPOSITIVE_DENSITY")
        if D.shape[1] != 1:
            reasons.append("DARK_DIMENSION")

        dark_res = None
        inter = None
        if D.shape[1] == 1:
            C = orth_complement(D, 3)
            Pperp = np.eye(3) - D @ D.T
            dark_res = {
                "measurement": max_abs(Vt @ D),
                "Aphys": max_abs(Pperp @ Aphys @ D),
                "Arec": max_abs(Pperp @ Arec @ D),
                "B": max_abs(Pperp @ B @ D),
            }
            if max(dark_res.values()) > DARK_TOL:
                reasons.append("DARK_INVARIANCE")

            L = C.T
            Aqp = L @ Aphys @ C
            Aqr = L @ Arec @ C
            Bq = L @ B @ C
            inter = {
                "phys_A": max_abs(L @ Aphys - Aqp @ L),
                "record_A": max_abs(L @ Arec - Aqr @ L),
                "B": max_abs(L @ B - Bq @ L),
            }
            if max(inter.values()) > DARK_TOL:
                reasons.append("QUOTIENT_INTERTWINING")

            Gp = sym_generator(Aqp, Bq)
            Gr = sym_generator(Aqr, Bq)
            lift_error = max(
                max_abs(Gp - sym_generator_kron(Aqp, Bq)),
                max_abs(Gr - sym_generator_kron(Aqr, Bq)),
            )
            if lift_error > LIFT_TOL:
                reasons.append("MOMENT_LIFT")
                lift_ok = False

            ap = alpha(Gp)
            ar = alpha(Gr)
            q = eta * f["kappa"]
            da = ar - ap
            slope = da / q
            residual = abs(slope - f["predictor_2S"])
            sign_agree = (da > 0.0 and f["S"] > 0.0) or (da < 0.0 and f["S"] < 0.0)
        else:
            lift_error = None
            ap = ar = q = da = slope = residual = None
            sign_agree = False

        admitted = len(reasons) == 0
        if not admitted:
            quotient_ok = False
        level_records.append({
            "eta": eta,
            "admitted": admitted,
            "reasons": reasons,
            "rho_min_eigenvalue": rho_min,
            "observability_singular_values": [float(v) for v in svals],
            "dark_residuals": dark_res,
            "intertwining_residuals": inter,
            "lift_error": lift_error,
            "q": q,
            "alpha_phys": ap,
            "alpha_rec": ar,
            "delta_alpha": da,
            "slope": slope,
            "predictor_2S": f["predictor_2S"],
            "slope_residual": residual,
            "sign_agree": sign_agree,
        })
    records.append({
        "id": f["id"],
        "sign_group": f["sign_group"],
        "candidate_index": f["candidate_index"],
        "parameters": {k: v for k, v in f.items() if k not in ("id", "sign_group", "candidate_index")},
        "levels": level_records,
    })

F1 = quotient_ok and len(records) == 128 and all(all(l["admitted"] for l in r["levels"]) for r in records)
F2 = lift_ok and all(all(l["lift_error"] is not None and l["lift_error"] <= LIFT_TOL for l in r["levels"]) for r in records)

fine_index = ETA_LEVELS.index(1e-5)
sign_failures = [r["id"] for r in records if not r["levels"][fine_index]["sign_agree"]]
F3 = len(sign_failures) == 0

magnitude_failures = [r["id"] for r in records if r["levels"][fine_index]["slope_residual"] > FINE_RESID_TOL]
F4 = len(magnitude_failures) == 0

group_medians = {}
F5 = True
for group in ["POSITIVE_S", "NEGATIVE_S"]:
    subset = [r for r in records if r["sign_group"] == group]
    medians = []
    for j, eta in enumerate(ETA_LEVELS):
        med = float(np.median([r["levels"][j]["slope_residual"] for r in subset]))
        medians.append(med)
    group_medians[group] = {str(ETA_LEVELS[j]): medians[j] for j in range(len(ETA_LEVELS))}
    if not (medians[0] > medians[1] > medians[2] and medians[2] <= FINE_MEDIAN_TOL):
        F5 = False

if not F0:
    status = "GENERATOR_HOLD"
elif not F1:
    status = "QUOTIENT_HOLD"
elif not F2:
    status = "AUDIT_FAILURE"
elif F3 and F4 and F5:
    status = "PASS_PROSPECTIVE_FAILURE_MECHANISM"
else:
    status = "FAIL_PROSPECTIVE_FAILURE_MECHANISM"

criteria = {
    "F0": {"status": "PASS" if F0 else "FAIL", "seed": SEED, "accepted": len(panel_a), "candidates_examined": candidates_a, "near_zero_or_full_group_skips": rejected_a},
    "F1": {"status": "PASS" if F1 else "FAIL"},
    "F2": {"status": "PASS" if F2 else "FAIL", "max_lift_error": max(l["lift_error"] for r in records for l in r["levels"] if l["lift_error"] is not None)},
    "F3": {"status": "PASS" if F3 else "FAIL", "sign_failure_ids": sign_failures},
    "F4": {"status": "PASS" if F4 else "FAIL", "magnitude_failure_ids": magnitude_failures, "max_fine_residual": max(r["levels"][fine_index]["slope_residual"] for r in records)},
    "F5": {"status": "PASS" if F5 else "FAIL", "group_median_residuals": group_medians},
}

payload = {
    "schema": "stability-arc-conditioning-failure-mechanism-v0.1",
    "scope": "PROSPECTIVE_WEAK_MEASUREMENT_MECHANISM",
    "phase_status": status,
    "environment": {"python": platform.python_version(), "numpy": np.__version__, "platform": platform.platform()},
    "criteria": criteria,
    "records": records,
    "interpretation_firewall": (
        "A PASS validates only the registered weak-measurement perturbative spectral-abscissa mechanism on the fresh "
        "low-kappa overdamped panel away from the repeated-root singularity. It does not restore generalized H2, prove "
        "class monotonicity, license a stochastic chi, or establish localization/collapse behavior."
    ),
}

OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"phase_status": status, "criteria": criteria}, indent=2, sort_keys=True))
raise SystemExit(0 if status == "PASS_PROSPECTIVE_FAILURE_MECHANISM" else 1)
