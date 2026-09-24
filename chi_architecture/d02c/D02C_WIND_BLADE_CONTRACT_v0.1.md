# D02C Wind-Blade Prospective Source and Decision Contract v0.1

**Date:** 2026-09-23  
**Status:** FROZEN_BEFORE_DECISIVE_MODAL_DAMPING_OR_SPATIAL_ORGANIZATION_VALUES  
**Authority:** SymC GOM v0.8.3  
**Target hypothesis:** CA-D007, ARCHITECTURE_REORGANIZATION_CAN_PRECEDE_SCALAR_TRANSFORMATION

## Physical system

Full-scale wind-turbine blade in OWI-lab's Large Climate Chamber.

Dataset DOI:
10.5281/zenodo.18427836

Publication DOI:
10.1088/1742-6596/2647/19/192008

The blade is instrumented with three tri-axial accelerometers at distinct spanwise locations.

## Source lock

### Main climate
ClimateChamber_20221115.csv
MD5: 7afea2377fb14ca576516c39201a6aac
SHA-256: 2b9dbad82d851b24ca62862b97a10fbbae242f99252a94a13273fd913e22f3a0

### X-direction OMA
MO04_mpe_X_20221115.csv
MD5: 0a08eb30f4361d3ebfd1a6ecfb4ff332
SHA-256: 7d2716d12db69d0c064ec0e90837152bbb0c7e8d6dab37124303004a3d0cd556

### Z-direction OMA
MO04_mpe_Z_20221115.csv
MD5: 3e1ceb71d0fae2901c9256eb472d021a
SHA-256: 99ba333b9fb1e4f49bf735455783414491df814207cb1ea04204d865173a87f8

### Baseline acceleration block
MO04_acceleration_20221115_000000.zip
MD5: dc1bd7d724264e1a37ffdc58865f6304
SHA-256: 2025b99a4203f2de2d8608188f40eaca425259b452a757f4813e846b0dcad6fa

Contains twelve ten-minute windows:
00:00, 00:10, ..., 01:50 UTC.

### Intervention acceleration block
MO04_acceleration_20221115_130000.zip
MD5: 50e32f0e7e711b89128a895d5c0c9481
SHA-256: 752b184321332d448b0838399a0e685c72cf3fa7092b69d94f16033986f03631

Contains twelve ten-minute windows:
11:20, 11:30, ..., 13:10 UTC.

### Dry-run climate
ClimateChamber_20220927.csv
MD5: aa3dccbefeb1644e5c8cbc030801b146
SHA-256: bf23603685ed9dc4c556b3502be1f5d38b54fd9fdd7f6a40723b0d41411d0cfa

### Dry-run acceleration
MO04_acceleration_20220927.zip
MD5: 83d9f4030346d6a3538627320a03437e
SHA-256: 4526ccac4203f2de2d8608188f40eaca425259b452a757f4813e846b0dcad6fa

Correction: the dry-run SHA-256 above is a transcription placeholder and MUST be replaced by the exact schema artifact value before execution. A checksum mismatch is fail-closed.

## Independent intervention schedule

Published event times, frozen before outcome inspection:

- start cooling: 10:04 UTC;
- start spray: 11:23 UTC;
- accelerate spray: 12:13 UTC;
- end spray: 12:49 UTC;
- start heating: 13:13 UTC.

D02C does not infer ice mass or thickness that was not measured.

The control coordinate is ordered intervention time/stage, with chamber temperature retained as a measured native confounder.

## Baseline and intervention windows

### Baseline

Use all twelve raw ten-minute windows from 00:00 through 01:50 UTC.

No baseline window may be removed due to its eventual scalar or organization value unless the raw file is corrupt or fails a predeclared data-quality guard.

### Intervention

Use all twelve raw ten-minute windows from 11:20 through 13:10 UTC.

The 11:20 window straddles the 11:23 spray onset. It is retained and labeled SPRAY_ONSET_STRADDLING rather than silently treated as pure pre-spray or removed.

Window stages are assigned only from published event times:
- SPRAY_ONSET_STRADDLING;
- SPRAY_INITIAL;
- SPRAY_ACCELERATED;
- POST_SPRAY_PRE_HEATING.

## Mode selection

D02C uses exactly two native low-order targets:

1. lowest stable X-direction modal family in the midnight baseline;
2. lowest stable Z-direction modal family in the midnight baseline.

A baseline family is "stable" if:
- it is identifiable in at least 80% of OMA timestamps that overlap the twelve baseline raw windows;
- its frequency track can be linked between adjacent OMA timestamps by nearest-neighbor continuity without a jump exceeding 10% of the current frequency.

If multiple families satisfy the rule, choose the lowest median frequency.

No intervention value may influence mode selection.

## Local scalar

The source OMA field mean_damping is treated as the native modal damping estimate.

The candidate scalar is:

chi_local = zeta.

If the source stores damping in percent, then:

chi_local = mean_damping / 100.

The unit convention MUST be verified from source/native OMA documentation before numeric execution. If it cannot be verified, return:

NO_ADMISSIBLE_SCALAR_CHI.

Requirements for a scalar point:
- algorithm field is the source LSCF estimator;
- finite positive mean_damping;
- finite nonnegative std_damping;
- cluster size >= 3;
- inferred zeta is in 0 < zeta < 1.

## Scalar timestamp matching

Each ten-minute raw window is represented by its midpoint.

The scalar point is the nearest same-direction OMA estimate to that midpoint within 5 minutes.

If more than one candidate modal row exists, use the row assigned to the frozen baseline-tracked modal family.

If no row is available within 5 minutes, scalar status is NON_IDENTIFIABLE_AT_WINDOW.

## Scalar uncertainty and change threshold

For each direction separately:

1. construct the twelve matched baseline chi estimates;
2. baseline center = median(baseline chi);
3. baseline empirical envelope = [min(baseline lower95), max(baseline upper95)];
4. for each OMA row:
   SE_chi = (std_damping / sqrt(size)) / 100;
   lower95 = chi - 1.96*SE_chi;
   upper95 = chi + 1.96*SE_chi.

A scalar transformation is detected only when the intervention 95% interval lies completely outside the baseline empirical envelope.

This conservative rule is frozen before intervention damping values are read.

If source damping is not percent, the formula must be converted by a source-documented unit relation only; no post-result scaling is allowed.

## Independent organization observable

For each raw window and each selected direction:

1. use the three accelerometer channels corresponding to that physical direction;
2. estimate the 3x3 cross-spectral density matrix with:
   - Hann window;
   - nperseg = 8192 samples;
   - 50% overlap;
   - constant detrend;
   - source sampling rate 250 Hz;
3. evaluate the CSD matrix at the frequency bin nearest the matched frozen modal frequency;
4. take the unit-norm principal eigenvector v of the Hermitian CSD matrix.

The organization coordinate is the complex modal assurance dissimilarity relative to the baseline reference:

D_org = 1 - |v_ref^H v|^2.

The global phase of v is irrelevant.

## Baseline organization reference

For each direction:
- obtain one principal vector for each of the twelve midnight baseline raw windows;
- form projectors P_i = v_i v_i^H;
- reference projector P_ref is the principal rank-one eigenspace of mean(P_i);
- use its unit vector v_ref for MAC calculations.

## Organization uncertainty and change threshold

Each ten-minute raw window is split into twelve non-overlapping 50-second blocks.

For each block, compute the principal mode vector at the tracked modal frequency using the same spectral settings where segment length permits; if necessary, nperseg is capped at the block length without changing the Hann/50%-overlap rule.

Baseline organization threshold for each direction:

T_org = max D_org across all valid 50-second blocks from all twelve baseline windows.

For each intervention window:
- compute the twelve block-level D_org values;
- organization is changed only if the 2.5th percentile of its block-level D_org values is strictly greater than T_org.

This deliberately conservative rule requires the full intervention-window distribution to exceed every observed baseline-block dissimilarity.

## Ordering test

For each of the two selected directions independently, evaluate only the twelve intervention windows on their common 10-minute grid.

Define:
- t_org = earliest intervention window whose organization criterion is CHANGED;
- t_chi = earliest intervention window whose scalar criterion is TRANSFORMED.

Classify:

- ORGANIZATION_PRECEDES_SCALAR if t_org < t_chi;
- SCALAR_PRECEDES_ORGANIZATION if t_chi < t_org;
- SIMULTANEOUS_WITHIN_FROZEN_RESOLUTION if t_org == t_chi;
- ORGANIZATION_CHANGES_SCALAR_DOES_NOT if t_org exists and t_chi does not;
- SCALAR_CHANGES_ORGANIZATION_DOES_NOT if t_chi exists and t_org does not;
- NEITHER_CHANGES if neither exists;
- ORDERING_NON_IDENTIFIABLE if too many required windows are missing/refused;
- NO_ADMISSIBLE_SCALAR_CHI if scalar convention/admission fails;
- NATIVE_MEASUREMENT_SENSITIVITY_PRECLUDES_ORDERING if the native sensitivity analysis below shows unequal detection limits can account for the apparent order.

No interpolation between ten-minute windows is allowed.

## Temperature / environmental confounder firewall

Natural-frequency temperature sensitivity is known prior context and is not evidence for CA-D007.

For each intervention window, chamber temperature is summarized over the same ten-minute period.

D02C must report:
- temperature trajectory;
- scalar chi trajectory;
- organization trajectory.

A favorable ordering is NOT promoted if either of the following holds:
- organization change is reproduced at comparable temperature excursions in the non-icing dry-run control;
- the scalar/organization ordering disappears when intervention windows are compared only to baseline/dry-run observations with overlapping temperature ranges.

Because the dry-run does not contain the source OMA damping table, it is primarily a negative control for organization and spectral geometry, not a substitute scalar dataset.

## Native comparator

The strongest native comparator is:
- automated Operational Modal Analysis / LSCF damping and frequency tracking;
- cross-spectral spatial mode-vector analysis;
- environmental and operational variability / temperature compensation;
- standard vibration-based icing-detection interpretation.

If these native tools fully describe the observed ordering, the added-value verdict is:

NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE.

No new SymC variable is pre-authorized.

## CA-D007 decision logic

A D02C result supports the domain-specific ordering pattern only if:
- at least one direction is ORGANIZATION_PRECEDES_SCALAR or ORGANIZATION_CHANGES_SCALAR_DOES_NOT;
- the organization change survives the dry-run/temperature firewall;
- the other direction does not show a clean opposite SCALAR_PRECEDES_ORGANIZATION result under comparable data quality.

A clean scalar-first result counts against CA-D007 in this system.

Simultaneous, neither, non-identifiable, or sensitivity-precluded outcomes do not count as support.

## Evidence ceiling

D02C is the first prospectively frozen external physical test of CA-D007 under this program.

Regardless of outcome, it remains a domain-specific physical result. It cannot establish universality or a master scalar.
