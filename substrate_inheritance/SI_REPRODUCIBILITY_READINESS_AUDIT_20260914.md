# Substrate Inheritance reproducibility readiness audit

**Date:** 14 September 2026  
**Branch:** `substrate-inheritance-next`  
**Scope:** already-produced SI P0-D/P0-Q evidence  
**New scientific computation performed by this audit:** no  
**Physical inheritance claim:** no

## Executive result

The SI repository has strong reproducibility structure for its existing synthetic/mathematical program: source code, tests, frozen plans for current Function/Limit maps, validation environment records, workflow provenance, summary documents, and fail-closed physical-ingestion schemas are all present. The principal remaining reproducibility debt is not missing computation. It is **reader-level unification**: connecting each manuscript-facing result to its exact plan, implementation, run/artifact, summary, interpretation ceiling, and regeneration path in one place.

The living manuscript evidence matrix now begins that consolidation.

## 1. Environment and validation controls

Present:

- `requirements-validation.txt`;
- `VALIDATION_ENVIRONMENT.md`;
- GitHub Actions workflow(s) for the SI validation suite;
- pinned/frozen historical reference run information in the README;
- test modules for ground truth, correspondence, embedding, robustness, non-normal cases, SI-next semantics, and Function/Limit modules.

Historical fixed reference for the frozen v0.2-era method suite remains recorded as:

- commit `9a1f357e73a27e532c755649568dde8af0b229cd`;
- Actions run `33292821080`, conclusion `success`;
- artifact `substrate-inheritance-synthetic-validation`;
- artifact ID `9726488007`;
- ZIP SHA-256 `332e5c463c597015a5cbe832b84ce8843be4eef688c8f62ca2e3ef4df18b7635`.

This is a fixed milestone, not a claim that the cited run is the latest CI execution.

## 2. Frozen physical route

Present and separated from candidate development:

- `CORRESPONDENCE_PROTOCOL_v0.2.json`;
- `REAL_SYSTEM_INPUT_SCHEMA_v0.2.json`;
- `real_system_adapter.py`;
- `PHYSICAL_INPUT_READINESS_v0.2.json`.

The adapter is fail-closed and does not assign a physical inheritance label or require chi/damping merely for ingestion. No admitted physical record currently exists, which is correctly represented as a readiness boundary rather than filled with development data.

## 3. SI-next candidate route

Present:

- `SI_NEXT_CANDIDATE_CONTRACT_v0.4.json`;
- `SI_NEXT_DIAGNOSTIC_INPUT_CONTRACT_v0.4.json`;
- candidate implementation modules;
- semantic/adversarial tests;
- explicit guard that candidate semantics cannot overwrite v0.2 physical science.

Current status remains `P0Q_CANDIDATE_ONLY`.

## 4. Function/Limit map reproducibility

### FM1 coupling response

Source-of-record set:

- plan: `SI_FM1_COUPLING_RESPONSE_PLAN_v0.1.json`;
- implementation: `coupling_response_landscape.py`;
- tests: `test_coupling_response_landscape.py`;
- summary: `SI_FM1_COUPLING_RESPONSE_SUMMARY_v0.1.md`;
- validation run: `34699663974`;
- then-current suite: `149 passed`;
- artifact ID: `10300106281`;
- artifact SHA-256: `f34d2dfa48a22d70b6b8cf14d63a13fc0f0321843bfb65fcdf0a257f738586db`.

Readiness: **GOOD**.

Remaining reader-level debt: add a compact regeneration command/index entry if not already explicit in the validation ledger.

### FM2 embedding depth

Source-of-record set:

- plan: `SI_FM2_EMBEDDING_DEPTH_PLAN_v0.1.json`;
- execution freeze: `SI_FM2_EXECUTION_FREEZE_v0.1.json`;
- implementation: `embedding_depth_landscape.py`;
- tests: `test_embedding_depth_landscape.py`;
- summary: `SI_FM2_EMBEDDING_DEPTH_SUMMARY_v0.1.md`;
- validation run: `34756837555`;
- dedicated tests: `5 passed`;
- artifact ID: `10317721694`;
- artifact SHA-256: `b897ddf7a70c21949bf93b689a59c20d62c2474c7d73bb6cc09cb7fb43a60d65`;
- generated result SHA-256: `4415074b6ce0007bfcb07daa96e2e94daa10c04618fe683e2fdc72123ea58847`.

Readiness: **GOOD**.

### FM3 lineage flow

Source-of-record set:

- plan: `SI_FM3_LINEAGE_FLOW_PLAN_v0.1.json`;
- implementation: `lineage_flow_landscape.py`;
- tests: `test_lineage_flow_landscape.py`;
- summary: `SI_FM3_LINEAGE_FLOW_SUMMARY_v0.1.md`;
- validation run: `34756644076`;
- dedicated tests: `6 passed`;
- artifact ID: `10317572637`;
- artifact SHA-256: `21e4c21b318cd86cc1ed83ecf05d242ebc26d705f7c1b270fec8ac2c5e320049`;
- generated result SHA-256: `e59179fc993a9354ca1531f0c8ac673c78df0c96dc193c4e2ce81505a912e9a5`.

Readiness: **GOOD**.

Important semantic validator: direct reconvergence and normalized-flow disagreement must remain separately represented. A reproduction that emits only the normalized-flow result is scientifically incomplete.

### FM4 hierarchical closure

Source-of-record set:

- plan: `SI_FM4_HIERARCHICAL_CLOSURE_PLAN_v0.1.json`;
- implementation: `hierarchical_closure_validation.py`;
- tests: `test_hierarchical_closure_validation.py`;
- summary: `SI_FM4_HIERARCHICAL_CLOSURE_SUMMARY_v0.1.md`;
- validation run: `34699314595`;
- then-current full suite: `137 passed`;
- synthetic-validation artifact ID: `10300145609`, SHA-256 `ff351bc208d13693ba10717eed11bec0db0100be1aacb11852d77b654d708358`;
- FM4 artifact ID: `10300070726`, SHA-256 `4b52b683e7f4635ea76ca4d1c05d8d2210589ddda8ac7dd418bad5201a33c181`.

Readiness: **GOOD**.

Important semantic validator: exact closure and approximate-method error surfaces must not be collapsed into one binary “closure works” statement.

## 5. Baseline synthetic/adversarial findings

Implemented and test-backed:

- ground-truth battery;
- same-spectrum modal discrimination;
- coupling-rewire specificity;
- intervention derivative cross-check;
- scalar nonidentifiability;
- coordinate invariance;
- near-degenerate subspace robustness;
- finite-depth/semi-infinite embedding validation;
- non-normal/biorthogonal handling;
- fail-closed real-system adapter.

Readiness: **GOOD FOR P0-Q CLAIMS**, subject to keeping each result attached to its synthetic generator and refusing physical promotion.

## 6. Literature and attribution reproducibility

Present:

- pre-search experimental record: `SI_EXPERIMENTAL_OPPORTUNITY_v0.1.md`;
- first collision: `SI_LITERATURE_COLLISION_v0.1.md`;
- deeper collision: `SI_LITERATURE_COLLISION_v0.2.md`;
- attribution ledgers through v0.3.

Sequence integrity is preserved: experimental ideation preceded the targeted prior-experiment collision.

Readiness: **GOOD FOR CURRENT ATTRIBUTION CEILING**.

Remaining requirement before manuscript freeze: bibliographic line-by-line verification and, for any novelty-bearing sentence, a claim-specific nearest-prior-art search rather than reliance on generic keyword coverage.

## 7. Manuscript traceability

New canonical working sources:

- `manuscript/SI_MANUSCRIPT_WORKING.md`;
- `manuscript/SI_MANUSCRIPT_EVIDENCE_MATRIX_v0.1.md`;
- `manuscript/README.md`.

The manuscript is explicitly non-final and P0-D/P0-Q only.

Readiness: **ACTIVE WORKING STATE**.

## 8. Missing or incomplete reproducibility elements

### R1. Single regeneration index

There is no single compact file yet listing the exact local commands/workflows required to regenerate each FM output from a clean environment. The constituent information exists, but a release-quality reproduction guide should consolidate it.

Disposition: `DOCUMENTATION_DEBT; NOT_A_SCIENTIFIC_BLOCKER`.

### R2. FM5

FM5 does not yet have a completed source-of-record result. It must not be represented as reproducible evidence until a prospective plan/freeze, implementation, known-truth tests, run/artifact, and summary exist.

Disposition: `NOT_YET_EXECUTED`.

### R3. Physical SI

No real-system result exists, so no physical reproduction package can yet exist.

Disposition: `NOT_APPLICABLE_YET`, not missing-data failure.

### R4. Final manuscript figures

No manuscript figure freeze exists. Figure specifications should derive from source-of-record data, and generated figure artifacts should be hashed once the manuscript enters evidence-complete internal draft status.

Disposition: `PENDING_MANUSCRIPT_DEVELOPMENT`.

## 9. Release-quality checklist for existing P0-D/P0-Q evidence

Before an SI methods/architecture release:

- [ ] all environment/dependency versions verified;
- [ ] clean-room regeneration commands consolidated;
- [ ] plans/freeze files linked from each generated result;
- [ ] output hashes recorded for every manuscript-used generated file;
- [ ] semantic validators confirm the quantity described in prose is the quantity computed;
- [ ] mutation/known-bad tests preserved for fail-closed gates;
- [ ] every negative result remains reproducible rather than only narrated;
- [ ] no synthetic threshold is relabeled physical;
- [ ] literature references verified against primary bibliographic sources;
- [ ] living manuscript evidence matrix complete at sentence/claim level for quantitative results;
- [ ] manuscript figures generated from current source-of-record outputs;
- [ ] no stale GP authority reference presented as current GOM authority.

## 10. Verdict

`CURRENT_P0D_P0Q_REPRODUCIBILITY = STRONG_BUT_NOT_RELEASE_FROZEN`

`MAJOR_MISSING_SCIENTIFIC_ARTIFACT = NONE_FOR_FM1_FM4`

`MAJOR_DOCUMENTATION_DEBT = CONSOLIDATED_REGENERATION_INDEX_AND_FINAL_MANUSCRIPT_FIGURE_PROVENANCE`

`PHYSICAL_REPRODUCIBILITY = NOT_APPLICABLE_NO_REAL_SYSTEM_RESULT`

`FM5_REPRODUCIBILITY = NOT_APPLICABLE_NOT_YET_EXECUTED`

The next reproducibility work can proceed without a new scientific computation by consolidating the clean-room regeneration index and finalizing manuscript claim/figure provenance.