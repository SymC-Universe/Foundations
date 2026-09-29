# Riveted-Joint Mendeley Source Discovery v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Status:** FROZEN METADATA-ONLY SOURCE DISCOVERY
**Evidence class:** PUBLIC DATASET INTAKE / NO NUMERIC FRF ACCESS
**P1 eligibility:** NO

## Purpose

Discover a provenance-clean official file route for the two public Vrtac riveted-joint datasets before constructing any cross-host transfer-boundary analysis.

Datasets:
- small: 10.17632/sgmxhdc599.1
- large: 10.17632/dy66vm8t95.1

The dataset pages state CC BY 4.0 and describe data.h5 plus image/metadata assets.

## Scientific reason

Later-literature review establishes that generic transfer of a host-reduced joint representation across assemblies is already native prior art. The remaining useful question is conditional transfer: under which host/local-equivalence conditions does a declared interface representation preserve identity, reorganize, or become nontransportable?

No scientific score may be defined until official source identity is established.

## Allowed operations

For each dataset:

1. request only the public dataset landing page and documented/public metadata endpoints;
2. record HTTP status, redirect target, content type, response length, and SHA-256 of the metadata response;
3. extract candidate official file URLs, file identifiers, filenames, or download endpoints appearing in public metadata;
4. record whether data.h5, Structure_images.jpg, or equivalent published filenames are discoverable;
5. optionally issue HEAD requests to discovered official file URLs to record content length/type without downloading file bodies.

## Prohibited operations

- do not download data.h5 bodies;
- do not open FRF values;
- do not inspect force labels beyond public metadata already on the landing page;
- do not define train/test splits from numeric outcomes;
- do not use unofficial mirrors.

## Dispositions

- OFFICIAL_FILE_ROUTE_DISCOVERED if an official downloadable data.h5 route or stable public file identifier is found.
- METADATA_ROUTE_ONLY if public metadata is accessible but no direct official file route is exposed.
- SOURCE_DISCOVERY_BLOCKED if the public landing/metadata routes cannot be accessed.
- SOURCE_IDENTITY_CHANGED if the public DOI/page resolves to a materially different dataset identity.

An OFFICIAL_FILE_ROUTE_DISCOVERED result permits a separately frozen no-values layout intake. It does not authorize FRF scoring.
