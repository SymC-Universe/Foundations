#!/usr/bin/env python3
import hashlib
import json
import math
import platform
from pathlib import Path

import mpmath as mp
import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "c3_displacement_d3_high_precision_v02.json"

SEED = 2026082908
N_BASE = 256
COEF_TOL = 1e-12
SIGN_TOL = 1e-10
DET_TOL = 2e-10
END_TOL = 2e-10
OFFSET_REL = 1e-7
MP_DPS = 80

mp.mp.dps = MP_DPS

SYM_BASIS_NP = [
    np.array([[1.0, 0.0], [0.0, 0.0]], dtype=float),
    np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float),
    np.array([[0.0, 0.0], [0.0, 1.0]], dtype=float),
]

SYM_BASIS_MP = [
    mp.matrix([[1, 0], [0, 0]]),
    mp.matrix([[0, 1], [1, 0]]),
    mp.matrix([[0, 0], [0, 1]]),
]


def mpf_float(x):
    return mp.mpf(repr(float(x)))


def canonical_bytes(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def root_close(a, b):
    return abs(a - b) <= END_TOL * max(1.0, abs(a), abs(b))


def unique_sorted(vals):
    out = []
    for v in sorted(vals):
        if not out or not root_close(v, out[-1]):
            out.append(float(v))
    return out


def generate_bases():
    rng = np.random.default_rng(SEED)
    out = []
    for i in range(N_BASE):
        k = float(10.0 ** rng.uniform(math.log10(0.2), math.log10(100.0)))
        eta = float(rng.uniform(0.001, 0.95))
        r = float(rng.uniform(0.05, 0.98))
        theta = float(rng.uniform(0.0, 2.0 * math.pi))
        x = r * math.cos(theta)
        z = r * math.sin(theta)
        out.append({
            "id": f"BD{i+1:03d}",
            "g": 1.0,
            "k": k,
            "eta": eta,
            "q": eta * k,
            "x": x,
            "z": z,
        })
    return out


def coeff_np(f, record=False):
    g, k, q, x, z = f["g"], f["k"], f["q"], f["x"], f["z"]
    if not record:
        A = 2.0 * (3.0 * g + 2.0 * k - 2.0 * q * x * x - 10.0 * q * z * z)
        B = 16.0 * q * x * z * (g + k - 3.0 * q * z * z)
        C = ((g - 4.0 * q * z * z)
             * (3.0 * g + 2.0 * k - 8.0 * q * z * z)
             * (g + 2.0 * k - 2.0 * q * z * z))
    else:
        A = 2.0 * (3.0 * g + 2.0 * k + 4.0 * q - 2.0 * q * x * x - 14.0 * q * z * z)
        B = 4.0 * q * x * z * (7.0 * g + 6.0 * k + 8.0 * q - 30.0 * q * z * z)
        C = ((g + 2.0 * k - 2.0 * q * z * z)
             * (g + 2.0 * q - 6.0 * q * z * z)
             * (3.0 * g + 2.0 * k + 4.0 * q - 12.0 * q * z * z))
    return float(A), float(B), float(C)


def coeff_mp(f, record=False):
    g = mpf_float(f["g"])
    k = mpf_float(f["k"])
    q = mpf_float(f["q"])
    x = mpf_float(f["x"])
    z = mpf_float(f["z"])
    if not record:
        A = 2 * (3*g + 2*k - 2*q*x*x - 10*q*z*z)
        B = 16*q*x*z*(g + k - 3*q*z*z)
        C = (g - 4*q*z*z)*(3*g + 2*k - 8*q*z*z)*(g + 2*k - 2*q*z*z)
    else:
        A = 2 * (3*g + 2*k + 4*q - 2*q*x*x - 14*q*z*z)
        B = 4*q*x*z*(7*g + 6*k + 8*q - 30*q*z*z)
        C = (g + 2*k - 2*q*z*z)*(g + 2*q - 6*q*z*z)*(3*g + 2*k + 4*q - 12*q*z*z)
    return A, B, C


def poly_np(c, w):
    A, B, C = c
    return (A * w + B) * w + C


def poly_mp(c, w):
    A, B, C = c
    return (A * w + B) * w + C


def poly_scale_np(c, w):
    A, B, C = c
    return max(1.0, abs(A) * w * w + abs(B) * w + abs(C))


def poly_scale_mp(c, w):
    A, B, C = c
    return max(mp.mpf(1), abs(A) * w * w + abs(B) * w + abs(C))


def sign_np(c, w):
    v = poly_np(c, w)
    tol = SIGN_TOL * poly_scale_np(c, w)
    if abs(v) <= tol:
        return "BOUNDARY"
    return "POS" if v > 0 else "NEG"


def sign_value_mp(v, scale):
    tol = mpf_float(SIGN_TOL) * scale
    if abs(v) <= tol:
        return "BOUNDARY"
    return "POS" if v > 0 else "NEG"


def roots_np(c):
    A, B, C = c
    scale = max(1.0, abs(A), abs(B), abs(C))
    tol = COEF_TOL * scale
    if abs(A) <= tol:
        if abs(B) <= tol:
            return []
        raw = [-C / B]
    else:
        disc = B * B - 4.0 * A * C
        dscale = max(1.0, abs(B * B), abs(4.0 * A * C))
        dtol = COEF_TOL * dscale
        if disc < -dtol:
            raw = []
        elif abs(disc) <= dtol:
            raw = [-B / (2.0 * A)]
        else:
            sd = math.sqrt(max(0.0, disc))
            raw = [(-B - sd) / (2.0 * A), (-B + sd) / (2.0 * A)]
    kept = []
    for r in raw:
        if r >= -END_TOL:
            kept.append(0.0 if abs(r) <= END_TOL else float(r))
    return unique_sorted(kept)


def probe_panel(cp, cr):
    roots = unique_sorted(roots_np(cp) + roots_np(cr))
    fixed = [float(v) for v in np.logspace(-3.0, 3.0, 96)]
    adjacent = []
    probes = list(fixed) + roots
    for root in roots:
        eps = OFFSET_REL * max(1.0, abs(root))
        if root - eps >= 0.0:
            probes.append(root - eps)
            adjacent.append(root - eps)
        probes.append(root + eps)
        adjacent.append(root + eps)
    return unique_sorted([p for p in probes if p >= 0.0]), roots, adjacent


def is_root_adjacent(w, adjacent):
    return any(root_close(w, a) for a in adjacent)


def active_np(f, w, record=False):
    g, k, q, x, z = f["g"], f["k"], f["q"], f["x"], f["z"]
    s = math.sqrt(2.0 * q)
    A = np.array([[-(g / 2.0 + k), w], [-w, -g]], dtype=float)
    if record:
        A = A + np.array([[0.0, 2.0*q*z*x], [0.0, -2.0*q*(1.0-z*z)]], dtype=float)
    B = np.array([[-s*z, -s*x], [0.0, -2.0*s*z]], dtype=float)
    return A, B


def sym_coords_np(P):
    return np.array([P[0, 0], 0.5*(P[0, 1]+P[1, 0]), P[1, 1]], dtype=float)


def G_np(f, w, record=False):
    A, B = active_np(f, w, record)
    cols = []
    for P in SYM_BASIS_NP:
        out = A @ P + P @ A.T + B @ P @ B.T
        cols.append(sym_coords_np(out))
    return np.column_stack(cols)


def active_mp(f, w_float, record=False):
    g = mpf_float(f["g"])
    k = mpf_float(f["k"])
    q = mpf_float(f["q"])
    x = mpf_float(f["x"])
    z = mpf_float(f["z"])
    w = mpf_float(w_float)
    s = mp.sqrt(2*q)
    A = mp.matrix([[-(g/2+k), w], [-w, -g]])
    if record:
        A = A + mp.matrix([[0, 2*q*z*x], [0, -2*q*(1-z*z)]])
    B = mp.matrix([[-s*z, -s*x], [0, -2*s*z]])
    return A, B


def G_mp(f, w_float, record=False):
    A, B = active_mp(f, w_float, record)
    cols = []
    for P in SYM_BASIS_MP:
        M = A*P + P*A.T + B*P*B.T
        cols.append([M[0, 0], (M[0, 1]+M[1, 0])/2, M[1, 1]])
    return mp.matrix([[cols[j][i] for j in range(3)] for i in range(3)])


def relabs_np(a, b):
    return abs(a-b) / max(1.0, abs(a), abs(b))


def relabs_mp(a, b):
    return abs(a-b) / max(mp.mpf(1), abs(a), abs(b))


# P0 lineage.
failure_report = ROOT.parent / "c3_displacement_v01" / "FAILURE_SIGNAL_REPORT_v0.1.md"
c3_result = ROOT.parent / "c3_boundary_v01" / "C3_BOUNDARY_DERIVATION_RESULT_v0.1.md"
source_identity = RESULTS / "source_identity.txt"
P0 = failure_report.exists() and c3_result.exists() and source_identity.exists()

# P1 deterministic panel identity.
bases_a = generate_bases()
bases_b = generate_bases()
panel_sha_a = hashlib.sha256(canonical_bytes(bases_a)).hexdigest()
panel_sha_b = hashlib.sha256(canonical_bytes(bases_b)).hexdigest()
P1 = len(bases_a) == N_BASE and panel_sha_a == panel_sha_b

hp_failures = []
hp_sign_disagreements = []
float_failures = []
float_sign_disagreements = []
max_hp_error = mp.mpf(0)
max_float_error = 0.0
nonboundary_checks = 0

for f in bases_a:
    cp_np = coeff_np(f, record=False)
    cr_np = coeff_np(f, record=True)
    cp_mp = coeff_mp(f, record=False)
    cr_mp = coeff_mp(f, record=True)
    probes, roots, adjacent = probe_panel(cp_np, cr_np)

    for w in probes:
        sp = sign_np(cp_np, w)
        sr = sign_np(cr_np, w)
        if sp == "BOUNDARY" or sr == "BOUNDARY":
            continue
        nonboundary_checks += 1

        row_float_failed = False
        for channel, c_np, c_mp, expected_sign in [
            ("physical", cp_np, cp_mp, sp),
            ("record", cr_np, cr_mp, sr),
        ]:
            # Original binary64 diagnostic.
            c_det_np = -float(np.linalg.det(G_np(f, w, record=(channel == "record"))))
            c_poly_np = poly_np(c_np, w)
            e_np = relabs_np(c_det_np, c_poly_np)
            max_float_error = max(max_float_error, e_np)
            det_sign_np = "BOUNDARY" if abs(c_det_np) <= SIGN_TOL * max(1.0, abs(c_det_np)) else ("POS" if c_det_np > 0 else "NEG")
            if det_sign_np != expected_sign:
                float_sign_disagreements.append({"id": f["id"], "channel": channel, "w": w, "expected": expected_sign, "observed": det_sign_np})
            if e_np > DET_TOL or det_sign_np != expected_sign:
                row_float_failed = True

            # Independent 80-decimal determinant reconstruction.
            w_mp = mpf_float(w)
            Ghp = G_mp(f, w, record=(channel == "record"))
            c_det_hp = -mp.det(Ghp)
            c_poly_hp = poly_mp(c_mp, w_mp)
            e_hp = relabs_mp(c_det_hp, c_poly_hp)
            max_hp_error = max(max_hp_error, e_hp)
            hp_sign = sign_value_mp(c_det_hp, poly_scale_mp(c_mp, w_mp))
            poly_sign_hp = sign_value_mp(c_poly_hp, poly_scale_mp(c_mp, w_mp))
            if hp_sign != poly_sign_hp or hp_sign != expected_sign:
                hp_sign_disagreements.append({
                    "id": f["id"], "channel": channel, "w": w,
                    "expected_binary64_quadratic_sign": expected_sign,
                    "high_precision_determinant_sign": hp_sign,
                    "high_precision_quadratic_sign": poly_sign_hp,
                })
            if e_hp > mpf_float(DET_TOL):
                hp_failures.append({
                    "id": f["id"], "channel": channel, "w": w,
                    "error": mp.nstr(e_hp, 30),
                    "determinant": mp.nstr(c_det_hp, 40),
                    "quadratic": mp.nstr(c_poly_hp, 40),
                })

        if row_float_failed:
            float_failures.append({
                "id": f["id"],
                "w": w,
                "root_adjacent": is_root_adjacent(w, adjacent),
            })

P2 = len(hp_failures) == 0 and max_hp_error <= mpf_float(DET_TOL)
P3 = len(hp_sign_disagreements) == 0
P4 = len(float_sign_disagreements) == 0 and all(row["root_adjacent"] for row in float_failures)
P5 = (len(float_failures) == 0) or (max_hp_error < mpf_float(max_float_error))

criteria = {
    "P0": {"status": "PASS" if P0 else "FAIL"},
    "P1": {"status": "PASS" if P1 else "FAIL", "panel_sha256": panel_sha_a, "base_count": len(bases_a)},
    "P2": {
        "status": "PASS" if P2 else "FAIL",
        "nonboundary_probe_pairs": nonboundary_checks,
        "high_precision_failure_count": len(hp_failures),
        "max_high_precision_relative_or_absolute_error": mp.nstr(max_hp_error, 30),
        "unchanged_gate": DET_TOL,
    },
    "P3": {"status": "PASS" if P3 else "FAIL", "high_precision_sign_disagreements": len(hp_sign_disagreements)},
    "P4": {
        "status": "PASS" if P4 else "FAIL",
        "binary64_failed_probe_count": len(float_failures),
        "binary64_sign_disagreements": len(float_sign_disagreements),
        "all_binary64_failures_root_adjacent": all(row["root_adjacent"] for row in float_failures),
        "historical_expected_failed_probe_count_diagnostic": 16,
        "max_binary64_relative_or_absolute_error": max_float_error,
    },
    "P5": {"status": "PASS" if P5 else "FAIL", "strict_precision_improvement": bool(P5)},
}

status = "PASS_D3_HIGH_PRECISION_REMEDIATION" if all([P0, P1, P2, P3, P4, P5]) else "HIGH_PRECISION_D3_FAILURE"

result = {
    "schema": "stability-arc-c3-displacement-d3-high-precision-v0.2",
    "phase_status": status,
    "scope": "NUMERICAL_ORACLE_REMEDIATION_ONLY",
    "environment": {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "mpmath": mp.__version__,
        "mp_dps": MP_DPS,
        "platform": platform.platform(),
    },
    "frozen_parameters": {
        "seed": SEED,
        "n_base": N_BASE,
        "determinant_gate": DET_TOL,
        "coefficient_tolerance": COEF_TOL,
        "boundary_sign_tolerance": SIGN_TOL,
        "endpoint_tolerance": END_TOL,
        "root_offset_relative": OFFSET_REL,
    },
    "criteria": criteria,
    "binary64_failure_probes": float_failures,
    "binary64_sign_disagreements": float_sign_disagreements,
    "high_precision_failures": hp_failures,
    "high_precision_sign_disagreements": hp_sign_disagreements,
    "interpretation": "V0_1_FAILURE_PRESERVED_HIGH_PRECISION_D3_REMEDIATION_ONLY",
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"phase_status": status, "criteria": criteria}, indent=2, sort_keys=True))
raise SystemExit(0 if status == "PASS_D3_HIGH_PRECISION_REMEDIATION" else 1)
