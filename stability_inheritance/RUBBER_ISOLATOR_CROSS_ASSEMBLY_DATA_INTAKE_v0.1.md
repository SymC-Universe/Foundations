# Rubber-Isolator Cross-Assembly Benchmark Intake v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Dataset:** Identification of rubber isolator dynamics: substructure frequency response functions for identification and cross validation
**Public identifier:** 38cp7wdjz7
**DOI:** 10.17632/38cp7wdjz7.1
**Contributor:** Jure Korbar
**License:** CC BY 4.0
**Evidence class:** PUBLIC EXTERNAL MEASURED / P0-Q ONLY
**P1 eligibility:** NO
**Status:** METADATA / STRUCTURE INTAKE ONLY

## Scientific role

The public dataset is designed around two different host assemblies:

1. C1 - J - C2, where a rubber-isolator joint model can be identified using measurements in all directions and a virtual-point transformation;
2. A - J - B, where two identical rubber isolators connect different host structures and the identified joint model can be cross-validated.

This is valuable to Stability Architecture because it separates:
- an independently characterized transferable joint/interface object;
- one identification host system;
- a different validation host system;
- an independently measured target assembly.

The native dynamic-substructuring/joint-identification framework owns the mechanism. Any successful result is architecture-supporting native evidence, not SI novelty.

## Intake firewall

Before a cross-assembly protocol is frozen, this intake may inspect only:

- public dataset metadata;
- version and DOI;
- license;
- file names, IDs, sizes, media types, and published SHA-256 hashes where supplied;
- README.md contents describing HDF5 organization;
- HDF5 group names only if the official API requires downloading a small metadata object later.

This intake must not:
- download or parse experimental.h5 FRF arrays;
- download or parse numerical.h5 FRF arrays;
- inspect A_J_B response values;
- inspect C1_J_C2 response values;
- choose frequencies, channels, VPT definitions, or error metrics from numeric outcomes.

## Expected public files

At minimum:
- experimental.h5
- numerical.h5
- README.md
- STL geometry files for C1, C2, C1_J_C2, A, B, and A_J_B.

Published sizes are approximately:
- experimental.h5: 428 MB
- numerical.h5: 288 MB
- README.md: 3.55 KB.

## Frozen intake route

Use the official Digital Commons / Mendeley Data API at api.data.mendeley.com for dataset version 1.

Attempt:
- public dataset metadata;
- public file listing.

If the API exposes a direct download URL for README.md, download README only and record its SHA-256 and text.

Do not download experimental.h5 or numerical.h5 in this intake.

## Intake dispositions

### INTAKE_METADATA_PASS

Assign if:
- official public dataset/version is identifiable;
- CC BY 4.0 is confirmed;
- experimental.h5, numerical.h5, and README.md are present;
- file identities/sizes are recorded;
- README is available or the file listing itself supplies enough structure for a subsequent non-value HDF5-layout preflight.

### INTAKE_API_BLOCKED

Assign if the official public metadata/files cannot be retrieved programmatically from the declared API route.

This is a transport/access limitation only.

### INTAKE_IDENTITY_MISMATCH

Assign if DOI/version/file set materially differs from the frozen public description.

## Consequence

INTAKE_METADATA_PASS permits a separate non-value HDF5 layout preflight.

Only after layout qualification may a cross-assembly identification/transfer protocol be frozen before any A_J_B target FRF scoring.
