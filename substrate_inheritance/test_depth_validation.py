import numpy as np

from substrate_inheritance.depth_validation import (
    SCOPE,
    finite_surface_green,
    inheritance_depth_curve,
    recursive_surface_green,
    run_depth_validation,
    semi_infinite_surface_green,
)


def test_finite_matrix_and_recursive_surface_green_agree():
    onsite = 3.5 - 0.2j
    for length in (1, 2, 4, 8, 16):
        direct = finite_surface_green(length, onsite, 0.8)
        recursive = recursive_surface_green(length, onsite, 0.8)
        assert abs(direct - recursive) < 1e-12


def test_semi_infinite_solution_satisfies_fixed_point_equation():
    onsite = 3.5 - 0.2j
    hopping = 0.8
    g = semi_infinite_surface_green(onsite, hopping)
    residual = g - 1.0 / (onsite - hopping**2 * g)
    assert abs(residual) < 1e-12


def test_depth_curve_converges_toward_semi_infinite_embedding():
    result = inheritance_depth_curve()
    errors = np.array([row["relative_error_to_semi_infinite"] for row in result["depth_curve"]])
    residuals = np.array([row["matrix_vs_recursive_residual"] for row in result["depth_curve"]])
    assert errors[-1] < errors[0]
    assert errors[-1] < 1e-10
    assert np.max(residuals) < 1e-12


def test_depth_validation_is_not_physical_evidence():
    result = run_depth_validation()
    assert result["scope"] == SCOPE
    assert result["physical_thresholds_frozen"] is False
    assert result["real_system_evidence"] is False
