# Repository and Evidence Governance

This document defines how the SymC Foundations repository distinguishes active scientific authority from historical research artifacts and how changes are admitted without erasing provenance.

## 1. Governing principle

The repository is both a research record and an active investigation. Historical documents are preserved, but they do not automatically govern current claims.

Current interpretation is controlled by the latest explicit README qualifications, active contracts, reproducibility records, validation ledgers, retraction or correction notes, and program-specific status files. When an older artifact conflicts with a later explicit correction, the later governing record controls the current interpretation while the older artifact remains available as history.

## 2. Evidence classes

Repository material should be identified, where relevant, as one or more of the following:

- exact mathematical result;
- software or numerical-method validation;
- synthetic ground-truth validation;
- retrospective physical evidence;
- prospective physical evidence;
- robustness or sensitivity analysis;
- development-only evidence;
- historical or superseded claim;
- unresolved, nonidentifiable, or held result.

A successful result in one class does not automatically promote into another class.

## 3. Scientific change control

A change is **mechanical** when it affects implementation, formatting, automation, provenance capture, tests, navigation, or documentation without changing a frozen scientific assumption or interpretation.

A change is **science-affecting** when it changes, among other things:

- a governing equation or physical model;
- a preregistered or frozen threshold;
- a target, system, mode, or coordinate selection rule;
- an evidentiary label or promotion criterion;
- an admissibility rule;
- a scientific conclusion.

Mechanical changes may proceed with regression checks and clear commit history. Science-affecting changes require an explicit record of why the change is justified and whether it is prospective or retrospective relative to the target result.

## 4. Frozen and superseded records

Once a file is designated frozen or preregistered, it should not be silently edited after target inspection.

If a frozen record contains a mechanical defect that must be corrected:

1. preserve the earlier version;
2. create a versioned successor;
3. state exactly what changed and why;
4. state whether target data had been inspected;
5. avoid altering scientific criteria unless the change is explicitly treated as a science-affecting revision.

## 5. Branch roles

`main` is the public archival and repository-governance branch.

Program branches may contain prospective computational work, temporary development records, active validation workflows, and machine-readable evidence that is not yet appropriate for archival promotion.

Merging a program branch into `main` does not itself promote a scientific result. Promotion requires the evidentiary conditions defined by the relevant program.

## 6. Negative and null results

The repository treats failures as evidence about the tested claim or method. Failed gates, null results, nonidentifiability, refusals, and retractions should remain discoverable and must not be deleted merely because they weaken a hypothesis.

## 7. Reproducibility

Computational evidence should retain enough information to reconstruct the result when practical, including:

- source or input identity;
- code or commit identity;
- environment or dependency information;
- seeds for stochastic work;
- parameter and threshold provenance;
- machine-readable outputs when used by downstream gates;
- hashes for evidence-bearing artifacts where appropriate.

## 8. Citation and attribution

Cite specific papers, datasets, software artifacts, and versions whenever possible. The repository-level `CITATION.cff` is a fallback, not a substitute for citing the exact scientific work used.

## 9. Repository maintenance

Professional maintenance changes may improve navigation, metadata, issue templates, CI reproducibility, and contribution guidance without reopening frozen scientific decisions. Such changes should remain clearly separated from scientific revisions in commit and pull-request history.
