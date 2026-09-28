import json
import numpy as np
from scipy.linalg import eigh, eig

SEED = 20260927
N_SWEEP = 2000
TIME = np.linspace(0.0, 15.0, 1501)

J_BASE = np.array([0.045, 0.060, 0.055])
K_BASE = np.array([0.6, 1.5, 0.9, 0.12, 0.18])
ALPHA = 0.18
BETA = 0.012
Y0 = np.r_[np.array([0.0, 0.0, 0.1]), np.zeros(3)]


def stiffness(k, interface):
    k1, k2, k3, kp, kc = k
    K = np.diag([k1, k2, k3]).astype(float)
    K[0, 0] += kp
    K[1, 1] += kp
    K[0, 1] -= kp
    K[1, 0] -= kp
    i = 0 if interface == "A" else 1
    K[i, i] += kc
    K[2, 2] += kc
    K[i, 2] -= kc
    K[2, i] -= kc
    return K


def parent_modal(Jd=J_BASE, k=K_BASE):
    M = np.diag(Jd[:2])
    K = np.array([[k[0] + k[3], -k[3]], [-k[3], k[1] + k[3]]])
    C = ALPHA * M + BETA * K
    lam, V = eigh(K, M)
    w = np.sqrt(lam)
    zeta = []
    for i in range(2):
        phi = V[:, i]
        zeta.append((phi @ C @ phi) / (2.0 * w[i] * (phi @ M @ phi)))
    modes = V / np.max(np.abs(V), axis=0)
    return w / (2 * np.pi), np.asarray(zeta), modes


def assembly_response(Jd, k, interface):
    M = np.diag(Jd)
    K = stiffness(k, interface)
    C = ALPHA * M + BETA * K
    freq = np.sqrt(eigh(K, M, eigvals_only=True)) / (2 * np.pi)
    Minv = np.diag(1.0 / Jd)
    A = np.block([[np.zeros((3, 3)), np.eye(3)], [-Minv @ K, -Minv @ C]])
    lam, V = eig(A)
    coeff = np.linalg.solve(V, Y0)
    Y = (V @ (coeff[:, None] * np.exp(lam[:, None] * TIME[None, :]))).real
    peak = np.max(np.abs(Y[:3]), axis=1)
    return freq, peak


def quantiles(x):
    return {
        "min": float(np.min(x)),
        "p05": float(np.quantile(x, 0.05)),
        "median": float(np.median(x)),
        "p95": float(np.quantile(x, 0.95)),
        "max": float(np.max(x)),
    }


def main():
    pf, pchi, pmodes = parent_modal()
    fa, pa = assembly_response(J_BASE, K_BASE, "A")
    fb, pb = assembly_response(J_BASE, K_BASE, "B")

    rng = np.random.default_rng(SEED)
    rows = []
    for _ in range(N_SWEEP):
        Jd = J_BASE * (1 + rng.uniform(-0.05, 0.05, 3))
        k = K_BASE * (1 + rng.uniform(-0.05, 0.05, 5))
        a_f, a_p = assembly_response(Jd, k, "A")
        b_f, b_p = assembly_response(Jd, k, "B")
        rows.append([
            a_p[0] / b_p[0],
            b_p[1] / a_p[1],
            (b_f[0] - a_f[0]) / a_f[0],
            (b_f[1] - a_f[1]) / a_f[1],
            (b_f[2] - a_f[2]) / a_f[2],
        ])
    arr = np.asarray(rows)

    out = {
        "status": "KNOWN_TRUTH_DIGITAL_TWIN_ONLY",
        "parent_frequency_hz": pf.tolist(),
        "parent_modal_chi": pchi.tolist(),
        "parent_mode_shapes_maxnorm_columns": pmodes.tolist(),
        "nominal": {
            "assembly_A_frequency_hz": fa.tolist(),
            "assembly_B_frequency_hz": fb.tolist(),
            "parent_coord1_peak_ratio_A_over_B": float(pa[0] / pb[0]),
            "parent_coord2_peak_ratio_B_over_A": float(pb[1] / pa[1]),
        },
        "tolerance_sweep": {
            "seed": SEED,
            "n": N_SWEEP,
            "rule": "paired independent uniform +/-5% perturbation of all inertias and stiffnesses",
            "q1_peak_ratio_A_over_B": quantiles(arr[:, 0]),
            "q2_peak_ratio_B_over_A": quantiles(arr[:, 1]),
            "mode1_rel_shift_B_minus_A": quantiles(arr[:, 2]),
            "mode2_rel_shift_B_minus_A": quantiles(arr[:, 3]),
            "mode3_rel_shift_B_minus_A": quantiles(arr[:, 4]),
        },
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
