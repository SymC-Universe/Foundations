# Fine Steering Mirror Published Baseline Adjudication v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** DERIVED EXTERNAL BASELINE EVIDENCE / P0-Q ONLY
**Raw frozen FSM protocol:** NOT EXECUTED; raw binary unavailable in current runtime
**Empirical Stability Inheritance claim:** NONE

## Source identity

Official benchmark repository:
https://github.com/merijnfloren/fsm-benchmark-data

Source notebook:
baseline_results/analyze_models.ipynb

Notebook Git blob:
18aff6b6ea4ebb2d49e60c5adfcca2416fa0b0dd

The notebook evaluates official test sets using the benchmark's supplied baseline models and official nonlinear_benchmarks error metrics.

The repository README states that the linear baselines are separate 28th-order state-space models fitted at 100, 200, and 300 mV, plus a single nonlinear LFR model fitted across all three amplitudes.

## Published test results

Relative error reported by the official baseline notebook:

| Model | test 100 mV | test 200 mV | test 300 mV |
|---|---:|---:|---:|
| Linear BLA trained at 100 mV | 8.38% | 20.50% | 32.71% |
| Linear BLA trained at 200 mV | 21.78% | 7.95% | 17.34% |
| Linear BLA trained at 300 mV | 32.84% | 15.17% | 5.63% |
| Single linear BLA trained on all amplitudes | 18.61% | 6.61% | 16.28% |
| Single nonlinear NL-LFR trained on all amplitudes | 6.37% | 4.84% | 4.19% |

Corresponding RMSEs reported by the notebook:

| Model | test 100 mV | test 200 mV | test 300 mV |
|---|---:|---:|---:|
| Linear BLA 100 | 0.1142 um | 0.5548 um | 1.319 um |
| Linear BLA 200 | 0.2963 um | 0.2161 um | 0.6987 um |
| Linear BLA 300 | 0.4459 um | 0.4119 um | 0.2277 um |
| Pooled linear BLA | 0.2523 um | 0.1790 um | 0.6575 um |
| Pooled nonlinear NL-LFR | 0.08662 um | 0.1309 um | 0.1686 um |

## Adjudication

Among the **linear** models:
- 100 mV test: amplitude-specific 100 mV BLA is best.
- 200 mV test: pooled linear BLA is best, narrowly outperforming the 200 mV-specific BLA.
- 300 mV test: amplitude-specific 300 mV BLA is best.

Therefore the public baseline results do **not** support a simple rule that every operating amplitude requires its own local linear representation.

The shared nonlinear NL-LFR is better than every linear baseline at all three amplitudes.

## Architecture interpretation

The result supports a stronger and less simplistic relation than amplitude-specific specialization:

> When operating regime changes expose native nonlinear/hysteretic behavior, a richer shared representation can transport across regimes better than multiple locally specialized linear representations.

This is consistent with the benchmark's native description of piezo hysteresis and is not Stability Inheritance novelty.

For the current relation matrix:
- scalar chi remains NOT ADMITTED from these data by default;
- modal/state representation is task- and regime-dependent;
- the system-level response architecture cannot be reduced to "one amplitude = one architecture";
- representation class can matter more than operating-condition specialization;
- native nonlinear models can dominate locally fitted linear models across conditions.

## Relation to the frozen FSM raw-data protocol

FSM_CROSS_AMPLITUDE_PROTOCOL_v0.1.md remains a valid pre-exposure protocol, but it was **not executed** because the raw binary arrays could not be transferred into the current compute runtime.

These published baseline outputs are not substituted for that protocol. They are a separate derived external-evidence lane.

If raw access becomes available later, the frozen frequency-response protocol may still be executed unchanged.

## Claim ceiling

- external measured representation evidence: INFORMATIVE;
- universal amplitude-conditioned representation rule: NOT SUPPORTED;
- native nonlinear shared representation transport: SUPPORTED by published benchmark baseline;
- empirical Stability Inheritance: NOT TESTED;
- chi threshold or damping claim: NOT APPLICABLE.
