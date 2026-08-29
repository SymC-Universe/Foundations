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

Canonical failure analysis:
`stability_arc/measurement_conditioned/representation_v01/FAILURE_SIGNAL_REPORT_v0.1.md`

The failure exposed an incorrect measurement-dissipator normalization, a missing stochastic amplitude in the matrix labeled `B`, and partial self-certification of the same-record comparative gate. It remains failed.

### Corrective joint-channel representation v0.2

**PASS** under frozen R0-R5 gates on fresh fixtures with independent full-map reconstruction.

Canonical run: `33234401976`
Artifact: `9709462702`
Artifact SHA-256: `0ae0bf6cb694aacada0ad54427d3d56ae694868e5179702ef7d12159e4f56be9`
Canonical result:
`stability_arc/measurement_conditioned/representation_v02/JOINT_CHANNEL_REPRESENTATION_AUDIT_RESULT_v0.2.md`

Licensed full representation remains

`C = (A_phys, A_rec, DeltaA, B, A_joint)`.

Full 3x3 channel matrices remain `FULL_MATRIX_REQUIRED`.

### Stochastic second-moment lift v0.1

**PASS** under frozen M0-M6 gates.

Canonical run: `33234878303`
Artifact: `9709601806`
Canonical result:
`stability_arc/measurement_conditioned/moment_lift_v01/STOCHASTIC_MOMENT_LIFT_AUDIT_RESULT_v0.1.md`

Closed lift:

`dP/dt = A P + P A^T + B P B^T`

with column-major generator

`K(A,B) = I tensor A + A tensor I + B tensor B`.

Moment objects remain full operators.

### Information-rank secular bridge v0.1

**PASS** under frozen I0-I6 gates.

Canonical run: `33245531943`
Canonical result:
`stability_arc/measurement_conditioned/information_rank_v01/INFORMATION_RANK_SECULAR_BRIDGE_RESULT_v0.1.md`

Closed identities include

`A_rec = A_phys + U V^T`,

`rank(UV^T) <= m`,

and away from physical poles

`det(zI-A_rec)/det(zI-A_phys) = det(I_m - V^T (zI-A_phys)^(-1) U)`.

Closed second-moment rank bounds:

`rank(DeltaK) <= 2 n r-r^2`

and

`rank(DeltaK_sym) <= r(2 n-r+1)/2`.

Observed saturation remains observation only.

### Secular-continuation / mode-correspondence v0.1

**PASS_WITH_ALL_FRESH_PATHS_ADMISSIBLE** under frozen S0-S6 gates.

Canonical run: `33248271329`
Artifact: `9713536443`
Artifact SHA-256: `a40752981daa19f768c4216effff311c07671fb8bf494d20957a958208644581`
Canonical result:
`stability_arc/measurement_conditioned/secular_continuation_v01/SECULAR_CONTINUATION_MODE_CORRESPONDENCE_RESULT_v0.1.md`

The audit tracked invariant spectral clusters on fresh controls, preserved conjugate pairs, and refused degeneracy, collision, and exact physical-resolvent poles where preregistered.

### Conditioning-dark / active-sector factorization v0.1

**PASS** under frozen F0-F7 gates.

Canonical run: `33250353613`
Execution commit: `6d8cb0020038e0e0831fe858890c009e48247fd3`
Artifact: `9714162157`
Artifact SHA-256: `134a131d17ee9e5ca45a0cbbe4830f199a30df256194eb465999b6fb42dd3429`
Result JSON SHA-256: `59644460988d8775fa2b72e3d51b8eea480d3fa83bfb64bea17339208f125fda`
Canonical result:
`stability_arc/measurement_conditioned/dark_active_factor_v01/CONDITIONING_DARK_ACTIVE_FACTOR_RESULT_v0.1.md`

The maximal conditioning-dark subspace is reconstructed outcome-free as

`D = ker([V^T; V^T A; ...; V^T A^(n-1)])`.

For the fresh qubit controls, `dim ker(V^T)=2` but only a one-dimensional subspace is dynamically invariant. The common dark factor is exact and all deterministic conditioning-induced characteristic change is confined to the remaining 2D active quotient. Degenerate and defective attribution controls REFUSED as required.

### Active-quotient scalar admissibility v0.1

**PASS** under frozen A0-A7 gates.

Canonical first run: `33252642667`
Execution commit: `e6833f60cb6591dc00b6be9e6403a6e5ed48b867`
Artifact: `9714831463`
Artifact SHA-256: `9aa92ed8d0a8f851b06c4723d161a350049fb9fbc453d64a3106af2d39e77c6c`
Result JSON SHA-256: `66ef426d61d0e1a850a4abe1a7fcfe09bccd88d6f870b0a4b0fb2024c406fa34`
Canonical result:
`stability_arc/measurement_conditioned/active_quotient_scalar_v01/ACTIVE_QUOTIENT_SCALAR_ADMISSIBILITY_RESULT_v0.1.md`

When the independently reconstructed active quotient is exactly 2D, real, asymptotically stable, identifiable, nondefective, and coordinate-valid, the deterministic coordinate

`chi_active = -tr(A_A)/(2 sqrt(det(A_A)))`

is licensed separately for physical and record-conditioned channels. The full 3x3 generators remain `FULL_MATRIX_REQUIRED`; the stochastic term remained uncompressed at this stage.

A redundant orchestration-only run `33252664549` reproduced the identical result JSON hash and does not supersede the first canonical execution.

### Stochastic dark/active compatibility and quotient closure v0.1

**PASS** under frozen S0-S7 gates.

Canonical run: `33255726584`
Execution commit: `2394f836902bddc934eda3fae1cd31e71a7c27d9`
Artifact: `9715736382`
Artifact SHA-256: `2572a5197475e6d586663b4607f4ce5ff087a302fead240ccb7b39900674d360`
Result JSON SHA-256: `985f21fdd278c44503045716eb124b6a9906202b642da3775e8bd623dbdfc21e`
Canonical result:
`stability_arc/measurement_conditioned/stochastic_dark_active_v01/STOCHASTIC_DARK_ACTIVE_QUOTIENT_RESULT_v0.1.md`

Frozen source identities:

- preregistration SHA-256 `cd201a8279860dbf14708c7c744fdc8fa59487b4f8bf52b2546fcf078ab6e40a`;
- code SHA-256 `3a8b969d656d9035050fe66073dc1bf3ae9735906b7432a7211b3e671a135164`;
- workflow SHA-256 `e67708350d88f3b141205a38d36af8133a0e12c1ec6a1f13755509a502d5bdef`.

For all three fresh quantum controls, the independently reconstructed deterministic dark subspace also satisfied

`B D subset D`.

The maximum stochastic leakage residual was `2.900837493222097e-17`. Therefore the full local multiplicative-noise SDE descends exactly to the same two-dimensional quotient:

`d q = A_A q dt + B_A q dW`.

The quotient intertwining identities

`L A = A_A L`

and

`L B = B_A L`

held to `2.669225551699129e-16`, and the second-moment intertwining

`(L tensor L) K(A,B) = K(A_A,B_A) (L tensor L)`

held to `2.72301505788164e-16`. Direct full-vs-quotient stochastic trajectories and covariance propagation agreed to `5.551115123125783e-17`.

The result survived the frozen non-orthogonal complement shear and active-basis change at roundoff. All refusal controls returned exactly the preregistered states, including `REFUSE_STOCHASTIC_LEAKAGE`.

The dark coordinate is **not** claimed to be noise-free. The licensed statement is exact stochastic quotient closure: active projected dynamics do not depend on which representative is chosen along the dark fiber.

The stochastic pair remains

`STOCHASTIC_PAIR_NOT_COMPRESSED`.

No noise-aware scalar is licensed.

## Current theoretical consequence

The measurement-conditioned branch now supports the following outcome-free hierarchy:

1. separate physical and same-record tangent dynamics are valid;
2. measurement conditioning enters the deterministic drift through a low-rank bridge;
3. an exact dynamically invariant conditioning-dark factor can be reconstructed from the physical generator and measurement functional;
4. all deterministic conditioning-induced spectral change lies in a 2D active quotient for the admitted qubit controls;
5. a deterministic `chi_active` is licensed only on that admitted 2D quotient;
6. the same dark factor is also invariant under the multiplicative stochastic tangent matrix for fresh controls;
7. therefore the **full stochastic local tangent SDE**, not merely its drift, descends exactly to the same 2D active quotient.

This removes the previous stochastic-leakage objection to using the active quotient as the correct reduced state space. It does **not** remove stochasticity from the problem and does not make deterministic `chi_active` a complete stochastic stability coordinate.

## Next justified frontier

The next safe question is the **mean-square stability geometry of the exact 2D stochastic active quotient**.

The quotient second moment is three-dimensional. A new outcome-free phase should derive and freeze the real 3x3 symmetric second-moment generator for `(A_A,B_A)`, its coordinate-invariant characteristic coefficients, and the exact cubic Routh-Hurwitz stability conditions. It should explicitly distinguish deterministic damping morphology (`chi_active`, including the critical-damping boundary) from stochastic mean-square stability loss.

A suitable next audit must, before execution:

- use fresh quantum fixtures and independent synthetic controls;
- verify induced-coordinate invariance of the quotient second-moment characteristic polynomial;
- verify the cubic Routh-Hurwitz classifier against direct eigenvalue signs and direct covariance evolution;
- include exact stable, unstable, and boundary controls;
- include noiseless oscillator controls on both sides of and at `chi=1` to test whether critical damping is or is not a mean-square stability boundary;
- preserve physical and record-conditioned channels separately;
- return `MEAN_SQUARE_INVARIANTS_REQUIRED` unless a later independently derived scalar is mathematically justified;
- use no historical localization or measurement-performance outcome to choose coefficients, margins, thresholds, or preferred channel.

No claim connecting `chi_active` to localization, collapse, or measurement quality is licensed yet.

## GFSA state

GFSA v0.7.2 package validation, C18, OBS18, OBS19, external-interface licensing, and observable-only EP firewall remain closed PASS.

The external numerical-admission lane remains quarantined because the exact authentic frozen v0.7 external-candidate contract has not been recovered. Candidate response values must not be inspected, plotted, summarized, filtered, or scored until that contract is recovered, persisted, hashed, and bound.

No missing scientific rule may be reconstructed from memory, gate names, or outcomes.

## QuTiP state

QuTiP 5.3.1 runtime admission v0.1 remains `RUNTIME_ADMITTED`.

Historical v0.6 notebook reproduction remains open. Expected historical notebook SHA-256:
`be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82`.

Runtime admission is not a substitute for recovering/reproducing the historical notebook.

## Failure-signal state

Failures remain evidence and cannot be deleted by later PASS results.

- run `33231598000`: **MECHANICAL / CI CONFIGURATION**, before scientific execution;
- run `33234191815`: **MATHEMATICAL SPECIFICATION / REPRESENTATION FAIL**, permanently retained;
- historical Phase 3Y Y2 FAIL -> fresh Phase 3Z remains the canonical precedent for failure-driven refinement without evidentiary recycling.

Stochastic leakage, degeneracy, defectivity, collision, non-invariant nullspace, physical-pole, quotient-dimension, instability, nonpositive determinant, non-real quotient, coordinate failure, and nonidentifiable-dark-factor states are explicit refusal regions, not invitations to loosen thresholds.

## Anti-circularity state

- same-noise and same-record channels remain separate inside every joint representation;
- joint/conglomerate analysis is allowed, but constituent identities may not be erased;
- no average, weighting, mode pairing, scalar reduction, branch label, threshold, or preferred representation is selected from localization outcomes;
- the v0.1 joint failure remains failed;
- successor audits use fresh outcome-free controls and frozen gates;
- deterministic `chi_active_phys` and `chi_active_rec` are separately licensed only on admitted deterministic 2D quotients;
- stochastic quotient closure is now independently licensed, but the pair `(A_A,B_A)` remains uncompressed;
- GFSA external candidate values remain sealed.

## Blockers

- GFSA external admission: exact v0.7 contract/source package absent;
- historical QuTiP reproduction: authentic original notebook/source absent;
- historical Phase 4A: PENDING/INCOMPLETE.

None blocks the mean-square stability geometry audit.

## User action

None currently required.
