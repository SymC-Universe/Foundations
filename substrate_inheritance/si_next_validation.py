from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from substrate_inheritance.si_next_architecture import (
    CrossViewState,
    ViewUncertainty,
    dominant_lineage_transition,
    perturbation_envelope,
    propagate_uncertainty,
    relationship_pattern,
    source_ablation_effects,
    source_inclusion_exclusion,
    trace_dominant_lineage,
)


def synthetic_si_next_validation() -> dict:
    relationship_cases = {
        "all_supported": relationship_pattern(CrossViewState("SUPPORTED", "SUPPORTED", "SUPPORTED")),
        "scalar_only": relationship_pattern(CrossViewState("SUPPORTED", "DISRUPTED", "DISRUPTED")),
        "scalar_modal_only": relationship_pattern(CrossViewState("SUPPORTED", "SUPPORTED", "DISRUPTED")),
        "modal_nonidentifiable": relationship_pattern(CrossViewState("SUPPORTED", "NONIDENTIFIABLE", "SUPPORTED")),
    }

    uncertainty = propagate_uncertainty(
        ViewUncertainty(modal=("near_degenerate_subspace",), conglomeration=("mapping_uncertain",))
    )
    envelope = perturbation_envelope(np.array([0.91, 0.92, 0.90, 0.915, 0.905]))

    transition_1 = np.array([[0.96, 0.04], [0.05, 0.95]])
    transition_2 = np.array([[0.93, 0.07], [0.08, 0.92]])
    lineage = trace_dominant_lineage((transition_1, transition_2), start_parent=0)
    exact_tie = dominant_lineage_transition(np.array([[0.5, 0.5]]))[0]

    weights = {"substrate_A": 2.0, "substrate_B": -0.5}

    def additive_response(active: frozenset[str]) -> np.ndarray:
        return np.array([1.0 + sum(weights[name] for name in active)])

    additive = source_inclusion_exclusion(additive_response, tuple(weights))

    def interacting_response(active: frozenset[str]) -> np.ndarray:
        a = 1.0 if "substrate_A" in active else 0.0
        b = 1.0 if "substrate_B" in active else 0.0
        return np.array([0.25 + 2.0 * a - 0.5 * b + 1.25 * a * b])

    interacting = source_inclusion_exclusion(interacting_response, tuple(weights))
    ablation = source_ablation_effects(interacting_response, tuple(weights))

    return {
        "scope": "synthetic_si_next_architecture_validation_only",
        "status": "candidate_v0.3_non_authoritative",
        "frozen_v0.2_changed": False,
        "physical_thresholds_frozen": False,
        "real_system_evidence": False,
        "inheritance_promotion_rule_changed": False,
        "relationship_cases": relationship_cases,
        "uncertainty": {
            "joint_identifiable": uncertainty["joint_identifiable"],
            "joint_blockers": list(uncertainty["joint_blockers"]),
        },
        "perturbation_envelope": envelope,
        "lineage": {
            "path": [
                {
                    "parent_index": step.parent_index,
                    "child_index": step.child_index,
                    "dominant_score": step.dominant_score,
                    "runner_up_score": step.runner_up_score,
                    "margin": step.margin,
                    "identifiable": step.identifiable,
                }
                for step in lineage
            ],
            "exact_tie_refused": not exact_tie.identifiable and exact_tie.child_index is None,
        },
        "multi_parent": {
            "additive_pair_interaction_norm": float(np.linalg.norm(next(iter(additive.pair_interactions.values())))),
            "additive_higher_order_residual_norm": float(np.linalg.norm(additive.higher_order_residual)),
            "interacting_pair_interaction_norm": float(np.linalg.norm(next(iter(interacting.pair_interactions.values())))),
            "interacting_higher_order_residual_norm": float(np.linalg.norm(interacting.higher_order_residual)),
            "ablation_effect_norms": {name: float(np.linalg.norm(effect)) for name, effect in ablation.items()},
            "effects_forced_to_sum_to_one": False,
        },
    }


def write_validation(path: str | Path) -> dict:
    result = synthetic_si_next_validation()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = write_validation("substrate_inheritance/results/si_next_validation.json")
    print(json.dumps(result, indent=2, sort_keys=True))
