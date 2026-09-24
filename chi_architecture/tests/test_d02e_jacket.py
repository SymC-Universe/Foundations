import numpy as np
from scipy.signal import csd

from d02e_jacket import (
    WINDOW_LOW_HZ,
    WINDOW_HIGH_HZ,
    vectorized_fdd_window,
    domain_outcome,
    classify_location,
)


def test_vectorized_fdd_matches_pairwise_csd_eigenvalue_and_subspace():
    rng=np.random.default_rng(7)
    n=20000
    t=np.arange(n)/1600.0
    base=np.sin(2*np.pi*8.7890625*t)
    x=np.column_stack([
        (1+0.05*k)*base + 0.05*rng.standard_normal(n)
        for k in range(4)
    ])
    f,s1,v=vectorized_fdd_window(x)
    q=int(np.argmax(s1))
    target=float(f[q])

    mat=np.zeros((4,4),dtype=complex)
    for i in range(4):
        for j in range(i,4):
            ff,p=csd(x[:,i],x[:,j],fs=1600.0,window="hann",nperseg=8192,
                     noverlap=4096,detrend="constant",scaling="density")
            idx=int(np.argmin(abs(ff-target)))
            mat[i,j]=p[idx]
            mat[j,i]=np.conjugate(p[idx])
    vals,vecs=np.linalg.eigh(mat)
    k=int(np.argmax(np.real(vals)))
    vv=vecs[:,k]/np.linalg.norm(vecs[:,k])
    assert np.isclose(s1[q],np.real(vals[k]),rtol=1e-10,atol=1e-12)
    assert abs(np.vdot(v[q],vv))**2 > 1-1e-10


def test_tracking_window_is_frozen_around_selected_baseline_family():
    assert np.isclose(WINDOW_LOW_HZ,0.95*8.7890625)
    assert np.isclose(WINDOW_HIGH_HZ,1.05*8.7890625)


def test_location_ordering_scalar_first():
    states={
      "9Nm":{"scalar_status":"TRANSFORMED","organization_status":"UNCHANGED"},
      "6Nm":{"scalar_status":"TRANSFORMED","organization_status":"CHANGED"},
      "NoBolt":{"scalar_status":"TRANSFORMED","organization_status":"CHANGED"},
    }
    assert classify_location(states)["outcome"]=="SCALAR_PRECEDES_ORGANIZATION"


def test_location_ordering_blocks_later_onset_after_missing_state():
    states={
      "9Nm":{"scalar_status":"NON_IDENTIFIABLE","organization_status":"UNCHANGED"},
      "6Nm":{"scalar_status":"TRANSFORMED","organization_status":"CHANGED"},
      "NoBolt":{"scalar_status":"TRANSFORMED","organization_status":"CHANGED"},
    }
    assert classify_location(states)["outcome"]=="ORDERING_NON_IDENTIFIABLE"


def test_domain_rules_are_symmetric_three_of_four():
    assert domain_outcome({
      "level_1":"ORGANIZATION_PRECEDES_SCALAR",
      "level_2":"ORGANIZATION_CHANGES_SCALAR_DOES_NOT",
      "level_3":"ORGANIZATION_PRECEDES_SCALAR",
      "level_4":"SIMULTANEOUS_WITHIN_FROZEN_RESOLUTION",
    })=="SUPPORT"
    assert domain_outcome({
      "level_1":"SCALAR_PRECEDES_ORGANIZATION",
      "level_2":"SCALAR_CHANGES_ORGANIZATION_DOES_NOT",
      "level_3":"SCALAR_PRECEDES_ORGANIZATION",
      "level_4":"SIMULTANEOUS_WITHIN_FROZEN_RESOLUTION",
    })=="ADVERSE"


def test_parser_skips_irregular_width_rows():
    from d02e_jacket import parse_response_csv
    header="," + ",".join(f"sensor_{i}" for i in range(1,25)) + "\n"
    good="0," + ",".join("1.0" for _ in range(24)) + "\n"
    bad="0,1,2,3,4,5\n"
    raw=(header + good + bad + good).encode("utf-8")
    names,x=parse_response_csv(raw)
    assert len(names)==24
    assert x.shape==(2,24)
