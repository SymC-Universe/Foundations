#!/usr/bin/env python3
import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "targeted_class_crossing_audit_v01.json"
STAGE_A = RESULTS / "stageA_physical_stable_selection.json"
STAGE_A_SHA = RESULTS / "stageA_physical_stable_selection.sha256"

SEED = 2026082905
N = 100000
ROBUST_TOL = 1e-6
DARK_TOL = 5e-9
LIFT_TOL = 5e-11
NULL_TOL = 1e-10
MIN_STAGE_A = 10000

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
ident2 = np.eye(2, dtype=complex)
sm = np.array([[0, 1], [0, 0]], dtype=complex)
xop = 0.5 * sz
BASIS = [0.5 * sx, 0.5 * sy, 0.5 * sz]
PAULI = [sx, sy, sz]
ACTIVE = np.array([[1.0, 0.0], [0.0, 0.0], [0.0, 1.0]], dtype=float)

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


def canonical_bytes(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def generate_inputs():
    rng = np.random.default_rng(SEED)
    out = []
    for i in range(1, N + 1):
        rk = float(10.0 ** rng.uniform(math.log10(3.0), math.log10(100.0)))
        rw = float(10.0 ** rng.uniform(math.log10(3.0), math.log10(100.0)))
        eta = float(rng.uniform(0.05, 0.25))
        sign_z = -1.0 if int(rng.integers(0, 2)) == 0 else 1.0
        zabs = float(rng.uniform(0.90, 0.999))
        z = sign_z * zabs
        fx = float(rng.uniform(0.20, 0.99))
        x = -sign_z * fx * math.sqrt(1.0 - z * z)
        out.append({
            "id": f"XC{i:06d}",
            "gamma": 1.0,
            "kappa": rk,
            "omega": rw,
            "eta": eta,
            "x": x,
            "y": 0.0,
            "z": z,
        })
    return out


def arrays(inputs):
    return {k: np.array([f[k] for f in inputs], dtype=float) for k in ["gamma", "kappa", "omega", "eta", "x", "z"]}


def batch_G(gamma, kappa, omega, eta, x, z, record=False):
    q = eta * kappa
    s = np.sqrt(2.0 * q)
    a11 = -(gamma / 2.0 + kappa)
    a12 = omega.copy()
    a21 = -omega
    a22 = -gamma.copy()
    if record:
        a12 = a12 + 2.0 * q * z * x
        a22 = a22 - 2.0 * q * (1.0 - z * z)
    b11 = -s * z
    b12 = -s * x
    b21 = np.zeros_like(b11)
    b22 = -2.0 * s * z

    G = np.empty((len(gamma), 3, 3), dtype=float)
    G[:, 0, 0] = 2.0 * a11 + b11 * b11
    G[:, 1, 0] = a21 + b11 * b21
    G[:, 2, 0] = b21 * b21

    G[:, 0, 1] = 2.0 * a12 + 2.0 * b11 * b12
    G[:, 1, 1] = a11 + a22 + b11 * b22 + b12 * b21
    G[:, 2, 1] = 2.0 * a21 + 2.0 * b21 * b22

    G[:, 0, 2] = b12 * b12
    G[:, 1, 2] = a12 + b12 * b22
    G[:, 2, 2] = 2.0 * a22 + b22 * b22
    return G


def alpha_batch(G):
    eigs = np.linalg.eigvals(G)
    return np.max(np.real(eigs), axis=1)


def physical_active(f):
    q = f["eta"] * f["kappa"]
    s = math.sqrt(2.0 * q)
    A = np.array([[-(f["gamma"] / 2.0 + f["kappa"]), f["omega"]], [-f["omega"], -f["gamma"]]], dtype=float)
    B = np.array([[-s * f["z"], -s * f["x"]], [0.0, -2.0 * s * f["z"]]], dtype=float)
    return A, B


def record_active(f):
    A, B = physical_active(f)
    q = f["eta"] * f["kappa"]
    A = A + np.array([[0.0, 2.0 * q * f["z"] * f["x"]], [0.0, -2.0 * q * (1.0 - f["z"] ** 2)]], dtype=float)
    return A, B


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


def comm(a, b):
    return a @ b - b @ a


def dissipator(c, state):
    cd = c.conj().T
    cdc = cd @ c
    return c @ state @ cd - 0.5 * (cdc @ state + state @ cdc)


def rho_from_xyz(f):
    return 0.5 * (ident2 + f["x"] * sx + f["y"] * sy + f["z"] * sz)


def mu(state):
    return float(np.trace(xop @ state).real)


def h_super(state):
    return xop @ state + state @ xop - 2.0 * mu(state) * state


def delta_h(state, perturbation):
    dm = float(np.trace(xop @ perturbation).real)
    return xop @ perturbation + perturbation @ xop - 2.0 * mu(state) * perturbation - 2.0 * dm * state


def liouvillian(state, f):
    H = 0.5 * f["omega"] * sy
    c = math.sqrt(f["gamma"]) * sm
    return -1j * comm(H, state) + dissipator(c, state) + 2.0 * f["kappa"] * dissipator(xop, state)


def coords(operator):
    vals = [complex(np.trace(p @ operator)) for p in PAULI]
    if max(abs(v.imag) for v in vals) > 1e-9:
        raise ValueError("non-real Bloch coordinate")
    return np.array([v.real for v in vals], dtype=float)


def linear_matrix(action):
    return np.column_stack([coords(action(e)) for e in BASIS])


def full_reconstruct(f):
    state = rho_from_xyz(f)
    Aphys = linear_matrix(lambda e: liouvillian(e, f))
    amp = math.sqrt(2.0 * f["eta"] * f["kappa"])
    B = amp * linear_matrix(lambda e: delta_h(state, e))
    h = coords(h_super(state))
    Vt = np.array([[float(np.trace(xop @ e).real) for e in BASIS]], dtype=float)
    U = -4.0 * f["eta"] * f["kappa"] * h.reshape(-1, 1)
    Arec = Aphys + U @ Vt
    return state, Aphys, Arec, B, Vt


def dark_space(A, Vt):
    O = np.vstack([Vt, Vt @ A, Vt @ A @ A])
    _, s, vh = np.linalg.svd(O, full_matrices=True)
    rank = int(np.sum(s > NULL_TOL))
    D = vh[rank:].T.copy()
    if D.size:
        D, _ = np.linalg.qr(D)
    return s, D


# X0 input determinism.
inputs_a = generate_inputs()
inputs_b = generate_inputs()
input_sha_a = hashlib.sha256(canonical_bytes(inputs_a)).hexdigest()
input_sha_b = hashlib.sha256(canonical_bytes(inputs_b)).hexdigest()
X0 = input_sha_a == input_sha_b and len(inputs_a) == N

# Stage A: physical channel only.
a = arrays(inputs_a)
Gp_batch = batch_G(a["gamma"], a["kappa"], a["omega"], a["eta"], a["x"], a["z"], record=False)
alpha_p = alpha_batch(Gp_batch)
scale = a["gamma"] + a["kappa"] + a["omega"] + a["eta"] * a["kappa"]
norm_p = alpha_p / scale
eligible_idx = np.where(norm_p < -ROBUST_TOL)[0]

stageA_payload = {
    "schema": "stability-arc-targeted-class-crossing-stageA-v0.1",
    "seed": SEED,
    "candidate_input_sha256": input_sha_a,
    "n_candidates": N,
    "robust_physical_stable_tolerance": -ROBUST_TOL,
    "eligible_count": int(len(eligible_idx)),
    "eligible": [
        {"id": inputs_a[int(i)]["id"], "normalized_alpha_phys": float(norm_p[int(i)])}
        for i in eligible_idx
    ],
}
stageA_bytes = json.dumps(stageA_payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"
STAGE_A.write_bytes(stageA_bytes)
stageA_sha = hashlib.sha256(stageA_bytes).hexdigest()
STAGE_A_SHA.write_text(stageA_sha + "  stageA_physical_stable_selection.json\n", encoding="utf-8")
X1 = len(eligible_idx) >= MIN_STAGE_A

# Verify frozen bytes before Stage B.
assert hashlib.sha256(STAGE_A.read_bytes()).hexdigest() == stageA_sha
frozen_ids = [row["id"] for row in json.loads(STAGE_A.read_text(encoding="utf-8"))["eligible"]]
assert frozen_ids == [inputs_a[int(i)]["id"] for i in eligible_idx]

# Stage B: same-record reveal only for frozen eligible IDs.
sel = {k: a[k][eligible_idx] for k in a}
Gr_batch = batch_G(sel["gamma"], sel["kappa"], sel["omega"], sel["eta"], sel["x"], sel["z"], record=True)
alpha_r = alpha_batch(Gr_batch)
scale_sel = scale[eligible_idx]
norm_r = alpha_r / scale_sel
cross_local = np.where(norm_r > ROBUST_TOL)[0]
analytic_crossings = []
for j in cross_local:
    idx = int(eligible_idx[int(j)])
    analytic_crossings.append({
        "id": inputs_a[idx]["id"],
        "candidate_index": idx + 1,
        "parameters": inputs_a[idx],
        "normalized_alpha_phys": float(norm_p[idx]),
        "normalized_alpha_rec": float(norm_r[int(j)]),
        "alpha_phys": float(alpha_p[idx]),
        "alpha_rec": float(alpha_r[int(j)]),
        "scale": float(scale[idx]),
    })
X2 = len(frozen_ids) == len(eligible_idx)

# Independent full-Hilbert reconstruction for every analytic robust crossing.
reconstruction_records = []
verified_crossing_ids = []
for c in analytic_crossings:
    f = c["parameters"]
    state, Aphys3, Arec3, B3, Vt = full_reconstruct(f)
    rho_min = float(np.min(np.linalg.eigvalsh(state)))
    svals, D = dark_space(Aphys3, Vt)
    reasons = []
    if rho_min <= 0.0:
        reasons.append("NONPOSITIVE_DENSITY")
    if D.shape[1] != 1:
        reasons.append("DARK_DIMENSION")

    if D.shape[1] == 1:
        Pperp = np.eye(3) - D @ D.T
        L = ACTIVE.T
        dark_res = {
            "measurement": max_abs(Vt @ D),
            "Aphys": max_abs(Pperp @ Aphys3 @ D),
            "Arec": max_abs(Pperp @ Arec3 @ D),
            "B": max_abs(Pperp @ B3 @ D),
            "active_kernel": max_abs(L @ D),
        }
        if max(dark_res.values()) > DARK_TOL:
            reasons.append("DARK_INVARIANCE")

        Ap = L @ Aphys3 @ ACTIVE
        Ar = L @ Arec3 @ ACTIVE
        Bp = L @ B3 @ ACTIVE
        inter = {
            "Aphys": max_abs(L @ Aphys3 - Ap @ L),
            "Arec": max_abs(L @ Arec3 - Ar @ L),
            "B": max_abs(L @ B3 - Bp @ L),
        }
        if max(inter.values()) > DARK_TOL:
            reasons.append("INTERTWINING")

        A_an, B_an = physical_active(f)
        Ar_an, _ = record_active(f)
        matrix_error = max(max_abs(Ap - A_an), max_abs(Ar - Ar_an), max_abs(Bp - B_an))
        if matrix_error > DARK_TOL:
            reasons.append("ANALYTIC_RECONSTRUCTION")

        Gp = sym_generator(Ap, Bp)
        Gr = sym_generator(Ar, Bp)
        lift_error = max(
            max_abs(Gp - sym_generator_kron(Ap, Bp)),
            max_abs(Gr - sym_generator_kron(Ar, Bp)),
        )
        if lift_error > LIFT_TOL:
            reasons.append("MOMENT_LIFT")

        R = f["gamma"] + f["kappa"] + f["omega"] + f["eta"] * f["kappa"]
        nap = alpha(Gp) / R
        nar = alpha(Gr) / R
        robust = nap < -ROBUST_TOL and nar > ROBUST_TOL
        if not robust:
            reasons.append("CROSSING_NOT_REPRODUCED")
    else:
        dark_res = inter = None
        matrix_error = lift_error = None
        nap = nar = None
        robust = False

    admitted = len(reasons) == 0
    if admitted:
        verified_crossing_ids.append(c["id"])
    reconstruction_records.append({
        "id": c["id"],
        "admitted_verified_crossing": admitted,
        "reasons": reasons,
        "rho_min_eigenvalue": rho_min,
        "observability_singular_values": [float(v) for v in svals],
        "dark_residuals": dark_res,
        "intertwining_residuals": inter,
        "matrix_reconstruction_error": matrix_error,
        "lift_error": lift_error,
        "normalized_alpha_phys_reconstructed": nap,
        "normalized_alpha_rec_reconstructed": nar,
    })

X3 = len(analytic_crossings) > 0 and len(verified_crossing_ids) > 0

# X4 controls.
control_eta0 = {"id": "ETA0", "gamma": 1.0, "kappa": 5.0, "omega": 6.0, "eta": 0.0, "x": -0.2, "y": 0.0, "z": 0.9}
A0p, B0p = physical_active(control_eta0)
A0r, B0r = record_active(control_eta0)
eta0_ok = max_abs(A0p - A0r) == 0.0 and max_abs(B0p - B0r) == 0.0

As = np.array([[-0.3, 1.0], [-1.0, -0.3]], dtype=float)
Bs = 0.2 * np.eye(2)
Au = As + np.array([[0.8, 0.0], [0.0, 0.0]], dtype=float)
alpha_base = alpha(sym_generator(As, Bs))
alpha_updated = alpha(sym_generator(Au, Bs))
synthetic_ok = alpha_base < -ROBUST_TOL and alpha_updated > ROBUST_TOL
X4 = eta0_ok and synthetic_ok
X5 = X3

if not X0:
    status = "AUDIT_FAILURE"
elif not X1:
    status = "SELECTION_HOLD"
elif not X2 or not X4:
    status = "AUDIT_FAILURE"
elif len(analytic_crossings) == 0:
    status = "FAIL_TARGETED_CROSSING_H4"
elif not X3:
    status = "RECONSTRUCTION_HOLD"
else:
    status = "PASS_TARGETED_CROSSING_H4"

criteria = {
    "X0": {"status": "PASS" if X0 else "FAIL", "candidate_input_sha256": input_sha_a},
    "X1": {"status": "PASS" if X1 else "FAIL", "eligible_count": int(len(eligible_idx)), "stageA_sha256": stageA_sha},
    "X2": {"status": "PASS" if X2 else "FAIL", "stageB_evaluated_count": int(len(frozen_ids)), "analytic_robust_crossing_count": int(len(analytic_crossings))},
    "X3": {"status": "PASS" if X3 else "FAIL", "verified_crossing_count": int(len(verified_crossing_ids)), "verified_crossing_ids": verified_crossing_ids},
    "X4": {"status": "PASS" if X4 else "FAIL", "eta_zero_identity": eta0_ok, "synthetic_base_alpha": alpha_base, "synthetic_updated_alpha": alpha_updated},
    "X5": {"status": "PASS" if X5 else "FAIL"},
}

payload = {
    "schema": "stability-arc-targeted-class-crossing-v0.1",
    "scope": "FRESH_TARGETED_CLASS_CROSSING_EXISTENCE_TEST",
    "phase_status": status,
    "environment": {"python": platform.python_version(), "numpy": np.__version__, "platform": platform.platform()},
    "criteria": criteria,
    "stageA_selection_sha256": stageA_sha,
    "analytic_crossings": analytic_crossings,
    "independent_reconstruction": reconstruction_records,
    "interpretation_firewall": (
        "A PASS prospectively establishes existence of a stable-to-unstable mean-square class crossing in this frozen target "
        "region of the exact measured-qubit family. It does not erase the bounded H3 PASS, license a stochastic chi, or "
        "establish localization/collapse behavior. A FAIL leaves the prior exploratory lead non-confirmatory."
    ),
}
OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"phase_status": status, "criteria": criteria, "first_crossings": analytic_crossings[:10]}, indent=2, sort_keys=True))
raise SystemExit(0 if status == "PASS_TARGETED_CROSSING_H4" else 1)
