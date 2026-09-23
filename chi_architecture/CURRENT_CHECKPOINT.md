# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02B-CP0-CANDIDATE-SELECTION-FROZEN  
**Date:** 2026-09-22  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.3  
**Parent state:** D02A-CP4-CLOSED

## Active task

Identify D02B using the frozen eligibility/ranking contract:

chi_architecture/d02b/D02B_CANDIDATE_SELECTION_FREEZE_v0.1.md

No D02B candidate has yet been selected under this contract.

## Resume rule

1. Read this checkpoint.
2. Read the D02B candidate selection freeze.
3. Search candidates using metadata/method/data-availability criteria.
4. Do not choose a system because its observed outcome is favorable.
5. Verify all six eligibility axes.
6. Commit the selected system and exact source/data contract before extracting decisive outcome values.
7. Only then inspect/execute the physical analysis.
8. Package eventual reproduction behind python chi_architecture/reproduce.py d02b.

## Current external literature workspace

Undermind workspace: Stability Inheritance Publication Build

Active search: D02B physical candidate completeness search

The search goal explicitly ranks candidates by direct measurement completeness and reproducibility, not by favorable Stability Inheritance outcome.
