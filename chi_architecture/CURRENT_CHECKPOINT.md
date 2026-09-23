# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02C-CP2-HEADER-LOCK-IMPLEMENTED  
**Date:** 2026-09-23  
**Branch:** chi-architecture-p0  
**Protocol:** SymC GOM v0.8.3  
**Parent contract:** D02C_WIND_BLADE_CONTRACT_v0.1.md

## Unit convention

The OWI-lab LSCF/OMA convention is damping in percent.

D02C therefore uses:

chi = zeta = mean_damping / 100

and:

SE_chi = (std_damping / sqrt(size)) / 100.

This convention is locked before decisive damping values are inspected.

## Current action

A header-only workflow is reading exactly one raw acceleration CSV header from the intervention archive.

It emits no acceleration values.

After success:
1. freeze exact X/Z sensor columns;
2. correct the dry-run checksum wording in the source contract;
3. implement D02C and tests;
4. commit before numeric execution.
