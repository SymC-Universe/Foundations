# Fine Steering Mirror Cross-Amplitude P0-Q Protocol v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** FROZEN BEFORE RAW TEST SCORING
**Evidence class:** public measured external benchmark / P0-Q only
**Scientific ceiling:** representation transport and regime qualification only

## Frozen question

Does a single linear MIMO frequency-response representation adequately transport across the 100, 200, and 300 mV operating amplitudes, or does the declared task require amplitude-conditioned response representations?

This is not an inheritance claim. It is a measured-data representation/transport test.

## Data partition

For each amplitude:
- official train realizations R1-R6, both steady-state periods;
- fit realizations: R1-R4;
- internal validation realizations: R5-R6;
- official test realizations: all R_test=3, both periods.

No official test value may influence regularization, frequency-bin selection, or model definition.

## Frozen representation

At each DFT frequency bin, estimate the complex 3x3 linear frequency-response matrix G(f) from U to Y.

For a set of training columns q spanning realizations and periods:

Y_f = G_f U_f + error.

Estimate G_f by complex ridge regression.

### Amplitude-specific representations
Fit G_100, G_200, G_300 separately.

### Pooled representation
Fit G_pool using the fit realizations from all three amplitudes together.

## Frozen regularization

For every candidate model, choose one global relative ridge value from:

0, 1e-12, 1e-10, 1e-8, 1e-6, 1e-4, 1e-2.

At each frequency, define ridge magnitude as:

lambda_abs = lambda_rel * trace(U U^H) / 3.

Select lambda_rel by minimum normalized spectral prediction error on the internal validation realizations only.

After selection, refit that representation using all six official train realizations at its declared amplitude set.

## Frozen frequency support

Define the scored excitation support from TRAIN data only.

For each frequency bin, compute total pooled training input spectral energy. Retain positive-frequency bins, excluding DC/Nyquist, whose training energy exceeds 1e-12 times the maximum pooled training-bin energy.

This threshold is numerical support detection only, not a scientific transition threshold.

The same frozen bin set is used for every amplitude/model comparison.

## Frozen metrics

For every official test amplitude and candidate representation report:

1. relative complex spectral error:
   sqrt(sum ||Y-GU||_F^2 / sum ||Y||_F^2)
   over the frozen excitation-support bins and all test realizations/periods;

2. per-output relative spectral errors;

3. pairwise normalized representation distance between fitted G_100, G_200, G_300:
   sqrt(sum ||Ga-Gb||_F^2 / sum ||Ga||_F^2)
   over the frozen bins;

4. pooled-vs-amplitude-specific representation distances.

No chi scalar is computed.

## Frozen categorical dispositions

For each test amplitude a:

- AMPLITUDE_SPECIFIC_BEST if G_a has strictly lower total relative spectral error than G_pool and both cross-amplitude G models.
- POOLED_BEST if G_pool has strictly lower total error than all three amplitude-specific G models.
- CROSS_AMPLITUDE_BEST if an amplitude-specific model from another amplitude has the lowest error.
- MIXED_OR_TIED if exact ordering cannot be established.

Overall:
- AMPLITUDE_CONDITIONED_REPRESENTATION_REQUIRED_FOR_TASK only if AMPLITUDE_SPECIFIC_BEST occurs at all three amplitudes.
- POOLED_LINEAR_REPRESENTATION_SUFFICIENT_FOR_TASK only if POOLED_BEST occurs at all three amplitudes.
- otherwise MIXED_AMPLITUDE_TRANSPORT.

Strict ordering is descriptive. Without a repeatability-derived equivalence margin, tiny numerical differences are not promoted as physically meaningful effect sizes.

## Native comparator firewall

Amplitude-dependent behavior and hysteresis are established benchmark science. A finding that amplitude-conditioned linear representations perform better is not SI novelty.

The official benchmark also has stronger linear state-space and nonlinear LFR baselines. This P0-Q test cannot claim state-of-the-art predictive value.

## Failure consequence

If frequency-domain estimation is rank-deficient or numerically unstable on the declared support despite frozen ridge handling, record METHOD_SCOPE_TEST_FAILED or INDETERMINATE. Do not inspect the official test set to redesign the estimator.

If a cross-amplitude model performs unexpectedly best, preserve that outcome; do not retune amplitude labels or model complexity.
