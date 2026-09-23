# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02C-CP1-WIND-BLADE-SYSTEM-AND-DECISION-CONTRACT-FROZEN  
**Date:** 2026-09-23  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.3

## Selected system

Full-scale wind-turbine blade climate-chamber icing experiment.

Dataset DOI:
10.5281/zenodo.18427836

Publication DOI:
10.1088/1742-6596/2647/19/192008

Selection record:
chi_architecture/d02c/D02C_CANDIDATE_SELECTION_RECORD_v0.2.md

Prospective decision contract:
chi_architecture/d02c/D02C_WIND_BLADE_CONTRACT_v0.1.md

## Frozen decisive variables

Local scalar:
source OMA damping ratio chi = zeta, contingent on source unit verification.

Independent organization:
three-sensor complex modal-vector dissimilarity 1-MAC from raw cross-spectral matrices.

Control:
published time-ordered icing intervention, with chamber temperature retained as a native confounder.

## Baseline

Twelve midnight ten-minute windows:
00:00 through 01:50 UTC.

## Intervention

Twelve ten-minute windows:
11:20 through 13:10 UTC.

Published events:
- spray start 11:23;
- accelerate spray 12:13;
- end spray 12:49;
- heating starts 13:13.

## Critical anti-bias rule

The scalar and organization onset thresholds are frozen in D02C_WIND_BLADE_CONTRACT_v0.1.md before reading decisive OMA damping or acceleration values.

Natural-frequency temperature behavior seen in prior methods/public text is excluded from the decisive D02C scalar endpoint.

## Next action

1. verify the damping unit convention mechanically/native-documentation-only;
2. inspect raw CSV column headers only and freeze exact sensor-column mapping;
3. implement tests and one-command reproduction;
4. commit implementation before decisive execution;
5. execute D02C once;
6. archive before interpretation;
7. compare the observed onset ordering against CA-D007 and the native temperature/EOV comparator.
