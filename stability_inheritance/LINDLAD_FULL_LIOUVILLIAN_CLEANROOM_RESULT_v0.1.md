# Lindblad Full-Liouvillian Clean-Room Result v0.1

**Date:** 2026-10-01  
**Task:** `LINDLAD_FULL_LIOUVILLIAN_CLEANROOM_V01`  
**Workflow run:** 36864049059  
**Frozen source commit:** `d2c0037a5b2f40f0c15869d33f68315fcda725da`  
**Result SHA-256:** `c46acb420ec83d50c3c896cde7a953ae59d894d7c650ea9fc6e476c814471cff`  
**Artifact digest:** `sha256:ad4a90107b0c242a0e99ed25ebfc2d748000a8264a51e79b40973b8af5f1a18f`  
**Status:** COMPLETE / POSITIVE CLEAN-ROOM DEFECTIVENESS CHECK / SOURCE-CONVENTION MATCH STILL REQUIRED

The clean-room model used the declared driven pure-dephasing convention

[
dotho=-i[Omegasigma_x/2,ho]
+rac{Gamma_phi}{2}(sigma_zhosigma_z-ho).
]

This convention damps the Bloch (x,y) components at (Gamma_phi) and gives the (y,z) block

[
egin{pmatrix}
-Gamma_phi & -Omega\\
Omega & 0
end{pmatrix}.
]

At (Omega=1), (Gamma_phi=2Omega=2):

- the reduced Bloch target eigenvalue (-1) has algebraic multiplicity 2 and geometric multiplicity 1;
- the full (4	imes4) Liouvillian target eigenvalue (-1) also has algebraic multiplicity 2 and geometric multiplicity 1;
- the remaining full-Liouvillian eigenvalues are numerically (0) and (-2), with roundoff-scale splitting of the repeated (-1) pair in direct eigensolver output.

**Clean-room result:** under this master-equation convention, the EP is not merely an artifact of reducing to the Bloch (y,z) block; the full Liouvillian is defective at the same parameter boundary.

**Ceiling:** before the source-locked evidence ledger is upgraded from "full-Liouvillian comparison required" to a manuscript-level full-Liouvillian claim, the exact Lindblad-v4 normalization/convention must be matched to this clean-room convention. No universal (chi=1) optimality or cross-domain inheritance conclusion follows.
