# Exact physical-vs-record c3 boundary-displacement map audit v0.1

**Status:** FROZEN BEFORE EXECUTION
**Scope:** DERIVATION_AND_REPRESENTATION_ONLY

## Purpose

H5 prospectively reproduced the bounded target-family result that robust physical mean-square STABLE -> record UNSTABLE crossings have record-channel `c3<0` while `c1`, `c2`, and `c1*c2-c3` remain positive.

The exact c3 derivation separately established channel-specific quadratic surfaces `c3_p(omega)` and `c3_r(omega)`.

This phase builds a deterministic boundary-displacement representation from those two already-licensed surfaces without using any H4/H5 crossing outcome to choose a root, interval, sign, weight, or scalar compression.

No localization/collapse/measurement-quality outcome and no GFSA external candidate value may enter.

## Registered object

For fixed `g=gamma>0`, `k=kappa>0`, `q=eta*kappa>=0`, and physical active-plane state coordinates `x,z`, retain the exact separate quadratics

`c3_p(w)=A_p*w^2+B_p*w+C_p`,

`c3_r(w)=A_r*w^2+B_r*w+C_r`.

Use the already-closed exact coefficients from `C3_BOUNDARY_DERIVATION_RESULT_v0.1.md`.

For each channel construct the exact sign partition on the physical frequency half-line `w>=0` using all real nonnegative roots. Boundaries themselves are labeled `BOUNDARY` and are never silently assigned a sign.

Define the joint interval sets

`I_destab = {w>=0 : c3_p(w)>0 and c3_r(w)<0}`,

`I_stab = {w>=0 : c3_p(w)<0 and c3_r(w)>0}`,

`I_agree_pos = {w>=0 : c3_p(w)>0 and c3_r(w)>0}`,

`I_agree_neg = {w>=0 : c3_p(w)<0 and c3_r(w)<0}`.

These are set-valued joint objects. They do not average the channels and are not a stochastic chi.

## Special cases

The interval engine must explicitly handle:

- ordinary quadratic with two real roots;
- quadratic with one repeated real root;
- quadratic with no real root;
- effectively linear polynomial (`A=0`, `B!=0`);
- constant nonzero polynomial (`A=B=0`, `C!=0`);
- identically zero polynomial (`A=B=C=0`) -> `REFUSE_IDENTICALLY_ZERO`.

Only real roots `w>=0` partition the physical domain. Negative roots are retained as metadata but do not partition `w>=0`.

## Frozen numerical conventions

- coefficient degeneracy tolerance: `1e-12` relative to `max(1,|A|,|B|,|C|)`;
- boundary sign tolerance for verification only: `1e-10` relative to `max(1,|c3| scale)`;
- direct determinant comparison tolerance: relative-or-absolute `2e-10`;
- interval equality tolerance: `2e-10` on finite endpoints.

These tolerances are frozen before execution.

## Frozen gates

### D0 coefficient lineage

Recompute the closed exact coefficient formulas directly from the registered expressions and verify source hashes are captured before execution.

### D1 synthetic interval-engine controls

The sign-partition engine must correctly classify frozen synthetic controls covering:

1. `w^2-1` on `w>=0`;
2. `-(w-1)(w-3)`;
3. `(w-2)^2`;
4. `w^2+1`;
5. `2w-4`;
6. constant `+3`;
7. constant `-2`;
8. identically zero -> refusal.

### D2 fresh clean-room sign-partition controls

Use NumPy `default_rng(seed=2026082908)` to generate exactly 256 fresh base tuples:

- `gamma=1`;
- `log10(kappa/gamma) ~ Uniform(log10(0.2),log10(100))`;
- `eta ~ Uniform(0.001,0.95)`;
- `r ~ Uniform(0.05,0.98)`;
- `theta ~ Uniform(0,2*pi)`;
- `x=r*cos(theta)`, `z=r*sin(theta)`.

For each base tuple construct both channel partitions before evaluating any probe signs.

Then verify partition labels against direct polynomial evaluation on a fixed frequency probe set containing `logspace(-3,3,96)` plus two-sided offsets around every finite nonnegative root. Boundary-ambiguous probes are labeled `BOUNDARY` and excluded from sign disagreement counts rather than forced.

### D3 independent determinant reconstruction

For every non-boundary fresh probe, independently construct the channel 2x2 active matrices and 3x3 symmetric second-moment generator `G`, and verify

`c3=-det(G)`

agrees with the channel quadratic evaluation to relative-or-absolute `2e-10` and has the same sign partition label.

### D4 channel-swap covariance

Swapping the physical and record quadratics must exchange `I_destab <-> I_stab` while leaving the two agreement sets unchanged.

### D5 set reconstruction

For every fresh base tuple, the union of the four open-sign joint sets plus all explicit boundary points must cover the tested `w>=0` domain without overlap between incompatible labels.

## Decision rule

Overall status is `PASS_C3_BOUNDARY_DISPLACEMENT_MAP` only if D0-D5 pass.

Any mismatch is `DISPLACEMENT_MAP_FAILURE` and must be preserved and investigated. Identically-zero synthetic control refusal is an expected PASS condition, not an error.

## Interpretation firewall

A PASS licenses only an exact set-valued representation of how the physical and record `c3=0` surfaces partition frequency space.

It does not establish that every `I_destab` point is a full physical STABLE -> record UNSTABLE crossing, because the other Routh-Hurwitz margins remain mandatory.

The next prospective phase may use only this frozen map to select fresh predicted displacement cases, freeze those selections before full mean-square evaluation, and measure how often the full four-gate classification agrees. No H4/H5 case may be reused as prospective evidence.
