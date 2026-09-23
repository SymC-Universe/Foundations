# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02B-CP4-STAGE-A-IMPLEMENTED  
**Date:** 2026-09-22  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.3  
**Active source contract:** D02B_FOUR_BOLT_SOURCE_CONTRACT_v0.3.md

## State

Stage A acquisition is implemented.

It downloads only:

- 01_documentation.zip
- 02_processed_tables.zip
- 04_scripts.zip

from Zenodo, verifies the published MD5 checksums, records SHA-256 hashes, and emits:

- archive file names;
- contained file names/sizes/CRC;
- CSV headers and row counts only.

Scientific CSV cell values are deliberately withheld at this checkpoint.

## Resume rule

1. Inspect the successful Stage A schema artifact.
2. Freeze the exact table/column/file mapping for D02B.
3. Only then permit numerical processed-table inspection.
4. Raw 00_raw_exports.zip remains unopened until the numeric mapping is frozen.
