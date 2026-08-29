# Stability Arc current state

Last updated: 2026-08-29
Canonical repository: `SymC-Universe/Foundations`
Canonical working branch: `agent/stability-arc-gfsa-v072`

## Active project controls

- `stability_arc/gfsa_v0.7.2/ANTI_CIRCULARITY_GUARD_v0.1.md`
- `stability_arc/CONTINUITY_AND_FAILURE_SIGNAL_PROTOCOL_v0.1.md`
- `stability_arc/HISTORICAL_FAILURE_SIGNAL_RECOVERY_v0.1.md`
- `stability_arc/gfsa_v0.7.2/PROVENANCE_RECOVERY_SEARCH_LOG_v0.1.md`
- `stability_arc/gfsa_v0.7.2/external_admission/v0.7/RECOVERY_TARGETS_v0.1.json`
- `stability_arc/measurement_conditioned/PREREGISTRATION_CONDITIONAL_TANGENT_DERIVATION_AUDIT_v0.1.md`
- `stability_arc/measurement_conditioned/CONDITIONAL_TANGENT_DERIVATION_AUDIT_RESULT_v0.1.md`
- `stability_arc/measurement_conditioned/representation_v01/FAILURE_SIGNAL_REPORT_v0.1.md`
- `stability_arc/measurement_conditioned/representation_v02/PREREGISTRATION_JOINT_CHANNEL_REPRESENTATION_AUDIT_v0.2.md`
- `stability_arc/measurement_conditioned/representation_v02/JOINT_CHANNEL_REPRESENTATION_AUDIT_RESULT_v0.2.md`
- `stability_arc/qutip_runtime/QUTIP_RUNTIME_ADMISSION_RESULT_v0.1.md`

## Latest verified closed state

### GFSA observable interface

- GFSA v0.7.2 executable package validation: PASS.
- C18 calibration validity: PASS.
- OBS18 interface admissibility: PASS.
- OBS19 blind holdout: PASS.
- External interface status: LICENSED_FOR_EXTERNAL_NUMERICAL_ADMISSION.
- Observable-only EP firewall: PASS.

The licensed GFSA observable output remains limited to a finite-band visible modal pole-proximity interval across the permitted surrogate equivalence class, or `NONIDENTIFIABLE`. No hidden-generator order/rationality, mechanical chi, or observable-only exceptional-point claim is licensed.

### Measurement-conditioned derivation

- conditional measurement-tangent derivation audit v0.1: PASS under frozen T0-T4 gates;
- same-noise physical tangent and same-record inference tangent remain distinct objects;
- exact real 2x2 oscillator reduction to `Gamma/(2 Omega)` is closed;
- full higher-dimensional conditional objects are not automatically licensed a scalar chi.

### Joint-channel representation

- joint-channel representation audit v0.1: **FAIL**, preserved;
- corrective joint-channel representation audit v0.2: **PASS** under frozen R0-R5 gates using three fresh fixtures and independent full-map finite-difference reconstruction.

The licensed v0.2 joint object is

`C = (A_phys, A_rec, DeltaA, B, A_joint)`

with

- `A_phys`: same-noise deterministic local drift;
- `A_rec`: same-record deterministic local drift;
- `DeltaA=A_rec-A_phys`: conditioning contribution;
- `B`: fully normalized shared stochastic tangent matrix including `sqrt(2 eta kappa)`;
- `A_joint=diag(A_phys,A_rec)`: identity-preserving joint drift representation.

Full 3x3 channel matrices remain `FULL_MATRIX_REQUIRED`; no joint scalar compression is licensed.

### QuTiP runtime

QuTiP 5.3.1 runtime admission v0.1: `RUNTIME_ADMITTED` under frozen Q0-Q3 gates. This does not reproduce the historical v0.6 QuTiP notebook, which remains open.

## Current work-cycle milestone

### v0.1 joint-channel failure retained and mined for signal

Canonical failed run: `33234191815`, artifact `9709402456`, artifact SHA-256 `f95209cf3ae0480722e0391224e78ba663136387c141891bbc47f614e05f6f98`.

Only R0 failed numerically, but adversarial failure investigation identified three distinct weaknesses:

1. **measurement-dissipator normalization error:** for `2 kappa D[sigma_z/2]`, transverse Bloch damping is `kappa`, not `2 kappa`;
2. **diffusion normalization omission:** the matrix labeled `B` omitted the SDE prefactor `sqrt(2 eta kappa)`;
3. **self-certifying comparative gate:** v0.1 formed `A_rec` from the same conditioning formula it then checked, so that comparison was not independent.

The v0.1 result remains FAIL. It was not repaired in place.

### v0.2 corrective audit frozen on fresh evidence

Before execution, v0.2 froze:

- corrected unconditional control;
- correctly normalized stochastic matrix `B`;
- three fresh parameter/base-state fixtures not used in v0.1;
- independent same-noise and same-record Jacobian recovery from full nonlinear one-step maps using fixed `+/-dW` detector increments;
- unchanged conservative scalar-refusal logic.

Canonical successful run: `33234401976` at execution commit `1840750ce94ad5f3a62d9199ab14c9aee81dfe68`.

Frozen source identities at execution:

- preregistration SHA-256 `31dca30a5817bbdad8cdd1665c3e21ab86881a7d3a37b3bdae4f4e5350742517`
- audit-code SHA-256 `065b881c10ebe45159867cbf7b57000f00ee8c221a50f4f4b4789511bdfbc5f2`
- execution-workflow SHA-256 `cf1bc5d393ee14f13b470f470471a153225c2891ad18cd389c6f4b88948fa4e2`
- preserved v0.1 failure-report SHA-256 `7c1b89190fbc334195d638e1e2120a4153a14969c2c60a9f59394ab831e3dcdc`

All R0-R5 gates passed:

- R0 corrected control max error `1.1102230246251565e-16` under `5e-13`;
- R1 fully normalized diffusion: max analytic-vs-same-noise error `3.209545684779158e-10`, max analytic-vs-same-record error `1.168363461534483e-10`, max cross error `2.0411822232446752e-10`, all under `2e-6`;
- R2 independently reconstructed drift: max `A_phys` error `3.1673200728832285e-09`, max `A_rec` error `2.632416729042575e-09` under `2e-6`; `DeltaA` identity residual `5.551115123125783e-17`, rank one in all fresh fixtures;
- R3 joint characteristic-polynomial residual `3.552713678800501e-15` under `5e-10`;
- R4 common-coordinate invariance passed at floating-point residual scale;
- R5 exact 2x2 recovery passed and all invalid/wrong-shape controls were REFUSED.

Artifact ID `9709462702`, artifact ZIP SHA-256 `0ae0bf6cb694aacada0ad54427d3d56ae694868e5179702ef7d12159e4f56be9`.

Internal result JSON SHA-256: `b29255c8957e252437476ecebf44df0ecf3cf383a4271060525069c8127c1116`.

### Workflow hygiene

The old conditional-tangent workflow and failed v0.1 joint-channel workflow had overly broad path triggers that caused redundant reruns when provenance/result documents changed. Their triggers were narrowed mechanically. The v0.2 workflow trigger was also narrowed after the canonical execution so future result documentation does not silently rerun scientific gates. No scientific input or conclusion changed.

## Structural interpretation currently licensed

The user-requested conglomerate view is now mathematically explicit without conflating channels.

For the registered single-observable convention:

- same-noise and same-record channels share the same fully normalized local stochastic matrix `B`;
- same-record conditioning changes deterministic local perturbation drift through `DeltaA`;
- `DeltaA` is rank one in all three fresh fixtures under this convention;
- the joint characteristic polynomial is exactly the product of the two channel characteristic polynomials, so `A_joint` preserves both spectra rather than manufacturing an averaged one;
- the fresh fixtures have nonzero `[A_phys,A_rec]`, showing that conditioning is not merely a scalar rescaling of the physical drift in those fixtures.

These are representation-level results only. They do not establish localization prediction or a preferred stability boundary.

## Active frontiers

### A. Stochastic stability / moment-lift representation

The highest-priority unblocked mathematical issue is now that drift spectra alone do not contain the full stability information of

`d r = A r dt + B r dW`.

The next safe phase should freeze and audit the second-moment/covariance lift, where stochastic diffusion contributes explicitly. For a real linear local SDE, the candidate full-space moment operator is expected to involve the Kronecker terms

`K(A,B) = A tensor I + I tensor A + B tensor B`,

with channel-specific

- `K_phys = K(A_phys,B)`;
- `K_rec = K(A_rec,B)`;
- comparative `DeltaK = K_rec-K_phys`;
- a joint representation retaining both moment operators.

Before execution, this phase must independently derive the vectorization convention, verify it against direct covariance propagation, preserve coordinate invariance/refusal rules, and avoid scalar compression. No localization outcomes may be used to choose a moment metric, eigenmode, weighting, or threshold.

### B. Cross-channel mode correspondence

If modal comparisons are later made between physical and record-conditioned spectra, matching must be frozen outcome-free. A homotopy/continuation rule with degeneracy/ambiguity refusal is preferable to post-hoc nearest-mode pairing. This should be developed only after the moment-level stability object is validated, because stochastic stability may reorganize which modes are meaningful.

### C. QuTiP historical reproduction

The admitted QuTiP 5.3.1 runtime is available for future preregistered independent work. Historical reproduction remains blocked until the original v0.6 notebook/source with expected SHA-256 `be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82` or an authenticated exact equivalent is recovered.

### D. GFSA v0.7 external admission

Recover and bind the exact frozen v0.7 external-candidate admission contract before inspecting any candidate response values.

## Anti-circularity state

- GFSA external candidate search remains metadata-only.
- No external candidate numerical response may be inspected, plotted, summarized, filtered, or scored until the exact authentic v0.7 contract is recovered, persisted, hashed, and bound.
- No historical localization outcome was used to choose the v0.2 corrections, fresh fixtures, gates, or representation.
- v0.1 remains failed; v0.2 is a separately versioned corrective test on fresh fixtures.
- same-noise and same-record channels remain separately recoverable inside the joint representation.
- no combined scalar is licensed simply because it might align with chi=1.
- `REFUSE` and `NONIDENTIFIABLE` remain valid outcomes.

## Failure-signal state

Failures remain evidence.

- `33231598000`: **MECHANICAL / CI CONFIGURATION**, occurred before scientific execution and exposed a portability defect.
- `33234191815`: **MATHEMATICAL SPECIFICATION / REPRESENTATION AUDIT FAIL**, exposed a dissipator-normalization error and, on adversarial inspection, diffusion-normalization and self-certification weaknesses.
- Those failures remain preserved and are not overwritten by later PASS results.

The historical Phase 3Y Y2 FAIL -> separately frozen fresh Phase 3Z refinement remains the canonical precedent for learning from failure without recycling the failed evidence as confirmation.

## Current blockers

- **GFSA PROVENANCE / EXECUTION:** exact frozen v0.7 external-candidate contract and authoritative candidate-source package remain unrecovered.
- **HISTORICAL REPRODUCIBILITY:** original v0.6 QuTiP cross-check notebook/source remains unrecovered; runtime admission is not a substitute.
- **HISTORICAL SCIENTIFIC:** Phase 4A remains PENDING/INCOMPLETE and would require a new complete preregistered package if restarted.

None blocks the outcome-free measurement-conditioned moment-lift derivation.

## Queue

### COMPLETED THIS CYCLE

1. Froze and executed joint-channel representation audit v0.1.
2. Preserved its R0 failure rather than repairing it in place.
3. Investigated the failure deeply enough to expose two additional latent representation defects.
4. Froze a separately versioned v0.2 correction using fresh parameter/base-state fixtures.
5. Added independent full-map same-noise and same-record Jacobian reconstruction to eliminate the v0.1 self-certification path.
6. Executed v0.2 and closed R0-R5 as PASS.
7. Preserved exact source hashes, environment, result hashes, artifact ID, artifact digest, and v0.1 failure lineage.
8. Mechanically narrowed redundant workflow triggers without changing scientific logic.
9. Preserved the GFSA external-candidate quarantine throughout.

### ACTIVE

- derive and preregister the stochastic second-moment/covariance lift for the separate-plus-joint conditional tangent representation;
- continue exact-source recovery for the historical QuTiP notebook/source and GFSA v0.7 external contract when authenticatable sources become available.

### BLOCKED

- external numerical admission/scoring: exact v0.7 contract absent;
- historical QuTiP notebook reproduction: authentic source absent;
- historical Phase 4A: PENDING/INCOMPLETE.

### NEXT

1. Derive the exact moment-lift equation and vectorization convention independently before freezing its audit.
2. Freeze fresh controls that compare lifted covariance dynamics against direct one-step/short-time covariance propagation.
3. Preserve physical, record-conditioned, comparative, and joint moment operators separately.
4. Refuse scalar compression unless a later invariant rule independently warrants it.
5. Only after stochastic representation closure, preregister outcome-free cross-channel mode correspondence and eventually a genuinely prospective localization/interface test on untouched systems.

## User action

None currently required.
