#!/usr/bin/env python3
import json
import math
import platform
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parent
RESULTS=ROOT/"results"
RESULTS.mkdir(parents=True,exist_ok=True)
OUT=RESULTS/"rotated_measurement_architecture_v01.json"

SEED=2026082916
N=128
REAL_TOL=1e-11
BRIDGE_TOL=5e-11
DARK_TOL=5e-10
INTER_TOL=5e-10
MOMENT_TOL=5e-9
COV_TOL=5e-9
NULL_TOL=1e-10
R_ACTIVE=np.array([[1.2,0.3],[-0.2,0.9]],float)

sx=np.array([[0,1],[1,0]],complex)
sy=np.array([[0,-1j],[1j,0]],complex)
sz=np.array([[1,0],[0,-1]],complex)
I2=np.eye(2,dtype=complex)
sm=np.array([[0,1],[0,0]],complex)
BASIS=[0.5*sx,0.5*sy,0.5*sz]
PAULI=[sx,sy,sz]
X45=(sx+sz)/(2.0*math.sqrt(2.0))
X3=(sx+sy+sz)/(2.0*math.sqrt(3.0))


def max_abs(a):
    a=np.asarray(a)
    return 0.0 if a.size==0 else float(np.max(np.abs(a)))

def comm(a,b): return a@b-b@a

def dissipator(c,rho):
    cd=c.conj().T; cdc=cd@c
    return c@rho@cd-0.5*(cdc@rho+rho@cdc)

def rho_from_bloch(v): return 0.5*(I2+v[0]*sx+v[1]*sy+v[2]*sz)

def coords(op):
    vals=[complex(np.trace(p@op)) for p in PAULI]
    return np.array([v.real for v in vals],float), max(abs(v.imag) for v in vals)

def linear_matrix(action):
    cols=[]; imag=0.0
    for e in BASIS:
        c,im=coords(action(e)); cols.append(c); imag=max(imag,im)
    return np.column_stack(cols),imag

def measurement_mu(X,rho): return float(np.trace(X@rho).real)

def h_super(X,rho):
    mu=measurement_mu(X,rho)
    return X@rho+rho@X-2.0*mu*rho

def delta_h(X,rho,e):
    mu=measurement_mu(X,rho); dm=float(np.trace(X@e).real)
    return X@e+e@X-2.0*mu*e-2.0*dm*rho

def build_matrices(f,X):
    rho=rho_from_bloch(f["base"])
    H=0.5*f["omega"]*sy
    c=math.sqrt(f["gamma"])*sm
    def L(e): return -1j*comm(H,e)+dissipator(c,e)+2.0*f["kappa"]*dissipator(X,e)
    A,ia=linear_matrix(L)
    amp=math.sqrt(2.0*f["eta"]*f["kappa"])
    B,ib=linear_matrix(lambda e: amp*delta_h(X,rho,e))
    h,ih=coords(h_super(X,rho))
    Vt=np.array([[float(np.trace(X@e).real) for e in BASIS]],float)
    U=-4.0*f["eta"]*f["kappa"]*h.reshape(-1,1)
    Arec=A+U@Vt
    return rho,A,Arec,B,U,Vt,max(ia,ib,ih,max_abs(np.imag(Arec)))

def dark_space(A,Vt):
    O=np.vstack([Vt,Vt@A,Vt@A@A])
    _,s,vh=np.linalg.svd(O,full_matrices=True)
    rank=int(np.sum(s>NULL_TOL))
    D=vh[rank:].T.copy()
    if D.size: D,_=np.linalg.qr(D)
    return O,s,D

def orth_complement(D,n=3):
    if D.shape[1]==0: return np.eye(n)
    _,_,vh=np.linalg.svd(D.T,full_matrices=True)
    C=vh[D.shape[1]:].T.copy()
    C,_=np.linalg.qr(C)
    return C

def quotient(A,B,D,C):
    L=C.T
    return L,L@A@C,L@B@C

def Kfull(A,B):
    n=A.shape[0]
    return np.kron(np.eye(n),A)+np.kron(A,np.eye(n))+np.kron(B,B)

def poly_err(A,B): return max_abs(np.poly(A)-np.poly(B))

# deterministic fresh fixture generation
rng=np.random.default_rng(SEED)
fixtures=[]
for i in range(N):
    g=float(10**rng.uniform(math.log10(0.1),math.log10(2.0)))
    k=float(10**rng.uniform(math.log10(0.05),math.log10(2.0)))
    eta=float(rng.uniform(0.05,0.95)); omega=float(rng.uniform(0.1,3.0)); r=float(rng.uniform(0.05,0.85))
    d=rng.normal(size=3); d=d/np.linalg.norm(d)
    fixtures.append({"id":f"RM{i+1:03d}","gamma":g,"kappa":k,"eta":eta,"omega":omega,"base":(r*d).tolist()})

R0=True; R1=True; R2=True; R3=True; R4=True; R5=True; R6=True
max_imag=0.0; min_rho=1.0; max_bridge=0.0; max_dark=0.0; max_stoch=0.0; max_inter=0.0; max_moment=0.0; max_cov=0.0
structural_failures=[]; records=[]
Rinv=np.linalg.inv(R_ACTIVE)

for f in fixtures:
    rho,A,Ar,B,U,Vt,imag=build_matrices(f,X45)
    eig=np.linalg.eigvalsh(rho); min_rho=min(min_rho,float(np.min(eig))); max_imag=max(max_imag,imag)
    if np.min(eig)<=0 or imag>REAL_TOL: R0=False
    bridge=max_abs((Ar-A)-U@Vt); rank=int(np.linalg.matrix_rank(U@Vt,tol=1e-10)); max_bridge=max(max_bridge,bridge)
    if bridge>BRIDGE_TOL or rank>1: R1=False
    O,svals,D=dark_space(A,Vt)
    if D.shape[1]!=1:
        R2=False; R3=False; R4=False; R5=False; R6=False
        structural_failures.append({"id":f["id"],"reason":"DARK_DIMENSION","dim":int(D.shape[1])}); continue
    Pperp=np.eye(3)-D@D.T
    dark=max(max_abs(Vt@D),max_abs(Pperp@A@D)); stoch=max(max_abs(Pperp@Ar@D),max_abs(Pperp@B@D))
    max_dark=max(max_dark,dark); max_stoch=max(max_stoch,stoch)
    if dark>DARK_TOL: R2=False
    if stoch>DARK_TOL: R3=False
    C=orth_complement(D)
    L,Aqp,Bq=quotient(A,B,D,C); _,Aqr,Bqr=quotient(Ar,B,D,C)
    inter=max(max_abs(L@A-Aqp@L),max_abs(L@Ar-Aqr@L),max_abs(L@B-Bq@L),max_abs(Bqr-Bq))
    max_inter=max(max_inter,inter)
    if inter>INTER_TOL: R4=False
    J=np.kron(L,L)
    mres=max(max_abs(J@Kfull(A,B)-Kfull(Aqp,Bq)@J),max_abs(J@Kfull(Ar,B)-Kfull(Aqr,Bq)@J))
    max_moment=max(max_moment,mres)
    if mres>MOMENT_TOL: R5=False
    # quotient coordinate covariance under fixed R
    Aqp_t=Rinv@Aqp@R_ACTIVE; Aqr_t=Rinv@Aqr@R_ACTIVE; Bq_t=Rinv@Bq@R_ACTIVE
    Kp=Kfull(Aqp,Bq); Kr=Kfull(Aqr,Bq); Kpt=Kfull(Aqp_t,Bq_t); Krt=Kfull(Aqr_t,Bq_t)
    cov=max(poly_err(Aqp,Aqp_t),poly_err(Aqr,Aqr_t),poly_err(Kp,Kpt),poly_err(Kr,Krt))
    max_cov=max(max_cov,cov)
    if cov>COV_TOL: R6=False
    records.append({"id":f["id"],"dark_dim":1,"bridge_rank":rank,"dark_residual":dark,"stochastic_residual":stoch,"intertwine_residual":inter,"moment_residual":mres,"coordinate_invariant_error":cov})

# R7 generic 3D measurement-axis refusal control
fc={"id":"R7","gamma":0.3,"kappa":0.2,"eta":0.7,"omega":1.1,"base":[0.2,0.1,-0.3]}
_,Ac,Arc,Bc,Uc,Vc,imc=build_matrices(fc,X3)
Oc,sc,Dc=dark_space(Ac,Vc)
refusal="REFUSE_NO_1D_DARK_FACTOR" if Dc.shape[1]!=1 else "UNEXPECTED_1D_DARK_FACTOR"
R7=(int(np.linalg.matrix_rank(Oc,tol=NULL_TOL))==3 and refusal=="REFUSE_NO_1D_DARK_FACTOR")

all_pass=all([R0,R1,R2,R3,R4,R5,R6,R7])
status="PASS_ROTATED_AXIS_STOCHASTIC_QUOTIENT" if all_pass else "FAIL_ROTATED_AXIS_ARCHITECTURE"
result={
    "schema":"stability-arc-rotated-measurement-architecture-v0.1",
    "phase_status":status,
    "environment":{"python":platform.python_version(),"numpy":np.__version__},
    "measurement_axis":"(x+z)/sqrt(2)",
    "criteria":{
        "R0":{"status":"PASS" if R0 else "FAIL","min_density_eigenvalue":min_rho,"max_imag":max_imag},
        "R1":{"status":"PASS" if R1 else "FAIL","max_bridge_error":max_bridge},
        "R2":{"status":"PASS" if R2 else "FAIL","max_dark_error":max_dark},
        "R3":{"status":"PASS" if R3 else "FAIL","max_stochastic_dark_error":max_stoch},
        "R4":{"status":"PASS" if R4 else "FAIL","max_intertwine_error":max_inter},
        "R5":{"status":"PASS" if R5 else "FAIL","max_moment_intertwine_error":max_moment},
        "R6":{"status":"PASS" if R6 else "FAIL","max_coordinate_invariant_error":max_cov},
        "R7":{"status":"PASS" if R7 else "FAIL","observability_rank":int(np.linalg.matrix_rank(Oc,tol=NULL_TOL)),"refusal":refusal,"singular_values":[float(v) for v in sc]},
    },
    "fresh_fixture_count":N,
    "structural_failure_count":len(structural_failures),
    "structural_failures":structural_failures,
    "records":records,
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"phase_status":status,"criteria":result["criteria"],"fresh_fixture_count":N,"structural_failure_count":len(structural_failures)},indent=2,sort_keys=True))
