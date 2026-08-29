# Secular-continuation / mode-correspondence audit v0.1 result

**Status:** PASS_WITH_ALL_FRESH_PATHS_ADMISSIBLE
**Scope:** outcome-free comparative spectral representation only
**Canonical run:** `33248271329`
**Execution commit:** `529924eee7e41115084695f3d7d748ce44a6806b`

## Frozen source identities

- preregistration SHA-256: `d8c5a3c650106809724908013c59d1e1f058dd649a1a7285df276efb8a403992`
- audit-code SHA-256: `f595c52ce977f13022b64b8b7e2ec91086adac70c1160eee0f2c4f325a6f95ed`
- workflow SHA-256: `9126787423830083dc65af87ce0ac51ee91d209255dbfdecbbb85bbcf7525330`
- bound information-rank result SHA-256: `184b9b2192a691872815f3a38d366c1a4dc6e16812fd4b2584287b347ecfc1f8`

## Preserved execution evidence

Artifact ID: `9713536443`

Artifact ZIP SHA-256:
`a40752981daa19f768c4216effff311c07671fb8bf494d20957a958208644581`

Result JSON SHA-256:
`63b660aa9a75d1c649284d1260f155a19354875743f5217762a983aaf1c514c1`

Other internal evidence hashes:

- environment lock: `922bda33668b532b1f38c3212a5f3cf7f0618296eaa35ef1388793e0c3cd5845`
- source identity: `b25a2d98a0aafa403f15d45a0ab9942519b3c06b96743e12c713a420f924e63c`
- stdout: `8e05ee805b5e8a9db6d5d7f7594b9f9066a5c5e62be17199a4bef5307c9961ac`

Runner environment used Python 3.12 and pinned NumPy 2.1.3.

## Frozen gate results

- **S0 path construction / low-rank identity: PASS.** Maximum identity residual `1.0842021724855044e-16`; maximum fresh update rank `1`.
- **S1 spectral admissibility / projector algebra: PASS.** Maximum projector residual `2.2399083160561363e-16`.
- **S2 continuation correspondence: PASS.** All three fresh quantum paths were admissible from `t=0` through `t=1`; no fresh refusal occurred; endpoint recovery residual `0.0`.
- **S3 secular-root consistency / pole refusal: PASS.** Maximum admissible secular-root residual `7.203195710628172e-14`; all 18 exact physical-pole probes correctly returned `REFUSE_NEAR_PHYSICAL_POLE`.
- **S4 mandatory refusal controls: PASS.** N1 refused the initial degeneracy at `t=0`; N2 refused the conjugate-pair collision exactly at `t=0.5`; neither was relabeled through the singular point.
- **S5 common-coordinate invariance: PASS.** Maximum branch-representative residual `1.4228624520802642e-15`; maximum projector covariance residual `4.458529307625244e-16`.
- **S6 interpretation firewall: PASS.** `PHYSICAL_GENERATOR=FULL_MATRIX_REQUIRED`, `RECORD_GENERATOR=FULL_MATRIX_REQUIRED`, `MODE_OBJECT=INVARIANT_CLUSTER_OR_REFUSE`, `SECULAR_OBJECT=COMPARATIVE_ONLY`, `SCALAR_CHI=NOT_LICENSED`.

## Descriptive fresh-path geometry

The registered branch summaries were not used to tune the audit and carry no localization interpretation.

For each of the three fresh quantum fixtures, one real singleton branch had exactly zero endpoint displacement in the stored result. The conjugate-pair branch changed as follows:

- S1: real-part displacement `-0.08792784000000015`; oscillation-magnitude displacement `+0.0011617051306200832`.
- S2: real-part displacement `-0.13855968000000002`; oscillation-magnitude displacement `-0.013225067905431764`.
- S3: real-part displacement `-0.06618384`; oscillation-magnitude displacement `-0.004890429604078039`.

No sign pattern is promoted from these three controls.

## Exact corollary exposed by the continuation result

The unchanged singleton in all three fresh fixtures prompted an algebraic check against the already-closed identity

`A_rec = A_phys + U V^T`.

The following is an exact mathematical corollary of that identity and does not use the three observed paths as prospective evidence:

If `W` is an `A_phys`-invariant subspace and `W subset ker(V^T)`, then for every `w in W`,

`A_rec w = A_phys w`.

Therefore the restriction of the physical and record-conditioned generators to `W` is identical. In particular, if `x` is a physical right eigenvector with

`A_phys x = lambda x`

and

`V^T x = 0`,

then

`A_rec x = lambda x`.

Such a mode is **conditioning-dark** with respect to the record-update drift: it is a common physical/inference eigenmode with the same eigenvalue. Dually, a physical left eigenvector `y^T` satisfying `y^T U=0` is also unchanged as a left mode.

For the registered single-observable qubit convention, the measurement functional acts only on the `z` tangent coordinate, while the unconditional physical generator has an exact `y`-axis eigenmode. That explains the zero-displacement singleton observed in S1-S3 without promoting the observation itself into evidence.

There is also an immediate second-moment corollary: if `w1,w2 in ker(V^T)`, then the conditioning-difference moment operator

`DeltaK = I tensor DeltaA + DeltaA tensor I`

annihilates `w1 tensor w2`. Thus the symmetric second-moment sector generated entirely inside a conditioning-dark subspace is also untouched by the conditioning **difference** term. This does not mean the shared stochastic term `B tensor B` vanishes, and it does not imply localization immunity.

## Scientific interpretation

This audit closes a conservative spectral-correspondence layer between the same-noise and same-record generators. It shows that, when the spectrum is identifiable under fixed rules, conjugate-pair/invariant-subspace branches can be tracked through the low-rank information bridge without hand matching; when a degeneracy or collision is encountered, the machinery refuses rather than inventing continuity.

The exact conditioning-dark corollary sharpens the bridge further: measurement information can only directly alter tangent directions visible to `V^T`, and any physical invariant subspace fully contained in that nullspace is spectrally protected from the record-conditioning drift update.

This remains a local generator statement. It does not establish a localization predictor, a preferred mode, a scalar chi, or a chi=1 optimum.

## Next justified frontier

Freeze a fresh outcome-free **conditioning-dark / active-sector factorization audit**. It should test the exact common-spectrum consequence on new quantum and synthetic controls, distinguish instantaneous nullspace annihilation from genuinely invariant dark subspaces, verify common characteristic factors without dividing at poles, and determine whether the comparative secular problem can be reduced to the measurement-visible invariant sector without losing any moved eigenvalues.
