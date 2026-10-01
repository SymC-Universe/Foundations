# DESI Cross-Block Relational Result v0.1c — Provisional Numerical Result

**Date:** 2026-09-30
**Governance:** SymC GOM v1.0 + mandatory Continuity Hardening Addendum
**Protocol:** `DESI_CROSS_BLOCK_RELATIONAL_QUALIFICATION_v0.1.md`
**Mechanical repair lineage:** v0.1a + v0.1b + v0.1c
**Execution:** Popstop, exact verified DESI DR1 baseline + `base_mu_sigma` source pair
**Full local result:** `C:\Users\CCGTi\Documents\SymC\Foundations\cosmology_desi\results\desi_cross_block_relational_v0_1c.json`
**Result SHA-256:** `54d76ed074d31dce99e06fa92be7ea068d656962711a4432e29a13d0bba05252`
**Raw disposition:** `CROSS_BLOCK_RELATIONSHIP_ADDS`
**Validity status:** `PROVISIONAL_NUMERICAL_CONVERGENCE`
**P1 eligibility:** NO

## Raw frozen-design result

The exact interaction-builder equivalence guard passed:
- rows checked = 1024;
- exact allclose = true;
- maximum absolute difference = 0.

Four-fold leave-one-source-chain-out mean metrics:

| Representation | Log loss | ROC AUC |
|---|---:|---:|
| Additive A | 0.6629694083 | 0.6478719357 |
| Relational X | 0.6557921524 | 0.6617139016 |
| Pairing-destroyed X_shift | 0.6633069441 | 0.6468739468 |

Frozen decision diagnostics:
- X beat A in 4/4 folds;
- X beat X_shift in 4/4 folds;
- A matched/beat X in 0/4 folds;
- pooled X beat A;
- pooled X beat X_shift.

Thus the raw decision rule returns `CROSS_BLOCK_RELATIONSHIP_ADDS`.

## Numerical validity hold

During execution, multiple required unpenalized `lbfgs` fits emitted scikit-learn `ConvergenceWarning` because the frozen `max_iter=400` ceiling was reached.

The warning was observed and `DESI_CROSS_BLOCK_CONVERGENCE_VALIDITY_AUDIT_v0.1.md` was frozen **before the final v0.1c disposition was exposed**.

Therefore the raw disposition is preserved as evidence but cannot enter final three-result SI adjudication until the same scientific design is rerun under the frozen convergence audit:
- same source rows and posterior weights;
- same features and order;
- same residualization and standardization;
- same 49 interactions;
- same pairing-destroyed control;
- same four LOSC folds;
- same unpenalized logistic objective;
- same `lbfgs` solver;
- same `tol=1e-8`;
- only `max_iter` increases 400 -> 2000 and per-fit convergence telemetry is recorded.

## Scientific ceiling

No final relational-conglomeration claim is made from this provisional result. If the convergence-qualified rerun preserves the frozen decision ordering, the already-frozen three-result adjudication plan applies. If convergence fails again, stop as a mechanical numerical-convergence block rather than retuning the science.
