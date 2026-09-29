# pyFBS Native Hierarchical Conditioning / Error Audit v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** POST-RESULT P0-D ROOT-CAUSE / LIMIT-MAP AUDIT
**Parent result:** PYFBS_CURRENT_METADATA_SVT_LMFBS_RESULT_v0.4.md
**Claim promotion:** PROHIBITED

## Purpose

Map where the already-established native SVT/LM-FBS recovery succeeds and fails across frequency.

The parent P0-Q result is fixed:
- E_DEC = 1.20313;
- E_BASE = 1.25333;
- DEC improves 80.25% of positive-frequency bins;
- interface conditioning is high and variable.

This audit does not change that disposition. It asks whether recovery error and decoupling benefit covary with the conditioning of the native interface matrix and with independent-target response magnitude.

## Frozen source / transform

Recompute exactly the v0.4 current-metadata transformation using:
- Y_A.p, Y_B.p, Y_AB.p;
- decoupling_example_SVT.xlsx;
- pyFBS 1.0.6;
- k=6;
- grouping [1,10];
- same SVT/LM-FBS equations and A extraction 6:12.

No parameter may be changed.

## Per-frequency quantities

For every strictly positive frequency bin f compute:

- c_f = condition number of Y_int(f);
- d_f = normalized Frobenius error of native recovered A;
- b_f = normalized Frobenius error of no-decoupling baseline;
- s_f = normalized Frobenius error of deterministic shuffled correspondence;
- r_f = d_f / b_f;
- q_f = d_f / s_f;
- a_f = Frobenius norm of independently measured target A.

Smaller r_f means more native decoupling benefit over baseline.
Smaller q_f means greater native advantage over the shuffled correspondence.

## Frozen descriptive analyses

1. Spearman rank correlations:
   - log10(c_f) vs log10(r_f);
   - log10(c_f) vs log10(d_f);
   - log10(c_f) vs log10(q_f);
   - log10(a_f) vs log10(d_f);
   - log10(a_f) vs log10(r_f).

2. Divide positive-frequency bins into four equal-count quartiles by c_f. For each quartile report:
   - condition-number range and median;
   - frequency range;
   - median d_f, b_f, r_f, q_f;
   - fraction d_f < b_f;
   - fraction d_f < s_f;
   - median target norm a_f.

3. Report the 20 highest-condition bins and the 20 lowest-condition bins with:
   - frequency;
   - condition number;
   - d_f, b_f, r_f, q_f;
   - target norm.

4. Report aggregate results separately for bins where:
   - d_f < b_f;
   - d_f >= b_f.

No frequency band may be dropped or selected after inspection.

## Interpretation discipline

This is descriptive post-result root-cause mapping. No correlation magnitude is a universal threshold. No p-value or independence assumption is used because adjacent frequency bins are not treated as independent experiments.

Possible conclusions include:
- conditioning appears materially associated with failure;
- conditioning does not explain the failure pattern;
- target-magnitude / normalization effects appear more important;
- multiple factors contribute;
- the present diagnostics remain insufficient.

All are valid Limit Map outcomes.

The parent NATIVE_FRAMEWORK_EQUIVALENT disposition cannot be changed by this audit.
