# Brake-Reuss Beam Long-Term History-to-Response Architecture Protocol v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Status:** FROZEN BEFORE RAND-FRF SIGNAL SCORING
**Evidence class:** PUBLIC EXTERNAL MEASURED / P0-Q
**P1 eligibility:** NO
**Architecture evidence role:** eligible for ARCHITECTURE_SUPPORTING_NATIVE_HISTORY
**Native novelty ceiling:** established BRB wear/joint dynamics remain the sufficient mechanism-level explanation

## Native experimental sequence fixed before scoring

The authors' public experiment description defines five Random-FRF states:

- S0 = FirstRound / RandFRF_Before: initial assembled state before monotone excitation.
- S1 = FirstRound / RandFRF_After: after the first 4 h of 172 Hz monotone excitation.
- S2 = SecondRound / RandFRF_After: after the second 4 h block, 8 h cumulative on the original assembly.
- S3 = ThirdRound / RandFRF_Before: after disassembly, interface scanning/cleaning, and reassembly, before the final 4 h block.
- S4 = ThirdRound / RandFRF_After: after the final 4 h block.

The published long-term BRB literature already establishes that wear and interface evolution can alter resonance/damping behavior. This protocol does not claim novelty for that mechanism. It asks how that established history appears inside the Stability Architecture representation/refusal map.

## Frozen archive and file selection

Canonical OSF project: fbwhz.

Use the three official shaker ZIP archives only through selective HTTP Range extraction. Do not download or redistribute the complete archives.

The metadata-only central-directory preflight established a common Random-FRF set at nominal input-voltage levels:

- 0.01 V
- 0.10 V
- 1.00 V

with realization indices 0-9 in every S0-S4 state.

The 5.00 V data present only in S0 are excluded because they are not common across all states.

For every state and voltage:
- FIT realizations = even indices {0,2,4,6,8}
- TEST realizations = odd indices {1,3,5,7,9}

This split is frozen before signal scoring.

## Raw CSV semantics

Use the native published CSV convention:
- row 1: channel names;
- row 2: channel sampling intervals;
- rows 3 onward: time-series samples.

Input:
- excitation Force channel, located by channel name containing "force"; failure to identify exactly one force channel is INVALID_TEST.

Outputs:
- the seven acceleration channels corresponding to the published shaker sensor configuration;
- identify by channel names containing acceleration/accel semantics and verify against the documented channel order;
- if a unique seven-channel acceleration set cannot be identified without looking at response behavior, return INVALID_TEST.

Force and selected acceleration channels must share a common sampling interval within numerical precision. No outcome-dependent resampling is allowed.

If realization lengths differ, freeze N_common as the minimum valid sample count across all selected S0-S4 Rand-FRF files and use the first N_common samples from every realization. This is a structural harmonization rule, not an outcome-dependent crop.

Subtract each record mean and apply one Hann window before FFT.

## Frozen frequency domain

Primary band:
- 140-200 Hz, centered broadly around the published approximately 172 Hz first-mode/monotone-excitation region.

Fit-only excitation support:
- pool Force FFT energy from all FIT realizations, states, and common voltage levels;
- within 140-200 Hz retain bins whose pooled fit input energy exceeds 1e-12 of the maximum fit input energy in that band.

TEST response values may not influence frequency support.

If fewer than 10 bins survive, INVALID_TEST.

## Frozen FRF estimator

For each state s, voltage v, and split q in {FIT, TEST}, estimate a multi-output H1-style FRF:

H_s,v,q(f) = sum_r Y_r(f) F_r(f)* / sum_r |F_r(f)|^2

over the five realizations in that split.

The representation contains all seven acceleration outputs.

Also record median measured Force RMS and the pooled input power spectrum for each state/voltage/split. These are input diagnostics, not outcomes.

## Comparator A: same nominal drive, state-blind leave-one-state-out

For each target state s and voltage v, construct H_LOSO(s,v) from FIT realizations of the other four states at the same nominal voltage v.

This is an amplitude-class comparator that does not know the target state's response.

Compare H_LOSO(s,v) with the held-out H_s,v,TEST.

## Comparator B: input-spectrum-matched state-blind predictor

For each target state/voltage, choose one predictor from all FIT state/voltage combinations belonging to other states.

Selection uses INPUT ONLY:
- compute normalized log Force-power spectrum on the frozen primary support;
- select the candidate with minimum Euclidean distance to the target state's FIT Force-power spectrum.

No output FRF value may influence this selection.

Use the selected candidate's FIT FRF to predict the target held-out FRF.

This comparator controls more directly for current forcing-spectrum differences without using target response information.

## Frozen primary errors

For any predictor P and held-out target T:

E(P,T) = sqrt( sum |P-T|^2 / sum |T|^2 )

over all frozen frequency bins and seven acceleration outputs.

Compute:

1. E_SELF(s,v): H_s,v,FIT -> H_s,v,TEST.
2. E_LOSO(s,v): H_LOSO(s,v) -> H_s,v,TEST.
3. E_INPUTMATCH(s,v): input-spectrum-selected other-state FIT FRF -> H_s,v,TEST.

Aggregate over all 15 state/voltage targets by concatenating the complex arrays before the same normalized error calculation:

- E_SELF_ALL
- E_LOSO_ALL
- E_INPUTMATCH_ALL

Primary ratios:

R_LOSO = E_SELF_ALL / E_LOSO_ALL
R_INPUT = E_SELF_ALL / E_INPUTMATCH_ALL

No equivalence margin is invented. Exact ordering is reported with all state/voltage components.

## Frozen temporal-transition tests

For each transition, use the prior state's FIT FRF at the same voltage to predict the current state's TEST FRF:

- T01: S0 -> S1, first 4 h wear block
- T12: S1 -> S2, second 4 h wear block
- T23: S2 -> S3, disassembly/reassembly transition
- T34: S3 -> S4, final 4 h wear block

For each transition aggregate all three common voltages and seven outputs:

R_ab = E_SELF(b) / E_PRIOR(a->b)

R_ab < 1 means the current-state representation predicts its held-out response better than the immediately preceding state representation.

Wear-history transitions are T01, T12, and T34.
Reassembly T23 is adjudicated separately.

## Frozen history disposition

### HISTORY_CONDITIONED_RESPONSE_ARCHITECTURE

Assign if:
- R_LOSO < 1;
- R_INPUT < 1;
- R_01 < 1;
- R_12 < 1;
- R_34 < 1.

Meaning:
state/history-specific response organization adds held-out information beyond both same-voltage state-blind and input-spectrum-matched state-blind representations across all three wear intervals.

### MIXED_HISTORY_RESPONSE_ARCHITECTURE

Assign if at least one, but not all, of the above five conditions is satisfied.

Preserve which branch fails. Do not retune voltage levels, band, split, or input matcher.

### STATE_HISTORY_NOT_REQUIRED_FOR_DECLARED_TASK

Assign if R_LOSO >= 1 and R_INPUT >= 1 and none of the three wear-transition ratios is < 1.

### INDETERMINATE

Reserve for valid finite analysis where the error normalization is degenerate or input matching is nonunique to numerical precision.

### INVALID_TEST

Assign for source identity, selective extraction, schema, channel, sampling, or frequency-support failure.

## Frozen reassembly classification

First determine whether S2 predicts S3 worse than S3's own FIT representation:

- if R_23 >= 1: REASSEMBLY_CHANGE_NOT_RESOLVED.

If R_23 < 1, compute FIT-representation distances:

D20 = D(S2,S0)
D30 = D(S3,S0)
D23 = D(S3,S2)

using the same normalized complex distance over all three voltages and primary-band outputs.

Then:
- REASSEMBLY_PARTIAL_RESET_TOWARD_INITIAL if D30 < D20;
- REASSEMBLY_REORGANIZATION_NOT_RESET if D30 >= D20.

This classification is descriptive of the measured response representation. It is not a claim that all microscopic wear is reversed or reorganized.

## Secondary diagnostics fixed before scoring

Report:
- voltage-specific SELF/LOSO/INPUTMATCH errors;
- transition ratios at each voltage;
- median Force RMS by state/voltage/split;
- the input-spectrum match selected for each target;
- representation distance from S0 for S1-S4;
- frequency of maximum response norm within 140-200 Hz for each state/voltage;
- within-state FIT-vs-TEST repeatability error distribution.

No secondary result may replace the frozen primary disposition.

## Stability Architecture interpretation ceiling

A positive result is architecture-supporting native evidence that system response retains information about accumulated interface/history state beyond current nominal drive class and beyond an input-spectrum-matched state-blind comparator.

It remains consistent with established tribomechadynamics and the published BRB wear study.

This protocol does not establish:
- a new wear mechanism;
- universal memory;
- a universal substrate;
- a universal inheritance law;
- causal sufficiency of wear alone;
- a unique Chi_arc object.

Project notation:
- chi: NOT ADMITTED by this FRF analysis.
- Chi: NOT FORCED from generic multi-output FRFs; a later modal extraction may independently license it.
- Chi_arc: NOT AUTOMATICALLY IDENTIFIED. The result may support history/context as a constituent of architecture without equating the FRF with Chi_arc.

## Promotion / exposure

The dataset and native published outcome family are historical/public, so this is P0-Q architecture reconstruction, never untouched P1.

The exact computational classification above is frozen before this implementation opens any selected Rand-FRF response values.
