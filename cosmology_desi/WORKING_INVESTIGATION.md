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

## DR1 full-shape growth gate frozen — 2026-09-29

The matter-growth lane is now frozen in `cosmology_desi/DR1_FULL_SHAPE_GROWTH_GATE.md`. The confirmatory target is the official DESI DR1 full-shape plus BAO analysis, with the first reproduction criterion anchored to
\[
\Omega_{\mathrm m,0}=0.2962\pm0.0095,
\qquad
\sigma_8=0.842\pm0.034.
\]
The DESI Key Project likelihood lineage is pinned by immutable commit and blob identities in `cosmology_desi/data/desi_dr1_fullshape_upstream_provenance.json`. No upstream source code is vendored because no explicit root license file was detected at the pinned repository revision; the code is referenced rather than copied.

The compressed ShapeFit+BAO Appendix-A blocks are separately recorded in `cosmology_desi/data/desi_dr1_shapefit_bao_appendixA.json` with the explicit status `exploratory_engineering_only`. Those values were inspected during design, so they cannot serve as an unseen confirmatory holdout. Their provisional coordinate
\[
g_{\mathrm{SF}}(z_i)
=
\frac{f\sigma_{s8}(z_i)}{[f\sigma_{s8}(z_i)]_{\mathrm{fid}}}
\]
is an engineering diagnostic, not \(\Chi_{\mathrm m}\). The corresponding preflight script tests only covariance handling, consistency with the fiducial growth history, and simple constant/trend summaries. No transition or SI claim is licensed from those six points.

The next confirmatory action is therefore reproduction of the DESI full-modeling posterior under its native likelihood structure. Only after that reproduction passes may the growth-side quantities be reconstructed into candidate \(\Chi_{\mathrm m}(k,a)\) components and compared with \(\Chi_{\mathrm{bg}}(a)\).

## DR1 ShapeFit engineering preflight executed — 2026-09-29

The frozen exploratory preflight has been executed from the exact six ShapeFit+BAO Appendix-A blocks. The normalized growth coordinates are
\[
g_{\mathrm{SF}}(z_i)
=
[0.8391,\,1.1571,\,1.0407,\,0.9969,\,0.9449,\,1.1649]
\]
for BGS, LRG1, LRG2, LRG3, ELG2 and QSO respectively, with propagated one-sigma uncertainties
\[
[0.1905,\,0.1255,\,0.1042,\,0.0938,\,0.0871,\,0.1223].
\]
Relative to the fiducial compressed growth history, the block-independent growth-only statistic is
\[
\chi^2=4.6517\quad\text{for 6 coordinates},
\qquad p=0.5892.
\]
The weighted constant is \(g_{\mathrm{SF}}=1.0256\pm0.0449\), while a weighted linear fit gives a slope \(0.0084\pm0.1226\) per unit redshift. This engineering representation therefore contains no resolved overall offset or simple redshift trend from the fiducial growth history.

Using the published DESI full-shape central value \(\Omega_{\mathrm m,0}=0.2962\) only as a background overlay gives
\[
z_{q=0}=z_{\chi_\delta=1}=0.68125
\]
for flat \(\Lambda\)CDM. The six compressed growth points straddle that redshift, but **no break or transition test was preregistered for these sparse points**, so no discontinuity claim is permitted. This is an explicit anti-post-hoc constraint. The machine-readable output is stored at `cosmology_desi/results/desi_dr1_growth_preflight.json`.

The result is therefore a useful null-like engineering check: the compact growth representation behaves ordinarily enough to proceed, but it does not itself supply a \(\Chi_{\mathrm m}\) detection. The confirmatory full-modeling reproduction remains the active gate.

## Confirmatory DR1 lineage correction — 2026-09-29

A lineage audit found that the initially inspected compact chain directory used the \`all-nolya\` suffix. That directory is **not** the exact chain family corresponding to the published DESI (FS+BAO)+BBN+\(n_{\mathrm{s10}}\) baseline because DESI includes Ly\(\alpha\) BAO as a background-geometry constraint while using no Ly\(\alpha\) full-shape growth information. The confirmatory target has therefore been corrected, before any \(\Chi_{\mathrm m}\) result was inspected, to

\`cobaya/base/desi-reptvelocileptors-fs-bao-all_schoneberg2024-bbn_planck2018-ns10/\`.

The official release SHA-256 manifest and file sizes are now pinned in \`cosmology_desi/data/desi_dr1_fullshape_upstream_provenance.json\`. The four exact posterior chain files total \(992{,}643{,}390\) bytes, so the default reproduction path will use the compact input, covariance, checkpoint and marginal-statistic files first and will download the full posterior only when sample-level \(\Chi_{\mathrm m}\) derivation requires it. The \`all-nolya\` products remain available only as a later sensitivity check on the effect of removing Ly\(\alpha\) background information.


## DR1 adversarial-ladder correction — 2026-09-29

The DR1 model ladder has been tightened before any confirmatory (Chi_{mathrm m}) result is inspected. The DESI-only (mu)-(Sigma) modified-gravity chain is the first clean growth-sector adversary after the baseline reproduction. A free-neutrino-mass DESI-only baseline chain has not yet been qualified and is therefore marked fresh-run-required rather than silently replaced by a CMB-combined chain. The DESI-only (w_0w_a) chain is retained solely as a parameter-projection stress test; it is not the physical DE comparator because the published DESI analysis reports strong projection effects in that DESI-only posterior. The physical DE lane will use a DESI+CMB+SN combination selected and frozen before its Stability-Architecture result is inspected.

The transport runner now accepts explicit chain roles via `--chain-key baseline`, `modified_gravity`, or `w0wa_desi_only_stress`. Those names encode the scientific role so a stress-test chain cannot accidentally be promoted into confirmatory evidence by convenience.

## Dark-energy comparator suite frozen — 2026-09-29

To avoid selecting a supernova sample by the resulting \(w_0,w_a\) behavior, the physical DE comparator is now a three-member sensitivity suite: DESI (FS+BAO)+CMB+Pantheon+, DESI (FS+BAO)+CMB+Union3, and DESI (FS+BAO)+CMB+DESY5, all using the DESI default Planck PR3 TT/TE/EE plus Planck+ACT DR6 lensing combination. No member is designated primary. A later Stability-Architecture result must state whether it is common to all three, limited to a subset, or materially sample-dependent. The exact public release directory identities and file sizes are pinned in the provenance manifest; SHA-256 receipts remain to be added before automated download.


## DR1 confirmatory baseline gate passed on Popstop — 2026-09-29

The exact DESI DR1 confirmatory baseline compact release files were downloaded on Popstop through the frozen transport runner and all five SHA-256 receipts matched the pinned manifest. The released DESI posterior summary \`chain.margestats\` gives
\[
\Omega_{\mathrm m,0}=0.2963\pm0.0094,
\qquad
\sigma_8=0.842\pm0.034.
\]
Against the preregistered reproduction targets
\[
\Omega_{\mathrm m,0}=0.2962\pm0.0095,
\qquad
\sigma_8=0.842\pm0.034,
\]
the \(\Omega_{\mathrm m,0}\) central-value offset is approximately \(0.011\) published standard deviations and its 68% interval width differs by approximately \(1.1\%\); \(\sigma_8\) matches at the reported precision. Both preregistered acceptance criteria therefore pass.

The released \`chain.input.yaml\` and \`chain.updated.yaml\` also confirm the intended baseline structure: flat \(\Lambda\)CDM with \(w_0=-1\), \(w_a=0\), \(\Omega_k=0\), \(\sum m_\nu=0.06\,\mathrm{eV}\), DESI full-shape+BAO tracers BGS/LRG/ELG/QSO plus Ly\(\alpha\) BAO geometry, Schöneberg-2024 BBN, and the broad Planck-2018 \(n_s\) prior used by the DESI release. The updated configuration records the full-shape \(k\)-range \(0.02\le k\le0.2\) and analytic marginalization mode.

This passes the confirmatory reproduction gate required before sample-level matter-architecture work. Full baseline posterior download is now scientifically admitted for reconstruction of native growth quantities and candidate \(\Chi_{\mathrm m}(k,a)\). The gate passage does not itself establish \(\Chi_{\mathrm m}\), a joint Stability Arc, SI, modified gravity, DM interaction, or DE dynamics.


## Scope boundary — DM/DE lane only — 2026-09-29

By explicit program decision, this investigation now remains restricted to dark matter, dark energy, and directly competing cosmological explanations. Earlier Stability-Architecture and Stability-Inheritance material in this working history is retained for provenance only and is not an active interpretive lane here. Cross-project conglomeration, \(\Chi\) construction, Stability Arc, and SI interpretation continue in the separate SI project.

The active sequence is native cosmology first: flat \(\Lambda\)CDM reference, dynamical-DE alternatives, modified-gravity adversaries, neutrino-mass effects, and DM-DE interaction models where a released or freshly reproducible likelihood is available. No dark-sector result will be promoted merely because it supports a broader cross-domain framework.

## Full DR1 baseline posterior audited — 2026-09-29

All four official DESI DR1 full-shape+BAO baseline posterior chains are present on Popstop and pass the pinned SHA-256 receipts, totaling 992,643,390 bytes. Weighted analysis of 857,201 released chain rows gives \(\Omega_m=0.29612\,[0.28687,0.30566]\), \(\Omega_\Lambda=0.70380\,[0.69427,0.71305]\), \(\sigma_8=0.84091\,[0.80787,0.87529]\), \(H_0=68.566\,[67.829,69.310]\,\mathrm{km\,s^{-1}\,Mpc^{-1}}\), and standard \(S_8=0.83562\,[0.80133,0.87104]\) for the 16th/50th/84th percentiles.

Within the frozen flat-\(\Lambda\)CDM reference only, the corresponding non-baryonic fraction of total matter is 0.84211 [0.83642, 0.84757], the present \(\rho_{\rm DE}/\rho_m\) ratio is 2.3767 [2.2714, 2.4856], matter-DE density equality occurs at \(z=0.33452\,[0.31451,0.35460]\), and the acceleration transition occurs at \(z=0.68139\,[0.65618,0.70670]\). These are native-model posterior re-expressions, not evidence for interacting DM, dynamical DE, or modified gravity.

The four chain means agree to 0.013 pooled standard deviations for \(\Omega_m\), 0.0069 for \(\sigma_8\), and 0.033 for \(H_0\), establishing a stable numerical reference surface for adversarial dark-sector comparisons.


## DESI-only modified-gravity adversary completed — 2026-09-29

The four official DESI DR1 \(\mu_0\)-\(\Sigma_0\) posterior chains were downloaded on Popstop and all pinned SHA-256 receipts passed. In this nested flat-\(\Lambda\)CDM perturbation-sector extension, weighted full-chain analysis gives \(\mu_0=0.0872\,[-0.3805,0.6065]\) for the 16th/50th/84th percentiles, consistent with the GR reference \(\mu_0=0\). DESI FS+BAO alone does not directly constrain \(\Sigma_0\); its one-sided marginal is therefore not interpreted as evidence and is strongly shaped by the hard numerical prior \(\mu_0<2\Sigma_0+1\).

Allowing \(\mu_0,\Sigma_0\) produces only small descriptive shifts in the core dark-sector reference posterior: \(\Omega_m\) moves by \(-0.071\) baseline standard deviations, \(\sigma_8\) by \(-0.096\), \(H_0\) by \(-0.060\), and standard \(S_8\) by \(-0.119\). Their posterior widths change by only about 0.5–2%. The dominant new degeneracy is instead \(\mathrm{corr}(\mu_0,\log A_s)=-0.829\), and the \(\log A_s\) posterior standard deviation expands by a factor of 1.80. Correlations of \(\mu_0\) with \(\sigma_8\) and \(S_8\) are much smaller, approximately \(-0.190\) and \(-0.206\).

This is a useful refusal result for any claim that DESI-only modified-gravity freedom materially reorganizes the fitted \(\Omega_m\), \(\sigma_8\), \(S_8\), or \(H_0\) reference posterior. It does not exclude modified gravity generally. The DESI functional form also ties the redshift dependence of \(\mu(a)\) and \(\Sigma(a)\) to the dark-energy density, so an approach toward GR at higher redshift is partly parameterization-imposed rather than an independent empirical discovery.


## Physical \(w_0w_a\) dark-energy sensitivity suite completed — 2026-09-29

The frozen three-member physical-DE suite has completed on Popstop. All official DESI DR1 full-shape+BAO+CMB+SN chain files for Pantheon+, Union3, and DESY5 were downloaded from the public release and passed their pinned SHA-256 receipts before analysis. The same weighted analysis was then applied to all three chain sets without selecting a preferred supernova sample.

The recovered posterior centers reproduce the published DESI full-shape constraints to rounding. Pantheon+ gives \(w_0=-0.8591\) [\(-0.9189,-0.7978\)] and \(w_a=-0.6706\) [\(-0.9337,-0.4279\)]; Union3 gives \(w_0=-0.7439\) [\(-0.8390,-0.6477\)] and \(w_a=-1.0066\) [\(-1.3597,-0.6715\)]; DESY5 gives \(w_0=-0.7624\) [\(-0.8257,-0.6962\)] and \(w_a=-0.9510\) [\(-1.2402,-0.6824\)]. All intervals are weighted 16th/50th/84th percentiles.

The directional result is common to all three samples: every posterior median has \(w_0>-1\) and \(w_a<0\). However, the exact posterior location is not sample-invariant. The largest pairwise median displacement is \(1.085\) quadrature-combined posterior standard deviations in \(w_0\) and \(0.783\) in \(w_a\). The corresponding largest normalized shifts are \(0.91\) for \(\Omega_m\), \(0.57\) for \(\sigma_8\), \(0.93\) for \(H_0\), and only \(0.39\) for standard \(S_8\). The correct classification is therefore **shared directional DE behavior with non-negligible supernova-sample dependence in its precise location**, not a single sample-independent parameter point.

Within the CPL form \(w(a)=w_0+w_a(1-a)\), nearly all posterior weight in each member admits a positive finite \(w=-1\) crossing. Conditional crossing medians are \(z\simeq0.263\) (Pantheon+), \(0.339\) (Union3), and \(0.332\) (DESY5). At \(z=0.5\), all three weighted median trajectories are already near \(w\simeq-1.08\); by \(z=2\), the medians are approximately \(-1.31\), \(-1.41\), and \(-1.40\). These histories are CPL-derived consequences of the fitted \((w_0,w_a)\) posterior and are not model-independent reconstructions.

Posterior sign masses and Gaussian covariance distances from \((-1,0)\) are retained only as descriptive diagnostics. They are not frequentist significances or model-selection statistics. Exact nested-model comparison is reserved for the matched released \(\Lambda\)CDM and \(w_0w_a\) posterior-maximization products under the identical three data combinations.


## Matched released \(\Lambda\)CDM versus \(w_0w_a\) best-fit gate — 2026-09-29

The official DESI DR1 iminuit posterior-maximization products were independently retrieved for matched \(\Lambda\)CDM and \(w_0w_a\)CDM fits under each of the three DESI(FS+BAO)+CMB+SN combinations. All six bestfit.minimum.txt files passed their official release SHA-256 receipts.

The released minimizer products give \(\Delta\chi^2=\chi^2_{w_0w_a}-\chi^2_{\Lambda{\rm CDM}}\) of \(-8.2629\) for Pantheon+, \(-14.3983\) for Union3, and \(-17.6711\) for DESY5. An asymptotic two-degree-of-freedom Wilks conversion gives descriptive two-sided normal equivalents of \(2.41\sigma\), \(3.37\sigma\), and \(3.80\sigma\), respectively. These independently reproduce the ordering and closely reproduce the magnitudes of the DESI paper's chain-MAP values \(-8.8,-14.5,-17.5\) and reported \(2.5\sigma,3.4\sigma,3.8\sigma\). The released minimizer outputs and paper MAP values are not treated as mathematically identical estimators.

The fit improvement is not supplied by a single probe in the released minima. For Pantheon+, the DESI FS+BAO, CMB, and SN contributions change by approximately \(-3.43,-2.82,-1.73\); for Union3 by \(-5.45,-3.00,-5.96\); and for DESY5 by \(-6.38,-2.18,-9.07\). Component sums can differ slightly from the total because the full objective contains prior and nuisance contributions. The important result is that the preference is jointly supported by the combined likelihood rather than reducible to one isolated data component.

This gate supports further investigation of dynamical-DE explanations but does not establish a physical dark-energy mechanism. CPL remains a phenomenological two-parameter expansion-history model, and model-form dependence, supernova systematics, neutrino freedom, modified gravity, and explicit dark-sector interaction alternatives remain active adversarial lanes.
