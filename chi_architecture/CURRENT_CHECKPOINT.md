# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02A-CP2-V0.1-PARTIAL  
**Date:** 2026-09-22  
**Branch:** `chi-architecture-p0`  
**Execution commit:** `9709b8f5a3a19197fad957d9b757b24d190d5519`  
**Workflow run:** `35815810797`  
**Artifact ID:** `10731497089`  
**Protocol:** SymC GOM v0.8.3

## Official v0.1 result

`PARTIAL_VALID_LINEWIDTH__CARRIER_PARSER_INADEQUATE__CHI_REFUSED`

Trusted source extraction:

- FIG3 source hash matched;
- FIG4 source hash matched;
- six-row M-point linewidth table is valid;
- lowercase chi is refused because same-condition omega0 is not available in the locked tabulation.

Not admissible:

- v0.1 FIG3 A:C carrier extraction;
- v0.1 direct DHO plotting-curve standardized residual.

See:

- `d02_cspbbr3/D02A_V0.1_POSTEXECUTION_INTEGRITY_AUDIT.md`
- `results/D02A_EXECUTION_ARCHIVE_v0.1.json`

## Resume rule

1. Preserve v0.1 unchanged as the official prospective parser result.
2. Build v0.2 only from a new full-workbook layout diagnostic.
3. Mark v0.2 as post-result parser development.
4. Do not alter the valid 4b linewidth values.
5. Do not promote chi.
6. Re-freeze the exact FIG3 grid reconstruction before using any corrected carrier values for interpretation.
7. Only then test physical preservation/transformation/reorganization against the native phonon comparator.
