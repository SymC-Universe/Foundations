# Wiener-Hammerstein 2009 P0-Q External Result v0.1

**Date:** 2026-09-28  
**Governance:** SymC GOM v1.0  
**Protocol:** stability_inheritance/WH2009_P0Q_PROTOCOL_v0.1.md  
**Protocol freeze commit:** 7a548622063d03e8c964c2e4c8c9ebec1dd648da  
**Successful scoring run:** 36498397948  
**Successful scoring commit:** 33869f26e1cca3cc5af871f8382eaf65fff00a3e  
**Status:** METHOD_SCOPE_TEST_PASSED / PUBLIC EXTERNAL MEASURED DATA  
**P1 status:** INELIGIBLE  
**Empirical Stability Inheritance claim:** NONE

## Data identity

Runtime source:
https://raw.githubusercontent.com/matheuswhite/narmax/master/res/wienerhammer.csv

Frozen expected Git blob SHA:
`865a402fc495291422133f7473867a82a8aee12e`

Verified downloaded Git blob SHA:
`865a402fc495291422133f7473867a82a8aee12e`

Downloaded raw SHA-256:
`db69ccd7fea954adef57ff4e3bdfdf22b24c0e325b7ecd683751c9bae3d92462`

Shape:
- 188,000 rows
- 3 columns

The source identity matched before any scoring proceeded.

## Frozen split

- train: [5200, 105200)
- fit: [5200, 85200)
- internal validation: [85200, 105200)
- official test: [105200, 184000)
- free-run initialization: first 50 test samples

Fit-only standardization:
- input mean = -0.002649990745
- input SD = 0.6776319834
- output mean = -0.04006761423
- output SD = 0.2426947808

## Frozen model selection

Selected ridge parameter for both M1 linear ARX-8 and M2 polynomial NARX-8:
- lambda = 0.01

Selection used only the internal validation segment.

## Official test result

| Model | One-step RMSE | One-step NRMSE | Free-run RMSE | Free-run NRMSE | Diverged |
|---|---:|---:|---:|---:|---|
| Persistence | 0.03285510 | 0.13473088 | n/a | n/a | n/a |
| M1 linear ARX-8 | 0.0008874133 | 0.003639069 | 0.04419645 | 0.18120929 | false |
| M2 polynomial NARX-8 | 0.0007311239 | 0.002998163 | 0.02433026 | 0.09975617 | false |

Relative to M1, M2 reduced:
- one-step RMSE by approximately 17.61%;
- free-run RMSE by approximately 44.95%.

Frozen disposition:

**NONLINEAR_EXTENSION_ADDS_FOR_TASK**

M2 remained finite and outperformed M1 on both frozen metrics.

## Interpretation

This is a representation-adequacy result, not Stability Inheritance novelty.

The benchmark is natively Wiener-Hammerstein: a static nonlinearity between two linear dynamical blocks. Therefore a polynomial nonlinear autoregressive representation outperforming a linear ARX representation is consistent with established nonlinear system-identification science.

The SI-relevant qualification is narrower:

- a linear representation can fit local/one-step behavior very well while remaining substantially less adequate for recursive system behavior;
- representation admission and representation adequacy for the declared task are distinct;
- richer dynamics should not be reinterpreted as inheritance simply because they outperform a reduced model;
- no scalar chi is admitted from this input/output record by default.

## Claim consequence

- public measured external P0-Q representation qualification: PASS;
- nonlinear extension adds for this frozen task: YES;
- native nonlinear structure sufficient explanation: YES;
- empirical Stability Inheritance: NOT TESTED;
- carrier-resolved inheritance: NOT TESTED;
- universal chi claim: NOT SUPPORTED;
- physical threshold transfer: PROHIBITED.

## Execution-failure provenance

Three launch attempts failed mechanically before valid scoring:

1. run 36498162920: raw transport URL used a Git blob SHA as a raw ref and returned HTTP 404 before parsing;
2. run 36498237609: mechanical source patch introduced a literal newline escape into Python source and failed syntax parsing before data access;
3. run 36498325274: a second literal newline escape remained in the result dictionary and failed syntax parsing before data access.

No failed attempt parsed or scored the benchmark. The successful run changed only transport/syntax mechanics; the frozen split, models, lag horizon, regularization grid, metrics, and outcome rule were unchanged.
