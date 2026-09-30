# DESI Cross-Block Logistic Convergence Validity Audit v0.1

**Date:** 2026-09-30
**Governance:** SymC GOM v1.0 + mandatory Continuity Hardening Addendum
**Trigger:** pre-result `ConvergenceWarning` observed during active v0.1c execution
**Scientific design change:** NONE
**Status:** FROZEN BEFORE v0.1c disposition is known

## Purpose

The active `DESI_CROSS_BLOCK_RELATIONAL_V01C` run uses the frozen unpenalized logistic objective, `lbfgs`, `tol=1e-8`, and `max_iter=400`.

Before any final v0.1c disposition was observed, one or more fits emitted scikit-learn `ConvergenceWarning` indicating that the iteration limit was reached.

A classifier metric from a non-converged numerical optimizer is not sufficient for final scientific adjudication. This audit therefore treats convergence as an implementation-validity condition, not as a new scientific choice.

## Rules

1. Allow the active v0.1c run to complete unchanged. Do not alter or restart it midstream.
2. Preserve its raw output, warnings, metrics, and disposition as provenance.
3. If no fit emitted `ConvergenceWarning`, no recovery run is required.
4. If any fit emitted `ConvergenceWarning`, the raw v0.1c disposition is **provisional** until a convergence-qualified same-design rerun is completed.
5. The recovery may change only the numerical iteration ceiling and add convergence telemetry:
   - objective: unchanged, unpenalized logistic;
   - solver: unchanged, `lbfgs`;
   - tolerance: unchanged, `1e-8`;
   - features, rows, weights, folds, residualization, interactions, pairing-destroyed control: unchanged;
   - storage/memmap implementation: unchanged;
   - raise `max_iter` from 400 to 2000;
   - record `n_iter_` for every A, X, and X_shift fit.
6. A recovery fit is convergence-qualified only when it terminates without `ConvergenceWarning` before the 2000-iteration ceiling.
7. If any required fit still reaches the 2000-iteration ceiling, stop as `MECHANICAL_NUMERICAL_CONVERGENCE_BLOCK`. Do not change solver, regularization, tolerance, features, scaling, or scientific design without a new explicit gate.
8. If all required fits converge, the convergence-qualified metrics supersede the raw v0.1c metrics for the three-result adjudication.
9. Report raw-vs-qualified metric differences fold by fold. No post-result tolerance threshold is introduced; the frozen scientific disposition is recomputed from the original decision rules using the convergence-qualified metrics.

## Interpretation ceiling

This audit can validate or invalidate the numerical execution of the frozen representation test. It cannot strengthen the scientific claim, introduce a new model family, or authorize lowercase chi, capital Chi, or Chi_arc.

## Stop

After convergence-qualified completion, persist the result identity and proceed directly to the already-frozen `DESI_THREE_RESULT_CONGLOMERATION_ADJUDICATION_PLAN_v0.1.md`.
