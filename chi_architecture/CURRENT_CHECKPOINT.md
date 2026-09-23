# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02A-CP2.2-V0.2-PARSER-FROZEN  
**Date:** 2026-09-22  
**Parent:** D02A-CP2.1-V0.2-LAYOUT-DIAGNOSTIC  
**Status:** post-result parser development / frozen before corrected carrier extraction

## Corrected FIG3 geometry

The v0.2 layout diagnostic established that the experimental Figure 3 source sheets are matrices.

- 300 K orthorhombic: q `A3:A23`, E `B3:B48`, S(Q,E) `C3:W48` = 46 x 21.
- 385 K tetragonal: q `A3:A23`, E `B3:B40`, S(Q,E) `C3:W40` = 38 x 21.
- 419 K cubic M-R block: q `A66:A86`, E `B66:B86`, S(Q,E) `C66:W86` = 21 x 21.

All three q axes span the same 21 source points from 0.5 to 1.0 rlu.

The corrected parser contract is:

`chi_architecture/d02_cspbbr3/D02A_V0.2_CARRIER_PARSER_CONTRACT.json`

## Comparison rule

Absolute intensity is not compared across SPINS and CNCS.

The frozen cross-phase comparison uses only per-q normalized energy-distribution shape on the common source-supported window 0.0-2.2 meV and a fixed 0.2 meV grid.

Per-q outputs are energy centroid, RMS width, and peak-energy location. Pairwise outputs are descriptive RMS differences and correlations only. No categorical similarity threshold is introduced.

## Evidence firewall

v0.2 is post-result parser development and cannot become untouched confirmation.

The v0.1 partial result remains official and preserved.

Lowercase chi remains refused. No DHO parameter fitting is authorized.

## Resume rule

1. Read the v0.1 integrity audit and preserve it unchanged.
2. Read the v0.2 parser contract before executing corrected carrier values.
3. Implement the three exact matrix ranges without value-dependent exclusions.
4. Verify the locked FIG3 SHA-256 before parsing.
5. Reconstruct every frozen matrix cell.
6. Compare carrier shape only after per-q normalization on the frozen common grid.
7. Archive the corrected output before interpretation.
8. Do not call the result inheritance by threshold; assess preservation/transformation/reorganization against native phonon analysis after archival.

## Next action

Implement and execute the v0.2 corrected matrix parser through the one-command D02A path.
