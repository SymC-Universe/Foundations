# D02E Candidate Selection Freeze v0.1

**Date:** 2026-09-23  
**Status:** FROZEN_BEFORE_CANDIDATE_OUTCOME_INSPECTION  
**Authority:** SymC General Operations Manual v0.8.6  
**Target hypothesis:** CA-D007, ARCHITECTURE_REORGANIZATION_CAN_PRECEDE_SCALAR_TRANSFORMATION

## Purpose

Select a third prospective external physical test that improves power against the two prior prospective failure modes without selecting on the desired ordering.

Known prospective outcomes:

- D02C: prospective null, no frozen scalar or organization onset;
- D02D: prospective indeterminate, insufficient environmental/operational overlap for complete graded ordering.

Neither outcome authorizes relaxing the CA-D007 falsification structure.

## Required eligibility axes

A D02E candidate is eligible only if every axis is verified before decisive relative-onset values are inspected.

### E1. Graded intervention

At least three ordered states including reference/baseline and at least two non-baseline perturbation levels.

The levels must be externally defined by the experiment, not created by binning a continuous response after inspection.

### E2. Licensed local scalar

A directly measured or natively recoverable local/modal scalar must exist under the same condition as each intervention level.

Allowed examples include a native damping ratio, linewidth/frequency coordinate, Q-derived damping coordinate, or another domain-native scalar with a frozen interpretation.

No proxy may be invented because it produces a useful ordering.

### E3. Independent organization observable

A carrier, mode shape, network, spatial response, coupling, eigenvector/subspace, or another native organization observable must be measurable independently of the local scalar.

The organization observable may share raw sensors but may not be an algebraic transform of the scalar.

### E4. Automated public access

The decisive data and metadata must be downloadable from GitHub Actions or another ordinary noninteractive reproducibility environment through stable public URLs, DOI APIs, or a public repository.

A system requiring browser-only manual assembly is ineligible.

### E5. Intervention-power evidence without ordering leakage

Before candidate selection, native documentation or a source-level methods statement must establish that the planned intervention range measurably affects at least one relevant system observable.

The relative onset ordering of the frozen scalar and organization observables must remain uninspected.

A candidate is not eligible merely because a paper abstract says damage/perturbation was detectable if that statement reveals the exact relative ordering targeted by CA-D007.

### E6. Prospective completeness/overlap adequacy

Before decisive outcome inspection, the source metadata/schema must demonstrate enough observations at every required perturbation level to satisfy the planned scalar and organization uncertainty rules.

If environmental/operational matching is required, the overlap floor must be verifiable from covariate metadata before selection.

Prefer laboratory systems in which intervention levels are measured under matched acquisition conditions so the D02D overlap failure cannot recur.

### E7. Native comparator

The domain must supply a standard native analysis capable of defeating the SymC added-value interpretation.

### E8. Outcome symmetry

The frozen design must permit at least:

- ORGANIZATION_PRECEDES_SCALAR
- SCALAR_PRECEDES_ORGANIZATION
- SIMULTANEOUS_WITHIN_FROZEN_RESOLUTION
- ORGANIZATION_CHANGES_SCALAR_DOES_NOT
- SCALAR_CHANGES_ORGANIZATION_DOES_NOT
- NEITHER_CHANGES
- ORDERING_NON_IDENTIFIABLE
- NO_ADMISSIBLE_SCALAR_CHI
- NATIVE_MEASUREMENT_SENSITIVITY_PRECLUDES_ORDERING

## Ranking among eligible candidates

Rank only by:

1. completeness at every graded level;
2. automation/reproducibility;
3. independence of scalar and organization observables;
4. directness of scalar licensing;
5. strength of controlled intervention;
6. strength of native comparator;
7. simplicity of a one-command reproduction.

Do not rank by:
- organization-first appearance;
- closeness to any chi boundary;
- effect size after outcome inspection;
- novelty narrative;
- exceptional-point proximity;
- apparent agreement with D02B.

## Selection outcome

Select the highest-ranked fully eligible candidate.

If no candidate satisfies every axis, record:

NO_ELIGIBLE_D02E_SYSTEM

and do not lower the gate.

## Evidence ceiling

D02E is a prospective domain-specific physical test of CA-D007.

A single supportive D02E result would not establish universality or a program-level added-value claim.
