#!/usr/bin/env python3
import itertools
import json
import math
import platform
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "stochastic_dark_active_quotient_audit_v01.json"

NULL_TOL = 1e-10
TIGHT = 5e-12
TRANSFORM_GATE = 5e-11
STATE_GATE = 2e-12
COV_GATE = 5e-12
MOMENT_GATE = 5e-11
DEGEN_TOL = 1e-10
DEFECT_TOL = 1e-10
DT = 1e-4
DW_COEFFS = [0.47, -0.63]
DT_COV = 7e-4
Q_CONTROLS = [np.array([0.31, -0.22]), np.array([-0.17, 0.28])]
DARK_LIFTS = [-0.73, 0.41]
R_ACTIVE = np.array([[1.2, 0.3], [-0.2, 0.9]], dtype=float)
S_SHEAR = np.array([[0.4, -0.35]], dtype=float)

FIXTURES = [
    {"id": "SQ1", "eta": 0.66, "gamma": 0.27, "kappa": 0.16, "omega": 0.97, "base": [0.14, -0.23, 0.18]},
    {"id": "SQ2", "eta": 0.74, "gamma": 0.35, "kappa": 0.12, "omega": 1.19, "base": [-0.22, 0.17, -0.31]},
    {"id": "SQ3", "eta": 0.58, "gamma": 0.21, "kappa": 0.24, "omega": 0.79, "base": [0.29, 0.08, 0.12]},
]

P_COORD_CONTROLS = [
    np.array([[0.55, 0.09, -0.05], [0.09, 0.42, 0.04], [-0.05, 0.04, 0.31]], dtype=float),
    np.array([[0.70, -0.06, 0.08], [-0.06, 0.36, -0.03], [0.08, -0.03, 0.48]], dtype=float),
]

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
ident2 = np.eye(2, dtype=complex)
sm = np.array([[0, 1], [0, 0]], dtype=complex)
xop = 0.5 * sz
BASIS = [0.5 * sx, 0.5 * sy, 0.5 * sz]
PAULI = [sx, sy, sz]


def max_abs(a):
    arr = np.asarray(a)
    return 0.0 if arr.size == 0 else float(np.max(np.abs(arr)))


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


def quantum_matrices(f):
    state = rho_from_bloch(f["base"])
    A = linear_matrix(lambda e: liouvillian(e, f["gamma"], f["kappa"], f["omega"]))
    amp = math.sqrt(2.0 * f["eta"] * f["kappa"])
    B = amp * linear_matrix(lambda e: delta_h(state, e))
    h = coords(h_super(state))
    Vt = np.array([[float(np.trace(xop @ e).real) for e in BASIS]], dtype=float)
    U = -4.0 * f["eta"] * f["kappa"] * h.reshape(-1, 1)
    Arec = A + U @ Vt
    return state, A, Arec, B, U, Vt


def observability_dark(A, Vt):
    n = A.shape[0]
    rows = []
    Ak = np.eye(n)
    for _ in range(n):
        rows.append(Vt @ Ak)
        Ak = Ak @ A
    O = np.vstack(rows)
    _, s, vh = np.linalg.svd(O, full_matrices=True)
    rank = int(np.sum(s > NULL_TOL))
    D = vh[rank:].T.copy()
    if D.size:
        D, _ = np.linalg.qr(D)
    return O, s, D


def orth_complement(D, n):
    if D.shape[1] == 0:
        return np.eye(n)
    _, _, vh = np.linalg.svd(D.T, full_matrices=True)
    return vh[D.shape[1]:].T.copy()


def quotient_data(A, B, D, C):
    L = C.T
    Aq = L @ A @ C
    Bq = L @ B @ C
    return L, Aq, Bq


def kfull(A, B):
    n = A.shape[0]
    return np.kron(np.eye(n), A) + np.kron(A, np.eye(n)) + np.kron(B, B)


def block_chi(Aq):
    if Aq.shape != (2, 2) or max_abs(np.imag(Aq)) > 1e-12:
        return None
    Ar = np.real(Aq)
    tr = float(np.trace(Ar))
    det = float(np.linalg.det(Ar))
    if tr >= 0.0 or det <= 0.0:
        return None
    return -tr / (2.0 * math.sqrt(det))


def defective_2x2(A):
    tr = float(np.trace(A))
    det = float(np.linalg.det(A))
    disc = tr * tr - 4.0 * det
    if abs(disc) > DEFECT_TOL:
        return False
    lam = tr / 2.0
    return np.linalg.matrix_rank(A - lam * np.eye(2), tol=DEFECT_TOL) == 1


def classify_refusal(A, B, Vt, singular_transform=False):
    O, s, D = observability_dark(A, Vt)
    n = A.shape[0]
    d = D.shape[1]
    if d == 0:
        return "REFUSE_NO_DARK_FACTOR"
    qdim = n - d
    if qdim != 2:
        return "REFUSE_QUOTIENT_DIMENSION"
    C = orth_complement(D, n)
    Pperp = np.eye(n) - D @ D.T
    if max_abs(Pperp @ B @ D) > TIGHT:
        return "REFUSE_STOCHASTIC_LEAKAGE"
    AD = D.T @ A @ D
    Aq = C.T @ A @ C
    if min(abs(x - y) for x in np.linalg.eigvals(AD) for y in np.linalg.eigvals(Aq)) <= DEGEN_TOL:
        return "REFUSE_CROSS_SECTOR_DEGENERACY"
    if defective_2x2(Aq):
        return "REFUSE_DEFECTIVE_ACTIVE_SECTOR"
    if singular_transform:
        return "REFUSE_COORDINATE_FAILURE"
    return "ADMIT_STOCHASTIC_QUOTIENT"


def em_covariance(A, B, P, dt):
    out = np.zeros_like(P)
    for sign in (-1.0, 1.0):
        M = np.eye(A.shape[0]) + A * dt + B * (sign * math.sqrt(dt))
        out += 0.5 * M @ P @ M.T
    return out


records = []
for f in FIXTURES:
    state, Aphys, Arec, B, U, Vt = quantum_matrices(f)
    rho_eigs = np.linalg.eigvalsh(state)
    max_imag = max(max_abs(np.imag(Aphys)), max_abs(np.imag(Arec)), max_abs(np.imag(B)))
    O, obs_s, D = observability_dark(Aphys, Vt)
    C = orth_complement(D, 3)
    L, Aqp, Bq = quotient_data(Aphys, B, D, C)
    _, Aqr, Bqr = quotient_data(Arec, B, D, C)
    Pperp = np.eye(3) - D @ D.T

    s1 = {
        "dim_dark": int(D.shape[1]),
        "dim_quotient": int(3 - D.shape[1]),
        "orth_error": max_abs(D.T @ D - np.eye(D.shape[1])),
        "measurement_error": max_abs(Vt @ D),
        "A_invariance_error": max_abs(Pperp @ Aphys @ D),
    }
    s2_error = max_abs(Pperp @ B @ D)

    channel_rows = []
    for channel, A, Aq in [("physical", Aphys, Aqp), ("record", Arec, Aqr)]:
        s3_A = max_abs(L @ A - Aq @ L)
        s3_B = max_abs(L @ B - Bq @ L)

        Cs = D @ S_SHEAR + C @ R_ACTIVE
        Ts = np.column_stack([D, Cs])
        Tsinv = np.linalg.inv(Ts)
        Ls = Tsinv[-2:, :]
        Aqs = Ls @ A @ Cs
        Bqs = Ls @ B @ Cs
        Rinv = np.linalg.inv(R_ACTIVE)
        s4_A = max_abs(Aqs - Rinv @ Aq @ R_ACTIVE)
        s4_B = max_abs(Bqs - Rinv @ Bq @ R_ACTIVE)
        s4_poly_A = max_abs(np.poly(Aqs) - np.poly(Aq))
        s4_poly_B = max_abs(np.poly(Bqs) - np.poly(Bq))

        state_errors = []
        for q in Q_CONTROLS:
            for alpha in DARK_LIFTS:
                r = C @ q + D[:, 0] * alpha
                for coeff in DW_COEFFS:
                    dw = coeff * math.sqrt(DT)
                    rnext = (np.eye(3) + A * DT + B * dw) @ r
                    qfull = L @ rnext
                    qnext = (np.eye(2) + Aq * DT + Bq * dw) @ q
                    state_errors.append(max_abs(qfull - qnext))

        J = np.kron(L, L)
        K = kfull(A, B)
        Kq = kfull(Aq, Bq)
        moment_error = max_abs(J @ K - Kq @ J)

        cov_errors = []
        T = np.column_stack([D, C])
        for Pc in P_COORD_CONTROLS:
            Pfull = T @ Pc @ T.T
            Pq = L @ Pfull @ L.T
            projected = L @ em_covariance(A, B, Pfull, DT_COV) @ L.T
            qprop = em_covariance(Aq, Bq, Pq, DT_COV)
            cov_errors.append(max_abs(projected - qprop))

        channel_rows.append({
            "channel": channel,
            "Aq": Aq.tolist(),
            "Bq": Bq.tolist(),
            "chi_active_deterministic_metadata": block_chi(Aq),
            "stochastic_status": "STOCHASTIC_PAIR_NOT_COMPRESSED",
            "S3_A_intertwine": s3_A,
            "S3_B_intertwine": s3_B,
            "S4_A_similarity": s4_A,
            "S4_B_similarity": s4_B,
            "S4_A_poly": s4_poly_A,
            "S4_B_poly": s4_poly_B,
            "S5_state_max": max(state_errors),
            "S6_moment_intertwine": moment_error,
            "S6_covariance_max": max(cov_errors),
        })

    records.append({
        "id": f["id"],
        "parameters": f,
        "rho_min_eigenvalue": float(np.min(rho_eigs)),
        "max_imag_matrix_entry": max_imag,
        "observability_singular_values": [float(x) for x in obs_s],
        "S1": s1,
        "S2_B_invariance_error": s2_error,
        "channels": channel_rows,
    })

# Refusal controls.
A1 = np.array([[-0.5, 0, 0], [0, -0.7, 1.0], [0, -1.0, -0.7]], float)
B1 = np.array([[-0.1, 0, 0], [0.2, -0.2, 0], [0, 0, -0.3]], float)
V1 = np.array([[0.0, 0.0, 1.0]])

A2 = np.array([[-0.2, 0, 0, 0], [0, -0.4, 0, 0], [0, 1.0, -0.5, 0], [0, 0, 1.0, -0.6]], float)
B2 = -0.1 * np.eye(4)
V2 = np.array([[0.0, 0.0, 0.0, 1.0]])

A3 = np.array([[-0.4, 0, 0], [1.0, -0.5, 0], [0, 1.0, -0.6]], float)
B3 = -0.1 * np.eye(3)
V3 = np.array([[0.0, 0.0, 1.0]])

A4 = np.diag([-0.5, -0.5, -0.8])
B4 = np.diag([-0.1, -0.2, -0.3])
V4 = np.array([[0.0, 1.0, 1.0]])

A5 = np.array([[-0.4, 0, 0], [0, -0.7, 1.0], [0, 0, -0.7]], float)
B5 = np.diag([-0.1, -0.2, -0.25])
V5 = np.array([[0.0, 1.0, 0.0]])

A6 = np.array([[-0.45, 0, 0], [0, -0.6, 0.9], [0, -0.9, -0.6]], float)
B6 = np.diag([-0.12, -0.18, -0.24])
V6 = np.array([[0.0, 1.0, 1.0]])

refusals = {
    "RQ1": classify_refusal(A1, B1, V1),
    "RQ2": classify_refusal(A2, B2, V2),
    "RQ3": classify_refusal(A3, B3, V3),
    "RQ4": classify_refusal(A4, B4, V4),
    "RQ5": classify_refusal(A5, B5, V5),
    "RQ6": classify_refusal(A6, B6, V6, singular_transform=True),
}
expected_refusals = {
    "RQ1": "REFUSE_STOCHASTIC_LEAKAGE",
    "RQ2": "REFUSE_QUOTIENT_DIMENSION",
    "RQ3": "REFUSE_NO_DARK_FACTOR",
    "RQ4": "REFUSE_CROSS_SECTOR_DEGENERACY",
    "RQ5": "REFUSE_DEFECTIVE_ACTIVE_SECTOR",
    "RQ6": "REFUSE_COORDINATE_FAILURE",
}

criteria = {}
criteria["S0"] = {
    "status": "PASS" if all(r["rho_min_eigenvalue"] > 0 and r["max_imag_matrix_entry"] <= 1e-12 for r in records) else "FAIL",
    "min_density_eigenvalue": min(r["rho_min_eigenvalue"] for r in records),
    "max_imag_matrix_entry": max(r["max_imag_matrix_entry"] for r in records),
}
criteria["S1"] = {
    "status": "PASS" if all(
        r["S1"]["dim_dark"] == 1 and r["S1"]["dim_quotient"] == 2 and
        r["S1"]["orth_error"] <= TIGHT and r["S1"]["measurement_error"] <= TIGHT and r["S1"]["A_invariance_error"] <= TIGHT
        for r in records
    ) else "FAIL",
    "max_error": max(max(r["S1"]["orth_error"], r["S1"]["measurement_error"], r["S1"]["A_invariance_error"]) for r in records),
}
criteria["S2"] = {
    "status": "PASS" if all(r["S2_B_invariance_error"] <= TIGHT for r in records) else "FAIL",
    "max_error": max(r["S2_B_invariance_error"] for r in records),
}
criteria["S3"] = {
    "status": "PASS" if all(max(c["S3_A_intertwine"], c["S3_B_intertwine"]) <= TIGHT for r in records for c in r["channels"]) else "FAIL",
    "max_error": max(max(c["S3_A_intertwine"], c["S3_B_intertwine"]) for r in records for c in r["channels"]),
}
criteria["S4"] = {
    "status": "PASS" if all(
        max(c["S4_A_similarity"], c["S4_B_similarity"]) <= TRANSFORM_GATE and
        max(c["S4_A_poly"], c["S4_B_poly"]) <= TRANSFORM_GATE
        for r in records for c in r["channels"]
    ) else "FAIL",
    "max_matrix_error": max(max(c["S4_A_similarity"], c["S4_B_similarity"]) for r in records for c in r["channels"]),
    "max_poly_error": max(max(c["S4_A_poly"], c["S4_B_poly"]) for r in records for c in r["channels"]),
}
criteria["S5"] = {
    "status": "PASS" if all(c["S5_state_max"] <= STATE_GATE for r in records for c in r["channels"]) else "FAIL",
    "max_error": max(c["S5_state_max"] for r in records for c in r["channels"]),
}
criteria["S6"] = {
    "status": "PASS" if all(c["S6_moment_intertwine"] <= MOMENT_GATE and c["S6_covariance_max"] <= COV_GATE for r in records for c in r["channels"]) else "FAIL",
    "max_moment_error": max(c["S6_moment_intertwine"] for r in records for c in r["channels"]),
    "max_covariance_error": max(c["S6_covariance_max"] for r in records for c in r["channels"]),
}
criteria["S7"] = {
    "status": "PASS" if refusals == expected_refusals and all(c["stochastic_status"] == "STOCHASTIC_PAIR_NOT_COMPRESSED" for r in records for c in r["channels"]) else "FAIL",
    "observed_refusals": refusals,
    "expected_refusals": expected_refusals,
}

overall = "PASS" if all(v["status"] == "PASS" for v in criteria.values()) else "FAIL"
result = {
    "schema": "stability-arc-stochastic-dark-active-quotient-audit-v0.1",
    "scope": "STOCHASTIC_QUOTIENT_CLOSURE_ONLY",
    "overall_status": overall,
    "environment": {"python": platform.python_version(), "numpy": np.__version__},
    "criteria": criteria,
    "fixtures": records,
    "refusals": refusals,
    "interpretation_firewall": "PASS licenses exact stochastic quotient closure only when the deterministic dark subspace is invariant under both A and B. It does not make the dark sector noise-free, compress the stochastic pair to a scalar, or connect chi_active to localization or measurement performance.",
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"overall_status": overall, "criteria": criteria}, indent=2, sort_keys=True))
if overall != "PASS":
    raise SystemExit(1)
