# Hidden-State Memory Identifiability Follow-up v0.1

**Date:** 2026-09-28  
**Status:** P0-Q ROOT-CAUSE FOLLOW-UP / POST-RESULT EXPLORATION  
**Trigger:** ST-004 cases where AR(2) history closure underperformed AR(1)

## Observed failure

The deterministic stress atlas showed that mathematically present memory did not guarantee that a naive AR(2) estimator improved held-out prediction when displacement observations were noisy.

The degradation was strongly associated with measurement regime. Across finite-noise cases, log10(test SNR) correlated 0.84094 with log10(AR1-RMSE / AR2-RMSE).

## Targeted root-cause control

For gamma=0.7, omega0=2.3, observation noise=0.001:

| Control | AR(1) RMSE | AR(2) RMSE | AR1/AR2 |
|---|---:|---:|---:|
| clean | 0.00026123 | 1.85e-16 | 1.41e12 |
| noise in regression target only | 0.00026120 | 1.91e-6 | 136.98 |
| noise in lagged predictors only | 0.00103416 | 0.00217844 | 0.4747 |
| noise in both predictors and target | 0.00103424 | 0.00218684 | 0.4729 |

## Interpretation

The failure is consistent with an errors-in-variables / identifiability problem in the lagged predictors rather than disappearance of the underlying hidden-state memory. A more complex history model can be scientifically appropriate yet operationally worse when the state/history variables cannot be estimated with adequate signal quality.

This motivates a distinct Limit Map state:

**HISTORY_PRESENT_BUT_NOT_OPERATIONALLY_IDENTIFIABLE**

for a declared estimator/measurement regime.

It must not be generalized to all closure methods, because this follow-up tested ordinary least-squares AR(2), not every native state-space, filtering, or Mori-Zwanzig estimator.

## Epistemic status

Post-result root-cause analysis only. It does not retroactively change the ST-004 protocol or create a confirmatory claim.
