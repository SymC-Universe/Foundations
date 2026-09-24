# D02F Candidate Selection Record v0.1

**Date:** 2026-09-24  
**Status:** D02F_CANDIDATE_SELECTED_BEFORE_DECISIVE_MODAL_OUTCOME_INSPECTION  
**Authority:** SymC General Operations Manual v0.8.6  
**Target:** CA-D007, ARCHITECTURE_REORGANIZATION_CAN_PRECEDE_SCALAR_TRANSFORMATION  
**Parent:** D02F_CANDIDATE_SELECTION_FREEZE_v0.1.md

STATUS

FLOOD-SHAB is selected for D02F.

CURRENT GATE

Freeze MFR-14 and the environmental/operational comparator before reading damping or complex mode-shape trajectories.

NEXT ACTION

Implement the exact D02F prospective test after this selection/MFR commit.

WHY

FLOOD-SHAB is the first screened candidate to solve D02E's measured scalar-admission failure with source-reported damping ratio and same-record complex mode shapes across the full graded event surface.

USER ACTION

NONE.

## Selected system

Dataset:
FLOOD-SHAB: Cable-stayed bridge case-study SHM monitoring features dataset during the April 2026 hydrometric event.

Dataset DOI:
10.5281/zenodo.20443860

Project DOI:
10.3030/101154316

## Selection evidence

### Perturbation-robust scalar

The source data dictionary defines:
- freq_mode_XX_Hz as tracked modal frequency;
- damping_mode_XX as identified damping ratio.

No half-power reconstruction is required.

### Independent organization

The same records provide real and imaginary complex mode-shape components for each tracked mode plus modal complexity factor.

D02F uses complex mode shape, not MCF, as the primary organization observable.

### Graded event surface

Metadata-only event probe:
- 54 event records have observed water-level proxy;
- event water range: 2.24 to 5.03 m;
- frozen event quartile edges:
  - q25 = 3.4025 m;
  - median = 3.535 m;
  - q75 = 4.7275 m;
- event-bin record counts:
  - E1_LOW: 14;
  - E2: 13;
  - E3: 13;
  - E4_HIGH: 14.

### Joint scalar + organization completeness

Mode 1:
- E1_LOW: 14/14;
- E2: 13/13;
- E3: 13/13;
- E4_HIGH: 14/14.

Modes 2 and 3 also have complete same-record scalar+organization coverage in all four event bins and are retained only as secondary robustness families.

### Environmental/operational metadata

Event rows:
- RMS covariates: 54/54;
- air temperature: 52/54;
- wind speed: 52/54.

Pre-event rows:
- 239 total;
- 217 with each frozen EOV covariate.

### Native intervention power

A pre-selection gate used non-modal bridge-response fields only.

Criterion:
at least one non-modal response must show abs Spearman rho >= 0.20 with p < 0.01 versus event water level.

Result:
PASS.

Strongest:
- field: loadcell_U1_N;
- n = 52;
- abs rho = 0.7929635977631981;
- p = 2.4360256114967208e-12.

No modal frequency, damping, MCF, or mode-shape value was used in this gate.

### Automated access

Public Zenodo files are small CSV/text assets with published MD5 checksums.

Reviewer target:

python chi_architecture/reproduce.py d02f

### Relative-onset firewall

Before this selection:
- source schema was inspected;
- missingness/completeness was counted;
- water-level control values were inspected;
- environmental-covariate availability was inspected;
- non-modal native response power was tested.

Not inspected:
- damping trajectory by event-water level;
- complex mode-shape trajectory by event-water level;
- first scalar change level;
- first organization change level;
- scalar-versus-organization relative onset.

## Probe provenance

Final metadata/power workflow:
36036220071

Artifact:
d02f-flood-shab-completeness-v01

Artifact ID:
10824926643

Artifact digest:
sha256:ef60e42770f9f9e423711557b0d5e5f45cf9f45c8579790e9c2d8455c8755bd0

## Selection outcome

D02F_CANDIDATE_SELECTED.
