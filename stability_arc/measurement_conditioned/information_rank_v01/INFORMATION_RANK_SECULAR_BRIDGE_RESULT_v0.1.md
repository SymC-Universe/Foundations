# Information-rank secular bridge audit v0.1 result

**Status:** PASS
**Scope:** LOCAL COMPARATIVE STABILITY STRUCTURE ONLY
**Branch:** `agent/stability-arc-gfsa-v072`

## Canonical execution

- GitHub Actions run: `33245531943`
- execution commit: `3667e3a41f73e66552bd0c94cc8dfcfa61aff77e`
- job: `99082218514`
- preregistration SHA-256: `325aec4e9dbb5dfa012e3b3fdc61dabafd4320d40814ae6f1f0af710a21f309b`
- audit-code SHA-256: `9f53c96d01942e5d6870fd67be5320d71d64379fb5afb59fd51ddcc61568e81f`
- workflow SHA-256: `9088a3753104cd05e1794c40e415c5b281f3a76af1253d4cc25d6b6452fd26d4`
- bound moment-result SHA-256: `80774388c3a8e99fef26e07edc85b6e45ce4231b7c943b94cb9bbcdf54d5114c`
- Python: `3.12.14`
- NumPy: `2.1.3`

## Frozen gate results

- **I0 independent quantum conditioning reconstruction:** PASS. Maximum independent finite-difference reconstruction error `1.0115218218587074e-08`, far below the frozen drift gates; every fresh quantum fixture had `rank(DeltaA)=1` at the registered tolerance.
- **I1 global rank-one characteristic-polynomial identity:** PASS. Maximum residual `3.794299872214038e-15` versus gate `2e-10`, including evaluation at physical-generator eigenvalues using the cofactor adjugate form rather than a resolvent inverse.
- **I2 resolvent secular factor:** PASS. Maximum determinant-lemma residual `7.020296723414116e-16` versus gate `2e-10`; no frozen probe required near-pole refusal.
- **I3 information-rank bound:** PASS. The three fresh single-record quantum fixtures had conditioning-update rank 1; the `m=2` and `m=3` algebraic controls had ranks 2 and 3 respectively, satisfying `rank(DeltaA)<=m`.
- **I4 moment-update rank bounds:** PASS. For all three quantum fixtures, the full second-moment conditioning update had rank 5 and the symmetric-covariance update had rank 3, within the preregistered single-record bounds `<=5` and `<=3`. The `n=4,r=2` control had ranks `(12,7)` within bounds `(12,7)`; the `n=5,r=3` control had ranks `(21,12)` within bounds `(21,12)`.
- **I5 coordinate invariance:** PASS. Maximum secular-factor residual under the frozen common orthogonal coordinate change was `2.2215299868541707e-16` versus gate `2e-11`.
- **I6 interpretation/refusal firewall:** PASS. Physical and record generators remain `FULL_MATRIX_REQUIRED`; moment generators remain `FULL_MOMENT_OPERATOR_REQUIRED`; the new secular object is `COMPARATIVE_ONLY`.

Overall preregistered decision: **PASS**.

## Preserved evidence

- artifact ID: `9712708402`
- artifact ZIP SHA-256: `465e5bf237e202e3d04855b0dc4f512962c3778cf4ec57697f14c1bfe11365a7`
- artifact size: 3249 bytes
- retention expiry: 2026-11-27

Internal artifact SHA-256 values:

- `information_rank_secular_bridge_v01.json`: `8a07e8833ca67f7ca13aacd939e4cd5194de9d56afac2e84d794e119a12fdfb2`
- `stdout.txt`: `0c6f3ef036b404ba84170a16cd6be29796b125286ea44869d0d5d88e5497342b`
- `environment_lock.txt`: `922bda33668b532b1f38c3212a5f3cf7f0618296eaa35ef1388793e0c3cd5845`
- `source_identity.txt`: `bb7463a0fc5d91c690962c493c714031edc76c30fc1a155f474fb77130fd9456`
- `SHA256.txt`: `340f78c4fd3af4ad06397f2b9795d4fd066d8b69f6d791d6fa98a27144cc07a6`
- `MANIFEST_VERIFIED.txt`: `97ab902bc355d0ff075e54281786ff976a90e9a89b498d8fb438b1fcaeeb7428`

## Licensed theoretical result

For the registered local continuous-measurement tangent, each scalar measurement record contributes one outer-product drift correction. With `m` scalar records,

`DeltaA = U V^T = sum_j u_j v_j^T`,

so

`rank(DeltaA) <= m`.

Thus the same-record inference generator is a low-rank update of the same-noise physical generator:

`A_rec = A_phys + U V^T`.

Away from poles of the physical resolvent, their characteristic-polynomial ratio is governed by the `m x m` comparative secular determinant

`det(zI-A_rec)/det(zI-A_phys) = det(I_m - V^T (zI-A_phys)^(-1) U)`.

For one scalar measurement record this comparative bridge is a single scalar meromorphic factor, even though **neither full generator is licensed as a scalar object**. At physical poles the resolvent ratio is refused and the globally valid adjugate characteristic-polynomial identity remains available.

The closed second-moment result also implies that if `r=rank(DeltaA)`, the direct conditioning change obeys

`rank(DeltaK) <= 2 n r-r^2`

on full vectorized second moments and

`rank(DeltaK_sym) <= r(2 n-r+1)/2`

on symmetric covariances. For a single effective record (`r=1`) these reduce to `<=2n-1` and `<=n`.

## Scientific meaning

The physical and inference descriptions are not being averaged or conflated. Instead, the **information supplied by the measurement record enters the local stability problem through a rank-limited bridge whose dimension is bounded by the number of scalar record channels**. This gives a mathematically controlled conglomerate description: full physical dynamics, full inference dynamics, plus a low-dimensional comparative secular object that describes how measurement information can move the spectrum between them.

This is a structural result about local conditional dynamics. It is not evidence that localization is predicted, not evidence for chi=1, and not permission to choose a preferred mode or scalar using prior localization outcomes.

The fact that the registered rank bounds were saturated in all five executed controls is retained as an **observation only**. Equality was not preregistered as a universal claim and is not promoted here.
