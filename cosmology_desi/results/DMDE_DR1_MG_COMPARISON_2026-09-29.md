# DESI DR1 DM/DE Modified-Gravity Adversary

Flat LambdaCDM background retained; mu0 and Sigma0 are added perturbation-sector parameters.

- mu0 = 0.087179 [-0.38048, 0.60650]; GR reference = 0
- mu(a=1) = 1.0872 [0.61952, 1.6065]; GR reference = 1
- Sigma0 = 1.3324 [0.14378, 2.4757]; DESI-only direct constraint not admitted
- Omega_m baseline -> MG: 0.29612 [0.28687, 0.30566] -> 0.29545 [0.28608, 0.30523]
- sigma8 baseline -> MG: 0.84091 [0.80787, 0.87529] -> 0.83766 [0.80447, 0.87223]
- S8 baseline -> MG: 0.83562 [0.80133, 0.87104] -> 0.83145 [0.79689, 0.86729]
- H0 baseline -> MG: 68.566 [67.829, 69.310] -> 68.521 [67.781, 69.270]

Core median shifts relative to the baseline posterior width are small: Omega_m -0.071 sigma, sigma8 -0.096 sigma, H0 -0.060 sigma, and S8 -0.119 sigma. Their posterior widths change by only about 0.5-2.0%.

The dominant new degeneracy is between mu0 and logA, with weighted posterior correlation r = -0.829. Correlations of mu0 with sigma8 and S8 are much smaller, -0.190 and -0.206 respectively. Allowing the MG degree of freedom therefore broadens logA strongly (SD ratio 1.80) while leaving the directly reported late-time clustering amplitudes comparatively stable.

## Interpretation guardrails

DESI FS+BAO alone does not directly constrain Sigma0; its marginal shape is strongly affected by the hard prior mu0 < 2*Sigma0 + 1. The one-sided Sigma0 interval is not a detection.

All parameter-shift measures are descriptive because the posteriors are nested and use the same DESI data. The sampled minimum chi-square values are not used for model selection.

The DESI mu(a)-Sigma(a) functional form ties late-time deviations to the dark-energy density. Any redshift trend implied by that functional form must be separated from information supplied by the data itself.