# D02B Four-Bolt Plate Source Contract v0.3

**Date:** 2026-09-22  
**Status:** FROZEN_BEFORE_NUMERICAL_D02B_EXTRACTION  
**Authority:** SymC GOM v0.8.3  
**Selection record:** D02B_CANDIDATE_SELECTION_CORRECTION_v0.3.md

## Physical system

Aluminum plate with four bolted corner joints measured by full-field scanning laser Doppler vibrometry under 18 controlled bolt-torque configurations.

Dataset DOI: 10.5281/zenodo.20038951  
Related preprint: arXiv:2609.05378

## Stability-inheritance substrate candidate

The physical substrate is the bolted interface organization:

S = (T1,T2,T3,T4)

where Ti is the nominal torque of bolt i.

This descriptor is externally imposed and recorded independently of the vibration response.

## Native data

Raw exports:
- H1 displacement-to-force FRF amplitude, m/N;
- H1 phase, degrees;
- frequency axis 1...51200 Hz at 1 Hz spacing;
- 51 common LDV scan points across all torque states.

Preprocessed/native support:
- torque_states.csv;
- candidate_resonance_groups.csv;
- resonance_group_selection_audit.csv;
- adaptive_tracking_windows.csv;
- tracked_frequencies.csv;
- per_case_metrics.csv;
- family_summary.csv;
- dose_response.csv.

## Frozen mode set

Use every resonance group retained by the dataset's own predeclared/native retention audit.

Do not choose or exclude resonance groups based on D02B outcomes.

If the source retention audit yields seven groups, all seven are retained.

## Licensed scalar chi

For a retained resonance group and torque state, if a locally isolated passive resonance admits a half-power bandwidth estimate,

Q = f_n / Delta_f

and

chi = 1/(2Q) = Delta_f/(2 f_n).

This chi is a modal/local second-order damping coordinate only.

It is not a whole-plate master scalar.

## Scalar admission and refusal

For each resonance-group / torque-state pair:

1. locate the native tracked peak inside the predeclared tracking window;
2. estimate the two -3 dB crossings around the local peak from amplitude response;
3. require both crossings to lie inside the tracking window;
4. require no competing local maximum to invalidate unique local peak assignment;
5. require positive finite bandwidth;
6. emit chi only when all conditions pass.

Otherwise emit one of:

- NO_ADMISSIBLE_SCALAR_CHI
- NON_IDENTIFIABLE_MODAL_OVERLAP
- WINDOW_TRUNCATED
- HALF_POWER_CROSSING_NOT_OBSERVED

No fitted alternative damping model may replace a refused half-power result in v0.3.

## Frozen hierarchy of source use

Stage A, before raw archive:
- documentation;
- processed tables;
- scripts;
- checksums;
- environment files.

Purpose: freeze file/schema mapping and reproduce the dataset's native retained-group definitions.

Stage B:
- download raw exports only after Stage A mapping is checkpointed;
- verify raw file checksums;
- compute same-condition half-power chi for the frozen retained groups and torque states.

## Primary torque contrast

Primary confirmatory-within-P0 contrast:

- all-tight 10/10/10/10 Nm
versus
- four single-bolt 0 Nm cases.

Reason: these cases are explicitly used by the source dataset for cross-case trackability and are defined before D02B analysis.

## Secondary dose-response contrast

For each bolt where the source provides 10/5/0 Nm sequence:

- 10 Nm baseline;
- 5 Nm intermediate;
- 0 Nm loose.

This is a monotonicity / transformation stress test, not a basis for dropping primary cases.

## Frozen local-vs-embedded tests

### T1: local scalar transformation

For each retained mode family, compare admissible chi across the all-tight and four single-bolt-loose states.

Report:
- preserved within uncertainty/resolution;
- transformed;
- refused/non-identifiable.

No universal preservation threshold is assumed.

### T2: same/similar chi, different embedded organization

Identify condition pairs only through a predeclared numerical rule:

two chi estimates are "similar" when their absolute difference is no larger than the larger of:
- one frequency-bin-induced bandwidth-resolution unit propagated to chi;
- the bootstrap/measurement uncertainty if supplied.

No wider tolerance may be introduced after viewing response differences.

For such pairs, compare native embedded response:
- tracked resonance frequency shift;
- amplitude-only spatial dissimilarity;
- complex amplitude+phase dissimilarity;
- phase-only dissimilarity.

### T3: interface-state added information

Evaluate whether bolt torque identity/state explains embedded response differences beyond local chi alone.

Because this is one physical specimen with repeated structured conditions, inference must respect within-family repeated measures and may not treat every scan point as an independent experimental replicate.

### T4: carrier/shape relation

Use only native source metrics in v0.3:
- MACa-derived dissimilarity;
- CMAC-derived dissimilarity;
- phase-only CMAC-derived dissimilarity;
- local FRAC deficit only if directly supplied/reproducible by source scripts.

Do not invent a new Chi carrier score.

### T5: native-toolkit sufficiency

The strongest native comparator is the existing structural-dynamics toolkit:
- FRF peak tracking;
- half-power damping;
- MAC/CMAC;
- local FRAC;
- bolt-torque condition labels.

If that toolkit explains the result, report:

NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE

## Primary scientific question

Can two conditions retain similar local modal damping coordinates while controlled bolt-interface reorganization produces materially different full-field response organization?

The reverse direction is also retained:

Can local chi itself transform systematically with interface state?

The relation, not a preferred direction, is the research target.

## Predeclared descriptive outcome states

For each mode family:
- PRESERVED
- TRANSFORMED
- REORGANIZED
- LOCAL_SCALAR_VALID_BUT_EMBEDDED_INSUFFICIENT
- NO_ADMISSIBLE_SCALAR_CHI
- NON_IDENTIFIABLE
- NO_RELATION_DETECTED
- CONTRADICTS_INHERITANCE_HYPOTHESIS

Added-value verdict:
- NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE
- INCREMENTAL_VALUE_UNRESOLVED

No positive incremental-value claim is pre-authorized.

## Failure conditions

The working inheritance interpretation is weakened when:
- torque-state changes do not reproducibly alter local or embedded response;
- full-field response differences are not larger than source/resolution uncertainty;
- low-dimensional local chi fully accounts for response changes without interface information;
- mode matching is unstable under the source's own retention criteria;
- scalar admission fails for most/all states;
- results depend on post-hoc mode selection or tolerance changes.

## Reproduction contract

Reviewer-facing command:

python chi_architecture/reproduce.py d02b

The wrapper will:
1. fetch only Stage-A small Zenodo assets first;
2. verify hashes/metadata;
3. validate the frozen schema;
4. acquire the raw archive automatically only when needed for half-power extraction;
5. avoid exposing reviewers to 1,838 manual files;
6. generate one compact result bundle and manifest.

The implementation may cache/unpack raw files internally. Reviewers interact with one command.
