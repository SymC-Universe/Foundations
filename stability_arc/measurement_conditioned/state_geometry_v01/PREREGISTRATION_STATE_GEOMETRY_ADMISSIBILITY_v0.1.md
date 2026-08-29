# State-geometry admissibility audit v0.1

**Status:** FROZEN BEFORE EXECUTION
**Scope:** POST-H7 DOMAIN-BOUNDARY TEST

## Motivation and firewall

H7 returned `SELECTION_HOLD` because its fresh broad generator, restricted to Bloch radius `r<0.98`, produced zero robust cases satisfying both the c3 destabilizing displacement class and positive physical c1. An audit-only consistency check showed that a previously preserved H4 crossing lies at radius about `0.9981`, outside H7's sampling support.

That historical case motivates the domain question but is not evidence for this phase. No H4/H5/H6/H7 candidate may enter the fresh panel or decision rule.

This phase asks where, in state radius and the sign of `x*z`, the already-derived c1+c3 admissibility condition appears, and whether fresh admissible cases are complete physical STABLE -> record UNSTABLE crossings after the hidden Routh-Hurwitz margins are revealed.

## Frozen fresh stratified generator

Use NumPy `default_rng(seed=2026082913)`.

Use four non-overlapping radial shells:

- `R1: 0.90 <= r < 0.95`;
- `R2: 0.95 <= r < 0.98`;
- `R3: 0.98 <= r < 0.995`;
- `R4: 0.995 <= r < 0.9999`.

For each shell use two orientation-product strata:

- `NEG: x*z < 0`;
- `POS: x*z > 0`.

Generate exactly `50000` candidates per shell/sign stratum, exactly `400000` candidates total.

For each candidate fix `gamma=1` and independently draw:

- `log10(kappa/gamma) ~ Uniform(log10(0.2),log10(100))`;
- `eta ~ Uniform(0.001,0.95)`;
- `log10(omega/gamma) ~ Uniform(-3,3)`;
- `r ~ Uniform(shell_lo,shell_hi)`;
- `phi ~ Uniform(0,pi/2)`;
- `sign_z` uniformly from `{-1,+1}`;
- set `|x|=r*cos(phi)`, `|z|=r*sin(phi)`;
- set `z=sign_z*|z|`;
- for `NEG`, set `sign_x=-sign_z`; for `POS`, set `sign_x=sign_z`;
- set `x=sign_x*|x|`, `q=eta*kappa`.

Endpoints with exactly zero x or z have probability zero; if floating-point generation produces `x*z==0`, retain the candidate and label it `ORIENTATION_ZERO` rather than redrawing it.

No candidate may be replaced because of any c1, c3, or full-stability result.

## Stage A: exact c1+c3 coordinates only

Before any active matrix, stochastic matrix, second-moment generator, eigenvalue, c2, or final Hurwitz determinant is constructed, compute only:

`c1_phys = 9*gamma/2 + 3*kappa - 14*q*z^2`,

and the already-closed exact channel c3 quadratics at the generated omega.

Define

`R = gamma+kappa+omega+q`.

Use frozen robust thresholds:

- `C1_TOL=1e-8` on `c1_phys/R`;
- `MAP_TOL=1e-8` on each c3 divided by `max(1,|A|omega^2+|B|omega+|C|)`.

A candidate is `ADMISSIBLE_DESTAB_C1C3` iff

- `c1_phys/R > C1_TOL`;
- normalized `c3_phys > MAP_TOL`;
- normalized `c3_record < -MAP_TOL`.

For each of the 8 fixed strata, record the total admissible count and freeze the first `128` admissible cases by within-stratum generation index. Fewer than 128 does not invalidate a stratum; all available cases are frozen. Freeze the complete Stage-A bytes and SHA-256 before Stage B.

Stage A also records descriptive, non-decision metadata for each frozen case: `r`, `|z|`, `x*z`, and the three normalized selection coordinates. These values may not alter selection.

## Registered geometry hypotheses

### H8E high-radius existence

Across `R3+R4` combined, at least `20` fresh robust `ADMISSIBLE_DESTAB_C1C3` cases exist.

- PASS: at least 20;
- FAIL: fewer than 20.

### H8L low-radius absence replication

Across `R1+R2` combined, the fresh panel contains zero robust `ADMISSIBLE_DESTAB_C1C3` cases.

- PASS: zero;
- FAIL: one or more.

This is deliberately falsifiable and remains bounded to the registered sampling frame.

Orientation-sign counts are reported by stratum but no sign asymmetry claim is preregistered in v0.1.

## Stage B: full mean-square reveal

Only after the Stage-A file and digest are written and re-verified, construct for every frozen admissible case the physical and same-record 2x2 drift matrices, shared multiplicative-noise matrix, and real 3x3 symmetric second-moment generators.

Use the established four normalized Routh-Hurwitz margins:

`m1=c1/R`,
`m2=c2/R^2`,
`m3=c3/R^3`,
`mh=(c1*c2-c3)/R^3`.

Use frozen `RH_TOL=1e-9`:

- STABLE iff all four margins are `>+RH_TOL`;
- UNSTABLE iff any margin is `<-RH_TOL`;
- BOUNDARY otherwise.

Direct G-derived c1 and c3 must agree with Stage-A exact formulas to relative-or-absolute `2e-10`.

## Registered H8F c1+c3 sufficiency on fresh admissible geometry

Every frozen `ADMISSIBLE_DESTAB_C1C3` case must be full

`physical STABLE -> record UNSTABLE`.

Scoring requires at least 20 total frozen admissible cases and zero reconstruction/boundary holds.

- `PASS_H8F` if every scored case is a full crossing;
- `FAIL_H8F` on the first or any robust counterexample;
- `INSUFFICIENT_H8F` if fewer than 20 admissible cases exist overall;
- `BOUNDARY_HOLD` if any frozen case is boundary-classed;
- `RECONSTRUCTION_HOLD` for c1/c3 reconstruction mismatch.

If H8F fails, preserve every counterexample and report only the still-unseen physical blockers among `m2` and `mh`. Do not add those margins to H8F after outcome exposure.

## Frozen gates

- **G0 deterministic stratified generator:** regenerate all 8 stratum hashes exactly.
- **G1 Stage-A firewall:** c1+c3-only selection and complete frozen selection digest verify before Stage B.
- **G2 shell/orientation integrity:** every candidate lies in its registered radius shell and orientation-product stratum, except explicitly retained `ORIENTATION_ZERO` candidates.
- **G3 c1/c3 replay:** all frozen cases reproduce their Stage-A admissibility labels exactly.
- **G4 full reconstruction:** direct G-derived c1/c3 agree with exact Stage-A formulas within `2e-10`.
- **G5 classifier controls:** eta-zero physical/record identity and fixed stable/unstable/boundary cubic controls pass.

Scientific H8E, H8L, and H8F are reported separately from mechanical G0-G5.

## Interpretation firewall

This phase maps a state-domain boundary exposed by a prior selection hold. It does not establish universality, a theorem that radius alone controls crossings, or any localization/collapse/measurement-quality consequence.

Same-noise physical and same-record channels remain separately recoverable. No stochastic scalar is introduced.
