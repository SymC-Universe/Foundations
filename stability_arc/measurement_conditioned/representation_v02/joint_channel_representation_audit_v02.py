#!/usr/bin/env python3
import json
import math
import platform
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "joint_channel_representation_audit_v02.json"

FRESH_FIXTURES = [
    {"id": "F1", "eta": 0.64, "gamma": 0.11, "kappa": 0.17, "omega": 0.83, "base": [0.12, -0.18, 0.27]},
    {"id": "F2", "eta": 0.81, "gamma": 0.37, "kappa": 0.29, "omega": 1.31, "base": [-0.31, 0.22, -0.14]},
    {"id": "F3", "eta": 0.55, "gamma": 0.52, "kappa": 0.07, "omega": 0.61, "base": [0.05, 0.33, 0.41]},
]

FD_DT = 1e-3
FD_Z = 0.43
FD_EPS = 1e-5
R0_GATE = 5e-13
R1_GATE = 2e-6
R2_DRIFT_GATE = 2e-6
R2_IDENTITY_GATE = 5e-13
RANK_TOL = 1e-12
R3_GATE = 5e-10
R4_POLY_GATE = 5e-10
R4_NORM_GATE = 5e-13
CHI_GATE = 1e-14

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
ident2 = np.eye(2, dtype=complex)
sm = np.array([[0, 1], [0, 0]], dtype=complex)
xop = 0.5 * sz
BASIS = [0.5 * sx, 0.5 * sy, 0.5 * sz]
PAULI = [sx, sy, sz]


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


def liouvillian(state, gamma, kappa, omega):
    hamiltonian = 0.5 * omega * sy
    collapse = math.sqrt(gamma) * sm
    return (
        -1j * comm(hamiltonian, state)
        + dissipator(collapse, state)
        + 2.0 * kappa * dissipator(xop, state)
    )


def coords(operator):
    vals = [complex(np.trace(p @ operator)) for p in PAULI]
    if max(abs(v.imag) for v in vals) > 1e-11:
        raise ValueError("non-real Bloch coordinate encountered")
    return np.array([v.real for v in vals], dtype=float)


def linear_matrix(action):
    return np.column_stack([coords(action(e)) for e in BASIS])


def centered_state_jacobian(map_func, state, eps):
    columns = []
    for e in BASIS:
        fp = map_func(state + eps * e)
        fm = map_func(state - eps * e)
        columns.append(coords((fp - fm) / (2.0 * eps)))
    return np.column_stack(columns)


def same_noise_map(state, fixture, dt, dw):
    amp = math.sqrt(2.0 * fixture["eta"] * fixture["kappa"])
    return state + liouvillian(state, fixture["gamma"], fixture["kappa"], fixture["omega"]) * dt + amp * h_super(state) * dw


def same_record_map(state, fixture, dt, dy):
    amp = math.sqrt(2.0 * fixture["eta"] * fixture["kappa"])
    obs = math.sqrt(8.0 * fixture["eta"] * fixture["kappa"])
    innovation = dy - obs * mu(state) * dt
    return state + liouvillian(state, fixture["gamma"], fixture["kappa"], fixture["omega"]) * dt + amp * h_super(state) * innovation


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


def spectrum(a):
    vals = np.linalg.eigvals(a)
    vals = sorted(vals, key=lambda z: (float(z.real), float(z.imag)))
    return [{"real": float(v.real), "imag": float(v.imag)} for v in vals]


def json_matrix(a):
    return [[float(v) for v in row] for row in np.asarray(a, dtype=float)]


Q = rot_z(0.37) @ rot_y(-0.52) @ rot_x(0.29)
I3 = np.eye(3)
fixture_results = []

for fixture in FRESH_FIXTURES:
    rho = rho_from_bloch(fixture["base"])
    eigs_rho = np.linalg.eigvalsh(rho)
    if float(np.min(eigs_rho)) <= 0.0:
        raise RuntimeError(f"fresh fixture {fixture['id']} is not strictly inside Bloch ball")

    gamma = fixture["gamma"]
    kappa = fixture["kappa"]
    omega = fixture["omega"]
    eta = fixture["eta"]

    # Analytic/local matrices.
    A_phys = linear_matrix(lambda e: liouvillian(e, gamma, kappa, omega))
    amp = math.sqrt(2.0 * eta * kappa)
    B = amp * linear_matrix(lambda e: delta_h(rho, e))
    h = coords(h_super(rho))
    m = np.array([float(np.trace(xop @ e).real) for e in BASIS], dtype=float)
    Delta_expected = -4.0 * eta * kappa * np.outer(h, m)
    A_rec_formula = A_phys + Delta_expected
    DeltaA = A_rec_formula - A_phys

    # R0 corrected independent analytic control.
    decay_xy = gamma / 2.0 + kappa
    A_control = np.array([
        [-decay_xy, 0.0, omega],
        [0.0, -decay_xy, 0.0],
        [-omega, 0.0, -gamma],
    ], dtype=float)
    r0_error = max_abs(A_phys - A_control)

    # Independent full-map finite-difference decomposition using +/- noise.
    dw = FD_Z * math.sqrt(FD_DT)
    obs = math.sqrt(8.0 * eta * kappa)
    dy_plus = obs * mu(rho) * FD_DT + dw
    dy_minus = obs * mu(rho) * FD_DT - dw

    Jn_plus = centered_state_jacobian(lambda s: same_noise_map(s, fixture, FD_DT, dw), rho, FD_EPS)
    Jn_minus = centered_state_jacobian(lambda s: same_noise_map(s, fixture, FD_DT, -dw), rho, FD_EPS)
    Jr_plus = centered_state_jacobian(lambda s: same_record_map(s, fixture, FD_DT, dy_plus), rho, FD_EPS)
    Jr_minus = centered_state_jacobian(lambda s: same_record_map(s, fixture, FD_DT, dy_minus), rho, FD_EPS)

    A_phys_fd = ((Jn_plus + Jn_minus) / 2.0 - I3) / FD_DT
    B_noise_fd = (Jn_plus - Jn_minus) / (2.0 * dw)
    A_rec_fd = ((Jr_plus + Jr_minus) / 2.0 - I3) / FD_DT
    B_record_fd = (Jr_plus - Jr_minus) / (2.0 * dw)

    r1_noise_error = max_abs(B_noise_fd - B)
    r1_record_error = max_abs(B_record_fd - B)
    r1_cross_error = max_abs(B_noise_fd - B_record_fd)

    r2_phys_drift_error = max_abs(A_phys_fd - A_phys)
    r2_record_drift_error = max_abs(A_rec_fd - A_rec_formula)
    r2_identity_error = max_abs(DeltaA - Delta_expected)
    svals = np.linalg.svd(DeltaA, compute_uv=False)
    delta_rank = int(np.sum(svals > RANK_TOL))

    # R3 exact block-diagonal joint identity.
    A_joint = np.zeros((6, 6), dtype=float)
    A_joint[:3, :3] = A_phys
    A_joint[3:, 3:] = A_rec_formula
    r3_error = max_abs(np.poly(A_joint) - np.convolve(np.poly(A_phys), np.poly(A_rec_formula)))

    # R4 fixed common coordinate change.
    def sim(a):
        return Q.T @ a @ Q

    poly_errors = {
        "A_phys": max_abs(np.poly(A_phys) - np.poly(sim(A_phys))),
        "A_rec": max_abs(np.poly(A_rec_formula) - np.poly(sim(A_rec_formula))),
        "DeltaA": max_abs(np.poly(DeltaA) - np.poly(sim(DeltaA))),
    }
    delta_norm_error = abs(float(np.linalg.norm(DeltaA, ord="fro")) - float(np.linalg.norm(sim(DeltaA), ord="fro")))
    b_norm_error = abs(float(np.linalg.norm(B, ord="fro")) - float(np.linalg.norm(sim(B), ord="fro")))

    fixture_results.append({
        "id": fixture["id"],
        "parameters": fixture,
        "rho_eigenvalues": [float(v) for v in eigs_rho],
        "matrices": {
            "A_phys": json_matrix(A_phys),
            "A_rec": json_matrix(A_rec_formula),
            "DeltaA": json_matrix(DeltaA),
            "B": json_matrix(B),
            "A_phys_FD": json_matrix(A_phys_fd),
            "A_rec_FD": json_matrix(A_rec_fd),
            "B_noise_FD": json_matrix(B_noise_fd),
            "B_record_FD": json_matrix(B_record_fd),
        },
        "spectra": {
            "A_phys": spectrum(A_phys),
            "A_rec": spectrum(A_rec_formula),
            "A_joint": spectrum(A_joint),
        },
        "comparative": {
            "conditioning_h": [float(v) for v in h],
            "measurement_functional_m": [float(v) for v in m],
            "DeltaA_singular_values": [float(v) for v in svals],
            "DeltaA_numerical_rank": delta_rank,
            "DeltaA_frobenius_norm": float(np.linalg.norm(DeltaA, ord="fro")),
            "B_frobenius_norm": float(np.linalg.norm(B, ord="fro")),
            "commutator_frobenius_norm": float(np.linalg.norm(A_phys @ A_rec_formula - A_rec_formula @ A_phys, ord="fro")),
        },
        "errors": {
            "R0_control": r0_error,
            "R1_B_noise": r1_noise_error,
            "R1_B_record": r1_record_error,
            "R1_B_cross": r1_cross_error,
            "R2_A_phys_FD": r2_phys_drift_error,
            "R2_A_rec_FD": r2_record_drift_error,
            "R2_Delta_identity": r2_identity_error,
            "R3_joint_poly": r3_error,
            "R4_poly": poly_errors,
            "R4_Delta_norm": delta_norm_error,
            "R4_B_norm": b_norm_error,
        },
        "scalar_status": {
            "A_phys": "FULL_MATRIX_REQUIRED",
            "A_rec": "FULL_MATRIX_REQUIRED",
        },
    })

criteria = {}
criteria["R0"] = {
    "status": "PASS" if all(r["errors"]["R0_control"] <= R0_GATE for r in fixture_results) else "FAIL",
    "gate": R0_GATE,
    "max_error": max(r["errors"]["R0_control"] for r in fixture_results),
}
criteria["R1"] = {
    "status": "PASS" if all(
        max(r["errors"]["R1_B_noise"], r["errors"]["R1_B_record"], r["errors"]["R1_B_cross"]) <= R1_GATE
        for r in fixture_results
    ) else "FAIL",
    "gate": R1_GATE,
    "max_noise_error": max(r["errors"]["R1_B_noise"] for r in fixture_results),
    "max_record_error": max(r["errors"]["R1_B_record"] for r in fixture_results),
    "max_cross_error": max(r["errors"]["R1_B_cross"] for r in fixture_results),
}
criteria["R2"] = {
    "status": "PASS" if all(
        r["errors"]["R2_A_phys_FD"] <= R2_DRIFT_GATE
        and r["errors"]["R2_A_rec_FD"] <= R2_DRIFT_GATE
        and r["errors"]["R2_Delta_identity"] <= R2_IDENTITY_GATE
        and r["comparative"]["DeltaA_numerical_rank"] <= 1
        for r in fixture_results
    ) else "FAIL",
    "drift_gate": R2_DRIFT_GATE,
    "identity_gate": R2_IDENTITY_GATE,
    "rank_tolerance": RANK_TOL,
    "max_A_phys_FD_error": max(r["errors"]["R2_A_phys_FD"] for r in fixture_results),
    "max_A_rec_FD_error": max(r["errors"]["R2_A_rec_FD"] for r in fixture_results),
    "max_Delta_identity_error": max(r["errors"]["R2_Delta_identity"] for r in fixture_results),
    "max_rank": max(r["comparative"]["DeltaA_numerical_rank"] for r in fixture_results),
}
criteria["R3"] = {
    "status": "PASS" if all(r["errors"]["R3_joint_poly"] <= R3_GATE for r in fixture_results) else "FAIL",
    "gate": R3_GATE,
    "max_error": max(r["errors"]["R3_joint_poly"] for r in fixture_results),
}
criteria["R4"] = {
    "status": "PASS" if all(
        max(r["errors"]["R4_poly"].values()) <= R4_POLY_GATE
        and max(r["errors"]["R4_Delta_norm"], r["errors"]["R4_B_norm"]) <= R4_NORM_GATE
        for r in fixture_results
    ) else "FAIL",
    "polynomial_gate": R4_POLY_GATE,
    "norm_gate": R4_NORM_GATE,
    "max_polynomial_error": max(max(r["errors"]["R4_poly"].values()) for r in fixture_results),
    "max_Delta_norm_error": max(r["errors"]["R4_Delta_norm"] for r in fixture_results),
    "max_B_norm_error": max(r["errors"]["R4_B_norm"] for r in fixture_results),
    "Q_orthogonality_error": max_abs(Q.T @ Q - I3),
    "Q_determinant": float(np.linalg.det(Q)),
}

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
    "wrong_shape_3x3": np.eye(3),
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
    "full_matrix_policy": "A_phys and A_rec remain FULL_MATRIX_REQUIRED for every fresh fixture",
}

overall = all(v["status"] == "PASS" for v in criteria.values())
payload = {
    "schema": "stability-arc-joint-channel-representation-audit-v0.2",
    "scope": "CORRECTIVE_REPRESENTATION_AUDIT_ONLY",
    "lineage": {
        "v0.1_status": "FAIL",
        "v0.1_failure_run": 33234191815,
        "v0.1_failure_preserved": True,
        "corrections": [
            "measurement dephasing normalization: transverse rate kappa, not 2*kappa for x=sigma_z/2",
            "diffusion matrix includes sqrt(2*eta*kappa)",
            "same-record drift checked against independent full nonlinear map finite differences",
        ],
    },
    "finite_difference_decomposition": {
        "dt": FD_DT,
        "z": FD_Z,
        "epsilon": FD_EPS,
    },
    "criteria": criteria,
    "fresh_fixtures": fixture_results,
    "environment": {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "platform": platform.platform(),
    },
    "interpretation_firewall": (
        "PASS licenses only the corrected instantaneous separate-plus-joint stochastic tangent representation and its algebraic checks. "
        "It does not establish localization prediction, a universal scalar chi, or an optimum at chi=1."
    ),
}
OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(payload, indent=2, sort_keys=True))
raise SystemExit(0 if overall else 1)
