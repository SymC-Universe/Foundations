#!/usr/bin/env python3
import json
import math
import platform
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "c3_boundary_displacement_audit_v01.json"

SEED = 2026082908
N_BASE = 256
COEF_TOL = 1e-12
SIGN_TOL = 1e-10
DET_TOL = 2e-10
END_TOL = 2e-10
OFFSET_REL = 1e-7

SYM_BASIS = [
    np.array([[1.0, 0.0], [0.0, 0.0]], dtype=float),
    np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float),
    np.array([[0.0, 0.0], [0.0, 1.0]], dtype=float),
]


def max_abs(x):
    a = np.asarray(x)
    return 0.0 if a.size == 0 else float(np.max(np.abs(a)))


def c3_coefficients(g, k, q, x, z, record=False):
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


def poly_value(coeff, w):
    A, B, C = coeff
    return (A * w + B) * w + C


def polynomial_scale(coeff, w):
    A, B, C = coeff
    return max(1.0, abs(A) * w * w + abs(B) * w + abs(C))


def sign_direct(coeff, w):
    val = poly_value(coeff, w)
    tol = SIGN_TOL * polynomial_scale(coeff, w)
    if abs(val) <= tol:
        return "BOUNDARY"
    return "POS" if val > 0.0 else "NEG"


def root_close(a, b):
    return abs(a - b) <= END_TOL * max(1.0, abs(a), abs(b))


def unique_sorted(vals):
    out = []
    for v in sorted(vals):
        if not out or not root_close(v, out[-1]):
            out.append(float(v))
    return out


def polynomial_roots(coeff):
    A, B, C = coeff
    scale = max(1.0, abs(A), abs(B), abs(C))
    tol = COEF_TOL * scale
    if abs(A) <= tol:
        if abs(B) <= tol:
            if abs(C) <= tol:
                return {"status": "REFUSE_IDENTICALLY_ZERO", "kind": "zero", "roots_all": [], "roots_nonnegative": []}
            return {"status": "OK", "kind": "constant", "roots_all": [], "roots_nonnegative": []}
        r = -C / B
        roots_all = [float(r)]
        roots_nonnegative = [0.0 if abs(r) <= END_TOL else float(r)] if r >= -END_TOL else []
        return {"status": "OK", "kind": "linear", "roots_all": roots_all, "roots_nonnegative": unique_sorted(roots_nonnegative)}

    disc = B * B - 4.0 * A * C
    disc_scale = max(1.0, abs(B * B), abs(4.0 * A * C))
    disc_tol = COEF_TOL * disc_scale
    if disc < -disc_tol:
        roots_all = []
        kind = "quadratic_no_real"
    elif abs(disc) <= disc_tol:
        roots_all = [float(-B / (2.0 * A))]
        kind = "quadratic_double"
    else:
        sd = math.sqrt(max(0.0, disc))
        roots_all = [float((-B - sd) / (2.0 * A)), float((-B + sd) / (2.0 * A))]
        roots_all = unique_sorted(roots_all)
        kind = "quadratic_two_real"
    roots_nonnegative = []
    for r in roots_all:
        if r >= -END_TOL:
            roots_nonnegative.append(0.0 if abs(r) <= END_TOL else r)
    return {"status": "OK", "kind": kind, "roots_all": roots_all, "roots_nonnegative": unique_sorted(roots_nonnegative)}


def interval_sample(lo, hi):
    if hi is None:
        return lo + max(1.0, 0.5 * max(1.0, abs(lo)))
    if lo == 0.0:
        return 0.5 * hi
    return 0.5 * (lo + hi)


def sign_partition(coeff):
    roots = polynomial_roots(coeff)
    if roots["status"] != "OK":
        return {**roots, "intervals": [], "boundaries": []}
    bounds = roots["roots_nonnegative"]
    positive_bounds = [r for r in bounds if r > END_TOL]
    intervals = []
    lo = 0.0
    for hi in positive_bounds:
        if hi > lo + END_TOL:
            sample = interval_sample(lo, hi)
            intervals.append({"lo": lo, "hi": hi, "sign": sign_direct(coeff, sample)})
        lo = hi
    sample = interval_sample(lo, None)
    intervals.append({"lo": lo, "hi": None, "sign": sign_direct(coeff, sample)})
    return {**roots, "intervals": intervals, "boundaries": bounds}


def classify_partition(part, w):
    if w < -END_TOL:
        return "OUTSIDE_DOMAIN"
    for r in part.get("boundaries", []):
        if root_close(w, r):
            return "BOUNDARY"
    if part.get("status") != "OK":
        return part["status"]
    for interval in part["intervals"]:
        lo = interval["lo"]
        hi = interval["hi"]
        if w >= lo - END_TOL and (hi is None or w < hi - END_TOL):
            return interval["sign"]
    return "BOUNDARY"


def joint_label(sp, sr):
    if "BOUNDARY" in (sp, sr):
        return "BOUNDARY"
    if sp == "POS" and sr == "NEG":
        return "I_destab"
    if sp == "NEG" and sr == "POS":
        return "I_stab"
    if sp == "POS" and sr == "POS":
        return "I_agree_pos"
    if sp == "NEG" and sr == "NEG":
        return "I_agree_neg"
    return "REFUSE"


def merged_joint_partition(coeff_p, coeff_r):
    pp = sign_partition(coeff_p)
    pr = sign_partition(coeff_r)
    if pp["status"] != "OK" or pr["status"] != "OK":
        return {"status": "REFUSE", "physical": pp, "record": pr, "intervals": [], "boundaries": []}
    bounds = unique_sorted(pp["boundaries"] + pr["boundaries"])
    positive_bounds = [r for r in bounds if r > END_TOL]
    intervals = []
    lo = 0.0
    for hi in positive_bounds:
        if hi > lo + END_TOL:
            sample = interval_sample(lo, hi)
            intervals.append({
                "lo": lo,
                "hi": hi,
                "label": joint_label(sign_direct(coeff_p, sample), sign_direct(coeff_r, sample)),
            })
        lo = hi
    sample = interval_sample(lo, None)
    intervals.append({
        "lo": lo,
        "hi": None,
        "label": joint_label(sign_direct(coeff_p, sample), sign_direct(coeff_r, sample)),
    })
    return {"status": "OK", "physical": pp, "record": pr, "intervals": intervals, "boundaries": bounds}


def classify_joint(part, w):
    if part["status"] != "OK":
        return "REFUSE"
    for r in part["boundaries"]:
        if root_close(w, r):
            return "BOUNDARY"
    for interval in part["intervals"]:
        if w >= interval["lo"] - END_TOL and (interval["hi"] is None or w < interval["hi"] - END_TOL):
            return interval["label"]
    return "BOUNDARY"


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
    return np.column_stack([sym_coords(moment_action(A, B, E)) for E in SYM_BASIS])


def det_c3(g, k, q, x, z, w, record=False):
    A, B = active_matrices(g, k, q, x, z, w, record=record)
    G = sym_generator(A, B)
    return -float(np.linalg.det(G))


def relabs(a, b):
    return abs(a - b) / max(1.0, abs(a), abs(b))


def interval_equal(a, b):
    if a["label"] != b["label"]:
        return False
    if not root_close(a["lo"], b["lo"]):
        return False
    if (a["hi"] is None) != (b["hi"] is None):
        return False
    if a["hi"] is not None and not root_close(a["hi"], b["hi"]):
        return False
    return True


def swap_label(label):
    return {
        "I_destab": "I_stab",
        "I_stab": "I_destab",
        "I_agree_pos": "I_agree_pos",
        "I_agree_neg": "I_agree_neg",
    }.get(label, label)


# D0 lineage: required upstream durable results must exist and source identities must be present.
upstream_c3 = ROOT.parent / "c3_boundary_v01" / "C3_BOUNDARY_DERIVATION_RESULT_v0.1.md"
upstream_h5 = ROOT.parent / "c3_gate_test_v01" / "C3_GATE_CROSSING_RESULT_v0.1.md"
source_identity = RESULTS / "source_identity.txt"
D0 = upstream_c3.exists() and upstream_h5.exists() and source_identity.exists()

# D1 synthetic interval-engine controls.
synthetics = [
    {"name": "w2_minus_1", "coeff": (1.0, 0.0, -1.0), "checks": [(0.0, "NEG"), (1.0, "BOUNDARY"), (2.0, "POS")]},
    {"name": "negative_two_roots", "coeff": (-1.0, 4.0, -3.0), "checks": [(0.0, "NEG"), (1.0, "BOUNDARY"), (2.0, "POS"), (3.0, "BOUNDARY"), (4.0, "NEG")]},
    {"name": "double_root", "coeff": (1.0, -4.0, 4.0), "checks": [(1.0, "POS"), (2.0, "BOUNDARY"), (3.0, "POS")]},
    {"name": "no_real", "coeff": (1.0, 0.0, 1.0), "checks": [(0.0, "POS"), (10.0, "POS")]},
    {"name": "linear", "coeff": (0.0, 2.0, -4.0), "checks": [(1.0, "NEG"), (2.0, "BOUNDARY"), (3.0, "POS")]},
    {"name": "constant_pos", "coeff": (0.0, 0.0, 3.0), "checks": [(0.0, "POS"), (100.0, "POS")]},
    {"name": "constant_neg", "coeff": (0.0, 0.0, -2.0), "checks": [(0.0, "NEG"), (100.0, "NEG")]},
]
synthetic_rows = []
D1 = True
for s in synthetics:
    part = sign_partition(s["coeff"])
    observed = [(w, classify_partition(part, w)) for w, _ in s["checks"]]
    expected = s["checks"]
    ok = all(obs == exp for (_, obs), (_, exp) in zip(observed, expected))
    synthetic_rows.append({"name": s["name"], "ok": ok, "observed": observed, "expected": expected, "partition": part})
    D1 = D1 and ok
zero_part = sign_partition((0.0, 0.0, 0.0))
zero_ok = zero_part["status"] == "REFUSE_IDENTICALLY_ZERO"
D1 = D1 and zero_ok

# D2-D5 fresh clean-room controls.
rng = np.random.default_rng(SEED)
bases = []
for i in range(N_BASE):
    k = float(10.0 ** rng.uniform(math.log10(0.2), math.log10(100.0)))
    eta = float(rng.uniform(0.001, 0.95))
    r = float(rng.uniform(0.05, 0.98))
    theta = float(rng.uniform(0.0, 2.0 * math.pi))
    x = r * math.cos(theta)
    z = r * math.sin(theta)
    bases.append({"id": f"BD{i+1:03d}", "g": 1.0, "k": k, "eta": eta, "q": eta * k, "x": x, "z": z})

fixed_probes = np.logspace(-3.0, 3.0, 96)
partition_disagreements = 0
determinant_disagreements = 0
max_det_error = 0.0
swap_failures = 0
coverage_failures = 0
fresh_rows = []

for f in bases:
    cp = c3_coefficients(f["g"], f["k"], f["q"], f["x"], f["z"], record=False)
    cr = c3_coefficients(f["g"], f["k"], f["q"], f["x"], f["z"], record=True)
    joint = merged_joint_partition(cp, cr)
    swapped = merged_joint_partition(cr, cp)

    swap_ok = joint["status"] == "OK" and swapped["status"] == "OK" and len(joint["intervals"]) == len(swapped["intervals"])
    if swap_ok:
        for a, b in zip(joint["intervals"], swapped["intervals"]):
            expected_b = {"lo": a["lo"], "hi": a["hi"], "label": swap_label(a["label"])}
            if not interval_equal(expected_b, b):
                swap_ok = False
                break
    if not swap_ok:
        swap_failures += 1

    roots = unique_sorted(joint.get("boundaries", []))
    probes = list(float(v) for v in fixed_probes)
    probes.extend(roots)
    for root in roots:
        eps = OFFSET_REL * max(1.0, abs(root))
        if root - eps >= 0.0:
            probes.append(root - eps)
        probes.append(root + eps)
    probes = unique_sorted([p for p in probes if p >= 0.0])

    local_part_bad = 0
    local_det_bad = 0
    local_max_det = 0.0
    labels_seen = set()
    for w in probes:
        sp = sign_direct(cp, w)
        sr = sign_direct(cr, w)
        direct_joint = joint_label(sp, sr)
        partition_joint = classify_joint(joint, w)
        labels_seen.add(partition_joint)
        if direct_joint != partition_joint:
            partition_disagreements += 1
            local_part_bad += 1

        if direct_joint != "BOUNDARY":
            c3p_det = det_c3(f["g"], f["k"], f["q"], f["x"], f["z"], w, record=False)
            c3r_det = det_c3(f["g"], f["k"], f["q"], f["x"], f["z"], w, record=True)
            ep = relabs(c3p_det, poly_value(cp, w))
            er = relabs(c3r_det, poly_value(cr, w))
            local_max_det = max(local_max_det, ep, er)
            max_det_error = max(max_det_error, ep, er)
            det_sp = sign_direct((0.0, 0.0, c3p_det), 0.0)
            det_sr = sign_direct((0.0, 0.0, c3r_det), 0.0)
            if ep > DET_TOL or er > DET_TOL or joint_label(det_sp, det_sr) != direct_joint:
                determinant_disagreements += 1
                local_det_bad += 1

    compatible = {"I_destab", "I_stab", "I_agree_pos", "I_agree_neg", "BOUNDARY"}
    coverage_ok = all(lbl in compatible for lbl in labels_seen)
    if not coverage_ok:
        coverage_failures += 1

    fresh_rows.append({
        "id": f["id"],
        "parameters": f,
        "physical_coefficients": cp,
        "record_coefficients": cr,
        "joint_partition": joint,
        "swap_ok": swap_ok,
        "partition_disagreements": local_part_bad,
        "determinant_disagreements": local_det_bad,
        "max_determinant_error": local_max_det,
        "coverage_ok": coverage_ok,
    })

D2 = partition_disagreements == 0
D3 = determinant_disagreements == 0 and max_det_error <= DET_TOL
D4 = swap_failures == 0
D5 = coverage_failures == 0

criteria = {
    "D0": {"status": "PASS" if D0 else "FAIL"},
    "D1": {"status": "PASS" if D1 else "FAIL", "zero_refusal": zero_ok},
    "D2": {"status": "PASS" if D2 else "FAIL", "fresh_base_count": N_BASE, "partition_disagreements": partition_disagreements},
    "D3": {"status": "PASS" if D3 else "FAIL", "determinant_disagreements": determinant_disagreements, "max_relative_or_absolute_error": max_det_error},
    "D4": {"status": "PASS" if D4 else "FAIL", "swap_failures": swap_failures},
    "D5": {"status": "PASS" if D5 else "FAIL", "coverage_failures": coverage_failures},
}
status = "PASS_C3_BOUNDARY_DISPLACEMENT_MAP" if all([D0, D1, D2, D3, D4, D5]) else "DISPLACEMENT_MAP_FAILURE"

result = {
    "schema": "stability-arc-c3-boundary-displacement-map-v0.1",
    "phase_status": status,
    "scope": "DERIVATION_AND_REPRESENTATION_ONLY",
    "environment": {"python": platform.python_version(), "numpy": np.__version__, "platform": platform.platform()},
    "frozen_parameters": {
        "seed": SEED,
        "n_base": N_BASE,
        "coefficient_tolerance": COEF_TOL,
        "boundary_sign_tolerance": SIGN_TOL,
        "determinant_tolerance": DET_TOL,
        "endpoint_tolerance": END_TOL,
    },
    "criteria": criteria,
    "synthetic_controls": synthetic_rows,
    "fresh_controls": fresh_rows,
    "interpretation": "SET_VALUED_CHANNEL_PRESERVING_C3_DISPLACEMENT_MAP_ONLY",
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"phase_status": status, "criteria": criteria}, indent=2, sort_keys=True))
raise SystemExit(0 if status == "PASS_C3_BOUNDARY_DISPLACEMENT_MAP" else 1)
