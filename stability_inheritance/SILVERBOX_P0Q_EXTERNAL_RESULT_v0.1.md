# Silverbox P0-Q External Computational Qualification Result v0.1

**Date:** 2026-09-28
**Protocol:** SILVERBOX_P0Q_EXTERNAL_PROTOCOL_v0.1.md
**Protocol freeze commit:** 3b99455ed659a43e0eaaf9a297147deea9f9174c
**Data intake commit:** e400cf2883eb5b676d0f3f94fe24d30b8b5f34ff
**Status:** METHOD_SCOPE_TEST_PASSED / PUBLIC EXTERNAL MEASURED DATA
**P1 status:** INELIGIBLE
**Empirical Stability Inheritance claim:** NONE

## Training/validation result

Fit subset: [40650, 92699)
Validation subset: [92699, 105712)

Fit-only standardization:
- input mean = 0.0061716248461 V
- input SD = 0.0222174079052 V
- output mean = 0.000817179080684 V
- output SD = 0.0545914244604 V

Frozen ridge grid selected lambda=0 for both models from validation only.

Validation one-step RMSE:
- M1 linear ARX-2: 0.0005617633 V
- M2 Duffing-informed cubic NARX-2: 0.0001872234 V

No reserved score was used for model or regularization selection.

## Reserved result 1 - arrow no-extrapolation

Official segment: [100, 32100)

Persistence baseline:
- RMSE = 0.02945010 V
- NRMSE = 0.685257

M1 linear ARX-2:
- one-step RMSE = 0.000580057 V
- one-step NRMSE = 0.0134968
- free-run RMSE = 0.00663613 V
- free-run NRMSE = 0.154294
- divergence = false

M2 Duffing-informed cubic NARX-2:
- one-step RMSE = 0.000187326 V
- one-step NRMSE = 0.00435871
- free-run RMSE = 0.00208702 V
- free-run NRMSE = 0.0485245
- divergence = false

Frozen disposition:
**NONLINEAR_EXTENSION_ADDS_FOR_TASK**

The M2 error is lower than M1 on both frozen metrics and remains finite.

## Reserved result 2 - official multisine test

Official segment: [105712, 127400)

Persistence baseline:
- RMSE = 0.03732834 V
- NRMSE = 0.687715

M1 linear ARX-2:
- one-step RMSE = 0.000690007 V
- one-step NRMSE = 0.0127121
- free-run RMSE = 0.00697516 V
- free-run NRMSE = 0.128454
- divergence = false

M2 Duffing-informed cubic NARX-2:
- one-step RMSE = 0.000219004 V
- one-step NRMSE = 0.00403475
- free-run RMSE = 0.00207911 V
- free-run NRMSE = 0.0382887
- divergence = false

Frozen disposition:
**NONLINEAR_EXTENSION_ADDS_FOR_TASK**

## Representation interpretation

This result is consistent with the native benchmark description: Silverbox is a Duffing-like electronic oscillator with a cubic nonlinearity in feedback. The measured-data result therefore does **not** establish a new SI mechanism.

What it qualifies is the refusal/regime logic:

- a simple linear second-order representation can remain locally predictive while being materially worse for recursive system behavior;
- a natively motivated nonlinear extension can reduce both one-step and free-run error;
- a scalar or linear representation should not be forced beyond its validity regime merely because it remains numerically fit-able.

The result supports a Function/Limit Map distinction between **representation licensed locally** and **representation adequate for the declared task**.

## Model-local chi diagnostic

The M1 linear ARX-2 output recursion has a complex pole pair which maps, under a continuous-time logarithmic pole transform using fs=610.35 Hz, to approximately:

- continuous pole real part = -20.986 s^-1
- imaginary part magnitude = 436.426 rad/s
- local natural frequency = 69.540 Hz
- damping-ratio-like coordinate = 0.04803

This is recorded only as:

**MODEL_LOCAL_CHI_CANDIDATE**

It is not independently measured physical damping, is not a universal Silverbox chi, and is not a threshold.

## Native comparator firewall

The simple cubic NARX is a native nonlinear system-identification comparator deliberately aligned with the benchmark's known cubic feedback structure. More sophisticated published Silverbox models exist and achieve substantially better accuracy. Therefore this result cannot be described as ADDS_OVER_STATE_OF_ART.

## Claim consequence

- P0-Q external measured representation qualification: PASS.
- empirical Stability Inheritance: NOT TESTED.
- carrier-resolved inheritance: NOT TESTED.
- universal chi claim: REFUSED.
- physical-threshold transfer: PROHIBITED.
