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
OUT=RESULTS/"dephasing_augmented_planar_transfer_v01.json"

SEED=2026082919
N=256
NEAR_TOL=1e-8
DARK_TOL=5e-10
MATRIX_TOL=2e-9
COEFF_TOL=2e-8
MOMENT_TOL=5e-9
NULL_TOL=1e-9

sx=np.array([[0,1],[1,0]],complex)
sy=np.array([[0,-1j],[1j,0]],complex)
sz=np.array([[1,0],[0,-1]],complex)
I2=np.eye(2,dtype=complex)
sm=np.array([[0,1],[0,0]],complex)
BASIS=[0.5*sx,0.5*sy,0.5*sz]
PAULI=[sx,sy,sz]
SYM_BASIS=[np.array([[1.,0.],[0.,0.]]),np.array([[0.,1.],[1.,0.]]),np.array([[0.,0.],[0.,1.]])]
EY=np.array([0.,1.,0.])


def max_abs(a):
    a=np.asarray(a)
    return 0.0 if a.size==0 else float(np.max(np.abs(a)))

def relabs(a,b): return abs(a-b)/max(1.0,abs(a),abs(b))

def comm(a,b): return a@b-b@a

def dissipator(c,rho):
    cd=c.conj().T; cdc=cd@c
    return c@rho@cd-0.5*(cdc@rho+rho@cdc)

def rho_from_bloch(r): return 0.5*(I2+r[0]*sx+r[1]*sy+r[2]*sz)

def coords(op):
    vals=[complex(np.trace(p@op)) for p in PAULI]
    return np.array([v.real for v in vals]),max(abs(v.imag) for v in vals)

def linear_matrix(action):
    cols=[]; imag=0.0
    for e in BASIS:
        c,im=coords(action(e)); cols.append(c); imag=max(imag,im)
    return np.column_stack(cols),imag

def Xtheta(theta): return 0.5*(math.sin(theta)*sx+math.cos(theta)*sz)

def mu(X,rho): return float(np.trace(X@rho).real)

def h_super(X,rho): return X@rho+rho@X-2*mu(X,rho)*rho

def delta_h(X,rho,e):
    dm=float(np.trace(X@e).real)
    return X@e+e@X-2*mu(X,rho)*e-2*dm*rho

def build(f,X=None):
    if X is None: X=Xtheta(f["theta"])
    rho=rho_from_bloch(f["base"])
    H=0.5*f["omega"]*sy
    cd=math.sqrt(f["gamma"])*sm
    cp=math.sqrt(f["gamma_phi"]/2.0)*sz
    def L(e):
        return -1j*comm(H,e)+dissipator(cd,e)+dissipator(cp,e)+2*f["kappa"]*dissipator(X,e)
    A,ia=linear_matrix(L)
    amp=math.sqrt(2*f["eta"]*f["kappa"])
    B,ib=linear_matrix(lambda e: amp*delta_h(X,rho,e))
    h,ih=coords(h_super(X,rho))
    Vt=np.array([[float(np.trace(X@e).real) for e in BASIS]])
    U=-4*f["eta"]*f["kappa"]*h.reshape(-1,1)
    Ar=A+U@Vt
    return rho,A,Ar,B,Vt,max(ia,ib,ih,max_abs(np.imag(Ar)))

def dark_space(A,Vt):
    O=np.vstack([Vt,Vt@A,Vt@A@A])
    _,s,vh=np.linalg.svd(O,full_matrices=True)
    rank=int(np.sum(s>NULL_TOL)); D=vh[rank:].T.copy()
    if D.size: D,_=np.linalg.qr(D)
    return O,s,D,rank

def Kfull(A,B):
    n=A.shape[0]
    return np.kron(np.eye(n),A)+np.kron(A,np.eye(n))+np.kron(B,B)

def moment(A,B,P): return A@P+P@A.T+B@P@B.T

def symcoords(P): return np.array([P[0,0],0.5*(P[0,1]+P[1,0]),P[1,1]],float)

def Gnum(A,B): return np.column_stack([symcoords(moment(A,B,E)) for E in SYM_BASIS])

def coeff_direct(A,B): return np.real_if_close(np.poly(Gnum(A,B))).astype(float)

def canonical(f):
    th=f["theta"]; sn,cs=math.sin(th),math.cos(th); r=np.asarray(f["base"],float)
    u=sn*r[0]+cs*r[2]; v=cs*r[0]-sn*r[2]; q=f["eta"]*f["kappa"]
    a=f["gamma"]/2+f["gamma_phi"]; b=f["gamma"]
    p=a*sn*sn+b*cs*cs
    d=f["kappa"]+a*cs*cs+b*sn*sn
    h=(b-a)*sn*cs
    Ap=np.array([[-p,h-f["omega"]],[h+f["omega"],-d]],float)
    B=-math.sqrt(2*q)*np.array([[2*u,0],[v,u]],float)
    Ar=Ap+np.array([[-2*q*(1-u*u),0],[2*q*u*v,0]],float)
    return Ap,Ar,B,{"u":u,"v":v,"q":q,"p":p,"d":d,"h":h,"a":a,"b":b}

def quotient_full(f,A,Ar,B):
    sn,cs=math.sin(f["theta"]),math.cos(f["theta"])
    C=np.array([[sn,cs],[0.,0.],[cs,-sn]],float); L=C.T
    return L@A@C,L@Ar@C,L@B@C,L,C

# Independent closed-form canonical coefficient evaluator from the previously derived p,d,h algebra.
def coeff_formula(p,d,h,w,q,u,v,record=False):
    if not record:
        c1=3*d+3*p-14*q*u*u
        c2=2*(d*d+4*d*p-17*d*q*u*u-2*h*h-6*h*q*u*v+p*p-11*p*q*u*u+28*q*q*u**4+6*q*u*v*w+2*w*w)
        F=(-d*d*p+4*d*d*q*u*u+d*h*h+4*d*h*q*u*v-d*p*p+9*d*p*q*u*u-20*d*q*q*u**4-4*d*q*u*v*w-d*w*w+h*h*p-5*h*h*q*u*u+h*h*q*v*v+2*h*p*q*u*v-12*h*q*q*u**3*v-2*h*q*v*v*w+p*p*q*u*u-8*p*q*q*u**4-2*p*q*u*v*w-p*w*w+16*q**3*u**6+12*q*q*u**3*v*w+5*q*u*u*w*w+q*v*v*w*w)
        c3=-4*F
    else:
        c1=3*d+3*p-20*q*u*u+6*q
        c2=2*(d*d+4*d*p-25*d*q*u*u+8*d*q-2*h*h-10*h*q*u*v+p*p-15*p*q*u*u+4*p*q+54*q*q*u**4-30*q*q*u*u+4*q*q+10*q*u*v*w+2*w*w)
        F=(-d*d*p+6*d*d*q*u*u-2*d*d*q+d*h*h+6*d*h*q*u*v-d*p*p+13*d*p*q*u*u-4*d*p*q-42*d*q*q*u**4+26*d*q*q*u*u-4*d*q*q-6*d*q*u*v*w-d*w*w+h*h*p-7*h*h*q*u*u+h*h*q*v*v+2*h*h*q+4*h*p*q*u*v-30*h*q*q*u**3*v+8*h*q*q*u*v-2*h*q*v*v*w+p*p*q*u*u-12*p*q*q*u**4+4*p*q*q*u*u-4*p*q*u*v*w-p*w*w+36*q**3*u**6-24*q**3*u**4+4*q**3*u*u+30*q*q*u**3*v*w-8*q*q*u*v*w+7*q*u*u*w*w+q*v*v*w*w-2*q*w*w)
        c3=-4*F
    return np.array([1.0,c1,c2,c3],float)

# ---------- symbolic Hilbert-space derivation ----------
I=sp.I
g,gp,k,eta,w,th=sp.symbols("g gp k eta w th", positive=True, real=True)
rx,ry,rz,u,v=sp.symbols("rx ry rz u v", real=True)
sx_s=sp.Matrix([[0,1],[1,0]]); sy_s=sp.Matrix([[0,-I],[I,0]]); sz_s=sp.Matrix([[1,0],[0,-1]])
ident=sp.eye(2); sm_s=sp.Matrix([[0,1],[0,0]]); pauli=[sx_s,sy_s,sz_s]; basis=[p/2 for p in pauli]
sn,cs=sp.sin(th),sp.cos(th); X=(sn*sx_s+cs*sz_s)/2; H=w*sy_s/2; cd=sp.sqrt(g)*sm_s; cphi=sp.sqrt(gp/2)*sz_s

def sdiss(cop,state):
    cdag=cop.conjugate().T; cc=cdag*cop
    return cop*state*cdag-sp.Rational(1,2)*(cc*state+state*cc)

def scoords(op): return sp.Matrix([sp.simplify(sp.trace(P*op)) for P in pauli])
def Ls(e): return -I*(H*e-e*H)+sdiss(cd,e)+sdiss(cphi,e)+2*k*sdiss(X,e)
A_s=sp.Matrix.hstack(*[scoords(Ls(e)) for e in basis]).applyfunc(sp.trigsimp)
a_s=g/2+gp; b_s=g
A_target=sp.Matrix([[-a_s-k*cs**2,0,w+k*sn*cs],[0,-a_s-k,0],[-w+k*sn*cs,0,-b_s-k*sn**2]])
D0=all(sp.trigsimp(A_s[i,j]-A_target[i,j])==0 for i in range(3) for j in range(3))
# observability determinant on x-z
Axz=sp.Matrix([[A_s[0,0],A_s[0,2]],[A_s[2,0],A_s[2,2]]]); nrow=sp.Matrix([[sn,cs]])
detobs=sp.trigsimp(sp.Matrix.vstack(nrow,nrow*Axz).det()); delta=w-(b_s-a_s)*sn*cs
D1=sp.trigsimp(detobs-delta)==0
# stochastic identities from Hilbert measurement Jacobian
rho=(ident+rx*sx_s+ry*sy_s+rz*sz_s)/2; mus=sp.simplify(sp.trace(X*rho)); amp=sp.sqrt(2*eta*k)
def dh(e):
    dm=sp.simplify(sp.trace(X*e)); return X*e+e*X-2*mus*e-2*dm*rho
B_s=sp.Matrix.hstack(*[scoords(amp*dh(e)) for e in basis]).applyfunc(sp.trigsimp)
ey=sp.Matrix([0,1,0]); V=sp.Matrix([[sn/2,0,cs/2]]); ndotr=sn*rx+cs*rz
D2=(sp.simplify((V*ey)[0])==0 and all(sp.trigsimp(t)==0 for t in (A_s*ey+ (a_s+k)*ey)) and all(sp.trigsimp(t)==0 for t in (B_s*ey+amp*ndotr*ey)))
# canonical transform
Q=sp.Matrix([[sn,cs],[cs,-sn]]); Alab=Axz; Blab=sp.Matrix([[B_s[0,0],B_s[0,2]],[B_s[2,0],B_s[2,2]]])
mu_xz=sn*rx+cs*rz; n2=sp.Matrix([sn,cs]); r2=sp.Matrix([rx,rz]); hvec=n2-mu_xz*r2; Arlab=Alab-2*eta*k*hvec*n2.T
subsuv={rx:sn*u+cs*v,rz:cs*u-sn*v}; q_s=eta*k
p_s=a_s*sn**2+b_s*cs**2; d_s=k+a_s*cs**2+b_s*sn**2; h_s=(b_s-a_s)*sn*cs
Acan=sp.Matrix([[-p_s,h_s-w],[h_s+w,-d_s]]); Bcan=-sp.sqrt(2*q_s)*sp.Matrix([[2*u,0],[v,u]]); Arcan=Acan+sp.Matrix([[-2*q_s*(1-u**2),0],[2*q_s*u*v,0]])
Aq=sp.simplify(Q*Alab*Q.T); Bq=sp.simplify(Q*Blab.subs(subsuv)*Q.T); Arq=sp.simplify(Q*Arlab.subs(subsuv)*Q.T)
D3=all(sp.trigsimp(Aq[i,j]-Acan[i,j])==0 and sp.trigsimp(Bq[i,j]-Bcan[i,j])==0 and sp.trigsimp(Arq[i,j]-Arcan[i,j])==0 for i in range(2) for j in range(2))
# gamma_phi=0 reduction to preceding maps
D4=(sp.trigsimp(delta.subs(gp,0)-(w-g*sn*cs/2))==0 and sp.trigsimp(p_s.subs(gp,0)-g*(1+cs**2)/2)==0 and sp.trigsimp(d_s.subs(gp,0)-(k+g*(1+sn**2)/2))==0 and sp.trigsimp(h_s.subs(gp,0)-g*sp.sin(2*th)/4)==0)

# ---------- fresh numerical transfer ----------
rng=np.random.default_rng(SEED); failures=[]; near=[]; max_dark=max_matrix=max_coeff=max_moment=max_axis=max_imag=0.0; scored=0
for i in range(N):
    gamma=float(10**rng.uniform(math.log10(.1),math.log10(2.0))); gphi=float(10**rng.uniform(math.log10(.001),math.log10(2.0))); kap=float(10**rng.uniform(math.log10(.05),math.log10(2.0))); eff=float(rng.uniform(.05,.95)); omega=float(rng.uniform(.05,3.0)); theta=float(rng.uniform(-math.pi,math.pi)); rad=float(rng.uniform(.05,.85)); vec=rng.normal(size=3); vec=vec/np.linalg.norm(vec)
    f={"id":f"DP{i+1:03d}","gamma":gamma,"gamma_phi":gphi,"kappa":kap,"eta":eff,"omega":omega,"theta":theta,"base":(rad*vec).tolist()}
    aa=gamma/2+gphi; bb=gamma; delt=omega-(bb-aa)*math.sin(theta)*math.cos(theta); nd=abs(delt)/(aa+bb+omega)
    rho,A,Ar,B,Vt,imag=build(f); max_imag=max(max_imag,imag); O,sv,D,rank=dark_space(A,Vt)
    if nd<=NEAR_TOL:
        near.append({"id":f["id"],"normalized_delta":nd,"rank":rank,"dark_dim":int(D.shape[1])}); continue
    scored+=1; reasons=[]
    if D.shape[1]!=1:
        failures.append({"id":f["id"],"reasons":["DARK_DIMENSION"],"rank":rank}); continue
    overlap=abs(float(D[:,0]@EY)); max_axis=max(max_axis,abs(1-overlap)); Pperp=np.eye(3)-D@D.T
    derr=max(max_abs(Vt@D),max_abs(Pperp@A@D),max_abs(Pperp@Ar@D),max_abs(Pperp@B@D)); max_dark=max(max_dark,derr)
    if overlap<1-1e-10: reasons.append("DARK_AXIS")
    if derr>DARK_TOL: reasons.append("DARK_INVARIANCE")
    Apf,Arf,Bf,L,C=quotient_full(f,A,Ar,B); Apc,Arc,Bc,meta=canonical(f); merr=max(max_abs(Apf-Apc),max_abs(Arf-Arc),max_abs(Bf-Bc)); max_matrix=max(max_matrix,merr)
    if merr>MATRIX_TOL: reasons.append("CANONICAL_MATRIX")
    cp=coeff_direct(Apf,Bf); cr=coeff_direct(Arf,Bf); vals=(meta["p"],meta["d"],meta["h"],omega,meta["q"],meta["u"],meta["v"]); cpf=coeff_formula(*vals,record=False); crf=coeff_formula(*vals,record=True); cerr=max(max(relabs(a,b) for a,b in zip(cp,cpf)),max(relabs(a,b) for a,b in zip(cr,crf))); max_coeff=max(max_coeff,cerr)
    if cerr>COEFF_TOL: reasons.append("CANONICAL_COEFFICIENT")
    J=np.kron(L,L); mres=max(max_abs(J@Kfull(A,B)-Kfull(Apf,Bf)@J),max_abs(J@Kfull(Ar,B)-Kfull(Arf,Bf)@J)); max_moment=max(max_moment,mres)
    if mres>MOMENT_TOL: reasons.append("MOMENT_INTERTWINING")
    if imag>1e-11: reasons.append("NONREAL")
    if reasons: failures.append({"id":f["id"],"reasons":reasons,"normalized_delta":nd,"dark_error":derr,"matrix_error":merr,"coefficient_error":cerr,"moment_error":mres})
D5=len(failures)==0

# Exact shifted-boundary controls.
bcs=[{"id":"Bphi1","theta":math.pi/4,"gamma":1.0,"gamma_phi":0.1,"omega":0.2},{"id":"Bphi2","theta":-math.pi/4,"gamma":1.0,"gamma_phi":0.8,"omega":0.15}]
brecords=[]; bok=True
for bc in bcs:
    f={**bc,"kappa":.3,"eta":.7,"base":[.2,.1,-.3]}; aa=f["gamma"]/2+f["gamma_phi"]; bb=f["gamma"]; delt=f["omega"]-(bb-aa)*math.sin(f["theta"])*math.cos(f["theta"]); _,A,_,_,Vt,_=build(f); _,sv,D,rank=dark_space(A,Vt); refusal="REFUSE_QUOTIENT_DIMENSION" if D.shape[1]==2 else "UNEXPECTED_DARK_DIMENSION"; good=abs(delt)<=5e-15 and rank==1 and D.shape[1]==2 and refusal=="REFUSE_QUOTIENT_DIMENSION"; bok=bok and good; brecords.append({"id":bc["id"],"delta":delt,"rank":rank,"dark_dim":int(D.shape[1]),"refusal":refusal,"pass":good,"singular_values":[float(v) for v in sv]})
D6=bok

# Generic out-of-plane refusal.
n3=np.array([1.,1.,1.])/math.sqrt(3); X3=.5*(n3[0]*sx+n3[1]*sy+n3[2]*sz); f3={"gamma":.3,"gamma_phi":.4,"kappa":.2,"eta":.7,"omega":1.1,"theta":0.,"base":[.2,.1,-.3]}; _,A3,_,_,V3,_=build(f3,X3); _,s3,D3,rank3=dark_space(A3,V3); ref3="REFUSE_NO_1D_DARK_FACTOR" if rank3==3 else "UNEXPECTED_OBSERVABILITY_RANK"; D7=rank3==3 and D3.shape[1]==0 and ref3=="REFUSE_NO_1D_DARK_FACTOR"

status="PASS_DEPHASING_AUGMENTED_PLANAR_TRANSFER" if all([D0,D1,D2,D3,D4,D5,D6,D7]) else "DEPHASING_AUGMENTED_TRANSFER_FAILURE"
result={"schema":"stability-arc-dephasing-augmented-planar-transfer-v0.1","phase_status":status,"environment":{"python":platform.python_version(),"numpy":np.__version__,"sympy":sp.__version__},"symbolic":{"delta_phi":str(sp.factor(detobs)),"canonical_p":str(sp.factor(p_s)),"canonical_d":str(sp.factor(d_s)),"canonical_h":str(sp.factor(h_s))},"criteria":{"D0":{"status":"PASS" if D0 else "FAIL"},"D1":{"status":"PASS" if D1 else "FAIL"},"D2":{"status":"PASS" if D2 else "FAIL"},"D3":{"status":"PASS" if D3 else "FAIL"},"D4":{"status":"PASS" if D4 else "FAIL"},"D5":{"status":"PASS" if D5 else "FAIL","fresh_total":N,"scored":scored,"near_boundary_count":len(near),"failure_count":len(failures),"max_dark_error":max_dark,"max_matrix_error":max_matrix,"max_coefficient_error":max_coeff,"max_moment_error":max_moment,"max_dark_axis_error":max_axis,"max_imag":max_imag},"D6":{"status":"PASS" if D6 else "FAIL","controls":brecords},"D7":{"status":"PASS" if D7 else "FAIL","rank":rank3,"dark_dim":int(D3.shape[1]),"refusal":ref3,"singular_values":[float(v) for v in s3]}},"near_boundary":near,"failures":failures}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"phase_status":status,"criteria":result["criteria"]},indent=2,sort_keys=True))
