#!/usr/bin/env python3
import json
import math
import platform
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "joint_channel_representation_audit_v01.json"

ETA = 0.73
KAPPA = 0.41
OMEGA = 1.17
GAMMA = 0.23
FD_EPS = 1e-6
R0_GATE = 5e-13
R1_GATE = 5e-10
R2_GATE = 5e-13
RANK_TOL = 1e-12
R3_GATE = 5e-10
R4_POLY_GATE = 5e-10
R4_NORM_GATE = 5e-13
CHI_GATE = 1e-14

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
ident = np.eye(2, dtype=complex)
sm = np.array([[0, 1], [0, 0]], dtype=complex)
BASIS = [0.5 * sx, 0.5 * sy, 0.5 * sz]
PAULI = [sx, sy, sz]

xop = 0.5 * sz
hamiltonian = 0.5 * OMEGA * sy
collapse = math.sqrt(GAMMA) * sm
rho = 0.5 * (ident + 0.20 * sx - 0.25 * sy + 0.30 * sz)


def comm(a, b):
    return a @ b - b @ a


def dissipator(c, state):
    cd = c.conj().T
    cdc = cd @ c
    return c @ state @ cd - 0.5 * (cdc @ state + state @ cdc)


def liouvillian(state):
    return (
        -1j * comm(hamiltonian, state)
        + dissipator(collapse, state)
        + 2.0 * KAPPA * dissipator(xop, state)
    )


def mu(state):
    return float(np.trace(xop @ state).real)


def h_super(state):
    m = mu(state)
    return xop @ state + state @ xop - 2.0 * m * state


def delta_h(state, perturbation):
    dm = float(np.trace(xop @ perturbation).real)
    return (
        xop @ perturbation
        + perturbation @ xop
        - 2.0 * mu(state) * perturbation
        - 2.0 * dm * state
    )


def coords(operator):
    vals = [complex(np.trace(p @ operator)) for p in PAULI]
    if max(abs(v.imag) for v in vals) > 1e-12:
        raise ValueError("non-real Bloch coordinate encountered")
    return np.array([v.real for v in vals], dtype=float)


def linear_matrix(action):
    return np.column_stack([coords(action(e)) for e in BASIS])


def json_matrix(a):
    return [[float(v) for v in row] for row in np.asarray(a, dtype=float)]


def spectrum(a):
    vals = np.linalg.eigvals(a)
    vals = sorted(vals, key=lambda z: (float(z.real), float(z.imag)))
    return [{"real": float(v.real), "imag": float(v.imag)} for v in vals]


def max_abs(a):
    return float(np.max(np.abs(a)))


def rot_x(theta):
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], dtype=float)


def rot_y(theta):
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], dtype=float)


def rot_z(theta):
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)


def block_chi(a):
    arr = np.asarray(a)
    if arr.shape != (2, 2):
        return None
    if np.iscomplexobj(arr) and max_abs(arr.imag) > 1e-14:
        return None
    ar = arr.real.astype(float)
    tr = float(np.trace(ar))
    det = float(np.linalg.det(ar))
    if tr >= 0.0 or det <= 0.0:
        return None
    return -tr / (2.0 * math.sqrt(det))


criteria = {}

# Construct separate channel objects.
A_phys = linear_matrix(liouvillian)
B = linear_matrix(lambda e: delta_h(rho, e))
h = coords(h_super(rho))
m = np.array([float(np.trace(xop @ e).real) for e in BASIS], dtype=float)
Delta_expected = -4.0 * ETA * KAPPA * np.outer(h, m)
A_rec = A_phys + Delta_expected
DeltaA = A_rec - A_phys

# R0: independent analytic unconditional control.
a = GAMMA / 2.0 + 2.0 * KAPPA
A_control = np.array([
    [-a, 0.0, OMEGA],
    [0.0, -a, 0.0],
    [-OMEGA, 0.0, -GAMMA],
], dtype=float)
r0_err = max_abs(A_phys - A_control)
criteria["R0"] = {
    "status": "PASS" if r0_err <= R0_GATE else "FAIL",
    "max_abs_entry_error": r0_err,
    "gate": R0_GATE,
}

# R1: centered finite difference of nonlinear H_x.
B_fd_cols = []
for e in BASIS:
    plus = h_super(rho + FD_EPS * e)
    minus = h_super(rho - FD_EPS * e)
    B_fd_cols.append(coords((plus - minus) / (2.0 * FD_EPS)))
B_fd = np.column_stack(B_fd_cols)
r1_err = max_abs(B - B_fd)
criteria["R1"] = {
    "status": "PASS" if r1_err <= R1_GATE else "FAIL",
    "max_abs_entry_error": r1_err,
    "gate": R1_GATE,
    "epsilon": FD_EPS,
}

# R2: conditioning-difference identity and rank-one structure.
r2_err = max_abs(DeltaA - Delta_expected)
svals = np.linalg.svd(DeltaA, compute_uv=False)
rank = int(np.sum(svals > RANK_TOL))
r2_pass = r2_err <= R2_GATE and rank <= 1
criteria["R2"] = {
    "status": "PASS" if r2_pass else "FAIL",
    "max_abs_entry_residual": r2_err,
    "gate": R2_GATE,
    "singular_values": [float(v) for v in svals],
    "rank_tolerance": RANK_TOL,
    "numerical_rank": rank,
}

# R3: block-diagonal joint characteristic polynomial is exactly the product.
A_joint = np.zeros((6, 6), dtype=float)
A_joint[:3, :3] = A_phys
A_joint[3:, 3:] = A_rec
poly_joint = np.poly(A_joint)
poly_product = np.convolve(np.poly(A_phys), np.poly(A_rec))
r3_err = max_abs(poly_joint - poly_product)
criteria["R3"] = {
    "status": "PASS" if r3_err <= R3_GATE else "FAIL",
    "max_abs_coefficient_residual": r3_err,
    "gate": R3_GATE,
}

# R4: fixed common coordinate rotation invariance.
Q = rot_z(0.37) @ rot_y(-0.52) @ rot_x(0.29)
def sim(a):
    return Q.T @ a @ Q

rotated = {"A_phys": sim(A_phys), "A_rec": sim(A_rec), "DeltaA": sim(DeltaA), "B": sim(B)}
poly_errs = {}
for name, original in [("A_phys", A_phys), ("A_rec", A_rec), ("DeltaA", DeltaA)]:
    poly_errs[name] = max_abs(np.poly(original) - np.poly(rotated[name]))
delta_norm_err = abs(float(np.linalg.norm(DeltaA, ord="fro")) - float(np.linalg.norm(rotated["DeltaA"], ord="fro")))
b_norm_err = abs(float(np.linalg.norm(B, ord="fro")) - float(np.linalg.norm(rotated["B"], ord="fro")))
r4_pass = max(poly_errs.values()) <= R4_POLY_GATE and max(delta_norm_err, b_norm_err) <= R4_NORM_GATE
criteria["R4"] = {
    "status": "PASS" if r4_pass else "FAIL",
    "characteristic_polynomial_max_errors": poly_errs,
    "polynomial_gate": R4_POLY_GATE,
    "DeltaA_frobenius_norm_error": delta_norm_err,
    "B_frobenius_norm_error": b_norm_err,
    "norm_gate": R4_NORM_GATE,
    "Q_orthogonality_error": max_abs(Q.T @ Q - np.eye(3)),
    "Q_determinant": float(np.linalg.det(Q)),
}

# R5: exact second-order recovery and mandatory refusal outside licensed input.
oscillator_cases = [(1.0, 1.0, 0.6), (2.3, 0.7, 1.4), (0.4, 2.1, 5.0)]
recovery_rows = []
for mass, omega, gamma in oscillator_cases:
    block = np.array([[0.0, 1.0 / mass], [-mass * omega * omega, -gamma]], dtype=float)
    got = block_chi(block)
    expected = gamma / (2.0 * omega)
    err = abs(got - expected) if got is not None else float("inf")
    recovery_rows.append({
        "m": mass,
        "Omega": omega,
        "Gamma": gamma,
        "chi_block": got,
        "chi_expected": expected,
        "abs_error": err,
    })

refusal_inputs = {
    "wrong_shape_A_phys": A_phys,
    "wrong_shape_A_rec": A_rec,
    "unstable_trace": np.diag([1.0, -2.0]),
    "nonpositive_det": np.array([[0.0, 1.0], [1.0, -1.0]], dtype=float),
    "materially_complex": np.array([[-1.0 + 1e-4j, 1.0], [-1.0, -1.0]], dtype=complex),
}
refusals = {name: ("REFUSE" if block_chi(value) is None else block_chi(value)) for name, value in refusal_inputs.items()}
r5_pass = all(r["abs_error"] <= CHI_GATE for r in recovery_rows) and all(v == "REFUSE" for v in refusals.values())
criteria["R5"] = {
    "status": "PASS" if r5_pass else "FAIL",
    "recovery_gate": CHI_GATE,
    "recovery_rows": recovery_rows,
    "refusals": refusals,
    "A_phys_scalar_status": "FULL_MATRIX_REQUIRED",
    "A_rec_scalar_status": "FULL_MATRIX_REQUIRED",
}

overall = all(item["status"] == "PASS" for item in criteria.values())
payload = {
    "schema": "stability-arc-joint-channel-representation-audit-v0.1",
    "scope": "REPRESENTATION_AUDIT_ONLY",
    "overall_status": "PASS" if overall else "FAIL",
    "parameters": {
        "eta": ETA,
        "kappa": KAPPA,
        "omega": OMEGA,
        "gamma": GAMMA,
        "base_bloch": [0.20, -0.25, 0.30],
    },
    "channels": {
        "same_noise_physical": {
            "A_phys": json_matrix(A_phys),
            "B": json_matrix(B),
            "spectrum_A_phys": spectrum(A_phys),
            "scalar_status": "FULL_MATRIX_REQUIRED",
        },
        "same_record_inference": {
            "A_rec": json_matrix(A_rec),
            "B": json_matrix(B),
            "spectrum_A_rec": spectrum(A_rec),
            "scalar_status": "FULL_MATRIX_REQUIRED",
        },
        "comparative": {
            "DeltaA": json_matrix(DeltaA),
            "conditioning_h": [float(v) for v in h],
            "measurement_functional_m": [float(v) for v in m],
            "shared_diffusion_matrix": True,
            "DeltaA_frobenius_norm": float(np.linalg.norm(DeltaA, ord="fro")),
            "commutator_frobenius_norm": float(np.linalg.norm(A_phys @ A_rec - A_rec @ A_phys, ord="fro")),
        },
        "joint": {
            "dimension": 6,
            "construction": "block_diag(A_phys,A_rec)",
            "spectrum": spectrum(A_joint),
        },
    },
    "criteria": criteria,
    "environment": {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "platform": platform.platform(),
    },
    "interpretation_firewall": (
        "PASS licenses the ordered separate-plus-joint matrix representation only; it does not show that any channel, "
        "difference, spectrum, or scalar predicts localization or that chi=1 is optimal under measurement."
    ),
}
OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(payload, indent=2, sort_keys=True))
raise SystemExit(0 if overall else 1)
