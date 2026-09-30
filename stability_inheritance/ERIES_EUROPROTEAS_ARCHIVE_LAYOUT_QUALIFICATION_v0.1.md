# ERIES EuroProteas Archive Layout Qualification v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Status:** FROZEN BEFORE ARCHIVE MEMBER BODY OR NUMERIC RESPONSE ACCESS
**Parent source result:** ERIES_EUROPROTEAS_SOURCE_MATRIX_QUALIFIED
**Evidence class:** P0-Q archive/schema qualification

## Purpose

Determine whether the open RESPOND and POLIS archives expose enough outcome-blind file/directory structure to construct a legitimate matched hierarchy protocol without downloading experimental signal bodies.

## Allowed access

For Zenodo records 15518567 and 15575887 only:
- query official file metadata;
- issue byte-range requests restricted to ZIP end-of-central-directory, ZIP64 directory metadata when needed, and central-directory records;
- read member paths, member sizes, compression metadata, and directory structure.

Forbidden:
- local-file payloads;
- member body bytes;
- acceleration/displacement/force values;
- spectra, FRFs, fitted parameters, plots, numeric outcome summaries.

If the server does not honor range requests or the central directory cannot be isolated without full archive download, return a route-unavailable disposition. Do not fall back to downloading the archives.

## Layout questions

Outcome-blind path metadata should be tested for evidence of:
- foundation/pile/substructure-only measurements or test families in RESPOND;
- EuroProteas / structure-installed measurements in RESPOND;
- soil/foundation/roof or equivalent spatial hierarchy;
- forced-vibration families in both RESPOND and POLIS;
- free/pull-out vibration family in POLIS;
- instrumentation/layout or documentation files useful for channel mapping.

## Dispositions

**ERIES_ARCHIVE_LAYOUT_QUALIFIED**
- both open archives can be indexed by central-directory metadata;
- RESPOND contains distinguishable lower-level foundation/substructure and structure-installed/higher-level test organization;
- POLIS contains distinguishable structure response organization and at least one forced-vibration family;
- enough path-level hierarchy exists to justify a later channel/matched-test preflight.

**ERIES_ARCHIVE_LAYOUT_PARTIAL**
- both identities remain valid but only one archive or one required hierarchy can be indexed.

**ERIES_ARCHIVE_LAYOUT_INSUFFICIENT**
- archive indexes are readable but do not expose enough path-level organization to freeze a matched hierarchy without inspecting response values.

**ERIES_ARCHIVE_INDEX_ROUTE_UNAVAILABLE**
- official archive structure cannot be isolated by byte-range metadata access.

No scientific response disposition is authorized by this task.
