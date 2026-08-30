# Contributing to SymC Foundations

Thank you for examining the work critically. Contributions are welcome when they improve correctness, reproducibility, provenance, documentation, or the clarity of the scientific record.

This repository is a research archive as well as an active computational workspace. Historical files are preserved for provenance, so a contribution should normally correct the current governing record rather than silently rewriting older artifacts.

## Before opening an issue or pull request

Please identify which kind of contribution you are making:

1. **Scientific correction**: a mathematical, physical, statistical, interpretive, or evidentiary error.
2. **Reproducibility or computational defect**: code, workflow, environment, data, hash, schema, or execution behavior that prevents an independent reconstruction.
3. **Documentation improvement**: wording, navigation, citations, formatting, metadata, or explanatory material that does not change the scientific content.
4. **New scientific extension**: a proposed analysis, system, derivation, or test that goes beyond the current registered scope.

Use the corresponding GitHub issue template when possible.

## Research-integrity requirements

Changes that affect scientific interpretation must preserve the following rules:

- Do not select a model, mode, coordinate, threshold, system, or comparison because it gives a preferred downstream result.
- Do not weaken a frozen or preregistered gate after inspecting the target outcome.
- Do not promote a synthetic validation result into physical evidence.
- Keep distinct physical quantities distinct unless an explicit derivation licenses the mapping.
- Preserve negative results, refusals, nonidentifiability, failed prospective tests, and superseded claims in the record.
- Identify whether a change is prospective, retrospective, robustness-only, or historical clarification.
- When a current contract supersedes an older document, update the current-status record and preserve the historical artifact unless there is a compelling archival reason not to.

The active substrate-inheritance program has additional frozen correspondence and input contracts on its dedicated branch. Those contracts govern that program where applicable.

## Evidence expected for scientific corrections

A strong scientific issue or pull request should include:

- the exact file, equation, figure, code path, dataset row, or claim affected;
- the current statement or behavior;
- the reason it is incorrect or insufficient;
- a derivation, reproducible calculation, source, or minimal counterexample;
- the proposed correction;
- whether the correction changes a conclusion, only a method, or only presentation.

Claims that depend on external literature should provide stable bibliographic information such as DOI, journal, year, and title. Where numerical extraction is involved, identify the table, equation, or other source location when possible.

## Computational contributions

For code or workflow changes:

- prefer deterministic or seeded tests where randomness is necessary;
- add a regression test for a repaired defect when practical;
- keep generated evidence records machine-readable when the surrounding workflow already does so;
- record environment or dependency requirements needed for reproduction;
- do not silently change physical thresholds, frozen schemas, or scientific labels inside a mechanical refactor;
- preserve fail-closed behavior at provenance and admissibility boundaries.

## Pull requests

Keep pull requests narrow enough to review. The PR description should state:

- what changed;
- why it changed;
- whether scientific assumptions changed;
- what tests or checks were run;
- what files or claims are intentionally not changed;
- any remaining holds or unresolved questions.

Documentation-only changes should say so explicitly.

## Style

Use plain, professional scientific language. Distinguish established results from hypotheses, tests, and open questions. Avoid promotional wording and avoid presenting a research program as a universal law unless the evidence and current governing documents explicitly support that statement.

## Licensing

By contributing, you agree that your contribution may be distributed under the repository's CC BY 4.0 license unless a file states otherwise.
