from __future__ import annotations

import json
from pathlib import Path

import numpy as np


SCOPE = "synthetic_electronic_inheritance_validation_only"
SEED = 20260850


def retarded_substrate_green(hamiltonian: np.ndarray, energy: float, eta: float) -> np.ndarray:
    h = np.asarray(hamiltonian, dtype=complex)
    if eta <= 0.0:
        raise ValueError("eta must be positive for the finite-system resolvent")
    z = complex(float(energy), float(eta))
    return np.linalg.inv(z * np.eye(h.shape[0], dtype=complex) - h)


def electronic_self_energy(
    substrate_hamiltonian: np.ndarray,
    coupling: np.ndarray,
    energy: float,
    eta: float,
) -> complex:
    v = np.asarray(coupling, dtype=complex).reshape(-1, 1)
    g = retarded_substrate_green(substrate_hamiltonian, energy, eta)
    return complex((v.conj().T @ g @ v)[0, 0])


def reduced_adsorbate_green(
    substrate_hamiltonian: np.ndarray,
    coupling: np.ndarray,
    adsorbate_energy: float,
    energy: float,
    eta: float,
) -> complex:
    sigma = electronic_self_energy(substrate_hamiltonian, coupling, energy, eta)
    z = complex(float(energy), float(eta))
    return complex(1.0 / (z - float(adsorbate_energy) - sigma))


def full_adsorbate_green(
    substrate_hamiltonian: np.ndarray,
    coupling: np.ndarray,
    adsorbate_energy: float,
    energy: float,
    eta: float,
) -> complex:
    hs = np.asarray(substrate_hamiltonian, dtype=complex)
    v = np.asarray(coupling, dtype=complex).reshape(-1, 1)
    full = np.block(
        [
            [hs, v],
            [v.conj().T, np.array([[complex(adsorbate_energy)]])],
        ]
    )
    z = complex(float(energy), float(eta))
    green = np.linalg.inv(z * np.eye(full.shape[0], dtype=complex) - full)
    return complex(green[-1, -1])


def self_energy_curve(
    substrate_hamiltonian: np.ndarray,
    coupling: np.ndarray,
    energies: np.ndarray,
    eta: float,
) -> np.ndarray:
    return np.array(
        [electronic_self_energy(substrate_hamiltonian, coupling, float(e), eta) for e in energies],
        dtype=complex,
    )


def _random_orthogonal(rng: np.random.Generator, n: int) -> np.ndarray:
    q, r = np.linalg.qr(rng.normal(size=(n, n)))
    signs = np.sign(np.diag(r))
    signs[signs == 0.0] = 1.0
    return q @ np.diag(signs)


def schur_identity_case() -> dict:
    hs = np.array(
        [
            [-1.5, 0.25, 0.0],
            [0.25, 0.2, 0.35],
            [0.0, 0.35, 1.4],
        ]
    )
    coupling = np.array([0.4, 0.15, 0.25])
    adsorbate_energy = 0.55
    energies = np.linspace(-2.0, 2.0, 81)
    eta = 0.08
    residuals = []
    for energy in energies:
        reduced = reduced_adsorbate_green(hs, coupling, adsorbate_energy, float(energy), eta)
        full = full_adsorbate_green(hs, coupling, adsorbate_energy, float(energy), eta)
        residuals.append(abs(reduced - full))
    return {
        "energy_points": int(energies.size),
        "eta": eta,
        "eta_role": "finite-system resolvent regularization only, not mechanical damping",
        "maximum_full_vs_reduced_green_residual": float(np.max(residuals)),
        "interpretation": (
            "Checks exact electronic block elimination by comparing the adsorbate Green function from the full Hamiltonian with the substrate-self-energy reduction."
        ),
    }


def basis_invariance_case() -> dict:
    rng = np.random.default_rng(SEED)
    eigenvalues = np.array([-2.0, -0.8, 0.1, 1.1, 2.4])
    hs = np.diag(eigenvalues)
    coupling = np.array([0.55, 0.25, 0.15, 0.35, 0.20])
    coupling = coupling / np.linalg.norm(coupling)
    q = _random_orthogonal(rng, 5)

    energies = np.linspace(-2.8, 2.8, 121)
    eta = 0.06
    original = self_energy_curve(hs, coupling, energies, eta)
    transformed_h = q.T @ hs @ q
    transformed_v = q.T @ coupling
    transformed = self_energy_curve(transformed_h, transformed_v, energies, eta)

    return {
        "maximum_curve_residual": float(np.max(np.abs(original - transformed))),
        "interpretation": (
            "A common basis change of substrate Hamiltonian and interface coupling must not alter the electronic self-energy."
        ),
    }


def same_spectrum_carrier_scramble_ensemble(
    trials: int = 256,
    dimension: int = 5,
    seed: int = SEED + 1,
) -> dict:
    rng = np.random.default_rng(seed)
    eigenvalues = np.linspace(-2.0, 2.0, dimension)
    hs = np.diag(eigenvalues)
    coupling = rng.normal(size=dimension)
    coupling /= np.linalg.norm(coupling)
    energies = np.linspace(-2.6, 2.6, 101)
    eta = 0.08
    reference = self_energy_curve(hs, coupling, energies, eta)
    reference_scale = max(float(np.linalg.norm(reference)), 1e-15)

    relative_curve_gaps: list[float] = []
    spectrum_errors: list[float] = []
    for _ in range(trials):
        q = _random_orthogonal(rng, dimension)
        scrambled_h = q @ np.diag(eigenvalues) @ q.T
        scrambled = self_energy_curve(scrambled_h, coupling, energies, eta)
        relative_curve_gaps.append(float(np.linalg.norm(scrambled - reference) / reference_scale))
        spectrum_errors.append(
            float(np.max(np.abs(np.linalg.eigvalsh(scrambled_h) - eigenvalues)))
        )

    gaps = np.asarray(relative_curve_gaps)
    return {
        "trials": trials,
        "dimension": dimension,
        "eta": eta,
        "eta_role": "finite-system resolvent regularization only, not mechanical damping",
        "maximum_same_spectrum_numerical_error": float(np.max(spectrum_errors)),
        "relative_self_energy_curve_gap": {
            "mean": float(np.mean(gaps)),
            "median": float(np.median(gaps)),
            "q05": float(np.quantile(gaps, 0.05)),
            "q95": float(np.quantile(gaps, 0.95)),
            "fraction_nonzero_above_machine_scale": float(np.mean(gaps > 1e-12)),
        },
        "interpretation": (
            "Preserves the electronic substrate eigenvalue spectrum while scrambling orbital/modal geometry relative to a fixed physical interface coupling. "
            "A changed self-energy curve shows that electronic influence depends on carrier/coupling structure, not the scalar spectrum alone."
        ),
    }


def run_electronic_validation() -> dict:
    return {
        "scope": SCOPE,
        "physical_thresholds_frozen": False,
        "real_system_evidence": False,
        "mechanical_damping_inferred": False,
        "electronic_hybridization_identified_with_mechanical_gamma": False,
        "schur_identity": schur_identity_case(),
        "basis_invariance": basis_invariance_case(),
        "same_spectrum_carrier_scramble": same_spectrum_carrier_scramble_ensemble(),
        "reporting_rule": (
            "Electronic substrate self-energy and hybridization are retained as electronic-channel objects. They must not be silently renamed mechanical damping or added to a phononic gamma without an independent derivation."
        ),
    }


def write_electronic_validation(path: str | Path) -> dict:
    result = run_electronic_validation()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    output = write_electronic_validation("substrate_inheritance/results/electronic_validation.json")
    print(json.dumps(output, indent=2, sort_keys=True))
