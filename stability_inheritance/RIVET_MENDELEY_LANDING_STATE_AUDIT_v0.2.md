# Riveted-Joint Mendeley Landing-Page State Audit v0.2

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Status:** FINAL METADATA-ONLY SOURCE DISCOVERY PASS
**Parents:** RIVET_MENDELEY_SOURCE_DISCOVERY_v0.1.md; RIVET_MENDELEY_METADATA_STRUCTURE_AUDIT_v0.1.md
**Evidence class:** PUBLIC DATASET INTAKE / NO NUMERIC FRF ACCESS

## Purpose

Inspect only the public landing-page HTML and embedded script/JSON state for stable official file descriptors associated with data.h5.

This is the final source-discovery attempt before placing the raw dataset lane on SOURCE_ACCESS_HOLD.

## Allowed operations

- fetch the public dataset landing page;
- inventory script tags and JSON-LD / embedded application-state blocks;
- search those text blocks for data.h5, Structure_images.jpg, file IDs, UUIDs, public-files URLs, and download fields;
- issue HEAD only to any official file URL recovered.

## Prohibited operations

- no HDF5 body download;
- no FRF value access;
- no unofficial mirror;
- no inference from numeric response data.

## Dispositions

- OFFICIAL_FILE_ROUTE_DISCOVERED
- FILE_DESCRIPTOR_WITHOUT_ROUTE
- LANDING_STATE_INSUFFICIENT

If LANDING_STATE_INSUFFICIENT, place the raw rivet dataset on SOURCE_ACCESS_HOLD and do not continue transport probing absent a newly documented official route.
