# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02B-CP2-SCHEMA-ACQUISITION-IMPLEMENTED  
**Date:** 2026-09-22  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.3  
**CP1 source contract:** 8f818467dc0fcd467883edf85fc4b212393b02a7

## State

The selected source contract remains frozen.

A GitHub Actions schema-only acquisition lane now:

1. downloads the publisher source workbook;
2. downloads the archived author code;
3. records source sizes and SHA-256 hashes;
4. inspects workbook sheet names/dimensions/cell types/string labels only;
5. deliberately omits numeric cell values.

Workflow:

.github/workflows/chi-architecture-d02b-schema.yml

Schema acquisition script:

chi_architecture/d02b/acquire_schema.py

## Resume rule

Check the first successful D02B Source Schema Lock workflow.

If acquisition fails mechanically, repair URLs/HTTP handling only. Do not change the scientific source contract.

If it succeeds, archive the run/artifact/hash record and use sheet names/string labels to freeze the exact sheet/column extraction map before numerical cell values are read.
