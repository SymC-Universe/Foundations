# Chi Architecture Investigation

**Status:** P0-D / P0-Q DOMAIN-FIRST ARCHITECTURE MAPPING  
**Branch:** `chi-architecture-p0`  
**Authority:** General Cross-Project Research Protocol v0.7.1 FINAL + v0.7.1A Functional Mapping and Natural Limit-Testbed Addendum  
**Claim ceiling:** exploratory and qualification evidence only  
**Confirmatory MFR-14:** not yet activated  
**Predictive tool status:** not a tool; no validated cross-domain Atlas; no prospective cross-domain confirmation

## Current scientific question

Can materially different domains each generate a scientifically useful stability-coordinate map from their own native scalar content, modal/vector carriers, coupling/system organization, feedback/relationships, uncertainty, and other structure that earns admission, and do those independently derived domain maps later admit meaningful cross-domain alignment?

The program does **not** assume that every domain has the same formula, dimensionality, components, or scalar chi.

The current ordering is:

`native domain science -> Function Map + Limit Map -> candidate Chi_d coordinate map -> within-domain qualification -> frozen domain map -> cross-domain Stability Architecture Atlas`

The inverse dependency is forbidden:

`desired Atlas pattern -> tune Chi_d -> rediscover desired Atlas pattern`

See `DOMAIN_FIRST_CHI_COORDINATE_PROGRAM_v0.1.md`.

## Scope discipline

Universality is **not** a research target or promotion criterion.

The architecture is being investigated because it may be unusually broad across otherwise different systems and regimes. Its scope must be earned one regime, mechanism, and untouched test at a time. A result that works in several domains remains a bounded cross-regime result unless additional evidence extends that boundary.

`BROAD != UNIVERSAL`

A scientifically valuable outcome may therefore be any of the following:

- broad cross-regime architecture;
- domain-family architecture;
- regime-specific architecture;
- partial transportability of selected components;
- multidimensional rather than scalar coordinate structure;
- no admissible chi coordinate in a particular domain;
- or failure of the proposed architecture outside a narrow class.

None is treated as a continuity failure.

## Historical interpretation of the scalar-first investigation

The program should not be read as having started from the belief that a scalar chi was the fundamental object.

The earlier conceptual premise was that systems are shaped not only by their isolated properties but by pressure, influence, coupling, and feedback from other systems or components, and that a coupled/grouped system can contain scientifically important behavior not recoverable from isolated components alone.

The damped oscillator supplied an early mathematically tractable realization in which competing tendencies admit the scalar coordinate

`chi = gamma / (2 omega_0)`.

That success motivated an extended **scalar-first investigation** because the scalar was measurable, compact, and analytically useful. It did not establish that the scalar was ontologically primary.

The historical progression is recorded as:

`systems/feedback/coupling premise -> tractable scalar probe -> scalar-first testing -> evidence that scalar alone is insufficient -> modal/carrier and conglomerate/system structure -> domain-first architecture/coordinate reconstruction`

Documentary provenance for the earliest pre-mathematical formulation should be added separately if the original paper or dated record is recovered. Such provenance would establish hypothesis history, not empirical correctness.

## Working Chi object

For a domain `d`, the working hypothesis is that native measurable architecture `A_d` may generate a coordinate object

`Chi_d : A_d -> Z_d`.

`Z_d` is the smallest scientifically adequate coordinate space supported by that domain. It is not required to be one-dimensional.

Possible outcomes include scalar, vector, subspace/projector, graph/network, operator/manifold, hybrid discrete-continuous, or refused coordinate structures.

A lowercase scalar `chi_d` is admitted only if one-dimensional compression earns its existence from the native mathematics and preserves the information needed for the declared scientific task.

The cross-domain Atlas is downstream of these independently derived coordinates. The Atlas records placements; it does not create them.

## Current starting basis

Where native science supports them, inspect:

- **scalar:** compressed stability coordinates, invariants, rates, ratios, spectra, or other defensibly derived scalar summaries;
- **vector/modal:** resolved carrier structure such as eigenvectors, invariant subspaces, projectors, participation structure, latent modes, or other domain-native multidimensional objects;
- **conglomerate/system:** organization created by coupling, feedback, networks, subsystem interaction, memory, environmental structure, cross-layer mappings, or collective behavior;
- **relationships/open channels:** feedback paths, coupling direction, disagreement, inheritance, uncertainty/nonidentifiability, adequacy, and other domain-native structure not reducible to the first three views.

These are starting representations, not a mandated complete decomposition.

## Chi naming and admission rule

An object is not called chi merely because it is a useful stability quantity.

- `chi = gamma / (2 omega_0)` remains a licensed scalar construction only for a justified passive second-order factor with the required conventions and boundary structure.
- A different regime may generate a different candidate scalar chi only through its own native model, derivation, validity conditions, uncertainty treatment, nulls, and admission rules.
- A scalar chi is not required for an architecture to be scientifically meaningful.
- Any proposed scalar compression must earn its existence by preserving or adding scientifically useful information beyond the richer native representation.
- A domain may legitimately return `NO_ADMISSIBLE_SCALAR_CHI` or `NO_ADMISSIBLE_CHI_COORDINATE`.
- A visually attractive cross-domain alignment cannot be used to retrofit a domain coordinate.

## Function Map and Limit Map

Under General Protocol v0.7.1A, every mature domain investigation should characterize both:

1. **Function Map:** ordinary supported operation, variation, perturbation response, compensation/redistribution where present, alternate stable organizations, and trajectories through the functioning regime;
2. **Limit Map:** transitions, saturation, model breakdown, loss of identifiability, refusal, instability, and qualified rare natural limit states.

The objective is to map the phenomenon, not only to attack it.

Qualified rare natural occurrences are high-information limit testbeds. They must be selected using domain-native rarity/extremeness rather than favorable chi placement. Already-viewed rare events are P0-D/P0-Q evidence; P1 use requires independent prospective selection/freeze.

## D01 linear-dynamics map

`D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json` is the first domain-map plan.

### D01A exact SDOF anchor: complete

The frozen D01A plan scanned `chi=0...4` in increments of `0.05`, four values of `omega0`, and two normalized initial conditions.

GitHub Actions run `34615114508` completed successfully. Artifact `chi-architecture-d01a-domain-map-v01`, ID `10269408539`, digest `sha256:fcaefcb95485a390b79530a890fad3dff5f4419fc3d31749c9240eeec8a7012c`.

Observed within-domain results:

- normalized trajectories at fixed chi collapse across `omega0=0.5,1,2,5` to machine precision;
- maximum normalized displacement collapse error = `0.0`;
- maximum normalized velocity collapse error = `1.1102230246251565e-16`;
- `chi=1` is the exact first nonoscillatory grid point and maximizes the slowest dimensionless decay rate;
- for initial displacement `(x0,u0)=(1,0)`, the frozen grid gives minimum 2% state-settling time at `chi=0.80`, minimum integrated absolute displacement at `chi=0.65`, and minimum integrated energy at `chi=0.70`;
- for initial normalized velocity `(x0,u0)=(0,1)`, minimum 2% state-settling time occurs at `chi=0.75`, while two integrated metrics continue improving through the upper scanned boundary and therefore do not license an interior optimum claim.

Interpretation: within the exact oscillator, chi earns its existence as a dimensionless response-placement coordinate, while different function metrics and perturbations value different locations on that coordinate. `chi=1` is structurally special but is not a task-independent optimum.

See `D01A_SDOF_DOMAIN_MAP_READOUT_v0.1.md`.

### D01B coupled 2DOF extension: next

D01B deliberately predeclares no master scalar. It will map scalar/spectral information, modal carriers/subspaces, physical coupling, energy redistribution, transient response, and whole-system recovery over a broad coupled parameter surface.

Its central question is whether one-dimensional placement remains adequate after coupling, or whether the scientifically adequate Chi coordinate becomes multidimensional.

## Anti-circularity position

The workstream must not follow these invalid chains:

`inspect favorable architecture -> choose a scalar that matches it -> call that scalar chi -> use the match as evidence for chi architecture`

or

`inspect desired cross-domain Atlas alignment -> alter domain coordinate -> claim the altered coordinate independently aligns across domains`.

Instead:

`native model -> native observables -> Function/Limit Map -> candidate domain coordinate -> within-domain qualification -> freeze -> cross-domain comparison`.

The conglomerate cannot mean "whatever combination performs best." It must be a named native mathematical or physical relationship whose construction is fixed independently of the outcome being used to test it.

### Designed fixtures are not evidence for the hypothesis they encode

F0-F8 are **known-truth designed fixtures**. Their parameters were chosen to exercise specific mathematical and software behaviors. Correct recovery qualifies implementation behavior only.

Therefore:

- F4's analytically selected feedback cases verify the Hurwitz coupling criterion; they do not establish compensatory discordance.
- F1/F6 verify established fixed-spectrum non-normal behavior; they do not establish added architecture value beyond standard non-normal analysis.
- F8 verifies admission/refusal behavior for a licensed second-order scalar; it does not establish cross-regime chi.
- no F0-F8 success counts as empirical confirmation, P1 evidence, or program-level `ADDS`.

`P0_EXPERIMENT_PLAN_v0.2.json` remains the immutable current fixture source. It is not silently rewritten around the new domain-first program.

## Current developmental domain sequence

1. second-order damped dynamics, exact scalar anchor;
2. coupled/non-normal linear dynamics;
3. NSD synthetic known-truth dynamics and observable-rank/refusal architecture;
4. GRI static multi-omic architecture with biological chi withheld;
5. substrate-inheritance coupled dynamics;
6. Chemistry single-barrier versus network-resolved systems;
7. additional mature domains such as power-grid, seismological, quantum/open-system, and cosmological systems after native-domain audit.

Already-viewed GRI, Barrier Atlas, and NSD evidence remains calibration/provenance evidence for rules learned from it, not pristine confirmation.

## Current status against the General Protocol

See:

- `DOMAIN_FIRST_CHI_COORDINATE_PROGRAM_v0.1.md`
- `DOMAIN_CHI_MAP_SCHEMA_v0.1.json`
- `D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json`
- `D01A_SDOF_DOMAIN_MAP_READOUT_v0.1.md`
- `GENERAL_PROTOCOL_AUDIT_20260910.md`
- `CIRCULARITY_AUDIT_20260910.md`
- `CROSS_PROJECT_UPDATE_AUDIT_20260910.md`
- `POST_RESULT_DISCOVERY_LEDGER.md`
- `P0_FALSIFIABILITY_CHARTER_v0.1.md`
- `P0_EXPERIMENT_PLAN_v0.1.json` for preserved historical v0.1 provenance
- `P0_EXPERIMENT_PLAN_v0.2.json` for current P0 fixture execution

## Project control

**Current status:** D01A is mapped and validated as the exact within-domain scalar anchor. The domain-first program is active; no cross-domain Atlas has been constructed.  
**Next scientific/computational step:** execute D01B, the coupled two-degree-of-freedom Function/Limit Map, without predeclaring a master scalar.  
**Why:** this is the first direct test of whether a coordinate that is sufficient for an isolated exact system remains sufficient once multiple functioning components exchange energy and influence one another.  
**What can advance immediately:** implement the D01B raw architecture map, preserve the full parameter surface, and only afterward ask whether any lower-dimensional Chi coordinate earns adequate compression.  
**User action required:** none.
