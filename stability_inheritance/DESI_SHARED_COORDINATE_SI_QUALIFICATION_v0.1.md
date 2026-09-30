# DESI Shared-Coordinate Stability-Inheritance Qualification v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0 + mandatory Continuity Hardening Addendum
**Stage:** P0-Q representation qualification
**Evidence class:** PUBLIC EXTERNAL POSTERIOR / ADVERSARIAL REPRESENTATION TEST
**P1 eligibility:** NO
**Source status:** already-downloaded official DESI DR1 full-shape posterior chains on Popstop, all chain files SHA-256 verified against the frozen transport receipts before this protocol.

## Purpose

Use DESI as an SI representation stress test, not as a new dark-energy/dark-matter claim.

The parent cosmology work already established two critical facts:

1. in flat GR late-time background cosmology, the published scalar balance coordinate is algebraically dependent on the native background model and therefore cannot by itself establish an independent capital-Chi architecture;
2. the DESI DR1 full-shape baseline reproduction passed its preregistered native-model gate, licensing use of the full baseline posterior for matter-side investigation.

The SI question is therefore whether a perturbation that changes the allowed gravitational/growth response can reorganize the **relationship among shared background, growth, and tracer-response coordinates** in a way that is not exhausted by any one scalar or marginal block.

This is a representation-qualification test. It is not a test of whether modified gravity is true and it does not compare cosmological model preference.

## Frozen source pair

### Baseline
Official DESI DR1 chain family:

`cobaya/base/desi-reptvelocileptors-fs-bao-all_schoneberg2024-bbn_planck2018-ns10/`

Four full chain files, verified aggregate size 992,643,390 bytes.

### Growth-sector adversary
Official DESI DR1 chain family:

`cobaya/base_mu_sigma/desi-reptvelocileptors-fs-bao-all_schoneberg2024-bbn_planck2018-ns10/`

Four full chain files. This family is used only as a controlled perturbation of the growth/gravity sector.

**Critical anti-leakage rule:** model-specific parameters `mu0` and `Sigma0` are excluded from every representation score, classifier, distance, covariance comparison, and added-information calculation. They may be reported later only as native-model context.

## Shared coordinate blocks

### Background block B

Use only coordinates present in both chains:

- `omegam`
- `H0`
- `rdrag`

The published scalar balance coordinate may be derived from `omegam` only for descriptive overlay after the primary block analysis. It is not an independent input feature.

### Growth block G

Use:

- `sigma8`
- `s8h5`
- `s8omegamp5`
- `s8omegamp25`

These are native/derived DESI posterior growth-amplitude summaries. None is renamed lowercase chi or capital Chi.

### Tracer-response block T

Use the seven per-tracer likelihood coordinates shared by both chains:

- `Lya_z0.loglikelihood`
- `QSO_z0.loglikelihood`
- `ELG_z1.loglikelihood`
- `LRG_z2.loglikelihood`
- `LRG_z1.loglikelihood`
- `LRG_z0.loglikelihood`
- `BGS_z0.loglikelihood`

These are treated as a response-organization vector, not independent observations and not a physical modal basis.

### Joint conglomerate block C

[
C = B oplus G oplus T.
]

The term conglomerate here means the joint organization/covariance of admitted shared coordinates. It does not by itself define (Chi_{mathrm{arc}}).

## Primary quantities

All summaries are posterior-weighted.

For B, G, T, and C separately:

1. weighted mean vector;
2. weighted covariance and correlation matrix;
3. effective sample size (N_{mathrm{eff}}=(sum w)^2/sum w^2);
4. pooled-standardized mean-shift norm between baseline and adversary;
5. covariance-reorganization distance using the Frobenius norm of the difference between pooled-standardized correlation matrices.

For the B-G relationship:

6. largest canonical correlation (ho_{BG,1}) in each posterior;
7. full canonical-correlation spectrum where numerically identified;
8. change in the B-G canonical spectrum between baseline and adversary.

For added representation value:

9. five-fold weighted logistic discrimination of baseline versus adversary using B only, G only, T only, B+G, and C;
10. folds are assigned deterministically by source-chain identity and within-chain row index modulo five;
11. all features are standardized inside each training fold only;
12. report weighted held-out log loss and ROC AUC;
13. primary added-value contrasts are:
   - C versus B;
   - C versus G;
   - C versus T;
   - B+G versus max(B,G).

The model-specific (mu_0,Sigma_0) coordinates are never classifier inputs.

## Interpretation rules

Return **JOINT_REORGANIZATION_ADDS** only if:

- C improves held-out log loss over B, G, and T individually;
- B+G improves over both B and G individually;
- and at least one independent relationship diagnostic shows reorganization: either the B-G canonical spectrum changes beyond chain-to-chain robustness variation or the pooled-standardized C correlation-matrix distance exceeds both corresponding B-only and G-only distances.

Return **MARGINAL_BLOCK_SUFFICIENT** if one marginal block matches or exceeds the joint representation within chain-to-chain robustness variation.

Return **JOINT_DIFFERENCE_REDUNDANT** if the joint representation discriminates but its gain over the best marginal block is negligible relative to chain-to-chain variation.

Return **REPRESENTATION_INDETERMINATE** if chain-to-chain variation, numerical rank, effective sample size, or posterior-weight concentration prevents stable ordering.

Return **REPRESENTATION_REFUSED** if shared-coordinate correspondence is broken or the classifier requires model-only parameters to discriminate.

No numeric universal threshold is introduced. Ordering must be robust to leave-one-source-chain-out summaries.

## Function / Limit interpretation

A positive result would establish only that a controlled cosmological growth-sector perturbation can reorganize joint shared-coordinate structure beyond a marginal scalar/growth description.

It would **not** establish:
- modified gravity;
- dark matter or dark energy ontology;
- SI as a cosmological mechanism;
- a new field or force;
- lowercase (chi);
- capital (Chi);
- (Chi_{mathrm{arc}});
- predictive superiority over (Lambda)CDM.

A null/redundant result is equally informative: it would show that, for this DESI posterior pair and these shared coordinates, the apparent architecture is adequately compressed by a marginal block.

## Protected next stage

No alternative DE chain, supernova suite, neutrino chain, new feature, threshold, or transformed coordinate may be selected after seeing this result without a new protocol.

The three frozen DE comparator suites remain separate future adversaries and are not part of v0.1.
