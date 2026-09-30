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

## Adversarial update — 2026-09-29

Official DESI `iminuit` posterior-maximization products were checked for the matched baseline and DESI-only mu-Sigma models. The baseline optimizer reports chi2 = 331.86911. The mu-Sigma optimizer reports chi2 = 332.86328 despite two additional gravity parameters, so the extension does not improve the matched DESI-only fit at the published optimizer point. Its optimizer also places Sigma0 = 2.9999586, effectively the upper prior boundary, while mu0 = 0.03554. Together with the analytically induced marginal prior geometry and DESI's published interpretation, Sigma0 is classified as poorly identified by DESI-only clustering rather than anomalous.

The public DESI DR1 `cobaya/base_mnu` directory was re-inspected. It contains CMB-combined DESI full-shape families but no exact DESI-only FS+BAO + Schoneberg-2024 BBN + wide-ns baseline counterpart. Therefore the matched DESI-only free-neutrino lane remains `FRESH_RUN_REQUIRED`; no CMB-combined chain may be substituted for the null-matched adversary. CMB-combined neutrino chains remain admissible later for the physical multi-probe neutrino constraint lane.

The DESI-only w0wa chain is now being prepared strictly under its frozen role `projection_stress_test_only`; it cannot be promoted to the physical dark-energy comparator.


## Fresh DESI-only free-neutrino run activation — 2026-09-30

The previously frozen `FRESH_RUN_REQUIRED` lane has advanced to `ACTIVE_RUN_PUBLIC_RELEASE_IMPLEMENTATION`. No exact released DESI-only `base_mnu` chain exists for the matched FS+BAO + Schoneberg-2024 BBN + wide-`n_s` dataset, so a fresh public-release likelihood run is now active on the Victus desktop.

Reproducibility and implementation gates completed before launch:

- the exact released baseline chain set was copied to the Victus and all nine baseline files independently re-verified against the frozen SHA-256 receipts;
- the public DESI DR1 full-shape likelihood source was frozen at commit `7d51f4f86dc3bee6bf10f1a684913c943a89a844`;
- all 66 downloaded DESI likelihood HDF5 products pass the release SHA-256 manifest;
- the inference environment is Python 3.11, Cobaya 3.5, CAMB 1.5.4, with pinned source snapshots for `cosmoprimo`, `lsstypes`, and `velocileptors`;
- the public likelihood was cross-qualified against the released private/internal DESI likelihood component. Across six baseline-chain states spanning internal FS+BAO chi2 from 2387.60 down to 342.86, public-minus-internal delta-chi2 ranged from -0.474 to +0.242, and at the two low-chi2 states it was -0.0151 and +0.0158;
- a separate varying-neutrino qualification used released DESI+CMB `base_mnu` samples only as implementation test vectors, never as a substitute scientific result. At the best DESI-compatible row in successive neutrino-mass bins from 0.014 to 0.129 eV, public-minus-internal delta-chi2 was 0.836, 0.804, 0.789, 0.719, and 0.892. The 0.173 span is consistent with a near-common likelihood normalization shift across the directly tested mass region.

The exact private Y1 production repository is not publicly accessible, while DESI's DR1 release documentation designates the public full-shape likelihood repository as the reproducible implementation for cosmological inference. Accordingly, the fresh run is defined by the public-release implementation, not claimed as byte-for-byte replication of the private production code.

Frozen scientific configuration:

- model: flat `base_mnu`;
- data: DESI DR1 FS+BAO all tracers + Schoneberg-2024 BBN + Planck-2018 `n_s10`;
- `sum mnu` prior: [0, 5] eV;
- three degenerate massive neutrino eigenstates, matching the DESI `base_mnu` convention;
- fixed `tau=0.0544`, `N_eff=3.044`, `w=-1`, `wa=0`, `Omega_k=0`;
- all baseline nuisance priors and analytic marginalization settings retained;
- released baseline covariance retained for all pre-existing sampled parameters, with one independent initial `mnu` covariance dimension added for proposal learning;
- Cobaya convergence target retained at `Rminus1_stop=0.01` and `Rminus1_cl_stop=0.2`.

Execution identity:

- machine: HP Victus 15L, Ryzen 5 5600G, 6 cores / 12 threads, 7.34 GB usable RAM;
- concurrency ceiling: one full likelihood worker to avoid memory-pressure false liveness;
- detached process PID at launch: `17948`;
- launch time: 2026-09-30 08:27:58 America/Chicago;
- active local output: `cosmology_desi/.external/dr1_fullshape/fresh_mnu/fresh_run/chain*`;
- checkpoint, covariance, input, updated-config, progress, and frozen-input files were present immediately after initialization;
- sampler reached `Sampling!` with all 24 sampled-parameter covariance entries loaded.

Promotion guard: the chain may explore the full frozen [0,5] eV prior, but if material posterior support lies above the directly qualified public/internal mass range, the result remains `NEEDS_IMPLEMENTATION_SENSITIVITY_CHECK` until that high-mass region is adversarially tested. No prior truncation or outcome-dependent restriction is permitted.
