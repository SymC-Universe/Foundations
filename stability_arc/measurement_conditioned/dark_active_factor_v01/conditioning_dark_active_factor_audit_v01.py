#!/usr/bin/env python3
import json, math, platform
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
RESULTS=ROOT/'results'; RESULTS.mkdir(parents=True,exist_ok=True)
OUT=RESULTS/'conditioning_dark_active_factor_audit_v01.json'
REL=1e-11; ABS=1e-13; RES=1e-10; POLY=2e-9; DEG=1e-8; DEFREL=1e-10; DEFABS=1e-12

QFIX=[
 {'id':'QF1','eta':0.71,'gamma':0.27,'kappa':0.16,'omega':0.88,'base':[0.14,0.26,-0.19]},
 {'id':'QF2','eta':0.63,'gamma':0.35,'kappa':0.12,'omega':1.19,'base':[-0.22,0.17,0.31]},
 {'id':'QF3','eta':0.82,'gamma':0.21,'kappa':0.24,'omega':0.67,'base':[0.29,-0.13,0.08]},]

def maxabs(a):
 a=np.asarray(a); return float(np.max(np.abs(a))) if a.size else 0.0

def nullspace(M,rel=REL,absfloor=ABS):
 M=np.asarray(M,float); _,s,vh=np.linalg.svd(M,full_matrices=True)
 smax=float(s[0]) if s.size else 0.0; tol=max(absfloor,rel*smax); rank=int(np.sum(s>tol))
 return vh[rank:].T.copy(),rank,tol

def rank_num(M,rel=REL,absfloor=ABS):
 s=np.linalg.svd(np.asarray(M,float),compute_uv=False); smax=float(s[0]) if s.size else 0.0
 tol=max(absfloor,rel*smax); return int(np.sum(s>tol)),tol

def dark_basis(A,V):
 n=A.shape[0]; blocks=[]; Ak=np.eye(n)
 for _ in range(n):
  blocks.append(V.T@Ak); Ak=Ak@A
 O=np.vstack(blocks); D,_,tol=nullspace(O); return D,O,tol

def complement(D,n):
 if D.shape[1]==0: return np.eye(n)
 C,_,_=nullspace(D.T); return C

def as_cols(M,n):
 M=np.asarray(M,float)
 return M.reshape(n,1) if M.ndim==1 else M

def defective(A):
 A=np.asarray(A,float)
 if A.size==0: return False,[]
 vals=np.linalg.eigvals(A); used=np.zeros(len(vals),bool); detail=[]; bad=False
 for i,v in enumerate(vals):
  if used[i]: continue
  idx=[j for j,w in enumerate(vals) if (not used[j]) and abs(w-v)<=DEG]
  for j in idx: used[j]=True
  alg=len(idx); M=A-v*np.eye(A.shape[0]); s=np.linalg.svd(M,compute_uv=False)
  smax=float(s[0]) if s.size else 0.0; tol=max(DEFABS,DEFREL*smax); geom=A.shape[0]-int(np.sum(s>tol))
  detail.append({'real':float(v.real),'imag':float(v.imag),'algebraic':alg,'geometric':geom})
  if geom<alg: bad=True
 return bad,detail

def rot_x(t):
 c,s=math.cos(t),math.sin(t); return np.array([[1,0,0],[0,c,-s],[0,s,c]],float)
def rot_y(t):
 c,s=math.cos(t),math.sin(t); return np.array([[c,0,s],[0,1,0],[-s,0,c]],float)
def rot_z(t):
 c,s=math.cos(t),math.sin(t); return np.array([[c,-s,0],[s,c,0],[0,0,1]],float)
Q0=rot_z(0.31)@rot_y(-0.47)@rot_x(0.22)

def quantum_control(f):
 g,k,w=f['gamma'],f['kappa'],f['omega']; rx,ry,rz=f['base']
 A=np.array([[-g/2-k,0,w],[0,-g/2-k,0],[-w,0,-g]],float)
 h=np.array([-rz*rx,-rz*ry,1-rz*rz],float)
 U=(-4*f['eta']*k*h).reshape(3,1); V=np.array([[0.0],[0.0],[0.5]])
 return A,U,V

def evaluate(cid,A,U,V):
 A=np.asarray(A,float); n=A.shape[0]; U=as_cols(U,n); V=as_cols(V,n); m=V.shape[1]
 Arec=A+U@V.T; D,O,otol=dark_basis(A,V); d=D.shape[1]; C=complement(D,n); Q=np.column_stack([D,C])
 N0,_,_=nullspace(V.T); n0=N0.shape[1]
 invN=maxabs((np.eye(n)-N0@N0.T)@A@N0) if n0 else 0.0
 full_kernel_status='ADMIT_FULL_KERNEL_FACTOR' if invN<=RES else 'REFUSE_FULL_KERNEL_FACTOR'
 annih=maxabs((Arec-A)@D) if d else 0.0
 invD=maxabs((np.eye(n)-D@D.T)@A@D) if d else 0.0
 vdark=maxabs(V.T@D) if d else 0.0
 if d:
  At=Q.T@A@Q; Rt=Q.T@Arec@Q; Ad=At[:d,:d]; Aa=At[d:,d:]; Ard=Rt[:d,:d]; Ara=Rt[d:,d:]
  lower=max(maxabs(At[d:,:d]),maxabs(Rt[d:,:d])); darkeq=maxabs(Ad-Ard)
  pA=np.poly(A); pR=np.poly(Arec); pd=np.poly(Ad); pa=np.poly(Aa); pra=np.poly(Ara)
  polyA=maxabs(pA-np.convolve(pd,pa)); polyR=maxabs(pR-np.convolve(pd,pra))
 else:
  Ad=np.empty((0,0)); Aa=A.copy(); Ara=Arec.copy(); pd=np.array([1.0]); lower=darkeq=polyA=polyR=0.0
 Ua=C.T@U; Va=C.T@V; bridge=maxabs((Ara-Aa)-Ua@Va.T); qrank,qtol=rank_num(Ara-Aa)
 preserve=maxabs(Arec@D-A@D) if d else 0.0
 defect,defdetail=defective(Aa)
 mode_status='NO_NONTRIVIAL_DARK_FACTOR' if d==0 else 'IDENTIFIABLE_DARK_FACTOR'
 overlap=None
 if d and Aa.size:
  de=np.linalg.eigvals(Ad); ae=np.linalg.eigvals(Aa); overlap=float(min(abs(x-y) for x in de for y in ae))
  if overlap<=DEG: mode_status='REFUSE_DEGENERATE_SECTOR_ATTRIBUTION'
  elif defect: mode_status='REFUSE_DEFECTIVE_ACTIVE_SECTOR'
  elif d==1: mode_status='IDENTIFIABLE_DARK_MODE'
 elif defect:
  mode_status='REFUSE_DEFECTIVE_ACTIVE_SECTOR'
 return {'id':cid,'n':n,'m':m,'dark_dim':d,'instantaneous_null_dim':n0,'observability_tol':otol,
  'full_kernel_invariance_residual':invN,'full_kernel_status':full_kernel_status,
  'dark_annihilation_residual':annih,'dark_invariance_residual':invD,'Vt_dark_residual':vdark,
  'lower_left_block_residual':lower,'dark_block_agreement_residual':darkeq,
  'physical_factor_poly_residual':polyA,'record_factor_poly_residual':polyR,
  'active_bridge_residual':bridge,'active_update_rank':qrank,'active_update_rank_tol':qtol,
  'dark_preservation_residual':preserve,'cross_sector_min_separation':overlap,
  'active_defective':defect,'defectivity_detail':defdetail,'mode_status':mode_status,
  '_D':D,'_Ad':Ad,'_pd':pd,'_A':A,'_Arec':Arec,'_U':U,'_V':V}

controls=[]; quantum=[]
for f in QFIX:
 A,U,V=quantum_control(f); e=evaluate(f['id'],A,U,V); e['parameters']=f; quantum.append(e); controls.append(e)
A=np.zeros((4,4)); A[:2,:2]=np.diag([-0.4,-0.9]); A[2:,2:]=np.array([[-0.7,1.2],[-1.2,-0.7]])
V=np.column_stack([np.array([0,0,1,0.]),np.array([0,0,0,1.])]); U=np.column_stack([np.array([.2,-.1,.3,.4]),np.array([-.15,.25,-.2,.35])]); controls.append(evaluate('S1',A,U,V))
A=np.array([[-.4,0,1.0],[0,-.6,0],[-1.0,0,-.8]]); controls.append(evaluate('S2',A,np.array([.3,-.2,.25]),np.array([0,0,1.])))
A=np.array([[-.5,1.0],[-1.0,-.5]]); controls.append(evaluate('S3',A,np.array([.2,.3]),np.array([1.,0.])))
A=np.diag([-.5,-.8,-.5]); controls.append(evaluate('R1',A,np.array([.2,-.1,.3]),np.array([0,0,1.])))
A=np.zeros((3,3)); A[0,0]=-.4; A[1:,1:]=np.array([[-1,1],[0,-1]],float); V=np.column_stack([np.array([0,1.,0]),np.array([0,0,1.])]); U=np.column_stack([np.array([.1,.2,-.1]),np.array([-.2,.15,.25])]); controls.append(evaluate('R2',A,U,V))

# Coordinate covariance on fresh quantum controls, with dark space reconstructed from rotated inputs.
coord=[]
for e in quantum:
 A,U,V=e['_A'],e['_U'],e['_V']; Ap=Q0.T@A@Q0; Up=Q0.T@U; Vp=Q0.T@V
 er=evaluate(e['id']+'_rot',Ap,Up,Vp); P=e['_D']@e['_D'].T; Pr=er['_D']@er['_D'].T; Pback=Q0@Pr@Q0.T
 proj=maxabs(P-Pback); poly=maxabs(np.asarray(e['_pd'])-np.asarray(er['_pd'])) if len(e['_pd'])==len(er['_pd']) else float('inf')
 coord.append({'id':e['id'],'dark_dim_original':e['dark_dim'],'dark_dim_rotated':er['dark_dim'],'projector_residual':proj,'dark_poly_residual':poly})

pub=[]
for e in controls:
 pub.append({k:v for k,v in e.items() if not k.startswith('_')})

f0=max(max(e['Vt_dark_residual'],e['dark_invariance_residual'],e['dark_annihilation_residual']) for e in controls)
f1_ok=next(e for e in controls if e['id']=='S1')['full_kernel_status']=='ADMIT_FULL_KERNEL_FACTOR' and next(e for e in controls if e['id']=='S2')['full_kernel_status']=='REFUSE_FULL_KERNEL_FACTOR'
f2=max(max(e['lower_left_block_residual'],e['dark_block_agreement_residual'],e['physical_factor_poly_residual']/20,e['record_factor_poly_residual']/20) for e in controls)
f2_ok=all(e['lower_left_block_residual']<=RES and e['dark_block_agreement_residual']<=RES and e['physical_factor_poly_residual']<=POLY and e['record_factor_poly_residual']<=POLY for e in controls)
f3_ok=all(e['active_bridge_residual']<=RES and e['active_update_rank']<=e['m'] for e in controls)
f4_ok=all(e['physical_factor_poly_residual']<=POLY and e['record_factor_poly_residual']<=POLY for e in controls)
f5_ok=all(e['dark_preservation_residual']<=RES for e in controls)
r1=next(e for e in controls if e['id']=='R1'); r2=next(e for e in controls if e['id']=='R2')
f6_ok=r1['mode_status']=='REFUSE_DEGENERATE_SECTOR_ATTRIBUTION' and r2['mode_status']=='REFUSE_DEFECTIVE_ACTIVE_SECTOR'
f7_ok=all(c['dark_dim_original']==c['dark_dim_rotated'] and c['projector_residual']<=POLY and c['dark_poly_residual']<=POLY for c in coord)
criteria={
 'F0':{'status':'PASS' if f0<=RES else 'FAIL','max_residual':f0,'gate':RES},
 'F1':{'status':'PASS' if f1_ok else 'FAIL','S1':next(e for e in pub if e['id']=='S1')['full_kernel_status'],'S2':next(e for e in pub if e['id']=='S2')['full_kernel_status']},
 'F2':{'status':'PASS' if f2_ok else 'FAIL','poly_gate':POLY,'block_gate':RES,'max_physical_poly':max(e['physical_factor_poly_residual'] for e in controls),'max_record_poly':max(e['record_factor_poly_residual'] for e in controls)},
 'F3':{'status':'PASS' if f3_ok else 'FAIL','max_bridge_residual':max(e['active_bridge_residual'] for e in controls),'gate':RES},
 'F4':{'status':'PASS' if f4_ok else 'FAIL','interpretation':'ALL_CONDITIONING_INDUCED_CHARACTERISTIC_CHANGE_ACCOUNTED_FOR_BY_ACTIVE_QUOTIENT'},
 'F5':{'status':'PASS' if f5_ok else 'FAIL','max_preservation_residual':max(e['dark_preservation_residual'] for e in controls),'gate':RES},
 'F6':{'status':'PASS' if f6_ok else 'FAIL','R1':r1['mode_status'],'R2':r2['mode_status']},
 'F7':{'status':'PASS' if f7_ok else 'FAIL','max_projector_residual':max(c['projector_residual'] for c in coord),'max_dark_poly_residual':max(c['dark_poly_residual'] for c in coord),'gate':POLY}}
overall='PASS' if all(v['status']=='PASS' for v in criteria.values()) else 'FAIL'
out={'audit':'conditioning_dark_active_factor_v0.1','status':overall,'python':platform.python_version(),'numpy':np.__version__,'criteria':criteria,'controls':pub,'coordinate_covariance':coord,'interpretation':'COMPARATIVE_DARK_ACTIVE_FACTORIZATION_ONLY'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':overall,'criteria':criteria},indent=2))
if overall!='PASS': raise SystemExit(1)
