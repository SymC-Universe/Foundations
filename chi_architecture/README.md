# Chi Architecture Investigation

**Status:** P0 EXPLORATORY / POST-RESULT HYPOTHESIS GENERATION  
**Branch:** `chi-architecture-p0`  
**Authority:** General Cross-Project Research Protocol v0.7.1, Final Baseline, 10 September 2026  
**Claim ceiling:** exploratory only  
**Confirmatory MFR-14:** not yet activated  
**Predictive tool status:** not a tool; no independent atlas; no prospective validation

## Current scientific question

Does stability across materially different native regimes admit a useful architecture that can be progressively reconstructed from independently interpretable scalar, vector/modal, and conglomerate/system starting representations, together with their coupling, feedback, disagreement, inheritance, emergence, and any additional structure that earns admission?

This workstream does **not** assume that the three current starting representations are a complete decomposition of chi, a universal ontology, or a literal formula for chi.

## Scope discipline

Universality is **not** a research target or promotion criterion.

The architecture is being investigated because it may be unusually broad across otherwise different systems and regimes. Its scope must be earned one regime, mechanism, and untouched test at a time. A result that works in several domains remains a bounded cross-regime result unless additional evidence extends that boundary.

If the architecture ultimately proves extremely broad, that conclusion must emerge from continued successful testing, failures, domain limits, mathematical development, independent replication, and peer review rather than from a prior universal claim.

`BROAD != UNIVERSAL`

A scientifically valuable outcome may therefore be any of the following:

- broad cross-regime architecture;
- domain-family architecture;
- regime-specific architecture;
- partial transportability of selected components;
- or failure of the proposed architecture outside a narrow class.

None is treated as a continuity failure.

## Historical interpretation of the scalar-first investigation

The program should not be read as having started from the belief that a scalar chi was the fundamental object.

The earlier conceptual premise was that systems are shaped not only by their isolated properties but by pressure, influence, coupling, and feedback from other systems or components, and that a coupled/grouped system can contain scientifically important behavior not recoverable from isolated components alone.

The damped oscillator supplied an early mathematically tractable realization in which competing tendencies admit the scalar coordinate

`chi = gamma / (2 omega_0)`.

That success motivated an extended **scalar-first investigation** because the scalar was measurable, compact, and analytically useful. It did not establish that the scalar was ontologically primary.

The present investigation therefore records the historical progression as:

`systems/feedback/coupling premise -> tractable scalar probe -> scalar-first testing -> evidence that scalar alone is insufficient -> modal/carrier and conglomerate/system structure -> progressive architecture reconstruction`

The current result is not that a once-fundamental scalar has been replaced. It is that the program tested the scalar as though it might carry the deeper structure and has accumulated reasons to conclude that scalar-only description is not generally sufficient.

Documentary provenance for the earliest pre-mathematical formulation should be added separately if the original paper or dated record is recovered. Such provenance would establish hypothesis history, not empirical correctness.

## Current starting basis

Where native science supports them, inspect:

- **scalar:** compressed stability coordinates, invariants, rates, ratios, spectra, or other defensibly derived scalar summaries;
- **vector/modal:** resolved carrier structure such as eigenvectors, invariant subspaces, projectors, participation structure, latent modes, or other domain-native multidimensional objects;
- **conglomerate/system:** organization created by coupling, feedback, networks, subsystem interaction, memory, environmental structure, cross-layer mappings, or collective behavior.

The scientifically important target is increasingly the relationship among these representations and any higher-order architecture that survives falsification.

## Chi naming rule

An object is not called chi merely because it is a useful stability quantity.

- `chi = gamma / (2 omega_0)` remains a licensed scalar construction only for a justified passive second-order factor with the required conventions and boundary structure.
- A different regime may generate a different candidate scalar chi only through its own native model, derivation, validity conditions, uncertainty treatment, nulls, and admission rules.
- A scalar chi is not required for an architecture to be scientifically meaningful.
- Any proposed scalar compression must earn its existence by preserving or adding scientifically useful information beyond the richer native representation.
- Modal and conglomerate objects can belong to the stability architecture without being renamed chi.
- A domain may legitimately return `NOT_APPLICABLE` or `NO_ADMISSIBLE_CHI`.

The working architectural hypothesis is therefore not "find a scalar chi everywhere." It is to determine whether a deeper stability architecture can be identified across regimes and, only where justified, whether that architecture admits a useful scalar projection.

## Why this workstream exists now

Three current program observations motivated the investigation but do not confirm it:

1. The published Stability Arc work established a bounded cross-domain role for a licensed damping-ratio construction in the systems studied there.
2. The rebuilt GRI program recovered reproducible static scalar, modal, and cross-layer organization while explicitly withholding a biological chi coordinate. This makes GRI a post-result hypothesis source, not prospective confirmation of generalized chi architecture.
3. The substrate-inheritance program developed independent carrier, coupling, uncertainty, and refusal machinery that may later be reusable, but its SI-next branch remains non-authoritative and is not inherited into this branch as evidence.

## Post-result hypothesis under investigation

A recent observation suggested that scalar/modal disagreement may sometimes coincide with a conglomerate response that preserves system organization. This is currently **only a mechanistic hypothesis**.

The project does not equate disagreement with compensation.

A disagreement can be called compensatory only after a prospectively specified coupling-dependent response predicts an independently measured future or held-out stability outcome. Observation noise, estimation error, destabilizing discordance, redundancy, and ordinary native-domain explanations remain competing explanations.

## Anti-circularity position

The workstream must not follow this invalid chain:

`inspect favorable architecture -> choose a scalar that matches it -> call that scalar chi -> use the match as evidence for chi architecture`

Instead:

`native model -> native observables -> independently defined representations -> explicit relationships/nulls -> exploratory qualification -> frozen evaluative rule -> untouched decisive evidence`

Likewise, the conglomerate cannot mean "whatever combination performs best." It must be a named native mathematical or physical object whose construction is fixed independently of the outcome being used to test it.

### Designed fixtures are not evidence for the hypothesis they encode

F0-F8 are **known-truth designed fixtures**. Their parameters were chosen to exercise specific mathematical and software behaviors. Correct recovery qualifies implementation behavior only.

Therefore:

- F4's analytically selected feedback cases verify the Hurwitz coupling criterion; they do not establish compensatory discordance.
- F1/F6 verify established fixed-spectrum non-normal behavior; they do not establish added architecture value beyond standard non-normal analysis.
- F8 verifies admission/refusal behavior for a licensed second-order scalar; it does not establish cross-regime chi.
- no F0-F8 success counts as empirical confirmation, P1 evidence, or program-level `ADDS`.

`P0_EXPERIMENT_PLAN_v0.2.json` is now the single source of executable fixture parameters. The runner may not maintain hidden duplicate parameter lists.

The complete review is recorded in `CIRCULARITY_AUDIT_20260910.md`.

## P0 known-truth battery

The circularity-hardened v0.2 battery retains F0-F8 and adds stronger execution controls:

- a normal decoupled case where ordinary eigenvalue stability should remain sufficient;
- same-spectrum/different-modal-geometry cases;
- same-modal-basis/different-spectrum cases;
- fixed-local-subsystem/different-coupling cases;
- a feedback stability fixture explicitly barred from compensation inference;
- no-noise, process-noise, feedback/sensor-noise, and observer-only paths using a nonzero initial perturbation and four retained seeds;
- non-normal transient-growth cases using the declared F6 parameter list;
- exact degenerate-subspace refusal;
- underdamped, critical, overdamped, undamped, active-antidamping, anti-restoring, and single-pole chi admission/refusal cases.

F0-F6 emit raw/native measurements rather than prewritten scientific outcome labels. Exact admission/refusal states remain allowed where they are directly generated by the mathematical guard.

### Validation status

The circularity-hardened v0.2 head passed GitHub Actions run `34534717778` at commit `83886a4d14d520a5151751437d02018e8bdaf4f3`.

The validated job included:

- v0.2 anti-circularity experiment-plan guards;
- 23/23 known-truth, plan-synchronization, and demonstrated-failing tests;
- plan-driven raw fixture result generation;
- evidence-class, parameter-synchronization, and refusal guards;
- source/result manifest generation;
- artifact upload.

Artifact: `chi-architecture-p0-known-truth-v02`  
Artifact ID: `10174926702`  
Artifact SHA-256: `2589275e2a032e168ea852d32eaed746e1173b7926d709d2648ba3346a6d2b51`

This validation establishes implementation behavior only. It does not establish generalized chi architecture, empirical added value, compensation in GRI, or cross-domain validity.

## Current status against the General Protocol

See:

- `GENERAL_PROTOCOL_AUDIT_20260910.md`
- `CIRCULARITY_AUDIT_20260910.md`
- `POST_RESULT_DISCOVERY_LEDGER.md`
- `P0_FALSIFIABILITY_CHARTER_v0.1.md`
- `P0_EXPERIMENT_PLAN_v0.1.json` for preserved historical v0.1 provenance
- `P0_EXPERIMENT_PLAN_v0.2.json` for current P0 fixture execution

## Project control

**Current status:** P0 governance, known-truth mechanical qualification, and the first circularity hardening pass are complete; generalized chi architecture remains unconfirmed.  
**Next scientific/computational step:** evaluate the raw F0-F8 fixtures only as method checks against native mathematics, then design the first separate evaluative synthetic experiment whose target, parameter rule, architecture metrics, native comparator, and negative result are frozen before decisive outcomes are opened.  
**What can advance immediately:** native-comparator method checks and design of a non-fixture synthetic evaluation with independent outcome and preserved calibration/holdout separation.  
**User action required:** none. A separate decision will be requested only if a future move would freeze a confirmatory P1 claim, comparator, threshold, or untouched validation target.
