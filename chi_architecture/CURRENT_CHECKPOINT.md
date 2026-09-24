# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02E-CP3-BASELINE-SELECTION-IMPLEMENTED  
**Date:** 2026-09-23  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.6

STATUS

D02E MFR-14 remains frozen. Baseline-only target-mode selection is implemented.

CURRENT GATE

Run the baseline selector on the 20 Healthy A_1 original CSV files only.

NEXT ACTION

Execute .github/workflows/chi-architecture-d02e-baseline.yml.

WHY

The primary modal family must be frozen without leakage from any damaged vibration record.

ACTIVE EXECUTION

The selector:
- queries the DOI-locked Dataverse metadata;
- downloads only DATA/A_1/Healthy original CSV files;
- validates source MD5 values;
- constructs 24-channel FDD spectra;
- applies the frozen >=16/20 scalar-admission rule;
- selects the lowest qualifying healthy family.

USER ACTION

NONE.

SUCCESS CONDITION

PRIMARY_MODE_SELECTED and a frozen primary family with >=16/20 admitted healthy chi estimates.

FAILURE BRANCH

NO_ADMISSIBLE_PRIMARY_MODE. No damaged CSV is opened and D02E closes without a prospective ordering test.
