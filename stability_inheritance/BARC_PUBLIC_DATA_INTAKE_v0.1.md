# BARC Public Data Intake v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**System:** Box Assembly with Removable Component (BARC)
**Source authority:** Dynamic Substructuring Focus Group / Society for Experimental Mechanics wiki, with Sandia-origin challenge data mirrored through BYU Box
**Status:** FROZEN P0-Q SOURCE / METADATA INTAKE
**Numeric test-data scoring:** PROHIBITED
**P1 eligibility:** NO

## Scientific role

BARC was created to study how a removable component's dynamic response changes when its boundary condition changes between a next-level assembly and laboratory fixtures. This is directly relevant to the Stability Architecture question of whether realized behavior is conditioned by embedding/interface/boundary architecture.

The raw-data intake is separate from the literature evidence. Failure of the public-file route does not erase the published BARC evidence.

## Frozen public sources

Authoritative index:
https://wiki.sem.org/wiki/BARC

Public Box share links exposed by that index:

- Boundary Condition Challenge document:
  https://byu.box.com/s/w2aivpyq1r9gvvd916vkj80j7c4h5i42
- Random Vibration Data:
  https://byu.box.com/s/a16vknrscqt2ukp786a0j9yyqrhydsec
- Test Data:
  https://byu.box.com/s/gbu486g0chzvzkw64mf53kfjocdthaqn
- Hardware and Models:
  https://byu.box.com/s/zi6ntcjfdsi0uc1o2e8bf7g3iq82wrnv

## Allowed intake operations

For each public share URL:
- issue an HTTP GET only for the public share landing page;
- follow ordinary redirects;
- record HTTP status, final URL, content type, HTML byte count, title, and public page text snippets sufficient to identify whether the share is alive;
- do not click/download individual numeric test files;
- do not parse or score vibration data.

For the SEM wiki:
- record page identity and the four public share targets.

## Dispositions

- BARC_PUBLIC_INDEX_PASS if the SEM wiki and at least Test Data plus Hardware/Models Box shares are publicly reachable.
- BARC_PUBLIC_INDEX_PARTIAL if the wiki is reachable but one or more required Box shares are inaccessible.
- BARC_PUBLIC_INDEX_BLOCKED if the public index itself cannot be reached.
- BARC_SOURCE_IDENTITY_CHANGED if the share targets materially differ from the frozen index.

A PASS permits a later file-inventory preflight before any numeric data acquisition. It does not authorize test-data scoring.
