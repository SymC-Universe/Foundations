# D02D LUMO MFR-14 v0.1

**Date:** 2026-09-23  
**Status:** COMPLETE_CONFIRMATORY_FREEZE_BEFORE_DECISIVE_DAMAGE-STATE ANALYSIS  
**Authority:** SymC General Operations Manual v0.8.4  
**Claim ID:** CA-D007-D02D-LUMO-v0.1

## MFR-01 Frozen claim

Exact claim:

Within at least one independently retained LUMO damage-location stratum, graded structural damage can produce a detectable reorganization of the embedded spatial vibration organization at a weaker damage extent than the damage extent at which the local modal damping coordinate crosses its prospectively frozen control boundary.

Scope:
- LUMO benchmark only;
- retained damage locations DAM3, DAM4, DAM6;
- healthy -> 010 -> 111 severity ladder;
- one prospectively selected low-order mode family per principal horizontal direction where identifiable.

Intended value axis:
relative onset ordering of local modal damping versus independent spatial organization.

## MFR-02 Hypothesis provenance

- DATA_DERIVED: CA-D007 originated from D02B.
- CROSS_DOMAIN_TRANSFER: D02D transfers the graded-ordering question to an untouched lattice-tower system.
- Prior prospective evidence: D02C returned a null and does not support the claim.

## MFR-03 Target object / native observable

Local scalar:
modal damping ratio zeta for the frozen mode family, estimated from multichannel vibration data with a native operational-modal route.

Organization:
complex spatial mode-vector / dominant cross-spectral eigenspace across the frozen accelerometer channel set, compared by phase-invariant complex modal assurance dissimilarity.

Damage control:
source-defined physical states healthy, 010, 111 at DAM3, DAM4, DAM6.

## MFR-04 Representation and validity regime

Native regime:
short-window approximately linear structural vibration under ambient excitation.

Scalar:
chi_local = zeta.

No whole-tower scalar is defined.

Scalar is refused when:
- the mode cannot be uniquely tracked;
- damping is non-finite/non-positive;
- estimator uncertainty is unresolved;
- modal overlap or insufficient excitation defeats the frozen identification route.

Organization is refused when:
- the same mode family cannot be tracked;
- too few spatial channels are valid;
- the cross-spectral eigenspace is numerically non-identifiable.

## MFR-05 Strongest relevant native comparator

Comparator status:
COMPARATOR_IDENTIFIED.

Strongest comparator:
standard Operational Modal Analysis / SSI-COV modal frequency, damping, and mode-shape tracking with MAC-based damage assessment and environmental/operational-variability control.

Comparator basis:
the LUMO methods paper and structural-health-monitoring literature for the benchmark.

Freeze date:
2026-09-23.

## MFR-06 Null / competing explanations

H0-A:
damping and spatial organization respond at the same first severity level.

H0-B:
damping changes before spatial organization.

H0-C:
neither observable crosses its control boundary.

H0-D:
apparent ordering is attributable to environmental/operational variability or unequal estimator sensitivity.

H0-E:
mode tracking becomes non-identifiable before a valid ordering can be assigned.

## MFR-07 Expected response

Target CA-D007-compatible ordering:

healthy -> 010:
organization changes while chi remains inside its frozen healthy control region;

010 -> 111:
chi subsequently transforms or becomes refused/non-identifiable while organization remains changed or changes further.

The exact same ordering is not required at all three damage locations.

A positive D02D result requires at least two of three damage locations to show organization-first ordering and none to show a clean scalar-first ordering under comparable completeness.

## MFR-08 Decision / adjudication rule

Each damage location receives one class:

- ORGANIZATION_PRECEDES_SCALAR
- SCALAR_PRECEDES_ORGANIZATION
- SIMULTANEOUS_AT_010
- SIMULTANEOUS_AT_111
- ORGANIZATION_ONLY_THROUGH_111
- SCALAR_ONLY_THROUGH_111
- NEITHER_CHANGES
- ORDERING_NON_IDENTIFIABLE
- NATIVE_MEASUREMENT_SENSITIVITY_PRECLUDES_ORDERING

Program-level D02D outcome:

EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST only if:
- at least two locations are ORGANIZATION_PRECEDES_SCALAR or ORGANIZATION_ONLY_THROUGH_111;
- no location is SCALAR_PRECEDES_ORGANIZATION;
- completeness floors are met;
- the environmental/sensitivity firewall does not preclude the result.

EMPIRICAL_CLAIM_FALSIFIED if:
- at least two locations are SCALAR_PRECEDES_ORGANIZATION under adequate completeness, or
- all three adequate locations show simultaneous or scalar-first behavior with zero organization-first strata.

INDETERMINATE otherwise.

## MFR-09 Uncertainty, tolerance, indeterminate zone

Scalar control:
healthy-state chi distribution is estimated from repeated healthy 10-minute windows paired to each damage campaign.

A damage-state scalar is transformed only when its uncertainty interval lies wholly outside the paired healthy control envelope.

Organization control:
healthy-state block-level complex-MAC dissimilarity defines a campaign-specific no-change envelope.

A damaged state is changed only when its lower uncertainty quantile exceeds the maximum healthy-control dissimilarity.

The exact bootstrap/block counts and estimator-specific intervals must be frozen after source schema inspection but before damage-state values are opened.

Any missing control floor, unresolved mode identity, or estimator failure yields ORDERING_NON_IDENTIFIABLE rather than threshold relaxation.

## MFR-10 Evidence independence / leakage map

Discovery source:
D02B bolted plate.

Prior prospective test:
D02C wind blade.

D02D decisive data:
LUMO lattice tower, unused in D02B/D02C.

Shared conceptual structure:
damping scalar plus independent spatial organization.

Not shared:
physical specimen, source repository, intervention, raw measurements, damage architecture, frozen thresholds.

Selection used:
methods, repository structure, damage labels, and known activity of structural modal response.

Selection did not use:
relative damping-versus-organization onset at 010 or 111.

## MFR-11 Multiplicity / search-space accounting

Confirmatory family:
- 3 damage locations;
- up to 2 principal horizontal directions per location;
- 2 damaged severity levels.

No post-result location selection is allowed.

The location-level decision is primary.

Direction-level outcomes are nested within location and do not count as independent replication strata.

If both directions are identifiable and disagree within a location, that location is ORDERING_NON_IDENTIFIABLE unless a pre-frozen native mode-family hierarchy resolves the disagreement before damage outcomes are opened.

## MFR-12 Freeze identity and untouched decisive test

Freeze:
this file and its Git commit.

Dataset:
LUMO, DOI 10.25835/0027803.

Decisive resources:
the source-provided exemplary paired healthy/damaged ZIP resources for DAM3, DAM4, DAM6 at 010 and 111 extents.

Engine:
D02D production implementation to be committed after schema-only source inspection and before decisive modal calculation.

Untouched requirement:
damage-state damping and organization values must not be inspected before the final schema/method freeze.

## MFR-13 Explicit falsifier

A clean scalar-first ordering in at least two adequate damage locations falsifies the frozen empirical claim.

A fully adequate three-location map with no organization-first location and no measurement-sensitivity explanation also counts against the claim according to MFR-08.

## MFR-14 Precommitted failure consequence

If falsified:
- CA-D007 is marked EMPIRICAL_CLAIM_FALSIFIED for the current generalized physical-ordering formulation;
- the claim is removed from the active promotion path;
- D02B remains a system-specific physical observation;
- no threshold, mode family, location, or scalar definition is retuned to rescue the claim;
- any new narrower hypothesis is entered as a post-result discovery with new promotion debt.

If indeterminate:
- CA-D007 remains unconfirmed;
- no promotion occurs;
- the next experiment must target the specific source of indeterminacy rather than reinterpret D02D as support.


## Pre-execution amendment A1: complete simultaneous-outcome vocabulary

**Date:** 2026-09-23  
**Timing:** before any damaged LUMO scientific array value was opened.

MFR-08 originally named SIMULTANEOUS_AT_010 but omitted the logically possible case in which both observables remain unchanged at 010 and first change together at 111.

The outcome vocabulary is therefore completed with:

SIMULTANEOUS_AT_111

This amendment closes a categorical gap. It does not alter the survival or falsification direction: simultaneous behavior does not support organization-first ordering and counts with simultaneous/scalar-first adequate maps under the existing all-three-locations falsification clause.
