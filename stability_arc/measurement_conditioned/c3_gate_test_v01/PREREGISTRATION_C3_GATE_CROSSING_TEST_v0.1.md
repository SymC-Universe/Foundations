# Prospective c3-gate class-crossing test v0.1

**Status:** FROZEN BEFORE EXECUTION
**Hypothesis:** H5
**Scope:** FRESH_MECHANISM_TEST

## Lineage

H4 prospectively established that robust physical mean-square STABLE -> same-record UNSTABLE crossings exist in a frozen high-kappa/high-omega measured-qubit target region. H4 found 50 independently reconstructed crossings in 100000 fresh inputs.

Only after H4 closed was it observed that all 50 record endpoints had `c3<0` while `c1>0`, `c2>0`, and `c1*c2-c3>0`. That 50/50 pattern remains post-outcome relative to H4.

The subsequent outcome-free c3 derivation phase independently established the exact physical and same-record `c3=0` surfaces from the model equations and passed its frozen B0-B5 audit. It did not establish that `c3` is the exclusive Routh-Hurwitz gate associated with fresh class crossings.

H5 tests that learned mechanism on a new seed. No H4 candidate may enter H5.

## Registered H5 statement

Within a fresh realization of the already-frozen H4 target-region generator, robust physical mean-square STABLE -> same-record UNSTABLE crossings will be **c3-gate crossings at the record endpoint**:

`c1_rec > 0`,
`c2_rec > 0`,
`c3_rec < 0`,
`h_rec = c1_rec*c2_rec-c3_rec > 0`.

The hypothesis concerns the fresh crossing population in this target family only. It does not state that `c3` is always the first or only failure gate in every measured-qubit regime.

## Fresh generator

Use exactly NumPy `default_rng(seed=2026082907)`.

Generate exactly `100000` candidate inputs `C5000001...C5100000` using the **unchanged H4 target-region distribution**:

- `gamma=1`;
- `log10(kappa/gamma) ~ Uniform(log10(3),log10(100))`;
- `log10(omega/gamma) ~ Uniform(log10(3),log10(100))`;
- `eta ~ Uniform(0.05,0.25)`;
- `sign_z` uniformly from `{-1,+1}`;
- `|z| ~ Uniform(0.90,0.999)`;
- `f_x ~ Uniform(0.20,0.99)`;
- `z=sign_z*|z|`;
- `x=-sign_z*f_x*sqrt(1-z^2)`;
- `y=0`.

No candidate may be replaced because of an outcome.

## Model and mean-square invariants

Let `q=eta*kappa` and

`A_phys=[[-(gamma/2+kappa),omega],[-omega,-gamma]]`,

`B=[[-sqrt(2q) z,-sqrt(2q) x],[0,-2 sqrt(2q) z]]`,

`DeltaA=[[0,2qzx],[0,-2q(1-z^2)]]`,

`A_rec=A_phys+DeltaA`.

For each channel form the real 3x3 symmetric second-moment generator `G` from

`dP/dt=A P+P A^T+B P B^T`.

Define

`det(lambda I-G)=lambda^3+c1 lambda^2+c2 lambda+c3`,

`h=c1*c2-c3`,

and spectral abscissa `alpha=max Re eig(G)`.

Use scale

`R=gamma+kappa+omega+eta*kappa`.

Normalized margins are

`m1=c1/R`,
`m2=c2/R^2`,
`m3=c3/R^3`,
`mh=h/R^3`.

Frozen numerical ambiguity tolerance for the mechanism margins is `1e-9`.

## Two-stage freeze-before-view

### Stage A: physical channel only

Generate all 100000 input bytes and hash them.

Construct only `A_phys`, `B`, and `G_phys`. Do not construct `DeltaA`, `A_rec`, `G_rec`, or same-record c3 values during Stage A.

A candidate enters the immutable Stage-A set iff

`alpha_phys/R < -1e-6`.

Before Stage B, write and SHA-256 hash:

- all generator inputs;
- every Stage-A eligible ID;
- its normalized physical spectral abscissa;
- the exact Stage-A selection bytes.

Require at least 10000 Stage-A eligible cases or return `SELECTION_HOLD`.

### Stage B: same-record reveal

Only after Stage-A bytes and digest are frozen may `DeltaA` and the record channel be constructed for the immutable eligible IDs.

A robust analytic crossing is any frozen Stage-A case with

`alpha_rec/R > +1e-6`.

Every analytic crossing must be retained. None may be replaced or excluded because its Routh-Hurwitz pattern is inconvenient.

For every crossing record `m1_rec,m2_rec,m3_rec,mh_rec` and the exact c3 formula value from the closed c3 derivation.

## Independent full-Hilbert reconstruction

Every analytic crossing must be independently reconstructed from the two-level Hilbert-space model used by H4:

- measured operator `sigma_z/2`;
- Hamiltonian `omega sigma_y/2`;
- amplitude damping `sqrt(gamma)`;
- unconditional measurement backaction `2 kappa D[x]`;
- same-noise tangent amplitude `sqrt(2 eta kappa)`;
- same-record deterministic conditioning correction.

Require:

- positive density matrix;
- one-dimensional conditioning-dark factor and two-dimensional active quotient;
- dark/invariance/intertwining and analytic-matrix residuals `<=5e-9`;
- direct symmetric moment lift versus Kronecker/duplication lift `<=5e-11`;
- independently reconstructed physical `alpha/R<-1e-6`;
- independently reconstructed record `alpha/R>+1e-6`;
- independently reconstructed normalized Routh-Hurwitz margins agree with analytic values to absolute tolerance `5e-9`.

If any analytic crossing fails reconstruction, return `RECONSTRUCTION_HOLD`. Crossings may not be silently dropped.

## Exact c3 cross-check

For every analytic crossing independently evaluate the frozen exact same-record quadratic

`c3_r(w)=A_r3*w^2+B_r3*w+C_r3`

with

`A_r3=2*(3g+2k+4q-2q*x^2-14q*z^2)`,

`B_r3=4q*x*z*(7g+6k+8q-30q*z^2)`,

`C_r3=(g+2k-2q*z^2)*(g+2q-6q*z^2)*(3g+2k+4q-12q*z^2)`.

Require relative-or-absolute agreement with `c3=-det(G_rec)` to `2e-10`.

## Controls

- `eta=0` identity control: physical and record channels must be identical.
- synthetic `c3`-only unstable cubic control with eigenvalues `{-1,-2,+0.5}` must be classified as `c1>0,c2>0,c3<0,h>0`.
- synthetic multi-gate unstable cubic control with eigenvalues `{-1,-2,+1}` must **not** be classified as c3-gate-exclusive.
- boundary control with eigenvalues `{-1,-2,0}` must return `c3=0` within `1e-12` and may not be counted as an H5 crossing.

## Frozen gates and decision rule

- **Y0 input determinism:** all 100000 candidate bytes reproduce exactly in-process.
- **Y1 Stage-A freeze:** at least 10000 robust physical STABLE cases; selection bytes and digest frozen before record construction.
- **Y2 record reveal integrity:** Stage B evaluates exactly the immutable Stage-A IDs.
- **Y3 reconstruction:** every analytic robust crossing independently reconstructs.
- **Y4 exact c3 identity:** every crossing passes the frozen quadratic-versus-determinant check.
- **Y5 mechanism pattern:** every independently reconstructed robust crossing has `m1_rec>1e-9`, `m2_rec>1e-9`, `m3_rec<-1e-9`, and `mh_rec>1e-9`.
- **Y6 controls:** all frozen controls classify correctly.

A minimum of `20` independently reconstructed robust crossings is required to promote the population-level mechanism statement in this target family. This minimum is frozen before H5 execution.

Overall status:

- `PASS_PROSPECTIVE_C3_GATE_H5` if Y0-Y6 pass and at least 20 robust crossings are reconstructed;
- `FAIL_C3_GATE_H5` if any independently reconstructed robust crossing violates Y5;
- `INSUFFICIENT_CROSSINGS_H5` if Y0-Y6 otherwise pass but fewer than 20 robust crossings occur;
- `RECONSTRUCTION_HOLD` if Y3 fails;
- `SELECTION_HOLD` if Y1 fails;
- `AUDIT_FAILURE` for other gate failures.

## Interpretation firewall

A PASS would prospectively support c3-gate-exclusive record endpoints for robust class crossings in this frozen target region. It would not prove that c3 is the universal mean-square failure gate, would not license a stochastic scalar chi, and would not connect this mechanism to localization, collapse, or measurement quality.

A FAIL is scientifically valuable: preserve the counterexample and investigate which alternate Routh-Hurwitz gate or mixed mechanism occurs. Do not alter H5 to rescue the hypothesis.
