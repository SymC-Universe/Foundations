# Mean-square stability geometry of the stochastic active quotient v0.1

**Status:** FROZEN BEFORE EXECUTION

## Purpose

The upstream stochastic dark/active audit established, on fresh controls, an exact two-dimensional quotient SDE

`d q = A_A q dt + B_A q dW`

while explicitly refusing to compress `(A_A,B_A)` to a scalar.

This phase asks the next outcome-free question: what coordinate-invariant object governs **mean-square stability** of that exact 2D stochastic quotient?

This audit is mathematical/reproducibility work only. It may not read historical localization errors, measurement-quality outcomes, GFSA external-candidate response values, or any prior outcome to choose coefficients, margins, fixtures, pairings, or preferred channels.

## Fixed second-moment representation

For real 2x2 matrices `A` and `B`, define symmetric second moment

`P = E[q q^T] = [[p11,p12],[p12,p22]]`.

Ito evolution is

`dP/dt = A P + P A^T + B P B^T`.

Use fixed coordinate vector

`m = (p11,p12,p22)^T`.

The induced real 3x3 generator `G(A,B)` is defined by

`dm/dt = G m`.

Independently, with column-major vectorization,

`K(A,B) = I tensor A + A tensor I + B tensor B`.

Use fixed duplication and symmetric-elimination maps

`D2 m = vec(P) = (p11,p12,p12,p22)^T`

and

`E2 vec(P) = (p11,(p12+p21)/2,p22)^T`.

The audit must verify

`G = E2 K D2`

against an independently reconstructed direct symmetric-basis action.

## Coordinate invariants

For

`det(lambda I - G) = lambda^3 + c1 lambda^2 + c2 lambda + c3`,

`(c1,c2,c3)` are the registered coordinate-invariant mean-square descriptors.

No scalar compression is licensed in v0.1.

Under any registered invertible active-coordinate change `q = R q'`, use

`A' = R^-1 A R`, `B' = R^-1 B R`.

PASS requires the characteristic coefficients of `G(A',B')` to agree with those of `G(A,B)` within the frozen numerical tolerance.

## Cubic Routh-Hurwitz classifier

For a real cubic

`lambda^3 + c1 lambda^2 + c2 lambda + c3`,

strict mean-square asymptotic stability is classified by

`c1 > 0`,
`c2 > 0`,
`c3 > 0`,
`c1*c2 > c3`.

Define Hurwitz margin vector

`h = (c1,c2,c3,c1*c2-c3)`.

With `RH_TOL = 1e-10`:

- `STABLE` if every component of `h` is greater than `RH_TOL`;
- `BOUNDARY` if no component is below `-RH_TOL` and at least one component has absolute value `<= RH_TOL`;
- `UNSTABLE` otherwise.

The direct spectral classifier is:

- `STABLE` if `max Re eig(G) < -RH_TOL`;
- `BOUNDARY` if `|max Re eig(G)| <= RH_TOL`;
- `UNSTABLE` if `max Re eig(G) > RH_TOL`.

The two classifiers must agree for every admitted registered control.

## Frozen fresh quantum fixtures

These fixtures are new to this phase and were not selected from localization outcomes.

- `MSQ1`: `eta=0.61`, `gamma=0.31`, `kappa=0.19`, `omega=1.07`, base Bloch vector `(0.11,-0.19,0.27)`.
- `MSQ2`: `eta=0.79`, `gamma=0.24`, `kappa=0.14`, `omega=0.88`, base Bloch vector `(-0.18,0.21,-0.16)`.
- `MSQ3`: `eta=0.55`, `gamma=0.42`, `kappa=0.09`, `omega=1.31`, base Bloch vector `(0.26,0.05,-0.22)`.

For each fixture reconstruct independently:

1. physical tangent drift `A_phys`;
2. same-record drift `A_rec`;
3. multiplicative tangent matrix `B`;
4. measurement functional `V^T`;
5. maximal deterministic conditioning-dark space from `[V^T;V^T A;V^T A^2]`;
6. the active quotient only if that dark space is one-dimensional, is invariant under both `A_phys` and `B`, and gives a 2D quotient.

The physical and record-conditioned channels remain separately recorded. Their invariant triples may be compared, but may not be averaged or collapsed.

## Frozen synthetic stability controls

### Exact isotropic stochastic controls

Use `A=-a I2`, `B=b I2`.

- `ISO_STABLE`: `a=1`, `b=1`, expected `STABLE` because every second-moment rate is `-2a+b^2=-1`.
- `ISO_BOUNDARY`: `a=0.5`, `b=1`, expected `BOUNDARY` because every second-moment rate is exactly `0`.
- `ISO_UNSTABLE`: `a=0.4`, `b=1`, expected `UNSTABLE` because every second-moment rate is `0.2`.

### Routh-Hurwitz plane boundary classifier control

Use the real 3x3 control generator

`G_RH = diag(-1, J)` with `J=[[0,-1],[1,0]]`.

Its polynomial is exactly

`lambda^3 + lambda^2 + lambda + 1`,

so `c1*c2-c3=0`. It must classify `BOUNDARY` by both the coefficient and spectral rules. This control tests the nontrivial Hurwitz-plane equality separately from the zero-generator boundary.

## Frozen noiseless oscillator controls

Use

`A = [[0,1/m],[-m Omega^2,-Gamma]]`, `B=0`,

with fixed `m=1.7`, `Omega=1.2` and:

- `OSC_UNDER`: `Gamma=1.2`, formula metadata `chi=Gamma/(2 Omega)=0.5`;
- `OSC_CRITICAL`: `Gamma=2.4`, formula metadata `chi=1`;
- `OSC_OVER`: `Gamma=3.6`, formula metadata `chi=1.5`;
- `OSC_NEUTRAL`: `Gamma=0`, formula metadata `chi=0`.

Expected mean-square classifications:

- under: `STABLE`;
- critical: `STABLE`;
- over: `STABLE`;
- neutral: `BOUNDARY`.

Thus v0.1 explicitly does **not** assume that deterministic critical damping at `chi=1` is a mean-square stability boundary. The audit must preserve whichever result the frozen mathematics returns.

`chi` in these oscillator controls is analytic metadata only and is not a stochastic scalar coordinate.

## Fixed coordinate transformation

For every admitted stochastic quotient use

`R = [[1.18,0.27],[-0.16,0.91]]`.

PASS requires transformed and original characteristic coefficients to agree within `COORD_TOL=5e-10`.

## Fixed covariance controls

Use symmetric positive-definite initial moments

`P1=[[0.63,0.11],[0.11,0.41]]`

and

`P2=[[0.48,-0.07],[-0.07,0.72]]`.

With `DT=0.002`, compare a direct one-step matrix update

`P + DT*(A P + P A^T + B P B^T)`

against the registered coordinate update

`m + DT*G m`.

PASS requires maximum coordinate disagreement `<=5e-12`.

## Frozen gates

- **M0 fresh-quotient admission:** each quantum fixture has a physical density matrix with minimum eigenvalue `>0`, a one-dimensional independently reconstructed dark factor, 2D quotient, `A` and `B` dark-invariance residuals `<=5e-10`, and quotient intertwining residuals `<=5e-10` for both physical and record channels.
- **M1 symmetric lift identity:** direct symmetric-basis `G` agrees with `E2 K D2` to `<=5e-12` for every admitted pair.
- **M2 coordinate invariance:** characteristic coefficient residual under the frozen active-coordinate change is `<=5e-10`.
- **M3 classifier agreement:** cubic Routh-Hurwitz and direct eigenvalue-sign classifications agree for every admitted quantum channel, isotropic control, and oscillator control.
- **M4 exact stability controls:** `ISO_STABLE`, `ISO_BOUNDARY`, `ISO_UNSTABLE`, and `G_RH` return their frozen expected classes.
- **M5 oscillator distinction:** `OSC_UNDER`, `OSC_CRITICAL`, and `OSC_OVER` are all mean-square `STABLE`, while `OSC_NEUTRAL` is `BOUNDARY`. Any disagreement remains a failed scientific/mathematical gate.
- **M6 covariance-coordinate closure:** direct matrix and `G`-coordinate one-step covariance updates agree to `<=5e-12` for both fixed initial moments and every admitted `(A,B)` pair.

Overall PASS requires `M0 & M1 & M2 & M3 & M4 & M5 & M6`.

## Failure and refusal rules

A quantum fixture that does not reproduce the required stochastic 2D quotient is not silently replaced. Record the exact failed condition and classify the phase under the failure-signal protocol.

No tolerance, fixture, coefficient, transformation, expected control class, or channel may be changed inside v0.1 after outcome exposure. A scientifically motivated successor requires a new version and preserved v0.1 outcome.

## Interpretation firewall

A PASS would license only:

1. the real 3x3 symmetric second-moment generator as the correct local mean-square stability operator for admitted 2D stochastic active quotients;
2. `(c1,c2,c3)` and the cubic Hurwitz conditions as coordinate-invariant descriptors/classifier;
3. the distinction between deterministic damping morphology and mean-square stochastic stability on the frozen controls.

A PASS does **not** license:

- a stochastic scalar `chi`;
- localization, collapse, or measurement-quality prediction;
- averaging physical and same-record channels;
- treating `chi=1` as a stochastic stability boundary;
- selection of a preferred channel from prior outcomes.

Until a separate independent derivation justifies otherwise, every admitted stochastic quotient must report:

`MEAN_SQUARE_INVARIANTS_REQUIRED`.
