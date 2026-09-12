import pytest

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


def _valid_relational_record():
    return {
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


def test_scalar_may_be_not_applicable_without_forcing_relationship_unresolved():
    state = ArchitectureViews("NOT_APPLICABLE", "SUPPORTED", "SUPPORTED")
    assert relationship_pattern_v04(state) == "MODAL_CONGLOMERATION_WITHOUT_SCALAR"


def test_single_applicable_view_can_be_reported_without_manufacturing_other_layers():
    state = ArchitectureViews("NOT_APPLICABLE", "SUPPORTED", "NOT_APPLICABLE")
    assert relationship_pattern_v04(state) == "SINGLE_APPLICABLE_VIEW_SUPPORTED"


def test_all_views_not_applicable_is_explicit_not_a_fake_failure():
    state = ArchitectureViews("NOT_APPLICABLE", "NOT_APPLICABLE", "NOT_APPLICABLE")
    assert relationship_pattern_v04(state) == "NO_APPLICABLE_VIEW_SUPPORT"


def test_nonidentifiable_applicable_view_keeps_relationship_unresolved():
    state = ArchitectureViews("NOT_APPLICABLE", "NONIDENTIFIABLE", "SUPPORTED")
    assert relationship_pattern_v04(state) == "RELATIONSHIP_UNRESOLVED"


def test_uncertainty_not_applicable_must_align_with_view_not_applicable():
    state = ArchitectureViews("NOT_APPLICABLE", "SUPPORTED", "SUPPORTED")
    result = validate_uncertainty_alignment(
        state,
        {"scalar": "NOT_APPLICABLE", "modal": "BOUNDED", "conglomeration": "UNRESOLVED"},
    )
    assert result["scalar"] == "NOT_APPLICABLE"


def test_uncertainty_not_applicable_mismatch_refuses():
    state = ArchitectureViews("NOT_APPLICABLE", "SUPPORTED", "SUPPORTED")
    with pytest.raises(SIV04Refusal, match="NOT_APPLICABLE_MISMATCH"):
        validate_uncertainty_alignment(
            state,
            {"scalar": "BOUNDED", "modal": "BOUNDED", "conglomeration": "BOUNDED"},
        )


def test_local_embedded_firewall_accepts_separated_record():
    result = validate_local_embedded_firewall(_valid_relational_record())
    assert result["local_identity_separate_from_embedded_behavior"] is True


def test_lower_level_scalar_averaging_is_refused():
    record = _valid_relational_record()
    record["lower_level_scalars_averaged_into_system_scalar"] = True
    with pytest.raises(SIV04Refusal, match="SYSTEM_SCALAR_AGGREGATION"):
        validate_local_embedded_firewall(record)


def test_atlas_coordinate_leakage_is_refused():
    record = _valid_relational_record()
    record["atlas_used_to_define_or_tune_coordinate"] = True
    with pytest.raises(SIV04Refusal, match="ATLAS_COORDINATE_LEAKAGE"):
        validate_local_embedded_firewall(record)


def test_system_scalar_without_separate_derivation_is_refused():
    record = _valid_relational_record()
    record["system_scalar_reported"] = True
    record["system_scalar_separately_derived_if_reported"] = False
    with pytest.raises(SIV04Refusal, match="UNLICENSED_SYSTEM_SCALAR"):
        validate_local_embedded_firewall(record)


def test_disabled_hierarchical_gate_uses_not_applicable():
    result = validate_hierarchical_closure(
        {
            "enabled": False,
            "higher_level_question": "NOT_APPLICABLE",
            "validity_regime": "NOT_APPLICABLE",
            "preservation_targets": [],
            "reference_artifact_sha256": None,
            "reduced_artifact_sha256": None,
            "uncertainty_or_tolerance": "NOT_APPLICABLE",
            "closure_status": "NOT_APPLICABLE",
        }
    )
    assert result["closure_status"] == "NOT_APPLICABLE"


def test_disabled_hierarchical_gate_cannot_report_success():
    with pytest.raises(SIV04Refusal, match="DISABLED_HIERARCHY_WITH_DECISION"):
        validate_hierarchical_closure(
            {
                "enabled": False,
                "closure_status": "HIERARCHICAL_REDUCTION_SUPPORTED_IN_REGIME",
            }
        )


def test_enabled_hierarchical_gate_requires_question_regime_targets_and_provenance():
    result = validate_hierarchical_closure(
        {
            "enabled": True,
            "higher_level_question": "Does the reduced coupled subsystem preserve the declared return operator?",
            "validity_regime": "synthetic linear time-invariant qualification regime",
            "preservation_targets": ["input-output response", "feedback return"],
            "reference_artifact_sha256": _h("a"),
            "reduced_artifact_sha256": _h("b"),
            "uncertainty_or_tolerance": "machine-precision comparison under the synthetic construction",
            "closure_status": "HIERARCHICAL_REDUCTION_SUPPORTED_IN_REGIME",
        }
    )
    assert result["closure_status"] == "HIERARCHICAL_REDUCTION_SUPPORTED_IN_REGIME"


def test_enabled_hierarchical_gate_missing_targets_refuses():
    with pytest.raises(SIV04Refusal, match="INCOMPLETE_HIERARCHY_GATE"):
        validate_hierarchical_closure(
            {
                "enabled": True,
                "higher_level_question": "question",
                "validity_regime": "regime",
                "preservation_targets": [],
                "reference_artifact_sha256": _h("a"),
                "reduced_artifact_sha256": _h("b"),
                "uncertainty_or_tolerance": "tolerance",
                "closure_status": "UNRESOLVED",
            }
        )


def test_recovery_semantics_keep_state_and_recovery_separate():
    result = validate_recovery_resilience(
        {
            "enabled": True,
            "state_classification_separate": True,
            "asymptotic_return_separate_from_finite_time_resilience": True,
            "native_measure_family": "synthetic state-transition response family",
            "source_artifact_sha256": _h("c"),
        }
    )
    assert result["enabled"] is True


def test_recovery_state_conflation_refuses():
    with pytest.raises(SIV04Refusal, match="RECOVERY_STATE_CONFLATION"):
        validate_recovery_resilience(
            {
                "enabled": True,
                "state_classification_separate": False,
                "asymptotic_return_separate_from_finite_time_resilience": True,
                "native_measure_family": "synthetic response",
                "source_artifact_sha256": _h("c"),
            }
        )


def test_asymptotic_return_cannot_be_declared_equivalent_to_finite_time_resilience():
    with pytest.raises(SIV04Refusal, match="ASYMPTOTIC_TRANSIENT_CONFLATION"):
        validate_recovery_resilience(
            {
                "enabled": True,
                "state_classification_separate": True,
                "asymptotic_return_separate_from_finite_time_resilience": False,
                "native_measure_family": "synthetic response",
                "source_artifact_sha256": _h("c"),
            }
        )


def test_cross_scale_record_preserves_scope_without_universality():
    result = validate_cross_scale_scope(
        {
            "claim_level": "PRESERVED_ARCHITECTURE_ACROSS_SCALE",
            "universal_claim": False,
            "preserved_quantity": "declared input-output response",
            "transformed_quantity": "internal carrier basis",
            "validity_regime": "synthetic qualification regime",
            "loss_condition": "response preservation exceeds the frozen tolerance",
        }
    )
    assert result["claim_level"] == "PRESERVED_ARCHITECTURE_ACROSS_SCALE"


def test_finite_cross_scale_recurrence_cannot_be_called_universal():
    with pytest.raises(SIV04Refusal, match="UNIVERSALITY_FIREWALL"):
        validate_cross_scale_scope(
            {
                "claim_level": "REPEATED_MATHEMATICAL_MOTIF",
                "universal_claim": True,
                "preserved_quantity": "motif",
                "transformed_quantity": "scale",
                "validity_regime": "synthetic",
                "loss_condition": "motif absent",
            }
        )
