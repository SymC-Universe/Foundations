# ERIES EuroProteas Archive Layout Transport Repair v0.1a

**Date:** 2026-09-29  
**Governance:** SymC GOM v1.0 + mandatory Continuity Hardening Addendum  
**Parent protocol:** `ERIES_EUROPROTEAS_ARCHIVE_LAYOUT_QUALIFICATION_v0.1.md`  
**Repair class:** MECHANICAL_TRANSPORT_ONLY  
**Scientific design change:** NONE  
**Response/member-body exposure:** PROHIBITED

## Preserved failure

Workflow run `36651136544` executed the frozen archive-layout task and received HTTP 406 for both RESPOND and POLIS during the first ZIP tail range request. No central directory was parsed, no member body was opened, and no numeric response was accessed.

The raw task disposition `ERIES_ARCHIVE_LAYOUT_INSUFFICIENT` is therefore not accepted as a scientific/layout insufficiency finding. The underlying evidence is a transport failure before layout observation.

Corrected execution classification:

`MECHANICAL_RANGE_TRANSPORT_FAILURE_PRE_LAYOUT`

## Repair

The parent implementation used the file URL supplied by the Zenodo API together with an `Accept: application/octet-stream` header.

v0.1a changes only transport:
- construct the official public download route `https://zenodo.org/records/<record>/files/<filename>?download=1`;
- use `Accept: */*`;
- retain `Accept-Encoding: identity`;
- issue the same ZIP tail / ZIP64 / central-directory byte-range requests;
- retain the same maximum central-directory size;
- retain the same path-only classification and dispositions;
- do not download a full archive if range requests are not honored.

No scientific threshold, dataset identity, file checksum, hierarchy criterion, path classifier, or interpretation rule changes.

## Duplicate-race note

A conveyor-code hardening commit can trigger the watched workflow while a stale queue entry remains `READY`. Any such rerun of v0.1 is duplicate mechanical work and may not replace the authoritative v0.1 failure or count as new scientific advancement. v0.1a is the only licensed recovery task.
