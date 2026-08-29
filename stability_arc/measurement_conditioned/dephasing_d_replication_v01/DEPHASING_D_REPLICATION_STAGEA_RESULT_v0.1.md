# H12 dephasing D replication Stage A result v0.1

**Status:** `READY_FOR_BLIND_REVEAL_H12`
**Role:** OUTCOME-BLIND AVAILABILITY / SELECTION ONLY
**Scientific PASS/FAIL:** NOT YET SCORED

## Frozen execution

- workflow run: `33269142763`
- execution commit: `40eaea41fd5331c1e740fc7882ecdc865414e8e9`
- artifact: `9719557784`
- artifact ZIP SHA-256: `1e9ca9e306b14f751abfbd6fc8200e6387b2adb8671ec9b7d51649ac07c21498`
- replication seed: `2026082922`
- generated inputs: `10,000,000`
- H11 Stage-A engine SHA-256: `d49778d7f07865d0bbf8530b0bc8430664589fb3cd8e4eaab45df453f0763fa0`

The only protocol change from H11 Stage A was the preregistered untouched replication seed. Hidden full stability was not computed during H12 Stage A.

## Availability and frozen selection

- S3 eligible: `6`
- S4 eligible: `65`
- total eligible `D_C13`: `71`
- frozen for blind reveal: first `64` in deterministic generation order
- frozen selection SHA-256: `364ba6a18b5ea8b8cad7a164028013bf605db5a44f847bcc9e1d13dfacb46de5`
- minimum preregistered readiness count: `16`

The deterministic replay/hash check passed.

## Firewall

This result establishes only that a sufficiently large untouched H12 selection exists for a separate blind reveal. It is not confirmation of physical STABLE -> same-record UNSTABLE behavior. No `G`, `c2`, final Hurwitz margin, eigenvalue, or full stability class was used to select these 64 cases.

The next admissible calculation is a separately frozen blind reveal bound to the exact H12 run, artifact, and selection SHA-256 above. No frozen case may be replaced or reselected after hidden stability is exposed.
