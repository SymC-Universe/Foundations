# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02B-CP1-SYSTEM-AND-SOURCE-CONTRACT-FROZEN  
**Date:** 2026-09-22  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.3

## Selected D02B system

Zhang et al. 2025 coupled nonlinear MEMS resonators.

Article DOI: 10.1038/s41467-025-59292-2  
Source-data DOI: 10.6084/m9.figshare.28714484  
Code DOI: 10.5281/zenodo.15162385

Selection was made under the precommitted completeness ranking in D02B_CANDIDATE_SELECTION_FREEZE_v0.1.md.

## Frozen scientific contract

Read:

chi_architecture/d02b/D02B_SOURCE_CONTRACT_v0.1.md

before touching machine-readable source outcomes.

## Evidence ceiling

Qualitative outcome descriptions were encountered during eligibility verification. D02B is therefore physical P0-Q qualification, not untouched P1 confirmation.

The numerical extraction and decision rules are frozen before workbook inspection.

## Resume rule

1. Read this checkpoint and D02B_SOURCE_CONTRACT_v0.1.md.
2. Acquire the source workbook and archived author code.
3. Record source hashes before analysis.
4. Inspect workbook schema/layout only and checkpoint the sheet/column mapping.
5. Do not change the primary-response hierarchy after seeing numeric outcome values.
6. Implement a one-entrypoint parser/analysis.
7. Execute in GitHub Actions.
8. Archive run ID, artifact digest, source hashes, and results before scientific interpretation.
9. Reproduce via python chi_architecture/reproduce.py d02b.
