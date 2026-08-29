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
OUT = RESULTS / "c3_boundary_derivation_audit_v01.json"

SEED = 2026082906
NUM_TOL = 2e-10

# Symbolic construction from the model, not from the registered c3 targets.
g, k, q, w, x, z, lam = sp.symbols("g k q w x z lam", real=True)
sq = sp.sqrt(2 * q)
Aphys = sp.Matrix([[-(g / 2 + k), w], [-w, -g]])
B = sp.Matrix([[-sq * z, -sq * x], [0, -2 * sq * z]])
Arec = Aphys + sp.Matrix([[0, 2 * q * z * x], [0, -2 * q * (1 - z**2)]])
SYM_BASIS = [
    sp.Matrix([[1, 0], [0, 0]]),
    sp.Matrix([[0, 1], [1, 0]]),
    sp.Matrix([[0, 0], [0, 1]]),
]


def sym_coords(M):
    return sp.Matrix([M[0, 0], sp.expand((M[0, 1] + M[1, 0]) / 2), M[1, 1]])


def build_G(A):
    cols = []
    for P in SYM_BASIS:
        M = sp.expand(A * P + P * A.T + B * P * B.T)
        cols.append(sym_coords(M))
    return sp.Matrix.hstack(*cols)


Gp = build_G(Aphys)
Gr = build_G(Arec)
B0 = Gp.shape == (3, 3) and Gr.shape == (3, 3)


def char_c3(G):
    poly = sp.Poly(sp.expand((lam * sp.eye(3) - G).det()), lam)
    return sp.factor(poly.all_coeffs()[-1])


c3p = sp.factor(char_c3(Gp))
c3r = sp.factor(char_c3(Gr))

Ap = 2 * (3 * g + 2 * k - 2 * q * x**2 - 10 * q * z**2)
Bp = 16 * q * x * z * (g + k - 3 * q * z**2)
Cp = (g - 4 * q * z**2) * (3 * g + 2 * k - 8 * q * z**2) * (g + 2 * k - 2 * q * z**2)

Ar = 2 * (3 * g + 2 * k + 4 * q - 2 * q * x**2 - 14 * q * z**2)
Br = 4 * q * x * z * (7 * g + 6 * k + 8 * q - 30 * q * z**2)
Cr = (g + 2 * k - 2 * q * z**2) * (g + 2 * q - 6 * q * z**2) * (3 * g + 2 * k + 4 * q - 12 * q * z**2)

target_p = sp.expand(Ap * w**2 + Bp * w + Cp)
target_r = sp.expand(Ar * w**2 + Br * w + Cr)
B1p = sp.simplify(sp.expand(c3p - target_p)) == 0
B1r = sp.simplify(sp.expand(c3r - target_r)) == 0
B1 = B1p and B1r

poly_p = sp.Poly(sp.expand(c3p), w)
poly_r = sp.Poly(sp.expand(c3r), w)
coeff_p = [sp.factor(v) for v in poly_p.all_coeffs()]
coeff_r = [sp.factor(v) for v in poly_r.all_coeffs()]
B2 = all(sp.simplify(a - b) == 0 for a, b in zip(coeff_p, [Ap, Bp, Cp])) and all(
    sp.simplify(a - b) == 0 for a, b in zip(coeff_r, [Ar, Br, Cr])
)

B3 = sp.simplify(c3p + Gp.det()) == 0 and sp.simplify(c3r + Gr.det()) == 0

Dp = sp.factor(Bp**2 - 4 * Ap * Cp)
Dr = sp.factor(Br**2 - 4 * Ar * Cr)
rp_minus = (-Bp - sp.sqrt(Dp)) / (2 * Ap)
rp_plus = (-Bp + sp.sqrt(Dp)) / (2 * Ap)
rr_minus = (-Br - sp.sqrt(Dr)) / (2 * Ar)
rr_plus = (-Br + sp.sqrt(Dr)) / (2 * Ar)
fac_p = sp.simplify(sp.expand(Ap * (w - rp_minus) * (w - rp_plus) - target_p))
fac_r = sp.simplify(sp.expand(Ar * (w - rr_minus) * (w - rr_plus) - target_r))
B4 = fac_p == 0 and fac_r == 0

# Fresh implementation controls.
rng = np.random.default_rng(SEED)
num_rows = []
max_error = 0.0


def moment_G_num(A, Bn):
    basis = [
        np.array([[1.0, 0.0], [0.0, 0.0]]),
        np.array([[0.0, 1.0], [1.0, 0.0]]),
        np.array([[0.0, 0.0], [0.0, 1.0]]),
    ]
    cols = []
    for P in basis:
        M = A @ P + P @ A.T + Bn @ P @ Bn.T
        cols.append([M[0, 0], 0.5 * (M[0, 1] + M[1, 0]), M[1, 1]])
    return np.column_stack(cols)


def relabs(a, b):
    return abs(a - b) / max(1.0, abs(a), abs(b))


for i in range(64):
    gn = float(10 ** rng.uniform(-3, 2))
    kn = float(10 ** rng.uniform(-3, 2))
    wn = float(10 ** rng.uniform(-3, 2))
    eta = float(rng.uniform(0.0, 1.0))
    qn = eta * kn
    direction = rng.normal(size=2)
    direction = direction / np.linalg.norm(direction)
    radius = float(rng.uniform(0.0, 0.999))
    xn, zn = [float(v) for v in radius * direction]
    sn = math.sqrt(2 * qn)
    Apn = np.array([[-(gn / 2 + kn), wn], [-wn, -gn]], dtype=float)
    Bn = np.array([[-sn * zn, -sn * xn], [0.0, -2 * sn * zn]], dtype=float)
    Arn = Apn + np.array([[0.0, 2 * qn * zn * xn], [0.0, -2 * qn * (1 - zn * zn)]], dtype=float)
    Gpn = moment_G_num(Apn, Bn)
    Grn = moment_G_num(Arn, Bn)
    direct_p = float(-np.linalg.det(Gpn))
    direct_r = float(-np.linalg.det(Grn))
    Apc = 2 * (3 * gn + 2 * kn - 2 * qn * xn * xn - 10 * qn * zn * zn)
    Bpc = 16 * qn * xn * zn * (gn + kn - 3 * qn * zn * zn)
    Cpc = (gn - 4 * qn * zn * zn) * (3 * gn + 2 * kn - 8 * qn * zn * zn) * (gn + 2 * kn - 2 * qn * zn * zn)
    Arc = 2 * (3 * gn + 2 * kn + 4 * qn - 2 * qn * xn * xn - 14 * qn * zn * zn)
    Brc = 4 * qn * xn * zn * (7 * gn + 6 * kn + 8 * qn - 30 * qn * zn * zn)
    Crc = (gn + 2 * kn - 2 * qn * zn * zn) * (gn + 2 * qn - 6 * qn * zn * zn) * (3 * gn + 2 * kn + 4 * qn - 12 * qn * zn * zn)
    quad_p = Apc * wn * wn + Bpc * wn + Cpc
    quad_r = Arc * wn * wn + Brc * wn + Crc
    ep = relabs(direct_p, quad_p)
    er = relabs(direct_r, quad_r)
    max_error = max(max_error, ep, er)
    num_rows.append({
        "id": f"B5_{i+1:02d}",
        "g": gn, "k": kn, "q": qn, "w": wn, "x": xn, "z": zn,
        "physical_error": ep, "record_error": er,
    })

B5 = max_error <= NUM_TOL

overall = B0 and B1 and B2 and B3 and B4 and B5
status = "PASS_C3_BOUNDARY_DERIVATION" if overall else "DERIVATION_FAILURE"

payload = {
    "schema": "stability-arc-c3-boundary-derivation-v0.1",
    "scope": "DERIVATION_ONLY",
    "phase_status": status,
    "environment": {"python": platform.python_version(), "numpy": np.__version__, "sympy": sp.__version__, "platform": platform.platform()},
    "criteria": {
        "B0": {"status": "PASS" if B0 else "FAIL"},
        "B1": {"status": "PASS" if B1 else "FAIL", "physical": B1p, "record": B1r},
        "B2": {"status": "PASS" if B2 else "FAIL"},
        "B3": {"status": "PASS" if B3 else "FAIL"},
        "B4": {"status": "PASS" if B4 else "FAIL"},
        "B5": {"status": "PASS" if B5 else "FAIL", "max_relative_or_absolute_error": max_error},
    },
    "physical": {
        "A": str(sp.factor(Ap)), "B": str(sp.factor(Bp)), "C": str(sp.factor(Cp)),
        "discriminant": str(Dp),
    },
    "record": {
        "A": str(sp.factor(Ar)), "B": str(sp.factor(Br)), "C": str(sp.factor(Cr)),
        "discriminant": str(Dr),
    },
    "numerical_controls": num_rows,
    "interpretation_firewall": (
        "A PASS licenses the exact channel-specific c3=0 quadratic boundary representation only. Full mean-square class "
        "still requires all Routh-Hurwitz inequalities. No stochastic scalar, localization/collapse claim, or channel average is licensed."
    ),
}
OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"phase_status": status, "criteria": payload["criteria"], "physical": payload["physical"], "record": payload["record"]}, indent=2, sort_keys=True))
raise SystemExit(0 if overall else 1)
