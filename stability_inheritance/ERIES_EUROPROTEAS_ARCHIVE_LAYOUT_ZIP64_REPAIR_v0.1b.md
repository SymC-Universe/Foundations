# ERIES EuroProteas Archive Layout ZIP64 Parser Repair v0.1b

**Date:** 2026-09-29  
**Governance:** SymC GOM v1.0 + mandatory Continuity Hardening Addendum  
**Parent protocol:** `ERIES_EUROPROTEAS_ARCHIVE_LAYOUT_QUALIFICATION_v0.1.md`  
**Parent repair:** `ERIES_EUROPROTEAS_ARCHIVE_LAYOUT_TRANSPORT_REPAIR_v0.1a.md`  
**Repair class:** MECHANICAL_PARSER_ONLY  
**Scientific design change:** NONE  
**Response/member-body exposure:** PROHIBITED

## Preserved v0.1a result

Workflow run `36653158566` proved the official `?download=1` byte-range route is operational. POLIS returned HTTP 206, its central directory parsed successfully, and 447 member paths were indexed without opening any member body.

RESPOND also returned HTTP 206 for the ZIP tail but then failed in the local ZIP64 EOCD parser with `IndexError: tuple index out of range`.

The defect is deterministic implementation arithmetic: the unpack format `<4sQ2H2I4Q` returns indices 0..9, while v0.1a attempted to read index 10. Correct ZIP64 fields are:
- total entries = tuple index 7;
- central-directory size = tuple index 8;
- central-directory offset = tuple index 9.

## Repair

v0.1b changes only those three tuple indices.

Everything else remains frozen:
- Zenodo record IDs and ZIP checksums;
- official download route;
- byte-range-only access;
- no full archive fallback;
- no member-body access;
- central-directory size ceiling;
- path-only classifier;
- layout questions;
- disposition rules;
- interpretation ceiling.

The POLIS result from v0.1a is preserved as valid checkpoint evidence. v0.1b may re-read its central-directory metadata only because the combined frozen disposition requires both archives and the exact source/config identity is unchanged; no member body may be read.
