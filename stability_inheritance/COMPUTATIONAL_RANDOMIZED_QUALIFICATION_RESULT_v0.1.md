# Stability Inheritance Randomized Computational Qualification Result v0.1

**Date:** 2026-09-28  
**Protocol freeze commit:** 09e407e32ceed906e1c507add4b2afbcfa0a7c11  
**Master seed:** 2026092802  
**Status:** P0-Q RANDOMIZED COMPUTATIONAL QUALIFICATION ONLY  
**Script SHA256:** 1c5e33805c4e2892e9720f6f4c48816404fea73415161c0e0a7120f85170cc50  
**Result JSON SHA256:** 93a8f184c04a513a239b1e7bc5068d86769a690ea782a6455e81c69042e4a4a8

The protocol was committed before this randomized ensemble was generated.

## RQ-1 - same scalar spectrum / randomized modal geometry

500 parent pairs.

- maximum scalar-spectrum difference = 4.44e-16;
- response-ratio p05 = 1.0068;
- median = 1.3146;
- p95 = 2.9589;
- maximum = 6.3261;
- near-null fraction ratio < 1.02 = 10.6%;
- non-null fraction ratio > 1.20 = 59.8%.

**Disposition:** METHOD_SCOPE_TEST_PASSED. Identical scalar spectra coexist with both near-null and large task-level response differences depending on modal/interface geometry.

## RQ-2 - randomized non-proportional damping

500 / 500 mathematically valid draws.

- off-diagonal-damping / reconstruction-error correlation = 0.68684;
- error p05 = 0.01057;
- median = 0.10018;
- p95 = 0.33569;
- maximum = 0.61924.

**Disposition:** METHOD_SCOPE_TEST_PASSED. Independent mode scalars lose response information as non-classical damping structure becomes important, but no universal cutoff is licensed.

## RQ-3 - fixed spectrum / randomized non-normal geometry

500 systems, every one retaining eigenvalues {-1,-2}.

- gain p05 = 1.0;
- median = 3.8235;
- p95 = 7.1429;
- maximum = 7.5020;
- low-gain fraction < 1.1 = 14.8%;
- high-gain fraction > 2 = 74.6%.

**Disposition:** METHOD_SCOPE_TEST_PASSED. Spectrum alone is not a sufficient transient-stability representation for this family.

## RQ-4 - hidden-state memory identifiability

300 randomized oscillators with chronological held-out testing.

- AR(2) better overall = 63.33%;
- high-SNR (>100) cases: AR(2) better = 100% (n=142);
- low-SNR (<10) cases: AR(2) better = 22.5% (n=80);
- log-SNR / log-advantage correlation = 0.89961.

**Disposition:** METHOD_SCOPE_TEST_PASSED because both predeclared regimes occurred. Mathematical history dependence and operationally useful history estimation separate cleanly.

## RQ-5 - direct Chi_arc reference independence

300 randomized known-truth assemblies.

- absolute predictor-corruption / prediction-error correlation = 0.82905;
- error p05 = 0.01846;
- median = 0.19242;
- p95 = 0.63794;
- maximum = 0.85637;
- zero predictor corruption has expected numerical-zero error.

**Disposition:** METHOD_SCOPE_TEST_PASSED. The direct reference remains independent while predictor quality changes.

## Overall disposition

All five randomized protocol tests passed their precommitted method-scope criteria.

This does **not** mean Stability Inheritance is empirically confirmed. The result qualifies representation/refusal behavior over the declared synthetic ensemble and adds Limit Map detail, especially the high-SNR/low-SNR separation for history identification.
