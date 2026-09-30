# DM + DE WORKING INVESTIGATION

Status: ACTIVE
Branch: `dm-de-investigation`
Scope: dark matter / dark energy cosmology only. Stability Inheritance, broader Χ architecture, and cross-project conglomeration are out of scope here and remain in the SI project.

## Frozen scientific question

Use DESI DR1/DR2 cosmological constraints to test the dark-sector model ladder against a flat ΛCDM null, while keeping modified gravity and neutrino physics as explicit competing explanations rather than folding them into dark-sector claims.

Current ladder:
1. flat ΛCDM baseline;
2. μ-Σ modified gravity as the first clean growth-sector adversary;
3. free neutrino mass as a scale-dependent growth alternative when an exact matched chain/run is qualified;
4. constant-w and w0wa dark-energy extensions;
5. physical w0wa sensitivity suite using DESI+CMB+Pantheon+, Union3, and DESY5;
6. interacting DM-DE models only after the observational null/adversary structure is established and a reproducible implementation is frozen.

No dark-sector interpretation may be promoted merely because an extension fits differently. Native parameter priors, projection effects, external-dataset dependence, and model dimensionality must be checked first.

## DESI DR1 baseline gate

The exact four released DESI DR1 FS+BAO baseline chains are present on Popstop and SHA-256 verified. Direct weighted analysis of 857,201 stored MCMC rows gives:

- H0 median 68.5663, 68% interval [67.8289, 69.3105]
- Omega_m median 0.296124, 68% interval [0.286870, 0.305657]
- sigma8 median 0.840907, 68% interval [0.807867, 0.875288]
- n_s median 0.994358, 68% interval [0.968051, 1.020545]
- minimum sampled chi2 = 343.0982

This independently reproduces the released compact summary and therefore passes the frozen baseline gate.

## First adversary: DESI-only mu-Sigma modified gravity

The exact four released μ-Σ chains are also present on Popstop and SHA-256 verified. Direct weighted analysis of 1,207,745 stored rows gives:

- mu0 median 0.0872, 68% interval [-0.3805, 0.6065]
- Sigma0 median 1.3324, 68% interval [0.1438, 2.4757]
- Omega_m median 0.295453, 68% interval [0.286080, 0.305228]
- sigma8 median 0.837664, 68% interval [0.804468, 0.872231]
- minimum sampled chi2 = 343.9817

The apparent positive Sigma0 marginal MUST NOT be interpreted as evidence against GR. The released DESI-only setup imposes the joint prior

```
mu0 < 2*Sigma0 + 1
mu0, Sigma0 in [-3,3]
```

which strongly reshapes the marginal prior for Sigma0. Under this prior alone, P(Sigma0>0)=17/21=0.8095, the prior median is 1.25, and the prior 16th/84th percentiles are approximately -0.167 and 2.44. The posterior values P(Sigma0>0)=0.8788, median=1.332, and [0.144,2.476] therefore lie close to the induced prior geometry. DESI's own published interpretation correspondingly quotes the DESI-only constraint on mu0, not Sigma0, and reports consistency with GR.

This is a Limit/interpretation result for the DM/DE program: DESI-only clustering does not license a Sigma0 anomaly claim from this marginal.

## Immediate next actions

1. Quantify baseline vs μ-Σ posterior shifts in shared cosmological parameters and compare likelihood maxima using the official DESI posterior-maximization products rather than MCMC minima.
2. Locate/qualify the exact matched DESI-only free-neutrino-mass chain, or retain fresh-run-required status if no matched public chain exists.
3. Execute the DESI-only w0wa chain strictly as a projection-stress test.
4. Pin hashes for the three physical DE sensitivity chains before opening their posterior results.
5. Only after these gates, open the interacting DM-DE literature/model lane and freeze a reproducible interaction parameterization and acceptance/refusal tests.
