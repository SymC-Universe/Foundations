# DESI Cross-Block Relational Qualification v0.1b — Columnwise Standardization Repair

**Date:** 2026-09-29
**Parent:** `DESI_CROSS_BLOCK_RELATIONAL_QUALIFICATION_v0.1.md`
**Prior repair:** `DESI_CROSS_BLOCK_RELATIONAL_MEMORY_REPAIR_v0.1a.md`
**Failure class:** MECHANICAL_RESOURCE_ALLOCATION
**Scientific design change:** NONE
**Status:** FROZEN BEFORE RECOVERY EXECUTION

## Preserved v0.1a failure

The direct 2D interaction builder passed its exact 1024-row equivalence guard against the original `einsum(...).reshape(...)` construction.

The run then failed before any X-fold metric was produced because the weighted standardizer created full-matrix temporary arrays while computing

`(X - mean) ** 2`

for a training matrix of shape approximately (1{,}546{,}666	imes64), requiring an additional ~755 MiB temporary allocation.

The failure is implementation/resource only.

## v0.1b mechanical repair

Keep every scientific element unchanged.

Replace only full-matrix standardization temporaries with a float64 column loop:

For each feature (j):
1. compute weighted mean from (X[:,j]);
2. compute weighted variance using a single temporary vector (d=X[:,j]-mu_j);
3. standardize training column in place;
4. standardize test column in place;
5. discard the one-column temporary before proceeding.

No row, feature, weight, fold, interaction, control, threshold, classifier, or decision rule changes.

The interaction-builder equivalence guard remains mandatory.
