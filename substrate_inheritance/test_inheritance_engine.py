import numpy as np

from substrate_inheritance.inheritance_engine import (
    EvidenceGates,
    classify_evidence,
    dynamic_stiffness,
    eigenvalue_preserving_modal_scramble,
    finite_harmonic_kernel,
    modal_overlap,
    principal_angle_cosines,
    schur_effective_child,
    substrate_self_energy,
    synthetic_validation,
)


def test_evidence_ladder_does_not_promote_influence_to_inheritance():
    gates = EvidenceGates(True, False, False, False, True, False)
    assert classify_evidence(gates) == "SUBSTRATE_INFLUENCE"


def test_conditional_inheritance_requires_frozen_mapping_and_prediction():
    gates = EvidenceGates(True, True, True, True, False, False)
    assert classify_evidence(gates) == "CONDITIONAL_INHERITANCE"


def test_full_inheritance_requires_all_gates():
    gates = EvidenceGates(True, True, True, True, True, True)
    assert classify_evidence(gates) == "SUBSTRATE_INHERITANCE"


def test_modal_overlap_identifies_rotated_carriers():
    theta = 0.25
    parent = np.eye(2)
    child = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    overlap = modal_overlap(parent, child, np.ones(2))
    assert overlap.shape == (2, 2)
    assert overlap[0, 0] > overlap[0, 1]
    assert overlap[1, 1] > overlap[1, 0]


def test_subspace_metric_handles_basis_rotation_without_false_loss():
    parent = np.eye(3)[:, :2]
    q = np.array([[0.0, 1.0], [1.0, 0.0], [0.0, 0.0]])
    cosines = principal_angle_cosines(parent, q, np.ones(3))
    assert np.allclose(cosines, np.ones(2), atol=1e-12)


def test_schur_elimination_matches_explicit_self_energy_identity():
    k_ss = np.array([[4.0, 0.4], [0.4, 3.0]])
    d_ss = dynamic_stiffness(k_ss, np.eye(2), 0.7)
    d_aa = dynamic_stiffness(np.array([[2.2]]), np.eye(1), 0.7)
    coupling = np.array([[0.3], [0.15]])
    sigma = substrate_self_energy(d_ss, coupling, coupling.T)
    effective = schur_effective_child(d_ss, coupling, coupling.T, d_aa)
    assert np.allclose(effective, d_aa - sigma, atol=1e-12)


def test_eigenvalue_preserving_scramble_really_preserves_spectrum():
    eigenvalues = np.array([1.0, 2.0, 4.0])
    scrambled = eigenvalue_preserving_modal_scramble(eigenvalues, seed=7)
    assert np.allclose(np.linalg.eigvalsh(scrambled), eigenvalues, atol=1e-12)
    assert not np.allclose(scrambled, np.diag(eigenvalues))


def test_finite_harmonic_bath_retains_late_recurrence():
    times = np.linspace(0.0, 100.0, 2001)
    kernel = finite_harmonic_kernel(np.array([0.7, 1.1, 1.6]), np.array([0.6, 0.3, 0.1]), times)
    assert np.max(np.abs(kernel[times > 50.0])) > 0.2


def test_synthetic_validation_is_not_labeled_physical_evidence():
    result = synthetic_validation()
    assert result["scope"] == "synthetic_software_validation_only"
    assert result["schur_identity_residual"] < 1e-12
    assert result["eigenvalue_preserving_scramble_specificity_gap"] > 0.0
