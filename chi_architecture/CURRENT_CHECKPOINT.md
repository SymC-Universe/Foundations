# Chi Architecture Active Checkpoint

**Checkpoint ID:** D01C-CP0-PREEXECUTION-FREEZE  
**Date:** 2026-09-22  
**Branch:** `chi-architecture-p0`  
**Parent before checkpoint:** `53be86c5bdf0c62888114090e2589ec84902557b`  
**Protocol:** SymC GOM v0.8.3

## Current scientific state

D01A is complete. D01B is complete and has a repository readout plus post-result discovery ledger entry.

D01C is now the active experiment.

The D01C scientific design is frozen in:

`chi_architecture/D01C_PREEXECUTION_FREEZE_v0.1.json`

No D01C numerical output existed when this checkpoint was created.

## Resume rule

A future session should start here and do the following in order:

1. Read this checkpoint.
2. Read `D01C_PREEXECUTION_FREEZE_v0.1.json`.
3. Do **not** change the frozen parameter grid, metrics, perturbations, time window, resolvent window, or comparators after viewing D01C output.
4. Implement the runner and tests without changing scientific content.
5. Commit the implementation as **D01C-CP1-IMPLEMENTED** before executing the full map.
6. Execute through GitHub Actions.
7. Archive the complete result and environment as one workflow artifact.
8. Update this checkpoint to the observed run ID, artifact ID, commit SHA, result hash, and next unresolved scientific question.
9. Interpret only after the execution checkpoint is immutable.

## Reproducibility target

The public/reviewer-facing path must converge to:

`python chi_architecture/reproduce.py d01c`

That single command should validate the freeze, run the D01C tests, execute the frozen map, generate the compact readout, and write a manifest.

Reviewers should not need to know or manually invoke the internal runner/test files.

## Current next action

Implement D01C and the single-entry reproduction wrapper. No user input is required.
