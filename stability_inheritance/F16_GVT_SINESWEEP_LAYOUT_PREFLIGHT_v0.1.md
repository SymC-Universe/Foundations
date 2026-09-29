# F-16 GVT Sine-Sweep Layout Preflight v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** FROZEN DATA-LAYOUT PREFLIGHT / NO SIGNAL SCORING
**Evidence class:** PUBLIC EXTERNAL MEASURED P0-Q
**P1 eligibility:** NO

## Native acquisition facts frozen before raw inspection

From the benchmark report:

- excitation: linear negative-rate sine sweep;
- sweep rate: 0.05 Hz/s downward;
- frequency range: 15 to 2 Hz;
- seven excitation levels;
- Level 1: 4.8 N low-amplitude approximately linear reference;
- estimation levels:
  - Level 3: 28.8 N
  - Level 5: 67.0 N
  - Level 7: 95.6 N
- test levels:
  - Level 2: 19.2 N
  - Level 4: 57.6 N
  - Level 6: 86.0 N
- sampling frequency for the benchmark: 400 Hz;
- three acceleration outputs in the published order: excitation point, wing side of nonlinear interface, payload side of nonlinear interface.

## Purpose

Establish only the storage layout and mathematical compatibility of the seven SineSw MAT files before any signal value, resonance curve, amplitude trend, or held-out outcome is inspected.

## Allowed operations

For files matching the official SineSw family:

- list filenames;
- map level numbers from filenames;
- record file size and SHA-256;
- list MAT variable names;
- record array shape, dtype, and element count for Force, Voltage, Acceleration, Fs, and any explicit time/frequency coordinate arrays;
- record scalar Fs if present;
- verify that seven levels are present;
- determine whether the three outputs and measured Force can be mapped without reading their numeric values.

## Prohibited operations

- no Force/Acceleration numeric signal values;
- no extrema, RMS, spectra, phase, FRF, resonance frequency, damping, or time-history plotting;
- no comparison among excitation levels;
- no fitting or smoothing;
- no use of test levels to design an estimator.

## Dispositions

- SINESWEEP_LAYOUT_QUALIFIED if all seven levels are present and the storage layout admits a unique non-value-based mapping of measured Force and the three outputs.
- SINESWEEP_LAYOUT_NEEDS_MAPPING if files are present but the array organization requires an explicit non-value-based mapping rule.
- SINESWEEP_LAYOUT_INVALID if required levels/arrays are missing or incompatible with the published benchmark structure.

Only after this preflight may the time-frequency scoring protocol be finalized and frozen before numeric signal scoring.
