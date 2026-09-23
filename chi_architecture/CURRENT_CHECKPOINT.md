# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02C-CP0-CANDIDATE-SELECTION-FROZEN  
**Date:** 2026-09-23  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.3

## Active task

Select the untouched D02C physical system under:

chi_architecture/d02c/D02C_CANDIDATE_SELECTION_FREEZE_v0.1.md

The system must prospectively test CA-D007:

ARCHITECTURE_REORGANIZATION_CAN_PRECEDE_SCALAR_TRANSFORMATION

## Selection rule

Choose by completeness, independent observables, graded perturbation, uncertainty support, native comparator strength, and automated reproducibility.

Do not choose based on published outcome direction.

## External literature search

Undermind:
D02C untouched graded physical candidate search

## Resume rule

1. Read this checkpoint and D02C_CANDIDATE_SELECTION_FREEZE_v0.1.md.
2. Inspect the completed candidate search.
3. Verify eligibility axes using source methods/data availability only.
4. Freeze the selected system, exact source/data contract, perturbation levels, scalar definition, organization metric, uncertainty/detection rules, and native comparator before reading decisive direction/order.
5. Only then acquire and analyze decisive data.
6. Package final reproduction behind python chi_architecture/reproduce.py d02c.
