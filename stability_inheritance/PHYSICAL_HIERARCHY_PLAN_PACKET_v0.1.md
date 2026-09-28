# Stability Inheritance Controlled Physical Hierarchy Plan Packet v0.1

**Status:** PLAN_DRAFT / NOT FROZEN / DO NOT EXECUTE AS CONFIRMATION  
**Lifecycle:** Stage 2, Adversarial Plan Qualification  
**Date:** 2026-09-27  
**Governance:** SymC GOM v1.0  
**Claim ceiling:** P0-Q physical qualification unless a later independently frozen P1 extension is approved.

## 1. Purpose

Qualify the Stability Inheritance representation and refusal logic in a controlled modular mechanical system where lower-level modes, scalar damping coordinates, interface coupling, and assembled-system behavior can be measured independently.

The experiment does **not** test whether component modes influence an assembly. That is established prior art. It tests whether the SI workflow correctly separates:

- licensed scalar χ;
- base modal/vector Χ;
- coupling/interface mapping;
- conglomerate/system Χ_con;
- realized perturbation/recovery behavior;

and whether the proposed inheritance labels agree with native component-mode/substructuring predictions while refusing unsupported stronger claims.

## 2. Primary scientific question

When a mechanically characterized parent module is embedded in a larger assembly, which parent properties remain identifiable in the assembled response, which are transformed by interface coupling, and which become insufficient or nonidentifying once the separate Χ_con organization is considered?

## 3. Representation contract

### Scalar χ

For a parent mode i, report

χ_i = γ_i / (2 ω_i)

only if a stable second-order modal reduction and damping assignment are independently licensed. If damping is nonproportional or the modal quotient is not identifiable, return χ = REFUSED for that mode.

### Base modal/vector Χ

For each independently characterized component:

- natural frequencies / complex poles as appropriate;
- mode shapes or invariant subspaces;
- interface participation amplitudes;
- modal mass/normalization convention;
- damping information with uncertainty;
- conditioning / near-degeneracy diagnostics;
- measured FRF/state-space representation where available.

### Conglomerate/system Χ_con

Χ_con is not the parent modal basis. It is the assembled-system organization, including where measurable:

- assembly modes/subspaces;
- modal participation and mixing across components;
- interface energy/response transfer;
- assembly transfer functions/state-transition structure;
- transient amplification;
- recovery/reorganization profile after a frozen perturbation.

No single scalar Χ_con is presumed.

## 4. Apparatus class

Use a modular passive mechanical assembly with at least:

- one independently characterizable parent substructure with >=2 resolved modes;
- one independently characterizable receiving/child substructure;
- a repeatable coupling interface whose location or stiffness can be changed prospectively;
- an excitation and response measurement path sufficient for modal/FRF identification;
- optional independently adjustable damping that does not require changing stiffness/mass geometry.

The user’s available fabrication access, springs, bearings, aluminum, threaded rod, fasteners, and salvaged speaker magnets may support implementation, including possible non-contact eddy-current damping, but the APQ plan does not freeze a hardware layout until measurement precision and repeatability are justified.

## 5. Planned qualification manipulations

### Q1: Interface-specificity test, parent held fixed

Independently characterize the parent module once. Couple the same parent to the same child through prospectively selected interface A versus interface B, chosen from parent modal geometry before assembled response is measured.

The parent χ and parent Χ remain fixed. The coupling map changes.

**Prediction:** standard substructuring/CMS and the SI modal-plus-coupling representation should predict different Χ_con/response when the interface samples different modal participation. Scalar-only parent χ should not be sufficient.

**Refusal:** if interfaces are not mechanically repeatable or the parent modal state drifts beyond frozen equivalence bounds between assemblies, Q1 is INVALID_TEST rather than inheritance evidence.

### Q2: Parent-modal intervention, coupling held fixed

With interface geometry fixed, make one prospective parent intervention that changes a resolved parent modal property, such as stiffness or mass distribution, while leaving the child and interface definition unchanged.

**Prediction:** the frozen component/substructuring model predicts a corresponding change in assembly Χ_con and response. The intervention direction and target assembly observables must be frozen before the modified assembly is measured.

**Refusal:** if the intervention simultaneously changes uncontrolled interface properties or invalidates the original component boundary, classify CONFOUNDED_INTERVENTION.

### Q3: Scalar-damping intervention, modal geometry approximately fixed

If an independently calibrated damping intervention is feasible, alter damping through a mechanism such as controlled eddy-current damping while keeping component mass/stiffness geometry fixed within measurement tolerance.

**Prediction:** χ-linked recovery changes may occur while undamped modal geometry Χ remains approximately preserved. The test determines which recovery observables are captured by χ and which still require Χ_con.

**Refusal:** if the damping intervention substantially changes stiffness, boundary conditions, or modal geometry, do not interpret it as a scalar-specific intervention.

Q3 is optional for the first qualification cycle. Failure to implement a clean damping intervention does not invalidate Q1/Q2.

## 6. Perturbation / response protocol

Use a prospectively fixed perturbation that can be repeated without changing the assembly, such as a calibrated impulse or release from a fixed displacement.

Response outcomes are separated into:

- initial resistance / peak response;
- transient amplification;
- energy or response transfer across modules;
- first zero crossing where applicable;
- first reclaim of a declared response band;
- sustained recovery within that band;
- settling/recovery timescale;
- final state;
- repeated-perturbation drift/hysteresis only if a dedicated repeated-perturbation extension is frozen later.

Recovery is a probe, not the definition of stability.

## 7. Native comparator stack

The experiment must be analyzed against, at minimum:

1. direct component-mode synthesis / dynamic substructuring using independently measured component information;
2. state-space or FRF-based native model appropriate to the apparatus;
3. scalar-only representation using admissible local χ and frequency information;
4. modal-only representation using Χ without explicit interface/conglomerate organization;
5. modal + coupling / Χ_con representation;
6. persistence/simple empirical baseline for any predictive time-series endpoint.

Where approximate bisimulation, passivity/small-gain, or another native control-theoretic comparator is scientifically appropriate, add it before outcome exposure.

## 8. Primary qualification contrasts

### Contrast A: scalar sufficiency

Does χ-only predict the frozen assembly response as well as the modal/native alternatives?

Expected admissible outcomes:
- SCALAR_SUFFICIENT_FOR_TASK;
- SCALAR_INFORMATION_LOSS;
- SCALAR_REFUSED.

### Contrast B: modal carrier specificity

Does interface-resolved Χ distinguish Q1 interface A versus B when scalar summaries are unchanged?

Expected admissible outcomes:
- MODAL_CARRIER_ADDS;
- MODAL_EQUIVALENT_TO_NATIVE_SIMPLE;
- MODAL_NONIDENTIFIABLE;
- INVALID_TEST.

### Contrast C: conglomerate necessity

Does explicit coupling/system organization improve prediction over parent Χ alone?

Expected admissible outcomes:
- Χ_CON_ADDS;
- MODAL_ONLY_SUFFICIENT;
- NATIVE_MODEL_SUFFICIENT;
- SYSTEM_ONLY_STRUCTURE_WITHOUT_INHERITANCE.

### Contrast D: intervention consistency

Does the prospectively predicted direction/magnitude of the Q2 intervention survive measurement?

Expected admissible outcomes:
- INTERVENTION_CONSISTENT;
- TRANSFORMED_RELATION;
- INTERVENTION_FALSIFIED;
- CONFOUNDED_INTERVENTION.

## 9. Mechanistic inheritance ceiling

The first physical qualification cycle cannot label CARRIER_RESOLVED_INHERITANCE unless all six gates are satisfied:

1. parent characterization before assembly target reveal;
2. explicit interface/carrier correspondence;
3. frozen transformation rule;
4. prospective assembly prediction;
5. parent/carrier intervention;
6. specificity against at least one alternative interface/carrier control.

Even if all six pass, the claim remains apparatus-specific P0-Q unless design adequacy and an independent confirmatory cycle are frozen before new decisive evidence.

## 10. Masking and information firewall

- Parent/component characterization is completed before assembled target data are inspected.
- Q1 interface locations are selected from parent modal geometry and engineering feasibility, not from assembled outcomes.
- Q2 intervention target and predicted direction are frozen before modified assembly data.
- Analysis code and outcome definitions are frozen before decisive target runs.
- A separate operator may label files A/B or intervention/control if practical; if not, lack of analyst masking is recorded.
- Pilot runs used for sensor placement or mechanical debugging are permanently excluded from confirmation.

## 11. Precision and design-adequacy requirements before freeze

Before full execution, demonstrate mechanically:

- repeatable assembly/disassembly without unacceptable modal drift;
- sufficient frequency resolution to distinguish targeted modes;
- sensor/excitation linearity over the chosen perturbation range;
- measurement noise low enough for principal-angle/FRF comparisons;
- stable timing synchronization across channels;
- uncertainty propagation for modal frequency, damping, and response metrics;
- no clipping/saturation;
- enough repeated trials to estimate within-configuration variability.

No numeric equivalence margin is frozen in v0.1. Margins must be derived from measurement repeatability or external instrument specifications before target outcomes.

## 12. Known-truth / negative controls

- uncoupled or near-zero coupling condition where assembly transfer should collapse;
- repeat assembly with unchanged interface to estimate mechanical repeatability;
- label-scrambled modal correspondence in analysis;
- same-spectrum or modal-permutation control where analytically/physically feasible;
- coupling rewire / alternate interface;
- synthetic digital twin with known component matrices to verify analysis code;
- deliberately nonidentifiable case if feasible, such as near-degenerate parent modes, to test subspace rather than one-to-one mode matching.

## 13. Failure architecture

The experiment succeeds scientifically even if SI adds nothing.

Preserve:
- NATIVE_MODEL_SUFFICIENT;
- SCALAR_REFUSED;
- MODAL_NONIDENTIFIABLE;
- MODAL_ONLY;
- Χ_CON_ONLY;
- TRANSFORMED_NOT_INHERITED;
- NO_ADDED_INHERITANCE_VALUE;
- INVALID_TEST / mechanical confound.

A result may not be rescued by changing the interface, perturbation, metric, mapping, or equivalence threshold after target exposure.

## 14. Scale-up sequence

1. digital/synthetic known-truth verification of the exact analysis pipeline;
2. single-component repeatability and χ admissibility check;
3. uncoupled two-module control;
4. coupled baseline preflight;
5. Q1 interface-specificity pilot excluded from confirmation;
6. mechanical-repeatability audit and margin freeze;
7. independent Q1/Q2 qualification execution;
8. only after closeout, decide whether an untouched P1 replication or cross-apparatus transfer is scientifically justified.

## 15. Current APQ questions

Before this plan can freeze, adversarial review must answer:

- Is the proposed experiment merely a demonstration of standard CMS with SI labels?
- Can Χ_con be defined independently enough to avoid circularly deriving it from the same modes used as predictors?
- Is the higher-level native comparator truly independent of the lower-level descriptors, or does the comparison double-count the same information?
- Can Q1 alter coupling without changing the parent boundary conditions?
- Can Q2 alter parent Χ without contaminating the interface?
- Is Q3 feasible without stiffness/boundary-condition contamination?
- What result would genuinely falsify the SI qualification framework rather than only one apparatus?
- Does the experiment test inheritance, or only influence/composition?
- Is a real physical experiment scientifically preferable to a public benchmark dataset for this first qualification stage?

## 16. Plan status

**DRAFT ONLY.** No apparatus, threshold, equivalence margin, perturbation amplitude, sensor, interface, endpoint, or P1 claim is frozen.

The next action is APQ-2 adversarial review plus a prior-art collision specifically on the final apparatus class and comparator stack.
