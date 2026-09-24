from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np


class D01CRefusal(ValueError):
    """Fail-closed refusal for invalid D01C inputs."""


def _require_finite(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x):
        raise D01CRefusal(f"{name} must be finite")
    return x


def construct_generator(lambda1: float, lambda2: float, theta_deg: float) -> tuple[np.ndarray, np.ndarray]:
    l1 = _require_finite(lambda1, "lambda1")
    l2 = _require_finite(lambda2, "lambda2")
    theta = math.radians(_require_finite(theta_deg, "theta_deg"))
    if l1 >= 0.0 or l2 >= 0.0:
        raise D01CRefusal("D01C frozen families require strictly stable real eigenvalues")
    if abs(l1 - l2) <= 1e-14:
        raise D01CRefusal("D01C v0.1 requires distinct eigenvalues")
    if not (0.0 < theta <= math.pi / 2.0):
        raise D01CRefusal("theta must lie in (0, 90] degrees")

    c = math.cos(theta)
    s = math.sin(theta)
    v = np.array([[1.0, c], [0.0, s]], dtype=float)
    if abs(np.linalg.det(v)) <= 1e-14:
        raise D01CRefusal("carrier basis is numerically singular")

    a = v @ np.diag([l1, l2]) @ np.linalg.inv(v)
    return a, v


def exact_propagators(lambda1: float, lambda2: float, theta_deg: float, time: np.ndarray) -> np.ndarray:
    l1 = float(lambda1)
    l2 = float(lambda2)
    theta = math.radians(float(theta_deg))
    t = np.asarray(time, dtype=float)
    if t.ndim != 1 or t.size < 2 or not np.all(np.isfinite(t)) or np.any(t < 0.0):
        raise D01CRefusal("time grid must be finite, one-dimensional, and nonnegative")
    if np.any(np.diff(t) <= 0.0):
        raise D01CRefusal("time grid must be strictly increasing")

    e1 = np.exp(l1 * t)
    e2 = np.exp(l2 * t)
    cot = math.cos(theta) / math.sin(theta)
    off = cot * (e2 - e1)

    p = np.zeros((t.size, 2, 2), dtype=float)
    p[:, 0, 0] = e1
    p[:, 0, 1] = off
    p[:, 1, 1] = e2
    return p


def _operator_gain(propagators: np.ndarray, time: np.ndarray) -> dict[str, float]:
    singular = np.linalg.svd(propagators, compute_uv=False)
    smax = singular[:, 0]
    idx = int(np.argmax(smax))
    return {
        "max_operator_state_gain": float(smax[idx]),
        "time_of_max_operator_state_gain": float(time[idx]),
        "max_operator_energy_gain": float(smax[idx] ** 2),
    }


def _fixed_perturbation_gain(propagators: np.ndarray, x0: np.ndarray, time: np.ndarray) -> dict[str, float]:
    x = np.asarray(x0, dtype=float)
    if x.shape != (2,) or not np.all(np.isfinite(x)):
        raise D01CRefusal("fixed perturbation must be a finite length-2 vector")
    norm0 = float(np.linalg.norm(x))
    if norm0 <= 0.0:
        raise D01CRefusal("fixed perturbation must be nonzero")
    response = np.einsum("tij,j->ti", propagators, x)
    norm = np.linalg.norm(response, axis=1) / norm0
    idx = int(np.argmax(norm))
    return {
        "max_state_gain": float(norm[idx]),
        "time_of_max_state_gain": float(time[idx]),
        "final_state_gain": float(norm[-1]),
    }


def _resolvent_metrics(a: np.ndarray, omega: np.ndarray) -> dict[str, float]:
    w = np.asarray(omega, dtype=float)
    if w.ndim != 1 or w.size < 2 or not np.all(np.isfinite(w)) or np.any(w < 0.0):
        raise D01CRefusal("omega grid must be finite, one-dimensional, and nonnegative")
    if np.any(np.diff(w) <= 0.0):
        raise D01CRefusal("omega grid must be strictly increasing")

    z = 1j * w
    mats = np.empty((w.size, 2, 2), dtype=complex)
    mats[:, 0, 0] = z - a[0, 0]
    mats[:, 0, 1] = -a[0, 1]
    mats[:, 1, 0] = -a[1, 0]
    mats[:, 1, 1] = z - a[1, 1]
    inv = np.linalg.inv(mats)
    singular = np.linalg.svd(inv, compute_uv=False)
    peak = singular[:, 0]
    idx = int(np.argmax(peak))
    peak_value = float(peak[idx])
    return {
        "resolvent_peak_2norm": peak_value,
        "resolvent_peak_frequency": float(w[idx]),
        "complex_unstructured_stability_radius_from_resolvent_scan": float(1.0 / peak_value),
    }


def evaluate_case(family_id: str, eigenvalues: list[float], theta_deg: float, freeze: dict[str, Any]) -> dict[str, Any]:
    if len(eigenvalues) != 2:
        raise D01CRefusal("each D01C spectral family must contain two eigenvalues")
    l1, l2 = (float(eigenvalues[0]), float(eigenvalues[1]))
    a, v = construct_generator(l1, l2, theta_deg)

    eig = np.linalg.eigvals(a)
    eig = np.sort(np.real_if_close(eig).astype(float))
    expected = np.sort(np.asarray([l1, l2], dtype=float))
    spectral_residual = float(np.max(np.abs(eig - expected)))

    symmetric = 0.5 * (a + a.T)
    numerical_abscissa = float(np.max(np.linalg.eigvalsh(symmetric)))
    spectral_abscissa = float(max(l1, l2))
    condition = float(np.linalg.cond(v))
    henrici = float(math.sqrt(max(0.0, np.linalg.norm(a, ord="fro") ** 2 - (l1 * l1 + l2 * l2))))

    tg = freeze["observation_grids"]["time"]
    time = np.linspace(float(tg["start"]), float(tg["stop"]), int(tg["points"]))
    propagators = exact_propagators(l1, l2, theta_deg, time)
    operator = _operator_gain(propagators, time)

    fixed = {}
    for perturbation in freeze["fixed_perturbations"]:
        fixed[perturbation["id"]] = _fixed_perturbation_gain(
            propagators,
            np.asarray(perturbation["x0"], dtype=float),
            time,
        )

    rg = freeze["observation_grids"]["resolvent_frequency"]
    omega = np.linspace(float(rg["start"]), float(rg["stop"]), int(rg["points"]))
    resolvent = _resolvent_metrics(a, omega)

    return {
        "family_id": family_id,
        "theta_deg": float(theta_deg),
        "eigenvalues": [l1, l2],
        "generator": [[float(a[0, 0]), float(a[0, 1])], [float(a[1, 0]), float(a[1, 1])]],
        "spectral_residual": spectral_residual,
        "spectral_abscissa": spectral_abscissa,
        "numerical_abscissa": numerical_abscissa,
        "right_eigenvector_condition_number": condition,
        "right_eigenvector_angle_deg": float(theta_deg),
        "Henrici_departure_from_normality": henrici,
        **operator,
        "fixed_perturbations": fixed,
        **resolvent,
        "scalar_status": "NO_MASTER_SCALAR_SEARCHED",
    }


def _family_summary(records: list[dict[str, Any]], numerical_error_floor: float) -> dict[str, Any]:
    ordered = sorted(records, key=lambda r: r["theta_deg"], reverse=True)
    normal = max(ordered, key=lambda r: r["theta_deg"])
    strongest = min(ordered, key=lambda r: r["theta_deg"])

    gains = np.asarray([r["max_operator_state_gain"] for r in ordered], dtype=float)
    resolvents = np.asarray([r["resolvent_peak_2norm"] for r in ordered], dtype=float)
    radii = np.asarray([r["complex_unstructured_stability_radius_from_resolvent_scan"] for r in ordered], dtype=float)

    positive_numerical = [r for r in ordered if r["numerical_abscissa"] > numerical_error_floor]
    first_positive = max(positive_numerical, key=lambda r: r["theta_deg"]) if positive_numerical else None

    gain_span = float(np.max(gains) - np.min(gains))
    resolvent_span = float(np.max(resolvents) - np.min(resolvents))

    return {
        "family_id": normal["family_id"],
        "eigenvalues": normal["eigenvalues"],
        "spectral_abscissa": normal["spectral_abscissa"],
        "normal_theta_deg": normal["theta_deg"],
        "smallest_theta_deg": strongest["theta_deg"],
        "normal_max_operator_state_gain": normal["max_operator_state_gain"],
        "smallest_theta_max_operator_state_gain": strongest["max_operator_state_gain"],
        "state_gain_ratio_smallest_theta_to_normal": float(
            strongest["max_operator_state_gain"] / normal["max_operator_state_gain"]
        ),
        "max_operator_state_gain_span": gain_span,
        "resolvent_peak_span": resolvent_span,
        "minimum_scanned_stability_radius": float(np.min(radii)),
        "first_theta_with_positive_numerical_abscissa": (
            None if first_positive is None else float(first_positive["theta_deg"])
        ),
        "eigenvalue_set_sufficient_for_finite_time_response": bool(gain_span <= numerical_error_floor),
    }


def run_d01c(freeze: dict[str, Any]) -> dict[str, Any]:
    if freeze.get("schema") != "d01c-nonnormal-preexecution-freeze-v0.1":
        raise D01CRefusal("D01C requires preexecution freeze v0.1")
    if freeze.get("status") != "P0_D_PREEXECUTION_FROZEN_BEFORE_D01C_OUTPUT":
        raise D01CRefusal("unexpected D01C freeze status")
    if freeze["scalar_policy"]["master_scalar_search"] is not False:
        raise D01CRefusal("D01C v0.1 forbids a master scalar search")

    families = freeze["generator_family"]["spectral_families"]
    theta_values = [float(v) for v in freeze["generator_family"]["theta_degrees"]]
    records = []
    for family in families:
        for theta in theta_values:
            records.append(evaluate_case(family["id"], family["eigenvalues"], theta, freeze))

    floor = float(freeze["decision_rules"]["numerical_error_floor"])
    family_summaries = []
    for family in families:
        subset = [r for r in records if r["family_id"] == family["id"]]
        family_summaries.append(_family_summary(subset, floor))

    max_spectral_residual = max(float(r["spectral_residual"]) for r in records)
    eigenvalue_only_refuted = any(
        not s["eigenvalue_set_sufficient_for_finite_time_response"] for s in family_summaries
    )

    return {
        "schema": "d01c-nonnormal-domain-map-result-v0.1",
        "status": "P0_DOMAIN_MAP_NONNORMAL_LINEAR",
        "phase_id": "D01C_NONNORMAL_EXTENSION",
        "freeze": "D01C_PREEXECUTION_FREEZE_v0.1.json",
        "atlas_blind": True,
        "cross_domain_confirmation": False,
        "physical_system_evidence": False,
        "master_scalar_searched": False,
        "case_count": len(records),
        "expected_case_count": len(families) * len(theta_values),
        "max_spectral_residual": max_spectral_residual,
        "family_summaries": family_summaries,
        "eigenvalue_only_sufficiency_status": (
            "REFUTED_WITHIN_FROZEN_CONSTRUCTION"
            if eigenvalue_only_refuted
            else "NOT_REFUTED_WITHIN_FROZEN_CONSTRUCTION"
        ),
        "native_toolkit_position": (
            "D01C uses established state-transition, conditioning, numerical-abscissa, and resolvent "
            "diagnostics as the reference toolkit. Any SymC added-value interpretation is downstream "
            "of these native results and cannot rename them as new quantities."
        ),
        "records": records,
    }


def load_freeze(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
