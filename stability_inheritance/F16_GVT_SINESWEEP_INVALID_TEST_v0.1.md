# F-16 GVT Sine-Sweep v0.1 Invalid-Test Adjudication

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Protocol:** F16_GVT_SINESWEEP_ARCHITECTURE_PROTOCOL_v0.1.md
**Workflow run:** 36514191804
**Status:** INVALID_TEST / INPUT-COORDINATE GATE FAILURE
**Scientific score produced:** NO
**Architecture consequence:** NONE from v0.1

## Failure

The v0.1 protocol prospectively required the Voltage-derived instantaneous frequency coordinate to be monotonically decreasing on at least 90% of successive valid samples.

The first scoring execution stopped before any result metric or disposition was produced because the observed monotonic-decreasing fraction was:

0.5028311059424628

The frozen gate therefore failed.

## Interpretation

This is not evidence against amplitude-conditioned architecture and not evidence against the F-16 sine-sweep data.

It establishes that the specific v0.1 analytic-Voltage-phase coordinate is not operational for this measured record under the frozen rule.

The protocol may not be repaired in place by smoothing the phase, changing the gate, switching to Force phase, imposing the commanded sweep law, or selecting a different time-frequency estimator after this failure.

## Exposure status

The execution loaded the sine-sweep signals and constructed intermediate analytic objects before the gate stopped the run. No held-out error metrics or architecture outcome were emitted.

Because the same dataset has nevertheless entered a failed scoring path, any redesigned sine-sweep analysis is conservatively classified POST-RESULT / P0-D with promotion debt. It may contribute to Function/Limit mapping but cannot increase the prospective confirmation ceiling.

## Next clean action

Run an input-only coordinate diagnostic using Voltage and/or Force while explicitly ignoring acceleration outputs. Determine whether the published 15-to-2 Hz, 0.05 Hz/s sweep can be reconstructed with a documented native time-frequency coordinate.

If a robust coordinate exists, freeze a new P0-D sine-sweep architecture protocol before computing any response score under that redesigned coordinate.
