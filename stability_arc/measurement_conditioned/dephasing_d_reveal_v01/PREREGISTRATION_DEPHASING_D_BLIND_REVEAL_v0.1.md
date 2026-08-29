# Dephasing destabilization blind reveal v0.1

**Status:** FROZEN BEFORE HIDDEN FULL-STABILITY REVEAL
**Scope:** PROSPECTIVE_REVEAL_OF_FROZEN_H11_SELECTION

## Frozen input

Consume only the H11 Stage-A selection artifact from run `33269021023`, artifact `9719520204`.

Required selection SHA-256:
`f0f266117f5f86ee6cf9e86667a73f4412844c2555a4fa0c81250f40978d80dc`

The selected set contains exactly the first 64 fresh H11 `D_C13` eligible cases in deterministic generation order. No case may be replaced, removed, reordered for scoring, or supplemented after hidden stability is revealed.

The H11 selected parameter values have not been used to tune the reveal rule. H11 broad outcomes motivated only the already-frozen H11 availability recovery; this reveal is bound to the resulting immutable selection hash.

## Frozen reconstruction

For every frozen case independently reconstruct the full two-level Hilbert-space model with:

- Hamiltonian `H=(omega/2) sigma_y`;
- amplitude damping jump `sqrt(gamma) sigma_-`;
- pure-dephasing jump `sqrt(gamma_phi/2) sigma_z`;
- planar measurement operator `X_theta=(sin(theta) sigma_x + cos(theta) sigma_z)/2`;
- measurement dissipator `2 kappa D[X_theta]`;
- stochastic tangent amplitude `sqrt(2 eta kappa)`;
- same-noise physical tangent and same-record deterministic correction kept separate.

Require a positive density matrix and exactly one physical dark dimension. Reconstruct the measurement-aligned 2D quotient and compare it against the already-closed dephasing canonical matrices.

Frozen tolerances:

- Stage-A replay / map tolerance: `1e-8`;
- Routh-Hurwitz margin tolerance: `1e-9`;
- canonical c1/c3 reconstruction: `2e-8`;
- canonical quotient matrix reconstruction: `2e-9`;
- second-moment intertwining: `5e-9`;
- dark-space numerical rank: `1e-9`.

## Stage-A replay

Before full-class scoring, independently verify every frozen row still satisfies the exact H11 eligibility rule:

1. `abs(Delta_phi)/R > 1e-8`;
2. `c1_phys/R > 1e-8`;
3. `c3_phys/R^3 > 1e-8`;
4. `c3_record/R^3 < -1e-8`.

Any failure is `PROVENANCE_HOLD`, not a scientific result.

## Hidden reveal and decision

For each frozen case construct physical and same-record symmetric second-moment generators and reveal all four Routh-Hurwitz margins:

`m1=c1/R`, `m2=c2/R^2`, `m3=c3/R^3`, `mh=(c1*c2-c3)/R^3`.

A case is correct iff the full physical class is `STABLE` and the full same-record class is `UNSTABLE`.

Decision:

- `PASS_H11D_BLIND_REVEAL` only if all 64 frozen cases reconstruct cleanly, none is boundary, and all 64 are correct;
- `FAIL_H11D_BLIND_REVEAL` if any independently reconstructed nonboundary frozen case is not physical STABLE -> record UNSTABLE;
- `RECONSTRUCTION_HOLD` on any full-Hilbert/canonical/intertwining reconstruction failure;
- `BOUNDARY_HOLD` if any frozen case lies within the registered full-class boundary tolerance;
- `PROVENANCE_HOLD` on selection-hash or Stage-A replay mismatch.

For every scientific counterexample preserve the exact hidden physical blockers `m2` and/or `mh`. Do not change H11 eligibility or replace the case.

## Interpretation firewall

A PASS would support only this explicitly targeted fresh high-radius dephasing-augmented D-side family. It does not universalize destabilization, state radius, measurement angle, or c1/c3 sufficiency to other generators. A FAIL must be mined for the smallest missing invariant and then tested on new evidence. No scalar chi is licensed by this phase.