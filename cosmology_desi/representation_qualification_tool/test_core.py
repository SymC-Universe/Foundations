from core import (
    Decision,
    Disposition,
    GateEvidence,
    QualificationRecord,
    qualify,
)


def gate(name, status, sources=None):
    return GateEvidence(
        gate=name,
        status=status,
        reason="prospective unit-test fixture",
        sources=sources or [],
    )


def full_record(statuses):
    names = [
        "F1_local_chi",
        "F2_modal",
        "F3_capital_chi",
        "F4_arc",
        "F5_inheritance",
        "F6_joint_dmde",
        "F7_adversaries",
    ]
    source_map = {
        "F1_local_chi": ["Chr26"],
        "F2_modal": ["Nad16", "Lee26b", "Sui25", "Hea20"],
        "F3_capital_chi": ["Sui25"],
        "F4_arc": ["Chr26", "Roy11", "Wie10"],
        "F5_inheritance": ["Vru21", "Wie10"],
        "F6_joint_dmde": ["Per22", "You26", "Kun07b", "Mar19"],
        "F7_adversaries": ["Nic18", "Hea20", "Bas19", "Sha21"],
    }
    return QualificationRecord(
        target="fixture",
        preregistration_id="RQE-TEST-001",
        native_model="LambdaCDM/GR",
        adversaries=["w0wa", "mnu", "MG", "IDE"],
        gates=[
            gate(n, statuses.get(n, "pass"), source_map[n])
            for n in names
        ],
    )


def test_missing_gate_needs_more_info():
    rec = QualificationRecord(
        target="fixture",
        preregistration_id="RQE-TEST-002",
        native_model="LambdaCDM/GR",
        gates=[gate("F1_local_chi", "pass", ["Chr26"])],
    )
    assert qualify(rec).disposition == Disposition.NEED_MORE_INFO


def test_scalar_adequate_when_modal_fails_incremental_value():
    decision = qualify(full_record({"F2_modal": "fail"}))
    assert decision.disposition == Disposition.SCALAR_ADEQUATE


def test_modal_required_when_capital_chi_fails():
    decision = qualify(full_record({"F3_capital_chi": "fail"}))
    assert decision.disposition == Disposition.MODAL_REQUIRED


def test_full_architecture_requires_all_gates():
    decision = qualify(full_record({}))
    assert decision.disposition == Disposition.FULL_ARCHITECTURE_REQUIRED


def test_adversarial_failure_refuses_model_imposed_architecture():
    decision = qualify(full_record({"F7_adversaries": "fail"}))
    assert decision.disposition == Disposition.REFUSED_MODEL_IMPOSED
