# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02B-CP2B-ORION-MANIFEST-IMPLEMENTED  
**Date:** 2026-09-22  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.3  
**Active source contract:** D02B_ORION_SOURCE_CONTRACT_v0.2.md

## State

The Orion selection correction is active.

A metadata-only GitHub Actions lane now probes the public Mendeley dataset page and candidate public API endpoints to recover file/download metadata without opening MAT/ASCII response values.

Workflow:

.github/workflows/chi-architecture-d02b-orion-manifest.yml

Script:

chi_architecture/d02b/orion_public_manifest.py

## Resume rule

1. Inspect the first successful manifest artifact.
2. Use only file names, directory structure, sizes, hashes, and download endpoints to freeze the exact source-file subset.
3. Do not inspect scientific response values before that file-selection freeze.
4. If public API access is unavailable, use links embedded in the public page or the repository's documented download-all path; any mechanical acquisition workaround must be committed before data inspection.
