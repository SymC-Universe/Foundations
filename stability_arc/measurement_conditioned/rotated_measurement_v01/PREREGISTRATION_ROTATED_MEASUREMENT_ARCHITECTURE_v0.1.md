# Rotated-measurement stochastic architecture audit v0.1

**Status:** FROZEN BEFORE EXECUTION
**Scope:** INDEPENDENT_MEASUREMENT_GEOMETRY_TRANSFER_TEST

## Purpose

The preceding measurement-conditioned lineage used measurement operator `sigma_z/2`. This phase changes the measurement geometry before any localization or performance outcome is consulted.

Fix the new measured observable

`X45 = (sigma_x + sigma_z)/(2*sqrt(2))`,

a 45-degree rotation in the x-z plane.

Keep the Hamiltonian and amplitude-damping geometry unchanged:

`H = omega*sigma_y/2`,

`c = sqrt(gamma)*sigma_-`,

with unconditional measurement backaction `2*kappa*D[X45]`.

The phase tests whether the separate same-noise physical tangent, same-record correction, conditioning-dark factor, and exact stochastic quotient architecture survive this independent geometry.

No c1/c3 orientation result from the sigma_z model is assumed to transfer.

## Fresh fixtures

Use NumPy `default_rng(seed=2026082916)` to generate exactly 128 fresh physical fixtures.

Draw independently:

- `log10(gamma) ~ Uniform(log10(0.1),log10(2.0))`;
- `log10(kappa) ~ Uniform(log10(0.05),log10(2.0))`;
- `eta ~ Uniform(0.05,0.95)`;
- `omega ~ Uniform(0.1,3.0)`;
- Bloch radius `r ~ Uniform(0.05,0.85)`;
- isotropic Bloch direction from a normalized 3D Gaussian draw.

No fixture may be replaced because of any rank, quotient, or stability result.

## Frozen constructions

For every fixture independently construct from two-level Hilbert-space operators:

- physical tangent matrix `A_phys`;
- same-record tangent matrix `A_rec`;
- stochastic tangent matrix `B`;
- measurement functional `V^T`;
- conditioning bridge factorization `A_rec-A_phys = U V^T`.

The conditioning-dark space must be reconstructed from the physical pair `(A_phys,V^T)` only:

`D = ker([V^T; V^T A_phys; V^T A_phys^2])`.

No same-record outcome may be used to choose D.

## Registered structural hypothesis R45

For all 128 fresh X45 fixtures:

1. `dim(D)=1`;
2. `D` is invariant under `A_phys`, `A_rec`, and `B`;
3. the quotient dimension is exactly 2;
4. both deterministic and stochastic tangent dynamics descend exactly to that same quotient;
5. the quotient second-moment generator intertwines with the full second-moment generator.

A single fresh fixture violating any item falsifies universal R45 for this registered geometry.

## Frozen gates

- **R0 state/source validity:** all density matrices positive; A/B matrices real to `1e-11`.
- **R1 rank-one bridge:** direct `A_rec-A_phys` agrees with independently constructed `U V^T` to `5e-11`; bridge rank <=1.
- **R2 dark reconstruction:** exactly one-dimensional D on every fresh fixture, with `V^T D` and physical invariance residuals <=`5e-10`.
- **R3 stochastic compatibility:** `A_rec D subset D` and `B D subset D` residuals <=`5e-10`.
- **R4 quotient intertwining:** for an independently reconstructed orthonormal complement C and quotient map L=C^T, require `L A=A_q L` and `L B=B_q L` <=`5e-10` for both channels.
- **R5 second-moment closure:** `(L tensor L)K(A,B)=K(A_q,B_q)(L tensor L)` <=`5e-9` for both channels, where `K=I tensor A + A tensor I + B tensor B`.
- **R6 active-coordinate covariance:** fixed non-orthogonal 2x2 transform `R=[[1.2,0.3],[-0.2,0.9]]` preserves quotient characteristic polynomials and second-moment spectra to `5e-9`.
- **R7 refusal control:** replace X45 only in a fixed negative control by `X3=(sigma_x+sigma_y+sigma_z)/(2*sqrt(3))`. For fixed control parameters `gamma=0.3,kappa=0.2,eta=0.7,omega=1.1` and Bloch vector `(0.2,0.1,-0.3)`, the observability matrix must have rank 3 and the architecture must return `REFUSE_NO_1D_DARK_FACTOR`, not force a 2D quotient.

Overall status is `PASS_ROTATED_AXIS_STOCHASTIC_QUOTIENT` only if R0-R7 pass. A fresh structural violation is `FAIL_ROTATED_AXIS_ARCHITECTURE`; an audit/implementation inconsistency is separately preserved as `AUDIT_FAILURE`.

## Interpretation firewall

A PASS licenses transfer of the dark/active stochastic quotient architecture to this fixed 45-degree x-z measurement axis only. It does not transfer the sigma_z c1/c3 orientation asymmetry, does not license a stochastic scalar, and does not establish localization/collapse or measurement-quality behavior.

The generic 3D-axis refusal control is part of the scientific boundary: the framework must be able to say that the 2D quotient is unavailable.
