# F-16 GVT Cross-Excitation Architecture Transport Protocol v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** FROZEN BEFORE SPECIALODD SIGNAL SCORING
**Evidence class:** PUBLIC EXTERNAL MEASURED P0-Q
**P1 eligibility:** NO
**Relation to prior tests:** independent cross-excitation transport test; does not alter FullMSine or SpecialOdd protocols

## Frozen question

Does the amplitude-conditioned response architecture learned only from the FullMSine estimation levels transport across excitation design to the held-out SpecialOdd validation realizations in the preregistered 6.5-8.2 Hz wing-torsion band?

This is stronger than an within-family fit question because the predictor representation and target come from different excitation families.

## Frozen source roles

FullMSine:
- Level 1 = 12.4 N RMS estimation/reference
- Level 3 = 36.8 N RMS estimation
- Level 5 = 73.6 N RMS estimation
- Level 7 = 97.8 N RMS estimation
- periods 2-9 only

SpecialOdd:
- Level 1 = 12.2 N RMS
- Level 2 = 49.0 N RMS
- Level 3 = 97.1 N RMS
- main files, realizations 1-9 and periods 2-3, may be used only to define excitation-support availability
- Validation files, realization 10 periods 2-3, are the scoring targets

SpecialOdd estimation output values are not used to fit the cross-family predictor.

## Frozen frequency mapping

FullMSine uses N=8192 at 400 Hz.
SpecialOdd uses N=16384 at 400 Hz.

Therefore every FullMSine DFT bin maps exactly to every second SpecialOdd DFT bin.

Primary band:
- 6.5-8.2 Hz.

Define FullMSine support from pooled FullMSine estimation input energy using the already frozen numerical support rule: energy > 1e-12 times the maximum estimation energy in the band.

Define SpecialOdd availability from pooled SpecialOdd ESTIMATION input energy only using the same relative numerical rule.

Primary scoring support is the exact-frequency intersection of:
- FullMSine estimation-supported bins;
- SpecialOdd estimation-supported bins;
- 6.5-8.2 Hz.

Held-out SpecialOdd Validation inputs may not change this support.

If a held-out target lacks finite excitation on the frozen intersection, the test is INVALID_TEST rather than post-result support trimming.

## Frozen cross-family predictors

For each common frequency and all three outputs, construct FullMSine empirical complex FRFs exactly as in the FullMSine v0.1 protocol.

For the SpecialOdd target amplitudes:

### 12.2 N low-amplitude calibration
Use FullMSine Level-1 H at 12.4 N directly. No extrapolation below the FullMSine amplitude range is permitted.

This low-amplitude case is a calibration/transport diagnostic, not part of the primary amplitude-conditioning decision.

### 49.0 N primary target
Interpolate linearly in force RMS, separately in real and imaginary components, between FullMSine Levels 3 and 5:
- 36.8 N
- 73.6 N.

### 97.1 N primary target
Interpolate between FullMSine Levels 5 and 7:
- 73.6 N
- 97.8 N.

Frozen fixed comparator for all targets:
- FullMSine Level-1 H at 12.4 N.

No FullMSine held-out Levels 2/4/6 are used to construct the cross-family predictor.

## Frozen target representation

For each SpecialOdd Validation realization:
- measured Force is input;
- periods 2-3 only;
- compute empirical complex FRF for each of the three outputs;
- score only on the frozen cross-family support.

## Frozen primary metrics

For SpecialOdd 49.0 N and 97.1 N targets:

E_COND(a) = normalized complex error of the FullMSine amplitude-conditioned predictor.

E_FIXED(a) = normalized complex error of the FullMSine Level-1 predictor.

R(a) = E_COND(a) / E_FIXED(a).

Primary decision uses only 49.0 and 97.1 N because 12.2 N is below the FullMSine interpolation range and is therefore a low-amplitude calibration diagnostic.

## Frozen dispositions

### CROSS_EXCITATION_ARCHITECTURE_TRANSPORTS
Assign if valid finite scores exist and:
- R(49.0) < 1; and
- R(97.1) < 1.

Evidence role:
ARCHITECTURE_SUPPORTING_NATIVE_CROSS_EXCITATION.

### CROSS_EXCITATION_MIXED
Assign if exactly one of the two primary targets has R < 1.

### CROSS_EXCITATION_CONDITIONING_NOT_SUPPORTED
Assign if neither primary target has R < 1.

### INVALID_TEST
Assign for source identity/layout failure, insufficient pre-target common support, nonfinite predictor/target representation, or held-out excitation absent on the frozen support.

### INDETERMINATE
Reserve for valid finite but numerically degenerate comparison.

## Frozen secondary diagnostics

Report without changing the primary disposition:
- 12.2 N low-amplitude calibration error;
- per-output cross-family errors;
- same comparison over common 2-15 Hz support;
- interface-relative response errors for H_payload - H_wing;
- comparison with within-SpecialOdd amplitude-specific representation only as a descriptive native ceiling if that independently frozen result is available.

## Interpretation ceiling

A positive result would support transport of an amplitude-conditioned architecture relation across excitation families. It would remain native nonlinear structural-dynamics evidence and would not establish SI novelty or a universal inheritance law.

No physical chi is admitted.
Native FRFs are not automatically renamed capital Chi.
Chi_arc is not automatically identified solely by this test.

## No-retuning rule

After SpecialOdd signal scoring begins, do not change:
- amplitude coordinates;
- FullMSine predictor levels;
- no-extrapolation low-amplitude rule;
- common-frequency mapping;
- primary band;
- estimation-only support intersection;
- primary metric;
- primary target amplitudes;
- disposition rule.
