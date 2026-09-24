# D02C Wind-Blade Exact Mapping and Thermal Firewall v0.1

**Date:** 2026-09-23  
**Status:** FROZEN_BEFORE_DECISIVE_NUMERIC_EXECUTION  
**Authority:** SymC GOM v0.8.3  
**Parent contract:** D02C_WIND_BLADE_CONTRACT_v0.1.md

## Raw column lock

Intervention raw header:

- time
- ACC2_X
- ACC2_Y
- ACC2_Z
- ACC3_X
- ACC3_Y
- ACC3_Z
- ACC4_X
- ACC4_Y
- ACC4_Z

Edgewise organization channels:

ACC2_X, ACC3_X, ACC4_X

Flapwise organization channels:

ACC2_Z, ACC3_Z, ACC4_Z

Y channels are excluded from D02C.

## Sampling

Source sampling frequency:

250 Hz.

Each ten-minute main-test raw file is expected to contain approximately 150,000 samples.

Files with less than 95% or more than 105% of the expected sample count are refused as RAW_WINDOW_LENGTH_INVALID.

## Modal scalar convention

OWI-lab LSCF damping is reported in percent.

Therefore:

chi = zeta = mean_damping / 100.

Per-row precision:

SE_chi = (std_damping / sqrt(size)) / 100.

95% interval:

chi +/- 1.96 SE_chi.

## Baseline mode-track construction

Use the twelve main-test baseline raw-window midpoints:

00:05, 00:15, ..., 01:55 UTC.

For each direction separately:

1. collect all admissible LSCF modal rows at each midpoint within +/-5 minutes;
2. initialize candidate tracks from the first midpoint;
3. extend each track by nearest-frequency matching at each subsequent midpoint;
4. a match is allowed only when relative frequency jump <=10%;
5. no row may be used by two tracks at the same timestamp; nearest match receives it;
6. retain tracks present at >=10 of 12 midpoint times;
7. select the retained track with the lowest median frequency.

This track is frozen before intervention matching.

## Intervention tracking

At each intervention midpoint:

11:25, 11:35, ..., 13:15 UTC.

Use the nearest OMA timestamp within 5 minutes.

Within that timestamp, select the admissible row nearest the previously matched family frequency, requiring relative jump <=10%.

If no row meets the rule:

NON_IDENTIFIABLE_AT_WINDOW.

Tracking is sequential and may not jump to a different family to rescue a missing point.

## Scalar thermal-control envelope

The decisive scalar threshold is deliberately more conservative than the parent contract.

For each selected direction/mode:

1. build the baseline envelope from the twelve midnight matched estimates;
2. independently track the same modal family through all admissible OMA timestamps from 00:00 UTC up to but not after 11:20 UTC, before the published spray start at 11:23;
3. calculate each row's 95% chi interval;
4. define the no-change scalar envelope as:

lower_chi_control = minimum lower95 over all admissible pre-spray rows;
upper_chi_control = maximum upper95 over all admissible pre-spray rows.

An intervention scalar point is TRANSFORMED only if its entire 95% interval lies outside this full pre-spray control envelope.

This controls for temperature and other pre-spray environmental variation without fitting a post-result temperature model.

## Main organization estimator

For each main-test ten-minute raw window and selected direction:

- channels: frozen three-sensor set above;
- detrend: constant;
- spectral window: Hann;
- scipy.signal.csd;
- nperseg=8192;
- noverlap=4096;
- scaling=density;
- evaluate at frequency bin nearest the same-window matched OMA frequency.

Construct the 3x3 Hermitian CSD matrix and take its largest-eigenvalue eigenvector.

Normalize vector to Euclidean norm 1.

Organization dissimilarity:

D_org = 1 - |v_ref^H v|^2.

## Main baseline organization reference

Compute one full-window mode vector from each of the twelve midnight windows.

For each vector v_i form projector P_i=v_i v_i^H.

P_ref = mean(P_i).

v_ref is the principal eigenvector of P_ref.

## Block uncertainty

Split each ten-minute main window into twelve consecutive 50-second blocks of 12,500 samples.

For each block:
- nperseg=8192;
- noverlap=4096;
- same target modal frequency;
- same CSD/eigenvector algorithm.

A block is invalid only for non-finite data or insufficient samples.

## Midnight baseline organization threshold

Compute block-level D_org for every valid 50-second block from all twelve midnight windows relative to v_ref.

T_org_midnight = maximum baseline block D_org.

## Dry-run thermal organization threshold

The September dry-run raw file is treated only as a thermal/no-icing organization sensitivity control.

1. Verify 250 Hz sampling and at least 120 minutes of valid data.
2. Divide the first 120 minutes into twelve consecutive ten-minute windows.
3. For each direction, select the lowest stable modal spectral peak using only the dry-run initial two windows and the same spatial CSD principal-vector construction.
4. Build a dry-run reference projector from the first two dry-run windows.
5. Compute ten-minute and 50-second block mode vectors for all twelve dry-run windows.
6. D_dry is computed relative to the dry-run reference, never relative to the November baseline, because the support setup may have changed between experiments.
7. T_org_dry = maximum valid dry-run block D_dry.

The effective organization no-change threshold is:

T_org = max(T_org_midnight, T_org_dry).

This is deliberately conservative.

## Dry-run peak selection

Within each direction:

- calculate the spatially averaged PSD of the three frozen channels for the first two dry-run windows;
- consider frequencies 0.5 to 4.0 Hz;
- require a local peak to be present in both windows within +/-0.1 Hz;
- choose the lowest such common peak.

No November outcome may influence this selection.

## Organization change criterion

For each intervention window:

- compute twelve block-level D_org values;
- require at least 10 valid blocks;
- CHANGED only if the 2.5th percentile of block-level D_org is strictly greater than T_org.

Otherwise UNCHANGED.

## Intervention stage labels

Using raw-window start time:

- 11:20 = SPRAY_ONSET_STRADDLING;
- 11:30 through 12:10 = SPRAY_INITIAL;
- 12:20 through 12:40 = SPRAY_ACCELERATED;
- 12:50 through 13:10 = POST_SPRAY_PRE_HEATING.

These labels are descriptive and do not alter the onset rule.

## Ordering outcome

For each direction independently:

- t_org = earliest window with organization CHANGED;
- t_chi = earliest window with scalar TRANSFORMED.

Use the outcome categories frozen in D02C_CANDIDATE_SELECTION_FREEZE_v0.1.md and D02C_WIND_BLADE_CONTRACT_v0.1.md.

No interpolation below ten-minute resolution.

## Measurement-sensitivity firewall

Before assigning ORGANIZATION_PRECEDES_SCALAR:

- report T_org_midnight and T_org_dry;
- report scalar pre-spray control envelope;
- report intervention scalar CI widths and organization block spread;
- if organization onset disappears when T_org_dry is applied, classify NATIVE_MEASUREMENT_SENSITIVITY_PRECLUDES_ORDERING rather than organization-first.

## Checksum correction

The exact dry-run raw SHA-256 from the pre-result schema lock is:

4526ccac42059ea194aa6abe984a3e74aa8945dd106390094c3aa86eaf12f75f

This replaces the parent contract's wording that called the same value a transcription placeholder.

No source bytes changed.
