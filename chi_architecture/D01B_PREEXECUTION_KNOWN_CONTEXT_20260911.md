# D01B Pre-Execution Known-Context Attestation — 2026-09-11

**Status:** P0-D pre-execution provenance record  
**Applies to:** `D01B_COUPLED_2DOF` in `D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json`  
**Purpose:** Preserve what was already known before D01B execution and prevent later overstatement of independence.

## Already-viewed relevant evidence

Before D01B execution, the following NSD P0-D results had already been inspected:

- P0-D14 population versus finite-sample chi recovery;
- P0-D15 chi/discriminant uncertainty;
- P0-D16 coupled-feedback chi surface;
- P0-D17 feedback transformation geometry;
- P0-D19 closed-loop recovery surface.

In particular, it was already known from NSD synthetic development that reciprocal feedback can reorganize emergent global chi lineages while local subsystem chi values remain fixed, that equal edge magnitude does not determine the feedback outcome, and that a closed-loop coupling surface can contain both improved-recovery and degraded-recovery regions.

Therefore D01B cannot be described as an untouched confirmation of those general observations.

## Why D01B remains scientifically useful

D01B was prospectively specified before this attestation and uses a different native generator geometry:

`M q_ddot + C q_dot + K q = 0`, with `M=I` for the first pass.

Its coupling is expressed through mechanical stiffness and damping matrices and its declared outputs include modal structure, component energy redistribution, coupling-energy exchange, transient response, and perturbation recovery.

The relevant NSD feedback experiments instead used directed off-diagonal state-space transformations between fixed second-order subsystem generators.

D01B therefore remains a useful within-domain P0 comparison of how native mechanical coupling changes the adequate coordinate description.

## Frozen-before-execution items

The following remain exactly as recorded in `D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json` and will not be changed in response to NSD P0-D14 through P0-D19:

- `k1 = [1.0]`;
- `k2 = [0.5, 1.0, 2.0]`;
- `local_damping_c1 = [0.1, 0.5, 1.0, 2.0]`;
- `local_damping_c2 = [0.1, 0.5, 1.0, 2.0]`;
- `coupling_stiffness_kc = [0.0, 0.1, 0.25, 0.5, 1.0, 2.0]`;
- `coupling_damping_cc = [0.0, 0.1, 0.5, 1.0]`;
- both declared component-specific perturbations;
- declared Function Map and Limit Map metrics;
- no predeclared master scalar;
- allowance for multidimensional coordinate structure and no-admissible-scalar outcomes;
- Atlas blindness.

## Interpretation ceiling

D01B may:

- map the native mechanical coupled response surface;
- identify where local/modal scalar summaries remain adequate or lose information;
- expose how stiffness/damping coupling changes modal, energy-transfer, and recovery behavior;
- motivate later coordinate-compression candidates;
- return multidimensional/no-scalar outcomes.

D01B may not:

- count as untouched cross-domain confirmation of NSD feedback results;
- establish a universal or prevalent Chi architecture;
- use the NSD chi values, coupling strengths, turnover location, or preferred transformation geometry to tune its own grid;
- infer a biological, chemical, or natural target range;
- create Atlas admission credit.

## Post-result rule

Any lower-dimensional coordinate suggested by D01B results is a P0-D discovery candidate. It must be recorded after result inspection, then separately qualified. It cannot be retroactively treated as having predicted the D01B surface that generated it.
