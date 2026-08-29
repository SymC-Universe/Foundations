# Mean-square stability geometry of the stochastic active quotient v0.1 result

**Status:** PASS
**Scope:** MEAN_SQUARE_GEOMETRY_ONLY
**Canonical run:** `33256099802`
**Execution commit:** `f95c13d3974cdd18aca0bd4eb3b7e84800722988`

## Frozen source identities

- preregistration SHA-256: `b668ca34fd4a9b420a446c9eb8cb789a10449233e2a8e2d888fb852ae1483c46`
- audit-code SHA-256: `221f267f8ad3b6fe8326e7e75a1959e0e8e1347ce251cfae5f61c78abd94087e`
- workflow SHA-256: `9a5ae6641da5fb6d9a0e7ab9d93b0c725b04fb76bd46aba16f3928e37934afab`
- upstream stochastic-quotient result SHA-256: `abcf6a9caa3e5d80dc8f4b74fba2a1805b2ce25006198ba80c51b8df7e22d256`

## Preserved evidence

- artifact ID: `9715844649`
- artifact ZIP SHA-256: `1e45e2060675e0b126a78bdcc6d11af7047d91f178d952eaf3000dadbb2add4b`
- result JSON SHA-256: `9c334206d37515e0aa3cae63f7ddab85f0c88077a46cb98826baae892b8efbda`
- stdout SHA-256: `9c334206d37515e0aa3cae63f7ddab85f0c88077a46cb98826baae892b8efbda`
- environment-lock SHA-256: `922bda33668b532b1f38c3212a5f3cf7f0618296eaa35ef1388793e0c3cd5845`
- source-identity SHA-256: `18ac5fb3a79ba0ce62bb884bf2eace6b5b5fbae1320589a9f8a0c708177371e5`
- SHA256 manifest SHA-256: `1d23f1102dea4ec91bc8b437c8eeef63881ccbd4421f1ac63da431132c88dac3`

The workflow independently verified its file manifest before artifact upload.

## Frozen gate results

All M0-M6 gates passed.

- **M0 fresh-quotient admission: PASS.** All three new quantum fixtures independently reconstructed a one-dimensional conditioning-dark factor and exact 2D stochastic quotient for both physical and same-record channels. Maximum quotient intertwining error was `0.0`; minimum density-matrix eigenvalue was `0.32600287358694685`.
- **M1 symmetric lift identity: PASS.** The direct 3x3 symmetric second-moment generator agreed exactly at recorded precision with `E2 K(A,B) D2`; maximum error `0.0`.
- **M2 coordinate invariance: PASS.** Maximum characteristic-coefficient residual under the frozen non-orthogonal active-coordinate transformation was `5.684341886080802e-14`, below the frozen `5e-10` gate.
- **M3 classifier agreement: PASS.** Cubic Routh-Hurwitz classification and direct eigenvalue-sign classification agreed for every registered pair; zero mismatches.
- **M4 exact stability controls: PASS.** Exact stable, boundary, unstable, and nontrivial Hurwitz-plane boundary controls all returned their preregistered classes. The `lambda^3+lambda^2+lambda+1` control had Hurwitz margin component `c1*c2-c3=0` and was correctly classified `BOUNDARY`.
- **M5 oscillator distinction: PASS.** The frozen noiseless oscillator controls at formula metadata `chi=0.5`, `chi=1`, and `chi=1.5` were all mean-square `STABLE`. The undamped `Gamma=0`, `chi=0` control was `BOUNDARY`.
- **M6 covariance-coordinate closure: PASS.** Direct matrix covariance updates and the registered 3x3 coordinate generator agreed with maximum error `0.0`.

## Licensed mean-square representation

For an admitted exact 2D stochastic active quotient

`d q = A_A q dt + B_A q dW`,

the symmetric second moment

`P = E[q q^T]`

evolves under

`dP/dt = A_A P + P A_A^T + B_A P B_A^T`.

In coordinates

`m=(p11,p12,p22)^T`,

this defines a real 3x3 generator `G(A_A,B_A)`.

For

`det(lambda I-G)=lambda^3+c1 lambda^2+c2 lambda+c3`,

strict mean-square asymptotic stability is classified by

`c1>0`, `c2>0`, `c3>0`, and `c1*c2>c3`.

The characteristic triple `(c1,c2,c3)` is invariant under the registered active-coordinate changes and is therefore licensed as the current coordinate-free mean-square descriptor.

The required reporting state remains

`MEAN_SQUARE_INVARIANTS_REQUIRED`.

No stochastic scalar `chi` is licensed.

## Deterministic critical damping versus stochastic mean-square stability

The preregistered oscillator controls establish a clean separation of concepts in the noiseless second-order limit.

With `Omega=1.2`:

- `chi=0.5`: mean-square `STABLE`;
- `chi=1`: mean-square `STABLE`;
- `chi=1.5`: mean-square `STABLE`;
- `Gamma=0`, `chi=0`: mean-square `BOUNDARY`.

Therefore deterministic critical damping at `chi=1` is **not** the mean-square asymptotic-stability boundary of the noiseless oscillator. It remains a damping-morphology / repeated-root boundary. Mean-square stability answers a different question: whether second moments decay asymptotically.

This distinction is a scientific constraint, not a negative result to be repaired.

## Fresh quantum observations

All six fresh quantum quotient channels were mean-square `STABLE`.

Recorded spectral abscissae were:

- MSQ1 physical: `-0.6115501489104832`; same-record: `-0.825733469477126`;
- MSQ2 physical: `-0.48239868099333605`; same-record: `-0.6971170828334983`;
- MSQ3 physical: `-0.7048880735257141`; same-record: `-0.7992651572090776`.

The same-record channel was more negative in these three fresh fixtures. This pattern is **OBSERVATION_ONLY**. It was not preregistered as a directional hypothesis, so it is not promoted as evidence that measurement conditioning generally increases mean-square stability.

If investigated, that directionality must be frozen as a new hypothesis and tested on genuinely fresh fixtures, including adversarial cases capable of reversing it.

## Interpretation firewall

This PASS licenses the mean-square operator geometry and classifier only. It does not license:

- a stochastic analogue of `chi`;
- localization, collapse, or measurement-quality prediction;
- a general claim that conditioning stabilizes mean-square dynamics;
- averaging physical and same-record channels;
- treating `chi=1` as a stochastic stability boundary.

The physical and same-record channels remain separately auditable. Their joint relationship may be studied prospectively without erasing their identities.
