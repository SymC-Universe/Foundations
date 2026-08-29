# Exact c3 boundary derivation audit v0.1

**Status:** FROZEN BEFORE EXECUTION
**Scope:** DERIVATION_ONLY

## Purpose

The fresh H4 class-crossing phase prospectively verified 50 physical mean-square STABLE -> same-record UNSTABLE crossings. Post-outcome inspection found that all 50 record-channel failures occurred through the cubic Routh-Hurwitz coefficient `c3` becoming negative while `c1`, `c2`, and `c1*c2-c3` remained positive.

That 50/50 pattern is a post-outcome observation and is not promoted here.

This phase derives the exact `c3=0` geometry directly from the measured-qubit active stochastic equations, independently of the H4 numerical outcomes.

No localization, collapse, measurement-quality, GFSA external-candidate, H4 crossing ID, or fitted boundary may enter the derivation.

## Model notation

Use

`g = gamma > 0`,
`k = kappa > 0`,
`q = eta*kappa >= 0`,
`w = omega >= 0`,

with physical Bloch coordinates `x,z` satisfying `x^2+z^2<1` for the active-plane controls.

The physical active matrices are

`A_p=[[-(g/2+k),w],[-w,-g]]`

and

`B=[[-sqrt(2q) z,-sqrt(2q) x],[0,-2 sqrt(2q) z]]`.

The same-record drift is

`A_r=A_p+[[0,2qzx],[0,-2q(1-z^2)]]`.

For each channel let `G` be the real 3x3 symmetric second-moment generator and define

`det(lambda I-G)=lambda^3+c1 lambda^2+c2 lambda+c3`.

## Registered exact c3 quadratics

The derivation must independently recover

`c3_p(w)=A_p3 w^2+B_p3 w+C_p3`

with

`A_p3 = 2*(3g+2k-2q*x^2-10q*z^2)`,

`B_p3 = 16*q*x*z*(g+k-3q*z^2)`,

`C_p3 = (g-4q*z^2)*(3g+2k-8q*z^2)*(g+2k-2q*z^2)`,

and

`c3_r(w)=A_r3 w^2+B_r3 w+C_r3`

with

`A_r3 = 2*(3g+2k+4q-2q*x^2-14q*z^2)`,

`B_r3 = 4*q*x*z*(7g+6k+8q-30q*z^2)`,

`C_r3 = (g+2k-2q*z^2)*(g+2q-6q*z^2)*(3g+2k+4q-12q*z^2)`.

These are frozen derivation targets, not fits to H4.

## Boundary geometry

For either channel `j in {p,r}`, define

`Delta_j = B_j3^2-4*A_j3*C_j3`.

When `A_j3 != 0` and `Delta_j >= 0`, define exact roots

`w_j_minus=(-B_j3-sqrt(Delta_j))/(2*A_j3)`,

`w_j_plus=(-B_j3+sqrt(Delta_j))/(2*A_j3)`

and sort them numerically as `w_j_low <= w_j_high`.

The audit must verify that the factorization

`c3_j(w)=A_j3*(w-w_j_minus)*(w-w_j_plus)`

holds wherever the roots are real.

Special cases `A_j3=0` or `Delta_j<0` must be explicitly classified rather than forced into the root formula.

## Frozen symbolic gates

- **B0 independent moment construction:** derive `G_p` and `G_r` from `A P + P A^T + B P B^T` on the symmetric basis without inserting the target `c3` formulas.
- **B1 exact polynomial identity:** SymPy must simplify the independently derived `c3_p` and `c3_r` minus the registered quadratic targets exactly to zero.
- **B2 coefficient extraction:** direct polynomial coefficient extraction in `w` must reproduce all six registered `A/B/C` expressions exactly.
- **B3 determinant identity:** independently verify `c3=-det(G)` for both channels.
- **B4 boundary factorization:** exact symbolic discriminant/root algebra must reproduce the quadratic factorization relation, with explicit handling of degenerate cases.
- **B5 numerical clean-room controls:** use fresh seed `2026082906` to generate 64 physical active-plane controls over broad positive rates and physical states, then compare direct determinant `c3` against the registered quadratic evaluation to relative/absolute tolerance `2e-10` for both channels. These controls test implementation only and do not establish a class-crossing frequency.

Overall status is `PASS_C3_BOUNDARY_DERIVATION` only if B0-B5 pass. Any mismatch is `DERIVATION_FAILURE` and must be preserved.

## Interpretation firewall

A PASS licenses an exact channel-specific `c3=0` boundary surface and its quadratic-in-frequency representation for this active measured-qubit model.

It does not establish that `c3` is always the first Routh-Hurwitz gate to fail. Full mean-square classification still requires all four inequalities.

It does not license a universal scalar, localization/collapse prediction, or averaging the physical and same-record boundaries.

The useful joint object is the pair of separately recoverable boundary surfaces and their displacement under the conditioning bridge.
