# BRB Long-Term OSF Fast Identity Preflight v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Status:** FROZEN METADATA-ONLY IDENTITY PREFLIGHT
**Parent intake:** BRB_LONGTERM_OSF_IDENTITY_INTAKE_v0.1.md
**Purpose:** Resolve GHKJ7 versus FBWHZ without recursively crawling the full public file tree.
**Numeric experimental data:** PROHIBITED

Allowed:
- public OSF node metadata for ghkj7 and fbwhz;
- public storage-provider metadata;
- first page of root file/folder names only.

Prohibited:
- file-body download;
- recursive file-tree traversal;
- signal values;
- scientific scoring.

Disposition:
- CANONICAL_OSF_IDENTITY_RESOLVED if exactly one node title/description clearly matches BRB_LTERM_MULTISCALE21;
- OSF_IDS_LINKED_OR_DUPLICATE if both resolve to matching BRB long-term objects and metadata indicate a relation;
- OSF_IDENTITY_AMBIGUOUS otherwise.
