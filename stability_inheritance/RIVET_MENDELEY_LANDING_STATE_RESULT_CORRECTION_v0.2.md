# Riveted-Joint Mendeley Landing-State Result Correction v0.2

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Affected workflow run:** 36568654976
**Affected artifact:** rivet_mendeley_landing_state/result.json
**Correction class:** RESULT-CLASSIFICATION LOGIC ERROR / NO FILE BODY ACCESSED
**Corrected disposition:** FILE_DESCRIPTOR_WITHOUT_ROUTE / SOURCE_ACCESS_HOLD

## What happened

The repaired landing-state audit correctly parsed the public Mendeley landing-page HTML and embedded script state, but its final classification rule was too permissive.

It labeled the result OFFICIAL_FILE_ROUTE_DISCOVERED when a fragment containing the published filename data.h5 also contained:
- generic HTTP strings such as schema.org or the dataset landing URL; and
- unrelated UUIDs such as customer/owner/profile identifiers.

Manual audit of the stored result artifact shows:

- data.h5 appears only in the public dataset description;
- no candidate URL contains data.h5;
- no public-files URL was recovered;
- no file_download URL was recovered;
- no file-specific UUID or stable file identifier was recovered;
- the candidate URLs are generic site/schema/licence/dataset-page resources.

Therefore the prior automatic disposition was false-positive.

## Corrected interpretation

The public dataset identity and published HDF5 layout are well supported, but a provenance-clean direct file route is not operationally available from the current runtime discovery path.

Correct disposition:

**FILE_DESCRIPTOR_WITHOUT_ROUTE**

Operational status:

**SOURCE_ACCESS_HOLD**

## Scientific consequence

No FRF body was opened and no target outcome was exposed.

The published native evidence remains valid:
- two host assemblies ARB and A'RB';
- joint dynamics depend on rivet-squeezing force;
- host-reduced joint impedance can be compared/transferred when local material/geometry equivalence conditions are satisfied.

The raw-data cross-host boundary test is deferred until an official file route is independently available.

No unofficial mirror or further endpoint guessing is authorized under this intake lineage.
