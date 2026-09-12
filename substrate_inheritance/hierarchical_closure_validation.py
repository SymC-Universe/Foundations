from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from substrate_inheritance.inheritance_engine import dynamic_stiffness


PLAN_SCHEMA = "substrate-inheritance-fm4-hierarchical-closure-plan-v0.1"
RESULT_SCHEMA = "substrate-inheritance-fm4-hierarchical-closure-result-v0.1"


class HierarchicalClosureRefusal(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _complex_pair(value: complex) -> list[float]:
    z = complex(value)
    return [float(np.real(z)), float(np.imag(z))]


def _relative_error(estimate: complex, reference: complex, floor: float = 1e-14) -> float | None:
    ref = abs(reference)
    if ref <= floor:
        return None
    return float(abs(estimate - reference) / ref)


def _finite_nonnegative(name: str, value: float) -> float:
    x = float(value)
    if not np.isfinite(x) or x < 0.0:
        raise HierarchicalClosureRefusal("INVALID_PARAMETER", f"{name} must be finite and nonnegative")
    return x


def _finite_positive_vector(name: str, values: Any, n: int) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.shape != (n,) or not np.all(np.isfinite(arr)) or np.any(arr <= 0.0):
        raise HierarchicalClosureRefusal(
            "INVALID_PARAMETER",
            f"{name} must contain exactly {n} finite positive values",
        )
    return arr


def _add_pair_spring(k_matrix: np.ndarray, i: int, j: int, stiffness: float) -> None:
    k = _finite_nonnegative("pair stiffness", stiffness)
    k_matrix[i, i] += k
    k_matrix[j, j] += k
    k_matrix[i, j] -= k
    k_matrix[j, i] -= k


def assemble_four_dof_chain(
    masses: np.ndarray,
    ground_stiffness: np.ndarray,
    inner1_boundary_coupling: float,
    internal_coupling: float,
    boundary_outer_coupling: float,
    rayleigh_alpha: float,
    rayleigh_beta: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    masses = _finite_positive_vector("masses", masses, 4)
    ground = _finite_positive_vector("ground_stiffness", ground_stiffness, 4)
    k_ib = _finite_nonnegative("inner1_boundary_coupling", inner1_boundary_coupling)
    k_internal = _finite_nonnegative("internal_coupling", internal_coupling)
    k_outer = _finite_nonnegative("boundary_outer_coupling", boundary_outer_coupling)
    alpha = _finite_nonnegative("rayleigh_alpha", rayleigh_alpha)
    beta = _finite_nonnegative("rayleigh_beta", rayleigh_beta)

    mass = np.diag(masses)
    stiffness = np.diag(ground)
    _add_pair_spring(stiffness, 0, 1, k_internal)
    _add_pair_spring(stiffness, 1, 2, k_ib)
    _add_pair_spring(stiffness, 2, 3, k_outer)
    damping = alpha * mass + beta * stiffness

    if np.min(np.linalg.eigvalsh(stiffness)) <= 0.0:
        raise HierarchicalClosureRefusal("NONPOSITIVE_STIFFNESS", "assembled stiffness must be positive definite")
    if np.min(np.linalg.eigvalsh(mass)) <= 0.0:
        raise HierarchicalClosureRefusal("NONPOSITIVE_MASS", "assembled mass must be positive definite")
    return mass, damping, stiffness


def direct_outer_reduction(d: np.ndarray) -> dict[str, complex]:
    d = np.asarray(d, dtype=complex)
    if d.shape != (4, 4):
        raise HierarchicalClosureRefusal("INVALID_DYNAMIC_STIFFNESS", "expected a 4x4 dynamic-stiffness matrix")
    group = d[:3, :3]
    group_to_outer = d[:3, 3:4]
    outer_to_group = d[3:4, :3]
    outer = complex(d[3, 3])
    try:
        return_term = complex((outer_to_group @ np.linalg.solve(group, group_to_outer))[0, 0])
    except np.linalg.LinAlgError as exc:
        raise HierarchicalClosureRefusal("SINGULAR_GROUP", "group dynamic stiffness is singular") from exc
    effective = outer - return_term
    if abs(effective) <= 1e-15:
        raise HierarchicalClosureRefusal("SINGULAR_OUTER_EFFECTIVE", "outer effective dynamic stiffness is singular")
    return {
        "return": return_term,
        "effective": effective,
        "compliance": 1.0 / effective,
    }


def nested_exact_outer_reduction(d: np.ndarray) -> dict[str, complex]:
    d = np.asarray(d, dtype=complex)
    if d.shape != (4, 4):
        raise HierarchicalClosureRefusal("INVALID_DYNAMIC_STIFFNESS", "expected a 4x4 dynamic-stiffness matrix")

    d_ii = d[:2, :2]
    d_ib = d[:2, 2:3]
    d_bi = d[2:3, :2]
    d_bb = complex(d[2, 2])
    try:
        inner_return = complex((d_bi @ np.linalg.solve(d_ii, d_ib))[0, 0])
    except np.linalg.LinAlgError as exc:
        raise HierarchicalClosureRefusal("SINGULAR_INNER", "inner dynamic stiffness is singular") from exc
    boundary_effective = d_bb - inner_return
    if abs(boundary_effective) <= 1e-15:
        raise HierarchicalClosureRefusal("SINGULAR_BOUNDARY_EFFECTIVE", "boundary effective dynamic stiffness is singular")

    d_bo = complex(d[2, 3])
    d_ob = complex(d[3, 2])
    d_oo = complex(d[3, 3])
    outer_return = d_ob * (1.0 / boundary_effective) * d_bo
    outer_effective = d_oo - outer_return
    if abs(outer_effective) <= 1e-15:
        raise HierarchicalClosureRefusal("SINGULAR_OUTER_EFFECTIVE", "nested outer effective dynamic stiffness is singular")
    return {
        "inner_return": inner_return,
        "boundary_effective": boundary_effective,
        "return": outer_return,
        "effective": outer_effective,
        "compliance": 1.0 / outer_effective,
    }


def full_outer_compliance(d: np.ndarray) -> complex:
    d = np.asarray(d, dtype=complex)
    if d.shape != (4, 4):
        raise HierarchicalClosureRefusal("INVALID_DYNAMIC_STIFFNESS", "expected a 4x4 dynamic-stiffness matrix")
    try:
        inverse = np.linalg.inv(d)
    except np.linalg.LinAlgError as exc:
        raise HierarchicalClosureRefusal("SINGULAR_FULL_SYSTEM", "full dynamic stiffness is singular") from exc
    return complex(inverse[3, 3])


def guyuan_boundary_reduction(
    mass: np.ndarray,
    damping: np.ndarray,
    stiffness: np.ndarray,
    omega: float,
) -> dict[str, complex]:
    """Guyan-style static internal condensation, consistently transformed for M/C/K."""
    m_gg = np.asarray(mass[:3, :3], dtype=float)
    c_gg = np.asarray(damping[:3, :3], dtype=float)
    k_gg = np.asarray(stiffness[:3, :3], dtype=float)
    k_ii = k_gg[:2, :2]
    k_ib = k_gg[:2, 2:3]
    try:
        interior_map = -np.linalg.solve(k_ii, k_ib)
    except np.linalg.LinAlgError as exc:
        raise HierarchicalClosureRefusal("SINGULAR_STATIC_INNER", "static internal stiffness is singular") from exc
    transform = np.vstack((interior_map, np.ones((1, 1))))

    d_gg = dynamic_stiffness(k_gg, m_gg, omega, c_gg)
    d_go = dynamic_stiffness(stiffness, mass, omega, damping)[:3, 3:4]
    d_og = dynamic_stiffness(stiffness, mass, omega, damping)[3:4, :3]
    d_oo = complex(dynamic_stiffness(stiffness, mass, omega, damping)[3, 3])

    boundary_dynamic = complex((transform.T @ d_gg @ transform)[0, 0])
    if abs(boundary_dynamic) <= 1e-15:
        raise HierarchicalClosureRefusal("SINGULAR_GUYAN_BOUNDARY", "Guyan boundary dynamic stiffness is singular")
    coupling_go = complex((transform.T @ d_go)[0, 0])
    coupling_og = complex((d_og @ transform)[0, 0])
    outer_return = coupling_og * (1.0 / boundary_dynamic) * coupling_go
    outer_effective = d_oo - outer_return
    if abs(outer_effective) <= 1e-15:
        raise HierarchicalClosureRefusal("SINGULAR_GUYAN_OUTER", "Guyan outer effective dynamic stiffness is singular")
    return {
        "boundary_dynamic": boundary_dynamic,
        "return": outer_return,
        "effective": outer_effective,
        "compliance": 1.0 / outer_effective,
    }


def _mass_orthonormal_modes(k: np.ndarray, m: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    k = np.asarray(k, dtype=float)
    m = np.asarray(m, dtype=float)
    try:
        chol = np.linalg.cholesky(m)
    except np.linalg.LinAlgError as exc:
        raise HierarchicalClosureRefusal("INVALID_MODAL_MASS", "modal mass matrix must be positive definite") from exc
    linv = np.linalg.inv(chol)
    standard = linv @ k @ linv.T
    values, vectors = np.linalg.eigh(standard)
    modes = linv.T @ vectors
    return values, modes


def one_mode_internal_resolvent_reduction(
    mass: np.ndarray,
    damping: np.ndarray,
    stiffness: np.ndarray,
    omega: float,
) -> dict[str, complex]:
    """Approximate the inner 2-DOF resolvent using only its lowest generalized mode."""
    d = dynamic_stiffness(stiffness, mass, omega, damping)
    k_ii = np.asarray(stiffness[:2, :2], dtype=float)
    m_ii = np.asarray(mass[:2, :2], dtype=float)
    c_ii = np.asarray(damping[:2, :2], dtype=float)
    eigenvalues, modes = _mass_orthonormal_modes(k_ii, m_ii)
    mode = modes[:, 0:1]
    modal_damping = float((mode.T @ c_ii @ mode)[0, 0])
    denominator = complex(eigenvalues[0] - omega**2, omega * modal_damping)
    if abs(denominator) <= 1e-15:
        raise HierarchicalClosureRefusal("SINGULAR_ONE_MODE", "retained modal denominator is singular")
    approximate_inverse = (mode @ mode.T) / denominator

    d_ib = d[:2, 2:3]
    d_bi = d[2:3, :2]
    d_bb = complex(d[2, 2])
    inner_return = complex((d_bi @ approximate_inverse @ d_ib)[0, 0])
    boundary_effective = d_bb - inner_return
    if abs(boundary_effective) <= 1e-15:
        raise HierarchicalClosureRefusal("SINGULAR_ONE_MODE_BOUNDARY", "one-mode boundary effective dynamic stiffness is singular")

    d_bo = complex(d[2, 3])
    d_ob = complex(d[3, 2])
    d_oo = complex(d[3, 3])
    outer_return = d_ob * (1.0 / boundary_effective) * d_bo
    outer_effective = d_oo - outer_return
    if abs(outer_effective) <= 1e-15:
        raise HierarchicalClosureRefusal("SINGULAR_ONE_MODE_OUTER", "one-mode outer effective dynamic stiffness is singular")
    return {
        "retained_inner_eigenvalue": float(eigenvalues[0]),
        "omitted_inner_eigenvalue": float(eigenvalues[1]),
        "return": outer_return,
        "effective": outer_effective,
        "compliance": 1.0 / outer_effective,
    }


def _summarize_errors(values: list[float]) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    if arr.size == 0 or not np.all(np.isfinite(arr)):
        raise HierarchicalClosureRefusal("INVALID_ERROR_SERIES", "error series must be finite and nonempty")
    return {
        "median": float(np.median(arr)),
        "p95": float(np.quantile(arr, 0.95)),
        "maximum": float(np.max(arr)),
    }


def load_plan(path: str | Path) -> dict[str, Any]:
    plan = json.loads(Path(path).read_text(encoding="utf-8"))
    if plan.get("schema") != PLAN_SCHEMA:
        raise HierarchicalClosureRefusal("WRONG_PLAN", "unexpected FM4 plan schema")
    if plan.get("status") != "P0_D_EXPLORATORY_FUNCTION_AND_LIMIT_MAPPING":
        raise HierarchicalClosureRefusal("WRONG_PLAN_STATUS", "FM4 plan is not the expected P0-D plan")
    if plan.get("confirmatory_language_allowed") is not False or plan.get("mfr14_activated") is not False:
        raise HierarchicalClosureRefusal("P0_SCOPE_VIOLATION", "FM4 plan must remain exploratory")
    model = plan["model"]
    _finite_positive_vector("masses", model["masses"], 4)
    _finite_positive_vector("ground_stiffness", model["ground_stiffness"], 4)
    for name in (
        "inner1_boundary_coupling",
        "rayleigh_damping_alpha",
        "rayleigh_damping_beta",
    ):
        _finite_nonnegative(name, model[name])
    for value in model["internal_coupling_values"]:
        _finite_nonnegative("internal_coupling_values", value)
    for value in model["boundary_outer_coupling_values"]:
        _finite_nonnegative("boundary_outer_coupling_values", value)
    grid = plan["frequency_grid"]
    start = float(grid["omega_start"])
    stop = float(grid["omega_stop"])
    points = int(grid["points"])
    if not (np.isfinite(start) and np.isfinite(stop) and start >= 0.0 and stop > start and points >= 2):
        raise HierarchicalClosureRefusal("INVALID_FREQUENCY_GRID", "frequency grid is invalid")
    tolerance = float(plan["exact_numerical_tolerance"])
    if not np.isfinite(tolerance) or tolerance <= 0.0:
        raise HierarchicalClosureRefusal("INVALID_TOLERANCE", "exact numerical tolerance must be finite and positive")
    return plan


def run_fm4(plan_path: str | Path) -> dict[str, Any]:
    plan = load_plan(plan_path)
    model = plan["model"]
    grid = plan["frequency_grid"]
    frequencies = np.linspace(float(grid["omega_start"]), float(grid["omega_stop"]), int(grid["points"]))
    tolerance = float(plan["exact_numerical_tolerance"])

    records: list[dict[str, Any]] = []
    exact_compliance_abs_errors: list[float] = []
    nested_direct_abs_errors: list[float] = []
    exact_return_abs_errors: list[float] = []
    guyuan_compliance_errors_all: list[float] = []
    one_mode_compliance_errors_all: list[float] = []
    guyuan_return_errors_nonzero: list[float] = []
    one_mode_return_errors_nonzero: list[float] = []
    nonzero_outer_guyuan_compliance: list[float] = []
    nonzero_outer_one_mode_compliance: list[float] = []

    guyuan_max_location: dict[str, float] | None = None
    one_mode_max_location: dict[str, float] | None = None
    guyuan_max = -1.0
    one_mode_max = -1.0
    max_group_condition = 0.0
    max_inner_condition = 0.0

    masses = np.asarray(model["masses"], dtype=float)
    ground = np.asarray(model["ground_stiffness"], dtype=float)

    for k_internal in model["internal_coupling_values"]:
        for k_outer in model["boundary_outer_coupling_values"]:
            mass, damping, stiffness = assemble_four_dof_chain(
                masses=masses,
                ground_stiffness=ground,
                inner1_boundary_coupling=model["inner1_boundary_coupling"],
                internal_coupling=k_internal,
                boundary_outer_coupling=k_outer,
                rayleigh_alpha=model["rayleigh_damping_alpha"],
                rayleigh_beta=model["rayleigh_damping_beta"],
            )
            for omega in frequencies:
                d = dynamic_stiffness(stiffness, mass, float(omega), damping)
                full = full_outer_compliance(d)
                direct = direct_outer_reduction(d)
                nested = nested_exact_outer_reduction(d)
                guyuan = guyuan_boundary_reduction(mass, damping, stiffness, float(omega))
                one_mode = one_mode_internal_resolvent_reduction(mass, damping, stiffness, float(omega))

                full_direct_abs = float(abs(full - direct["compliance"]))
                direct_nested_abs = float(abs(direct["compliance"] - nested["compliance"]))
                return_abs = float(abs(direct["return"] - nested["return"]))
                exact_compliance_abs_errors.append(full_direct_abs)
                nested_direct_abs_errors.append(direct_nested_abs)
                exact_return_abs_errors.append(return_abs)

                guyuan_comp_rel = _relative_error(guyuan["compliance"], full)
                one_mode_comp_rel = _relative_error(one_mode["compliance"], full)
                if guyuan_comp_rel is None or one_mode_comp_rel is None:
                    raise HierarchicalClosureRefusal("ZERO_REFERENCE_COMPLIANCE", "full outer compliance unexpectedly vanished")
                guyuan_compliance_errors_all.append(guyuan_comp_rel)
                one_mode_compliance_errors_all.append(one_mode_comp_rel)
                if float(k_outer) > 0.0:
                    nonzero_outer_guyuan_compliance.append(guyuan_comp_rel)
                    nonzero_outer_one_mode_compliance.append(one_mode_comp_rel)

                guyuan_return_rel = _relative_error(guyuan["return"], direct["return"])
                one_mode_return_rel = _relative_error(one_mode["return"], direct["return"])
                if guyuan_return_rel is not None:
                    guyuan_return_errors_nonzero.append(guyuan_return_rel)
                if one_mode_return_rel is not None:
                    one_mode_return_errors_nonzero.append(one_mode_return_rel)

                if guyuan_comp_rel > guyuan_max:
                    guyuan_max = guyuan_comp_rel
                    guyuan_max_location = {
                        "internal_coupling": float(k_internal),
                        "boundary_outer_coupling": float(k_outer),
                        "omega": float(omega),
                    }
                if one_mode_comp_rel > one_mode_max:
                    one_mode_max = one_mode_comp_rel
                    one_mode_max_location = {
                        "internal_coupling": float(k_internal),
                        "boundary_outer_coupling": float(k_outer),
                        "omega": float(omega),
                    }

                group_condition = float(np.linalg.cond(d[:3, :3]))
                inner_condition = float(np.linalg.cond(d[:2, :2]))
                max_group_condition = max(max_group_condition, group_condition)
                max_inner_condition = max(max_inner_condition, inner_condition)

                records.append(
                    {
                        "internal_coupling": float(k_internal),
                        "boundary_outer_coupling": float(k_outer),
                        "omega": float(omega),
                        "full_outer_compliance": _complex_pair(full),
                        "direct_outer_compliance": _complex_pair(direct["compliance"]),
                        "nested_outer_compliance": _complex_pair(nested["compliance"]),
                        "direct_group_return": _complex_pair(direct["return"]),
                        "nested_group_return": _complex_pair(nested["return"]),
                        "full_vs_direct_compliance_absolute_error": full_direct_abs,
                        "direct_vs_nested_compliance_absolute_error": direct_nested_abs,
                        "direct_vs_nested_return_absolute_error": return_abs,
                        "guyan_outer_compliance_relative_error": guyuan_comp_rel,
                        "one_mode_outer_compliance_relative_error": one_mode_comp_rel,
                        "guyan_return_relative_error": guyuan_return_rel,
                        "one_mode_return_relative_error": one_mode_return_rel,
                        "group_dynamic_stiffness_condition_number": group_condition,
                        "inner_dynamic_stiffness_condition_number": inner_condition,
                    }
                )

    max_exact = max(
        max(exact_compliance_abs_errors),
        max(nested_direct_abs_errors),
        max(exact_return_abs_errors),
    )
    exact_status = (
        "HIERARCHICAL_REDUCTION_SUPPORTED_IN_REGIME"
        if max_exact <= tolerance
        else "HIERARCHICAL_REDUCTION_FAILED"
    )

    zero_outer_records = [r for r in records if r["boundary_outer_coupling"] == 0.0]
    zero_outer_max_return = max(
        max(abs(complex(*r["direct_group_return"])) for r in zero_outer_records),
        max(abs(complex(*r["nested_group_return"])) for r in zero_outer_records),
    )

    result = {
        "schema": RESULT_SCHEMA,
        "scope": "synthetic_si_fm4_hierarchical_closure_landscape_p0d_only",
        "status": "P0_D_DESCRIPTIVE_OR_STRUCTURAL_METHOD_LANDSCAPE",
        "experiment_plan": str(Path(plan_path).name),
        "general_protocol": "v0.7.4",
        "physical_thresholds_frozen": False,
        "real_system_evidence": False,
        "physical_inheritance_claim": False,
        "mfr14_activated": False,
        "system_scalar_chi_constructed": False,
        "atlas_used_for_parameter_selection": False,
        "record_count": len(records),
        "parameter_case_count": len(model["internal_coupling_values"]) * len(model["boundary_outer_coupling_values"]),
        "frequency_count_per_case": len(frequencies),
        "exact_closure": {
            "status": exact_status,
            "numerical_tolerance": tolerance,
            "tolerance_role": plan["exact_tolerance_role"],
            "maximum_full_vs_direct_compliance_absolute_error": max(exact_compliance_abs_errors),
            "maximum_direct_vs_nested_compliance_absolute_error": max(nested_direct_abs_errors),
            "maximum_direct_vs_nested_return_absolute_error": max(exact_return_abs_errors),
            "maximum_exact_identity_error": max_exact,
        },
        "zero_outer_coupling_control": {
            "record_count": len(zero_outer_records),
            "maximum_absolute_group_return": float(zero_outer_max_return),
        },
        "approximation_surfaces": {
            "guyan_outer_compliance_relative_error_all": _summarize_errors(guyuan_compliance_errors_all),
            "one_mode_outer_compliance_relative_error_all": _summarize_errors(one_mode_compliance_errors_all),
            "guyan_outer_compliance_relative_error_nonzero_outer_coupling": _summarize_errors(nonzero_outer_guyuan_compliance),
            "one_mode_outer_compliance_relative_error_nonzero_outer_coupling": _summarize_errors(nonzero_outer_one_mode_compliance),
            "guyan_return_relative_error_nonzero_reference": _summarize_errors(guyuan_return_errors_nonzero),
            "one_mode_return_relative_error_nonzero_reference": _summarize_errors(one_mode_return_errors_nonzero),
            "guyan_maximum_compliance_error_location": guyuan_max_location,
            "one_mode_maximum_compliance_error_location": one_mode_max_location,
            "binary_physical_pass_threshold_applied": False,
            "approximation_ordering_predeclared": False,
        },
        "conditioning": {
            "maximum_group_dynamic_stiffness_condition_number": max_group_condition,
            "maximum_inner_dynamic_stiffness_condition_number": max_inner_condition,
        },
        "interpretation_ceiling": {
            "exact_nested_schur": "formal/method-level hierarchical closure for the declared synthetic linear response quantities only",
            "approximation_surfaces": "P0-D descriptive Function/Limit map; no physical adequacy threshold or inheritance promotion is assigned",
            "cross_domain_or_universal_claim": False,
        },
        "records": records,
    }
    return result


def write_fm4_result(
    plan_path: str | Path = "substrate_inheritance/SI_FM4_HIERARCHICAL_CLOSURE_PLAN_v0.1.json",
    output_path: str | Path = "substrate_inheritance/results/SI_FM4_HIERARCHICAL_CLOSURE_RESULTS_v0.1.json",
) -> dict[str, Any]:
    result = run_fm4(plan_path)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = write_fm4_result()
    summary = {k: v for k, v in result.items() if k != "records"}
    print(json.dumps(summary, indent=2, sort_keys=True))
