from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from substrate_inheritance.inheritance_engine import dynamic_stiffness, substrate_self_energy


SCOPE = "synthetic_identifiability_validation_only"
SEED = 20260833


def _unit_vector(rng: np.random.Generator, dimension: int) -> np.ndarray:
    v = rng.normal(size=(dimension, 1))
    return v / np.linalg.norm(v)


def _self_energy_scalar(k_diag: np.ndarray, coupling: np.ndarray, omega: float) -> float:
    d = dynamic_stiffness(np.diag(k_diag), np.eye(k_diag.size), omega)
    sigma = substrate_self_energy(d, coupling, coupling.T)
    return float(np.real(sigma[0, 0]))


def equivalent_single_frequency_couplings(
    k_diag: np.ndarray,
    coupling_reference: np.ndarray,
    trial_direction: np.ndarray,
    omega: float,
) -> tuple[np.ndarray, float, float]:
    """Construct a distinct coupling with the same scalar self-energy at one frequency.

    For positive real D at the selected synthetic frequency, Sigma = c^T D^-1 c.
    Scaling any nonzero trial direction can reproduce the same scalar Sigma. This
    construction is used to demonstrate nonidentifiability, not to fit physical data.
    """
    k_diag = np.asarray(k_diag, dtype=float)
    c_ref = np.asarray(coupling_reference, dtype=float).reshape(-1, 1)
    direction = np.asarray(trial_direction, dtype=float).reshape(-1, 1)
    if np.linalg.norm(direction) == 0.0:
        raise ValueError("trial_direction must be nonzero")

    d = dynamic_stiffness(np.diag(k_diag), np.eye(k_diag.size), omega)
    target = float(np.real(substrate_self_energy(d, c_ref, c_ref.T)[0, 0]))
    raw = float(np.real(substrate_self_energy(d, direction, direction.T)[0, 0]))
    if target <= 0.0 or raw <= 0.0:
        raise ValueError("synthetic construction requires a positive quadratic form")

    scaled = direction * np.sqrt(target / raw)
    matched = float(np.real(substrate_self_energy(d, scaled, scaled.T)[0, 0]))
    return scaled, target, matched


def run_identifiability_validation(
    trials: int = 256,
    dimension: int = 5,
    omega_match: float = 0.40,
    omega_probe: float = 0.90,
    seed: int = SEED,
) -> dict:
    rng = np.random.default_rng(seed)
    match_errors: list[float] = []
    coupling_cosines: list[float] = []
    probe_relative_gaps: list[float] = []

    for _ in range(trials):
        # Keep both probe frequencies below every synthetic stiffness scale so the
        # quadratic form remains positive and the construction is unambiguous.
        k_diag = rng.uniform(2.0, 7.0, size=dimension)
        reference = _unit_vector(rng, dimension)
        trial_direction = _unit_vector(rng, dimension)

        alternative, target, matched = equivalent_single_frequency_couplings(
            k_diag, reference, trial_direction, omega_match
        )
        match_errors.append(abs(target - matched))

        ref_unit = reference.reshape(-1) / np.linalg.norm(reference)
        alt_unit = alternative.reshape(-1) / np.linalg.norm(alternative)
        coupling_cosines.append(float(abs(np.dot(ref_unit, alt_unit))))

        ref_probe = _self_energy_scalar(k_diag, reference, omega_probe)
        alt_probe = _self_energy_scalar(k_diag, alternative, omega_probe)
        scale = max(abs(ref_probe), abs(alt_probe), 1e-15)
        probe_relative_gaps.append(float(abs(ref_probe - alt_probe) / scale))

    match = np.asarray(match_errors)
    cosines = np.asarray(coupling_cosines)
    probe = np.asarray(probe_relative_gaps)

    return {
        "scope": SCOPE,
        "seed": seed,
        "trials": trials,
        "dimension": dimension,
        "omega_match": omega_match,
        "omega_probe": omega_probe,
        "physical_thresholds_frozen": False,
        "real_system_evidence": False,
        "single_scalar_response_identifies_unique_coupling": False,
        "matched_frequency_self_energy_error": {
            "maximum": float(np.max(match)),
            "mean": float(np.mean(match)),
        },
        "absolute_coupling_direction_cosine": {
            "mean": float(np.mean(cosines)),
            "median": float(np.median(cosines)),
            "q05": float(np.quantile(cosines, 0.05)),
            "q95": float(np.quantile(cosines, 0.95)),
        },
        "second_frequency_relative_response_gap": {
            "mean": float(np.mean(probe)),
            "median": float(np.median(probe)),
            "q05": float(np.quantile(probe, 0.05)),
            "q95": float(np.quantile(probe, 0.95)),
            "fraction_nonzero_above_machine_scale": float(np.mean(probe > 1e-12)),
        },
        "interpretation": (
            "Distinct substrate-to-child coupling geometries can be scaled to produce the same scalar child response at one frequency. "
            "A second frequency generally separates them. Therefore a single scalar response can establish influence but cannot by itself identify conglomerative inheritance."
        ),
    }


def write_identifiability_validation(path: str | Path) -> dict:
    result = run_identifiability_validation()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    output = write_identifiability_validation("substrate_inheritance/results/identifiability_validation.json")
    print(json.dumps(output, indent=2, sort_keys=True))
