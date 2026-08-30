# Recommended GitHub Repository Settings

This file records the intended GitHub-hosting configuration for the Foundations repository. These settings are repository mechanics only and do not alter scientific content.

Some settings live in GitHub's repository metadata rather than in version-controlled files. Keeping the intended configuration here makes those choices auditable.

## About panel

### Description

Recommended description:

> Foundational research for the generator-first SymC framework: stability boundaries, spectral and modal structure, exceptional points, and prospective substrate-inheritance tests.

This replaces older wording that describes chi approximately 1 as a universal cross-domain stability boundary. That wording no longer matches the current repository-level scientific qualifications.

### Suggested topics

Prefer topics that describe the current work without implying a demonstrated universal theory:

- stability-theory
- exceptional-points
- dissipative-systems
- spectral-theory
- mathematical-physics
- computational-physics
- open-quantum-systems
- control-theory
- nonlinear-dynamics
- substrate-inheritance
- reproducible-research
- scientific-computing

Historical domain topics may remain where they accurately describe archived work, but broad promotional topics such as `unified-theory` should not be used as a current repository-level scientific claim.

## Pull requests

Recommended repository settings:

- enable squash merging;
- allow merge commits or rebase merges only if they remain useful for active research branches;
- enable automatic deletion of head branches after merged pull requests;
- keep the pull-request template and CODEOWNERS file active.

For repository-governance and narrow mechanical changes, a squash merge keeps the public history readable while preserving the full PR discussion.

## `main` protection

Recommended branch or ruleset controls for `main`:

- block force pushes;
- block branch deletion;
- require changes to arrive through a pull request for normal work;
- require conversation resolution before merge;
- allow an administrator bypass for genuine recovery situations;
- do not require signed commits unless the project deliberately adopts a signing workflow, because historical commits are not uniformly signed;
- do not require a status check that does not actually exist on `main`.

The goal is to protect archival history without creating ceremonial checks that do not validate anything.

## `substrate-inheritance` protection

Recommended controls for the active prospective branch:

- block force pushes;
- block branch deletion;
- require pull requests for changes to frozen contracts, workflows, inference code, or evidence logic;
- require the `validate` GitHub Actions job before merging changes that trigger the substrate-inheritance workflow;
- require the branch to be current with its target before a protected merge when GitHub can enforce that check reliably;
- require conversation resolution;
- preserve an administrator recovery path for infrastructure failures.

A failed scientific or computational validation should not be bypassed merely to obtain a green branch. Mechanical CI failure may be repaired, but scientific criteria should remain frozen unless an explicit science-affecting revision is recorded.

## `agent/stability-arc-gfsa-v072` protection

This is a canonical paused research-lineage branch, not a temporary automation branch. Its current-state record declares the internal handoff closed and the research intentionally paused while preserving a separate science-freeze anchor and open historical provenance/source holds.

Recommended controls:

- block force pushes;
- block branch deletion;
- require pull requests for future changes once branch protection is enabled;
- require conversation resolution for any future resumption or maintenance PR;
- do not require an unrelated current `main` CI check;
- preserve an administrator recovery path;
- do not rebase or merge the branch merely to eliminate its divergence from `main`.

If Stability Arc work resumes, any new required status check should be added only after an actual validation workflow exists for the resumed campaign. Historical workflows and frozen results should not be mechanically rerun and reinterpreted merely to satisfy a newly invented branch rule.

## Actions

Recommended Actions posture:

- keep workflow permissions read-only unless a workflow specifically needs more;
- pin external actions to reviewed commit SHAs;
- pin evidence-bearing validation environments where practical;
- archive realized runtime environments with computational evidence;
- avoid introducing repository secrets into workflows unless there is a clear requirement;
- review dependency/action updates as reproducibility changes before adoption.

## Issues and discussions

- keep structured issue forms enabled for scientific corrections, reproducibility defects, documentation changes, and proposed research extensions;
- keep Discussions available for exploratory questions that are not yet specific corrections;
- avoid using issue closure to erase unfavorable scientific findings.

## Releases and archival material

Use GitHub Releases only when a repository state is intended to be a stable public release. Do not create a release merely to mark an internal computational checkpoint.

Historical PDFs, ZIPs, and source files should not be renamed or reorganized solely for cosmetic reasons if doing so would break links or obscure provenance.

## Periodic review

Review these settings when:

- the project gains additional maintainers;
- a new required CI workflow is introduced;
- an active research branch becomes archival or a paused branch resumes;
- repository permissions or security requirements materially change;
- a current metadata field no longer matches the scientific position documented in `README.md` and `GOVERNANCE.md`.
