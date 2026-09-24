# D02E Offshore Jacket MFR-14 v0.1

**Date:** 2026-09-23  
**Status:** P1_FROZEN_BEFORE_DECISIVE_DAMAGE_RESPONSE_VALUES  
**Authority:** SymC General Operations Manual v0.8.6  
**Target:** CA-D007, ARCHITECTURE_REORGANIZATION_CAN_PRECEDE_SCALAR_TRANSFORMATION

## MFR-01 Frozen claim

claim_id: CA-D007-D02E-v0.1

Exact claim:

Under a graded bolt-interface perturbation in the selected offshore-jacket experiment, independently measured modal organization can cross its frozen change boundary before the licensed local modal damping coordinate crosses its frozen transformation boundary.

Scope:

- one scaled laboratory offshore-jacket structure;
- fixed A_1 white-noise excitation;
- four physical bolt locations;
- source-defined states Healthy 12 Nm, 9 Nm, 6 Nm, and NoBolt;
- lowest stable healthy modal family as the primary mode.

Frozen task:

Determine the ordinal onset relation between local modal damping and modal spatial organization across 12 -> 9 -> 6 -> NoBolt for each of four bolt locations.

Intended value axis:

prospective cross-level ordering/identifiability, not superiority over native structural dynamics.

Version: D02E-v0.1.

## MFR-02 Hypothesis provenance

DATA_DERIVED + CROSS_DOMAIN_TRANSFER.

CA-D007 was generated after D02B.

D02C was a prospective null.
D02D was prospectively indeterminate.

D02E is new decisive evidence and was not used to generate CA-D007.

## MFR-03 Target native observables

Local scalar:

modal damping ratio zeta estimated from the half-power bandwidth of the first FDD singular-value resonance:

chi_local = zeta = Delta_f / (2 f_n).

Organization observable:

complex mode-shape dissimilarity of the FDD first left singular vector relative to the healthy reference:

D_org = 1 - |v_ref^H v|^2.

The 24 accelerometer channels provide the spatial response vector.

Bolt torque/state is the externally controlled intervention coordinate.

## MFR-04 Representation and validity regime

Native model:

linear operational/modal vibration analysis under stationary broadband shaker excitation.

Primary operational condition:

A_1 only.

Primary structural sequence:

Healthy 12 Nm, 9 Nm, 6 Nm, NoBolt.

All 20 source replicates per state are retained.

Primary modal family:

lowest stable healthy FDD modal family selected from healthy A_1 data only under the baseline-only target-selection rule below.

Half-power chi is licensed only when:

- one locally dominant FDD singular-value peak is identified;
- both half-power crossings occur inside the frozen tracking window;
- the peak is not at the window boundary;
- no competing peak exceeds 90% of the selected peak within the frozen window;
- Delta_f > 0.

Otherwise the scalar is refused.

Organization is licensed only when the same modal family can be tracked and its complex singular vector is finite and unit-normalizable.

## Baseline-only target-selection rule

Before any 9 Nm, 6 Nm, or NoBolt vibration file is opened:

1. compute a 24-channel FDD spectrum for each of the 20 Healthy A_1 replicates;
2. construct the median first-singular-value spectrum across healthy replicates;
3. find local modal peaks between 0.5 Hz and 100 Hz;
4. require a peak to be identifiable in at least 16/20 healthy replicates within +/-5% of the median peak frequency;
5. require finite half-power chi in at least 16/20 healthy replicates;
6. order qualifying families by median frequency;
7. freeze the lowest qualifying family as primary;
8. freeze the second-lowest qualifying family, if present, as secondary robustness only.

No damaged file may influence mode selection.

## MFR-05 Strongest relevant native comparator

Comparator status:

COMPARATOR_IDENTIFIED.

Comparator:

standard Frequency Domain Decomposition / operational modal analysis with half-power damping and complex modal-assurance comparison across bolt states.

Comparator selection basis:

the source is explicitly a vibration/structural-health-monitoring benchmark with distributed accelerometers and controlled bolt loosening. Standard modal frequency, damping, and mode-shape tracking directly address the frozen task.

Comparator freeze date:

2026-09-23.

SymC does not receive added-value credit for quantities already expressed by the native FDD/OMA toolkit.

## MFR-06 Null / competing explanations

N1:
bolt loosening changes modal damping before measurable spatial mode-shape organization.

N2:
damping and organization cross their frozen boundaries at the same torque level.

N3:
neither observable crosses its frozen boundary.

N4:
apparent ordering is caused by estimator sensitivity or modal non-identifiability rather than physical level ordering.

N5:
location-specific mixed orderings prevent a domain-level ordering claim.

## MFR-07 Expected response

CA-D007 expected response:

for the primary healthy-selected mode, organization onset occurs at a weaker perturbation level than scalar onset in most physical bolt-location strata.

No exact torque onset is predicted.

## MFR-08 Decision / adjudication rule

For each physical location independently:

states are ordered:

12 Nm baseline < 9 Nm < 6 Nm < NoBolt

in perturbation severity.

Define:

t_org = first non-baseline state classified ORGANIZATION_CHANGED.

t_chi = first non-baseline state classified SCALAR_TRANSFORMED.

Location outcomes:

- ORGANIZATION_PRECEDES_SCALAR if t_org is less severe than t_chi;
- SCALAR_PRECEDES_ORGANIZATION if t_chi is less severe than t_org;
- SIMULTANEOUS_WITHIN_FROZEN_RESOLUTION if equal;
- ORGANIZATION_CHANGES_SCALAR_DOES_NOT if organization changes and scalar never does;
- SCALAR_CHANGES_ORGANIZATION_DOES_NOT if scalar changes and organization never does;
- NEITHER_CHANGES if neither changes;
- ORDERING_NON_IDENTIFIABLE if completeness/admission prevents ordering.

Primary domain-level support requires:

- at least 3 of 4 locations are ORGANIZATION_PRECEDES_SCALAR or ORGANIZATION_CHANGES_SCALAR_DOES_NOT;
- zero locations are SCALAR_PRECEDES_ORGANIZATION.

Primary domain-level adverse ordering requires:

- at least 3 of 4 locations are SCALAR_PRECEDES_ORGANIZATION or SCALAR_CHANGES_ORGANIZATION_DOES_NOT;
- zero locations are ORGANIZATION_PRECEDES_SCALAR.

All other mixtures are INDETERMINATE or NO_SUPPORT under the frozen rule.

The secondary mode cannot rescue a failed primary mode.

## MFR-09 Uncertainty, tolerance, indeterminate zone

Replicate unit:

one source CSV experiment.

Each state has 20 source replicates.

Scalar state summary:

- median admitted chi across replicates;
- 10,000 bootstrap resamples of replicate-level median with fixed seed 20260923;
- 95% percentile interval.

Healthy scalar reference:

95% bootstrap interval of healthy median chi.

SCALAR_TRANSFORMED only when the damaged-state 95% bootstrap interval is fully outside the healthy 95% bootstrap interval.

Organization healthy reference:

- align complex modal-vector global phase by inner product;
- form healthy replicate projectors P_i = v_i v_i^H;
- v_ref is the principal eigenvector of mean(P_i).

Healthy leave-one-out dissimilarity:

for each healthy replicate, compute D_org against a reference built from the other 19.

T_org = 97.5th percentile of the 20 healthy leave-one-out D_org values.

For each damaged state:

ORGANIZATION_CHANGED only when the 2.5th percentile of its 20 replicate D_org values is strictly greater than T_org.

Completeness floor per state:

- at least 16/20 valid scalar replicates to adjudicate scalar;
- at least 16/20 valid organization replicates to adjudicate organization.

Any earlier non-identifiable state blocks a later onset from being used to infer ordering.

## MFR-10 Evidence-independence / leakage map

Hypothesis discovery:
D02B, separate dataset.

Prior prospective tests:
D02C and D02D, separate systems.

D02E candidate selection:
methods, metadata, file counts, repository access, intervention labels, and generic native statement that bolt state affects vibration.

D02E target-mode selection:
Healthy A_1 files only.

D02E decisive evidence:
A_1 9 Nm, 6 Nm, and NoBolt files at four locations.

No damaged D02E vibration values were inspected before this MFR freeze.

## MFR-11 Multiplicity / search-space accounting

Primary family:

one baseline-selected modal family.

Primary strata:

four physical bolt locations.

Primary endpoints:

one scalar onset and one organization onset per location.

Domain-level adjudication is the fixed 3-of-4 symmetric rule in MFR-08.

Secondary family:

one second-lowest baseline-selected family, if eligible, reported as robustness only and prohibited from changing the primary verdict.

No alternate excitation amplitude, mode, threshold, channel subset, or location subset may replace the primary analysis after outcome inspection.

A_05 and A_2 remain untouched sensitivity strata.

## MFR-12 Freeze identity and untouched decisive test

Freeze identity:

Git commit containing this MFR and the D02E selection record.

Engine/model:

to be implemented after this freeze behind:

python chi_architecture/reproduce.py d02e

Confirmatory dataset:

DOI 10.34810/data1011, version 3.0.

Frozen decisive slice:

A_1 original CSV files:
- Healthy, all 20 replicates;
- 9 Nm level_1..level_4, all 20 each;
- 6 Nm level_1..level_4, all 20 each;
- NoBolt level_1..level_4, all 20 each.

Dataverse-generated .tab files are excluded.

## MFR-13 Explicit falsifier

Results count against CA-D007 in D02E if the frozen primary mode produces the primary adverse ordering defined in MFR-08:

at least 3 of 4 physical locations show scalar-first or scalar-only change and none show organization-first.

A mixed result, simultaneous result, neither-change result, or incompleteness does not support CA-D007 and is retained as null/indeterminate rather than redescribed as success.

## MFR-14 Precommitted failure consequence

If MFR-13 occurs:

- CA-D007 is classified DOMAIN_LIMITED_TO_GENERATING_SYSTEM_OR_RETIRED_PENDING_NEW_MECHANISM;
- the program stops pursuing the current organization-first ordering as a promotable general physical hypothesis;
- D02B remains a descriptive physical result;
- no post-hoc threshold or alternate mode may rescue D02E;
- any replacement hypothesis enters the discovery ledger with new promotion debt.

If D02E is null or indeterminate:

- CA-D007 remains unconfirmed;
- no promotion occurs;
- another prospective test is justified only if it resolves a specific measured power/identifiability limitation rather than merely seeking a favorable outcome.
