# DESI Stability Architecture Conglomeration — Working Investigation

**Status:** ACTIVE, preregistration-before-interpretation  
**Branch:** `desi-stability-arc`  
**Parent program:** SymC / Stability Architecture / Stability Inheritance  
**Primary external dataset:** DESI DR2 public BAO cosmology posterior products  
**Created:** 2026-09-29

## Scientific purpose

This investigation tests the published cosmological Stability Architecture construction against released DESI posterior products before extending interpretation to capital Chi, the Stability Arc, Stability Inheritance (SI), dark matter (DM), or dark energy (DE).

The first gate is deliberately scalar and reproduction-first. For each posterior sample, derive the late-time background quantities and compute

\[
\chi_\delta(z)=\frac{H(z)}{\sqrt{4\pi G\rho_m(z)}}=\sqrt{\frac{2}{3\Omega_m(z)}}
\]

under the same late-time matter+DE assumptions used for the published construction, together with the deceleration parameter

\[
q(z)=-\frac{\ddot a}{aH^2}.
\]

The primary transition quantities are

\[
z_{\chi_\delta=1},\qquad z_{q=0},\qquad
\Delta z=z_{q=0}-z_{\chi_\delta=1}.
\]

For flat late-time LambdaCDM, the required internal positive control is

\[
\chi_\delta=1\Longleftrightarrow q=0,
\]

up to numerical root tolerance under the same assumptions.

## Gate structure

**G0 — provenance and ingestion.** Download DESI public posterior chain files directly from the official DESI data host. Record exact source URLs and SHA-256 hashes. Refuse interpretation if the files cannot be retrieved or parsed.

**G1 — native posterior reproduction.** Parse Cobaya posterior weights and parameters without re-fitting. Record sample counts, effective weight information, parameter aliases actually used, and weighted posterior summaries. No Stability Architecture interpretation is allowed if parameter identification is ambiguous.

**G2 — published scalar positive control.** Apply the flat late-time LambdaCDM reconstruction. Require numerical coincidence of the most recent roots of \(q(z)=0\) and \(\chi_\delta(z)=1\) for posterior samples with valid unique roots. Failure is a code/model-assumption error until proven otherwise.

**G3 — extension without reinterpretation.** Apply the same root extraction to \(w\)CDM and \(w_0w_a\)CDM. Report posterior distributions of \(z_{q=0}\), \(z_{\chi_\delta=1}\), \(\Delta z\), current \(q_0\), and \(\chi_{\delta,0}\). Do not treat nonzero \(\Delta z\) as evidence for SI, modified gravity, or dynamical DE by itself.

**G4 — architecture admission.** Only after G0–G3 pass may candidate background and matter architectures \(\Chi_{\mathrm{bg}}\) and \(\Chi_{\mathrm{m}}\) be reconstructed. Their components are not fixed in advance.

**G5 — Stability Arc and SI.** A cosmological Stability Arc \(\mathcal A_{\Chi}^{\mathrm{cosmo}}\) and any SI transformation \(\mathcal T_{\mathrm{SI}}\) remain gated behind evidence that the joint representation adds information beyond the native cosmological model.

## Root and refusal rules

The first-pass search interval is \(0\le z\le 5\). The primary reported transition is the lowest nonnegative-redshift crossing, i.e. the most recent crossing in cosmic history.

For both \(q(z)=0\) and \(\chi_\delta(z)=1\), each posterior sample is classified as having zero, one, or multiple sign-changing roots on the search interval. Zero-root and multiple-root samples are preserved in the output. They are not replaced by boundary values and are not dropped silently.

A posterior summary of \(\Delta z\) uses only samples for which both primary roots are defined. The output must also report the weighted fraction of the posterior excluded by this requirement and the reason.

## Model order

The initial model order is:

1. flat LambdaCDM (`base`) as the positive control;
2. constant-\(w\) CDM (`base_w`);
3. CPL \(w_0w_a\)CDM (`base_w_wa`).

The first ingestion run uses the official `desi-bao-all` chain directories. External combinations such as DESI+CMB and DESI+CMB+SN are added only after the ingestion and scalar machinery passes on the simplest released products.

## Interpretation firewall

A nonzero \(\Delta z\), a shift in \(q_0\), or a difference between models is not by itself evidence for SI, DM-DE interaction, modified gravity, or a new physical field. The first-stage outputs are posterior-derived coordinates and transition statistics.

The working null remains that LambdaCDM + GR + standard structure growth explains all apparent relations between the scalar Stability Architecture quantities and any later reconstructed capital-Chi architecture. SI must add predictive or organizational information beyond native-model dependence to earn promotion.

## Immediate deliverables

The executable lane must produce: (1) a provenance manifest with official URLs and hashes, (2) machine-readable posterior summaries, (3) per-model root/refusal counts, (4) a LambdaCDM identity QA record, and (5) a compact human-readable report. Later stages will add DESI+CMB, SN combinations, DR1 full-shape growth information, candidate \(\Chi_{\mathrm{bg}}\) and \(\Chi_{\mathrm{m}}\), and \(\mathcal A_{\Chi}^{\mathrm{cosmo}}\) only after the scalar gate is clean.
