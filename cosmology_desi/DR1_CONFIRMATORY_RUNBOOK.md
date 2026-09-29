# DESI DR1 Full-Shape Confirmatory Runbook

This runbook executes the confirmatory growth gate without changing the scientific definitions frozen in `DR1_FULL_SHAPE_GROWTH_GATE.md`. The exact target is the DESI DR1 `desi-reptvelocileptors-fs-bao-all_schoneberg2024-bbn_planck2018-ns10` chain family. The `all` suffix is intentional because Ly\(\alpha\) BAO contributes to background geometry in the published FS+BAO baseline while contributing no full-shape growth measurement.

The first command downloads only the five compact official chain files and verifies them against DESI's release SHA-256 manifest:

```bash
python cosmology_desi/prepare_dr1_fullshape_confirmatory.py --dependency-check
```

This creates an untracked workspace under `cosmology_desi/.external/dr1_fullshape/`. It does not download the four posterior chains and does not run an inference.

To pin the official DESI implementation at its frozen upstream commit and download the packaged HDF5 likelihood inputs:

```bash
python cosmology_desi/prepare_dr1_fullshape_confirmatory.py \
  --clone-implementation \
  --likelihood-data \
  --dependency-check
```

The upstream source remains outside the repository history. No upstream code is vendored because the pinned repository root does not contain an explicit license file.

The confirmatory reproduction target is

\[
\Omega_{\mathrm m,0}=0.2962\pm0.0095,
\qquad
\sigma_8=0.842\pm0.034,
\]

for DESI (FS+BAO)+BBN+\(n_{\mathrm{s10}}\). Reproduction is accepted only if the central values fall within \(0.25\sigma\) of the published values and the 68% interval widths agree within 15%. A miss triggers root-cause analysis rather than retuning.

The four released MCMC chains total \(992{,}643{,}390\) bytes. They are not needed for the configuration/provenance preflight. Download them only when posterior-sample-level derivation is required:

```bash
python cosmology_desi/prepare_dr1_fullshape_confirmatory.py --full-chains
```

Those downloads are resumable and hash-verified. Once present, the chains can be read directly for sample-level native growth/background reconstructions without rerunning the expensive DESI likelihood. A fresh likelihood run remains a separate reproducibility check.

The order after transport qualification is: inspect the official `chain.input.yaml` and `chain.updated.yaml`; verify native priors and component paths; reproduce the published \(\Omega_{\mathrm m,0}\) and \(\sigma_8\) posterior; freeze the mock-derived candidate matter representation; validate it on the 25 held-out AbacusSummit cut-sky mocks; only then evaluate the real DESI data for candidate \(\Chi_{\mathrm m}(k,a)\), \(\mathcal A_{\Chi}^{\mathrm{cosmo}}\), or any later \(\mathcal T_{\mathrm{SI}}\).


## Adversarial released-chain preparation

The same transport runner can prepare the pinned DESI-only modified-gravity chain without changing its evidentiary role:

```bash
python cosmology_desi/prepare_dr1_fullshape_confirmatory.py \
  --chain-key modified_gravity \
  --dependency-check
```

This model is the first clean growth-sector adversary and is evaluated only after the baseline reproduction passes. Full modified-gravity posterior chains total approximately 1.466 GB and therefore remain opt-in with `--full-chains`.

The released DESI-only (w_0w_a) chain can be prepared with `--chain-key w0wa_desi_only_stress`, but its role is deliberately restricted to projection/stability stress testing. It is **not** the physical dark-energy comparator. DESI's published DR1 full-shape analysis identifies strong projection effects in the DESI-only (w_0w_a) posterior, so the physical DE lane requires a frozen DESI+CMB+SN combination.

The neutrino lane remains intentionally unresolved at the transport layer. A DESI-only (base_mnu) chain matching the exact baseline likelihood has not yet been qualified in the public release tree. Unless such a chain is located and hash-pinned, the scale-dependent-neutrino adversary requires a fresh run of the official DESI likelihood.
