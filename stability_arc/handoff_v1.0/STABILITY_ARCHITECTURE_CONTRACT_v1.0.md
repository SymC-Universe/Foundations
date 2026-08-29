# Stability Architecture Contract v1.0

**Status:** canonical internal reporting contract  
**Science anchor:** `5a1c0d3a579f0251374544973c1ff53194bba722`

## 1. Purpose

This contract defines what other program branches are allowed to mean by a Stability Arc representation after the measurement-conditioned investigation.

It is a reporting and admissibility contract. It is not a new universal physical postulate.

## 2. Required representation

For internal use, record a stability analysis as

\[
\mathcal S_{\rm report}
=
(\mathcal G;
\mathbf s,
\mathcal V,
\mathcal C,
\mathcal R,
\mathcal U).
\]

### \(\mathcal G\): governing dynamics

The operator from which stability is actually derived, such as a dynamical generator, Jacobian, tangent operator, response operator, Hessian-derived local dynamics, or explicitly justified reduced model.

No stability coordinate may float free of its generating object.

### \(\mathbf s\): scalar coordinate set

All licensed scalar quantities needed for the question being asked. Examples include:

- \(\chi=\Gamma/(2\Omega)\) for an identified second-order mode;
- \(-\mathrm{tr}(A)/(2\sqrt{\det A})\) on an admitted real stable 2D quotient;
- decay rates or spectral abscissae;
- \(c_1,c_2,c_3,c_1c_2-c_3\);
- distances to registered scalar boundary surfaces;
- uncertainty-scaled residuals or other preregistered scalar diagnostics.

A scalar coordinate is not a system-wide verdict unless that scope has been independently established.

### \(\mathcal V\): modal/vector/subspace geometry

The directional carrier of the scalar information. Examples include:

- right and left eigenvectors when relevant;
- tangent directions;
- normal modes;
- active and dark subspaces;
- state orientation;
- mode participation or projection;
- invariant subspaces;
- mode correspondence across channels or parameter continuation.

### \(\mathcal C\): scalar-to-mode coupling map

The assignment telling the reader which scalar belongs to which mode, direction, pair, or subspace.

A report that lists eigenvalues and eigenvectors separately without preserving their correspondence is incomplete.

A report that lists a scalar boundary coordinate without its modal carrier is also incomplete when more than one physically distinct mode exists.

### \(\mathcal R\): inter-channel relations

When multiple dynamical descriptions are legitimately present, preserve their relationship.

For the measurement-conditioned branch:

\[
\mathcal R
=
(A_{\rm phys},A_{\rm rec},\Delta A,B,A_{\rm joint}),
\]

with physical same-noise and same-record inference channels separately recoverable.

Other domains may define different channel relations, but may not average them into a single object unless that reduction is preregistered and independently justified.

### \(\mathcal U\): uncertainty, admissibility, and refusal state

Record:

- numerical uncertainty;
- measurement or fit uncertainty;
- conditioning and identifiability diagnostics;
- reduction assumptions;
- frozen tolerance or gate;
- PASS/FAIL/NONIDENTIFIABLE/REFUSE status;
- provenance and source hashes when material.

## 3. Scalar and modal information are jointly required

The contract does not rank scalar information above modal information or modal information above scalar information.

The scalar component answers magnitude and boundary questions.

The modal component answers carrier, direction, and assignment questions.

The coupled object answers the physical question.

## 4. Admissible \(\chi\)-type reduction

A \(\chi\)-type scalar may be reported when one of the following is independently justified:

1. the physical model is genuinely an identified second-order damped mode with \(\Gamma\) and \(\Omega\);
2. an independently reconstructed real, stable 2D quotient exists and the registered invariant
   \[
   \chi_A=-\frac{\mathrm{tr}A}{2\sqrt{\det A}}
   \]
   is applicable;
3. a future preregistered derivation licenses another mathematically equivalent reduction.

Even then, report the mode/subspace to which the scalar belongs.

## 5. Mandatory refusal

Do not manufacture a scalar if the required reduction is absent.

Examples from the closed quantum branch include:

- `FULL_MATRIX_REQUIRED`;
- `STOCHASTIC_PAIR_NOT_COMPRESSED`;
- `MEAN_SQUARE_INVARIANTS_REQUIRED`;
- `REFUSE_QUOTIENT_DIMENSION`;
- `REFUSE_NONIDENTIFIABLE_DARK_FACTOR`;
- `REFUSE_STOCHASTIC_LEAKAGE`;
- `REFUSE_DEFECTIVE_ACTIVE_SECTOR`;
- `REFUSE_NONREAL_QUOTIENT`;
- `NONIDENTIFIABLE`.

Equivalent domain-specific refusal states are allowed and encouraged.

## 6. Distinct boundary types

Never identify these boundaries without an independent derivation:

- repeated-root / damping-morphology boundary;
- asymptotic stability boundary;
- mean-square stability boundary;
- exceptional-point condition;
- observability/identifiability boundary;
- localization or measurement-quality optimum;
- kinetic turnover or reaction-rate boundary.

The closed oscillator controls explicitly show that \(\chi=1\) can be a repeated-root boundary while not being the mean-square stability boundary.

## 7. Multicoordinate stability

A vector of scalar invariants may be required.

For the admitted 2D stochastic quotient, the complete mean-square conditions are:

\[
c_1>0,\quad
c_2>0,\quad
c_3>0,\quad
c_1c_2>c_3.
\]

No one component should be substituted for the full condition unless a theorem or preregistered restricted result justifies it.

H6 is the permanent counterexample to treating \(c_3\) alone as full-class sufficient.

## 8. Cross-channel and cross-domain comparison

Before comparing stability coordinates:

- match the physical definition;
- match the mode or subspace;
- match the generator class;
- match the observation bandwidth and uncertainty model where relevant;
- state any coordinate transform;
- freeze the comparison rule before outcome inspection.

Do not pool raw coordinates across generator or boundary classes merely because the numerical scales look similar.

## 9. Failure handling

Every failure remains part of the architecture.

A failed preregistered rule may generate a new hypothesis but may not be rewritten as success.

Mechanical repairs receive a new execution lineage and may not alter scientific gates.

Post-hoc observations require new preregistration and fresh evidence.

## 10. Minimum compliant record

A Stability Arc result is internally compliant only if a future reader can recover:

1. governing dynamics \(\mathcal G\);
2. scalar set \(\mathbf s\);
3. modal/subspace set \(\mathcal V\);
4. scalar-to-mode assignment \(\mathcal C\);
5. inter-channel relation \(\mathcal R\), if applicable;
6. uncertainty/admissibility \(\mathcal U\);
7. frozen decision rule;
8. provenance sufficient to reconstruct the result.

## 11. Interpretation rule

The program may say:

> the system occupies this scalar-modal stability state under the stated generator and admissibility contract.

The program may not say:

> this one number is the stability of the system

unless the reduction itself has been independently established for that system.
