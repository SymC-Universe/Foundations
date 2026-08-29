#!/usr/bin/env python3
import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "state_geometry_admissibility_v01.json"
STAGE_A = RESULTS / "stageA_state_geometry_selection.json"
STAGE_A_SHA = RESULTS / "stageA_state_geometry_selection.sha256"

SEED = 2026082913
N_PER_STRATUM = 50000
MAX_FREEZE = 128
MAP_TOL = 1e-8
C1_TOL = 1e-8
RH_TOL = 1e-9
RECON_TOL = 2e-10
SHELLS = [
    ("R1", 0.90, 0.95),
    ("R2", 0.95, 0.98),
    ("R3", 0.98, 0.995),
    ("R4", 0.995, 0.9999),
]
SIGNS = ["NEG", "POS"]

SYM_BASIS = [
    np.array([[1.0, 0.0], [0.0, 0.0]], float),
    np.array([[0.0, 1.0], [1.0, 0.0]], float),
    np.array([[0.0, 0.0], [0.0, 1.0]], float),
]


def relabs(a, b):
    return abs(a - b) / max(1.0, abs(a), abs(b))


def max_abs(a):
    a = np.asarray(a)
    return 0.0 if a.size == 0 else float(np.max(np.abs(a)))


def c3_coeff(g, k, q, x, z, record=False):
    if not record:
        A = 2.0 * (3.0*g + 2.0*k - 2.0*q*x*x - 10.0*q*z*z)
        B = 16.0*q*x*z*(g+k-3.0*q*z*z)
        C = (g-4.0*q*z*z)*(3.0*g+2.0*k-8.0*q*z*z)*(g+2.0*k-2.0*q*z*z)
    else:
        A = 2.0 * (3.0*g + 2.0*k + 4.0*q - 2.0*q*x*x - 14.0*q*z*z)
        B = 4.0*q*x*z*(7.0*g+6.0*k+8.0*q-30.0*q*z*z)
        C = (g+2.0*k-2.0*q*z*z)*(g+2.0*q-6.0*q*z*z)*(3.0*g+2.0*k+4.0*q-12.0*q*z*z)
    return A, B, C


def c3_value_norm(g, k, q, x, z, w, record=False):
    A, B, C = c3_coeff(g, k, q, x, z, record=record)
    v = (A*w+B)*w+C
    scale = max(1.0, abs(A)*w*w + abs(B)*w + abs(C))
    return float(v), float(v/scale)


def c1_phys(g, k, q, z):
    return 4.5*g + 3.0*k - 14.0*q*z*z


def generate_all():
    rng = np.random.default_rng(SEED)
    strata = []
    for shell, lo, hi in SHELLS:
        for orient in SIGNS:
            k = 10.0 ** rng.uniform(math.log10(0.2), math.log10(100.0), N_PER_STRATUM)
            eta = rng.uniform(0.001, 0.95, N_PER_STRATUM)
            w = 10.0 ** rng.uniform(-3.0, 3.0, N_PER_STRATUM)
            r = rng.uniform(lo, hi, N_PER_STRATUM)
            phi = rng.uniform(0.0, math.pi/2.0, N_PER_STRATUM)
            sign_z = np.where(rng.integers(0, 2, N_PER_STRATUM) == 0, -1.0, 1.0)
            ax = r*np.cos(phi)
            az = r*np.sin(phi)
            z = sign_z*az
            sign_x = -sign_z if orient == "NEG" else sign_z
            x = sign_x*ax
            q = eta*k
            strata.append({
                "shell": shell, "lo": lo, "hi": hi, "orientation": orient,
                "gamma": np.ones(N_PER_STRATUM), "kappa": k, "eta": eta,
                "omega": w, "r": r, "phi": phi, "x": x, "z": z, "q": q,
            })
    return strata


def stratum_hash(s):
    h = hashlib.sha256()
    h.update(f"{s['shell']}|{s['orientation']}|{N_PER_STRATUM}|{SEED}\n".encode())
    for key in ["gamma","kappa","eta","omega","r","phi","x","z","q"]:
        h.update(key.encode()+b"\0")
        h.update(np.asarray(s[key], dtype="<f8").tobytes())
    return h.hexdigest()


def active_matrices(f, record=False):
    g,k,q,x,z,w = f["gamma"],f["kappa"],f["q"],f["x"],f["z"],f["omega"]
    s = math.sqrt(2.0*q)
    A = np.array([[-(g/2.0+k),w],[-w,-g]], float)
    if record:
        A += np.array([[0.0,2.0*q*z*x],[0.0,-2.0*q*(1.0-z*z)]], float)
    B = np.array([[-s*z,-s*x],[0.0,-2.0*s*z]], float)
    return A,B


def moment_action(A,B,P):
    return A@P + P@A.T + B@P@B.T


def sym_coords(P):
    return np.array([P[0,0],0.5*(P[0,1]+P[1,0]),P[1,1]], float)


def sym_generator(A,B):
    return np.column_stack([sym_coords(moment_action(A,B,E)) for E in SYM_BASIS])


def rh(G,R):
    tr=float(np.trace(G))
    c1=-tr
    c2=0.5*(tr*tr-float(np.trace(G@G)))
    c3=-float(np.linalg.det(G))
    mh=c1*c2-c3
    m={"m1":c1/R,"m2":c2/R**2,"m3":c3/R**3,"mh":mh/R**3}
    if all(v>RH_TOL for v in m.values()): cls="STABLE"
    elif any(v<-RH_TOL for v in m.values()): cls="UNSTABLE"
    else: cls="BOUNDARY"
    return {"c1":c1,"c2":c2,"c3":c3,"mh_raw":mh,"margins":m,"class":cls}


# G0 deterministic generator replay.
A = generate_all()
B = generate_all()
hashes_a = {f"{s['shell']}_{s['orientation']}": stratum_hash(s) for s in A}
hashes_b = {f"{s['shell']}_{s['orientation']}": stratum_hash(s) for s in B}
G0 = hashes_a == hashes_b and len(A) == 8

# Stage A c1+c3 only.
stratum_summary = {}
frozen_rows = []
geometry_ok = True
orientation_zero = 0
for s in A:
    key=f"{s['shell']}_{s['orientation']}"
    eligible=[]
    for i in range(N_PER_STRATUM):
        g=1.0; k=float(s["kappa"][i]); q=float(s["q"][i]); x=float(s["x"][i]); z=float(s["z"][i]); w=float(s["omega"][i]); r=float(s["r"][i])
        prod=x*z
        if prod == 0.0:
            orientation_zero += 1
        if not (s["lo"] <= r < s["hi"]): geometry_ok=False
        if s["orientation"] == "NEG" and prod > 0.0: geometry_ok=False
        if s["orientation"] == "POS" and prod < 0.0: geometry_ok=False
        R=g+k+w+q
        c1n=c1_phys(g,k,q,z)/R
        _,sp=c3_value_norm(g,k,q,x,z,w,False)
        _,sr=c3_value_norm(g,k,q,x,z,w,True)
        if c1n>C1_TOL and sp>MAP_TOL and sr<-MAP_TOL:
            row={
                "id":f"{key}_{i+1:05d}","shell":s["shell"],"orientation":s["orientation"],"index":i+1,
                "gamma":g,"kappa":k,"eta":float(s["eta"][i]),"omega":w,"r":r,"x":x,"z":z,"q":q,
                "abs_z":abs(z),"xz":prod,"c1_phys_norm":c1n,"c3_phys_norm":sp,"c3_record_norm":sr,
            }
            eligible.append(row)
    freeze=eligible[:MAX_FREEZE]
    frozen_rows.extend(freeze)
    stratum_summary[key]={"eligible_count":len(eligible),"frozen_count":len(freeze),"generator_sha256":hashes_a[key]}

stage_payload={
    "schema":"stability-arc-state-geometry-stageA-v0.1","seed":SEED,"n_per_stratum":N_PER_STRATUM,
    "thresholds":{"C1_TOL":C1_TOL,"MAP_TOL":MAP_TOL},"strata":stratum_summary,"frozen":frozen_rows,
}
stage_bytes=json.dumps(stage_payload,indent=2,sort_keys=True).encode()+b"\n"
STAGE_A.write_bytes(stage_bytes)
stage_sha=hashlib.sha256(stage_bytes).hexdigest()
STAGE_A_SHA.write_text(stage_sha+"  stageA_state_geometry_selection.json\n")
digest_ok=hashlib.sha256(STAGE_A.read_bytes()).hexdigest()==stage_sha
G1=digest_ok
G2=geometry_ok

# Registered H8E/H8L from Stage A counts.
high_count=sum(v["eligible_count"] for k,v in stratum_summary.items() if k.startswith("R3_") or k.startswith("R4_"))
low_count=sum(v["eligible_count"] for k,v in stratum_summary.items() if k.startswith("R1_") or k.startswith("R2_"))
H8E = high_count >= 20
H8L = low_count == 0

# G3 replay exact Stage A coordinates before full reveal.
frozen=json.loads(STAGE_A.read_text())
replay_fail=[]
for f in frozen["frozen"]:
    R=f["gamma"]+f["kappa"]+f["omega"]+f["q"]
    c1n=c1_phys(f["gamma"],f["kappa"],f["q"],f["z"])/R
    _,sp=c3_value_norm(f["gamma"],f["kappa"],f["q"],f["x"],f["z"],f["omega"],False)
    _,sr=c3_value_norm(f["gamma"],f["kappa"],f["q"],f["x"],f["z"],f["omega"],True)
    if not (c1n>C1_TOL and sp>MAP_TOL and sr<-MAP_TOL):
        replay_fail.append(f["id"])
G3=len(replay_fail)==0

# Stage B full reveal.
recon=[]
boundaries=[]
counter=[]
correct=0
blockers={"m2":0,"mh":0}
max_recon=0.0
stageB=[]
if G0 and G1 and G2 and G3:
    for f in frozen["frozen"]:
        Ap,Bm=active_matrices(f,False); Ar,_=active_matrices(f,True)
        Gp=sym_generator(Ap,Bm); Gr=sym_generator(Ar,Bm)
        R=f["gamma"]+f["kappa"]+f["omega"]+f["q"]
        rp=rh(Gp,R); rr=rh(Gr,R)
        c1e=c1_phys(f["gamma"],f["kappa"],f["q"],f["z"])
        c3pe,_=c3_value_norm(f["gamma"],f["kappa"],f["q"],f["x"],f["z"],f["omega"],False)
        c3re,_=c3_value_norm(f["gamma"],f["kappa"],f["q"],f["x"],f["z"],f["omega"],True)
        errs={"c1p":relabs(rp["c1"],c1e),"c3p":relabs(rp["c3"],c3pe),"c3r":relabs(rr["c3"],c3re)}
        max_recon=max(max_recon,*errs.values())
        if max(errs.values())>RECON_TOL: recon.append({"id":f["id"],"errors":errs})
        rec={"id":f["id"],"shell":f["shell"],"orientation":f["orientation"],"r":f["r"],"abs_z":f["abs_z"],"physical":rp,"record":rr}
        stageB.append(rec)
        if rp["class"]=="BOUNDARY" or rr["class"]=="BOUNDARY": boundaries.append(rec); continue
        if rp["class"]=="STABLE" and rr["class"]=="UNSTABLE": correct+=1
        else:
            b=[]
            if rp["margins"]["m2"]<=RH_TOL: b.append("m2"); blockers["m2"]+=1
            if rp["margins"]["mh"]<=RH_TOL: b.append("mh"); blockers["mh"]+=1
            counter.append({**rec,"blocking_margins":b})

G4=len(recon)==0 and max_recon<=RECON_TOL
# G5 controls.
f0={"gamma":1.0,"kappa":1.2,"q":0.0,"x":0.2,"z":0.3,"omega":0.7}
A0p,B0=active_matrices(f0,False); A0r,_=active_matrices(f0,True)
eta0=max_abs(A0p-A0r)<=1e-15
controls=(rh(np.diag([-1.,-2.,-3.]),1.)["class"]=="STABLE" and rh(np.diag([.2,-1.,-2.]),1.)["class"]=="UNSTABLE" and rh(np.diag([0.,-1.,-2.]),1.)["class"]=="BOUNDARY")
G5=eta0 and controls

n_frozen=len(frozen_rows)
if not all([G0,G1,G2,G3,G4,G5]): h8f_status="AUDIT_OR_RECONSTRUCTION_HOLD"
elif n_frozen<20: h8f_status="INSUFFICIENT_H8F"
elif boundaries: h8f_status="BOUNDARY_HOLD"
elif counter: h8f_status="FAIL_H8F"
else: h8f_status="PASS_H8F"

result={
    "schema":"stability-arc-state-geometry-admissibility-v0.1",
    "environment":{"python":platform.python_version(),"numpy":np.__version__},
    "mechanical":{"G0":G0,"G1":G1,"G2":G2,"G3":G3,"G4":G4,"G5":G5,"max_reconstruction_error":max_recon},
    "stageA":{"selection_sha256":stage_sha,"strata":stratum_summary,"high_radius_eligible_count":high_count,"low_radius_eligible_count":low_count,"total_frozen":n_frozen,"orientation_zero_count":orientation_zero},
    "scientific":{"H8E_high_radius_existence":"PASS" if H8E else "FAIL","H8L_low_radius_absence":"PASS" if H8L else "FAIL","H8F_status":h8f_status,"H8F_correct":correct,"H8F_counterexamples":len(counter),"H8F_blockers":blockers,"boundary_count":len(boundaries)},
    "replay_failures":replay_fail,"reconstruction_failures":recon,"counterexamples":counter,"boundary_rows":boundaries,
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"mechanical":result["mechanical"],"stageA":result["stageA"],"scientific":result["scientific"]},indent=2,sort_keys=True))
