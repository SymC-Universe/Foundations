# DESI-for-SI Preliminary Prior-Art and Novelty Gate v0.1

**Date:** 2026-09-30
**Governance:** SymC GOM v1.0 + mandatory Continuity Hardening Addendum
**Stage:** P0-N preliminary novelty map
**Status:** PRELIMINARY; not a final novelty claim
**Outcome firewall:** written while convergence-qualified DESI cross-block v0.1d is still running; no v0.1d disposition used.

## Scope

This audit asks which parts of the current DESI-for-SI methodology are already established in cosmology/statistics and which combination may remain worth a deeper novelty search.

The current SI method is deliberately not a model-selection claim. It stages representation qualification:

1. scalar/background and growth blocks;
2. multicomponent tracer-response vector versus scalar summed fit;
3. residual composition after removal of the scalar fit direction;
4. additive multiblock representation;
5. explicit cross-block interaction representation;
6. pairing-destroyed negative control;
7. source-chain-held-out validation;
8. prospective refusal/adjudication rules.

## Strong prior art: not novel by itself

### DESI full-shape and modified-gravity posterior inference

DESI Collaboration, *DESI 2024 VII: Cosmological Constraints from the Full-Shape Modeling of Clustering Measurements*, arXiv:2411.12022.

Established prior art includes DESI full-shape + BAO posterior inference for flat LambdaCDM and extensions, including growth/amplitude quantities and modified-gravity constraints.

M. Ishak et al., *Modified Gravity Constraints from the Full Shape Modeling of Clustering Measurements from DESI 2024*, arXiv:2411.12026.

Established prior art includes the time-dependent `mu-Sigma` parameterization and DESI full-shape constraints on departures from GR. Therefore the present use of the official `base_mu_sigma` posterior as an adversarial source family is not itself novel.

D. Gonzalez et al., *Testing Scale-Dependent Modified Gravity with DESI DR1*, arXiv:2604.26915.

Current DESI work already tests scale-dependent MG, parameter degeneracies, tracer-separated robustness, and neutrino interactions. Any SI novelty claim must therefore avoid generic statements such as “DESI can reveal scale-dependent organization” or “different tracers respond differently to MG.”

### Multitracer structure

The cosmological multitracer technique and cross-tracer information are established prior art. Examples include:
- *Cosmological constraints from multiple tracers in spectroscopic surveys*, MNRAS 473 (2018);
- later multitracer DESI forecasting/analysis pipelines.

Thus “a vector of multiple tracers contains more information than one tracer” is not a novel claim.

### Classifier two-sample testing

D. Lopez-Paz and M. Oquab, *Revisiting Classifier Two-Sample Tests*, arXiv:1610.06545.

Using held-out binary classification to determine whether two sample distributions differ is established statistical methodology.

Classifier two-sample tests are also used in modern cosmological simulation-based inference evaluation. Therefore using logistic discrimination/AUC/log loss between posterior families is not independently novel.

### Cosmological model comparison and posterior diagnostics

Bayes factors, likelihood ratios, information criteria, posterior predictive checks, frequentist profile likelihoods, and posterior-distribution diagnostics are extensively established.

Recent DESI frequentist work, arXiv:2508.11811, further emphasizes that extended-model Bayesian posteriors can show strong prior-volume/projection effects. This is directly relevant to the SI Limit Map: posterior-family discriminability must not be interpreted as physical model preference.

## Candidate novelty: requires deeper search

The current literature pass did **not** identify an obvious prior instance of the complete following prospective sequence applied to released cosmological posterior/likelihood-response coordinates:

1. test an intentionally scalar compression;
2. prove held-out added information in the full response vector;
3. regress out the scalar direction and require residual composition to remain informative;
4. combine native cosmological coordinates and scalar-removed response composition additively;
5. add explicit cross-block products;
6. destroy only sample-level cross-block pairing while preserving marginal coordinates and within-response composition;
7. require the observed pairing representation to beat both the additive model and the pairing-destroyed feature-count-matched control;
8. adjudicate the result through prospectively frozen Function/Limit outcomes rather than model-preference language.

This **combination** is the only currently plausible methodological novelty target.

It should provisionally be described as:

`PROSPECTIVE_SCALAR_VECTOR_RELATIONAL_REPRESENTATION_QUALIFICATION`

and not as a discovery of a new cosmological mode or a new model-selection statistic.

## Important novelty risks

1. **Classifier novelty risk:** C2ST and classifier-based discrepancy tests are mature prior art.
2. **Interaction-feature novelty risk:** pairwise feature interactions and permutation controls are generic statistical tools.
3. **Multitracer novelty risk:** tracer combination and cross-tracer covariance are mature cosmological methodology.
4. **Posterior-geometry risk:** baseline-versus-MG posterior discrimination may encode prior geometry, nuisance structure, or inference construction rather than physical organization.
5. **Likelihood-coordinate risk:** per-tracer log-likelihood contributions are analysis-response variables, not physical state variables.
6. **Selection risk:** the present DESI source pair was scientifically motivated and frozen, but final novelty claims require testing whether the methodology generalizes beyond this one posterior-family pair.

## Current novelty ceiling

Until a deeper systematic literature search is completed, the defensible statement is:

> The individual ingredients are established. The potentially distinctive contribution is the preregistered decomposition-and-refusal workflow that asks, in sequence, whether scalar compression loses information, whether vector composition survives scalar removal, and whether observed cross-block pairing itself adds information beyond additive and pairing-destroyed controls.

No claim of field-first novelty is yet authorized.

## Next novelty work after numerical validity closes

After v0.1d and the frozen three-result adjudication:
- conduct a deeper search specifically for interaction/permutation-based posterior two-sample diagnostics in cosmology;
- search information-decomposition and conditional-dependence tests applied to per-probe/per-tracer likelihood contributions;
- compare against likelihood-free inference diagnostics and posterior predictive discrepancy frameworks;
- classify the resulting SI methodology as native-equivalent, adaptation, composition-level novelty, or genuinely new method.

Do not broaden the scientific DESI evidence set during this novelty search.
