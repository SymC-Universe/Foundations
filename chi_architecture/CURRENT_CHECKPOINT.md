# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02B-CP5-EXACT-MAPPING-FROZEN  
**Date:** 2026-09-22  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.3

## Stage A status

Stage A completed successfully without emitting scientific CSV values.

Workflow: 35819369668  
Artifact ID: 10732747680  
Artifact digest: sha256:47a5c916566541b422e0429e37d34012350b78da69e935f6b4ad1d965be0bb7f

## Frozen mapping

Exact file/column selection and the raw half-power scalar algorithm are frozen in:

chi_architecture/d02b/D02B_EXACT_SOURCE_MAPPING_v0.1.md

## Permission boundary

Processed table numerical values may now be inspected under the frozen mapping.

The 635.4 MB raw archive remains unopened.

Before raw extraction:
1. inspect processed values;
2. record retained group IDs and torque-state identifiers;
3. implement raw archive acquisition/checksum logic;
4. checkpoint that implementation;
5. only then read raw FRFs.
