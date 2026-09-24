# D02F Candidate Selection Freeze v0.1

**Date:** 2026-09-24  
**Status:** FROZEN_BEFORE_CANDIDATE_OUTCOME_INSPECTION  
**Authority:** SymC General Operations Manual v0.8.6  
**Target:** CA-D007, ARCHITECTURE_REORGANIZATION_CAN_PRECEDE_SCALAR_TRANSFORMATION  
**Parent evidence:** D02C prospective null; D02D prospective indeterminate; D02E prospective indeterminate.

## Purpose

Select the next prospective CA-D007 system only if it directly resolves the measured D02E failure:

`BASELINE-LICENSED SCALAR != PERTURBATION-ROBUST SCALAR ADMISSION`.

Candidate selection is based on measurement architecture, data completeness, and native intervention power. It may not use the desired relative scalar-versus-organization onset.

## Required eligibility axes

A candidate is eligible only if all axes are verified before decisive ordering inspection.

### 1. Graded intervention

At least three ordered intervention levels beyond or including baseline must be available under a physically interpretable control variable.

Preferred:
baseline + at least three nonbaseline levels.

Minimum:
baseline + two nonbaseline levels if the source supplies dense continuous/parametric measurements spanning at least three prospectively definable bins.

### 2. Perturbation-robust local scalar

The local stability scalar must have a source-native measurement route available at every required intervention level.

Preferred routes, in order:
1. source-reported damping ratio;
2. source-reported Q;
3. source-reported linewidth/decay rate paired with frequency under the same condition;
4. a prospectively validated estimator shown from source methods/schema to remain defined across the full intervention range.

A scalar is not eligible merely because it is estimable at baseline.

Single-mode half-power damping is ineligible unless the source itself demonstrates trackability/admission across every required perturbation level before D02F selection.

### 3. Independent organization observable

A carrier, mode-composition, eigenvector, spatial mode-shape, coupling fraction, network/subspace, or equivalent organization observable must be independently measurable at every intervention level.

It must not be algebraically identical to the scalar.

### 4. Pre-verifiable completeness

Before candidate promotion, source metadata/schema/methods must demonstrate enough observations at every graded level to meet the planned completeness floor.

No environmental or operational matching rule may be introduced after selection merely to rescue incompleteness.

### 5. Native intervention power

Independent source/method evidence must establish that the intervention range measurably affects at least one of the two frozen observables or the native system response.

This requirement exists to avoid another D02C-style powerless test.

The source must not reveal the relative scalar-versus-organization onset used by CA-D007.

### 6. Relative onset remains unseen

Candidate screening may inspect:
- methods;
- schemas;
- metadata;
- variable names;
- file counts;
- intervention schedules;
- generic statements that the intervention affects the system;
- existence of scalar and organization measurements.

Candidate screening may not inspect:
- the graded scalar trajectory;
- the graded organization trajectory;
- the first level at which either changes;
- any analysis that already ranks their relative onset.

If unavoidable public text directly exposes the relative onset, the candidate is contaminated and cannot serve as D02F P1 evidence.

### 7. Automated public reproduction

Raw or processed machine-readable data must be publicly fetchable through stable DOI/repository/API/HTTPS routes.

The target reviewer interface remains:

`python chi_architecture/reproduce.py d02f`.

No manual digitization or manual file selection is allowed.

### 8. Strong native comparator

The domain must provide a native analysis capable of explaining the scalar, organization, and intervention response without SymC terminology.

If sufficient, the verdict remains:

`NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE`.

## Ranking

Among eligible candidates, rank by:

1. directness and perturbation robustness of scalar measurement;
2. independence and completeness of organization measurement;
3. completeness across graded levels;
4. automated public access;
5. intervention power established without revealing relative onset;
6. native comparator strength;
7. simplicity of one-command reproduction.

Do not rank by:
- apparent organization-first behavior;
- closeness to chi=1;
- exceptional-point proximity;
- effect magnitude after outcome inspection;
- narrative fit to D02B.

## Predeclared selection outcomes

The selection process must return one of:

- `D02F_CANDIDATE_SELECTED`;
- `NO_ELIGIBLE_D02F_SYSTEM`.

No eligibility criterion may be relaxed because a candidate is scientifically attractive.

## Search domains

The screen may include, without preference:

- structural/modal dynamics with source-reported modal damping;
- optomechanical or electromechanical coupled modes with linewidth/Q and mode composition;
- cavity-magnon / polariton / hybrid-mode systems with condition-resolved linewidth and participation;
- acoustic or photonic resonators with graded coupling/detuning and direct Q/linewidth;
- other physical systems satisfying the same measurement conditions.

The search domain is broad because the target is a cross-level ordering hypothesis, not a structural-engineering-specific effect.

## Promotion consequence

D02F cannot support CA-D007 unless:
- the selected candidate satisfies every eligibility axis before decisive outcome inspection;
- a full MFR-14 is frozen;
- the decisive run is archived before interpretation.

If no eligible system is found, preserve `NO_ELIGIBLE_D02F_SYSTEM` rather than weakening the gate.
