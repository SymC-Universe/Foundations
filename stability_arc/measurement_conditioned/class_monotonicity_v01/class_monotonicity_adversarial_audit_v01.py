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
OUT = RESULTS / "class_monotonicity_adversarial_audit_v01.json"
SELECTION_FILE = RESULTS / "stageA_selection.json"
SELECTION_SHA_FILE = RESULTS / "stageA_selection.sha256"

SEED = 2026082904
N_CANDIDATES = 50000
N_SELECT = 512
DARK_TOL = 5e-9
LIFT_TOL = 5e-11
REPLAY_TOL = 1e-8
CLASS_TOL = 1e-9
MIN_D = 1e-7
MAX_SELECTED_D = 0.05
NULL_TOL = 1e-10

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


def generate_candidates():
    rng = np.random.default_rng(SEED)
    out = []
    for i in range(1, N_CANDIDATES + 1):
        eta = float(rng.uniform(1e-4, 0.9999))
        gamma = float(10.0 ** rng.uniform(-5.0, 1.0))
        kappa = float(10.0 ** rng.uniform(-5.0, 1.0))
        omega = float(10.0 ** rng.uniform(-5.0, 1.0))
        direction = rng.normal(size=3)
        direction = direction / np.linalg.norm(direction)
        if i % 2 == 1:
            u = float(rng.uniform(0.0, 1.0))
            radius = 0.98 * (u ** (1.0 / 3.0))
        else:
            radius = float(rng.uniform(0.95, 0.9999))
        base = radius * direction
        out.append({
            "id": f"CM{i:05d}",
            "eta": eta,
            "gamma": gamma,
            "kappa": kappa,
            "omega": omega,
            "base": [float(v) for v in base],
        })
    return out


def physical_active_matrices(f):
    eta, gamma, kappa, omega = f["eta"], f["gamma"], f["kappa"], f["omega"]
    x, _, z = f["base"]
    q = eta * kappa
    a = gamma / 2.0 + kappa
    s = math.sqrt(2.0 * q)
    A = np.array([[-a, omega], [-omega, -gamma]], dtype=float)
    B = np.array([[-s * z, -s * x], [0.0, -2.0 * s * z]], dtype=float)
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


def spectral_alpha(G):
    return float(np.max(np.real(np.linalg.eigvals(G))))


def normalized_class(alpha, scale):
    x = alpha / scale
    if x < -CLASS_TOL:
        return "STABLE"
    if abs(x) <= CLASS_TOL:
        return "BOUNDARY"
    return "UNSTABLE"


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
        raise ValueError("non-real coordinate")
    return np.array([v.real for v in vals], dtype=float)


def linear_matrix(action):
    return np.column_stack([coords(action(e)) for e in BASIS])


def full_reconstruct(f):
    state = rho_from_bloch(f["base"])
    Aphys = linear_matrix(lambda e: liouvillian(e, f["gamma"], f["kappa"], f["omega"]))
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


# C0: deterministic input generation.
candidates_a = generate_candidates()
candidates_b = generate_candidates()
hash_a = hashlib.sha256(canonical_bytes(candidates_a)).hexdigest()
hash_b = hashlib.sha256(canonical_bytes(candidates_b)).hexdigest()
C0 = hash_a == hash_b and len(candidates_a) == N_CANDIDATES

# Stage A: physical channel only. No same-record construction occurs in this loop.
eligible = []
for f in candidates_a:
    A, B = physical_active_matrices(f)
    G = sym_generator(A, B)
    ap = spectral_alpha(G)
    q = f["eta"] * f["kappa"]
    scale = f["gamma"] + f["kappa"] + f["omega"] + q
    klass = normalized_class(ap, scale)
    d = -ap / scale
    rho_min = 0.5 * (1.0 - float(np.linalg.norm(f["base"])))
    if klass == "STABLE" and d >= MIN_D and rho_min > 0.0:
        eligible.append({
            "id": f["id"],
            "parameters": f,
            "stageA_alpha_phys": ap,
            "stageA_scale": scale,
            "stageA_d_phys": d,
            "stageA_class": klass,
            "stageA_rho_min": rho_min,
            "stageA_A_phys": A.tolist(),
            "stageA_B": B.tolist(),
            "stageA_G_coefficients": [float(v) for v in np.real_if_close(np.poly(G)[1:])],
        })

eligible.sort(key=lambda r: (r["stageA_d_phys"], int(r["id"][2:])))
selected = eligible[:N_SELECT]
selection_hold = len(selected) < N_SELECT or (selected and selected[-1]["stageA_d_phys"] > MAX_SELECTED_D)
selection_payload = {
    "schema": "stability-arc-class-monotonicity-stageA-selection-v0.1",
    "seed": SEED,
    "candidate_input_sha256": hash_a,
    "n_candidates": N_CANDIDATES,
    "n_eligible": len(eligible),
    "n_selected": len(selected),
    "selection_rule": "512 smallest physical-only d_phys, tie by candidate id",
    "selected": selected,
}
selection_bytes = json.dumps(selection_payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"
SELECTION_FILE.write_bytes(selection_bytes)
selection_sha = hashlib.sha256(selection_bytes).hexdigest()
SELECTION_SHA_FILE.write_text(selection_sha + "  stageA_selection.json\n", encoding="utf-8")

# Immutable Stage-B input is read back from frozen bytes.
stageB_selection = json.loads(SELECTION_FILE.read_text(encoding="utf-8"))["selected"]

records = []
reconstruction_ok = True
replay_ok = True
crossings = []
max_lift_error = 0.0
max_replay_error = 0.0

for srec in stageB_selection:
    f = srec["parameters"]
    state, Aphys3, Arec3, B3, Vt = full_reconstruct(f)
    rho_min = float(np.min(np.linalg.eigvalsh(state)))
    svals, D = dark_space(Aphys3, Vt)
    reasons = []
    if rho_min <= 0.0:
        reasons.append("NONPOSITIVE_DENSITY")
    if D.shape[1] != 1:
        reasons.append("DARK_DIMENSION")

    dark_res = None
    if D.shape[1] == 1:
        Pperp = np.eye(3) - D @ D.T
        L = ACTIVE.T
        dark_res = {
            "measurement": max_abs(Vt @ D),
            "Aphys_dark": max_abs(Pperp @ Aphys3 @ D),
            "Arec_dark": max_abs(Pperp @ Arec3 @ D),
            "B_dark": max_abs(Pperp @ B3 @ D),
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

        A_stage = np.array(srec["stageA_A_phys"], dtype=float)
        B_stage = np.array(srec["stageA_B"], dtype=float)
        analytic_res = max(max_abs(Ap - A_stage), max_abs(Bp - B_stage))
        if analytic_res > DARK_TOL:
            reasons.append("PHYSICAL_RECONSTRUCTION")

        Gp = sym_generator(Ap, Bp)
        Gr = sym_generator(Ar, Bp)
        lift_error = max(
            max_abs(Gp - sym_generator_kron(Ap, Bp)),
            max_abs(Gr - sym_generator_kron(Ar, Bp)),
        )
        max_lift_error = max(max_lift_error, lift_error)
        if lift_error > LIFT_TOL:
            reasons.append("MOMENT_LIFT")

        ap = spectral_alpha(Gp)
        ar = spectral_alpha(Gr)
        scale = srec["stageA_scale"]
        pclass = normalized_class(ap, scale)
        rclass = normalized_class(ar, scale)
        replay_error = abs(ap / scale - srec["stageA_alpha_phys"] / scale)
        max_replay_error = max(max_replay_error, replay_error)
        if pclass != "STABLE" or replay_error > REPLAY_TOL:
            replay_ok = False
        crossing = pclass == "STABLE" and rclass != "STABLE"
        if crossing:
            crossings.append(srec["id"])
    else:
        inter = None
        analytic_res = None
        lift_error = None
        ap = ar = None
        pclass = rclass = "REFUSE"
        replay_error = None
        crossing = False

    admitted = len(reasons) == 0
    if not admitted:
        reconstruction_ok = False
    records.append({
        "id": srec["id"],
        "stageA_d_phys": srec["stageA_d_phys"],
        "parameters": f,
        "admitted": admitted,
        "reasons": reasons,
        "rho_min_eigenvalue": rho_min,
        "observability_singular_values": [float(v) for v in svals],
        "dark_residuals": dark_res,
        "intertwining_residuals": inter,
        "physical_reconstruction_error": analytic_res,
        "lift_error": lift_error,
        "physical_alpha": ap,
        "record_alpha": ar,
        "scale": srec["stageA_scale"],
        "physical_class": pclass,
        "record_class": rclass,
        "normalized_replay_error": replay_error,
        "stable_to_nonstable_crossing": crossing,
    })

C1 = C0 and not selection_hold and len(selected) == N_SELECT
C2 = reconstruction_ok and len(records) == N_SELECT
C3 = C2 and replay_ok and max_replay_error <= REPLAY_TOL

# Independent adversarial classifier control.
A0 = np.array([[-0.3, 1.0], [-1.0, -0.3]], dtype=float)
B0 = 0.2 * np.eye(2)
A1 = A0 + np.array([[0.8, 0.0], [0.0, 0.0]], dtype=float)
G0 = sym_generator(A0, B0)
G1 = sym_generator(A1, B0)
scale_ctrl = 1.0
ctrl_base = normalized_class(spectral_alpha(G0), scale_ctrl)
ctrl_updated = normalized_class(spectral_alpha(G1), scale_ctrl)
C4 = ctrl_base == "STABLE" and ctrl_updated == "UNSTABLE"
C5 = C3 and len(crossings) == 0

if not C0:
    status = "AUDIT_FAILURE"
elif not C1:
    status = "SELECTION_HOLD"
elif not C2:
    status = "RECONSTRUCTION_HOLD"
elif not (C3 and C4):
    status = "AUDIT_FAILURE"
elif not C5:
    status = "FAIL_CLASS_MONOTONICITY"
else:
    status = "PASS_ADVERSARIAL_CLASS_MONOTONICITY"

criteria = {
    "C0": {"status": "PASS" if C0 else "FAIL", "candidate_input_sha256": hash_a},
    "C1": {
        "status": "PASS" if C1 else "FAIL",
        "eligible": len(eligible),
        "selected": len(selected),
        "selection_sha256": selection_sha,
        "min_selected_d_phys": selected[0]["stageA_d_phys"] if selected else None,
        "max_selected_d_phys": selected[-1]["stageA_d_phys"] if selected else None,
    },
    "C2": {"status": "PASS" if C2 else "FAIL", "max_lift_error": max_lift_error},
    "C3": {"status": "PASS" if C3 else "FAIL", "max_normalized_physical_replay_error": max_replay_error},
    "C4": {"status": "PASS" if C4 else "FAIL", "control_base_class": ctrl_base, "control_updated_class": ctrl_updated},
    "C5": {"status": "PASS" if C5 else "FAIL", "crossing_count": len(crossings), "crossing_ids": crossings},
}

payload = {
    "schema": "stability-arc-class-monotonicity-adversarial-v0.1",
    "scope": "PROSPECTIVE_STABILITY_CLASS_TEST",
    "phase_status": status,
    "environment": {"python": platform.python_version(), "numpy": np.__version__, "platform": platform.platform()},
    "criteria": criteria,
    "selection_sha256": selection_sha,
    "selected_records": records,
    "interpretation_firewall": (
        "A PASS is strong adversarial evidence only within this exact measured-qubit family. It is not a proof, does not "
        "restore spectral-abscissa H2, does not license a stochastic chi, and does not establish localization/collapse behavior. "
        "A single stable-to-boundary/unstable selected case is a preserved scientific failure."
    ),
}
OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"phase_status": status, "criteria": criteria}, indent=2, sort_keys=True))
raise SystemExit(0 if status == "PASS_ADVERSARIAL_CLASS_MONOTONICITY" else 1)
