# pyFBS SVT API Compatibility Preflight Result v0.2

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Protocol:** stability_inheritance/PYFBS_SVT_API_COMPATIBILITY_PREFLIGHT_v0.2.md
**Workflow run:** 36512302527
**Status:** RELEASE_COMPATIBILITY_NOT_FOUND
**Target Y_A scoring:** NOT PERFORMED
**Empirical Stability Inheritance claim:** NONE

## Result

The frozen preflight tested pyFBS releases 1.0.0, 1.0.4, 1.0.5, and 1.0.6 against the official measured B and AB FRFs plus decoupling_example.xlsx metadata.

Across all four requested releases:

- SVT construction from B completed;
- applying the SVT to B completed and returned a finite 801 x 18 x 18 transformed object;
- applying the same SVT to AB failed before target scoring with IndexError: index 9 is out of bounds for axis 2 with size 9;
- no release produced the documented B 6 x 6 and AB 12 x 12 route required by the frozen decoupling protocol.

The runtime package reports an internal version string of 1.0.0 for the tested 1.0.x wheels, so the requested package version is the authoritative compatibility coordinate recorded by the preflight.

## Disposition

**RELEASE_COMPATIBILITY_NOT_FOUND**

This closes the current measured SVT route under the frozen official-example configuration.

It does not establish failure of SVT as a method. The official documentation describes the route, but the present released package/data combination did not reproduce it under the frozen test.

## GOM consequence

- preserve PYFBS_LAB_SVT_DECOUPLING_PROTOCOL_v0.1.md and its pre-score execution failure;
- preserve this cross-release compatibility refusal;
- do not tune k, grouping numbers, metadata, coordinate extraction, or target reference against Y_A;
- do not spend additional runway searching package versions unless an independently documented correction or upstream compatibility fix appears;
- continue other external measured qualification lanes.

## Architecture role

This is a **method-operability Limit Map** result. It contributes evidence about the practical limits of an otherwise valid native substructuring route in the currently available software/data package, but it carries no negative inference about the physical architecture and no inheritance claim.
