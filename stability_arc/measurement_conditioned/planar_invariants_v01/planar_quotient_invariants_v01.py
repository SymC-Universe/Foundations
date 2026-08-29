#!/usr/bin/env python3
import json
import math
import platform
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "planar_quotient_invariants_v01.json"

SEED = 2026082918
TOL = 2e-9
POLY_TOL = 2e-8
NEAR_TOL = 1e-8
NULL_TOL = 1e-9
R_ACTIVE = np.array([[1.2, 0.3], [-0.2, 0.9]], dtype=float)

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)
sm = np.array([[0, 1], [0, 0]], dtype=complex)
BASIS = [0.5*sx, 0.5*sy, 0.5*sz]
PAULI = [sx, sy, sz]
SYM_BASIS = [
    np.array([[1.0, 0.0], [0.0, 0.0]]),
    np.array([[0.0, 1.0], [1.0, 0.0]]),
    np.array([[0.0, 0.0], [0.0, 1.0]]),
]


def max_abs(a):
    a = np.asarray(a)
    return 0.0 if a.size == 0 else float(np.max(np.abs(a)))


def relabs(a, b):
    return abs(a-b)/max(1.0, abs(a), abs(b))


def comm(a, b):
    return a@b-b@a


def dissipator(c, rho):
    cd = c.conj().T
    cdc = cd@c
    return c@rho@cd - 0.5*(cdc@rho + rho@cdc)


def rho_from_bloch(r):
    return 0.5*(I2 + r[0]*sx + r[1]*sy + r[2]*sz)


def coords(op):
    vals = [complex(np.trace(p@op)) for p in PAULI]
    return np.array([v.real for v in vals]), max(abs(v.imag) for v in vals)


def linear_matrix(action):
    cols = []
    imag = 0.0
    for e in BASIS:
        c, im = coords(action(e))
        cols.append(c)
        imag = max(imag, im)
    return np.column_stack(cols), imag


def Xtheta(theta):
    return 0.5*(math.sin(theta)*sx + math.cos(theta)*sz)


def mu(X, rho):
    return float(np.trace(X@rho).real)


def h_super(X, rho):
    return X@rho + rho@X - 2.0*mu(X, rho)*rho


def delta_h(X, rho, e):
    dm = float(np.trace(X@e).real)
    return X@e + e@X - 2.0*mu(X, rho)*e - 2.0*dm*rho


def full_matrices(f):
    X = Xtheta(f["theta"])
    rho = rho_from_bloch(f["base"])
    H = 0.5*f["omega"]*sy
    c = math.sqrt(f["gamma"])*sm
    def L(e):
        return -1j*comm(H,e) + dissipator(c,e) + 2.0*f["kappa"]*dissipator(X,e)
    A, ia = linear_matrix(L)
    amp = math.sqrt(2.0*f["eta"]*f["kappa"])
    B, ib = linear_matrix(lambda e: amp*delta_h(X,rho,e))
    h, ih = coords(h_super(X,rho))
    Vt = np.array([[float(np.trace(X@e).real) for e in BASIS]])
    U = -4.0*f["eta"]*f["kappa"]*h.reshape(-1,1)
    Ar = A + U@Vt
    return rho,A,Ar,B,Vt,max(ia,ib,ih,max_abs(np.imag(Ar)))


def canonical_from_fixture(f):
    th = f["theta"]
    sn, cs = math.sin(th), math.cos(th)
    r = np.asarray(f["base"], dtype=float)
    u = sn*r[0] + cs*r[2]
    v = cs*r[0] - sn*r[2]
    q = f["eta"]*f["kappa"]
    p = 0.5*f["gamma"]*(1.0 + cs*cs)
    d = f["kappa"] + 0.5*f["gamma"]*(1.0 + sn*sn)
    h = 0.25*f["gamma"]*math.sin(2.0*th)
    Ap = np.array([[-p, h-f["omega"]], [h+f["omega"], -d]], dtype=float)
    B = -math.sqrt(2.0*q)*np.array([[2.0*u,0.0],[v,u]], dtype=float)
    Ar = Ap + np.array([[-2.0*q*(1.0-u*u),0.0],[2.0*q*u*v,0.0]], dtype=float)
    return Ap,Ar,B,{"u":u,"v":v,"q":q,"p":p,"d":d,"h":h}


def quotient_from_full(f, A, Ar, B):
    th=f["theta"]
    sn,cs=math.sin(th),math.cos(th)
    C=np.array([[sn,cs],[0.0,0.0],[cs,-sn]],dtype=float)
    # Columns are n and m embedded in (x,y,z); L=C^T and C^T C=I.
    L=C.T
    return L@A@C, L@Ar@C, L@B@C


def moment_action(A,B,P):
    return A@P + P@A.T + B@P@B.T


def sym_coords(P):
    return np.array([P[0,0],0.5*(P[0,1]+P[1,0]),P[1,1]],dtype=float)


def Gnum(A,B):
    return np.column_stack([sym_coords(moment_action(A,B,E)) for E in SYM_BASIS])


def coeff_num(A,B):
    pol=np.poly(Gnum(A,B))
    # np.poly(G) gives det(lambda I-G) coefficients [1,c1,c2,c3]
    return np.real_if_close(pol).astype(float)


def dark_dim_full(f,A,Vt):
    O=np.vstack([Vt,Vt@A,Vt@A@A])
    _,s,vh=np.linalg.svd(O,full_matrices=True)
    rank=int(np.sum(s>NULL_TOL))
    return 3-rank,rank,[float(v) for v in s]


# ---------------- exact symbolic canonicalization ----------------
g,k,q,w,th,x,z,u,v,p,d,h = sp.symbols("g k q w th x z u v p d h", real=True)
sn,cs=sp.sin(th),sp.cos(th)
Q=sp.Matrix([[sn,cs],[cs,-sn]])
A_lab=sp.Matrix([[-g/2-k*cs**2, w+k*sn*cs],[-w+k*sn*cs,-g-k*sn**2]])
mu_lab=sn*x+cs*z
B_lab=-sp.sqrt(2*q)*sp.Matrix([[x*sn+mu_lab,x*cs],[z*sn,z*cs+mu_lab]])
n=sp.Matrix([sn,cs]); rlab=sp.Matrix([x,z]); hh=n-mu_lab*rlab
Ar_lab=A_lab-2*q*hh*n.T
subs_uv={x:sn*u+cs*v,z:cs*u-sn*v}
Aq=sp.simplify(Q*A_lab*Q.T)
Bq=sp.simplify(Q*B_lab.subs(subs_uv)*Q.T)
Arq=sp.simplify(Q*Ar_lab.subs(subs_uv)*Q.T)
p_th=g*(1+cs**2)/2
d_th=k+g*(1+sn**2)/2
h_th=g*sp.sin(2*th)/4
A_target=sp.Matrix([[-p_th,h_th-w],[h_th+w,-d_th]])
B_target=-sp.sqrt(2*q)*sp.Matrix([[2*u,0],[v,u]])
Ar_target=A_target+sp.Matrix([[-2*q*(1-u**2),0],[2*q*u*v,0]])
Q0=all(sp.trigsimp(Aq[i,j]-A_target[i,j])==0 and sp.trigsimp(Arq[i,j]-Ar_target[i,j])==0 and sp.trigsimp(Bq[i,j]-B_target[i,j])==0 for i in range(2) for j in range(2))

# Build generic canonical invariants in independent p,d,h symbols.
Acan=sp.Matrix([[-p,h-w],[h+w,-d]])
Bcan=-sp.sqrt(2*q)*sp.Matrix([[2*u,0],[v,u]])
Arcan=Acan+sp.Matrix([[-2*q*(1-u**2),0],[2*q*u*v,0]])
P11=sp.Matrix([[1,0],[0,0]]); P12=sp.Matrix([[0,1],[1,0]]); P22=sp.Matrix([[0,0],[0,1]])

def Gsym(A,B):
    cols=[]
    for P in [P11,P12,P22]:
        Y=sp.expand(A*P+P*A.T+B*P*B.T)
        cols.append(sp.Matrix([Y[0,0],sp.simplify((Y[0,1]+Y[1,0])/2),Y[1,1]]))
    return sp.Matrix.hstack(*cols)

Gp=Gsym(Acan,Bcan); Gr=Gsym(Arcan,Bcan)
lam=sp.symbols("lambda")

def coeff_sym(G):
    pol=sp.Poly(sp.expand((lam*sp.eye(3)-G).det()),lam)
    return [sp.factor(c) for c in pol.all_coeffs()[1:]]

cp=coeff_sym(Gp); cr=coeff_sym(Gr)
Q1=len(cp)==3 and len(cr)==3
c1p_target=3*(p+d)-14*q*u**2
c1r_target=3*(p+d)+6*q-20*q*u**2
Q2=(sp.simplify(cp[0]-c1p_target)==0 and sp.simplify(cr[0]-c1r_target)==0 and sp.simplify((cr[0]-cp[0])-6*q*(1-u**2))==0)

# Exact sigma_z reduction of c1/c3. At theta=0: p=g,d=k+g/2,h=0,u=z,v=x.
subs_z={p:g,d:k+g/2,h:0,u:z,v:x}
c3p_sigma=(g-4*q*z**2)*(3*g+2*k-8*q*z**2)*(g+2*k-2*q*z**2) + 16*q*x*z*(g+k-3*q*z**2)*w + 2*(3*g+2*k-2*q*x**2-10*q*z**2)*w**2
c3r_sigma=(g+2*k-2*q*z**2)*(g+2*q-6*q*z**2)*(3*g+2*k+4*q-12*q*z**2) + 4*q*x*z*(7*g+6*k+8*q-30*q*z**2)*w + 2*(3*g+2*k+4*q-2*q*x**2-14*q*z**2)*w**2
Q3=(sp.simplify(cp[0].subs(subs_z)-(sp.Rational(9,2)*g+3*k-14*q*z**2))==0 and
    sp.simplify(cr[0].subs(subs_z)-(sp.Rational(9,2)*g+3*k+6*q-20*q*z**2))==0 and
    sp.factor(cp[2].subs(subs_z)-c3p_sigma)==0 and sp.factor(cr[2].subs(subs_z)-c3r_sigma)==0)

# lambdify exact coefficients for numerical clean-room checks.
args=(p,d,h,w,q,u,v)
cp_fn=sp.lambdify(args,cp,"numpy"); cr_fn=sp.lambdify(args,cr,"numpy")

rng=np.random.default_rng(SEED)
max_matrix_err=0.0; max_coeff_err=0.0; max_poly_err=0.0
q4_fail=[]; q5_fail=[]; near=[]

def fresh_fixture(i,theta_fixed=None):
    gamma=float(10**rng.uniform(math.log10(0.1),math.log10(2.0)))
    kappa=float(10**rng.uniform(math.log10(0.05),math.log10(2.0)))
    eta=float(rng.uniform(0.05,0.95)); omega=float(rng.uniform(0.05,3.0))
    theta=float(math.pi/4 if theta_fixed is not None else rng.uniform(-math.pi,math.pi))
    rad=float(rng.uniform(0.05,0.85)); vec=rng.normal(size=3); vec=vec/np.linalg.norm(vec)
    return {"id":i,"gamma":gamma,"kappa":kappa,"eta":eta,"omega":omega,"theta":theta,"base":(rad*vec).tolist()}


def score_fixture(f,allow_near=False):
    global max_matrix_err,max_coeff_err,max_poly_err
    delta=f["omega"]-0.25*f["gamma"]*math.sin(2*f["theta"])
    nd=abs(delta)/(f["gamma"]+f["omega"])
    if allow_near and nd<=NEAR_TOL:
        return "NEAR",{"normalized_delta":nd}
    rho,A,Ar,B,Vt,imag=full_matrices(f)
    Apf,Arf,Bf=quotient_from_full(f,A,Ar,B)
    Apc,Arc,Bc,meta=canonical_from_fixture(f)
    merr=max(max_abs(Apf-Apc),max_abs(Arf-Arc),max_abs(Bf-Bc))
    max_matrix_err=max(max_matrix_err,merr)
    cp_direct=coeff_num(Apf,Bf); cr_direct=coeff_num(Arf,Bf)
    vals=(meta["p"],meta["d"],meta["h"],f["omega"],meta["q"],meta["u"],meta["v"])
    cp_exact=np.array([1.0]+[float(vv) for vv in cp_fn(*vals)])
    cr_exact=np.array([1.0]+[float(vv) for vv in cr_fn(*vals)])
    cerr=max(max(relabs(a,b) for a,b in zip(cp_direct,cp_exact)),max(relabs(a,b) for a,b in zip(cr_direct,cr_exact)))
    max_coeff_err=max(max_coeff_err,cerr)
    Rinv=np.linalg.inv(R_ACTIVE)
    Apt=Rinv@Apf@R_ACTIVE; Art=Rinv@Arf@R_ACTIVE; Bt=Rinv@Bf@R_ACTIVE
    perr=max(max_abs(np.poly(Gnum(Apf,Bf))-np.poly(Gnum(Apt,Bt))),max_abs(np.poly(Gnum(Arf,Bf))-np.poly(Gnum(Art,Bt))))
    max_poly_err=max(max_poly_err,perr)
    ok=(merr<=TOL and cerr<=TOL and perr<=POLY_TOL and imag<=1e-11)
    return "PASS" if ok else "FAIL",{"normalized_delta":nd,"matrix_error":merr,"coefficient_error":cerr,"poly_error":perr,"imag":imag}

# Q4 fixed 45-degree fixtures.
for i in range(64):
    f=fresh_fixture(f"Q4_{i+1:03d}",theta_fixed=math.pi/4)
    st,rec=score_fixture(f,allow_near=False)
    if st!="PASS": q4_fail.append({"id":f["id"],**rec})
Q4=len(q4_fail)==0

# Q5 general planar fixtures, all retained; near boundary reported.
scored5=0
for i in range(128):
    f=fresh_fixture(f"Q5_{i+1:03d}")
    st,rec=score_fixture(f,allow_near=True)
    if st=="NEAR": near.append({"id":f["id"],**rec})
    elif st=="PASS": scored5+=1
    else: q5_fail.append({"id":f["id"],**rec})
Q5=len(q5_fail)==0
Q6=max_poly_err<=POLY_TOL

# Q7 exact boundary firewall.
boundary_controls=[
    {"theta":math.pi/4,"gamma":1.0,"omega":0.25},
    {"theta":math.pi/6,"gamma":2.0,"omega":math.sqrt(3)/4},
]
boundary_records=[]; q7=True
for i,bc in enumerate(boundary_controls,1):
    f={"id":f"Q7_{i}","theta":bc["theta"],"gamma":bc["gamma"],"omega":bc["omega"],"kappa":0.3,"eta":0.7,"base":[0.2,0.1,-0.3]}
    _,A,_,_,Vt,_=full_matrices(f)
    dd,rank,sv=dark_dim_full(f,A,Vt)
    refusal="REFUSE_QUOTIENT_DIMENSION" if dd==2 else "UNEXPECTED_DARK_DIMENSION"
    good=(rank==1 and dd==2 and refusal=="REFUSE_QUOTIENT_DIMENSION")
    q7=q7 and good
    boundary_records.append({"id":f["id"],"rank":rank,"dark_dim":dd,"refusal":refusal,"pass":good,"singular_values":sv})
Q7=q7

status="PASS_PLANAR_QUOTIENT_INVARIANTS" if all([Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7]) else "PLANAR_QUOTIENT_INVARIANT_FAILURE"
result={
    "schema":"stability-arc-planar-quotient-invariants-v0.1",
    "phase_status":status,
    "environment":{"python":platform.python_version(),"numpy":np.__version__,"sympy":sp.__version__},
    "exact":{
        "A_phys":str(Acan),"A_record":str(Arcan),"B":str(Bcan),
        "physical_coefficients":{"c1":str(cp[0]),"c2":str(cp[1]),"c3":str(cp[2])},
        "record_coefficients":{"c1":str(cr[0]),"c2":str(cr[1]),"c3":str(cr[2])},
        "c1_displacement":str(sp.factor(cr[0]-cp[0])),
    },
    "criteria":{
        "Q0":{"status":"PASS" if Q0 else "FAIL"},
        "Q1":{"status":"PASS" if Q1 else "FAIL"},
        "Q2":{"status":"PASS" if Q2 else "FAIL"},
        "Q3":{"status":"PASS" if Q3 else "FAIL"},
        "Q4":{"status":"PASS" if Q4 else "FAIL","failure_count":len(q4_fail)},
        "Q5":{"status":"PASS" if Q5 else "FAIL","fresh_total":128,"scored":scored5,"near_boundary_count":len(near),"failure_count":len(q5_fail)},
        "Q6":{"status":"PASS" if Q6 else "FAIL","max_coordinate_poly_error":max_poly_err},
        "Q7":{"status":"PASS" if Q7 else "FAIL","controls":boundary_records},
    },
    "max_matrix_error":max_matrix_err,
    "max_coefficient_error":max_coeff_err,
    "near_boundary":near,
    "q4_failures":q4_fail,
    "q5_failures":q5_fail,
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps({"phase_status":status,"criteria":result["criteria"],"max_matrix_error":max_matrix_err,"max_coefficient_error":max_coeff_err},indent=2,sort_keys=True))
