# Stochastic second-moment lift audit v0.1 result

**Status:** PASS
**Scope:** REPRESENTATION / SECOND-MOMENT CONSISTENCY ONLY
**Branch:** `agent/stability-arc-gfsa-v072`

## Frozen execution identity

- GitHub Actions run: `33234878303`
- execution commit: `68d1eb37df71b308add030e6bf9e7064b91faa3e`
- job: `99053983690`
- preregistration SHA-256: `7e452f7ce5ff7e01cfd396cb32de34c830a4fd76a7f8284ac0cecd9ed490b9d4`
- audit-code SHA-256: `2ae18238650b2f75d547df61c64780ba154b4a2a4e2acb5d44174eea82f7016d`
- workflow SHA-256: `466a04e54dbebfaca698b2f531100317fb473895592b3bff9df4fa204f519212`
- Python: `3.12.14`
- NumPy: `2.1.3`

## Frozen gate results

- **M0 vectorization convention:** PASS; maximum residual `0.0` versus gate `5e-13`.
- **M1 symmetric-subspace closure/projection:** PASS; maximum residual `2.220446049250313e-16` versus gate `5e-13`.
- **M2 independent covariance propagation:** PASS; maximum Richardson matrix/vector residual `1.0191847366058937e-12` versus gate `2e-9`; every registered fine-step raw error was no larger than its corresponding coarse-step error.
- **M3 comparative moment identity:** PASS; maximum residual `2.220446049250313e-16` versus gate `5e-13`.
- **M4 common-coordinate covariance:** PASS; induced symmetric-coordinate orthogonality residual `2.220446049250313e-16` and maximum similarity residual `6.661338147750939e-16` versus gate `5e-12`.
- **M5 joint identity preservation:** PASS; maximum residual `0.0` versus gate `5e-13`.
- **M6 scalar refusal and noiseless inheritance:** PASS; all full moment operators remain `FULL_MOMENT_OPERATOR_REQUIRED`; maximum noiseless 2x2 pairwise-sum inheritance mismatch `2.673771110915334e-15` versus gate `1e-10`.

Overall preregistered decision: **PASS**.

## Preserved artifact

- artifact ID: `9709601806`
- artifact ZIP SHA-256: `c95b21a8d54480b5e36443c278d5b90a0f6e631d6bcd3df29db7237179484bed`
- artifact size: 2902 bytes
- retention expiry: 2026-11-27

Internal evidence SHA-256 values from the uploaded artifact:

- `stochastic_moment_lift_audit_v01.json`: `0caf92f2ab9d7667b472124340176d30cf500f5c41e083ae2a1e7113496c2316`
- `stdout.txt`: `98c34cd6c68e690bd190fcd35fd584dd141d779949d75427ee91bed180ae3bc2`
- `environment_lock.txt`: `922bda33668b532b1f38c3212a5f3cf7f0618296eaa35ef1388793e0c3cd5845`
- `source_identity.txt`: `e3a0af1802bd9116673d0e031149e929597f80fd074497781ae526b314a17526`
- `SHA256.txt`: `65fd83879f596966ab84c2bc30294ffbf2907006f0b45b4ad692169e8928cab1`
- `MANIFEST_VERIFIED.txt`: `7622812aa6a349f82e71819801742ed1220c6865f794fba6af1b3e642320fcdb`

## Licensed representation

For each channel, the local multiplicative-noise tangent

`d r = A r dt + B r dW`

has a mathematically consistent second-moment lift

`dP/dt = A P + P A^T + B P B^T`

with column-major vectorized generator

`K(A,B) = I tensor A + A tensor I + B tensor B`.

The licensed joint moment representation remains

`M = (K_phys_sym, K_rec_sym, DeltaK_sym, K_joint_sym)`

with physical and record-conditioned channels separately recoverable.

## Interpretation firewall

This PASS establishes consistency of the stochastic second-moment lift with the already-closed local tangent representation. It does **not** establish that any moment eigenvalue predicts localization, that a preferred spectral statistic exists, that a scalar chi exists for the lift, or that chi=1 is optimal under measurement.

No localization outcome or GFSA external-candidate value was used in selecting this representation, fixtures, timesteps, sigma-point rule, gates, or scalar-refusal policy.
