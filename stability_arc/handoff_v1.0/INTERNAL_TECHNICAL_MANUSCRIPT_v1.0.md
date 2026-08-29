# Coupled Scalar-Modal Stability Architecture for Measurement-Conditioned Open Dynamics

## Internal Technical Manuscript v1.0

**Status:** internal architecture closure for program use  
**Science freeze anchor:** `5a1c0d3a579f0251374544973c1ff53194bba722`  
**Not a submission manuscript**

## Abstract

The Stability Arc program began from a simple and useful scalar boundary in second-order dissipative dynamics,

\[
\chi=\frac{\Gamma}{2\Omega},
\]

where damping and reversible oscillation can be compared in one coordinate and the repeated-root condition occurs at \(\chi=1\). The present investigation asked what survives when the system is no longer adequately described by one damped second-order mode, with continuous quantum measurement serving as the adversarial test case.

The result is neither the abandonment of scalar stability coordinates nor their promotion to universal sufficiency. The current evidence supports an internal architecture in which stability is represented by a coupled scalar-modal description. Scalar coordinates quantify damping, decay, algebraic stability margins, or boundary proximity. Modal and vector structure identifies the perturbation directions, modes, subspaces, and channels to which those scalar quantities belong. Their assignment and coupling are part of the stability description. In general, neither scalar data nor modal geometry alone provides the full state of the problem.

For continuously measured open quantum systems, same-noise physical perturbations and same-record inference perturbations were derived and independently audited. Their joint representation preserves both channels and the conditioning-induced difference rather than averaging them. Where an independently reconstructed dark factor permits an exact two-dimensional active quotient, a deterministic Stability Arc coordinate

\[
\chi_{\rm active}
=
-\frac{\operatorname{tr}A_A}{2\sqrt{\det A_A}}
\]

is legitimate and exactly reduces to \(\Gamma/(2\Omega)\) for the canonical oscillator. The stochastic tangent, however, requires the matrix pair \((A_A,B_A)\). Mean-square stability is governed by the lifted second-moment generator \(G(A_A,B_A)\) and the complete cubic Routh-Hurwitz conditions, not by a single stochastic analogue of \(\chi\).

Broad stress tests falsified universal monotonic improvement under measurement conditioning and demonstrated that decay-rate ordering and algebraic stability margins can move in opposite directions. Fresh prospective tests subsequently established bounded physical-STABLE to same-record-UNSTABLE crossings and isolated a `c3` gate mechanism within registered families, while a later test demonstrated that `c3` alone is insufficient for full stability classification because other margins can already fail. The architecture transferred to general planar measurement and to an independently augmented pure-dephasing generator. Two final untouched-seed blind reveals in the targeted dephasing family each reproduced 64/64 registered crossings with zero counterexamples.

The internal conclusion is therefore a reporting and reasoning architecture rather than a new universal scalar law: stability should be carried as scalar quantities attached to identified modal and directional structure, with refusal when the reduction is not justified.

## 1. Why this investigation was necessary

Chemistry and the broader SymC program forced a foundational question. If the original Stability Arc coordinate is clean in a damped oscillator, what exactly should be inherited when the physical system is multimode, stochastic, non-normal, measured, or only partially observable?

There are two easy but scientifically dangerous answers.

The first is to assume that every sufficiently complicated system must secretly possess one scalar that plays the role of \(\chi\). That invites circularity because a scalar can be selected or tuned after inspecting which candidate best reproduces a desired boundary.

The second is to discard scalar information entirely and declare the full matrix or vector field the only meaningful object. That loses real physical compression when a well-defined mode or quotient does possess a legitimate scalar damping coordinate.

The audit program instead treated the issue as an admissibility problem. We asked what representation is justified by the dynamics before asking whether it predicts any desired outcome. That distinction is the basis of the present handoff.

## 2. The scalar-modal principle

The mature internal interpretation is:

\[
\boxed{\text{stability information} =
\text{scalar magnitude}
+
\text{modal/directional structure}
+
\text{their assignment and coupling}}
\]

The plus signs here do not imply arithmetic addition. They indicate jointly required information.

A scalar may answer questions such as:

- how strongly a mode decays;
- whether a repeated-root morphology is approached;
- how far a Routh-Hurwitz margin lies from zero;
- which side of a scalar boundary a particular identified mode occupies.

A modal or vector quantity may answer:

- which perturbation direction the scalar describes;
- which active sector or eigenmode is involved;
- how state orientation changes the relevant dynamics;
- whether two channels even possess corresponding modes;
- whether a dark/active decomposition exists.

The coupling between them tells us that a scalar belongs to a specific mode or subspace rather than floating free of its physical carrier.

This is why two systems can share the same scalar coordinate while differing materially in mode geometry, and why two systems can share similar mode directions while lying at very different scalar distances from instability.

## 3. Conditional quantum dynamics as the adversarial case

For the registered single-observable convention, the conditional stochastic master equation was written

\[
d\rho
=
\mathcal L(\rho)\,dt
+
\sqrt{2\eta\kappa}\,
\mathcal H_x(\rho)\,dW,
\]

with

\[
\mathcal H_x(\rho)
=
x\rho+\rho x-2\operatorname{Tr}(x\rho)\rho.
\]

Let \(\delta\rho\) be a traceless perturbation and

\[
\delta\mu=\operatorname{Tr}(x\,\delta\rho).
\]

The same-noise physical tangent is

\[
d(\delta\rho)
=
\mathcal L(\delta\rho)\,dt
+
\sqrt{2\eta\kappa}\,
\delta\mathcal H_x\,dW,
\]

where

\[
\delta\mathcal H_x
=
x\delta\rho+\delta\rho x
-2\mu\,\delta\rho
-2\delta\mu\,\rho.
\]

The same-record inference tangent contains the additional deterministic conditioning term,

\[
d(\delta\rho)
=
\mathcal L(\delta\rho)\,dt
+
\sqrt{2\eta\kappa}\,
\delta\mathcal H_x\,dW
-
4\eta\kappa\,
\delta\mu\,\mathcal H_x(\rho)\,dt.
\]

These channels answer different questions. Same-noise evolution measures physical sensitivity to perturbation under the same noise realization. Same-record evolution measures convergence or divergence of nearby state estimates conditioned on one detector record.

The first derivation audit independently validated both identities against finite differences, including exact second-order recovery and refusal controls. Their distinction is therefore not a semantic choice. It is mathematical structure that must remain recoverable in all later analysis.

## 4. Joint analysis without conflation

Keeping the channels separate does not mean they should never be studied together.

The corrective joint-channel audit established the conglomerate representation

\[
\mathcal C
=
(A_{\rm phys},A_{\rm rec},\Delta A,B,A_{\rm joint}),
\]

with

\[
\Delta A=A_{\rm rec}-A_{\rm phys}
=
-4\eta\kappa\,h\,m^T
\]

under the registered convention, and

\[
A_{\rm joint}
=
\operatorname{diag}(A_{\rm phys},A_{\rm rec}).
\]

The joint characteristic polynomial factors into the two channel characteristic polynomials, so the joint construction retains both spectra rather than replacing them with an averaged spectrum.

The common stochastic tangent matrix \(B\) and the rank-one conditioning update \(\Delta A\) make the relationship explicit. Fresh controls also showed nonzero commutators between \(A_{\rm phys}\) and \(A_{\rm rec}\). Conditioning can therefore reorganize modal structure rather than acting as a simple rescaling of all decay rates.

This is a concrete example of why scalar and modal information must be kept together.

## 5. When a scalar Stability Arc coordinate is legitimate

The active-quotient audit asked a narrower question: can the familiar scalar architecture survive on an objectively identified sector without compressing the full system?

For the registered fixtures, an independently reconstructed one-dimensional conditioning-dark factor left a real, asymptotically stable two-dimensional deterministic active quotient \(A_A\). On that admitted quotient,

\[
\chi_{\rm active}
=
-\frac{\operatorname{tr}(A_A)}
{2\sqrt{\det(A_A)}}
\]

was basis- and complement-invariant.

For canonical damped-oscillator controls this recovered exactly

\[
\chi=\frac{\Gamma}{2\Omega}.
\]

This is an important positive result. It means the original scalar is not merely historical notation. It is a legitimate coordinate when the system has the required two-dimensional mode structure.

But the audit also established refusal boundaries. The full three-dimensional generators remained `FULL_MATRIX_REQUIRED`; the stochastic term remained `STOCHASTIC_TERM_NOT_COMPRESSED`; invalid quotient dimension, instability, nonpositive determinant, degeneracy, defectiveness, nonreal quotient, coordinate failure, or nonidentifiable dark factor all required explicit refusal.

The correct internal interpretation is therefore not "scalar only when vectors fail" or "vectors only when scalars fail." It is that an admitted scalar coordinate is carried **with** the mode or quotient that licenses it.

## 6. Exact stochastic quotient closure

A deterministic factorization would not be enough if multiplicative noise leaked between dark and active sectors.

The stochastic dark/active audit therefore tested both

\[
A D\subset D
\]

and

\[
B D\subset D.
\]

For the admitted fresh fixtures, both held. With quotient map \(L\),

\[
LA=A_A L,
\qquad
LB=B_A L.
\]

The full stochastic tangent

\[
dr=A r\,dt+B r\,dW
\]

therefore descends exactly to

\[
dq=A_Aq\,dt+B_Aq\,dW.
\]

At second-moment level,

\[
(L\otimes L)K(A,B)
=
K(A_A,B_A)(L\otimes L).
\]

This establishes quotient closure, not noise-free dark dynamics. It also demonstrates why the deterministic \(\chi_{\rm active}\) cannot by itself describe the stochastic system. The stochastic carrier is the matrix pair \((A_A,B_A)\).

## 7. Mean-square stability and the invariant vector

For

\[
dq=A_Aq\,dt+B_Aq\,dW,
\]

the covariance-like second moment

\[
P=E[qq^T]
\]

evolves as

\[
\frac{dP}{dt}
=
A_AP+PA_A^T+B_APB_A^T.
\]

Using the symmetric coordinates

\[
m=(p_{11},p_{12},p_{22})^T,
\]

this becomes a real three-dimensional linear system with generator

\[
G(A_A,B_A).
\]

Writing

\[
\det(\lambda I-G)
=
\lambda^3+c_1\lambda^2+c_2\lambda+c_3,
\]

strict mean-square asymptotic stability requires

\[
c_1>0,
\qquad
c_2>0,
\qquad
c_3>0,
\qquad
c_1c_2>c_3.
\]

The characteristic triple and final Hurwitz combination provide scalar invariant information, while the quotient modes and state orientation retain the directional structure to which those invariants belong.

A critical control separated two concepts that had previously been easy to blur. Noiseless oscillator cases at \(\chi=0.5\), \(1\), and \(1.5\) were all mean-square stable. The undamped \(\Gamma=0\) case was the mean-square boundary. Thus \(\chi=1\) remains a repeated-root or damping-morphology boundary in the deterministic second-order problem. It is not the general mean-square stability boundary.

## 8. Failure of one-dimensional stability ordering

The broad conditioning stress test produced one of the most useful negative results.

A preregistered hypothesis that same-record conditioning would monotonically improve the mean-square spectral abscissa failed in 441 admitted cases.

Among the stable counterexamples, the dominant decay rate became less negative even while every registered cubic Routh-Hurwitz margin increased.

That means two perfectly legitimate scalar summaries of "stability" can move in opposite directions:

- spectral-abscissa decay ordering;
- algebraic distance through Hurwitz margins.

This is not a contradiction. They measure different properties.

The result directly rejects a one-dimensional ordering of stability and is one of the strongest reasons to preserve a multicoordinate scalar component attached to modal structure rather than seeking a single master number.

The failed H2 remains permanently failed.

## 9. Class crossings and boundary geometry

A bounded adversarial panel initially supported class preservation. A later fresh targeted test then falsified universal class preservation.

In H4, 100,000 new cases were generated. Stage A used only the permitted physical information and froze 52,435 robust physical-STABLE cases before the same-record outcomes were exposed. Fifty physical-STABLE to record-UNSTABLE crossings were identified and all 50 independently reconstructed.

Post-outcome inspection suggested that the crossings were passing through the record-side \(c_3<0\) gate while the other Routh-Hurwitz conditions remained positive. Because that observation was post-hoc, it was not counted as confirmation.

The subsequent H5 test used fresh evidence and prospectively registered that mechanism. It froze 52,944 physical robust-STABLE cases before reveal, found 54 crossings, independently reconstructed all 54, and observed zero preregistered \(c_3\)-pattern counterexamples.

The exact \(c_3\) boundary was separately derived. A numerical audit then failed near roots because ordinary binary64 determinant evaluation lost precision. That failure was preserved. A separate 80-digit remediation passed under the unchanged tolerance, so the mathematical boundary was supported without rewriting the original numerical-oracle failure.

## 10. Why one scalar gate was still insufficient

The H6 full-class test was designed to attack the tempting conclusion that a correct \(c_3\) displacement map might be enough.

It failed decisively.

All 512 registered `I_destab` predictions were already physically unstable through the \(c_1\) gate before the record-conditioned crossing was considered. The `I_stab` side was correct in its bounded panel, but the failure proved that \(c_3\) alone does not classify the full stability state.

The exact \(c_1\) relation was then derived. In the sigma-z representation,

\[
c_{1,\rm rec}-c_{1,\rm phys}
=
6q(1-z^2)\ge0.
\]

A subsequent broad-frame test encountered a selection hold because the relevant geometry was concentrated extremely near the pure-state boundary. Stratified fresh tests localized that admissibility structure rather than relaxing the rules.

H9 then tested the near-pure orientation effect prospectively. In the registered R4 shell, 33 fresh negative-orientation cases were eligible, zero positive-orientation cases were eligible, and all 33/33 negative-orientation cases were full physical-STABLE to record-UNSTABLE crossings. This is a bounded result, not a universal orientation law.

The exact orientation algebra subsequently showed that orientation sign enters \(c_3\) affinely while \(c_1\) is sign-independent in that representation.

The lesson is architectural: scalar boundary values become physically interpretable only after their modal and state-direction assignment is preserved.

## 11. General planar measurement

The next attack changed measurement geometry.

A fixed 45-degree measurement axis preserved the exact one-dimensional dark factor and two-dimensional stochastic quotient. A generic out-of-plane axis correctly returned `REFUSE_NO_1D_DARK_FACTOR`.

For the full planar family

\[
n(\theta)=(\sin\theta,0,\cos\theta),
\]

the exact structural boundary was

\[
\Delta_{\rm obs}
=
\omega-\frac{\gamma}{4}\sin(2\theta).
\]

The measurement strength \(\kappa\) cancels from this observability boundary.

Away from \(\Delta_{\rm obs}=0\), the maximal dark factor is exactly \(\operatorname{span}(e_y)\) and the stochastic tangent descends to a two-dimensional quotient. At the exact boundary the dark dimension becomes two, so the correct action is `REFUSE_QUOTIENT_DIMENSION`, not to force the old representation.

In measurement-aligned coordinates \(u,v\), define

\[
q=\eta\kappa,
\]

\[
p=\frac{\gamma(1+\cos^2\theta)}{2},
\]

\[
d=\kappa+\frac{\gamma(1+\sin^2\theta)}{2},
\]

\[
h=\frac{\gamma}{4}\sin(2\theta).
\]

Then

\[
A_{\rm phys}
=
\begin{bmatrix}
-p & h-\omega\\
h+\omega & -d
\end{bmatrix},
\]

\[
B
=
-\sqrt{2q}
\begin{bmatrix}
2u & 0\\
v & u
\end{bmatrix},
\]

and

\[
A_{\rm rec}
=
A_{\rm phys}
+
\begin{bmatrix}
-2q(1-u^2)&0\\
2quv&0
\end{bmatrix}.
\]

The full separate physical and record-conditioned \((c_1,c_2,c_3)\) triples follow exactly from this quotient.

## 12. Transfer to an independent dissipation family

The next extension changed the generator itself by adding pure dephasing,

\[
\sqrt{\gamma_\phi/2}\,\sigma_z,
\]

alongside amplitude damping.

Define

\[
a=\gamma/2+\gamma_\phi,
\qquad
b=\gamma.
\]

The planar structural boundary becomes

\[
\Delta_\phi
=
\omega-(b-a)\sin\theta\cos\theta.
\]

The canonical quotient retains the same algebraic structure with

\[
p=a\sin^2\theta+b\cos^2\theta,
\]

\[
d=\kappa+a\cos^2\theta+b\sin^2\theta,
\]

\[
h=(b-a)\sin\theta\cos\theta.
\]

The parent structural-transfer run suffered an implementation failure because one Python identifier was reused and overwrote a boolean result. The parent remains permanently classified as an audit implementation failure. A separately frozen remediation recomputed the affected symbolic identity with distinct identifiers and passed all gates. The transfer is therefore composite-closed through the explicit failure-plus-remediation lineage.

This lineage is intentionally retained because a handoff architecture that hides its own implementation failures would be less trustworthy, not more.

## 13. Dephasing crossing transfer and final blind replication

The broad H10 dephasing panel contained 1.2 million fresh systems across four radial strata.

The stabilizing direction produced 128 frozen cases and passed 128/128 with zero counterexamples.

The destabilizing direction produced only two eligible cases, both correct, which was below the preregistered minimum. That result was a selection hold, not a pass.

H11 therefore performed a post-H10 availability search only. It generated 10 million fresh high-radius systems, using only the already-licensed structural and \(c_1/c_3\) information. It found 69 eligible cases and froze the first 64 before hidden full stability was computed.

The H11 blind reveal then independently reconstructed all 64 from the full Hilbert-space model. All 64 were physical-STABLE to same-record-UNSTABLE, with zero counterexamples, boundaries, reconstruction failures, or hidden \(m_2/m_h\) blockers.

H12 was preregistered as the one-time same-family untouched-seed replication. Its Stage A generated another 10 million fresh systems, found 71 eligible cases, froze the first 64, and did not compute hidden full stability. The blind reveal again produced 64/64 physical-STABLE to same-record-UNSTABLE with zero counterexamples or holds.

The stop rule was then reached. Additional repetitions of the same targeted family would add sample size without adding the independent physics needed for the next scientific claim.

## 14. What is actually established

For internal program use, the evidence supports the following architecture:

1. A governing generator or response operator must be identified before stability coordinates are interpreted.
2. Scalar coordinates are meaningful when their physical carrier is defined.
3. Modal/vector/subspace geometry is required to identify that carrier.
4. The assignment between scalar quantities and modes is part of the result.
5. Distinct physical and inference channels may be compared jointly, but their identities must remain recoverable.
6. Stochastic dynamics can require lifted invariant vectors even when deterministic quotient scalars exist.
7. Different stability metrics can rank the same system differently without inconsistency.
8. Refusal and nonidentifiability are legitimate outcomes.
9. A repeated-root boundary, an asymptotic stability boundary, a mean-square stability boundary, an observability boundary, and a localization criterion are different objects unless separately proven to coincide.

## 15. What is not established

This work does not show that:

- one universal scalar governs all stable dynamics;
- modal geometry alone determines stability;
- \(\chi=1\) is a universal optimum;
- \(\chi=1\) is the stochastic mean-square boundary;
- measurement conditioning always stabilizes or always destabilizes;
- the bounded orientation and radius findings are universal;
- the architecture predicts localization, collapse, or measurement quality;
- the historical unrecovered QuTiP source has been reproduced;
- the quarantined GFSA external candidate may be numerically admitted.

## 16. Chemistry implication

The chemistry program should inherit the **representation discipline**, not only a formula.

For a chemically relevant mode that genuinely reduces to a real stable two-dimensional second-order block, a \(\chi\)-type coordinate remains useful and should be reported.

But it must be carried together with:

- the mode identity and eigenvector/subspace;
- the generator or Hessian/dynamical object from which it was obtained;
- neighboring modes and degeneracy information;
- applicable uncertainty and numerical conditioning;
- any competing scalar stability margins;
- the explicit reduction or refusal status.

For multimode or stochastic chemistry, a vector of stability invariants plus modal geometry may be the correct object. The goal is not to force every chemical problem into one number. The goal is to preserve the relation between magnitude and direction that makes the number physically interpretable.

## 17. Internal closure decision

The current work is mature enough to pause for program use because the foundational question that motivated the rabbit hole has been answered:

**Stability Arc should be inherited as a coupled scalar-modal architecture with explicit admissibility and refusal, not as either a standalone scalar law or an unstructured full-matrix fallback.**

Future publication work should attack this architecture with a genuinely independent generator or geometry rather than accumulating additional replicas of the same dephasing family.
