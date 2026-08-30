from __future__ import annotations

import json
from pathlib import Path

import numpy as np


SCOPE = "synthetic_nonnormal_biorthogonal_validation_only"


def sorted_biorthogonal_eigensystem(generator: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return eigenvalues, right eigenvectors V, and left rows W^H with W^H V = I.

    The routine is restricted to diagonalizable matrices. Conditioning is reported
    separately and must be used to refuse or qualify comparisons near defectiveness.
    """
    a = np.asarray(generator, dtype=complex)
    values, right = np.linalg.eig(a)
    order = np.lexsort((np.imag(values), np.real(values)))
    values = values[order]
    right = right[:, order]
    if np.linalg.matrix_rank(right) < right.shape[0]:
        raise np.linalg.LinAlgError("generator is numerically non-diagonalizable")
    left_h = np.linalg.inv(right)
    return values, right, left_h


def biorthogonal_cross_matrix(
    parent_right: np.ndarray,
    parent_left_h: np.ndarray,
    child_right: np.ndarray,
    child_left_h: np.ndarray,
) -> np.ndarray:
    """Scale-invariant parent-child biorthogonal carrier correspondence matrix.

    B_ij = |(w_i^P)^H v_j^C * (w_j^C)^H v_i^P|.
    The symmetric product is invariant to reciprocal rescaling of each left/right
    eigenvector pair and to a common similarity transformation of both generators.
    It is a correspondence diagnostic, not a probability and not a physical cutoff.
    """
    vp = np.asarray(parent_right, dtype=complex)
    wp = np.asarray(parent_left_h, dtype=complex)
    vc = np.asarray(child_right, dtype=complex)
    wc = np.asarray(child_left_h, dtype=complex)
    if vp.shape != vc.shape or wp.shape != wc.shape or vp.shape[0] != wp.shape[1]:
        raise ValueError("incompatible eigensystem shapes")
    n = vp.shape[1]
    result = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            forward = wp[i, :] @ vc[:, j]
            backward = wc[j, :] @ vp[:, i]
            result[i, j] = float(abs(forward * backward))
    return result


def ordinary_right_overlap(right: np.ndarray) -> np.ndarray:
    v = np.asarray(right, dtype=complex)
    norms = np.linalg.norm(v, axis=0)
    vn = v / norms[None, :]
    return np.abs(vn.conj().T @ vn) ** 2


def triangular_nonnormal_generator(shear: float) -> np.ndarray:
    eigenvalues = np.array([1.0, 2.0, 4.0])
    s = float(shear)
    basis = np.array(
        [
            [1.0, s, 0.5 * s],
            [0.0, 1.0, s],
            [0.0, 0.0, 1.0],
        ]
    )
    return basis @ np.diag(eigenvalues) @ np.linalg.inv(basis)


def conditioning_sweep(shears: tuple[float, ...] = (0.0, 0.5, 1.0, 3.0, 10.0, 30.0)) -> dict:
    rows = []
    for shear in shears:
        a = triangular_nonnormal_generator(shear)
        _, right, left_h = sorted_biorthogonal_eigensystem(a)
        right_overlap = ordinary_right_overlap(right)
        biorth = biorthogonal_cross_matrix(right, left_h, right, left_h)
        offdiag = right_overlap - np.diag(np.diag(right_overlap))
        rows.append(
            {
                "shear": float(shear),
                "right_eigenvector_condition_number": float(np.linalg.cond(right)),
                "maximum_offdiagonal_right_overlap": float(np.max(offdiag)),
                "biorthogonal_identity_residual": float(np.linalg.norm(biorth - np.eye(3))),
            }
        )
    return {
        "rows": rows,
        "interpretation": (
            "Shows that ordinary right-eigenvector geometry becomes increasingly misleading as non-normality grows, while the biorthogonal self-correspondence remains the identity until numerical conditioning fails."
        ),
    }


def similarity_invariance_case() -> dict:
    parent = triangular_nonnormal_generator(4.0)
    child_basis = np.array(
        [
            [1.0, 2.7, 0.8],
            [0.0, 1.0, 1.5],
            [0.0, 0.0, 1.0],
        ]
    )
    child = child_basis @ np.diag([1.15, 2.25, 4.2]) @ np.linalg.inv(child_basis)

    _, vp, wp = sorted_biorthogonal_eigensystem(parent)
    _, vc, wc = sorted_biorthogonal_eigensystem(child)
    before = biorthogonal_cross_matrix(vp, wp, vc, wc)

    transform = np.array(
        [
            [1.4, 0.2, 0.1],
            [0.1, 0.9, 0.15],
            [0.0, 0.1, 1.2],
        ]
    )
    transformed_parent = np.linalg.solve(transform, parent @ transform)
    transformed_child = np.linalg.solve(transform, child @ transform)
    _, vp2, wp2 = sorted_biorthogonal_eigensystem(transformed_parent)
    _, vc2, wc2 = sorted_biorthogonal_eigensystem(transformed_child)
    after = biorthogonal_cross_matrix(vp2, wp2, vc2, wc2)

    return {
        "before": before.tolist(),
        "after_common_similarity_transform": after.tolist(),
        "maximum_correspondence_change": float(np.max(np.abs(before - after))),
        "interpretation": (
            "Tests that the symmetric left/right carrier correspondence is unchanged by a common invertible coordinate transformation of parent and child generators."
        ),
    }


def near_defective_conditioning_sweep(
    epsilons: tuple[float, ...] = (1e-1, 1e-2, 1e-4, 1e-6, 1e-8),
) -> dict:
    rows = []
    for epsilon in epsilons:
        a = np.array([[1.0, 1.0], [float(epsilon), 1.0]])
        values, right, left_h = sorted_biorthogonal_eigensystem(a)
        identity_residual = float(np.linalg.norm(left_h @ right - np.eye(2)))
        rows.append(
            {
                "epsilon": float(epsilon),
                "eigenvalue_gap": float(abs(values[1] - values[0])),
                "right_eigenvector_condition_number": float(np.linalg.cond(right)),
                "biorthogonal_normalization_residual": identity_residual,
            }
        )
    return {
        "rows": rows,
        "interpretation": (
            "Approaches a defective two-dimensional generator. The growing eigenvector condition number is retained as an uncertainty/refusal signal even while algebraic biorthogonal normalization can still be computed numerically."
        ),
    }


def run_nonnormal_validation() -> dict:
    return {
        "scope": SCOPE,
        "physical_thresholds_frozen": False,
        "real_system_evidence": False,
        "conditioning_sweep": conditioning_sweep(),
        "similarity_invariance": similarity_invariance_case(),
        "near_defective_conditioning": near_defective_conditioning_sweep(),
        "reporting_rule": (
            "For a non-normal physical generator, promoted carrier correspondence must retain left and right eigenvectors or equivalent invariant projectors/subspaces plus conditioning. Right eigenvectors alone are insufficient."
        ),
    }


def write_nonnormal_validation(path: str | Path) -> dict:
    result = run_nonnormal_validation()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    output = write_nonnormal_validation("substrate_inheritance/results/nonnormal_validation.json")
    print(json.dumps(output, indent=2, sort_keys=True))
