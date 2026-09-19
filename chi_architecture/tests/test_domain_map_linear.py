import json
from pathlib import Path

import numpy as np
import pytest

from domain_map_linear import (
    DomainMapRefusal,
    normalized_sdof_metrics,
    normalized_sdof_trajectory,
    physical_sdof_from_chi,
    run_d01a,
)


PLAN_PATH = Path("chi_architecture/D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json")


def load_plan():
    return json.loads(PLAN_PATH.read_text(encoding="utf-8"))


def test_normalized_solution_respects_initial_conditions():
    tau = np.linspace(0.0, 5.0, 1001)
    for chi in (0.0, 0.5, 1.0, 2.0):
        x, u = normalized_sdof_trajectory(chi, tau, x0=0.7, u0=-0.2)
        assert x[0] == pytest.approx(0.7, abs=1e-12)
        assert u[0] == pytest.approx(-0.2, abs=1e-12)


def test_regime_classification_is_generated_from_native_roots():
    tau = np.linspace(0.0, 10.0, 1001)
    assert normalized_sdof_metrics(0.5, tau, x0=1.0, u0=0.0)["regime"] == "UNDERDAMPED"
    assert normalized_sdof_metrics(1.0, tau, x0=1.0, u0=0.0)["regime"] == "CRITICAL"
    assert normalized_sdof_metrics(2.0, tau, x0=1.0, u0=0.0)["regime"] == "OVERDAMPED"


def test_same_chi_collapses_after_native_nondimensionalization():
    tau = np.linspace(0.0, 20.0, 4001)
    traces = []
    for omega0 in (0.5, 1.0, 2.0, 5.0):
        r = physical_sdof_from_chi(omega0, 0.65, tau, x0=1.0, normalized_u0=0.0)
        traces.append((r["x"], r["normalized_velocity"]))
    ref_x, ref_u = traces[0]
    for x, u in traces[1:]:
        assert np.max(np.abs(x - ref_x)) < 1e-12
        assert np.max(np.abs(u - ref_u)) < 1e-12


def test_dimensionless_slowest_decay_rate_peaks_at_critical_boundary_on_declared_grid():
    tau = np.linspace(0.0, 10.0, 1001)
    chis = np.arange(0.0, 4.0 + 0.05, 0.05)
    rates = [normalized_sdof_metrics(float(c), tau, x0=1.0, u0=0.0)["slowest_dimensionless_decay_rate"] for c in chis]
    best = int(np.argmax(rates))
    assert chis[best] == pytest.approx(1.0, abs=1e-12)
    assert rates[best] == pytest.approx(1.0, abs=1e-12)


def test_zero_crossings_distinguish_oscillatory_and_nonoscillatory_regions():
    tau = np.linspace(0.0, 30.0, 6001)
    under = normalized_sdof_metrics(0.5, tau, x0=1.0, u0=0.0)
    critical = normalized_sdof_metrics(1.0, tau, x0=1.0, u0=0.0)
    over = normalized_sdof_metrics(2.0, tau, x0=1.0, u0=0.0)
    assert under["zero_crossing_count"] > 0
    assert critical["zero_crossing_count"] == 0
    assert over["zero_crossing_count"] == 0


def test_negative_chi_refuses_passive_anchor():
    tau = np.linspace(0.0, 1.0, 11)
    with pytest.raises(DomainMapRefusal):
        normalized_sdof_trajectory(-0.1, tau, x0=1.0, u0=0.0)


def test_plan_is_atlas_blind_and_scalar_is_not_forced_in_coupled_extension():
    plan = load_plan()
    assert plan["atlas_blind"] is True
    assert plan["cross_domain_alignment_used_for_parameter_or_metric_selection"] is False
    d01b = next(p for p in plan["phases"] if p["id"] == "D01B_COUPLED_2DOF")
    assert d01b["coordinate_policy"]["master_scalar_predeclared"] is False
    assert d01b["coordinate_policy"]["no_admissible_scalar_allowed"] is True


def test_runner_retains_full_declared_grid_and_both_initial_conditions():
    result = run_d01a(load_plan())
    assert result["status"] == "P0_DOMAIN_MAP_EXACT_ANCHOR"
    assert result["atlas_blind"] is True
    assert result["cross_domain_confirmation"] is False
    assert result["chi_grid"][0] == 0.0
    assert result["chi_grid"][-1] == 4.0
    assert len(result["chi_grid"]) == 81
    assert len(result["normalized_initial_conditions"]) == 2
    assert len(result["records"]) == 162
    assert len(result["scale_collapse"]) == 162
