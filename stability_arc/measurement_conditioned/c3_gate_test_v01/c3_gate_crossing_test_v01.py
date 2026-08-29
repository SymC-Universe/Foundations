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
OUT = RESULTS / "c3_gate_crossing_test_v01.json"
INPUTS_FILE = RESULTS / "candidate_inputs.json"
STAGE_A = RESULTS / "stageA_physical_stable_selection.json"
STAGE_A_SHA = RESULTS / "stageA_physical_stable_selection.sha256"

SEED = 2026082907
N = 100000
ROBUST_TOL = 1e-6
MARGIN_TOL = 1e-9
DARK_TOL = 5e-9
LIFT_TOL = 5e-11
MARGIN_RECON_TOL = 5e-9
C3_FORMULA_TOL = 2e-10
NULL_TOL = 1e-10
MIN_STAGE_A = 10000
MIN_CROSSINGS = 20

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
            "id": f"C5{i:06d}",
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
    keys = ["gamma", "kappa", "omega", "eta", "x", "z"]
    return {k: np.array([f[k] for f in inputs], dtype=float) for k in keys}


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


def rh_batch(G):
    tr = np.trace(G, axis1=1, axis2=2)
    tr2 = np.trace(G @ G, axis1=1, axis2=2)
    c1 = -tr
    c2 = 0.5 * (tr * tr - tr2)
    c3 = -np.linalg.det(G)
    h = c1 * c2 - c3
    eigs = np.linalg.eigvals(G)
    alpha = np.max(np.real(eigs), axis=1)
    return c1, c2, c3, h, alpha


def physical_active(f):
    q = f["eta"] * f["kappa"]
    s = math.sqrt(2.0 * q)
    A = np.array(
        [[-(f["gamma"] / 2.0 + f["kappa"]), f["omega"]],
         [-f["omega"], -f["gamma"]]], dtype=float)
    B = np.array(
        [[-s * f["z"], -s * f["x"]],
         [0.0, -2.0 * s * f["z"]]], dtype=float)
    return A, B


def record_active(f):
    A, B = physical_active(f)
    q = f["eta"] * f["kappa"]
    A = A + np.array(
        [[0.0, 2.0 * q * f["z"] * f["x"]],
         [0.0, -2.0 * q * (1.0 - f["z"] ** 2)]], dtype=float)
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


def rh_one(G):
    tr = float(np.trace(G))
    c1 = -tr
    c2 = 0.5 * (tr * tr - float(np.trace(G @ G)))
    c3 = -float(np.linalg.det(G))
    h = c1 * c2 - c3
    alpha = float(np.max(np.real(np.linalg.eigvals(G))))
    return c1, c2, c3, h, alpha


def normalized_margins(G, scale):
    c1, c2, c3, h, alpha = rh_one(G)
    return {
        "m1": c1 / scale,
        "m2": c2 / (scale ** 2),
        "m3": c3 / (scale ** 3),
        "mh": h / (scale ** 3),
        "normalized_alpha": alpha / scale,
        "c1": c1,
        "c2": c2,
        "c3": c3,
        "h": h,
        "alpha": alpha,
    }


def c3_record_formula(f):
    g = f["gamma"]
    k = f["kappa"]
    q = f["eta"] * f["kappa"]
    w = f["omega"]
    x = f["x"]
    z = f["z"]
    A = 2.0 * (3.0 * g + 2.0 * k + 4.0 * q - 2.0 * q * x * x - 14.0 * q * z * z)
    Bc = 4.0 * q * x * z * (7.0 * g + 6.0 * k + 8.0 * q - 30.0 * q * z * z)
    C = ((g + 2.0 * k - 2.0 * q * z * z)
         * (g + 2.0 * q - 6.0 * q * z * z)
         * (3.0 * g + 2.0 * k + 4.0 * q - 12.0 * q * z * z))
    return A * w * w + Bc * w + C


def relabs_error(a, b):
    return abs(a - b) / max(1.0, abs(a), abs(b))


def mechanism_pattern(m):
    return (
        m["m1"] > MARGIN_TOL
        and m["m2"] > MARGIN_TOL
        and m["m3"] < -MARGIN_TOL
        and m["mh"] > MARGIN_TOL
    )


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


# Y0: deterministic fresh input generation.
inputs_a = generate_inputs()
inputs_b = generate_inputs()
input_bytes = canonical_bytes(inputs_a)
input_sha_a = hashlib.sha256(input_bytes).hexdigest()
input_sha_b = hashlib.sha256(canonical_bytes(inputs_b)).hexdigest()
INPUTS_FILE.write_bytes(input_bytes)
Y0 = input_sha_a == input_sha_b and len(inputs_a) == N

# Stage A: physical channel only. No record channel is constructed above this line.
a = arrays(inputs_a)
Gp = batch_G(a["gamma"], a["kappa"], a["omega"], a["eta"], a["x"], a["z"], record=False)
pc1, pc2, pc3, ph, alpha_p = rh_batch(Gp)
scale = a["gamma"] + a["kappa"] + a["omega"] + a["eta"] * a["kappa"]
norm_p = alpha_p / scale
eligible_idx = np.where(norm_p < -ROBUST_TOL)[0]

stageA_payload = {
    "schema": "stability-arc-c3-gate-stageA-v0.1",
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
Y1 = len(eligible_idx) >= MIN_STAGE_A

# Freeze verification before same-record reveal.
assert hashlib.sha256(STAGE_A.read_bytes()).hexdigest() == stageA_sha
frozen = json.loads(STAGE_A.read_text(encoding="utf-8"))
frozen_ids = [row["id"] for row in frozen["eligible"]]
assert frozen_ids == [inputs_a[int(i)]["id"] for i in eligible_idx]

# Stage B: reveal same-record channel only for immutable Stage-A set.
sel = {k: a[k][eligible_idx] for k in a}
Gr = batch_G(sel["gamma"], sel["kappa"], sel["omega"], sel["eta"], sel["x"], sel["z"], record=True)
rc1, rc2, rc3, rh, alpha_r = rh_batch(Gr)
scale_sel = scale[eligible_idx]
norm_r = alpha_r / scale_sel
cross_local = np.where(norm_r > ROBUST_TOL)[0]
Y2 = len(frozen_ids) == len(eligible_idx)

analytic_crossings = []
formula_errors = []
for j0 in cross_local:
    j = int(j0)
    idx = int(eligible_idx[j])
    f = inputs_a[idx]
    sc = float(scale[idx])
    margins = {
        "m1": float(rc1[j] / sc),
        "m2": float(rc2[j] / (sc ** 2)),
        "m3": float(rc3[j] / (sc ** 3)),
        "mh": float(rh[j] / (sc ** 3)),
    }
    formula = float(c3_record_formula(f))
    ferr = relabs_error(float(rc3[j]), formula)
    formula_errors.append(ferr)
    analytic_crossings.append({
        "id": f["id"],
        "candidate_index": idx + 1,
        "parameters": f,
        "normalized_alpha_phys": float(norm_p[idx]),
        "normalized_alpha_rec": float(norm_r[j]),
        "record_margins": margins,
        "record_c3_direct": float(rc3[j]),
        "record_c3_formula": formula,
        "record_c3_formula_error": ferr,
        "analytic_c3_gate_pattern": bool(
            margins["m1"] > MARGIN_TOL
            and margins["m2"] > MARGIN_TOL
            and margins["m3"] < -MARGIN_TOL
            and margins["mh"] > MARGIN_TOL
        ),
    })

Y4 = all(e <= C3_FORMULA_TOL for e in formula_errors)

# Y3/Y5: independent full-Hilbert reconstruction of every analytic crossing.
reconstruction = []
for c in analytic_crossings:
    f = c["parameters"]
    reasons = []
    state, Aphys3, Arec3, B3, Vt = full_reconstruct(f)
    rho_min = float(np.min(np.linalg.eigvalsh(state)))
    _, D = dark_space(Aphys3, Vt)
    if rho_min <= 0.0:
        reasons.append("NONPOSITIVE_DENSITY")
    if D.shape[1] != 1:
        reasons.append("DARK_DIMENSION")

    dark_res = {}
    inter = {}
    matrix_error = math.inf
    lift_error = math.inf
    rec_margins = None
    phys_norm = math.inf
    rec_norm = math.inf
    margin_error = math.inf
    formula_error = math.inf

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

        Ap_an, B_an = physical_active(f)
        Ar_an, _ = record_active(f)
        matrix_error = max(max_abs(Ap - Ap_an), max_abs(Ar - Ar_an), max_abs(Bp - B_an))
        if matrix_error > DARK_TOL:
            reasons.append("ANALYTIC_RECONSTRUCTION")

        Gpr = sym_generator(Ap, Bp)
        Grr = sym_generator(Ar, Bp)
        lift_error = max(
            max_abs(Gpr - sym_generator_kron(Ap, Bp)),
            max_abs(Grr - sym_generator_kron(Ar, Bp)),
        )
        if lift_error > LIFT_TOL:
            reasons.append("MOMENT_LIFT")

        sc = f["gamma"] + f["kappa"] + f["omega"] + f["eta"] * f["kappa"]
        pm = normalized_margins(Gpr, sc)
        rec_margins = normalized_margins(Grr, sc)
        phys_norm = pm["normalized_alpha"]
        rec_norm = rec_margins["normalized_alpha"]
        if not phys_norm < -ROBUST_TOL:
            reasons.append("PHYSICAL_CLASS_REPLAY")
        if not rec_norm > ROBUST_TOL:
            reasons.append("RECORD_CLASS_REPLAY")

        analytic_m = c["record_margins"]
        margin_error = max(
            abs(rec_margins["m1"] - analytic_m["m1"]),
            abs(rec_margins["m2"] - analytic_m["m2"]),
            abs(rec_margins["m3"] - analytic_m["m3"]),
            abs(rec_margins["mh"] - analytic_m["mh"]),
        )
        if margin_error > MARGIN_RECON_TOL:
            reasons.append("MARGIN_RECONSTRUCTION")

        formula_error = relabs_error(rec_margins["c3"], c3_record_formula(f))
        if formula_error > C3_FORMULA_TOL:
            reasons.append("C3_FORMULA_RECONSTRUCTION")

    pattern = False if rec_margins is None else mechanism_pattern(rec_margins)
    reconstruction.append({
        "id": c["id"],
        "valid": len(reasons) == 0,
        "reasons": reasons,
        "rho_min": rho_min,
        "dark_residuals": dark_res,
        "intertwining_residuals": inter,
        "matrix_error": matrix_error,
        "lift_error": lift_error,
        "margin_error": margin_error,
        "c3_formula_error": formula_error,
        "normalized_alpha_phys": phys_norm,
        "normalized_alpha_rec": rec_norm,
        "record_margins_reconstructed": rec_margins,
        "c3_gate_pattern": bool(pattern),
    })

Y3 = len(reconstruction) == len(analytic_crossings) and all(r["valid"] for r in reconstruction)
Y5 = all(r["c3_gate_pattern"] for r in reconstruction if r["valid"])
mechanism_counterexamples = [r for r in reconstruction if r["valid"] and not r["c3_gate_pattern"]]

# Y6 frozen controls.
control_f = {"gamma": 1.0, "kappa": 10.0, "omega": 20.0, "eta": 0.0, "x": 0.1, "y": 0.0, "z": -0.95}
Ac_p, Bc = physical_active(control_f)
Ac_r, _ = record_active(control_f)
Gcp = sym_generator(Ac_p, Bc)
Gcr = sym_generator(Ac_r, Bc)
eta0_identity = max_abs(Gcp - Gcr) <= 1e-12

G_c3_only = np.diag([-1.0, -2.0, 0.5])
G_multi = np.diag([-1.0, -2.0, 1.0])
G_boundary = np.diag([-1.0, -2.0, 0.0])
c3_only_pattern = mechanism_pattern(normalized_margins(G_c3_only, 1.0))
multi_pattern = mechanism_pattern(normalized_margins(G_multi, 1.0))
boundary_c3 = rh_one(G_boundary)[2]
boundary_ok = abs(boundary_c3) <= 1e-12
Y6 = eta0_identity and c3_only_pattern and (not multi_pattern) and boundary_ok

criteria = {
    "Y0": {"status": "PASS" if Y0 else "FAIL", "candidate_input_sha256": input_sha_a},
    "Y1": {"status": "PASS" if Y1 else "FAIL", "eligible_count": int(len(eligible_idx)), "stageA_sha256": stageA_sha},
    "Y2": {"status": "PASS" if Y2 else "FAIL", "revealed_count": int(len(eligible_idx)), "analytic_crossing_count": int(len(analytic_crossings))},
    "Y3": {"status": "PASS" if Y3 else "FAIL", "reconstructed_count": int(sum(r["valid"] for r in reconstruction)), "required_count": int(len(analytic_crossings))},
    "Y4": {"status": "PASS" if Y4 else "FAIL", "max_c3_formula_error": max(formula_errors) if formula_errors else 0.0},
    "Y5": {"status": "PASS" if Y5 else "FAIL", "counterexample_count": len(mechanism_counterexamples), "minimum_crossings_for_promotion": MIN_CROSSINGS},
    "Y6": {"status": "PASS" if Y6 else "FAIL", "eta0_identity": eta0_identity, "c3_only_control": c3_only_pattern, "multi_gate_control_rejected": not multi_pattern, "boundary_control": boundary_ok},
}

if not Y0 or not Y2 or not Y4 or not Y6:
    status = "AUDIT_FAILURE"
elif not Y1:
    status = "SELECTION_HOLD"
elif not Y3:
    status = "RECONSTRUCTION_HOLD"
elif len(mechanism_counterexamples) > 0:
    status = "FAIL_C3_GATE_H5"
elif len(reconstruction) < MIN_CROSSINGS:
    status = "INSUFFICIENT_CROSSINGS_H5"
elif Y5:
    status = "PASS_PROSPECTIVE_C3_GATE_H5"
else:
    status = "AUDIT_FAILURE"

result = {
    "schema": "stability-arc-c3-gate-crossing-test-v0.1",
    "phase_status": status,
    "scope": "FRESH_MECHANISM_TEST",
    "environment": {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "platform": platform.platform(),
    },
    "frozen_parameters": {
        "seed": SEED,
        "n_candidates": N,
        "robust_alpha_tolerance": ROBUST_TOL,
        "normalized_margin_tolerance": MARGIN_TOL,
        "minimum_stageA": MIN_STAGE_A,
        "minimum_crossings_for_promotion": MIN_CROSSINGS,
    },
    "criteria": criteria,
    "analytic_crossings": analytic_crossings,
    "reconstruction": reconstruction,
    "mechanism_counterexamples": mechanism_counterexamples,
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({
    "phase_status": status,
    "eligible_count": int(len(eligible_idx)),
    "analytic_crossing_count": int(len(analytic_crossings)),
    "reconstructed_count": int(sum(r["valid"] for r in reconstruction)),
    "counterexample_count": len(mechanism_counterexamples),
    "max_c3_formula_error": max(formula_errors) if formula_errors else 0.0,
    "criteria": criteria,
}, indent=2, sort_keys=True))

raise SystemExit(0 if status in {"PASS_PROSPECTIVE_C3_GATE_H5", "FAIL_C3_GATE_H5", "INSUFFICIENT_CROSSINGS_H5"} else 1)
