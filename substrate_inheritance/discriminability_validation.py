from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from substrate_inheritance.ensemble_validation import (
    SEED,
    auc_probability,
    best_assignment_score,
)
from substrate_inheritance.inheritance_engine import modal_overlap


SCOPE = "synthetic_discriminability_strength_validation_only"


def _random_orthogonal(rng: np.random.Generator, n: int) -> np.ndarray:
    q, r = np.linalg.qr(rng.normal(size=(n, n)))
    signs = np.sign(np.diag(r))
    signs[signs == 0.0] = 1.0
    return q @ np.diag(signs)


def _planted_rotation(rng: np.random.Generator, n: int, angle_scale: float) -> np.ndarray:
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


def discriminability_strength_sweep(
    angle_scales: tuple[float, ...] = (0.0, 0.05, 0.10, 0.20, 0.35, 0.55, 0.80, 1.20, 1.80),
    trials_per_scale: int = 256,
    dimension: int = 5,
    seed: int = SEED + 10,
) -> dict:
    """Measure threshold-free separation as a planted carrier map is weakened.

    The scalar spectrum is identical for planted and null cases at every strength.
    Angle scale is a synthetic generator parameter and is not a physical inheritance
    coordinate or promotion threshold.
    """
    rng = np.random.default_rng(seed)
    parent_modes = np.eye(dimension)
    metric = np.ones(dimension)

    rows = []
    for scale in angle_scales:
        planted_scores: list[float] = []
        null_scores: list[float] = []
        for _ in range(trials_per_scale):
            planted = _planted_rotation(rng, dimension, float(scale))
            null = _random_orthogonal(rng, dimension)
            planted_scores.append(best_assignment_score(modal_overlap(parent_modes, planted, metric)))
            null_scores.append(best_assignment_score(modal_overlap(parent_modes, null, metric)))

        p = np.asarray(planted_scores)
        n = np.asarray(null_scores)
        rows.append(
            {
                "synthetic_angle_scale_rad": float(scale),
                "planted_mean": float(np.mean(p)),
                "planted_median": float(np.median(p)),
                "planted_q05": float(np.quantile(p, 0.05)),
                "planted_q95": float(np.quantile(p, 0.95)),
                "null_mean": float(np.mean(n)),
                "null_median": float(np.median(n)),
                "null_q05": float(np.quantile(n, 0.05)),
                "null_q95": float(np.quantile(n, 0.95)),
                "threshold_free_auc_probability": auc_probability(p, n),
                "mean_score_gap": float(np.mean(p) - np.mean(n)),
            }
        )

    return {
        "dimension": dimension,
        "trials_per_strength": trials_per_scale,
        "same_scalar_spectrum_at_every_strength": True,
        "strength_parameter_is_physical_threshold": False,
        "rows": rows,
        "interpretation": (
            "Maps where the current modal-correspondence statistic loses threshold-free discriminability as the planted carrier relation is progressively randomized. "
            "This is a method failure-boundary study, not calibration of a real-system inheritance cutoff."
        ),
    }


def run_discriminability_validation() -> dict:
    sweep = discriminability_strength_sweep()
    aucs = np.array([row["threshold_free_auc_probability"] for row in sweep["rows"]])
    gaps = np.array([row["mean_score_gap"] for row in sweep["rows"]])
    return {
        "scope": SCOPE,
        "seed": SEED + 10,
        "physical_thresholds_frozen": False,
        "real_system_evidence": False,
        "sweep": sweep,
        "summary": {
            "maximum_auc": float(np.max(aucs)),
            "minimum_auc": float(np.min(aucs)),
            "maximum_mean_score_gap": float(np.max(gaps)),
            "minimum_mean_score_gap": float(np.min(gaps)),
        },
    }


def write_discriminability_validation(path: str | Path) -> dict:
    result = run_discriminability_validation()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    output = write_discriminability_validation("substrate_inheritance/results/discriminability_validation.json")
    print(json.dumps(output, indent=2, sort_keys=True))
