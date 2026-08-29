# Fresh c1-corrected displacement-map test v0.1

**Status:** FROZEN BEFORE EXECUTION
**Scope:** POST-H6 MINIMAL-CORRECTION PROSPECTIVE TEST

## Purpose

H6 falsified c3 displacement as a sufficient full-class coordinate because all 512 failed `I_destab` predictions were already physically non-stable through c1. A separate exact derivation then established

`c1_record-c1_phys = 6*q*(1-z^2) >= 0`

for physical states.

This phase tests the smallest justified correction. It does **not** add c2 or the final Hurwitz determinant margin during selection.

## Fresh generator

Use exactly NumPy `default_rng(seed=2026082912)` and generate exactly `500000` candidates `H7000001...H7500000`.

Use the same broad sampling frame as H6:

- `gamma=1`;
- `log10(kappa/gamma) ~ Uniform(log10(0.2),log10(100))`;
- `eta ~ Uniform(0.001,0.95)`;
- `r ~ Uniform(0.05,0.98)`;
- `theta ~ Uniform(0,2*pi)`;
- `log10(omega/gamma) ~ Uniform(-3,3)`;
- `x=r*cos(theta)`, `z=r*sin(theta)`, `q=eta*kappa`.

No candidate may be regenerated or replaced because of any outcome.

## Stage A allowed information

Stage A may evaluate only:

1. the frozen exact physical and record c3 quadratics;
2. the frozen exact physical c1 formula
   `c1_phys=9*gamma/2+3*kappa-14*q*z^2`.

It may not construct A, B, G, c2, the final Hurwitz determinant margin, eigenvalues, or full class labels.

Define the same robust c3 map threshold as H6:

`MAP_TOL=1e-8` using `c3 / max(1,|A|w^2+|B|w+|C|)`.

Define

`R=gamma+kappa+omega+q`

and the new robust first-gate selection threshold

`C1_TOL=1e-8` on `c1_phys/R`.

### H7D selection

Select a candidate into `I_destab_c1` iff

- robust `I_destab`: physical c3 positive and record c3 negative under `MAP_TOL`;
- `c1_phys/R > C1_TOL`.

By the already-closed exact c1 displacement identity, the record c1 is then also positive.

### H7S replication selection

Independently retain the uncorrected opposite class `I_stab` iff physical c3 is robustly negative and record c3 robustly positive. This is a fresh replication of the 512/512 one-sided H6 observation, not a reuse of H6 cases.

Freeze the first `512` candidates by candidate ID from each class. Require at least `128` available in each class or return `SELECTION_HOLD`.

Write all selected IDs, parameters, c3 signs, physical normalized c1, generator hash, and selection hash before Stage B.

## Stage B full reveal

Only after the Stage-A bytes and SHA-256 verify may the active matrices and real 3x3 second-moment generators be constructed.

Use the same normalized four Routh-Hurwitz margins and `RH_TOL=1e-9` as H6:

`m1=c1/R`,
`m2=c2/R^2`,
`m3=c3/R^3`,
`mh=(c1*c2-c3)/R^3`.

Classify a channel `STABLE` iff all four are `>+RH_TOL`, `UNSTABLE` iff at least one is `<-RH_TOL`, else `BOUNDARY`.

Verify direct-generator c1 and c3 against the frozen Stage-A formulas to relative-or-absolute tolerance `2e-10`.

## Registered hypotheses

### H7D minimal correction

Every fresh `I_destab_c1` case is full

`physical STABLE -> record UNSTABLE`.

A single robust counterexample falsifies H7D.

### H7S one-sided replication

Every fresh `I_stab` case is full

`physical UNSTABLE -> record STABLE`.

A single robust counterexample falsifies H7S.

The two hypotheses are scored separately. Failure of one does not relabel the other.

## Failure decomposition

If H7D fails, preserve every counterexample and report which still-unseen physical margins block it: `m2` and/or `mh`. Do not add those margins to H7D after the fact.

If H7S fails, preserve every counterexample and report record-side blockers among `m1`, `m2`, and `mh`.

These decompositions may motivate a later fresh phase only.

## Frozen gates

- **T0 generator determinism:** exact candidate-array SHA-256 reproduction.
- **T1 Stage-A freeze:** at least 128 available per class; first 512 by ID frozen and hashed before Stage B.
- **T2 predictor replay:** every frozen selection replays its exact c3/c1 Stage-A label.
- **T3 reconstruction:** direct G-derived c1 and c3 agree with Stage-A formulas within `2e-10`.
- **T4 robustness:** no selected channel is `BOUNDARY` under frozen full-class tolerance.
- **T5 H7D:** zero `I_destab_c1` full-class counterexamples.
- **T6 H7S:** zero `I_stab` full-class counterexamples.
- **T7 controls:** eta-zero physical/record identity and fixed cubic classifier controls pass.

## Decision labels

Report H7D and H7S separately as PASS or FAIL when T0-T4/T7 are valid. Use `SELECTION_HOLD`, `RECONSTRUCTION_HOLD`, `BOUNDARY_HOLD`, or `AUDIT_FAILURE` when those conditions prevent scientific scoring.

## Interpretation firewall

A H7D PASS would license only the bounded statement that c3 displacement plus physical c1 positivity is sufficient in this fresh sampling frame. A FAIL means c2 and/or the final Hurwitz margin remains independently necessary.

A H7S PASS would be a second fresh bounded replication of the one-sided `I_stab` behavior, not a theorem.

No stochastic scalar, localization, collapse, or measurement-quality claim is licensed.
