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
OUT = RESULTS / "near_pure_orientation_test_v01.json"
STAGE_A = RESULTS / "stageA_near_pure_orientation_selection.json"
STAGE_A_SHA = RESULTS / "stageA_near_pure_orientation_selection.sha256"

SEED = 2026082914
N_PER = 500000
MAX_FREEZE = 128
MIN_TOTAL = 20
MAP_TOL = 1e-8
C1_TOL = 1e-8
RH_TOL = 1e-9
RECON_TOL = 2e-10
R_LO = 0.995
R_HI = 0.9999
SIGNS = ["NEG", "POS"]

SYM_BASIS = [
    np.array([[1.0,0.0],[0.0,0.0]], float),
    np.array([[0.0,1.0],[1.0,0.0]], float),
    np.array([[0.0,0.0],[0.0,1.0]], float),
]


def relabs(a,b):
    return abs(a-b)/max(1.0,abs(a),abs(b))


def max_abs(a):
    a=np.asarray(a)
    return 0.0 if a.size==0 else float(np.max(np.abs(a)))


def generate():
    rng=np.random.default_rng(SEED)
    out={}
    for orient in SIGNS:
        k=10.0**rng.uniform(math.log10(0.2),math.log10(100.0),N_PER)
        eta=rng.uniform(0.001,0.95,N_PER)
        w=10.0**rng.uniform(-3.0,3.0,N_PER)
        r=rng.uniform(R_LO,R_HI,N_PER)
        phi=rng.uniform(0.0,math.pi/2.0,N_PER)
        sign_z=np.where(rng.integers(0,2,N_PER)==0,-1.0,1.0)
        ax=r*np.cos(phi); az=r*np.sin(phi); z=sign_z*az
        sign_x=-sign_z if orient=="NEG" else sign_z
        x=sign_x*ax
        q=eta*k
        out[orient]={"gamma":np.ones(N_PER),"kappa":k,"eta":eta,"omega":w,"r":r,"phi":phi,"x":x,"z":z,"q":q}
    return out


def hash_stratum(s,orient):
    h=hashlib.sha256()
    h.update(f"seed={SEED};n={N_PER};orient={orient};r={R_LO}:{R_HI}\n".encode())
    for key in ["gamma","kappa","eta","omega","r","phi","x","z","q"]:
        h.update(key.encode()+b"\0"); h.update(np.asarray(s[key],dtype="<f8").tobytes())
    return h.hexdigest()


def c3_coeff_arrays(s,record=False):
    g,k,q,x,z=s["gamma"],s["kappa"],s["q"],s["x"],s["z"]
    if not record:
        A=2*(3*g+2*k-2*q*x*x-10*q*z*z)
        B=16*q*x*z*(g+k-3*q*z*z)
        C=(g-4*q*z*z)*(3*g+2*k-8*q*z*z)*(g+2*k-2*q*z*z)
    else:
        A=2*(3*g+2*k+4*q-2*q*x*x-14*q*z*z)
        B=4*q*x*z*(7*g+6*k+8*q-30*q*z*z)
        C=(g+2*k-2*q*z*z)*(g+2*q-6*q*z*z)*(3*g+2*k+4*q-12*q*z*z)
    return A,B,C


def c3_norm_arrays(coeff,w):
    A,B,C=coeff
    v=(A*w+B)*w+C
    scale=np.maximum(1.0,np.abs(A)*w*w+np.abs(B)*w+np.abs(C))
    return v,v/scale


def c3_scalar(g,k,q,x,z,w,record=False):
    if not record:
        A=2*(3*g+2*k-2*q*x*x-10*q*z*z)
        B=16*q*x*z*(g+k-3*q*z*z)
        C=(g-4*q*z*z)*(3*g+2*k-8*q*z*z)*(g+2*k-2*q*z*z)
    else:
        A=2*(3*g+2*k+4*q-2*q*x*x-14*q*z*z)
        B=4*q*x*z*(7*g+6*k+8*q-30*q*z*z)
        C=(g+2*k-2*q*z*z)*(g+2*q-6*q*z*z)*(3*g+2*k+4*q-12*q*z*z)
    v=(A*w+B)*w+C
    scale=max(1.0,abs(A)*w*w+abs(B)*w+abs(C))
    return float(v),float(v/scale)


def c1_phys(g,k,q,z):
    return 4.5*g+3*k-14*q*z*z


def row(s,i,orient,sp,sr,u1):
    return {
        "id":f"NP_{orient}_{i+1:06d}","orientation":orient,"index":int(i+1),
        "gamma":1.0,"kappa":float(s["kappa"][i]),"eta":float(s["eta"][i]),"omega":float(s["omega"][i]),
        "r":float(s["r"][i]),"x":float(s["x"][i]),"z":float(s["z"][i]),"q":float(s["q"][i]),
        "abs_z":float(abs(s["z"][i])),"xz":float(s["x"][i]*s["z"][i]),
        "c1_phys_norm":float(u1[i]),"c3_phys_norm":float(sp[i]),"c3_record_norm":float(sr[i]),
    }


def active(f,record=False):
    g,k,q,x,z,w=f["gamma"],f["kappa"],f["q"],f["x"],f["z"],f["omega"]
    ss=math.sqrt(2*q)
    A=np.array([[-(g/2+k),w],[-w,-g]],float)
    if record: A+=np.array([[0,2*q*z*x],[0,-2*q*(1-z*z)]],float)
    B=np.array([[-ss*z,-ss*x],[0,-2*ss*z]],float)
    return A,B


def moment(A,B,P): return A@P+P@A.T+B@P@B.T

def coords(P): return np.array([P[0,0],0.5*(P[0,1]+P[1,0]),P[1,1]],float)

def Gmat(A,B): return np.column_stack([coords(moment(A,B,E)) for E in SYM_BASIS])


def rh(G,R):
    tr=float(np.trace(G)); c1=-tr; c2=0.5*(tr*tr-float(np.trace(G@G))); c3=-float(np.linalg.det(G)); mh=c1*c2-c3
    m={"m1":c1/R,"m2":c2/R**2,"m3":c3/R**3,"mh":mh/R**3}
    if all(v>RH_TOL for v in m.values()): cls="STABLE"
    elif any(v<-RH_TOL for v in m.values()): cls="UNSTABLE"
    else: cls="BOUNDARY"
    return {"c1":c1,"c2":c2,"c3":c3,"mh_raw":mh,"margins":m,"class":cls}


# N0 deterministic replay.
D1=generate(); D2=generate()
h1={o:hash_stratum(D1[o],o) for o in SIGNS}; h2={o:hash_stratum(D2[o],o) for o in SIGNS}
N0=h1==h2

# N1 geometry and Stage A c1+c3-only selection.
geometry_ok=True
selection={}; counts={}
for orient in SIGNS:
    s=D1[orient]
    prod=s["x"]*s["z"]
    geometry_ok &= bool(np.all((s["r"]>=R_LO)&(s["r"]<R_HI)))
    geometry_ok &= bool(np.all(prod<0)) if orient=="NEG" else bool(np.all(prod>0))
    _,sp=c3_norm_arrays(c3_coeff_arrays(s,False),s["omega"])
    _,sr=c3_norm_arrays(c3_coeff_arrays(s,True),s["omega"])
    R=s["gamma"]+s["kappa"]+s["omega"]+s["q"]
    u1=(4.5*s["gamma"]+3*s["kappa"]-14*s["q"]*s["z"]*s["z"])/R
    idx=np.where((u1>C1_TOL)&(sp>MAP_TOL)&(sr<-MAP_TOL))[0]
    counts[orient]=int(len(idx))
    selection[orient]=[row(s,int(i),orient,sp,sr,u1) for i in idx[:MAX_FREEZE]]
N1=geometry_ok

payload={"schema":"stability-arc-near-pure-orientation-stageA-v0.1","seed":SEED,"n_per":N_PER,"hashes":h1,"eligible_counts":counts,"selected":selection,"thresholds":{"C1_TOL":C1_TOL,"MAP_TOL":MAP_TOL}}
b=json.dumps(payload,indent=2,sort_keys=True).encode()+b"\n"; STAGE_A.write_bytes(b); stage_sha=hashlib.sha256(b).hexdigest(); STAGE_A_SHA.write_text(stage_sha+"  stageA_near_pure_orientation_selection.json\n")
N2=hashlib.sha256(STAGE_A.read_bytes()).hexdigest()==stage_sha

H9N=counts["NEG"]>=20
H9P=counts["POS"]==0

# N3 replay from frozen bytes.
frozen=json.loads(STAGE_A.read_text()); rows=frozen["selected"]["NEG"]+frozen["selected"]["POS"]
replay=[]
for f in rows:
    R=f["gamma"]+f["kappa"]+f["omega"]+f["q"]
    u1=c1_phys(f["gamma"],f["kappa"],f["q"],f["z"])/R
    _,sp=c3_scalar(f["gamma"],f["kappa"],f["q"],f["x"],f["z"],f["omega"],False)
    _,sr=c3_scalar(f["gamma"],f["kappa"],f["q"],f["x"],f["z"],f["omega"],True)
    if not(u1>C1_TOL and sp>MAP_TOL and sr<-MAP_TOL): replay.append(f["id"])
N3=len(replay)==0

# Stage B.
recon=[]; boundary=[]; counter=[]; correct=0; blockers={"m2":0,"mh":0}; maxerr=0.0
if N0 and N1 and N2 and N3:
    for f in rows:
        Ap,B=active(f,False); Ar,_=active(f,True); Gp=Gmat(Ap,B); Gr=Gmat(Ar,B); R=f["gamma"]+f["kappa"]+f["omega"]+f["q"]
        rp=rh(Gp,R); rr=rh(Gr,R)
        c1e=c1_phys(f["gamma"],f["kappa"],f["q"],f["z"]); c3pe,_=c3_scalar(f["gamma"],f["kappa"],f["q"],f["x"],f["z"],f["omega"],False); c3re,_=c3_scalar(f["gamma"],f["kappa"],f["q"],f["x"],f["z"],f["omega"],True)
        errs={"c1p":relabs(rp["c1"],c1e),"c3p":relabs(rp["c3"],c3pe),"c3r":relabs(rr["c3"],c3re)}; maxerr=max(maxerr,*errs.values())
        if max(errs.values())>RECON_TOL: recon.append({"id":f["id"],"errors":errs})
        rec={"id":f["id"],"orientation":f["orientation"],"r":f["r"],"abs_z":f["abs_z"],"physical":rp,"record":rr}
        if rp["class"]=="BOUNDARY" or rr["class"]=="BOUNDARY": boundary.append(rec); continue
        if rp["class"]=="STABLE" and rr["class"]=="UNSTABLE": correct+=1
        else:
            bs=[]
            if rp["margins"]["m2"]<=RH_TOL: bs.append("m2"); blockers["m2"]+=1
            if rp["margins"]["mh"]<=RH_TOL: bs.append("mh"); blockers["mh"]+=1
            counter.append({**rec,"blocking_margins":bs})
N4=len(recon)==0 and maxerr<=RECON_TOL

# N5 controls.
f0={"gamma":1.0,"kappa":1.2,"q":0.0,"x":0.2,"z":0.3,"omega":0.7}; A0,B0=active(f0,False); A1,_=active(f0,True)
eta0=max_abs(A0-A1)<=1e-15
class_ok=(rh(np.diag([-1.,-2.,-3.]),1.)["class"]=="STABLE" and rh(np.diag([.2,-1.,-2.]),1.)["class"]=="UNSTABLE" and rh(np.diag([0.,-1.,-2.]),1.)["class"]=="BOUNDARY")
N5=eta0 and class_ok

total_eligible=counts["NEG"]+counts["POS"]
if not all([N0,N1,N2,N3,N4,N5]): h9f="AUDIT_OR_RECONSTRUCTION_HOLD"
elif len(boundary)>0: h9f="BOUNDARY_HOLD"
elif total_eligible<MIN_TOTAL: h9f="INSUFFICIENT_H9F"
elif len(counter)>0: h9f="FAIL_H9F"
else: h9f="PASS_H9F"

result={
    "schema":"stability-arc-near-pure-orientation-test-v0.1",
    "environment":{"python":platform.python_version(),"numpy":np.__version__},
    "audit":{"N0":N0,"N1":N1,"N2":N2,"N3":N3,"N4":N4,"N5":N5,"max_reconstruction_error":maxerr},
    "stageA":{"selection_sha256":stage_sha,"eligible_counts":counts,"frozen_counts":{o:len(selection[o]) for o in SIGNS},"generator_hashes":h1},
    "scientific":{"H9N":"PASS" if H9N else "FAIL","H9P":"PASS" if H9P else "FAIL","H9F":h9f,"H9F_correct":correct,"H9F_counterexamples":len(counter),"H9F_blockers":blockers,"boundary_count":len(boundary)},
    "replay_failures":replay,"reconstruction_failures":recon,"counterexamples":counter,"boundary_rows":boundary,
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"audit":result["audit"],"stageA":result["stageA"],"scientific":result["scientific"]},indent=2,sort_keys=True))
