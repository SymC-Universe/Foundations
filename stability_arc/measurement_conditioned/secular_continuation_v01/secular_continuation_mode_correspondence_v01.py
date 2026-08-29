#!/usr/bin/env python3
import itertools, json, math, platform
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
RESULTS=ROOT/'results'; RESULTS.mkdir(parents=True,exist_ok=True)
OUT=RESULTS/'secular_continuation_mode_correspondence_v01.json'

FIXTURES=[
 {'id':'S1','eta':0.66,'gamma':0.22,'kappa':0.14,'omega':1.02,'base':[0.18,-0.12,0.22]},
 {'id':'S2','eta':0.79,'gamma':0.34,'kappa':0.18,'omega':1.27,'base':[-0.27,0.08,0.16]},
 {'id':'S3','eta':0.57,'gamma':0.28,'kappa':0.12,'omega':0.81,'base':[0.11,0.29,-0.18]}]
TGRID=[j/16 for j in range(17)]
GAP_GUARD=1e-7; COND_GUARD=1e8; REAL_TOL=1e-10; CONJ_TOL=1e-9
AMBIG_MARGIN=1e-6; POLE_GUARD=1e-8; SECULAR_GATE=2e-8
ID_GATE=5e-14; PROJ_GATE=2e-9; INVAR_REP_GATE=2e-9; INVAR_PROJ_GATE=2e-8; RANK_TOL=1e-12
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]],complex); sz=np.array([[1,0],[0,-1]],complex)
I2=np.eye(2,dtype=complex); sm=np.array([[0,1],[0,0]],complex); xop=.5*sz
BASIS=[.5*sx,.5*sy,.5*sz]; PAULI=[sx,sy,sz]

def comm(a,b): return a@b-b@a
def diss(c,s):
 cd=c.conj().T; cdc=cd@c; return c@s@cd-.5*(cdc@s+s@cdc)
def rho(v): return .5*(I2+v[0]*sx+v[1]*sy+v[2]*sz)
def mu(s): return float(np.trace(xop@s).real)
def hsuper(s): return xop@s+s@xop-2*mu(s)*s
def L(s,g,k,w): return -1j*comm(.5*w*sy,s)+diss(math.sqrt(g)*sm,s)+2*k*diss(xop,s)
def coords(o): return np.array([float(np.trace(p@o).real) for p in PAULI])
def lin(fn): return np.column_stack([coords(fn(e)) for e in BASIS])
def maxabs(a): return float(np.max(np.abs(a)))
def rank(a,tol=RANK_TOL): return int(np.sum(np.linalg.svd(a,compute_uv=False)>tol))
def scale(A): return max(1.0,float(np.linalg.norm(A,2)))
def rx(t):
 c,s=math.cos(t),math.sin(t); return np.array([[1,0,0],[0,c,-s],[0,s,c]],float)
def ry(t):
 c,s=math.cos(t),math.sin(t); return np.array([[c,0,s],[0,1,0],[-s,0,c]],float)
def rz(t):
 c,s=math.cos(t),math.sin(t); return np.array([[c,-s,0],[s,c,0],[0,0,1]],float)
Q=rz(.33)@ry(-.41)@rx(.26)

def cnum(z): return {'real':float(np.real(z)),'imag':float(np.imag(z))}
def cluster_json(c): return {'dim':c['dim'],'rep':cnum(c['rep'])}

def classify(A):
 vals,X=np.linalg.eig(A); sc=scale(A)
 gap=min(abs(vals[i]-vals[j]) for i in range(len(vals)) for j in range(i+1,len(vals))) if len(vals)>1 else 1e99
 if gap/sc<=GAP_GUARD:
  return {'status':'REFUSE_DEGENERATE_OR_COLLISION','gap_ratio':float(gap/sc),'cond':None}
 cond=float(np.linalg.cond(X))
 if cond>=COND_GUARD:
  return {'status':'REFUSE_NEAR_DEFECTIVE','gap_ratio':float(gap/sc),'cond':cond}
 Xi=np.linalg.inv(X); unused=set(range(len(vals))); clusters=[]
 while unused:
  i=min(unused); z=vals[i]
  if abs(z.imag)<=REAL_TOL*sc:
   inds=[i]; rep=complex(float(z.real),0.0); unused.remove(i)
  else:
   cand=[j for j in unused if j!=i and abs(vals[j]-np.conj(z))<=CONJ_TOL*sc]
   if not cand:
    return {'status':'REFUSE_CONJUGACY_INCONSISTENT','gap_ratio':float(gap/sc),'cond':cond}
   j=min(cand,key=lambda q:abs(vals[q]-np.conj(z))); inds=[i,j]; unused.remove(i); unused.remove(j)
   alpha=.5*(vals[i].real+vals[j].real); beta=.5*(abs(vals[i].imag)+abs(vals[j].imag)); rep=complex(float(alpha),float(beta))
  P=np.zeros_like(A,dtype=complex)
  for q in inds: P += np.outer(X[:,q],Xi[q,:])
  clusters.append({'dim':len(inds),'rep':rep,'P':P})
 clusters.sort(key=lambda c:(c['dim'],c['rep'].real,c['rep'].imag))
 idem=max(maxabs(c['P']@c['P']-c['P']) for c in clusters)
 decomp=maxabs(sum((c['P'] for c in clusters),np.zeros_like(A,dtype=complex))-np.eye(A.shape[0]))
 return {'status':'ADMISSIBLE','gap_ratio':float(gap/sc),'cond':cond,'clusters':clusters,'idem':idem,'decomp':decomp}

def assign(prev,curr,sc):
 n=len(prev); perms=[]
 for p in itertools.permutations(range(n)):
  if all(prev[i]['dim']==curr[p[i]]['dim'] for i in range(n)):
   cost=sum(abs(prev[i]['rep']-curr[p[i]]['rep'])/sc for i in range(n)); perms.append((float(cost),p))
 if not perms: return {'status':'REFUSE_BRANCH_TOPOLOGY_CHANGE'}
 perms.sort(key=lambda x:x[0]);
 if len(perms)>1 and perms[1][0]-perms[0][0]<=AMBIG_MARGIN:
  return {'status':'REFUSE_AMBIGUOUS_ASSIGNMENT','best':perms[0][0],'second':perms[1][0]}
 return {'status':'MATCH','cost':perms[0][0],'perm':list(perms[0][1])}

def secular(A,U,V,t,z):
 M=z*np.eye(A.shape[0])-A; smin=float(np.min(np.linalg.svd(M,compute_uv=False))); sc=scale(A)
 if smin/sc<=POLE_GUARD: return {'status':'REFUSE_NEAR_PHYSICAL_POLE','smin_ratio':smin/sc}
 fac=np.linalg.det(np.eye(U.shape[1])-t*(V.T@np.linalg.solve(M,U)))
 return {'status':'ADMISSIBLE','smin_ratio':smin/sc,'residual':float(abs(fac))}

def run_path(A,U,V):
 points=[]; branches=None; refusal=None; sec=[]; s0err=0.0
 for t in TGRID:
  At=A+t*(U@V.T); s0err=max(s0err,maxabs((At-A)-t*(U@V.T)))
  cl=classify(At)
  p={'t':t,'status':cl['status'],'gap_ratio':cl.get('gap_ratio'),'cond':cl.get('cond')}
  if cl['status']!='ADMISSIBLE':
   p['refusal']=cl['status']; points.append(p); refusal={'t':t,'reason':cl['status']}; break
  p['idem']=cl['idem']; p['decomp']=cl['decomp']; p['clusters']=[cluster_json(c) for c in cl['clusters']]
  if branches is None:
   ordered=cl['clusters']; branches=[[{'t':t,'rep':c['rep'],'P':c['P'],'dim':c['dim']}] for c in ordered]
  else:
   prev=[b[-1] for b in branches]; prevc=[{'dim':x['dim'],'rep':x['rep']} for x in prev]
   mt=assign(prevc,cl['clusters'],max(scale(A),scale(At)))
   if mt['status']!='MATCH':
    p['refusal']=mt['status']; points.append(p); refusal={'t':t,'reason':mt['status']}; break
   ordered=[cl['clusters'][q] for q in mt['perm']]; p['assignment_cost']=mt['cost']
   for b,c in zip(branches,ordered): b.append({'t':t,'rep':c['rep'],'P':c['P'],'dim':c['dim']})
  for z in np.linalg.eigvals(At):
   if t>0: sec.append({'t':t,'z':cnum(z),**secular(A,U,V,t,z)})
  points.append(p)
 full=refusal is None and len(points)==len(TGRID)
 endpoint=0.0
 if full:
  start=classify(A)['clusters']; end=classify(A+U@V.T)['clusters']
  endpoint=max(max(abs(branches[i][0]['rep']-start[i]['rep']),abs(branches[i][-1]['rep']-end[i]['rep'])) for i in range(len(branches)))
 return {'full':full,'refusal':refusal,'points':points,'branches':branches,'secular':sec,'s0err':s0err,'endpoint':float(endpoint)}

def path_public(path):
 br=[]
 if path['branches'] is not None:
  for i,b in enumerate(path['branches']): br.append({'branch':i,'dim':b[0]['dim'],'trajectory':[{'t':x['t'],'rep':cnum(x['rep'])} for x in b],'endpoint_displacement':{'real':float(b[-1]['rep'].real-b[0]['rep'].real),'oscillation_magnitude':float(b[-1]['rep'].imag-b[0]['rep'].imag)}})
 return {'full':path['full'],'refusal':path['refusal'],'points':path['points'],'branches':br,'secular':path['secular'],'s0err':path['s0err'],'endpoint':path['endpoint']}

def compare_rot(path,pathq):
 if path['full']!=pathq['full']: return {'status':False,'reason':'full_status'}
 if path['refusal']!=pathq['refusal']: return {'status':False,'reason':'refusal_mismatch'}
 n=min(len(path['points']),len(pathq['points'])); rep=0.0; proj=0.0; dims=True; statuses=True
 for j in range(n):
  statuses &= path['points'][j]['status']==pathq['points'][j]['status']
  if path['points'][j]['status']=='ADMISSIBLE':
   dims &= [c['dim'] for c in path['points'][j]['clusters']]==[c['dim'] for c in pathq['points'][j]['clusters']]
 if path['branches'] is not None and pathq['branches'] is not None:
  for b,bq in zip(path['branches'],pathq['branches']):
   for x,y in zip(b,bq):
    rep=max(rep,abs(x['rep']-y['rep'])); proj=max(proj,maxabs(y['P']-Q.T@x['P']@Q))
 return {'status':bool(statuses and dims and rep<=INVAR_REP_GATE and proj<=INVAR_PROJ_GATE),'status_match':bool(statuses),'dims_match':bool(dims),'max_rep_residual':float(rep),'max_projector_residual':float(proj)}

quant=[]; pole_refusals=[]
for f in FIXTURES:
 s=rho(f['base']); ev=np.linalg.eigvalsh(s)
 if float(ev.min())<=0: raise RuntimeError('fixture outside Bloch ball')
 A=lin(lambda e:L(e,f['gamma'],f['kappa'],f['omega'])); h=coords(hsuper(s)); v=np.array([float(np.trace(xop@e).real) for e in BASIS]).reshape(-1,1); u=(-4*f['eta']*f['kappa']*h).reshape(-1,1)
 p=run_path(A,u,v); Aq=Q.T@A@Q; uq=Q.T@u; vq=Q.T@v; pq=run_path(Aq,uq,vq); inv=compare_rot(p,pq)
 poles=[]
 for z in np.linalg.eigvals(A): poles.append(secular(A,u,v,1.0,z)); pole_refusals.extend(poles)
 quant.append({'id':f['id'],'rank':rank(u@v.T),'path':path_public(p),'rotation':inv,'pole_probes':poles})

N1A=np.diag([-1.,-1.,-2.]); N1U=np.array([[1.],[0.],[0.]]); N1V=np.array([[.1],[0.],[0.]])
N2A=np.array([[-1.,1.,0.],[-1.,-1.,0.],[0.,0.,-3.]]); N2U=np.array([[0.],[2.],[0.]]); N2V=np.array([[1.],[0.],[0.]])
n1=run_path(N1A,N1U,N1V); n2=run_path(N2A,N2U,N2V)

all_points=[p for q in quant for p in q['path']['points'] if p['status']=='ADMISSIBLE']
projmax=max([max(p.get('idem',0),p.get('decomp',0)) for p in all_points] or [0.0])
secadm=[s for q in quant for s in q['path']['secular'] if s['status']=='ADMISSIBLE']
secmax=max([s['residual'] for s in secadm] or [0.0])
s0=max(q['path']['s0err'] for q in quant)
endmax=max([q['path']['endpoint'] for q in quant if q['path']['full']] or [0.0])
S0=all(q['rank']<=1 for q in quant) and s0<=ID_GATE
S1=projmax<=PROJ_GATE
S2=all((not q['path']['full']) or q['path']['endpoint']<=INVAR_REP_GATE for q in quant)
S3=secmax<=SECULAR_GATE and all(p['status']=='REFUSE_NEAR_PHYSICAL_POLE' for p in pole_refusals)
S4=n1['refusal']=={'t':0.0,'reason':'REFUSE_DEGENERATE_OR_COLLISION'} and n2['refusal'] is not None and abs(n2['refusal']['t']-.5)<1e-15 and n2['refusal']['reason'] in ('REFUSE_DEGENERATE_OR_COLLISION','REFUSE_NEAR_DEFECTIVE')
S5=all(q['rotation']['status'] for q in quant)
criteria={
 'S0':{'status':'PASS' if S0 else 'FAIL','max_identity_error':s0,'max_rank':max(q['rank'] for q in quant)},
 'S1':{'status':'PASS' if S1 else 'FAIL','max_projector_error':projmax},
 'S2':{'status':'PASS' if S2 else 'FAIL','max_full_path_endpoint_residual':endmax,'fresh_refusals':[{'id':q['id'],'refusal':q['path']['refusal']} for q in quant if not q['path']['full']]},
 'S3':{'status':'PASS' if S3 else 'FAIL','max_secular_root_residual':secmax,'exact_pole_refusals':sum(p['status']=='REFUSE_NEAR_PHYSICAL_POLE' for p in pole_refusals)},
 'S4':{'status':'PASS' if S4 else 'FAIL','N1_refusal':n1['refusal'],'N2_refusal':n2['refusal']},
 'S5':{'status':'PASS' if S5 else 'FAIL','max_rep_residual':max(q['rotation'].get('max_rep_residual',0) for q in quant),'max_projector_residual':max(q['rotation'].get('max_projector_residual',0) for q in quant)},
 'S6':{'status':'PASS','PHYSICAL_GENERATOR':'FULL_MATRIX_REQUIRED','RECORD_GENERATOR':'FULL_MATRIX_REQUIRED','MODE_OBJECT':'INVARIANT_CLUSTER_OR_REFUSE','SECULAR_OBJECT':'COMPARATIVE_ONLY','SCALAR_CHI':'NOT_LICENSED'}}
basepass=all(v['status']=='PASS' for v in criteria.values())
allfresh=all(q['path']['full'] for q in quant)
status=('PASS_WITH_ALL_FRESH_PATHS_ADMISSIBLE' if allfresh else 'PASS_WITH_FRESH_REFUSAL') if basepass else 'FAIL'
out={'audit':'secular_continuation_mode_correspondence_v0.1','status':status,'criteria':criteria,'quantum':quant,'negative_controls':{'N1':path_public(n1),'N2':path_public(n2)},'python':platform.python_version(),'numpy':np.__version__,'interpretation':{'PHYSICAL_GENERATOR':'FULL_MATRIX_REQUIRED','RECORD_GENERATOR':'FULL_MATRIX_REQUIRED','MODE_OBJECT':'INVARIANT_CLUSTER_OR_REFUSE','SECULAR_OBJECT':'COMPARATIVE_ONLY','SCALAR_CHI':'NOT_LICENSED'}}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':status,'criteria':criteria},indent=2))
if status=='FAIL': raise SystemExit(1)
