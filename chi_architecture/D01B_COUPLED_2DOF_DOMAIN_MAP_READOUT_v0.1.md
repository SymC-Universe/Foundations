# D01B Coupled 2DOF Domain Map Readout v0.1

**Date:** 2026-09-22  
**Status:** P0-D WITHIN-DOMAIN READOUT / POST-RESULT INTERPRETATION  
**Authority:** SymC General Operations Manual v0.8.3  
**Parent plan:** D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json  
**Execution freeze:** D01B_EXECUTION_FREEZE_v0.1.json  
**Claim ceiling:** mathematical and synthetic within-domain evidence only; not physical inheritance evidence and not cross-domain confirmation

## Provenance

The frozen D01B recovery workflow completed successfully in GitHub Actions run 34860174294 on 2026-09-14.

- artifact: chi-architecture-d01b-domain-map-v01-recovery
- artifact ID: 10355685958
- artifact digest: sha256:d3ec2f01d1a8faa3e636dddacddbd3bc4bb60d75eb0a6b7961fbdb97cc17478f
- result file: D01B_COUPLED_2DOF_DOMAIN_MAP_v0.1.json
- result SHA-256: 07224a81e860ec97ae7f222268bb255036b2d4eccf9a7344ae49455aefb746ec
- Python: 3.12.14
- NumPy: 2.3.5
- SciPy: 1.17.0

The run retained all 1,152 frozen parameter cases and both frozen perturbations per case, for 2,304 response records. No master system chi was searched or emitted.

## 1. Frozen-map result

All 1,152 parameter cases were asymptotically stable and all 2,304 responses settled within the fixed 0-240 observation window.

Exact real modal scalarization was admitted in 227/1,152 cases (19.7049%) and refused in 925/1,152 cases (80.2951%).

The largest numerical energy-balance residual fraction was 0.00339649, below the predeclared 0.02 workflow guard.

Across the full frozen map:

- minimum observed 2% settling time: 3.1;
- maximum observed finite 2% settling time: 78.7;
- largest receiving-component peak energy fraction: 0.719295;
- maximum RMS spectral displacement from the corresponding uncoupled system: 1.414214.

These are descriptive Function/Limit Map outputs, not fitted acceptance thresholds.

## 2. Exact modal-scalarization compatibility condition

For M=I and the frozen matrices

K = [[k1+kc,-kc],[-kc,k2+kc]]

and

C = [[c1+cc,-cc],[-cc,c2+cc]],

classical real modal decoupling requires C and K to be simultaneously orthogonally diagonalizable. For real symmetric C and K this is equivalent to [C,K]=0.

For the D01B construction the off-diagonal commutator factor reduces exactly to

D = kc(c2-c1) + cc(k1-k2).

Therefore,

D = 0

is the exact compatibility surface for real modal scalarization in this model.

Applying this symbolic condition to the frozen grid predicts exactly 227 scalarizable cases, with zero mismatches against the numerical admission result.

This condition is established classical-damping mathematics, not a new theorem of SymC. Its role here is as a controlled boundary for asking when local scalar coordinates can or cannot survive embedding as independent real modal coordinates.

## 3. Fixed local chi does not fix embedded behavior

For every intrinsic component tuple (k1,k2,c1,c2), D01B varies 24 coupling configurations while preserving both isolated-component coordinates

chi1 = c1/(2 sqrt(k1)),
chi2 = c2/(2 sqrt(k2)).

There are 48 such intrinsic tuples.

Forty-four of the 48 tuples contain both scalarizable and non-scalarizable coupled realizations as coupling changes. Only the four equal-component tuples with k1=k2=1 and c1=c2 remain exactly real-modal scalarizable for all 24 coupling configurations.

The coupling-only perturbation consequences are large despite fixed local chi and fixed isolated component dynamics:

- largest coupling-only 2% settling-time span: 5.9 to 78.2 for the same intrinsic tuple (k1,k2,c1,c2)=(1,0.5,2,0.1), perturbing component 2. The local coordinates remain chi1=1 and chi2=0.0707107. The span is 13.25-fold.
- largest coupling-only state-norm-integral span: 1.78209 to 20.03429 for (1,0.5,0.1,2), perturbing component 1.
- largest coupling-only receiving-component peak-energy span: 0 to 0.719295 for (1,0.5,0.1,0.1), perturbing component 2.
- median coupling-induced settling-time range across the 96 intrinsic-tuple/perturbation strata is 12.4 time units.

Within this frozen synthetic domain, the pair of isolated local chi values therefore does not determine the embedded perturbation response.

This is a direct D01B realization of the GOM distinction between local dynamical identity and embedded realized behavior. It is not physical evidence that every real system behaves this way.

## 4. Exact invariant-mode inheritance in the symmetric subfamily

A sharper result occurs for equal intrinsic components:

k1=k2=k,
c1=c2=c.

Using symmetric and antisymmetric coordinates

qs = (q1+q2)/sqrt(2),
qa = (q1-q2)/sqrt(2),

the system decouples exactly into

qs_ddot + c qs_dot + k qs = 0,

qa_ddot + (c+2cc) qa_dot + (k+2kc) qa = 0.

Thus the symmetric collective mode inherits the isolated component coordinate exactly:

chi_s = c/(2 sqrt(k)),

independent of kc and cc.

The antisymmetric branch is transformed by the embedding:

chi_a = (c+2cc)/(2 sqrt(k+2kc)).

This gives an exact model-level example in which coupling organization simultaneously preserves one scalar lineage and transforms another. The broader coupled architecture determines which statement is true.

For the frozen equal critical subfamily k=1, c=2,

chi_s = 1

for every coupling pair in the grid. The symmetric state-space block is therefore critically damped for every kc and cc.

Critical damping of a second-order oscillator is an EP2 of its 2x2 state-space generator: the repeated eigenvalue has algebraic multiplicity two and geometric multiplicity one. Accordingly, the symmetric critical branch is an exact coupling-invariant EP2 within this idealized symmetric D01B model.

This is an exact mathematical inheritance result inside the declared model. It is not a claim that a microscopic material exceptional point has been observed or that EP inheritance is generic.

## 5. Limit-map warning: repeated poles are not all EPs

The frozen map contains 19 cases with machine-zero minimum pole separation. They do not all have the same structure.

Examples include:

- critically damped component or modal blocks, which are defective EP2 cases;
- identical uncoupled underdamped oscillators, which produce repeated eigenvalues with independent eigendirections and are ordinary semisimple degeneracies.

Therefore numerical pole coincidence alone cannot classify an exceptional point. Structural defectiveness or an equivalent validated criterion is required.

This directly reinforces GOM v0.8.3 Section 18.1.

## 6. Literature collision and novelty boundary

The modal-scalarization condition is classical normal-mode theory. Caughey and O'Kelly established the necessary and sufficient condition that damping be diagonalized by the same transformation that uncouples the undamped system; for M=I and real symmetric matrices this is the C-K commutation condition. Later work places this result in the general simultaneous-diagonalization framework.

Likewise, critical damping as an exceptional point of the damped-oscillator state-space generator is established in the exceptional-point literature.

Therefore neither fact is claimed as new mathematics here.

The program-specific result is narrower: D01B uses a prospectively frozen coupling/perturbation map to distinguish three states that a local scalar-only reading would conflate:

1. local chi retained but embedded response reorganized;
2. exact real modal scalarization refused because coupling breaks compatibility;
3. a symmetry-protected invariant branch that inherits the local chi exactly while another branch is transformed.

Whether this architecture has added scientific value beyond standard native modal/state-space analysis remains an open question requiring independent physical and prospective tests.

## 7. Joint lowercase chi / broader Chi interpretation

D01B supports the following bounded interpretation:

- lowercase local chi remains a valid coordinate of each isolated licensed second-order component;
- local chi values alone are generally insufficient to reconstruct the coupled response;
- coupling structure is required to determine whether real modal scalarization exists and how perturbations are redistributed;
- in invariant subspaces, a local chi lineage can be preserved exactly;
- broader Chi must therefore retain at least the coupling/carrier organization needed to determine preservation, transformation, or refusal.

Symbolically, the frozen model supports

local chi information + coupling/carrier organization -> embedded behavior,

while the reverse compression

local chi pair -> embedded behavior

fails in general across the D01B grid.

No unique master Chi scalar is inferred.

## 8. Evidence status and promotion debt

D01B is P0-D/P0-Q within-domain evidence. It was executed with NSD P0D14/P0D15/P0D16/P0D17/P0D19 already declared as known context, so it is not untouched confirmation of generalized coupling or architecture hypotheses.

The invariant-mode inheritance interpretation was recognized after viewing D01B output and is therefore entered separately in the post-result discovery ledger. It cannot be promoted by reinterpreting this same result.

## 9. Next controlled step

The next domain step remains D01C, the predeclared non-normal extension.

Before execution, D01C must receive its own pre-execution freeze with parameter ranges chosen from native non-normal dynamics rather than from favorable D01B outcomes. D01B is now known context and must be recorded as such.

D01C should test whether spectrum/local decay coordinates remain adequate when eigenvector geometry, transient amplification, resolvent gain, and pseudospectral sensitivity vary independently. No scalar chi is presumed.
