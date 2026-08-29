# Prospective conditioning mean-square directionality audit v0.1

**Status:** FROZEN BEFORE EXECUTION
**Hypothesis lineage:** POST-HOC OBSERVATION -> NEW PROSPECTIVE TEST

## Why this phase exists

The prior mean-square geometry phase used three fresh quantum fixtures and found, as an unregistered observation only, that the same-record channel had a more negative mean-square spectral abscissa than the physical same-noise channel in all three cases.

Those three cases are **not** evidence for a directional claim because the direction was not preregistered.

This phase freezes that observation into a new falsifiable hypothesis and tests it only on genuinely fresh fixtures generated from a fixed seed and parameter ranges defined before execution.

No historical localization, collapse, measurement-quality, GFSA external-candidate, or prior spectral outcome may be used to select or replace fixtures.

## Registered channel objects

For every fresh quantum fixture reconstruct separately:

- physical tangent pair `(A_phys,B)`;
- same-record tangent pair `(A_rec,B)`;
- exact one-dimensional conditioning-dark factor from the physical drift and measurement functional;
- exact 2D stochastic active quotient `(A_A_phys,B_A)` and `(A_A_rec,B_A)` if admissible;
- real 3x3 symmetric second-moment generators `G_phys` and `G_rec`;
- coordinate-invariant cubic coefficient triples `(c1,c2,c3)`;
- spectral abscissae `alpha_phys=max Re eig(G_phys)` and `alpha_rec=max Re eig(G_rec)`.

The two channels remain separately auditable. The comparison does not average or collapse them.

## Prospective hypothesis H1

**H1:** for every admitted fresh quantum fixture in this registered sample,

`alpha_rec <= alpha_phys + 1e-10`.

Equivalently, same-record conditioning does not worsen the local mean-square spectral abscissa on any registered fresh fixture.

This is deliberately stringent. A single admitted fixture with

`alpha_rec > alpha_phys + 1e-10`

makes H1 `FAIL_PROSPECTIVE`.

No fractional-success rescue, majority vote, threshold relaxation, fixture deletion, or reinterpretation is permitted inside v0.1.

A failure is scientifically informative and must be investigated for the parameter/structural conditions under which conditioning worsens mean-square stability.

## Fresh fixture generator

Use exactly NumPy `default_rng(seed=2026082901)`.

Generate exactly 24 accepted fixtures in order.

For each candidate draw independently:

- `eta ~ Uniform(0.25,0.90)`;
- `gamma ~ Uniform(0.12,0.60)`;
- `kappa ~ Uniform(0.04,0.35)`;
- `omega ~ Uniform(0.55,1.60)`;
- Bloch components `x,y,z ~ Uniform(-0.40,0.40)`.

Accept the candidate only if Bloch norm `<0.70`; otherwise redraw the Bloch vector only while retaining the already-drawn dynamical parameters.

Fixture IDs are `CD01` through `CD24` in acceptance order.

No fixture may be replaced after execution because it gives an inconvenient result.

## Quotient admission rule

For each fixture, reconstruct the deterministic dark space from

`O=[V^T;V^T A_phys;V^T A_phys^2]`.

An admitted fixture requires:

- positive base density matrix;
- exactly one-dimensional dark space;
- exactly two-dimensional quotient;
- `V^T D` residual `<=5e-10`;
- physical-drift, record-drift, and stochastic `B` invariance residuals `<=5e-10`;
- quotient intertwining residuals for both channels `<=5e-10`.

If a fixture fails admission, preserve it as `REFUSE_QUOTIENT` and H1 is not evaluated on that fixture. However, the phase receives `QUOTIENT_ADMISSION_HOLD` if fewer than 20 of 24 fixtures are admitted. No refused fixture may be replaced.

## Mean-square representation

Use the already-frozen symmetric second-moment construction

`dP/dt = A P + P A^T + B P B^T`

and `m=(p11,p12,p22)^T`.

For each admitted channel compute `G` independently by direct symmetric-basis action and verify it against `E2 K(A,B) D2` to `<=5e-12`.

The cubic Routh-Hurwitz classifier must agree with direct eigenvalue-sign classification for every admitted channel using the previously frozen `1e-10` tolerance.

No stochastic scalar chi is introduced.

## Conditioning bridge checks

Because the same-record drift differs from the physical drift by a rank-one deterministic correction on the admitted active quotient, define

`DeltaA = A_A_rec - A_A_phys`

and

`DeltaG = G_rec - G_phys`.

For every admitted fixture verify:

- `rank(DeltaA) <= 1` using singular-value tolerance `1e-10`;
- `rank(DeltaG) <= 2` using the same tolerance;
- `DeltaG` agrees to `<=5e-12` with the symmetric second-moment lift of `DeltaA` with zero stochastic increment, because `B_A` is common to both channels.

These are structural checks, not directional evidence.

## Adversarial comparator controls

The analysis pipeline must demonstrate that it can report either direction.

Use base pair

`A0=[[-0.3,1],[-1,-0.3]]`, `B0=0.2 I2`.

### CTRL_STABILIZE

Use rank-one update

`DeltaA=[[-0.4,0],[0,0]]`.

Expected comparator result:

`alpha_updated < alpha_base`.

### CTRL_DESTABILIZE

Use rank-one update

`DeltaA=[[0.8,0],[0,0]]`.

Expected comparator result:

`alpha_updated > alpha_base`, with the updated mean-square generator unstable.

These controls prove the comparator is capable of detecting both stabilizing and destabilizing rank-one updates. They do not enter H1.

## Frozen gates

- **D0 generator determinism:** rerunning the fixed seed generator in-process yields byte-equivalent numeric fixture arrays and exactly 24 accepted fixtures.
- **D1 quotient admission:** at least 20 of 24 fresh fixtures are admitted without replacement; every refusal is preserved.
- **D2 mean-square reconstruction:** direct and Kronecker/symmetric lift generators agree to `<=5e-12`; Routh-Hurwitz and spectral classes agree for every admitted channel.
- **D3 low-rank conditioning bridge:** every admitted fixture has `rank(DeltaA)<=1`, `rank(DeltaG)<=2`, and mean-square lift residual `<=5e-12`.
- **D4 adversarial comparator:** CTRL_STABILIZE reports a negative spectral-abscissa displacement and CTRL_DESTABILIZE reports a positive displacement and unstable updated class.
- **D5 prospective H1:** PASS only if every admitted fresh fixture satisfies `alpha_rec <= alpha_phys + 1e-10`; otherwise `FAIL_PROSPECTIVE`.

Overall phase status is:

- `PASS_PROSPECTIVE_H1` if D0-D5 pass;
- `FAIL_PROSPECTIVE_H1` if D0-D4 pass but D5 fails;
- `QUOTIENT_ADMISSION_HOLD` if D1 fails;
- `AUDIT_FAILURE` for any other failed gate.

## Interpretation firewall

A H1 PASS would support only the bounded claim that same-record conditioning did not worsen mean-square spectral abscissa on this fresh registered sample from this model family.

It would not establish a universal theorem, localization/collapse improvement, measurement quality, or a stochastic chi.

A H1 FAIL is not a nuisance result. It would identify fresh parameter conditions where conditioning worsens mean-square stability and would become the next failure-signal investigation target.
