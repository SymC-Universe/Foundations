# Brake-Reuss Beam Long-Term History-to-Response Architecture Protocol v0.2

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Status:** FROZEN BEFORE ANY BRB LONG-TERM FRF SCORE
**Evidence class:** PUBLIC EXTERNAL MEASURED / P0-Q
**P1 eligibility:** NO
**Architecture evidence role:** eligible for ARCHITECTURE_SUPPORTING_NATIVE_HISTORY
**Supersedes for future execution:** v0.1 only with respect to cross-file sampling-grid harmonization
**Preserved lineage:** v0.1 and v0.1a pre-score failures remain authoritative provenance

## Reason for v0.2

The v0.1 scientific protocol required Force and the seven selected acceleration channels to share a sampling interval within each file. The v0.1a implementation added an extra cross-file common-dt assumption that was not part of the frozen protocol and stopped before FRF scoring when at least two native sampling intervals were encountered.

v0.2 fixes only that implementation gap. It does not change the states, voltages, realization split, channels, history transitions, primary frequency band, comparators, error metric, or scientific disposition rules.

Execution is authorized only if BRB_LONGTERM_SAMPLING_GRID_AUDIT_v0.1 returns SAMPLING_GRID_MAPPING_QUALIFIED and confirms within-file timing consistency for every selected record.

## Frozen states and source set

Use the same canonical OSF project and official shaker archives as v0.1.

States:
- S0 = FirstRound / RandFRF_Before
- S1 = FirstRound / RandFRF_After
- S2 = SecondRound / RandFRF_After
- S3 = ThirdRound / RandFRF_Before
- S4 = ThirdRound / RandFRF_After

Common nominal voltage levels:
- 0.01 V
- 0.10 V
- 1.00 V

For every state and voltage:
- FIT realizations = even indices {0,2,4,6,8}
- TEST realizations = odd indices {1,3,5,7,9}

5.00 V remains excluded because it is not common across all states.

## Frozen channels

Input:
- native Force channel F1.

Outputs:
- A1, X1, Y1, Z1, X2, Y2, Z2 in that order.

Within each selected CSV, all eight selected channels must share one native dt within numerical precision. Any violation is INVALID_TEST.

Cross-file dt equality is not required.

## Frozen time-duration harmonization

For every selected record i after numeric parsing:

- n_i = valid selected sample count;
- dt_i = native selected-channel sampling interval;
- T_i = (n_i - 1) dt_i.

Define:

T_common = min_i T_i.

For each record retain the first

N_i = floor(T_common / dt_i) + 1

samples.

This uses a common physical observation duration while retaining each record at its native sampling interval.

No interpolation or resampling of the time-domain signals is permitted.

If any retained record has fewer than 256 samples, return INVALID_TEST.

## Frozen common physical-frequency grid

Define:

df = 1 / T_common.

Within the primary 140-200 Hz band, use the common physical frequencies

f_k = k df

for every integer k satisfying 140 <= f_k <= 200.

Every record is evaluated directly at these same physical frequencies using its own native time coordinate t_n = n dt_i.

No FFT-bin interpolation is used.

If fewer than 10 common physical-frequency points exist, return INVALID_TEST.

## Frozen spectral estimator

For each retained record:

1. subtract the record mean separately from Force and every acceleration output;
2. apply one Hann window of length N_i;
3. evaluate the complex Fourier sum directly at every common f_k;
4. normalize Force and output Fourier amplitudes by the sum of the Hann window so input spectra remain comparable across records with different N_i.

For signal x_i[n]:

X_i(f_k) = (1 / sum_n w_i[n]) sum_n w_i[n] (x_i[n]-mean(x_i)) exp(-j 2 pi f_k n dt_i).

The H1-style FRF estimator remains:

H_s,v,q(f_k) =
sum_r Y_r(f_k) F_r(f_k)* /
sum_r |F_r(f_k)|^2

over the frozen FIT or TEST realization sets.

## Frozen fit-only support

Pool normalized Force spectral energy from all FIT realizations, states, and common voltages on the common 140-200 Hz grid.

Retain common physical-frequency points whose pooled FIT input energy exceeds 1e-12 of the maximum pooled FIT input energy in the band.

TEST responses may not influence support.

If fewer than 10 support frequencies survive, return INVALID_TEST.

## Comparator A: same nominal drive, state-blind leave-one-state-out

Unchanged from v0.1.

For each target state s and voltage v, construct H_LOSO(s,v) from FIT realizations of the other four states at the same nominal voltage.

Compare with held-out H_s,v,TEST.

## Comparator B: input-spectrum-matched state-blind predictor

Unchanged from v0.1.

For each target state/voltage, choose one FIT state/voltage representation from another state using INPUT ONLY.

On frozen support:
- normalize each FIT Force-power spectrum by its total support power;
- take the natural logarithm after a numerical floor of 1e-300;
- choose the candidate with minimum Euclidean distance.

No output response may influence matching.

## Frozen primary errors

Unchanged from v0.1.

For predictor P and held-out target T:

E(P,T) = sqrt(sum |P-T|^2 / sum |T|^2)

over frozen physical-frequency support and all seven acceleration outputs.

Aggregate:
- E_SELF_ALL
- E_LOSO_ALL
- E_INPUTMATCH_ALL

Primary ratios:
- R_LOSO = E_SELF_ALL / E_LOSO_ALL
- R_INPUT = E_SELF_ALL / E_INPUTMATCH_ALL

No equivalence margin is invented.

## Frozen temporal-transition tests

Unchanged from v0.1.

At the same voltage, use prior-state FIT FRFs to predict current-state TEST FRFs:

- T01: S0 -> S1
- T12: S1 -> S2
- T23: S2 -> S3
- T34: S3 -> S4

For each transition aggregate all three voltages and seven outputs.

R_ab = E_SELF(b) / E_PRIOR(a->b).

Wear-history transitions:
- T01
- T12
- T34

Reassembly T23 remains separately classified.

## Frozen history disposition

Unchanged from v0.1.

HISTORY_CONDITIONED_RESPONSE_ARCHITECTURE if:
- R_LOSO < 1;
- R_INPUT < 1;
- R_01 < 1;
- R_12 < 1;
- R_34 < 1.

MIXED_HISTORY_RESPONSE_ARCHITECTURE if at least one but not all five conditions is satisfied.

STATE_HISTORY_NOT_REQUIRED_FOR_DECLARED_TASK if R_LOSO >= 1, R_INPUT >= 1, and none of T01/T12/T34 has ratio < 1.

INDETERMINATE for valid finite analysis with degenerate normalization or nonunique input matching to numerical precision.

INVALID_TEST for source identity, schema, within-file timing, common-duration, frequency-support, or nonfinite-analysis failure.

## Frozen reassembly classification

Unchanged from v0.1.

If R_23 >= 1:
- REASSEMBLY_CHANGE_NOT_RESOLVED.

If R_23 < 1, compute FIT representation distances:
- D20 = D(S2,S0)
- D30 = D(S3,S0)
- D23 = D(S3,S2)

Then:
- REASSEMBLY_PARTIAL_RESET_TOWARD_INITIAL if D30 < D20;
- REASSEMBLY_REORGANIZATION_NOT_RESET otherwise.

## Secondary diagnostics

Unchanged in scientific role:
- voltage-specific SELF/LOSO/INPUTMATCH errors;
- transition ratios by voltage;
- median Force RMS by state/voltage/split;
- input-spectrum match identity;
- representation distance from S0;
- maximum response-norm frequency within 140-200 Hz;
- within-state FIT-vs-TEST repeatability errors.

Sampling diagnostics additionally report native dt, retained N_i, T_common, and common df. These are method metadata, not scientific outcomes.

## Stability Architecture interpretation ceiling

Unchanged from v0.1.

A positive result is architecture-supporting native evidence that system response retains measurable information about accumulated interface/history state beyond current nominal drive class and beyond an input-spectrum-matched state-blind comparator.

Established BRB wear and joint tribomechadynamics remain sufficient mechanism-level explanations.

Project notation:
- chi: NOT ADMITTED by this FRF analysis.
- Chi: NOT FORCED from generic multi-output FRFs.
- Chi_arc: NOT AUTOMATICALLY IDENTIFIED.

The result may support history/context as a constituent of Stability Architecture without treating the FRF itself as Chi_arc.

## No-retuning rule

After v0.2 signal scoring starts, do not change:
- source states;
- voltage set;
- FIT/TEST realization split;
- channel set/order;
- common-duration rule;
- direct physical-frequency grid rule;
- 140-200 Hz band;
- fit-only support threshold;
- LOSO comparator;
- input-spectrum matcher;
- primary errors;
- transition definitions;
- disposition rules.

Any alternative becomes a new post-result P0-D object with promotion debt.
