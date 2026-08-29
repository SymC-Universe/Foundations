# Stability Arc current state

Last updated: 2026-08-29
Canonical repository: `SymC-Universe/Foundations`
Canonical working branch: `agent/stability-arc-gfsa-v072`

## Active controls

- `stability_arc/gfsa_v0.7.2/ANTI_CIRCULARITY_GUARD_v0.1.md`
- `stability_arc/CONTINUITY_AND_FAILURE_SIGNAL_PROTOCOL_v0.1.md`
- `stability_arc/HISTORICAL_FAILURE_SIGNAL_RECOVERY_v0.1.md`
- `stability_arc/gfsa_v0.7.2/PROVENANCE_RECOVERY_SEARCH_LOG_v0.1.md`

Frozen science, preregistrations, thresholds, exclusions, failure records, and interpretation firewalls remain controlling. FAIL, HOLD, null, NONIDENTIFIABLE, and REFUSE are admissible evidence and may not be repaired by retuning against observed outcomes.

## GFSA v0.7.2 state

Closed PASS:

- package validation;
- C18 calibration validity;
- OBS18 interface admissibility;
- OBS19 blind holdout;
- observable-only EP firewall;
- external interface status `LICENSED_FOR_EXTERNAL_NUMERICAL_ADMISSION`.

External numerical admission remains quarantined because the exact authentic frozen v0.7 external-candidate contract and authoritative candidate-source package have not been recovered. Candidate response values must not be inspected, plotted, summarized, filtered, or scored until that contract is recovered, persisted, hashed, chronology-authenticated, and bound.

## Measurement-conditioned established hierarchy

The outcome-free representation now contains:

1. separate same-noise physical and same-record inference tangent generators;
2. a low-rank conditioning bridge;
3. an exact conditioning-dark factor on admitted measured-qubit controls;
4. an exact two-dimensional stochastic active quotient `dq=A_A q dt+B_A q dW`;
5. deterministic `chi_active=-tr(A_A)/(2 sqrt(det(A_A)))` separately licensed only under deterministic two-dimensional scalar-admissibility conditions;
6. the stochastic pair `(A_A,B_A)` remains uncompressed;
7. symmetric second moments evolve under a real 3x3 generator `G`;
8. cubic mean-square stability requires `c1>0`, `c2>0`, `c3>0`, and `c1*c2>c3`.

Required stochastic reporting state remains `MEAN_SQUARE_INVARIANTS_REQUIRED`. No stochastic scalar chi is licensed.

## Preserved failures and bounded passes

### Joint representation v0.1

Permanent FAIL, run `33234191815`. The failure exposed an incorrect measurement-dissipator normalization, missing stochastic amplitude, and partial self-certification. Later corrective work does not erase it.

### Generalized spectral-abscissa H2

Permanent `FAIL_GENERALIZED_H2`, run `33256389876`, with 441 admitted counterexamples to global `alpha_rec<=alpha_phys`.

The subsequent fresh weak-measurement failure-mechanism phase prospectively validated a bounded first-order coefficient explaining a structured subset of those failures. H2 itself remains failed.

### H3 bounded near-boundary class test

`PASS_ADVERSARIAL_CLASS_MONOTONICITY`, run `33256865456`, on the frozen 512-case panel selected physical-only from 50000 fresh candidates. All 512 remained mean-square stable under record conditioning. This is a bounded panel result, not a theorem.

## H4 fresh targeted class-crossing closure

Canonical result:
`stability_arc/measurement_conditioned/class_crossing_v01/TARGETED_CLASS_CROSSING_RESULT_v0.1.md`

Run `33257117162`: `PASS_TARGETED_CROSSING_H4`.

H4 used a new seed and strict two-stage freeze-before-view design:

- exactly 100000 fresh target-region inputs;
- 52435 robust physical mean-square STABLE cases frozen before any record reveal;
- exactly 50 analytic robust physical STABLE -> record UNSTABLE crossings;
- all 50/50 independently reconstructed from full two-level Hilbert-space operators.

Therefore mean-square stability-class preservation is **not universal even within this exact measured-qubit family**. The earlier H3 bounded PASS remains valid for its own panel.

Post-H4 inspection found `c3_rec<0` while `c1_rec`, `c2_rec`, and `c1_rec*c2_rec-c3_rec` remained positive in all 50 crossings. That 50/50 pattern remained post-outcome relative to H4 and was not promoted directly.

## Exact c3 boundary derivation closure

Canonical result:
`stability_arc/measurement_conditioned/c3_boundary_v01/C3_BOUNDARY_DERIVATION_RESULT_v0.1.md`

Run `33257258056`: `PASS_C3_BOUNDARY_DERIVATION`.

The derivation independently reconstructed the physical and record 3x3 second-moment generators and proved the registered channel-specific quadratic forms

`c3_p(w)=A_p3*w^2+B_p3*w+C_p3`

and

`c3_r(w)=A_r3*w^2+B_r3*w+C_r3`,

verified `c3=-det(G)`, exact coefficient identities, discriminant/root factorization, and fresh seed-`2026082906` clean-room controls. Maximum numerical formula error was `1.3657194584723663e-14` against a frozen `2e-10` gate.

Artifact `9716183849`, ZIP SHA-256 `fa3a9b2814c8f6f049eb14db03a543d05f93cbd0f8507d7ab13e1f5e06153f20`.

This licenses the separate physical and record `c3=0` boundary surfaces. It does not license the claim that `c3` is always the failure gate.

## ACTIVE: H5 prospective c3-gate mechanism test

Preregistration:
`stability_arc/measurement_conditioned/c3_gate_test_v01/PREREGISTRATION_C3_GATE_CROSSING_TEST_v0.1.md`

Workflow:
`Stability Arc prospective c3-gate crossing test v0.1`

Live run: `33263959965`
Head commit: `ea27b9be79df3a88ce426551328c024eefce579e`

H5 uses new seed `2026082907` and the unchanged pre-H4 target-region generator. It generates exactly 100000 fresh candidates.

Stage A constructs only the physical channel and freezes every robust physical STABLE eligible case plus its digest before any record channel exists.

Stage B then reveals the record channel for the immutable Stage-A set. Every robust STABLE -> UNSTABLE crossing must be retained and independently reconstructed.

The fresh H5 mechanism statement is that record endpoints of fresh robust crossings satisfy

`c1_rec>0`, `c2_rec>0`, `c3_rec<0`, `c1_rec*c2_rec-c3_rec>0`

with frozen normalized margin tolerance `1e-9`. A minimum of 20 independently reconstructed crossings is required for population-level promotion in this target family. Any reconstructed counterexample makes H5 FAIL; it may not be removed or repaired.

## Continuity incident

The Stability Arc continuity controller became disabled after the c3 derivation run completed, leaving GitHub Actions idle and this state file stale. This is classified **MECHANICAL / CONTINUITY AUTOMATION**, not scientific. No frozen scientific input or result was altered or lost. The missing c3 result record has now been persisted and H5 launched.

The controller must remain enabled and, when a workflow finishes, inspect/persist its result and advance the next justified safe phase rather than stopping at an idle Actions page.

## QuTiP state

QuTiP 5.3.1 runtime admission remains `RUNTIME_ADMITTED`.

Historical v0.6 notebook reproduction remains open. Expected original notebook SHA-256:
`be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82`.

Runtime admission is not a substitute for authentic notebook recovery/reproduction.

## Anti-circularity state

- same-noise and same-record channels remain separately recoverable in every joint analysis;
- joint/conglomerate analysis is permitted only while channel identity is preserved;
- generalized H2 remains permanently failed;
- H3 remains bounded to its preregistered panel;
- H4 used a fresh seed and physical-only freeze before record reveal;
- the c3 mechanism observation from H4 was not promoted until an independent equation-level derivation closed;
- H5 is a new-seed prospective test of the learned mechanism;
- no stochastic scalar has been promoted;
- no historical localization outcome has selected the current representation or thresholds;
- GFSA external candidate values remain sealed.

## Current blockers

- GFSA external numerical admission: exact authentic v0.7 contract/source package absent;
- historical QuTiP comparison: authentic original notebook/source absent;
- historical Phase 4A: PENDING/INCOMPLETE.

None blocks H5 or continued measurement-conditioned derivation/testing.

## Queue

### COMPLETED

- stochastic active quotient closure;
- mean-square invariant geometry;
- generalized H2 falsification and fresh bounded failure-mechanism test;
- H3 bounded 512-case class-preservation PASS;
- H4 fresh targeted class-crossing PASS with 50/50 independent reconstructions;
- exact physical/record `c3=0` boundary derivation PASS.

### ACTIVE

- H5 fresh prospective c3-gate crossing mechanism test, run `33263959965`.

### NEXT IF H5 PASSES

Derive and freeze a boundary-displacement map comparing the separate physical and record `c3=0` root surfaces, while retaining the other Routh-Hurwitz margins as mandatory admissibility conditions. Then test that map on another untouched seed before any attempt to connect it to localization/interface behavior.

### NEXT IF H5 FAILS

Preserve every counterexample, classify which alternate or mixed Routh-Hurwitz gate fails, derive the smallest mechanism refinement from the failure, and require a new frozen fresh test. Do not repair H5.

## User action

None currently required.
