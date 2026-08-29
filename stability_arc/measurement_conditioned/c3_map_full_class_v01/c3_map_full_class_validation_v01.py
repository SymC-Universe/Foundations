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
OUT = RESULTS / "c3_map_full_class_validation_v01.json"
STAGE_A = RESULTS / "stageA_c3_map_selection.json"
STAGE_A_SHA = RESULTS / "stageA_c3_map_selection.sha256"

SEED = 2026082909
N = 250000
MAX_PER_CLASS = 512
MIN_PER_CLASS = 128
MAP_TOL = 1e-8
RH_TOL = 1e-9
C3_RECON_TOL = 2e-10

SYM_BASIS = [
    np.array([[1.0, 0.0], [0.0, 0.0]], dtype=float),
    np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float),
    np.array([[0.0, 0.0], [0.0, 1.0]], dtype=float),
]


def canonical_bytes(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


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
    return {
        "gamma": gamma,
        "kappa": kappa,
        "eta": eta,
        "r": r,
        "theta": theta,
        "omega": omega,
        "x": x,
        "z": z,
        "q": q,
    }


def array_sha256(a):
    h = hashlib.sha256()
    h.update(f"seed={SEED};n={N};schema=c3-map-full-class-v0.1\n".encode("ascii"))
    for key in ["gamma", "kappa", "eta", "r", "theta", "omega", "x", "z", "q"]:
        h.update(key.encode("ascii") + b"\0")
        h.update(np.asarray(a[key], dtype="<f8").tobytes(order="C"))
    return h.hexdigest()


def c3_coeff_arrays(a, record=False):
    g, k, q, x, z = a["gamma"], a["kappa"], a["q"], a["x"], a["z"]
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
    return A, B, C


def c3_coeff_scalar(g, k, q, x, z, record=False):
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


def normalized_c3_arrays(coeff, w):
    A, B, C = coeff
    value = (A * w + B) * w + C
    scale = np.maximum(1.0, np.abs(A) * w * w + np.abs(B) * w + np.abs(C))
    return value, value / scale


def normalized_c3_scalar(g, k, q, x, z, w, record=False):
    A, B, C = c3_coeff_scalar(g, k, q, x, z, record=record)
    value = (A * w + B) * w + C
    scale = max(1.0, abs(A) * w * w + abs(B) * w + abs(C))
    return value, value / scale


def map_label(sp, sr):
    if sp > MAP_TOL and sr < -MAP_TOL:
        return "I_destab"
    if sp < -MAP_TOL and sr > MAP_TOL:
        return "I_stab"
    return "OTHER"


def row_from_index(a, i, sp, sr, label):
    return {
        "id": f"MV{i + 1:06d}",
        "candidate_index": int(i + 1),
        "map_class": label,
        "gamma": float(a["gamma"][i]),
        "kappa": float(a["kappa"][i]),
        "eta": float(a["eta"][i]),
        "omega": float(a["omega"][i]),
        "x": float(a["x"][i]),
        "z": float(a["z"][i]),
        "q": float(a["q"][i]),
        "normalized_c3_phys_stageA": float(sp[i]),
        "normalized_c3_rec_stageA": float(sr[i]),
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
    mh_raw = c1 * c2 - c3
    margins = {
        "m1": c1 / R,
        "m2": c2 / (R * R),
        "m3": c3 / (R * R * R),
        "mh": mh_raw / (R * R * R),
    }
    vals = list(margins.values())
    if all(v > RH_TOL for v in vals):
        cls = "STABLE"
    elif any(v < -RH_TOL for v in vals):
        cls = "UNSTABLE"
    else:
        cls = "BOUNDARY"
    return {"c1": c1, "c2": c2, "c3": c3, "mh_raw": mh_raw, "margins": margins, "class": cls}


def blocking_margins(side, expected_stable=True):
    m = side["margins"]
    if expected_stable:
        return [name for name in ["m1", "m2", "m3", "mh"] if m[name] <= RH_TOL]
    return []


# V0: exact generator determinism.
a1 = generate_arrays()
a2 = generate_arrays()
sha1 = array_sha256(a1)
sha2 = array_sha256(a2)
V0 = sha1 == sha2

# Stage A: c3 map only. No active matrices or G are constructed above this line.
cp = c3_coeff_arrays(a1, record=False)
cr = c3_coeff_arrays(a1, record=True)
_, sp = normalized_c3_arrays(cp, a1["omega"])
_, sr = normalized_c3_arrays(cr, a1["omega"])

dest_all = np.where((sp > MAP_TOL) & (sr < -MAP_TOL))[0]
stab_all = np.where((sp < -MAP_TOL) & (sr > MAP_TOL))[0]
dest_sel = dest_all[:MAX_PER_CLASS]
stab_sel = stab_all[:MAX_PER_CLASS]
selection_sufficient = len(dest_all) >= MIN_PER_CLASS and len(stab_all) >= MIN_PER_CLASS

selected_dest = [row_from_index(a1, int(i), sp, sr, "I_destab") for i in dest_sel]
selected_stab = [row_from_index(a1, int(i), sp, sr, "I_stab") for i in stab_sel]
stage_payload = {
    "schema": "stability-arc-c3-map-full-class-stageA-v0.1",
    "seed": SEED,
    "n_candidates": N,
    "candidate_array_sha256": sha1,
    "map_tolerance": MAP_TOL,
    "selection_rule": "first_by_candidate_id",
    "max_per_class": MAX_PER_CLASS,
    "min_per_class": MIN_PER_CLASS,
    "available_counts": {"I_destab": int(len(dest_all)), "I_stab": int(len(stab_all))},
    "selected": {"I_destab": selected_dest, "I_stab": selected_stab},
}
stage_bytes = json.dumps(stage_payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"
STAGE_A.write_bytes(stage_bytes)
stage_sha = hashlib.sha256(stage_bytes).hexdigest()
STAGE_A_SHA.write_text(stage_sha + "  stageA_c3_map_selection.json\n", encoding="utf-8")
digest_ok = hashlib.sha256(STAGE_A.read_bytes()).hexdigest() == stage_sha
V1 = selection_sufficient and digest_ok

# V2: map replay from frozen bytes, still using only c3 formulas.
frozen = json.loads(STAGE_A.read_text(encoding="utf-8"))
all_rows = frozen["selected"]["I_destab"] + frozen["selected"]["I_stab"]
map_replay_failures = []
for f in all_rows:
    _, spp = normalized_c3_scalar(f["gamma"], f["kappa"], f["q"], f["x"], f["z"], f["omega"], record=False)
    _, srr = normalized_c3_scalar(f["gamma"], f["kappa"], f["q"], f["x"], f["z"], f["omega"], record=True)
    got = map_label(spp, srr)
    if got != f["map_class"]:
        map_replay_failures.append({"id": f["id"], "expected": f["map_class"], "observed": got, "sp": spp, "sr": srr})
V2 = len(map_replay_failures) == 0

# Stage B: full mean-square reveal on exactly the immutable Stage-A selections.
reconstruction_failures = []
boundary_rows = []
counterexamples = []
correct_counts = {"I_destab": 0, "I_stab": 0}
blocker_counts = {
    "I_destab_physical": {"m1": 0, "m2": 0, "m3": 0, "mh": 0},
    "I_stab_record": {"m1": 0, "m2": 0, "m3": 0, "mh": 0},
}
max_c3_recon_error = 0.0
stageB_records = []

if selection_sufficient and digest_ok and V0 and V2:
    for f in all_rows:
        Ap, Bp = active_matrices(f, record=False)
        Ar, Br = active_matrices(f, record=True)
        Gp = sym_generator(Ap, Bp)
        Gr = sym_generator(Ar, Br)
        R = f["gamma"] + f["kappa"] + f["omega"] + f["q"]
        rp = rh_data(Gp, R)
        rr = rh_data(Gr, R)
        c3p_exact, _ = normalized_c3_scalar(f["gamma"], f["kappa"], f["q"], f["x"], f["z"], f["omega"], record=False)
        c3r_exact, _ = normalized_c3_scalar(f["gamma"], f["kappa"], f["q"], f["x"], f["z"], f["omega"], record=True)
        ep = relabs(rp["c3"], c3p_exact)
        er = relabs(rr["c3"], c3r_exact)
        max_c3_recon_error = max(max_c3_recon_error, ep, er)
        if ep > C3_RECON_TOL or er > C3_RECON_TOL:
            reconstruction_failures.append({"id": f["id"], "error_phys": ep, "error_rec": er})

        rec = {
            "id": f["id"],
            "map_class": f["map_class"],
            "physical": rp,
            "record": rr,
            "c3_reconstruction_error": {"physical": ep, "record": er},
        }
        stageB_records.append(rec)

        if rp["class"] == "BOUNDARY" or rr["class"] == "BOUNDARY":
            boundary_rows.append(rec)
            continue

        if f["map_class"] == "I_destab":
            correct = rp["class"] == "STABLE" and rr["class"] == "UNSTABLE"
            if correct:
                correct_counts["I_destab"] += 1
            else:
                blockers = blocking_margins(rp, expected_stable=True)
                for b in blockers:
                    blocker_counts["I_destab_physical"][b] += 1
                counterexamples.append({**rec, "expected": "physical STABLE -> record UNSTABLE", "blocking_margins": blockers})
        elif f["map_class"] == "I_stab":
            correct = rp["class"] == "UNSTABLE" and rr["class"] == "STABLE"
            if correct:
                correct_counts["I_stab"] += 1
            else:
                blockers = blocking_margins(rr, expected_stable=True)
                for b in blockers:
                    blocker_counts["I_stab_record"][b] += 1
                counterexamples.append({**rec, "expected": "physical UNSTABLE -> record STABLE", "blocking_margins": blockers})

V3 = len(reconstruction_failures) == 0 and max_c3_recon_error <= C3_RECON_TOL
V4 = len(boundary_rows) == 0
V5 = len(counterexamples) == 0 and selection_sufficient

# V6 fixed controls.
f0 = {"gamma": 1.0, "kappa": 1.2, "eta": 0.0, "q": 0.0, "omega": 0.7, "x": 0.2, "z": 0.3}
A0p, B0p = active_matrices(f0, record=False)
A0r, B0r = active_matrices(f0, record=True)
eta_zero_ok = max(max_abs(A0p - A0r), max_abs(B0p - B0r)) <= 1e-15
Gstable = np.diag([-1.0, -2.0, -3.0])
Gunstable = np.diag([0.2, -1.0, -2.0])
Gboundary = np.diag([0.0, -1.0, -2.0])
classifier_ok = (
    rh_data(Gstable, 1.0)["class"] == "STABLE"
    and rh_data(Gunstable, 1.0)["class"] == "UNSTABLE"
    and rh_data(Gboundary, 1.0)["class"] == "BOUNDARY"
)
V6 = eta_zero_ok and classifier_ok

if not V0 or not digest_ok or not V2 or not V6:
    phase_status = "AUDIT_FAILURE"
elif not selection_sufficient:
    phase_status = "SELECTION_HOLD"
elif not V3:
    phase_status = "RECONSTRUCTION_HOLD"
elif not V4:
    phase_status = "BOUNDARY_HOLD"
elif not V5:
    phase_status = "FAIL_C3_MAP_FULL_CLASS_H6"
else:
    phase_status = "PASS_C3_MAP_FULL_CLASS_H6"

n_dest = len(selected_dest)
n_stab = len(selected_stab)
precision_dest = None if n_dest == 0 else correct_counts["I_destab"] / n_dest
precision_stab = None if n_stab == 0 else correct_counts["I_stab"] / n_stab

result = {
    "schema": "stability-arc-c3-map-full-class-validation-v0.1",
    "phase_status": phase_status,
    "environment": {"python": platform.python_version(), "numpy": np.__version__},
    "frozen": {
        "seed": SEED,
        "n_candidates": N,
        "max_per_class": MAX_PER_CLASS,
        "min_per_class": MIN_PER_CLASS,
        "map_tolerance": MAP_TOL,
        "rh_tolerance": RH_TOL,
        "c3_reconstruction_tolerance": C3_RECON_TOL,
    },
    "stageA": {
        "candidate_array_sha256": sha1,
        "selection_sha256": stage_sha,
        "available_counts": stage_payload["available_counts"],
        "selected_counts": {"I_destab": n_dest, "I_stab": n_stab},
    },
    "criteria": {
        "V0": {"status": "PASS" if V0 else "FAIL"},
        "V1": {"status": "PASS" if V1 else "FAIL", "selection_sufficient": selection_sufficient, "digest_ok": digest_ok},
        "V2": {"status": "PASS" if V2 else "FAIL", "map_replay_failure_count": len(map_replay_failures)},
        "V3": {"status": "PASS" if V3 else "FAIL", "reconstruction_failure_count": len(reconstruction_failures), "max_c3_reconstruction_error": max_c3_recon_error},
        "V4": {"status": "PASS" if V4 else "FAIL", "boundary_case_count": len(boundary_rows)},
        "V5": {"status": "PASS" if V5 else "FAIL", "counterexample_count": len(counterexamples)},
        "V6": {"status": "PASS" if V6 else "FAIL", "eta_zero_identity": eta_zero_ok, "classifier_controls": classifier_ok},
    },
    "prospective_performance": {
        "I_destab_correct": correct_counts["I_destab"],
        "I_destab_precision": precision_dest,
        "I_stab_correct": correct_counts["I_stab"],
        "I_stab_precision": precision_stab,
        "blocker_counts": blocker_counts,
    },
    "map_replay_failures": map_replay_failures,
    "reconstruction_failures": reconstruction_failures,
    "boundary_rows": boundary_rows,
    "counterexamples": counterexamples,
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({
    "phase_status": phase_status,
    "stageA_available": stage_payload["available_counts"],
    "stageA_selected": {"I_destab": n_dest, "I_stab": n_stab},
    "counterexample_count": len(counterexamples),
    "boundary_case_count": len(boundary_rows),
    "max_c3_reconstruction_error": max_c3_recon_error,
    "I_destab_precision": precision_dest,
    "I_stab_precision": precision_stab,
    "blocker_counts": blocker_counts,
}, indent=2, sort_keys=True))
