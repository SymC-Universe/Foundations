# pyFBS Current Official SVT Notebook Audit Result v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Workflow run:** 36516063337
**Status:** CURRENT_NOTEBOOK_ROUTE_IDENTIFIED
**Target data downloaded:** NO

## Current official notebook identity

Source:
https://gitlab.com/pyFBS/pyFBS/-/raw/master/examples/09_FBS_decoupling_SVT.ipynb

- bytes: 146,858
- SHA-256: c19d6418c82c2d591ffaab38d0982dbd2920a0ad51408c3aff9681ad8b16bee6

## Material correction found

The current maintained notebook uses:

`./lab_testbench/Measurements/decoupling_example_SVT.xlsx`

for Sensors/Channels/Impacts of A, B, and AB.

The prior failed Stability Inheritance protocols used the older/general `decoupling_example.xlsx` metadata object.

The current notebook retains the same core scientific/native route:

- k = 6
- SVT basis extracted from B
- grouping [1,10]
- apply the same SVT to B and AB
- construct an 18 x 18 decoupling block
- extract recovered A at reduced indices 6:12

## Interpretation

This is an independently documented upstream route change and therefore licenses a new **pre-target compatibility preflight** using `decoupling_example_SVT.xlsx`.

It does not erase the previous failures. Those failures remain valid for the stale metadata route that was actually tested.

No Y_A target was downloaded or scored during this audit.
