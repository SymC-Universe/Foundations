#!/usr/bin/env python3
import hashlib
import json
import platform
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "dephasing_d3_identifier_remediation_v011.json"
REPO = ROOT.parents[2]
PARENT = REPO / "stability_arc/measurement_conditioned/dephasing_augmented_v01/dephasing_augmented_planar_transfer_v01.py"
FAILURE = REPO / "stability_arc/measurement_conditioned/dephasing_augmented_v01/FAILURE_SIGNAL_REPORT_v0.1.md"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

# M0 parent identity.
parent_sha = sha256(PARENT)
failure_sha = sha256(FAILURE)
M0 = bool(parent_sha and failure_sha)

# Independent symbolic reconstruction of the frozen D3 target.
g, gp, k, eta, w, th = sp.symbols("g gp k eta w th", positive=True, real=True)
rx, rz, u, v = sp.symbols("rx rz u v", real=True)
sn, cs = sp.sin(th), sp.cos(th)
a = g / 2 + gp
b = g
q = eta * k

# Frozen laboratory x-z tangent from parent preregistration.
A_lab = sp.Matrix([
    [-a - k * cs**2, w + k * sn * cs],
    [-w + k * sn * cs, -b - k * sn**2],
])

mu = sn * rx + cs * rz
# Same-noise stochastic x-z tangent from measurement Jacobian.
B_lab = -sp.sqrt(2 * q) * sp.Matrix([
    [rx * sn + mu, rx * cs],
    [rz * sn, rz * cs + mu],
])

n = sp.Matrix([sn, cs])
r = sp.Matrix([rx, rz])
hvec = n - mu * r
A_rec_lab = A_lab - 2 * q * hvec * n.T

# Measurement-aligned orthogonal transform and inverse coordinate substitution.
Q = sp.Matrix([[sn, cs], [cs, -sn]])
subs_uv = {rx: sn * u + cs * v, rz: cs * u - sn * v}

A_phys_transformed = sp.simplify(Q * A_lab * Q.T)
B_transformed = sp.simplify(Q * B_lab.subs(subs_uv) * Q.T)
A_rec_transformed = sp.simplify(Q * A_rec_lab.subs(subs_uv) * Q.T)

p = a * sn**2 + b * cs**2
d = k + a * cs**2 + b * sn**2
h = (b - a) * sn * cs

A_phys_target = sp.Matrix([[-p, h - w], [h + w, -d]])
B_target = -sp.sqrt(2 * q) * sp.Matrix([[2 * u, 0], [v, u]])
A_rec_target = A_phys_target + sp.Matrix([[-2 * q * (1 - u**2), 0], [2 * q * u * v, 0]])

phys_residuals = [sp.trigsimp(A_phys_transformed[i, j] - A_phys_target[i, j]) for i in range(2) for j in range(2)]
stoch_residuals = [sp.trigsimp(B_transformed[i, j] - B_target[i, j]) for i in range(2) for j in range(2)]
record_residuals = [sp.trigsimp(A_rec_transformed[i, j] - A_rec_target[i, j]) for i in range(2) for j in range(2)]

M1 = all(r == 0 for r in phys_residuals)
M2 = all(r == 0 for r in stoch_residuals)
M3 = all(r == 0 for r in record_residuals)
M4 = isinstance(M1, bool) and isinstance(M2, bool) and isinstance(M3, bool) and M1 and M2 and M3

M5 = (
    sp.trigsimp(p.subs(gp, 0) - g * (1 + cs**2) / 2) == 0
    and sp.trigsimp(d.subs(gp, 0) - (k + g * (1 + sn**2) / 2)) == 0
    and sp.trigsimp(h.subs(gp, 0) - g * sp.sin(2 * th) / 4) == 0
)

status = "PASS_D3_IDENTIFIER_REMEDIATION" if all([M0, M1, M2, M3, M4, M5]) else "D3_IDENTIFIER_REMEDIATION_FAILURE"
result = {
    "schema": "stability-arc-dephasing-d3-identifier-remediation-v0.1.1",
    "phase_status": status,
    "environment": {"python": platform.python_version(), "sympy": sp.__version__},
    "parent": {"code_sha256": parent_sha, "failure_report_sha256": failure_sha},
    "criteria": {
        "M0": {"status": "PASS" if M0 else "FAIL"},
        "M1": {"status": "PASS" if M1 else "FAIL", "residuals": [str(r) for r in phys_residuals]},
        "M2": {"status": "PASS" if M2 else "FAIL", "residuals": [str(r) for r in stoch_residuals]},
        "M3": {"status": "PASS" if M3 else "FAIL", "residuals": [str(r) for r in record_residuals]},
        "M4": {"status": "PASS" if M4 else "FAIL", "types": [type(M1).__name__, type(M2).__name__, type(M3).__name__]},
        "M5": {"status": "PASS" if M5 else "FAIL"},
    },
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
