# F-16 GVT Interface-to-System Architecture P0-Q Protocol v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** FROZEN BEFORE RAW NUMERIC SIGNAL SCORING
**Evidence class:** PUBLIC EXTERNAL MEASURED / P0-Q
**P1 eligibility:** NO
**Architecture evidence role:** eligible for ARCHITECTURE_SUPPORTING_NATIVE
**Novelty ceiling:** no new F-16 mechanism; no empirical Stability Inheritance claim

## Native benchmark facts fixed before scoring

The benchmark paper reports:

- sampling frequency: 400 Hz;
- three acceleration outputs, ordered as:
  1. excitation location,
  2. right wing next to the nonlinear payload interface,
  3. payload next to the same interface;
- the right-wing/payload mounting interface is the primary expected source of nonlinear distortions;
- a wing-torsion mode near 7.3 Hz carries substantial nonlinear distortion;
- full-grid multisine data span 2-15 Hz;
- each full-grid level contains 9 periods of 8192 samples;
- period 1 contains transients;
- level 1 is the low-amplitude approximately linear reference;
- levels 3, 5, 7 are designated nonlinear estimation levels;
- levels 2, 4, 6 are their corresponding test levels.

Published force RMS levels for the full-grid multisine data:

| Level | Force RMS N | Role |
|---|---:|---|
| 1 | 12.4 | low-amplitude estimation/reference |
| 2 | 24.6 | held-out test |
| 3 | 36.8 | estimation |
| 4 | 61.4 | held-out test |
| 5 | 73.6 | estimation |
| 6 | 85.7 | held-out test |
| 7 | 97.8 | estimation |

These roles and the 7.3 Hz mode location are taken from the benchmark description, not selected from the raw outcomes.

## Intake dependency

Execution is authorized only after F16_GVT_DATA_INTAKE_v0.1 returns INTAKE_PASS for the official 4TU archive. Any changed source identity/layout stops scoring.

Raw data are reacquired from the official 4TU source at runtime and are never committed or uploaded.

## Frozen data subset

Use only files matching the official FullMSine Level1-Level7 MAT datasets.

Do not use sine-sweep or SpecialOddMSine data in the primary analysis.

For every level:
- reshape the force input and each of the three acceleration outputs into 9 periods x 8192 samples;
- discard period 1;
- use periods 2-9 only;
- use the measured Force signal as input, not generator Voltage.

Any shape mismatch is INVALID_TEST.

## Frozen empirical FRF estimator

For each level and each positive Fourier frequency bin, compute the period-averaged H1-style empirical transfer estimate for each output j:

H_j(f) = sum_p Y_j,p(f) U_p(f)* / sum_p |U_p(f)|^2

using the 8 steady-state periods.

No time-domain model is fit.

## Frozen frequency support

Primary architecture band:
- 6.5 to 8.2 Hz, fixed around the published approximately 7.3 Hz wing-torsion mode.

Secondary full benchmark band:
- 2 to 15 Hz.

Within each band, define numerical excitation support from estimation levels 1,3,5,7 only. Retain bins whose pooled estimation input energy exceeds 1e-12 times the maximum pooled input energy in that band.

The held-out levels 2,4,6 may not affect support selection.

## Frozen representations

For each output and frequency bin:

1. H_1: low-amplitude invariant reference from Level 1.

2. H_amp(F): amplitude-conditioned complex FRF obtained by linear interpolation in published force RMS between the two bracketing estimation levels:
   - Level 2 from Levels 1 and 3;
   - Level 4 from Levels 3 and 5;
   - Level 6 from Levels 5 and 7.

Interpolation is performed separately on the real and imaginary parts of H.

3. H_rel = H_payload - H_wing, using outputs 3 minus 2, as a native measured relative-response proxy across the interface-adjacent measurement locations. It is an acceleration-response difference, not a displacement or force-gap measurement.

## Frozen primary metric

For each held-out test level t in {2,4,6}, over the 6.5-8.2 Hz support and all three outputs, compute normalized complex error:

E(X,t) = sqrt( sum |X - H_t|^2 / sum |H_t|^2 ).

Score:
- E_INVARIANT(t) using H_1;
- E_AMPLITUDE(t) using the frozen bracketing interpolation.

Primary ratios:
- R_t = E_AMPLITUDE(t) / E_INVARIANT(t).

No equivalence margin is invented. Exact numerical ordering is reported descriptively.

## Frozen secondary diagnostics

Without changing the primary disposition, report:

- the same invariant vs amplitude-conditioned errors over 2-15 Hz;
- output-specific errors for excitation-point, wing-side, and payload-side responses;
- H_rel representation distance from Level 1 at estimation and test levels;
- frequency of the largest |H_rel| response within 6.5-8.2 Hz for each level;
- complex representation distance between each estimation-level FRF and H_1;
- whether interface-relative changes are larger than excitation-point changes, descriptively only.

No post-result band shift, modal window change, smoothing choice, or output reordering is allowed.

## Frozen primary dispositions

### AMPLITUDE_CONDITIONED_ARCHITECTURE_SUPPORT

Assign if:
- all three held-out levels have finite valid scores; and
- R_2 < 1, R_4 < 1, and R_6 < 1.

Meaning:
an amplitude-conditioned representation derived only from designated estimation levels transports better than one fixed low-amplitude representation to every reserved level in the declared torsional band.

Evidence role:
ARCHITECTURE_SUPPORTING_NATIVE.

Native explanation:
known excitation-dependent structural dynamics generated by clearance/friction and related interface nonlinearities.

This does not establish SI added value or inheritance.

### MIXED_AMPLITUDE_ARCHITECTURE

Assign if at least one but not all held-out levels has R_t < 1.

Preserve the mixed result. Do not retune interpolation, band, or level pairing.

### LOW_AMPLITUDE_REPRESENTATION_NOT_OUTPERFORMED

Assign if none of the held-out levels has R_t < 1.

This is a valid Limit Map outcome for the declared metric/band.

### INVALID_TEST

Assign for source/layout mismatch, non-finite FRFs, missing levels, incorrect period structure, or insufficient frozen frequency support.

### INDETERMINATE

Reserve for valid finite scores whose ordering cannot be interpreted because the normalization denominator or numerical conditioning is degenerate.

## Architecture interpretation

This test separates evidence role from novelty role.

A positive result would support the larger Stability Architecture case by showing, on a real high-order structure, that a localized interface regime is associated with organized amplitude-dependent changes in measured system response that transport prospectively to reserved excitation levels.

It would remain NATIVE_MODEL_COMPATIBLE and PRIOR_ART_COMPATIBLE. The benchmark itself was designed to study these nonlinearities.

No physical chi is admitted.

The measured multi-output FRFs are native response representations. They are not automatically relabeled capital Chi.

Chi_arc is not automatically assigned from this test alone. The result may support architecture-level organization as a constituent of the broader reconstruction without claiming that the project-specific Chi_arc object has been uniquely identified.

## No-retuning rule

After raw scoring starts, do not change:
- data family;
- force input choice;
- period exclusion;
- level roles;
- force RMS coordinates;
- 6.5-8.2 Hz primary band;
- interpolation rule;
- primary metric;
- output order;
- primary disposition rule.

Any alternative becomes a new post-result P0-Q protocol.
