# Near-pure orientation admissibility test v0.1

**Status:** FROZEN BEFORE EXECUTION
**Scope:** FRESH_POST-H8_TARGETED_GEOMETRY_TEST

## Motivation and evidentiary firewall

H8 used eight fresh radius/orientation strata and found only two robust c1+c3 destabilizing candidates. Both occurred in the preregistered highest shell `0.995 <= r < 0.9999` and both had `x*z<0`. The registered H8 existence threshold failed and its sufficiency test remained insufficient.

Those two cases are hypothesis-generation only for this phase. They are not included in the new panel and cannot count as evidence.

This phase keeps the **same H8 R4 shell**, the same broad rate/frequency/orientation-magnitude distributions, and the same c1/c3 thresholds. It changes only the prospective sampling allocation: the R4 negative and positive orientation-product strata are each sampled deeply enough to test the H8 orientation lead on a new seed.

## Frozen fresh generator

Use NumPy `default_rng(seed=2026082914)`.

Generate exactly:

- `500000` candidates in `NEG`, with `x*z<0`;
- `500000` candidates in `POS`, with `x*z>0`;
- `1000000` total fresh candidates.

For every candidate:

- `gamma=1`;
- `log10(kappa/gamma) ~ Uniform(log10(0.2),log10(100))`;
- `eta ~ Uniform(0.001,0.95)`;
- `log10(omega/gamma) ~ Uniform(-3,3)`;
- `r ~ Uniform(0.995,0.9999)`;
- `phi ~ Uniform(0,pi/2)`;
- choose `sign_z` uniformly from `{-1,+1}`;
- `|x|=r*cos(phi)`, `|z|=r*sin(phi)`;
- `z=sign_z*|z|`;
- for NEG, `sign_x=-sign_z`; for POS, `sign_x=sign_z`;
- `x=sign_x*|x|`;
- `q=eta*kappa`.

No candidate may be regenerated or replaced because of any outcome.

## Stage A information firewall

Stage A may use only the already-closed exact formulas

`c1_phys = 9*gamma/2 + 3*kappa - 14*q*z^2`

and the exact separate physical/record c3 quadratics.

It may not construct A, B, G, c2, the final Hurwitz determinant margin, eigenvalues, or full class labels.

Use unchanged frozen thresholds:

- `C1_TOL=1e-8` on `c1_phys/R`;
- `MAP_TOL=1e-8` on normalized physical and record c3;
- `R=gamma+kappa+omega+q`.

A case is `ADMISSIBLE_DESTAB_C1C3` iff

- `c1_phys/R > C1_TOL`;
- normalized `c3_phys > MAP_TOL`;
- normalized `c3_record < -MAP_TOL`.

Record total eligible count separately for NEG and POS. Freeze the first `128` eligible cases by within-stratum candidate index from each sign stratum, along with complete inputs and Stage-A coordinates. Write and verify the selection SHA-256 before Stage B.

## Registered hypotheses

### H9N negative-orientation existence

The fresh NEG stratum contains at least `20` robust `ADMISSIBLE_DESTAB_C1C3` cases.

### H9P positive-orientation absence

The fresh POS stratum contains zero robust `ADMISSIBLE_DESTAB_C1C3` cases.

The two hypotheses are scored independently. Failure of H9P does not affect H9N and vice versa.

## Stage B full mean-square reveal

Only after the Stage-A bytes and digest are frozen may the full physical and same-record active matrices and 3x3 second-moment generators be constructed for the frozen eligible cases.

Use the established normalized margins

`m1=c1/R`, `m2=c2/R^2`, `m3=c3/R^3`, `mh=(c1*c2-c3)/R^3`

with unchanged `RH_TOL=1e-9`.

Classify each channel STABLE iff all four margins are `>+RH_TOL`, UNSTABLE iff any is `<-RH_TOL`, else BOUNDARY.

Direct G-derived c1/c3 must reproduce the Stage-A exact formulas to relative-or-absolute `2e-10`.

## Registered H9F sufficiency

If at least 20 total eligible cases are frozen and no reconstruction/boundary hold occurs, every frozen `ADMISSIBLE_DESTAB_C1C3` case, from either orientation sign, must be a full

`physical STABLE -> record UNSTABLE`

crossing.

A single robust counterexample is `FAIL_H9F` and must be preserved. Still-hidden physical `m2` and/or `mh` blockers may be reported after failure but may not be added to H9F post-outcome.

If fewer than 20 total eligible cases exist, report `INSUFFICIENT_H9F`.

## Frozen audit gates

- **N0 deterministic generator:** both 500000-case stratum SHA-256 values reproduce exactly.
- **N1 geometry integrity:** every generated state satisfies `0.995<=r<0.9999` and its assigned orientation sign.
- **N2 Stage-A freeze:** selection bytes/digest exist and verify before Stage B.
- **N3 Stage-A replay:** all frozen eligible cases replay the same c1+c3 label exactly.
- **N4 full reconstruction:** direct G-derived c1/c3 match exact formulas within `2e-10`.
- **N5 controls:** eta-zero physical/record identity and fixed stable/unstable/boundary classifier controls pass.

## Interpretation firewall

H9N PASS would confirm only that the high-radius negative-orientation stratum contains the c1+c3 admissible class at the registered fresh sampling density. H9P PASS would be a bounded absence result for the matched positive-orientation stratum, not a theorem.

H9F PASS would license c1+c3 sufficiency only for the frozen near-pure admissible cases. No radius-only rule, universal orientation rule, stochastic scalar, localization, collapse, or measurement-quality claim is licensed.
