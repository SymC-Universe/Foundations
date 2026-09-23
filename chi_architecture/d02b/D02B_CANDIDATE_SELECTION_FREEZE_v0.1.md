# D02B Candidate Selection Freeze v0.1

**Date:** 2026-09-22  
**Status:** PRESELECTION_FROZEN_BEFORE_DECISIVE_OUTCOME_INSPECTION  
**Authority:** SymC GOM v0.8.3  
**Parent checkpoint:** D02A-CP4-CLOSED

## Purpose

Select the next physical/domain-native Stability Inheritance test by source completeness and native interpretability rather than by whether the system appears to support the working hypothesis.

## Exclusion

CsPbBr3 is excluded because it already served as D02A calibration.

## Required eligibility axes

A candidate is eligible only if all six axes can be satisfied without reverse-fitting the target claim:

1. **Direct same-condition scalar inputs**
   - same-condition natural frequency or equivalent native restoring frequency is directly reported, tabulated, or recoverable from a machine-readable source;
   - same-condition damping, linewidth, decay rate, or equivalent dissipative term is directly reported or recoverable;
   - units and conventions are sufficient to test whether a licensed lowercase chi can be constructed without fitting the desired result.

2. **Independent carrier/coupling structure**
   - mode identity, eigenvector/subspace, component identity, network path, coupling coefficient, or another native carrier/organization descriptor is independently defined.

3. **Controlled organization change**
   - coupling, substrate, boundary condition, temperature, pressure, field, environment, geometry, or another native control changes while enough lower-level information remains measurable to test preservation/transformation/refusal.

4. **Independent response consequence**
   - ring-down, transfer function, transient amplification, recovery, switching, redistribution, or another outcome exists that is not algebraically identical to the coordinate being tested.

5. **Strong native comparator**
   - the domain has an established native analysis that can fully defeat the SymC added-value claim if sufficient.

6. **Reproducibility**
   - open-access full text plus machine-readable supplementary data, a public repository, or a stable downloadable dataset is available;
   - the analysis can be packaged behind one reviewer-facing GitHub entrypoint.

## Ranking rule

Among eligible candidates, rank only by:

1. machine-readable data accessibility;
2. directness of same-condition frequency+damping measurements;
3. independence of carrier/coupling measurement from response outcome;
4. presence of a controlled intervention/contrast;
5. availability of a strong native comparator;
6. simplicity of automated reproduction.

Do **not** rank by:
- closeness to chi=1;
- apparent support for stability inheritance;
- visual agreement with an Atlas;
- presence of an exceptional point;
- magnitude of an effect;
- favorable narrative.

## Selection rule

Select the highest-ranked candidate for which all required source fields can be verified.

If no candidate satisfies all six axes, return NO_ELIGIBLE_D02B_SYSTEM and preserve that as the result.

## Predeclared D02B outcome states

The selected system may yield any of:

- PRESERVED
- TRANSFORMED
- REORGANIZED
- LOCAL_SCALAR_VALID_BUT_EMBEDDED_INSUFFICIENT
- NO_ADMISSIBLE_SCALAR_CHI
- NON_IDENTIFIABLE
- NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE
- NO_RELATION_DETECTED
- CONTRADICTS_INHERITANCE_HYPOTHESIS

No outcome will be converted after inspection merely to preserve continuity.

## Reproduction target

The eventual supported reviewer command should be:

python chi_architecture/reproduce.py d02b

Internal files may be multiple, but the reviewer-facing interface remains one experiment command.
