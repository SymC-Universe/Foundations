# Cosmology RQE Current Evidence State — 2026-09-30

**Status:** PARTIALLY POPULATED; ACTIVE-RUN-DEPENDENT VALUES REMAIN PENDING  
**Rule:** This record uses only already-canonical results in the repository. It does not inspect or infer from the active local Python computation.

## F1 — local \(\chi\)

**Current classification:** coordinate_only for the tested late-time background construction.

Evidence:
- flat-\(\Lambda\)CDM numerical identity:
\[
\max|z_{q=0}-z_{\chi_\delta=1}|=5.33\times10^{-15};
\]
- in constant-\(w\)CDM, \(\Delta z\) is strongly correlated with \(w\), \(r\approx-0.97\);
- \(q(a)\) and \(\chi_\delta(a)\) are algebraically linked once the flat GR matter+smooth-DE background model is specified;
- BAO-only \(w_0w_a\) exhibits multiple \(q=0\) crossings in about 60.7% of posterior resamples, demonstrating failure of an unlabeled scalar \(\Delta z\) when transition topology is non-unique.

Disposition:
- retain \(\chi_\delta\) as a useful stability coordinate;
- prohibit treating it as an independent background degree of freedom;
- preserve transition sets when scalar compression loses branch structure.

Source/reference: [Chr26].  
Canonical evidence: results/DESI_DR2_BAO_INDEPENDENT_GATE_2026-09-29.md.

## F2 — modal necessity

**Current status:** PENDING_ACTIVE_COMPUTE / NEED_MORE_INFO.

Already-qualified supporting evidence:
- DR1 ShapeFit engineering points are consistent with the fiducial growth history and show no simple overall offset or redshift trend;
- this does not decide whether full-shape/modal structure carries additional information.

Required next evidence:
- resolved growth/full-shape representation;
- information eigen-spectrum / \(d_{\rm eff}\) or equivalent;
- lower-order compressed/scalar comparator;
- held-out predictive/discriminating score.

Sources/references: [Nad16, Lee26b, Sui25, Hea20, Bas19].

## F3 — aggregate \(\Chi\)

**Current status:** NOT YET EVALUABLE.

Reason: no candidate capital-\(\Chi\) construction may be frozen until F2 establishes which modal components are scientifically qualified.

Required next evidence:
- explicit candidate \(\Chi\);
- conditional incremental-information test;
- matched-complexity marginal null;
- relation-destroying null where admissible.

Sources/references: [Sui25, Nad16].

## F4 — Stability Arc

**Current status:** BACKGROUND ARC IS DESCRIPTIVELY QUALIFIED; INCREMENTAL ARC VALUE NOT YET EVALUATED.

Established:
- background transition trajectory is well-defined in flat \(\Lambda\)CDM and can be generalized to transition sets in non-monotonic cases;
- the background Arc alone does not establish new dynamics because its current scalar ingredients are model-linked.

Required next evidence:
- static-state versus trajectory comparison after F2/F3;
- held-out target demonstrating trajectory-specific value.

Sources/references: [Chr26, Roy11, Wie10].

## F5 — Stability Inheritance

**Current status:** NEED_MORE_INFO.

No cosmological SI carrier has yet passed an incremental predictive test against standard transfer/history variables.

Required:
- explicit measurable inheritance map;
- comparison against standard growth/transfer/initial-condition history;
- lineage-destroying null;
- prospective later-state target.

Sources/references: [Vru21, Wie10].

## F6 — joint DM/DE function

**Current status:** PARTIALLY QUALIFIED COMPARATOR SPACE; ARCHITECTURE VALUE UNTESTED.

Canonical comparator evidence already available:
- flat-\(\Lambda\)CDM DR1 reference posterior is stable;
- DESI-only modified-gravity freedom causes only small shifts in \(\Omega_m,\sigma_8,H_0,S_8\), with dominant new degeneracy in \(\mu_0\)-\(\log A_s\);
- free neutrino mass materially affects the growth-amplitude sector but does not absorb the common \(w_0>-1,\;w_a<0\) direction in the matched physical-DE suites;
- Pantheon+, Union3 and DESY5 share the same directional \(w_0,w_a\) behavior but differ non-negligibly in exact location;
- matched released minima favor \(w_0w_a\) over \(\Lambda\)CDM by differing amounts across the three SN combinations, so sample dependence must remain explicit.

What is not yet shown:
- that the integrated \(\chi+\mathcal M+\Chi+\)SA+SI representation improves on conventional expansion-growth analysis.

Sources/references: [Roy11, Sha21, Bas19, Kun07b, Mar19, Per22, You26].  
Canonical evidence:
- results/DMDE_DR1_BASELINE_AUDIT_2026-09-29.md
- results/DMDE_DR1_MG_COMPARISON_2026-09-29.md
- results/DMDE_NEUTRINO_ADVERSARY_2026-09-29.md
- results/DMDE_DE_SUITE_ANALYSIS_2026-09-29.md
- results/DMDE_DE_BESTFIT_COMPARISON_2026-09-29.md

## F7 — adversarial transport

**Current status:** PARTIALLY POPULATED.

Already available:
- \(\Lambda\)CDM/GR reference;
- dynamical DE suite;
- free-neutrino-mass adversary;
- modified-gravity adversary;
- supernova-sample sensitivity.

Still missing for full architecture qualification:
- dataset-matched interacting-dark-sector adversary;
- architecture-level misspecification/rejection comparison;
- full representation-decision transport after F2-F6 are defined.

Sources/references: [Nic18, Hea20, Kun07b, Mar19, You26].

## Current RQE disposition

A final engine disposition is not admissible yet because F2-F5 and part of F7 remain unresolved.

The scientifically correct current state is:

\[
\boxed{\mathrm{NEED\ MORE\ INFO}}
\]

with one useful positive conclusion already locked:

\[
\boxed{\chi_\delta\ \text{is currently a qualified coordinate, not an independent background degree of freedom}.}
\]

No statement about the necessity of modal \(\mathcal M\), aggregate \(\Chi\), SA trajectory information, SI, or the full architecture is licensed until their incremental-value gates are executed.
