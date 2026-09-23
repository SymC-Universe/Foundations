# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02B-CP8-PARSER-AND-LABELS-FROZEN  
**Date:** 2026-09-23  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.3

## Raw manifest closed

Run: 35822278161  
Artifact ID: 10732894919  
Digest: sha256:5602ac9a83cbe1ee3aa59d76ca6140f27e8b5fc95ddc5b4660014a9dcc0f5f63

Raw archive:
- MD5 68450ff0f1c25492ee243b8adba29991
- SHA-256 2e6ece8670ab2201d2a8cdf38e31cc2b979062d0c7eaf93da152e1e27b6ffb89
- 919 amplitude + 919 phase + one README member.

## Frozen matched spatial support

All 18 torque states share exactly 51 scan-point IDs.

The all-loose state has one extra point ID 20.

D02B uses only the exact 51-point intersection for all states.

## Final pre-FRF freeze

Read:

chi_architecture/d02b/D02B_RAW_PARSER_AND_CLASSIFICATION_FREEZE_v0.1.md

This file freezes:
- filename parsing;
- common-point filtering;
- scalar refusal states;
- similar-chi resolution rule;
- response-reorganization rule;
- family labels;
- native-toolkit verdict.

## Permission boundary

Raw FRF member values may now be read.

Next:
1. inspect one amplitude/phase file format mechanically;
2. implement the D02B parser/analyzer and tests;
3. expose through python chi_architecture/reproduce.py d02b;
4. commit implementation before full scientific execution;
5. execute in GitHub Actions and archive before interpretation.
