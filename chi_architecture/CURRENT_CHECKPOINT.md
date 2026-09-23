# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02D-CP3-SOURCE-LOCKED-SCHEMA-PROBE-IMPLEMENTED  
**Date:** 2026-09-23  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.4

## Source lock

CKAN resource lock passed.

Run:
35901853086

Artifact:
d02d-lumo-resource-lock-v01

Artifact ID:
10769004313

Artifact digest:
sha256:05ad421db9c7884234d627eaf89a880f15748806b426b4a1f9dd9ad8fd4a6b23

Permanent source mapping:

chi_architecture/d02d/D02D_LUMO_SOURCE_LOCK_v0.1.json

## Schema probe

DAM3 010 is selected for schema inspection only because it is the smallest decisive archive by CKAN file size.

The probe:
- downloads the archive and README;
- records SHA-256 hashes;
- lists ZIP paths/sizes/CRC;
- inspects up to eight MAT members with scipy.io.whosmat;
- does not load or emit scientific arrays.

## Resume rule

1. Observe the schema workflow.
2. Freeze exact MAT variable/channel mapping from schema only.
3. Freeze the estimator implementation, uncertainty/bootstrap counts, environmental matching, and mode-family selection.
4. Commit the production Engine and tests.
5. Only then open damage-state scientific array values.
