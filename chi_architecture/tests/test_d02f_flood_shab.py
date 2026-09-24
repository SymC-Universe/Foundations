import numpy as np

from d02f_flood_shab import (
    dissimilarity,
    organization_margin,
    ordering,
    scalar_margin,
    water_bin,
)


def test_water_bins_are_frozen():
    assert water_bin(3.0) == "E1_LOW"
    assert water_bin(3.4025) == "E1_LOW"
    assert water_bin(3.50) == "E2"
    assert water_bin(3.535) == "E2"
    assert water_bin(4.0) == "E3"
    assert water_bin(4.7275) == "E3"
    assert water_bin(5.0) == "E4_HIGH"


def test_complex_mode_dissimilarity_is_global_phase_invariant():
    v=np.array([1+0j,2+1j,-0.5+0.3j],complex)
    v=v/np.linalg.norm(v)
    w=v*np.exp(1j*1.234)
    assert abs(dissimilarity(v,w)) < 1e-12


def test_scalar_margin_sign():
    controls=np.linspace(0.01,0.02,30)
    assert scalar_margin(0.015,controls) < 0
    assert scalar_margin(0.03,controls) > 0
    assert scalar_margin(0.001,controls) > 0


def test_organization_margin_detects_rotated_vector():
    controls=[]
    base=np.array([1+0j,0+0j,0+0j])
    for k in range(30):
        eps=1e-5*(k+1)
        v=np.array([1+0j,eps+0j,0+0j])
        controls.append(v/np.linalg.norm(v))
    event=np.array([0+0j,1+0j,0+0j])
    margin, d, threshold=organization_margin(event,controls)
    assert margin > 0
    assert d > threshold


def test_ordering_classes():
    scalar={x:"UNCHANGED" for x in ("E1_LOW","E2","E3","E4_HIGH")}
    org=dict(scalar)
    org["E2"]="CHANGED"
    scalar["E3"]="TRANSFORMED"
    assert ordering(scalar,org)["outcome"]=="ORGANIZATION_PRECEDES_SCALAR"

    scalar={x:"UNCHANGED" for x in ("E1_LOW","E2","E3","E4_HIGH")}
    org=dict(scalar)
    scalar["E2"]="TRANSFORMED"
    org["E3"]="CHANGED"
    assert ordering(scalar,org)["outcome"]=="SCALAR_PRECEDES_ORGANIZATION"

    scalar={x:"UNCHANGED" for x in ("E1_LOW","E2","E3","E4_HIGH")}
    org=dict(scalar)
    assert ordering(scalar,org)["outcome"]=="NEITHER_CHANGES"
