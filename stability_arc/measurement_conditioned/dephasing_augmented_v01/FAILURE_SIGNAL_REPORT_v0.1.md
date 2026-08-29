# Dephasing-augmented planar transfer v0.1 failure-signal report

Canonical run: `33267651929`
Execution commit: `a70d52eefad4f1a7fade43eda8833297f900fa58`
Artifact: `9719129878`
Artifact ZIP SHA-256: `91b50a529d77edcb47ecbac908f9d824b376b9d8399891fb2a116f2a0f312936`

Classification: `AUDIT_IMPLEMENTATION_FAILURE / VARIABLE_NAME_COLLISION`

## Preserved observed result

The v0.1 workflow completed successfully as a GitHub Actions job but emitted phase status `DEPHASING_AUGMENTED_TRANSFER_FAILURE` because criterion D3 was reported FAIL.

D0, D1, D2, D4, D5, D6, and D7 all reported PASS.

D5 contained 256/256 fresh successful dephasing-augmented transfer fixtures with zero structural failures, maximum canonical-matrix error `8.881784197001252e-16`, maximum invariant-coefficient error `1.8818280267396403e-14`, and maximum second-moment intertwining error `1.7763568394002505e-15`.

Both exact shifted-boundary controls returned `REFUSE_QUOTIENT_DIMENSION`. The generic out-of-plane control returned `REFUSE_NO_1D_DARK_FACTOR`.

## Exact implementation defect

The source first assigns the symbolic canonical-map predicate to the Python name `D3`:

`D3=all(...)`

Later, the generic out-of-plane refusal control reuses the same name for the returned dark-space array:

`_,s3,D3,rank3=dark_space(A3,V3)`.

The intended refusal has dark dimension zero, so this second `D3` is an empty NumPy array. The final expression

`all([D0,D1,D2,D3,D4,D5,D6,D7])`

therefore evaluates the overwritten empty array rather than the earlier symbolic D3 boolean. The run log emitted NumPy DeprecationWarnings about the ambiguous truth value of an empty array at both the overall-status line and the D3 report line.

Thus the stored v0.1 D3 FAIL is not an interpretable scientific or symbolic contradiction. It is an audit-reporting defect caused by identifier reuse.

## What remains valid

The v0.1 run remains permanently preserved and is not rewritten to PASS.

Its independently executed D0/D1/D2/D4/D5/D6/D7 evidence remains part of the lineage. In particular, the fresh D5 numerical transfer and both refusal classes are not invalidated by this reporting collision.

## Smallest permitted remediation

Create a separate v0.1.1 audit that recomputes only the already-frozen symbolic D3 canonical quotient identity using distinct variable names. It must not change any scientific formula, parameter map, fixture, threshold, or interpretation.

Only if that independent D3 remediation passes may the dephasing transfer be described as composite-closed by explicitly citing both the permanent v0.1 audit-implementation failure and the v0.1.1 remediation.
