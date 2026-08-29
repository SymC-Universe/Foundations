#!/usr/bin/env python3
import json, math, platform
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
RESULTS=ROOT/'results'; RESULTS.mkdir(parents=True,exist_ok=True)
OUT=RESULTS/'active_quotient_scalar_admissibility_audit_v01.json'
REL=1e-11; ABS=1e-13; RES=1e-10; INV=5e-12; POLY=2e-10; DEG=1e-8; REAL=1e-12; COND=1e10; OSC=1e-13

QFIX=[
 {'id':'AQ1','eta':0.66,'gamma':0.24,'kappa':0.14,'omega':0.96,'base':[0.18,-0.23,0.12]},
 {'id':'AQ2','eta':0.74,'gamma':0.39,'kappa':0.18,'omega':1.14,'base':[-0.27,0.15,-0.21]},
 {'id':'AQ3','eta':0.57,'gamma':0.29,'kappa':0.11,'omega':0.79,'base':[0.11,0.32,0.26]},
]
S1=np.array([[1.2,0.25],[-0.15,0.85]],float)
S2=np.array([[0.9,-0.28],[0.19,1.1]],float)
H=np.array([[0.31,-0.22]],float)
S_BAD=np.array([[1.,1.],[1.,1.]],float)


def maxabs(a):
 a=np.asarray(a); return float(np.max(np.abs(a))) if a.size else 0.0

def nullspace(M):
 M=np.asarray(M,float); _,s,vh=np.linalg.svd(M,full_matrices=True)
 smax=float(s[0]) if s.size else 0.0; tol=max(ABS,REL*smax); rank=int(np.sum(s>tol))
 return vh[rank:].T.copy(),rank,tol

def dark_basis(A,V):
 n=A.shape[0]; blocks=[]; Ak=np.eye(n)
 for _ in range(n):
  blocks.append(V.T@Ak); Ak=Ak@A
 O=np.vstack(blocks); D,rank,tol=nullspace(O); return D,O,rank,tol

def complement(D,n):
 if D.shape[1]==0: return np.eye(n)
 C,_,_=nullspace(D.T); return C

def defective(A):
 A=np.asarray(A,complex); vals=np.linalg.eigvals(A)
 if len(vals)!=2: return False
 if abs(vals[0]-vals[1])>DEG: return False
 v=0.5*(vals[0]+vals[1]); M=A-v*np.eye(2); s=np.linalg.svd(M,compute_uv=False); tol=max(1e-12,1e-10*(float(s[0]) if s.size else 0.0)); geom=2-int(np.sum(s>tol))
 return geom<2

def scalar_policy(A):
 A=np.asarray(A)
 if A.shape!=(2,2): return {'status':'REFUSE_QUOTIENT_DIMENSION','chi':None}
 if np.iscomplexobj(A) and maxabs(A.imag)>REAL: return {'status':'REFUSE_NONREAL_QUOTIENT','chi':None}
 Ar=np.asarray(A.real,float); tr=float(np.trace(Ar)); det=float(np.linalg.det(Ar))
 if tr>=0: return {'status':'REFUSE_NOT_ASYMPTOTICALLY_STABLE','chi':None,'trace':tr,'det':det}
 if det<=0: return {'status':'REFUSE_NONPOSITIVE_DETERMINANT','chi':None,'trace':tr,'det':det}
 chi=-tr/(2*math.sqrt(det))
 return {'status':'ADMIT_ACTIVE_SCALAR','chi':float(chi),'trace':tr,'det':det}

def quantum_control(f):
 g,k,w=f['gamma'],f['kappa'],f['omega']; rx,ry,rz=f['base']
 A=np.array([[-g/2-k,0,w],[0,-g/2-k,0],[-w,0,-g]],float)
 h=np.array([-rz*rx,-rz*ry,1-rz*rz],float)
 U=(-4*f['eta']*k*h).reshape(3,1); V=np.array([[0.0],[0.0],[0.5]])
 return A,U,V

def quotient_data(A,U,V):
 A=np.asarray(A,float); U=np.asarray(U,float).reshape(A.shape[0],-1); V=np.asarray(V,float).reshape(A.shape[0],-1)
 Arec=A+U@V.T; D,O,orank,otol=dark_basis(A,V); d=D.shape[1]; q=A.shape[0]-d
 if d==0:
  return {'status':'REFUSE_NONIDENTIFIABLE_DARK_FACTOR','D':D,'O':O,'dark_dim':0,'quot_dim':q,'A':A,'Arec':Arec,'U':U,'V':V,'otol':otol}
 C=complement(D,A.shape[0]); Q=np.column_stack([D,C]); cond=float(np.linalg.cond(Q))
 if (not np.isfinite(cond)) or cond>COND:
  return {'status':'REFUSE_COORDINATE_FAILURE','D':D,'C':C,'dark_dim':d,'quot_dim':q,'A':A,'Arec':Arec,'U':U,'V':V,'otol':otol,'cond':cond}
 At=Q.T@A@Q; Rt=Q.T@Arec@Q; Ad=At[:d,:d]; Aa=At[d:,d:]; Ara=Rt[d:,d:]
 invD=maxabs((np.eye(A.shape[0])-D@D.T)@A@D); annih=maxabs(V.T@D); preserve=maxabs(Arec@D-A@D)
 sep=float(min(abs(x-y) for x in np.linalg.eigvals(Ad) for y in np.linalg.eigvals(Aa))) if d and q else float('inf')
 if q!=2: status='REFUSE_QUOTIENT_DIMENSION'
 elif sep<=DEG: status='REFUSE_DEGENERATE_SECTOR_ATTRIBUTION'
 elif defective(Aa) or defective(Ara): status='REFUSE_DEFECTIVE_ACTIVE_SECTOR'
 else: status='FACTOR_IDENTIFIED'
 return {'status':status,'D':D,'C':C,'Q':Q,'O':O,'dark_dim':d,'quot_dim':q,'A':A,'Arec':Arec,'U':U,'V':V,'Ad':Ad,'Aa':Aa,'Ara':Ara,'otol':otol,'cond':cond,'dark_invariance':invD,'VtD':annih,'dark_preservation':preserve,'cross_sep':sep}

def transformed_quotient(A,D,C,S,Hshear=None):
 if Hshear is None: C2=C@S
 else: C2=D@Hshear+C@S
 T=np.column_stack([D,C2]); cond=float(np.linalg.cond(T))
 if (not np.isfinite(cond)) or cond>COND: return {'status':'REFUSE_COORDINATE_FAILURE','cond':cond,'Aq':None}
 Ti=np.linalg.inv(T); At=Ti@A@T; d=D.shape[1]
 return {'status':'OK','cond':cond,'Aq':At[d:,d:]}

def poly_factor(A,Ad,Aa):
 p=np.poly(A); pd=np.poly(Ad); q,r=np.polydiv(p,pd); qa=np.poly(Aa)
 q=q/q[0]
 return {'coef_resid':max(maxabs(q-qa),maxabs(r)),'trace_resid':abs((-q[1])-np.trace(Aa)),'det_resid':abs(q[2]-np.linalg.det(Aa))}

def eval_quantum(f):
 A,U,V=quantum_control(f); qd=quotient_data(A,U,V)
 if qd['status']!='FACTOR_IDENTIFIED': return {'id':f['id'],'factor_status':qd['status']}
 D,C=qd['D'],qd['C']; recs={}
 for nm,M,Aq in [('phys',A,qd['Aa']),('rec',qd['Arec'],qd['Ara'])]:
  base=scalar_policy(Aq)
  t1=transformed_quotient(M,D,C,S1)
  t2=transformed_quotient(M,D,C,S2,H)
  invs=[]
  for t in (t1,t2):
   if t['status']!='OK': invs.append({'status':t['status'],'cond':t['cond']}); continue
   sp=scalar_policy(t['Aq'])
   invs.append({'status':sp['status'],'cond':t['cond'],'trace_resid':abs(sp.get('trace',np.nan)-base.get('trace',np.nan)),'det_resid':abs(sp.get('det',np.nan)-base.get('det',np.nan)),'chi_resid':abs(sp.get('chi',np.nan)-base.get('chi',np.nan))})
  pf=poly_factor(M,qd['Ad'],Aq)
  recs[nm]={'scalar':base,'invariance':invs,'poly_factor':pf}
 return {'id':f['id'],'parameters':f,'factor_status':qd['status'],'dark_dim':qd['dark_dim'],'quotient_dim':qd['quot_dim'],'VtD':qd['VtD'],'dark_invariance':qd['dark_invariance'],'dark_preservation':qd['dark_preservation'],'cross_sector_separation':qd['cross_sep'],'channels':recs,'full_generator_status':{'phys':'FULL_MATRIX_REQUIRED','rec':'FULL_MATRIX_REQUIRED'},'stochastic_status':'STOCHASTIC_TERM_NOT_COMPRESSED'}

quantum=[eval_quantum(f) for f in QFIX]

osc=[]
for m,o,g in [(1.7,0.9,0.8),(0.6,1.4,2.1),(2.2,0.55,1.3)]:
 A=np.array([[0,1/m],[-m*o*o,-g]],float); sp=scalar_policy(A); exp=g/(2*o); osc.append({'m':m,'Omega':o,'Gamma':g,'status':sp['status'],'chi':sp['chi'],'expected':exp,'error':abs(sp['chi']-exp)})

ref={}
A=np.diag([-0.3,-0.5,-0.7,-0.9]); V=np.column_stack([np.array([0,1,0,0.]),np.array([0,0,1,0.]),np.array([0,0,0,1.])]); U=np.zeros((4,3)); ref['RQ1']=quotient_data(A,U,V)['status']
A=np.zeros((3,3)); A[0,0]=-.4; A[1:,1:]=np.array([[.2,-1],[1,.2]]); V=np.column_stack([np.array([0,1.,0]),np.array([0,0,1.])]); U=np.zeros((3,2)); q=quotient_data(A,U,V); ref['RQ2']=scalar_policy(q['Aa'])['status'] if q['status']=='FACTOR_IDENTIFIED' else q['status']
A=np.diag([-.4,.2,-1.0]); q=quotient_data(A,np.zeros((3,2)),V); ref['RQ3']=scalar_policy(q['Aa'])['status'] if q['status']=='FACTOR_IDENTIFIED' else q['status']
A=np.diag([-.5,-.5,-1.2]); q=quotient_data(A,np.zeros((3,2)),V); ref['RQ4']=q['status']
A=np.zeros((3,3)); A[0,0]=-.4; A[1:,1:]=np.array([[-1,1],[0,-1]],float); q=quotient_data(A,np.zeros((3,2)),V); ref['RQ5']=q['status']
A=np.zeros((3,3)); A[0,0]=-.4; A[1:,1:]=np.array([[-.7,1.1],[-1.1,-.7]]); q=quotient_data(A,np.zeros((3,2)),V); ref['RQ6']=transformed_quotient(A,q['D'],q['C'],S_BAD)['status']
ref['RQ7']=scalar_policy(np.array([[-.5+0j,1j*1e-3],[-1.,-.6]],complex))['status']
A=np.array([[-0.45,0.70,0.10],[-0.60,-0.55,0.40],[-0.20,-0.50,-0.75]],float); V8=np.array([[1.],[0.],[0.]]); U8=np.array([[.12],[-.08],[.15]]); ref['RQ8']=quotient_data(A,U8,V8)['status']

A0_ok=all(q.get('factor_status')=='FACTOR_IDENTIFIED' and q['dark_dim']==1 and q['quotient_dim']==2 and q['VtD']<=1e-11 and q['dark_invariance']<=RES and q['dark_preservation']<=RES for q in quantum)
A1_ok=all(q['channels'][c]['scalar']['status']=='ADMIT_ACTIVE_SCALAR' for q in quantum for c in ('phys','rec'))
A2_ok=all(all(x['status']=='ADMIT_ACTIVE_SCALAR' and x['trace_resid']<=INV and x['det_resid']<=INV and x['chi_resid']<=INV for x in q['channels'][c]['invariance']) for q in quantum for c in ('phys','rec'))
A3_ok=all(max(v for v in q['channels'][c]['poly_factor'].values())<=POLY for q in quantum for c in ('phys','rec'))
A4_ok=max(x['error'] for x in osc)<=OSC
A5_ok=A1_ok and all('chi' in q['channels']['phys']['scalar'] and 'chi' in q['channels']['rec']['scalar'] for q in quantum)
expected={'RQ1':'REFUSE_QUOTIENT_DIMENSION','RQ2':'REFUSE_NOT_ASYMPTOTICALLY_STABLE','RQ3':'REFUSE_NONPOSITIVE_DETERMINANT','RQ4':'REFUSE_DEGENERATE_SECTOR_ATTRIBUTION','RQ5':'REFUSE_DEFECTIVE_ACTIVE_SECTOR','RQ6':'REFUSE_COORDINATE_FAILURE','RQ7':'REFUSE_NONREAL_QUOTIENT','RQ8':'REFUSE_NONIDENTIFIABLE_DARK_FACTOR'}
A6_ok=all(ref[k]==v for k,v in expected.items())
A7_ok=all(q.get('full_generator_status')=={'phys':'FULL_MATRIX_REQUIRED','rec':'FULL_MATRIX_REQUIRED'} and q.get('stochastic_status')=='STOCHASTIC_TERM_NOT_COMPRESSED' for q in quantum)
criteria={
 'A0':{'status':'PASS' if A0_ok else 'FAIL','max_VtD':max(q.get('VtD',1e9) for q in quantum),'max_dark_invariance':max(q.get('dark_invariance',1e9) for q in quantum),'max_dark_preservation':max(q.get('dark_preservation',1e9) for q in quantum)},
 'A1':{'status':'PASS' if A1_ok else 'FAIL'},
 'A2':{'status':'PASS' if A2_ok else 'FAIL','max_trace_residual':max(x['trace_resid'] for q in quantum for c in ('phys','rec') for x in q['channels'][c]['invariance'] if 'trace_resid' in x),'max_det_residual':max(x['det_resid'] for q in quantum for c in ('phys','rec') for x in q['channels'][c]['invariance'] if 'det_resid' in x),'max_chi_residual':max(x['chi_resid'] for q in quantum for c in ('phys','rec') for x in q['channels'][c]['invariance'] if 'chi_resid' in x),'gate':INV},
 'A3':{'status':'PASS' if A3_ok else 'FAIL','max_factor_residual':max(max(v for v in q['channels'][c]['poly_factor'].values()) for q in quantum for c in ('phys','rec')),'gate':POLY},
 'A4':{'status':'PASS' if A4_ok else 'FAIL','max_inheritance_error':max(x['error'] for x in osc),'gate':OSC},
 'A5':{'status':'PASS' if A5_ok else 'FAIL','interpretation':'SEPARATE_CHANNEL_SCALARS_ONLY'},
 'A6':{'status':'PASS' if A6_ok else 'FAIL','observed':ref,'expected':expected},
 'A7':{'status':'PASS' if A7_ok else 'FAIL','full_generator':'FULL_MATRIX_REQUIRED','stochastic':'STOCHASTIC_TERM_NOT_COMPRESSED'},
}
overall='PASS' if all(v['status']=='PASS' for v in criteria.values()) else 'FAIL'
out={'audit':'active_quotient_scalar_admissibility_v0.1','status':overall,'python':platform.python_version(),'numpy':np.__version__,'criteria':criteria,'quantum_controls':quantum,'oscillator_controls':osc,'refusal_controls':ref,'interpretation':'ACTIVE_QUOTIENT_SCALAR_ONLY_NO_LOCALIZATION_CLAIM'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':overall,'criteria':criteria,'chis':[{q['id']:{'phys':q.get('channels',{}).get('phys',{}).get('scalar',{}).get('chi'),'rec':q.get('channels',{}).get('rec',{}).get('scalar',{}).get('chi')}} for q in quantum]},indent=2))
if overall!='PASS': raise SystemExit(1)
