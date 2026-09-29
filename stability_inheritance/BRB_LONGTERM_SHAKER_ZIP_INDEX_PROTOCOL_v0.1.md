# Brake-Reuss Beam Long-Term Shaker ZIP Index Preflight v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Status:** P0-Q METADATA-ONLY PREFLIGHT / NO SIGNAL BODY ACCESS
**Parent intake:** BRB_LONGTERM_OSF_IDENTITY_V01 -> LONG_TERM_LAYOUT_QUALIFIED
**Canonical OSF project:** fbwhz
**Scientific score:** PROHIBITED

## Purpose

Recover the exact file-name layout of the three BRB long-term shaker archives before any signal values are opened. The only permitted bytes are ZIP end-of-central-directory records and central-directory metadata obtained by HTTP Range requests.

This preflight exists so the later history protocol can freeze:
- temporal state identity;
- excitation-level identity from filenames;
- repeat/realization counts;
- which measurements are present before/after each 4-hour excitation block and reassembly.

## Frozen archives

- FirstRound_16Dec2020.zip, OSF download p5trv, indexed size 4,620,032,365 bytes
- SecondRound_17Dec2020.zip, OSF download rkg4b, indexed size 1,228,105,544 bytes
- ThirdRound_18Dec2020.zip, OSF download 4r8ku, indexed size 2,703,467,720 bytes

## Allowed operations

For each archive:
1. issue a one-byte Range request to verify byte-range support and total size;
2. fetch only the ZIP tail needed to locate EOCD/ZIP64 metadata;
3. fetch only the exact central-directory byte range;
4. parse file names and archive metadata;
5. group names into RandFRF_Before, RandFRF_After, StepSine_Before, StepSine_After, and SingFreqTest;
6. parse voltage/repeat/frequency indices from filenames where encoded.

No local file entry body may be requested.

## Abort rule

If the server ignores Range and returns HTTP 200 for a range request, close the response without reading the body and return RANGE_ACCESS_NOT_AVAILABLE.

## Dispositions

- SHAKER_ZIP_INDEX_QUALIFIED if all three indexed archive sizes match the frozen OSF metadata and central directories are parsed without entry-body access.
- SHAKER_ZIP_INDEX_PARTIAL if at least one but not all archives can be indexed.
- RANGE_ACCESS_NOT_AVAILABLE if byte-range access cannot be established.
- SHAKER_ZIP_IDENTITY_CHANGED if the total byte size differs from the frozen OSF metadata.

No disposition licenses signal scoring. A qualified index permits construction of the history-response protocol.
