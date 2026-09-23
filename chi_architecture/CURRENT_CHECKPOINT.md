# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02B-CP6-PROCESSED-SNAPSHOT-IMPLEMENTED  
**Date:** 2026-09-22  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.3

## State

The processed-value extraction is implemented only after CP5 froze the exact mapping and scalar algorithm.

This workflow reads:
- torque_states.csv;
- retained rows from resonance_group_selection_audit.csv;
- adaptive_tracking_windows.csv;
- tracked_frequencies.csv;
- per_case_metrics.csv;
- dose_response.csv.

It explicitly does not download or open the raw FRF archive.

## Resume rule

1. Archive the successful processed snapshot with run/artifact/digest.
2. Record retained family IDs and exact torque case names.
3. Do not change CP5 mappings.
4. Implement raw archive acquisition and half-power extraction.
5. Commit that implementation before raw FRF execution.
