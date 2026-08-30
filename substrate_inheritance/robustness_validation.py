from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from substrate_inheritance.ensemble_validation import best_assignment_score
from substrate_inheritance.inheritance_engine import (
    dynamic_stiffness,
    modal_overlap,
    principal_angle_cosines,
    substrate_self_energy,
)


SCOPE = "synthetic_robustness_validation_only"
SEED = 20260834


def _random_orthogonal(rng: np.random.Generator, n: int) -> np.ndarray:
    q, r = np.linalg.qr(rng.normal(size=(n, n)))
    signs = np.sign(np.diag(r))
    signs[signs == 0.0] = 1.0
    return q @ np.diag(signs)


def coordinate_invariance_ensemble(trials: int = 256, dimension: int = 5, seed: int = SEED) -> dict:
    rng = np.random.default_rng(seed)
    orthogonal_residuals: list[float] = []
    scaling_residuals: list[float] = []

    for _ in range(trials):
        a = rng.normal(size=(dimension, dimension))
        k = a.T @ a + 3.0 * np.eye(dimension)
        omega = float(rng.uniform(0.15, 0.65))
        d = dynamic_stiffness(k, np.eye(dimension), omega)
        c = rng.normal(size=(dimension, 1))
        sigma = substrate_self_energy(d, c, c.T)[0, 0]

        q = _random_orthogonal(rng, dimension)
        d_q = q.T @ d @ q
        c_q = q.T @ c
        sigma_q = substrate_self_energy(d_q, c_q, c_q.T)[0, 0]
        orthogonal_residuals.append(float(abs(sigma - sigma_q)))

        scales = rng.uniform(0.4, 2.5, size=dimension)
        s = np.diag(scales)
        d_s = s.T @ d @ s
        c_s = s.T @ c
        sigma_s = substrate_self_energy(d_s, c_s, c_s.T)[0, 0]
        scaling_residuals.append(float(abs(sigma - sigma_s)))

    ortho = np.asarray(orthogonal_residuals)
    scale = np.asarray(scaling_residuals)
    return {
        "trials": trials,
        "dimension": dimension,
        "orthogonal_basis_change_residual": {
            "maximum": float(np.max(ortho)),
            "mean": float(np.mean(ortho)),
        },
        "invertible_coordinate_scaling_residual": {
            "maximum": float(np.max(scale)),
            "mean": float(np.mean(scale)),
        },
        "interpretation": (
            "Tests whether the substrate embedding/self-energy calculation is invariant under consistent changes of substrate coordinates. "
            "An inheritance claim must not depend on an arbitrary coordinate representation."
        ),
    }


def _symmetric_noise(rng: np.random.Generator, n: int, amplitude: float) -> np.ndarray:
    raw = rng.normal(size=(n, n))
    sym = 0.5 * (raw + raw.T)
    norm = np.linalg.norm(sym)
    return sym * (amplitude / norm)


def degeneracy_robustness_ensemble(
    trials: int = 256,
    dimension: int = 5,
    perturbation_norm: float = 1e-4,
    seed: int = SEED + 1,
) -> dict:
    rng = np.random.default_rng(seed)
    metric = np.ones(dimension)

    near_eigs = np.array([1.0, 1.0 + 1e-8, 3.0, 5.0, 7.0])[:dimension]
    separated_eigs = np.array([1.0, 1.7, 3.0, 5.0, 7.0])[:dimension]
    parent_near = np.diag(near_eigs)
    parent_sep = np.diag(separated_eigs)
    _, parent_near_vecs = np.linalg.eigh(parent_near)
    _, parent_sep_vecs = np.linalg.eigh(parent_sep)

    near_individual_scores: list[float] = []
    near_min_subspace_cosines: list[float] = []
    sep_individual_scores: list[float] = []
    sep_min_subspace_cosines: list[float] = []

    for _ in range(trials):
        noise = _symmetric_noise(rng, dimension, perturbation_norm)

        _, child_near_vecs = np.linalg.eigh(parent_near + noise)
        overlap_near = modal_overlap(parent_near_vecs[:, :2], child_near_vecs[:, :2], metric)
        near_individual_scores.append(best_assignment_score(overlap_near))
        near_cosines = principal_angle_cosines(parent_near_vecs[:, :2], child_near_vecs[:, :2], metric)
        near_min_subspace_cosines.append(float(np.min(near_cosines)))

        _, child_sep_vecs = np.linalg.eigh(parent_sep + noise)
        overlap_sep = modal_overlap(parent_sep_vecs[:, :2], child_sep_vecs[:, :2], metric)
        sep_individual_scores.append(best_assignment_score(overlap_sep))
        sep_cosines = principal_angle_cosines(parent_sep_vecs[:, :2], child_sep_vecs[:, :2], metric)
        sep_min_subspace_cosines.append(float(np.min(sep_cosines)))

    near_i = np.asarray(near_individual_scores)
    near_s = np.asarray(near_min_subspace_cosines)
    sep_i = np.asarray(sep_individual_scores)
    sep_s = np.asarray(sep_min_subspace_cosines)

    return {
        "trials": trials,
        "dimension": dimension,
        "perturbation_frobenius_norm": perturbation_norm,
        "near_degenerate_pair_gap": float(near_eigs[1] - near_eigs[0]),
        "separated_pair_gap": float(separated_eigs[1] - separated_eigs[0]),
        "near_degenerate": {
            "individual_assignment_mean": float(np.mean(near_i)),
            "individual_assignment_q05": float(np.quantile(near_i, 0.05)),
            "minimum_subspace_cosine_mean": float(np.mean(near_s)),
            "minimum_subspace_cosine_q05": float(np.quantile(near_s, 0.05)),
        },
        "separated": {
            "individual_assignment_mean": float(np.mean(sep_i)),
            "individual_assignment_q05": float(np.quantile(sep_i, 0.05)),
            "minimum_subspace_cosine_mean": float(np.mean(sep_s)),
            "minimum_subspace_cosine_q05": float(np.quantile(sep_s, 0.05)),
        },
        "interpretation": (
            "Tests the known failure mode in which nearly degenerate individual eigenvectors rotate strongly under tiny perturbations while their combined subspace remains stable. "
            "This validates the protocol requirement to use subspace geometry rather than forced one-to-one vectors in crowded sectors."
        ),
    }


def run_robustness_validation() -> dict:
    return {
        "scope": SCOPE,
        "seed": SEED,
        "physical_thresholds_frozen": False,
        "real_system_evidence": False,
        "coordinate_invariance": coordinate_invariance_ensemble(),
        "degeneracy_robustness": degeneracy_robustness_ensemble(),
    }


def write_robustness_validation(path: str | Path) -> dict:
    result = run_robustness_validation()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    output = write_robustness_validation("substrate_inheritance/results/robustness_validation.json")
    print(json.dumps(output, indent=2, sort_keys=True))
