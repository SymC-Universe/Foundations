# Exact c1 first-Hurwitz-gate derivation v0.1

**Status:** FROZEN BEFORE EXECUTION
**Scope:** POST-H6 FAILURE-MECHANISM DERIVATION

## Purpose

H6 prospectively falsified c3 sign displacement as a sufficient complete mean-square class coordinate. All 512 failed `I_destab` predictions shared a physical `m1` failure. That observation motivates this derivation but does not determine its algebra.

This phase derives the channel-specific first cubic Routh-Hurwitz coefficient directly from the active stochastic quotient without using any H6 candidate values.

## Frozen model

Use

`g=gamma>0`, `k=kappa>0`, `q=eta*kappa>=0`, frequency `w`, and active-plane coordinates `x,z`.

Physical drift and shared stochastic matrix:

`A_p=[[-(g/2+k),w],[-w,-g]]`,

`B=[[-sqrt(2q) z,-sqrt(2q) x],[0,-2 sqrt(2q) z]]`.

Same-record drift:

`A_r=A_p+[[0,2qzx],[0,-2q(1-z^2)]]`.

For each channel independently construct the real 3x3 symmetric second-moment generator from

`dP/dt=A P+P A^T+B P B^T`.

For

`det(lambda I-G)=lambda^3+c1 lambda^2+c2 lambda+c3`, use the identity `c1=-tr(G)` only after `G` has been independently constructed.

## Registered exact targets

The audit must independently recover

`c1_p = 9*g/2 + 3*k - 14*q*z^2`

and

`c1_r = 9*g/2 + 3*k + 6*q - 20*q*z^2`.

It must then independently establish

`Delta_c1 = c1_r-c1_p = 6*q*(1-z^2)`.

For physical Bloch states `x^2+z^2<1`, this implies `Delta_c1>0` whenever `q>0`; at `q=0`, `Delta_c1=0`.

This directionality is an algebraic consequence of the registered model, not a fit to H6.

## Frozen gates

- **C0 independent moment construction:** construct physical and record `G` directly from the covariance action on a symmetric basis.
- **C1 exact symbolic c1 identities:** SymPy simplifies independently derived `-tr(G_p)` and `-tr(G_r)` minus the registered targets exactly to zero.
- **C2 exact displacement identity:** SymPy simplifies `(c1_r-c1_p)-6*q*(1-z^2)` exactly to zero.
- **C3 fresh clean-room controls:** NumPy `default_rng(seed=2026082911)` generates exactly 128 fresh broad physical states and positive rates; direct numerical `-tr(G)` must agree with the exact formulas to relative-or-absolute `2e-12` for both channels.
- **C4 physical-state directionality:** all 128 fresh controls must satisfy `c1_r>=c1_p` to `2e-12`, with exact equality under a fixed `q=0` control.
- **C5 active-coordinate invariance:** under fixed non-orthogonal active-coordinate transform `R=[[1.2,0.3],[-0.2,0.9]]`, the induced second-moment generators must preserve c1 to `2e-11` for both channels on all fresh controls.

Overall status is `PASS_C1_GATE_DERIVATION` only if C0-C5 pass. Any mismatch is `C1_DERIVATION_FAILURE` and must be preserved.

## Interpretation firewall

A PASS licenses c1 as an exact separate mean-square stability coordinate and licenses the model-specific nonnegative conditioning displacement `Delta_c1` for physical states.

It does not establish that `c1_p>0` together with `I_destab` is sufficient for full STABLE -> UNSTABLE crossing. That requires a new fresh prospective test after this derivation closes.

No c2, final Hurwitz determinant, stochastic scalar chi, localization, collapse, or measurement-quality claim is licensed here.
