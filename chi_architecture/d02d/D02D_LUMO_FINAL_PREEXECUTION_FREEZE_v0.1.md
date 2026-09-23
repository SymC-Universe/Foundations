# D02D LUMO Final Preexecution Analysis Freeze v0.1

**Date:** 2026-09-23  
**Status:** FROZEN_BEFORE_ANY_DAMAGED_SCIENTIFIC_ARRAY_VALUE  
**Authority:** SymC GOM v0.8.4  
**Parent MFR:** D02D_LUMO_MFR14_v0.1.md

## Source metadata

Sampling frequency:
1651.6129032258063 Hz.

Record shape:
990600 samples x 22 channels.

Duration:
599.77734375 s.

Acceleration channels:
- X: accel01x through accel09x;
- Y: accel01y through accel09y.

Environmental channel:
temp01.

Strain channels are not used in D02D v0.1.

## Campaign structure

Each decisive ZIP contains:
- five healthy ten-minute MAT records;
- five damaged ten-minute MAT records.

Damage locations:
DAM3, DAM4, DAM6.

Severity levels:
010 and 111.

Each severity is compared only with the five healthy records supplied in the same ZIP. Healthy controls are therefore campaign-paired and are not pooled across different damage campaigns for change thresholds.

## Signal preprocessing

For every record and selected direction:

1. use the nine frozen acceleration channels for that direction;
2. convert no units, because all nine channels share source unit g and spectral/modal comparisons are scale-invariant;
3. remove each channel mean;
4. reject a record if any selected acceleration channel contains non-finite values or if sample count differs from 990600 by more than 1%;
5. retain temp01 only for environmental matching.

## Block structure

Each ten-minute record is divided into three consecutive 199-second analysis blocks.

At Fs=1651.6129032258063 Hz, block length is:

328671 samples.

The final unused tail is ignored symmetrically for healthy and damaged records.

This yields:
- 15 healthy blocks per campaign;
- 15 damaged blocks per campaign.

No block is selected or removed based on modal outcome.

## Frequency-domain decomposition

For each analysis block:

- Hann window;
- nperseg = 32768;
- noverlap = 16384;
- constant detrend;
- one-sided spectral range retained from 0.3 to 10.0 Hz.

For each segment and frequency bin, construct the 9x9 cross-spectral matrix.

At each frequency bin, compute the largest eigenvalue and associated unit-norm eigenvector.

The largest eigenvalue is the FDD singular-value spectrum used for peak and bandwidth estimation.

## Healthy mode-family selection

For each damage location and direction, mode selection uses healthy blocks only from both severity campaigns, 30 healthy blocks total.

1. Normalize each healthy block's largest-eigenvalue spectrum by its own median value over 0.3 to 10 Hz.
2. Form the median normalized healthy spectrum.
3. Identify local maxima with scipy.signal.find_peaks using:
   - prominence >= 5.0 in normalized linear units;
   - minimum separation 0.20 Hz.
4. Starting from the lowest-frequency candidate, test healthy-block trackability:
   - each healthy block must contain a local maximum within +/-0.15 Hz of the candidate;
   - at least 24 of 30 healthy blocks must satisfy this condition.
5. Select the lowest candidate satisfying the 24/30 rule.
6. If no candidate passes, the direction is MODE_FAMILY_NON_IDENTIFIABLE and cannot contribute to a location ordering.

Damage spectra do not participate in mode selection.

## Per-block modal tracking

For the selected family center f_ref:

- search only within +/-0.15 Hz;
- choose the local maximum nearest f_ref;
- require a unique peak;
- if two local maxima inside the window differ in amplitude by less than 10%, return MODAL_OVERLAP_NON_IDENTIFIABLE.

No sequential damage-driven retuning of f_ref is allowed.

## Local scalar chi

For an identifiable block peak:

- use the FDD largest-eigenvalue spectrum;
- half-power threshold = peak PSD / 2;
- find left and right crossings inside the frozen +/-0.15 Hz window;
- linearly interpolate each crossing;
- bandwidth Delta_f = f_right - f_left;
- chi = zeta = Delta_f / (2 f_peak).

Refuse scalar block if:
- either half-power crossing is absent;
- the peak is on a tracking-window boundary;
- modal overlap rule is triggered;
- bandwidth <= 0.

A severity scalar evaluation requires at least 10 valid healthy blocks and at least 10 environmentally matched valid damaged blocks.

## Scalar change threshold

For each campaign/direction:

healthy scalar control envelope:

[min(healthy chi), max(healthy chi)]

over all valid healthy blocks after the same estimator rules.

For the environmentally matched damaged blocks:

- deterministic bootstrap of the median;
- 5000 resamples;
- RNG seed = 20260923 + 100*location_index + 10*severity_index + direction_index;
- 95% percentile interval.

Scalar status is:
- TRANSFORMED only when the full damaged median 95% interval lies outside the healthy scalar envelope;
- UNCHANGED otherwise;
- NON_IDENTIFIABLE if completeness is not met.

This deliberately conservative rule does not use a fitted effect-size threshold.

## Organization coordinate

For each healthy block's selected modal peak, retain the unit-norm principal CSD eigenvector.

Campaign healthy reference:

1. form projector P_i = v_i v_i^H for every valid healthy block;
2. P_ref = mean(P_i);
3. v_ref = principal eigenvector of P_ref.

Block organization dissimilarity:

D_org = 1 - |v_ref^H v|^2.

Healthy organization threshold:

T_org = max(D_org) over valid healthy blocks.

For environmentally matched damaged blocks:

organization status is CHANGED only when the 2.5th percentile of damaged D_org values is strictly greater than T_org.

Otherwise UNCHANGED.

If fewer than 10 matched valid damage blocks remain, status is NON_IDENTIFIABLE.

## Environmental and operational matching firewall

For every block compute:
- median temp01;
- log RMS acceleration across all nine selected directional channels.

For each campaign/direction, define the healthy matching rectangle by the minimum and maximum of each covariate over valid healthy blocks.

A damaged block is environmentally matched only when both:
- its median temp01 lies within the healthy min-max range;
- its log RMS lies within the healthy min-max range.

No extrapolation, regression correction, or tolerance expansion is permitted in v0.1.

At least 10 of 15 damage blocks must remain after matching. Otherwise the severity is NON_IDENTIFIABLE for both scalar and organization.

The raw covariate ranges and retained-block counts are reported.

## Severity ordering per direction

Let scalar_010, org_010, scalar_111, org_111 each be CHANGED/TRANSFORMED, UNCHANGED, or NON_IDENTIFIABLE as appropriate.

If any required severity status is NON_IDENTIFIABLE:
ORDERING_NON_IDENTIFIABLE.

Otherwise:

- org010 CHANGED, scalar010 UNCHANGED, scalar111 TRANSFORMED:
  ORGANIZATION_PRECEDES_SCALAR.
- org010 CHANGED, scalar010 UNCHANGED, scalar111 UNCHANGED:
  ORGANIZATION_ONLY_THROUGH_111.
- scalar010 TRANSFORMED, org010 UNCHANGED, org111 CHANGED:
  SCALAR_PRECEDES_ORGANIZATION.
- scalar010 TRANSFORMED, org010 UNCHANGED, org111 UNCHANGED:
  SCALAR_ONLY_THROUGH_111.
- org010 CHANGED and scalar010 TRANSFORMED:
  SIMULTANEOUS_AT_010.
- org010 UNCHANGED and scalar010 UNCHANGED and org111 CHANGED and scalar111 TRANSFORMED:
  SIMULTANEOUS_AT_111.
- all four severity statuses UNCHANGED:
  NEITHER_CHANGES.
- any remaining logically inconsistent pattern:
  ORDERING_NON_IDENTIFIABLE.

## Location-level ordering

Both X and Y directions are required to be identifiable.

If X and Y return the same ordering class, the location receives that class.

If either direction is ORDERING_NON_IDENTIFIABLE, or if the two directions disagree, the location is ORDERING_NON_IDENTIFIABLE.

No favorable direction may stand in for an inconclusive or opposite direction.

## Program-level adjudication

Use MFR-08 exactly, with the completed SIMULTANEOUS_AT_111 vocabulary.

Supportive location classes:
- ORGANIZATION_PRECEDES_SCALAR
- ORGANIZATION_ONLY_THROUGH_111

Adverse scalar-first class:
- SCALAR_PRECEDES_ORGANIZATION

Simultaneous classes:
- SIMULTANEOUS_AT_010
- SIMULTANEOUS_AT_111

The result is:
- EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST only under the MFR two-of-three support rule with no scalar-first location;
- EMPIRICAL_CLAIM_FALSIFIED under the MFR scalar-first / all-three-adequate no-organization-first rule;
- INDETERMINATE otherwise.

## Native comparator and added-value rule

All reported quantities remain standard FDD/modal-damping/MAC/environmental-control quantities.

Even if CA-D007 survives D02D, the quantitative verdict remains:

NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE

unless a separately frozen incremental-value test is performed.

No new SymC variable is fit or searched in D02D.
