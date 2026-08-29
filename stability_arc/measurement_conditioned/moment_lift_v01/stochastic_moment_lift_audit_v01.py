#!/usr/bin/env python3
import json, math, platform
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / 'results'; RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / 'stochastic_moment_lift_audit_v01.json'

FIXTURES=[
 {'id':'M1','eta':0.68,'gamma':0.19,'kappa':0.13,'omega':0.91,'base':[0.21,0.09,-0.24]},
 {'id':'M2','eta':0.77,'gamma':0.43,'kappa':0.21,'omega':1.07,'base':[-0.16,-0.28,0.19]},
 {'id':'M3','eta':0.59,'gamma':0.31,'kappa':0.09,'omega':0.73,'base':[0.08,-0.11,0.36]},]
P_CONTROLS=[np.diag([0.7,0.4,0.2]),np.array([[0.6,0.08,-0.04],[0.08,0.5,0.06],[-0.04,0.06,0.4]],float)]
DT_C=1e-3; DT_F=5e-4
G0=5e-13; G2=2e-9; G4=5e-12; G6=1e-10
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]],complex); sz=np.array([[1,0],[0,-1]],complex)
I2=np.eye(2,dtype=complex); sm=np.array([[0,1],[0,0]],complex); xop=0.5*sz
BASIS=[0.5*sx,0.5*sy,0.5*sz]; PAULI=[sx,sy,sz]

def comm(a,b): return a@b-b@a
def dissipator(c,s):
 cd=c.conj().T; cdc=cd@c; return c@s@cd-0.5*(cdc@s+s@cdc)
def rho(v): return 0.5*(I2+v[0]*sx+v[1]*sy+v[2]*sz)
def mu(s): return float(np.trace(xop@s).real)
def h_super(s): return xop@s+s@xop-2*mu(s)*s
def delta_h(s,e):
 dm=float(np.trace(xop@e).real); return xop@e+e@xop-2*mu(s)*e-2*dm*s
def L(s,g,k,w): return -1j*comm(0.5*w*sy,s)+dissipator(math.sqrt(g)*sm,s)+2*k*dissipator(xop,s)
def coords(o): return np.array([float(np.trace(p@o).real) for p in PAULI])
def lin(action): return np.column_stack([coords(action(e)) for e in BASIS])
def maxabs(a): return float(np.max(np.abs(a)))
def vecF(a): return np.asarray(a).reshape(-1,order='F')
def Kfull(A,B): return np.kron(np.eye(3),A)+np.kron(A,np.eye(3))+np.kron(B,B)
def G(A,B,P): return A@P+P@A.T+B@P@B.T

def rx(t):
 c,s=math.cos(t),math.sin(t); return np.array([[1,0,0],[0,c,-s],[0,s,c]],float)
def ry(t):
 c,s=math.cos(t),math.sin(t); return np.array([[c,0,s],[0,1,0],[-s,0,c]],float)
def rz(t):
 c,s=math.cos(t),math.sin(t); return np.array([[c,-s,0],[s,c,0],[0,0,1]],float)
Q=rz(0.37)@ry(-0.52)@rx(0.29)

E=[]
for i in range(3):
 for j in range(3):
  a=np.zeros((3,3)); a[i,j]=1; E.append(a)
S=[]
for i in range(3):
 a=np.zeros((3,3)); a[i,i]=1; S.append(a)
for i,j in [(0,1),(0,2),(1,2)]:
 a=np.zeros((3,3)); a[i,j]=a[j,i]=1/math.sqrt(2); S.append(a)
U=np.column_stack([vecF(s) for s in S])
R=np.array([[np.sum(S[i]*(Q.T@S[j]@Q)) for j in range(6)] for i in range(6)])
R_orth=maxabs(R@R.T-np.eye(6))

def sigma_cov(P,A,B,dt):
 Lc=np.linalg.cholesky(P); out=np.zeros((3,3)); w=1/12
 for i in range(3):
  v=math.sqrt(3)*Lc[:,i]
  for sign in (-1,1):
   r=sign*v
   for nsign in (-1,1):
    rp=(np.eye(3)+A*dt+B*(nsign*math.sqrt(dt)))@r
    out += w*np.outer(rp,rp)
 return out

def mincost_match(vals,target):
 import itertools
 best=1e99
 for perm in itertools.permutations(range(len(target))):
  best=min(best,max(abs(vals[i]-target[perm[i]]) for i in range(len(vals))))
 return float(best)

records=[]
for f in FIXTURES:
 r0=rho(f['base']); ev=np.linalg.eigvalsh(r0)
 if ev.min()<=0: raise RuntimeError('fixture outside Bloch ball')
 Aphys=lin(lambda e:L(e,f['gamma'],f['kappa'],f['omega']))
 amp=math.sqrt(2*f['eta']*f['kappa']); B=amp*lin(lambda e:delta_h(r0,e))
 h=coords(h_super(r0)); m=np.array([float(np.trace(xop@e).real) for e in BASIS])
 dA=-4*f['eta']*f['kappa']*np.outer(h,m); Arec=Aphys+dA
 ch=[]
 for name,A in [('phys',Aphys),('rec',Arec)]:
  K=Kfull(A,B); Ksym=U.T@K@U
  m0=max(maxabs(K@vecF(e)-vecF(G(A,B,e))) for e in E)
  anti=max(maxabs(G(A,B,s)-G(A,B,s).T) for s in S)
  direct=np.array([[np.sum(S[i]*G(A,B,S[j])) for j in range(6)] for i in range(6)])
  m1proj=maxabs(direct-Ksym)
  cov=[]
  for idx,P in enumerate(P_CONTROLS):
   Dc=(sigma_cov(P,A,B,DT_C)-P)/DT_C; Df=(sigma_cov(P,A,B,DT_F)-P)/DT_F
   DR=2*Df-Dc; gp=G(A,B,P)
   cov.append({'P':idx+1,'rich':maxabs(DR-gp),'vec':maxabs(vecF(DR)-K@vecF(P)),'coarse':maxabs(Dc-gp),'fine':maxabs(Df-gp),'monotone':maxabs(Df-gp)<=maxabs(Dc-gp)+1e-15})
  Ap=Q.T@A@Q; Bp=Q.T@B@Q; Kp=Kfull(Ap,Bp); Smat=np.kron(Q.T,Q.T)
  m4full=maxabs(Kp-Smat@K@np.linalg.inv(Smat)); Ksymp=U.T@Kp@U; m4sym=maxabs(Ksymp-R@Ksym@R.T)
  ch.append({'name':name,'K':K,'Ksym':Ksym,'M0':m0,'M1anti':anti,'M1proj':m1proj,'cov':cov,'M4full':m4full,'M4sym':m4sym})
 Kp,Kr=ch[0]['K'],ch[1]['K']; Kps,Krs=ch[0]['Ksym'],ch[1]['Ksym']; dK=Kr-Kp; exp=np.kron(np.eye(3),dA)+np.kron(dA,np.eye(3)); dKs=Krs-Kps
 m3=max(maxabs(dK-exp),maxabs(dKs-U.T@dK@U))
 joint=np.zeros((12,12)); joint[:6,:6]=Kps; joint[6:,6:]=Krs
 m5=max(maxabs(joint[:6,:6]-Kps),maxabs(joint[6:,6:]-Krs),maxabs(joint[:6,6:]),maxabs(joint[6:,:6]))
 records.append({'id':f['id'],'rho_min_eig':float(ev.min()),'channels':[{k:v for k,v in c.items() if k not in ('K','Ksym')} for c in ch],'M3':m3,'M5':m5,'Rorth':R_orth})

blocks=[np.array([[-0.3,1.1],[-1.1,-0.3]]),np.array([[-0.7,0.4],[-0.4,-0.7]]),np.array([[-1.2,0.2],[-0.2,-1.2]])]
m6errs=[]
for A in blocks:
 K=np.kron(np.eye(2),A)+np.kron(A,np.eye(2)); vals=np.linalg.eigvals(K); lam=np.linalg.eigvals(A); targ=np.array([a+b for a in lam for b in lam]); m6errs.append(mincost_match(vals,targ))

criteria={}
criteria['M0']={'status':'PASS' if max(c['M0'] for r in records for c in r['channels'])<=G0 else 'FAIL','max_error':max(c['M0'] for r in records for c in r['channels']),'gate':G0}
criteria['M1']={'status':'PASS' if max(max(c['M1anti'],c['M1proj']) for r in records for c in r['channels'])<=G0 else 'FAIL','max_error':max(max(c['M1anti'],c['M1proj']) for r in records for c in r['channels']),'gate':G0}
criteria['M2']={'status':'PASS' if all(x['rich']<=G2 and x['vec']<=G2 and x['monotone'] for r in records for c in r['channels'] for x in c['cov']) else 'FAIL','max_rich':max(x['rich'] for r in records for c in r['channels'] for x in c['cov']),'max_vec':max(x['vec'] for r in records for c in r['channels'] for x in c['cov']),'gate':G2}
criteria['M3']={'status':'PASS' if max(r['M3'] for r in records)<=G0 else 'FAIL','max_error':max(r['M3'] for r in records),'gate':G0}
criteria['M4']={'status':'PASS' if R_orth<=G0 and max(max(c['M4full'],c['M4sym']) for r in records for c in r['channels'])<=G4 else 'FAIL','R_orth':R_orth,'max_error':max(max(c['M4full'],c['M4sym']) for r in records for c in r['channels']),'gate':G4}
criteria['M5']={'status':'PASS' if max(r['M5'] for r in records)<=G0 else 'FAIL','max_error':max(r['M5'] for r in records),'gate':G0}
criteria['M6']={'status':'PASS' if max(m6errs)<=G6 else 'FAIL','scalar_status':'FULL_MOMENT_OPERATOR_REQUIRED','max_inheritance_error':max(m6errs),'gate':G6}
overall='PASS' if all(v['status']=='PASS' for v in criteria.values()) else 'FAIL'
out={'audit':'stochastic_second_moment_lift_v0.1','status':overall,'python':platform.python_version(),'numpy':np.__version__,'criteria':criteria,'fixtures':records,'m6_errors':m6errs,'representation_status':'FULL_MOMENT_OPERATOR_REQUIRED'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':overall,'criteria':criteria},indent=2))
if overall!='PASS': raise SystemExit(1)
