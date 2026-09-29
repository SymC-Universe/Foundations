# F-16 SpecialOdd Layout Preflight Mechanical Repair 2026-09-28

**Governance:** SymC GOM v1.0
**Affected protocol:** F16_GVT_SPECIALODD_LAYOUT_PREFLIGHT_v0.1.md
**Failed workflow:** 36513019102
**Failure class:** MECHANICAL / EPHEMERAL-WORKSPACE DEPENDENCY
**Scientific result produced:** NO

## Failure

The preflight stopped before source access because it required a local file:

stability_inheritance/results/f16_gvt_intake/manifest.json

That manifest was produced in a preceding GitHub Actions run and was therefore not present in the fresh runner workspace.

## Repair

Replace the local-manifest dependency with direct verification of the exact source identity already established by the successful F-16 intake:

- official 4TU URL unchanged;
- required byte count = 148,455,295;
- required SHA-256 = 2278429b1f15f15448e6f101d395a5587d58ac23d32052fd42f8b33a894c0afa.

The repaired preflight reacquires the archive, verifies those two frozen identity values, and then performs the same metadata/shape-only SpecialOdd inspection.

## Scientific invariance

Unchanged:
- three published SpecialOdd excitation levels;
- 10-realization / 3-period / 16,384-sample acquisition expectation;
- no signal values scored;
- no FFT/model fitting;
- no output-driven mapping;
- disposition definitions.

The failed run remains preserved as a mechanical failure and is not overwritten.
