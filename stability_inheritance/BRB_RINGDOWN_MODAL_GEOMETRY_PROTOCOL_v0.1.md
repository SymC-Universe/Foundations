# Brake-Reuss Beam Ringdown Modal-Geometry P0-Q Protocol v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Evidence class:** PUBLIC EXTERNAL MEASURED / KNOWN-TRUTH P0-Q
**Status:** FROZEN BEFORE DIC RESPONSE SCORING
**Source commit:** 2d42d3a618206da58642674d3287ae34dfc7d5e5
**Source file:** ShakerRingdown.mat
**Source SHA-256 from metadata intake:** a62c551e34cc45257257d4e683cc9406beec2cbc1c7270329658fd9033de2f4a
**P1 eligibility:** NO
**Architecture target:** modal/vector representation qualification
**Empirical Stability Inheritance claim:** NONE

## Prior native evidence

The associated Part II paper reports amplitude-dependent mode-shape reconstruction from DIC. Therefore a positive result is known/native architecture evidence, not SI novelty.

The repository's own showData.mlx source, audited before response scoring, declares:

- SRDdataDIC.position
- SRDdataDIC.time
- SRDdataDIC.deflection_above
- SRDdataDIC.deflection_below
- DIC position index 185 as nearest to Accelerometer 3
- DIC data filtered around the slowest vibration mode
- approximately 80 Hz for the first four cycles
- accelerometer after-release display window 30.2 to 34.2 s.

The DIC record itself is treated by the source as shaker-ringdown data.

## Frozen question

Within the DIC-filtered slow-mode ringdown, is one spatial modal vector invariant across response amplitude, or does amplitude-conditioned modal geometry describe held-out spatial response peaks better than a fixed cross-amplitude shape?

This tests modal/vector architecture directly. It does not test whether nonlinearity exists.

## Frozen measured object

Use DIC only for the primary analysis.

At every DIC time sample form the concatenated spatial response vector:

v(t) = [deflection_above(:,t); deflection_below(:,t)].

No spatial smoothing, coordinate deletion, or outcome-based point selection is allowed except removal of coordinates that are nonfinite in any selected peak vector.

The source-defined DIC position index 185, converted to Python index 184, is the amplitude-reference location.

Reference trace:

r(t) = 0.5 * [deflection_above(185,t) + deflection_below(185,t)].

## Frozen peak extraction

Use the full SRDdataDIC time record.

Compute dt as the median positive time increment.

Use the source-declared approximately 80 Hz slow-mode frequency only to set a duplicate-peak exclusion distance:

minimum peak distance = round(0.4 / (80 * dt)) samples, lower-bounded by 1.

Detect local maxima of abs(r(t)) with scipy.signal.find_peaks using only this distance constraint. No prominence or amplitude threshold is tuned.

If fewer than 8 usable peaks exist, disposition is INSUFFICIENT_RINGDOWN_PEAKS and no architecture conclusion is drawn.

## Frozen amplitude strata

Rank detected peaks by abs(r).

Let n = max(3, floor(number_of_peaks / 3)).

- HIGH = n largest-amplitude peaks.
- LOW = n smallest-amplitude peaks.
- middle peaks are not used in the primary comparison.

Within each stratum, sort peaks by time and split deterministically:
- FIT = alternating peaks starting with the first;
- TEST = alternating peaks starting with the second.

No split is changed after scoring.

## Frozen spatial normalization

For each selected peak vector:

- require finite coordinates;
- concatenate above and below lines;
- normalize by Euclidean norm;
- do not align sign manually.

Because a one-dimensional modal subspace is sign-invariant, comparison uses squared inner products / MAC-style quantities.

## Frozen modal bases

For HIGH-FIT and LOW-FIT separately:

- stack normalized spatial peak vectors as columns;
- compute SVD;
- retain the leading left singular vector as the one-dimensional native spatial modal basis for that amplitude stratum.

Also compute rank-1 energy fraction within each fit matrix as a diagnostic of whether a one-dimensional shape is adequate.

No rank expansion is permitted in the primary analysis.

## Frozen held-out projection error

For normalized test vector x and unit basis phi:

e(x,phi) = sqrt(max(0, 1 - abs(phi^T x)^2)).

Report:

- HIGH test error under HIGH basis: E_HH
- HIGH test error under LOW basis: E_LH
- LOW test error under LOW basis: E_LL
- LOW test error under HIGH basis: E_HL

Each E is the median over the declared held-out peak vectors.

Primary self/cross ratios:

R_H = E_HH / E_LH
R_L = E_LL / E_HL

with zero-denominator cases handled as exact/indeterminate rather than regularized post hoc.

## Frozen repeatability comparator

Construct a basis from each TEST subset itself, solely for repeatability assessment.

Report:

- MAC_H_within = MAC(HIGH-FIT basis, HIGH-TEST basis)
- MAC_L_within = MAC(LOW-FIT basis, LOW-TEST basis)
- MAC_cross = MAC(HIGH-FIT basis, LOW-FIT basis)

No external MAC threshold is used.

## Frozen primary dispositions

### AMPLITUDE_CONDITIONED_MODAL_GEOMETRY

Assign if all are true:

1. E_HH < E_LH;
2. E_LL < E_HL;
3. MAC_cross < MAC_H_within;
4. MAC_cross < MAC_L_within.

Meaning:
each amplitude-stratum basis represents its own held-out spatial peaks better than the opposite-stratum basis, and the high/low difference exceeds the observed split-half geometric difference within both strata.

Evidence role:
ARCHITECTURE_SUPPORTING_NATIVE_MODAL_REORGANIZATION.

### MODAL_GEOMETRY_STABLE_WITHIN_REPEATABILITY

Assign if MAC_cross is greater than or equal to at least one within-stratum MAC and neither stratum shows a clear self-over-cross advantage in the opposite direction.

Meaning:
the declared data do not resolve a high/low spatial geometry difference beyond internal shape repeatability.

### MIXED_MODAL_GEOMETRY

Assign for any valid finite result not meeting either rule above.

Preserve the mixed direction without tuning peak selection, rank, or amplitude strata.

### MODAL_RANK1_NOT_QUALIFIED

Assign if the one-dimensional basis cannot be stably computed, a declared stratum lacks a fit/test vector, or finite-coordinate support is inadequate.

### INSUFFICIENT_RINGDOWN_PEAKS

Assign if fewer than 8 peaks survive the frozen extraction.

### INVALID_TEST

Assign for source identity, field, time, position, or dimension mismatch.

## Secondary diagnostics

Using the same peaks and splits only:

- repeat the basis/error comparison separately for deflection_above and deflection_below;
- report principal angle between HIGH-FIT and LOW-FIT concatenated bases;
- report HIGH/LOW median reference peak amplitudes;
- report number of retained spatial coordinates;
- report rank-1 energy fractions.

These do not replace the primary disposition.

## Project-notation admission

chi:
- NOT ADMITTED by this test.

Chi:
- CANDIDATE ADMISSION is licensed because the native measurement is a spatial modal/vector object.
- If one-dimensional within-stratum bases are repeatable, the declared native modal subspace can instantiate the project Chi layer for this task.
- If rank-1 is not qualified, do not force a one-vector Chi representation; subspace expansion would require a new protocol.

Chi_arc:
- NOT IDENTIFIED by this test alone.

## No-retuning rule

After DIC response scoring starts, do not change:

- source commit/file;
- DIC above/below fields;
- source index 185;
- 80 Hz duplicate-peak spacing reference;
- peak detector;
- top/bottom-third strata;
- alternating fit/test split;
- vector concatenation;
- rank 1;
- projection metric;
- repeatability comparator;
- disposition rules.

Any alternative is post-result P0-D and carries promotion debt.
