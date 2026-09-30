# DESI Cross-Block Relational Qualification v0.1a — Memory-Safe Mechanical Repair

**Date:** 2026-09-29
**Parent protocol:** `DESI_CROSS_BLOCK_RELATIONAL_QUALIFICATION_v0.1.md`
**Failure class:** MECHANICAL_RESOURCE_ALLOCATION
**Scientific design change:** NONE
**Status:** FROZEN BEFORE RECOVERY EXECUTION

## Preserved failure

The first Popstop execution of the frozen v0.1 analyzer failed before producing any fold metric or scientific disposition.

Failure:

`numpy._core._exceptions._ArrayMemoryError`

The implementation attempted to materialize an intermediate float64 tensor with shape

[
(1{,}546{,}666,7,7)
]

for one training-fold interaction block, requiring approximately 578 MiB before the final flattened matrix and other live arrays were considered.

No feature ordering, classifier result, fold result, or disposition was produced.

## Mechanical repair

v0.1a preserves exactly:

- all posterior rows;
- all posterior weights;
- B, G, S, and R definitions;
- training-fold residualization;
- training-fold standardization;
- all 49 ((B+G)	imes R) products;
- within-model/source-chain (n//3) pairing-destroyed control;
- four LOSC folds;
- unpenalized logistic classifier;
- decision rules.

The only implementation changes are:

1. allocate the final 2D interaction design matrix directly;
2. write each of the 49 float64 product columns one at a time instead of creating a 3D tensor;
3. evaluate A, X, and X_shift sequentially;
4. delete/free X before constructing X_shift;
5. use in-place standardization where supported.

No float32 conversion, sampling, row thinning, feature removal, or scientific simplification is permitted.

## Equivalence guard

Before full fitting, v0.1a must compare the columnwise interaction builder to the original `einsum(...).reshape(...)` construction on the first 1024 rows of the first available fold and require exact float64 equality within `np.allclose(..., rtol=0, atol=0)`.

Failure of that equivalence guard is a mechanical stop.
