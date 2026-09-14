from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping


VIEW_STATES = frozenset({"SUPPORTED", "DISRUPTED", "NONIDENTIFIABLE", "NOT_MEASURED", "NOT_APPLICABLE"})
UNCERTAINTY_STATES = frozenset({"BOUNDED", "UNRESOLVED", "NOT_AVAILABLE", "NOT_APPLICABLE"})
CLOSURE_STATES = frozenset(
    {
        "HIERARCHICAL_REDUCTION_SUPPORTED_IN_REGIME",
        "PARTIAL_HIERARCHICAL_CLOSURE",
        "HIERARCHICAL_REDUCTION_FAILED",
        "UNRESOLVED",
        "NOT_APPLICABLE",
    }
)
CROSS_SCALE_LEVELS = frozenset(
    {
        "REPEATED_MATHEMATICAL_MOTIF",
        "PRESERVED_ARCHITECTURE_ACROSS_SCALE",
        "COMMON_PHYSICAL_MECHANISM",
        "COMMON_NUMERICAL_CHI_REGION",
    }
)
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


class SIV04Refusal(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


@dataclass(frozen=True)
class ArchitectureViews:
    scalar: str
    modal: str
    conglomeration: str

    def __post_init__(self) -> None:
        for name, value in (
            ("scalar", self.scalar),
            ("modal", self.modal),
            ("conglomeration", self.conglomeration),
        ):
            if value not in VIEW_STATES:
                raise SIV04Refusal("INVALID_VIEW_STATE", f"{name} state {value!r} is unsupported")

    def as_dict(self) -> dict[str, str]:
        return {
            "scalar": self.scalar,
            "modal": self.modal,
            "conglomeration": self.conglomeration,
        }


def relationship_pattern_v04(state: ArchitectureViews) -> str:
    views = state.as_dict()
    applicable = {name: value for name, value in views.items() if value != "NOT_APPLICABLE"}
    if not applicable:
        return "NO_APPLICABLE_VIEW_SUPPORT"
    if any(value in {"NONIDENTIFIABLE", "NOT_MEASURED"} for value in applicable.values()):
        return "RELATIONSHIP_UNRESOLVED"

    supported_names = {name for name, value in applicable.items() if value == "SUPPORTED"}
    if len(applicable) == 1:
        return "SINGLE_APPLICABLE_VIEW_SUPPORTED" if supported_names else "NO_VIEW_SUPPORT"

    supported = (
        "scalar" in supported_names,
        "modal" in supported_names,
        "conglomeration" in supported_names,
    )
    patterns = {
        (True, True, True): "CROSS_VIEW_COHERENCE",
        (True, False, False): "SCALAR_ONLY",
        (False, True, False): "MODAL_ONLY",
        (False, False, True): "CONGLOMERATION_ONLY",
        (True, True, False): "SCALAR_MODAL_WITHOUT_CONGLOMERATION",
        (True, False, True): "SCALAR_CONGLOMERATION_WITHOUT_MODAL",
        (False, True, True): "MODAL_CONGLOMERATION_WITHOUT_SCALAR",
        (False, False, False): "NO_VIEW_SUPPORT",
    }
    return patterns[supported]


def validate_uncertainty_alignment(
    views: ArchitectureViews,
    uncertainty: Mapping[str, str],
) -> dict[str, str]:
    required = {"scalar", "modal", "conglomeration"}
    if set(uncertainty) != required:
        raise SIV04Refusal(
            "INCOMPLETE_UNCERTAINTY_RECORD",
            "uncertainty must explicitly contain scalar, modal, and conglomeration reporting slots",
        )
    normalized: dict[str, str] = {}
    for name, view_state in views.as_dict().items():
        status = uncertainty[name]
        if status not in UNCERTAINTY_STATES:
            raise SIV04Refusal("INVALID_UNCERTAINTY_STATE", f"{name} uncertainty {status!r} is unsupported")
        if view_state == "NOT_APPLICABLE" and status != "NOT_APPLICABLE":
            raise SIV04Refusal(
                "NOT_APPLICABLE_MISMATCH",
                f"{name} view is NOT_APPLICABLE so its uncertainty must also be NOT_APPLICABLE",
            )
        if view_state != "NOT_APPLICABLE" and status == "NOT_APPLICABLE":
            raise SIV04Refusal(
                "NOT_APPLICABLE_MISMATCH",
                f"{name} view is applicable so its uncertainty cannot be NOT_APPLICABLE",
            )
        normalized[name] = status
    return normalized


def _require_bool(record: Mapping[str, Any], field: str, expected: bool, code: str) -> None:
    if record.get(field) is not expected:
        raise SIV04Refusal(code, f"{field} must be {expected}")


def validate_local_embedded_firewall(record: Mapping[str, Any]) -> dict[str, Any]:
    _require_bool(record, "local_identity_separate_from_embedded_behavior", True, "LOCAL_EMBEDDED_CONFLATION")
    _require_bool(record, "atlas_used_to_define_or_tune_coordinate", False, "ATLAS_COORDINATE_LEAKAGE")
    _require_bool(record, "atlas_used_to_define_or_tune_mapping", False, "ATLAS_MAPPING_LEAKAGE")
    _require_bool(record, "lower_level_scalars_averaged_into_system_scalar", False, "SYSTEM_SCALAR_AGGREGATION")

    system_scalar_reported = record.get("system_scalar_reported")
    separately_derived = record.get("system_scalar_separately_derived_if_reported")
    if not isinstance(system_scalar_reported, bool) or not isinstance(separately_derived, bool):
        raise SIV04Refusal(
            "INVALID_SYSTEM_SCALAR_FIREWALL",
            "system scalar firewall fields must be boolean",
        )
    if system_scalar_reported and not separately_derived:
        raise SIV04Refusal(
            "UNLICENSED_SYSTEM_SCALAR",
            "a reported system scalar requires a separate native derivation",
        )

    objects = record.get("objects")
    required_objects = {
        "local_or_intrinsic_subsystem_model",
        "outward_coupling_or_signal",
        "environment_or_connected_system_transformation",
        "feedback_or_return",
        "embedded_or_closed_loop_model",
        "survival_transformation_emergence_record",
    }
    if not isinstance(objects, Mapping) or set(objects) != required_objects:
        raise SIV04Refusal(
            "INCOMPLETE_RELATIONAL_RECORD",
            "relational-stability object slots must be present explicitly",
        )
    allowed_object_states = {"PROVIDED", "UNRESOLVED", "NOT_MEASURED", "NOT_APPLICABLE"}
    for name, value in objects.items():
        if value not in allowed_object_states:
            raise SIV04Refusal("INVALID_RELATIONAL_OBJECT_STATE", f"{name} state {value!r} is unsupported")
    return dict(record)


def _validate_hash(value: Any, where: str, allow_none: bool = False) -> str | None:
    if value is None and allow_none:
        return None
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise SIV04Refusal("INVALID_SHA256", f"{where} must be a 64-character hexadecimal SHA-256")
    return value.lower()


def validate_hierarchical_closure(record: Mapping[str, Any]) -> dict[str, Any]:
    enabled = record.get("enabled")
    if not isinstance(enabled, bool):
        raise SIV04Refusal("INVALID_HIERARCHY_GATE", "hierarchical_closure.enabled must be boolean")
    status = record.get("closure_status")
    if status not in CLOSURE_STATES:
        raise SIV04Refusal("INVALID_HIERARCHY_STATUS", f"unsupported closure status {status!r}")

    if not enabled:
        if status != "NOT_APPLICABLE":
            raise SIV04Refusal(
                "DISABLED_HIERARCHY_WITH_DECISION",
                "a disabled hierarchy gate must use NOT_APPLICABLE",
            )
        return dict(record)

    if status == "NOT_APPLICABLE":
        raise SIV04Refusal(
            "ENABLED_HIERARCHY_NOT_APPLICABLE",
            "an enabled hierarchy gate cannot use NOT_APPLICABLE",
        )
    for field in ("higher_level_question", "validity_regime", "uncertainty_or_tolerance"):
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            raise SIV04Refusal("INCOMPLETE_HIERARCHY_GATE", f"{field} must be a nonempty string")
    targets = record.get("preservation_targets")
    if not isinstance(targets, list) or not targets or any(not isinstance(x, str) or not x.strip() for x in targets):
        raise SIV04Refusal(
            "INCOMPLETE_HIERARCHY_GATE",
            "preservation_targets must be a nonempty list of declared higher-level quantities",
        )
    _validate_hash(record.get("reference_artifact_sha256"), "reference_artifact_sha256")
    _validate_hash(record.get("reduced_artifact_sha256"), "reduced_artifact_sha256")
    return dict(record)


def validate_recovery_resilience(record: Mapping[str, Any]) -> dict[str, Any]:
    enabled = record.get("enabled")
    if not isinstance(enabled, bool):
        raise SIV04Refusal("INVALID_RECOVERY_RECORD", "recovery_resilience.enabled must be boolean")
    _require_bool(record, "state_classification_separate", True, "RECOVERY_STATE_CONFLATION")
    _require_bool(
        record,
        "asymptotic_return_separate_from_finite_time_resilience",
        True,
        "ASYMPTOTIC_TRANSIENT_CONFLATION",
    )
    family = record.get("native_measure_family")
    if enabled:
        if not isinstance(family, str) or not family.strip() or family == "UNIVERSAL_RESILIENCE_SCORE":
            raise SIV04Refusal(
                "INVALID_RECOVERY_MEASURE",
                "enabled recovery/resilience requires a named domain-native measure family",
            )
        _validate_hash(record.get("source_artifact_sha256"), "recovery_resilience.source_artifact_sha256")
    else:
        if family not in {None, "NOT_APPLICABLE"}:
            raise SIV04Refusal(
                "DISABLED_RECOVERY_WITH_MEASURE",
                "disabled recovery/resilience must not report an active measure family",
            )
        _validate_hash(record.get("source_artifact_sha256"), "recovery_resilience.source_artifact_sha256", allow_none=True)
    return dict(record)


def validate_cross_scale_scope(record: Mapping[str, Any]) -> dict[str, Any]:
    level = record.get("claim_level")
    if level not in CROSS_SCALE_LEVELS:
        raise SIV04Refusal("INVALID_CROSS_SCALE_LEVEL", f"unsupported cross-scale claim level {level!r}")
    if record.get("universal_claim") is not False:
        raise SIV04Refusal(
            "UNIVERSALITY_FIREWALL",
            "finite recurrence or cross-scale structure may not be converted into a universal claim",
        )
    preserved = record.get("preserved_quantity")
    transformed = record.get("transformed_quantity")
    validity = record.get("validity_regime")
    loss = record.get("loss_condition")
    for name, value in (
        ("preserved_quantity", preserved),
        ("transformed_quantity", transformed),
        ("validity_regime", validity),
        ("loss_condition", loss),
    ):
        if not isinstance(value, str) or not value.strip():
            raise SIV04Refusal("INCOMPLETE_CROSS_SCALE_RECORD", f"{name} must be a nonempty string")
    return dict(record)
