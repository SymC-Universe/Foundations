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
OUT = RESULTS / "c1_corrected_map_test_v01.json"
STAGE_A = RESULTS / "stageA_c1_corrected_selection.json"
STAGE_A_SHA = RESULTS / "stageA_c1_corrected_selection.sha256"

SEED = 2026082912
N = 500000
MAX_PER_CLASS = 512
MIN_PER_CLASS = 128
MAP_TOL = 1e-8
C1_TOL = 1e-8
RH_TOL = 1e-9
RECON_TOL = 2e-10

SYM_BASIS = [
    np.array([[1.0, 0.0], [0.0, 0.0]], dtype=float),
    np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float),
    np.array([[0.0, 0.0], [0.0, 1.0]], dtype=float),
]


def max_abs(x):
    a = np.asarray(x)
    return 0.0 if a.size == 0 else float(np.max(np.abs(a)))


def relabs(a, b):
    return abs(a - b) / max(1.0, abs(a), abs(b))


def generate_arrays():
    rng = np.random.default_rng(SEED)
    kappa = 10.0 ** rng.uniform(math.log10(0.2), math.log10(100.0), N)
    eta = rng.uniform(0.001, 0.95, N)
    r = rng.uniform(0.05, 0.98, N)
    theta = rng.uniform(0.0, 2.0 * math.pi, N)
    omega = 10.0 ** rng.uniform(-3.0, 3.0, N)
    x = r * np.cos(theta)
    z = r * np.sin(theta)
    gamma = np.ones(N, dtype=float)
    q = eta * kappa
    return {"gamma": gamma, "kappa": kappa, "eta": eta, "r": r, "theta": theta, "omega": omega, "x": x, "z": z, "q": q}


def array_sha256(a):
    h = hashlib.sha256()
    h.update(f"seed={SEED};n={N};schema=c1-corrected-map-v0.1\n".encode("ascii"))
    for key in ["gamma", "kappa", "eta", "r", "theta", "omega", "x", "z", "q"]:
        h.update(key.encode("ascii") + b"\0")
        h.update(np.asarray(a[key], dtype="<f8").tobytes(order="C"))
    return h.hexdigest()


def c3_coeff_arrays(a, record=False):
    g, k, q, x, z = a["gamma"], a["kappa"], a["q"], a["x"], a["z"]
    if not record:
        A = 2.0 * (3.0 * g + 2.0 * k - 2.0 * q * x * x - 10.0 * q * z * z)
        B = 16.0 * q * x * z * (g + k - 3.0 * q * z * z)
        C = ((g - 4.0 * q * z * z) * (3.0 * g + 2.0 * k - 8.0 * q * z * z) * (g + 2.0 * k - 2.0 * q * z * z))
    else:
        A = 2.0 * (3.0 * g + 2.0 * k + 4.0 * q - 2.0 * q * x * x - 14.0 * q * z * z)
        B = 4.0 * q * x * z * (7.0 * g + 6.0 * k + 8.0 * q - 30.0 * q * z * z)
        C = ((g + 2.0 * k - 2.0 * q * z * z) * (g + 2.0 * q - 6.0 * q * z * z) * (3.0 * g + 2.0 * k + 4.0 * q - 12.0 * q * z * z))
    return A, B, C


def c3_coeff_scalar(g, k, q, x, z, record=False):
    if not record:
        A = 2.0 * (3.0 * g + 2.0 * k - 2.0 * q * x * x - 10.0 * q * z * z)
        B = 16.0 * q * x * z * (g + k - 3.0 * q * z * z)
        C = ((g - 4.0 * q * z * z) * (3.0 * g + 2.0 * k - 8.0 * q * z * z) * (g + 2.0 * k - 2.0 * q * z * z))
    else:
        A = 2.0 * (3.0 * g + 2.0 * k + 4.0 * q - 2.0 * q * x * x - 14.0 * q * z * z)
        B = 4.0 * q * x * z * (7.0 * g + 6.0 * k + 8.0 * q - 30.0 * q * z * z)
        C = ((g + 2.0 * k - 2.0 * q * z * z) * (g + 2.0 * q - 6.0 * q * z * z) * (3.0 * g + 2.0 * k + 4.0 * q - 12.0 * q * z * z))
    return float(A), float(B), float(C)


def c3_norm_arrays(coeff, w):
    A, B, C = coeff
    v = (A * w + B) * w + C
    scale = np.maximum(1.0, np.abs(A) * w * w + np.abs(B) * w + np.abs(C))
    return v, v / scale


def c3_scalar(g, k, q, x, z, w, record=False):
    A, B, C = c3_coeff_scalar(g, k, q, x, z, record=record)
    v = (A * w + B) * w + C
    scale = max(1.0, abs(A) * w * w + abs(B) * w + abs(C))
    return v, v / scale


def c1_phys_scalar(g, k, q, z):
    return 4.5 * g + 3.0 * k - 14.0 * q * z * z


def c1_rec_scalar(g, k, q, z):
    return 4.5 * g + 3.0 * k + 6.0 * q - 20.0 * q * z * z


def row_from_index(a, i, label, sp, sr, u1p):
    return {
        "id": f"H7{i+1:06d}",
        "candidate_index": int(i + 1),
        "selection_class": label,
        "gamma": float(a["gamma"][i]),
        "kappa": float(a["kappa"][i]),
        "eta": float(a["eta"][i]),
        "omega": float(a["omega"][i]),
        "x": float(a["x"][i]),
        "z": float(a["z"][i]),
        "q": float(a["q"][i]),
        "stageA_c3_phys_norm": float(sp[i]),
        "stageA_c3_rec_norm": float(sr[i]),
        "stageA_c1_phys_norm": float(u1p[i]),
    }


def active_matrices(f, record=False):
    g, k, q, x, z, w = f["gamma"], f["kappa"], f["q"], f["x"], f["z"], f["omega"]
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


def rh_data(G, R):
    tr = float(np.trace(G))
    c1 = -tr
    c2 = 0.5 * (tr * tr - float(np.trace(G @ G)))
    c3 = -float(np.linalg.det(G))
    mh = c1 * c2 - c3
    margins = {"m1": c1 / R, "m2": c2 / (R * R), "m3": c3 / (R**3), "mh": mh / (R**3)}
    vals = list(margins.values())
    if all(v > RH_TOL for v in vals):
        cls = "STABLE"
    elif any(v < -RH_TOL for v in vals):
        cls = "UNSTABLE"
    else:
        cls = "BOUNDARY"
    return {"c1": c1, "c2": c2, "c3": c3, "mh_raw": mh, "margins": margins, "class": cls}


# T0 exact generator determinism.
a1 = generate_arrays()
a2 = generate_arrays()
sha1 = array_sha256(a1)
sha2 = array_sha256(a2)
T0 = sha1 == sha2

# Stage A: exact c3 plus exact physical c1 only.
cp = c3_coeff_arrays(a1, record=False)
cr = c3_coeff_arrays(a1, record=True)
_, sp = c3_norm_arrays(cp, a1["omega"])
_, sr = c3_norm_arrays(cr, a1["omega"])
Rall = a1["gamma"] + a1["kappa"] + a1["omega"] + a1["q"]
c1p = 4.5 * a1["gamma"] + 3.0 * a1["kappa"] - 14.0 * a1["q"] * a1["z"] * a1["z"]
u1p = c1p / Rall

dest_all = np.where((sp > MAP_TOL) & (sr < -MAP_TOL) & (u1p > C1_TOL))[0]
stab_all = np.where((sp < -MAP_TOL) & (sr > MAP_TOL))[0]
dest_sel = dest_all[:MAX_PER_CLASS]
stab_sel = stab_all[:MAX_PER_CLASS]
selection_sufficient = len(dest_all) >= MIN_PER_CLASS and len(stab_all) >= MIN_PER_CLASS

selected_dest = [row_from_index(a1, int(i), "I_destab_c1", sp, sr, u1p) for i in dest_sel]
selected_stab = [row_from_index(a1, int(i), "I_stab", sp, sr, u1p) for i in stab_sel]
payload = {
    "schema": "stability-arc-c1-corrected-map-stageA-v0.1",
    "seed": SEED,
    "n_candidates": N,
    "candidate_array_sha256": sha1,
    "map_tolerance": MAP_TOL,
    "c1_tolerance": C1_TOL,
    "selection_rule": "first_by_candidate_id",
    "available_counts": {"I_destab_c1": int(len(dest_all)), "I_stab": int(len(stab_all))},
    "selected": {"I_destab_c1": selected_dest, "I_stab": selected_stab},
}
stage_bytes = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"
STAGE_A.write_bytes(stage_bytes)
stage_sha = hashlib.sha256(stage_bytes).hexdigest()
STAGE_A_SHA.write_text(stage_sha + "  stageA_c1_corrected_selection.json\n", encoding="utf-8")
digest_ok = hashlib.sha256(STAGE_A.read_bytes()).hexdigest() == stage_sha
T1 = selection_sufficient and digest_ok

# T2 replay from frozen Stage-A bytes without full G.
frozen = json.loads(STAGE_A.read_text(encoding="utf-8"))
rows = frozen["selected"]["I_destab_c1"] + frozen["selected"]["I_stab"]
replay_failures = []
for f in rows:
    _, spp = c3_scalar(f["gamma"], f["kappa"], f["q"], f["x"], f["z"], f["omega"], record=False)
    _, srr = c3_scalar(f["gamma"], f["kappa"], f["q"], f["x"], f["z"], f["omega"], record=True)
    R = f["gamma"] + f["kappa"] + f["omega"] + f["q"]
    u1 = c1_phys_scalar(f["gamma"], f["kappa"], f["q"], f["z"]) / R
    if f["selection_class"] == "I_destab_c1":
        ok = spp > MAP_TOL and srr < -MAP_TOL and u1 > C1_TOL
    else:
        ok = spp < -MAP_TOL and srr > MAP_TOL
    if not ok:
        replay_failures.append({"id": f["id"], "sp": spp, "sr": srr, "u1p": u1})
T2 = len(replay_failures) == 0

# Stage B full reveal.
recon_failures = []
boundary_rows = []
h7d_counterexamples = []
h7s_counterexamples = []
h7d_blockers = {"m2": 0, "mh": 0}
h7s_blockers = {"m1": 0, "m2": 0, "mh": 0}
correct_d = 0
correct_s = 0
max_recon_error = 0.0

if selection_sufficient and digest_ok and T0 and T2:
    for f in rows:
        Ap, B = active_matrices(f, record=False)
        Ar, _ = active_matrices(f, record=True)
        Gp = sym_generator(Ap, B)
        Gr = sym_generator(Ar, B)
        R = f["gamma"] + f["kappa"] + f["omega"] + f["q"]
        rp = rh_data(Gp, R)
        rr = rh_data(Gr, R)
        c3p_exact, _ = c3_scalar(f["gamma"], f["kappa"], f["q"], f["x"], f["z"], f["omega"], record=False)
        c3r_exact, _ = c3_scalar(f["gamma"], f["kappa"], f["q"], f["x"], f["z"], f["omega"], record=True)
        c1p_exact = c1_phys_scalar(f["gamma"], f["kappa"], f["q"], f["z"])
        c1r_exact = c1_rec_scalar(f["gamma"], f["kappa"], f["q"], f["z"])
        errs = {
            "c1p": relabs(rp["c1"], c1p_exact),
            "c1r": relabs(rr["c1"], c1r_exact),
            "c3p": relabs(rp["c3"], c3p_exact),
            "c3r": relabs(rr["c3"], c3r_exact),
        }
        max_recon_error = max(max_recon_error, *errs.values())
        if max(errs.values()) > RECON_TOL:
            recon_failures.append({"id": f["id"], "errors": errs})
        rec = {"id": f["id"], "selection_class": f["selection_class"], "physical": rp, "record": rr, "reconstruction_errors": errs}
        if rp["class"] == "BOUNDARY" or rr["class"] == "BOUNDARY":
            boundary_rows.append(rec)
            continue
        if f["selection_class"] == "I_destab_c1":
            if rp["class"] == "STABLE" and rr["class"] == "UNSTABLE":
                correct_d += 1
            else:
                blockers = []
                if rp["margins"]["m2"] <= RH_TOL:
                    blockers.append("m2"); h7d_blockers["m2"] += 1
                if rp["margins"]["mh"] <= RH_TOL:
                    blockers.append("mh"); h7d_blockers["mh"] += 1
                h7d_counterexamples.append({**rec, "blocking_margins": blockers})
        else:
            if rp["class"] == "UNSTABLE" and rr["class"] == "STABLE":
                correct_s += 1
            else:
                blockers = []
                for name in ["m1", "m2", "mh"]:
                    if rr["margins"][name] <= RH_TOL:
                        blockers.append(name); h7s_blockers[name] += 1
                h7s_counterexamples.append({**rec, "blocking_margins": blockers})

T3 = len(recon_failures) == 0 and max_recon_error <= RECON_TOL
T4 = len(boundary_rows) == 0
T5 = len(h7d_counterexamples) == 0 and selection_sufficient
T6 = len(h7s_counterexamples) == 0 and selection_sufficient

# T7 fixed controls.
f0 = {"gamma": 1.0, "kappa": 1.2, "eta": 0.0, "q": 0.0, "omega": 0.7, "x": 0.2, "z": 0.3}
A0p, B0 = active_matrices(f0, record=False)
A0r, _ = active_matrices(f0, record=True)
eta_zero_ok = max(max_abs(A0p - A0r), max_abs(B0 - B0)) <= 1e-15
Gstable = np.diag([-1.0, -2.0, -3.0])
Gunstable = np.diag([0.2, -1.0, -2.0])
Gboundary = np.diag([0.0, -1.0, -2.0])
classifier_ok = rh_data(Gstable, 1.0)["class"] == "STABLE" and rh_data(Gunstable, 1.0)["class"] == "UNSTABLE" and rh_data(Gboundary, 1.0)["class"] == "BOUNDARY"
T7 = eta_zero_ok and classifier_ok

if not T0 or not digest_ok or not T2 or not T7:
    phase_status = "AUDIT_FAILURE"
    h7d_status = "NOT_SCORED"
    h7s_status = "NOT_SCORED"
elif not selection_sufficient:
    phase_status = "SELECTION_HOLD"
    h7d_status = "NOT_SCORED"
    h7s_status = "NOT_SCORED"
elif not T3:
    phase_status = "RECONSTRUCTION_HOLD"
    h7d_status = "NOT_SCORED"
    h7s_status = "NOT_SCORED"
elif not T4:
    phase_status = "BOUNDARY_HOLD"
    h7d_status = "NOT_SCORED"
    h7s_status = "NOT_SCORED"
else:
    h7d_status = "PASS_H7D_C1_CORRECTED_DESTAB" if T5 else "FAIL_H7D_C1_CORRECTED_DESTAB"
    h7s_status = "PASS_H7S_ISTAB_REPLICATION" if T6 else "FAIL_H7S_ISTAB_REPLICATION"
    phase_status = h7d_status + "__" + h7s_status

nd = len(selected_dest)
ns = len(selected_stab)
result = {
    "schema": "stability-arc-c1-corrected-map-test-v0.1",
    "phase_status": phase_status,
    "h7d_status": h7d_status,
    "h7s_status": h7s_status,
    "environment": {"python": platform.python_version(), "numpy": np.__version__},
    "frozen": {"seed": SEED, "n_candidates": N, "map_tolerance": MAP_TOL, "c1_tolerance": C1_TOL, "rh_tolerance": RH_TOL, "reconstruction_tolerance": RECON_TOL},
    "stageA": {"candidate_array_sha256": sha1, "selection_sha256": stage_sha, "available_counts": payload["available_counts"], "selected_counts": {"I_destab_c1": nd, "I_stab": ns}},
    "criteria": {
        "T0": {"status": "PASS" if T0 else "FAIL"},
        "T1": {"status": "PASS" if T1 else "FAIL", "selection_sufficient": selection_sufficient, "digest_ok": digest_ok},
        "T2": {"status": "PASS" if T2 else "FAIL", "replay_failure_count": len(replay_failures)},
        "T3": {"status": "PASS" if T3 else "FAIL", "reconstruction_failure_count": len(recon_failures), "max_reconstruction_error": max_recon_error},
        "T4": {"status": "PASS" if T4 else "FAIL", "boundary_count": len(boundary_rows)},
        "T5": {"status": "PASS" if T5 else "FAIL", "h7d_counterexamples": len(h7d_counterexamples)},
        "T6": {"status": "PASS" if T6 else "FAIL", "h7s_counterexamples": len(h7s_counterexamples)},
        "T7": {"status": "PASS" if T7 else "FAIL", "eta_zero_identity": eta_zero_ok, "classifier_controls": classifier_ok},
    },
    "performance": {
        "H7D_correct": correct_d,
        "H7D_precision": None if nd == 0 else correct_d / nd,
        "H7D_blockers": h7d_blockers,
        "H7S_correct": correct_s,
        "H7S_precision": None if ns == 0 else correct_s / ns,
        "H7S_blockers": h7s_blockers,
    },
    "replay_failures": replay_failures,
    "reconstruction_failures": recon_failures,
    "boundary_rows": boundary_rows,
    "h7d_counterexamples": h7d_counterexamples,
    "h7s_counterexamples": h7s_counterexamples,
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({
    "phase_status": phase_status,
    "stageA_available": payload["available_counts"],
    "stageA_selected": {"I_destab_c1": nd, "I_stab": ns},
    "H7D_precision": result["performance"]["H7D_precision"],
    "H7D_counterexamples": len(h7d_counterexamples),
    "H7D_blockers": h7d_blockers,
    "H7S_precision": result["performance"]["H7S_precision"],
    "H7S_counterexamples": len(h7s_counterexamples),
    "H7S_blockers": h7s_blockers,
    "boundary_count": len(boundary_rows),
    "max_reconstruction_error": max_recon_error,
}, indent=2, sort_keys=True))
