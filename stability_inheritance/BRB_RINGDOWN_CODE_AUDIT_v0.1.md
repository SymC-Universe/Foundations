# Brake-Reuss Beam Ringdown Source-Code Audit v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Source:** mattiacenedese/BRBtesting showData.mlx
**Frozen commit:** 2d42d3a618206da58642674d3287ae34dfc7d5e5
**Status:** SOURCE-CODE SEMANTICS AUDIT ONLY
**Response data access:** PROHIBITED

## Purpose

Recover the repository authors' declared shaker-ringdown plotting/preprocessing conventions, especially the after-release time window and DIC field semantics, before any numerical BRB response is scored.

## Allowed

- download showData.mlx only;
- verify frozen blob identity;
- extract matlab/document.xml;
- return only CDATA code blocks containing ShakerRingdown.mat;
- preserve numeric constants exactly because they are source-code configuration, not measured outcomes.

## Prohibited

- download MAT response files;
- execute the MATLAB code;
- inspect embedded figure/output images;
- choose a time window from measured response values;
- score modal or DIC behavior.

## Disposition

- BRB_RINGDOWN_CODE_QUALIFIED if both accelerometer and DIC ShakerRingdown code blocks are recovered.
- BRB_RINGDOWN_CODE_INCOMPLETE otherwise.
