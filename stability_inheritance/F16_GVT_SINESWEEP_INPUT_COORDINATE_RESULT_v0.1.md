# F-16 Sine-Sweep Input-Coordinate Diagnostic Result v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Protocol:** F16_GVT_SINESWEEP_INPUT_COORDINATE_DIAGNOSTIC_v0.1.md
**Workflow run:** 36515710058
**Status:** INPUT_COORDINATE_QUALIFIED
**Acceleration loaded:** NO
**Evidence class:** P0-D INPUT-ONLY METHOD QUALIFICATION

## Result

Four preregistered Voltage-only coordinate estimators were compared against the published 15-to-2 Hz, -0.05 Hz/s sine-sweep law.

- C1 raw Hilbert derivative: not qualified across all levels.
- C2 global quadratic-phase chirp fit: qualified across all seven levels.
- C3 STFT ridge: not qualified across all levels under the frozen monotonic/R2 criteria.
- C4 positive zero-crossing coordinate: qualified across all seven levels.

Under the frozen selection rule, C2 was selected because it had the smallest median absolute sweep-rate error among all-level-qualified candidates.

### C2 aggregate diagnostics

- all seven levels qualified: YES
- median absolute sweep-rate error: 0.00007733799 Hz/s
- median frequency-vs-time R2: 1.0
- median monotonic-decreasing fraction: 1.0

### Independent C4 check

Zero-crossing estimates independently recovered the published sweep with:

- level-specific slopes approximately -0.04981 to -0.04994 Hz/s;
- R2 approximately 0.99724 to 0.999998;
- primary-band coverage at every level;
- monotonic-decreasing fractions approximately 0.991 to 0.997.

## Interpretation

The failure of the v0.1 raw Hilbert derivative did not indicate that the experimental chirp coordinate was absent. It indicated that samplewise derivative of noisy/real Voltage phase was a poor operational coordinate.

The excitation law is recoverable robustly from input data alone using two independent methods.

This qualifies C2 as the selected coordinate for a separately frozen post-result sine-sweep response analysis.

## Epistemic consequence

Because the failed v0.1 scoring path already loaded the sine-sweep records, any redesigned response analysis remains P0-D/post-result and cannot restore prospective status.

The input-coordinate result itself was obtained without loading acceleration values and therefore does not use response outcomes to choose the replacement coordinate.
