import numpy as np

from d02d_lumo import (
    adjudicate,
    bootstrap_median_ci,
    classify_direction,
    classify_location,
    dorg,
    projective_reference,
)


def campaign(scalar, organization):
    return {
        "status": "EVALUATED",
        "scalar": {"status": scalar},
        "organization": {"status": organization},
    }


def test_direction_organization_precedes_scalar():
    assert classify_direction(
        campaign("UNCHANGED", "CHANGED"),
        campaign("TRANSFORMED", "CHANGED"),
    ) == "ORGANIZATION_PRECEDES_SCALAR"


def test_direction_scalar_precedes_organization():
    assert classify_direction(
        campaign("TRANSFORMED", "UNCHANGED"),
        campaign("TRANSFORMED", "CHANGED"),
    ) == "SCALAR_PRECEDES_ORGANIZATION"


def test_direction_simultaneous_at_111_is_explicit():
    assert classify_direction(
        campaign("UNCHANGED", "UNCHANGED"),
        campaign("TRANSFORMED", "CHANGED"),
    ) == "SIMULTANEOUS_AT_111"


def test_location_requires_direction_agreement():
    assert classify_location("NEITHER_CHANGES", "NEITHER_CHANGES") == "NEITHER_CHANGES"
    assert classify_location("NEITHER_CHANGES", "ORGANIZATION_PRECEDES_SCALAR") == "ORDERING_NON_IDENTIFIABLE"


def test_program_survival_and_falsification_rules():
    assert adjudicate({
        "DAM3": "ORGANIZATION_PRECEDES_SCALAR",
        "DAM4": "ORGANIZATION_ONLY_THROUGH_111",
        "DAM6": "NEITHER_CHANGES",
    }) == "EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST"
    assert adjudicate({
        "DAM3": "SCALAR_PRECEDES_ORGANIZATION",
        "DAM4": "SCALAR_PRECEDES_ORGANIZATION",
        "DAM6": "NEITHER_CHANGES",
    }) == "EMPIRICAL_CLAIM_FALSIFIED"
    assert adjudicate({
        "DAM3": "SIMULTANEOUS_AT_010",
        "DAM4": "SIMULTANEOUS_AT_111",
        "DAM6": "SIMULTANEOUS_AT_111",
    }) == "EMPIRICAL_CLAIM_FALSIFIED"


def test_projective_mac_is_phase_invariant():
    v = np.array([1.0, 2.0j, -0.5], dtype=complex)
    v /= np.linalg.norm(v)
    ref = projective_reference([v, v * np.exp(1j * 0.7)])
    assert dorg(ref, v) < 1e-12


def test_bootstrap_is_deterministic():
    a = bootstrap_median_ci([1, 2, 3, 4, 5], seed=123)
    b = bootstrap_median_ci([1, 2, 3, 4, 5], seed=123)
    assert a == b
