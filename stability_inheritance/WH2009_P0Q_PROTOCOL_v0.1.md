# Wiener-Hammerstein 2009 P0-Q Representation Protocol v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** FROZEN BEFORE RAW TEST SCORING
**Evidence class:** public measured external benchmark / P0-Q only
**Scientific ceiling:** representation adequacy/refusal only

## Frozen question

On the measured Wiener-Hammerstein benchmark, does a low-order nonlinear autoregressive representation with the same lag horizon materially change held-out prediction/simulation behavior relative to a linear ARX representation?

This is not an inheritance claim and not a test of the benchmark's true block decomposition.

## Official data split

Use the official loader split:
- train: [5200, 105200)
- test: [105200, 184000)

Within official train:
- fit: first 80,000 samples
- internal validation: final 20,000 samples

Official test is not used for model structure or ridge selection.

Initialization:
- first 50 test samples may initialize recursive simulation and are excluded from free-run scoring.

## Frozen preprocessing

Fit-only mean and standard deviation are used to standardize u and y.
No test-based rescaling.

## Frozen models

Lag horizon L = 8 for both learned models.

### M0 persistence
y_hat[t] = y[t-1]

### M1 linear ARX-8
Features:
- intercept
- y[t-1] ... y[t-8]
- u[t] ... u[t-8]

### M2 polynomial NARX-8
All M1 features plus elementwise square and cubic terms of each of the same y and u lag variables.

No cross-products, extra lags, filters, or block decomposition may be added after test exposure.

## Frozen regularization

Ridge least squares, intercept unpenalized.

Lambda grid:
0, 1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 1

Choose lambda separately for M1 and M2 by minimum one-step RMSE on the internal validation segment only.

## Frozen metrics

On the official test segment report:
1. one-step RMSE and NRMSE;
2. recursive free-run RMSE and NRMSE after 50-sample initialization;
3. divergence/nonfinite flag;
4. persistence one-step RMSE/NRMSE.

## Frozen disposition

- NONLINEAR_EXTENSION_ADDS_FOR_TASK if M2 is finite and has lower error than M1 on both one-step and free-run metrics.
- LINEAR_REPRESENTATION_ADEQUATE_FOR_TASK if M1 is no worse on both metrics.
- MIXED_REPRESENTATION_RESULT if the metric ordering disagrees.
- REPRESENTATION_OUT_OF_REGIME if a declared representation diverges/nonfinite in free run.
- INDETERMINATE if data identity/numerics prevent a fair test.

No tiny numerical difference is promoted as a universal effect because no equivalence margin is frozen.

## Native comparator firewall

The actual system is natively Wiener-Hammerstein. A polynomial NARX advantage would only qualify nonlinear representation/refusal logic.

The benchmark has mature block-oriented and nonlinear state-space methods that are stronger native comparators than M2. This test cannot claim state-of-the-art added value.

## Failure consequence

If M2 fails, diverges, or is worse than M1, preserve it. Do not add cross-terms, lags, or hidden filters after test exposure to rescue the protocol.
