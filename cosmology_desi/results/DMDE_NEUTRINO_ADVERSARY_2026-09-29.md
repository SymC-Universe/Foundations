# DESI DR1 Neutrino-Mass Adversarial Suite

## DESI FS+BAO+CMB: fixed versus free neutrino mass

- free sum mnu 95% upper = 0.070701 eV
- free sum mnu median = 0.020827 eV
- P(sum mnu > 0.06 eV) = 0.08832
- omegam: fixed 0.30555 [0.30069, 0.31058] -> free 0.30264 [0.29761, 0.30786]; shift -0.583 fixed-sigma
- sigma8: fixed 0.81203 [0.8068, 0.81737] -> free 0.81938 [0.81279, 0.82532]; shift 1.383 fixed-sigma
- H0: fixed 68.068 [67.689, 68.444] -> free 68.345 [67.937, 68.743]; shift 0.726 fixed-sigma
- S8_standard: fixed 0.81957 [0.81064, 0.82862] -> free 0.82275 [0.8136, 0.8318]; shift 0.353 fixed-sigma

## Pantheon+: w0wa fixed-mnu versus free-mnu

- sum mnu 95% upper = 0.17266 eV
- w0: -0.85913 [-0.91894, -0.79784] -> -0.85781 [-0.92088, -0.79386]; shift 0.022 fixed-sigma
- wa: -0.67064 [-0.93366, -0.42791] -> -0.67614 [-0.9817, -0.39848]; shift -0.022 fixed-sigma
- free-mnu P(w0>-1, wa<0) = 0.98871

## Union3: w0wa fixed-mnu versus free-mnu

- sum mnu 95% upper = 0.19685 eV
- w0: -0.74386 [-0.839, -0.64774] -> -0.73507 [-0.83542, -0.62852]; shift 0.091 fixed-sigma
- wa: -1.0066 [-1.3597, -0.67155] -> -1.0596 [-1.509, -0.67209]; shift -0.154 fixed-sigma
- free-mnu P(w0>-1, wa<0) = 0.99492

## DESY5: w0wa fixed-mnu versus free-mnu

- sum mnu 95% upper = 0.19371 eV
- w0: -0.76244 [-0.82567, -0.69621] -> -0.75496 [-0.82406, -0.68504]; shift 0.115 fixed-sigma
- wa: -0.95101 [-1.2402, -0.68243] -> -0.99708 [-1.3463, -0.68039]; shift -0.164 fixed-sigma
- free-mnu P(w0>-1, wa<0) = 0.99982

## Guardrails

- The CMB neutrino gate is DESI FS+BAO+CMB, not a DESI-only neutrino constraint.
- Free-mnu chains use the DESI release prior mnu > 0 and three degenerate mass eigenstates.
- The w0-wa robustness test compares each free-mnu chain only to the same SN sample with fixed mnu.
- Posterior mass above thresholds is descriptive and is not a frequentist significance.