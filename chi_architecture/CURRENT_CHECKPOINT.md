# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02A-CP1.5-IMPLEMENTED-PREOUTPUT  
**Date:** 2026-09-22  
**Branch:** `chi-architecture-p0`  
**CP0 scientific freeze:** `27164b36a0c3ecd1931cfe8cdf840f6fc7b9fbb6`  
**CP1 source-schema lock:** `c1e7d8c5814e872a7d1f88f210af473cbdf1e631`  
**Protocol:** SymC GOM v0.8.3

## Scientific surface remains frozen

The parser and execution metrics are now implemented under:

- `d02_cspbbr3/D02A_EXECUTION_CONTRACT_v0.1.json`
- `src/d02a_physical.py`
- `tests/test_d02a_physical.py`

Reviewer entrypoint:

`python chi_architecture/reproduce.py d02a`

## Pre-output DHO decision

Lowercase chi remains refused before value execution:

`OMEGA0_NOT_IDENTIFIABLE_FROM_LOCKED_SOURCE_TABLES`

The source table identifies DHO-derived linewidths, but the locked publisher tables do not tabulate same-condition natural frequency omega0. Published fit curves are retained as source curves and are not inverted for parameters.

## Physical carrier correspondence

The M-R path correspondence is frozen independently of source values:

- 300 K orthorhombic, SPINS M-R;
- 385 K tetragonal, SPINS M-R;
- 419 K cubic, CNCS M-R segment.

## Resume rule

1. Execute the dedicated D02A workflow.
2. If failure is mechanical, repair code/transport only.
3. Do not alter source hashes, parser ranges, phase bins, or DHO license in response to values.
4. Archive run ID, artifact ID/digest, result hash, manifest hash, and exact numeric output as D02A-CP2 before interpretation.
5. Only after CP2 assess joint local-linewidth / broader-carrier inheritance, transformation, reorganization, or native-toolkit sufficiency.
