from __future__ import annotations

import json
import os
from pathlib import Path
import numpy as np

OUT = Path(os.environ.get("SI_DISTRIBUTED_OUTPUT_DIR", "stability_inheritance/results/foundational_lindblad_cleanroom"))
OUT.mkdir(parents=True, exist_ok=True)

OMEGA = 1.0
GAMMA = 2.0 * OMEGA

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)

# Convention: d rho/dt = -i[Omega sx/2,rho] + (Gamma_phi/2)(sz rho sz-rho).
# This makes x,y Bloch coherences decay at Gamma_phi and gives the yz block
# [[-Gamma_phi,-Omega],[Omega,0]], whose repeated-root condition is Gamma_phi=2 Omega.
H = 0.5 * OMEGA * sx

def liouvillian(gamma_phi: float) -> np.ndarray:
    # Column-stacking vec convention.
    coherent = -1j * (np.kron(I2, H) - np.kron(H.T, I2))
    dissip = 0.5 * gamma_phi * (np.kron(sz.T, sz) - np.eye(4, dtype=complex))
    return coherent + dissip

def bloch_generator(gamma_phi: float) -> np.ndarray:
    return np.array([
        [-gamma_phi, 0.0, 0.0],
        [0.0, -gamma_phi, -OMEGA],
        [0.0, OMEGA, 0.0],
    ], dtype=float)

def geom_mult(M: np.ndarray, lam: complex, tol: float = 1e-10) -> int:
    s = np.linalg.svd(M - lam * np.eye(M.shape[0], dtype=M.dtype), compute_uv=False)
    rank = int(np.sum(s > tol))
    return M.shape[0] - rank

L = liouvillian(GAMMA)
B = bloch_generator(GAMMA)
eval_L = np.linalg.eigvals(L)
eval_B = np.linalg.eigvals(B)

target = -OMEGA
gm_L = geom_mult(L, target)
gm_B = geom_mult(B.astype(complex), target)

# Sweep only diagnoses topology around the analytically fixed point; it does not select it.
ratios = np.linspace(0.5, 3.5, 301)
sweep = []
for r in ratios:
    g = r * OMEGA
    vals = np.linalg.eigvals(bloch_generator(g))
    yz = sorted(vals, key=lambda z: (abs(z + g), z.real))[:2]
    sweep.append({
        "Gamma_phi_over_Omega": float(r),
        "eigenvalues": [[float(v.real), float(v.imag)] for v in vals],
    })

result = {
    "task_id": os.environ.get("SI_DISTRIBUTED_TASK_ID"),
    "model": "driven qubit with pure dephasing",
    "master_equation_convention": "d rho/dt=-i[Omega sigma_x/2,rho]+(Gamma_phi/2)(sigma_z rho sigma_z-rho)",
    "Omega": OMEGA,
    "Gamma_phi": GAMMA,
    "analytic_EP_condition": "Gamma_phi=2*Omega",
    "bloch_generator_xyz": B.tolist(),
    "bloch_eigenvalues_at_EP": [[float(v.real), float(v.imag)] for v in eval_B],
    "full_liouvillian_eigenvalues_at_EP": [[float(v.real), float(v.imag)] for v in eval_L],
    "target_repeated_eigenvalue": target,
    "bloch_geometric_multiplicity_at_target": gm_B,
    "full_liouvillian_geometric_multiplicity_at_target": gm_L,
    "bloch_target_algebraic_count": int(np.sum(np.isclose(eval_B, target, atol=1e-9))),
    "full_liouvillian_target_algebraic_count": int(np.sum(np.isclose(eval_L, target, atol=1e-9))),
    "interpretation_rule": "defectiveness is supported only if algebraic multiplicity exceeds geometric multiplicity",
    "claim_ceiling": "clean-room generator qualification only; no universal chi optimality or cross-domain inheritance claim"
}
(OUT / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
(OUT / "sweep.json").write_text(json.dumps(sweep, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
