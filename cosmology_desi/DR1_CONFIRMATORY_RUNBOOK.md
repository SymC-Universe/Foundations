# DESI DR1 Full-Shape Confirmatory Runbook

This runbook executes the confirmatory growth gate without changing the scientific definitions frozen in \`DR1_FULL_SHAPE_GROWTH_GATE.md\`. The exact target is the DESI DR1 \`desi-reptvelocileptors-fs-bao-all_schoneberg2024-bbn_planck2018-ns10\` chain family. The \`all\` suffix is intentional because Ly\(\alpha\) BAO contributes to background geometry in the published FS+BAO baseline while contributing no full-shape growth measurement.

The first command downloads only the five compact official chain files and verifies them against DESI's release SHA-256 manifest:

\`\`\`bash
python cosmology_desi/prepare_dr1_fullshape_confirmatory.py --dependency-check
\`\`\`

This creates an untracked workspace under \`cosmology_desi/.external/dr1_fullshape/\`. It does not download the four posterior chains and does not run an inference.

To pin the official DESI implementation at its frozen upstream commit and download the packaged HDF5 likelihood inputs:

\`\`\`bash
python cosmology_desi/prepare_dr1_fullshape_confirmatory.py \
  --clone-implementation \
  --likelihood-data \
  --dependency-check
\`\`\`

The upstream source remains outside the repository history. No upstream code is vendored because the pinned repository root does not contain an explicit license file.

The confirmatory reproduction target is

\[
\Omega_{\mathrm m,0}=0.2962\pm0.0095,
\qquad
\sigma_8=0.842\pm0.034,
\]

for DESI (FS+BAO)+BBN+\(n_{\mathrm{s10}}\). Reproduction is accepted only if the central values fall within \(0.25\sigma\) of the published values and the 68% interval widths agree within 15%. A miss triggers root-cause analysis rather than retuning.

The four released MCMC chains total \(992{,}643{,}390\) bytes. They are not needed for the configuration/provenance preflight. Download them only when posterior-sample-level derivation is required:

\`\`\`bash
python cosmology_desi/prepare_dr1_fullshape_confirmatory.py --full-chains
\`\`\`

Those downloads are resumable and hash-verified. Once present, the chains can be read directly for sample-level native growth/background reconstructions without rerunning the expensive DESI likelihood. A fresh likelihood run remains a separate reproducibility check.

The order after transport qualification is: inspect the official \`chain.input.yaml\` and \`chain.updated.yaml\`; verify native priors and component paths; reproduce the published \(\Omega_{\mathrm m,0}\) and \(\sigma_8\) posterior; freeze the mock-derived candidate matter representation; validate it on the 25 held-out AbacusSummit cut-sky mocks; only then evaluate the real DESI data for candidate \(\Chi_{\mathrm m}(k,a)\), \(\mathcal A_{\Chi}^{\mathrm{cosmo}}\), or any later \(\mathcal T_{\mathrm{SI}}\).
