# pyFBS SVT API Compatibility Preflight v0.2

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** FROZEN POST-FAILURE P0-Q SOFTWARE/DATA COMPATIBILITY PREFLIGHT
**Predecessor:** PYFBS_LAB_SVT_DECOUPLING_PROTOCOL_v0.1.md -> execution failure before scoring
**Target Y_A scoring:** PROHIBITED
**P1 status:** INELIGIBLE

## Purpose

Determine whether the official measured SVT transformation route for the pyFBS academic testbench is executable under released pyFBS 1.0.x versions without inspecting or scoring the independently measured A target.

The v0.1 decoupling protocol is preserved unchanged. This preflight is a new post-result software-compatibility object and cannot retroactively rescue that execution.

## Frozen source identities

Use only:
- Y_B.p SHA-256 2e4a83f4ce1b87e773c5872764c4e4bd11f71b256a11964ac7574a81feeeed12
- Y_AB.p SHA-256 197deff3bc1f546bc1653ecb877d34dece01dfc1d360217dc903f4d1a694d4d7
- decoupling_example.xlsx SHA-256 20d246430c163c5abd935d71f36a65b470fd3b0fff6243a81d1e2cc0099a04a9

Do not download Y_A.p in this preflight.

## Frozen package versions

Test exactly:
- pyFBS 1.0.0
- pyFBS 1.0.4
- pyFBS 1.0.5
- pyFBS 1.0.6

Each version is tested independently under Python 3.12.

## Frozen operation

For each version:

1. load Y_B and Y_AB using the documented response x input x frequency -> frequency x response x input transpose;
2. load Channels_B / Impacts_B and Channels_AB / Impacts_AB from decoupling_example.xlsx;
3. instantiate SVT using the documented named arguments:
   - grouping_no = [1, 10]
   - no_svs = 6
   - basis estimated only from B;
4. apply the same SVT object to B and AB using the public apply_svt/apply_SVT method available in that release;
5. record only:
   - constructor success/failure;
   - apply-to-B success/failure;
   - apply-to-AB success/failure;
   - transformed shapes;
   - finite-value status;
   - exception class/message.

No LM-FBS decoupling or comparison with A is allowed.

## Frozen dispositions

Per version:
- SVT_ROUTE_EXECUTABLE if both B and AB transform successfully, outputs are finite, B transformed dimensions are 6x6 per frequency, and AB transformed dimensions are 12x12 per frequency.
- SVT_ROUTE_NOT_EXECUTABLE otherwise.
- INVALID_TEST only for source hash/frequency/metadata identity failure.

Cross-version:
- COMPATIBLE_RELEASE_FOUND if at least one frozen release is SVT_ROUTE_EXECUTABLE.
- RELEASE_COMPATIBILITY_NOT_FOUND if none are executable.
- INVALID_TEST if source identity fails.

## Consequence

If COMPATIBLE_RELEASE_FOUND:
- select the newest executable frozen version;
- freeze a new v0.2 measured SVT decoupling scoring protocol using that version before downloading/scoring Y_A;
- preserve all v0.1 failure provenance.

If RELEASE_COMPATIBILITY_NOT_FOUND:
- stop the SVT scoring path and classify the current released-software route as not operational for this benchmark under the tested official example configuration;
- do not tune grouping, k, metadata, or target extraction against Y_A.

This preflight is software/data-interface qualification only.
