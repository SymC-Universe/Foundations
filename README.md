# SymC Foundations

The **SymC Foundations** repository contains the core theoretical works underlying the Symmetry of Criticality (SymC) research program. All titles are a continuous work in progress open to outside scrutiny and perspective.

The current SymC framework is **generator-first**. It studies stability boundaries, damping, spectral structure, exceptional points, and inheritance mechanisms while requiring each proposed stability coordinate to be derived from the dynamics of the system being studied.

SymC does **not** currently assert that a single scalar damping ratio universally governs quantum, biological, cosmological, chemical, or informational systems.

Domain-specific applications are maintained separately.

---

## Contents

### Foundational Papers

| Title | Description | PDF |
|-------|-------------|-----|
| **SymC Postulate (v3)** | Historical foundational statement of the χ = 1 hypothesis and exceptional-point framing. Current use of χ is restricted by the generator and domain-licensing rules described below. | [PDF](./SymC_Posv3.pdf) |
| **SymC Noughts** | Introduces substrate noughts and the inheritance hypothesis. Current inheritance work requires explicit operator projection before assigning descendant stability coordinates. | [PDF](./SymC_Noughts.pdf) |
| **Closing Critical Gaps (v3)** | Historical particle-sector extension involving electron, quark, and neutrino scales. Current interpretation distinguishes spectral-width ratios from mechanically licensed χ unless an appropriate generator is independently derived. | [PDF](./SymC_Gapsv3.pdf) / [Supps](./SymC_Supmats.pdf) |
| **SymC AIF** | Explores connections between SymC, predictive processing, and active inference. Domain-specific stability claims require their own generator and empirical validation. | [PDF](./SymC_AIFv3.pdf) |

---

### Quantum and Mathematical Foundations

| Title | Description | PDF |
|-------|-------------|-----|
| **SymC Lindblad (v4)** | Develops open-quantum-system and exceptional-point geometry. Current interpretation requires defectiveness of the relevant full generator for an EP claim; simple amplitude damping is not automatically a finite-frequency critical-damping EP. | [PDF](./SymC_Lindbladv4.pdf) / [Supps](./SymC_Lindbladv4_Supps.pdf) |
| **SymC and the QFT (v2)** | Explores relaxation and width-scale structure in quantum field settings. Such ratios are not automatically identified with mechanical χ without a licensed dynamical reduction. | [PDF](./SymC_QFTv2.pdf) |
| **SymC Neutrinos** | Studies matter-induced dephasing effects in neutrino flavor oscillations with exact vacuum unitarity. | [PDF](./SymC_Neutrinosv2.pdf) |

---

## Current Mathematical Core

For a passive positive-curvature second-order mode,

\[
\ddot q + \gamma \dot q + \kappa q = 0,
\qquad
\kappa > 0,
\]

define

\[
\Omega = \sqrt{\kappa},
\qquad
\chi = \frac{\gamma}{2\Omega}.
\]

The characteristic roots are

\[
\lambda_\pm
=
-\frac{\gamma}{2}
\pm
\sqrt{\frac{\gamma^2}{4}-\Omega^2}.
\]

Within this licensed dynamical class:

- **0 ≤ χ < 1** corresponds to underdamped oscillatory decay.
- **χ = 1** is the critical-damping boundary where the two characteristic roots coalesce.
- **χ > 1** corresponds to overdamped monotone decay.
- In the standard companion-matrix realization, the repeated root at χ = 1 is defective and therefore has the algebraic structure of an EP2.
- For fixed restoring scale Ω, χ = 1 gives the fastest asymptotic nonoscillatory relaxation within the critical/overdamped branch.

These statements are exact consequences of the specified second-order generator. They are **not automatically transferable to systems with different generators**.

---

## Domain-Licensing Rule

The current framework follows a simple principle:

> **No boundary without a generator; no coordinate without a licensed domain.**

Different dynamical classes require different coordinates.

### Positive curvature

For

\[
\ddot q+\gamma\dot q+\Omega^2 q=0,
\]

the mechanical damping ratio χ is licensed and χ = 1 is the critical-damping boundary.

### Negative curvature and reaction barriers

For

\[
\ddot q+\gamma\dot q-\omega_b^2 q=0,
\]

a useful normalized friction coordinate is

\[
\alpha_b=\frac{\gamma}{2\omega_b},
\]

but **α_b = 1 is not a critical-damping exceptional point**. The roots remain distinct with one stable and one unstable direction.

### Cosmological density growth

The flat-ΛCDM density-growth equation contains an inverted restoring term. Its normalized balance coordinate may satisfy

\[
\alpha_\delta=1 \iff q=0
\]

within flat ΛCDM, but this is a **balance/kinematic synchronization**, not a mechanical critical-damping EP of the density-growth generator.

### Particle widths

Ratios such as

\[
\Gamma/(2M)
\]

are treated as spectral-width coordinates unless an appropriate mechanical or equivalent dynamical generator is independently demonstrated.

### Non-Markovian dynamics

When dissipation contains memory, the characteristic object is generally

\[
D(s)=s^2+s\widetilde K(s)+\Omega_0^2.
\]

A repeated pole requires

\[
D(s_*)=0,
\qquad
D'(s_*)=0.
\]

The ordinary χ = 1 boundary is recovered only under an appropriate local/Markovian reduction.

### Open quantum systems

An exceptional-point claim requires coalescence and defectiveness of the relevant open-system generator. A scalar second-order rewriting alone does not establish defectiveness of the full microscopic or Liouvillian generator.

---

## Current Evidentiary Status

The following distinctions are part of the current SymC framework:

- The positive-curvature mechanical χ = 1 boundary is an exact dynamical result.
- The normalized underdamped poles of the canonical scalar generator trace a well-defined stability arc in the complex plane.
- Operator-first inheritance has prospective computational support within its registered passive-mechanical test domain, but is not presently claimed as a universal cross-domain inheritance law.
- Preferential natural occupancy near χ = 1 remains an open empirical question requiring an independently justified population or control null.
- A universal adaptive band such as **0.8 ≤ χ ≤ 1.0 is not a current general claim**.
- A universal maximum of information efficiency near χ = 1 is **not a current supported claim** for the proxies previously tested.
- Chemical barrier coordinates, cosmological balance coordinates, particle spectral-width ratios, and mechanical χ are not pooled as though they were the same physical observable.
- SymC is not presently asserted as a universal law of nature.

Negative results, retractions, failed prospective criteria, and domain restrictions are retained as part of the research record rather than removed or reclassified as successes.

---

## Historical Scope Note

Several PDFs in this repository are versioned research artifacts produced before the current generator-first domain-licensing framework was completed. They may therefore contain broader language or hypotheses that have since been narrowed, reclassified, or retracted.

The files are retained unchanged to preserve the research history.

When an older document conflicts with a later explicit correction, retraction, domain license, or reproducibility record, the later qualified interpretation should be used when describing the current SymC framework.

---

## Purpose of This Repository

- Preserve the foundational SymC research record.
- Maintain stable, versioned paper releases.
- Host supplementary derivations and supporting materials.
- Separate exact mathematical results from hypotheses and empirical claims.
- Record revisions, negative results, and scope corrections transparently.
- Provide a common theoretical base for independently tested domain-level applications.

---

## Related Resources

**Zenodo releases:** https://zenodo.org/communities/symc-universe/  
**ResearchGate:** https://www.researchgate.net/profile/Nate-Christensen-2  

Published stability-architecture work:

**Exceptional-point stability boundaries from quantum dissipation to cosmological acceleration**  
*Scientific Reports* (2026)  
DOI: 10.1038/s41598-026-56887-7

---

## License

This repository and its contents are licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)** unless otherwise stated in a specific file.

Reuse, redistribution, and adaptation are permitted with appropriate attribution. See the [LICENSE](./LICENSE) file for details.

When citing a research work, use the DOI and version associated with that work where available.

---

## Contact

**Nate Christensen**  
Independent Researcher  
SymC Universe Project
