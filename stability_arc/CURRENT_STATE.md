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

Full 3x3 channel matrices remain `FULL_MATRIX_REQUIRED`; no combined scalar is licensed.

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

Moment objects remain full operators; no scalar compression is licensed.

### Information-rank secular bridge v0.1

**PASS** under frozen I0-I6 gates.

Canonical run: `33245531943`
Canonical result:
`stability_arc/measurement_conditioned/information_rank_v01/INFORMATION_RANK_SECULAR_BRIDGE_RESULT_v0.1.md`

Closed identities:

`A_rec = A_phys + U V^T`,

`rank(UV^T) <= m`,

and, away from physical poles,

`det(zI-A_rec)/det(zI-A_phys) = det(I_m - V^T (zI-A_phys)^(-1) U)`.

Closed second-moment rank bounds:

`rank(DeltaK) <= 2 n r-r^2`

and

`rank(DeltaK_sym) <= r(2 n-r+1)/2`.

Observed saturation in five controls remains observation only, not a promoted equality claim.

### Secular-continuation / mode-correspondence v0.1

**PASS_WITH_ALL_FRESH_PATHS_ADMISSIBLE** under frozen S0-S6 gates.

Canonical run: `33248271329`
Artifact: `9713536443`
Artifact SHA-256: `a40752981daa19f768c4216effff311c07671fb8bf494d20957a958208644581`
Canonical result:
`stability_arc/measurement_conditioned/secular_continuation_v01/SECULAR_CONTINUATION_MODE_CORRESPONDENCE_RESULT_v0.1.md`

The audit tracked invariant spectral clusters for all three fresh quantum fixtures, preserved conjugate pairs, refused initial degeneracy and a pair collision exactly where preregistered, and refused exact physical-resolvent poles. Mode objects remain invariant clusters or REFUSE.

### Conditioning-dark / active-sector factorization v0.1

**PASS** under frozen F0-F7 gates.

Canonical run: `33250353613`
Execution commit: `6d8cb0020038e0e0831fe858890c009e48247fd3`
Artifact: `9714162157`
Artifact SHA-256: `134a131d17ee9e5ca45a0cbbe4830f199a30df256194eb465999b6fb42dd3429`
Result JSON SHA-256: `59644460988d8775fa2b72e3d51b8eea480d3fa83bfb64bea17339208f125fda`
Canonical result:
`stability_arc/measurement_conditioned/dark_active_factor_v01/CONDITIONING_DARK_ACTIVE_FACTOR_RESULT_v0.1.md`

The maximal conditioning-dark subspace is defined outcome-free as

`D = ker([V^T; V^T A; ...; V^T A^(n-1)])`,

the maximal `A_phys`-invariant subspace contained in the instantaneous nullspace `ker(V^T)`.

For all three fresh quantum controls:

- `dim ker(V^T) = 2`;
- the full instantaneous nullspace was not dynamically invariant and correctly returned `REFUSE_FULL_KERNEL_FACTOR`;
- `dim D = 1`;
- the dark mode was exactly preserved by the record-conditioning drift update;
- the active quotient had dimension 2;
- the active quotient update retained rank 1.

Exact factorization for every admissible dark control:

`det(zI-A_phys) = det(zI-A_D) det(zI-A_A)`

and

`det(zI-A_rec) = det(zI-A_D) det(zI-Arec_A)`.

All conditioning-induced characteristic-polynomial change is contained in the active quotient after extracting only the independently constructed dark factor. Degenerate and defective sector controls correctly REFUSED attribution.

### Active-quotient scalar admissibility v0.1

**PASS** under frozen A0-A7 gates.

Canonical first run: `33252642667`
Execution commit: `e6833f60cb6591dc00b6be9e6403a6e5ed48b867`
Artifact: `9714831463`
Artifact SHA-256: `9aa92ed8d0a8f851b06c4723d161a350049fb9fbc453d64a3106af2d39e77c6c`
Result JSON SHA-256: `66ef426d61d0e1a850a4abe1a7fcfe09bccd88d6f870b0a4b0fb2024c406fa34`
Canonical result:
`stability_arc/measurement_conditioned/active_quotient_scalar_v01/ACTIVE_QUOTIENT_SCALAR_ADMISSIBILITY_RESULT_v0.1.md`

Base preregistration SHA-256:
`9afc75864f704d9a9f1310e102a58ca36b5ce24ed6cb45ad4f3361e2f1f07eda`

A pre-execution adversarial review found one refusal-coverage omission and added only RQ8 before any execution:
`stability_arc/measurement_conditioned/active_quotient_scalar_v01/PREEXECUTION_AMENDMENT_v0.1a.md`
SHA-256 `486b2d5e0bc08ba95432529dd2e9f5c3d2fbe571e12bf17d3a2853e06452f790`.

The canonical run established that when the independently reconstructed dark factor leaves an identifiable, real, asymptotically stable 2D deterministic active quotient,

`chi_active = -tr(A_A)/(2 sqrt(det(A_A)))`

is invariant under the frozen active-basis change and under a non-orthogonal complement shear plus active-basis change. Maximum trace, determinant, and chi residuals were at roundoff (`<=2.220446049250313e-16`). Polynomial-factor reconstruction agreed to `6.661338147750939e-16`, and three fresh canonical oscillator blocks recovered `Gamma/(2 Omega)` to `1.1102230246251565e-16`.

Separate admitted values on the fresh quantum controls were:

- AQ1: `chi_active_phys=0.25202432454547247`, `chi_active_rec=0.3352225058179115`;
- AQ2: `chi_active_phys=0.3181045051401759`, `chi_active_rec=0.40837538880643054`;
- AQ3: `chi_active_phys=0.32615439934795415`, `chi_active_rec=0.3871758850234289`.

Their ordering is observation only and is not a promoted directional claim.

All explicit refusal controls passed: wrong quotient dimension, unstable quotient, nonpositive determinant, cross-sector degeneracy, defective active sector, coordinate failure, non-real quotient, and absent nontrivial dark factor all returned the preregistered REFUSE states with no fallback scalar.

The full 3x3 generators remain `FULL_MATRIX_REQUIRED`. The multiplicative stochastic term remains `STOCHASTIC_TERM_NOT_COMPRESSED`.

A redundant orchestration-only run `33252664549` reproduced the identical result JSON SHA-256 and does not supersede the first canonical execution.

## Current theoretical consequence

The measurement-conditioned branch now has a mathematically licensed route from a full 3D deterministic generator to a scalar **without compressing the full system**:

1. reconstruct the maximal dynamically invariant conditioning-dark factor from the physical generator and measurement functional;
2. factor that exact common dark component from both physical and record-conditioned characteristic polynomials;
3. require the remaining active quotient to be exactly 2D, real, stable, identifiable, nondefective, and coordinate-valid;
4. only then define `chi_active=-tr/(2 sqrt(det))` separately on each deterministic active quotient.

This is stronger than the earlier low-rank bridge because it identifies exactly where a Stability Arc scalar is mathematically admissible and where it must be refused.

It is still a **deterministic quotient result**. The shared multiplicative stochastic tangent matrix `B` has not yet been shown to respect the same dark/active decomposition.

## Next justified frontier

The next safe question is therefore an outcome-free **stochastic dark/active compatibility and quotient-closure audit**.

Before any localization or measurement-performance test, freeze fresh controls that ask:

1. whether the independently reconstructed deterministic dark subspace also satisfies `B D subset D`;
2. whether the stochastic SDE descends exactly to the same 2D active quotient;
3. whether quotient `A_A` and quotient `B_A` are invariant under the allowed complement/basis changes;
4. whether the active second-moment generator closes on the quotient and agrees with direct full-system projection;
5. whether stochastic leakage across the dark/active split must trigger REFUSE rather than be hidden inside `chi_active`;
6. whether any later noise-aware stability coordinate is mathematically justified without fitting to localization outcomes.

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

Degeneracy, defectivity, collision, non-invariant-nullspace, physical-pole, quotient-dimension, instability, nonpositive determinant, non-real quotient, coordinate-failure, and nonidentifiable-dark-factor states are explicit refusal regions, not invitations to loosen thresholds.

## Anti-circularity state

- same-noise and same-record channels remain separate inside every joint representation;
- joint/conglomerate analysis is allowed, but constituent identities may not be erased;
- no average, weighting, mode pairing, scalar reduction, branch label, threshold, or preferred representation is selected from localization outcomes;
- the v0.1 joint failure remains failed;
- successor audits used fresh outcome-free controls and frozen gates;
- `chi_active_phys` and `chi_active_rec` are separately licensed only on admitted deterministic 2D active quotients;
- their observed ordering is not promoted;
- GFSA external candidate values remain sealed.

## Blockers

- GFSA external admission: exact v0.7 contract/source package absent;
- historical QuTiP reproduction: authentic original notebook/source absent;
- historical Phase 4A: PENDING/INCOMPLETE.

None blocks the stochastic dark/active compatibility audit.

## User action

None currently required.
