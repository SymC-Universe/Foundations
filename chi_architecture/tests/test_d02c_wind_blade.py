from datetime import datetime, timezone, timedelta

import numpy as np

from d02c_wind_blade import (
    build_baseline_track,
    classify_order,
    mac_dissimilarity,
    scalar_change_status,
    scalar_control_envelope,
    scalar_from_row,
)


def row(ts, f, damping=1.0, std=0.1, size=25):
    return {
        "timestamp": ts,
        "frequency": f,
        "std_frequency": 0.001,
        "damping_pct": damping,
        "std_damping_pct": std,
        "size": size,
        "algorithm": "lscf",
    }


def test_scalar_percent_convention_and_interval():
    r = scalar_from_row(row(datetime.now(timezone.utc), 2.0, damping=1.0, std=0.1, size=25))
    assert r["status"] == "ADMITTED"
    assert abs(r["chi"] - 0.01) < 1e-12
    assert abs(r["se_chi"] - 0.0002) < 1e-12


def test_scalar_control_envelope_is_fail_closed():
    base = [row(datetime.now(timezone.utc), 2.0, damping=1.0) for _ in range(10)]
    control = [row(datetime.now(timezone.utc), 2.0, damping=1.0) for _ in range(20)]
    env = scalar_control_envelope(base, control)
    assert env["status"] == "ADEQUATE"
    unchanged = scalar_from_row(row(datetime.now(timezone.utc), 2.0, damping=1.05))
    changed = scalar_from_row(row(datetime.now(timezone.utc), 2.0, damping=3.0, std=0.01))
    assert scalar_change_status(unchanged, env) == "UNCHANGED"
    assert scalar_change_status(changed, env) == "TRANSFORMED"


def test_complex_mac_is_global_phase_invariant():
    v = np.array([1.0 + 0j, 1j, 0.5 - 0.2j])
    w = np.exp(1j * 1.234) * v
    assert mac_dissimilarity(v, w) < 1e-12


def test_onset_missing_before_change_is_nonidentifiable():
    out = classify_order(
        ["UNCHANGED", "NON_IDENTIFIABLE", "TRANSFORMED"] + ["UNCHANGED"] * 9,
        ["UNCHANGED", "CHANGED"] + ["UNCHANGED"] * 10,
        ["UNCHANGED", "CHANGED"] + ["UNCHANGED"] * 10,
    )
    assert out["outcome"] == "ORDERING_NON_IDENTIFIABLE"


def test_thermal_firewall_can_preclude_apparent_org_first():
    out = classify_order(
        ["UNCHANGED"] * 3 + ["TRANSFORMED"] + ["UNCHANGED"] * 8,
        ["UNCHANGED"] * 5 + ["CHANGED"] + ["UNCHANGED"] * 6,
        ["UNCHANGED", "CHANGED"] + ["UNCHANGED"] * 10,
    )
    assert out["outcome"] == "NATIVE_MEASUREMENT_SENSITIVITY_PRECLUDES_ORDERING"


def test_baseline_track_selects_lowest_stable_family():
    start = datetime(2022, 1, 1, 0, 5, tzinfo=timezone.utc)
    targets = [start + timedelta(minutes=10*i) for i in range(12)]
    rows = []
    for i, ts in enumerate(targets):
        rows.append(row(ts, 1.5 + 0.001*i))
        rows.append(row(ts, 2.1 + 0.002*i))
    track = build_baseline_track(rows, targets)
    assert track["presence"] == 12
    assert track["median_frequency"] < 1.6
