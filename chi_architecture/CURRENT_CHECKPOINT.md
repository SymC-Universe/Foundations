# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02A-CP1-SOURCE-SCHEMA-LOCKED  
**Date:** 2026-09-22  
**Branch:** `chi-architecture-p0`  
**CP0 scientific freeze:** `27164b36a0c3ecd1931cfe8cdf840f6fc7b9fbb6`  
**Protocol:** SymC GOM v0.8.3

## Source integrity checkpoint

The schema-only workflow completed successfully before scientific numeric values were inspected.

- workflow run: `35815354508`
- artifact: `chi-architecture-d02a-source-schema-v01`
- artifact ID: `10732010233`
- artifact digest: `sha256:77f862cda4d2e277f39e9048876edd9b190db0e0a0f5d7e06bf8ae8f3f8e0ead`
- FIG3 SHA-256: `6db8784c4e8e95c560ccce0bebe70b86dfc7613cccfe62853dc7eec7a25a1a0a`
- FIG4 SHA-256: `938d401c4b6ce766244d2c1dba9edd5d0804067ec8d21b5d43379241bab78bf5`

No scientific numeric values were emitted by the schema stage.

## Frozen parser surface

Source/header roles are locked in:

`chi_architecture/d02_cspbbr3/D02A_SOURCE_SCHEMA_LOCK_v0.1.json`

Value extraction rules are locked in:

`chi_architecture/d02_cspbbr3/D02A_PARSER_CONTRACT_v0.1.json`

The parser may now inspect values only through those schema-defined sheets, columns, and rows.

## Critical scientific guard

The M-point linewidth table alone does **not** license lowercase chi.

`linewidth != Gamma` until the 2021 DHO convention is documented, and `Gamma` alone is insufficient without a same-condition `omega0`.

Therefore stage 1 may legitimately return:

`DHO_CONVENTION_AMBIGUOUS`

or

`OMEGA0_NOT_IDENTIFIABLE`

while still completing a physical linewidth/carrier map.

## Resume rule

1. Read CP0, this checkpoint, the source schema lock, and parser contract.
2. Implement the parser without changing scientific ranges.
3. Fetch the exact source workbooks and verify the locked SHA-256 values.
4. Extract all schema-defined values.
5. Audit the 2021 DHO method convention separately from the numerical result.
6. Do not fit or backsolve `omega0` from the plotted DHO curve unless a new fit contract is frozen before doing so.
7. Archive extracted values + DHO license decision as CP2 before joint chi/Chi interpretation.
8. Reproduction target remains `python chi_architecture/reproduce.py d02a`.
