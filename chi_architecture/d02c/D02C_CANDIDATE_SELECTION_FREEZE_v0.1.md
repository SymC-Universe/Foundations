# D02C Untouched Physical Candidate Selection Freeze v0.1

**Date:** 2026-09-23  
**Status:** PRESELECTION_FROZEN_BEFORE_DECISIVE_CANDIDATE_OUTCOME_INSPECTION  
**Authority:** SymC GOM v0.8.3  
**Target discovery:** CA-D007, ARCHITECTURE_REORGANIZATION_CAN_PRECEDE_SCALAR_TRANSFORMATION  
**Parent state:** D02B-CP11-INTERPRETED-CLOSED

## Purpose

Select a genuinely untouched physical system for a prospective test of the temporal/graded ordering proposed by CA-D007.

D02C must be able to test whether an independently measured organization/carrier observable crosses its own frozen detection boundary before, with, or after a licensed local scalar stability coordinate crosses its own frozen boundary as a physical control is varied.

## Excluded systems

The following are ineligible because they were already used or screened during prior work:

- CsPbBr3 phonon system;
- Kullukcu & Hannebauer four-bolt LDV plate;
- Orion beam dataset;
- Zhang et al. 2025 coupled MEMS resonators;
- de Jong et al. beating ringdowns;
- TRC jointed-plate benchmark;
- SiN membrane-sandwich pressure system;
- boundary-condition-controlled plate candidates already inspected in D02B search;
- any other system explicitly documented in D02B candidate-selection provenance.

## Mandatory eligibility axes

A candidate is eligible only if all eight axes are satisfied prospectively.

### 1. Graded perturbation

At least three distinct controlled perturbation levels must exist, including a baseline/reference condition.

The perturbation must be externally defined before response analysis, such as:
- pressure;
- field;
- voltage;
- temperature;
- coupling;
- preload;
- geometry;
- boundary condition;
- concentration;
- another native physical control.

### 2. Licensed local scalar

The same experimental condition must provide enough information to construct a local/modal scalar through an already licensed native relation.

Preferred examples:
- chi = gamma/(2 omega_n);
- chi = 1/(2Q);
- chi = Delta_f/(2 f_n);
- a mathematically equivalent passive second-order native coordinate.

No new scalar normalization may be invented for D02C.

### 3. Independent organization observable

At least one organization/carrier observable must be independently measured and not algebraically derived from the scalar.

Examples:
- mode shape / eigenvector / participation ratio;
- localization / hybridization fraction;
- spatial coherence;
- transfer path / coupling matrix element;
- polarization;
- network/carrier geometry;
- another native structural observable.

### 4. Independent physical outcome or carrier consequence

The organization observable must have a physical interpretation that is not merely a rewritten form of frequency or damping.

### 5. Prospective detection thresholds

The source must provide enough uncertainty, resolution, repeatability, noise, or raw data to freeze separate detection boundaries for:
- scalar transformation;
- organization reorganization.

D02C cannot infer ordering from unequal unquantified measurement sensitivity.

### 6. Strong native comparator

The domain must have a standard native model/analysis capable of fully defeating any SymC-added-value claim.

### 7. Open reproducibility

The decisive data must be machine-readable and fetchable automatically from a stable public source such as:
- Zenodo;
- Figshare;
- OSF;
- GitHub;
- another direct-HTTPS repository.

Manual browser-only download is insufficient.

### 8. One-command packaging

A reviewer must be able to reproduce D02C through:

python chi_architecture/reproduce.py d02c

without manually selecting, renaming, or assembling source files.

## Ranking rule

Among eligible systems, rank only by:

1. completeness of scalar inputs across perturbation levels;
2. independence and directness of the organization observable;
3. number and spacing of perturbation levels;
4. availability of quantified uncertainty/repeatability for both scalar and organization measures;
5. native comparator strength;
6. automated source accessibility;
7. simplicity of one-command reproduction.

Do not rank by:
- whether organization appears to move first;
- whether scalar appears to move first;
- closeness to chi=1;
- exceptional-point proximity;
- effect magnitude;
- narrative attractiveness;
- agreement with D02B.

## Selection rule

Select the highest-ranked candidate that satisfies all mandatory axes.

If no candidate satisfies all eight axes, return:

NO_ELIGIBLE_D02C_SYSTEM

and preserve that outcome.

## Predeclared ordering outcomes

The eventual prospective D02C result must classify one of:

- ORGANIZATION_PRECEDES_SCALAR
- SCALAR_PRECEDES_ORGANIZATION
- SIMULTANEOUS_WITHIN_FROZEN_RESOLUTION
- ORGANIZATION_CHANGES_SCALAR_DOES_NOT
- SCALAR_CHANGES_ORGANIZATION_DOES_NOT
- NEITHER_CHANGES
- ORDERING_NON_IDENTIFIABLE
- NO_ADMISSIBLE_SCALAR_CHI
- NATIVE_MEASUREMENT_SENSITIVITY_PRECLUDES_ORDERING

These outcomes are descriptive. They do not by themselves establish new dynamics.

## Failure logic for CA-D007

CA-D007 is weakened or falsified for the selected system if:

- scalar transformation clearly precedes organization reorganization;
- both changes are simultaneous within frozen uncertainty over the graded series;
- apparent early organization change disappears after uncertainty/repeatability treatment;
- ordering can be explained solely by unequal measurement sensitivity;
- organization change is absent despite scalar transformation;
- the candidate fails scalar admission or carrier identifiability in most decisive conditions.

## Promotion ceiling

Even a favorable D02C result remains domain-specific physical evidence.

No universal law, universal ordering, universal chi threshold, or master Chi scalar is authorized.

## External search provenance

Undermind workspace:
Stability Inheritance Publication Build

Search:
D02C untouched graded physical candidate search

The search goal explicitly excludes prior systems and forbids ranking by outcome direction.
