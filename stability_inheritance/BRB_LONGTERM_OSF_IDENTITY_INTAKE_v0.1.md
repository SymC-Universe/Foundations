# BRB Long-Term Multiscale OSF Identity and Layout Intake v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Status:** FROZEN METADATA-ONLY INTAKE
**Evidence class:** PUBLIC EXTERNAL DATASET / NO NUMERIC RESPONSE ACCESS
**P1 eligibility:** NO

## Trigger

The Joints Committee long-term BRB page identifies the dataset as BRB_LTERM_MULTISCALE21 and describes a 12-hour campaign with random FRF, step-sine, monotone 172 Hz, impact, disassembly/reassembly, and interface-scan stages.

The same official page contains two OSF identifiers in different citation locations:
- GHKJ7
- FBWHZ

This intake resolves the canonical public OSF project identity from OSF metadata rather than choosing one manually.

## Scientific role

This dataset can address a nonredundant architecture relation already supported qualitatively by published wear work:

past loading -> evolved physical interface state -> later realized dynamic response.

The first intake must remain outcome-blind. It is only allowed to identify the official project and discover whether the public file tree supports a clean temporal/state split:
- initial / before;
- after 4 hours;
- after 8 hours;
- after disassembly/reassembly;
- final after the last 4 hours;
- initial/final hammer;
- before/after interface scans.

## Candidate OSF GUIDs

Test exactly:
- ghkj7
- fbwhz

Use public OSF API metadata and file-tree endpoints only.

## Allowed operations

For each GUID:
1. request public node metadata;
2. record node title, description length, public status, dates, contributors count, registration/category metadata if exposed;
3. enumerate storage providers and recursively list file/folder metadata;
4. record file/folder names, paths, sizes, IDs, hashes/checksums, and download links as metadata only;
5. classify names into the published experimental stages using filename/path text only;
6. do not download file bodies.

## Prohibited operations

- no CSV/MAT/ZIP data-body download;
- no response-value inspection;
- no FRF or spectral calculation;
- no selection of excitation amplitudes based on outcomes;
- no model fitting;
- no use of a file body to decide project identity.

## Canonical identity rule

Assign CANONICAL_OSF_IDENTITY_RESOLVED only if one GUID clearly matches BRB_LTERM_MULTISCALE21 by node title/description/file-tree semantics.

If both GUIDs resolve to the same project/linked object, record the relationship explicitly.

If neither can be uniquely adjudicated, assign OSF_IDENTITY_AMBIGUOUS.

## Layout dispositions

For the canonical node:
- LONG_TERM_LAYOUT_QUALIFIED if metadata alone identifies the five random-FRF/step-sine state blocks described by the official campaign plus the initial/final or interface-scan branches needed for history mapping.
- LONG_TERM_LAYOUT_PARTIAL if the project is correct but file-tree metadata are insufficient for the full state sequence.
- OSF_SOURCE_BLOCKED if public node/file metadata cannot be retrieved.

No scoring protocol is authorized by this intake alone.
