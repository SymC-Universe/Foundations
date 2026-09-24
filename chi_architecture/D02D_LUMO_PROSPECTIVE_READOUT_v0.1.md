# D02D LUMO Prospective Test of CA-D007 v0.1

**Date:** 2026-09-23  
**Status:** PROSPECTIVE_EXTERNAL_PHYSICAL_INDETERMINATE  
**Current governance authority:** SymC General Operations Manual v0.8.6  
**Frozen scientific authority:** D02D MFR-14 and final preexecution freeze created under GOM v0.8.4  
**Claim ID:** CA-D007-D02D-LUMO-v0.1  
**Dataset DOI:** 10.25835/0027803  
**Successful workflow:** 35904120749  
**Execution commit:** 856ed0ae63df13b557fba8a4cfd44aa8c720c32e  
**Artifact ID:** 10770159354  
**Full result SHA-256:** f372bb0e7e1069fe731e49b8831c3d39559eea5c61679df42e6a428e4f92c111

## Status

D02D is the second prospectively frozen external physical test of CA-D007.

The frozen program-level result is:

`INDETERMINATE`.

All three damage-location strata are:

`ORDERING_NON_IDENTIFIABLE`.

The native-toolkit verdict is:

`NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE`.

D02D does not support CA-D007 and does not satisfy its frozen falsification rule.

## What happened

The selected healthy mode families were identifiable in all three locations and both directions:

- X family: approximately 2.82258 Hz;
- Y family: approximately 2.77218 Hz.

All healthy and damaged blocks were modally tracked under the frozen +/-0.15 Hz rule.

The decisive loss of identifiability occurred later, at the environmental and operational matching gate.

The final preexecution freeze required at least 10 of 15 damaged blocks to remain inside the paired healthy rectangle in both:
- median temperature;
- directional log RMS acceleration.

When fewer than 10 matched damaged blocks remained, both scalar and organization status were frozen to NON_IDENTIFIABLE for that severity/direction.

### DAM3

010:
- X matched 8/15;
- Y matched 8/15.

111:
- X matched 3/15;
- Y matched 3/15.

Both severities fail the >=10 matching floor in both directions.

Location outcome:

`ORDERING_NON_IDENTIFIABLE`.

### DAM4

010:
- X matched 11/15;
- Y matched 12/15.

The 010 state is adequate and both scalar and organization remain UNCHANGED.

111:
- X matched 5/15;
- Y matched 3/15.

The 111 state fails the matching floor.

Location outcome:

`ORDERING_NON_IDENTIFIABLE`.

### DAM6

010:
- X matched 6/15;
- Y matched 6/15.

The 010 state fails the matching floor.

111:
- X matched 12/15;
- Y matched 12/15.

The 111 state is adequate.

At DAM6 111:

X direction:
- organization: CHANGED;
- scalar: UNCHANGED.

Y direction:
- organization: CHANGED;
- scalar: TRANSFORMED.

These are valid native observations at the 111 severity, but the frozen ordering test requires the preceding 010 state to be identifiable. Because 010 fails the completeness floor, neither direction receives an onset ordering.

Location outcome:

`ORDERING_NON_IDENTIFIABLE`.

## Why it matters

D02D does not fail because the modal family disappeared, the half-power estimator collapsed, or the organization metric became numerically undefined.

It fails prospectively because the frozen environmental matching firewall removes too many damaged blocks to establish the graded 010 -> 111 ordering.

This distinction matters.

The experiment therefore identifies a concrete limitation in the current prospective design:

`PHYSICAL_SIGNAL_AVAILABLE != ORDERING_IDENTIFIABLE`

when environmental and operational overlap is insufficient to preserve the full graded comparison.

The DAM6 111 observations cannot be promoted into organization-first evidence because doing so would violate the frozen completeness and ordering rules.

## CA-D007 consequence

D02D's MFR-14 precommitted consequence for an indeterminate result was:

- CA-D007 remains unconfirmed;
- no promotion occurs;
- the next experiment targets the specific source of indeterminacy.

That consequence is applied exactly.

After D02C and D02D, the prospective record is:

1. D02C: `PROSPECTIVE_NULL / NO_SUPPORT / NO_CLEAN_REVERSAL`.
2. D02D: `INDETERMINATE / ENVIRONMENTAL-MATCHING COMPLETENESS FAILURE`.

CA-D007 therefore has:
- one post-result generating system, D02B;
- zero prospective supporting systems;
- one prospective null;
- one prospective indeterminate test.

It must not be described as prospectively replicated.

## Native-toolkit comparison

All D02D quantities are standard structural-dynamics objects:

- FDD spectral families;
- half-power damping ratio;
- complex spatial mode vectors;
- MAC-type projective dissimilarity;
- temperature matching;
- excitation-level matching.

No additional SymC variable is required.

Verdict:

`NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE`.

## Integrity note

The GitHub Actions artifact was immutable and all output hashes were computed before scientific interpretation.

A sequencing deviation occurred after hashing: the compact result card was opened locally before the archive checkpoint commit.

No source, code, scientific rule, result file, artifact, or threshold changed after that exposure.

The archive record preserves this deviation explicitly. D02D remains computationally reproducible, but its archive sequence is not described as perfectly blind.

## What happens next

A D02E test should not relax D02D's matching rectangle or completeness floor.

Instead, candidate eligibility should require, using metadata or non-decisive control information only, that every graded intervention level has enough environmental and operational overlap with its paired control to make the frozen >=10-of-15 style completeness floor achievable.

The relative scalar-versus-organization ordering must remain uninspected.

This converts the next design problem from threshold relaxation into prospective data-adequacy qualification.
