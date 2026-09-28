# pyFBS Lab Component-to-Assembly P0-Q Result v0.1

**Date:** 2026-09-28  
**Governance:** SymC GOM v1.0  
**Frozen protocol:** stability_inheritance/PYFBS_LAB_COMPONENT_ASSEMBLY_PROTOCOL_v0.1.md  
**Protocol commit:** 5485a57fda952547353fd72256de917e12c5869d  
**Workflow run:** 36499703108  
**Status:** INVALID_TEST  
**Scientific score produced:** NO  
**Empirical Stability Inheritance claim:** NONE

## Failure

The frozen protocol attempted to apply the six-DoF VPT defined by `coupling_example.xlsx` to the measured `Y_A.p` FRF object.

pyFBS failed before an assembly prediction or target score was produced:

`ValueError: matmul ... size 6 is different from 15`

The mismatch occurs inside the VPT matrix multiplication, showing that the measured FRF response dimension does not match the channel layout assumed by the frozen coupling metadata.

## GOM disposition

This result is **INVALID_TEST**, exactly as predeclared for a metadata/interface map that is not executable as frozen.

The test is not repaired in place by switching metadata, channels, VPT definition, or interface layout after target access.

No:
- E_FBS;
- E_UNCOUPLED;
- E_SHUFFLED;
- per-frequency score;
- outcome ordering

was produced.

## Root-cause interpretation

The public academic testbench packages several measurement/metadata configurations. The acquisition stage treated `coupling_example.xlsx` as the metadata companion to `Y_A.p`, `Y_B.p`, and `Y_AB.p`; the execution failure shows that this pairing is not operational for the measured VPT route as frozen.

This is a protocol/data-identity mismatch, not a failure of FBS and not a Stability Inheritance result.

## Consequence

- Preserve this invalid test in the failure ledger.
- Do not alter the frozen protocol and overwrite the failure.
- A new post-result P0-Q protocol may be constructed only after a metadata/shape identity pass determines which official positional-data object actually matches the measured FRFs.
- The new protocol remains public/seen P0-Q and cannot become P1.

## Next clean action

Run a **shape-and-metadata identity audit only**:
- report the raw FRF array shapes and frequency lengths without response values;
- hash and inspect official metadata candidates such as `AM_measurements.xlsx` and `decoupling_example.xlsx`;
- match response/input counts to metadata counts;
- then freeze a new native measured-data operation before any valid target scoring.
