# Chi Architecture Active Checkpoint

**Checkpoint ID:** D01C-CP2-EXECUTED  
**Date:** 2026-09-22  
**Branch:** `chi-architecture-p0`  
**Scientific freeze:** `b8bf36c2776e2d788cdbf7a5f33e4254d1cb5f9b`  
**Execution implementation:** `9818612abae93e460af7ab45281fd9a5e4ae68e7`  
**Protocol:** SymC GOM v0.8.3

## Execution state

D01C has executed successfully under the frozen CP0 scientific design.

- GitHub Actions run: `35809467796`
- workflow: `Chi Architecture D01C Reproduction`
- conclusion: `success`
- artifact: `chi-architecture-d01c-v01`
- artifact ID: `10728829675`
- artifact digest: `sha256:7178cd28a579b17d35da57e37ebfccb4a540ac6f0f23a688233d9f2c665c305e`
- full result SHA-256: `ab24c3dcb9490d1b07c9043b922e326f149cf71fd3522c67e2b54c1d53206d38`
- manifest SHA-256: `7d06190f0111e092433eeb9a042151119d9e0e31d515197dbf59be426ed2cbb8`

The permanent compact archival metadata is:

`chi_architecture/results/D01C_ARCHIVAL_RECORD_v0.1.json`

## Frozen numerical facts

- 26/26 frozen cases executed.
- maximum spectrum-preservation residual: `2.220446049250313e-16`.
- eigenvalue-only sufficiency status: `REFUTED_WITHIN_FROZEN_CONSTRUCTION`.
- N1 fixed spectrum `[-1,-2]`: max operator state gain changed from `1.0` at 90 degrees to `28.6524936441728` at 0.5 degrees.
- N2 fixed spectrum `[-0.25,-2]`: max operator state gain changed from `1.0` at 90 degrees to `74.5003623740674` at 0.5 degrees.
- minimum scanned complex stability radius reached `0.01745041361890063` in N1 and `0.002493264858180868` in N2.

These are archived observations, not yet a promoted interpretation.

## Resume rule

A future session should:

1. read this checkpoint;
2. read `D01C_PREEXECUTION_FREEZE_v0.1.json`;
3. read `results/D01C_ARCHIVAL_RECORD_v0.1.json`;
4. read `D01C_LITERATURE_POSITION.md`;
5. reproduce if needed with `python chi_architecture/reproduce.py d01c`;
6. interpret D01C against the standard nonmodal toolkit;
7. preserve the rule that established transient-growth/resolvent mathematics is not SymC novelty;
8. create a new version before any new scalar, metric, parameter range, or post-result targeted experiment.

## Next scientific action

Create the D01C scientific readout and decide whether the broader Chi framing contributes anything beyond established nonmodal/state-space analysis.

If the standard toolkit is already sufficient, record that explicitly rather than manufacturing added value.
