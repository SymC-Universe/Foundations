# Circularity Audit: Chi Architecture P0

**Date:** 10 September 2026  
**Branch:** `chi-architecture-p0`  
**Status:** P0 EXPLORATORY / METHOD HARDENING  
**Authority:** General Cross-Project Research Protocol v0.7.1

## Purpose

This audit asks whether the current synthetic parameters, labels, and experiments could manufacture support for the hypotheses they are intended to investigate.

The answer is: **the v0.1 battery was appropriate as known-truth implementation qualification, but several features would become circular if treated as scientific evidence.** Those features are now explicitly bounded and corrected in v0.2.

## Findings

### C1. Hard-coded result-state labels

`run_f0_f8()` in the v0.1 implementation wrote labels such as `COUPLING_SPECIFIC_SYSTEM_RESPONSE` and `COMPENSATION_REQUIRES_COUPLING_SPECIFICITY` directly into the result record.

Those labels were design annotations, not inferred conclusions. If reused as evidence, that would be circular because the desired interpretation was placed into the output by construction.

**Correction:** v0.2 raw outputs must contain native measured quantities only for F0-F6. Scientific interpretation is separated into a later versioned evaluation rule.

### C2. F4 parameters were chosen around the known Hurwitz boundary

The F4 feedback cases were deliberately chosen so that `k*h` falls below, above, and across the exact stability condition `k*h > 0.3`.

This is excellent for checking whether code recovers known control mathematics. It cannot independently demonstrate compensatory discordance because the stabilizing and destabilizing behavior was analytically encoded in the case selection.

**Correction:** F4 is renamed `feedback_stability_control` and explicitly classified as `DESIGNED_FIXTURE_NOT_COMPENSATION_EVIDENCE`.

### C3. F1/F6 parameter implementation drift

The v0.1 plan specified F6 `k = [0,2,4,8,12]`, but the implementation reused the F1 list and produced `k = [0,1,4,8,12]` for F6.

This is not circularity by itself, but duplicated hidden parameter lists make selective drift possible and weaken provenance.

**Correction:** v0.2 makes the JSON plan the single source of all runner parameters. Hidden duplicate parameter lists are prohibited.

### C4. Noise-entry fixture was too trivial

The v0.1 noise test began at the exact zero state. Observer-only noise therefore produced a noisy observation of a physical trajectory that remained identically zero.

That correctly verified the path distinction, but it made the demonstration unnecessarily trivial and could exaggerate the appearance of separation.

**Correction:** v0.2 adds a nonzero initial perturbation, an explicit `NO_NOISE` physical baseline, and four fixed seeds. Observer-only state trajectories must equal the no-noise physical trajectory while process and feedback/sensor perturbations can alter it. Every seed is retained.

### C5. The chi=1 fixture was overly privileged

The v0.1 positive second-order case used exactly `gamma=2`, `kappa=1`, so `chi=1` and the discriminant vanished.

That is a legitimate canonical boundary check, but using only that positive case risks letting the historical boundary dictate the admission test.

**Correction:** v0.2 includes underdamped, critical, overdamped, undamped, active-antidamping, anti-restoring, and single-pole cases. Chi admission is about the licensed native model, not proximity to one.

### C6. Negative damping was not refused by the damping-ratio helper

The v0.1 `second_order_chi()` required positive `kappa` but did not reject negative `gamma`. Negative `gamma` represents active antidamping rather than the dissipative construction being licensed in this demo.

**Correction:** v0.2 refuses negative `gamma` as a damping-ratio chi unless a separate active-system construction is derived and licensed.

### C7. Designed fixtures cannot be their own confirmation set

F0-F8 were selected because their native mathematics are known and because they exercise specific method branches. Therefore successful recovery is method qualification, not evidence that a generalized chi architecture exists.

**Correction:** v0.2 explicitly separates `DESIGNED_FIXTURE` from any future `EVALUATIVE_EXPERIMENT`. F0-F8 cannot supply untouched confirmation, P1 credit, or portfolio `ADDS`.

## Circularity firewall for future experiments

A future evaluative test must satisfy all of the following before its decisive outcome is opened:

1. **Independent target:** the stability/recovery/prediction outcome is defined independently of the S/M/C/R quantities claimed to explain it.
2. **Parameter provenance:** each parameter range is justified by native mathematics, physical range, or a predeclared sampling rule rather than by observed favorable outcomes.
3. **Single source of truth:** executable code reads the frozen parameter plan rather than maintaining hidden duplicates.
4. **No outcome-derived chi:** a scalar cannot earn the name chi because it was optimized against an already-viewed architecture or target.
5. **No fixture promotion:** behavior intentionally built into a calibration fixture cannot confirm the corresponding general hypothesis.
6. **Native comparator first:** the strongest established method for the task is specified before the decisive comparison.
7. **Untouched evidence:** discovery/calibration evidence is separated from a future holdout or system not used to define the rule.
8. **Explicit negative result:** the plan contains at least one outcome that counts against the hypothesis and cannot be redescribed as support.
9. **No rescue by redefinition:** changing a metric, mapping, component, threshold, parameter range, or interpretation after viewing a result starts a new version and preserves the failed result.
10. **All declared cases retained:** no seed, parameter point, generator, or domain is dropped because it weakens the pattern.

## Consequence for the current evidence record

The existing v0.1 GitHub Actions success remains valid as **mechanical known-truth qualification**. It is not withdrawn and should not be rewritten.

What changes is its scientific ceiling: its deliberately constructed outcomes cannot be cited as confirmation of generalized chi architecture, compensatory discordance, cross-regime transportability, or added value over native analysis.

`P0_EXPERIMENT_PLAN_v0.2.json` governs future P0 runs after this audit.

## Current next step

Update the executable harness so that:

- parameters are loaded directly from v0.2;
- F0-F6 emit raw native metrics without embedded favorable state labels;
- F5 uses the explicit no-noise baseline and all fixed seeds;
- F6 uses the correct declared parameter list;
- F8 exercises the full admission/refusal set;
- CI verifies plan/code agreement and refuses hidden parameter drift.

Only after that mechanical hardening should scientific comparator analysis continue.
