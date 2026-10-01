# Cosmology Literature Gap Map — Representation Qualification

**Status:** PROVISIONAL PRIOR-ART MAP, novelty not yet promoted  
**Date:** 2026-09-30  
**Lane:** DM/DE Stability Architecture  
**Scientific firewall:** Literature/design record only. No active Python inputs, code, outputs, thresholds, or checkpoints changed.

## Question

What is already established in cosmology, which connections have already been made, and what gaps remain between otherwise mature literatures that could support a useful methodology or later diagnostic tool?

The candidate contribution is **not** generic cosmological model comparison, generic model-independent reconstruction, generic expansion-growth consistency, or generic data compression. All of those are established.

The narrow candidate is a preregistered **representation-qualification methodology** that asks, before physical interpretation:

1. Is a scalar representation sufficient for the question?
2. If not, is redshift-, scale-, tracer-, or modal-resolved structure required?
3. If resolved components qualify, does their coupled/relational state add information beyond the marginals?
4. Does the candidate survive native-model sufficiency tests and matched adversaries?
5. Is the evidence sufficient to decide, or is the correct state REFUSE / NEED MORE INFO?
6. What held-out result could falsify the promoted representation?

## Established island A — dark degeneracy and observables-first reasoning

Kunz (2007) established the core dark degeneracy: gravity measures total stress-energy, and interacting and non-interacting dark-sector descriptions can be observationally equivalent without additional assumptions. The prescription to parameterize observables rather than over-interpret components is therefore established prior art.

von Marttens et al. (2020) extended the degeneracy explicitly through background and linear perturbation descriptions, showing how sound speed / pressure perturbations and anisotropic stress enter degeneracy breaking.

You, Cai & Yang (2026) is a direct modern collision with any claim that expansion and growth had not been connected nonparametrically. They jointly reconstruct the expansion and growth histories and infer both dark-energy dynamics and dark-sector interaction without fixed parametric forms. Their result is consistent with LambdaCDM and no nonzero interaction.

**Consequence:** expansion-growth coupling, model-independent degeneracy breaking, and null dark-sector interaction outcomes are already established. The present project must not claim novelty there.

## Established island B — null and consistency tests

A large literature tests LambdaCDM, GR, FLRW geometry, and scale-independent growth through relations that should vanish or remain invariant under a reference theory.

Examples include growth-versus-expansion consistency, scale-dependence null tests, geometry consistency relations, and model-independent density/expansion diagnostics. Koksbang & Heinesen (2026) now provide a particularly strong model-independent FLRW diagnostic using distance derivatives and the line-of-sight expansion rate, plus a nonparametric density estimator independent of the Friedmann equations.

**Consequence:** "build a falsifiable null test" is not itself novel. The residual question is whether multiple null/consistency tests can be organized into a prior representation-selection logic rather than applied after a representation/model has already been chosen.

## Established island C — nonparametric reconstruction and complexity control

Gaussian processes, PCA/binning, crossing statistics, flexknot methods, and other nonparametric reconstructions have long been used to infer H(z), w(z), transition behavior, interactions, and related cosmological functions.

Crittenden et al. emphasized reconstruction bias and prior control. Gerardi et al. showed how theoretical priors alter reconstructed dark-energy histories. DESI DR1/DR2 analyses now compare parametric and nonparametric reconstructions directly and find broadly consistent trends, while retaining model dependence and supernova-sample sensitivity.

**Consequence:** flexible representation of w(z) is not a gap. What remains potentially open is a procedure that decides *whether w(z) is even the right level/type of representation to promote* versus a scale-resolved growth representation or an explicit indeterminate state.

## Established island D — compression and information loss

Lossless / Fisher-optimal compression is mature. Score compression, MOPED, KL/PCA methods, ShapeFit, and related approaches can preserve information for specified parameter targets.

Critically, Heavens, Sellentin & Jaffe (2020) explicitly warn that compression optimized for a baseline model can suppress or erase evidence for new physics. Their MOPED-PC construction preserves additional agnostic directions to protect sensitivity to departures from the baseline.

DESI comparison papers validate Full-Modeling, ShapeFit, and standard compression under controlled model families and mocks. The DESI DR2 Ly-alpha full-shape result demonstrates empirically that using resolved full-shape information can tighten constraints beyond BAO-only compression and shift central values toward a different region of model space.

**Consequence:** the fact that compression can hide physics is established. A possible gap is to elevate that fact into an explicit scientific gate: scalar/compressed adequacy must itself be tested before the compressed representation is permitted to carry interpretation.

## Established island E — model checking, rejection and inconsistency

Posterior predictive checks, relative entropy / KL consistency measures, Bayesian model evidence, tension metrics, and model-rejection frameworks already provide ways to identify poor fit, inconsistency or lack of support.

Nicola, Amara & Refregier (2019) explicitly combine relative entropy with posterior predictive distributions in a model-rejection framework.

**Consequence:** REFUSE cannot be claimed as a new statistical concept. The narrower question is whether refusal is made a first-class *representation state* before model interpretation, with a separate NEED MORE INFO state for under-resolved evidence.

## Connections already made

The following bridges therefore already exist and must be treated as occupied:

- expansion + growth -> model-independent cosmological constraints;
- expansion + growth -> dark-sector interaction / dynamical-DE degeneracy breaking;
- background + perturbations -> GR / modified-gravity consistency tests;
- compression + new-physics sensitivity -> agnostic extra modes;
- full-shape + BAO -> improved and sometimes shifted cosmological constraints;
- parametric + nonparametric DE reconstruction -> robustness checks;
- dataset consistency + posterior predictive distributions -> model rejection;
- interacting DE + perturbation assumptions -> partial dark-degeneracy breaking.

## Provisional gaps between papers

### Gap 1 — no clear representation-order gate

The located methods generally start with a representation: a parameter vector, a function such as w(z), a compressed summary, a null statistic, or a chosen data vector. The unresolved methodological question is whether the data can first be asked to justify the *order and structure* of the representation itself.

Candidate ladder:

[
	ext{scalar}
ightarrow
	ext{resolved/modal}
ightarrow
	ext{coupled/relational}
]

with lower-order sufficiency tested before higher-order promotion.

This is a provisional gap, not yet a novelty claim.

### Gap 2 — compression adequacy is rarely a scientific output

Compression studies quantify retained information relative to target parameters/models. New-physics-aware compression protects extra directions. What appears less developed is a domain workflow where "compression is scientifically inadequate for this question" is itself an admissible preregistered result that forces promotion to resolved structure.

The DESI Ly-alpha DR2 BAO-only versus full-shape shift is an excellent empirical test case because the same dataset family visibly changes inferential power when more structure is retained.

### Gap 3 — degeneracy breaking and representation sufficiency are separate literatures

The 2026 expansion-growth dark-degeneracy work chooses expansion and growth as the needed observables. Compression literature asks what summaries preserve targeted information. Null-test literature asks whether a relation holds. These are adjacent but not identical questions.

Potential unconnected dot:

> Before trying to break a physical degeneracy, test whether the chosen representation has enough independent information to make that degeneracy breakable at all.

That would convert algebraic/model dependence and information loss from caveats into explicit admission/refusal gates.

### Gap 4 — NEED MORE INFO is not usually separated from model non-preference

Bayesian evidence can be inconclusive, a null test can be consistent with zero, and a reconstruction can be prior dominated. Those conditions are statistically familiar. But the scientific workflow often still reports parameter constraints within the chosen representation.

A possible methodological contribution is to distinguish:

- **REFUSED:** representation fails a prerequisite or is redundant/non-identifiable;
- **NEED MORE INFO:** representation could discriminate in principle, but current resolution/covariance/coverage cannot decide;
- **QUALIFIED:** representation carries independent information for the frozen question.

The novelty would be the operational decision architecture, not the existence of uncertainty or inconclusive evidence.

### Gap 5 — relational/coupled promotion usually follows modeling choice

Cosmology routinely studies cross-correlations and joint likelihoods. The candidate gap is not "combine observables." It is whether a coupled representation is promoted only after showing incremental predictive/discriminating information over both marginals under matched complexity and held-out testing.

This requires explicit incremental-value testing rather than interpreting correlation as architecture.

### Gap 6 — representation failure is rarely treated as a reusable scientific product

A failed scalar, a model-imposed transition, a prior-bound reconstruction, or a lossy compression is usually a limitation of an analysis. The program-wide methodology instead proposes storing these failures as positive knowledge about the *domain of validity of representations*.

A reusable Limit Map of representation failure may be more distinctive than another dark-energy parameter estimator.

## Closest direct collision to the candidate methodology

The strongest current collision is the combination of:

1. **You, Cai & Yang (2026):** nonparametric expansion-growth degeneracy breaking;
2. **Heavens, Sellentin & Jaffe (2020):** compression can erase new physics and should preserve agnostic directions;
3. **Koksbang & Heinesen (2026):** model-independent diagnostic consistency testing of foundational geometry;
4. **Nicola, Amara & Refregier (2019):** posterior-predictive model rejection and consistency;
5. **DESI Full-Shape / ShapeFit literature:** controlled tests of compressed versus resolved information.

Any final method must add something not obtained by simply running these approaches side by side.

## Smallest prospective novelty test

Do not test "does Stability Architecture fit cosmology?" first.

Test whether **representation qualification changes a scientific conclusion in a preregistered case**.

Use at least three information levels from the same or tightly matched cosmological data lineage:

- compressed/scalar;
- resolved full-shape / redshift- or scale-dependent;
- joint background + growth.

Before inspecting held-out results, freeze:

1. the information retained at each level;
2. the lower-order adequacy criterion;
3. the matched native/adversarial models;
4. the conditions for QUALIFIED, REFUSED and NEED MORE INFO;
5. the scientific conclusion each representation would license.

A useful method result occurs if the gate correctly identifies that a lower-order representation is adequate in one case, insufficient in another, and genuinely under-resolved in a third, **without changing rules after seeing the result**.

If ordinary information criteria, posterior predictive checks or existing compression diagnostics reproduce all three decisions with no additional benefit, the representation-qualification methodology is refused as redundant.

## Current disposition

- Generic model comparison: **occupied**
- Generic null testing: **occupied**
- Generic nonparametric reconstruction: **occupied**
- Expansion-growth degeneracy breaking: **occupied, including 2026 direct collision**
- Information-preserving / new-physics-aware compression: **occupied**
- Explicit model rejection / posterior predictive inconsistency: **occupied**
- Representation-order qualification with REFUSE / NEED MORE INFO before interpretation: **provisional gap**
- Reusable cross-analysis Limit Map of representation failure: **provisional gap**
- Executable representation diagnostic: **not yet earned**

A comprehensive deep literature search targeting the representation-qualification gap was launched on 2026-09-30. This file must be revised if that search identifies a direct methodological collision.
