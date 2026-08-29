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
OUT = RESULTS / "dephasing_crossing_transfer_v01.json"
STAGE_A = RESULTS / "stageA_dephasing_crossing_selection.json"
STAGE_A_SHA = RESULTS / "stageA_dephasing_crossing_selection.sha256"

SEED = 2026082920
N_PER = 300000
MAX_FREEZE = 128
MIN_SCORE = 16
MAP_TOL = 1e-8
RH_TOL = 1e-9
RECON_TOL = 2e-8
MATRIX_TOL = 2e-9
MOMENT_TOL = 5e-9
NULL_TOL = 1e-9
SHELLS = [
    ("S1", 0.05, 0.50),
    ("S2", 0.50, 0.90),
    ("S3", 0.90, 0.98),
    ("S4", 0.98, 0.9999),
]

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)
sm = np.array([[0, 1], [0, 0]], dtype=complex)
BASIS = [0.5 * sx, 0.5 * sy, 0.5 * sz]
PAULI = [sx, sy, sz]
SYM_BASIS = [
    np.array([[1.0, 0.0], [0.0, 0.0]], dtype=float),
    np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float),
    np.array([[0.0, 0.0], [0.0, 1.0]], dtype=float),
]


def max_abs(a):
    arr = np.asarray(a)
    return 0.0 if arr.size == 0 else float(np.max(np.abs(arr)))


def relabs(a, b):
    return abs(a - b) / max(1.0, abs(a), abs(b))


def generate_panel():
    rng = np.random.default_rng(SEED)
    panel = []
    for shell, lo, hi in SHELLS:
        gamma = 10.0 ** rng.uniform(math.log10(0.1), math.log10(2.0), N_PER)
        gamma_phi = 10.0 ** rng.uniform(math.log10(0.001), math.log10(2.0), N_PER)
        kappa = 10.0 ** rng.uniform(math.log10(0.05), math.log10(5.0), N_PER)
        eta = rng.uniform(0.01, 0.95, N_PER)
        omega = 10.0 ** rng.uniform(math.log10(0.02), math.log10(10.0), N_PER)
        theta = rng.uniform(-math.pi, math.pi, N_PER)
        radius = rng.uniform(lo, hi, N_PER)
        dirs = rng.normal(size=(N_PER, 3))
        dirs /= np.linalg.norm(dirs, axis=1)[:, None]
        xyz = radius[:, None] * dirs
        x, y, z = xyz[:, 0], xyz[:, 1], xyz[:, 2]
        q = eta * kappa
        panel.append({
            "shell": shell, "lo": lo, "hi": hi,
            "gamma": gamma, "gamma_phi": gamma_phi, "kappa": kappa,
            "eta": eta, "omega": omega, "theta": theta, "r": radius,
            "x": x, "y": y, "z": z, "q": q,
        })
    return panel


def stratum_hash(s):
    h = hashlib.sha256()
    h.update(f"seed={SEED};shell={s['shell']};n={N_PER};schema=dephasing-crossing-v0.1\n".encode())
    for key in ["gamma", "gamma_phi", "kappa", "eta", "omega", "theta", "r", "x", "y", "z", "q"]:
        h.update(key.encode() + b"\0")
        h.update(np.asarray(s[key], dtype="<f8").tobytes(order="C"))
    return h.hexdigest()


def canonical_arrays(s):
    sn, cs = np.sin(s["theta"]), np.cos(s["theta"])
    a = 0.5 * s["gamma"] + s["gamma_phi"]
    b = s["gamma"]
    q = s["q"]
    u = sn * s["x"] + cs * s["z"]
    v = cs * s["x"] - sn * s["z"]
    p = a * sn * sn + b * cs * cs
    d = s["kappa"] + a * cs * cs + b * sn * sn
    h = (b - a) * sn * cs
    delta = s["omega"] - h
    R = a + b + s["kappa"] + s["omega"] + q
    return a, b, q, u, v, p, d, h, delta, R


def exact_c1_arrays(p, d, q, u, record=False):
    if not record:
        return 3.0 * (p + d) - 14.0 * q * u * u
    return 3.0 * (p + d) + 6.0 * q - 20.0 * q * u * u


def exact_c3_arrays(p, d, h, w, q, u, v, record=False):
    if not record:
        F = (
            -d*d*p + 4*d*d*q*u*u + d*h*h + 4*d*h*q*u*v - d*p*p
            + 9*d*p*q*u*u - 20*d*q*q*u**4 - 4*d*q*u*v*w - d*w*w
            + h*h*p - 5*h*h*q*u*u + h*h*q*v*v + 2*h*p*q*u*v
            - 12*h*q*q*u**3*v - 2*h*q*v*v*w + p*p*q*u*u
            - 8*p*q*q*u**4 - 2*p*q*u*v*w - p*w*w + 16*q**3*u**6
            + 12*q*q*u**3*v*w + 5*q*u*u*w*w + q*v*v*w*w
        )
    else:
        F = (
            -d*d*p + 6*d*d*q*u*u - 2*d*d*q + d*h*h + 6*d*h*q*u*v
            - d*p*p + 13*d*p*q*u*u - 4*d*p*q - 42*d*q*q*u**4
            + 26*d*q*q*u*u - 4*d*q*q - 6*d*q*u*v*w - d*w*w
            + h*h*p - 7*h*h*q*u*u + h*h*q*v*v + 2*h*h*q
            + 4*h*p*q*u*v - 30*h*q*q*u**3*v + 8*h*q*q*u*v
            - 2*h*q*v*v*w + p*p*q*u*u - 12*p*q*q*u**4
            + 4*p*q*q*u*u - 4*p*q*u*v*w - p*w*w + 36*q**3*u**6
            - 24*q**3*u**4 + 4*q**3*u*u + 30*q*q*u**3*v*w
            - 8*q*q*u*v*w + 7*q*u*u*w*w + q*v*v*w*w - 2*q*w*w
        )
    return -4.0 * F


def canonical_scalar(f):
    sn, cs = math.sin(f["theta"]), math.cos(f["theta"])
    a = 0.5 * f["gamma"] + f["gamma_phi"]
    b = f["gamma"]
    q = f["eta"] * f["kappa"]
    u = sn * f["x"] + cs * f["z"]
    v = cs * f["x"] - sn * f["z"]
    p = a * sn * sn + b * cs * cs
    d = f["kappa"] + a * cs * cs + b * sn * sn
    h = (b - a) * sn * cs
    delta = f["omega"] - h
    R = a + b + f["kappa"] + f["omega"] + q
    c1p = 3.0 * (p + d) - 14.0 * q * u*u
    c1r = 3.0 * (p + d) + 6.0 * q - 20.0 * q * u*u
    c3p = float(exact_c3_arrays(p, d, h, f["omega"], q, u, v, False))
    c3r = float(exact_c3_arrays(p, d, h, f["omega"], q, u, v, True))
    return {"a": a, "b": b, "q": q, "u": u, "v": v, "p": p, "d": d, "h": h,
            "delta": delta, "R": R, "c1p": c1p, "c1r": c1r, "c3p": c3p, "c3r": c3r}


def row_from_index(s, i, cls, meta, global_index):
    return {
        "id": f"DPX{global_index:07d}", "global_index": int(global_index), "shell": s["shell"],
        "selection_class": cls,
        "gamma": float(s["gamma"][i]), "gamma_phi": float(s["gamma_phi"][i]),
        "kappa": float(s["kappa"][i]), "eta": float(s["eta"][i]),
        "omega": float(s["omega"][i]), "theta": float(s["theta"][i]),
        "r": float(s["r"][i]), "x": float(s["x"][i]), "y": float(s["y"][i]), "z": float(s["z"][i]),
        "q": float(meta["q"][i]), "u": float(meta["u"][i]), "v": float(meta["v"][i]),
        "delta_norm": float(np.abs(meta["delta"][i]) / meta["R"][i]),
        "c1_phys_norm": float(meta["c1p"][i] / meta["R"][i]),
        "c1_record_norm": float(meta["c1r"][i] / meta["R"][i]),
        "c3_phys_norm": float(meta["c3p"][i] / meta["R"][i]**3),
        "c3_record_norm": float(meta["c3r"][i] / meta["R"][i]**3),
    }


def comm(a, b):
    return a @ b - b @ a


def dissipator(c, rho):
    cd = c.conj().T
    cdc = cd @ c
    return c @ rho @ cd - 0.5 * (cdc @ rho + rho @ cdc)


def rho_from_bloch(f):
    return 0.5 * (I2 + f["x"]*sx + f["y"]*sy + f["z"]*sz)


def coords(op):
    vals = [complex(np.trace(P @ op)) for P in PAULI]
    return np.array([z.real for z in vals]), max(abs(z.imag) for z in vals)


def linear_matrix(action):
    cols, imag = [], 0.0
    for e in BASIS:
        c, im = coords(action(e))
        cols.append(c)
        imag = max(imag, im)
    return np.column_stack(cols), imag


def Xtheta(theta):
    return 0.5 * (math.sin(theta)*sx + math.cos(theta)*sz)


def mu(X, rho):
    return float(np.trace(X @ rho).real)


def h_super(X, rho):
    return X@rho + rho@X - 2.0*mu(X, rho)*rho


def delta_h(X, rho, e):
    dm = float(np.trace(X @ e).real)
    return X@e + e@X - 2.0*mu(X, rho)*e - 2.0*dm*rho


def full_matrices(f):
    X = Xtheta(f["theta"])
    rho = rho_from_bloch(f)
    H = 0.5 * f["omega"] * sy
    c_amp = math.sqrt(f["gamma"]) * sm
    c_phi = math.sqrt(f["gamma_phi"] / 2.0) * sz
    def L(e):
        return -1j*comm(H, e) + dissipator(c_amp, e) + dissipator(c_phi, e) + 2.0*f["kappa"]*dissipator(X, e)
    A, ia = linear_matrix(L)
    amp = math.sqrt(2.0*f["eta"]*f["kappa"])
    B, ib = linear_matrix(lambda e: amp*delta_h(X, rho, e))
    h, ih = coords(h_super(X, rho))
    Vt = np.array([[float(np.trace(X @ e).real) for e in BASIS]])
    U = -4.0*f["eta"]*f["kappa"]*h.reshape(-1, 1)
    Ar = A + U @ Vt
    return rho, A, Ar, B, Vt, max(ia, ib, ih, max_abs(np.imag(Ar)))


def dark_space(A, Vt):
    O = np.vstack([Vt, Vt@A, Vt@A@A])
    _, s, vh = np.linalg.svd(O, full_matrices=True)
    rank = int(np.sum(s > NULL_TOL))
    D = vh[rank:].T.copy()
    if D.size:
        D, _ = np.linalg.qr(D)
    return s, D


def quotient_full(f, A, Ar, B):
    sn, cs = math.sin(f["theta"]), math.cos(f["theta"])
    C = np.array([[sn, cs], [0.0, 0.0], [cs, -sn]], dtype=float)
    L = C.T
    return L@A@C, L@Ar@C, L@B@C, L, C


def canonical_matrices(f):
    m = canonical_scalar(f)
    Ap = np.array([[-m["p"], m["h"]-f["omega"]], [m["h"]+f["omega"], -m["d"]]])
    B = -math.sqrt(2.0*m["q"]) * np.array([[2.0*m["u"], 0.0], [m["v"], m["u"]]])
    Ar = Ap + np.array([[-2.0*m["q"]*(1.0-m["u"]**2), 0.0], [2.0*m["q"]*m["u"]*m["v"], 0.0]])
    return Ap, Ar, B, m


def moment_action(A, B, P):
    return A@P + P@A.T + B@P@B.T


def sym_coords(P):
    return np.array([P[0, 0], 0.5*(P[0, 1]+P[1, 0]), P[1, 1]])


def Gnum(A, B):
    return np.column_stack([sym_coords(moment_action(A, B, E)) for E in SYM_BASIS])


def rh(G, R):
    tr = float(np.trace(G))
    c1 = -tr
    c2 = 0.5*(tr*tr - float(np.trace(G@G)))
    c3 = -float(np.linalg.det(G))
    mh = c1*c2 - c3
    margins = {"m1": c1/R, "m2": c2/R**2, "m3": c3/R**3, "mh": mh/R**3}
    if all(v > RH_TOL for v in margins.values()):
        cls = "STABLE"
    elif any(v < -RH_TOL for v in margins.values()):
        cls = "UNSTABLE"
    else:
        cls = "BOUNDARY"
    return {"c1": c1, "c2": c2, "c3": c3, "mh_raw": mh, "margins": margins, "class": cls}


def Kfull(A, B):
    n = A.shape[0]
    return np.kron(np.eye(n), A) + np.kron(A, np.eye(n)) + np.kron(B, B)


# X0: deterministic generator and Stage A exact c1/c3-only screening.
panel_a = generate_panel()
hashes_a = {s["shell"]: stratum_hash(s) for s in panel_a}
panel_b = generate_panel()
hashes_b = {s["shell"]: stratum_hash(s) for s in panel_b}
X0 = hashes_a == hashes_b

d_counts, s_counts, near_counts = {}, {}, {}
d_candidates, s_candidates = [], []
global_offset = 0
for s in panel_a:
    a, b, q, u, v, p, d, h, delta, R = canonical_arrays(s)
    c1p = exact_c1_arrays(p, d, q, u, False)
    c1r = exact_c1_arrays(p, d, q, u, True)
    c3p = exact_c3_arrays(p, d, h, s["omega"], q, u, v, False)
    c3r = exact_c3_arrays(p, d, h, s["omega"], q, u, v, True)
    adm = np.abs(delta) / R > MAP_TOL
    dmask = adm & (c1p/R > MAP_TOL) & (c3p/R**3 > MAP_TOL) & (c3r/R**3 < -MAP_TOL)
    smask = adm & (c1r/R > MAP_TOL) & (c3p/R**3 < -MAP_TOL) & (c3r/R**3 > MAP_TOL)
    didx = np.where(dmask)[0]
    sidx = np.where(smask)[0]
    d_counts[s["shell"]] = int(len(didx))
    s_counts[s["shell"]] = int(len(sidx))
    near_counts[s["shell"]] = int(np.sum(~adm))
    meta = {"q": q, "u": u, "v": v, "delta": delta, "R": R, "c1p": c1p, "c1r": c1r, "c3p": c3p, "c3r": c3r}
    for i in didx:
        d_candidates.append(row_from_index(s, int(i), "D_C13", meta, global_offset + int(i) + 1))
    for i in sidx:
        s_candidates.append(row_from_index(s, int(i), "S_C13", meta, global_offset + int(i) + 1))
    global_offset += N_PER

d_candidates.sort(key=lambda r: r["global_index"])
s_candidates.sort(key=lambda r: r["global_index"])
frozen_d = d_candidates[:MAX_FREEZE]
frozen_s = s_candidates[:MAX_FREEZE]

stage_payload = {
    "schema": "stability-arc-dephasing-crossing-stageA-v0.1",
    "seed": SEED, "n_per_stratum": N_PER, "n_total": N_PER*len(SHELLS),
    "stratum_hashes": hashes_a, "map_tolerance": MAP_TOL,
    "near_boundary_counts": near_counts,
    "available_counts": {"D_C13": d_counts, "S_C13": s_counts,
                         "D_total": len(d_candidates), "S_total": len(s_candidates)},
    "selected": {"D_C13": frozen_d, "S_C13": frozen_s},
}
stage_bytes = json.dumps(stage_payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"
STAGE_A.write_bytes(stage_bytes)
stage_sha = hashlib.sha256(stage_bytes).hexdigest()
STAGE_A_SHA.write_text(stage_sha + "  stageA_dephasing_crossing_selection.json\n", encoding="utf-8")
X1 = hashlib.sha256(STAGE_A.read_bytes()).hexdigest() == stage_sha

# X2 exact Stage-A replay, still without hidden margins.
frozen = json.loads(STAGE_A.read_text(encoding="utf-8"))
rows = frozen["selected"]["D_C13"] + frozen["selected"]["S_C13"]
replay_failures = []
for f in rows:
    m = canonical_scalar(f)
    admitted = abs(m["delta"])/m["R"] > MAP_TOL
    if f["selection_class"] == "D_C13":
        ok = admitted and m["c1p"]/m["R"] > MAP_TOL and m["c3p"]/m["R"]**3 > MAP_TOL and m["c3r"]/m["R"]**3 < -MAP_TOL
    else:
        ok = admitted and m["c1r"]/m["R"] > MAP_TOL and m["c3p"]/m["R"]**3 < -MAP_TOL and m["c3r"]/m["R"]**3 > MAP_TOL
    if not ok:
        replay_failures.append(f["id"])
X2 = len(replay_failures) == 0

# Stage B: independent full Hilbert reveal for frozen cases.
recon_failures, boundary_rows = [], []
d_counter, s_counter = [], []
d_blockers = {"m2": 0, "mh": 0}
s_blockers = {"m2": 0, "mh": 0}
d_correct = s_correct = 0
max_matrix_error = max_c13_error = max_moment_error = 0.0

if X0 and X1 and X2:
    for f in rows:
        rho, A, Ar, B, Vt, imag = full_matrices(f)
        reasons = []
        rho_min = float(np.min(np.linalg.eigvalsh(rho)))
        sv, D = dark_space(A, Vt)
        if rho_min <= 0.0:
            reasons.append("NONPOSITIVE_DENSITY")
        if D.shape[1] != 1:
            reasons.append("DARK_DIMENSION")
        Apf, Arf, Bf, L, C = quotient_full(f, A, Ar, B)
        Apc, Arc, Bc, meta = canonical_matrices(f)
        matrix_error = max(max_abs(Apf-Apc), max_abs(Arf-Arc), max_abs(Bf-Bc))
        max_matrix_error = max(max_matrix_error, matrix_error)
        if matrix_error > MATRIX_TOL:
            reasons.append("CANONICAL_MATRIX")
        Gp, Gr = Gnum(Apf, Bf), Gnum(Arf, Bf)
        rp, rr = rh(Gp, meta["R"]), rh(Gr, meta["R"])
        c13_error = max(relabs(rp["c1"], meta["c1p"]), relabs(rr["c1"], meta["c1r"]),
                        relabs(rp["c3"], meta["c3p"]), relabs(rr["c3"], meta["c3r"]))
        max_c13_error = max(max_c13_error, c13_error)
        if c13_error > RECON_TOL:
            reasons.append("C1_C3_RECONSTRUCTION")
        J = np.kron(L, L)
        moment_error = max(max_abs(J@Kfull(A, B)-Kfull(Apf, Bf)@J),
                           max_abs(J@Kfull(Ar, B)-Kfull(Arf, Bf)@J))
        max_moment_error = max(max_moment_error, moment_error)
        if moment_error > MOMENT_TOL:
            reasons.append("MOMENT_INTERTWINING")
        if imag > 1e-11:
            reasons.append("NONREAL")
        if reasons:
            recon_failures.append({"id": f["id"], "selection_class": f["selection_class"], "reasons": reasons,
                                   "rho_min": rho_min, "singular_values": [float(x) for x in sv],
                                   "matrix_error": matrix_error, "c13_error": c13_error, "moment_error": moment_error})
            continue
        rec = {"id": f["id"], "shell": f["shell"], "selection_class": f["selection_class"],
               "physical": rp, "record": rr}
        if rp["class"] == "BOUNDARY" or rr["class"] == "BOUNDARY":
            boundary_rows.append(rec)
            continue
        if f["selection_class"] == "D_C13":
            if rp["class"] == "STABLE" and rr["class"] == "UNSTABLE":
                d_correct += 1
            else:
                blockers = []
                if rp["margins"]["m2"] <= RH_TOL:
                    blockers.append("m2"); d_blockers["m2"] += 1
                if rp["margins"]["mh"] <= RH_TOL:
                    blockers.append("mh"); d_blockers["mh"] += 1
                d_counter.append({**rec, "blocking_margins": blockers})
        else:
            if rp["class"] == "UNSTABLE" and rr["class"] == "STABLE":
                s_correct += 1
            else:
                blockers = []
                if rr["margins"]["m2"] <= RH_TOL:
                    blockers.append("m2"); s_blockers["m2"] += 1
                if rr["margins"]["mh"] <= RH_TOL:
                    blockers.append("mh"); s_blockers["mh"] += 1
                s_counter.append({**rec, "blocking_margins": blockers})

X3 = len(recon_failures) == 0
X4 = len(boundary_rows) == 0

# X5 controls.
f0 = {"gamma": 1.0, "gamma_phi": 0.4, "kappa": 0.7, "eta": 0.0, "omega": 0.8,
      "theta": 0.3, "x": 0.2, "y": -0.1, "z": 0.3}
_, A0, Ar0, B0, _, _ = full_matrices(f0)
eta_zero_ok = max_abs(A0-Ar0) <= 1e-15 and max_abs(B0) <= 1e-15
Gstable = np.diag([-1.0, -2.0, -3.0])
Gunstable = np.diag([0.2, -1.0, -2.0])
Gboundary = np.diag([0.0, -1.0, -2.0])
classifier_ok = (rh(Gstable, 1.0)["class"] == "STABLE" and rh(Gunstable, 1.0)["class"] == "UNSTABLE" and rh(Gboundary, 1.0)["class"] == "BOUNDARY")
X5 = eta_zero_ok and classifier_ok

D_available = len(d_candidates)
S_available = len(s_candidates)
h10de = D_available >= MIN_SCORE
h10se = S_available >= MIN_SCORE

if not all([X0, X1, X2, X3, X5]):
    h10d_status = h10s_status = "RECONSTRUCTION_OR_AUDIT_HOLD"
elif not X4:
    h10d_status = h10s_status = "BOUNDARY_HOLD"
else:
    if not h10de:
        h10d_status = "SELECTION_HOLD_D"
    else:
        h10d_status = "PASS_H10D" if len(d_counter) == 0 else "FAIL_H10D"
    if not h10se:
        h10s_status = "SELECTION_HOLD_S"
    else:
        h10s_status = "PASS_H10S" if len(s_counter) == 0 else "FAIL_H10S"

result = {
    "schema": "stability-arc-dephasing-crossing-transfer-v0.1",
    "environment": {"python": platform.python_version(), "numpy": np.__version__},
    "audit": {"X0": X0, "X1": X1, "X2": X2, "X3": X3, "X4": X4, "X5": X5,
              "max_matrix_error": max_matrix_error, "max_c13_error": max_c13_error,
              "max_moment_error": max_moment_error},
    "stageA": {"selection_sha256": stage_sha, "stratum_hashes": hashes_a,
               "near_boundary_counts": near_counts, "D_counts": d_counts, "S_counts": s_counts,
               "D_available": D_available, "S_available": S_available,
               "D_frozen": len(frozen_d), "S_frozen": len(frozen_s)},
    "scientific": {"H10D_E": "PASS" if h10de else "FAIL", "H10S_E": "PASS" if h10se else "FAIL",
                   "H10D": h10d_status, "H10S": h10s_status,
                   "D_correct": d_correct, "D_counterexamples": len(d_counter), "D_blockers": d_blockers,
                   "S_correct": s_correct, "S_counterexamples": len(s_counter), "S_blockers": s_blockers,
                   "boundary_count": len(boundary_rows)},
    "replay_failures": replay_failures,
    "reconstruction_failures": recon_failures,
    "boundary_rows": boundary_rows,
    "D_counterexamples": d_counter,
    "S_counterexamples": s_counter,
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"audit": result["audit"], "stageA": result["stageA"], "scientific": result["scientific"]}, indent=2, sort_keys=True))
