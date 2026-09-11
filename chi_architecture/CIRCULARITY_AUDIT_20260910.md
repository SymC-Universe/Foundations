# Circularity Audit: Chi Architecture P0

**Date:** 10 September 2026  
**Branch:** `chi-architecture-p0`  
**Status:** P0 EXPLORATORY / FIRST CIRCULARITY HARDENING COMPLETE  
**Authority:** General Cross-Project Research Protocol v0.7.1

## Purpose

This audit asks whether the current synthetic parameters, labels, and experiments could manufacture support for the hypotheses they are intended to investigate.

The answer is: **the v0.1 battery was appropriate as known-truth implementation qualification, but several features would become circular if treated as scientific evidence.** Those features are explicitly bounded and corrected in v0.2.

## Findings and corrections

### C1. Hard-coded result-state labels

The v0.1 runner wrote interpretive labels such as `COUPLING_SPECIFIC_SYSTEM_RESPONSE` and `COMPENSATION_REQUIRES_COUPLING_SPECIFICITY` directly into the result record.

Those were design annotations, not inferred conclusions. Reusing them as evidence would be circular.

**Correction completed:** v0.2 F0-F6 outputs contain raw/native measured quantities and no prewritten architecture-success state. Scientific interpretation must be performed under a separate versioned evaluation rule.

### C2. F4 parameters were chosen around the known Hurwitz boundary

The F4 feedback cases were deliberately selected so that `k*h` falls below, above, and across the exact stability condition `k*h > 0.3`.

This is valid for code qualification. It cannot independently demonstrate compensatory discordance because the qualitative behavior was analytically encoded in the fixture.

**Correction completed:** F4 is now `feedback_stability_control` with role `DESIGNED_FIXTURE_NOT_COMPENSATION_EVIDENCE`.

### C3. F1/F6 parameter implementation drift

The v0.1 plan specified F6 `k = [0,2,4,8,12]`, while the implementation reused the F1 list and produced `k = [0,1,4,8,12]`.

This was not circularity by itself, but duplicated hidden parameter lists allowed plan/code drift.

**Correction completed:** v0.2 makes the JSON experiment plan the single source of runner parameters. CI verifies plan/output agreement. F6 now executes exactly `[0,2,4,8,12]`.

### C4. Noise-entry fixture was too trivial

The v0.1 noise test began at the exact zero state. Observer-only noise therefore altered observation while the unforced physical state remained identically zero.

That verified the path distinction but made the example unnecessarily easy.

**Correction completed:** v0.2 uses a nonzero initial perturbation, an explicit `NO_NOISE` physical control, four fixed seeds, and all-seed retention. Observer-only noise must preserve the no-noise physical trajectory while process and feedback/sensor noise enter the physical state.

### C5. The chi=1 fixture was overly privileged

The v0.1 positive second-order case used exactly `gamma=2`, `kappa=1`, producing `chi=1` and zero discriminant.

That is a valid canonical boundary test but was too narrow for an admission fixture.

**Correction completed:** v0.2 includes underdamped, critical, overdamped, undamped, active-antidamping, anti-restoring, and single-pole cases. Scalar admission is governed by the native model, not proximity to unity.

### C6. Negative damping was not refused by the damping-ratio helper

The v0.1 helper required positive `kappa` but did not reject negative `gamma`. Negative `gamma` is active antidamping, not the passive dissipative construction being licensed here.

**Correction completed:** negative `gamma` now returns `NO_ADMISSIBLE_CHI` for this passive damping-ratio construction. A future active-system scalar would require its own derivation and admission rule.

### C7. Designed fixtures cannot be their own confirmation set

F0-F8 were selected because their native mathematics are known and because they exercise specific method branches. Therefore successful recovery is method qualification, not evidence that a generalized chi architecture exists.

**Correction completed:** v0.2 explicitly distinguishes `DESIGNED_FIXTURE` from any future `EVALUATIVE_EXPERIMENT`. F0-F8 cannot supply untouched confirmation, P1 credit, or program-level `ADDS`.

## Circularity firewall for future experiments

A future evaluative test must satisfy all of the following before its decisive outcome is opened:

1. **Independent target:** stability, recovery, prediction, or failure outcome is defined independently of the S/M/C/R quantities claimed to explain it.
2. **Parameter provenance:** ranges arise from native mathematics, physical bounds, or a frozen sampling rule, not from favorable observed outcomes.
3. **Single source of truth:** executable code reads the frozen parameter plan rather than hidden duplicate values.
4. **No outcome-derived chi:** a scalar cannot earn the name chi because it was optimized against an already-viewed architecture or target.
5. **No fixture promotion:** behavior intentionally built into a qualification fixture cannot confirm the corresponding general hypothesis.
6. **Native comparator first:** the strongest established method for the declared task is fixed before decisive comparison.
7. **Untouched evidence:** discovery/calibration evidence is separated from future decisive holdout evidence.
8. **Explicit negative result:** at least one predeclared outcome must count against the hypothesis and cannot be redescribed as support.
9. **No rescue by redefinition:** changing a metric, mapping, component, threshold, parameter range, or interpretation after viewing a result creates a new version and preserves the prior result.
10. **All declared cases retained:** no seed, parameter point, generator, or domain is dropped because it weakens the pattern.

## Current validated state

`P0_EXPERIMENT_PLAN_v0.2.json` governs future P0 fixture execution. The v0.1 plan and artifacts remain preserved as historical method-development provenance.

GitHub Actions run `34534809484` passed on head `3d0626e8a8d4895fbcca68108caad09298d61b95` after the README/status synchronization.

The validated v0.2 machinery includes:

- plan-driven parameters;
- no hard-coded scientific state labels in F0-F6;
- plan/output parameter synchronization guards;
- nontrivial no-noise versus process/sensor/observer noise controls;
- expanded scalar admission/refusal coverage;
- refusal of negative-gamma passive damping chi;
- 23/23 known-truth, synchronization, and demonstrated-failing tests;
- explicit evidence-class guards;
- source/result hashing and artifact preservation.

Artifact: `chi-architecture-p0-known-truth-v02`  
Artifact ID: `10174963106`  
Artifact SHA-256: `31f13d2a5ea722915a674b4adae7a12582aca2d6eb2f02d0a0b876afa44c0f78`

This remains **method qualification only**. It does not establish generalized chi architecture, compensatory discordance, biological chi, cross-regime transportability, or added value over native analysis.

## Current next step

The next scientific task is **not** to mine F0-F8 for confirmation. They are already-viewed designed fixtures.

The next task is to design the first separate evaluative synthetic experiment with:

- an independently defined outcome;
- parameter-generation rules fixed before outcome inspection;
- architecture measurements fixed before decisive evaluation;
- a strongest native comparator;
- explicit null/negative cases;
- discovery/calibration versus untouched-evaluation separation;
- and a result that is allowed to count against the architecture.

Only after that design is frozen at the appropriate maturity level should its decisive outputs be opened.
