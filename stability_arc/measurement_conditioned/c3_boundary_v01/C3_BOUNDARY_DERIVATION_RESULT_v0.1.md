# Exact c3 boundary derivation audit v0.1 result

**Status:** PASS_C3_BOUNDARY_DERIVATION
**Scope:** DERIVATION_ONLY
**Canonical run:** `33257258056`
**Execution commit:** `4bc2da711471dfef72da8e73e68864d938951c08`

## Frozen source identities

- preregistration SHA-256: `67ed98045e0ff212889060962c6120561f60074cbcb1fbbe5ce314aaa7a6bf9f`
- audit-code SHA-256: `a70236f1556765c1851f2163bb04fc281ac951336c98755ffab2e1a42911af65`
- workflow SHA-256: `da8e8a04f69adb7f18ab2002a96f21436394445e3198757dfef8a74e2cd3e8dd`
- upstream H4 result SHA-256: `50a65476b7dc7d982a8dbaccd2633384a0b5b988c37f02ca1eaf13aa81a135ff`

## Preserved evidence

- artifact ID: `9716183849`
- artifact ZIP SHA-256: `fa3a9b2814c8f6f049eb14db03a543d05f93cbd0f8507d7ab13e1f5e06153f20`
- runner environment: Python 3.12.14, NumPy 2.1.3, SymPy 1.13.3

The workflow independently verified the evidence manifest before upload.

## Frozen gate results

All registered B0-B5 gates passed.

- **B0 independent moment construction:** PASS.
- **B1 exact polynomial identity:** PASS for both physical and same-record channels.
- **B2 coefficient extraction:** PASS; all six registered quadratic coefficients were recovered exactly.
- **B3 determinant identity:** PASS; `c3=-det(G)` for both channels.
- **B4 boundary factorization:** PASS, including explicit discriminant/root handling.
- **B5 fresh clean-room controls:** PASS on seed `2026082906`; maximum relative-or-absolute error `1.3657194584723663e-14` versus frozen `2e-10` gate.

## Exact licensed boundary surfaces

Use `g=gamma>0`, `k=kappa>0`, `q=eta*kappa>=0`, `w=omega>=0` and active-plane state coordinates `x,z`.

The physical channel has

`c3_p(w)=A_p3*w^2+B_p3*w+C_p3`

with

`A_p3 = 2*(3g+2k-2q*x^2-10q*z^2)`,

`B_p3 = 16*q*x*z*(g+k-3q*z^2)`,

`C_p3 = (g-4q*z^2)*(3g+2k-8q*z^2)*(g+2k-2q*z^2)`.

The same-record channel has

`c3_r(w)=A_r3*w^2+B_r3*w+C_r3`

with

`A_r3 = 2*(3g+2k+4q-2q*x^2-14q*z^2)`,

`B_r3 = 4*q*x*z*(7g+6k+8q-30q*z^2)`,

`C_r3 = (g+2k-2q*z^2)*(g+2q-6q*z^2)*(3g+2k+4q-12q*z^2)`.

For either channel `j`, with `Delta_j=B_j3^2-4*A_j3*C_j3`, real nondegenerate roots satisfy

`w_j_±=(-B_j3 ± sqrt(Delta_j))/(2*A_j3)`

and

`c3_j(w)=A_j3*(w-w_j_-)*(w-w_j_+)`.

Degenerate and no-real-root cases remain explicitly classified rather than forced into this formula.

## Interpretation firewall

This PASS licenses the exact channel-specific `c3=0` surfaces for the active measured-qubit stochastic model. It does **not** license the claim that `c3` is always the first Routh-Hurwitz condition to fail, a universal scalar, a localization/collapse prediction, or an average of physical and record boundaries.

The H4 observation that all 50 fresh crossings failed through `c3<0` remains post-outcome relative to H4. The next justified step is a new prospective test on fresh inputs asking whether robust STABLE -> UNSTABLE crossings in the already-frozen H4 target family consistently cross through the `c3` gate while the other Routh-Hurwitz margins remain positive.
