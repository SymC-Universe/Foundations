from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class EvidenceGates:
    independent_parent_characterization: bool
    explicit_carrier_correspondence: bool
    mapping_rule_frozen_before_target_reveal: bool
    prospective_child_prediction: bool
    intervention_or_counterfactual_confirmation: bool
    specificity_against_scrambled_or_generic_controls: bool


def classify_evidence(gates: EvidenceGates) -> str:
    values = [
        gates.independent_parent_characterization,
        gates.explicit_carrier_correspondence,
        gates.mapping_rule_frozen_before_target_reveal,
        gates.prospective_child_prediction,
        gates.intervention_or_counterfactual_confirmation,
        gates.specificity_against_scrambled_or_generic_controls,
    ]
    if all(values):
        return "SUBSTRATE_INHERITANCE"
    if all(values[:4]):
        return "CONDITIONAL_INHERITANCE"
    if gates.independent_parent_characterization and gates.intervention_or_counterfactual_confirmation:
        return "SUBSTRATE_INFLUENCE"
    return "UNRESOLVED"


def _metric_matrix(metric: np.ndarray | Iterable[float], n: int) -> np.ndarray:
    arr = np.asarray(metric, dtype=float)
    if arr.ndim == 1:
        if arr.shape[0] != n:
            raise ValueError("Metric vector length does not match vector dimension")
        return np.diag(arr)
    if arr.shape != (n, n):
        raise ValueError("Metric matrix shape does not match vector dimension")
    return arr


def mass_normalize_columns(vectors: np.ndarray, metric: np.ndarray | Iterable[float]) -> np.ndarray:
    v = np.asarray(vectors, dtype=float)
    if v.ndim != 2:
        raise ValueError("vectors must be a two-dimensional matrix with vectors in columns")
    m = _metric_matrix(metric, v.shape[0])
    out = v.copy()
    for j in range(out.shape[1]):
        norm2 = float(out[:, j].T @ m @ out[:, j])
        if norm2 <= 0:
            raise ValueError("Each vector must have positive norm under the supplied metric")
        out[:, j] /= np.sqrt(norm2)
    return out


def modal_overlap(parent_vectors: np.ndarray, child_vectors: np.ndarray, metric: np.ndarray, projector: np.ndarray | None = None) -> np.ndarray:
    vp = mass_normalize_columns(parent_vectors, metric)
    vc = mass_normalize_columns(child_vectors, metric)
    p = np.eye(vp.shape[0]) if projector is None else np.asarray(projector, dtype=float)
    if p.shape != (vp.shape[0], vp.shape[0]):
        raise ValueError("projector shape mismatch")
    m = _metric_matrix(metric, vp.shape[0])
    amp = vp.T @ m @ p @ vc
    return np.abs(amp) ** 2


def principal_angle_cosines(parent_subspace: np.ndarray, child_subspace: np.ndarray, metric: np.ndarray) -> np.ndarray:
    vp = mass_normalize_columns(parent_subspace, metric)
    vc = mass_normalize_columns(child_subspace, metric)
    m = _metric_matrix(metric, vp.shape[0])
    singular_values = np.linalg.svd(vp.T @ m @ vc, compute_uv=False)
    return np.clip(singular_values, 0.0, 1.0)


def dynamic_stiffness(k: np.ndarray, m: np.ndarray, omega: float, c: np.ndarray | None = None) -> np.ndarray:
    k = np.asarray(k, dtype=complex)
    m = np.asarray(m, dtype=complex)
    if k.shape != m.shape or k.ndim != 2 or k.shape[0] != k.shape[1]:
        raise ValueError("k and m must be square matrices of equal shape")
    damping = np.zeros_like(k) if c is None else np.asarray(c, dtype=complex)
    if damping.shape != k.shape:
        raise ValueError("c shape mismatch")
    return k - (omega ** 2) * m + 1j * omega * damping


def schur_effective_child(d_ss: np.ndarray, d_sa: np.ndarray, d_as: np.ndarray, d_aa: np.ndarray) -> np.ndarray:
    d_ss = np.asarray(d_ss, dtype=complex)
    d_sa = np.asarray(d_sa, dtype=complex)
    d_as = np.asarray(d_as, dtype=complex)
    d_aa = np.asarray(d_aa, dtype=complex)
    return d_aa - d_as @ np.linalg.solve(d_ss, d_sa)


def substrate_self_energy(d_ss: np.ndarray, d_sa: np.ndarray, d_as: np.ndarray) -> np.ndarray:
    d_ss = np.asarray(d_ss, dtype=complex)
    d_sa = np.asarray(d_sa, dtype=complex)
    d_as = np.asarray(d_as, dtype=complex)
    return d_as @ np.linalg.solve(d_ss, d_sa)


def finite_harmonic_kernel(omega: np.ndarray, weights: np.ndarray, times: np.ndarray) -> np.ndarray:
    omega = np.asarray(omega, dtype=float)
    weights = np.asarray(weights, dtype=float)
    times = np.asarray(times, dtype=float)
    if omega.ndim != 1 or weights.ndim != 1 or omega.shape != weights.shape:
        raise ValueError("omega and weights must be one-dimensional arrays of equal length")
    return np.sum(weights[:, None] * np.cos(omega[:, None] * times[None, :]), axis=0)


def finite_difference_transfer(parent: np.ndarray, child_fn, eps: float = 1e-6) -> np.ndarray:
    x = np.asarray(parent, dtype=float)
    base = np.asarray(child_fn(x), dtype=float)
    transfer = np.empty((base.size, x.size), dtype=float)
    for i in range(x.size):
        xp = x.copy()
        xm = x.copy()
        xp[i] += eps
        xm[i] -= eps
        transfer[:, i] = (np.asarray(child_fn(xp)) - np.asarray(child_fn(xm))) / (2.0 * eps)
    return transfer


def eigenvalue_preserving_modal_scramble(eigenvalues: np.ndarray, seed: int = 0) -> np.ndarray:
    eig = np.asarray(eigenvalues, dtype=float)
    rng = np.random.default_rng(seed)
    q, _ = np.linalg.qr(rng.normal(size=(eig.size, eig.size)))
    return q @ np.diag(eig) @ q.T


def synthetic_validation() -> dict:
    metric = np.ones(3)
    parent_modes = np.eye(3)
    theta = 0.20
    child_modes = np.array([
        [np.cos(theta), -np.sin(theta), 0.0],
        [np.sin(theta), np.cos(theta), 0.0],
        [0.0, 0.0, 1.0],
    ])
    overlap = modal_overlap(parent_modes, child_modes, metric)

    k_ss = np.array([[4.0, 0.4], [0.4, 3.0]])
    m_ss = np.eye(2)
    k_aa = np.array([[2.2]])
    m_aa = np.array([[1.0]])
    k_sa = np.array([[0.30], [0.15]])
    omega = 0.7
    d_ss = dynamic_stiffness(k_ss, m_ss, omega)
    d_aa = dynamic_stiffness(k_aa, m_aa, omega)
    d_eff = schur_effective_child(d_ss, k_sa, k_sa.T, d_aa)
    sigma = substrate_self_energy(d_ss, k_sa, k_sa.T)
    schur_residual = float(np.max(np.abs(d_eff - (d_aa - sigma))))

    parent_parameters = np.array([4.0, 3.0])

    def child_response(x):
        local = np.array([[x[0], 0.4], [0.4, x[1]]])
        ds = dynamic_stiffness(local, m_ss, omega)
        return np.array([np.real(substrate_self_energy(ds, k_sa, k_sa.T)[0, 0])])

    transfer = finite_difference_transfer(parent_parameters, child_response)

    scrambled_k = eigenvalue_preserving_modal_scramble(np.linalg.eigvalsh(k_ss), seed=20260829)
    scrambled_ds = dynamic_stiffness(scrambled_k, m_ss, omega)
    scrambled_sigma = substrate_self_energy(scrambled_ds, k_sa, k_sa.T)
    specificity_gap = float(abs(np.real(scrambled_sigma[0, 0] - sigma[0, 0])))

    times = np.linspace(0.0, 100.0, 2001)
    kernel = finite_harmonic_kernel(np.array([0.7, 1.1, 1.6]), np.array([0.6, 0.3, 0.1]), times)
    late_recurrence_amplitude = float(np.max(np.abs(kernel[times > 50.0])))

    return {
        "scope": "synthetic_software_validation_only",
        "modal_overlap": overlap.tolist(),
        "schur_identity_residual": schur_residual,
        "finite_difference_transfer": transfer.tolist(),
        "eigenvalue_preserving_scramble_specificity_gap": specificity_gap,
        "finite_bath_late_recurrence_amplitude": late_recurrence_amplitude,
        "interpretation": {
            "modal_overlap": "tests carrier correspondence machinery",
            "schur_identity": "tests exact block elimination implementation",
            "transfer": "tests parent-to-child intervention machinery",
            "scramble": "tests a modal-specificity null while preserving eigenvalues",
            "finite_bath": "demonstrates that finite harmonic mode sets retain recurrence and are not automatically irreversible friction"
        }
    }


def write_synthetic_validation(path: str | Path) -> dict:
    result = synthetic_validation()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    output = write_synthetic_validation("substrate_inheritance/results/synthetic_validation.json")
    print(json.dumps(output, indent=2, sort_keys=True))
