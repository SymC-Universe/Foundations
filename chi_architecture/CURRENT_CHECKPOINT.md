# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02A-CP0-PHYSICAL-FREEZE  
**Date:** 2026-09-22  
**Branch:** `chi-architecture-p0`  
**Parent checkpoint:** D01C-CP4-CLOSED-CI-HARDENED  
**Protocol:** SymC GOM v0.8.3

## Active experiment

`D02A_CSPBBR3_PHONON_INHERITANCE`

This is the first post-D01 domain-native physical calibration test.

Scientific freeze:

`chi_architecture/d02_cspbbr3/D02A_PREEXECUTION_FREEZE_v0.1.json`

Literature / novelty firewall:

`chi_architecture/d02_cspbbr3/D02A_LITERATURE_POSITION.md`

## Important evidence status

The broad qualitative result of the 2021 CsPbBr3 paper was already known before this freeze.

Therefore:

`PHYSICAL != UNTOUCHED_CONFIRMATION`

D02A is P0-D physical calibration. It may validate or reject the proposed inheritance/refusal representation on real material data but cannot pay prospective confirmation debt.

## Resume rule

1. Read this checkpoint and the D02A freeze.
2. Do not inspect numerical source values manually before the schema checkpoint is archived.
3. Run the source-schema workflow.
4. Archive exact source-file SHA-256 hashes plus workbook sheet/dimension/text-header inventory as D02A-CP1.
5. Build the parser from schema only. No value-dependent sheet/range selection.
6. Execute every frozen applicable source range.
7. Fail closed on DHO convention ambiguity or missing omega0/Gamma.
8. Archive execution as D02A-CP2 before interpretation.
9. Interpret only against the frozen native comparator and novelty firewall.
10. Reviewer-facing reproduction must converge to `python chi_architecture/reproduce.py d02a`.

## Immediate next action

Run source integrity/schema inventory against the two frozen publisher workbooks.


## CP0.1 mechanical source-fetch hardening

The first source-schema run was slow on the primary Springer Nature media host before any scientific values were emitted.

The schema workflow now tries the exact frozen publisher URL first and the standard Springer static-content mirror second, with bounded connect/read timeouts and a browser-like User-Agent.

This is a transport-only change. The frozen source filenames, DOI, scientific question, ranges, metrics, chi-admission rules, comparators, falsifiers, and evidence class are unchanged.
