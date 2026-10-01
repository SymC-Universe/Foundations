# Parallel Non-Compute Work Queue

**Date:** 2026-09-30  
**Applies while:** an external/local Python computation is active  
**Rule:** do not modify active scripts, inputs, result paths, checkpoints, environments, or run-control files.

## Authorized work that cannot contaminate the active run

### 1. Method-first / tool-emergence design — COMPLETE

Formalize the methodology as the first tool and make executable-tool emergence conditional rather than mandatory. See `METHODOLOGY_TOOL_EMERGENCE_PROTOCOL.md`.

### 2. Representation qualification — FROZEN FOR NEXT REVIEW

The representation ladder is scalar -> modal/scale-resolved -> coupled/conglomerate, with REFUSE and NEED MORE INFO as first-class outputs. Promotion is based on information retained and discriminating utility, not visual complexity.

### 3. Adversarial map — ACTIVE

Current required comparison families:
- flat LambdaCDM / GR;
- dynamical-DE alternatives;
- free neutrino mass;
- modified gravity;
- supernova-sample sensitivity;
- explicit DM-DE interaction models when a reproducible matched likelihood is available;
- projection / prior-bound / model-form effects.

No alternative is allowed to stand in for a dataset-matched adversary merely because its chain is convenient.

### 4. Novelty gate — ACTIVE

Search target is not generic cosmological model comparison. Prior art already includes Bayesian model selection, null/consistency tests, Gaussian-process and other non-parametric reconstructions, profile likelihoods, and full-shape-versus-compressed comparisons.

The provisional novelty question is:

> Can a preregistered representation-qualification procedure determine when scalar, resolved-modal, or coupled structure is warranted, while returning explicit REFUSE and NEED-MORE-INFO states and preserving falsification paths?

This must be collision-tested before any novelty claim is made.

### 5. Next-result decision table — PREPARED

When the active Python result arrives, classify it without changing thresholds post hoc:

- expected result + native explanation sufficient -> retain as native-model result; do not promote architecture;
- result changes materially only under one nuisance/model family -> classify as model-dependent and investigate that dependency;
- resolved structure survives matched adversaries and lower-order representation loses predictive/information content -> admit modal/coupled qualification testing;
- unresolved because covariance, resolution or model coverage is inadequate -> NEED MORE INFO;
- preregistered criterion fails -> REFUSE the candidate representation and preserve the failure.

### 6. Literature collision targets — ACTIVE

Prioritize:
- representation and compression sufficiency in cosmology;
- growth-versus-expansion consistency/null tests;
- full-shape versus BAO-only information gain;
- non-parametric dark-energy reconstruction;
- dark degeneracy / interacting dark-sector identifiability;
- modified-gravity and neutrino degeneracies;
- methods that explicitly return indeterminate/refusal outcomes rather than forced model choice.

### 7. No-touch boundary for current run

Until the active computation ends, do not:
- edit any `.py` file used by the run;
- edit `requirements.txt`;
- alter `cosmology_desi/data/**` or `cosmology_desi/results/**`;
- rerun, cancel, restart or duplicate the active job;
- change scientific thresholds based on partial output.

Documentation-only commits on the investigation branch are permitted.
