# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02B-CP7-RAW-MANIFEST-IMPLEMENTED  
**Date:** 2026-09-22  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.3

## Processed snapshot

Run: 35819505039  
Artifact: d02b-processed-snapshot-v01  
Artifact ID: 10732403880  
Digest: sha256:888106929cbac43437e53643b7dcf38c96951da68dfbd589a020f05dcf4ad0ce

Retained source families:
3325, 4703, 7034, 7861, 8163, 8428, 8695 Hz.

These identifiers are source-defined, not D02B-selected.

## Raw acquisition state

A path-only raw archive acquisition workflow is implemented.

It downloads and verifies 00_raw_exports.zip, then reads only ZIP directory metadata.

No FRF member contents are opened at this checkpoint.

## Resume rule

After the raw path manifest succeeds:
1. freeze exact case/file-name parsing from the manifest;
2. verify there are 919 amplitude + 919 phase files;
3. map the five primary torque states by case_name;
4. commit the parser and one-command D02B implementation;
5. only then read raw FRF values.
