# Chi Architecture Active Checkpoint

**Checkpoint ID:** D01C-CP4-CLOSED-CI-HARDENED  
**Date:** 2026-09-22  
**Branch:** `chi-architecture-p0`  
**Scientific freeze:** `b8bf36c2776e2d788cdbf7a5f33e4254d1cb5f9b`  
**Execution commit:** `9818612abae93e460af7ab45281fd9a5e4ae68e7`  
**Execution archive commit:** `df29383f7c060a8a8e52034deeed6d67a17dd8cc`  
**Protocol:** SymC GOM v0.8.3

## D01C closure

D01C is complete.

Frozen result:

- 26/26 cases executed;
- spectrum preserved to maximum residual `2.22e-16`;
- fixed-spectrum N1 gain range: 1.0 to 28.6524936;
- fixed-spectrum N2 gain range: 1.0 to 74.5003624;
- eigenvalue-only sufficiency: `REFUTED_WITHIN_FROZEN_CONSTRUCTION`.

Comparator verdict:

`STANDARD_NONMODAL_TOOLKIT_SUFFICIENT_FOR_D01C`

No new non-normal chi, transient-growth law, resolvent quantity, or pseudospectral quantity is admitted.

## Joint chi / Chi interpretation

D01C supports a representation rule:

A scalar/spectrum may remain valid for asymptotic placement while being insufficient for a finite-time or robustness question. When that happens, broader Chi must retain the native carrier/operator structure required by the question rather than inventing a replacement scalar.

This is architecture discipline, not evidence for a new physical agent.

## Reproduction

Supported reviewer command:

`python chi_architecture/reproduce.py d01c`

Guide:

`chi_architecture/REPRODUCIBILITY_GUIDE.md`

Permanent archival metadata:

`chi_architecture/results/D01C_ARCHIVAL_RECORD_v0.1.json`

Scientific readout:

`chi_architecture/D01C_NONNORMAL_DOMAIN_MAP_READOUT_v0.1.md`

## Resume rule

Do not reopen D01C merely to add more synthetic non-normal families.

A new D01 version is justified only by a genuinely new scientific question.

The next high-information move is a prospectively frozen physical/domain-native test with independently grounded:

1. local or spectral coordinate;
2. carrier/coupling/system organization;
3. perturbation/recovery outcome;
4. native comparator.

Any such experiment requires its own pre-result checkpoint and freeze before decisive outcome inspection.

## CI hardening after closure

The umbrella P0 workflow previously reran the full 1,152-case D01B map on every `chi_architecture/**` change under a 10-minute timeout. That created non-scientific timeout/cancellation noise on otherwise valid commits.

CP4 removes the expensive D01B full-map execution from the fast umbrella lane. The umbrella lane still runs the complete unit/scientific-guard test suite, including D01B tests and freeze validation, plus the D01A exact map. Full D01B reproduction remains in its dedicated archival workflow.

This is a mechanical CI separation only. No D01A, D01B, or D01C scientific parameter, metric, result, threshold, or interpretation changed.
