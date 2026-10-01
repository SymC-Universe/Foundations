from __future__ import annotations

import cmath
import json
import os
from pathlib import Path
import numpy as np

OUT = Path(os.environ.get("SI_DISTRIBUTED_OUTPUT_DIR", "stability_inheritance/results/foundational_qft_cleanroom"))
OUT.mkdir(parents=True, exist_ok=True)

OMEGA = 1.0

def generator(gamma: float) -> np.ndarray:
    return np.array([[0.0, 1.0], [-OMEGA**2, -gamma]], dtype=float)

def poles(gamma: float) -> tuple[complex, complex]:
    root = cmath.sqrt(OMEGA**2 - gamma**2 / 4.0)
    return (-0.5j * gamma + root, -0.5j * gamma - root)

def geom_mult(M: np.ndarray, lam: complex, tol: float = 1e-10) -> int:
    s = np.linalg.svd(M.astype(complex) - lam * np.eye(M.shape[0], dtype=complex), compute_uv=False)
    return M.shape[0] - int(np.sum(s > tol))

gamma_ep = 2.0 * OMEGA
A = generator(gamma_ep)
eval_A = np.linalg.eigvals(A)
lam_ep = -OMEGA
gm = geom_mult(A, lam_ep)
p_ep = poles(gamma_ep)

chis = np.linspace(0.2, 1.8, 321)
sweep = []
for chi in chis:
    gamma = 2.0 * OMEGA * chi
    vals = np.linalg.eigvals(generator(gamma))
    ps = poles(gamma)
    sweep.append({
        "chi": float(chi),
        "gamma": float(gamma),
        "generator_eigenvalues": [[float(v.real), float(v.imag)] for v in vals],
        "retarded_poles": [[float(v.real), float(v.imag)] for v in ps],
        "discriminant": float(gamma**2 - 4.0 * OMEGA**2),
    })

result = {
    "task_id": os.environ.get("SI_DISTRIBUTED_TASK_ID"),
    "native_reduced_equation": "qddot + gamma qdot + omega^2 q = 0",
    "omega": OMEGA,
    "gamma_EP": gamma_ep,
    "chi_EP": gamma_ep / (2.0 * OMEGA),
    "first_order_generator_at_EP": A.tolist(),
    "generator_eigenvalues_at_EP": [[float(v.real), float(v.imag)] for v in eval_A],
    "generator_target_algebraic_count": int(np.sum(np.isclose(eval_A, lam_ep, atol=1e-9))),
    "generator_target_geometric_multiplicity": gm,
    "retarded_poles_at_EP": [[float(v.real), float(v.imag)] for v in p_ep],
    "pole_separation_at_EP": float(abs(p_ep[0] - p_ep[1])),
    "analytic_discriminant_at_EP": float(gamma_ep**2 - 4.0 * OMEGA**2),
    "claim_ceiling": "clean-room local Markovian reduced-generator/pole qualification only; microscopic self-energy derivation and covariance wording remain separate source-audit tasks"
}
(OUT / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
(OUT / "sweep.json").write_text(json.dumps(sweep, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
