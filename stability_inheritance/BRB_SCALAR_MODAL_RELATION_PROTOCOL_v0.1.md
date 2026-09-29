# Brake-Reuss Beam Scalar-Modal Relation P0-D Protocol v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Evidence class:** PUBLIC EXTERNAL MEASURED / POST-RESULT P0-D
**Status:** FROZEN BEFORE SCALAR EXTRACTION
**Promotion debt:** YES - the positive BRB modal-geometry result was known before this relation question was frozen
**Parent evidence:** BRB_RINGDOWN_MODAL_GEOMETRY_RESULT_v0.1.md
**Empirical Stability Inheritance claim:** NONE

## Purpose

Test the relation between a locally licensed scalar damping coordinate chi and the already-qualified modal/vector geometry Chi during the same Brake-Reuss Beam slow-mode ringdown.

The objective is not to prove that chi and Chi must agree. The objective is to determine whether the local scalar tracks the measured modal deformation, adds information beyond response amplitude, is redundant with amplitude, or is operationally inadequate.

## Frozen source

Repository:
mattiacenedese/BRBtesting

Commit:
2d42d3a618206da58642674d3287ae34dfc7d5e5

ShakerRingdown.mat:
- Git blob 739048b2b1c71839f773ff1aecf4880fda5d62ed
- SHA-256 a62c551e34cc45257257d4e683cc9406beec2cbc1c7270329658fd9033de2f4a

Native source semantics established before this protocol:
- DIC record is the slow-mode shaker ringdown;
- DIC index 185 is nearest Accelerometer 3;
- approximately 80 Hz is used by the source for the first four slow-mode cycles.

## Frozen local windows

Use the complete SRDdataDIC time interval.

Window duration:
- 0.25 s, corresponding to 20 cycles at the source-declared 80 Hz reference.

Step:
- 0.125 s, 50% overlap.

Window start times are generated chronologically from the first DIC timestamp. No window is shifted based on response outcome.

A final partial window shorter than 0.25 s is not used.

## Frozen reference trace and spatial vectors

Use the same native reference coordinate as the completed modal protocol:

r(t) = 0.5 * [deflection_above(185,t) + deflection_below(185,t)]

with MATLAB index 185 = Python index 184.

At every selected peak form:

v(t) = [deflection_above(:,t); deflection_below(:,t)]

and normalize v by its Euclidean norm.

No spatial smoothing or coordinate selection is allowed except removal of coordinates nonfinite across all windows used for modal geometry.

## Frozen peak extraction

Within each 0.25 s window, detect local maxima of abs(r(t)) with the same source-anchored duplicate exclusion rule used by the parent modal protocol:

minimum peak distance = round(0.4 / (80 * dt)), lower-bounded by 1.

No prominence or response-amplitude threshold is tuned.

A window requires at least 10 detected peaks for scalar/modal estimation.

## Local scalar chi admission

For every eligible window:

1. Let a_k = abs(r(t_k)) at detected peaks.
2. Fit:
   ln(a_k) = c - sigma * t_k
   by ordinary least squares.
3. Record R2 and RMS log-envelope residual as model-adequacy diagnostics.
4. Let Delta_t be the median positive spacing between consecutive absolute peaks.
5. Because absolute-value peaks occur every half cycle:
   omega_d = pi / Delta_t.
6. If sigma is finite and strictly positive, define the local effective underdamped coordinate:
   chi_ring = sigma / sqrt(sigma^2 + omega_d^2).

This equals the local damping ratio under the declared second-order exponentially decaying sinusoid approximation.

If sigma <= 0, omega_d <= 0, fewer than 10 peaks exist, or the calculation is nonfinite, scalar chi is REFUSED for that window.

No R2 threshold is imposed after outcome inspection. R2 and residual structure remain explicit diagnostics, so a numerically defined chi does not imply a globally exact second-order model.

The project admission is therefore:
LOCAL_EFFECTIVE_CHI_ADMITTED_CONDITIONALLY, not universal physical chi.

## Window-level Chi geometry

For every window with at least 10 peaks:

- stack the normalized spatial peak vectors;
- compute SVD;
- retain the leading left singular vector;
- record rank-1 energy fraction.

The final chronological window for which both scalar chi and a finite rank-1 basis are available is frozen as the low-amplitude reference basis after validity filtering. It is selected by time order only, not by modal result.

For each valid window compute:
- principal angle theta to the final valid basis;
- MAC to final valid basis;
- median absolute reference peak amplitude A.

No angle or MAC threshold defines validity.

## Frozen relation metrics

Across all windows with admitted chi and valid Chi basis, report:

1. Spearman rho(chi_ring, theta)
2. Spearman rho(log A, theta)
3. Spearman rho(chi_ring, log A)
4. rank-1 energy fraction distribution
5. chi_ring range
6. theta range
7. R2 and envelope-residual distribution for local scalar fits.

No correlation threshold is interpreted as universal.

## Frozen prospective-within-P0-D prediction comparison

Chronologically split valid windows:

- TRAIN = first two thirds, floor(2N/3)
- TEST = remaining windows

Fit ordinary least-squares models on TRAIN only:

- M0: theta = constant
- M_amp: theta ~ log A
- M_chi: theta ~ chi_ring
- M_both: theta ~ log A + chi_ring

Standardize nonconstant predictors using TRAIN means and standard deviations only.

Report TEST RMSE for all four models.

Exact ordering is descriptive because no independent equivalence margin exists.

## Frozen relation dispositions

### CHI_ADDS_BEYOND_AMPLITUDE_FOR_DECLARED_TASK

Assign if:
- M_chi TEST RMSE < M0 TEST RMSE; and
- M_both TEST RMSE < M_amp TEST RMSE.

Meaning:
the local scalar has prospective descriptive value for modal geometry beyond a constant baseline and adds to response amplitude within this already-seen exploratory dataset.

### CHI_TRACKS_BUT_IS_REDUNDANT_WITH_AMPLITUDE

Assign if:
- M_chi TEST RMSE < M0 TEST RMSE; and
- M_both TEST RMSE >= M_amp TEST RMSE.

Meaning:
chi tracks modal geometry but does not add held-out predictive value beyond amplitude in this task.

### CHI_NOT_OPERATIONALLY_PREDICTIVE_OF_MODAL_GEOMETRY

Assign if:
- M_chi TEST RMSE >= M0 TEST RMSE.

This does not mean chi is mathematically invalid. It means scalar chi does not prospectively predict the declared modal geometry target under this relation test.

### CHI_RELATION_INDETERMINATE

Assign if fewer than 8 valid windows remain, predictor variance is numerically zero, or model fitting is nonfinite.

## Architecture interpretation ceiling

This test can support or refuse a local relation between chi and Chi.

It cannot establish:
- a universal chi-to-Chi mapping;
- a universal Stability Arc equation;
- Chi_arc;
- SI-specific novelty;
- untouched confirmation.

A positive relation remains post-result evidence with promotion debt and would require a fresh independent jointed-system test for promotion.

A negative or redundant result is equally valuable because it supports scalar/modal complementarity rather than forcing scalar compression.

## No-retuning rule

After scalar values are extracted, do not change:
- 0.25 s window;
- 0.125 s step;
- reference coordinate;
- peak detector;
- minimum 10 peaks;
- scalar formula;
- final chronological modal reference;
- relation metrics;
- chronological split;
- predictor set;
- disposition rules.

Any alternative is a new post-result analysis.
