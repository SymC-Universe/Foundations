# Hidden-State History Estimator Qualification Protocol v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** FROZEN BEFORE FRESH ENSEMBLE GENERATION
**Evidence class:** P0-Q synthetic estimator/identifiability qualification
**Origin:** post-result question from prior OLS AR2 low-SNR failure
**Promotion debt:** ACTIVE for any generalized history-admissibility rule

## Question

When a projected dynamical system has genuine finite-history structure but its observed lag coordinates are noisy, how much of the loss of history-model advantage is caused by parameter-estimation bias versus the measurement/observability regime itself?

## Fresh ensemble

Master seed: 2026092803

Generate 600 independent damped second-order oscillators:

x'' + gamma x' + omega0^2 x = 0

with:
- gamma uniform on [0.1, 1.2]
- omega0 uniform on [1.2, 4.0]
- initial displacement uniform on [-1,1], rejecting |x0| < 0.15
- initial velocity uniform on [-1,1]
- dt = 0.02
- 600 time samples
- no process noise
- additive independent Gaussian observation noise on displacement
- noise SD sampled log-uniformly from 1e-5 to 1e-2

Use first 60% of each trajectory for estimation and final 40% for scoring.

This ensemble is independent of the earlier ST-004/RQ-4 draws.

## Frozen models

All learned models use noisy observed displacement only.

### E0 AR(1) OLS
Observed y[t] from y[t-1].

### E1 AR(2) OLS
Observed y[t] from y[t-1], y[t-2].

### E2 AR(2) total least squares
Center the training triplets [y[t-1], y[t-2], y[t]], solve the homogeneous errors-in-variables problem using the smallest right singular vector, and restore the centered intercept.

### E3 oracle AR(2) recurrence
Use the exact discrete-time two-lag recurrence implied by the known continuous oscillator parameters and dt. Feed it the same noisy lagged observations as the learned estimators.

E3 is an identifiability upper-bound diagnostic, not an implementable empirical method.

## Frozen outcomes

Score one-step prediction against:

1. latent clean displacement (primary);
2. noisy observed displacement (secondary).

Record:
- test SNR = SD(clean test signal) / known observation-noise SD;
- RMSE for E0-E3;
- advantage ratio E0_RMSE / model_RMSE.

Stratify only by the following predeclared SNR bands:
- HIGH: SNR > 100
- MID: 10 <= SNR <= 100
- LOW: SNR < 10

## Frozen interpretation

- If E3 remains superior to E0 while E1 fails, parameter-estimation/attenuation bias is implicated.
- If E3 itself loses advantage over E0 in a regime, measurement noise has made the true history relation operationally weak for the declared observation task even with perfect dynamics.
- If E2 recovers a substantial portion of E3's advantage where E1 fails, errors-in-variables correction is mechanistically relevant.
- If E2 does not recover the advantage, do not force the conclusion that history is absent; classify the estimator path separately from the mathematical state dependence.

No numeric 'substantial portion' threshold is frozen; report continuous advantage ratios and regime fractions.

## Allowed local labels

- HISTORY_RECOVERABLE_WITH_DECLARED_ESTIMATOR
- HISTORY_ESTIMATOR_LIMIT
- HISTORY_MEASUREMENT_LIMIT
- HISTORY_PRESENT_BUT_NOT_OPERATIONALLY_IDENTIFIABLE
- INDETERMINATE

These are estimator/measurement-regime labels only.

## Failure consequence

If the fresh ensemble does not reproduce any low-SNR loss of operational history advantage, the earlier Limit Map finding is narrowed to the previous generator/settings rather than generalized.

No result promotes a universal history layer or empirical Stability Inheritance claim.
