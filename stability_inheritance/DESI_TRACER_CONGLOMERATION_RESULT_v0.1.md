# DESI Tracer Vector-vs-Scalar Conglomeration Result v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0 + mandatory Continuity Hardening Addendum
**Protocol:** `DESI_TRACER_CONGLOMERATION_QUALIFICATION_v0.1.md`
**Analyzer:** `analyze_desi_tracer_conglomeration_v0_1.py`
**Execution:** Popstop against the same verified DESI DR1 baseline and `base_mu_sigma` posterior families as the parent SI test
**Full local result:** `C:\Users\CCGTi\Documents\SymC\Foundations\cosmology_desi\results\desi_tracer_conglomeration_v0_1.json`
**Full result SHA-256:** `3460333fbf62183669559ef68ed5e3de42eb6e60e38e6bbe5354fe4b1f0ee77f`
**Disposition:** `TRACER_VECTOR_ADDS_OVER_SCALAR_FIT`
**P1 eligibility:** NO

## Primary LOSC result

The scalar total tracer fit was defined prospectively as

[
S=sum_{j=1}^{7}ell_j.
]

The full tracer vector was

[
T=(ell_{m Lyalpha},ell_{m QSO},ell_{m ELG},ell_{m LRG2},ell_{m LRG1},ell_{m LRG0},ell_{m BGS}).
]

Training-fold-only linear residualization removed the summed-fit direction to form the residual-composition vector (R).

Four-fold leave-one-original-chain-out mean metrics:

| Representation | Log loss | ROC AUC |
|---|---:|---:|
| Scalar total S | 0.677594 | 0.610378 |
| Full tracer vector T | 0.668370 | 0.630477 |
| Residual composition R | 0.680355 | 0.590242 |
| S + R | 0.668370 | 0.630477 |

The S+R and T results agree to approximately (4.5	imes10^{-10}) in mean log loss, confirming the residualization/reconstruction implementation.

## Frozen decision conditions

- T beat S in 4/4 LOSC folds.
- S matched or beat T in 0/4 folds.
- R beat the balanced intercept-only reference with AUC > 0.5 in 4/4 folds.
- No single tracer matched or beat the full T vector in pooled LOSC log loss.
- Removing one tracer never erased the T-over-S gain in 3/4 or 4/4 folds.

Therefore the frozen disposition is:

**TRACER_VECTOR_ADDS_OVER_SCALAR_FIT**

## Single-tracer results

Pooled LOSC log loss / AUC:

- Ly-alpha: 0.693143 / 0.501241
- QSO: 0.689288 / 0.544494
- ELG: 0.692400 / 0.524684
- LRG2: 0.692889 / 0.515106
- LRG1: 0.692698 / 0.517495
- LRG0: 0.684217 / 0.589952
- BGS: 0.684824 / 0.562852

LRG0 and BGS are the strongest individual tracers, but neither reaches the full-vector performance.

## Leave-one-tracer-out robustness

Pooled LOSC log loss / AUC after removing each tracer:

- without Ly-alpha: 0.668363 / 0.630503
- without QSO: 0.674102 / 0.616126
- without ELG: 0.670323 / 0.623208
- without LRG2: 0.668526 / 0.630722
- without LRG1: 0.668533 / 0.628955
- without LRG0: 0.677172 / 0.601674
- without BGS: 0.677126 / 0.612564

LRG0 and BGS carry substantial parts of the vector advantage, but removal of either does not satisfy the preregistered single-tracer-dependence rule. No one tracer is sufficient to explain the full T-over-S result.

## SI interpretation

This is a positive **representation-qualification** result.

For the declared task of distinguishing the two DESI posterior families using only coordinates common to both, the pattern across tracer responses contains held-out information that cannot be compressed without loss into the scalar summed tracer fit.

The residual tracer composition remains informative after removing the total-fit direction. This directly demonstrates a case where scalar compression loses relational/vector information.

This does **not** establish:
- a physical cosmological mode;
- a new gravitational degree of freedom;
- a cosmological SI mechanism;
- capital (Chi);
- (Chi_{m arc});
- preference for modified gravity;
- a DM/DE ontology claim.

The tracer vector is an observational/likelihood response organization, not a physical modal basis.

## Function / Limit map

Function:
- `TRACER_VECTOR_ADDS_OVER_SCALAR_FIT`
- `RESIDUAL_TRACER_COMPOSITION_INFORMATIVE_AFTER_SCALAR_REMOVAL`
- `DISTRIBUTED_MULTI_TRACER_INFORMATION`

Limits:
- `TRACER_VECTOR_IS_NOT_PHYSICAL_MODAL_BASIS`
- `MODEL_FAMILY_DISCRIMINATION_IS_NOT_MODEL_PREFERENCE`
- `VECTOR_ADDED_VALUE_DOES_NOT_ESTABLISH_SI_MECHANISM`
- `LRG0_AND_BGS_CARRY_DISPROPORTIONATE_BUT_NOT_SUFFICIENT_SIGNAL`

## Next question

The parent joint model already showed that (B+G+T) improves over marginal blocks. The next required distinction is whether this is merely additive information from separate blocks or whether **cross-block relationships** between background/growth and tracer composition add held-out information beyond the additive representation.

That question must be frozen separately before interaction features are evaluated.
