# DESI Tracer Vector-vs-Scalar Conglomeration Qualification v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0 + mandatory Continuity Hardening Addendum
**Stage:** post-result P0-D decomposition / representation qualification
**Parent result:** `DESI_SHARED_COORDINATE_SI_RESULT_v0.1.md`
**Status:** FROZEN BEFORE EXECUTION
**P1 eligibility:** NO

## Trigger

The parent DESI SI test returned `JOINT_DIFFERENCE_REDUNDANT`.

The background-growth canonical relationship did not reorganize beyond source-chain variation, but the seven-tracer response vector T carried substantially more model-family discrimination than the background or growth blocks.

This follow-up asks whether that T advantage is genuinely vector/relational information or merely a redundant expansion of one scalar: total tracer fit quality.

## Frozen source pair

Use exactly the same SHA-256 verified baseline and `base_mu_sigma` DESI DR1 full-shape posterior chain files as the parent test.

No new model family, dataset, chain, tracer, cosmological parameter, or posterior transformation may be added.

Model-only `mu0` and `Sigma0` remain prohibited inputs.

## Tracer coordinates

Let

[
T=(ell_{m Lyalpha},ell_{m QSO},ell_{m ELG},ell_{m LRG2},ell_{m LRG1},ell_{m LRG0},ell_{m BGS}),
]

using the same seven released per-tracer log-likelihood coordinates as the parent protocol.

Define the scalar total

[
S = sum_{j=1}^{7} T_j.
]

No nonlinear rescaling or learned scalar compression is permitted.

## Residual composition R

Within each training fold only, fit the weighted linear expectation of each tracer likelihood from S:

[
T_j = a_j+b_j S+epsilon_j.
]

The seven residuals (epsilon_j) form the residual-composition block R for that fold.

Test-fold residuals must use coefficients fitted only on the training fold.

R therefore asks whether the **distribution of fit across tracers** contains information after the global fit-quality direction is removed.

## Primary validation

Use the same four-fold leave-one-original-chain-out pairing as v0.1a:

- fold j tests baseline chain j and adversary chain j;
- the other six source chains train;
- posterior weights are retained;
- class total training weights are normalized equally;
- standardization and residualization are training-fold only.

## Frozen comparisons

Evaluate weighted held-out log loss and ROC AUC for:

1. S only;
2. T full vector;
3. R residual composition only;
4. S + R, which should span the same information class as T up to numerical regression representation;
5. each single tracer (T_j);
6. seven leave-one-tracer-out vectors (T_{-j}).

## Decision rules

Return **TRACER_VECTOR_ADDS_OVER_SCALAR_FIT** if:
- T has lower pooled LOSC log loss than S;
- T beats S in at least 3/4 LOSC folds;
- R has AUC above 0.5 and lower log loss than an intercept-only balanced classifier in at least 3/4 folds;
- and no single tracer alone matches or beats T in pooled LOSC log loss.

Return **TRACER_SIGNAL_SCALAR_COMPRESSIBLE** if S matches or beats T in pooled LOSC and in at least 3/4 folds.

Return **TRACER_VECTOR_SINGLE_TRACER_DEPENDENT** if T beats S but one single tracer matches/beats T, or removal of one tracer erases the T-over-S gain in at least 3/4 folds.

Return **TRACER_VECTOR_DISTRIBUTED_BUT_WEAK** if T robustly beats S but R does not robustly beat the balanced intercept-only reference.

Return **REPRESENTATION_INDETERMINATE** if the ordering is not stable across source-chain folds.

## Interpretation ceiling

A positive vector-over-scalar result would qualify only the statement that the released tracer response pattern contains model-family information beyond total fit quality.

It would not establish:
- a physical cosmological mode;
- SI mechanism;
- capital Chi;
- Chi_arc;
- modified-gravity preference;
- dark-matter or dark-energy ontology.

A scalar-compressible result is a direct SI Limit Map result: the apparent seven-component organization would not justify a conglomerate interpretation for this declared task.

## Stop rule

After this decomposition, stop before introducing another cosmological model or dataset. Any next move must be chosen from the Function/Limit outcome of this test and separately frozen.
