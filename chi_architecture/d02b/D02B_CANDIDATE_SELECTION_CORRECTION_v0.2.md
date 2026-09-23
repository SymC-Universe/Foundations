# D02B Candidate Selection Correction v0.2

**Date:** 2026-09-22  
**Status:** PRENUMERIC_SELECTION_CORRECTION  
**Authority:** SymC GOM v0.8.3

## Why this correction exists

D02B v0.1 selection criteria were frozen before candidate outcome inspection. A provisional MEMS candidate (Zhang et al. 2025) was then selected before the external completeness search had finished.

The completed literature completeness audit subsequently identified stronger candidates under the already-frozen ranking rule.

Because the ranking contract explicitly requires selecting the highest-completeness eligible system, preserving the provisional MEMS choice would violate our own preregistered selection logic.

This correction therefore occurs **before numerical source-data extraction** and is treated as governance compliance, not result-based candidate switching.

## External completeness audit

The completed Undermind search "D02B physical candidate completeness search" identified four highest-completeness candidates:

- TRC benchmark;
- Orion bolted-beam dataset;
- SiN membrane sandwich under controlled pressure;
- boundary-condition-controlled plate.

Full-text eligibility verification then showed:

### TRC benchmark
- strong controlled joint/alignment/amplitude perturbations;
- direct frequency/damping estimates;
- strong native validation;
- but no explicit public machine-readable vibration dataset or reproduction code for the analyzed results.

Result: fails D02B reproducibility axis 6.

### SiN membrane sandwich
- same-condition frequency and Q versus controlled pressure;
- independent coupled-mode structure;
- strong physical intervention;
- but no public source-data/code repository identified.

Result: fails D02B reproducibility axis 6.

### Boundary-condition-controlled plate
- strong physical design in the search summary;
- public raw-data status not established.

Result: not promoted over a fully verified open-data candidate.

### Orion beam
- two-beam bolted-joint physical structure;
- independently defined lap-joint/contact-patch interface;
- controlled tightening torque;
- controlled excitation amplitude;
- raw and processed FRF/transmissibility data publicly downloadable;
- Matlab post-processing support supplied;
- natural frequency directly recoverable;
- damping directly recoverable from same-condition FRF data using frozen native half-power/modal procedures;
- strong native jointed-structure / FRF / nonlinear oscillator comparators.

Result: satisfies all six frozen D02B eligibility axes.

## Corrected D02B selection

**Selected system:** Orion Beam Dataset.

Dataset DOI: 10.17632/p4fg6snh3r.1

Data article DOI: 10.1016/j.dib.2021.107627

Companion native-method article DOI: 10.1016/j.ymssp.2021.108172

## Provisional MEMS branch status

The earlier Zhang et al. 2025 source contract and schema-acquisition workflow are retained as provenance but are now marked:

ABORTED_PRENUMERIC_SELECTION_CORRECTION

No D02B numerical outcome was extracted from that workbook before this correction.

It may be reused later only under a new experiment identifier or explicit D02B extension, not silently substituted back into D02B.

## Evidence status

This correction was driven by the frozen completeness ranking and completed candidate audit, not by a favorable or unfavorable Orion outcome.

The selected Orion numerical data have not yet been inspected for the D02B test.
