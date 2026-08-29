#!/usr/bin/env python3
import json, math, platform
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
RESULTS=ROOT/'results'; RESULTS.mkdir(parents=True,exist_ok=True)
OUT=RESULTS/'information_rank_secular_bridge_v01.json'
FIXTURES=[
 {'id':'Q1','eta':0.72,'gamma':0.27,'kappa':0.16,'omega':1.19,'base':[0.14,-0.07,0.31]},
 {'id':'Q2','eta':0.61,'gamma':0.36,'kappa':0.24,'omega':0.88,'base':[-0.23,0.17,0.12]},
 {'id':'Q3','eta':0.83,'gamma':0.15,'kappa':0.11,'omega':1.43,'base':[0.06,0.26,-0.29]}]
CONTROLS=[
 {'id':'C1','A':np.array([[-0.4,1.0,0,0],[-1.0,-0.4,0.2,0],[0,-0.2,-0.7,0.5],[0,0,-0.5,-0.7]],float),'U':np.array([[0.3,-0.2],[0.1,0.4],[-0.25,0.15],[0.2,0.05]],float),'V':np.array([[0.5,0.1],[-0.2,0.35],[0.3,-0.25],[0.15,0.4]],float)},
 {'id':'C2','A':np.array([[-0.5,0.8,0,0,0],[-0.8,-0.5,0.15,0,0],[0,-0.15,-0.65,0.45,0],[0,0,-0.45,-0.65,0.2],[0,0,0,-0.2,-0.9]],float),'U':np.array([[0.2,-0.1,0.05],[0.15,0.25,-0.2],[-0.3,0.1,0.12],[0.05,-0.2,0.3],[0.18,0.07,-0.11]],float),'V':np.array([[0.4,0.05,-0.12],[-0.1,0.3,0.2],[0.25,-0.2,0.15],[0.08,0.22,-0.3],[-0.18,0.1,0.27]],float)}]
PROBES=[0.5+0.7j,0.9+1.2j,1.4+0.35j]
DT=7e-4; Z=0.41; EPS=8e-6; RANK_TOL=1e-12; MOM_RANK_TOL=1e-10
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]],complex); sz=np.array([[1,0],[0,-1]],complex)
I2=np.eye(2,dtype=complex); sm=np.array([[0,1],[0,0]],complex); xop=.5*sz
BASIS=[.5*sx,.5*sy,.5*sz]; PAULI=[sx,sy,sz]

def comm(a,b): return a@b-b@a
def diss(c,s):
 cd=c.conj().T; cdc=cd@c; return c@s@cd-.5*(cdc@s+s@cdc)
def rho(v): return .5*(I2+v[0]*sx+v[1]*sy+v[2]*sz)
def mu(s): return float(np.trace(xop@s).real)
def hsuper(s): return xop@s+s@xop-2*mu(s)*s
def dh(s,e):
 dm=float(np.trace(xop@e).real); return xop@e+e@xop-2*mu(s)*e-2*dm*s
def L(s,g,k,w): return -1j*comm(.5*w*sy,s)+diss(math.sqrt(g)*sm,s)+2*k*diss(xop,s)
def coords(o): return np.array([float(np.trace(p@o).real) for p in PAULI])
def lin(fn): return np.column_stack([coords(fn(e)) for e in BASIS])
def same_noise(s,f,dt,dw): return s+L(s,f['gamma'],f['kappa'],f['omega'])*dt+math.sqrt(2*f['eta']*f['kappa'])*hsuper(s)*dw
def same_record(s,f,dt,dy):
 amp=math.sqrt(2*f['eta']*f['kappa']); obs=math.sqrt(8*f['eta']*f['kappa']); innov=dy-obs*mu(s)*dt
 return s+L(s,f['gamma'],f['kappa'],f['omega'])*dt+amp*hsuper(s)*innov
def jac(mapf,s): return np.column_stack([coords((mapf(s+EPS*e)-mapf(s-EPS*e))/(2*EPS)) for e in BASIS])
def rank(a,tol): return int(np.sum(np.linalg.svd(a,compute_uv=False)>tol))
def maxabs(a): return float(np.max(np.abs(a)))
def adj3(M):
 out=np.zeros((3,3),dtype=complex)
 for i in range(3):
  for j in range(3):
   minor=np.delete(np.delete(M,j,axis=0),i,axis=1)
   out[i,j]=((-1)**(i+j))*np.linalg.det(minor)
 return out
def rx(t):
 c,s=math.cos(t),math.sin(t); return np.array([[1,0,0],[0,c,-s],[0,s,c]],float)
def ry(t):
 c,s=math.cos(t),math.sin(t); return np.array([[c,0,s],[0,1,0],[-s,0,c]],float)
def rz(t):
 c,s=math.cos(t),math.sin(t); return np.array([[c,-s,0],[s,c,0],[0,0,1]],float)
Q=rz(.31)@ry(-.47)@rx(.22)

def sym_basis(n):
 S=[]
 for i in range(n):
  a=np.zeros((n,n)); a[i,i]=1; S.append(a)
 for i in range(n):
  for j in range(i+1,n):
   a=np.zeros((n,n)); a[i,j]=a[j,i]=1/math.sqrt(2); S.append(a)
 return np.column_stack([s.reshape(-1,order='F') for s in S])
def moment_ranks(dA):
 n=dA.shape[0]; dK=np.kron(np.eye(n),dA)+np.kron(dA,np.eye(n)); U=sym_basis(n); dKs=U.T@dK@U
 return rank(dK,MOM_RANK_TOL),rank(dKs,MOM_RANK_TOL)
def secular(A,U,V,z):
 M=z*np.eye(A.shape[0])-A; smin=float(np.min(np.linalg.svd(M,compute_uv=False)))
 if smin<=1e-8: return {'refuse':True,'smin':smin}
 left=np.linalg.det(z*np.eye(A.shape[0])-(A+U@V.T))/np.linalg.det(M)
 right=np.linalg.det(np.eye(U.shape[1])-V.T@np.linalg.solve(M,U))
 return {'refuse':False,'smin':smin,'residual':float(abs(left-right)),'factor_real':float(right.real),'factor_imag':float(right.imag)}

quant=[]
for f in FIXTURES:
 s=rho(f['base']); A=lin(lambda e:L(e,f['gamma'],f['kappa'],f['omega']))
 h=coords(hsuper(s)); m=np.array([float(np.trace(xop@e).real) for e in BASIS])
 u=(-4*f['eta']*f['kappa']*h).reshape(-1,1); v=m.reshape(-1,1); dA=u@v.T; Ar=A+dA
 dw=Z*math.sqrt(DT); obs=math.sqrt(8*f['eta']*f['kappa']); dy0=obs*mu(s)*DT
 Jnp=jac(lambda q:same_noise(q,f,DT,dw),s); Jnm=jac(lambda q:same_noise(q,f,DT,-dw),s)
 Jrp=jac(lambda q:same_record(q,f,DT,dy0+dw),s); Jrm=jac(lambda q:same_record(q,f,DT,dy0-dw),s)
 Afd=((Jnp+Jnm)/2-np.eye(3))/DT; Arfd=((Jrp+Jrm)/2-np.eye(3))/DT
 i0={'phys':maxabs(Afd-A),'rec':maxabs(Arfd-Ar),'delta':maxabs((Arfd-Afd)-dA),'rank':rank(dA,RANK_TOL)}
 i1=[]
 for z in list(PROBES)+list(np.linalg.eigvals(A)):
  M=z*np.eye(3)-A; lhs=np.linalg.det(z*np.eye(3)-Ar); rhs=np.linalg.det(M)-(v.T@adj3(M)@u)[0,0]
  i1.append(float(abs(lhs-rhs)))
 secs=[secular(A,u,v,z) for z in PROBES]
 r=rank(dA,RANK_TOL); mr=moment_ranks(dA); n=3
 Ap=Q.T@A@Q; up=Q.T@u; vp=Q.T@v; inv=[]
 for z in PROBES:
  a=secular(A,u,v,z); b=secular(Ap,up,vp,z)
  inv.append(math.hypot(a['factor_real']-b['factor_real'],a['factor_imag']-b['factor_imag']))
 quant.append({'id':f['id'],'I0':i0,'I1max':max(i1),'secular':secs,'rank':r,'moment_ranks':list(mr),'bounds':[2*n*r-r*r,r*(2*n-r+1)//2],'I5max':max(inv)})

controls=[]
for c in CONTROLS:
 A,U,V=c['A'],c['U'],c['V']; dA=U@V.T; r=rank(dA,RANK_TOL); n=A.shape[0]
 controls.append({'id':c['id'],'m':U.shape[1],'rank':r,'secular':[secular(A,U,V,z) for z in PROBES],'moment_ranks':list(moment_ranks(dA)),'bounds':[2*n*r-r*r,r*(2*n-r+1)//2]})

I0=max(max(q['I0']['phys'],q['I0']['rec'],q['I0']['delta']) for q in quant)
I1=max(q['I1max'] for q in quant)
allsec=[s for q in quant for s in q['secular']]+[s for c in controls for s in c['secular']]
I2=max(s['residual'] for s in allsec if not s['refuse']); refusals=sum(s['refuse'] for s in allsec)
I3=all(q['rank']<=1 for q in quant) and all(c['rank']<=c['m'] for c in controls)
I4=all(q['moment_ranks'][0]<=q['bounds'][0] and q['moment_ranks'][1]<=q['bounds'][1] for q in quant) and all(c['moment_ranks'][0]<=c['bounds'][0] and c['moment_ranks'][1]<=c['bounds'][1] for c in controls)
I5=max(q['I5max'] for q in quant)
criteria={
 'I0':{'status':'PASS' if all(q['I0']['phys']<=2e-6 and q['I0']['rec']<=2e-6 and q['I0']['delta']<=3e-6 and q['I0']['rank']<=1 for q in quant) else 'FAIL','max_error':I0},
 'I1':{'status':'PASS' if I1<=2e-10 else 'FAIL','max_error':I1},
 'I2':{'status':'PASS' if I2<=2e-10 else 'FAIL','max_error':I2,'refusals':refusals},
 'I3':{'status':'PASS' if I3 else 'FAIL'},
 'I4':{'status':'PASS' if I4 else 'FAIL'},
 'I5':{'status':'PASS' if I5<=2e-11 else 'FAIL','max_error':I5},
 'I6':{'status':'PASS','PHYSICAL_GENERATOR':'FULL_MATRIX_REQUIRED','RECORD_GENERATOR':'FULL_MATRIX_REQUIRED','MOMENT_GENERATOR':'FULL_MOMENT_OPERATOR_REQUIRED','SECULAR_OBJECT':'COMPARATIVE_ONLY'}}
status='PASS' if all(v['status']=='PASS' for v in criteria.values()) else 'FAIL'
out={'audit':'information_rank_secular_bridge_v0.1','status':status,'criteria':criteria,'quantum':quant,'controls':controls,'python':platform.python_version(),'numpy':np.__version__}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':status,'criteria':criteria,'quantum_rank_bounds':[{q['id']:{'rank':q['rank'],'moment_ranks':q['moment_ranks'],'bounds':q['bounds']}} for q in quant],'control_rank_bounds':[{c['id']:{'rank':c['rank'],'moment_ranks':c['moment_ranks'],'bounds':c['bounds']}} for c in controls]},indent=2))
if status!='PASS': raise SystemExit(1)
