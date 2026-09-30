# SI Continuity Failure - DESI Cross-Block False Liveness and Resource Exit

Date: 2026-09-29
Governance: SymC GOM v1.0 plus Mandatory Continuity Hardening Addendum
Classification: CONTINUITY_FAILURE / FALSE_LIVENESS / MECHANICAL_RESOURCE_ALLOCATION
Scientific authority change: NONE

Independent sentinel finding: the authoritative SI lineage had been redirected by explicit user direction from the preserved ERIES documentation-access gate to the already-authorized DESI SI conglomeration lane. ERIES remains deferred with its protected boundary unchanged.

At sentinel audit, CONTINUITY_STATE.json reported ACTIVE_COMPUTE with Popstop:PID9984, but Popstop had no such process and no active Python computation. GitHub Actions also had no active authoritative SI run. Local execution history showed PID 9984 had already failed with a NumPy ArrayMemoryError, and subsequent same-chain repairs v0.1a and v0.1b also terminated from memory allocation before a complete durable cross-block result was written.

The latest v0.1b failure occurred while allocating the dense X_shift design matrix at approximately 1.55 million rows by 64 float64 columns. No final four-fold result or scientific disposition was persisted.

Root cause: implementation/resource failure on the local runner. The frozen scientific question, source pair, rows, weights, B/G/S/R definitions, residualization, interaction set, pairing-destroyed control, LOSC folds, classifier objective, and decision rules remain unchanged.

A second continuity defect was present: the conveyor queue metadata remained on the earlier ERIES gate and contained no DESI execution entry even though WORKING_INVESTIGATION.md and CONTINUITY_STATE.json had moved the authoritative lane to DESI. This is stale execution-plumbing state, not scientific authority.

Recovery ceiling: remove only the memory-allocation implementation failure while preserving every frozen scientific element. No row thinning, float32 conversion, feature removal, evidence expansion, new cosmological family, threshold change, scientific retuning, or interpretation change is authorized.
