# Substrate Inheritance release-manifest hardening v0.1

**Date:** 14 September 2026  
**Scope:** existing FM1-FM4 P0-D evidence  
**New scientific computation:** none  
**Purpose:** close the remaining compact-manifest asymmetry identified by the reproducibility audit without rerunning or changing the science.

## 1. Principle

The dedicated FM2 and FM3 workflows already create explicit SHA-256 manifests around their frozen plan/source/output execution. FM1 and FM4 have equivalent scientific provenance in Git commits plus immutable-at-run artifact digests, but that provenance was distributed across Actions metadata and source history rather than collected into one compact record.

This file consolidates the retained FM1/FM4 execution identities. It does not claim byte identity between a historical CI artifact and any later regenerated output unless that identity is independently checked.

## 2. FM1 coupling-response retained execution

**Scientific scope:** synthetic P0-D Function/Limit map only.

**Execution commit:** `8a8d46fc148345abe77a9c139d55dc2ef7d90164`  
**Commit message:** `Run SI FM1 coupling response landscape in CI`  
**Commit tree:** `6f1d00798e3403943d6f2bca666d91d0de186060`  
**Workflow run:** `34699663974`  
**Head branch:** `substrate-inheritance-next`

Frozen source identities at the execution commit:

| Object | Git blob SHA |
| --- | --- |
| `.github/workflows/substrate-inheritance.yml` | `02928ec2b5821de5a2d7f025e184fcb0101aa07c` |
| `substrate_inheritance/SI_FM1_COUPLING_RESPONSE_PLAN_v0.1.json` | `24eedf60d5d11a4e1f0bb8ef84ecb597c5e6d255` |
| `substrate_inheritance/coupling_response_landscape.py` | `621e631e456f43a157afdf596ac986d9977b08b4` |
| `substrate_inheritance/test_coupling_response_landscape.py` | `fdaa01ed1777aace0b0c783da7b13dee22e53287` |
| `substrate_inheritance/requirements-validation.txt` | `4d5d71f764bcc86efe05af4051c983cd9579efda` |

Retained Actions artifact:

- artifact ID: `10300106281`
- name: `substrate-inheritance-fm1-coupling-response-v01`
- archive digest: `sha256:f34d2dfa48a22d70b6b8cf14d63a13fc0f0321843bfb65fcdf0a257f738586db`
- artifact contents declared by workflow:
  - `SI_FM1_COUPLING_RESPONSE_PLAN_v0.1.json`
  - generated `results/SI_FM1_COUPLING_RESPONSE_RESULTS_v0.1.json`
  - generated `results/validation_environment.txt`

The same run also retained a synthetic-validation artifact and an FM4 artifact because the main workflow regenerates the qualified suite. Those secondary artifacts are not substituted for the primary FM1 artifact identity above.

### FM1 release rule

A future manuscript/release package that uses FM1 numerics must either:

1. preserve/download the retained artifact and verify the archive digest above; or
2. clean-room regenerate FM1 from the execution source identities and record a new result SHA-256 plus environment manifest.

A regenerated output receives a new manifest identity even if its scientific values agree.

## 3. FM4 hierarchical-closure retained execution

**Scientific scope:** synthetic P0-D Function/Limit map only.

**Execution commit:** `0603ff5ef3b449a97f08cf32b78eb01fc691f89d`  
**Commit message:** `Run SI FM4 hierarchical closure landscape in CI`  
**Commit tree:** `2bffc19e508b0df68d9be88b9204ca357b0d9484`  
**Workflow run:** `34699314595`  
**Head branch:** `substrate-inheritance-next`

The retained execution uses the frozen FM4 plan and implementation lineage later preserved unchanged through the FM1 execution tree. The canonical source objects are:

| Object | Git blob SHA in retained lineage |
| --- | --- |
| `substrate_inheritance/SI_FM4_HIERARCHICAL_CLOSURE_PLAN_v0.1.json` | `7df178989fdb432080121dd3ebbfd1dd38cc0247` |
| `substrate_inheritance/hierarchical_closure_validation.py` | `51712729b8903ccd557e8aa324098e334cab99f1` |
| `substrate_inheritance/test_hierarchical_closure_validation.py` | `02441d4ad7057f4f5d1b2296a1539c0a10875bc0` |
| `substrate_inheritance/requirements-validation.txt` | `4d5d71f764bcc86efe05af4051c983cd9579efda` |

Retained Actions artifacts for the dedicated FM4 execution:

- FM4 artifact ID: `10300070726`
- name: `substrate-inheritance-fm4-hierarchical-closure-v01`
- archive digest: `sha256:4b52b683e7f4635ea76ca4d1c05d8d2210589ddda8ac7dd418bad5201a33c181`
- synthetic-validation artifact ID: `10300145609`
- synthetic-validation digest: `sha256:ff351bc208d13693ba10717eed11bec0db0100be1aacb11852d77b654d708358`

The FM4 workflow artifact contains:

- `SI_FM4_HIERARCHICAL_CLOSURE_PLAN_v0.1.json`
- generated `results/SI_FM4_HIERARCHICAL_CLOSURE_RESULTS_v0.1.json`
- generated `results/validation_environment.txt`

### FM4 release rule

A future manuscript/release package using FM4 numerics must preserve the retained artifact digest or create a new clean-room result/environment manifest. Exact closure and approximate-error surfaces must remain in the same scientific package so the release cannot preserve only the favorable exact result while losing the approximate-method Limit Map.

## 4. FM2/FM3 parity reference

Already retained elsewhere:

### FM2

- run `34756837555`
- artifact `10317721694`
- archive SHA-256 `b897ddf7a70c21949bf93b689a59c20d62c2474c7d73bb6cc09cb7fb43a60d65`
- generated result SHA-256 `4415074b6ce0007bfcb07daa96e2e94daa10c04618fe683e2fdc72123ea58847`

### FM3

- run `34756644076`
- artifact `10317572637`
- archive SHA-256 `21e4c21b318cd86cc1ed83ecf05d242ebc26d705f7c1b270fec8ac2c5e320049`
- generated result SHA-256 `e59179fc993a9354ca1531f0c8ac673c78df0c96dc193c4e2ce81505a912e9a5`

## 5. Release-manifest minimum for the manuscript

For every manuscript-used FM result, the eventual freeze should carry:

- scientific plan/freeze identity;
- implementation identity;
- test identity;
- environment lock/realized environment;
- workflow/run identity or clean-room execution record;
- generated result SHA-256;
- archive/package SHA-256;
- summary version;
- figure-generation script identity when figures exist;
- figure source-result hash;
- figure artifact hashes;
- evidence class and nonclaim fields.

Git blob SHA and file SHA-256 are different identity systems and must not be mislabeled as one another.

## 6. Current disposition

`FM1_COMPACT_PROVENANCE = HARDENED_FROM_EXECUTION_COMMIT_PLUS_ACTIONS_DIGEST`

`FM4_COMPACT_PROVENANCE = HARDENED_FROM_EXECUTION_COMMIT_PLUS_ACTIONS_DIGEST`

`FM2_FM3_MANIFEST_PARITY = ALREADY_PRESENT`

`NEW_SCIENCE_RUN = NOT_REQUIRED`

`NEXT_RELEASE_PROVENANCE_DEPENDENCY = MANUSCRIPT_FIGURE_GENERATION_AND_HASHING_AFTER_FIGURE_SPEC_FREEZE`

This closes the current non-compute release-manifest hardening task without changing or rerunning FM1-FM4 science.