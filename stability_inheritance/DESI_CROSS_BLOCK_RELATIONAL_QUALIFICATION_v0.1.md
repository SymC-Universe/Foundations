# DESI Cross-Block Relational Conglomeration Qualification v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0 + mandatory Continuity Hardening Addendum
**Stage:** P0-Q / post-result relational representation qualification
**Parents:** `DESI_SHARED_COORDINATE_SI_RESULT_v0.1.md`, `DESI_TRACER_CONGLOMERATION_RESULT_v0.1.md`
**Status:** FROZEN BEFORE EXECUTION
**P1 eligibility:** NO

## Trigger

Two prospectively bounded DESI-for-SI results are now established:

1. the shared-coordinate joint block discriminates the baseline and growth-sector-adversary posteriors better than background, growth, or tracer blocks alone, but the background-growth canonical relation does not reorganize beyond source-chain variation; disposition `JOINT_DIFFERENCE_REDUNDANT`;
2. the seven-tracer response vector contains robust held-out information beyond the summed tracer-fit scalar, including informative residual composition after the scalar fit direction is removed; disposition `TRACER_VECTOR_ADDS_OVER_SCALAR_FIT`.

The remaining representation question is whether the tracer-composition information merely adds beside the background/growth coordinates or whether **sample-level relationships between the blocks** add held-out information.

## Frozen source pair and firewall

Use exactly the same verified four baseline and four `base_mu_sigma` DESI DR1 chain files.

No new model, dataset, tracer, parameter, threshold, cosmological extension, or outcome transformation is allowed.

`mu0` and `Sigma0` remain prohibited classifier inputs.

## Base additive representation A

Use:

- background block B: `omegam`, `H0`, `rdrag`;
- growth block G: `sigma8`, `s8h5`, `s8omegamp5`, `s8omegamp25`;
- scalar tracer total (S=sum_j T_j);
- residual tracer composition R obtained exactly as in the parent tracer protocol by training-fold-only weighted linear residualization of each tracer likelihood against S.

Define

[
A = Boplus Goplus Soplus R.
]

A is an additive joint representation.

## Cross-block relational representation X

Within each training fold:

1. standardize B+G and R using training data only;
2. construct all pairwise products between the seven B+G coordinates and the seven residual-composition coordinates;
3. append those 49 products to A.

Thus

[
X = A oplus [(Boplus G)otimes R].
]

The interaction block tests representation-level cross-block dependence. It is not interpreted as a physical interaction term.

## Pairing-destroyed control X_shift

Construct a matched negative control that preserves every marginal coordinate and the internal tracer-composition vector while breaking sample-level pairing between B+G and R.

Within each model class and original source chain independently, circularly shift the complete R row vector by

[
Delta n=max(1,lfloor n/3floor)
]

before constructing the 49 cross-products.

The additive A features remain unshifted.

This produces `X_shift`: the same feature count and marginal distributions as X, but with the declared cross-block pairing disrupted.

## Validation

Primary validation is four-fold leave-one-original-chain-out, paired by chain index exactly as in the parent protocols.

All residualization, scaling, and interaction construction are training-fold bounded.

Use unpenalized logistic discrimination for A, X, and X_shift. Posterior weights are retained and model-class total weights are balanced.

Report weighted held-out log loss and ROC AUC.

## Decision rules

Return **CROSS_BLOCK_RELATIONSHIP_ADDS** only if:
- X has lower pooled LOSC log loss than A;
- X beats A in at least 3/4 LOSC folds;
- X has lower pooled LOSC log loss than X_shift;
- X beats X_shift in at least 3/4 LOSC folds.

Return **CROSS_BLOCK_ADDITIVE_SUFFICIENT** if A matches or beats X in pooled LOSC and in at least 3/4 folds.

Return **INTERACTION_GAIN_PAIRING_NONESSENTIAL** if X robustly beats A but does not robustly beat X_shift.

Return **CROSS_BLOCK_RELATIONSHIP_INDETERMINATE** otherwise.

## Interpretation ceiling

A positive result would qualify only that **sample-level relationships between the admitted background/growth coordinates and scalar-removed tracer composition carry model-family information beyond additive concatenation**.

It would not establish:
- causal coupling;
- a new cosmological mode;
- a physical SI transfer mechanism;
- capital (Chi) or (Chi_{m arc});
- modified-gravity preference;
- dark-sector ontology.

A pairing-nonessential result would be a refusal of a stronger conglomeration interpretation: nonlinear feature expansion may help, but not because the observed B/G-to-tracer pairing itself is necessary.

## Stop rule

After this test, update the SI Function and Limit maps. Do not add another DESI model family until the three-result sequence is conglomerated and its scientific ceiling is explicitly adjudicated.
