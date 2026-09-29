# F-16 Sine-Sweep Input-Coordinate Diagnostic v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** POST-v0.1-FAILURE INPUT-ONLY METHOD QUALIFICATION
**Evidence class:** P0-D / promotion debt for any later sine-sweep response scoring
**Acceleration outputs:** PROHIBITED in this diagnostic

## Purpose

The frozen sine-sweep v0.1 response protocol failed its Voltage-derived instantaneous-frequency monotonicity gate before producing a response score. This diagnostic asks only whether the published 15-to-2 Hz, -0.05 Hz/s excitation coordinate can be reconstructed robustly from the excitation channels without using any acceleration output.

No response architecture metric is computed.

## Frozen source

Use the verified official 4TU F-16 archive:
- size 148,455,295 bytes;
- SHA-256 2278429b1f15f15448e6f101d395a5587d58ac23d32052fd42f8b33a894c0afa.

Use the seven SineSw files already mapped by the layout preflight.

Read only:
- Voltage;
- Force;
- Fs.

Do not load Acceleration.

## Published reference law

The benchmark report specifies a downward linear sine sweep:
- nominal start: 15 Hz;
- nominal end: 2 Hz;
- nominal rate: -0.05 Hz/s.

The primary architecture band remains 6.5-8.2 Hz, but this diagnostic does not score response in that band.

## Frozen candidate coordinate estimators

### C1 Raw Hilbert derivative reference

Mean-center Voltage, form the analytic signal, unwrap phase, and differentiate phase sample-by-sample.

This reproduces the failed v0.1 coordinate only as a diagnostic reference.

### C2 Global quadratic-phase chirp fit

Mean-center Voltage, form the analytic signal, unwrap phase, discard the first and last 2 seconds to reduce analytic-edge contamination, and fit

phase(t) = a + b t + c t^2

by ordinary least squares.

Derive
f(t) = (b + 2 c t)/(2 pi).

This estimator is native to a linear chirp but does not impose the published -0.05 Hz/s rate.

### C3 STFT ridge

Use Voltage only:
- Hann window = 4.0 s;
- hop = 1.0 s;
- search band = 1.5-16.5 Hz;
- at each STFT time, select the maximum-magnitude Voltage frequency bin;
- smooth the selected ridge with a 5-point median filter;
- fit frequency versus time by ordinary least squares on ridge points between 2 and 15 Hz.

### C4 Positive zero-crossing coordinate

Mean-center Voltage.
Find upward zero crossings with linear interpolation of the crossing time.
Compute cycle frequency as the inverse time between consecutive upward crossings.
Assign frequency to the cycle midpoint.
Apply an 11-cycle median filter.
Fit frequency versus time using cycles whose estimated frequency is between 2 and 15 Hz.

## Frozen diagnostic fields

For each level/candidate report:
- fitted linear frequency slope in Hz/s;
- absolute slope error from 0.05 Hz/s magnitude;
- frequency-fit R^2 where applicable;
- minimum and maximum estimated frequency in the active 2-15 Hz segment;
- whether 6.5-8.2 Hz is covered;
- monotonic-decreasing fraction on the candidate's native coordinate sequence;
- number of coordinate samples/cycles/windows.

## Coordinate qualification rule

A candidate is COORDINATE_QUALIFIED only if all seven levels:
- have finite negative fitted slope;
- cover the complete 6.5-8.2 Hz primary band;
- have fitted sweep-rate magnitude within 10% of 0.05 Hz/s;
- have frequency-versus-time R^2 >= 0.98.

The 10% and R^2 gates qualify the excitation coordinate only. They are not scientific effect thresholds.

If more than one candidate qualifies all seven levels, select the candidate with the smallest median absolute sweep-rate error. Ties are broken by higher median R^2 and then higher median monotonic-decreasing fraction.

## Dispositions

- INPUT_COORDINATE_QUALIFIED if at least one candidate qualifies all seven levels.
- INPUT_COORDINATE_NOT_QUALIFIED if none does.
- INVALID_TEST for source/file identity or excitation-channel failure.

## Consequence

A qualified input coordinate permits a separately frozen post-result P0-D sine-sweep response protocol using only the selected coordinate method. It cannot restore prospective status to sine-sweep response scoring because v0.1 already entered a failed scoring path.

No acceleration value may be used in choosing the coordinate estimator.
