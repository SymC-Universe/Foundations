from substrate_inheritance.robustness_validation import (
    SCOPE,
    coordinate_invariance_ensemble,
    degeneracy_robustness_ensemble,
    run_robustness_validation,
)


def test_embedding_is_invariant_under_consistent_coordinate_changes():
    result = coordinate_invariance_ensemble(trials=64, dimension=5, seed=20260834)
    assert result["orthogonal_basis_change_residual"]["maximum"] < 1e-10
    assert result["invertible_coordinate_scaling_residual"]["maximum"] < 1e-10


def test_near_degeneracy_rotates_vectors_more_than_the_containing_subspace():
    result = degeneracy_robustness_ensemble(trials=64, dimension=5, seed=20260835)
    near = result["near_degenerate"]
    separated = result["separated"]
    assert near["individual_assignment_mean"] < separated["individual_assignment_mean"]
    assert near["minimum_subspace_cosine_q05"] > near["individual_assignment_q05"]
    assert near["minimum_subspace_cosine_q05"] > 0.999


def test_robustness_record_is_not_physical_evidence():
    result = run_robustness_validation()
    assert result["scope"] == SCOPE
    assert result["physical_thresholds_frozen"] is False
    assert result["real_system_evidence"] is False
