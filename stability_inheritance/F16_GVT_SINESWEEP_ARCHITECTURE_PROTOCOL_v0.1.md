# F-16 GVT Sine-Sweep Architecture Qualification Protocol v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** SCIENTIFIC QUESTION / ESTIMATOR / METRICS FROZEN BEFORE SINE-SWEEP SIGNAL SCORING
**Execution dependency:** F16_GVT_SINESWEEP_LAYOUT_PREFLIGHT_v0.1 must qualify the storage mapping
**Evidence class:** PUBLIC EXTERNAL MEASURED P0-Q
**P1 eligibility:** NO
**Architecture evidence role if positive:** ARCHITECTURE_SUPPORTING_NATIVE_THIRD_EXCITATION_FAMILY

## Frozen native facts

The benchmark paper specifies:

- sine-sweep excitation with linear negative rate 0.05 Hz/s;
- sweep from 15 Hz down to 2 Hz;
- benchmark sampling frequency 400 Hz;
- seven excitation levels;
- Level 1: 4.8 N, low-amplitude approximately linear;
- estimation:
  - Level 3: 28.8 N
  - Level 5: 67.0 N
  - Level 7: 95.6 N
- held-out tests:
  - Level 2: 19.2 N
  - Level 4: 57.6 N
  - Level 6: 86.0 N
- outputs are ordered:
  1. excitation location,
  2. wing side adjacent to nonlinear interface,
  3. payload side adjacent to the same interface.

## Frozen question

Does an amplitude-conditioned local complex response trajectory estimated only from sine-sweep Levels 1/3/5/7 predict the held-out Levels 2/4/6 more accurately than a single fixed low-amplitude Level-1 trajectory in the preregistered 6.5-8.2 Hz wing-torsion band?

This is a fresh third excitation-family challenge. No sine-sweep numeric signal values have been inspected before this protocol freeze.

## Frozen signal roles

- Voltage is used only as the reference chirp coordinate from which instantaneous excitation frequency is estimated.
- Force is the measured physical input used to normalize the response.
- Acceleration channels are outputs and may not influence frequency-coordinate construction or support selection.

## Frozen analytic-signal estimator

For each level:

1. remove the sample mean from Voltage, Force, and all acceleration outputs;
2. compute analytic signals using the Hilbert transform;
3. unwrap the phase of analytic Voltage;
4. estimate instantaneous reference frequency from the centered time derivative of unwrapped Voltage phase;
5. compute local complex Force-to-acceleration transfer for each output as

   H_j(t) = S[Y_j(t) U*(t)] / S[|U(t)|^2]

   where U is analytic Force, Y_j is analytic acceleration, and S is a centered Hann-weighted local average.

Frozen local-average duration:
- 4.0 s.

At 0.05 Hz/s this spans 0.2 Hz of the commanded sweep and is fixed before signal inspection.

No output-derived resonance tracking or adaptive window is permitted.

## Frozen frequency coordinate and interpolation

Primary evaluation grid:
- 6.5 to 8.2 Hz inclusive;
- spacing 0.05 Hz.

Secondary grid:
- 2.5 to 14.5 Hz inclusive;
- spacing 0.05 Hz.

For each level, use only samples satisfying all of:

- instantaneous Voltage-derived frequency lies within 2-15 Hz;
- local analytic Force energy denominator exceeds 1e-12 times that level's maximum local Force energy;
- sample is at least half the 4-s smoothing window from either record edge.

Because the sweep is negative-rate, sort valid H_j(t) samples by instantaneous frequency and linearly interpolate real and imaginary components onto the fixed grids.

If fewer than 90% of successive valid instantaneous-frequency differences are negative, or if the valid frequency coordinate does not cover the complete primary grid, that level is INVALID for the primary test. The 90% criterion is an input-coordinate quality gate frozen before signal scoring; it is not an outcome threshold.

## Frozen amplitude-conditioned predictor

Reference:
- H_1(f) from Level 1.

Held-out Level 2 at 19.2 N:
- interpolate in published input amplitude between Level 1 at 4.8 N and Level 3 at 28.8 N.

Held-out Level 4 at 57.6 N:
- interpolate between Level 3 at 28.8 N and Level 5 at 67.0 N.

Held-out Level 6 at 86.0 N:
- interpolate between Level 5 at 67.0 N and Level 7 at 95.6 N.

Interpolation is linear in amplitude and separately applied to real and imaginary components at each fixed frequency/output.

Fixed comparator:
- H_1(f) for all three held-out levels.

No held-out signal contributes to predictor construction.

## Frozen primary metric

Over the complete 6.5-8.2 Hz grid and all three outputs:

E(X,t) = sqrt(sum |X - H_t|^2 / sum |H_t|^2).

Report:
- E_FIXED(t)
- E_CONDITIONED(t)
- R_t = E_CONDITIONED / E_FIXED.

## Frozen primary dispositions

### SINESWEEP_AMPLITUDE_CONDITIONED_ARCHITECTURE_SUPPORT

Assign if:
- all three held-out levels are valid and finite; and
- R_2 < 1, R_4 < 1, R_6 < 1.

Evidence role:
ARCHITECTURE_SUPPORTING_NATIVE_THIRD_EXCITATION_FAMILY.

### SINESWEEP_MIXED_ARCHITECTURE

Assign if at least one but not all held-out levels has R_t < 1.

### SINESWEEP_FIXED_REFERENCE_NOT_OUTPERFORMED

Assign if none has R_t < 1.

### INVALID_TEST

Assign for source/layout failure, invalid chirp coordinate, incomplete primary frequency coverage, nonfinite local transfer estimate, or insufficient Force support.

### INDETERMINATE

Reserve for a valid but numerically degenerate comparison.

## Frozen secondary diagnostics

Without changing the primary disposition, report:

- the same comparison on 2.5-14.5 Hz;
- per-output primary errors;
- Level-specific wing/payload/excitation response trajectories;
- H_payload - H_wing diagnostic and whether its ordering agrees with the full multi-output result;
- frequency of maximum magnitude in the primary band for each output and level;
- monotonicity of the Voltage-derived sweep coordinate;
- Force-energy support diagnostics.

No secondary diagnostic may move the primary frequency band or alter the primary outcome.

## Architecture interpretation

A positive result would add a third excitation family showing that realized structural response is better represented conditionally on excitation/interface regime than by one fixed low-amplitude response object.

A mixed/null result would narrow the architecture by demonstrating excitation-design dependence.

The result remains native structural-dynamics evidence. It does not claim novelty for clearance/friction nonlinearities or amplitude-dependent modal behavior.

No physical chi is admitted.
Native local response trajectories are not automatically renamed capital Chi.
Chi_arc is not automatically identified solely from this test.

## No-retuning rule

After sine-sweep signal scoring begins, do not change:

- 4.0-s smoothing duration;
- Voltage frequency-coordinate role;
- measured Force normalization;
- primary/secondary frequency grids;
- level roles;
- amplitude interpolation;
- primary metric;
- output order;
- disposition rule.

Any alternative becomes a new post-result P0-Q/P0-D object with the appropriate promotion debt.
