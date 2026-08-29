# GFSA Anti-Circularity Execution Guard v0.1

Status: ACTIVE EXECUTION CONTROL
Scope: Stability Arc / Generator-First Stability Architecture external numerical admission and all successor prospective tests on branch `agent/stability-arc-gfsa-v072`.

This control adds no scientific threshold, scoring rule, physical interpretation, or outcome claim. It constrains execution order so that later evidence cannot retroactively define the test used to judge it.

## 1. Freeze-before-view rule

No external candidate response values may be inspected, plotted, summarized, filtered by outcome, or numerically scored until all required admission rules for that candidate class are recovered from the frozen preregistration and cryptographically recorded.

At minimum, the frozen contract must specify or point unambiguously to the already-registered rules for:

1. file provenance;
2. channel mapping;
3. numerical quality;
4. uncertainty handling;
5. bandwidth/admissible observation window;
6. observer/surrogate-order rules;
7. PASS / FAIL / NONIDENTIFIABLE decision logic;
8. all exclusions and stop conditions.

If any required rule is missing, ambiguous, or recoverable only from memory, execution stops as `PROVENANCE_HOLD`. The missing rule must not be reconstructed from candidate outcomes.

## 2. Hash-before-outcome rule

Before candidate-response inspection:

- hash all preregistration, configuration, source-code, calibration, and candidate-input files;
- record software/environment identity where it can affect results;
- record the exact execution entrypoint;
- preserve candidate filenames and metadata needed for provenance without exposing numerical response values beyond what the frozen protocol allows.

## 3. Calibration / validation firewall

Calibration evidence may be used only for rules explicitly licensed by its preregistration. Validation or holdout evidence may not be used to retune:

- thresholds;
- bandwidths;
- surrogate orders;
- scoring weights;
- uncertainty rules;
- inclusion/exclusion logic;
- interpretation categories.

If a validation result motivates a better rule, that rule begins a new version and requires fresh prospective data or a separately frozen holdout. The original result remains scored under the original rule.

## 4. One-way evidence promotion

Evidence may move only forward through:

`observation -> extraction -> frozen postulate/test rule -> prospective falsification -> replication/external admission`

No later-stage result may be used to rewrite an earlier-stage rule and then be counted again as prospective support for that rewritten rule.

## 5. Failure handling

A failed preregistered test remains a failure under that preregistration. It may generate a narrower or alternative hypothesis only if:

- the failed result remains preserved unchanged;
- the new hypothesis is explicitly marked post-hoc at the moment of generation;
- its next evaluation uses fresh prospective evidence or a holdout that was genuinely untouched by the new rule.

## 6. Nonidentifiability handling

`NONIDENTIFIABLE` is an admissible scientific outcome, not a prompt to loosen rules until a classification appears. No threshold or model-complexity expansion may be performed merely to convert `NONIDENTIFIABLE` into PASS or FAIL after seeing the candidate response.

## 7. Mechanical repair rule

Mechanical fixes are allowed without a new scientific preregistration only when they do not alter any frozen scientific input, rule, threshold, scoring convention, or interpretation. The repair must be documented, and outputs produced by a demonstrably broken execution path may be discarded only for the documented mechanical reason.

## 8. Independent-reconstruction rule

Where a result is promoted beyond exploratory status, the decision should be reproducible from raw admissible inputs by an independent reconstruction path that does not import the original decision output.

## 9. External-admission stop gate for v0.7.2

The v0.7.2 interface is licensed for external numerical admission only under the already-frozen v0.7 external-candidate contract. Until that exact contract is recovered, candidate numerical response values remain sealed and external scoring is blocked.

This guard must not be used to invent the missing v0.7 rules. Its purpose is to prevent circular reconstruction.

## 10. Required audit record

Every prospective execution must preserve:

- preregistration/config hashes recorded before outcome inspection;
- candidate-input hashes;
- code/entrypoint hash or commit SHA;
- execution timestamp and environment identity;
- raw result location;
- machine-readable decision record;
- explicit statement of whether any rule changed after outcome inspection.

Any post-outcome rule change invalidates the prospective status of that same evidence for the changed rule.
