#!/usr/bin/env python3
import json
import math
import platform
from pathlib import Path

import numpy as np
import qutip

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "qutip_runtime_result_v01.json"

GAMMA = 0.37
TLIST = np.linspace(0.0, 5.0, 101)
ANALYTIC_GATE = 1e-7
TRACE_GATE = 1e-10
HERMITICITY_GATE = 1e-10
POSITIVITY_GATE = -1e-9

sx = qutip.sigmax()
sz = qutip.sigmaz()
ket_plus = (qutip.basis(2, 0) + qutip.basis(2, 1)).unit()
rho0 = qutip.ket2dm(ket_plus)
H = 0.0 * sz
c_ops = [math.sqrt(GAMMA) * sz]

result = qutip.mesolve(
    H,
    rho0,
    TLIST,
    c_ops=c_ops,
    e_ops=[sx],
    options={"atol": 1e-12, "rtol": 1e-10, "store_states": True},
)

observed = np.asarray(result.expect[0], dtype=float)
expected = np.exp(-2.0 * GAMMA * TLIST)
max_abs_error = float(np.max(np.abs(observed - expected)))

trace_errors = []
hermiticity_residuals = []
minimum_eigenvalues = []
for state in result.states:
    arr = state.full()
    trace_errors.append(abs(complex(np.trace(arr)) - 1.0))
    hermiticity_residuals.append(float(np.linalg.norm(arr - arr.conj().T, ord="fro")))
    minimum_eigenvalues.append(float(np.min(np.linalg.eigvalsh(0.5 * (arr + arr.conj().T)))))

max_trace_error = float(max(trace_errors))
max_hermiticity_residual = float(max(hermiticity_residuals))
min_eigenvalue = float(min(minimum_eigenvalues))

q0 = qutip.__version__ == "5.3.1"
q1 = max_abs_error <= ANALYTIC_GATE
q2 = (
    max_trace_error <= TRACE_GATE
    and max_hermiticity_residual <= HERMITICITY_GATE
    and min_eigenvalue >= POSITIVITY_GATE
)

payload = {
    "schema": "stability-arc-qutip-runtime-admission-v0.1",
    "scope": "RUNTIME_ADMISSION_ONLY",
    "scientific_runtime_status": "PASS_Q0_Q1_Q2" if (q0 and q1 and q2) else "FAIL_Q0_Q1_Q2",
    "criteria": {
        "Q0": {
            "status": "PASS" if q0 else "FAIL",
            "required_qutip_version": "5.3.1",
            "observed_qutip_version": qutip.__version__,
        },
        "Q1": {
            "status": "PASS" if q1 else "FAIL",
            "gamma": GAMMA,
            "n_times": int(TLIST.size),
            "t_min": float(TLIST[0]),
            "t_max": float(TLIST[-1]),
            "max_abs_error": max_abs_error,
            "gate": ANALYTIC_GATE,
        },
        "Q2": {
            "status": "PASS" if q2 else "FAIL",
            "max_trace_error": max_trace_error,
            "trace_gate": TRACE_GATE,
            "max_hermiticity_frobenius": max_hermiticity_residual,
            "hermiticity_gate": HERMITICITY_GATE,
            "minimum_density_eigenvalue": min_eigenvalue,
            "positivity_gate": POSITIVITY_GATE,
        },
    },
    "environment": {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "qutip": qutip.__version__,
        "platform": platform.platform(),
    },
    "samples": {
        "t": [float(v) for v in TLIST],
        "observed_sigma_x": [float(v) for v in observed],
        "analytic_sigma_x": [float(v) for v in expected],
    },
    "interpretation_firewall": (
        "A pass only admits this runtime for later independent QuTiP work. "
        "It does not reproduce the historical notebook or establish agreement with Stability Arc results."
    ),
}

OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(payload, indent=2, sort_keys=True))
raise SystemExit(0 if (q0 and q1 and q2) else 1)
