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

Frozen science, preregistrations, thresholds, exclusions, failure records, and interpretation firewalls remain controlling. FAIL, HOLD, null, NONIDENTIFIABLE, and REFUSE are admissible results and may not be repaired by retuning against observed outcomes.

## Closed measurement-conditioned lineage

### Conditional tangent derivation v0.1

**PASS** under frozen T0-T4 gates.

Canonical result:
`stability_arc/measurement_conditioned/CONDITIONAL_TANGENT_DERIVATION_AUDIT_RESULT_v0.1.md`

This closes the separate same-noise physical tangent and same-record inference tangent identities plus the exact real 2x2 reduction only.

### Joint-channel representation v0.1

**FAIL, permanently preserved.**

Canonical failed run: `33234191815`
Artifact: `9709402456`
Artifact SHA-256: `f95209cf3ae0480722e0391224e78ba663136387c141891bbc47f614e05f6f98`

Failure analysis remains canonical at:
`stability_arc/measurement_conditioned/representation_v01/FAILURE_SIGNAL_REPORT_v0.1.md`

The failure exposed an incorrect measurement-dissipator normalization, a missing stochastic amplitude in the matrix labeled `B`, and partial self-certification of the same-record comparative gate. The failure is not erased by later correction.

### Corrective joint-channel representation v0.2

**PASS** under frozen R0-R5 gates on fresh fixtures with independent full-map reconstruction.

Canonical run: `33234401976`
Execution commit: `1840750ce94ad5f3a62d9199ab14c9aee81dfe68`
Artifact: `9709462702`
Artifact SHA-256: `0ae0bf6cb694aacada0ad54427d3d56ae694868e5179702ef7d12159e4f56be9`
Result JSON SHA-256: `b29255c8957e252437476ecebf44df0ecf3cf383a4271060525069c8127c1116`

Canonical result:
`stability_arc/measurement_conditioned/representation_v02/JOINT_CHANNEL_REPRESENTATION_AUDIT_RESULT_v0.2.md`

Licensed representation:

`C = (A_phys, A_rec, DeltaA, B, A_joint)`

with constituent channel identities preserved. Full 3x3 channel matrices remain `FULL_MATRIX_REQUIRED`; no combined scalar is licensed.

### Stochastic second-moment / covariance lift v0.1

**PASS** under frozen M0-M6 gates.

Canonical run: `33234878303`
Execution commit: `68d1eb37df71b308add030e6bf9e7064b91faa3e`
Artifact: `9709601806`
Artifact SHA-256: `c95b21a8d54480b5e36443c278d5b90a0f6e631d6bcd3df29db7237179484bed`
Result JSON SHA-256: `0caf92f2ab9d7667b472124340176d30cf500f5c41e083ae2a1e7113496c2316`

Canonical result:
`stability_arc/measurement_conditioned/moment_lift_v01/STOCHASTIC_MOMENT_LIFT_AUDIT_RESULT_v0.1.md`

The closed stochastic tangent

`d r = A r dt + B r dW`

has the consistent second-moment lift

`dP/dt = A P + P A^T + B P B^T`

and column-major generator

`K(A,B) = I tensor A + A tensor I + B tensor B`.

Independent Richardson covariance reconstruction reached maximum residual `1.0191847366058937e-12` versus the frozen `2e-9` gate. All 6x6 and 12x12 moment objects remain `FULL_MOMENT_OPERATOR_REQUIRED`.

### Information-rank secular bridge v0.1

**PASS** under frozen I0-I6 gates.

Canonical run: `33245531943`
Execution commit: `3667e3a41f73e66552bd0c94cc8dfcfa61aff77e`
Artifact: `9712708402`
Artifact SHA-256: `465e5bf237e202e3d04855b0dc4f512962c3778cf4ec57697f14c1bfe11365a7`
Result JSON SHA-256: `8a07e8833ca67f7ca13aacd939e4cd5194de9d56afac2e84d794e119a12fdfb2`

Canonical result:
`stability_arc/measurement_conditioned/information_rank_v01/INFORMATION_RANK_SECULAR_BRIDGE_RESULT_v0.1.md`

Under the registered local continuous-measurement convention,

`A_rec = A_phys + U V^T`,

with `rank(UV^T) <= m` for `m` scalar record channels. Away from physical resolvent poles,

`det(zI-A_rec)/det(zI-A_phys) = det(I_m - V^T (zI-A_phys)^(-1) U)`.

The full physical, inference, and moment generators remain full matrix/operator objects. The secular determinant is comparative only.

The second-moment conditioning change obeys the closed upper bounds

`rank(DeltaK) <= 2 n r-r^2`

and

`rank(DeltaK_sym) <= r(2 n-r+1)/2`.

All five executed controls saturated those bounds, but saturation remains an observation only and is not promoted to a universal equality claim.

### Secular-continuation / mode-correspondence v0.1

**PASS_WITH_ALL_FRESH_PATHS_ADMISSIBLE** under frozen S0-S6 rules.

Canonical run: `33248271329`
Execution commit: `529924eee7e41115084695f3d7d748ce44a6806b`
Artifact: `9713536443`
Artifact SHA-256: `a40752981daa19f768c4216effff311c07671fb8bf494d20957a958208644581`
Result JSON SHA-256: `63b660aa9a75d1c649284d1260f155a19354875743f5217762a983aaf1c514c1`

Canonical preregistration:
`stability_arc/measurement_conditioned/secular_continuation_v01/PREREGISTRATION_SECULAR_CONTINUATION_MODE_CORRESPONDENCE_v0.1.md`

Canonical result:
`stability_arc/measurement_conditioned/secular_continuation_v01/SECULAR_CONTINUATION_MODE_CORRESPONDENCE_RESULT_v0.1.md`

The fixed path

`A(t)=A_phys+t U V^T`, `t=j/16`,

successfully tracked invariant spectral clusters for all three fresh quantum fixtures without using localization outcomes or hand mode labels. Conjugate pairs were preserved as 2D invariant-subspace objects rather than split into independent eigenvector labels.

Frozen audit values:

- path / low-rank identity max residual `1.0842021724855044e-16`;
- projector algebra max residual `2.2399083160561363e-16`;
- endpoint recovery residual `0.0`;
- secular-root max residual `7.203195710628172e-14`;
- all 18 exact physical-pole probes correctly returned `REFUSE_NEAR_PHYSICAL_POLE`;
- N1 initial degeneracy correctly refused at `t=0`;
- N2 conjugate-pair collision correctly refused at `t=0.5`;
- orthogonal-coordinate branch-representative residual `1.4228624520802642e-15`;
- projector covariance residual `4.458529307625244e-16`.

Interpretation remains:

- `PHYSICAL_GENERATOR=FULL_MATRIX_REQUIRED`;
- `RECORD_GENERATOR=FULL_MATRIX_REQUIRED`;
- `MODE_OBJECT=INVARIANT_CLUSTER_OR_REFUSE`;
- `SECULAR_OBJECT=COMPARATIVE_ONLY`;
- `SCALAR_CHI=NOT_LICENSED`.

## New exact conditioning-dark corollary

The continuation output showed an unchanged real singleton in all three fresh quantum controls. That observation was not reused as prospective evidence. Instead, it prompted an algebraic consequence check against the already-closed identity

`A_rec=A_phys+UV^T`.

Exact corollary:

If `W` is an `A_phys`-invariant subspace and `W subset ker(V^T)`, then

`A_rec|_W = A_phys|_W`.

Equivalently, if `A_phys x=lambda x` and `V^T x=0`, then `A_rec x=lambda x` exactly. Such a right mode is **conditioning-dark** with respect to the record-conditioning drift update. Dually, a physical left eigenvector satisfying `y^T U=0` is unchanged as a left mode.

For the registered single-observable qubit convention, the measurement functional acts on the `z` tangent coordinate while the physical generator has an exact `y`-axis eigenmode, explaining the zero-displacement singleton without fitting or threshold repair.

The corresponding moment-difference operator

`DeltaK = I tensor DeltaA + DeltaA tensor I`

annihilates `w1 tensor w2` whenever both `w1,w2 in ker(V^T)`. This concerns the conditioning **difference** only; it does not remove the shared stochastic `B tensor B` term and does not imply localization immunity.

This is presently the sharpest theoretical consequence of the joint same-noise / same-record program: measurement information enters through a rank-limited bridge, and physical invariant directions invisible to the measurement functional are spectrally protected from that conditioning update.

## GFSA state

GFSA v0.7.2 package validation, C18, OBS18, OBS19, external-interface licensing, and observable-only EP firewall remain closed PASS.

The external numerical-admission lane remains quarantined because the exact authentic frozen v0.7 external-candidate contract has not been recovered. Candidate response values must not be inspected, plotted, summarized, filtered, or scored until that contract is recovered, persisted, hashed, and bound.

No missing scientific rule may be reconstructed from memory, gate names, or outcomes.

## QuTiP state

QuTiP 5.3.1 runtime admission v0.1 remains `RUNTIME_ADMITTED` under frozen Q0-Q3 gates.

Canonical result:
`stability_arc/qutip_runtime/QUTIP_RUNTIME_ADMISSION_RESULT_v0.1.md`

Historical v0.6 notebook reproduction remains open. Expected historical notebook SHA-256:
`be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82`.

Runtime admission is not a substitute for recovering/reproducing the historical notebook.

## Failure-signal state

Failures remain evidence and cannot be deleted by later PASS results.

- run `33231598000`: **MECHANICAL / CI CONFIGURATION**, before scientific execution;
- run `33234191815`: **MATHEMATICAL SPECIFICATION / REPRESENTATION FAIL**, permanently retained;
- historical Phase 3Y Y2 FAIL -> fresh Phase 3Z remains the canonical precedent for failure-driven refinement without evidentiary recycling.

The new secular-continuation negative controls also establish that degeneracy/collision and physical-resolvent-pole states are explicit refusal regions, not invitations to loosen thresholds or invent labels.

## Anti-circularity state

- same-noise and same-record channels remain separate inside every joint representation;
- joint/conglomerate analysis is required, but constituent identities may not be erased;
- no average, weighting, mode pairing, scalar reduction, branch label, threshold, or preferred representation is selected from localization outcomes;
- v0.1 joint failure remains failed;
- corrective and successor audits used fresh outcome-free controls and frozen gates;
- the conditioning-dark statement is an exact algebraic corollary of the already-closed low-rank identity, not a fitted claim from the three continuation trajectories;
- GFSA external candidate values remain sealed.

## Next justified frontier

1. Freeze a fresh outcome-free **conditioning-dark / active-sector factorization audit**.
2. Distinguish instantaneous annihilation by `UV^T` from a genuinely invariant conditioning-dark subspace.
3. Verify common physical/inference characteristic factors globally without dividing at poles.
4. Determine whether the comparative secular problem can be reduced exactly to a measurement-visible invariant sector while preserving every moved eigenvalue and explicitly refusing non-invariant nullspaces.
5. Treat moment-rank-bound saturation as a separate post-hoc hypothesis requiring a new version and fresh controls if pursued.
6. Only after representation/factorization closure, design a separately preregistered prospective measurement/localization test on untouched systems.
7. Independently continue exact-source recovery for the authentic GFSA v0.7 external-admission contract.

## Blockers

- GFSA external admission: exact v0.7 contract/source package absent;
- historical QuTiP reproduction: authentic original notebook/source absent;
- historical Phase 4A: PENDING/INCOMPLETE.

None blocks the conditioning-dark / active-sector work.

## User action

None currently required.
