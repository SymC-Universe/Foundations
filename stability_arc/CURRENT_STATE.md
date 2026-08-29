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

**PASS** under frozen T0-T4 gates.

Canonical result:
`stability_arc/measurement_conditioned/CONDITIONAL_TANGENT_DERIVATION_AUDIT_RESULT_v0.1.md`

This closes the registered same-noise physical tangent and same-record inference tangent identities plus the exact real 2x2 reduction. It does not establish localization prediction or a general scalar chi.

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

The v0.1 FAIL remains failed and is not erased by later correction.

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

Key frozen audit values:

- M0 vectorization max residual `0.0`;
- M1 symmetric projection max residual `2.220446049250313e-16`;
- M2 independent Richardson covariance reconstruction max residual `1.0191847366058937e-12` versus gate `2e-9`;
- M3 comparative moment identity max residual `2.220446049250313e-16`;
- M4 coordinate-similarity max residual `6.661338147750939e-16`;
- M5 joint block recovery max residual `0.0`;
- M6 noiseless spectral-inheritance max mismatch `2.673771110915334e-15`.

All 6x6 and 12x12 moment objects remain `FULL_MOMENT_OPERATOR_REQUIRED`.

### Information-rank secular bridge v0.1

**PASS** under frozen I0-I6 gates. This is the current theoretical frontier milestone.

Canonical run: `33245531943`
Execution commit: `3667e3a41f73e66552bd0c94cc8dfcfa61aff77e`
Artifact: `9712708402`
Artifact SHA-256: `465e5bf237e202e3d04855b0dc4f512962c3778cf4ec57697f14c1bfe11365a7`
Result JSON SHA-256: `8a07e8833ca67f7ca13aacd939e4cd5194de9d56afac2e84d794e119a12fdfb2`

Canonical preregistration:
`stability_arc/measurement_conditioned/information_rank_v01/PREREGISTRATION_INFORMATION_RANK_SECULAR_BRIDGE_v0.1.md`

Canonical result:
`stability_arc/measurement_conditioned/information_rank_v01/INFORMATION_RANK_SECULAR_BRIDGE_RESULT_v0.1.md`

The frozen audit establishes the following local comparative structure under the registered continuous-measurement convention.

Each scalar measurement record contributes one outer-product conditioning correction. For `m` scalar records,

`DeltaA = U V^T = sum_j u_j v_j^T`

and therefore

`rank(DeltaA) <= m`.

The same-record inference generator is thus a rank-limited update of the same-noise physical generator:

`A_rec = A_phys + U V^T`.

Away from physical resolvent poles,

`det(zI-A_rec)/det(zI-A_phys) = det(I_m - V^T (zI-A_phys)^(-1) U)`.

For one scalar record, the comparative bridge is a scalar meromorphic secular factor, but this does **not** scalarize either full generator. At physical poles the resolvent ratio is refused and the global adjugate characteristic-polynomial identity remains the valid representation.

Frozen audit values:

- independent quantum Jacobian reconstruction max error `1.0115218218587074e-08`;
- rank-one global characteristic identity max residual `3.794299872214038e-15`;
- determinant-lemma secular residual max `7.020296723414116e-16`;
- coordinate-invariance residual max `2.2215299868541707e-16`;
- all three fresh quantum fixtures had `rank(DeltaA)=1`;
- the `m=2` and `m=3` controls had update ranks 2 and 3, satisfying the registered information-rank bound.

The second-moment conditioning change obeys the registered bounds

`rank(DeltaK) <= 2 n r-r^2`

and

`rank(DeltaK_sym) <= r(2 n-r+1)/2`,

where `r=rank(DeltaA)`. For one effective scalar record these reduce to `<=2n-1` and `<=n`.

In all five executed controls the registered upper bounds were numerically saturated. That saturation is retained as an observation only; equality was not preregistered as a universal claim and is not promoted.

Interpretation remains:

- `PHYSICAL_GENERATOR=FULL_MATRIX_REQUIRED`;
- `RECORD_GENERATOR=FULL_MATRIX_REQUIRED`;
- `MOMENT_GENERATOR=FULL_MOMENT_OPERATOR_REQUIRED`;
- `SECULAR_OBJECT=COMPARATIVE_ONLY`.

No localization predictor, preferred mode, scalar chi, or chi=1 optimum is licensed by this result.

## Scientific significance of the current frontier

The same-noise and same-record descriptions are now connected without conflation. The information carried by the measurement record enters the local inference-stability drift through a rank-limited bridge whose rank is bounded by the number of scalar record channels. Consequently, the **comparative** spectral relation can be represented through an `m x m` secular determinant even though the physical, inference, and moment generators themselves remain full-dimensional objects.

This is a new structural result inside the measurement-conditioned Stability Arc investigation. It is theoretical/local and still requires prospective connection to physical measurement behavior before any stronger Stability Arc claim is warranted.

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
- joint/conglomerate analysis is required, but constituent identities may not be erased;
- no average, weighting, mode pairing, scalar reduction, or preferred representation may be selected from localization outcomes;
- v0.1 failure remains failed;
- v0.2 corrective PASS used fresh fixtures and independent reconstruction;
- moment-lift v0.1 and information-rank v0.1 were frozen before execution on fresh controls;
- GFSA external candidate values remain sealed.

## Next justified frontier

1. Freeze an outcome-free **secular-continuation / mode-correspondence audit** that uses the information-rank bridge to track physical-to-inference spectral motion while explicitly refusing ambiguous, degenerate, near-pole, or branch-collision cases.
2. Preserve conjugate-pair / invariant-subspace structure rather than forcing one-to-one eigenvector matches when the mathematics does not support them.
3. Treat the observed saturation of the moment-rank bounds as a post-hoc hypothesis only. If pursued, test equality on genuinely fresh controls under a new version.
4. Only after representation and correspondence closure, preregister a prospective measurement/localization test on untouched systems. Historical localization outcomes remain unavailable for choosing metrics, modes, thresholds, or combinations.
5. Independently continue exact-source recovery for the authentic GFSA v0.7 external-admission contract.

## Blockers

- GFSA external admission: exact v0.7 contract/source package absent;
- historical QuTiP reproduction: authentic original notebook/source absent;
- historical Phase 4A: PENDING/INCOMPLETE.

None blocks the outcome-free secular-continuation work.

## User action

None currently required.
