# F-16 GVT SpecialOdd Cross-Excitation Replication Protocol v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** SCIENTIFIC QUESTION / METRICS FROZEN BEFORE SPECIALODD SIGNAL SCORING
**Execution dependency:** F16_GVT_SPECIALODD_LAYOUT_PREFLIGHT_v0.1 must qualify the storage mapping
**Evidence class:** PUBLIC EXTERNAL MEASURED P0-Q
**P1 eligibility:** NO
**Relation to FullMSine:** independent excitation-family replication; not a retuning of the positive FullMSine result

## Frozen native facts

From the benchmark paper:

- SpecialOddMSine excites an odd random frequency grid from 1-60 Hz;
- three force RMS levels are used: 12.2, 49.0, 97.1 N;
- each level has 10 input realizations;
- each realization has 3 periods of 16,384 samples;
- only periods 2 and 3 are steady state;
- nine realizations are designated for estimation and the final realization for testing;
- the same three acceleration outputs retain their published ordering:
  1. excitation location,
  2. wing side of the nonlinear interface,
  3. payload side of the nonlinear interface.

## Frozen question

Does an amplitude-specific empirical response representation estimated from the nine designated estimation realizations generalize to the independent tenth realization more accurately than a single pooled representation across all three amplitudes in the same published wing-torsion band used by the FullMSine test?

This asks whether excitation-regime conditioning survives a different excitation design and independent realization split.

## Frozen data handling

At each amplitude:
- use realizations 1-9 for estimation;
- use realization 10 only for scoring;
- discard period 1;
- use periods 2 and 3;
- use measured Force as input;
- no signal from realization 10 may affect support selection, estimator form, or pooling rule.

If the official archive stores estimation and validation realizations in separate files, map those files to the same frozen 9-estimation / 1-test roles using only filenames and shape identity established by the layout preflight.

## Frozen empirical FRF representation

For each amplitude and each frequency bin, estimate the 3-output empirical complex transfer representation using all estimation realizations and both steady periods:

H_a(f) = sum Y U* / sum |U|^2.

Fit:
- H_12.2
- H_49.0
- H_97.1

Also fit:
- H_pool from all estimation amplitudes combined.

No parametric nonlinear model is fit.

## Frozen frequency support

Primary band:
- 6.5-8.2 Hz.

Secondary band:
- 1-15 Hz, overlapping the FullMSine benchmark bandwidth while remaining inside the SpecialOdd support.

Support is defined from estimation inputs only using pooled input energy > 1e-12 times the maximum estimation input energy within the declared band.

Unexcited/detection lines are not used in the primary FRF score.

## Frozen primary metric

For each held-out realization at amplitude a, calculate normalized complex prediction error over all three outputs in the primary band:

E(M,a) = sqrt(sum |M_a - H_test,a|^2 / sum |H_test,a|^2).

Compare:
- E_SPECIFIC(a): amplitude-specific H_a;
- E_POOLED(a): H_pool;
- E_CROSS_LOW(a), E_CROSS_MID(a), E_CROSS_HIGH(a): other amplitude-specific representations where applicable.

The held-out H_test,a is computed only from realization 10 periods 2-3.

## Frozen primary dispositions

### SPECIALODD_AMPLITUDE_SPECIFIC_REPLICATES

Assign if the amplitude-specific representation has strictly lower primary error than H_pool and both other-amplitude representations at all three amplitudes.

Evidence role:
ARCHITECTURE_SUPPORTING_NATIVE_REPLICATION.

### SPECIALODD_POOLED_SUFFICIENT

Assign if H_pool has strictly lower primary error than all amplitude-specific alternatives at all three amplitudes.

This is a valid Limit Map outcome.

### SPECIALODD_MIXED_TRANSPORT

Assign otherwise when all scores are valid and finite.

Preserve any cross-amplitude winner or nonmonotonic pattern.

### INVALID_TEST

Assign for source/layout mismatch, insufficient estimation-only support, invalid period/realization mapping, or nonfinite representations.

### INDETERMINATE

Reserve for mathematically valid but numerically unresolved ordering.

## Frozen secondary diagnostics

Report without changing the primary disposition:

- same representation ordering over 1-15 Hz;
- per-output errors;
- interface-relative representation H_payload - H_wing at each amplitude;
- distance among H_12.2, H_49.0, H_97.1 in the 6.5-8.2 Hz band;
- held-out interface-relative error;
- estimation/test repeatability within each amplitude where identifiable from the realization structure.

Do not create a new threshold from these diagnostics.

## Architecture and novelty interpretation

A replication would strengthen the evidence that the local interface operating regime conditions realized system response across distinct excitation designs. It would remain native structural-dynamics evidence and not SI novelty.

A mixed or pooled result would narrow the FullMSine finding by showing excitation-family dependence or stronger within-regime variability.

No scalar chi is admitted. Native FRFs are not automatically renamed capital Chi, and Chi_arc is not automatically declared from the result.

## No-retuning rule

After SpecialOdd signal scoring begins, do not change:
- amplitude levels;
- estimation/test realization roles;
- period exclusion;
- force input choice;
- 6.5-8.2 Hz primary band;
- support rule;
- FRF estimator;
- pooled model definition;
- primary metric;
- disposition rule.

Any alternative becomes a new post-result P0-Q protocol.
