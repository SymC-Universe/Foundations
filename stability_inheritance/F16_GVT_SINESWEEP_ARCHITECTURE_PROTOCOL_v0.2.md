# F-16 GVT Sine-Sweep Architecture Protocol v0.2

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** POST-v0.1-FAILURE P0-D / FROZEN BEFORE v0.2 RESPONSE SCORING
**Evidence class:** PUBLIC EXTERNAL MEASURED / P0-D / PROMOTION DEBT
**P1 eligibility:** NO
**Architecture evidence role if positive:** ARCHITECTURE_SUPPORTING_NATIVE_EXPLORATORY

## Provenance

The prospective v0.1 sine-sweep protocol failed before producing a response score because its raw Hilbert-derivative Voltage coordinate failed the frozen monotonicity gate.

A separately frozen input-only diagnostic then compared four Voltage-only coordinate estimators without loading acceleration outputs. C2, a global quadratic-phase chirp fit, was selected under the preregistered rule and independently agreed with a zero-crossing coordinate.

Because the v0.1 response path had already loaded the sine-sweep records before failing, this v0.2 response analysis is conservatively classified post-result P0-D and carries promotion debt. It may update the Function/Limit map but cannot increase the prospective claim ceiling.

## Frozen coordinate

For each level:

1. mean-center Voltage;
2. form the analytic signal;
3. unwrap phase;
4. discard first/last 2 s for the phase fit;
5. fit phase(t)=a+b t+c t^2 by ordinary least squares;
6. derive frequency coordinate f(t)=(b+2 c t)/(2 pi).

No acceleration output may alter this coordinate.

## Frozen local transfer estimator

Use the same v0.1 response estimator:

- mean-center Force and each acceleration output;
- analytic Force and analytic acceleration via Hilbert transform;
- 4.0 s centered Hann local average;
- local transfer H_j(t)=S[Y_j U*]/S[|U|^2];
- require local Force energy > 1e-12 of that level's maximum;
- exclude record edges by half the 4 s smoothing window;
- retain only samples whose selected C2 coordinate lies in 2-15 Hz.

Interpolate real and imaginary H_j separately onto:

- primary grid 6.5-8.2 Hz inclusive at 0.05 Hz;
- secondary grid 2.5-14.5 Hz inclusive at 0.05 Hz.

## Frozen level roles

Published force amplitudes:

- Level 1: 4.8 N reference/estimation
- Level 2: 19.2 N held-out test
- Level 3: 28.8 N estimation
- Level 4: 57.6 N held-out test
- Level 5: 67.0 N estimation
- Level 6: 86.0 N held-out test
- Level 7: 95.6 N estimation

Amplitude-conditioned predictors:

- Level 2 from Levels 1 and 3;
- Level 4 from Levels 3 and 5;
- Level 6 from Levels 5 and 7;

using linear interpolation in published force amplitude, separately for real and imaginary response components.

Comparator:
- fixed Level-1 response trajectory for all held-out levels.

## Frozen primary metric

Over the full 6.5-8.2 Hz grid and all three outputs:

E(X,t)=sqrt(sum |X-H_t|^2 / sum |H_t|^2)

Report:
- E_FIXED(t)
- E_CONDITIONED(t)
- R_t=E_CONDITIONED/E_FIXED

## Frozen dispositions

- SINESWEEP_P0D_AMPLITUDE_CONDITIONED_SUPPORT if R_2<1, R_4<1, and R_6<1.
- SINESWEEP_P0D_MIXED if at least one but not all R_t<1.
- SINESWEEP_P0D_FIXED_NOT_OUTPERFORMED if none R_t<1.
- INVALID_TEST for source, coordinate, support, interpolation, or finite-value failure.
- INDETERMINATE for a valid but numerically degenerate comparison.

No outcome from v0.2 may be described as prospective confirmation.

## Secondary diagnostics

Report without changing the primary disposition:

- same comparison on 2.5-14.5 Hz;
- per-output primary errors;
- H_payload-H_wing errors;
- primary-band peak frequency per output and level;
- fitted chirp slope and phase-fit quality per level.

## Interpretation ceiling

A positive result would add exploratory third-excitation-family evidence that realized structural response is better represented conditionally on operating/interface regime than by one fixed low-amplitude response object.

A mixed or null result would narrow that architecture.

No physical chi is admitted.
Native response trajectories are not automatically renamed capital Chi.
Chi_arc is not uniquely identified solely by this analysis.
Native structural nonlinearity remains the sufficient mechanistic explanation.

## No-retuning rule

After v0.2 scoring begins, do not alter:

- C2 coordinate definition;
- 2 s phase-fit edge trim;
- 4 s response smoothing;
- frequency grids;
- level roles;
- amplitude interpolation;
- metric;
- output order;
- disposition rule.
