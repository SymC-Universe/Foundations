#!/usr/bin/env python3
"""Published-central-value preflight for the DESI Stability Architecture lane.

This is NOT a substitute for the released DESI posterior chains. It uses
published Table V posterior means only to exercise the root logic and document
expected qualitative behavior before the full posterior is opened.
"""
from __future__ import annotations

from desi_scalar_gate import q_z, chi_delta_z, roots_on_grid

CASES = [
    ("DESI DR2 BAO, LambdaCDM", 0.2975, -1.0, 0.0),
    ("DESI DR2 BAO, wCDM", 0.2969, -0.916, 0.0),
    ("DESI DR2 + CMB, w0waCDM", 0.3530, -0.42, -1.75),
    ("DESI DR2 + CMB + Pantheon+, w0waCDM", 0.3114, -0.838, -0.62),
    ("DESI DR2 + CMB + Union3, w0waCDM", 0.3275, -0.667, -1.09),
    ("DESI DR2 + CMB + DESY5, w0waCDM", 0.3191, -0.752, -0.86),
]

def fmt(x):
    return "n/a" if x is None else f"{x:.9f}"

def main():
    print("# Published-central-value DESI preflight")
    print("# Source: DESI DR2 Results II, Table V, Phys. Rev. D 112, 083515 (2025)")
    for label, om0, w0, wa in CASES:
        rq = roots_on_grid(lambda z: q_z(z, om0, w0, wa))
        rc = roots_on_grid(lambda z: chi_delta_z(z, om0, w0, wa) - 1.0)
        delta = None if rq.primary is None or rc.primary is None else rq.primary - rc.primary
        print()
        print(label)
        print(f"  Omega_m0={om0:.6f} w0={w0:.6f} wa={wa:.6f}")
        print(f"  q0={float(q_z(0.0, om0, w0, wa)):.9f}")
        print(f"  chi_delta0={float(chi_delta_z(0.0, om0, w0, wa)):.9f}")
        print(f"  q_roots={','.join(f'{x:.9f}' for x in rq.all_roots) or 'none'}")
        print(f"  chi_roots={','.join(f'{x:.9f}' for x in rc.all_roots) or 'none'}")
        print(f"  primary_delta_z={fmt(delta)}")

if __name__ == "__main__":
    main()
