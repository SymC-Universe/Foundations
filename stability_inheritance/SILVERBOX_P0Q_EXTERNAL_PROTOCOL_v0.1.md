# Silverbox P0-Q External Computational Qualification Protocol v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** FROZEN BEFORE RESERVED-TEST SCORING
**Evidence class:** public measured external benchmark / P0-Q only
**Scientific ceiling:** representation and regime qualification only

## Frozen question

On measured Duffing-like dynamics, does a simple linear second-order input-output representation remain adequate across the official benchmark regimes, or does a prospectively specified cubic nonlinear extension materially change held-out predictive/simulation behavior?

This is not an inheritance claim. It is an external measured-data qualification of representation adequacy and refusal logic.

## Data split

Use the official Silverbox split recorded in SILVERBOX_DATA_INTAKE_v0.1.md.

Training/validation:
- multisine train/validation block [40650, 105712)
- within that block only, use the first 80% for coefficient fitting and the final 20% for model-selection/regularization choice

Reserved external scoring:
- primary: arrow no-extrapolation [100, 32100)
- secondary transfer: official multisine test [105712, 127400)

State initialization:
- first 50 samples of each reserved segment may initialize recursive simulation and are excluded from scored simulation error.

No model/hyperparameter may be changed after reserved scores are inspected.

## Frozen model classes

All models use only V1 input and V2 output.

### M0 persistence baseline
One-step:
y_hat[t] = y[t-1]

### M1 linear ARX-2
In standardized training coordinates:
y_hat[t] = b + a1*y[t-1] + a2*y[t-2] + c0*u[t] + c1*u[t-1] + c2*u[t-2]

### M2 Duffing-informed cubic NARX-2
M1 plus:
d1*y[t-1]^3 + d2*y[t-2]^3

The cubic terms are specified because the benchmark's native construction contains a third-degree static nonlinearity in feedback. No extra polynomial/cross terms may be added after test exposure.

## Estimation and regularization

Standardization parameters are learned on the fit subset only.

Fit coefficients by ridge least squares with intercept unpenalized.

Frozen lambda grid:
0, 1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 1

Choose lambda separately for M1 and M2 by minimum one-step RMSE on the internal validation subset only.

If a normal equation is singular/ill-conditioned at lambda=0, record that event and continue the predeclared positive-lambda grid.

## Frozen metrics

For each reserved segment report:

1. one-step RMSE in original output units;
2. one-step NRMSE = RMSE / standard deviation of scored measured output;
3. recursive free-run RMSE after the 50-sample initialization;
4. recursive free-run NRMSE;
5. nonfinite/divergent simulation flag.

Also report M0 one-step error as a simple sanity baseline.

## Frozen interpretation rules

- LINEAR_REPRESENTATION_ADEQUATE_FOR_TASK: M1 is not worse than M2 on both one-step and recursive metrics in the declared segment.
- NONLINEAR_EXTENSION_ADDS_FOR_TASK: M2 has lower error than M1 on both one-step and recursive metrics in the declared segment, with finite simulations.
- MIXED_REPRESENTATION_RESULT: one-step and recursive metrics disagree in ordering.
- REPRESENTATION_OUT_OF_REGIME: a fitted representation becomes nonfinite/divergent or produces grossly unstable recursive behavior on a declared reserved segment.
- INDETERMINATE: numerical/identity problems prevent a fair comparison.

Because this is P0-Q and lacks a repeatability-derived equivalence margin, no tiny difference is promoted as a general scientific advantage. Numerical magnitudes and direction are reported transparently.

## Local chi rule

No physical chi is assumed.

A local linear ARX pole-derived damping-like coordinate may be computed only as a MODEL_LOCAL_CHI_CANDIDATE after the primary representation comparison. It may not be called physical damping without independent identification and may not be converted into a universal threshold.

## Native comparator firewall

The benchmark is already a nonlinear system-identification problem. M2 is a deliberately simple Duffing-informed native nonlinear comparator, not a new SI mechanism. If M2 outperforms M1, the result supports nonlinear-regime/refusal logic only.

No result may be labeled ADDS_OVER_STATE_OF_ART or empirical Stability Inheritance.

## Failure consequence

If the simple workflow cannot reproduce the expected distinction between linear and nonlinear benchmark behavior, record METHOD_SCOPE_TEST_FAILED for this external benchmark. Do not tune the test set or add terms post hoc. Any improved model becomes a new exploratory/post-result branch.
