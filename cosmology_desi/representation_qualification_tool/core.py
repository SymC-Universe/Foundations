"""Representation Qualification Engine (RQE) v0.2.

This module is intentionally non-autonomous scientifically. It applies a
frozen preregistered policy to evidence supplied by the analysis pipeline.
It does not invent thresholds, choose models, or promote hypotheses.

Scientific provenance:
Chr26, Nad16, Lee26b, Roy11, Sha21, Bas19, Vru21, Wie10, Kun07b,
Mar19, Per22, You26, Sui25, Hea20, Nic18.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Mapping, Optional


class Disposition(str, Enum):
    SCALAR_ADEQUATE = "SCALAR_ADEQUATE"
    MODAL_REQUIRED = "MODAL_REQUIRED"
    CHI_AGGREGATE_REQUIRED = "CHI_AGGREGATE_REQUIRED"
    ARC_REQUIRED = "ARC_REQUIRED"
    INHERITANCE_REQUIRED = "INHERITANCE_REQUIRED"
    FULL_ARCHITECTURE_REQUIRED = "FULL_ARCHITECTURE_REQUIRED"
    REFUSED_REDUNDANT = "REFUSED_REDUNDANT"
    REFUSED_MODEL_IMPOSED = "REFUSED_MODEL_IMPOSED"
    NEED_MORE_INFO = "NEED_MORE_INFO"


SOURCE_REGISTRY: Mapping[str, str] = {
    "Chr26": "doi:10.1038/s41598-026-56887-7",
    "Nad16": "doi:10.1093/mnras/stx1662",
    "Lee26b": "arXiv:2602.08207",
    "Roy11": "doi:10.1088/0264-9381/28/16/165004",
    "Sha21": "doi:10.1016/j.dark.2023.101192",
    "Bas19": "doi:10.1103/PhysRevD.100.043524",
    "Vru21": "doi:10.1103/PhysRevLett.127.231101",
    "Wie10": "doi:10.1103/PhysRevD.82.023523",
    "Kun07b": "doi:10.1103/PhysRevD.80.123001",
    "Mar19": "doi:10.1016/j.dark.2020.100490",
    "Per22": "doi:10.1016/j.dark.2022.101119",
    "You26": "arXiv:2607.11813",
    "Sui25": "doi:10.3847/1538-4357/ae3aa4",
    "Hea20": "doi:10.1093/mnras/staa2589",
    "Nic18": "doi:10.1088/1475-7516/2019/01/011",
}


@dataclass(frozen=True)
class GateEvidence:
    """One preregistered gate result.

    status must be one of: pass, fail, indeterminate, not_applicable.
    classification is optional and records scientific role without changing
    the frozen threshold outcome. Examples: independent, coordinate_only,
    model_imposed, insufficient_resolution.

    metric/value/threshold are descriptive; the engine never computes or
    changes a scientific threshold.
    """

    gate: str
    status: str
    classification: Optional[str] = None
    metric: Optional[str] = None
    value: Optional[float] = None
    threshold: Optional[float] = None
    reason: str = ""
    sources: List[str] = field(default_factory=list)

    def validate(self) -> None:
        allowed = {"pass", "fail", "indeterminate", "not_applicable"}
        if self.status not in allowed:
            raise ValueError(f"{self.gate}: invalid status {self.status!r}")
        unknown = [s for s in self.sources if s not in SOURCE_REGISTRY]
        if unknown:
            raise ValueError(f"{self.gate}: unknown source keys {unknown}")


@dataclass(frozen=True)
class QualificationRecord:
    target: str
    preregistration_id: str
    gates: List[GateEvidence]
    native_model: str
    adversaries: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Decision:
    disposition: Disposition
    rationale: List[str]
    failed_gates: List[str]
    indeterminate_gates: List[str]
    provenance: Dict[str, str]


ORDER = [
    "F1_local_chi",
    "F2_modal",
    "F3_capital_chi",
    "F4_arc",
    "F5_inheritance",
    "F6_joint_dmde",
    "F7_adversaries",
]


def qualify(record: QualificationRecord) -> Decision:
    """Apply a frozen gate record to produce an auditable disposition."""

    evidence = {g.gate: g for g in record.gates}
    for g in record.gates:
        g.validate()

    missing = [name for name in ORDER if name not in evidence]
    if missing:
        return Decision(
            disposition=Disposition.NEED_MORE_INFO,
            rationale=[f"Missing required gate evidence: {', '.join(missing)}"],
            failed_gates=[],
            indeterminate_gates=missing,
            provenance=_provenance(record.gates),
        )

    indeterminate = [
        name for name in ORDER if evidence[name].status == "indeterminate"
    ]
    if indeterminate:
        return Decision(
            disposition=Disposition.NEED_MORE_INFO,
            rationale=[f"Indeterminate gate(s): {', '.join(indeterminate)}"],
            failed_gates=[],
            indeterminate_gates=indeterminate,
            provenance=_provenance(record.gates),
        )

    f1 = evidence["F1_local_chi"]
    if f1.status == "fail" and f1.classification != "coordinate_only":
        return _refusal(
            record,
            "F1_local_chi",
            "Local chi failed qualification and is not retained even as a coordinate.",
        )

    if evidence["F2_modal"].status == "fail":
        rationale = [
            "Modal representation did not add preregistered incremental value."
        ]
        if f1.classification == "coordinate_only":
            rationale.append(
                "Local chi remains a descriptive coordinate only; no independent scalar claim is licensed."
            )
        return Decision(
            disposition=Disposition.SCALAR_ADEQUATE,
            rationale=rationale,
            failed_gates=["F2_modal"],
            indeterminate_gates=[],
            provenance=_provenance(record.gates),
        )

    if evidence["F3_capital_chi"].status == "fail":
        return Decision(
            disposition=Disposition.MODAL_REQUIRED,
            rationale=[
                "Modal structure qualified, but aggregate capital-Chi relation added no independent value."
            ],
            failed_gates=["F3_capital_chi"],
            indeterminate_gates=[],
            provenance=_provenance(record.gates),
        )

    if evidence["F4_arc"].status == "fail":
        return Decision(
            disposition=Disposition.CHI_AGGREGATE_REQUIRED,
            rationale=[
                "Aggregate Chi qualified, but trajectory/Arc information was redundant."
            ],
            failed_gates=["F4_arc"],
            indeterminate_gates=[],
            provenance=_provenance(record.gates),
        )

    if evidence["F5_inheritance"].status == "fail":
        return Decision(
            disposition=Disposition.ARC_REQUIRED,
            rationale=[
                "Stability Arc qualified, but SI added no information beyond standard history/transfer variables."
            ],
            failed_gates=["F5_inheritance"],
            indeterminate_gates=[],
            provenance=_provenance(record.gates),
        )

    if evidence["F6_joint_dmde"].status == "fail":
        return Decision(
            disposition=Disposition.INHERITANCE_REQUIRED,
            rationale=[
                "Inheritance qualified for the frozen target, but joint DM/DE architecture did not."
            ],
            failed_gates=["F6_joint_dmde"],
            indeterminate_gates=[],
            provenance=_provenance(record.gates),
        )

    if evidence["F7_adversaries"].status == "fail":
        return Decision(
            disposition=Disposition.REFUSED_MODEL_IMPOSED,
            rationale=[
                "Integrated architecture failed matched adversarial transport."
            ],
            failed_gates=["F7_adversaries"],
            indeterminate_gates=[],
            provenance=_provenance(record.gates),
        )

    rationale = [
        "All preregistered component, integration, joint-DM/DE, and adversarial gates passed."
    ]
    if f1.classification == "coordinate_only":
        rationale.append(
            "Local chi is retained as a coordinate rather than an independent degree of freedom."
        )
    return Decision(
        disposition=Disposition.FULL_ARCHITECTURE_REQUIRED,
        rationale=rationale,
        failed_gates=[],
        indeterminate_gates=[],
        provenance=_provenance(record.gates),
    )


def _refusal(record: QualificationRecord, gate: str, reason: str) -> Decision:
    return Decision(
        disposition=Disposition.REFUSED_REDUNDANT,
        rationale=[reason],
        failed_gates=[gate],
        indeterminate_gates=[],
        provenance=_provenance(record.gates),
    )


def _provenance(gates: List[GateEvidence]) -> Dict[str, str]:
    keys = []
    for g in gates:
        for key in g.sources:
            if key not in keys:
                keys.append(key)
    return {key: SOURCE_REGISTRY[key] for key in keys}
