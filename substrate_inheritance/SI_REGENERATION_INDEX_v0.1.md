# Substrate Inheritance clean-room regeneration index v0.1

**Date:** 14 September 2026  
**Scope:** currently completed synthetic/mathematical SI evidence  
**Physical result:** none  
**Purpose:** close the reader-level reproducibility gap identified in `SI_REPRODUCIBILITY_READINESS_AUDIT_20260914.md` by consolidating the commands and source files needed to regenerate current P0-D/P0-Q outputs.

## 1. Environment

From repository root, use the pinned validation requirements:

```bash
python -m pip install --disable-pip-version-check -r substrate_inheritance/requirements-validation.txt
python -m pip check
```

The qualified CI line uses CPython 3.12.14 on Ubuntu 24.04. For a release-quality reproduction, record:

```bash
python --version
python -m pip --version
python -m pip freeze --all | sort
```

A local reproduction using a different platform/version is useful as a cross-check but should not silently replace the qualified reference environment.

## 2. Full current synthetic validation battery

Run the complete adversarial test suite:

```bash
python -m pytest -q substrate_inheritance/test_*.py
```

Then regenerate the core result records:

```bash
python substrate_inheritance/inheritance_engine.py
python -m substrate_inheritance.ground_truth_benchmarks
python -m substrate_inheritance.ensemble_validation
python -m substrate_inheritance.identifiability_validation
python -m substrate_inheritance.robustness_validation
python -m substrate_inheritance.depth_validation
python -m substrate_inheritance.discriminability_validation
python -m substrate_inheritance.nonnormal_validation
python -m substrate_inheritance.electronic_validation
python -m substrate_inheritance.adapter_validation
python -m substrate_inheritance.si_next_validation
python -m substrate_inheritance.si_next_contract_validation
python -m substrate_inheritance.si_v04_validation
python -m substrate_inheritance.hierarchical_closure_validation
python -m substrate_inheritance.coupling_response_landscape
```

The resulting JSON objects under `substrate_inheritance/results/` remain synthetic/method evidence. The generator command does not promote their epistemic status.

## 3. FM1 coupling-response landscape

Required source files:

- `SI_FM1_COUPLING_RESPONSE_PLAN_v0.1.json`;
- `coupling_response_landscape.py`;
- relevant tests in the general SI suite;
- `requirements-validation.txt`.

Regenerate:

```bash
python -m substrate_inheritance.coupling_response_landscape
```

Expected output:

```text
substrate_inheritance/results/SI_FM1_COUPLING_RESPONSE_RESULTS_v0.1.json
```

Semantic checks required before using the result:

- scope is synthetic P0-D Function/Limit mapping;
- 36 cases retained;
- zero-coupling response/rewire/intervention controls remain numerical zero within declared software precision;
- clean parent spectrum remains fixed under the same-spectrum control;
- no master relationship score;
- no system scalar chi;
- no Atlas parameter selection;
- no binary physical threshold;
- no physical inheritance claim.

Source summary: `SI_FM1_COUPLING_RESPONSE_SUMMARY_v0.1.md`.

## 4. FM2 embedding-depth landscape

Required source/freeze files:

- `SI_FM2_EMBEDDING_DEPTH_PLAN_v0.1.json`;
- `SI_FM2_EXECUTION_FREEZE_v0.1.json`;
- `embedding_depth_landscape.py`;
- `test_embedding_depth_landscape.py`;
- `depth_validation.py`.

Run dedicated tests:

```bash
python -m pytest -q substrate_inheritance/test_embedding_depth_landscape.py
```

Regenerate:

```bash
python -m substrate_inheritance.embedding_depth_landscape
```

Expected output:

```text
substrate_inheritance/results/fm2_embedding_depth_landscape.json
```

Required semantic checks:

- 48 parameter cases and 384 depth records;
- all eight frozen depths retained in each case;
- direct-matrix and recursive surface-Green-function implementations agree within frozen absolute tolerance `1e-9`;
- effective depth uses the sustained-depth rule;
- no chi used;
- imaginary probe component is not relabeled mechanical damping;
- numerical depth is not relabeled a physical inheritance length;
- no physical threshold or inheritance claim.

Source summary: `SI_FM2_EMBEDDING_DEPTH_SUMMARY_v0.1.md`.

## 5. FM3 lineage-flow landscape

Required files:

- `SI_FM3_LINEAGE_FLOW_PLAN_v0.1.json`;
- `lineage_flow_landscape.py`;
- `test_lineage_flow_landscape.py`;
- `si_next_architecture.py`;
- `si_next_higher_order.py`.

Run dedicated tests:

```bash
python -m pytest -q substrate_inheritance/test_lineage_flow_landscape.py
```

Regenerate:

```bash
python -m substrate_inheritance.lineage_flow_landscape
```

Expected output:

```text
substrate_inheritance/results/fm3_lineage_flow_landscape.json
```

Required semantic checks:

- 125 parameter cases;
- 32 frozen seeds per case;
- 4,000 seed-expanded evaluations;
- direct exact reconvergence error remains below numerical precision expectation;
- all frozen cases/seeds retained;
- normalized relative flow is not a probability, causal fraction, inheritance percentage, or promotion score;
- no extinction is manufactured in the full-rank same-spectrum construction;
- no master score, physical threshold, Atlas target, or physical inheritance claim.

Source summary: `SI_FM3_LINEAGE_FLOW_SUMMARY_v0.1.md`.

## 6. FM4 hierarchical-closure landscape

Required files:

- `SI_FM4_HIERARCHICAL_CLOSURE_PLAN_v0.1.json`;
- `hierarchical_closure_validation.py`;
- `test_hierarchical_closure_validation.py`.

Regenerate:

```bash
python -m substrate_inheritance.hierarchical_closure_validation
```

Expected output:

```text
substrate_inheritance/results/SI_FM4_HIERARCHICAL_CLOSURE_RESULTS_v0.1.json
```

Required semantic checks:

- 16 parameter cases × 121 frequencies = 1,936 records;
- exact full/direct/nested reduction identity stays inside frozen `5e-11` numerical tolerance;
- zero outer-coupling group return remains numerical zero;
- approximate surfaces retain all cases;
- no binary physical pass threshold;
- no post-result approximation ordering;
- no system scalar chi;
- no Atlas selection;
- no physical inheritance claim.

Source summary: `SI_FM4_HIERARCHICAL_CLOSURE_SUMMARY_v0.1.md`.

## 7. Fail-closed real-system adapter validation

The adapter path can be regenerated without a physical target:

```bash
python -m substrate_inheritance.adapter_validation
```

Expected synthetic validation output:

```text
substrate_inheritance/results/adapter_validation.json
```

The output must continue to state:

- physical inheritance threshold applied: false;
- inheritance promotion label assigned: false;
- chi computed: false;
- damping computed: false.

The existence of this output means the ingestion path works on synthetic known-truth input. It is not a physical result.

## 8. Manifests for release-grade reruns

For a release-grade rerun, hash at minimum:

- the plan/freeze record;
- implementation module;
- dedicated test module;
- generated result JSON;
- realized environment record.

FM2 and FM3 workflows already generate dedicated SHA-256 manifests. FM1/FM4 should receive equivalent explicit manifests at the next release-hardening pass if the existing artifact package does not already contain a complete source/result hash list.

## 9. Interpretation cross-check after regeneration

A byte-different result does not automatically mean a scientific difference. A byte-identical result does not automatically establish semantic validity. After regeneration, independently verify:

1. record counts and frozen grid identity;
2. expected known-truth controls;
3. negative-result semantics;
4. evidence-class fields;
5. no post-result threshold/selection drift;
6. source summaries still describe the computed object correctly.

## 10. Current regeneration disposition

`CORE_SYNTHETIC_SUITE = REGENERATABLE_FROM_REPOSITORY`

`FM1 = REGENERATION_PATH_DOCUMENTED`

`FM2 = REGENERATION_PATH_AND_MANIFEST_LOGIC_DOCUMENTED`

`FM3 = REGENERATION_PATH_AND_MANIFEST_LOGIC_DOCUMENTED`

`FM4 = REGENERATION_PATH_DOCUMENTED`

`PHYSICAL_SI = NOT_APPLICABLE_NO_ADMITTED_RESULT`

`FM5 = NOT_APPLICABLE_NOT_YET_EXECUTED`

This index is the current clean-room starting point for existing SI evidence and should be updated only when the source-of-record execution path changes.