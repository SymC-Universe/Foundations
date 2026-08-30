from __future__ import annotations

import json
from pathlib import Path

import numpy as np


SCOPE = "synthetic_inheritance_depth_validation_only"


def finite_chain_dynamic_matrix(length: int, onsite: complex, hopping: float) -> np.ndarray:
    if length < 1:
        raise ValueError("length must be positive")
    d = np.eye(length, dtype=complex) * onsite
    if length > 1:
        idx = np.arange(length - 1)
        d[idx, idx + 1] = -hopping
        d[idx + 1, idx] = -hopping
    return d


def finite_surface_green(length: int, onsite: complex, hopping: float) -> complex:
    d = finite_chain_dynamic_matrix(length, onsite, hopping)
    unit = np.zeros((length, 1), dtype=complex)
    unit[0, 0] = 1.0
    solution = np.linalg.solve(d, unit)
    return complex(solution[0, 0])


def recursive_surface_green(length: int, onsite: complex, hopping: float) -> complex:
    if length < 1:
        raise ValueError("length must be positive")
    g = 1.0 / onsite
    for _ in range(1, length):
        g = 1.0 / (onsite - (hopping**2) * g)
    return complex(g)


def semi_infinite_surface_green(onsite: complex, hopping: float) -> complex:
    if hopping == 0.0:
        return complex(1.0 / onsite)
    discriminant = onsite**2 - 4.0 * (hopping**2)
    root = np.sqrt(discriminant)
    candidates = [
        (onsite - root) / (2.0 * hopping**2),
        (onsite + root) / (2.0 * hopping**2),
    ]
    # The stable continued-fraction solution is the root with smaller magnitude.
    return complex(min(candidates, key=abs))


def inheritance_depth_curve(
    lengths: tuple[int, ...] = (1, 2, 4, 8, 16, 32, 64),
    substrate_onsite_stiffness: float = 4.0,
    hopping: float = 0.8,
    complex_probe_frequency: complex = 0.70 + 0.15j,
    child_coupling: float = 0.6,
) -> dict:
    z = complex(complex_probe_frequency)
    onsite = complex(substrate_onsite_stiffness) - z**2
    g_inf = semi_infinite_surface_green(onsite, hopping)
    sigma_inf = (child_coupling**2) * g_inf

    records = []
    for length in lengths:
        g_matrix = finite_surface_green(length, onsite, hopping)
        g_recursive = recursive_surface_green(length, onsite, hopping)
        sigma = (child_coupling**2) * g_matrix
        relative_error = abs(sigma - sigma_inf) / max(abs(sigma_inf), 1e-15)
        records.append(
            {
                "substrate_depth_dof": int(length),
                "self_energy_real": float(np.real(sigma)),
                "self_energy_imag": float(np.imag(sigma)),
                "relative_error_to_semi_infinite": float(relative_error),
                "matrix_vs_recursive_residual": float(abs(g_matrix - g_recursive)),
            }
        )

    return {
        "substrate_model": "uniform_nearest_neighbor_chain",
        "complex_probe_frequency": [float(np.real(z)), float(np.imag(z))],
        "imaginary_probe_component_role": "explicit numerical/analytic resolvent regularization, not physical damping",
        "substrate_onsite_stiffness": substrate_onsite_stiffness,
        "hopping": hopping,
        "child_coupling": child_coupling,
        "semi_infinite_self_energy": {
            "real": float(np.real(sigma_inf)),
            "imag": float(np.imag(sigma_inf)),
        },
        "depth_curve": records,
        "interpretation": (
            "Validates a substrate-depth convergence calculation against an analytic semi-infinite embedding. "
            "The numerical depth is a synthetic model size, not a physical inheritance length for any material."
        ),
    }


def coupling_strength_depth_sweep() -> list[dict]:
    results = []
    for hopping in (0.35, 0.65, 0.95, 1.25):
        result = inheritance_depth_curve(hopping=hopping)
        results.append(
            {
                "hopping": hopping,
                "depth_curve": [
                    {
                        "substrate_depth_dof": row["substrate_depth_dof"],
                        "relative_error_to_semi_infinite": row["relative_error_to_semi_infinite"],
                    }
                    for row in result["depth_curve"]
                ],
            }
        )
    return results


def run_depth_validation() -> dict:
    return {
        "scope": SCOPE,
        "physical_thresholds_frozen": False,
        "real_system_evidence": False,
        "reference_depth_curve": inheritance_depth_curve(),
        "coupling_strength_depth_sweep": coupling_strength_depth_sweep(),
        "purpose": (
            "Validate the machinery needed to ask how a child embedding response converges as progressively more substrate degrees of freedom are retained."
        ),
    }


def write_depth_validation(path: str | Path) -> dict:
    result = run_depth_validation()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    output = write_depth_validation("substrate_inheritance/results/depth_validation.json")
    print(json.dumps(output, indent=2, sort_keys=True))
