# D02F FLOOD-SHAB MFR-14 v0.1

**Date:** 2026-09-24  
**Status:** P1_FROZEN_BEFORE_DECISIVE_DAMPING_OR_MODE_SHAPE_VALUES  
**Authority:** SymC General Operations Manual v0.8.6  
**Target:** CA-D007, ARCHITECTURE_REORGANIZATION_CAN_PRECEDE_SCALAR_TRANSFORMATION

STATUS

MFR-14 frozen before decisive D02F modal values.

CURRENT GATE

Implementation may proceed only without altering the scientific rules below.

NEXT ACTION

Implement one-command D02F reproduction, archive the first successful decisive run, then interpret.

WHY

D02F is designed specifically to eliminate the scalar-admission failure measured in D02E while preserving unseen relative onset.

USER ACTION

NONE.

## MFR-01 Frozen claim

claim_id: CA-D007-D02F-v0.1

Exact claim:

Across graded flood-water levels in the selected cable-stayed bridge event, independently measured complex modal organization may cross its frozen change boundary at a lower water-level stratum than the source-reported modal damping ratio crosses its frozen scalar-transformation boundary.

Scope:
- one monitored cable-stayed bridge;
- April 2026 hydrometric event;
- source water-level proxy as graded control;
- mode 1 as primary;
- modes 2 and 3 as secondary robustness only.

Task:
determine the ordinal onset relation between source-reported modal damping ratio and complex mode-shape organization over E1 -> E2 -> E3 -> E4.

## MFR-02 Hypothesis provenance

DATA_DERIVED + CROSS_SYSTEM_TRANSFER.

CA-D007 was generated after D02B.

Prospective history:
- D02C: null;
- D02D: indeterminate;
- D02E: indeterminate due scalar-admission failure.

D02F is new decisive evidence.

## MFR-03 Native observables

Local scalar:

chi_local = damping_mode_01

because the source data dictionary identifies this field as the modal damping ratio.

No rescaling is permitted.

Admission:
- finite;
- 0 < chi < 1;
- same record has finite tracked frequency.

Organization:

complex mode vector assembled from every finite phi_mode_01_*_real / *_imag pair in source column order.

Normalize to Euclidean norm one.

Pairwise/projector geometry is phase-invariant.

Primary organization dissimilarity:

D_org = 1 - |v_ref^H v_event|^2.

## MFR-04 Representation and validity regime

Native framework:
operational modal analysis / tracked bridge modal features under environmental and hydrometric variation.

Primary family:
mode_01, selected because the metadata-only probe demonstrated 100% joint scalar+organization completeness in all four event-water strata.

Secondary robustness:
mode_02 and mode_03, prohibited from changing the primary verdict.

No mode selection uses decisive damping or shape values.

## MFR-05 Strongest native comparator

Comparator:
environmental/operational-variability-conditioned OMA with direct damping-ratio tracking and complex mode-shape MAC/projector analysis.

Frozen EOV covariates:
- temp_air_C;
- wind_speed_kmh;
- operational intensity = log1p(mean(rms_AM1Z_microg, rms_AM2Z_microg)).

Water level, bridge load-cell response, displacement response, modal frequency, damping, MCF, and mode shape are excluded from the matching covariate vector.

If native OMA/EOV analysis fully describes D02F, verdict remains:

NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE.

## MFR-06 Null / competing explanations

N1:
scalar damping changes before mode-shape organization.

N2:
scalar and organization change in the same water-level bin.

N3:
neither changes.

N4:
only scalar changes.

N5:
only organization changes.

N6:
apparent ordering is caused by environmental/operational support mismatch.

N7:
event-water proxy is too incomplete or too remote from local hydraulic forcing to identify ordering.

## MFR-07 Expected response

CA-D007 expectation:

organization onset occurs in an earlier event-water bin than scalar onset, or organization changes while scalar does not.

No specific bin is predicted.

## MFR-08 Decision rule

Ordered control:

PRE_EVENT_CONTROL < E1_LOW < E2 < E3 < E4_HIGH.

Event bin edges, frozen from water values only:
- E1_LOW: water <= 3.4025 m;
- E2: 3.4025 < water <= 3.535 m;
- E3: 3.535 < water <= 4.7275 m;
- E4_HIGH: water > 4.7275 m.

Define:
- t_org = earliest event bin classified ORGANIZATION_CHANGED;
- t_chi = earliest event bin classified SCALAR_TRANSFORMED.

Primary outcomes:
- ORGANIZATION_PRECEDES_SCALAR;
- SCALAR_PRECEDES_ORGANIZATION;
- SIMULTANEOUS_WITHIN_FROZEN_LEVELS;
- ORGANIZATION_CHANGES_SCALAR_DOES_NOT;
- SCALAR_CHANGES_ORGANIZATION_DOES_NOT;
- NEITHER_CHANGES;
- ORDERING_NON_IDENTIFIABLE.

CA-D007 support in D02F:
ORGANIZATION_PRECEDES_SCALAR or ORGANIZATION_CHANGES_SCALAR_DOES_NOT.

Adverse ordering:
SCALAR_PRECEDES_ORGANIZATION or SCALAR_CHANGES_ORGANIZATION_DOES_NOT.

Simultaneous, neither, or non-identifiable do not support CA-D007.

## MFR-09 Environmental matching, uncertainty, and completeness

### Pre-event control pool

Use rows with pre_event_window truthy.

Control row requirements:
- admitted primary chi;
- admitted primary complex mode vector;
- finite temp_air_C;
- finite wind_speed_kmh;
- finite rms_AM1Z_microg;
- finite rms_AM2Z_microg.

Require >=100 control rows.

### Frozen EOV vector

For each valid row:

x = [
  temp_air_C,
  wind_speed_kmh,
  log1p((rms_AM1Z_microg + rms_AM2Z_microg)/2)
].

Standardize from pre-event controls using:
- center = median;
- scale = 1.4826*MAD;
- if MAD=0, use IQR/1.349;
- if still zero, use sample standard deviation;
- if still zero, refuse the covariate/model.

### Matched control set

For each event row:
- compute Euclidean distance in standardized EOV space to every valid pre-event control;
- take the 30 nearest controls;
- require the 30th-nearest distance <= 3.0;
- otherwise both scalar and organization are EOV_NON_IDENTIFIABLE for that event row.

No control reuse restriction is imposed because matching is a local reference construction rather than a treatment-effect estimator.

### Scalar row margin

For each event row and its 30 matched controls:
- q2.5 = 2.5th percentile matched-control chi;
- q97.5 = 97.5th percentile matched-control chi.

Define scalar_margin:
- chi_event - q97.5 if above q97.5;
- q2.5 - chi_event if below q2.5;
- negative minimum distance to either envelope boundary if inside.

Positive margin means outside the matched native scalar envelope.

### Organization row margin

For the 30 matched controls:
- construct unit complex mode vectors;
- form projectors P_i = v_i v_i^H;
- v_ref = principal eigenvector of mean(P_i);
- D_event = 1 - |v_ref^H v_event|^2.

For each matched control j:
- construct leave-one-out reference from the other 29 controls;
- D_j_LOO = 1 - |v_ref,-j^H v_j|^2.

T_org,row = 97.5th percentile of the 30 leave-one-out D values.

organization_margin = D_event - T_org,row.

Positive margin means event organization lies beyond its matched native envelope.

### Bin-level change

For each event bin separately:
- require >=10 rows with valid scalar margins to adjudicate scalar;
- require >=10 rows with valid organization margins to adjudicate organization.

Bootstrap:
- 10,000 resamples of row margins;
- fixed seed 20260924 + bin index;
- statistic = median;
- 95% percentile interval.

SCALAR_TRANSFORMED only when the scalar-margin bootstrap lower95 > 0.

ORGANIZATION_CHANGED only when the organization-margin bootstrap lower95 > 0.

Otherwise the observable is UNCHANGED for that bin.

### Onset completeness

If an earlier event bin is non-identifiable for an observable, a later changed bin cannot establish onset for that observable.

If either observable's onset cannot be identified, ordering is ORDERING_NON_IDENTIFIABLE.

## MFR-10 Independence / leakage map

Hypothesis generator:
D02B, separate physical system.

Prior prospective tests:
D02C, D02D, D02E, separate systems.

Candidate screen inspected only:
- methods/schema/metadata;
- water-level control values;
- missingness counts;
- environmental covariate availability;
- non-modal load/displacement/RMS intervention-power summaries.

Not inspected before freeze:
- mode 1 damping values by water bin;
- mode 1 complex mode-shape values by water bin;
- scalar margins;
- organization margins;
- relative onset.

## MFR-11 Multiplicity

Primary:
one mode only, mode_01.

Secondary:
mode_02 and mode_03 reproduced under identical rules for robustness only.

Secondary outcomes cannot rescue or reverse the primary verdict.

No alternate water binning, mode, environmental covariate set, k, distance threshold, bootstrap rule, or organization metric may replace the primary analysis after outcome inspection.

## MFR-12 Freeze identity / decisive dataset

Dataset DOI:
10.5281/zenodo.20443860

Primary source:
CableStayedBridge_SHM_features_2026-03-27_2026-04-10.csv

MD5:
34ff627723494abe2b224db433d6fa76

SHA-256:
f25aa37950baf5d9afb50e282371e1aca6f9069e79f57a63ebbdf6a8ab83b941

Data dictionary SHA-256:
9147c446aa357ef729103d36d51ba739fc22051a9047855e70df9ecd68a98506

Engine:
to be implemented after this freeze behind:

python chi_architecture/reproduce.py d02f

## MFR-13 Explicit falsifier

D02F counts against CA-D007 in this system if the primary mode returns:

SCALAR_PRECEDES_ORGANIZATION

or

SCALAR_CHANGES_ORGANIZATION_DOES_NOT.

A simultaneous, neither, or non-identifiable result does not support CA-D007 and is retained without rescue.

## MFR-14 Failure consequence

If MFR-13 occurs:
- CA-D007 receives a clean prospective adverse ordering after one null and two indeterminate tests;
- program status becomes STRONGLY_DOMAIN_LIMITED / RETIRE_GENERAL_ORDERING_PENDING_NEW_MECHANISM;
- D02B remains descriptive;
- no alternate D02F mode/binning/EOV model may rescue the hypothesis;
- any replacement ordering enters the discovery ledger with new promotion debt.

If D02F supports CA-D007:
- this is one prospective external support after prior null/indeterminate tests;
- CA-D007 remains non-universal;
- replication debt remains.

If D02F is null or indeterminate:
- CA-D007 remains unconfirmed;
- another test is justified only if it resolves the measured limitation without weakening the gate.
