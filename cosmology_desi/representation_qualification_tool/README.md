# Representation Qualification Engine

This directory contains the first executable scaffold for the five-component Stability Architecture methodology.

It is deliberately a **decision engine, not a scientific oracle**. The engine receives already-evaluated, preregistered gate evidence and returns a disposition. It never chooses thresholds, invents observables, selects adversaries, or changes hypotheses.

## Five integrated components

1. local (chi) stability coordinate;
2. modal / eigenstructure;
3. aggregate capital-(Chi) relation;
4. Stability Arc trajectory;
5. Stability Inheritance / history map;

followed by a joint DM/DE function test and matched adversarial transport.

## Why the tool is structured this way

The source literature constrains the design:

- Christensen 2026 supplies the (chi)/EP starting point.
- Nadkarni-Ghosh & Réfrégier supply the mandatory modal/eigenvalue comparator.
- Lee 2026 prevents any claim that scalar-to-modal dimensionality testing is new.
- Roy et al. supply a dark-sector instability-sector precedent.
- Sharma & Sur and Basilakos et al. require background+perturbation stability comparisons.
- te Vrugt et al. and Wiegand & Buchert constrain claims about memory/history and structure-emergent behavior.
- Kunz and von Marttens et al. impose dark-degeneracy limits.
- Pèrenon et al. and You et al. impose expansion-growth comparator requirements.
- Sui et al. supplies information-sufficiency/complementarity precedent.
- Heavens et al. requires protection against lossy baseline-optimized compression.
- Nicola et al. supplies model-rejection / consistency precedent.

See `../FIVE_COMPONENT_INTEGRATION_METHOD_v0.1.md` for the full source-grounded methodology and bibliography.

## Dispositions

The current engine can return:

- `SCALAR_ADEQUATE`
- `MODAL_REQUIRED`
- `CHI_AGGREGATE_REQUIRED`
- `ARC_REQUIRED`
- `INHERITANCE_REQUIRED`
- `FULL_ARCHITECTURE_REQUIRED`
- `REFUSED_REDUNDANT`
- `REFUSED_MODEL_IMPOSED`
- `NEED_MORE_INFO`

The ladder intentionally allows the architecture to stop at any level.

## Current status

This is an isolated scaffold only. It has not been connected to the active DESI Python run and does not modify any existing cosmology scripts, data, results, checkpoints, requirements, or environments.
