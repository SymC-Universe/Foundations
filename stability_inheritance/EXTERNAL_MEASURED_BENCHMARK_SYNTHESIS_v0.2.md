# External Measured Benchmark Synthesis v0.2

**Date:** 2026-09-28  
**Governance:** SymC GOM v1.0  
**Status:** P0-Q CROSS-BENCHMARK SYNTHESIS / NOT A CONFIRMATORY CLAIM  
**Benchmarks:** Silverbox, Fine Steering Mirror, Wiener-Hammerstein 2009, F-16 GVT  
**Empirical Stability Inheritance claim:** NONE

## Purpose

Compare the current public measured-data qualification results without treating native nonlinear modeling, operating-regime dependence, or better predictive fit as Stability Inheritance.

The synthesis asks only:

1. what representation failures recur across measured systems;
2. whether scalar, modal/state, and architecture-level labels are actually licensed;
3. what the strongest native explanation already provides;
4. which unresolved SI question remains after the native explanation is admitted.

## Benchmark matrix

| Benchmark | Native system issue | Frozen/available comparison | Measured result | chi status | Chi status | Chi_arc status | Native explanation | SI consequence |
|---|---|---|---|---|---|---|---|---|
| Silverbox | Duffing-like cubic feedback | linear ARX-2 vs cubic NARX-2 on reserved measured segments | nonlinear model lower one-step and free-run error on both reserved segments | physical chi REFUSED; model-local chi candidate diagnostic only | linear state representation locally useful but task-limited | no independent Chi_arc inheritance object constructed | native nonlinear oscillator/system-identification structure | representation adequacy differs from local fit; no inheritance claim |
| Fine Steering Mirror | piezo hysteresis / operating-amplitude dependence | published amplitude-specific linear BLAs, pooled linear BLA, shared nonlinear NL-LFR | shared nonlinear NL-LFR beats every linear baseline at 100/200/300 mV; pooled vs amplitude-specific linear ordering is mixed | chi NOT ADMITTED | linear state representation regime/task dependent | no independent Chi_arc inheritance object constructed | native nonlinear hysteretic model transports across amplitudes | representation class can matter more than local specialization; no inheritance claim |
| Wiener-Hammerstein 2009 | static nonlinearity between LTI blocks | frozen linear ARX-8 vs polynomial NARX-8 on official held-out test | nonlinear M2 improves one-step RMSE ~17.6% and free-run RMSE ~45.0% without divergence | chi NOT ADMITTED | linear autoregressive representation highly accurate locally but less adequate recursively | no independent Chi_arc inheritance object constructed | native Wiener-Hammerstein/nonlinear system-identification structure | local accuracy does not imply recursive architectural adequacy; no inheritance claim |
| F-16 GVT | clearance/friction nonlinearity at payload mounting interface | frozen Level-1 invariant FRF vs force-amplitude-conditioned interpolation on reserved FullMSine levels 2/4/6 in 6.5-8.2 Hz torsional band | amplitude-conditioned representation lower error on all three reserved levels; error ratios 0.533, 0.117, 0.0335 | chi NOT ADMITTED | native multi-output FRF organization is amplitude-conditioned | no unique Chi_arc object claimed, but system-level organization is directly supported | native nonlinear structural/interface dynamics | embedded interface regime conditions realized system response; architecture-supporting native evidence |

## Cross-benchmark Function Map

### Function F-EM1 - Local reduced representations can remain useful

All four measured systems permit useful reduced or local representations in at least some operating or prediction tasks.

This supports:

**LOCAL_REPRESENTATION_USEFUL**

It does not imply:
- scalar sufficiency;
- global validity;
- inheritance;
- a unique Stability Architecture coordinate.

### Function F-EM2 - Richer native representation can transport better across the declared task

Silverbox:
- cubic nonlinear terms improve both local and recursive measured prediction.

FSM:
- one shared nonlinear representation outperforms multiple locally specialized linear models across all measured amplitudes.

WH2009:
- polynomial nonlinear autoregression improves both held-out one-step and long recursive simulation.

F-16 GVT:
- a force-amplitude-conditioned complex FRF representation built only from designated estimation levels improves held-out prediction at every reserved excitation level in the published wing-torsion band;
- the interface-adjacent relative-response proxy changes strongly across excitation level, while the effect is also visible at the excitation-point output.

This supports the general qualification statement:

> representation class must be matched to the system/task/regime rather than inferred from local fit quality alone.

This statement is native-model compatible and is not SI novelty.

## Cross-benchmark Limit Map

### Limit L-EM1 - Good one-step/local fit does not license recursive/global adequacy

The clearest measured example is WH2009:
- M1 one-step NRMSE ~0.00364;
- M1 free-run NRMSE ~0.1812.

A locally accurate linear model can therefore be operationally inadequate for the recursive task.

Silverbox shows the same direction with a smaller but material gap between linear and nonlinear free-run performance.

### Limit L-EM2 - Operating-condition specialization is not the same as architectural adequacy

FSM rejects a simplistic rule that each amplitude requires its own local linear model.

A pooled linear model can outperform an amplitude-specific linear model at 200 mV, while a shared nonlinear model outperforms all of them.

Therefore:
- operating regime matters;
- representation class matters;
- local specialization alone is not the architecture.

### Limit L-EM3 - Richer predictive model is not automatically Chi_arc

None of the four measured benchmark results independently constructs an architecture-level/conglomerate object that is separate from the predictor being scored.

Therefore the following inference is refused:

[
\text{better nonlinear model} \Rightarrow \Chi_{\mathrm{arc}}
]

A Chi_arc claim still requires an independently motivated/reconstructed system-level object under the project definition.

### Limit L-EM4 - Scalar chi is not supported program-wide by these benchmarks

- Silverbox permits only a model-local damping-ratio-like candidate from a fitted linear pole pair.
- FSM does not admit chi from the available published baseline evidence.
- WH2009 does not admit physical chi from the input/output record.

Thus the external measured benchmark set currently strengthens the case for **conditional scalar admission**, not a universal scalar axis.

## What the three benchmarks do NOT test

None of these three measured lanes establishes:

- lower-level source characterization followed by higher-level target reconstruction;
- carrier-specific inheritance;
- source-to-descendant preservation;
- causal cross-level transfer beyond native system identification;
- an independently measured Chi_arc object receiving inherited structure;
- a universal chi-to-Chi-to-Chi_arc ladder.

Therefore they qualify representation/refusal logic, not Stability Inheritance itself.

## Residual SI question after measured-data qualification

After admitting the native nonlinear explanations, the remaining discriminating question is narrower:

> When source and target representations are independently defined across an actual embedding, coupling, or lineage transition, does lower-level stability-relevant structure add a nonredundant, carrier-specific constraint on the target architecture beyond the strongest native target model?

That question remains untested by Silverbox, FSM, WH2009, and F-16 GVT.

## Current measured-data disposition

- REPRESENTATION_QUALIFICATION_TRANSPORT: SUPPORTED across four measured benchmark lanes.
- ARCHITECTURE_SUPPORTING_NATIVE: SUPPORTED directly in F-16 GVT for an embedded interface-regime/system-response relation.
- CONDITIONAL_SCALAR_ADMISSION: SUPPORTED as a governance/qualification rule.
- RICHER_MODEL_EQUALS_CHI_ARC: REFUSED.
- NONLINEAR_MODEL_SUCCESS_EQUALS_INHERITANCE: REFUSED.
- EMPIRICAL_STABILITY_INHERITANCE: NOT TESTED.
- NATIVE_MODEL_FIRST: REINFORCED.

## Next computational implication

The highest-value nonphysical next tests are those that add at least one of the missing SI gates rather than another generic nonlinear-vs-linear benchmark:

1. independent source and target representations;
2. explicit correspondence/carrier map;
3. frozen source-to-target transformation;
4. target prediction on measured data;
5. intervention or matched-condition specificity;
6. strongest native target comparator.

Public structural substructuring data such as F-16 GVT remains preferred if provenance-clean raw access becomes available.


## F-16-specific architectural contribution

F-16 differs from the other external measured lanes because the benchmark supplies both a native localized mechanism context and spatially separated responses on opposite sides of the interface plus the excitation location. The frozen FullMSine test therefore bears on the organization of response across an embedded interface rather than only on generic nonlinear model class.

The result does not prove a new causal mechanism. The benchmark authors already identify clearance and friction at the payload interface as the expected dominant nonlinearity. Its contribution to the Stability Architecture case is integrative: a local interface regime is measurably associated with broad changes in the realized response representation, and an amplitude-conditioned map learned from designated estimation levels transports to independent reserved levels.

The next useful question is whether this relation survives an independent excitation family without redesigning the analysis around the FullMSine outcome.
