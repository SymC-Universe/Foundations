# D02C Onset Completeness Rule v0.1

**Date:** 2026-09-23  
**Status:** PREEXECUTION_FAIL_CLOSED_RULE  
**Authority:** SymC GOM v0.8.3

## Purpose

Prevent missing/refused measurements from creating an artificial ordering.

## Valid intervention status

For each of the twelve intervention windows and each direction:

Scalar status must be one of:
- UNCHANGED
- TRANSFORMED
- NON_IDENTIFIABLE

Organization status must be one of:
- UNCHANGED
- CHANGED
- NON_IDENTIFIABLE

## Onset identifiability

An onset at window k is identifiable only when:

- the relevant observable is valid at window k;
- every earlier intervention window 1..k-1 is valid and explicitly UNCHANGED.

If any earlier window is NON_IDENTIFIABLE, the onset is not prospectively identifiable.

## No-change identifiability

A conclusion that an observable DOES_NOT_CHANGE requires all twelve intervention windows to be valid and UNCHANGED.

If any intervention window is NON_IDENTIFIABLE and no earlier identifiable change has already occurred, the no-change statement is not identifiable.

## Pairwise ordering

A direction receives an ordering class only when both observable histories support the class without an earlier missing-data ambiguity.

Otherwise return:

ORDERING_NON_IDENTIFIABLE.

## Sensitivity-precluded priority

If an organization onset would be identifiable using the midnight baseline threshold alone, but is removed or delayed past an otherwise decisive ordering by the dry-run thermal threshold, return:

NATIVE_MEASUREMENT_SENSITIVITY_PRECLUDES_ORDERING

rather than a favorable CA-D007 ordering.

## Minimum control adequacy

Scalar control envelope requires at least:
- 10 valid midnight baseline scalar points;
- 20 valid total pre-spray scalar points between 00:00 and 11:20 UTC.

Organization reference requires:
- at least 10 valid midnight full-window mode vectors;
- at least 100 valid midnight 50-second blocks.

Dry-run organization firewall requires:
- 12 ten-minute dry-run windows;
- at least 100 valid dry-run 50-second blocks.

Failure of these floors prevents a positive CA-D007 outcome.

## No post-result relaxation

These completeness floors cannot be lowered after execution.
