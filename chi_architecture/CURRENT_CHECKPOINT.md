# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02A-CP4-CLOSED  
**Date:** 2026-09-22  
**Branch:** `chi-architecture-p0`  
**Protocol:** SymC GOM v0.8.3

## D02A closure

D02A is closed as a P0-D physical calibration.

Official lineage:

1. CP0 physical scientific freeze: `27164b36a0c3ecd1931cfe8cdf840f6fc7b9fbb6`
2. CP1 source-schema lock: `c1e7d8c5814e872a7d1f88f210af473cbdf1e631`
3. v0.1 prospective execution: preserved partial failure
4. v0.1 partial archive: `d5af53320608be627b8edfcc3dfc2eb778986310`
5. v0.2 layout diagnostic / post-result parser repair
6. v0.2 corrected execution: workflow `35816379440`
7. v0.2 execution archive: `c83f2136e7b633f6a4172b79941c136dbccad3de`
8. scientific readout: `d02_cspbbr3/D02A_PHYSICAL_CALIBRATION_READOUT_v0.2.md`

## Official D02A scientific state

`CARRIER_CORRESPONDENCE_PERSISTS / LOCAL_DAMPING_TRANSFORMS / DISTRIBUTED_SHAPE_REORGANIZES / SCALAR_CHI_REFUSED`

Native comparator verdict:

`NATIVE_PHONON_TOOLKIT_SUFFICIENT`

Lowercase chi remains refused because same-condition natural frequency `omega0` is not tabulated in the locked source data and no reverse fit was licensed.

D02A does not establish a new phonon law, a master Chi scalar, untouched confirmation, or recovery/resilience.

## Reproduction

Reviewer command:

`python chi_architecture/reproduce.py d02a`

Guide:

`chi_architecture/REPRODUCIBILITY_GUIDE.md`

Permanent archive:

`chi_architecture/results/D02A_EXECUTION_ARCHIVE_v0.2.json`

## Next experiment requirements learned from D02A

The next physical system should be selected before decisive outcome inspection and should ideally contain:

1. same-condition natural frequency and damping/linewidth so lowercase chi admission can be tested directly;
2. independently defined modal/carrier/coupling organization;
3. a controlled substrate, coupling, temperature, pressure, or environmental change;
4. a perturbation, recovery, or future/held-out consequence where available;
5. a strong native comparator;
6. an explicit prospective failure state.

## Resume rule

Do not reopen D02A merely to fit omega0 from the plotting curves.

A D02A extension would require a new pre-fit contract and remains calibration evidence.

The active next task is to identify and freeze D02B, a stronger physical test with directly licensed same-condition scalar inputs.
