# Randomized Computational Qualification Multi-Seed Reproducibility v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** P0-Q STATISTICAL REPRODUCIBILITY PROBE
**Master-seed runs:** 10
**All seed-level runs passed all predeclared family checks:** YES

## Purpose

Test whether the randomized computational qualification result depends materially on one master seed. This is a distributional/statistical reproducibility probe, not a bitwise-repeatability requirement and not empirical Stability Inheritance evidence.

## Results across 10 master seeds

| Metric | Min | Median | Max | Mean | SD |
|---|---:|---:|---:|---:|---:|
| RQ-1 response ratio > 1.20 fraction | 0.5000 | 0.5600 | 0.6250 | 0.5605 | 0.0427 |
| RQ-1 near-null ratio < 1.02 fraction | 0.0950 | 0.1300 | 0.1800 | 0.1340 | 0.0291 |
| RQ-2 off-diagonal damping / reconstruction-error correlation | 0.6549 | 0.7239 | 0.7631 | 0.7178 | 0.0347 |
| RQ-3 transient gain > 2 fraction | 0.6900 | 0.7275 | 0.7550 | 0.7200 | 0.0224 |
| RQ-4 AR(2) better overall | 0.6083 | 0.6458 | 0.7167 | 0.6517 | 0.0335 |
| RQ-4 high-SNR AR(2) better | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| RQ-4 low-SNR AR(2) better | 0.1154 | 0.1788 | 0.3333 | 0.2006 | 0.0796 |
| RQ-4 log-SNR / log-advantage correlation | 0.8504 | 0.8836 | 0.9345 | 0.8875 | 0.0255 |
| RQ-5 predictor-corruption / prediction-error correlation | 0.7386 | 0.7992 | 0.8416 | 0.7924 | 0.0304 |

## Interpretation

The synthetic Function/Limit behavior is statistically stable across independent seed realizations. The exact percentages move, as expected, but the qualitative structure does not flip:

- same scalar spectra produce both near-null and non-null response differences depending on modal/interface geometry;
- non-proportional damping content remains positively associated with independent-mode reconstruction error;
- fixed stable spectra continue to admit substantial non-normal transient amplification;
- high-SNR history closure wins in every seed-level probe, while low-SNR history closure is frequently not operationally useful;
- direct Chi_arc reference error increases with predictor corruption while the reference itself remains unchanged.

This satisfies the intended stochastic reproducibility class for the P0-Q synthetic qualification suite.

## Claim ceiling

No empirical, physical, or P1 claim is promoted. These are stochastic method-qualification results only.
