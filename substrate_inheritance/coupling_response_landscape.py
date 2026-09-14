from __future__ import annotations

import json
from itertools import permutations
from pathlib import Path
from typing import Any

import numpy as np

from substrate_inheritance.inheritance_engine import dynamic_stiffness, substrate_self_energy


PLAN_SCHEMA = "substrate-inheritance-fm1-coupling-response-plan-v0.1"
RESULT_SCHEMA = "substrate-inheritance-fm1-coupling-response-result-v0.1"


class CouplingResponseRefusal(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _finite_nonnegative(name: str, value: Any) -> float:
    x = float(value)
    if not np.isfinite(x) or x < 0.0:
        raise CouplingResponseRefusal("INVALID_PARAMETER", f"{name} must be finite and nonnegative")
    return x


def _positive_vector(name: str, values: Any, n: int) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.shape != (n,) or not np.all(np.isfinite(arr)) or np.any(arr <= 0.0):
        raise CouplingResponseRefusal("INVALID_PARAMETER", f"{name} must contain {n} finite positive values")
    return arr


def _nonnegative_vector(name: str, values: Any, n: int) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.shape != (n,) or not np.all(np.isfinite(arr)) or np.any(arr < 0.0):
        raise CouplingResponseRefusal("INVALID_PARAMETER", f"{name} must contain {n} finite nonnegative values")
    return arr


def rotation_matrix(theta: float) -> np.ndarray:
    theta = float(theta)
    if not np.isfinite(theta):
        raise CouplingResponseRefusal("INVALID_PARAMETER", "theta must be finite")
    c1, s1 = np.cos(theta), np.sin(theta)
    phi = 0.6 * theta
    c2, s2 = np.cos(phi), np.sin(phi)
    return np.array(
        [
            [c1, -s1, 0.0, 0.0],
            [s1, c1, 0.0, 0.0],
            [0.0, 0.0, c2, -s2],
            [0.0, 0.0, s2, c2],
        ],
        dtype=float,
    )


def clean_parent_system(stiffness_eigenvalues: Any, masses: Any) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    eig = _positive_vector("parent_stiffness_eigenvalues", stiffness_eigenvalues, 4)
    mass_diag = _positive_vector("parent_masses", masses, 4)
    mass = np.diag(mass_diag)
    stiffness = np.diag(eig)
    weighted = np.diag(1.0 / np.sqrt(mass_diag)) @ stiffness @ np.diag(1.0 / np.sqrt(mass_diag))
    values, standard_vectors = np.linalg.eigh(weighted)
    modes = np.diag(1.0 / np.sqrt(mass_diag)) @ standard_vectors
    frequencies = np.sqrt(values)
    return mass, stiffness, frequencies, modes


def rotated_substrate_stiffness(stiffness_eigenvalues: Any, theta: float) -> np.ndarray:
    eig = _positive_vector("parent_stiffness_eigenvalues", stiffness_eigenvalues, 4)
    q = rotation_matrix(theta)
    return q @ np.diag(eig) @ q.T


def assemble_coupled_system(
    substrate_stiffness: np.ndarray,
    parent_masses: Any,
    child_local_mass: float,
    child_local_stiffness: float,
    coupling_scale: float,
    coupling_weights: Any,
    rayleigh_alpha: float,
    rayleigh_beta: float,
    coordinate_stiffness_shift: float = 0.0,
    intervention_coordinate: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    k_sub = np.asarray(substrate_stiffness, dtype=float)
    if k_sub.shape != (4, 4) or not np.all(np.isfinite(k_sub)) or not np.allclose(k_sub, k_sub.T, atol=1e-12, rtol=0.0):
        raise CouplingResponseRefusal("INVALID_SUBSTRATE", "substrate stiffness must be finite symmetric 4x4")
    parent_mass_diag = _positive_vector("parent_masses", parent_masses, 4)
    m_child = float(child_local_mass)
    k_child = float(child_local_stiffness)
    if not np.isfinite(m_child) or m_child <= 0.0 or not np.isfinite(k_child) or k_child <= 0.0:
        raise CouplingResponseRefusal("INVALID_PARAMETER", "child local mass and stiffness must be finite positive values")
    g = _finite_nonnegative("coupling_scale", coupling_scale)
    weights = _nonnegative_vector("coupling_weights", coupling_weights, 4)
    if not np.isclose(float(np.sum(weights)), 1.0, atol=1e-12, rtol=0.0):
        raise CouplingResponseRefusal("INVALID_COUPLING_WEIGHTS", "coupling weights must sum to one")
    alpha = _finite_nonnegative("rayleigh_alpha", rayleigh_alpha)
    beta = _finite_nonnegative("rayleigh_beta", rayleigh_beta)
    shift = float(coordinate_stiffness_shift)
    if not np.isfinite(shift):
        raise CouplingResponseRefusal("INVALID_PARAMETER", "coordinate_stiffness_shift must be finite")
    if intervention_coordinate not in range(4):
        raise CouplingResponseRefusal("INVALID_INTERVENTION_COORDINATE", "intervention coordinate must be in 0..3")

    mass = np.diag(np.concatenate((parent_mass_diag, np.array([m_child]))))
    stiffness = np.zeros((5, 5), dtype=float)
    stiffness[:4, :4] = k_sub
    stiffness[intervention_coordinate, intervention_coordinate] += shift
    spring = g * weights
    stiffness[:4, :4] += np.diag(spring)
    stiffness[4, 4] = k_child + float(np.sum(spring))
    stiffness[:4, 4] = -spring
    stiffness[4, :4] = -spring

    if np.min(np.linalg.eigvalsh(stiffness)) <= 0.0:
        raise CouplingResponseRefusal("NONPOSITIVE_STIFFNESS", "assembled coupled stiffness must remain positive definite")
    damping = alpha * mass + beta * stiffness
    return mass, damping, stiffness


def generalized_modes(mass: np.ndarray, stiffness: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    m = np.asarray(mass, dtype=float)
    k = np.asarray(stiffness, dtype=float)
    if m.shape != k.shape or m.ndim != 2 or m.shape[0] != m.shape[1]:
        raise CouplingResponseRefusal("INVALID_EIGENSYSTEM", "mass and stiffness must be square with equal shape")
    try:
        chol = np.linalg.cholesky(m)
    except np.linalg.LinAlgError as exc:
        raise CouplingResponseRefusal("INVALID_EIGENSYSTEM", "mass must be positive definite") from exc
    linv = np.linalg.inv(chol)
    standard = linv @ k @ linv.T
    values, vectors = np.linalg.eigh(standard)
    if np.any(values <= 0.0):
        raise CouplingResponseRefusal("NONPOSITIVE_MODE", "undamped modal eigenvalues must be positive")
    modes = linv.T @ vectors
    return np.sqrt(values), modes


def projected_carrier_overlap(
    parent_modes: np.ndarray,
    child_modes: np.ndarray,
    parent_mass_diag: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    parent = np.asarray(parent_modes, dtype=float)
    child = np.asarray(child_modes, dtype=float)
    mass_diag = _positive_vector("parent_mass_diag", parent_mass_diag, 4)
    if parent.shape != (4, 4) or child.shape != (5, 5):
        raise CouplingResponseRefusal("INVALID_MODAL_SHAPE", "expected 4x4 parent modes and 5x5 child modes")
    metric = np.diag(mass_diag)
    overlap = np.zeros((4, 5), dtype=float)
    participation = np.zeros(5, dtype=float)
    for j in range(5):
        sub = child[:4, j]
        part = float(sub.T @ metric @ sub)
        participation[j] = max(0.0, min(1.0, part))
        if part <= 1e-14:
            continue
        direction = sub / np.sqrt(part)
        amp = parent.T @ metric @ direction
        overlap[:, j] = np.abs(amp) ** 2
    return overlap, participation


def best_injective_assignment(score: np.ndarray, maximize: bool) -> tuple[list[int], float]:
    matrix = np.asarray(score, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] > matrix.shape[1] or not np.all(np.isfinite(matrix)):
        raise CouplingResponseRefusal("INVALID_ASSIGNMENT_MATRIX", "assignment matrix must be finite with rows <= columns")
    n_parent, n_child = matrix.shape
    best_assignment: tuple[int, ...] | None = None
    best_value = -np.inf if maximize else np.inf
    for assignment in permutations(range(n_child), n_parent):
        total = float(sum(matrix[i, j] for i, j in enumerate(assignment)))
        if (maximize and total > best_value) or ((not maximize) and total < best_value):
            best_value = total
            best_assignment = assignment
    if best_assignment is None:
        raise CouplingResponseRefusal("ASSIGNMENT_FAILED", "no injective assignment was available")
    return list(best_assignment), best_value


def self_energy_curve(
    mass: np.ndarray,
    damping: np.ndarray,
    stiffness: np.ndarray,
    frequencies: np.ndarray,
) -> tuple[np.ndarray, float]:
    curve: list[complex] = []
    max_condition = 0.0
    for omega in frequencies:
        d = dynamic_stiffness(stiffness, mass, float(omega), damping)
        d_ss = d[:4, :4]
        d_sa = d[:4, 4:5]
        d_as = d[4:5, :4]
        condition = float(np.linalg.cond(d_ss))
        max_condition = max(max_condition, condition)
        try:
            sigma = substrate_self_energy(d_ss, d_sa, d_as)[0, 0]
        except np.linalg.LinAlgError as exc:
            raise CouplingResponseRefusal("SINGULAR_SUBSTRATE_RESPONSE", "substrate dynamic stiffness is singular") from exc
        curve.append(complex(sigma))
    return np.asarray(curve, dtype=complex), max_condition


def intervention_derivative(
    substrate_stiffness: np.ndarray,
    model: dict[str, Any],
    coupling_scale: float,
    coupling_weights: np.ndarray,
    coordinate: int,
    delta: float,
    omega: float,
) -> complex:
    if delta <= 0.0 or not np.isfinite(delta):
        raise CouplingResponseRefusal("INVALID_INTERVENTION_DELTA", "intervention delta must be finite positive")

    responses: list[complex] = []
    for shift in (delta, -delta):
        mass, damping, stiffness = assemble_coupled_system(
            substrate_stiffness=substrate_stiffness,
            parent_masses=model["parent_masses"],
            child_local_mass=model["child_local_mass"],
            child_local_stiffness=model["child_local_stiffness"],
            coupling_scale=coupling_scale,
            coupling_weights=coupling_weights,
            rayleigh_alpha=model["rayleigh_damping_alpha"],
            rayleigh_beta=model["rayleigh_damping_beta"],
            coordinate_stiffness_shift=shift,
            intervention_coordinate=coordinate,
        )
        curve, _ = self_energy_curve(mass, damping, stiffness, np.array([omega], dtype=float))
        responses.append(complex(curve[0]))
    return (responses[0] - responses[1]) / (2.0 * delta)


def _pair(value: complex) -> list[float]:
    z = complex(value)
    return [float(np.real(z)), float(np.imag(z))]


def _summary(values: list[float]) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    if arr.size == 0 or not np.all(np.isfinite(arr)):
        raise CouplingResponseRefusal("INVALID_SUMMARY", "summary series must be finite and nonempty")
    return {
        "minimum": float(np.min(arr)),
        "median": float(np.median(arr)),
        "maximum": float(np.max(arr)),
    }


def load_plan(path: str | Path) -> dict[str, Any]:
    plan = json.loads(Path(path).read_text(encoding="utf-8"))
    if plan.get("schema") != PLAN_SCHEMA:
        raise CouplingResponseRefusal("WRONG_PLAN", "unexpected FM1 plan schema")
    if plan.get("status") != "P0_D_EXPLORATORY_FUNCTION_AND_LIMIT_MAPPING":
        raise CouplingResponseRefusal("WRONG_PLAN_STATUS", "FM1 plan is not the expected P0-D plan")
    if plan.get("confirmatory_language_allowed") is not False or plan.get("mfr14_activated") is not False:
        raise CouplingResponseRefusal("P0_SCOPE_VIOLATION", "FM1 plan must remain exploratory")
    model = plan["model"]
    _positive_vector("parent_masses", model["parent_masses"], 4)
    _positive_vector("parent_stiffness_eigenvalues", model["parent_stiffness_eigenvalues"], 4)
    base = _nonnegative_vector("base_coupling_weights", model["base_coupling_weights"], 4)
    rewired = _nonnegative_vector("rewired_coupling_weights", model["rewired_coupling_weights"], 4)
    if not np.isclose(np.sum(base), 1.0, atol=1e-12, rtol=0.0) or not np.isclose(np.sum(rewired), 1.0, atol=1e-12, rtol=0.0):
        raise CouplingResponseRefusal("INVALID_COUPLING_WEIGHTS", "both coupling weight vectors must sum to one")
    if not np.isclose(np.sum(base), np.sum(rewired), atol=1e-12, rtol=0.0):
        raise CouplingResponseRefusal("COUPLING_SCALE_MISMATCH", "base and rewired weights must preserve total coupling scale")
    for value in model["coupling_scale_values"]:
        _finite_nonnegative("coupling_scale_values", value)
    for value in model["carrier_geometry_angle_values_radians"]:
        if not np.isfinite(float(value)):
            raise CouplingResponseRefusal("INVALID_PARAMETER", "geometry angles must be finite")
    probes = np.asarray(plan["probe_frequencies"], dtype=float)
    if probes.ndim != 1 or probes.size == 0 or not np.all(np.isfinite(probes)) or np.any(probes < 0.0):
        raise CouplingResponseRefusal("INVALID_PROBE_FREQUENCIES", "probe frequencies must be finite nonnegative")
    intervention = plan["intervention"]
    if intervention["shared_coordinate_index"] not in range(4):
        raise CouplingResponseRefusal("INVALID_INTERVENTION_COORDINATE", "intervention coordinate must be in 0..3")
    if float(intervention["delta"]) <= 0.0:
        raise CouplingResponseRefusal("INVALID_INTERVENTION_DELTA", "intervention delta must be positive")
    return plan


def run_fm1(plan_path: str | Path) -> dict[str, Any]:
    plan = load_plan(plan_path)
    model = plan["model"]
    probes = np.asarray(plan["probe_frequencies"], dtype=float)
    intervention = plan["intervention"]
    parent_mass, parent_stiffness, parent_frequencies, parent_modes = clean_parent_system(
        model["parent_stiffness_eigenvalues"],
        model["parent_masses"],
    )
    parent_mass_diag = np.diag(parent_mass)
    base_weights = np.asarray(model["base_coupling_weights"], dtype=float)
    rewired_weights = np.asarray(model["rewired_coupling_weights"], dtype=float)

    records: list[dict[str, Any]] = []
    same_spectrum_max_error = 0.0

    for theta in model["carrier_geometry_angle_values_radians"]:
        substrate = rotated_substrate_stiffness(model["parent_stiffness_eigenvalues"], theta)
        rotated_eigs = np.linalg.eigvalsh(substrate)
        same_spectrum_error = float(np.max(np.abs(rotated_eigs - np.asarray(model["parent_stiffness_eigenvalues"], dtype=float))))
        same_spectrum_max_error = max(same_spectrum_max_error, same_spectrum_error)

        for coupling_scale in model["coupling_scale_values"]:
            mass, damping, stiffness = assemble_coupled_system(
                substrate_stiffness=substrate,
                parent_masses=model["parent_masses"],
                child_local_mass=model["child_local_mass"],
                child_local_stiffness=model["child_local_stiffness"],
                coupling_scale=coupling_scale,
                coupling_weights=base_weights,
                rayleigh_alpha=model["rayleigh_damping_alpha"],
                rayleigh_beta=model["rayleigh_damping_beta"],
            )
            child_frequencies, child_modes = generalized_modes(mass, stiffness)
            overlap, participation = projected_carrier_overlap(parent_modes, child_modes, parent_mass_diag)

            carrier_assignment, carrier_total = best_injective_assignment(overlap, maximize=True)
            carrier_mean_overlap = float(carrier_total / 4.0)
            carrier_assigned_participation = [float(participation[j]) for j in carrier_assignment]

            frequency_cost = np.abs(parent_frequencies[:, None] - child_frequencies[None, :])
            frequency_assignment, frequency_total_error = best_injective_assignment(frequency_cost, maximize=False)
            frequency_carrier_overlaps = [float(overlap[i, j]) for i, j in enumerate(frequency_assignment)]
            frequency_mean_carrier_overlap = float(np.mean(frequency_carrier_overlaps))
            frequency_assigned_participation = [float(participation[j]) for j in frequency_assignment]

            curve, max_condition = self_energy_curve(mass, damping, stiffness, probes)
            curve_norm = float(np.linalg.norm(curve))

            rewire_mass, rewire_damping, rewire_stiffness = assemble_coupled_system(
                substrate_stiffness=substrate,
                parent_masses=model["parent_masses"],
                child_local_mass=model["child_local_mass"],
                child_local_stiffness=model["child_local_stiffness"],
                coupling_scale=coupling_scale,
                coupling_weights=rewired_weights,
                rayleigh_alpha=model["rayleigh_damping_alpha"],
                rayleigh_beta=model["rayleigh_damping_beta"],
            )
            rewire_curve, rewire_condition = self_energy_curve(rewire_mass, rewire_damping, rewire_stiffness, probes)
            rewire_difference = float(np.linalg.norm(curve - rewire_curve))
            rewire_relative_change = 0.0 if curve_norm <= 1e-14 else float(rewire_difference / curve_norm)

            derivative = intervention_derivative(
                substrate_stiffness=substrate,
                model=model,
                coupling_scale=float(coupling_scale),
                coupling_weights=base_weights,
                coordinate=int(intervention["shared_coordinate_index"]),
                delta=float(intervention["delta"]),
                omega=float(intervention["probe_frequency"]),
            )

            records.append(
                {
                    "carrier_geometry_angle_radians": float(theta),
                    "coupling_scale": float(coupling_scale),
                    "same_spectrum_substrate_eigenvalue_max_error_before_coupling": same_spectrum_error,
                    "parent_frequencies": parent_frequencies.tolist(),
                    "child_frequencies": child_frequencies.tolist(),
                    "overlap_matrix": overlap.tolist(),
                    "child_substrate_participation": participation.tolist(),
                    "carrier_assignment": carrier_assignment,
                    "carrier_assignment_mean_overlap": carrier_mean_overlap,
                    "carrier_assignment_mean_substrate_participation": float(np.mean(carrier_assigned_participation)),
                    "frequency_only_assignment": frequency_assignment,
                    "frequency_only_total_absolute_frequency_error": float(frequency_total_error),
                    "frequency_only_assignment_mean_carrier_overlap": frequency_mean_carrier_overlap,
                    "frequency_only_assignment_mean_substrate_participation": float(np.mean(frequency_assigned_participation)),
                    "carrier_overlap_advantage_over_frequency_assignment": float(carrier_mean_overlap - frequency_mean_carrier_overlap),
                    "embedded_response_curve": [_pair(z) for z in curve],
                    "embedded_response_curve_norm": curve_norm,
                    "rewired_response_curve": [_pair(z) for z in rewire_curve],
                    "coupling_rewire_relative_curve_change": rewire_relative_change,
                    "intervention_derivative": _pair(derivative),
                    "intervention_derivative_magnitude": float(abs(derivative)),
                    "maximum_substrate_dynamic_stiffness_condition_number": max(max_condition, rewire_condition),
                }
            )

    def group_summary(field: str, key: str, value: float) -> dict[str, float]:
        vals = [float(r[field]) for r in records if np.isclose(float(r[key]), float(value), atol=1e-14, rtol=0.0)]
        return _summary(vals)

    by_coupling: list[dict[str, Any]] = []
    for coupling_scale in model["coupling_scale_values"]:
        by_coupling.append(
            {
                "coupling_scale": float(coupling_scale),
                "carrier_assignment_mean_overlap": group_summary("carrier_assignment_mean_overlap", "coupling_scale", coupling_scale),
                "carrier_assignment_mean_substrate_participation": group_summary("carrier_assignment_mean_substrate_participation", "coupling_scale", coupling_scale),
                "embedded_response_curve_norm": group_summary("embedded_response_curve_norm", "coupling_scale", coupling_scale),
                "coupling_rewire_relative_curve_change": group_summary("coupling_rewire_relative_curve_change", "coupling_scale", coupling_scale),
                "intervention_derivative_magnitude": group_summary("intervention_derivative_magnitude", "coupling_scale", coupling_scale),
            }
        )

    by_angle: list[dict[str, Any]] = []
    for theta in model["carrier_geometry_angle_values_radians"]:
        by_angle.append(
            {
                "carrier_geometry_angle_radians": float(theta),
                "carrier_assignment_mean_overlap": group_summary("carrier_assignment_mean_overlap", "carrier_geometry_angle_radians", theta),
                "frequency_only_total_absolute_frequency_error": group_summary("frequency_only_total_absolute_frequency_error", "carrier_geometry_angle_radians", theta),
                "frequency_only_assignment_mean_carrier_overlap": group_summary("frequency_only_assignment_mean_carrier_overlap", "carrier_geometry_angle_radians", theta),
                "carrier_overlap_advantage_over_frequency_assignment": group_summary("carrier_overlap_advantage_over_frequency_assignment", "carrier_geometry_angle_radians", theta),
            }
        )

    zero_cases = [r for r in records if r["coupling_scale"] == 0.0]
    origin = next(r for r in zero_cases if r["carrier_geometry_angle_radians"] == 0.0)

    return {
        "schema": RESULT_SCHEMA,
        "scope": "synthetic_si_fm1_coupling_response_landscape_p0d_only",
        "status": "P0_D_DESCRIPTIVE_OR_STRUCTURAL_FUNCTION_LIMIT_LANDSCAPE",
        "experiment_plan": str(Path(plan_path).name),
        "general_protocol": "v0.7.4",
        "mfr14_activated": False,
        "physical_thresholds_frozen": False,
        "real_system_evidence": False,
        "physical_inheritance_claim": False,
        "system_scalar_chi_constructed": False,
        "master_relationship_score_constructed": False,
        "atlas_used_for_parameter_selection": False,
        "case_count": len(records),
        "same_spectrum_control": {
            "maximum_clean_substrate_eigenvalue_error_across_geometry_angles": same_spectrum_max_error,
        },
        "zero_coupling_controls": {
            "case_count": len(zero_cases),
            "maximum_embedded_response_curve_norm": max(float(r["embedded_response_curve_norm"]) for r in zero_cases),
            "maximum_coupling_rewire_relative_curve_change": max(float(r["coupling_rewire_relative_curve_change"]) for r in zero_cases),
            "maximum_intervention_derivative_magnitude": max(float(r["intervention_derivative_magnitude"]) for r in zero_cases),
        },
        "origin_control": {
            "carrier_assignment_mean_overlap": float(origin["carrier_assignment_mean_overlap"]),
            "carrier_assignment_mean_substrate_participation": float(origin["carrier_assignment_mean_substrate_participation"]),
            "frequency_only_total_absolute_frequency_error": float(origin["frequency_only_total_absolute_frequency_error"]),
            "frequency_only_assignment_mean_carrier_overlap": float(origin["frequency_only_assignment_mean_carrier_overlap"]),
        },
        "global_summaries": {
            "carrier_assignment_mean_overlap": _summary([float(r["carrier_assignment_mean_overlap"]) for r in records]),
            "carrier_assignment_mean_substrate_participation": _summary([float(r["carrier_assignment_mean_substrate_participation"]) for r in records]),
            "frequency_only_total_absolute_frequency_error": _summary([float(r["frequency_only_total_absolute_frequency_error"]) for r in records]),
            "frequency_only_assignment_mean_carrier_overlap": _summary([float(r["frequency_only_assignment_mean_carrier_overlap"]) for r in records]),
            "carrier_overlap_advantage_over_frequency_assignment": _summary([float(r["carrier_overlap_advantage_over_frequency_assignment"]) for r in records]),
            "embedded_response_curve_norm": _summary([float(r["embedded_response_curve_norm"]) for r in records]),
            "coupling_rewire_relative_curve_change": _summary([float(r["coupling_rewire_relative_curve_change"]) for r in records]),
            "intervention_derivative_magnitude": _summary([float(r["intervention_derivative_magnitude"]) for r in records]),
            "maximum_substrate_dynamic_stiffness_condition_number": max(float(r["maximum_substrate_dynamic_stiffness_condition_number"]) for r in records),
        },
        "summary_by_coupling": by_coupling,
        "summary_by_geometry_angle": by_angle,
        "reporting_firewall": {
            "binary_physical_pass_threshold_applied": False,
            "post_result_favorable_region_promoted": False,
            "function_map_claimed_as_mechanistic_confirmation": False,
            "frequency_only_comparator_claimed_as_strongest_future_p1_toolkit": False,
        },
        "records": records,
    }


def write_fm1_result(
    plan_path: str | Path = "substrate_inheritance/SI_FM1_COUPLING_RESPONSE_PLAN_v0.1.json",
    output_path: str | Path = "substrate_inheritance/results/SI_FM1_COUPLING_RESPONSE_RESULTS_v0.1.json",
) -> dict[str, Any]:
    result = run_fm1(plan_path)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = write_fm1_result()
    summary = {k: v for k, v in result.items() if k != "records"}
    print(json.dumps(summary, indent=2, sort_keys=True))
