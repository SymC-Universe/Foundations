# Stability Arc current state

Last updated: 2026-08-29
Canonical repository: `SymC-Universe/Foundations`
Canonical working branch: `agent/stability-arc-gfsa-v072`

## Active controls

- `stability_arc/gfsa_v0.7.2/ANTI_CIRCULARITY_GUARD_v0.1.md`
- `stability_arc/CONTINUITY_AND_FAILURE_SIGNAL_PROTOCOL_v0.1.md`
- `stability_arc/HISTORICAL_FAILURE_SIGNAL_RECOVERY_v0.1.md`
- `stability_arc/gfsa_v0.7.2/PROVENANCE_RECOVERY_SEARCH_LOG_v0.1.md`
- `stability_arc/gfsa_v0.7.2/external_admission/v0.7/RECOVERY_TARGETS_v0.1.json`

## Closed measurement-conditioned milestones

### Conditional tangent derivation v0.1

PASS under frozen T0-T4 gates.

Canonical result:
`stability_arc/measurement_conditioned/CONDITIONAL_TANGENT_DERIVATION_AUDIT_RESULT_v0.1.md`

This closes the registered same-noise and same-record tangent identities and exact real 2x2 reduction only. It does not establish localization prediction or a general scalar chi.

### Joint-channel representation v0.1

**FAIL, permanently preserved.**

Canonical failed run: `33234191815`
Artifact: `9709402456`
Artifact SHA-256: `f95209cf3ae0480722e0391224e78ba663136387c141891bbc47f614e05f6f98`

Failure investigation established three issues:

1. for `2 kappa D[sigma_z/2]`, transverse Bloch damping is `kappa`, not `2 kappa`;
2. the v0.1 matrix labeled `B` omitted the SDE amplitude `sqrt(2 eta kappa)`;
3. the v0.1 same-record comparative gate partly self-certified because it constructed `A_rec` from the formula it then checked.

Canonical failure analysis:
`stability_arc/measurement_conditioned/representation_v01/FAILURE_SIGNAL_REPORT_v0.1.md`

The v0.1 FAIL is not erased by later correction.

### Corrective joint-channel representation v0.2

**PASS** under frozen R0-R5 gates using three fresh parameter/base-state fixtures and an independent full-map finite-difference reconstruction.

Canonical run: `33234401976`
Execution commit: `1840750ce94ad5f3a62d9199ab14c9aee81dfe68`
Artifact: `9709462702`
Artifact SHA-256: `0ae0bf6cb694aacada0ad54427d3d56ae694868e5179702ef7d12159e4f56be9`
Result JSON SHA-256: `b29255c8957e252437476ecebf44df0ecf3cf383a4271060525069c8127c1116`

Canonical result:
`stability_arc/measurement_conditioned/representation_v02/JOINT_CHANNEL_REPRESENTATION_AUDIT_RESULT_v0.2.md`

Licensed representation:

`C = (A_phys, A_rec, DeltaA, B, A_joint)`

where the same-noise and same-record channels remain individually recoverable, `DeltaA=A_rec-A_phys` is the conditioning contribution, `B` is the fully normalized shared stochastic tangent matrix for the registered convention, and `A_joint=diag(A_phys,A_rec)` preserves both channel spectra.

For the three fresh v0.2 fixtures:

- corrected unconditional-control max error: `1.1102230246251565e-16`;
- fully normalized `B` reconstruction max error: `3.209545684779158e-10`;
- independently reconstructed `A_phys` max error: `3.1673200728832285e-09`;
- independently reconstructed `A_rec` max error: `2.632416729042575e-09`;
- `DeltaA` identity max residual: `5.551115123125783e-17`;
- `DeltaA` numerical rank: 1 for all fresh fixtures under the frozen convention;
- joint characteristic-polynomial max residual: `3.552713678800501e-15`;
- all registered scalar-refusal controls passed.

Full 3x3 channel matrices remain `FULL_MATRIX_REQUIRED`. No combined scalar is licensed.

## Current frozen next frontier

### Stochastic second-moment / covariance lift v0.1

**PREREGISTERED / FROZEN BEFORE EXECUTION.**

Preregistration:
`stability_arc/measurement_conditioned/moment_lift_v01/PREREGISTRATION_STOCHASTIC_MOMENT_LIFT_AUDIT_v0.1.md`

The reason for this phase is mathematical, not outcome-driven: drift spectra alone do not contain the full stability information of the multiplicative-noise local SDE

`d r = A r dt + B r dW`.

The frozen Itô lift is

`dP/dt = A P + P A^T + B P B^T`

for `P=E[r r^T]`, with column-major vectorization

`K(A,B) = I tensor A + A tensor I + B tensor B`.

The preregistration preserves separate and joint moment objects:

- `K_phys`;
- `K_rec`;
- `DeltaK=K_rec-K_phys`;
- 6x6 symmetric-covariance projections `K_phys_sym` and `K_rec_sym`;
- `DeltaK_sym`;
- `K_joint_sym=diag(K_phys_sym,K_rec_sym)`.

No scalar compression is licensed.

The moment-lift audit is frozen on three fresh parameter/base-state fixtures not used in joint-channel v0.1 or v0.2. It includes:

- explicit column-major vectorization checks;
- symmetric covariance-subspace closure;
- independent deterministic sigma-point plus `+/-sqrt(dt)` noise-node covariance propagation;
- Richardson removal of the known Euler remainder with fixed `dt=1e-3` and `5e-4`;
- comparative `DeltaK` identity checks;
- common-coordinate covariance checks;
- joint block-identity preservation;
- scalar refusal;
- a noiseless 2x2 pairwise-eigenvalue-sum inheritance control that does not license applying the original scalar chi directly to the moment operator.

No localization outcome was consulted in choosing this phase, fixtures, metrics, or gates.

## GFSA state

GFSA v0.7.2 package validation, C18, OBS18, OBS19, external-interface licensing, and observable-only EP firewall remain closed PASS.

The external numerical-admission lane remains quarantined because the exact authentic frozen v0.7 external-candidate contract has not been recovered. Candidate response values must not be inspected, plotted, summarized, filtered, or scored until that contract is recovered, persisted, hashed, and bound.

No missing scientific rule may be reconstructed from memory, gate names, or outcomes.

## QuTiP state

QuTiP 5.3.1 runtime admission v0.1 is `RUNTIME_ADMITTED` under frozen Q0-Q3 gates.

Canonical result:
`stability_arc/qutip_runtime/QUTIP_RUNTIME_ADMISSION_RESULT_v0.1.md`

Historical v0.6 notebook reproduction remains open. Expected historical notebook SHA-256:
`be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82`.

Runtime admission is not a substitute for recovering/reproducing the historical notebook.

## Failure-signal state

Failures remain evidence and cannot be deleted by later PASS results.

- run `33231598000`: **MECHANICAL / CI CONFIGURATION**, before scientific execution;
- run `33234191815`: **MATHEMATICAL SPECIFICATION / REPRESENTATION FAIL**, retained and used only to motivate separately frozen fresh corrective evidence;
- historical Phase 3Y Y2 FAIL -> fresh Phase 3Z remains the canonical precedent for failure-driven hypothesis refinement without evidentiary recycling.

`REFUSE`, `NONIDENTIFIABLE`, HOLD, null, and negative outcomes remain legitimate results and must be investigated rather than discarded.

## Anti-circularity state

- same-noise and same-record channels remain separate inside every joint representation;
- joint/conglomerate analysis is allowed and required, but constituent identities may not be erased;
- no average, weighting, mode pairing, scalar reduction, or preferred representation may be selected from localization outcomes;
- v0.1 failure remains failed;
- v0.2 corrective PASS used fresh fixtures and independent reconstruction;
- moment-lift v0.1 is frozen before execution on fresh fixtures;
- GFSA external candidate values remain sealed.

## Workflow hygiene

Broad path triggers that caused redundant reruns of frozen audits were narrowed mechanically. This changed orchestration only, not scientific inputs or conclusions.

## Active work

1. adversarially review the frozen moment-lift v0.1 preregistration for algebraic orientation, self-certification, hidden scalar assumptions, and failure modes;
2. implement the frozen moment-lift audit without changing its scientific contract;
3. launch it in GitHub Actions only after the implementation matches the frozen contract;
4. preserve PASS/FAIL/HOLD exactly and investigate any failure before formulating a successor;
5. after moment-level closure, develop outcome-free cross-channel mode correspondence with ambiguity/degeneracy refusal before any prospective localization test.

## Blockers

- GFSA external admission: exact v0.7 contract/source package absent;
- historical QuTiP reproduction: authentic original notebook/source absent;
- historical Phase 4A: PENDING/INCOMPLETE.

None blocks the moment-lift audit.

## User action

None currently required.
