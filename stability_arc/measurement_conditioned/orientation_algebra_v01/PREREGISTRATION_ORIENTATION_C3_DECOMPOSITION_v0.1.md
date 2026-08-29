# Exact orientation-product c3 decomposition v0.1

**Status:** FROZEN BEFORE EXECUTION
**Scope:** OUTCOME-FREE_ALGEBRAIC_DERIVATION

## Purpose

H9 prospectively found a bounded near-pure orientation asymmetry: 33 robust c1+c3 admissible cases for `x*z<0`, zero for the matched `x*z>0` panel, and 33/33 full class crossings among the frozen admissible cases.

This phase does not reuse those 33 cases. It asks whether the model equations contain an exact orientation-sign structure that explains why changing the sign of `x*z` can move the c3 boundary while leaving c1 unchanged.

## Sign-separated coordinates

Write

`x = s*a`, `z=b`,

with `s in {-1,+1}`, `a>=0`, `b>=0`, and physical state condition `a^2+b^2<1`.

The sign product is `sign(x*z)=s` in this convention. Global simultaneous sign reversal of x and z leaves the same product sign and the same formulas.

Use `g>0`, `k>0`, `q>=0`, `w>=0`.

## Registered exact decomposition targets

For each channel, the exact c3 quadratic must reduce to an affine function of orientation sign:

`c3_p(s) = E_p + s*M_p`,

`c3_r(s) = E_r + s*M_r`,

where

`E_p = A_p*w^2 + C_p`,

`M_p = 16*q*a*b*w*(g+k-3*q*b^2)`,

`A_p = 2*(3*g+2*k-2*q*a^2-10*q*b^2)`,

`C_p = (g-4*q*b^2)*(3*g+2*k-8*q*b^2)*(g+2*k-2*q*b^2)`,

and

`E_r = A_r*w^2 + C_r`,

`M_r = 4*q*a*b*w*(7*g+6*k+8*q-30*q*b^2)`,

`A_r = 2*(3*g+2*k+4*q-2*q*a^2-14*q*b^2)`,

`C_r = (g+2*k-2*q*b^2)*(g+2*q-6*q*b^2)*(3*g+2*k+4*q-12*q*b^2)`.

Thus

`c3_j(+1)-c3_j(-1)=2*M_j`.

The first Hurwitz coefficients must be sign-independent:

`c1_p(+1)=c1_p(-1)`,

`c1_r(+1)=c1_r(-1)`.

## Exact two-sign c3 class map

For each fixed magnitude tuple `(g,k,q,w,a,b)`, define independently for `s=-1,+1`:

- `DESTAB_C3(s)` iff `c3_p(s)>0` and `c3_r(s)<0`;
- `STAB_C3(s)` iff `c3_p(s)<0` and `c3_r(s)>0`;
- otherwise `OTHER_C3(s)`;
- exact zero is `BOUNDARY_C3(s)`.

No orientation sign is privileged by definition. The algebra determines which of the two signs, if either, occupies each class.

## Frozen symbolic/numerical gates

- **O0 independent moment construction:** construct physical and record second-moment generators from `A P+P A^T+B P B^T` and derive c1/c3 directly, without substituting the registered decomposition targets.
- **O1 exact affine decomposition:** SymPy must reduce independently derived c3 for `s=+1` and `s=-1` to `E_j +/- M_j` exactly for both channels.
- **O2 exact sign-flip identities:** both `c3_j(+)-c3_j(-)-2*M_j` simplify exactly to zero; both c1 sign differences simplify exactly to zero.
- **O3 exact no-measurement orientation control:** at `q=0`, `M_p=M_r=0`, so c3 and c1 are orientation-sign invariant.
- **O4 fresh classifier controls:** NumPy `default_rng(seed=2026082915)` generates exactly 512 fresh physical magnitude/rate tuples, including radii from `0.2` to `0.9999`. For both signs of every tuple, the affine decomposition must reproduce direct G-derived c3 to relative-or-absolute `2e-10` and the algebraic c3 class label must equal the direct determinant sign label.
- **O5 coordinate transform control:** under fixed active-coordinate transform `R=[[1.2,0.3],[-0.2,0.9]]`, direct c1 and c3 invariants must agree to `2e-10`; no sign class may change solely because of coordinate basis.

Overall status is `PASS_ORIENTATION_C3_DECOMPOSITION` only if O0-O5 pass. Any failure is preserved as `ORIENTATION_DERIVATION_FAILURE`.

## Interpretation firewall

A PASS licenses an exact orientation-sign decomposition of the channel-specific c3 coordinates and the statement that c1 is orientation-sign blind in this measured-qubit active representation.

It does not prove that negative x*z is universally required for destabilization, does not promote the near-pure H9 result outside its sampling frame, and does not license a scalar combination of the physical and record channels.

The next scientific extension after a PASS should change the measurement/dissipation geometry or derive a bounded sufficient-condition region from these exact invariants before any localization/collapse claim.
