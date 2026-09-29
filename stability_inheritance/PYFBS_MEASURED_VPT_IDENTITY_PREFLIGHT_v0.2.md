# pyFBS Measured VPT Identity Preflight v0.2

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** FROZEN P0-Q DATA/TRANSFORM IDENTITY PREFLIGHT
**Predecessor:** PYFBS_LAB_COMPONENT_ASSEMBLY_PROTOCOL_v0.1.md -> INVALID_TEST
**Target scoring:** PROHIBITED in this preflight
**P1 status:** INELIGIBLE

## Reason for new version

The v0.1 measured component-to-assembly test failed before scoring because `coupling_example.xlsx` describes response/input dimensions that do not match measured `Y_A.p`, `Y_B.p`, and `Y_AB.p`. The preserved identity audit subsequently established that `AM_Measurements.xlsx` has channel/impact counts matching the measured FRF objects: A = 6, B = 21, AB = 27.

This v0.2 preflight is a new post-result P0-Q object. It does not alter or overwrite the v0.1 INVALID_TEST.

## Frozen source identities

Measured FRFs:
- Y_A.p SHA-256 3b8ece8b2b80b63e209427518cd6521c8028042ff1d79ff04e5de5f657a13db4
- Y_B.p SHA-256 2e4a83f4ce1b87e773c5872764c4e4bd11f71b256a11964ac7574a81feeeed12
- Y_AB.p SHA-256 197deff3bc1f546bc1653ecb877d34dece01dfc1d360217dc903f4d1a694d4d7

Positional metadata:
- AM_Measurements.xlsx SHA-256 b70f1abcf9f64cdd02140380fa6fc25a27d1ad463a734bf0346f316140acc4c8

Runtime source base:
https://gitlab.com/pyFBS/pyFBS_data/-/raw/master/lab_testbench/Measurements/

## Allowed operations

1. Download and hash-check Y_A.p, Y_B.p, and AM_Measurements.xlsx.
2. Read only shapes, frequency vectors, and official A/B positional metadata.
3. Instantiate the documented pyFBS VPT for A and B using AM_Measurements.xlsx.
4. Apply VPT to measured A and B FRFs.
5. Record transformation-matrix shapes, transformed FRF shapes, finite-value checks, and any pyFBS exception.

## Prohibited operations

- do not download or inspect Y_AB values for scoring;
- do not compare a component prediction with assembly response;
- do not choose output indices based on target performance;
- do not change metadata after seeing transformed target behavior;
- do not infer empirical Stability Inheritance.

## Frozen disposition

- VPT_ROUTE_EXECUTABLE if both A and B transforms complete, transformed arrays are finite, and frequency dimension is preserved.
- VPT_ROUTE_NOT_EXECUTABLE if the official matching metadata still cannot transform the measured component FRFs.
- INVALID_TEST if source identity/hash/frequency alignment fails.

A VPT_ROUTE_EXECUTABLE outcome permits construction of a separately frozen v0.2 component-to-assembly scoring protocol. It does not authorize scoring by itself.
