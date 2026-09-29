# DESI Stability Architecture Conglomeration — Working Investigation

**Status:** ACTIVE, preregistration-before-interpretation  
**Branch:** `desi-stability-arc-main`  
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


## Executed scalar gate — 2026-09-29

The direct released-chain replay remains pending because the available remote execution surfaces did not permit the approximately 30–35 MB DESI chain transfer during this session. This did not change the preregistered scalar definitions or root rules. An independent reproduction lane was therefore added using the released DESI DR2 combined Gaussian BAO likelihood distributed through `CobayaSampler/bao_data`. The 13-point measurement vector and its (13\times13) covariance are pinned in this branch at upstream commit `bb0c1c9009dc76d1391300e169e8df38fd1096db`, with upstream blob SHAs `8aff444fdb42c0946342aa0011ab287eda097c4c` and `fd8e5697ab61379b07b52efb781ea6713417a4d9`.

This independent likelihood reconstruction reproduces the published DESI DR2 BAO posterior geometry closely enough to qualify the scalar lane. In flat \(\Lambda\)CDM it gives \(\Omega_{m,0}=0.297826^{+0.00836}_{-0.00878}\); in constant-\(w\)CDM it gives \(\Omega_{m,0}=0.297137^{+0.00862}_{-0.00907}\) and \(w=-0.916988^{+0.07869}_{-0.07602}\). In BAO-only \(w_0w_a\)CDM it gives \(\Omega_{m,0}=0.353095^{+0.04189}_{-0.01740}\), \(w_0=-0.470343^{+0.34357}_{-0.16945}\), and the 68% upper limit \(w_a<-1.3456\). These are posterior means with shortest 68% credible intervals or the corresponding one-sided upper limit, matching the DESI reporting convention.

The independent numerical \(\Lambda\)CDM identity control passes with
\[
\max\left|z_{q=0}-z_{\chi_\delta=1}\right|
=5.33\times10^{-15}.
\]
The scalar positive-control gate is therefore qualified independently of the still-pending official-chain replay.

For constant-\(w\)CDM, the posterior transition summaries are approximately
\[
z_{q=0}=[0.6440,\,0.6716,\,0.6971]_{16,50,84},
\]
\[
z_{\chi_\delta=1}=[0.6769,\,0.7583,\,0.8621]_{16,50,84},
\]
and
\[
\Delta z=[-0.1940,\,-0.0852,\,-0.0041]_{16,50,84}.
\]
The posterior correlation between \(\Delta z\) and \(w\) is approximately \(-0.97\). This strongly limits the interpretation of \(\Delta z\) in constant-\(w\)CDM: it is principally a transformed equation-of-state diagnostic within the specified native background model, not independent evidence for new dynamics.

## Background algebraic-dependence boundary

For spatially flat GR with pressureless matter and a smooth dark-energy component,
\[
\Omega_m(a)=\frac{2}{3\chi_\delta^2(a)}
\]
and therefore
\[
q(a)
=
\frac12
\left[
1+3w(a)
\left(
1-\frac{2}{3\chi_\delta^2(a)}
\right)
\right].
\]
For \(\Lambda\)CDM, \(w=-1\), so
\[
q(a)=\chi_\delta^{-2}(a)-1.
\]
Thus \(q(a)\) and \(\chi_\delta(a)\) are not independent information once the flat GR matter+DE background model is specified. A background Stability Arc may use both as useful coordinates or representations, but their joint use alone cannot establish an independent capital-\(\Chi\) degree of freedom, SI, or new dark-sector dynamics. This is now a standing refusal condition for the cosmology lane.

A genuinely additional candidate \(\Chi_{\mathrm m}\) must therefore contain information from the matter-growth sector not algebraically generated by the same background coordinates. Candidate native quantities include \(D(k,a)\), \(f(k,a)\), \(f\sigma_8(a)\), \(P(k,a)\), and their covariance-supported modal or scale-dependent structure. DESI DR1 full-shape products are promoted to the next empirical lane for that purpose.

## Multiple-transition Limit Map

The BAO-only \(w_0w_a\) posterior exposes a failure of the single unlabeled transition-offset representation. Approximately 39.3% of posterior resamples contain one \(q(z)=0\) crossing on \(0\le z\le5\), while approximately 60.7% contain two. By contrast, \(\chi_\delta(z)=1\) has one crossing in approximately 99.97% of the same resamples. DESI explicitly identifies the BAO-only \(w_0w_a\) posterior as prior-bound, so these topology fractions are exploratory properties of that posterior and must not be promoted as cosmological population frequencies.

For the two-\(q\)-crossing branch, the most recent crossing has median
\[
z_{q=0}^{\mathrm{recent}}\approx0.132,
\]
the earlier crossing has median
\[
z_{q=0}^{\mathrm{earlier}}\approx0.852,
\]
and the unique scalar Stability Architecture crossing has median
\[
z_{\chi_\delta=1}\approx0.663.
\]
The same posterior states are typically decelerating again at \(z=0\), whereas the one-crossing branch is accelerating at \(z=0\). Therefore a single symbol \(z_{q=0}\) loses physically relevant history whenever the trajectory is non-monotonic.

The transition-set representation is now
\[
\mathcal Z_q
=
\{z\ge0:q(z)=0\},
\qquad
\mathcal Z_{\chi_\delta}
=
\{z\ge0:\chi_\delta(z)=1\}.
\]
A scalar \(\Delta z\) is admissible without an additional branch label only when the relevant transition set is unique. If \(|\mathcal Z_q|>1\), the analysis must retain the complete crossing set or explicitly identify the branch, for example \(z_{q=0}^{\mathrm{recent}}\) and \(z_{q=0}^{\mathrm{earlier}}\). This is a Stability Arc / Limit Map requirement, not an exception to be averaged away.

## Next admitted gate: independent matter-growth information

The scalar background gate has passed and simultaneously established its own information limit. The next stage is therefore not additional background-variable accumulation. It is a DESI full-shape growth investigation designed to determine whether a defensible matter-side architecture
\[
\Chi_{\mathrm m}(k,a)
\]
can be reconstructed independently enough to test its relationship with
\[
\Chi_{\mathrm{bg}}(a).
\]
The first task is to pin the public DESI DR1 full-shape data vector, covariance, window/response information, tracer/redshift definitions, and native likelihood or validated public implementation. The full-shape lane must reproduce a DESI-published growth or cosmological result before any joint \(\Chi\), Stability Arc, SI, DM, or DE interpretation is admitted.

The joint target, if both sides qualify, remains
\[
\mathcal A_{\Chi}^{\mathrm{cosmo}}
:
a\mapsto
\left[
\Chi_{\mathrm{bg}}(a),
\Chi_{\mathrm m}(k,a)
\right],
\]
with any proposed
\[
\mathcal T_{\mathrm{SI}}
\]
required to add predictive or organizational information beyond the native GR/Friedmann/growth dependence. The official DESI DR2 Cobaya-chain replay remains a required independent cross-check of the background lane, but it is no longer a blocker for opening the orthogonal full-shape growth lane.
