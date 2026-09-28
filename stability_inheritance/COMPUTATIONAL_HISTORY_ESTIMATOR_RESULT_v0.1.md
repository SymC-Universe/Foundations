# Hidden-State History Estimator Qualification Result v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Protocol:** COMPUTATIONAL_HISTORY_ESTIMATOR_PROTOCOL_v0.1.md
**Protocol freeze commit:** 19a8d3982761754cd9bbe03ac1cb7f38be075e63
**Status:** P0-Q FRESH RANDOMIZED ESTIMATOR / IDENTIFIABILITY QUALIFICATION
**Evidence class:** synthetic known-truth / fresh after protocol freeze
**Master seed:** 2026092803
**Ensemble size:** 600
**Script SHA256:** 48eb78bc3df10a9baacd5447986ef3c8d1908e7d678cd671ad29bca412d8fb1c
**Result JSON SHA256:** 5d439ceed91f58e3018713aa0e0b9ae08cd1ae580c4dea6faf08f15eaa9f5519
**Empirical Stability Inheritance claim:** NONE

## Purpose

Distinguish two candidate explanations for the previously observed loss of AR(2) history-model advantage under noisy displacement observations:

1. estimator / errors-in-variables bias in the learned lag model;
2. a deeper measurement/operability limit in which the noisy lag coordinates themselves no longer carry enough usable information for the declared prediction task.

The protocol, fresh seed, ensemble generator, estimator classes, SNR bands, metrics, and interpretation rules were frozen before this ensemble was generated.

## Frozen estimators

- **E0:** AR(1) ordinary least squares.
- **E1:** AR(2) ordinary least squares.
- **E2:** centered AR(2) total least squares.
- **E3:** oracle exact discrete-time AR(2) recurrence implied by the known oscillator parameters, fed the same noisy observed lags. E3 is an upper-bound diagnostic, not an empirical method.

Primary score: one-step prediction RMSE against latent clean displacement.

## Results by predeclared SNR regime

### HIGH SNR > 100

n = 267

- E1 AR(2) OLS better than E0: 1.0000
- E1 median AR1/AR2 advantage ratio: 23.6084
- E2 TLS better than E0: 1.0000
- E2 median advantage ratio: 23.6080
- E3 oracle AR(2) better than E0: 1.0000
- E3 median advantage ratio: 23.6083
- oracle not better than AR(1): 0 / 267

**Disposition:** HISTORY_RECOVERABLE_WITH_DECLARED_ESTIMATOR.

### MID SNR 10 to 100

n = 204

- E1 AR(2) OLS better than E0: 0.7990
- E1 median advantage ratio: 1.90135
- E2 TLS better than E0: 0.7598
- E2 median advantage ratio: 1.88510
- E3 oracle AR(2) better than E0: 0.7598
- E3 median advantage ratio: 1.88517
- oracle not better than AR(1): 49 / 204 = 0.2402
- cases where oracle beat AR(1) but learned OLS AR(2) did not: 0

**Disposition:** mixed transition region. Both HISTORY_RECOVERABLE_WITH_DECLARED_ESTIMATOR and HISTORY_MEASUREMENT_LIMIT cases occur.

### LOW SNR < 10

n = 129

- E1 AR(2) OLS better than E0: 0.24031
- E1 median advantage ratio: 0.76471
- E2 TLS better than E0: 0.08527
- E2 median advantage ratio: 0.50361
- E3 oracle AR(2) better than E0: 0.08527
- E3 median advantage ratio: 0.50377
- oracle not better than AR(1): 118 / 129 = 0.91473
- cases where oracle beat AR(1) but learned OLS AR(2) did not: 0

**Disposition:** HISTORY_MEASUREMENT_LIMIT dominates this declared observation/prediction regime.

## Overall mechanism counts

Across all 600 cases:

- learned OLS AR(2) better than AR(1): 461
- TLS AR(2) better than AR(1): 433
- oracle AR(2) better than AR(1): 433
- oracle not better than AR(1): 167
- oracle better while OLS AR(2) not better: 0
- TLS rescue cases in the predeclared sense, where oracle is better but OLS is not: 0

No TLS-invalid cases occurred.

## Interpretation

The fresh ensemble **reproduces the low-SNR loss of operational history advantage**, so the earlier Limit Map finding is not restricted to the previous selected cases.

However, the mechanism is narrower and clearer than the first post-result root-cause note suggested.

The earlier targeted control correctly showed that corruption of lagged predictors can make learned AR(2) worse than AR(1), which is consistent with an errors-in-variables problem. The fresh randomized test shows that **parameter-estimation bias is not the dominant explanation for the low-SNR boundary in this ensemble**:

- total least squares did not systematically rescue the history advantage;
- the exact oracle recurrence, despite knowing the true dynamics, usually failed to beat AR(1) in the low-SNR regime when fed the same noisy lagged observations;
- there were zero cases in which the oracle beat AR(1) while OLS AR(2) failed to do so.

Therefore the stronger supported interpretation for this declared task is:

> Mathematical finite-history dependence can remain present while the measured lag coordinates become too noisy for that history structure to provide useful predictive information.

This supports two distinct local labels:

- **HISTORY_PRESENT_BUT_NOT_OPERATIONALLY_IDENTIFIABLE**
- **HISTORY_MEASUREMENT_LIMIT**

The first denotes the separation between true latent history structure and operational use from the declared observations. The second identifies the dominant mechanism in the fresh low-SNR ensemble.

## Important boundary

This result does **not** establish a universal SNR threshold at 10 or 100. Those bands were predeclared analysis strata, not physical transition values.

It also does not establish that every filtering, state-space, Bayesian, or Mori-Zwanzig estimator must fail at low SNR. E3 is an oracle recurrence using the noisy observed lags directly; an estimator with additional independent information, a measurement model, smoothing, multiple observed channels, or a different target can change the operational boundary.

## Correction to prior interpretation

COMPUTATIONAL_MEMORY_IDENTIFIABILITY_FOLLOWUP_v0.1.md remains valid as a targeted post-result demonstration that lagged-predictor noise can produce errors-in-variables degradation. It is **not** the complete root-cause explanation for the broader low-SNR ensemble.

The current hierarchy of interpretation is:

1. latent projected dynamics contain finite-history structure;
2. learned lag estimators can suffer predictor-noise bias;
3. more fundamentally, noisy lag observations can become insufficient for useful history-based prediction even with exact dynamic parameters;
4. therefore history-layer admission requires both mathematical structure and operational measurement/identifiability support.

## Claim ceiling

- P0-Q estimator / representation qualification: PASSED.
- universal history layer: NOT SUPPORTED.
- universal SNR cutoff: REFUSED.
- empirical Stability Inheritance: NOT TESTED.
- physical threshold transfer: PROHIBITED.
