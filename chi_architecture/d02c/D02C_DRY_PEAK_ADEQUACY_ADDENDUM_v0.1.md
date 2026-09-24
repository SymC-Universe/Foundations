# D02C Dry-Run Peak Adequacy Addendum v0.1

**Date:** 2026-09-23  
**Status:** PREEXECUTION  
**Parent:** D02C_WIND_EXACT_MAPPING_v0.1.md

For the dry-run thermal organization control, a candidate local PSD peak in 0.5-4.0 Hz is eligible only when:

- it is a strict local maximum;
- its PSD height is at least 5 times the median spatially averaged PSD within 0.5-4.0 Hz in that same window;
- an eligible peak is present in both of the first two dry-run ten-minute windows within +/-0.1 Hz.

The lowest common eligible peak is selected.

If no peak meets this rule, the dry-run organization sensitivity control is NON_IDENTIFIABLE and D02C cannot assign a favorable CA-D007 ordering.

This threshold is a signal-identification guard, not a physical stability boundary.
