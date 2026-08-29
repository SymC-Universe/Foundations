#!/usr/bin/env python3
import json
import math
import platform
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "conditioning_mean_square_directionality_audit_v01.json"

SEED = 2026082901
N_FIXTURES = 24
NULL_TOL = 1e-10
QUOTIENT_TOL = 5e-10
LIFT_TOL = 5e-12
RH_TOL = 1e-10
RANK_TOL = 1e-10
H1_TOL = 1e-10

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
    rows = []
    Ak = np.eye(A.shape[0])
    for _ in range(A.shape[0]):
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


def moment_action(A, B, P):
    return A @ P + P @ A.T + B @ P @ B.T


def sym_generator(A, B):
    return np.column_stack([sym_coords(moment_action(A, B, E)) for E in SYM_BASIS])


def sym_generator_kron(A, B):
    return ELIM @ kfull(A, B) @ DUP


def coeffs(G):
    p = np.real_if_close(np.poly(G), tol=1000)
    if np.iscomplexobj(p) and max_abs(np.imag(p)) > 1e-10:
        raise ValueError("complex characteristic polynomial")
    return np.asarray(np.real(p[1:]), dtype=float)


def routh_class(G):
    c1, c2, c3 = [float(x) for x in coeffs(G)]
    h = np.array([c1, c2, c3, c1 * c2 - c3], dtype=float)
    if np.all(h > RH_TOL):
        return "STABLE", h
    if np.all(h >= -RH_TOL) and np.any(np.abs(h) <= RH_TOL):
        return "BOUNDARY", h
    return "UNSTABLE", h


def spectral_class(G):
    eigs = np.linalg.eigvals(G)
    alpha = float(np.max(np.real(eigs)))
    if alpha < -RH_TOL:
        klass = "STABLE"
    elif abs(alpha) <= RH_TOL:
        klass = "BOUNDARY"
    else:
        klass = "UNSTABLE"
    return klass, alpha, eigs


def matrix_rank_tol(M, tol=RANK_TOL):
    s = np.linalg.svd(M, compute_uv=False)
    return int(np.sum(s > tol)), [float(x) for x in s]


def generate_fixtures():
    rng = np.random.default_rng(SEED)
    out = []
    for i in range(N_FIXTURES):
        eta = float(rng.uniform(0.25, 0.90))
        gamma = float(rng.uniform(0.12, 0.60))
        kappa = float(rng.uniform(0.04, 0.35))
        omega = float(rng.uniform(0.55, 1.60))
        while True:
            base = rng.uniform(-0.40, 0.40, size=3)
            if float(np.linalg.norm(base)) < 0.70:
                break
        out.append({
            "id": f"CD{i+1:02d}",
            "eta": eta,
            "gamma": gamma,
            "kappa": kappa,
            "omega": omega,
            "base": [float(x) for x in base],
        })
    return out


def fixture_signature(fs):
    return json.dumps(fs, sort_keys=True, separators=(",", ":"))


fixtures_a = generate_fixtures()
fixtures_b = generate_fixtures()
D0 = fixture_signature(fixtures_a) == fixture_signature(fixtures_b) and len(fixtures_a) == N_FIXTURES

records = []
admitted = []
refused = []
D2_ok = True
D3_ok = True

for f in fixtures_a:
    state, Aphys, Arec, B, Vt = quantum_matrices(f)
    rho_min = float(np.min(np.linalg.eigvalsh(state)))
    _, svals, D = observability_dark(Aphys, Vt)
    dim_dark = int(D.shape[1])
    dim_q = 3 - dim_dark

    reasons = []
    if rho_min <= 0.0:
        reasons.append("NONPOSITIVE_DENSITY")
    if dim_dark != 1 or dim_q != 2:
        reasons.append("QUOTIENT_DIMENSION")

    row = {
        "id": f["id"],
        "parameters": f,
        "rho_min_eigenvalue": rho_min,
        "observability_singular_values": [float(x) for x in svals],
        "dim_dark": dim_dark,
        "dim_quotient": dim_q,
    }

    if dim_dark == 1 and dim_q == 2:
        C = orth_complement(D, 3)
        Pperp = np.eye(3) - D @ D.T
        residuals = {
            "measurement": max_abs(Vt @ D),
            "Aphys_dark": max_abs(Pperp @ Aphys @ D),
            "Arec_dark": max_abs(Pperp @ Arec @ D),
            "B_dark": max_abs(Pperp @ B @ D),
        }
        if any(v > QUOTIENT_TOL for v in residuals.values()):
            reasons.append("DARK_INVARIANCE")
        row["dark_residuals"] = residuals

        Lp, Aqp, Bqp = quotient(Aphys, B, D, C)
        Lr, Aqr, Bqr = quotient(Arec, B, D, C)
        inter = {
            "phys_A": max_abs(Lp @ Aphys - Aqp @ Lp),
            "phys_B": max_abs(Lp @ B - Bqp @ Lp),
            "rec_A": max_abs(Lr @ Arec - Aqr @ Lr),
            "rec_B": max_abs(Lr @ B - Bqr @ Lr),
            "Bq_common": max_abs(Bqp - Bqr),
        }
        if any(v > QUOTIENT_TOL for v in inter.values()):
            reasons.append("QUOTIENT_INTERTWINING")
        row["intertwining_residuals"] = inter

        if not reasons:
            Gp = sym_generator(Aqp, Bqp)
            Gr = sym_generator(Aqr, Bqr)
            Gp_k = sym_generator_kron(Aqp, Bqp)
            Gr_k = sym_generator_kron(Aqr, Bqr)
            lift_err = max(max_abs(Gp - Gp_k), max_abs(Gr - Gr_k))

            cp, ap, eigp = spectral_class(Gp)
            cr, ar, eigr = spectral_class(Gr)
            rp, hp = routh_class(Gp)
            rr, hr = routh_class(Gr)
            if lift_err > LIFT_TOL or cp != rp or cr != rr:
                D2_ok = False

            DeltaA = Aqr - Aqp
            DeltaG = Gr - Gp
            rank_A, sA = matrix_rank_tol(DeltaA)
            rank_G, sG = matrix_rank_tol(DeltaG)
            predicted_DeltaG = sym_generator(DeltaA, np.zeros((2, 2), dtype=float))
            bridge_err = max_abs(DeltaG - predicted_DeltaG)
            if rank_A > 1 or rank_G > 2 or bridge_err > LIFT_TOL:
                D3_ok = False

            row.update({
                "status": "ADMIT",
                "physical": {
                    "alpha": ap,
                    "class": cp,
                    "routh_class": rp,
                    "coefficients": [float(x) for x in coeffs(Gp)],
                    "hurwitz_margin": [float(x) for x in hp],
                    "eigenvalues": [[float(z.real), float(z.imag)] for z in eigp],
                },
                "record": {
                    "alpha": ar,
                    "class": cr,
                    "routh_class": rr,
                    "coefficients": [float(x) for x in coeffs(Gr)],
                    "hurwitz_margin": [float(x) for x in hr],
                    "eigenvalues": [[float(z.real), float(z.imag)] for z in eigr],
                },
                "alpha_displacement_record_minus_physical": ar - ap,
                "H1_fixture_pass": bool(ar <= ap + H1_TOL),
                "mean_square_lift_error": lift_err,
                "DeltaA_rank": rank_A,
                "DeltaA_singular_values": sA,
                "DeltaG_rank": rank_G,
                "DeltaG_singular_values": sG,
                "DeltaG_lift_error": bridge_err,
                "representation_status": "MEAN_SQUARE_INVARIANTS_REQUIRED",
            })
            admitted.append(row)
        else:
            row.update({"status": "REFUSE_QUOTIENT", "reasons": reasons})
            refused.append(row)
    else:
        row.update({"status": "REFUSE_QUOTIENT", "reasons": reasons})
        refused.append(row)

    records.append(row)

D1 = len(admitted) >= 20
D2 = D2_ok and all(r["mean_square_lift_error"] <= LIFT_TOL for r in admitted)
D3 = D3_ok and all(r["DeltaA_rank"] <= 1 and r["DeltaG_rank"] <= 2 and r["DeltaG_lift_error"] <= LIFT_TOL for r in admitted)

# Adversarial comparator controls.
A0 = np.array([[-0.3, 1.0], [-1.0, -0.3]], dtype=float)
B0 = 0.2 * np.eye(2)
G0 = sym_generator(A0, B0)
base_class, base_alpha, _ = spectral_class(G0)
controls = {}
for label, delta in [("CTRL_STABILIZE", -0.4), ("CTRL_DESTABILIZE", 0.8)]:
    DA = np.array([[delta, 0.0], [0.0, 0.0]], dtype=float)
    Gu = sym_generator(A0 + DA, B0)
    klass, au, _ = spectral_class(Gu)
    controls[label] = {
        "base_alpha": base_alpha,
        "updated_alpha": au,
        "displacement": au - base_alpha,
        "base_class": base_class,
        "updated_class": klass,
    }

D4 = (
    controls["CTRL_STABILIZE"]["displacement"] < 0.0
    and controls["CTRL_DESTABILIZE"]["displacement"] > 0.0
    and controls["CTRL_DESTABILIZE"]["updated_class"] == "UNSTABLE"
)

h1_failures = [r["id"] for r in admitted if not r["H1_fixture_pass"]]
D5 = D1 and len(h1_failures) == 0

if not D0 or not D2 or not D3 or not D4:
    phase_status = "AUDIT_FAILURE"
elif not D1:
    phase_status = "QUOTIENT_ADMISSION_HOLD"
elif D5:
    phase_status = "PASS_PROSPECTIVE_H1"
else:
    phase_status = "FAIL_PROSPECTIVE_H1"

criteria = {
    "D0": {"status": "PASS" if D0 else "FAIL", "seed": SEED, "n_fixtures": len(fixtures_a)},
    "D1": {"status": "PASS" if D1 else "FAIL", "admitted": len(admitted), "refused": len(refused)},
    "D2": {"status": "PASS" if D2 else "FAIL", "max_lift_error": max([r["mean_square_lift_error"] for r in admitted], default=None)},
    "D3": {"status": "PASS" if D3 else "FAIL", "max_DeltaG_lift_error": max([r["DeltaG_lift_error"] for r in admitted], default=None)},
    "D4": {"status": "PASS" if D4 else "FAIL", "controls": controls},
    "D5": {"status": "PASS" if D5 else "FAIL", "H1_failures": h1_failures},
}

payload = {
    "schema": "stability-arc-conditioning-mean-square-directionality-v0.1",
    "scope": "PROSPECTIVE_DIRECTIONALITY_TEST",
    "hypothesis": "H1: alpha_rec <= alpha_phys + 1e-10 for every admitted fresh fixture",
    "phase_status": phase_status,
    "environment": {"python": platform.python_version(), "numpy": np.__version__, "platform": platform.platform()},
    "criteria": criteria,
    "fresh_fixtures": records,
    "admitted_ids": [r["id"] for r in admitted],
    "refused_ids": [r["id"] for r in refused],
    "alpha_displacements": {r["id"]: r["alpha_displacement_record_minus_physical"] for r in admitted},
    "interpretation_firewall": (
        "A PASS supports only the bounded prospective statement that same-record conditioning did not worsen "
        "mean-square spectral abscissa in this seeded fresh sample. A FAIL identifies fresh conditions where it did. "
        "Neither outcome licenses localization, collapse, measurement-quality claims, channel averaging, or a stochastic chi."
    ),
}

OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(payload, indent=2, sort_keys=True))
raise SystemExit(0 if phase_status == "PASS_PROSPECTIVE_H1" else 1)
