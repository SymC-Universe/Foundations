# H12 dephasing destabilization blind reveal v0.1

**Status:** FROZEN BEFORE HIDDEN FULL-STABILITY REVEAL
**Scope:** PROSPECTIVE_REVEAL_OF_FROZEN_H12_SELECTION

## Frozen input

Consume only the H12 Stage-A selection artifact from run `33269142763`, artifact `9719557784`.

Required selection SHA-256:
`364ba6a18b5ea8b8cad7a164028013bf605db5a44f847bcc9e1d13dfacb46de5`

The selected set contains exactly the first 64 fresh H12 `D_C13` eligible cases in deterministic generation order. No case may be replaced, removed, reordered for scoring, or supplemented after hidden stability is revealed.

H12 is the preregistered one-time same-family untouched-seed replication of the closed H11 D-side blind reveal. The reveal rule is inherited unchanged from the already-frozen H11 blind-reveal protocol except for binding to the immutable H12 selection bytes and naming the replication decision H12.

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

Frozen tolerances remain unchanged from H11:

- Stage-A replay / map tolerance: `1e-8`;
- Routh-Hurwitz margin tolerance: `1e-9`;
- canonical c1/c3 reconstruction: `2e-8`;
- canonical quotient matrix reconstruction: `2e-9`;
- second-moment intertwining: `5e-9`;
- dark-space numerical rank: `1e-9`.

## Stage-A replay

Before full-class scoring, independently verify every frozen row still satisfies the exact H12/H11 eligibility rule:

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

- `PASS_H12D_REPLICATION` only if all 64 frozen cases reconstruct cleanly, none is boundary, and all 64 are correct;
- `FAIL_H12D_REPLICATION` if any independently reconstructed nonboundary frozen case is not physical STABLE -> record UNSTABLE;
- `RECONSTRUCTION_HOLD` on any full-Hilbert/canonical/intertwining reconstruction failure;
- `BOUNDARY_HOLD` if any frozen case lies within the registered full-class boundary tolerance;
- `PROVENANCE_HOLD` on selection-hash or Stage-A replay mismatch.

For every scientific counterexample preserve exact hidden physical blockers `m2` and/or `mh`. Do not change the eligibility rule or replace the case.

## Stop rule after H12

H12 is the planned same-family replication. After this reveal closes, do not launch further repetitions of this same targeted dephasing family merely to increase sample size. The next calculation must be an already-justified independent generator/dissipation/measurement falsification or the project must explicitly enter `BRAINSTORMING/DECISION REQUIRED` before defining a new scientific direction.

## Interpretation firewall

A PASS would provide an independent untouched-seed replication of the bounded high-radius dephasing D-side result. It does not universalize destabilization, state radius, measurement angle, or c1/c3 sufficiency to other generators. No scalar chi is licensed by this phase.
