# Brake-Reuss Beam Long-Term Sampling-Grid Audit v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Status:** FROZEN HEADER/SCHEMA AUDIT AFTER PRE-SCORE IMPLEMENTATION FAILURE
**Evidence class:** P0-Q SOURCE/SCHEMA QUALIFICATION
**Scientific scoring:** PROHIBITED

## Trigger

BRB_LONGTERM_HISTORY_RESPONSE_V01A stopped before FRF scoring because the implementation assumed one common sampling interval across every selected Rand-FRF file. The frozen v0.1 scientific protocol required only that Force and selected acceleration channels share a common sampling interval within each file; it did not freeze cross-file equality.

This audit maps the timing/storage structure without computing any response spectrum or scientific outcome.

## Frozen source set

Use the same canonical OSF project, shaker archives, states, common voltages, and realization indices as BRB_LONGTERM_HISTORY_RESPONSE_PROTOCOL_v0.1:

- S0 FirstRound/RandFRF_Before
- S1 FirstRound/RandFRF_After
- S2 SecondRound/RandFRF_After
- S3 ThirdRound/RandFRF_Before
- S4 ThirdRound/RandFRF_After
- voltages 0.01, 0.10, 1.00 V
- realizations 0-9

## Allowed fields

For every selected CSV record only:

- file identity/path;
- uncompressed byte size;
- channel names from row 1;
- sampling intervals from row 2;
- selected Force channel name;
- selected seven acceleration channel names;
- selected-channel within-file timing consistency;
- selected common dt for that file;
- approximate row/sample count from line count only.

Do not compute FFTs, FRFs, RMS, extrema, averages, response norms, or any signal-derived statistic.

## Frozen output

Report:

- unique selected-channel dt values;
- counts by state, voltage, and dt;
- sample-count ranges by dt;
- whether dt ratios are rational/integer-related within numerical tolerance;
- whether every file preserves within-file Force/acceleration timing consistency.

## Dispositions

- SAMPLING_GRID_MAPPING_QUALIFIED if every selected file has internally consistent Force/acceleration timing and the cross-file dt set is finite and explicitly mappable.
- WITHIN_FILE_TIMING_INVALID if any selected file violates the v0.1 within-file timing requirement.
- SAMPLING_GRID_AMBIGUOUS if the cross-file timing structure cannot be mapped without inspecting response values.
- SOURCE_IDENTITY_CHANGED for archive/layout mismatch.

A qualified mapping permits a new v0.2 history-response protocol to define a common physical-frequency evaluation grid before scoring. It does not authorize scientific scoring by itself.
