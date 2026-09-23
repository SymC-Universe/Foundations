# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02A-CP2.3-V0.2-IMPLEMENTED-PREOUTPUT  
**Date:** 2026-09-22  
**Parent:** D02A-CP2.2-V0.2-PARSER-FROZEN  
**Status:** post-result parser development / implementation complete before corrected carrier output

## Frozen v0.2 parser

`chi_architecture/d02_cspbbr3/D02A_V0.2_CARRIER_PARSER_CONTRACT.json`

The scientific ranges and transformations are fixed:

- 300 K: q A3:A23, E B3:B48, S C3:W48.
- 385 K: q A3:A23, E B3:B40, S C3:W40.
- 419 K M-R: q A66:A86, E B66:B86, S C66:W86.
- common q grid: the 21 source values 0.5-1.0 rlu.
- common comparison energy grid: 0.0-2.2 meV in 0.2 meV steps.
- absolute cross-instrument intensity comparison: forbidden.
- per-q normalization: positive-clipped interpolated intensity divided by its common-window sum.
- carrier metrics: energy centroid, RMS width, common-grid peak energy.
- pairwise outputs: descriptive RMS differences and Pearson correlations.
- categorical inheritance threshold: none.

## Implementation

New v0.2 code is isolated from the preserved v0.1 implementation:

- `chi_architecture/src/d02a_physical_v02.py`
- `chi_architecture/tests/test_d02a_physical_v02.py`

Reviewer entrypoint remains:

`python chi_architecture/reproduce.py d02a`

It now targets the corrected v0.2 carrier result while still retaining the valid v0.1 linewidth extraction and chi refusal.

Dedicated workflow:

`.github/workflows/chi-architecture-d02a.yml`

Expected single artifact:

`chi-architecture-d02a-physical-v02`

## Evidence firewall

The original prospective v0.1 result remains:

`PARTIAL_VALID_LINEWIDTH__CARRIER_PARSER_INADEQUATE__CHI_REFUSED`

v0.2 is a post-result parser repair. It cannot erase that failure or gain untouched confirmatory credit.

Lowercase chi remains refused before corrected carrier execution.

## Resume rule

1. Observe the first v0.2 D02A workflow.
2. If it fails mechanically, modify implementation only.
3. Do not change source hashes, matrix ranges, common energy window, normalization, or metrics after seeing corrected carrier output.
4. Archive exact workflow/artifact/result hashes as D02A-CP3 before interpretation.
5. Interpret only after CP3.
6. Compare the joint linewidth/carrier result against native q-resolved phonon analysis; if native phonon analysis already contains the whole result, record `NATIVE_PHONON_TOOLKIT_SUFFICIENT`.
