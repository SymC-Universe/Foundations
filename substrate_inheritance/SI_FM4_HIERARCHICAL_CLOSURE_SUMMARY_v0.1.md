# SI FM4 Hierarchical Closure Landscape Summary v0.1

Date: 2026-09-12
Status: P0-D descriptive/structural method landscape
Plan: `SI_FM4_HIERARCHICAL_CLOSURE_PLAN_v0.1.json`
Validation run: GitHub Actions `34699314595`
Head at validated run: `0603ff5ef3b449a97f08cf32b78eb01fc691f89d`

## Scientific question

When a lower-scale linear mechanical subsystem is reduced to an effective boundary component and then re-embedded into a larger system, which declared higher-level response quantities are preserved exactly, approximately, or poorly across an ordinary coupling/frequency landscape?

This is a P0-D method/structure question. It is not physical substrate-inheritance evidence and does not activate MFR-14.

## Model and coverage

The frozen FM4 plan used a four-degree-of-freedom linear mechanical chain:

`inner_0 <-> inner_1 <-> boundary <-> outer`

with:

- 4 internal-coupling values;
- 4 boundary-to-outer coupling values, including the zero-coupling control;
- 121 angular-frequency points from 0 to 3;
- 16 parameter cases;
- 1,936 retained records.

No Atlas coordinate, desired chi range, or post-result threshold selected the grid. No system scalar chi was constructed.

The declared higher-level quantities were:

- outer compliance `H_oo(omega)`;
- group-to-outer return/self-energy;
- outer effective dynamic stiffness.

## Native comparator structure

FM4 did not ask whether substructuring or reduction can be invented. Those are established methods.

It compared:

1. the unreduced full dynamic-stiffness system;
2. direct exact Schur elimination of the lower group;
3. nested exact Schur elimination, first inner -> boundary, then boundary -> outer;
4. Guyan-style static condensation as a deliberately approximate reduction away from zero frequency;
5. a one-internal-mode truncated modal resolvent as a second approximate reduction.

The exact identity tolerance, `5e-11`, is a software/mathematical numerical tolerance only. It is not a physical inheritance threshold.

## Result 1: exact nested closure preserves the declared response

The exact nested Schur reduction returned:

`HIERARCHICAL_REDUCTION_SUPPORTED_IN_REGIME`

for the declared synthetic linear response quantities across the full tested grid.

Maximum errors:

- full system vs direct Schur outer-compliance absolute error: `1.8720348745267393e-14`;
- direct vs nested outer-compliance absolute error: `1.7273871523195015e-14`;
- direct vs nested return/self-energy absolute error: `2.5121479338940403e-15`;
- maximum exact identity error: `1.8720348745267393e-14`.

All are far below the frozen `5e-11` numerical identity tolerance.

The zero boundary-to-outer coupling control produced exactly zero group return over all 484 zero-coupling records.

### Interpretation

For this linear construction and these declared higher-level quantities, the lower subsystem can be grouped into an exact frequency-dependent effective object without losing the response information required by the outer problem.

This is a formal/method-level closure statement. It does **not** show that an arbitrary physical substrate admits the same reduction, that the reduced object is microscopically complete, or that a substrate-inheritance claim has been confirmed.

## Result 2: closure depends on the reduction and the quantity being preserved

The approximate methods show why hierarchical closure cannot be inferred merely because a compact reduced representation exists.

### Guyan-style static condensation

Outer-compliance relative error over all records:

- median: `0.001161038394426284`;
- 95th percentile: `1.2750233838377454`;
- maximum: `10.416832309075158`.

Restricting to nonzero outer coupling:

- median: `0.012858579212380882`;
- 95th percentile: `1.6074759967534609`;
- maximum: `10.416832309075158`.

The maximum compliance error occurred at:

- internal coupling `0.15`;
- boundary-to-outer coupling `1.6`;
- `omega = 2.15`.

Return/self-energy relative error, where the reference return was nonzero:

- median: `0.18761867388427722`;
- 95th percentile: `3.4648232450633416`;
- maximum: `29.96139856506883`.

### One-internal-mode dynamic approximation

Outer-compliance relative error over all records:

- median: `0.0013717679262433976`;
- 95th percentile: `0.18480291979354133`;
- maximum: `0.9976388325550463`.

Restricting to nonzero outer coupling:

- median: `0.003922787714288961`;
- 95th percentile: `0.28121876302625115`;
- maximum: `0.9976388325550463`.

The maximum compliance error occurred at:

- internal coupling `0.5`;
- boundary-to-outer coupling `0.8`;
- `omega = 1.95`.

Return/self-energy relative error, where the reference return was nonzero:

- median: `0.019757438017495146`;
- 95th percentile: `0.41872562481125314`;
- maximum: `4.573768817639079`.

No approximation ordering was preregistered, and no binary physical adequacy cutoff was introduced after seeing these surfaces. Therefore these comparisons remain descriptive P0-D results rather than a claim that one approximate method is universally superior.

## What FM4 adds to the SI investigation

FM4 sharpens the phrase "a conglomerate can become a component of a larger conglomerate."

The scientifically defensible version is:

> A grouped subsystem may be reused at a higher level only to the extent that its effective representation preserves the quantities required by the higher-level question over the declared validity regime.

An exact dynamic reduction can preserve those quantities in the tested construction. A lossy reduction can look excellent across much of the ordinary landscape and still fail badly in restricted frequency/coupling regions.

Therefore:

`local convergence or compactness != hierarchical closure`

and:

`hierarchical closure is quantity-specific and regime-specific`.

This is consistent with GP v0.7.4's requirement to keep local identity, embedded behavior, observability/identifiability, and higher-scale preservation separately auditable.

## Function Map and Limit Map

FM4 produced both sides:

### Function Map

- exact nested closure across the tested linear regime;
- broad regions where approximate reductions have small outer-response error;
- continuous dependence of approximation quality on frequency and coupling.

### Limit Map

- sharply degraded static-condensation response in selected frequency/coupling regions;
- substantial one-mode approximation failure in a smaller but still material portion of the landscape;
- explicit conditioning diagnostics rather than silent interpretation near difficult response regions.

The result is therefore not merely a boundary scan.

## Validation and reproducibility

GitHub Actions run `34699314595` completed successfully.

- `137 passed` in the repository test suite;
- all historical V1-V10 validations remained green;
- SI-next v0.3 historical qualification remained green;
- SI-next v0.4 GP semantic guards remained green;
- FM4 plan guards, exact closure tests, known-bad refusals, zero-coupling control, full-grid retention, and non-physical evidence guards passed.

Artifacts:

- `substrate-inheritance-synthetic-validation`, ID `10300145609`, SHA-256 `ff351bc208d13693ba10717eed11bec0db0100be1aacb11852d77b654d708358`;
- `substrate-inheritance-fm4-hierarchical-closure-v01`, ID `10300070726`, SHA-256 `4b52b683e7f4635ea76ca4d1c05d8d2210589ddda8ac7dd418bad5201a33c181`.

## Claim ceiling

FM4 establishes only a synthetic/formal P0-D hierarchical-closure landscape for the declared linear construction.

It does not establish:

- physical substrate inheritance;
- a universal closure rule;
- a system scalar chi;
- cross-domain recurrence;
- superiority over all native model-reduction methods;
- a physical error threshold;
- a P1 prediction.

## Next scientific gate

FM4 closes the first v0.7.4-specific hierarchical-closure gap sufficiently for P0-D.

The next planned investigation is `FM1_COUPLING_RESPONSE_LANDSCAPE`.

Its purpose is to map the **ordinary functioning interior** of parent-to-child coupling rather than only where correspondence fails. It will separately track carrier/subspace correspondence, participation, embedded response, intervention response, and coupling specificity over frozen coupling and carrier-geometry controls, with frequency/eigenvalue-only matching retained as a native/simple comparator and with no master score or physical threshold.
