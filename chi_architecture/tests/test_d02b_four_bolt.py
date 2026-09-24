import numpy as np

from d02b_four_bolt import (
    analyze_half_power,
    parse_response_member,
    similar_chi,
)


def test_member_parser_handles_single_and_double_underscore_points():
    assert parse_response_member(
        "00_raw_exports/00_raw_exports/Amplitude/1234_10Nm_6mmSchraub_42.txt"
    ) == ("Amplitude", "1234_10Nm", 42)
    assert parse_response_member(
        "00_raw_exports/00_raw_exports/Phase/1234_10Nm_6mmSchraub__1.txt"
    ) == ("Phase", "1234_10Nm", 1)


def test_half_power_recovers_known_lorentzian_width():
    f = np.arange(1.0, 51201.0)
    f0 = 5000.0
    half_width = 10.0
    # Amplitude reaches 1/sqrt(2) at f0 +/- half_width.
    s = 1.0 / np.sqrt(1.0 + ((f - f0) / half_width) ** 2)
    r = analyze_half_power(s, 5000, 100)
    assert r["status"] == "ADMITTED"
    assert abs(r["peak_hz"] - 5000.0) < 1e-12
    assert abs(r["half_power_bandwidth_hz"] - 20.0) < 1e-8
    assert abs(r["chi"] - 0.002) < 1e-12


def test_half_power_refuses_near_equal_competing_peak():
    s = np.zeros(51200)
    s[4999] = 1.0
    s[5000] = 0.8
    s[5009] = 0.95
    s[5008] = 0.7
    s[5010] = 0.7
    r = analyze_half_power(s, 5000, 50)
    assert r["status"] == "NON_IDENTIFIABLE_MODAL_OVERLAP"


def test_similar_chi_uses_one_hz_resolution_and_no_percentage_tolerance():
    a = {"status": "ADMITTED", "chi": 0.0010, "chi_resolution_1Hz": 0.0001}
    b = {"status": "ADMITTED", "chi": 0.00108, "chi_resolution_1Hz": 0.00009}
    c = {"status": "ADMITTED", "chi": 0.0012, "chi_resolution_1Hz": 0.00009}
    assert similar_chi(a, b)[0] is True
    assert similar_chi(a, c)[0] is False
