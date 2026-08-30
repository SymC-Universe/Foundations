# Repository Guide

This repository contains published papers, historical research versions, LaTeX sources, figures, archives, reproducibility materials, and active computational-development branches. The root directory is intentionally archival and therefore contains multiple generations of work.

This guide explains how to navigate the repository without mistaking an older artifact for the current scientific position.

## Start here

1. Read [`README.md`](./README.md) for the current Foundations-level interpretation and domain-licensing rules.
2. Read [`GOVERNANCE.md`](./GOVERNANCE.md) for evidence classes, change control, frozen-record handling, and supersession rules.
3. Use [`CITATION.cff`](./CITATION.cff) for repository-level citation metadata, but cite the specific paper, DOI, dataset, or software artifact whenever available.
4. Use [`CONTRIBUTING.md`](./CONTRIBUTING.md) before submitting a correction, code change, or scientific extension.

## Branch roles

### `main`

The public archival and governance branch. It contains the Foundations research record and the current top-level qualification of historical claims.

### `substrate-inheritance`

The active prospective substrate-inheritance program. It contains computational validation, frozen correspondence rules, real-system ingestion contracts, machine-readable evidence records, and its own current-status README.

Material on an active branch is not automatically a promoted physical result. Read the program-specific status and evidence ledger before interpreting it.

## Root artifact conventions

The root contains several kinds of files:

- `*.pdf`: rendered papers, supplements, figures, or historical releases;
- `*.tex`: editable LaTeX sources where preserved;
- `*.zip`: archived data, scripts, or release bundles;
- figure files such as `Fig*.pdf`, `Fig*.png`, and `Fig*.svg`: publication assets;
- `README.md`: current repository-level scientific framing;
- `LICENSE`: repository licensing terms.

A filename or modification date alone does not establish which scientific claim is current.

## Current versus historical material

Historical PDFs and source files remain available for research provenance. Some contain broader claims made before later generator-first, domain-licensing, or prospective-inheritance restrictions were adopted.

Where historical material conflicts with a later explicit correction, retraction, active contract, validation ledger, reproducibility record, or current README qualification, the later governing record controls the present interpretation.

The historical file should still be cited when discussing the historical claim itself.

## Published work

The repository README identifies the published Scientific Reports stability-architecture paper and its DOI. For any paper with a DOI or versioned archive, use that work's own bibliographic identity rather than citing the repository generically.

## Computational evidence

Computational artifacts should be interpreted according to their evidence class. In particular:

- passing software tests validates implementation behavior, not a physical hypothesis;
- synthetic ground-truth tests validate inference machinery under constructed cases;
- development-only physical work is not automatically prospective validation;
- failed gates, refusals, nonidentifiability, and null results remain part of the evidence record.

## Reporting a problem

Use GitHub Issues for specific, evaluable problems. Structured templates are provided for:

- scientific corrections;
- reproducibility or computational defects;
- documentation and metadata improvements.

Use GitHub Discussions for exploratory questions or ideas that are not yet a specific correction.

## Why files are not being aggressively reorganized

The repository has an established citation and provenance history. Large-scale renames or moves can break external links and obscure lineage. Professionalization therefore favors stronger navigation, explicit status authority, versioned supersession, and structured contribution rules over cosmetic rearrangement of historical artifacts.
