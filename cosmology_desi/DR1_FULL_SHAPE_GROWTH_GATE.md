# DESI DR1 Full-Shape Growth Gate

**Status:** FROZEN BEFORE CONFIRMATORY GROWTH-ARCHITECTURE ANALYSIS  
**Opened:** 2026-09-29  
**Parent lane:** `cosmology_desi/WORKING_INVESTIGATION.md`

The DR2 BAO background gate established both a usable scalar representation and an information limit: within a specified flat GR matter+DE background, \(q(a)\) and \(\chi_\delta(a)\) are algebraically linked and therefore cannot by themselves establish an independent \(\Chi\) architecture or Stability Inheritance. The next admitted question is whether DESI growth information supports a matter-side organization \(\Chi_{\mathrm m}(k,a)\) that adds information beyond those background coordinates.

## Confirmatory lane

The confirmatory lane uses the DESI DR1 full-shape plus BAO analysis, not the compressed ShapeFit points. The implementation lineage is pinned to `cosmodesi/desi-kp-cosmological-likelihoods` at commit `7d51f4f86dc3bee6bf10f1a684913c943a89a844`. At that commit the relevant upstream blobs are:

- `dr1/cobaya/desi_fs_bao_all.py`: `b7df6f0a749853d7010024f56c412bf6a234a0e5`
- `dr1/cobaya/desi_fs_bao_all.yaml`: `45c5598b38f111a22993c8e47da4c54d157210e3`
- `dr1/cobaya/reptvelocileptors.py`: `6ce72067a744c7bb011bca7a3258d49a1fdfdc71`
- `dr1/cobaya/download.py`: `55cc0a6d7ef956e9b060f402d281fa56f8fbf573`
- `dr1/cobaya/test_fs_bao_all.yaml`: `5ea6bd68c07f448e5e7e0ec06ca4eaf984c9339c`

The upstream repository contains no explicit license file at the pinned root, so its source code is referenced by commit and blob identity rather than vendored into this repository. The public DESI likelihood/data products remain the intended scientific inputs.

The exact confirmatory chain family is

`cobaya/base/desi-reptvelocileptors-fs-bao-all_schoneberg2024-bbn_planck2018-ns10/`.

The `all` suffix is required. DESI's published FS+BAO baseline includes the Ly\(\alpha\) BAO likelihood as a background-geometry constraint even though Ly\(\alpha\) supplies no full-shape growth measurement in this analysis. The previously inspected `all-nolya` directory is therefore not the exact reproduction target for the published baseline and is retained only as a possible later sensitivity test.

The first confirmatory reproduction target is the published DESI-only full-shape plus BAO flat-\(\Lambda\)CDM result

\[
\Omega_{\mathrm m,0}=0.2962\pm0.0095,
\qquad
\sigma_8=0.842\pm0.034.
\]

Before any \(\Chi_{\mathrm m}\) construction is admitted, a reproduced posterior must satisfy both of the following implementation-level acceptance checks: the posterior central value for each target must lie within \(0.25\) published standard deviations of the DESI value, and the reproduced 68% interval width must agree with the published width to within 15%. Failure does not license retuning toward the target; it triggers root-cause analysis of data version, priors, nuisance treatment, scale cuts, covariance/systematics, theory engine, and summary convention.

The confirmatory lane must preserve the DESI tracer/redshift structure and covariance treatment. The official implementation uses BGS, three LRG bins, ELG, QSO and Ly\(\alpha\) BAO, with full-shape information for the non-Ly\(\alpha\) tracers, power-spectrum multipoles, window application, and analytic marginalization of specified nuisance directions. Any simplified alternative is a diagnostic or exploratory cross-check rather than a substitute for this gate.

## Exploratory engineering lane

The exact DR1 ShapeFit+BAO Appendix-A Gaussian blocks have already been inspected during design. They are therefore **not an unseen holdout** and cannot later be promoted as confirmatory evidence for \(\Chi_{\mathrm m}\), SI, DM, DE, or modified gravity. They are retained only as a compact engineering representation for testing notation, covariance handling, redshift ordering and candidate trajectory diagnostics.

The provisional normalized growth coordinate is

\[
g_{\mathrm{SF}}(z_i)
=
\frac{f\sigma_{s8}(z_i)}
{\left[f\sigma_{s8}(z_i)\right]_{\mathrm{fid}}},
\]

where the subscript \(s8\) is retained exactly because this is the ShapeFit quantity used by DESI. This coordinate is **not** \(\Chi_{\mathrm m}\). It is a six-bin growth diagnostic whose job is to expose whether a candidate architecture or transition statistic is merely repackaging the fiducial growth history.

The preregistered exploratory outputs are the six \(g_{\mathrm{SF}}(z_i)\) values with their propagated uncertainties, the block-independent growth-only \(\chi^2\) relative to \(g_{\mathrm{SF}}=1\), a weighted constant fit, and a weighted linear trend with redshift. Background quantities \(q(z_i)\) and \(\chi_\delta(z_i)\) may be overlaid only as coordinates for comparison. No discontinuity, slope change, or transition claim is admissible from six sparse points unless a separate model and covariance-aware test is frozen before it is evaluated.

## Admission and refusal rules

A candidate \(\Chi_{\mathrm m}\) is admitted only if it uses matter-growth or scale-dependent information not algebraically generated by the background coordinates alone, survives nuisance/covariance controls, and is demonstrably more informative than its native constituent observables. Possible native inputs include \(D(k,a)\), \(f(k,a)\), \(f\sigma_8(a)\), \(P(k,a)\), and modal or scale-dependent structure licensed by the full-shape likelihood.

A joint cosmological architecture

\[
\mathcal A_{\Chi}^{\mathrm{cosmo}}
:
a\mapsto
\left[
\Chi_{\mathrm{bg}}(a),
\Chi_{\mathrm m}(k,a)
\right]
\]

is refused if the apparent coupling disappears after conditioning on the native GR/Friedmann/growth model, if it is driven by one tracer/bin or nuisance choice, if \(\Chi_{\mathrm m}\) collapses to a monotonic rescaling of \(f\sigma_8\) or \(\sigma_8\), or if the construction requires post hoc component selection after seeing the confirmatory output. Any proposed \(\mathcal T_{\mathrm{SI}}\) remains one gate later and must add predictive or organizational information beyond the native cosmological dependence.

## Native growth/background partition and mock-first development

Inspection of the pinned DESI full-shape implementation establishes a native partition that will be retained before any capital-\(\Chi\) construction. The matter-growth theory state contains

\[
\mathcal G_{\mathrm{native}}(k,z)
=
\left\{
P_{\delta\delta}(k,z),
P_{\theta\theta}(k,z),
P_{\mathrm{nw}}(k,z),
\sigma_8(z),
f\sigma_8(z),
f(k,z)
\right\},
\]

where the implementation obtains the scale-dependent velocity-to-density response from the density and velocity power spectra. These are candidate native inputs, not a declaration that all components belong in \(\Chi_{\mathrm m}\). The background/geometry side is kept separate through quantities such as the Alcock-Paczynski responses \(q_{\parallel}(z)\), \(q_{\perp}(z)\), \(H(z)\), distances, and the already-qualified \(\chi_\delta(z)\). Nuisance/bias parameters remain a third layer and are not allowed to become apparent stability coordinates merely because they improve a fit.

The development order is mock-first. The 1000 EZmocks may be used for mechanical stress tests, null-distribution engineering and representation-development diagnostics, with the dependence created by their role in covariance estimation recorded explicitly. The 25 AbacusSummit cut-sky mocks are reserved as a higher-fidelity **pre-DESI holdout**: candidate representation choices and thresholds must be frozen before those 25 mocks are opened for evaluation. The real DESI data remain last. Failure on the Abacus holdout returns the representation to development without inspecting the DESI stability result.

## Adversarial cosmology ladder

Once the baseline full-shape posterior is reproduced, model comparisons are ordered by physical perturbation class rather than by whichever extension gives the most interesting answer. The baseline is flat \(\Lambda\)CDM. The first clean growth-sector adversary is DESI's \(\mu\)-\(\Sigma\) modified-gravity family, because it can alter the growth/gravity response while retaining a \(\Lambda\)CDM background. The exact DESI-only public chain family is pinned separately in the provenance manifest and may be used after the baseline reproduction passes.

The second desired adversary is free neutrino mass, which provides a physically established scale-dependent growth perturbation through free streaming. A DESI-only posterior with the required baseline likelihood is scientifically desirable, but an exact public chain matching the baseline naming has not yet been qualified in the release tree. The neutrino lane is therefore marked **fresh-run-required unless an exact released chain is subsequently located**. No substitute chain is to be chosen merely because it is available.

The DESI-only \(w_0w_a\) chain is retained only as a **projection-stress test**. DESI's published full-shape analysis states that the DESI-only \(w_0w_a\) posterior is strongly affected by parameter-projection effects and therefore does not present it as a physical dark-energy constraint. It must not be used as the confirmatory DE comparator. The physical DE comparison is deferred to the published DESI+CMB+SN combinations, with a specific supernova combination frozen before any Stability-Architecture result from that comparison is inspected. Joint extensions such as \(w_0w_a\)+modified gravity are admitted only after the single-extension tests establish identifiability.

The qualitative refusal tests are fixed in advance. If a proposed \(\Chi_{\mathrm m}\) cannot distinguish a growth-sector perturbation from a pure amplitude rescaling, it is inadequate. If it cannot represent scale-dependent neutrino suppression without collapsing that information into a single background coordinate, it is inadequate. If its apparent relation to \(\Chi_{\mathrm{bg}}\) remains unchanged under modified gravity even when the native growth observables change, the claimed cross-sector meaning is suspect. Conversely, a difference between model families is not automatically evidence for SI; it must survive conditioning on the native model variables and demonstrate information not already carried by those variables directly.
