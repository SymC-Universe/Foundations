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
OUT = RESULTS / "planar_measurement_dark_boundary_v01.json"

SEED = 2026082917
N = 256
NEAR_TOL = 1e-8
REAL_TOL = 1e-11
DARK_TOL = 5e-10
INTER_TOL = 5e-10
MOMENT_TOL = 5e-9
NULL_TOL = 1e-9

sx_np = np.array([[0, 1], [1, 0]], dtype=complex)
sy_np = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz_np = np.array([[1, 0], [0, -1]], dtype=complex)
I2_np = np.eye(2, dtype=complex)
sm_np = np.array([[0, 1], [0, 0]], dtype=complex)
BASIS_NP = [0.5 * sx_np, 0.5 * sy_np, 0.5 * sz_np]
PAULI_NP = [sx_np, sy_np, sz_np]
EY = np.array([0.0, 1.0, 0.0])


def max_abs(a):
    arr = np.asarray(a)
    return 0.0 if arr.size == 0 else float(np.max(np.abs(arr)))


def comm(a, b):
    return a @ b - b @ a


def dissipator(c, rho):
    cd = c.conj().T
    cdc = cd @ c
    return c @ rho @ cd - 0.5 * (cdc @ rho + rho @ cdc)


def rho_from_bloch(v):
    return 0.5 * (I2_np + v[0] * sx_np + v[1] * sy_np + v[2] * sz_np)


def coords(op):
    vals = [complex(np.trace(p @ op)) for p in PAULI_NP]
    return np.array([v.real for v in vals]), max(abs(v.imag) for v in vals)


def linear_matrix(action):
    cols = []
    imag = 0.0
    for e in BASIS_NP:
        c, im = coords(action(e))
        cols.append(c)
        imag = max(imag, im)
    return np.column_stack(cols), imag


def measurement_axis(theta):
    return np.array([math.sin(theta), 0.0, math.cos(theta)])


def measurement_operator(theta):
    n = measurement_axis(theta)
    return 0.5 * (n[0] * sx_np + n[2] * sz_np)


def mu(X, rho):
    return float(np.trace(X @ rho).real)


def h_super(X, rho):
    return X @ rho + rho @ X - 2.0 * mu(X, rho) * rho


def delta_h(X, rho, e):
    dm = float(np.trace(X @ e).real)
    return X @ e + e @ X - 2.0 * mu(X, rho) * e - 2.0 * dm * rho


def build(f, X):
    rho = rho_from_bloch(f["base"])
    H = 0.5 * f["omega"] * sy_np
    c = math.sqrt(f["gamma"]) * sm_np
    def L(e):
        return -1j * comm(H, e) + dissipator(c, e) + 2.0 * f["kappa"] * dissipator(X, e)
    A, ia = linear_matrix(L)
    amp = math.sqrt(2.0 * f["eta"] * f["kappa"])
    B, ib = linear_matrix(lambda e: amp * delta_h(X, rho, e))
    h, ih = coords(h_super(X, rho))
    Vt = np.array([[float(np.trace(X @ e).real) for e in BASIS_NP]])
    U = -4.0 * f["eta"] * f["kappa"] * h.reshape(-1, 1)
    Ar = A + U @ Vt
    return rho, A, Ar, B, U, Vt, max(ia, ib, ih, max_abs(np.imag(Ar)))


def dark_space(A, Vt):
    O = np.vstack([Vt, Vt @ A, Vt @ A @ A])
    _, s, vh = np.linalg.svd(O, full_matrices=True)
    rank = int(np.sum(s > NULL_TOL))
    D = vh[rank:].T.copy()
    if D.size:
        D, _ = np.linalg.qr(D)
    return O, s, D, rank


def orth_complement(D):
    _, _, vh = np.linalg.svd(D.T, full_matrices=True)
    C = vh[D.shape[1]:].T.copy()
    C, _ = np.linalg.qr(C)
    return C


def Kfull(A, B):
    n = A.shape[0]
    return np.kron(np.eye(n), A) + np.kron(A, np.eye(n)) + np.kron(B, B)


# ---------- symbolic independent Hilbert-space derivation ----------
I = sp.I
g, k, eta, w, th = sp.symbols("g k eta w th", positive=True, real=True)
rx, ry, rz = sp.symbols("rx ry rz", real=True)
sx = sp.Matrix([[0, 1], [1, 0]])
sy = sp.Matrix([[0, -I], [I, 0]])
sz = sp.Matrix([[1, 0], [0, -1]])
ident = sp.eye(2)
sm = sp.Matrix([[0, 1], [0, 0]])
pauli = [sx, sy, sz]
basis = [sp.Rational(1, 2) * p for p in pauli]
sn = sp.sin(th)
cs = sp.cos(th)
X = sp.Rational(1, 2) * (sn * sx + cs * sz)
H = sp.Rational(1, 2) * w * sy
c = sp.sqrt(g) * sm


def scomm(a, b):
    return a * b - b * a


def sdiss(cop, state):
    cd = cop.conjugate().T
    cdc = cd * cop
    return cop * state * cd - sp.Rational(1, 2) * (cdc * state + state * cdc)


def scoords(op):
    return sp.Matrix([sp.simplify(sp.trace(p * op)) for p in pauli])


def Lsym(e):
    return -I * scomm(H, e) + sdiss(c, e) + 2 * k * sdiss(X, e)

A_sym = sp.Matrix.hstack(*[scoords(Lsym(e)) for e in basis]).applyfunc(sp.trigsimp)
A_target = sp.Matrix([
    [-g/sp.Integer(2) - k*cs**2, 0, w + k*sn*cs],
    [0, -g/sp.Integer(2) - k, 0],
    [-w + k*sn*cs, 0, -g - k*sn**2],
])
P0 = all(sp.trigsimp(A_sym[i, j] - A_target[i, j]) == 0 for i in range(3) for j in range(3))

# Use unscaled n row for rank identity; scaling V by 1/2 does not change rank.
nrow = sp.Matrix([[sn, cs]])
Axz = sp.Matrix([[A_sym[0, 0], A_sym[0, 2]], [A_sym[2, 0], A_sym[2, 2]]])
obs2 = sp.Matrix.vstack(nrow, nrow * Axz)
det_obs = sp.trigsimp(sp.expand_trig(obs2.det()))
delta_target = w - g * sn * cs / 2
P1 = sp.trigsimp(det_obs - delta_target) == 0

ey_sym = sp.Matrix([0, 1, 0])
V_sym = sp.Matrix([[sn/2, 0, cs/2]])
P2 = (sp.simplify((V_sym * ey_sym)[0]) == 0 and
      all(sp.trigsimp(v) == 0 for v in (A_sym * ey_sym - (-g/2-k) * ey_sym)))

rho_sym = sp.Rational(1, 2) * (ident + rx*sx + ry*sy + rz*sz)
mu_sym = sp.simplify(sp.trace(X * rho_sym))

def delta_h_sym(e):
    dm = sp.simplify(sp.trace(X * e))
    return X*e + e*X - 2*mu_sym*e - 2*dm*rho_sym

amp_sym = sp.sqrt(2*eta*k)
B_sym = sp.Matrix.hstack(*[scoords(amp_sym * delta_h_sym(e)) for e in basis]).applyfunc(sp.trigsimp)
ndotr = sn*rx + cs*rz
P3 = all(sp.trigsimp(v) == 0 for v in (B_sym*ey_sym + amp_sym*ndotr*ey_sym))
# Same-record correction is U V^T, so annihilation follows from V^T e_y=0.
P4 = sp.simplify((V_sym * ey_sym)[0]) == 0

# ---------- fresh numerical audit ----------
rng = np.random.default_rng(SEED)
fixtures = []
for i in range(N):
    gamma = float(10.0 ** rng.uniform(math.log10(0.1), math.log10(2.0)))
    kappa = float(10.0 ** rng.uniform(math.log10(0.05), math.log10(2.0)))
    eff = float(rng.uniform(0.05, 0.95))
    omega = float(rng.uniform(0.05, 3.0))
    theta = float(rng.uniform(-math.pi, math.pi))
    rad = float(rng.uniform(0.05, 0.85))
    d = rng.normal(size=3)
    d = d / np.linalg.norm(d)
    fixtures.append({"id": f"PM{i+1:03d}", "gamma": gamma, "kappa": kappa, "eta": eff,
                     "omega": omega, "theta": theta, "base": (rad*d).tolist()})

near = []
failures = []
max_dark = max_stoch = max_inter = max_moment = max_axis = max_imag = 0.0
scored = 0
for f in fixtures:
    delta = f["omega"] - 0.5*f["gamma"]*math.sin(f["theta"])*math.cos(f["theta"])
    norm_delta = abs(delta)/(f["gamma"] + f["omega"])
    Xn = measurement_operator(f["theta"])
    rho, A, Ar, B, U, Vt, imag = build(f, Xn)
    max_imag = max(max_imag, imag)
    O, svals, D, rank = dark_space(A, Vt)
    if norm_delta <= NEAR_TOL:
        near.append({"id": f["id"], "normalized_delta": norm_delta, "rank": rank, "dark_dim": int(D.shape[1])})
        continue
    scored += 1
    reasons = []
    if D.shape[1] != 1:
        reasons.append("DARK_DIMENSION")
        failures.append({"id": f["id"], "reasons": reasons, "rank": rank, "normalized_delta": norm_delta})
        continue
    overlap = abs(float(D[:, 0] @ EY))
    axis_err = abs(1.0 - overlap)
    max_axis = max(max_axis, axis_err)
    Pperp = np.eye(3) - D @ D.T
    dark = max(max_abs(Vt @ D), max_abs(Pperp @ A @ D))
    stoch = max(max_abs(Pperp @ Ar @ D), max_abs(Pperp @ B @ D))
    max_dark = max(max_dark, dark)
    max_stoch = max(max_stoch, stoch)
    if overlap < 1.0 - 1e-10:
        reasons.append("DARK_AXIS")
    if dark > DARK_TOL:
        reasons.append("PHYSICAL_DARK_INVARIANCE")
    if stoch > DARK_TOL:
        reasons.append("STOCHASTIC_DARK_INVARIANCE")
    C = orth_complement(D)
    L = C.T
    Aqp = L @ A @ C
    Aqr = L @ Ar @ C
    Bq = L @ B @ C
    inter = max(max_abs(L@A - Aqp@L), max_abs(L@Ar - Aqr@L), max_abs(L@B - Bq@L))
    moment = max(max_abs(np.kron(L, L) @ Kfull(A, B) - Kfull(Aqp, Bq) @ np.kron(L, L)),
                 max_abs(np.kron(L, L) @ Kfull(Ar, B) - Kfull(Aqr, Bq) @ np.kron(L, L)))
    max_inter = max(max_inter, inter)
    max_moment = max(max_moment, moment)
    if inter > INTER_TOL:
        reasons.append("INTERTWINING")
    if moment > MOMENT_TOL:
        reasons.append("MOMENT_INTERTWINING")
    if reasons:
        failures.append({"id": f["id"], "reasons": reasons, "rank": rank, "normalized_delta": norm_delta})

P5 = len(failures) == 0 and max_imag <= REAL_TOL

# Exact boundary controls.
boundary_controls = [
    {"id": "B1", "theta": math.pi/4, "gamma": 1.0, "omega": 0.25},
    {"id": "B2", "theta": math.pi/6, "gamma": 2.0, "omega": math.sqrt(3.0)/4.0},
]
boundary_records = []
boundary_ok = True
for bc in boundary_controls:
    f = {"gamma": bc["gamma"], "kappa": 0.3, "eta": 0.7, "omega": bc["omega"],
         "theta": bc["theta"], "base": [0.2, 0.1, -0.3]}
    _, A, _, _, _, Vt, _ = build(f, measurement_operator(f["theta"]))
    O, sv, D, rank = dark_space(A, Vt)
    refusal = "REFUSE_QUOTIENT_DIMENSION" if D.shape[1] == 2 else "UNEXPECTED_DARK_DIMENSION"
    delta = f["omega"] - 0.5*f["gamma"]*math.sin(f["theta"])*math.cos(f["theta"])
    good = abs(delta) <= 5e-15 and rank == 1 and D.shape[1] == 2 and refusal == "REFUSE_QUOTIENT_DIMENSION"
    boundary_ok = boundary_ok and good
    boundary_records.append({"id": bc["id"], "delta": delta, "rank": rank, "dark_dim": int(D.shape[1]),
                             "refusal": refusal, "singular_values": [float(v) for v in sv], "pass": good})
# Signed algebraic control only.
signed_delta = -0.25 - 0.5*1.0*math.sin(3*math.pi/4)*math.cos(3*math.pi/4)
signed_ok = abs(signed_delta) <= 5e-15
P6 = boundary_ok and signed_ok

# Generic out-of-plane refusal.
n3 = np.array([1.0, 1.0, 1.0])/math.sqrt(3.0)
X3 = 0.5*(n3[0]*sx_np + n3[1]*sy_np + n3[2]*sz_np)
f3 = {"gamma": 0.3, "kappa": 0.2, "eta": 0.7, "omega": 1.1, "base": [0.2, 0.1, -0.3]}
_, A3, _, _, _, V3, _ = build(f3, X3)
O3, s3, D3, rank3 = dark_space(A3, V3)
ref3 = "REFUSE_NO_1D_DARK_FACTOR" if rank3 == 3 else "UNEXPECTED_OBSERVABILITY_RANK"
P7 = rank3 == 3 and D3.shape[1] == 0 and ref3 == "REFUSE_NO_1D_DARK_FACTOR"

status = "PASS_PLANAR_MEASUREMENT_DARK_BOUNDARY" if all([P0,P1,P2,P3,P4,P5,P6,P7]) else "DERIVATION_OR_ARCHITECTURE_FAILURE"
result = {
    "schema": "stability-arc-planar-measurement-dark-boundary-v0.1",
    "phase_status": status,
    "environment": {"python": platform.python_version(), "numpy": np.__version__, "sympy": sp.__version__},
    "symbolic": {
        "A_phys": str(A_sym),
        "observability_determinant": str(sp.trigsimp(det_obs)),
        "delta_target": "omega-(gamma/2)*sin(theta)*cos(theta)",
        "B_ey": str((B_sym*ey_sym).applyfunc(sp.trigsimp)),
    },
    "criteria": {
        "P0": {"status": "PASS" if P0 else "FAIL"},
        "P1": {"status": "PASS" if P1 else "FAIL"},
        "P2": {"status": "PASS" if P2 else "FAIL"},
        "P3": {"status": "PASS" if P3 else "FAIL"},
        "P4": {"status": "PASS" if P4 else "FAIL"},
        "P5": {"status": "PASS" if P5 else "FAIL", "fresh_total": N, "scored": scored,
               "near_exact_boundary_count": len(near), "failure_count": len(failures),
               "max_dark_error": max_dark, "max_stochastic_error": max_stoch,
               "max_intertwine_error": max_inter, "max_moment_error": max_moment,
               "max_dark_axis_error": max_axis, "max_imag": max_imag},
        "P6": {"status": "PASS" if P6 else "FAIL", "controls": boundary_records,
               "signed_algebraic_delta": signed_delta},
        "P7": {"status": "PASS" if P7 else "FAIL", "rank": rank3, "dark_dim": int(D3.shape[1]),
               "refusal": ref3, "singular_values": [float(v) for v in s3]},
    },
    "near_exact_boundary": near,
    "fresh_failures": failures,
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"phase_status": status, "criteria": result["criteria"]}, indent=2, sort_keys=True))
