# D02B Candidate Selection Correction v0.3

**Date:** 2026-09-22  
**Status:** PRENUMERIC_REPRODUCIBILITY_CORRECTION  
**Authority:** SymC GOM v0.8.3  
**Supersedes active selection in:** D02B_CANDIDATE_SELECTION_CORRECTION_v0.2.md

## Reason for correction

The Orion Beam Dataset satisfied the six scientific eligibility axes, but its Mendeley Data host returned Cloudflare HTTP 403 responses to automated GitHub Actions and public API probes.

The user explicitly requires reviewer reproduction to proceed from GitHub without manual file scavenging.

The original frozen D02B ranking placed:

1. machine-readable data accessibility;
2. directness of same-condition frequency+damping measurements;
...
6. simplicity of automated reproduction

ahead of favorable result direction.

Therefore, retaining Orion after the automated-acquisition failure would violate the frozen ranking.

No Orion scientific response values were parsed before this correction.

## Replacement candidate

Kullukcu & Hannebauer 2026:

"Full-field laser-Doppler-vibrometry frequency-response-function data for a four-bolt aluminum plate under bolt-torque variation"

Dataset DOI: 10.5281/zenodo.20038951  
Related preprint: arXiv:2609.05378

## Why it is eligible under the frozen rules

### 1. Direct/recoverable same-condition scalar inputs

Raw H1 FRFs supply frequency and amplitude for each torque state.

The dataset explicitly documents half-power bandwidth as a native processed quantity and supplies the raw FRFs required to recover same-condition half-power bandwidth for each eligible resonance/torque state.

Licensed modal scalar:

chi = Delta_f / (2 f_n) = 1/(2Q)

only when the isolated/trackable resonance passes a predeclared local second-order / half-power adequacy test.

### 2. Independent carrier/coupling structure

The physical organization is a four-bolt jointed plate.

Bolt identities B1-B4 and all 18 torque configurations are independently encoded in torque_states.csv.

The data contain full-field 51-point LDV response, amplitude and phase, allowing carrier/shape comparisons through native MAC/CMAC/FRAC-family measures.

### 3. Controlled organization change

The experiment deliberately changes bolt torque:

- all-tight reference;
- all-loose state;
- four single-bolt 10/5/0 Nm sequences;
- mixed multi-loose states.

### 4. Independent response consequence

Frequency shifts, full-field FRF-shape changes, amplitude/phase response, and spatial dissimilarity are available independently of the scalar damping coordinate.

### 5. Strong native comparator

Native structural-dynamics analysis includes FRF peak tracking, half-power bandwidth, MAC/CMAC, local FRAC-type spatial sensitivity, and standard bolt-torque structural-health-monitoring interpretation.

### 6. Reproducibility

Zenodo provides:

- raw exports;
- documentation;
- processed CSV tables;
- Python scripts;
- checksums;
- requirements/environment files;
- Makefile and run_all.sh;
- Data Package schema.

The small documentation, processed-table, and script archives can be fetched automatically before the 635 MB raw archive is needed.

## Selection outcome

D02B v0.3 selects the four-bolt Zenodo LDV dataset.

Orion remains a scientifically eligible alternate but is retired from active D02B because its public host does not support the required automated GitHub reproduction route.

The earlier Zhang MEMS candidate remains retired from D02B for lower completeness ranking.

## Pre-result status

No numerical response values from the selected Zenodo dataset have been inspected for D02B before this correction.

Public metadata, variable names, file structure, measurement protocol, and half-power-bandwidth availability were inspected only to establish eligibility and reproducibility.
