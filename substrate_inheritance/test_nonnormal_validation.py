import numpy as np

from substrate_inheritance.nonnormal_validation import (
    SCOPE,
    biorthogonal_cross_matrix,
    conditioning_sweep,
    near_defective_conditioning_sweep,
    ordinary_right_overlap,
    run_nonnormal_validation,
    similarity_invariance_case,
    sorted_biorthogonal_eigensystem,
    triangular_nonnormal_generator,
)


def test_left_right_basis_is_biorthogonally_normalized():
    a = triangular_nonnormal_generator(5.0)
    _, right, left_h = sorted_biorthogonal_eigensystem(a)
    assert np.linalg.norm(left_h @ right - np.eye(3)) < 1e-12
    cross = biorthogonal_cross_matrix(right, left_h, right, left_h)
    assert np.linalg.norm(cross - np.eye(3)) < 1e-10


def test_right_vectors_alone_become_misleading_as_nonnormality_grows():
    rows = conditioning_sweep(shears=(0.0, 1.0, 10.0))["rows"]
    assert rows[0]["maximum_offdiagonal_right_overlap"] < 1e-12
    assert rows[-1]["maximum_offdiagonal_right_overlap"] > rows[1]["maximum_offdiagonal_right_overlap"]
    assert rows[-1]["right_eigenvector_condition_number"] > rows[1]["right_eigenvector_condition_number"]
    assert rows[-1]["biorthogonal_identity_residual"] < 1e-8


def test_biorthogonal_correspondence_is_similarity_invariant():
    result = similarity_invariance_case()
    assert result["maximum_correspondence_change"] < 1e-9


def test_near_defectiveness_is_exposed_by_conditioning():
    result = near_defective_conditioning_sweep(epsilons=(1e-1, 1e-4, 1e-8))
    rows = result["rows"]
    assert rows[-1]["eigenvalue_gap"] < rows[0]["eigenvalue_gap"]
    assert rows[-1]["right_eigenvector_condition_number"] > rows[0]["right_eigenvector_condition_number"]
    assert rows[-1]["biorthogonal_normalization_residual"] < 1e-8


def test_nonnormal_record_is_not_physical_evidence():
    result = run_nonnormal_validation()
    assert result["scope"] == SCOPE
    assert result["physical_thresholds_frozen"] is False
    assert result["real_system_evidence"] is False
