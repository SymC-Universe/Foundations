# Rubber-Isolator Cross-Assembly Public-File Intake v0.1b

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Dataset:** Identification of rubber isolator dynamics: substructure frequency response functions for identification and cross validation
**Public identifier:** 38cp7wdjz7
**DOI:** 10.17632/38cp7wdjz7.1
**Status:** FROZEN P0-Q TRANSPORT / METADATA INTAKE
**Numeric FRF scoring:** PROHIBITED
**P1 eligibility:** NO

## Reason for new transport route

Two prior metadata-only attempts using Mendeley/Digital Commons API endpoints failed before any HDF5 download:
- v0.1: HTTP 401
- v0.1a: HTTP 404

The public dataset page remains accessible and lists the expected files under CC BY 4.0. Public Mendeley file-download links are also exposed through stable public-file routes of the form:

https://data.mendeley.com/public-files/datasets/<dataset_slug>/files/<filename>/download

This v0.1b intake uses that public route directly and remains metadata-only.

## Frozen allowed operations

For experimental.h5 and numerical.h5:
- issue HTTP HEAD requests only;
- record final URL, status, content type, content length, ETag/Last-Modified if present;
- do not read response bodies.

For README.md:
- download the complete README only;
- record byte length and SHA-256;
- preserve the README text because it contains structure documentation rather than FRF numeric arrays.

## Prohibited operations

- do not download experimental.h5 or numerical.h5 bodies;
- do not open HDF5 groups or datasets;
- do not inspect FRF values;
- do not define frequency bands, channels, VPT mappings, or scoring metrics from target data;
- do not claim cross-assembly transfer before a separately frozen protocol.

## Intake dispositions

- INTAKE_METADATA_PASS if both HDF5 HEAD requests return successful public metadata and README.md downloads successfully.
- INTAKE_PUBLIC_ROUTE_PARTIAL if README downloads but one or both HDF5 HEAD requests are unsupported/unavailable.
- INTAKE_PUBLIC_ROUTE_BLOCKED if README cannot be retrieved from the official public-file route.
- INTAKE_IDENTITY_MISMATCH if filenames/content types materially contradict the public dataset page.

An INTAKE_METADATA_PASS permits a separate non-value HDF5 layout preflight before any scientific scoring.
