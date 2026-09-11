---
title: "General Cross-Project Research Protocol v0.7.1A: Functional Mapping and Natural Limit-Testbed Addendum"
version: "0.7.1A"
status: "Authoritative Addendum"
applies_to: "General Cross-Project Research Protocol v0.7.1 FINAL"
date: "10 September 2026"
project: "SymC / Stability Architecture Research Program"
core_rule: "Truth outranks continuity, and understanding a phenomenon requires mapping both how it works and where it fails."
claim_effect: "Additive only. Does not weaken MFR-14, frozen-holdout rules, native-model-first requirements, or existing domain safeguards."
---

# GENERAL CROSS-PROJECT RESEARCH PROTOCOL v0.7.1A
## Functional Mapping and Natural Limit-Testbed Addendum

This addendum corrects a possible operational imbalance in v0.7.1: falsification safeguards must not make exploratory and qualification work so failure-dominated that the program stops learning how supported systems actually work.

The governing principle is:

> **Do not merely attack the hypothesis. Map the phenomenon.**

A mature investigation must learn both:

1. how the system behaves across the regime in which the relevant native model or representation is supported; and
2. where, how, and why that model, representation, mechanism, or stability architecture degrades, transforms, refuses, or fails.

Neither task substitutes for the other.

---

## A.1 Research-mode separation inside P0/P1/P2

The v0.7.1 maturity tiers remain unchanged. Two submodes are added inside P0 so that scientific learning is not forced to behave like confirmation.

### A.1.1 P0-D: discovery and mechanism mapping

P0-D may freely use open-ended parameter scans, alternative estimators, visualizations, post-hoc diagnostics, already-viewed data, failed cases, and candidate transformations to:

- discover structure and candidate mechanisms;
- map response surfaces and trajectories;
- inspect coupling, compensation, inheritance, redistribution, and reorganization;
- determine how a system behaves where it works;
- locate candidate limits and anomalies;
- generate candidate scalar, modal/vector, conglomerate/system, or additional architectural objects.

Required: provenance, versioned substantial computation, preserved failures/anomalies, explicit exploratory status, and no confirmatory language.

A result discovered in P0-D may be scientifically important, but it is not confirmatory evidence for itself.

### A.1.2 P0-Q: qualification and controlled iteration

P0-Q determines whether a candidate System Model, Engine component, estimator, transformation, or representation is fit to face confirmation.

It may iteratively use known-truth systems, calibration data, previously observed failures, adversarial synthetic systems, known-bad inputs, sensitivity analysis, identifiability analysis, and internal validation.

A failed P0-Q test may justify a new version using the same qualification evidence if the change and reason are preserved. The qualification evidence does not become confirmatory evidence for the revised version.

Canonical path:

`P0-D discovery -> P0-Q qualification -> P1 frozen confirmation -> P2 release/tool qualification`

### A.1.3 P1 remains hard at the claim boundary

Nothing here weakens P1. MFR-14, frozen decision rules, untouched decisive evidence, outcome-independent analysis, and preserved prospective failures remain mandatory. Post-result diagnosis may improve the next version but may not rescue the failed version.

### A.1.4 P2 remains engineering-grade

Clean-room reproduction, mutation testing, semantic validation, dependency closure, release manifests, refusal qualification, and mature Atlas controls belong to P2 where applicable. They are not automatically imposed on P0-D or P0-Q.

---

## A.2 Function Map and Limit Map are coequal targets

Section 2.7 makes failure architecture a scientific target. The complementary rule is now explicit:

> **Where native science permits it, map the functioning interior with the same seriousness used to map limits.**

### A.2.1 Function Map

The Function Map asks what happens where the native system/model is supported:

- which states and trajectories occur;
- how scalar, modal/vector, conglomerate/system, open-channel, or additional components vary;
- how ordinary perturbations are absorbed or propagated;
- which couplings or relationships organize behavior;
- whether compensation, redundancy, redistribution, or reorganization occurs;
- whether several internal organizations produce similar system outcomes;
- what information is destroyed by reduction;
- what regions are actually occupied, not merely mathematically possible.

### A.2.2 Limit Map

The Limit Map asks where supported organization changes, degrades, becomes non-identifiable, exits the model class, or fails:

- where the transition occurs;
- whether it is gradual, abrupt, hysteretic, stochastic, or unresolved;
- which component or relationship changes first;
- whether coupling protects or destabilizes the system;
- whether the correct output is transition, partial admission, refusal, or failure;
- whether another representation becomes necessary.

Neither map may erase the other.

### A.2.3 P0 should prefer landscapes over boundary-only scans

Where feasible, use scientifically meaningful ranges and produce response surfaces, trajectories, sensitivity fields, recovery curves, modal-reorganization maps, coupling sweeps, regime diagrams, uncertainty surfaces, or occupancy distributions.

No universal grid or equal compute allocation is required. Native science determines the useful range and resolution.

A favorable region found after inspection remains P0-D until independently tested. Broadness or visual coherence does not promote it automatically.

---

## A.3 Rare natural occurrences as limit testbeds

Rare natural occurrences can expose parameter combinations, couplings, scales, or perturbations that are difficult, unsafe, unethical, expensive, or impossible to reproduce experimentally. When scientifically qualified, they should be used as **high-information limit testbeds**.

### A.3.1 `RARE_NATURAL_TESTBED`

A `RARE_NATURAL_TESTBED` is a naturally occurring event, state, phenotype, transition, perturbation, or environment that is unusual by domain-native evidence and relevant to the declared scientific question.

Rarity should be established, where possible, by prevalence/event frequency, tail position in a reference distribution, an accepted extreme-event category, an unusual documented parameter combination, or another domain-native criterion.

A case is not rare merely because it surprises SymC or produces an interesting chi result. No universal rarity percentile is imposed.

### A.3.2 Scientific uses

A rare natural testbed may probe:

- robustness limits;
- boundary localization;
- regime transitions;
- nonlinear response;
- coupling saturation;
- loss of compensation/recovery;
- model-class breakdown;
- inheritance loss or reorganization;
- rare-mode activation;
- extreme forcing;
- refusal behavior;
- transfer beyond ordinary operating conditions.

A rare event can also reveal an unknown functioning mechanism. That discovery enters P0-D and follows the ordinary promotion path.

### A.3.3 Rare does not mean representative

Rare natural cases do not by themselves establish normal prevalence, typical behavior, ordinary operating range, population-average performance, or baseline parameters.

Preserve base-rate context when scientifically knowable.

`RARE NATURAL OCCURRENCE -> HIGH-INFORMATION LIMIT PROBE`

not

`RARE NATURAL OCCURRENCE -> REPRESENTATIVE DOMAIN EXAMPLE`

### A.3.4 Authenticity and confounding gate

Before interpreting a rare case, distinguish a genuine natural extreme from measurement/preprocessing error, corruption, selection artifact, mislabeling, duplicate/pseudoreplicated events, undocumented intervention, or unsupported anecdote.

Where possible, interpret it against matched ordinary or less-extreme context such as lower-severity events, nearby unaffected systems, before/after states, native historical baselines, or matched mechanistic controls.

### A.3.5 Rare-event selection firewall

For P1 use, eligibility and selection must be frozen independently of the System Model/Engine result.

Permitted selection information includes domain-native event magnitude, accepted category, location, exposure, phenotype, date, or independently measured severity.

Selection may not use closeness to a predicted chi value, favorable residuals, agreement with the proposed architecture, visual similarity to the expected result, or another output generated by the model being tested.

If selected after the framework outcome is known, the case remains post-result discovery and carries promotion debt. Preserve the eligible candidate universe or search route where feasible.

### A.3.6 Historical extremes versus untouched extremes

Previously inspected historical extremes may be used freely for P0-D discovery, mechanism diagnosis, P0-Q qualification, and boundary-hypothesis generation.

They cannot independently confirm rules developed from them.

Canonical path:

`historical extreme -> discovery/qualification -> frozen limit prediction -> untouched/future extreme -> confirmation or falsification`

If no suitable independent natural extreme exists, use synthetic known-truth stress tests, controlled perturbations, historical reconstruction, mechanistic extrapolation, or a lower claim ceiling. Scarcity does not permit one event to serve simultaneously as discovery, calibration, and independent confirmation.

---

## A.4 Coverage architecture

Where native science and data availability permit, substantial projects should seek evidence across four research roles:

- `NOMINAL_FUNCTION`: ordinary or well-supported functioning regime;
- `PERTURBED_FUNCTION`: perturbed but still functioning/recovering regime;
- `BOUNDARY_OR_TRANSITION`: region approaching or undergoing a physical/model/inferential transition;
- `RARE_NATURAL_LIMIT`: unusual natural states used as limit probes.

These are research roles, not universal physical phases. Any may be `NOT_AVAILABLE`, `NOT_APPLICABLE`, or `UNRESOLVED`.

Rules:

- excellent nominal performance does not erase a limit failure;
- a rare catastrophic failure does not imply poor ordinary performance;
- a boundary case does not define a population mean;
- refusal in one regime does not invalidate a licensed regime elsewhere;
- successful compensation in one range does not establish compensation everywhere.

---

## A.5 Claim-specific gates and partial results

Gates attach to the claim being made, not automatically to every possible layer.

A scalar claim requires a licensed scalar object. A modal claim requires identifiable modal/subspace evidence. A conglomerate/system claim requires the corresponding system object. A causal feedback/recovery claim requires causally informative evidence. An added-value claim requires the appropriate native comparator. A cross-domain claim inherits the portfolio rules.

A project does not need a full-system PASS before reporting a narrower supported result.

Allowed states include component-specific support, partial admission, `INDETERMINATE`, `UNRESOLVED`, `NOT_APPLICABLE`, and `REFUSED`.

There is no averaging of validity, but unrelated gates are not allowed to suppress a narrower claim they are not logically required to support.

---

## A.6 Independence is pathway-specific

Independence should be evaluated against the circularity pathway relevant to the claim. Where useful, record data, cohort/system, outcome, parameter/tuning, method, Atlas, source/literature, and temporal independence separately.

The controlling question is:

> **Could the shared information on this pathway force the agreement being presented as evidence?**

If yes, the relevant independence claim is weakened or refused. Shared non-decisive context does not automatically invalidate otherwise independent decisive evidence.

This clarifies, but does not weaken, MFR-10 or Atlas-independence rules.

---

## A.7 Scope is earned; universality is not a target

The program does not use `UNIVERSAL` as a target designation.

Scope is earned by surviving distinct systems, regimes, perturbations, estimators, domains, ordinary regions, and limit testbeds.

Preferred language includes `SUPPORTED_IN_TESTED_REGIME`, `CROSS_REGIME`, `CROSS_SYSTEM`, `CROSS_DOMAIN`, `ROBUST_ACROSS_TESTED_LIMITS`, `DOMAIN_LIMITED`, `REGIME_LIMITED`, and `UNRESOLVED_BEYOND_TESTED_RANGE`.

No finite collection of successful tests is relabeled universal by protocol. Scope may continue to expand through replication, new domains, natural limits, and peer review without a predetermined endpoint.

---

## A.8 Standard-output extension

Where applicable, mature tools should expose both:

**Function-map output:** supported operating regime, response surfaces/trajectories, supported coupling/mechanism relationships, uncertainty, and identifiability across that regime.

**Limit-map output:** transition/degradation/refusal/failure region, rare-natural-testbed outcomes, whether the limit is physical, inferential, estimator-related, or unresolved, and the evidence/independence class of each limit test.

A tool should distinguish:

`WORKS_HERE`

`STOPS_WORKING_HERE`

`NOT_KNOWN_HERE`

---

## A.9 Milestone balance check

At each major milestone or audit, ask:

1. **Have we learned how the system behaves where the representation works?**
2. **Have we meaningfully challenged where that behavior or representation stops working?**

If work has become failure-dominated, the next P0 step should prioritize function/mechanism mapping unless boundary-only study is scientifically justified.

If work has become success-dominated, the next qualification/confirmatory step should prioritize adversarial, transition, refusal, or limit testing where feasible.

The goal is balanced scientific coverage, not an equal number of positive and negative results.

---

# EFFECT ON EXISTING PROJECTS

This addendum applies prospectively to future protocol decisions. It does not retroactively change the epistemic status of any existing GRI, Barrier Atlas, NSD, ChemSA, Substrate Inheritance, or chi-architecture result.

Existing prospective failures remain failures. Existing post-result discoveries remain post-result discoveries. Already-viewed rare/extreme cases remain discovery or qualification evidence unless separately tested under an untouched confirmatory design.

Future audits should check for both failure-seeking bias and success-seeking bias and restore balance at the appropriate research stage without changing frozen outcomes.

---

# CORE SUMMARY

`MAP HOW IT WORKS + MAP WHERE IT STOPS WORKING`

and, where nature provides qualified extremes:

`ORDINARY REGIME + RARE NATURAL LIMIT TESTBED`

Rigor remains hardest at the claim boundary. Exploration and qualification remain free enough to discover what deserves to be tested there.
