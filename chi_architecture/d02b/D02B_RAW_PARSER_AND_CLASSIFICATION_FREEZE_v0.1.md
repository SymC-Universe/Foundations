# D02B Raw Parser and Outcome Classification Freeze v0.1

**Date:** 2026-09-23  
**Status:** FROZEN_BEFORE_FRF_MEMBER_CONTENT_INSPECTION  
**Authority:** SymC GOM v0.8.3  
**Parent mapping:** D02B_EXACT_SOURCE_MAPPING_v0.1.md

## Raw archive provenance

Successful manifest run: 35822278161  
Artifact: d02b-raw-archive-manifest-v01  
Artifact ID: 10732894919  
Artifact digest: sha256:5602ac9a83cbe1ee3aa59d76ca6140f27e8b5fc95ddc5b4660014a9dcc0f5f63  
Raw archive MD5: 68450ff0f1c25492ee243b8adba29991  
Raw archive SHA-256: 2e6ece8670ab2201d2a8cdf38e31cc2b979062d0c7eaf93da152e1e27b6ffb89

Archive structure:
- 919 amplitude response files;
- 919 phase response files;
- one README metadata member;
- 1,839 total non-directory members.

## Frozen case-name parser

Raw response members follow:

00_raw_exports/00_raw_exports/{Amplitude|Phase}/{case_name}_6mmSchraub_{point}.txt

Some low-number point IDs use a double underscore before the point token.

Parsing rule:

1. strip directory and .txt;
2. split once on literal "_6mmSchraub";
3. left side is case_name;
4. strip all leading underscores from the suffix;
5. remaining integer token is scan-point ID.

Do not infer case identity from response values.

## Frozen common-point rule

Across all 18 torque states, the exact intersection contains 51 point IDs:

1, 4, 6, 7, 8, 9, 12, 13, 16, 21, 24, 25, 26, 27, 28, 29, 30, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 60, 63, 66, 67, 70, 76, 77, 78, 79.

The all-loose state contains one additional amplitude/phase point ID 20.

D02B uses only the 51-point intersection for every torque state.

The extra all-loose point is excluded to preserve matched spatial support.

## Frozen response-file count guards

Expected after common-point filtering:

18 cases x 51 points = 918 amplitude files used;
18 cases x 51 points = 918 phase files used.

Two raw response members corresponding to the all-loose extra point 20 remain unused.

## Frozen scalar condition labels

For each family/state:

- ADMITTED: both half-power crossings found, positive bandwidth, non-boundary peak, no competitor violation.
- HALF_POWER_CROSSING_NOT_OBSERVED: either crossing absent inside frozen source window.
- NON_IDENTIFIABLE_MODAL_OVERLAP: competitor local maximum >= 0.90 x selected peak and separated by >=2 bins.
- WINDOW_TRUNCATED: selected peak is on a frozen tracking-window boundary.
- NO_ADMISSIBLE_SCALAR_CHI: other fail-closed scalar failure.

## Frozen pairwise chi relation

For two admitted conditions a,b:

resolution_a = 1/(2 f_peak_a)
resolution_b = 1/(2 f_peak_b)

similar_chi iff:

abs(chi_a-chi_b) <= max(resolution_a,resolution_b).

If not similar, the pair is CHI_TRANSFORMED_AT_FROZEN_RESOLUTION.

No percentage tolerance is allowed.

## Frozen embedded-response reorganization rule

For a primary single-bolt-loose comparison against all-tight, embedded response is classed as RESPONSE_REORGANIZED when either:

1. absolute tracked-frequency shift >= 1 Hz, or
2. any source-native spatial dissimilarity value (1-MACa, 1-CMAC, 1-CMAC_phaseonly) is strictly greater than 1e-12.

This is a descriptive detection rule, not a statistical materiality threshold.

Exact native values remain reported so readers can judge magnitude.

## Frozen family-level descriptive labels

For each retained resonance family:

### PRESERVED

All four single-bolt-loose states admit chi and are similar to all-tight under the frozen resolution rule, and no primary comparison is RESPONSE_REORGANIZED.

### LOCAL_SCALAR_VALID_BUT_EMBEDDED_INSUFFICIENT

All-tight and at least one single-bolt-loose state admit similar chi under the frozen resolution rule, while that same comparison is RESPONSE_REORGANIZED.

This label states insufficiency for the declared embedded-response question only. It does not invalidate the local chi.

### TRANSFORMED

At least one primary comparison has admitted chi in both conditions and is CHI_TRANSFORMED_AT_FROZEN_RESOLUTION.

TRANSFORMED may coexist with REORGANIZED.

### REORGANIZED

At least one primary comparison is RESPONSE_REORGANIZED.

### NO_ADMISSIBLE_SCALAR_CHI

All-tight is refused, or no primary single-bolt comparison has admitted chi in both states.

### NON_IDENTIFIABLE

Mode tracking/parser/source mapping fails independently of the half-power refusal labels.

### NO_RELATION_DETECTED

Chi is preserved within frozen resolution and no embedded reorganization is detected in any primary comparison.

### CONTRADICTS_INHERITANCE_HYPOTHESIS

Reserved for the stronger case in which the predeclared inheritance relation predicts preservation/transformation linked to substrate organization but the controlled interface variation produces no reproducible scalar or embedded response relation across the retained primary map.

D02B v0.3 does not force this label merely because one family is null.

## Added-value verdict rule

D02B reports:

NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE

if standard FRF peak tracking + half-power damping + torque state + MAC/CMAC/phase metrics fully express every reported result without requiring an additional fitted SymC quantity.

Otherwise:

INCREMENTAL_VALUE_UNRESOLVED

No positive incremental-value verdict is authorized in D02B.

## Dose-response rule

The 10/5/0 Nm single-bolt sequences are secondary.

For each bolt/family/metric, report the ordered values at 10,5,0 Nm.

Do not require monotonicity to retain the primary result.

A monotonic trend may be described only when the three values are ordered consistently in torque; no fitted dose-response curve is required in v0.3.
