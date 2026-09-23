# D02D Candidate Selection Freeze v0.1

**Date:** 2026-09-23  
**Status:** PRESELECTION_FROZEN_BEFORE_DECISIVE_OUTCOME_INSPECTION  
**Authority:** SymC General Operations Manual v0.8.4  
**Target discovery:** CA-D007, ARCHITECTURE_REORGANIZATION_CAN_PRECEDE_SCALAR_TRANSFORMATION

## Purpose

Select a second prospective physical test with greater power against the D02C `NEITHER_CHANGES` null while preserving ignorance of the relative onset ordering.

## Required eligibility

A D02D candidate is eligible only when all conditions below can be verified before decisive outcome inspection.

1. At least three ordered perturbation/intervention levels, including a baseline.
2. A directly licensed local or modal scalar with native units/convention and a prospective uncertainty route.
3. An organization/carrier observable measured independently of the scalar and not a fixed algebraic transform of it.
4. Prior native evidence, protocol knowledge, or dataset design showing that the chosen intervention range measurably changes at least one of the two observables.
5. The relative scalar-versus-organization onset ordering has not been inspected by this program.
6. A strongest relevant native comparator can be frozen.
7. Public machine-readable data can be acquired automatically from a stable repository or API.
8. The decisive analysis can be exposed through one production command and one compact artifact bundle.
9. There is enough repeated measurement or uncertainty information to define separate detection boundaries for scalar and organization.
10. No prior SymC experiment used the decisive data.

## Exclusions

Do not select on:
- an apparent organization-first ordering;
- closeness to chi=1;
- exceptional-point proximity;
- agreement with D02B;
- visual Atlas alignment;
- effect size discovered from the decisive trajectory;
- a system whose scalar and organization coordinates are merely two algebraic views of the same fitted quantity.

## Ranking

Among eligible candidates, rank by:

1. independence of scalar and organization measurements;
2. intervention-level completeness;
3. directness of scalar convention;
4. independent evidence that the perturbation range is active;
5. uncertainty/replicate quality;
6. native-comparator strength;
7. automated reproducibility;
8. data volume/economy.

Outcome direction is not a ranking axis.

## Selection failure

If no candidate meets every required condition, return:

`NO_ELIGIBLE_D02D_SYSTEM`

and preserve the failed search rather than weakening eligibility.

## Next gate

After selection, D02D must receive a complete MFR-14 record before decisive evidence is opened. Candidate selection alone is not a confirmatory freeze.
