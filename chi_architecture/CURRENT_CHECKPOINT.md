# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02F-CP3-ONE-COMMAND-IMPLEMENTED-PREEXECUTION  
**Date:** 2026-09-24  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.6

STATUS

D02F MFR-14, analyzer, regression tests, one-command reviewer entrypoint, and dedicated archival workflow are implemented.

CURRENT GATE

Execute the frozen D02F test once and archive the result before scientific interpretation.

NEXT ACTION

Observe the dedicated GitHub Actions workflow triggered by this implementation commit.

WHY

The science is frozen. Only mechanical/parser failures may be repaired from this point.

USER ACTION

NONE.

SUCCESS CONDITION

A successful D02F archival workflow with source hashes, result hashes, artifact digest, and frozen primary mode-01 outcome.

FAILURE BRANCH

Repair only implementation defects. Do not alter:
- water-bin edges;
- primary mode;
- EOV covariates;
- k=30 matching;
- maximum match distance 3.0;
- >=10 row completeness floor;
- bootstrap rule;
- scalar/organization margins;
- onset logic;
- MFR-14 consequence table.
