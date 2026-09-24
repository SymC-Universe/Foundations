# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02E-CP4-HEALTHY-SELECTION-ARCHIVED  
**Date:** 2026-09-24  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.6

STATUS

Healthy-only target selection is complete and archived before any damaged vibration record is opened.

CURRENT GATE

Implement the frozen D02E damaged-state analyzer for the already-selected 8.7890625 Hz primary family.

NEXT ACTION

Build tests, one-command reproduction, and a dedicated archival workflow for the frozen A_1 sequence:

Healthy 12 Nm -> 9 Nm -> 6 Nm -> NoBolt

across four physical bolt locations and all 20 source replicates per state.

WHY

The primary modal family now has independent healthy-only provenance and meets the >=16/20 scalar-admission requirement. Damaged data may now be opened under the frozen MFR-14 without target-selection leakage.

ACTIVE EXECUTION RECORD

- healthy selection run: 35944132810
- artifact ID: 10786042762
- artifact digest: sha256:ed50d5fd65b032721c5f20be928514bbba859bdf13b9c07007a8d92305038d5c
- healthy-selection result SHA-256: 8f4f554439bc520940f24b2b70f704c9a48e7c78c4c9828643631f442058f3bc
- selected primary family: 8.7890625 Hz
- admitted healthy chi replicates: 17/20

USER ACTION

NONE.

SUCCESS CONDITION

A dedicated D02E workflow completes the frozen four-location graded analysis and archives its result before interpretation.

FAILURE BRANCH

Mechanical/parser failures may be repaired without changing MFR-14. Scientific incompleteness, scalar refusal, mixed ordering, or adverse ordering are retained exactly under the frozen decision rules.
