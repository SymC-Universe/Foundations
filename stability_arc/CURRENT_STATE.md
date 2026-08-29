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

## Measurement-conditioned closed hierarchy

The current outcome-free representation is:

1. separate same-noise physical and same-record inference tangent generators `A_phys` and `A_rec`;
2. low-rank conditioning bridge `DeltaA=A_rec-A_phys`;
3. outcome-free conditioning-dark factor reconstructed from the physical generator and measurement functional;
4. exact 2D stochastic active quotient on admitted measured-qubit controls,
   `dq=A_A q dt+B_A q dW`;
5. deterministic `chi_active=-tr(A_A)/(2 sqrt(det(A_A)))` separately licensed for physical and record channels only under deterministic 2D scalar-admissibility conditions;
6. stochastic pair `(A_A,B_A)` remains uncompressed;
7. symmetric second moment governed by real 3x3 `G(A_A,B_A)`;
8. if `det(lambda I-G)=lambda^3+c1 lambda^2+c2 lambda+c3`, strict mean-square asymptotic stability requires
   `c1>0`, `c2>0`, `c3>0`, `c1*c2>c3`.

Required stochastic reporting state remains:

`MEAN_SQUARE_INVARIANTS_REQUIRED`.

No stochastic scalar chi is licensed.

## Preserved failures

### Joint representation v0.1

Run `33234191815`: permanent FAIL.

It exposed an incorrect measurement-dissipator normalization, missing stochastic amplitude, and partial self-certification. Later corrective work does not erase this failure.

### Generalized spectral-abscissa H2

Run `33256389876`: permanent `FAIL_GENERALIZED_H2`.

Canonical result:
`stability_arc/measurement_conditioned/conditioning_structural_stress_v01/CONDITIONING_STRUCTURAL_STRESS_RESULT_v0.1.md`

Artifact `9715934331`, ZIP SHA-256
`a14675b7957776cb552f94a14b1345361b6b0a018ee4466a82594e05978323eb`.

All structural/audit gates passed, but 441 admitted cases violated generalized

`alpha_rec <= alpha_phys`.

Of 4112 broad/corner cases:

- 3146 STABLE -> STABLE;
- 584 UNSTABLE -> STABLE;
- 382 UNSTABLE -> UNSTABLE;
- 0 STABLE -> UNSTABLE.

440 of the 441 H2 failures were still STABLE -> STABLE. The result therefore falsified monotonic decay-rate improvement without showing destabilizing class crossings.

For the 440 stable H2 failures, all four cubic Routh-Hurwitz margins increased while the spectral abscissa became less negative. Decay-rate ordering and algebraic stability margin are therefore distinct coordinates in this joint geometry.

## Prospective failure-mechanism closure

Run `33256684197`: `PASS_PROSPECTIVE_FAILURE_MECHANISM`.

Canonical result:
`stability_arc/measurement_conditioned/conditioning_failure_mechanism_v01/CONDITIONING_FAILURE_MECHANISM_RESULT_v0.1.md`

Artifact `9716016119`, ZIP SHA-256
`21cab1770ba4f95f10f1dc276a82d2e9715ff86f2500b4e161198b60144d2632`.

A post-hoc mechanism from the failed H2 phase was frozen and tested on new seed `2026082903` with 64 analytically predicted worsening and 64 predicted improving fixtures, each at `eta={1e-3,1e-4,1e-5}`.

All F0-F5 gates passed:

- 128/128 finest-level sign predictions correct;
- maximum finest-level residual `|delta_alpha/q-2S|=9.454596391766934e-05` versus frozen `0.01` gate;
- both sign groups converged monotonically toward the first-order formula as q approached zero.

The validated bounded weak-measurement coefficient is

`S=-(1-z^2)+((1-z^2)*delta-2*omega*x*z)/sqrt(delta^2-4*omega^2)`,

with `delta=gamma/2-kappa`, predicting

`(alpha_rec-alpha_phys)/q -> 2S`.

This explains a structured class of H2 failures without rescuing H2. It also shows that repeated-root geometry enters together with state orientation, measurement strength, and damping asymmetry.

## Adversarial stability-class H3 closure

Run `33256865456`: `PASS_ADVERSARIAL_CLASS_MONOTONICITY`.

Canonical result:
`stability_arc/measurement_conditioned/class_monotonicity_v01/CLASS_MONOTONICITY_ADVERSARIAL_RESULT_v0.1.md`

Artifact `9716068192`, ZIP SHA-256
`4c920d36823d7281c12e0996f7a1ba24174d89d72760ae4827a1ff35f40cf756`.

The phase used a two-stage freeze-before-view design.

### Stage A, physical only

- generated exactly 50000 fresh seed-`2026082904` candidates;
- candidate-input SHA-256 `de7d0e1bb9534d2b84ef25770d1f26c66a37c040d2fb7ec8f665156c740733c3`;
- found 35781 physical mean-square STABLE eligible cases;
- selected the 512 smallest physical-only normalized boundary distances;
- froze selection before constructing any same-record channel;
- Stage-A selection SHA-256 `df9439879548a15c88c5b3300764cfc81541576e21b0c415f527a37df4efb6fc`;
- selected `d_phys` ranged from `2.7705091743349526e-07` to `8.274334307965391e-05`.

### Stage B, record reveal

- all 512 passed independent reconstruction;
- max moment-lift error `0.0`;
- max normalized physical replay error `4.1817677792765906e-16`;
- independent adversarial control correctly produced STABLE -> UNSTABLE;
- measured-qubit crossing count: `0`.

Thus H3 has strong fresh adversarial support within this exact measured-qubit family:

> physical mean-square STABLE -> record mean-square STABLE

for all 512 fresh cases selected intentionally near the physical boundary.

This is not yet a theorem.

## Current scientific picture

Three statements must remain separate:

1. deterministic repeated-root / damping-morphology boundary, including `chi_active=1` when the deterministic scalar is admissible;
2. stochastic mean-square stability boundary from the cubic second-moment generator;
3. physical-versus-record comparative response of spectral decay rates and stability class.

The generalized decay-rate monotonicity claim is false. A bounded weak-measurement failure mechanism is prospectively validated. Stability-class preservation is strongly prospectively supported in the exact measured-qubit family but not proven.

This supports a multicoordinate joint stability architecture, not a forced universal scalar.

## Next justified frontier

Attempt an outcome-free symbolic implication / sufficient-condition analysis for H3:

> when the physical measured-qubit active quotient satisfies all cubic Routh-Hurwitz inequalities, determine whether the exact same-record rank-one correction plus shared multiplicative-noise term necessarily preserves those inequalities.

The proof attempt must derive exact symbolic physical and record cubic coefficients and Hurwitz margins from the model equations without using the 512 outcomes to choose signs, factors, or assumptions.

Allowed outcomes include:

- exact proof within stated physical constraints;
- only bounded sufficient conditions;
- `PROOF_NOT_CLOSED` with explicit unresolved terms;
- symbolic/numerical counterexample, which would override any temptation to promote H3 universally.

No computational PASS may be relabeled as a theorem without a closed proof.

## QuTiP state

QuTiP 5.3.1 runtime admission remains `RUNTIME_ADMITTED`.

Historical v0.6 notebook reproduction remains open. Expected original notebook SHA-256:
`be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82`.

Runtime admission is not a substitute for authentic notebook recovery/reproduction.

## Anti-circularity state

- same-noise and same-record channels remain separately recoverable in every joint analysis;
- the 24-case H1 PASS remains bounded to its registered sample;
- generalized H2 remains failed with all 441 counterexamples preserved;
- the H2 failure mechanism was promoted only after a separate fresh prospective test;
- H3 was tested with physical-only selection frozen before record-channel reveal;
- no stochastic scalar has been promoted;
- no localization outcome has selected any measurement-conditioned representation, failure wedge, threshold, or current hypothesis;
- GFSA external candidate values remain sealed.

## Current blockers

- GFSA external numerical admission: exact authentic v0.7 contract/source package absent;
- historical QuTiP comparison: authentic original notebook/source absent;
- historical Phase 4A: PENDING/INCOMPLETE.

None blocks the symbolic H3 implication analysis.

## Queue

### COMPLETED

- stochastic active quotient closure;
- mean-square 3x3 invariant geometry;
- bounded 24-case prospective H1 PASS;
- broad generalized H2 falsification;
- prospective mechanistic explanation of a major H2 failure regime;
- adversarial 50k-candidate / 512-near-boundary H3 class test PASS.

### ACTIVE / NEXT

- symbolic H3 implication / sufficient-condition analysis;
- preserve exact proof limits if full implication cannot be closed;
- then decide whether the next clean scientific extension is a new measurement/dissipation geometry or a prospective localization/interface test, without reusing historical localization outcomes for model selection.

## User action

None currently required.
