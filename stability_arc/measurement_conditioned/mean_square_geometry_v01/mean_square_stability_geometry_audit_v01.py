#!/usr/bin/env python3
import json
import math
import platform
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "mean_square_stability_geometry_audit_v01.json"

NULL_TOL = 1e-10
QUOTIENT_TOL = 5e-10
LIFT_TOL = 5e-12
COORD_TOL = 5e-10
RH_TOL = 1e-10
COV_TOL = 5e-12
DT = 0.002

R_ACTIVE = np.array([[1.18, 0.27], [-0.16, 0.91]], dtype=float)
P_CONTROLS = [
    np.array([[0.63, 0.11], [0.11, 0.41]], dtype=float),
    np.array([[0.48, -0.07], [-0.07, 0.72]], dtype=float),
]

QUANTUM_FIXTURES = [
    {"id": "MSQ1", "eta": 0.61, "gamma": 0.31, "kappa": 0.19, "omega": 1.07, "base": [0.11, -0.19, 0.27]},
    {"id": "MSQ2", "eta": 0.79, "gamma": 0.24, "kappa": 0.14, "omega": 0.88, "base": [-0.18, 0.21, -0.16]},
    {"id": "MSQ3", "eta": 0.55, "gamma": 0.42, "kappa": 0.09, "omega": 1.31, "base": [0.26, 0.05, -0.22]},
]

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
ident2 = np.eye(2, dtype=complex)
sm = np.array([[0, 1], [0, 0]], dtype=complex)
xop = 0.5 * sz
BASIS = [0.5 * sx, 0.5 * sy, 0.5 * sz]
PAULI = [sx, sy, sz]

D2 = np.array(
    [[1.0, 0.0, 0.0],
     [0.0, 1.0, 0.0],
     [0.0, 1.0, 0.0],
     [0.0, 0.0, 1.0]],
    dtype=float,
)
E2 = np.array(
    [[1.0, 0.0, 0.0, 0.0],
     [0.0, 0.5, 0.5, 0.0],
     [0.0, 0.0, 0.0, 1.0]],
    dtype=float,
)
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


def quantum_matrices(f):
    state = rho_from_bloch(f["base"])
    Aphys = linear_matrix(lambda e: liouvillian(e, f["gamma"], f["kappa"], f["omega"]))
    amp = math.sqrt(2.0 * f["eta"] * f["kappa"])
    B = amp * linear_matrix(lambda e: delta_h(state, e))
    h = coords(h_super(state))
    Vt = np.array([[float(np.trace(xop @ e).real) for e in BASIS]], dtype=float)
    U = -4.0 * f["eta"] * f["kappa"] * h.reshape(-1, 1)
    Arec = Aphys + U @ Vt
    return state, Aphys, Arec, B, Vt


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


def quotient(A, B, D, C):
    L = C.T
    Aq = L @ A @ C
    Bq = L @ B @ C
    return L, Aq, Bq


def kfull(A, B):
    n = A.shape[0]
    return np.kron(np.eye(n), A) + np.kron(A, np.eye(n)) + np.kron(B, B)


def sym_coords(P):
    return np.array([P[0, 0], 0.5 * (P[0, 1] + P[1, 0]), P[1, 1]], dtype=float)


def sym_matrix(m):
    return np.array([[m[0], m[1]], [m[1], m[2]]], dtype=float)


def moment_action(A, B, P):
    return A @ P + P @ A.T + B @ P @ B.T


def symmetric_generator_direct(A, B):
    return np.column_stack([sym_coords(moment_action(A, B, E)) for E in SYM_BASIS])


def symmetric_generator_kron(A, B):
    return E2 @ kfull(A, B) @ D2


def characteristic_coeffs(G):
    p = np.poly(G)
    p = np.real_if_close(p, tol=1000)
    if np.iscomplexobj(p) and max_abs(np.imag(p)) > 1e-10:
        raise ValueError("non-real characteristic polynomial")
    return np.asarray(np.real(p[1:]), dtype=float)


def routh_class(coeffs):
    c1, c2, c3 = [float(x) for x in coeffs]
    h = np.array([c1, c2, c3, c1 * c2 - c3], dtype=float)
    if np.all(h > RH_TOL):
        return "STABLE", h
    if np.all(h >= -RH_TOL) and np.any(np.abs(h) <= RH_TOL):
        return "BOUNDARY", h
    return "UNSTABLE", h


def spectral_class(G):
    eigs = np.linalg.eigvals(G)
    mx = float(np.max(np.real(eigs)))
    if mx < -RH_TOL:
        return "STABLE", eigs, mx
    if abs(mx) <= RH_TOL:
        return "BOUNDARY", eigs, mx
    return "UNSTABLE", eigs, mx


def pair_audit(label, A, B, expected=None, chi_metadata=None):
    Gd = symmetric_generator_direct(A, B)
    Gk = symmetric_generator_kron(A, B)
    lift_error = max_abs(Gd - Gk)
    coeffs = characteristic_coeffs(Gd)
    rc, h = routh_class(coeffs)
    sc, eigs, max_real = spectral_class(Gd)

    Rinv = np.linalg.inv(R_ACTIVE)
    At = Rinv @ A @ R_ACTIVE
    Bt = Rinv @ B @ R_ACTIVE
    Gt = symmetric_generator_direct(At, Bt)
    coeffs_t = characteristic_coeffs(Gt)
    coord_error = max_abs(coeffs - coeffs_t)

    cov_errors = []
    for P in P_CONTROLS:
        m = sym_coords(P)
        P_next = P + DT * moment_action(A, B, P)
        m_next_direct = sym_coords(P_next)
        m_next_G = m + DT * (Gd @ m)
        cov_errors.append(max_abs(m_next_direct - m_next_G))

    return {
        "label": label,
        "A": A.tolist(),
        "B": B.tolist(),
        "G": Gd.tolist(),
        "coefficients": {"c1": float(coeffs[0]), "c2": float(coeffs[1]), "c3": float(coeffs[2])},
        "hurwitz_margin": [float(x) for x in h],
        "routh_class": rc,
        "spectral_class": sc,
        "max_real_eigenvalue": max_real,
        "eigenvalues": [[float(z.real), float(z.imag)] for z in eigs],
        "expected_class": expected,
        "chi_formula_metadata": chi_metadata,
        "lift_identity_error": lift_error,
        "coordinate_coefficient_error": coord_error,
        "covariance_coordinate_error": max(cov_errors),
        "mean_square_representation_status": "MEAN_SQUARE_INVARIANTS_REQUIRED",
    }


quantum_records = []
pair_records = []
quotient_errors = []
rho_mins = []

for f in QUANTUM_FIXTURES:
    state, Aphys, Arec, B, Vt = quantum_matrices(f)
    rho_min = float(np.min(np.linalg.eigvalsh(state)))
    rho_mins.append(rho_min)

    O, svals, D = observability_dark(Aphys, Vt)
    C = orth_complement(D, 3)
    Pperp = np.eye(3) - D @ D.T if D.shape[1] else np.eye(3)
    dim_dark = int(D.shape[1])
    dim_q = 3 - dim_dark

    measurement_resid = max_abs(Vt @ D) if dim_dark else float("inf")
    Aphys_dark = max_abs(Pperp @ Aphys @ D) if dim_dark else float("inf")
    Arec_dark = max_abs(Pperp @ Arec @ D) if dim_dark else float("inf")
    B_dark = max_abs(Pperp @ B @ D) if dim_dark else float("inf")

    fixture_channels = []
    if dim_dark == 1 and dim_q == 2:
        for channel, A in [("physical", Aphys), ("record", Arec)]:
            L, Aq, Bq = quotient(A, B, D, C)
            a_intertwine = max_abs(L @ A - Aq @ L)
            b_intertwine = max_abs(L @ B - Bq @ L)
            quotient_errors.extend([a_intertwine, b_intertwine])
            rec = pair_audit(f["id"] + "_" + channel, Aq, Bq)
            rec["quotient_A_intertwine_error"] = a_intertwine
            rec["quotient_B_intertwine_error"] = b_intertwine
            pair_records.append(rec)
            fixture_channels.append(rec["label"])

    quantum_records.append({
        "id": f["id"],
        "parameters": f,
        "rho_min_eigenvalue": rho_min,
        "observability_singular_values": [float(x) for x in svals],
        "dim_dark": dim_dark,
        "dim_quotient": dim_q,
        "measurement_dark_error": measurement_resid,
        "Aphys_dark_invariance_error": Aphys_dark,
        "Arec_dark_invariance_error": Arec_dark,
        "B_dark_invariance_error": B_dark,
        "channel_records": fixture_channels,
    })

# Exact isotropic stochastic controls.
for label, a, b, expected in [
    ("ISO_STABLE", 1.0, 1.0, "STABLE"),
    ("ISO_BOUNDARY", 0.5, 1.0, "BOUNDARY"),
    ("ISO_UNSTABLE", 0.4, 1.0, "UNSTABLE"),
]:
    pair_records.append(pair_audit(label, -a * np.eye(2), b * np.eye(2), expected=expected))

# Noiseless oscillator controls.
mass = 1.7
Omega = 1.2
for label, Gamma, expected in [
    ("OSC_UNDER", 1.2, "STABLE"),
    ("OSC_CRITICAL", 2.4, "STABLE"),
    ("OSC_OVER", 3.6, "STABLE"),
    ("OSC_NEUTRAL", 0.0, "BOUNDARY"),
]:
    A = np.array([[0.0, 1.0 / mass], [-mass * Omega * Omega, -Gamma]], dtype=float)
    B = np.zeros((2, 2), dtype=float)
    chi = Gamma / (2.0 * Omega)
    pair_records.append(pair_audit(label, A, B, expected=expected, chi_metadata=chi))

# Nontrivial Routh-Hurwitz boundary-plane classifier control.
G_RH = np.array([[-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]], dtype=float)
rh_coeffs = characteristic_coeffs(G_RH)
rh_class, rh_margin = routh_class(rh_coeffs)
rh_spec, rh_eigs, rh_max_real = spectral_class(G_RH)
rh_control = {
    "coefficients": [float(x) for x in rh_coeffs],
    "hurwitz_margin": [float(x) for x in rh_margin],
    "routh_class": rh_class,
    "spectral_class": rh_spec,
    "max_real_eigenvalue": rh_max_real,
    "eigenvalues": [[float(z.real), float(z.imag)] for z in rh_eigs],
    "expected_class": "BOUNDARY",
}

# Frozen gates.
M0_rows = []
for q in quantum_records:
    ok = (
        q["rho_min_eigenvalue"] > 0.0
        and q["dim_dark"] == 1
        and q["dim_quotient"] == 2
        and q["measurement_dark_error"] <= QUOTIENT_TOL
        and q["Aphys_dark_invariance_error"] <= QUOTIENT_TOL
        and q["Arec_dark_invariance_error"] <= QUOTIENT_TOL
        and q["B_dark_invariance_error"] <= QUOTIENT_TOL
        and len(q["channel_records"]) == 2
    )
    M0_rows.append(ok)
M0 = all(M0_rows) and (max(quotient_errors) if quotient_errors else float("inf")) <= QUOTIENT_TOL

M1 = all(r["lift_identity_error"] <= LIFT_TOL for r in pair_records)
M2 = all(r["coordinate_coefficient_error"] <= COORD_TOL for r in pair_records)
M3 = all(r["routh_class"] == r["spectral_class"] for r in pair_records)

expected_pairs = {r["label"]: r for r in pair_records if r["expected_class"] is not None}
M4 = (
    expected_pairs["ISO_STABLE"]["routh_class"] == "STABLE"
    and expected_pairs["ISO_BOUNDARY"]["routh_class"] == "BOUNDARY"
    and expected_pairs["ISO_UNSTABLE"]["routh_class"] == "UNSTABLE"
    and rh_control["routh_class"] == "BOUNDARY"
    and rh_control["spectral_class"] == "BOUNDARY"
)
M5 = (
    expected_pairs["OSC_UNDER"]["routh_class"] == "STABLE"
    and expected_pairs["OSC_CRITICAL"]["routh_class"] == "STABLE"
    and expected_pairs["OSC_OVER"]["routh_class"] == "STABLE"
    and expected_pairs["OSC_NEUTRAL"]["routh_class"] == "BOUNDARY"
)
M6 = all(r["covariance_coordinate_error"] <= COV_TOL for r in pair_records)

criteria = {
    "M0": {
        "status": "PASS" if M0 else "FAIL",
        "min_density_eigenvalue": min(rho_mins) if rho_mins else None,
        "max_quotient_intertwining_error": max(quotient_errors) if quotient_errors else None,
    },
    "M1": {
        "status": "PASS" if M1 else "FAIL",
        "max_lift_identity_error": max(r["lift_identity_error"] for r in pair_records),
    },
    "M2": {
        "status": "PASS" if M2 else "FAIL",
        "max_coordinate_coefficient_error": max(r["coordinate_coefficient_error"] for r in pair_records),
    },
    "M3": {
        "status": "PASS" if M3 else "FAIL",
        "classifier_mismatches": [r["label"] for r in pair_records if r["routh_class"] != r["spectral_class"]],
    },
    "M4": {"status": "PASS" if M4 else "FAIL", "rh_plane_control": rh_control},
    "M5": {
        "status": "PASS" if M5 else "FAIL",
        "oscillator_classes": {k: expected_pairs[k]["routh_class"] for k in ["OSC_UNDER", "OSC_CRITICAL", "OSC_OVER", "OSC_NEUTRAL"]},
    },
    "M6": {
        "status": "PASS" if M6 else "FAIL",
        "max_covariance_coordinate_error": max(r["covariance_coordinate_error"] for r in pair_records),
    },
}

overall = all(criteria[k]["status"] == "PASS" for k in criteria)

payload = {
    "schema": "stability-arc-mean-square-stability-geometry-v0.1",
    "scope": "MEAN_SQUARE_GEOMETRY_ONLY",
    "overall_status": "PASS" if overall else "FAIL",
    "mean_square_scalar_status": "MEAN_SQUARE_INVARIANTS_REQUIRED",
    "environment": {"python": platform.python_version(), "numpy": np.__version__, "platform": platform.platform()},
    "tolerances": {
        "quotient": QUOTIENT_TOL,
        "lift": LIFT_TOL,
        "coordinate": COORD_TOL,
        "routh_hurwitz": RH_TOL,
        "covariance": COV_TOL,
    },
    "quantum_fixtures": quantum_records,
    "pair_records": pair_records,
    "rh_plane_control": rh_control,
    "criteria": criteria,
    "interpretation_firewall": (
        "A PASS licenses the 3x3 symmetric second-moment generator, its cubic characteristic coefficients, "
        "and the Routh-Hurwitz mean-square classifier for admitted 2D stochastic quotients. It does not "
        "license a stochastic scalar chi, localization or collapse prediction, channel averaging, or chi=1 "
        "as a stochastic stability boundary."
    ),
}

OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(payload, indent=2, sort_keys=True))
raise SystemExit(0 if overall else 1)
