# Substrate Inheritance in Coupled Dynamical Systems: A Prospective Carrier-Resolved Evidence Architecture

**WORKING MANUSCRIPT DRAFT**  
**Not submission-ready. Not a preprint release. Not a physical inheritance claim.**  
**Program:** SymC Substrate Inheritance (SI)  
**Current maturity:** P0-D / P0-Q  
**Program authority:** SymC General Operations Manual v0.8.0  
**Last major synchronization:** 14 September 2026

---

## Abstract

Coupled systems routinely exhibit influence, hybridization, mode mixing, response transmission, and successful subsystem reduction. None of those phenomena alone establishes that a dynamically characterized parent or substrate has transmitted a specific organization to a child or embedded system. We develop a prospective, carrier-resolved evidence architecture for distinguishing generic substrate influence from a stronger candidate relation termed substrate inheritance. The architecture requires independent parent characterization, explicit carrier or subspace correspondence, a parent-to-child transformation rule fixed before target inspection, prospective prediction against an independently generated child object, intervention or counterfactual response, and specificity controls capable of defeating frequency-only, same-spectrum, generic-parent, or coupling-rewire explanations. Scalar coordinates are retained when physically licensed, but scalar, modal/subspace, and conglomeration/system descriptions are treated as complementary starting representations rather than a complete decomposition or a required omnibus score.

We qualify the architecture using synthetic and mathematical Function/Limit maps rather than treating the synthetic systems as physical evidence. A coupling-response landscape shows that fixed parent spectrum does not determine embedded response and that carrier geometry carries information missed by frequency-only matching. An embedding-depth landscape shows that the parent extent required for a declared reduction task is regime- and tolerance-dependent and can converge non-monotonically. A multi-generation lineage study demonstrates a negative method result: direct carrier geometry can reconverge exactly while sequential row-normalized lineage flow loses the end-to-end information. A hierarchical-closure study shows exact response preservation under exact nested Schur reduction for the declared linear quantities, while common approximate reductions can be highly accurate over much of the functioning interior yet fail by orders of magnitude in restricted regimes. Additional adversarial tests demonstrate scalar nonidentifiability, coupling-specific response dependence, subspace robustness under near-degeneracy, and fail-closed refusal when individual carriers cannot be resolved.

A targeted prior-art collision identifies modal tracking, component-mode synthesis, dynamic substructuring, uncertainty propagation, surface Green-function embedding, adsorbate-substrate hybridization, isotope controls, and substrate-driven adsorbate response as established native science. The residual question is consequently narrower: whether an independently characterized parent architecture supplies prospectively useful, uncertainty-aware, carrier-resolved information about a coupled child that is not reducible to ordinary frequency matching or generic influence, and whether any resulting effective inherited subsystem preserves the declared quantities required after re-embedding. No real-system substrate-inheritance result, physical inheritance threshold, system-wide chi, or universal cross-domain mechanism is claimed here. The present contribution is a falsifiable evidence architecture, its synthetic qualification, its demonstrated failure modes, and a bounded route to future physical testing.

---

## 1. Introduction

Physical systems are rarely isolated. Molecules couple to substrates, adsorbates hybridize with surface vibrations, components transmit forces through interfaces, reduced subsystems are embedded into larger assemblies, open systems exchange information and energy with their environments, and collective organization can emerge from couplings that are absent from the isolated parts. Mature native theories already describe many of these processes. Hybridization, normal-mode mixing, dynamic substructuring, component-mode synthesis, Green-function embedding, self-energy, mode tracking, transfer functions, and uncertainty propagation are not new concepts introduced by SI.

The scientific problem considered here is narrower and more demanding. Suppose a parent or substrate is characterized independently, before the target child or coupled system is examined. Does that parent architecture contain prospectively useful information about which carrier-resolved structures survive, transform, split, mix, disappear, or emerge after coupling? Can the proposed relation predict the child better than ordinary frequency similarity or generic coupling influence? Does a controlled parent intervention produce the predicted child change? When individual carriers become nonidentifiable, can the analysis retain subspace structure and uncertainty rather than force a favorable correspondence? If a coupled subsystem is later grouped and reused as a higher-level component, which response quantities remain preserved and where does closure fail?

We use **substrate inheritance** as a deliberately high-bar evidentiary label for that stronger relation. The terminology is not meant to rename ordinary influence. The program therefore distinguishes three evidence classes:

- **Substrate influence:** changing a parent or substrate changes a child or coupled-system observable, but stable parent-to-child carrier correspondence has not been established.
- **Conditional inheritance:** a specified scalar, mode, subspace, or system organization is transmitted under stated conditions through a prospective mapping rule, but the full inheritance evidence sequence is not complete.
- **Substrate inheritance:** a carrier-resolved parent architecture makes prospectively successful child predictions, survives intervention and specificity/null tests, and is not reproduced equally well by appropriate generic or scrambled controls.

This distinction makes failure informative. A system can show strong influence without inheritance. A scalar response can agree perfectly while the underlying coupling geometry remains nonidentifiable. An individual eigenvector can lose identifiability while its containing subspace remains stable. A reduced component can reproduce one local quantity while failing the higher-level quantity for which it was intended. These are not nuisances to be tuned away; they are boundaries of what the evidence supports.

The present manuscript reports the current P0-D/P0-Q architecture and its synthetic qualification. It does not report a confirmed physical inheritance result. The paper is organized around three goals: first, to define a fail-closed prospective evidence architecture; second, to test whether the architecture behaves correctly on known-truth and adversarial synthetic systems; and third, to isolate the residual physical question after comparison with established native methods and prior experiments.

### 1.1 Scope of the term chi in this program

The broader SymC research program uses chi-like stability coordinates where a native dynamical reduction licenses them. SI does not require a scalar chi for inheritance analysis. A local mechanical damping ratio, for example, belongs to its licensed second-order carrier and is not automatically a system-wide quantity. Lower-level chi values are never averaged into a system chi merely to produce one coordinate.

The fullest SI description may require scalar information, modal or subspace geometry, and conglomeration/system organization together. These are complementary starting representations. They are not a claim that chi is exactly three things, and a native system need not instantiate all three. `NOT_APPLICABLE` and an explicit open channel are preferred over manufacturing a missing representation for aesthetic symmetry.

---

## 2. Native context and residual scientific question

### 2.1 Established native methods

The mathematical and experimental primitives surrounding SI have substantial prior art. Modal Assurance Criterion methods and their descendants compare modal vectors and support mode tracking. Clustered-eigenvalue methods retain subspace information when individual vectors become unstable. Uncertainty-aware modal correlation has also been developed. Structural dynamics provides mature dynamic-substructuring and Component Mode Synthesis families, including Craig-Bampton-style reductions, static condensation, frequency-based substructuring, state-space substructuring, and input-output model reduction. Surface science provides Green-function embedding and semi-infinite substrate methods. Adsorbate-surface physics already demonstrates vibrational coupling and hybridization, and isotope substitution has been used to separate coupling effects from simple chemical or frequency shifts.

Accordingly, SI does not claim novelty for vector overlap, mode tracking, subspace tracking, Schur complements, component-mode synthesis, Green-function embedding, adsorbate-substrate coupling, isotope controls, or the fact that a substrate perturbation can alter an adsorbate response.

### 2.2 Residual question after literature collision

The surviving question is more specific:

> Does an independently characterized parent or substrate architecture provide prospectively useful, uncertainty-aware, carrier-resolved information about a child or coupled system that cannot be reduced to ordinary frequency matching or generic coupling influence, and if an effective inherited subsystem is formed, what higher-level quantities does it preserve after grouping or re-embedding?

The question contains both a **Function Map** and a **Limit Map**. We want to know where correspondence and embedded response behave usefully across ordinary conditions, but also where scalar compression, individual-carrier matching, finite-depth reduction, normalized lineage summaries, or approximate closure cease to preserve the required information.

### 2.3 Local identity and embedded behavior

A central relational distinction is

`LOCAL DYNAMICAL IDENTITY != EMBEDDED REALIZED BEHAVIOR`.

Where native science permits, the System Model therefore keeps separate records for:

1. the local or intrinsic parent/subsystem model;
2. outward coupling or transmitted signal;
3. transformation imposed by the connected environment or receiver;
4. feedback or return;
5. the embedded/closed-loop model;
6. which local properties survive, transform, disappear, or emerge after embedding.

A system-level claim cannot be justified solely by listing isolated component properties.

---

## 3. Prospective evidence architecture

### 3.1 Governing objects and carriers

An SI analysis starts from the native governing objects appropriate to the domain: dynamical matrices, generators, transfer operators, response functions, Green functions, experimentally estimated modal objects, or other domain-native representations. The relevant carrier may be an individual mode, a degenerate or nearly degenerate subspace, a reaction-coordinate-adjacent structure, an interface response, or another explicitly declared object.

The architecture separates at least the following candidate information layers where applicable:

- licensed scalar coordinates;
- modal/vector or subspace geometry;
- participation in the observed response;
- coupling and embedding structure;
- system-level or conglomerated organization;
- uncertainty and numerical conditioning;
- observability and identifiability;
- lineage/correspondence across transformations;
- higher-level closure after grouping or re-embedding;
- recovery and transient response.

No master score is required.

### 3.2 Six physical promotion gates

A proposed physical inheritance relation must pass six prospective gates before the full inheritance label is available.

**Gate 1: independent parent characterization.** The parent architecture is characterized before the child target is revealed.

**Gate 2: explicit correspondence.** Parent and child carriers or subspaces are related through an explicit physical or coordinate correspondence, not numerical similarity alone.

**Gate 3: frozen transformation rule.** The parent-to-child transformation or matching rule is fixed before target inspection.

**Gate 4: prospective prediction.** The frozen parent representation predicts an independently generated child object.

**Gate 5: intervention or counterfactual.** A parent perturbation produces the prospectively specified child change, or an appropriate counterfactual behaves as predicted.

**Gate 6: specificity.** Frequency-only, same-spectrum, generic-parent, scrambled-modal, coupling-rewire, or other appropriate native controls do not perform equally well.

Failure at a higher gate does not erase lower-level evidence. It changes the evidence label.

### 3.3 Separated epistemic states

For each relevant object SI keeps separate, where applicable:

- existence/admission;
- participation;
- observability;
- identifiability;
- coordinate estimation;
- regime or branch placement;
- uncertainty/tolerance;
- final admission/refusal.

These distinctions matter in crowded spectra and non-normal systems. Weak observability is not physical absence, and participation is not the same as unique identification.

### 3.4 Hierarchical closure

A lower-scale coupled system may be reused as an effective higher-scale component only when it preserves the quantities required by the declared higher-level question over a stated validity regime. Closure can therefore be supported, partial, failed, unresolved, or not applicable. Passing closure does not imply microscopic completeness.

### 3.5 Recovery and resilience

Where the native dynamics permit perturbation testing, SI separates current-state characterization from perturbation response, transient amplification, asymptotic return, reorganization, and resilience erosion. A stable asymptotic state can coexist with large finite-time amplification in a non-normal system. No universal resilience metric is assumed.

---

## 4. Synthetic qualification strategy

The current computational program is designed to qualify the evidence architecture rather than to provide physical inheritance evidence. Synthetic systems are useful because the planted relation, null condition, or failure mechanism is known. That lets us test whether the analysis recovers what is actually present and refuses what is absent.

The qualification program includes:

- mass-normalized modal overlap and assignment;
- principal-angle/subspace comparison for degenerate sectors;
- left/right biorthogonal diagnostics for non-normal generators;
- dynamic stiffness and Schur-complement embedding;
- finite-bath memory calculations without relabeling recurrence as irreversible friction;
- parent-parameter interventions and finite-difference transfer maps;
- eigenvalue-preserving modal scrambles;
- coupling-rewire controls;
- representation-invariance checks;
- finite-depth versus semi-infinite embedding;
- fail-closed real-system ingestion;
- relationship, uncertainty, lineage, and multi-parent source diagnostics.

The current Function/Limit program contains four completed maps and one planned recovery/resilience map. This manuscript reports only completed results.

---

## 5. Results

### 5.1 Baseline known-truth and adversarial qualification

A ground-truth battery includes no-coupling, influence-only, conditional scalar mapping, modal inheritance with changed scalar values, same-spectrum false friends, mode splitting, degenerate-subspace rotation, coupling rewiring, finite-bath recurrence, and a full prospective synthetic inheritance case. The purpose is not to demonstrate physical inheritance but to ensure the machinery distinguishes planted evidence classes.

In a 256-trial same-spectrum modal ensemble, the planted carrier map produced a mean permutation-invariant assignment score of approximately **0.94981**, whereas eigenvalue-identical scrambled carriers produced a mean of approximately **0.53907**. The threshold-free pairwise AUC was **1.0** for this construction. The result shows synthetic discriminability under the declared generator, not a physical correspondence threshold.

In a coupling-specificity ensemble, rewiring child coupling while keeping the parent operator fixed changed the normalized substrate self-energy in **255/256** trials above machine scale; the median relative change was approximately **0.20734**. Parent spectrum alone therefore did not determine the embedded response in this synthetic family.

The finite-difference parent-to-child transfer map agreed with an independently derived analytic derivative to approximately **1e-9** worst relative error in the tested ensemble, supporting the intervention implementation.

### 5.2 Scalar nonidentifiability

A deliberately adversarial construction produced distinct coupling geometries with the same scalar child self-energy at one frequency. The maximum scalar mismatch was approximately **1.67e-16**, while the median absolute cosine between the corresponding coupling directions was only approximately **0.30763**. At a second frequency, every constructed pair separated above machine scale, with median relative response difference approximately **0.03263**.

This result gives a direct methodological boundary:

`one matched scalar response != identified conglomerative inheritance`.

The scalar can be exactly matched while the underlying coupling architecture remains substantially different. A second condition or carrier-resolved measurement can recover information that the first scalar erased.

### 5.3 Near-degeneracy favors subspace reporting over forced eigenvector identity

For a near-degenerate two-mode sector with eigenvalue gap approximately **1e-8**, small perturbations reduced the fifth-percentile individual-mode assignment score to approximately **0.53924**. In the same ensemble, the fifth-percentile minimum subspace cosine remained approximately **0.999999999747**.

The result supports a fail-closed rule: when individual vectors become unstable under spectral crowding, a well-preserved invariant subspace should not be mislabeled as loss merely because a one-to-one mode identity is not defensible.

---

### 5.4 FM1: coupling-response Function/Limit landscape

FM1 maps carrier correspondence, participation, embedded response, intervention sensitivity, and coupling specificity across **36** frozen synthetic cases formed by six carrier-geometry angles and six coupling strengths while the clean parent spectrum is held fixed.

Across the full surface:

- carrier assignment mean overlap: maximum `1.0`, median approximately `0.91595`, minimum approximately `0.66575`;
- substrate participation: maximum `1.0`, median approximately `0.99434`, minimum approximately `0.75006`;
- carrier-overlap advantage over frequency-only assignment: maximum approximately `0.22066`, median `0`;
- coupling-rewire relative response-curve change: maximum approximately `1.7724`, median approximately `1.08783`, minimum `0`;
- embedded response-curve norm: maximum approximately `2.30577`, median approximately `0.06078`, minimum `0`;
- intervention derivative magnitude: maximum approximately `13.42087`, median approximately `0.01784`, minimum `0`.

At zero coupling, embedded response, rewire response change, and intervention derivative all vanish. The analysis therefore does not manufacture an embedding influence when the parent-child coupling is removed.

Embedded response and intervention sensitivity rise strongly over the declared coupling range, but coupling-rewire sensitivity is not globally monotonic. Carrier correspondence weakens as planted carrier geometry is rotated away from the reference relation. Median carrier overlap falls from approximately `0.99993` at zero angle to approximately `0.69468` at the largest tested angle. At that largest angle, carrier-resolved assignment retains a median overlap advantage of approximately `0.21678` over frequency-only assignment.

FM1 therefore shows, for this synthetic family, that a fixed parent spectrum does not fix embedded behavior, coupling geometry matters, and frequency similarity can become materially misleading. No physical overlap cutoff is inferred.

---

### 5.5 FM2: embedding depth is task- and regime-dependent

FM2 compares finite parent-chain embedding against an analytic semi-infinite reference over **48** hopping/probe cases and **8** retained depths (`1, 2, 4, 8, 16, 32, 64, 128`), producing **384** depth records.

Direct finite-matrix and recursive finite-chain surface Green-function implementations agree with a maximum absolute residual of approximately **5.55e-16**, well inside the frozen software verification tolerance of `1e-9`.

The retained depth needed for a declared relative embedding-error task varies substantially:

| Relative task | Minimum depth | Median depth | Maximum depth |
| ---: | ---: | ---: | ---: |
| `0.1` | 1 | 1 | 32 |
| `0.01` | 1 | 2 | 64 |
| `0.001` | 2 | 4 | 64 |
| `0.0001` | 2 | 4 | 64 |

Two of the 48 hopping/probe cases show at least one non-monotonic finite-depth error step. The pre-frozen effective-depth rule consequently requires a chosen depth **and all deeper listed depths** to remain within tolerance rather than declaring convergence at the first favorable crossing.

This is a model-reduction depth, not a physical inheritance length. The result instead demonstrates that retained parent extent is a declared-task and native-regime property.

---

### 5.6 FM3: a normalized lineage summary can lose exact reconvergence

FM3 uses a same-spectrum three-mode construction whose carrier basis changes across generations and then returns exactly to its starting basis. The frozen grid contains five transformation strengths, five spectral gaps, five perturbation magnitudes, and 32 seeds per parameter case, for **4,000** seed-expanded evaluations.

By construction, direct generation-0 to generation-3 carrier correspondence reconverges exactly to identity, with maximum exact direct reconvergence error **0.0**. Sequential row-normalized lineage-flow propagation, however, does not generally reproduce the same end-to-end state.

Exact unperturbed sequential-flow versus direct-carrier L1 discrepancy:

- minimum: `0.0`;
- median: approximately `0.4398612`;
- maximum: approximately `1.25`.

At increasing transformation strengths the discrepancy grows from `0` to approximately `0.08831`, `0.43986`, `1.00892`, and `1.25` across the declared angle sequence.

This is a negative method result, not evidence of physical lineage loss. The correct interpretation is:

`sequential normalized flow disagreement != physical lineage loss`

when direct carrier or subspace geometry demonstrates reconvergence.

The same study maps identifiability. Direct generation-0 to generation-3 parent-0 identity is interval-identifiable in **0.8** of the 125 perturbation-envelope parameter cases; all transition rows are interval-identifiable in **0.632**. Increasing perturbation and spectral crowding degrade individual-carrier identifiability, while the containing low-eigenvalue subspace remains better preserved.

At the exact equal-split construction, the dominant-lineage routine correctly refuses a unique descendant rather than arbitrarily breaking a `0.5/0.5` tie. Extinction is not present in the full-rank same-spectrum construction, and no post-result zeroing rule was introduced merely to manufacture it.

FM3 shows that lineage is a layered object. Local transition correspondence, direct higher-generation geometry, uncertainty, identifiability, and subspace structure cannot safely be compressed to a single normalized flow vector.

---

### 5.7 FM4: hierarchical closure is quantity- and regime-specific

FM4 tests whether a lower-scale four-degree-of-freedom mechanical group can be reduced to an effective boundary object and re-embedded while preserving declared higher-level response quantities. The landscape spans four internal coupling values, four boundary-to-outer couplings including a zero-coupling control, and 121 angular-frequency points, for **1,936** retained records.

The native/reference comparisons include the unreduced full system, direct exact Schur elimination, nested exact Schur elimination, Guyan-style static condensation, and a one-internal-mode dynamic approximation.

For the declared response quantities, direct and nested exact reductions agree with the full system to maximum absolute error approximately **1.87e-14**, far below the frozen `5e-11` numerical identity tolerance. The zero boundary-to-outer coupling control yields exactly zero group return.

The approximate reductions show a different picture. Guyan-style static condensation outer-compliance relative error has median approximately **0.00116**, but 95th percentile approximately **1.275** and maximum approximately **10.417**. Its return/self-energy relative error has median approximately **0.1876**, 95th percentile approximately **3.465**, and maximum approximately **29.961**. The one-internal-mode approximation performs better over much of this specific grid, but still reaches outer-compliance relative error nearly **1.0** and return/self-energy relative error above **4.57** in its worst regions.

No post-result physical adequacy cutoff or universal approximation ranking was added. The result supports two bounded conclusions:

`local convergence or compactness != hierarchical closure`

and

`hierarchical closure is quantity-specific and regime-specific`.

An exact dynamic reduction can preserve the declared information in the tested linear construction. A lossy representation can look excellent across much of the ordinary functioning interior and still fail badly in selected frequency/coupling regions.

---

## 6. Function Map and Limit Map synthesis

The completed maps now give a broader picture than a collection of failure gates.

### 6.1 Function Map

Across ordinary synthetic regimes, the program resolves graded changes in:

- carrier correspondence;
- parent participation;
- embedded response magnitude;
- intervention sensitivity;
- coupling specificity;
- finite-depth reduction accuracy;
- splitting and mixing;
- subspace preservation;
- exact hierarchical response preservation;
- approximate-reduction quality.

There is no requirement that one scalar summarize these behaviors.

### 6.2 Limit Map

The same program identifies explicit limits:

- a scalar response can be nonidentifying for coupling architecture;
- frequency matching can identify the wrong carrier relation;
- near-degenerate individual modes can become nonidentifiable while the subspace survives;
- finite-depth error can be non-monotonic;
- sequential normalized lineage flow can erase end-to-end reconvergence information;
- approximate subsystem reductions can fail strongly in restricted regimes even when their median performance looks excellent;
- lack of physical input remains a valid refusal rather than an invitation to reuse development data retrospectively.

The Limit Map is not a collection of embarrassments around the Function Map. Both are required to know what the proposed evidence architecture can and cannot support.

---

## 7. Relationship to native comparators

A future physical SI claim must be tested against the strongest fair native comparator for the exact frozen task. No universal comparator exists because the tasks differ.

Current comparator families include:

| Task | Native comparator family |
| --- | --- |
| carrier/mode correspondence | MAC/CMAC and uncertainty-aware clustered-subspace tracking |
| subsystem reduction/reassembly | dynamic substructuring / Component Mode Synthesis |
| static condensation | Guyan/static condensation |
| exact linear frequency-domain elimination | Schur complement / dynamic stiffness condensation |
| stable input-output reduction | controllability/observability-based model reduction |
| semi-infinite substrate embedding | surface Green functions / embedding potentials |
| path contribution across assemblies | frequency-based or DS/CMS transfer-path analysis |
| adsorbate/surface vibrational structure | native phonon, VDOS, polarization, surface-vibration and isotope analyses |

The physical question must be frozen first. Only then can the fair comparator be selected. If no native method answers the same task after a good-faith search, the correct status is `NO_NATIVE_COMPARATOR`, not a manufactured benchmark against an irrelevant method.

---

## 8. Physical experimental path

### 8.1 Adsorbate-on-substrate vibrational test

A high-value physical test would characterize a clean parent/substrate carrier structure, freeze the shared coordinate and carrier/subspace mapping, predict the coupled adsorbate/substrate descendants, and only then inspect the coupled target. An independent parent intervention, such as a physically justified isotope, mass, coverage, or substrate modification, would test whether the child transformation changes as predicted. Frequency-only and generic-coupling controls would remain explicit.

Prior literature already establishes adsorbate-substrate hybridization, isotopic coupling diagnostics, and substrate-to-adsorbate dynamical response. Those are inherited controls, not candidate SI novelty. The residual experiment is the prospective carrier-prediction and specificity sequence.

### 8.2 Thickness/depth and hierarchical closure

A second route asks how much parent structure must be retained for a declared response and whether the resulting effective subsystem remains adequate when reused at a higher level. Because dynamic substructuring, CMS, and Green-function embedding are mature, the SI question is not whether reduction is possible. It is whether a prospectively specified parent-child relation preserves the particular SI-relevant quantities needed at the next scale, with uncertainty and failure retained.

### 8.3 Controlled hardware analogue

A reconfigurable oscillator array could qualify measurement semantics under controlled hardware: same-spectrum carrier changes, coupling rewires, near-degeneracy, grouping/re-embedding, intervention, and recovery. Such a platform would be method qualification only and cannot validate a materials-specific inheritance claim by analogy.

### 8.4 Multi-parent source attribution

Where two or more physically separable parents can be independently present, absent, or perturbed, exact subset interventions can separate main and interaction contributions without forcing normalized percentages that sum to one. The decomposition mathematics is established; the unresolved SI question is whether a prospective physical design makes the source attribution scientifically informative.

---

## 9. Current physical-input boundary

The fail-closed real-system adapter is ready to ingest a physical record once one exists, but no provenance-complete real-system SI record is currently admitted.

A future physical entry requires, at minimum:

- an independently characterized parent governing object;
- an independently computed or measured child/coupled governing object;
- a prospective shared-coordinate map where applicable;
- mass normalization and modal/subspace representation when mechanically applicable;
- source commits/artifact hashes or equivalent provenance;
- an explicit system role declaration;
- an outcome-blinding or temporal-freeze record for correspondence;
- local-versus-embedded reporting;
- separate participation, observability, identifiability, estimate, and uncertainty states;
- a hierarchical-closure record if the reduced subsystem is reused at a higher scale.

Neither chi nor damping is required simply to enter the SI program. Modal and system-organization inheritance can be investigated without a scalar damping reduction.

---

## 10. Limitations and falsification

The current evidence is dominated by synthetic and mathematical qualification. It demonstrates that the machinery can preserve known structure, reject several false equivalences, and expose information loss. It does not show that a physical substrate transmits the same architecture in nature.

Several outcomes would argue against a stronger SI claim for a proposed physical system:

1. frequency-only or generic native methods predict the target equally well;
2. the prospective carrier map fails on the independent child object;
3. parent interventions do not induce the predicted child response;
4. the apparent relation disappears under uncertainty, degeneracy, or coordinate-invariance checks;
5. a same-spectrum or scrambled-carrier control performs equally well;
6. a coupling rewire preserves the claimed relation when the proposed mechanism says it should not;
7. the result requires target-dependent mode selection or a post-result threshold;
8. the effective subsystem fails to preserve the higher-level quantity for which inheritance is claimed;
9. a future fair native comparator explains the same frozen task without the SI-specific evidence architecture adding measurable value.

A null or negative physical result would therefore narrow SI rather than constitute a mechanical failure of the program.

---

## 11. Discussion

The synthetic program suggests that the scientifically useful object is relational rather than purely scalar. Parent spectrum, scalar response, modal geometry, coupling structure, embedded response, lineage, and higher-scale closure can agree in some regimes and diverge in others. The divergences are especially informative because they show which compression has discarded information.

FM1 demonstrates that parent spectrum and coupling magnitude do not uniquely fix embedded response; geometry and rewiring matter. FM2 shows that even a simple parent-depth reduction has no single context-free depth. FM3 demonstrates that a convenient normalized lineage summary can contradict direct carrier reconvergence because the summary is lossy. FM4 shows that exact and approximate closure are qualitatively different propositions: exact grouping can preserve a declared response, while common approximations can fail sharply outside their favorable regions.

Together these results discourage a scalar-first ontology. They do not eliminate scalar coordinates. Instead, they attach each scalar to the carrier and governing structure that license it, then retain modal/subspace and system organization where those contain additional information. A future scalar compression of system behavior must earn its existence by preserving the distinctions required for the scientific task.

The same logic constrains cross-scale claims. The recurrence of a mathematical motif does not establish that architecture is preserved under scale change. Preserved architecture does not establish a common physical mechanism. A common mechanism does not imply a universal numerical chi region. Each proposition requires its own evidence.

The strongest current SI contribution is therefore not a new algebraic primitive. It is the prospective evidence architecture that integrates independent parent characterization, carrier-resolved correspondence, coupling specificity, intervention, uncertainty, refusal, Function/Limit mapping, and hierarchical closure while preserving the boundaries exposed by native methods and negative results. Whether this integration adds physical predictive value remains a future empirical question.

---

## 12. Conclusions

We have developed and stress-tested a fail-closed substrate-inheritance evidence architecture for coupled dynamical systems. The present P0-D/P0-Q program supports the following bounded conclusions:

1. generic influence is insufficient for inheritance;
2. scalar agreement can coexist with underlying architectural nonidentifiability;
3. carrier and subspace geometry can retain information absent from frequency-only matching;
4. embedded behavior depends on coupling organization, not parent spectrum alone;
5. reduction depth and hierarchical closure are task- and regime-specific;
6. convenient lineage summaries can lose exact end-to-end carrier information;
7. negative, unresolved, and nonidentifiable states are necessary outputs of an honest inheritance test;
8. established native methods cover much of the mathematical machinery, narrowing the residual SI contribution to a prospective, integrated evidence architecture and its eventual physical added value.

No physical substrate-inheritance law is established by the current work. The decisive next stage is not to search for favorable numerical similarity but to obtain an admissible independently characterized physical parent/child record and subject a prospectively frozen inheritance claim to prediction, intervention, specificity controls, uncertainty, fair native comparison, and untouched evidence.

---

## 13. Data, code, and reproducibility

The active SI development code, frozen/candidate contracts, synthetic Function/Limit plans, validation tests, summaries, and provenance records are maintained in the `substrate_inheritance/` directory of the `SymC-Universe/Foundations` repository on the `substrate-inheritance-next` development branch.

The frozen v0.2 physical-promotion route remains separate from the non-authoritative SI-next v0.4 P0-Q architecture. Numerical results reported here should be traceable to their source summary, workflow run, artifact identity, or validation ledger. The manuscript evidence matrix is maintained alongside this working draft.

---

## 14. Working reference list

**Modal correspondence and uncertainty**

- Allemang, R. J. & Brown, D. L. A Correlation Coefficient for Modal Vector Analysis. Proceedings of the 1st International Modal Analysis Conference (1982).
- Kim, T. S. & Kim, Y. Y. MAC-based mode-tracking in structural topology optimization. *Computers & Structures* 74, 375-383 (2000). DOI: `10.1016/S0045-7949(99)00056-5`.
- Lu, J., Tang, J., Apley, D. W., Zhan, Z. & Chen, W. A mode tracking method in modal metamodeling for structures with clustered eigenvalues. *Computer Methods in Applied Mechanics and Engineering* 369, 113174 (2020). DOI: `10.1016/j.cma.2020.113174`.
- Greś, S., Döhler, M. & Mevel, L. Uncertainty quantification of the Modal Assurance Criterion in operational modal analysis. *Mechanical Systems and Signal Processing* 152, 107457 (2021). DOI: `10.1016/j.ymssp.2020.107457`.

**Dynamic substructuring and model reduction**

- Guyan, R. J. Reduction of stiffness and mass matrices. *AIAA Journal* 3, 380 (1965). DOI: `10.2514/3.2874`.
- Craig, R. R. & Bampton, M. C. C. Coupling of substructures for dynamic analyses. *AIAA Journal* 6, 1313-1319 (1968). DOI: `10.2514/3.4741`.
- Moore, B. C. Principal component analysis in linear systems: controllability, observability, and model reduction. *IEEE Transactions on Automatic Control* 26, 17-32 (1981). DOI: `10.1109/TAC.1981.1102568`.
- de Klerk, D., Rixen, D. J. & Voormeeren, S. N. General framework for dynamic substructuring: history, review and classification of techniques. *AIAA Journal* 46, 1169-1181 (2008). DOI: `10.2514/1.33274`.
- Hinke, L., Dohnal, F., Mace, B. R., Waters, T. P. & Ferguson, N. Component mode synthesis as a framework for uncertainty analysis. *Journal of Sound and Vibration* 324, 161-178 (2009). DOI: `10.1016/j.jsv.2009.01.056`.
- Chatterjee, T., Adhikari, S. & Friswell, M. I. Uncertainty propagation in dynamic sub-structuring by model reduction integrated domain decomposition. *Computer Methods in Applied Mechanics and Engineering* 366, 113060 (2020). DOI: `10.1016/j.cma.2020.113060`.
- El Kadmiri Pedraza, S., Monner, H. P. & Algermissen, S. A framework for simulation-based transfer path analysis using dynamic substructuring and component mode synthesis. *Computers & Structures* 321, 108097 (2026). DOI: `10.1016/j.compstruc.2026.108097`.
- Bondsman, B. & Peplow, A. Response-dependent component mode-synthesis with interface reduction. *Applied Mathematical Modelling* 158, 116924 (2026). DOI: `10.1016/j.apm.2026.116924`.

**Surface embedding and adsorbate/substrate dynamics**

- Lopez Sancho, M. P., Lopez Sancho, J. M. & Rubio, J. Highly convergent schemes for the calculation of bulk and surface Green functions. *Journal of Physics F: Metal Physics* 15, 851-858 (1985). DOI: `10.1088/0305-4608/15/4/009`.
- Inglesfield, J. E. & Benesh, G. A. Surface electronic structure: embedded self-consistent calculations. *Physical Review B* 37, 6682 (1988). DOI: `10.1103/PhysRevB.37.6682`.
- Inglesfield, J. E. Embedding at surfaces. *Computer Physics Communications* 137, 89-107 (2001). DOI: `10.1016/S0010-4655(01)00173-4`.
- Kern, K., Zeppenfeld, P., David, R. & Comsa, G. Adsorbate-substrate vibrational coupling in physisorbed Kr films on Pt(111). *Physical Review B* 35, 886(R) (1987). DOI: `10.1103/PhysRevB.35.886`.
- Hirschmugl, C. J. & Williams, G. P. Chemical shifts and coupling interactions for the bonding vibrational modes for CO/Cu(111) and (100) surfaces. *Physical Review B* 52, 14177 (1995). DOI: `10.1103/PhysRevB.52.14177`.
- Liu, K. & Gao, S. Adsorbate vibration and resonance lifetime broadening of a cobalt adatom on a Cu(111) surface. *Physical Review B* 74, 195433 (2006). DOI: `10.1103/PhysRevB.74.195433`.
- Herrmann, C. & Reiher, M. Direct targeting of adsorbate vibrations with mode-tracking. *Surface Science* 600, 1891-1900 (2006). DOI: `10.1016/j.susc.2006.01.054`.
- Fritsch, J., Arnold, M. & Schröder, U. Ab initio calculation of the phonon dispersion of antimony-covered (110) surfaces of III-V compounds. *Physical Review B* 61, 16682 (2000). DOI: `10.1103/PhysRevB.61.16682`.

---

## 15. Open manuscript items

These are manuscript-development items, not hidden scientific results.

- [ ] Integrate FM5 only after a prospective FM5 plan is frozen and the computation is completed.
- [ ] Perform a deeper systematic nearest-prior-art pass around the full prospective parent-characterization -> frozen mapping -> child prediction -> intervention -> specificity sequence.
- [ ] Add a compact figure showing the evidence ladder and the distinction between influence, conditional inheritance, and inheritance.
- [ ] Add a Function/Limit synthesis figure after figure semantics are frozen.
- [ ] Decide whether the first submission should remain method/architecture-focused or wait for an admissible physical P1 target.
- [ ] Convert the working reference list to the target journal format at manuscript freeze.
- [ ] Perform a full claim/citation sentence-level audit before any release.

**Current manuscript disposition:** `ACTIVE_WORKING_DRAFT_P0D_P0Q_ONLY`.