# pyFBS Current-Metadata SVT Compatibility Preflight v0.3

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** FROZEN PRE-TARGET P0-Q COMPATIBILITY TEST
**Target Y_A:** MUST NOT BE DOWNLOADED
**Native source:** current maintained pyFBS SVT decoupling notebook
**Notebook SHA-256:** c19d6418c82c2d591ffaab38d0982dbd2920a0ad51408c3aff9681ad8b16bee6

## Why v0.3 is licensed

The current official pyFBS notebook audit found a material upstream metadata correction:

- current notebook: decoupling_example_SVT.xlsx
- prior failed Stability Inheritance route: decoupling_example.xlsx

The current notebook independently preserves:
- k = 6;
- grouping [1,10];
- B-derived SVT basis;
- same transform applied to B and AB;
- 18 x 18 decoupling block;
- A extraction at reduced indices 6:12.

This is an independently documented correction, not a target-driven retune.

## Frozen sources

Measured components:
- Y_B.p SHA-256 2e4a83f4ce1b87e773c5872764c4e4bd11f71b256a11964ac7574a81feeeed12
- Y_AB.p SHA-256 197deff3bc1f546bc1653ecb877d34dece01dfc1d360217dc903f4d1a694d4d7

Current metadata:
https://gitlab.com/pyFBS/pyFBS_data/-/raw/master/lab_testbench/Measurements/decoupling_example_SVT.xlsx

The metadata SHA-256 is recorded by this preflight and becomes frozen input identity for any later scoring protocol.

Package:
- pyFBS 1.0.6

## Frozen operation

1. Download and hash-check Y_B and Y_AB.
2. Download current decoupling_example_SVT.xlsx.
3. Read Channels_B, Impacts_B, Channels_AB, Impacts_AB.
4. Load and transpose B and AB FRFs exactly as the official notebook.
5. Construct:
   k = 6
   SVT(B, grouping=[1,10], no_svs=6)
6. Apply the same SVT to B and AB.
7. Record only source hashes, metadata row counts, transformed shapes, finite checks, and exceptions.

## Expected current-notebook shapes

- transformed B: frequency x 6 x 6
- transformed AB: frequency x 12 x 12

## Prohibited operations

- do not download Y_A;
- do not build the LM-FBS decoupling score;
- do not inspect a recovered A;
- do not alter k, grouping, metadata, channels, or package version after seeing any target.

## Dispositions

- CURRENT_SVT_ROUTE_EXECUTABLE if B and AB transform to the documented finite shapes.
- CURRENT_SVT_ROUTE_NOT_EXECUTABLE otherwise.
- INVALID_TEST for source identity/frequency/metadata read failure.

## Consequence

If executable, freeze a new measured SVT/LM-FBS scoring protocol using the exact metadata hash and route before downloading Y_A.

If not executable, close the released pyFBS measured SVT lane unless a later independently documented upstream correction appears.
