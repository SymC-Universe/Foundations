from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

from substrate_inheritance.inheritance_engine import (
    dynamic_stiffness,
    finite_difference_transfer,
    modal_overlap,
    substrate_self_energy,
)


SCOPE = "synthetic_ensemble_validation_only"
SEED = 20260830


def best_assignment_score(overlap: np.ndarray) -> float:
    """Maximum mean one-to-one modal overlap across all carrier assignments.

    This is a synthetic diagnostic, not a physical inheritance threshold.
    Dimensions used by this validation are intentionally small enough that exact
    permutation enumeration is preferable to adding an optimization dependency.
    """
    matrix = np.asarray(overlap, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("overlap must be a square matrix")
    n = matrix.shape[0]
    rows = np.arange(n)
    best = -np.inf
    for perm in itertools.permutations(range(n)):
        value = float(np.mean(matrix[rows, np.asarray(perm)]))
        if value > best:
            best = value
    return best


def auc_probability(positive: np.ndarray, negative: np.ndarray) -> float:
    """Probability that a random positive score exceeds a random negative score.

    Ties count as one half. This is threshold free and is used only to describe
    synthetic discriminability.
    """
    pos = np.asarray(positive, dtype=float)
    neg = np.asarray(negative, dtype=float)
    diff = pos[:, None] - neg[None, :]
    return float(np.mean(diff > 0.0) + 0.5 * np.mean(diff == 0.0))


def _random_orthogonal(rng: np.random.Generator, n: int) -> np.ndarray:
    q, r = np.linalg.qr(rng.normal(size=(n, n)))
    signs = np.sign(np.diag(r))
    signs[signs == 0.0] = 1.0
    return q @ np.diag(signs)


def _planted_rotation(rng: np.random.Generator, n: int, angle_scale: float = 0.18) -> np.ndarray:
    """Generate a known near-parent carrier map for synthetic validation only."""
    q = np.eye(n)
    order = rng.permutation(n)
    for a, b in zip(order[:-1], order[1:]):
        theta = float(rng.normal(0.0, angle_scale))
        g = np.eye(n)
        c = np.cos(theta)
        s = np.sin(theta)
        g[a, a] = c
        g[b, b] = c
        g[a, b] = -s
        g[b, a] = s
        q = q @ g
    return q


def modal_same_spectrum_ensemble(trials: int = 256, dimension: int = 5, seed: int = SEED) -> dict:
    rng = np.random.default_rng(seed)
    eigenvalues = np.linspace(1.0, 5.0, dimension)
    parent_modes = np.eye(dimension)
    metric = np.ones(dimension)

    planted_scores: list[float] = []
    null_scores: list[float] = []
    max_spectrum_errors: list[float] = []

    for _ in range(trials):
        planted_modes = _planted_rotation(rng, dimension)
        planted_overlap = modal_overlap(parent_modes, planted_modes, metric)
        planted_scores.append(best_assignment_score(planted_overlap))

        null_modes = _random_orthogonal(rng, dimension)
        null_overlap = modal_overlap(parent_modes, null_modes, metric)
        null_scores.append(best_assignment_score(null_overlap))

        # The null deliberately keeps the scalar spectrum exactly unchanged.
        parent_k = np.diag(eigenvalues)
        null_k = null_modes @ np.diag(eigenvalues) @ null_modes.T
        max_spectrum_errors.append(
            float(np.max(np.abs(np.linalg.eigvalsh(parent_k) - np.linalg.eigvalsh(null_k))))
        )

    planted = np.asarray(planted_scores)
    null = np.asarray(null_scores)
    return {
        "trials": trials,
        "dimension": dimension,
        "synthetic_generator_angle_scale_rad": 0.18,
        "same_scalar_spectrum_null": True,
        "max_same_spectrum_numerical_error": float(np.max(max_spectrum_errors)),
        "planted_assignment_score": {
            "mean": float(np.mean(planted)),
            "median": float(np.median(planted)),
            "q05": float(np.quantile(planted, 0.05)),
            "q95": float(np.quantile(planted, 0.95)),
        },
        "same_spectrum_scrambled_assignment_score": {
            "mean": float(np.mean(null)),
            "median": float(np.median(null)),
            "q05": float(np.quantile(null, 0.05)),
            "q95": float(np.quantile(null, 0.95)),
        },
        "threshold_free_auc_probability": auc_probability(planted, null),
        "interpretation": (
            "Tests whether carrier-resolved modal information distinguishes a planted parent-to-child map "
            "from a null with the same eigenvalue spectrum. No physical acceptance threshold is inferred."
        ),
    }


def coupling_rewire_ensemble(trials: int = 256, dimension: int = 5, seed: int = SEED + 1) -> dict:
    rng = np.random.default_rng(seed)
    eigenvalues = np.linspace(2.0, 6.0, dimension)
    omega = 0.65
    relative_gaps: list[float] = []

    for _ in range(trials):
        modes = _random_orthogonal(rng, dimension)
        k_ss = modes @ np.diag(eigenvalues) @ modes.T
        d_ss = dynamic_stiffness(k_ss, np.eye(dimension), omega)

        coupling = rng.normal(size=(dimension, 1))
        coupling /= np.linalg.norm(coupling)
        rewired = coupling[rng.permutation(dimension), :]

        sigma = substrate_self_energy(d_ss, coupling, coupling.T)[0, 0]
        sigma_rewired = substrate_self_energy(d_ss, rewired, rewired.T)[0, 0]
        scale = max(abs(sigma), abs(sigma_rewired), 1e-15)
        relative_gaps.append(float(abs(sigma - sigma_rewired) / scale))

    gaps = np.asarray(relative_gaps)
    return {
        "trials": trials,
        "dimension": dimension,
        "substrate_spectrum_changed_by_rewire": False,
        "relative_self_energy_change": {
            "mean": float(np.mean(gaps)),
            "median": float(np.median(gaps)),
            "q05": float(np.quantile(gaps, 0.05)),
            "q95": float(np.quantile(gaps, 0.95)),
            "fraction_nonzero_above_machine_scale": float(np.mean(gaps > 1e-12)),
        },
        "interpretation": (
            "Tests conglomeration specificity by rewiring the substrate-to-child coupling while preserving the substrate operator. "
            "The response change is descriptive synthetic evidence, not a physical cutoff."
        ),
    }


def _analytic_diagonal_stiffness_transfer(k_diag: np.ndarray, coupling: np.ndarray, omega: float) -> np.ndarray:
    d = np.diag(k_diag) - (omega**2) * np.eye(k_diag.size)
    z = np.linalg.solve(d, coupling.reshape(-1, 1)).reshape(-1)
    # Sigma = c^T D^-1 c and dSigma/dk_i = -(e_i^T D^-1 c)^2.
    return (-(z**2)).reshape(1, -1)


def transfer_consistency_ensemble(trials: int = 256, dimension: int = 5, seed: int = SEED + 2) -> dict:
    rng = np.random.default_rng(seed)
    omega = 0.55
    relative_errors: list[float] = []

    for _ in range(trials):
        k_diag = rng.uniform(2.0, 7.0, size=dimension)
        coupling = rng.normal(size=(dimension, 1))
        coupling /= np.linalg.norm(coupling)

        def child_fn(x: np.ndarray) -> np.ndarray:
            d_ss = dynamic_stiffness(np.diag(x), np.eye(dimension), omega)
            sigma = substrate_self_energy(d_ss, coupling, coupling.T)
            return np.array([float(np.real(sigma[0, 0]))])

        numerical = finite_difference_transfer(k_diag, child_fn, eps=1e-6)
        analytic = _analytic_diagonal_stiffness_transfer(k_diag, coupling, omega)
        denom = max(float(np.linalg.norm(analytic)), 1e-15)
        relative_errors.append(float(np.linalg.norm(numerical - analytic) / denom))

    errors = np.asarray(relative_errors)
    return {
        "trials": trials,
        "dimension": dimension,
        "relative_transfer_error": {
            "mean": float(np.mean(errors)),
            "median": float(np.median(errors)),
            "maximum": float(np.max(errors)),
            "q95": float(np.quantile(errors, 0.95)),
        },
        "interpretation": (
            "Cross-checks the numerical parent-to-child intervention map against an analytic derivative in a synthetic diagonal substrate."
        ),
    }


def run_ensemble_validation() -> dict:
    modal = modal_same_spectrum_ensemble()
    coupling = coupling_rewire_ensemble()
    transfer = transfer_consistency_ensemble()
    return {
        "scope": SCOPE,
        "seed": SEED,
        "physical_thresholds_frozen": False,
        "real_system_evidence": False,
        "purpose": (
            "Threshold-free ensemble falsification and numerical validation before real-system substrate-inheritance target reveal."
        ),
        "modal_same_spectrum_ensemble": modal,
        "coupling_rewire_ensemble": coupling,
        "transfer_consistency_ensemble": transfer,
    }


def write_ensemble_validation(path: str | Path) -> dict:
    result = run_ensemble_validation()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    output = write_ensemble_validation("substrate_inheritance/results/ensemble_validation.json")
    print(json.dumps(output, indent=2, sort_keys=True))
