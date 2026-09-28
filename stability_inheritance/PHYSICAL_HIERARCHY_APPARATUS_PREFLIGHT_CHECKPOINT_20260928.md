# Physical Hierarchy Apparatus Preflight Checkpoint

Date: 2026-09-28
Governance: SymC GOM v1.0
Status: pre-freeze design qualification only
Ceiling: P0-Q known-truth physical qualification

The digital twin remains feasibility-only. The physical plan is not ready to freeze until these apparatus-level items are prospectively specified:

- concrete parent/child geometry and two Q1 interface locations chosen from isolated-parent modal geometry before assembled outcomes;
- calibrated excitation and response channels adequate for FRF/state-space identification;
- assembly/disassembly repeatability protocol and a prospective rule for deriving equivalence margins from repeatability or instrument specifications;
- reciprocity, passivity/physical-consistency, interface-rank/conditioning, and sensor-health gates with explicit refusal behavior;
- parent remeasurement around Q1 assembly cycles to detect boundary/interface drift;
- a Q2 intervention that changes the parent modal state without changing the interface or child;
- at least one deliberate nonidentifiable or near-degenerate case so MODAL_NONIDENTIFIABLE is genuinely testable;
- scalar chi refusal when damping/modal reduction is not independently identifiable;
- Chi_arc defined only from direct assembled measurements after predictions are frozen.

No decisive Q1/Q2 physical outcome is authorized before the apparatus, measurement precision, equivalence margins, and failure/refusal rules are frozen.

Valid outcomes include NATIVE_FRAMEWORK_EQUIVALENT, FRAMEWORK_NO_ADDED_VALUE, FRAMEWORK_NOT_OPERATIONAL, SCALAR_REFUSED, MODAL_NONIDENTIFIABLE, MODAL_ONLY, TRANSFORMED_NOT_INHERITED, and NO_ADDED_INHERITANCE_VALUE.