# D02B Four-Bolt Physical Stability-Inheritance Readout v0.1

**Date:** 2026-09-23  
**Status:** P0-Q PHYSICAL QUALIFICATION COMPLETE  
**Authority:** SymC General Operations Manual v0.8.3  
**Dataset:** Kullukcu & Hannebauer four-bolt aluminum-plate LDV dataset  
**Dataset DOI:** 10.5281/zenodo.20038951  
**Successful workflow:** 35823640290  
**Execution commit:** cd4127b963cf2057841dff320c547ec7f3fad73d  
**Artifact ID:** 10734281523  
**Full-result SHA-256:** d7e0001413ef438aea2d8ea8757f7b4eeb8d6dab5ecfdf62be02b9f2575d4f10  
**Claim ceiling:** physical P0-Q qualification; not untouched P1 confirmation

## 1. Frozen question

D02B asked whether controlled reorganization of a real physical interface can:

1. preserve, transform, or make non-identifiable a licensed local/modal damping coordinate
   chi = Delta_f/(2 f_n);
2. reorganize the independently measured full-field response;
3. produce cases in which local chi remains similar while embedded response changes;
4. require anything beyond standard structural-dynamics tools.

The physical control variable is bolt torque. The response architecture is measured through tracked resonance frequency and the source-native full-field 1-MACa, 1-CMAC, and phase-only 1-CMAC quantities.

No master plate-level scalar was searched.

## 2. Execution integrity

The reviewer-facing command

python chi_architecture/reproduce.py d02b

completed successfully.

The run:

- checksum-verified all Zenodo source archives;
- retained all seven source-defined resonance families;
- used all 18 torque states;
- used the exact 51 scan points common to every state;
- reconstructed 126 family/state half-power scalar attempts;
- cross-checked all 35 declared all-tight/single-bolt tracked peak frequencies against the source table within the frozen 1 Hz tolerance;
- preserved every scalar refusal state.

Overall scalar admission:

- ADMITTED: 62/126;
- WINDOW_TRUNCATED: 52/126;
- HALF_POWER_CROSSING_NOT_OBSERVED: 7/126;
- NON_IDENTIFIABLE_MODAL_OVERLAP: 5/126.

A refusal is a methodological/model-admission result. In particular, WINDOW_TRUNCATED does not imply that the physical mode has no damping coordinate outside the frozen source window.

## 3. Primary 10 Nm -> 0 Nm result

The primary map contains seven mode families x four single-bolt-loose states = 28 comparisons.

All 28 comparisons show native embedded-response reorganization under the frozen rule.

Only 11/28 comparisons admit chi in both the all-tight and 0 Nm states.

For those 11 comparable pairs:

- similar chi at frozen 1 Hz resolution: 0/11;
- transformed chi: 11/11;
- every transformed chi is larger in the 0 Nm state;
- loose/tight chi ratio range: 1.124 to 4.552;
- median loose/tight chi ratio: 1.747.

The remaining 17/28 primary comparisons are not scalar-comparable:

- WINDOW_TRUNCATED: 11;
- HALF_POWER_CROSSING_NOT_OBSERVED: 4;
- NON_IDENTIFIABLE_MODAL_OVERLAP: 2.

Thus the primary contrast does **not** support the strong statement that full loosening leaves local chi unchanged while only the embedding changes.

Instead, full loosening generally either transforms the admitted local damping coordinate or defeats the frozen scalar-estimation route while the full-field response reorganizes.

## 4. Family-level primary result

| Family (Hz) | Primary admitted pairs | Frozen primary label |
|---:|---:|---|
| 3325 | 4/4 | TRANSFORMED + REORGANIZED |
| 4703 | 1/4 | TRANSFORMED + REORGANIZED |
| 7034 | 3/4 | TRANSFORMED + REORGANIZED |
| 7861 | 1/4 | TRANSFORMED + REORGANIZED |
| 8163 | 2/4 | TRANSFORMED + REORGANIZED |
| 8428 | 0/4 | NO_ADMISSIBLE_SCALAR_CHI comparison + REORGANIZED |
| 8695 | 0/4 | NO_ADMISSIBLE_SCALAR_CHI comparison + REORGANIZED |

For 8428 and 8695 Hz, NO_ADMISSIBLE_SCALAR_CHI is the frozen family-level comparative label: the all-tight scalar itself is admitted, but none of the four primary 0 Nm comparisons admit a paired loose-state scalar under the frozen method.

## 5. Secondary 10 -> 5 -> 0 Nm graded result

The predeclared dose-response layer reveals a more informative sequence.

At 10 Nm:
- all 28 family/bolt reference scalar instances are admitted.

At 5 Nm:
- all 28/28 scalar estimates are admitted;
- 16/28 remain similar to their 10 Nm baseline under the frozen one-bin chi-resolution rule;
- 12/28 are already transformed at that resolution;
- all 28/28 show embedded-response reorganization.

The 16 similar-chi/reorganized comparisons occur in six of seven mode families:

- 3325 Hz: 3/4 bolts;
- 4703 Hz: 1/4;
- 7034 Hz: 4/4;
- 7861 Hz: 2/4;
- 8163 Hz: 3/4;
- 8428 Hz: 3/4;
- 8695 Hz: 0/4.

This is the strongest D02B realization of

LOCAL SCALAR VALIDITY != EMBEDDED RESPONSE SUFFICIENCY.

The local damping coordinate can remain indistinguishable at the frozen measurement resolution while the full-field carrier/response organization has already changed.

At 0 Nm:
- only 11/28 primary loose-state scalar estimates remain admitted;
- every one of those 11 is transformed relative to both the 10 Nm baseline and the corresponding 5 Nm state;
- all 11 admitted 0 Nm chi values are larger than their 5 Nm values.

## 6. Native dose-response organization

The source-native response metrics show a remarkably consistent graded interface effect from 10 -> 5 -> 0 Nm.

Comparing the 5 Nm and 0 Nm single-bolt states relative to all-tight:

- amplitude-shape dissimilarity 1-MACa increases with further loosening in 28/28 family/bolt sequences;
- complex shape dissimilarity 1-CMAC increases in 28/28;
- phase-only 1-CMAC increases in 24/28;
- absolute tracked-frequency shift from all-tight increases in 28/28.

These are native structural-dynamics quantities. They are not new SymC metrics.

The result supports a graded organization response to interface degradation.

## 7. Joint lowercase chi / broader Chi interpretation

D02B supplies a physical realization of two different regimes.

### Moderate interface perturbation

For many 10 -> 5 Nm comparisons:

- local modal chi remains similar at frozen measurement resolution;
- the full-field response organization has already changed.

This corresponds to:

local chi approximately preserved + broader organization reorganized.

### Strong interface perturbation

For 10 -> 0 Nm:

- when local chi remains identifiable, it transforms;
- in many cases the frozen local scalar route is refused/non-identifiable;
- the full-field response reorganizes more strongly.

This corresponds to:

broader organization reorganized + local scalar transformed or no longer identifiable under the frozen representation.

The physical result therefore does not support treating chi and Chi as interchangeable summaries.

It supports investigating their relation as a perturbation-dependent hierarchy.

## 8. Stability-inheritance interpretation

Within this physical P0-Q system, the most defensible inheritance statement is:

The realized modal stability description depends on the state of the bolted interface, and the interface can reorganize embedded response before a local damping coordinate necessarily changes beyond measurement resolution.

With stronger interface degradation, the local coordinate itself often transforms or becomes non-identifiable under the frozen scalar model.

This is consistent with a graded stability-inheritance architecture.

It is **not** evidence for a new force, a universal chi law, a universal threshold, or a master system scalar.

## 9. Native-toolkit comparator

Every quantitative D02B result is already expressible with standard structural-dynamics tools:

- FRF peak tracking;
- half-power damping;
- bolt torque/state;
- MAC;
- CMAC;
- phase-aware CMAC;
- standard mode-trackability/refusal logic.

No additional fitted SymC quantity is required to describe or reproduce the observations.

Therefore the D02B added-value verdict is:

NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE.

The remaining SymC contribution is organizational: explicitly testing preservation, transformation, refusal, and embedded sufficiency across levels under controlled perturbation.

## 10. Evidence ceiling

D02B is not P1.

Candidate selection involved literature/data-availability screening and therefore was not pristine untouched confirmation.

The scalar rules, mode set, windows, similarity rule, refusal conditions, primary contrast, and secondary 10/5/0 stress test were nevertheless frozen before raw FRF outcome inspection.

D02B therefore qualifies the physical architecture and generates a sharper prospective hypothesis, but cannot pay its own promotion debt.

## 11. Post-result discovery

D02B motivates the new prospective hypothesis:

ARCHITECTURE_REORGANIZATION_CAN_PRECEDE_SCALAR_TRANSFORMATION.

In a graded perturbation, carrier/embedded organization may become detectably different before the local scalar stability coordinate exceeds its own measurement-resolution boundary; stronger perturbation may then transform or defeat that scalar representation.

This hypothesis is post-result and receives no confirmation credit from D02B.

It requires a new untouched system or perturbation series with:
- independently controlled substrate/interface state;
- prospectively frozen local scalar;
- independently measured organization metric;
- at least three perturbation levels;
- native comparator;
- explicit null/failure result.
