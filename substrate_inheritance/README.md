# Substrate Inheritance Program

Status: ACTIVE INVESTIGATION. Computational evidence is being developed prospectively. Nothing in this directory establishes a universal substrate-inheritance law.

Current-status authority: this README, the active contract, the frozen correspondence protocol, and the current computational records govern the present program. Older papers, repository metadata, release text, or prior README language are OUTDATED wherever they conflict with these current qualifications. Historical artifacts remain preserved for provenance rather than silently rewritten.

This branch consolidates the current Foundations generator-first framework with the parts of Stability Arc, Chemistry/ChemSA, and the Atlas program that are needed to test substrate inheritance without pooling physically distinct coordinates.

## Core distinction

Substrate influence and substrate inheritance are related but not interchangeable.

- SUBSTRATE_INFLUENCE: changing an independently defined substrate property changes a child or coupled-system observable, but a stable parent-to-child correspondence has not been established.
- CONDITIONAL_INHERITANCE: a specified scalar, mode, subspace, or conglomerated structure is prospectively transmitted under stated conditions through a frozen mapping rule.
- SUBSTRATE_INHERITANCE: a carrier-resolved parent architecture makes prospectively successful child predictions, survives intervention and specificity/null tests, and cannot be reproduced equally well by generic or scrambled controls.

Inheritance therefore requires influence, but influence does not by itself establish inheritance.

## Required representation

The program retains three coupled levels rather than reducing the system to one number:

1. Modal: eigenvectors, mode shapes, eigenspaces or subspaces, participation, localization, degeneracy, and conditioning.
2. Scalar: licensed coordinates attached to their physical carriers, including mechanical chi only where a stable second-order reduction or equivalent admitted quotient exists.
3. Conglomeration: the organization of modes, couplings, bath response, memory, and collective system structure across assembly or reaction-path evolution.

No level is permitted to substitute automatically for the others.

## Prospective evidence ladder

A proposed inherited quantity must pass the following gates before promotion beyond influence:

1. Independent parent characterization before child reveal.
2. Explicit carrier correspondence rather than numerical similarity alone.
3. Parent-to-child transformation rule frozen before target outcome inspection.
4. Prospective prediction against an independently computed child object.
5. Intervention or counterfactual test in which parent perturbation produces the predicted child response.
6. Specificity test showing that scrambled scalar, modal, coupling, or generic-substrate controls do not perform equally well.

Failure at a higher gate does not erase lower-level evidence. It changes the label.

The current carrier correspondence definitions are frozen in `CORRESPONDENCE_PROTOCOL_v0.1.json` before a real-system inheritance target has been revealed. No physical promotion threshold is frozen yet.

## Computational program

The current engine and validation suite implement:

- mass-normalized modal overlap matrices;
- subspace comparison using principal-angle cosines for degenerate or crowded sectors;
- frequency-domain dynamic stiffness construction;
- Schur-complement elimination of substrate degrees of freedom;
- substrate self-energy/embedding calculations;
- explicit finite-bath memory-kernel calculations without mislabeling a finite harmonic bath as irreversible friction;
- parent-parameter intervention and finite-difference transfer maps;
- eigenvalue-preserving modal-scramble controls;
- coupling-rewire controls;
- coordinate-representation invariance checks;
- near-degeneracy robustness checks;
- finite-depth versus analytic semi-infinite embedding validation;
- promotion logic that distinguishes influence, conditional inheritance, and inheritance.

Latest closed V1-V6 validation: GitHub Actions run `33290269457`, conclusion `success`, with 36 adversarial/unit tests passing. The archived validation artifact is `substrate-inheritance-synthetic-validation`, artifact ID `9725736036`, ZIP SHA-256 `8adc5e7135a824f8f3f726e8abd2ba60dbc64aacfae86a4db992ae9449e0343d`.

These are software, mathematical, synthetic, identifiability, and robustness results. They are not physical substrate-inheritance evidence.

## Current computational findings

### Ground-truth adversarial battery

Ten deliberately constructed cases test no coupling, influence only, conditional scalar mapping, modal inheritance with changed scalar values, same-spectrum false friends, mode splitting, degenerate-subspace rotation, coupling rewiring, finite-bath recurrence, and a full prospective synthetic inheritance case. All behave according to their intended evidence class under the current suite.

### Same-spectrum modal ensemble

Across 256 seeded dimension-5 trials, a planted carrier map had mean permutation-invariant assignment score approximately `0.94981`, while eigenvalue-identical scrambled carriers had mean approximately `0.53907`. The threshold-free pairwise AUC was `1.0` for this specified synthetic generator. This demonstrates method discriminability under the synthetic construction, not a physical threshold.

### Coupling-specificity ensemble

Rewiring the child coupling while keeping the substrate operator fixed changed the normalized substrate self-energy in 255/256 trials above machine scale. The median relative change was approximately `0.20734`. This shows that the conglomeration layer contains information not fixed by substrate spectrum alone in the tested synthetic ensemble.

### Intervention consistency

The finite-difference parent-to-child transfer map agrees with an independent analytic derivative to a worst relative error of approximately `1.12e-9` in the tested synthetic ensemble.

### Scalar nonidentifiability

Across 256 trials, distinct coupling geometries were constructed to reproduce the same scalar child self-energy at one frequency with maximum mismatch approximately `1.67e-16`. Their median absolute coupling-direction cosine was only approximately `0.30763`. At a second frequency every pair separated above machine scale, with median relative response difference approximately `0.03263`.

This supplies a direct computational boundary between influence and inheritance: one perfectly matched scalar response can demonstrate influence while remaining non-identifying for conglomerative inheritance.

### Coordinate and degeneracy robustness

The substrate self-energy is invariant under the tested consistent coordinate transformations to approximately `1.78e-15` maximum residual.

For a near-degenerate two-mode sector with gap approximately `1e-8`, tiny perturbations reduced the 5th-percentile individual-mode assignment score to approximately `0.53924`, while the 5th-percentile minimum subspace cosine remained approximately `0.999999999747`. This validates using subspace geometry rather than forced one-to-one eigenvectors in crowded sectors.

### Synthetic inheritance depth

A finite substrate-chain embedding was compared against an analytic semi-infinite surface Green function. In the reference synthetic case, relative self-energy error fell from approximately `5.40e-2` at depth 1 to `3.07e-3` at depth 2, `1.00e-5` at depth 4, `1.06e-10` at depth 8, and machine scale by depth 16. Stronger synthetic inter-site coupling required greater retained depth.

These depths are model sizes, not physical inheritance lengths for any material. The calculation validates the method that will later ask how much substrate must be retained before a real child embedding response converges.

Detailed numerical provenance is retained in `VALIDATION_LEDGER.md`.

## Physical-system readiness

`PHYSICAL_INPUT_READINESS_v0.1.json` prevents planned or upstream calculations from being mistaken for inheritance evidence.

Current status:

1. Na/Cu(001): development-only and not ready for physical ingestion because the planned active-region Hessian artifact is not present at the checked Chemistry head. It may later exercise the adapter as development evidence but cannot be retroactively promoted.
2. CO/Cu(111): prospective validation target, still upstream of inheritance analysis while its already-frozen Chemistry surface audit closes. This branch must not alter that route.
3. H/Ru(0001): contrast/limit target with protocol-level preparation but no admitted Foundations inheritance input record yet.

Mechanical chi or a damping scalar is not required to begin modal or conglomerative inheritance analysis. Any later scalar inheritance claim requires its own independent admissibility and dissipation provenance.

## Relationship to the Atlas program

The ARC Atlas and Barrier-Height/Rate Atlas remain separate evidence layers.

- ARC-type records provide independently estimated or computed stability/dissipation coordinates when physically licensed.
- Barrier-Height/Rate records provide reaction barriers, prefactors, rates, and associated provenance.
- Neither Atlas by itself establishes inheritance.
- This program adds the missing parent-to-child carrier and transformation evidence needed to test whether substrate structure is merely influential or is inherited in a defensible sense.

Barrier height, reaction rate, damping morphology, turnover, transmission, exceptional-point proximity, friction regime, and substrate inheritance remain distinct quantities unless a derivation explicitly relates them.

## Non-Markovian and bath rule

A finite harmonic slab or finite set of Hessian modes is not automatically an irreversible dissipative bath. Finite-mode recurrence must be retained as such.

For a memory-bearing reduction, the relevant effective object is frequency dependent. A local scalar damping constant and mechanical chi may be reported only after an independently justified reduction demonstrates that such compression is admissible on the relevant timescale.

## Electronic and phononic channels

Mechanical/phononic and electronic substrate inheritance are separate channels. They may be analyzed in parallel, but they must not be silently merged into one damping constant. Any combined reduction requires an explicit derivation and provenance audit.

## Historical material and outdated claims

Older SymC, Noughts, Stability Arc, Chemistry, ARC, or related documents may contain broader language written before the current generator-first, carrier-resolved, prospective inheritance criteria were adopted. Those artifacts remain part of the research record, but such broader claims are OUTDATED wherever they conflict with the current contract.

Current program status is an ongoing investigation aimed at developing computational evidence for or against substrate-inheritance claims. Historical statements are not prospective evidence merely because they anticipated the hypothesis.

## Current branch status

- Architecture and evidentiary ladder: active and prospective.
- Carrier correspondence definitions: frozen before real-system target reveal.
- V1-V6 synthetic/mathematical validation: PASS.
- Latest closed suite: 36 tests passed.
- Physical inheritance thresholds: not frozen.
- Real-system inheritance result: not established.
- Universal inheritance claim: not established.

A refusal, nonidentifiable correspondence, influence-only result, or failed inheritance test is a valid outcome and must remain in the record.
