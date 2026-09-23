# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02D-CP2C-RESOURCE-NAMES-NORMALIZED  
**Date:** 2026-09-23  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.4

## State

The D02D MFR-14 remains frozen.

A CKAN metadata-only source lock is implemented. It resolves:

- README.pdf;
- DAM3 010 and 111;
- DAM4 010 and 111;
- DAM6 010 and 111.

No ZIP or PDF source bytes are opened by this checkpoint.

## Resume rule

1. Observe the first successful resource-lock workflow.
2. Archive the exact resource IDs, URLs, sizes, repository hashes, and package metadata hash.
3. Download README plus one representative ZIP for schema/path inspection only.
4. Freeze channel mapping, sampling, file pairing, mode-selection implementation, uncertainty calculation, and environmental matching before reading damaged-state modal results.

## Mechanical CKAN-name correction

The first resource-lock run reached the CKAN API successfully but five reader-facing resource labels did not exactly match the API's internal names. The metadata script now emits the complete API resource-name inventory and missing-name list without opening source bytes. Scientific selection and MFR-14 remain unchanged.

## External-search adjudication

The completed D02D literature audit challenged but did not displace LUMO. Competing candidates retained unresolved eligibility axes; LUMO remains selected under the frozen criteria.

## CKAN name normalization

Five CKAN resource names contain doubled whitespace not shown in the reader-facing page. Matching now normalizes whitespace while preserving the API name and canonical reader-facing name separately.
