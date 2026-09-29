# F-16 GVT SpecialOdd Storage Mapping v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Source preflight:** F16_GVT_SPECIALODD_LAYOUT_PREFLIGHT_v0.1.md
**Workflow run:** 36513169165
**Status:** STORAGE MAPPING QUALIFIED / NO SIGNAL VALUES SCORED
**Scientific protocol affected:** F16_GVT_SPECIALODD_REPLICATION_PROTOCOL_v0.1.md
**Scientific question or metrics changed:** NO

## Observed file layout

The official archive contains six SpecialOdd MAT files, two per published excitation level:

- F16Data_SpecialOddMSine_Level1.mat
- F16Data_SpecialOddMSine_Level1_Validation.mat
- F16Data_SpecialOddMSine_Level2.mat
- F16Data_SpecialOddMSine_Level2_Validation.mat
- F16Data_SpecialOddMSine_Level3.mat
- F16Data_SpecialOddMSine_Level3_Validation.mat

For every main level file:
- Force shape = 9 x 49152
- Voltage shape = 9 x 49152
- Acceleration shape = 3 x 9 x 49152

For every Validation file:
- Force shape = 1 x 49152
- Voltage shape = 1 x 49152
- Acceleration shape = 3 x 1 x 49152

Since 49152 = 3 x 16384, the published acquisition design maps directly as:

- each row = one realization;
- each realization = three consecutive 16,384-sample periods;
- main file = realizations 1-9, estimation;
- Validation file = realization 10, held-out test;
- period 1 = transient, excluded;
- periods 2-3 = steady state, scored.

No numeric signal value was needed to establish this map.

## Level mapping

The frozen SpecialOdd protocol maps:

- archive Level1 -> 12.2 N RMS
- archive Level2 -> 49.0 N RMS
- archive Level3 -> 97.1 N RMS

The level identities are taken from the benchmark paper and were frozen before signal scoring.

## Disposition

**SPECIALODD_LAYOUT_QUALIFIED_AFTER_NONVALUE_MAPPING**

The initial layout preflight returned SPECIALODD_LAYOUT_NEEDS_MAPPING only because the published ten realizations are split across a 9-realization estimation file and a 1-realization Validation file rather than stored in one 10-realization array.

This is a storage-layout resolution, not a scientific plan change.

## Execution authorization

F16_GVT_SPECIALODD_REPLICATION_PROTOCOL_v0.1.md may now execute exactly as frozen using this file mapping.

No frequency band, estimator, representation, metric, disposition rule, or evidence class is altered.
