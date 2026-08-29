# Active-quotient scalar admissibility audit v0.1

**Status:** FROZEN BEFORE EXECUTION

## Purpose

The closed conditioning-dark / active-sector audit established, without localization outcomes, that the registered three-dimensional continuously measured qubit tangent can possess an exact one-dimensional conditioning-dark invariant factor and a two-dimensional active quotient carrying all deterministic record-conditioning-induced characteristic change.

This audit asks a narrower question: **when that active quotient is independently identifiable and exactly two-dimensional, is the already-registered real 2x2 Stability Arc coordinate mathematically admissible on that quotient?**

This phase does not test localization, measurement accuracy, collapse, state-estimation performance, or chi=1 as an optimum. It reads no E16-E27 localization error, no historical localization score, and no GFSA v0.7 external-candidate response.

## Frozen scalar definition

For a real 2x2 quotient generator `A_A`, define the scalar only when all admissibility conditions below pass:

`chi_active(A_A) = -tr(A_A)/(2 sqrt(det(A_A)))`.

This is exactly the previously registered second-order coordinate because for

`A = [[0,1/m],[-m Omega^2,-Gamma]]`

one has `tr(A)=-Gamma`, `det(A)=Omega^2`, hence

`chi_active = Gamma/(2 Omega)`.

No scalar is computed for the full 3x3 physical or record-conditioned generator.

## Independently reconstructed dark factor and quotient

For each fresh quantum fixture reconstruct the maximal physical-invariant conditioning-dark subspace directly from

`D = ker(O)`,

where

`O = [V^T; V^T A_phys; ...; V^T A_phys^(n-1)]`.

Use SVD rank/nullity with frozen tolerance

`tol = max(1e-13, 1e-11*s_max)`.

Let `d=dim(D)` and `q=n-d`.

Construct an orthonormal complement `C` from the nullspace of `D^T` and `Q=[D,C]`. Because `D` is invariant, the transformed generator has block-upper-triangular form

`Q^T A Q = [[A_D, *],[0,A_A]]`

for the orthogonal basis. Construct the same quotient for `A_rec=A_phys+UV^T`.

The quotient is admitted to scalar analysis only if `q=2`, the dark factor is identifiable, and all gates below pass.

## Fresh quantum fixtures

Use three parameter/base-state controls not used in prior measurement-conditioned audits:

1. `AQ1: eta=0.66, gamma=0.24, kappa=0.14, omega=0.96, base=(0.18,-0.23,0.12)`
2. `AQ2: eta=0.74, gamma=0.39, kappa=0.18, omega=1.14, base=(-0.27,0.15,-0.21)`
3. `AQ3: eta=0.57, gamma=0.29, kappa=0.11, omega=0.79, base=(0.11,0.32,0.26)`

Use the already-closed local convention:

- `x=sigma_z/2`;
- `H=omega sigma_y/2`;
- amplitude damping `sqrt(gamma)`;
- unconditional measurement term `2 kappa D[x]`;
- `A_phys=[[-gamma/2-kappa,0,omega],[0,-gamma/2-kappa,0],[-omega,0,-gamma]]`;
- `h=(-rz*rx,-rz*ry,1-rz^2)`;
- `U=-4 eta kappa h` as a column;
- `V=(0,0,1/2)^T`;
- `A_rec=A_phys+UV^T`.

These are representation controls only.

## Frozen basis/complement transformations

For every admitted fresh quantum fixture, verify quotient invariance under both of these outcome-free changes:

1. **active basis change**
   `S1=[[1.2,0.25],[-0.15,0.85]]`;
2. **complement shear plus active basis change**
   for one-dimensional `D`, use `H=[[0.31,-0.22]]` and `S2=[[0.9,-0.28],[0.19,1.1]]`, constructing
   `C2 = D H + C S2` and the generally non-orthogonal full basis `T=[D,C2]`.

For a general invertible full basis `T`, extract the quotient from the lower-right block of `T^{-1} A T`.

Freeze a coordinate-condition refusal threshold `cond(T)>1e10` or non-finite condition number -> `REFUSE_COORDINATE_FAILURE`.

## Frozen canonical 2x2 inheritance controls

Use three fresh canonical oscillator blocks:

1. `(m,Omega,Gamma)=(1.7,0.9,0.8)`;
2. `(m,Omega,Gamma)=(0.6,1.4,2.1)`;
3. `(m,Omega,Gamma)=(2.2,0.55,1.3)`.

For each, require the scalar formula to recover `Gamma/(2 Omega)` to absolute error `<=1e-13`.

## Frozen refusal controls

The scalar policy must return the exact listed refusal status rather than a number.

### RQ1 quotient dimension

A real stable 4x4 control with exactly one independently reconstructed dark dimension and hence a 3D quotient -> `REFUSE_QUOTIENT_DIMENSION`.

### RQ2 unstable quotient

A 3x3 dark-plus-active control whose exact 2x2 active block has `tr>=0` -> `REFUSE_NOT_ASYMPTOTICALLY_STABLE`.

### RQ3 nonpositive determinant

A 3x3 dark-plus-active control whose exact 2x2 active block has `det<=0` -> `REFUSE_NONPOSITIVE_DETERMINANT`.

### RQ4 cross-sector degeneracy

A 3x3 control whose dark eigenvalue equals an active eigenvalue within the frozen separation tolerance `1e-8` -> `REFUSE_DEGENERATE_SECTOR_ATTRIBUTION`.

### RQ5 defective active sector

A 3x3 control with a 1D exact dark factor and active block `[[ -1,1],[0,-1]]` -> `REFUSE_DEFECTIVE_ACTIVE_SECTOR`.

### RQ6 coordinate failure

Apply an exactly singular active basis change `S_bad=[[1,1],[1,1]]` to an otherwise admissible control -> `REFUSE_COORDINATE_FAILURE`.

### RQ7 non-real 2x2 block policy

A direct 2x2 scalar-policy control with an imaginary entry of magnitude `1e-3` -> `REFUSE_NONREAL_QUOTIENT`.

## Frozen gates

### A0 dark reconstruction and quotient dimension

For every fresh quantum fixture:

- reconstructed dark dimension must equal 1;
- quotient dimension must equal 2;
- `max|V^T D| <=1e-11`;
- physical dark-invariance residual and record dark-preservation residual must each be `<=1e-10`.

### A1 real stable quotient admissibility

For both physical and record-conditioned active quotients of every fresh fixture:

- maximum imaginary entry magnitude `<=1e-12`;
- `tr(A_A)<0`;
- `det(A_A)>0`.

Otherwise the corresponding scalar is refused with the registered reason.

### A2 coordinate/complement invariance

For both channels and every fresh fixture, under the frozen active-basis and complement-shear transformations:

- trace agreement `<=5e-12`;
- determinant agreement `<=5e-12`;
- chi agreement `<=5e-12`.

The transformed full basis must satisfy the condition-number gate.

### A3 characteristic-factor consistency

For both channels and every fresh fixture, the quotient trace and determinant must agree with the degree-2 factor obtained by exact polynomial division of the full characteristic polynomial by the independently reconstructed one-dimensional dark factor.

Maximum coefficient residual and trace/determinant reconstruction residual must each be `<=2e-10`.

This gate prevents the scalar from depending only on a chosen complement representation.

### A4 canonical 2x2 inheritance

All three fresh canonical oscillator controls must recover `Gamma/(2 Omega)` with maximum absolute error `<=1e-13`.

### A5 separate-channel preservation

The audit must record separate values

`chi_active_phys`

and

`chi_active_rec`

for each admitted fresh fixture. No average, weighted combination, preferred channel, or closeness-to-one score is permitted.

PASS requires both channels to be admitted independently on every fresh fixture. Their numerical ordering is observation only.

### A6 refusal behavior

RQ1-RQ7 must return exactly their preregistered refusal labels. No fallback scalar is permitted.

### A7 full-generator and stochastic firewall

For every fresh quantum fixture the 3x3 physical and record-conditioned generators must return

`FULL_MATRIX_REQUIRED`

under the full-generator scalar policy.

The shared stochastic tangent matrix `B` and the `B tensor B` moment contribution remain outside `chi_active`. PASS requires the result to record

`STOCHASTIC_TERM_NOT_COMPRESSED`.

## Decision rule

Overall PASS requires `A0 & A1 & A2 & A3 & A4 & A5 & A6 & A7`.

Any failed gate remains failed. No fixture, tolerance, quotient rule, dark-factor construction, basis transform, refusal status, scalar definition, or interpretation may be changed inside v0.1 after execution. A scientific correction requires a separately frozen successor version with the v0.1 result preserved.

## Interpretation firewall

A PASS would license only this statement:

> When an independently reconstructed conditioning-dark factor leaves an identifiable, real, asymptotically stable two-dimensional deterministic active quotient, the coordinate `-tr/(2 sqrt(det))` is a basis-invariant Stability Arc coordinate on that quotient, separately for the physical and record-conditioned deterministic drifts.

A PASS would **not** establish:

- a scalar coordinate for the full 3x3 quantum generator;
- a scalar compression of multiplicative measurement noise;
- that physical and record-conditioned active coordinates should be averaged;
- that either channel is privileged;
- that chi=1 predicts localization, measurement quality, collapse, or an optimum;
- that any observed movement toward or away from 1 is evidentiary support.

Any prospective connection to localization requires a later separately preregistered untouched-outcome phase.
