from substrate_inheritance.discriminability_validation import (
    SCOPE,
    discriminability_strength_sweep,
    run_discriminability_validation,
)


def test_zero_mixing_is_perfectly_distinguishable_from_random_carriers():
    result = discriminability_strength_sweep(
        angle_scales=(0.0,), trials_per_scale=64, dimension=5, seed=20260840
    )
    row = result["rows"][0]
    assert row["planted_mean"] == 1.0
    assert row["threshold_free_auc_probability"] == 1.0
    assert row["mean_score_gap"] > 0.0


def test_strength_sweep_reports_failure_boundary_without_freezing_threshold():
    result = discriminability_strength_sweep(
        angle_scales=(0.0, 0.2, 0.8, 1.8), trials_per_scale=64, dimension=5, seed=20260840
    )
    rows = result["rows"]
    assert result["same_scalar_spectrum_at_every_strength"] is True
    assert result["strength_parameter_is_physical_threshold"] is False
    assert rows[-1]["planted_mean"] < rows[0]["planted_mean"]
    for row in rows:
        assert 0.0 <= row["threshold_free_auc_probability"] <= 1.0


def test_discriminability_record_is_not_physical_evidence():
    result = run_discriminability_validation()
    assert result["scope"] == SCOPE
    assert result["physical_thresholds_frozen"] is False
    assert result["real_system_evidence"] is False
