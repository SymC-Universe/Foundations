# DESI Shared-Coordinate SI Qualification v0.1a — Pre-Result Validation Amendment

**Date:** 2026-09-29
**Parent:** `DESI_SHARED_COORDINATE_SI_QUALIFICATION_v0.1.md`
**Status:** FROZEN BEFORE NUMERIC POSTERIOR ANALYSIS
**Change class:** validation hardening only

The parent protocol specified deterministic five-fold row-index validation. Before any v0.1 posterior result was computed, this was recognized as weaker than the source structure permits because each model has four separately released MCMC chain files.

## Primary cross-validation

The primary classifier validation is therefore changed to **four-fold leave-one-source-chain-out (LOSC)**.

For fold (jin{1,2,3,4}):

- test = baseline `chain.j.txt` plus adversary `chain.j.txt`;
- train = the other three baseline and other three adversary chain files;
- feature standardization is fitted on training data only;
- posterior sample weights are retained;
- total training weight for each model class is normalized equally so class prevalence cannot determine the result;
- test metrics are weighted within each class and then macro-averaged.

The parent five-fold within-chain modulo split is retained only as a **secondary implementation diagnostic** and cannot promote the disposition if LOSC is inconsistent.

## Robust ordering rule

Any claim that a joint block adds information requires the declared log-loss ordering to hold in at least three of four LOSC folds and in the pooled LOSC aggregate.

If the pooled ordering is positive but only two or fewer LOSC folds agree, return `REPRESENTATION_INDETERMINATE` regardless of the row-modulo result.

All scientific coordinates, anti-leakage rules, source identities, interpretation ceilings, and protected future stages from v0.1 remain unchanged.
