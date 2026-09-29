# F-16 GVT SpecialOdd Layout Preflight v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** FROZEN DATA-LAYOUT PREFLIGHT / NO SIGNAL SCORING
**Evidence class:** PUBLIC EXTERNAL MEASURED P0-Q
**P1 eligibility:** NO

## Purpose

Qualify the raw layout of the F-16 SpecialOddMSine data family before any cross-excitation replication protocol is constructed or scored.

The benchmark paper specifies:
- three excitation levels: 12.2, 49.0, 97.1 N RMS;
- 10 input realizations per level;
- 3 periods per realization;
- 16,384 points per period;
- only periods 2 and 3 are steady state;
- nine realizations are suggested for estimation and the final realization for testing;
- frequency range 1-60 Hz with an odd random-grid multisine.

These facts are fixed before raw inspection.

## Intake dependency

Execution requires F16_GVT_DATA_INTAKE_v0.1 = INTAKE_PASS.

## Allowed operations

For every SpecialOddMSine MAT file:
- identify filename;
- list MAT variable names;
- record array shape and dtype for Force, Voltage, Acceleration, and Fs;
- record only scalar Fs if present;
- record file byte size and SHA-256;
- count files by apparent level from filename.

Do not record signal values, extrema, spectra, fit metrics, or output behavior.

## Prohibited operations

- no model fitting;
- no FFT/spectral scoring;
- no channel selection from outcomes;
- no test-realization inspection;
- no comparison with the FullMSine result.

## Dispositions

- SPECIALODD_LAYOUT_QUALIFIED if all three published levels are present and the raw arrays can be reconciled with 10 realizations x 3 periods x 16,384 samples without looking at values.
- SPECIALODD_LAYOUT_NEEDS_MAPPING if files are present but their storage arrangement requires an explicit non-value-based reshape/mapping rule.
- SPECIALODD_LAYOUT_INVALID if required files/arrays are absent or mathematically incompatible with the published acquisition design.

A qualified layout permits freezing a separate replication protocol before any signal scoring.
