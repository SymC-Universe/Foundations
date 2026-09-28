# SI Korbar Independence Correction

**Date:** 2026-09-28  
**Status:** P0-D / P0-Q provenance correction  
**Active GOM:** v0.8.8  
**Applies to:** `SI_PHYSICAL_BENCHMARK_KORBAR_2026_PREFLIGHT.md`

## Trigger

The Korbar A/B/AJB benchmark was initially opened as a candidate physical route because the raw experimental assembly values had not been inspected by SI.

A prior-art check now establishes a separate independence problem. Korbar et al. (2025), *Towards an improved experimental joint identification in frequency-based substructuring* (Mechanical Systems and Signal Processing, DOI 10.1016/j.ymssp.2025.113115), explicitly uses an alternative assembly denoted AJB consisting of substructures A and B connected by a single joint and performs experimental cross-validation using that assembly.

## Consequence

The raw `experimental.h5` AJB values remain unopened by SI. However, the A/B -> AJB assembly-response pathway is already literature-exposed.

Therefore:

- `KORBAR_A_B_AJB_P1_STATUS = REFUSED_FOR_UNTOUCHED_CONFIRMATION`
- `RAW_EXPERIMENTAL_AJB_OPENED_BY_SI = NO`
- `DEVELOPMENT_USE = ALLOWED`
- `NATIVE_COMPARATOR_QUALIFICATION_USE = ALLOWED`
- `FUNCTION_LIMIT_MAPPING_USE = ALLOWED`
- `RESPONSE_CHANNEL_INGESTION_DEVELOPMENT_USE = ALLOWED`

The benchmark remains valuable for:
- response-channel SI method qualification;
- Virtual Point Transformation / dynamic-substructuring comparator validation;
- carrier/subspace lineage stress tests;
- split, merge, weak-participation, and nonidentifiability handling;
- Function/Limit mapping using the numerical joint variants.

It must not be represented as independent untouched P1 evidence for the already published A/B -> AJB assembly-response pathway.

## Next safe action

Use Korbar only as a development/native-comparator benchmark and continue the search for a distinct real physical system or intervention whose decisive parent-to-child outcome pathway is unexposed at freeze.

No frozen v0.2 correspondence contract, physical threshold, or existing SI result is changed by this correction.
