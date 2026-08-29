# Frozen v0.7 external-admission recovery gate

Status: `PROVENANCE_HOLD`

This directory is intentionally outcome-free. It exists to recover and record the exact frozen v0.7 external-candidate contract **before** any external candidate response values are inspected or scored.

## What may be stored here before contract recovery

- metadata needed to locate the historical frozen contract;
- exact recovered preregistration/configuration/source files;
- cryptographic hashes;
- environment and entrypoint identity;
- candidate filenames and non-outcome provenance metadata only when the historical protocol licenses their inspection.

Do not store plots, numerical summaries, candidate scores, favorable/unfavorable labels, or outcome-derived filtering decisions here before the guard is ready.

## Required recovery record

The live guard expects:

`CONTRACT_RECOVERED.json`

That record is created only after the exact historical contract has been recovered. It must certify `candidate_values_inspected: false`, identify the source of every required frozen rule, and provide verifiable SHA-256 records for all load-bearing files.

`CONTRACT_RECOVERED.template.json` is a schema aid only. Its status is deliberately `TEMPLATE_ONLY_NOT_RECOVERED`; copying the template without recovering the historical sources cannot open the gate.

## Mechanical check

Run from the repository root:

```bash
python stability_arc/gfsa_v0.7.2/code/pre_admission_guard_v01.py
```

Expected state before exact recovery:

`PROVENANCE_HOLD`

Expected state only after exact recovery and successful hash verification:

`READY_FOR_FROZEN_EXTERNAL_ADMISSION`

The script contains no scientific threshold values and cannot invent missing scientific rules.
