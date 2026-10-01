# DESI DR2 BAO Independent Stability-Architecture Gate — 2026-09-29

## Scope and validation

This record documents the first executed DESI test in the Stability Architecture / Stability Inheritance cosmology lane. It uses the released DESI DR2 combined 13-point Gaussian BAO vector and 13x13 covariance distributed through `CobayaSampler/bao_data`, pinned at upstream commit `bb0c1c9009dc76d1391300e169e8df38fd1096db`. The upstream mean-vector blob is `8aff444fdb42c0946342aa0011ab287eda097c4c`; the covariance blob is `fd8e5697ab61379b07b52efb781ea6713417a4d9`. This is an independent likelihood reconstruction, not yet the planned replay of DESI's released Cobaya chains.

The released BAO likelihood is modeled in terms of the sampled scale (h r_d) and the flat late-time background. For each background shape, (h r_d) is locally marginalized under a broad flat prior; the Stability Architecture quantities used here depend on the background shape rather than the absolute BAO scale. The (Lambda)CDM maximum-likelihood solution is (Omega_{m,0}=0.2974618), (h r_d=101.5398,mathrm{Mpc}), with (chi^2_{min}=10.27104). The (w)CDM solution is (Omega_{m,0}=0.2976936), (w=-0.91190), with (chi^2_{min}=9.04105). The (w_0w_a)CDM maximum-likelihood solution is (Omega_{m,0}=0.38661), (w_0=-0.17883), (w_a=-2.71668), with (chi^2_{min}=5.61860). Thus (Deltachi^2_{mathrm{MAP}}=-4.65244) relative to (Lambda)CDM, equivalent to approximately (1.66sigma) for two added parameters, reproducing DESI's quoted BAO-only result of approximately (1.7sigma).

The marginalized shape posterior also reproduces DESI's published summaries. Using posterior means and shortest 68% credible intervals, the reconstruction gives (Omega_{m,0}=0.29783^{+0.00836}_{-0.00878}) in (Lambda)CDM, compared with DESI's (0.2975pm0.0086). In (w)CDM it gives (Omega_{m,0}=0.29714^{+0.00862}_{-0.00907}) and (w=-0.91699^{+0.07869}_{-0.07602}), compared with DESI's (0.2969pm0.0089) and (-0.916pm0.078). In BAO-only (w_0w_a)CDM it gives (Omega_{m,0}=0.35310^{+0.04189}_{-0.01740}), (w_0=-0.47034^{+0.34357}_{-0.16945}), and the 68% upper limit (w_a<-1.3456), compared with DESI's (0.352^{+0.041}_{-0.018}), (w_0=-0.48^{+0.35}_{-0.17}), and (w_a<-1.34). This agreement is the principal validation that the independent likelihood lane is sampling the intended DESI BAO posterior geometry.

The numerical (Lambda)CDM identity control evaluates (q(z)=0) and (chi_delta(z)=1) independently with root finding across 257 values of (Omega_{m,0}). The maximum absolute difference between the two roots is (5.33	imes10^{-15}), so the positive control passes by a wide margin.

## Stability results and the first Limit-Map finding

For (Lambda)CDM, the posterior transition is (z_{q=0}=z_{chi_delta=1}) with the 16th, 50th, and 84th percentiles approximately ([0.6542,,0.6773,,0.7004]); therefore (Delta z=0) exactly under the model assumptions. For constant-(w)CDM, the corresponding posterior summaries are (z_{q=0}approx[0.6440,,0.6716,,0.6971]), (z_{chi_delta=1}approx[0.6769,,0.7583,,0.8621]), and (Delta zapprox[-0.1940,,-0.0852,,-0.0041]). The correlation between (Delta z) and (w) in the posterior resample is approximately (-0.97), showing that this scalar offset is primarily a re-expression of the equation-of-state departure within the assumed background model rather than independent evidence for new physics.

The BAO-only (w_0w_a) posterior exposes a more important structural issue. Approximately 39.3% of posterior resamples have one (q(z)=0) crossing on (0leq zleq5), while approximately 60.7% have two. By contrast, (chi_delta(z)=1) has a single crossing in approximately 99.97% of the same resamples. The one-(q)-crossing branch is accelerating at (z=0), with median (z_{q=0}approx0.738), median (z_{chi_delta=1}approx0.690), and median (Delta zapprox+0.056). The two-(q)-crossing branch is decelerating again at (z=0): its most recent crossing has median (z_{q=0}^{mathrm{recent}}approx0.132), its earlier crossing has median (z_{q=0}^{mathrm{earlier}}approx0.852), and its median (z_{chi_delta=1}approx0.663). Relative to the unique (chi_delta=1) crossing, the recent branch gives median (Delta zapprox-0.525), whereas the earlier (q=0) branch lies about (+0.199) in redshift above the (chi_delta=1) crossing.

This is a representation failure of a single unlabeled (Delta z), not a failure of the data or the root calculation. Once (q(z)) has more than one crossing, the expression (z_{q=0}) is no longer a unique event unless a branch rule is supplied, and different branches represent physically different transitions. The live analysis therefore preserves the crossing sets rather than compressing them prematurely. A useful provisional representation is
[
mathcal Z_q={zgeq0:q(z)=0},qquad
mathcal Z_{chi_delta}={zgeq0:chi_delta(z)=1}.
]
The scalar (Delta z) remains unambiguous without an additional branch label only when the relevant transition set is unique.

## Consequence for (chi_delta), the Stability Arc, and SI

For a flat GR cosmology containing pressureless matter and a smooth dark-energy component with equation of state (w(a)),
[
Omega_m(a)=rac{2}{3chi_delta^2(a)}
]
and
[
q(a)=rac12left[1+3w(a)left(1-rac{2}{3chi_delta^2(a)}ight)ight].
]
For (w=-1), this reduces to
[
q(a)=chi_delta^{-2}(a)-1,
]
which explains the exact (Lambda)CDM transition identity. More generally, (q(a)) and (chi_delta(a)) are not independent observables once the native cosmological model is specified. A Stability Arc built only from these two background quantities can be a useful representation of the background history, but it cannot by itself establish new dynamics, SI, or an independent capital-(Chi) degree of freedom.

This narrows the next empirical target rather than closing it. A genuinely additional cosmological architecture must introduce information from the matter-growth sector, such as (D(k,a)), (f(k,a)), (fsigma_8(a)), (P(k,a)), or other native growth observables, and test their relationship to the background trajectory. The DESI DR1 full-shape products therefore become the next natural data lane for (Chi_{mathrm m}), while the DR2 BAO lane constrains (Chi_{mathrm{bg}}). Any SI claim remains behind the requirement that the joint background-growth construction predict or organize information beyond the native GR/Friedmann/growth equations.

The official DR2 Cobaya-chain replay remains pending as an independent reproduction cross-check. No result in this record is interpreted as evidence for SI, DM-DE interaction, modified gravity, or dynamical dark energy by itself.
