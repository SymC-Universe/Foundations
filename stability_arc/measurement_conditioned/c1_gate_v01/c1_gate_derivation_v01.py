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
OUT = RESULTS / "c1_gate_derivation_v01.json"

SEED = 2026082911
N = 128
FORMULA_TOL = 2e-12
DIRECTION_TOL = 2e-12
TRANSFORM_TOL = 2e-11
R_ACTIVE = np.array([[1.2, 0.3], [-0.2, 0.9]], dtype=float)

SYM_BASIS_NP = [
    np.array([[1.0, 0.0], [0.0, 0.0]], dtype=float),
    np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float),
    np.array([[0.0, 0.0], [0.0, 1.0]], dtype=float),
]


def relabs(a, b):
    return abs(a - b) / max(1.0, abs(a), abs(b))


def active_matrices(g, k, q, x, z, w, record=False):
    s = math.sqrt(2.0 * q)
    A = np.array([[-(g / 2.0 + k), w], [-w, -g]], dtype=float)
    if record:
        A = A + np.array([[0.0, 2.0 * q * z * x], [0.0, -2.0 * q * (1.0 - z * z)]], dtype=float)
    B = np.array([[-s * z, -s * x], [0.0, -2.0 * s * z]], dtype=float)
    return A, B


def moment_action(A, B, P):
    return A @ P + P @ A.T + B @ P @ B.T


def sym_coords(P):
    return np.array([P[0, 0], 0.5 * (P[0, 1] + P[1, 0]), P[1, 1]], dtype=float)


def sym_generator(A, B):
    return np.column_stack([sym_coords(moment_action(A, B, E)) for E in SYM_BASIS_NP])


def c1_formula(g, k, q, z, record=False):
    if not record:
        return 4.5 * g + 3.0 * k - 14.0 * q * z * z
    return 4.5 * g + 3.0 * k + 6.0 * q - 20.0 * q * z * z


# Symbolic independent construction.
g, k, q, x, z, w = sp.symbols("g k q x z w", real=True)
s = sp.sqrt(2 * q)
Ap = sp.Matrix([[-(g / 2 + k), w], [-w, -g]])
B = sp.Matrix([[-s * z, -s * x], [0, -2 * s * z]])
Ar = Ap + sp.Matrix([[0, 2 * q * z * x], [0, -2 * q * (1 - z**2)]])
SYM_BASIS_SP = [sp.Matrix([[1, 0], [0, 0]]), sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, 0], [0, 1]])]


def sym_generator_sp(A, Bm):
    cols = []
    for E in SYM_BASIS_SP:
        P = sp.expand(A * E + E * A.T + Bm * E * Bm.T)
        cols.append(sp.Matrix([P[0, 0], sp.simplify((P[0, 1] + P[1, 0]) / 2), P[1, 1]]))
    return sp.Matrix.hstack(*cols)


Gp = sym_generator_sp(Ap, B)
Gr = sym_generator_sp(Ar, B)
C0 = Gp.shape == (3, 3) and Gr.shape == (3, 3)

c1p_derived = sp.simplify(-sp.trace(Gp))
c1r_derived = sp.simplify(-sp.trace(Gr))
c1p_target = sp.Rational(9, 2) * g + 3 * k - 14 * q * z**2
c1r_target = sp.Rational(9, 2) * g + 3 * k + 6 * q - 20 * q * z**2
C1_phys = sp.simplify(c1p_derived - c1p_target) == 0
C1_rec = sp.simplify(c1r_derived - c1r_target) == 0
C1 = C1_phys and C1_rec

delta_derived = sp.simplify(c1r_derived - c1p_derived)
delta_target = 6 * q * (1 - z**2)
C2 = sp.simplify(delta_derived - delta_target) == 0

# Fresh clean-room controls.
rng = np.random.default_rng(SEED)
rows = []
max_formula_error = 0.0
max_transform_error = 0.0
direction_failures = 0
for i in range(N):
    gv = float(10.0 ** rng.uniform(math.log10(0.2), math.log10(3.0)))
    kv = float(10.0 ** rng.uniform(math.log10(0.1), math.log10(100.0)))
    eta = float(rng.uniform(0.001, 0.95))
    qv = eta * kv
    rv = float(rng.uniform(0.05, 0.98))
    theta = float(rng.uniform(0.0, 2.0 * math.pi))
    xv = rv * math.cos(theta)
    zv = rv * math.sin(theta)
    wv = float(10.0 ** rng.uniform(-2.0, 2.0))

    Apn, Bn = active_matrices(gv, kv, qv, xv, zv, wv, record=False)
    Arn, _ = active_matrices(gv, kv, qv, xv, zv, wv, record=True)
    Gpn = sym_generator(Apn, Bn)
    Grn = sym_generator(Arn, Bn)
    c1pn = -float(np.trace(Gpn))
    c1rn = -float(np.trace(Grn))
    fp = c1_formula(gv, kv, qv, zv, record=False)
    fr = c1_formula(gv, kv, qv, zv, record=True)
    ep = relabs(c1pn, fp)
    er = relabs(c1rn, fr)
    max_formula_error = max(max_formula_error, ep, er)
    if c1rn + DIRECTION_TOL * max(1.0, abs(c1rn), abs(c1pn)) < c1pn:
        direction_failures += 1

    Rin = np.linalg.inv(R_ACTIVE)
    Apt = Rin @ Apn @ R_ACTIVE
    Art = Rin @ Arn @ R_ACTIVE
    Bt = Rin @ Bn @ R_ACTIVE
    c1pt = -float(np.trace(sym_generator(Apt, Bt)))
    c1rt = -float(np.trace(sym_generator(Art, Bt)))
    etp = relabs(c1pt, c1pn)
    etr = relabs(c1rt, c1rn)
    max_transform_error = max(max_transform_error, etp, etr)
    rows.append({"id": f"C1F{i+1:03d}", "c1_phys": c1pn, "c1_rec": c1rn, "delta": c1rn - c1pn})

C3 = max_formula_error <= FORMULA_TOL
q0_args = (1.0, 1.2, 0.0, 0.2, 0.3, 0.7)
A0p, B0 = active_matrices(*q0_args, record=False)
A0r, _ = active_matrices(*q0_args, record=True)
q0_equal = relabs(-float(np.trace(sym_generator(A0p, B0))), -float(np.trace(sym_generator(A0r, B0)))) <= DIRECTION_TOL
C4 = direction_failures == 0 and q0_equal
C5 = max_transform_error <= TRANSFORM_TOL

overall = C0 and C1 and C2 and C3 and C4 and C5
phase_status = "PASS_C1_GATE_DERIVATION" if overall else "C1_DERIVATION_FAILURE"

result = {
    "schema": "stability-arc-c1-gate-derivation-v0.1",
    "phase_status": phase_status,
    "environment": {"python": platform.python_version(), "numpy": np.__version__, "sympy": sp.__version__},
    "symbolic": {
        "c1_phys": str(sp.factor(c1p_derived)),
        "c1_record": str(sp.factor(c1r_derived)),
        "delta_c1": str(sp.factor(delta_derived)),
    },
    "criteria": {
        "C0": {"status": "PASS" if C0 else "FAIL"},
        "C1": {"status": "PASS" if C1 else "FAIL", "physical": bool(C1_phys), "record": bool(C1_rec)},
        "C2": {"status": "PASS" if C2 else "FAIL"},
        "C3": {"status": "PASS" if C3 else "FAIL", "max_relative_or_absolute_error": max_formula_error, "n_fresh": N},
        "C4": {"status": "PASS" if C4 else "FAIL", "direction_failures": direction_failures, "q0_equality": q0_equal},
        "C5": {"status": "PASS" if C5 else "FAIL", "max_coordinate_transform_error": max_transform_error},
    },
    "fresh_delta_min": min(r["delta"] for r in rows),
    "fresh_delta_max": max(r["delta"] for r in rows),
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
