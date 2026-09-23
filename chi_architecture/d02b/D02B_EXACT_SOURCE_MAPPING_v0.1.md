# D02B Four-Bolt Exact Source Mapping v0.1

**Date:** 2026-09-22  
**Status:** FROZEN_FROM_SCHEMA_BEFORE_NUMERIC_TABLE INSPECTION  
**Authority:** SymC GOM v0.8.3  
**Source contract:** D02B_FOUR_BOLT_SOURCE_CONTRACT_v0.3.md  
**Stage A workflow:** 35819369668  
**Stage A artifact:** d02b-stage-a-schema-v01, ID 10732747680, digest sha256:47a5c916566541b422e0429e37d34012350b78da69e935f6b4ad1d965be0bb7f

## Frozen source archives and hashes

- 01_documentation.zip
  - MD5: 3eb96c388b4811380ab86af9bb4be1ad
  - SHA-256: e3909af929a5c215c8ed1d51ce09aaf47e413ab40ec8e6c5c077a5ca21f1ba72
- 02_processed_tables.zip
  - MD5: a8261869e61e2c41b799360f344b4394
  - SHA-256: af0d165311def77376f479365198b823d9307d103c930f7492f8e8ebb87e1021
- 04_scripts.zip
  - MD5: f7dc41fcf2ee9b2da491e289e045eeb9
  - SHA-256: 64f78f0cc072ed9021786a1f256c74b006d9387a7ee5cf1ba1e6a14f3ff01918

## Exact schema mapping

### Torque state table

File:
01_documentation/torque_states.csv

Required columns:
- case_name
- human_label
- bolt1_Nm
- bolt2_Nm
- bolt3_Nm
- bolt4_Nm
- n_loose_bolts

Primary-case selection is rule-based:
- all-tight = row where all four bolt torques equal 10 Nm;
- single-bolt-loose = rows where exactly one bolt torque equals 0 Nm and the other three equal 10 Nm;
- dose-response intermediate = rows where exactly one bolt equals 5 Nm and the other three equal 10 Nm.

No case names are hard-coded before numeric table inspection.

### Retained resonance families

File:
02_processed_tables/resonance_group_selection_audit.csv

Columns:
- peak_hz
- half_power_bw_hz
- retained
- retention_rule

Selection rule:
retain every row for which retained evaluates true.

Expected row count from schema: 15 total candidates.

The Stage A metadata separately reports seven rows in adaptive_tracking_windows.csv. The final retained-family count must match the source audit; mismatch is a refusal/error rather than a reason to choose a subset.

### Tracking windows

File:
02_processed_tables/adaptive_tracking_windows.csv

Columns:
- retained_resonance_group_hz
- half_power_bw_hz
- nearest_candidate_spacing_hz
- rounded_window_half_width_hz

These source windows define the frozen search neighborhood for each family.

They may not be widened after raw outcomes are viewed.

### Native tracked-frequency comparison

File:
02_processed_tables/tracked_frequencies.csv

Columns:
- family_hz
- tight_hz
- bolt1_hz
- bolt2_hz
- bolt3_hz
- bolt4_hz

This table is used as a native cross-check against independently reconstructed raw peak positions.

### Native embedded-response metrics

Primary processed table:
02_processed_tables/per_case_metrics.csv

Columns:
- family
- bolt
- f_base
- f_case
- one_minus_MACa
- one_minus_CMAC
- one_minus_CMAC_phaseonly

Dose-response table:
02_processed_tables/dose_response.csv

Columns:
- group
- bolt
- torque_Nm
- f_tracked
- one_minus_MACa
- one_minus_CMAC
- one_minus_CMAC_phaseonly

No new weighted combination of these metrics is allowed in D02B v0.3.

## Frozen raw scalar extraction algorithm

For each retained family and eligible torque state:

1. Build the spatial-RMS amplitude spectrum over the 51 common points:
   S(f) = sqrt(mean_p A(f,p)^2).
2. Restrict to the source-provided rounded tracking window around the family.
3. Locate the local maximum in that window.
4. Set half-power amplitude threshold to S_peak / sqrt(2).
5. Search left and right from the peak for the first threshold brackets.
6. Linearly interpolate frequency within each 1-Hz bracket.
7. Delta_f = f_right - f_left.
8. chi = Delta_f / (2 f_peak).

### Admission guards

Emit chi only if:
- both threshold crossings are found inside the frozen window;
- peak is not at the window boundary;
- Delta_f > 0;
- there is a unique dominant local peak under the following predeclared competitor rule.

Competitor rule:
if another local maximum inside the tracking window exceeds 0.90 times the selected peak amplitude and is separated from the selected peak by at least two frequency bins, return NON_IDENTIFIABLE_MODAL_OVERLAP.

The 0.90 competitor threshold is fixed now as a conservative ambiguity screen. It is not a physical boundary and will be reported as a sensitivity item if D02B later reaches interpretation.

No curve fit or alternative linewidth estimator may replace a refused case in v0.3.

## Raw/native cross-check

For all-tight and four single-bolt-loose states:
- reconstructed f_peak must agree with tracked_frequencies.csv within max(1 Hz, source rounded tracking precision);
- failure is a parser/mapping error or an explicit unresolved discrepancy, not an opportunity to alter the window.

## Resolution floor for similar-chi comparisons

The frequency axis is 1 Hz.

For chi = Delta_f/(2 f_peak), a conservative one-bin bandwidth resolution term is:

delta_chi_resolution = 1 / (2 f_peak).

Two chi values may enter the predeclared "similar chi" comparison only when:

abs(chi_a - chi_b) <= max(delta_chi_resolution_a, delta_chi_resolution_b).

If no pairs satisfy this rule, report NO_SIMILAR_CHI_PAIRS_AT_FROZEN_RESOLUTION.

## Numeric-inspection permission boundary

After this file is committed:
- processed CSV values may be read;
- retained family IDs and torque case IDs may be recorded;
- raw response data remain unopened until the raw archive acquisition/checksum checkpoint is implemented.

No change to the mappings above may be made in response to processed values.
