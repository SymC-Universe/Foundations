#!/usr/bin/env python3
import json
import math
import platform
from pathlib import Path

import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parent
RESULTS=ROOT/"results"
RESULTS.mkdir(parents=True,exist_ok=True)
OUT=RESULTS/"orientation_c3_decomposition_v01.json"

SEED=2026082915
N=512
TOL=2e-10
R_ACTIVE=np.array([[1.2,0.3],[-0.2,0.9]],float)
SYM_NP=[np.array([[1.,0.],[0.,0.]]),np.array([[0.,1.],[1.,0.]]),np.array([[0.,0.],[0.,1.]])]


def relabs(a,b): return abs(a-b)/max(1.0,abs(a),abs(b))

def moment_np(A,B,P): return A@P+P@A.T+B@P@B.T

def coords_np(P): return np.array([P[0,0],0.5*(P[0,1]+P[1,0]),P[1,1]],float)

def G_np(A,B): return np.column_stack([coords_np(moment_np(A,B,E)) for E in SYM_NP])

def inv_np(G):
    tr=float(np.trace(G)); c1=-tr; c2=.5*(tr*tr-float(np.trace(G@G))); c3=-float(np.linalg.det(G)); return c1,c2,c3


def active_np(g,k,q,w,a,b,sgn,record=False):
    x=sgn*a; z=b; ss=math.sqrt(2*q)
    A=np.array([[-(g/2+k),w],[-w,-g]],float)
    if record: A+=np.array([[0.,2*q*z*x],[0.,-2*q*(1-z*z)]],float)
    B=np.array([[-ss*z,-ss*x],[0.,-2*ss*z]],float)
    return A,B


def exact_parts(g,k,q,w,a,b,record=False):
    if not record:
        A=2*(3*g+2*k-2*q*a*a-10*q*b*b)
        C=(g-4*q*b*b)*(3*g+2*k-8*q*b*b)*(g+2*k-2*q*b*b)
        M=16*q*a*b*w*(g+k-3*q*b*b)
    else:
        A=2*(3*g+2*k+4*q-2*q*a*a-14*q*b*b)
        C=(g+2*k-2*q*b*b)*(g+2*q-6*q*b*b)*(3*g+2*k+4*q-12*q*b*b)
        M=4*q*a*b*w*(7*g+6*k+8*q-30*q*b*b)
    return A*w*w+C,M


def label(cp,cr):
    if cp==0 or cr==0: return "BOUNDARY_C3"
    if cp>0 and cr<0: return "DESTAB_C3"
    if cp<0 and cr>0: return "STAB_C3"
    return "OTHER_C3"

# symbolic independent moment construction
g,k,q,w,a,b,s=sp.symbols('g k q w a b s', real=True)
ss=sp.sqrt(2*q)
x=s*a; z=b
Ap=sp.Matrix([[-(g/2+k),w],[-w,-g]])
B=sp.Matrix([[-ss*z,-ss*x],[0,-2*ss*z]])
Ar=Ap+sp.Matrix([[0,2*q*z*x],[0,-2*q*(1-z**2)]])
SYM_SP=[sp.Matrix([[1,0],[0,0]]),sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,0],[0,1]])]

def G_sp(A,Bm):
    cols=[]
    for E in SYM_SP:
        P=sp.expand(A*E+E*A.T+Bm*E*Bm.T)
        cols.append(sp.Matrix([P[0,0],sp.simplify((P[0,1]+P[1,0])/2),P[1,1]]))
    return sp.Matrix.hstack(*cols)

Gp=G_sp(Ap,B); Gr=G_sp(Ar,B)
c1p=sp.factor(-sp.trace(Gp)); c1r=sp.factor(-sp.trace(Gr))
c3p=sp.factor(-Gp.det()); c3r=sp.factor(-Gr.det())
O0=Gp.shape==(3,3) and Gr.shape==(3,3)

Ap3=2*(3*g+2*k-2*q*a**2-10*q*b**2)
Cp3=(g-4*q*b**2)*(3*g+2*k-8*q*b**2)*(g+2*k-2*q*b**2)
Mp=16*q*a*b*w*(g+k-3*q*b**2)
Ar3=2*(3*g+2*k+4*q-2*q*a**2-14*q*b**2)
Cr3=(g+2*k-2*q*b**2)*(g+2*q-6*q*b**2)*(3*g+2*k+4*q-12*q*b**2)
Mr=4*q*a*b*w*(7*g+6*k+8*q-30*q*b**2)
Ep=Ap3*w**2+Cp3; Er=Ar3*w**2+Cr3

pplus=sp.simplify(c3p.subs(s,1)); pminus=sp.simplify(c3p.subs(s,-1)); rplus=sp.simplify(c3r.subs(s,1)); rminus=sp.simplify(c3r.subs(s,-1))
O1=all([
    sp.simplify(pplus-(Ep+Mp))==0,
    sp.simplify(pminus-(Ep-Mp))==0,
    sp.simplify(rplus-(Er+Mr))==0,
    sp.simplify(rminus-(Er-Mr))==0,
])
O2=(sp.simplify(pplus-pminus-2*Mp)==0 and sp.simplify(rplus-rminus-2*Mr)==0 and sp.simplify(c1p.subs(s,1)-c1p.subs(s,-1))==0 and sp.simplify(c1r.subs(s,1)-c1r.subs(s,-1))==0)
O3=(sp.simplify(Mp.subs(q,0))==0 and sp.simplify(Mr.subs(q,0))==0 and sp.simplify((pplus-pminus).subs(q,0))==0 and sp.simplify((rplus-rminus).subs(q,0))==0)

# O4/O5 fresh controls
rng=np.random.default_rng(SEED)
max_c3_err=0.0; label_mismatch=0; max_basis_err=0.0; c1_sign_mismatch=0
class_counts={"NEG":{"DESTAB_C3":0,"STAB_C3":0,"OTHER_C3":0,"BOUNDARY_C3":0},"POS":{"DESTAB_C3":0,"STAB_C3":0,"OTHER_C3":0,"BOUNDARY_C3":0}}
for i in range(N):
    gv=float(10**rng.uniform(math.log10(.2),math.log10(3.0)))
    kv=float(10**rng.uniform(math.log10(.1),math.log10(100.0)))
    eta=float(rng.uniform(.001,.95)); qv=eta*kv
    wv=float(10**rng.uniform(-3,3)); rv=float(rng.uniform(.2,.9999)); phi=float(rng.uniform(0,math.pi/2)); av=rv*math.cos(phi); bv=rv*math.sin(phi)
    sign_c1=[]
    for sgn,name in [(-1,"NEG"),(1,"POS")]:
        Apn,Bn=active_np(gv,kv,qv,wv,av,bv,sgn,False); Arn,_=active_np(gv,kv,qv,wv,av,bv,sgn,True)
        Gpn=G_np(Apn,Bn); Grn=G_np(Arn,Bn); c1pn,_,c3pn=inv_np(Gpn); c1rn,_,c3rn=inv_np(Grn)
        Epn,Mpn=exact_parts(gv,kv,qv,wv,av,bv,False); Ern,Mrn=exact_parts(gv,kv,qv,wv,av,bv,True)
        c3pe=Epn+sgn*Mpn; c3re=Ern+sgn*Mrn
        max_c3_err=max(max_c3_err,relabs(c3pn,c3pe),relabs(c3rn,c3re))
        lab_e=label(c3pe,c3re); lab_d=label(c3pn,c3rn)
        class_counts[name][lab_e]+=1
        if lab_e!=lab_d: label_mismatch+=1
        sign_c1.append((c1pn,c1rn))
        Rin=np.linalg.inv(R_ACTIVE); Apt=Rin@Apn@R_ACTIVE; Art=Rin@Arn@R_ACTIVE; Bt=Rin@Bn@R_ACTIVE
        c1pt,_,c3pt=inv_np(G_np(Apt,Bt)); c1rt,_,c3rt=inv_np(G_np(Art,Bt))
        max_basis_err=max(max_basis_err,relabs(c1pt,c1pn),relabs(c3pt,c3pn),relabs(c1rt,c1rn),relabs(c3rt,c3rn))
    if relabs(sign_c1[0][0],sign_c1[1][0])>TOL or relabs(sign_c1[0][1],sign_c1[1][1])>TOL: c1_sign_mismatch+=1

O4=max_c3_err<=TOL and label_mismatch==0 and c1_sign_mismatch==0
O5=max_basis_err<=TOL
status="PASS_ORIENTATION_C3_DECOMPOSITION" if all([O0,O1,O2,O3,O4,O5]) else "ORIENTATION_DERIVATION_FAILURE"
result={
    "schema":"stability-arc-orientation-c3-decomposition-v0.1",
    "phase_status":status,
    "environment":{"python":platform.python_version(),"numpy":np.__version__,"sympy":sp.__version__},
    "exact":{"c1_phys":str(c1p),"c1_record":str(c1r),"E_phys":str(sp.factor(Ep)),"M_phys":str(sp.factor(Mp)),"E_record":str(sp.factor(Er)),"M_record":str(sp.factor(Mr))},
    "criteria":{
        "O0":{"status":"PASS" if O0 else "FAIL"},
        "O1":{"status":"PASS" if O1 else "FAIL"},
        "O2":{"status":"PASS" if O2 else "FAIL"},
        "O3":{"status":"PASS" if O3 else "FAIL"},
        "O4":{"status":"PASS" if O4 else "FAIL","max_c3_error":max_c3_err,"label_mismatch_count":label_mismatch,"c1_sign_mismatch_count":c1_sign_mismatch,"fresh_tuples":N,"class_counts":class_counts},
        "O5":{"status":"PASS" if O5 else "FAIL","max_basis_invariant_error":max_basis_err},
    }
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps(result,indent=2,sort_keys=True))
