#!/usr/bin/env python3
import json
import math
import platform
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "conditioning_structural_stress_audit_v01.json"

SEED = 2026082902
N_STRESS = 4096
NULL_TOL = 1e-10
DARK_TOL = 5e-9
LIFT_TOL = 5e-11
STRUCT_TOL = 2e-10
H2_TOL = 1e-9
RH_TOL = 1e-9

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
    if max(abs(v.imag) for v in vals) > 1e-9:
        raise ValueError("non-real Bloch coordinate")
    return np.array([v.real for v in vals], dtype=float)


def linear_matrix(action):
    return np.column_stack([coords(action(e)) for e in BASIS])


def reconstruct(f):
    state = rho_from_bloch(f["base"])
    Aphys = linear_matrix(lambda e: liouvillian(e, f["gamma"], f["kappa"], f["omega"]))
    amp = math.sqrt(2.0 * f["eta"] * f["kappa"])
    B = amp * linear_matrix(lambda e: delta_h(state, e))
    h = coords(h_super(state))
    Vt = np.array([[float(np.trace(xop @ e).real) for e in BASIS]], dtype=float)
    U = -4.0 * f["eta"] * f["kappa"] * h.reshape(-1, 1)
    Arec = Aphys + U @ Vt
    return state, Aphys, Arec, B, Vt


def registered_active_form(f):
    eta, gamma, kappa, omega = f["eta"], f["gamma"], f["kappa"], f["omega"]
    x, _, z = f["base"]
    q = eta * kappa
    a = gamma / 2.0 + kappa
    s = math.sqrt(2.0 * q)
    Ap = np.array([[-a, omega], [-omega, -gamma]], dtype=float)
    B = np.array([[-s * z, -s * x], [0.0, -2.0 * s * z]], dtype=float)
    DA = np.array([[0.0, 2.0 * q * z * x], [0.0, -2.0 * q * (1.0 - z * z)]], dtype=float)
    DG = np.array(
        [[0.0, 4.0 * q * x * z, 0.0],
         [0.0, -2.0 * q * (1.0 - z * z), 2.0 * q * x * z],
         [0.0, 0.0, -4.0 * q * (1.0 - z * z)]], dtype=float)
    return Ap, Ap + DA, B, DA, DG


def observability_dark(A, Vt):
    O = np.vstack([Vt, Vt @ A, Vt @ A @ A])
    _, s, vh = np.linalg.svd(O, full_matrices=True)
    rank = int(np.sum(s > NULL_TOL))
    D = vh[rank:].T.copy()
    if D.size:
        D, _ = np.linalg.qr(D)
    return s, D


def moment_action(A, B, P):
    return A @ P + P @ A.T + B @ P @ B.T


def sym_coords(P):
    return np.array([P[0, 0], 0.5 * (P[0, 1] + P[1, 0]), P[1, 1]], dtype=float)


def sym_generator(A, B):
    return np.column_stack([sym_coords(moment_action(A, B, E)) for E in SYM_BASIS])


def sym_generator_kron(A, B):
    K = np.kron(np.eye(2), A) + np.kron(A, np.eye(2)) + np.kron(B, B)
    return ELIM @ K @ DUP


def char_coeffs(G):
    p = np.real_if_close(np.poly(G), tol=1000)
    if np.iscomplexobj(p) and max_abs(np.imag(p)) > 1e-8:
        raise ValueError("complex polynomial")
    return np.asarray(np.real(p[1:]), dtype=float)


def spectral_info(G):
    eigs = np.linalg.eigvals(G)
    alpha = float(np.max(np.real(eigs)))
    if alpha < -RH_TOL:
        klass = "STABLE"
    elif abs(alpha) <= RH_TOL:
        klass = "BOUNDARY"
    else:
        klass = "UNSTABLE"
    return klass, alpha


def routh_class(G):
    c1, c2, c3 = [float(x) for x in char_coeffs(G)]
    h = np.array([c1, c2, c3, c1 * c2 - c3])
    if np.all(h > RH_TOL):
        return "STABLE"
    if np.all(h >= -RH_TOL) and np.any(np.abs(h) <= RH_TOL):
        return "BOUNDARY"
    return "UNSTABLE"


def generate_stress():
    rng = np.random.default_rng(SEED)
    out = []
    for i in range(1, N_STRESS + 1):
        eta = float(rng.uniform(0.001, 0.999))
        gamma = float(10.0 ** rng.uniform(-4.0, 0.5))
        kappa = float(10.0 ** rng.uniform(-4.0, 0.5))
        omega = float(10.0 ** rng.uniform(-3.0, 0.7))
        direction = rng.normal(size=3)
        direction = direction / np.linalg.norm(direction)
        if i % 2 == 1:
            u = float(rng.uniform(0.0, 1.0))
            radius = 0.95 * (u ** (1.0 / 3.0))
        else:
            radius = float(rng.uniform(0.90, 0.999))
        base = radius * direction
        out.append({
            "id": f"BS{i:04d}", "eta": eta, "gamma": gamma,
            "kappa": kappa, "omega": omega,
            "base": [float(v) for v in base], "source": "seeded_stress"
        })
    return out


def generate_corners():
    etas = [0.001, 0.999]
    tuples = [(1e-4, 3.0, 1e-3), (3.0, 1e-4, 1e-3), (1e-4, 1e-4, 5.0), (3.0, 3.0, 5.0)]
    states = [[0.04, 0.0, 0.998], [0.04, 0.0, -0.998]]
    out = []
    idx = 1
    for eta in etas:
        for gamma, kappa, omega in tuples:
            for base in states:
                out.append({
                    "id": f"CORNER{idx:02d}", "eta": eta, "gamma": gamma,
                    "kappa": kappa, "omega": omega, "base": list(base), "source": "corner"
                })
                idx += 1
    return out


def symbolic_check():
    q, x, z, a, g, w, lam = sp.symbols("q x z a g w lam", real=True)
    s = sp.sqrt(2 * q)
    Ap = sp.Matrix([[-a, w], [-w, -g]])
    Ar = Ap + sp.Matrix([[0, 2*q*z*x], [0, -2*q*(1-z**2)]])
    B = sp.Matrix([[-s*z, -s*x], [0, -2*s*z]])
    Eb = [sp.Matrix([[1,0],[0,0]]), sp.Matrix([[0,1],[1,0]]), sp.Matrix([[0,0],[0,1]])]
    def G(A):
        cols = []
        for P in Eb:
            M = sp.expand(A*P + P*A.T + B*P*B.T)
            cols.append(sp.Matrix([M[0,0], M[0,1], M[1,1]]))
        return sp.Matrix.hstack(*cols)
    DG = sp.simplify(G(Ar) - G(Ap))
    expected = sp.Matrix([[0,4*q*x*z,0],[0,-2*q*(1-z**2),2*q*x*z],[0,0,-4*q*(1-z**2)]])
    matrix_ok = all(sp.simplify(v) == 0 for v in (DG - expected))
    poly = sp.expand((lam*sp.eye(3)-DG).det())
    expected_poly = sp.expand(lam*(lam+2*q*(1-z**2))*(lam+4*q*(1-z**2)))
    poly_ok = sp.simplify(poly - expected_poly) == 0
    return matrix_ok, poly_ok, str(sp.factor(poly))


def audit_fixture(f):
    state, Aphys, Arec, Bfull, Vt = reconstruct(f)
    rho_min = float(np.min(np.linalg.eigvalsh(state)))
    svals, D = observability_dark(Aphys, Vt)
    reasons = []
    if rho_min <= 0.0:
        reasons.append("NONPOSITIVE_DENSITY")
    if D.shape[1] != 1:
        reasons.append("DARK_DIMENSION")

    dark_res = None
    if D.shape[1] == 1:
        Pperp = np.eye(3) - D @ D.T
        dark_res = {
            "measurement": max_abs(Vt @ D),
            "Aphys": max_abs(Pperp @ Aphys @ D),
            "Arec": max_abs(Pperp @ Arec @ D),
            "B": max_abs(Pperp @ Bfull @ D),
            "active_kernel": max_abs(ACTIVE.T @ D),
        }
        if max(dark_res.values()) > DARK_TOL:
            reasons.append("DARK_INVARIANCE")

    Ap = ACTIVE.T @ Aphys @ ACTIVE
    Ar = ACTIVE.T @ Arec @ ACTIVE
    B = ACTIVE.T @ Bfull @ ACTIVE
    Ap_f, Ar_f, B_f, DA_f, DG_f = registered_active_form(f)
    Gp = sym_generator(Ap, B)
    Gr = sym_generator(Ar, B)
    DG = Gr - Gp

    struct_res = {
        "Aphys": max_abs(Ap - Ap_f),
        "Arec": max_abs(Ar - Ar_f),
        "B": max_abs(B - B_f),
        "DeltaA": max_abs((Ar-Ap) - DA_f),
        "DeltaG": max_abs(DG - DG_f),
    }
    if max(struct_res.values()) > STRUCT_TOL:
        reasons.append("STRUCTURAL_FORMULA")

    lift_err = max(max_abs(Gp-sym_generator_kron(Ap,B)), max_abs(Gr-sym_generator_kron(Ar,B)))
    if lift_err > LIFT_TOL:
        reasons.append("MOMENT_LIFT")

    cp, alpha_p = spectral_info(Gp)
    cr, alpha_r = spectral_info(Gr)
    rp, rr = routh_class(Gp), routh_class(Gr)
    class_ok = cp == rp and cr == rr
    if not class_ok:
        reasons.append("CLASSIFIER_MISMATCH")

    admitted = len(reasons) == 0
    return {
        "id": f["id"], "source": f["source"], "admitted": admitted,
        "reasons": reasons, "parameters": {k:v for k,v in f.items() if k not in ("id","source")},
        "rho_min_eigenvalue": rho_min,
        "observability_singular_values": [float(v) for v in svals],
        "dark_residuals": dark_res,
        "structural_residuals": struct_res,
        "lift_error": lift_err,
        "physical_class": cp, "record_class": cr,
        "alpha_phys": alpha_p, "alpha_rec": alpha_r,
        "delta_alpha": alpha_r-alpha_p,
        "H2_pass": bool(alpha_r <= alpha_p + H2_TOL) if admitted else None,
        "physical_coefficients": [float(v) for v in char_coeffs(Gp)],
        "record_coefficients": [float(v) for v in char_coeffs(Gr)],
    }


sym_matrix_ok, sym_poly_ok, sym_poly = symbolic_check()
stress_a = generate_stress()
stress_b = generate_stress()
S1 = json.dumps(stress_a, sort_keys=True, separators=(",",":")) == json.dumps(stress_b, sort_keys=True, separators=(",",":"))
corners = generate_corners()

records = [audit_fixture(f) for f in stress_a]
corner_records = [audit_fixture(f) for f in corners]
all_records = records + corner_records
admitted_stress = [r for r in records if r["admitted"]]
admitted_corners = [r for r in corner_records if r["admitted"]]
admitted_all = [r for r in all_records if r["admitted"]]

max_struct = max((max(r["structural_residuals"].values()) for r in all_records), default=float("inf"))
S0 = sym_matrix_ok and sym_poly_ok and max_struct <= STRUCT_TOL
S2_stress = len(admitted_stress) >= 4000
S2_corner = len(admitted_corners) == 16
S3 = all(r["lift_error"] <= LIFT_TOL and "CLASSIFIER_MISMATCH" not in r["reasons"] for r in admitted_all)

A0 = np.array([[-0.3,1.0],[-1.0,-0.3]], dtype=float)
B0 = 0.2*np.eye(2)
base_alpha = spectral_info(sym_generator(A0,B0))[1]
controls = {}
for label, delta in [("CTRL_STABILIZE",-0.4),("CTRL_DESTABILIZE",0.8)]:
    DA = np.array([[delta,0.0],[0.0,0.0]], dtype=float)
    G = sym_generator(A0+DA,B0)
    klass, alpha = spectral_info(G)
    controls[label] = {"base_alpha":base_alpha,"updated_alpha":alpha,"delta_alpha":alpha-base_alpha,"updated_class":klass}
S4 = controls["CTRL_STABILIZE"]["delta_alpha"] < 0 and controls["CTRL_DESTABILIZE"]["delta_alpha"] > 0 and controls["CTRL_DESTABILIZE"]["updated_class"] == "UNSTABLE"

counterexamples = [r for r in admitted_all if not r["H2_pass"]]
S5 = len(counterexamples) == 0

if not (S0 and S1 and S3 and S4):
    status = "AUDIT_FAILURE"
elif not S2_stress:
    status = "STRESS_ADMISSION_HOLD"
elif not S2_corner:
    status = "CORNER_ADMISSION_HOLD"
elif not S5:
    status = "FAIL_GENERALIZED_H2"
else:
    status = "PASS_GENERALIZED_H2_STRESS"

deltas = [(r["delta_alpha"],r["id"]) for r in admitted_all]
nearest_phys = sorted([(abs(r["alpha_phys"]),r["id"],r["alpha_phys"]) for r in admitted_all])[:10]
nearest_rec = sorted([(abs(r["alpha_rec"]),r["id"],r["alpha_rec"]) for r in admitted_all])[:10]

payload = {
    "schema":"stability-arc-conditioning-structural-stress-v0.1",
    "scope":"STRUCTURAL_AND_GENERALIZATION_STRESS",
    "phase_status":status,
    "environment":{"python":platform.python_version(),"numpy":np.__version__,"sympy":sp.__version__,"platform":platform.platform()},
    "symbolic":{"deltaG_matrix_identity":sym_matrix_ok,"characteristic_factorization":sym_poly_ok,"factored_polynomial":sym_poly},
    "criteria":{
        "S0":{"status":"PASS" if S0 else "FAIL","max_structural_residual":max_struct},
        "S1":{"status":"PASS" if S1 else "FAIL","seed":SEED,"n_seeded":len(stress_a)},
        "S2":{"status":"PASS" if (S2_stress and S2_corner) else "FAIL","seeded_admitted":len(admitted_stress),"seeded_total":4096,"corner_admitted":len(admitted_corners),"corner_total":16},
        "S3":{"status":"PASS" if S3 else "FAIL","max_lift_error":max((r["lift_error"] for r in admitted_all),default=None)},
        "S4":{"status":"PASS" if S4 else "FAIL","controls":controls},
        "S5":{"status":"PASS" if S5 else "FAIL","counterexample_count":len(counterexamples),"counterexample_ids":[r["id"] for r in counterexamples]},
    },
    "diagnostics":{
        "largest_delta_alpha":max(deltas) if deltas else None,
        "smallest_delta_alpha":min(deltas) if deltas else None,
        "nearest_physical_boundary":nearest_phys,
        "nearest_record_boundary":nearest_rec,
    },
    "refused_seeded":[r for r in records if not r["admitted"]],
    "refused_corners":[r for r in corner_records if not r["admitted"]],
    "counterexamples":counterexamples,
    "stress_records":records,
    "corner_records":corner_records,
    "interpretation_firewall":"A PASS is broad computational evidence within this exact measured-qubit family, not a universal theorem. A FAIL is a boundary signal. Neither licenses localization/collapse prediction, a stochastic chi, channel averaging, or transfer to other measurement/dissipation/Hilbert-space structures."
}
OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
summary = {
    "phase_status":status,
    "criteria":payload["criteria"],
    "symbolic":payload["symbolic"],
    "diagnostics":payload["diagnostics"],
}
print(json.dumps(summary,indent=2,sort_keys=True))
raise SystemExit(0 if status == "PASS_GENERALIZED_H2_STRESS" else 1)
