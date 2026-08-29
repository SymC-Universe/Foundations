# Dephasing destabilization-side availability recovery v0.1

**Status:** FROZEN BEFORE EXECUTION
**Scope:** TARGETED_SELECTION_AVAILABILITY_ONLY

## Motivation and evidentiary status

H10 used 1,200,000 fresh broadly sampled dephasing-augmented planar systems. The stabilizing `S_C13` direction had abundant support and passed 128/128 frozen reveals. The destabilizing `D_C13` direction produced only two admissible cases, one in S3 and one in S4, so H10D ended `SELECTION_HOLD_D` under its preregistered minimum of 16.

This phase is an explicitly post-H10 targeted availability recovery. It does not count as confirmation of H10D and may not reuse either H10 D case. Its sole purpose is to determine whether a sufficiently large fresh blind-reveal panel can be frozen from the high-radius region using only the already-derived structural/c1/c3 coordinates.

## Frozen generator

Use NumPy `default_rng(seed=2026082921)`.

Generate exactly 10,000,000 new inputs in two unchanged H10 radial shells:

- S3: 5,000,000 states with `r ~ Uniform(0.90,0.98)`;
- S4: 5,000,000 states with `r ~ Uniform(0.98,0.9999)`.

Within each shell retain the H10 broad distributions unchanged:

- `log10(gamma) ~ Uniform(log10(0.1),log10(2.0))`;
- `log10(gamma_phi) ~ Uniform(log10(0.001),log10(2.0))`;
- `log10(kappa) ~ Uniform(log10(0.05),log10(5.0))`;
- `eta ~ Uniform(0.01,0.95)`;
- `log10(omega) ~ Uniform(log10(0.02),log10(10.0))`;
- `theta ~ Uniform(-pi,pi)`;
- state direction isotropic in R3, then multiplied by the frozen radius.

The implementation may stream the panel in deterministic fixed-size chunks for memory control, but the RNG stream, total sample counts, shell order, and generated values are part of the frozen contract.

## Stage-A-only admissibility

For each generated input construct only the already-derived dephasing planar structural coordinate and exact channel-specific `c1`/`c3` invariants. Do not construct A, B, G, c2, `c1*c2-c3`, eigenvalues, or full stability labels in this phase.

Use the unchanged H10 scale

`R = a+b+kappa+omega+q`,

where `a=gamma/2+gamma_phi`, `b=gamma`, and `q=eta*kappa`.

Use unchanged H10 tolerance `MAP_TOL=1e-8`.

A fresh input is `D_C13` eligible iff all are true:

1. `abs(Delta_phi)/R > 1e-8`;
2. `c1_phys/R > 1e-8`;
3. `c3_phys/R^3 > 1e-8`;
4. `c3_record/R^3 < -1e-8`.

No hidden full-class information may enter selection.

## Frozen output and decision

Process every registered input and record exact per-shell eligibility counts. Freeze the first 64 eligible cases in deterministic generation order, including their full generated parameters and Stage-A coordinates. Hash the frozen selection JSON.

Decision:

- `READY_FOR_BLIND_REVEAL_H11` iff at least 16 fresh eligible cases exist across S3+S4 and all generation/hash controls pass;
- `SELECTION_HOLD_H11` if fewer than 16 exist;
- `MECHANICAL_OR_PROVENANCE_HOLD` on deterministic replay/hash/generation failure.

`READY_FOR_BLIND_REVEAL_H11` is not a scientific PASS. It licenses only a separate successor blind-reveal workflow on exactly the frozen selected IDs. That successor must reconstruct the full Hilbert generator and hidden Routh-Hurwitz margins without replacing any selected case.

## Anti-circularity firewall

H10 outcomes motivated the S3/S4 targeting and therefore H11 is explicitly post-H10 design work. H11 itself is fresh and freeze-before-reveal. The H10 two-case D observation may never be pooled with H11 as prospective evidence. No threshold, shell bound, sample count, or eligibility rule may change after H11 execution begins.