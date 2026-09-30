import importlib.util
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("gate", HERE / "desi_scalar_gate.py")
gate = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gate
spec.loader.exec_module(gate)

def test_lcdm_identity_pointwise():
    om0 = 0.3
    z = np.linspace(0, 3, 401)
    q = gate.q_z(z, om0, -1.0, 0.0)
    chi = gate.chi_delta_z(z, om0, -1.0, 0.0)
    # In flat late-time LCDM: q = 0 iff chi_delta = 1.
    rq = gate.roots_on_grid(lambda x: gate.q_z(x, om0, -1.0, 0.0))
    rc = gate.roots_on_grid(lambda x: gate.chi_delta_z(x, om0, -1.0, 0.0) - 1.0)
    assert rq.primary is not None and rc.primary is not None
    assert abs(rq.primary - rc.primary) < 1e-10

def test_lcdm_root_matches_analytic_solution():
    om0 = 0.3
    expected = (2.0 * (1.0 - om0) / om0) ** (1.0 / 3.0) - 1.0
    rq = gate.roots_on_grid(lambda x: gate.q_z(x, om0, -1.0, 0.0))
    rc = gate.roots_on_grid(lambda x: gate.chi_delta_z(x, om0, -1.0, 0.0) - 1.0)
    assert abs(rq.primary - expected) < 1e-10
    assert abs(rc.primary - expected) < 1e-10

def test_current_chi_definition():
    om0 = 0.3
    assert abs(gate.chi_delta_z(0.0, om0, -1.0, 0.0) - np.sqrt(2.0/(3.0*om0))) < 1e-12
