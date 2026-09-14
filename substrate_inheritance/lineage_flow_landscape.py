from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from substrate_inheritance.si_next_architecture import dominant_lineage_transition
from substrate_inheritance.si_next_higher_order import (
    interval_dominant_lineage,
    lineage_dispersion,
    propagate_relative_lineage,
)


PLAN_PATH = Path("substrate_inheritance/SI_FM3_LINEAGE_FLOW_PLAN_v0.1.json")
RESULT_PATH = Path("substrate_inheritance/results/fm3_lineage_flow_landscape.json")


def _rotation(i: int, j: int, theta: float, dimension: int = 3) -> np.ndarray:
    q = np.eye(dimension, dtype=float)
    c = math.cos(theta)
    s = math.sin(theta)
    q[i, i] = c
    q[j, j] = c
    q[i, j] = -s
    q[j, i] = s
    return q


def exact_generation_bases(theta: float) -> tuple[np.ndarray, ...]:
    q0 = np.eye(3, dtype=float)
    q1 = _rotation(0, 2, theta)
    q2 = _rotation(1, 2, theta) @ q1
    q3 = np.eye(3, dtype=float)
    return q0, q1, q2, q3


def operator_from_basis(basis: np.ndarray, spectral_gap: float) -> np.ndarray:
    if not math.isfinite(spectral_gap) or spectral_gap <= 0.0:
        raise ValueError("spectral_gap must be finite and positive")
    eigenvalues = np.array([1.0, 1.0 + spectral_gap, 3.0], dtype=float)
    return basis @ np.diag(eigenvalues) @ basis.T


def carrier_overlap(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    if left.shape != right.shape or left.ndim != 2:
        raise ValueError("carrier bases must be same-shape matrices")
    return np.abs(left.T @ right) ** 2


def _ordered_eigensystem(operator: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh(np.asarray(operator, dtype=float))
    order = np.argsort(values)
    return values[order], vectors[:, order]


def _symmetric_unit_frobenius(rng: np.random.Generator, dimension: int) -> np.ndarray:
    raw = rng.normal(size=(dimension, dimension))
    symmetric = 0.5 * (raw + raw.T)
    norm = float(np.linalg.norm(symmetric, ord="fro"))
    if norm == 0.0:
        raise RuntimeError("unexpected zero perturbation draw")
    return symmetric / norm


def perturbed_eigensystem(
    operator: np.ndarray,
    relative_frobenius: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    if not math.isfinite(relative_frobenius) or relative_frobenius < 0.0:
        raise ValueError("relative_frobenius must be finite and nonnegative")
    op = np.asarray(operator, dtype=float)
    if relative_frobenius == 0.0:
        return _ordered_eigensystem(op)
    direction = _symmetric_unit_frobenius(rng, op.shape[0])
    magnitude = relative_frobenius * float(np.linalg.norm(op, ord="fro"))
    return _ordered_eigensystem(op + magnitude * direction)


def _minimum_subspace_cosine(left: np.ndarray, right: np.ndarray, count: int = 2) -> float:
    singular = np.linalg.svd(left[:, :count].T @ right[:, :count], compute_uv=False)
    return float(np.min(singular))


def _matrix_list(matrix: np.ndarray) -> list[list[float]]:
    return [[float(v) for v in row] for row in np.asarray(matrix, dtype=float)]


def _lineage_dispersion_records(matrix: np.ndarray) -> list[dict[str, Any]]:
    return [
        {
            "parent_index": item.parent_index,
            "total_weight": item.total_weight,
            "dominant_child_index": item.dominant_child_index,
            "dominant_fraction": item.dominant_fraction,
            "effective_child_count": item.effective_child_count,
            "shannon_entropy": item.shannon_entropy,
            "normalized_entropy": item.normalized_entropy,
        }
        for item in lineage_dispersion(matrix)
    ]


def _dominant_records(matrix: np.ndarray) -> list[dict[str, Any]]:
    return [
        {
            "parent_index": step.parent_index,
            "child_index": step.child_index,
            "dominant_score": step.dominant_score,
            "runner_up_score": step.runner_up_score,
            "margin": step.margin,
            "unique_dominant": step.unique_dominant,
            "identifiable": step.identifiable,
        }
        for step in dominant_lineage_transition(matrix)
    ]


def _interval_records(lower: np.ndarray, upper: np.ndarray) -> list[dict[str, Any]]:
    return [
        {
            "parent_index": step.parent_index,
            "child_index": step.child_index,
            "winner_lower_bound": step.winner_lower_bound,
            "strongest_competitor_upper_bound": step.strongest_competitor_upper_bound,
            "robust_gap": step.robust_gap,
            "identifiable": step.identifiable,
        }
        for step in interval_dominant_lineage(lower, upper)
    ]


def exact_case(theta: float, spectral_gap: float) -> dict[str, Any]:
    bases = exact_generation_bases(theta)
    operators = [operator_from_basis(q, spectral_gap) for q in bases]
    eigensystems = [_ordered_eigensystem(op) for op in operators]
    vectors = [item[1] for item in eigensystems]
    values = [item[0] for item in eigensystems]
    transitions = [carrier_overlap(vectors[i], vectors[i + 1]) for i in range(3)]
    direct = carrier_overlap(vectors[0], vectors[3])

    flow = propagate_relative_lineage(transitions, start_parent=0)
    final_flow = np.asarray(flow["steps"][-1].descendant_weights, dtype=float)
    direct_row = direct[0]
    flow_direct_l1 = float(np.sum(np.abs(final_flow - direct_row)))

    return {
        "transition_correspondence": [_matrix_list(x) for x in transitions],
        "direct_generation0_to_generation3_correspondence": _matrix_list(direct),
        "transition_dispersion": [_lineage_dispersion_records(x) for x in transitions],
        "transition_dominant_lineage": [_dominant_records(x) for x in transitions],
        "subspace_minimum_cosines": [
            _minimum_subspace_cosine(vectors[i], vectors[i + 1], count=2) for i in range(3)
        ],
        "minimum_eigenvalue_gaps": [float(np.min(np.diff(x))) for x in values],
        "relative_flow_final_descendant_weights_parent0": [float(x) for x in final_flow],
        "direct_final_correspondence_parent0": [float(x) for x in direct_row],
        "flow_vs_direct_reconvergence_l1": flow_direct_l1,
        "direct_reconvergence_error_from_identity_fro": float(np.linalg.norm(direct - np.eye(3), ord="fro")),
        "relative_flow_semantics": flow["normalization_role"],
        "relative_flow_threshold_applied": flow["threshold_applied"],
    }


def perturbation_ensemble_case(
    theta: float,
    spectral_gap: float,
    relative_frobenius: float,
    seeds: list[int],
) -> dict[str, Any]:
    bases = exact_generation_bases(theta)
    operators = [operator_from_basis(q, spectral_gap) for q in bases]

    transition_samples: list[list[np.ndarray]] = [[], [], []]
    direct_samples: list[np.ndarray] = []
    subspace_samples: list[list[float]] = [[], [], []]
    gap_samples: list[list[float]] = [[], [], [], []]
    flow_l1_samples: list[float] = []
    seed_records: list[dict[str, Any]] = []

    for seed in seeds:
        rng = np.random.default_rng(seed)
        eigensystems = [perturbed_eigensystem(op, relative_frobenius, rng) for op in operators]
        values = [item[0] for item in eigensystems]
        vectors = [item[1] for item in eigensystems]
        transitions = [carrier_overlap(vectors[i], vectors[i + 1]) for i in range(3)]
        direct = carrier_overlap(vectors[0], vectors[3])
        flow = propagate_relative_lineage(transitions, start_parent=0)
        final_flow = np.asarray(flow["steps"][-1].descendant_weights, dtype=float)
        direct_row = direct[0]
        l1 = float(np.sum(np.abs(final_flow - direct_row)))

        for index, matrix in enumerate(transitions):
            transition_samples[index].append(matrix)
            subspace_samples[index].append(_minimum_subspace_cosine(vectors[index], vectors[index + 1], count=2))
        direct_samples.append(direct)
        for index, vals in enumerate(values):
            gap_samples[index].append(float(np.min(np.diff(vals))))
        flow_l1_samples.append(l1)

        seed_records.append(
            {
                "seed": seed,
                "transition_correspondence": [_matrix_list(x) for x in transitions],
                "direct_generation0_to_generation3_correspondence": _matrix_list(direct),
                "subspace_minimum_cosines": [
                    _minimum_subspace_cosine(vectors[i], vectors[i + 1], count=2) for i in range(3)
                ],
                "minimum_eigenvalue_gaps": [float(np.min(np.diff(x))) for x in values],
                "relative_flow_final_descendant_weights_parent0": [float(x) for x in final_flow],
                "direct_final_correspondence_parent0": [float(x) for x in direct_row],
                "flow_vs_direct_reconvergence_l1": l1,
            }
        )

    transition_bounds = []
    interval_identifiability = []
    for samples in transition_samples:
        stack = np.stack(samples, axis=0)
        lower = np.min(stack, axis=0)
        upper = np.max(stack, axis=0)
        transition_bounds.append({"minimum": _matrix_list(lower), "maximum": _matrix_list(upper)})
        interval_identifiability.append(_interval_records(lower, upper))

    direct_stack = np.stack(direct_samples, axis=0)
    direct_lower = np.min(direct_stack, axis=0)
    direct_upper = np.max(direct_stack, axis=0)

    return {
        "relative_frobenius": relative_frobenius,
        "seed_count": len(seeds),
        "seeds": list(seeds),
        "transition_correspondence_envelopes": transition_bounds,
        "transition_interval_identifiability": interval_identifiability,
        "direct_correspondence_envelope": {
            "minimum": _matrix_list(direct_lower),
            "maximum": _matrix_list(direct_upper),
        },
        "direct_interval_identifiability": _interval_records(direct_lower, direct_upper),
        "minimum_subspace_cosine_by_transition": [float(np.min(x)) for x in subspace_samples],
        "median_subspace_cosine_by_transition": [float(np.median(x)) for x in subspace_samples],
        "minimum_sampled_eigenvalue_gap_by_generation": [float(np.min(x)) for x in gap_samples],
        "median_sampled_eigenvalue_gap_by_generation": [float(np.median(x)) for x in gap_samples],
        "flow_vs_direct_reconvergence_l1_minimum": float(np.min(flow_l1_samples)),
        "flow_vs_direct_reconvergence_l1_median": float(np.median(flow_l1_samples)),
        "flow_vs_direct_reconvergence_l1_maximum": float(np.max(flow_l1_samples)),
        "seed_records": seed_records,
        "envelope_semantics": "seedwise_minimum_maximum_descriptive_perturbation_envelope_not_confidence_interval",
    }


def run_fm3(plan: dict[str, Any]) -> dict[str, Any]:
    if plan.get("schema") != "substrate-inheritance-fm3-lineage-flow-plan-v0.1":
        raise ValueError("FM3 requires the frozen v0.1 plan")
    if plan.get("status") != "P0_D_EXPLORATORY_FUNCTION_MAPPING":
        raise ValueError("FM3 plan must remain P0-D exploratory")
    if plan.get("physical_inheritance_claim") is not False:
        raise ValueError("FM3 cannot carry a physical inheritance claim")
    firewall = plan["anti_circularity"]
    required_false = [
        "relative_flow_is_probability",
        "relative_flow_is_causal_fraction",
        "relative_flow_is_inheritance_percentage",
        "relative_flow_is_promotion_score",
        "post_result_threshold_fitting",
    ]
    if any(firewall[name] is not False for name in required_false):
        raise ValueError("FM3 relative-flow/promotion firewalls changed")
    if not all(
        firewall[name] is True
        for name in [
            "no_master_score",
            "no_physical_threshold",
            "no_atlas_target_used",
            "no_chi_used_for_mapping",
            "same_spectrum_control_retained",
            "all_grid_cases_retained",
            "all_frozen_seeds_retained",
        ]
    ):
        raise ValueError("FM3 anti-circularity firewall is incomplete")

    grid = plan["parameter_grid"]
    thetas = [float(v) for v in grid["transformation_strength_theta_radians"]]
    gaps = [float(v) for v in grid["spectral_gap"]]
    perturbations = [float(v) for v in grid["perturbation_relative_frobenius"]]
    seeds = [int(v) for v in grid["perturbation_seeds"]]
    expected_cases = int(grid["case_count_without_seed_expansion"])
    if len(thetas) * len(gaps) * len(perturbations) != expected_cases:
        raise ValueError("FM3 grid count does not match frozen plan")
    if len(seeds) != len(set(seeds)) or len(seeds) == 0:
        raise ValueError("FM3 seeds must be non-empty and unique")

    records: list[dict[str, Any]] = []
    exact_cache: dict[tuple[float, float], dict[str, Any]] = {}
    for theta in thetas:
        for gap in gaps:
            exact_cache[(theta, gap)] = exact_case(theta, gap)
            for epsilon in perturbations:
                records.append(
                    {
                        "theta": theta,
                        "spectral_gap": gap,
                        "perturbation_relative_frobenius": epsilon,
                        "exact_unperturbed": exact_cache[(theta, gap)],
                        "perturbation_ensemble": perturbation_ensemble_case(theta, gap, epsilon, seeds),
                    }
                )

    exact_l1 = [x["flow_vs_direct_reconvergence_l1"] for x in exact_cache.values()]
    ensemble_l1 = [x["perturbation_ensemble"]["flow_vs_direct_reconvergence_l1_median"] for x in records]
    direct_identifiable_fraction = float(
        np.mean(
            [
                x["perturbation_ensemble"]["direct_interval_identifiability"][0]["identifiable"]
                for x in records
            ]
        )
    )
    all_transition_identifiable = []
    for record in records:
        statuses = record["perturbation_ensemble"]["transition_interval_identifiability"]
        all_transition_identifiable.append(all(step["identifiable"] for transition in statuses for step in transition))

    summary = {
        "case_count": len(records),
        "seed_count_per_case": len(seeds),
        "seed_expanded_evaluations": len(records) * len(seeds),
        "maximum_exact_direct_reconvergence_error_from_identity_fro": float(
            max(x["direct_reconvergence_error_from_identity_fro"] for x in exact_cache.values())
        ),
        "exact_sequential_flow_vs_direct_l1_minimum": float(np.min(exact_l1)),
        "exact_sequential_flow_vs_direct_l1_median": float(np.median(exact_l1)),
        "exact_sequential_flow_vs_direct_l1_maximum": float(np.max(exact_l1)),
        "perturbed_median_flow_vs_direct_l1_minimum": float(np.min(ensemble_l1)),
        "perturbed_median_flow_vs_direct_l1_median": float(np.median(ensemble_l1)),
        "perturbed_median_flow_vs_direct_l1_maximum": float(np.max(ensemble_l1)),
        "direct_parent0_interval_identifiable_fraction": direct_identifiable_fraction,
        "all_transition_rows_interval_identifiable_fraction": float(np.mean(all_transition_identifiable)),
        "extinction_constructed": False,
        "extinction_status": "NOT_PRESENT_IN_FULL_RANK_SAME_SPECTRUM_CONSTRUCTION",
    }

    return {
        "scope": "synthetic_fm3_lineage_function_limit_map_only",
        "status": "P0_D_DESCRIPTIVE_STRUCTURAL",
        "physical_inheritance_claim": False,
        "physical_thresholds_frozen": False,
        "atlas_target_used": False,
        "master_score_computed": False,
        "relative_flow_is_probability": False,
        "relative_flow_is_causal_fraction": False,
        "relative_flow_is_inheritance_percentage": False,
        "relative_flow_is_promotion_score": False,
        "plan": "substrate_inheritance/SI_FM3_LINEAGE_FLOW_PLAN_v0.1.json",
        "summary": summary,
        "records": records,
    }


def write_fm3(plan_path: Path = PLAN_PATH, result_path: Path = RESULT_PATH) -> dict[str, Any]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    result = run_fm3(plan)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = write_fm3()
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
