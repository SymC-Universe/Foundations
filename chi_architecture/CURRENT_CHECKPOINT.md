# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02D-CP5-HEALTHY-METADATA-IMPLEMENTED  
**Date:** 2026-09-23  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.4

## Healthy struct schema

Run:
35902420791

Artifact:
d02d-lumo-healthy-struct-schema-v01

Artifact ID:
10770235039

Artifact digest:
sha256:4a7a8f8fe43e14ac18bfb1a7ab2c60eca8e0fc146ace142625a6b80acb9178c4

The source Dat struct contains:
- Data: 990600 x 22 float32;
- ChannelNames: 22 entries;
- ChannelUnits: 22 entries;
- Fs scalar;
- Time metadata;
- Timestamps metadata.

Acceleration channels:
accel01x/y through accel09x/y.

Additional channels:
strain01, strain02, strain03, temp01.

## Active action

Verify the numeric sampling-rate metadata from the same first healthy record only.

No scientific array values and no damaged MAT values are emitted.

## Next gate

Freeze the final D02D production analysis after sampling rate is verified.
