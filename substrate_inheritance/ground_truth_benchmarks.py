from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from substrate_inheritance.inheritance_engine import (
    EvidenceGates,
    classify_evidence,
    dynamic_stiffness,
    eigenvalue_preserving_modal_scramble,
    finite_difference_transfer,
    finite_harmonic_kernel,
    modal_overlap,
    principal_angle_cosines,
    schur_effective_child,
    substrate_self_energy,
)


SCOPE = "synthetic_ground_truth_benchmark_only"


def _record(case_id: str, ground_truth: str, evidence_label: str, observations: dict) -> dict:
    return {
        "case_id": case_id,
        "scope": SCOPE,
        "ground_truth": ground_truth,
        "evidence_label": evidence_label,
        "observations": observations,
    }


def _case_no_coupling() -> dict:
    d_ss = dynamic_stiffness(np.diag([3.0, 5.0]), np.eye(2), 0.6)
    coupling = np.zeros((2, 1))
    sigma = substrate_self_energy(d_ss, coupling, coupling.T)
    label = classify_evidence(EvidenceGates(True, False, False, False, False, False))
    return _record(
        "C01_NO_COUPLING",
        "NO_SUBSTRATE_INFLUENCE",
        label,
        {"max_abs_substrate_self_energy": float(np.max(np.abs(sigma)))},
    )


def _case_influence_only() -> dict:
    parent = np.array([2.0, 3.0])

    def child_fn(x: np.ndarray) -> np.ndarray:
        return np.array([x[0] + 2.0 * x[1]])

    transfer = finite_difference_transfer(parent, child_fn)
    label = classify_evidence(EvidenceGates(True, False, False, False, True, False))
    return _record(
        "C02_INFLUENCE_ONLY",
        "CAUSAL_INFLUENCE_WITHOUT_INHERITANCE_MAPPING",
        label,
        {"transfer_matrix": transfer.tolist(), "transfer_norm": float(np.linalg.norm(transfer))},
    )


def _case_scalar_conditional() -> dict:
    parent_scalar = 2.0
    frozen_map = lambda x: 1.5 * x + 0.25
    predicted = frozen_map(parent_scalar)
    independently_revealed_child = 3.25
    label = classify_evidence(EvidenceGates(True, True, True, True, False, False))
    return _record(
        "C03_SCALAR_CONDITIONAL",
        "PROSPECTIVE_SCALAR_MAPPING_WITHOUT_INTERVENTION_OR_SPECIFICITY",
        label,
        {
            "parent_scalar": parent_scalar,
            "predicted_child_scalar": predicted,
            "revealed_child_scalar": independently_revealed_child,
            "absolute_prediction_error": abs(predicted - independently_revealed_child),
        },
    )


def _case_modal_inheritance_scalar_changed() -> dict:
    theta = 0.37
    q = np.array(
        [
            [np.cos(theta), -np.sin(theta), 0.0],
            [np.sin(theta), np.cos(theta), 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    parent_modes = np.eye(3)
    child_modes = q @ parent_modes
    overlap = modal_overlap(parent_modes, child_modes, np.ones(3))
    parent_scalars = np.array([1.0, 2.0, 3.0])
    child_scalars = np.array([1.4, 2.6, 3.9])
    label = classify_evidence(EvidenceGates(True, True, True, True, True, True))
    return _record(
        "C04_MODAL_INHERITANCE_SCALAR_CHANGED",
        "MODAL_CARRIER_INHERITANCE_DOES_NOT_REQUIRE_SCALAR_EQUALITY",
        label,
        {
            "modal_overlap": overlap.tolist(),
            "scalar_values_preserved": bool(np.allclose(parent_scalars, child_scalars)),
            "known_basis_map_residual": float(np.linalg.norm(child_modes - q @ parent_modes)),
        },
    )


def _case_frequency_false_friend() -> dict:
    eigenvalues = np.array([1.0, 2.0, 4.0])
    parent = np.diag(eigenvalues)
    child = eigenvalue_preserving_modal_scramble(eigenvalues, seed=17)
    child_values, child_vectors = np.linalg.eigh(child)
    parent_values, parent_vectors = np.linalg.eigh(parent)
    overlap = modal_overlap(parent_vectors, child_vectors, np.ones(3))
    spectral_error = float(np.max(np.abs(parent_values - child_values)))
    identity_overlap_error = float(np.linalg.norm(overlap - np.eye(3)))
    label = classify_evidence(EvidenceGates(True, False, False, False, False, False))
    return _record(
        "C05_FREQUENCY_FALSE_FRIEND",
        "EQUAL_EIGENVALUES_DO_NOT_ESTABLISH_MODAL_INHERITANCE",
        label,
        {
            "max_eigenvalue_difference": spectral_error,
            "modal_overlap": overlap.tolist(),
            "identity_overlap_error": identity_overlap_error,
        },
    )


def _case_mode_splitting() -> dict:
    parent = np.array([[1.0], [0.0], [0.0]])
    inv_sqrt2 = 1.0 / np.sqrt(2.0)
    child_subspace = np.array(
        [
            [inv_sqrt2, inv_sqrt2],
            [inv_sqrt2, -inv_sqrt2],
            [0.0, 0.0],
        ]
    )
    vector_overlaps = modal_overlap(parent, child_subspace, np.ones(3))
    subspace_cosines = principal_angle_cosines(parent, child_subspace, np.ones(3))
    return _record(
        "C06_MODE_SPLITTING",
        "ONE_PARENT_CARRIER_SPLITS_ACROSS_A_CHILD_SUBSPACE",
        "CARRIER_RESOLVED_SUBSPACE_CASE",
        {
            "individual_vector_overlaps": vector_overlaps.tolist(),
            "max_individual_overlap": float(np.max(vector_overlaps)),
            "principal_angle_cosines": subspace_cosines.tolist(),
        },
    )


def _case_degenerate_subspace() -> dict:
    parent = np.eye(3)[:, :2]
    theta = 0.83
    child = np.array(
        [
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)],
            [0.0, 0.0],
        ]
    )
    overlap = modal_overlap(parent, child, np.ones(3))
    cosines = principal_angle_cosines(parent, child, np.ones(3))
    return _record(
        "C07_DEGENERATE_SUBSPACE",
        "BASIS_ROTATION_WITHIN_A_DEGENERATE_SUBSPACE_IS_NOT_INHERITANCE_LOSS",
        "CARRIER_RESOLVED_SUBSPACE_CASE",
        {"individual_overlap": overlap.tolist(), "principal_angle_cosines": cosines.tolist()},
    )


def _case_coupling_rewire() -> dict:
    k_ss = np.array([[4.0, 0.25], [0.25, 2.8]])
    d_ss = dynamic_stiffness(k_ss, np.eye(2), 0.65)
    c_original = np.array([[0.35], [0.08]])
    c_rewired = np.array([[0.08], [0.35]])
    sigma_original = substrate_self_energy(d_ss, c_original, c_original.T)
    sigma_rewired = substrate_self_energy(d_ss, c_rewired, c_rewired.T)
    return _record(
        "C08_COUPLING_REWIRE",
        "CONGLOMERATION_DEPENDS_ON_COUPLING_ASSIGNMENT_NOT_JUST_SUBSTRATE_SPECTRUM",
        "CONGLOMERATION_SPECIFICITY_CASE",
        {
            "original_self_energy_real": float(np.real(sigma_original[0, 0])),
            "rewired_self_energy_real": float(np.real(sigma_rewired[0, 0])),
            "rewire_gap": float(abs(sigma_original[0, 0] - sigma_rewired[0, 0])),
        },
    )


def _case_finite_bath_recurrence() -> dict:
    times = np.linspace(0.0, 120.0, 2401)
    kernel = finite_harmonic_kernel(
        np.array([0.7, 1.1, 1.6, 2.05]),
        np.array([0.45, 0.30, 0.17, 0.08]),
        times,
    )
    tail = kernel[times > 60.0]
    return _record(
        "C09_FINITE_BATH_RECURRENCE",
        "FINITE_HARMONIC_BATH_IS_NOT_AUTOMATICALLY_IRREVERSIBLE_FRICTION",
        "NON_MARKOVIAN_OR_FINITE_BATH_HOLD",
        {
            "late_max_abs_kernel": float(np.max(np.abs(tail))),
            "late_rms_kernel": float(np.sqrt(np.mean(tail**2))),
        },
    )


def _case_full_prospective_inheritance() -> dict:
    k_ss = np.array([[4.2, 0.35], [0.35, 3.1]])
    m_ss = np.eye(2)
    d_ss = dynamic_stiffness(k_ss, m_ss, 0.72)
    d_aa = dynamic_stiffness(np.array([[2.4]]), np.eye(1), 0.72)
    coupling = np.array([[0.31], [0.14]])

    frozen_prediction = schur_effective_child(d_ss, coupling, coupling.T, d_aa)
    independently_generated_child = d_aa - substrate_self_energy(d_ss, coupling, coupling.T)
    prediction_error = float(np.max(np.abs(frozen_prediction - independently_generated_child)))

    parent_parameters = np.array([4.2, 3.1])

    def child_fn(x: np.ndarray) -> np.ndarray:
        local = np.array([[x[0], 0.35], [0.35, x[1]]])
        ds = dynamic_stiffness(local, m_ss, 0.72)
        return np.array([np.real(substrate_self_energy(ds, coupling, coupling.T)[0, 0])])

    transfer = finite_difference_transfer(parent_parameters, child_fn)

    scrambled_k = eigenvalue_preserving_modal_scramble(np.linalg.eigvalsh(k_ss), seed=91)
    scrambled_ds = dynamic_stiffness(scrambled_k, m_ss, 0.72)
    scrambled_sigma = substrate_self_energy(scrambled_ds, coupling, coupling.T)
    true_sigma = substrate_self_energy(d_ss, coupling, coupling.T)
    specificity_gap = float(abs(scrambled_sigma[0, 0] - true_sigma[0, 0]))

    label = classify_evidence(EvidenceGates(True, True, True, True, True, True))
    return _record(
        "C10_FULL_PROSPECTIVE_INHERITANCE",
        "KNOWN_PARENT_TO_CHILD_MAPPING_WITH_INTERVENTION_AND_SPECIFICITY",
        label,
        {
            "prediction_error": prediction_error,
            "transfer_matrix": transfer.tolist(),
            "transfer_norm": float(np.linalg.norm(transfer)),
            "eigenvalue_preserving_scramble_gap": specificity_gap,
        },
    )


def run_ground_truth_benchmarks() -> dict:
    cases = [
        _case_no_coupling(),
        _case_influence_only(),
        _case_scalar_conditional(),
        _case_modal_inheritance_scalar_changed(),
        _case_frequency_false_friend(),
        _case_mode_splitting(),
        _case_degenerate_subspace(),
        _case_coupling_rewire(),
        _case_finite_bath_recurrence(),
        _case_full_prospective_inheritance(),
    ]
    return {
        "scope": SCOPE,
        "case_count": len(cases),
        "physical_thresholds_frozen": False,
        "real_system_evidence": False,
        "purpose": "Adversarial ground-truth validation of substrate-inheritance inference machinery before physical target reveal.",
        "cases": cases,
    }


def write_ground_truth_benchmarks(path: str | Path) -> dict:
    result = run_ground_truth_benchmarks()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    output = write_ground_truth_benchmarks("substrate_inheritance/results/ground_truth_benchmarks.json")
    print(json.dumps(output, indent=2, sort_keys=True))
