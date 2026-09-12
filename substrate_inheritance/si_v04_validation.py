from __future__ import annotations

import json
from pathlib import Path

from substrate_inheritance.si_v04_semantics import (
    ArchitectureViews,
    SIV04Refusal,
    relationship_pattern_v04,
    validate_cross_scale_scope,
    validate_hierarchical_closure,
    validate_local_embedded_firewall,
    validate_recovery_resilience,
    validate_uncertainty_alignment,
)


def _h(char: str) -> str:
    return char * 64


def _refusal_code(fn, record) -> str:
    try:
        fn(record)
    except SIV04Refusal as exc:
        return exc.code
    raise AssertionError("known-bad record unexpectedly passed SI v0.4 guard")


def synthetic_si_v04_validation() -> dict:
    views = ArchitectureViews("NOT_APPLICABLE", "SUPPORTED", "SUPPORTED")
    uncertainty = validate_uncertainty_alignment(
        views,
        {"scalar": "NOT_APPLICABLE", "modal": "BOUNDED", "conglomeration": "UNRESOLVED"},
    )

    relational = {
        "local_identity_separate_from_embedded_behavior": True,
        "atlas_used_to_define_or_tune_coordinate": False,
        "atlas_used_to_define_or_tune_mapping": False,
        "lower_level_scalars_averaged_into_system_scalar": False,
        "system_scalar_reported": False,
        "system_scalar_separately_derived_if_reported": False,
        "objects": {
            "local_or_intrinsic_subsystem_model": "PROVIDED",
            "outward_coupling_or_signal": "PROVIDED",
            "environment_or_connected_system_transformation": "UNRESOLVED",
            "feedback_or_return": "NOT_APPLICABLE",
            "embedded_or_closed_loop_model": "PROVIDED",
            "survival_transformation_emergence_record": "PROVIDED",
        },
    }
    validate_local_embedded_firewall(relational)

    hierarchy = {
        "enabled": True,
        "higher_level_question": "Does a reduced coupled subsystem preserve the declared input-output and return behavior?",
        "validity_regime": "synthetic linear qualification regime only",
        "preservation_targets": ["input-output response", "feedback return"],
        "reference_artifact_sha256": _h("a"),
        "reduced_artifact_sha256": _h("b"),
        "uncertainty_or_tolerance": "synthetic numerical qualification tolerance",
        "closure_status": "HIERARCHICAL_REDUCTION_SUPPORTED_IN_REGIME",
    }
    validate_hierarchical_closure(hierarchy)

    recovery = {
        "enabled": True,
        "state_classification_separate": True,
        "asymptotic_return_separate_from_finite_time_resilience": True,
        "native_measure_family": "synthetic state-transition response family",
        "source_artifact_sha256": _h("c"),
    }
    validate_recovery_resilience(recovery)

    cross_scale = {
        "claim_level": "PRESERVED_ARCHITECTURE_ACROSS_SCALE",
        "universal_claim": False,
        "preserved_quantity": "declared input-output response",
        "transformed_quantity": "internal carrier basis",
        "validity_regime": "synthetic qualification regime",
        "loss_condition": "declared preservation target exceeds its qualification tolerance",
    }
    validate_cross_scale_scope(cross_scale)

    bad_scalar = dict(relational)
    bad_scalar["lower_level_scalars_averaged_into_system_scalar"] = True

    bad_atlas = dict(relational)
    bad_atlas["atlas_used_to_define_or_tune_coordinate"] = True

    bad_system_scalar = dict(relational)
    bad_system_scalar["system_scalar_reported"] = True
    bad_system_scalar["system_scalar_separately_derived_if_reported"] = False

    bad_hierarchy = {
        "enabled": False,
        "closure_status": "HIERARCHICAL_REDUCTION_SUPPORTED_IN_REGIME",
    }

    bad_recovery = dict(recovery)
    bad_recovery["asymptotic_return_separate_from_finite_time_resilience"] = False

    bad_cross_scale = dict(cross_scale)
    bad_cross_scale["universal_claim"] = True

    return {
        "scope": "synthetic_si_v04_gp074_semantic_validation_only",
        "status": "candidate_v0.4_non_authoritative_p0q",
        "general_protocol": "v0.7.4",
        "frozen_v0.2_changed": False,
        "physical_thresholds_frozen": False,
        "real_system_evidence": False,
        "physical_inheritance_claim": False,
        "relationship_pattern": relationship_pattern_v04(views),
        "uncertainty": uncertainty,
        "hierarchical_closure_status": hierarchy["closure_status"],
        "recovery_semantics_separated": True,
        "cross_scale_claim_level": cross_scale["claim_level"],
        "known_bad_refusals": {
            "lower_level_scalar_averaging": _refusal_code(validate_local_embedded_firewall, bad_scalar),
            "atlas_coordinate_leakage": _refusal_code(validate_local_embedded_firewall, bad_atlas),
            "unlicensed_system_scalar": _refusal_code(validate_local_embedded_firewall, bad_system_scalar),
            "disabled_hierarchy_with_decision": _refusal_code(validate_hierarchical_closure, bad_hierarchy),
            "asymptotic_transient_conflation": _refusal_code(validate_recovery_resilience, bad_recovery),
            "universality_from_recurrence": _refusal_code(validate_cross_scale_scope, bad_cross_scale),
        },
    }


def write_validation(path: str | Path) -> dict:
    result = synthetic_si_v04_validation()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = write_validation("substrate_inheritance/results/si_v04_validation.json")
    print(json.dumps(result, indent=2, sort_keys=True))
