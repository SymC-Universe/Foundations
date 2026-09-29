# Brake-Reuss Beam Long-Term History-Response Mechanical Schema Repair v0.1a

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Parent scientific protocol:** BRB_LONGTERM_HISTORY_RESPONSE_PROTOCOL_v0.1.md
**Failed execution:** workflow run 36579762569
**Failure class:** MECHANICAL_SCHEMA_MAPPING_BEFORE_SCIENTIFIC_SCORE
**Scientific protocol changes:** NONE

## Failure preserved

The first execution stopped while mapping the first extracted CSV header. No FRF, predictor, held-out error, transition ratio, or scientific disposition was produced.

The extracted channel labels contained binary length prefixes and native short codes rather than literal words such as "Force" or "Acceleration".

## Native channel identity

The public BRB long-term data documentation defines the shaker sensor order as:

1. excitation force;
2-4. three strain gauges;
5. acceleration at the excitation point;
6-11. X/Y/Z acceleration at the left and right ends;
12-14. three thermocouples;
15. command/input voltage channel in the stored acquisition.

The raw coded names observed before any response scoring correspond to:

- F1 = excitation force;
- A1 = acceleration at excitation point;
- X1, Y1, Z1 = left-side accelerations;
- X2, Y2, Z2 = right-side accelerations.

The implementation retry therefore freezes:

- force channel = F1;
- acceleration outputs = [A1, X1, Y1, Z1, X2, Y2, Z2] in that order.

Source:
https://jointmechanics.org/index.php/Brb_lterm_multiscale21

## Encoding repair

Before interpreting row-1 channel names or row-2 sampling intervals, each textual CSV field is normalized by stripping leading ASCII control bytes. This removes the length-prefix bytes while leaving the encoded channel name or numeric metadata intact.

No response row is used to infer channel identity.

## Scientific invariance

The following remain exactly as frozen in v0.1:

- states S0-S4;
- voltages 0.01, 0.1, 1.0 V;
- even FIT / odd TEST realization split;
- 140-200 Hz primary band;
- fit-only excitation support;
- H1 FRF estimator;
- same-voltage LOSO comparator;
- input-spectrum-matched state-blind comparator;
- transition definitions;
- primary error metric;
- history disposition rules;
- reassembly rules;
- interpretation ceiling.

This retry is not a new scientific protocol and does not erase the failed execution.
