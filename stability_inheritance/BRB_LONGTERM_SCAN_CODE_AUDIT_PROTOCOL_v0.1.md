# Brake-Reuss Beam Long-Term Interface-Scan Code Audit v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Status:** P0-Q NATIVE PROCESSING SOURCE AUDIT / NO SCAN OUTCOME ACCESS
**Canonical OSF project:** fbwhz
**Scientific score:** NONE

## Purpose

Determine the native processing semantics used by the long-term BRB dataset for interface scans before any interferometer height outcomes are analyzed.

The audit is limited to the three author-provided MATLAB scripts:
- scan_a_rawdat2meshsort.m
- scan_b_visdata.m
- scan_c_elemaspID.m

## Allowed operations

- download the three scripts from their public OSF file routes;
- compute SHA-256;
- preserve line numbers and code lines containing data-import, outlier/rejection, stitching/sorting, detrending/plane handling, roughness/asperity, peak/local-max, statistical-moment, area/volume, or element-assignment semantics;
- identify named intermediate/output objects and whether the scripts save processed MAT objects.

## Prohibited operations

- do not download any scan CSV/ZON/JPG/MAT data;
- do not inspect before/after surface values;
- do not choose a micro-scale metric from an observed macro-scale correlation;
- do not claim SI novelty.

## Dispositions

- SCAN_NATIVE_PROCESSING_ROUTE_IDENTIFIED if all three scripts are accessible and sufficient processing/statistical semantics are recovered to specify an outcome-blind scan metric protocol.
- SCAN_NATIVE_PROCESSING_ROUTE_INCOMPLETE if the scripts are accessible but do not define enough semantics.
- SCAN_SOURCE_AUDIT_BLOCKED if any required script cannot be acquired.

A successful audit permits a separately frozen interface-state metric protocol.
