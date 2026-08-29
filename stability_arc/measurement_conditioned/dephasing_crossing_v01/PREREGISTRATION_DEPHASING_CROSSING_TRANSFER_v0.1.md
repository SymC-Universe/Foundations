# Dephasing-augmented mean-square crossing transfer v0.1

**Status:** FROZEN BEFORE EXECUTION
**Scope:** FRESH_DEPHASING_FAMILY_SCIENTIFIC_TEST

## Purpose

The dephasing-augmented planar architecture is composite-closed structurally. This phase asks a new scientific question on untouched inputs:

> Do robust c1+c3 channel-displacement classes continue to predict complete mean-square stability-class crossings when independent pure dephasing is present?

This is not a replication of the old sigma_z/amplitude-damping crossing pocket. The new panel spans the full planar measurement angle, broad pure-dephasing strength, broad rates/frequencies, and four equal-allocation radial strata.

No H4/H5/H9 candidate, shell, orientation sign, or numerical crossing region is used to select outcomes.

## Fresh stratified generator

Use NumPy `default_rng(seed=2026082920)`.

Generate exactly `300000` candidates in each of four radial strata, `1200000` total:

- `S1: 0.05 <= r < 0.50`;
- `S2: 0.50 <= r < 0.90`;
- `S3: 0.90 <= r < 0.98`;
- `S4: 0.98 <= r < 0.9999`.

Within each stratum draw independently:

- `gamma ~ LogUniform(0.1,2.0)`;
- `gamma_phi ~ LogUniform(0.001,2.0)`;
- `kappa ~ LogUniform(0.05,5.0)`;
- `eta ~ Uniform(0.01,0.95)`;
- `omega ~ LogUniform(0.02,10.0)`;
- `theta ~ Uniform(-pi,pi)`;
- radius uniformly in the registered stratum;
- isotropic 3D Bloch direction from a normalized standard-Gaussian vector.

No candidate may be regenerated or replaced because of any structural or stability outcome.

## Frozen canonical coordinates

For every input define

`a=gamma/2+gamma_phi`, `b=gamma`, `q=eta*kappa`,

`u=sin(theta)*x+cos(theta)*z`,

`v=cos(theta)*x-sin(theta)*z`,

`p=a*sin(theta)^2+b*cos(theta)^2`,

`d=kappa+a*cos(theta)^2+b*sin(theta)^2`,

`h=(b-a)*sin(theta)*cos(theta)`,

`Delta_phi=omega-h`,

`R=a+b+kappa+omega+q`.

The candidate is structurally admitted to Stage-A crossing selection only if

`abs(Delta_phi)/R > 1e-8`.

Exact-boundary and near-boundary candidates are retained in the generated panel and counted, but are not assigned a 2D quotient crossing class.

## Stage A firewall

Stage A may evaluate only:

1. `Delta_phi` structural admissibility;
2. the already-closed exact canonical `c1_phys`, `c1_record`;
3. the already-closed exact canonical `c3_phys`, `c3_record`.

It may not construct the 3x3 second-moment generator, calculate c2, calculate the final Hurwitz determinant margin, calculate eigenvalues, or assign full stability classes.

Use

`c1_phys = 3*(p+d)-14*q*u^2`,

`c1_record = 3*(p+d)+6*q-20*q*u^2`.

Use the exact `c3_phys` and `c3_record` functions frozen by the canonical planar quotient invariant derivation, with the dephasing-augmented `(p,d,h,q,u,v)` map. Their source implementation is frozen in this phase before execution.

Normalize

`m1_exact = c1/R`,

`m3_exact = c3/R^3`.

Use fixed robust threshold `MAP_TOL=1e-8`.

### DESTAB selection

`D_C13` iff

- structurally admitted;
- `c1_phys/R > +MAP_TOL`;
- `c3_phys/R^3 > +MAP_TOL`;
- `c3_record/R^3 < -MAP_TOL`.

### STAB selection

`S_C13` iff

- structurally admitted;
- `c1_record/R > +MAP_TOL`;
- `c3_phys/R^3 < -MAP_TOL`;
- `c3_record/R^3 > +MAP_TOL`.

For each radial stratum and each class record total eligible count. Across all strata, freeze the first `128` cases by global candidate ID for each class. Require at least `16` available in a class for that class's scientific sufficiency test to be scored.

Before Stage B write and hash the complete generated-panel identity, stratum hashes, frozen selected cases, their exact Stage-A coordinates, and selection SHA-256. Re-read and verify the bytes before any hidden margin is evaluated.

## Registered existence questions

- **H10D-E:** at least 16 fresh `D_C13` cases exist across the full registered panel.
- **H10S-E:** at least 16 fresh `S_C13` cases exist across the full registered panel.

Report stratum counts descriptively. No radial-stratum claim is preregistered in v0.1.

## Stage B full reveal

Only after Stage-A freeze verification may each frozen selected case be reconstructed from the full two-level Hilbert-space generator containing amplitude damping, pure dephasing, and planar measurement.

For each selected case independently verify:

- positive density matrix;
- exact one-dimensional maximal dark factor;
- full-to-canonical quotient matrix agreement <=`2e-9`;
- direct G-derived c1/c3 agreement with frozen Stage-A exact values <=`2e-8`;
- second-moment quotient intertwining <=`5e-9`.

Then compute the previously hidden normalized margins

`m2=c2/R^2`,

`mh=(c1*c2-c3)/R^3`,

and use unchanged `RH_TOL=1e-9` for full class:

- STABLE iff all four margins `m1,m2,m3,mh > +RH_TOL`;
- UNSTABLE iff at least one margin `< -RH_TOL`;
- BOUNDARY otherwise.

## Registered crossing hypotheses

### H10D sufficiency

If at least 16 `D_C13` cases exist and no reconstruction/boundary hold occurs, every frozen `D_C13` case is full

`physical STABLE -> record UNSTABLE`.

A single robust counterexample is `FAIL_H10D`. Preserve all blockers among the previously hidden physical `m2` and `mh`; do not add them to H10D after outcome exposure.

### H10S sufficiency

If at least 16 `S_C13` cases exist and no reconstruction/boundary hold occurs, every frozen `S_C13` case is full

`physical UNSTABLE -> record STABLE`.

A single robust counterexample is `FAIL_H10S`. Preserve all blockers among the previously hidden record `m2` and `mh`; do not add them post-outcome.

The two directions are scored independently.

## Frozen audit gates

- **X0 generator determinism:** all four stratum SHA-256 values reproduce exactly.
- **X1 Stage-A firewall:** only structural delta/c1/c3 are used before the selection file is hashed.
- **X2 selection replay:** every frozen case reproduces its exact structural and c1/c3 selection label.
- **X3 full Hilbert reconstruction:** all frozen cases satisfy density, dark-factor, quotient, c1/c3, and moment-intertwining tolerances.
- **X4 robustness:** no scored selected case is full-class BOUNDARY.
- **X5 controls:** fixed eta-zero physical/record identity and fixed stable/unstable/boundary cubic classifier controls pass.

Use `SELECTION_HOLD_D` or `SELECTION_HOLD_S` independently when a direction has fewer than 16 cases. Use `RECONSTRUCTION_HOLD` or `BOUNDARY_HOLD` when those conditions prevent scoring.

## Interpretation firewall

A PASS in either direction is bounded to this dephasing-augmented planar family and registered sampling frame. A FAIL is evidence that c2 and/or the final Hurwitz margin remains an independent coordinate under changed dissipation.

No prior sigma_z crossing region is counted as evidence, no universal orientation/radius claim is imported, and no stochastic scalar, localization, collapse, or measurement-quality claim is licensed.
