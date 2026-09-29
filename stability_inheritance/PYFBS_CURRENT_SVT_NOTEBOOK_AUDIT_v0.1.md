# pyFBS Current Official SVT Notebook Audit v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** SOURCE-CODE / PROVENANCE AUDIT ONLY
**Target FRF values:** PROHIBITED
**Evidence class:** P0-Q native-method implementation audit

## Purpose

The measured pyFBS SVT lane failed to reproduce the documented B-to-AB transformation under the tested released packages and frozen metadata route. Current pyFBS documentation still specifies k=6 and the same high-level SVT/LM-FBS operation.

Before closing the implementation lane permanently, inspect the current maintained official example notebook to determine whether its actual metadata loading, channel filtering, grouping, or API calls differ from the legacy documentation used in the prior protocol.

## Official source

Current maintained repository:
https://gitlab.com/pyFBS/pyFBS

Notebook:
examples/09_FBS_decoupling_SVT.ipynb

Raw source:
https://gitlab.com/pyFBS/pyFBS/-/raw/master/examples/09_FBS_decoupling_SVT.ipynb

## Allowed operations

- download the notebook source only;
- record byte size and SHA-256;
- parse JSON code cells;
- extract code cells containing any of:
  - positional-data filename/path;
  - Channels_B / Impacts_B / Channels_AB / Impacts_AB loading;
  - dataframe filtering/subselection;
  - grouping_no/group;
  - k / no_svs;
  - SVT construction;
  - apply_SVT/apply_svt;
  - Y_A/Y_B/Y_AB file paths;
  - LM-FBS block construction and extraction indices.

## Prohibited operations

- do not download Y_A, Y_B, or Y_AB in this audit;
- do not execute the notebook;
- do not alter a parameter to obtain a desired target score;
- do not infer physical evidence from software implementation details.

## Dispositions

- CURRENT_NOTEBOOK_ROUTE_IDENTIFIED if the required metadata and SVT construction route can be reconstructed unambiguously from current code.
- CURRENT_NOTEBOOK_ROUTE_INCOMPLETE if the current notebook does not contain enough self-contained information.
- SOURCE_AUDIT_BLOCKED if the official notebook cannot be retrieved or parsed.

## Consequence

If the current notebook identifies an independently documented route that differs materially from the failed protocol, a new post-failure P0-Q compatibility preflight may be frozen before any target scoring.

If it does not, keep the measured pyFBS SVT route closed.
