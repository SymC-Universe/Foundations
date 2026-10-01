# DESI DR1 Matched Dark-Energy Best-Fit Comparison

Released iminuit minima; flat LambdaCDM versus flat CPL w0waCDM using identical data in each pair.

## Pantheon+

- Delta chi2 (w0wa - LambdaCDM) = -8.2629
- chi2 improvement = 8.2629 for 2 additional parameters
- w0 best fit = -0.83858
- wa best fit = -0.69449
- asymptotic 2-dof Wilks p = 0.0160596
- two-sided normal-equivalent diagnostic = 2.408 sigma
- component delta chi2 = {'chi2__DESI_FS_BAO': -3.4348600000000147, 'chi2__CMB': -2.815900000000056, 'chi2__SN': -1.7294999999999163}

## Union3

- Delta chi2 (w0wa - LambdaCDM) = -14.3983
- chi2 improvement = 14.3983 for 2 additional parameters
- w0 best fit = -0.66457
- wa best fit = -1.19776
- asymptotic 2-dof Wilks p = 0.000747221
- two-sided normal-equivalent diagnostic = 3.372 sigma
- component delta chi2 = {'chi2__DESI_FS_BAO': -5.453850000000045, 'chi2__CMB': -3.0003999999998996, 'chi2__SN': -5.956721999999999}

## DESY5

- Delta chi2 (w0wa - LambdaCDM) = -17.6711
- chi2 improvement = 17.6711 for 2 additional parameters
- w0 best fit = -0.73789
- wa best fit = -1.00487
- asymptotic 2-dof Wilks p = 0.000145469
- two-sided normal-equivalent diagnostic = 3.799 sigma
- component delta chi2 = {'chi2__DESI_FS_BAO': -6.379329999999982, 'chi2__CMB': -2.1842000000001462, 'chi2__SN': -9.073300000000017}

## Guardrails

- Each comparison uses the same DESI FS+BAO+CMB+SN dataset combination.
- Delta chi-square uses released iminuit posterior-maximization products, not minima sampled from MCMC chains.
- The Wilks diagnostic is asymptotic and descriptive; DESI's published inference remains the authoritative significance statement.