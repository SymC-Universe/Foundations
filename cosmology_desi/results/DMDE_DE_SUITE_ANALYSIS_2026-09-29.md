# DESI DR1 Physical Dark-Energy Sensitivity Suite

## Pantheon+

- w0 = -0.85913 [-0.91894, -0.79784]
- wa = -0.67064 [-0.93366, -0.42791]
- Omega_m = 0.30599 [0.29971, 0.31242]
- H0 = 68.336 [67.674, 69.01] km/s/Mpc
- S8 = 0.83076 [0.82174, 0.83993]
- P(w0 > -1) = 0.9913
- P(wa < 0) = 0.9986

## Union3

- w0 = -0.74386 [-0.839, -0.64774]
- wa = -1.0066 [-1.3597, -0.67155]
- Omega_m = 0.3155 [0.30663, 0.32451]
- H0 = 67.339 [66.437, 68.263] km/s/Mpc
- S8 = 0.83595 [0.82627, 0.84562]
- P(w0 > -1) = 0.9974
- P(wa < 0) = 0.9996

## DESY5

- w0 = -0.76244 [-0.82567, -0.69621]
- wa = -0.95101 [-1.2402, -0.68243]
- Omega_m = 0.31414 [0.30794, 0.32039]
- H0 = 67.48 [66.861, 68.107] km/s/Mpc
- S8 = 0.83525 [0.82617, 0.84441]
- P(w0 > -1) = 0.9999
- P(wa < 0) = 0.9999

## Cross-sample check

- All three median w0 values exceed -1: True
- All three median wa values are below 0: True
- Maximum pairwise normalized median shift in w0: 1.085
- Maximum pairwise normalized median shift in wa: 0.783

## Guardrails

- No supernova sample is primary and no sample is selected by outcome.
- CPL-derived w(z), rho_DE(z), q0 and crossing quantities inherit the assumed w0-wa functional form.
- Posterior sign masses are descriptive Bayesian chain summaries, not frequentist p-values.
- Exact model comparison requires matched LambdaCDM and w0wa best-fit likelihoods.