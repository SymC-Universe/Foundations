# Post-publication cosmology reinterpretation for the 2026 Scientific Reports paper

**Date:** 2026-09-19  
**Status:** CURRENT-PROGRAM MATHEMATICAL CORRECTION / POST-PUBLICATION FOLLOW-UP REQUIRED  
**Article:** *Exceptional-point stability boundaries from quantum dissipation to cosmological acceleration*, Scientific Reports 16, 28667 (2026), DOI 10.1038/s41598-026-56887-7  
**Program authority:** SymC General Operations Manual v0.8.0

## 1. Purpose

The published paper contains an algebraically exact flat-ΛCDM coincidence,

[
alpha_delta equiv rac{H}{sqrt{4pi Gho_m}} = 1
quadLongleftrightarrowquad
q=0,
]

but interprets this coordinate crossing as **critical damping of the density-growth equation** and as an exceptional-point stability transition.

Under the current generator-first framework, that interpretation does not survive direct inspection of the density-growth generator.

This note preserves the algebraic identity while correcting its dynamical classification.

## 2. Native density-growth equation

For pressureless clustering matter in the usual sub-horizon linear-growth limit,

[
ddotdelta + 2Hdotdelta - 4pi Gho_m,delta = 0.
]

If the coefficients are treated locally as frozen for characteristic-root classification, the characteristic equation is

[
lambda^2 + 2Hlambda - 4pi Gho_m = 0,
]

with roots

[
lambda_pm
=
-H pm sqrt{H^2+4pi Gho_m}.
]

The discriminant is therefore

[
Delta
=
(2H)^2 - 4(1)(-4pi Gho_m)
=
4H^2+16pi Gho_m.
]

For (H>0) and (ho_m>0),

[
Delta>0.
]

It cannot vanish.

The density-growth generator therefore does **not** undergo the ordinary passive second-order repeated-root transition at the coordinate value defined by (H/sqrt{4pi Gho_m}=1).

## 3. What happens at q = 0

Within spatially flat ΛCDM,

[
q=0
quadLongrightarrowquad
Omega_m=rac{2}{3}
quadLongrightarrowquad
H^2=4pi Gho_m.
]

The normalized magnitude coordinate consequently satisfies

[
alpha_delta
=
rac{H}{sqrt{4pi Gho_m}}
=
1.
]

That identity is retained.

However, at the same point the characteristic roots are

[
lambda_pm
=
-H pm sqrt{2},H,
]

which are distinct. One is positive and one is negative.

Thus (q=0) is not a coalescence of the density-growth eigenvalues and is not a mechanical critical-damping EP of this generator.

## 4. Sign/classification error

The ordinary stable damped oscillator is

[
ddot x+gammadot x+Omega^2x=0,
qquad
Omega^2>0.
]

Its characteristic discriminant is

[
gamma^2-4Omega^2,
]

which can vanish.

The cosmological density-growth equation instead contains

[
-4pi Gho_m,delta,
]

which is a negative-curvature / growth-driving term in this local characteristic classification. Replacing its magnitude by a positive (omega_delta^2=4pi Gho_m) and then importing the stable-oscillator damping-ratio discriminant changes the sign of the generator.

The Hubble term (2Hdotdelta) is legitimately friction-like, but the gravitational term is not a positive restoring term for the long-wavelength dust growth mode.

## 5. Current scientific disposition

The current program therefore uses the following classification:

- **Retained exactly:** the flat-ΛCDM algebraic identity
  [
  alpha_delta=1Longleftrightarrow q=0.
  ]
- **Retained as potentially useful:** (alpha_delta) as a normalized cosmological balance coordinate.
- **Withdrawn from current interpretation:** calling (alpha_delta=1) the ordinary mechanical critical-damping boundary of the density-growth equation.
- **Withdrawn from current interpretation:** calling the (q=0) density-growth crossing an EP2 on the basis of this scalar second-order equation.
- **Not implied:** that the algebraic coincidence has no scientific value. It may still be useful as a kinematic/balance relation and as a coordinate for comparing cosmological models.
- **Required for any future EP claim:** explicit coalescence and defectiveness of the relevant native generator, not magnitude substitution into the passive-oscillator formula.

## 6. Relationship to the published record

The Scientific Reports Version of Record is preserved as published. This note does not silently rewrite it.

The current SymC program treats the cosmological result more narrowly than the published wording:

> the (q=0) coincidence is an exact flat-ΛCDM balance identity, not an established critical-damping exceptional point of the density-growth generator.

A formal journal correction or author correction should be considered so that the external Version of Record and the current generator-first interpretation do not remain in avoidable conflict.

## 7. Consequence for cross-domain claims

This correction removes the cosmological density-growth equation from the set of systems that can currently be used as direct evidence for a shared mechanical (chi=1) EP boundary.

It does not affect the exact critical-damping/EP2 result for a licensed passive positive-curvature second-order companion system,

[
ddot q+gammadot q+Omega^2q=0,
qquad Omega^2>0,
]

for which the discriminant is genuinely

[
gamma^2-4Omega^2
]

and the repeated-root boundary is (gamma=2Omega).

Cross-domain recurrence must therefore be rebuilt from domain-licensed generators rather than preserved by notation.
