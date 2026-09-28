# Stability Inheritance Physical Benchmark Candidate Audit

**Date:** 2026-09-28  
**Governance:** SymC GOM v1.0  
**Active branch:** stability-inheritance  
**Status:** P0-D / P0-Q benchmark-screen provenance  
**Notation:** χ = licensed scalar coordinate; Χ = base modal/vector representation; Χ_arc = architecture-level/conglomerate representation reconstructed through Stability Arc machinery where licensed.

## ERIES-RESPOND

ERIES-RESPOND is retained as a useful hierarchical-embedding development benchmark. Public literature describes forced-vibration testing of a 2x2 pile-group foundation and the EuroProteas structure resting on that foundation, with instrumentation across soil, piles, foundation, and roof over approximately the 1–10 Hz range. A 2025 open-access conference paper by Di Laora et al. describes the campaign in multiple stages, including foundation-only and structure-installed excitation, and reports selected preliminary results.

**Disposition**
- P0-D / P0-Q development and native-comparator qualification: ACCEPT.
- Globally untouched P1 assumption: REFUSE.
- Endpoint-specific untouched P1 eligibility: NEED_MORE_INFO and requires proof that the decisive endpoint was not published, plotted, summarized, or used in tuning before target values are opened.

**Permitted SI use**
- Function/Limit mapping;
- soil-structure/substructure native-comparator qualification;
- amplitude dependence;
- hierarchical closure and Χ→Χ_arc reconstruction tests;
- uncertainty and refusal behavior.

Do not open decisive embedded-system values merely to determine eligibility.

## Korbar A/B/AJB benchmark

The Korbar experimental substructuring benchmark remains scientifically valuable but is not independent untouched P1 evidence for the A/B→AJB assembly-response pathway. Korbar et al. (2025), *Towards an improved experimental joint identification in frequency-based substructuring*, explicitly uses the AJB assembly formed from substructures A and B connected by a joint and performs experimental cross-validation against that assembly.

The raw AJB experimental values remain unopened by the current SI investigation, but the pathway itself is literature-exposed.

**Disposition**
- KORBAR_A_B_AJB_P1_STATUS = REFUSED_FOR_UNTOUCHED_CONFIRMATION.
- RAW_EXPERIMENTAL_AJB_OPENED_BY_CURRENT_SI = NO.
- P0-D / P0-Q development use: ALLOWED.
- native comparator qualification: ALLOWED.
- Function/Limit mapping: ALLOWED.

**Permitted SI use**
- response-channel method qualification;
- virtual-point / dynamic-substructuring comparator validation;
- modal/subspace carrier-lineage stress testing;
- split/merge/weak-participation/nonidentifiability handling;
- Χ→Χ_arc reconstruction and refusal behavior.

## Consequence for current APQ

Neither benchmark is promoted to untouched P1. Both strengthen the current plan because they provide real experimental known-truth systems for testing whether the χ / Χ / Χ_arc representation and refusal machinery behave correctly against established native substructuring physics.

The current controlled physical hierarchy remains P0-Q known-truth qualification only. A later novel empirical SI test still requires a decisive parent-to-descendant or lower-to-higher outcome pathway that is frozen before exposure and not already published or used in model tuning.
