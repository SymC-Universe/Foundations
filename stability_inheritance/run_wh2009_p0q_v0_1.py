#!/usr/bin/env python3
import csv, hashlib, json, math, sys, urllib.request
from pathlib import Path
import numpy as np

URL="https://raw.githubusercontent.com/matheuswhite/narmax/master/res/wienerhammer.csv"
EXPECTED_BLOB="865a402fc495291422133f7473867a82a8aee12e"
LAMBDAS=[0.0,1e-10,1e-8,1e-6,1e-4,1e-2,1.0]
L=8
OUT=Path("stability_inheritance/results/wh2009")
OUT.mkdir(parents=True,exist_ok=True)
raw=OUT/"wienerhammer.csv"
urllib.request.urlretrieve(URL,raw)
raw_bytes=raw.read_bytes()
raw_sha=hashlib.sha256(raw_bytes).hexdigest()
git_blob_sha=hashlib.sha1(f"blob {len(raw_bytes)}".encode("ascii") + b"\x00" + raw_bytes).hexdigest()
if git_blob_sha != EXPECTED_BLOB:
    raise RuntimeError(f"source blob mismatch: expected {EXPECTED_BLOB}, got {git_blob_sha}")

data=np.loadtxt(raw,delimiter=",",dtype=float)
if data.shape[0] < 184000 or data.shape[1] < 3:
    raise RuntimeError(f"unexpected dataset shape {data.shape}")
u=data[:,1].astype(float)
y=data[:,2].astype(float)

train=slice(5200,105200)
fit=slice(5200,85200)
val=slice(85200,105200)
test=slice(105200,184000)

mu_u=float(u[fit].mean()); sd_u=float(u[fit].std(ddof=0))
mu_y=float(y[fit].mean()); sd_y=float(y[fit].std(ddof=0))
if not (sd_u>0 and sd_y>0): raise RuntimeError("nonpositive fit SD")
us=(u-mu_u)/sd_u; ys=(y-mu_y)/sd_y

def feats_at(t, nonlinear=False, y_source=None):
    yy=ys if y_source is None else y_source
    base=[yy[t-k] for k in range(1,L+1)] + [us[t-k] for k in range(0,L+1)]
    x=[1.0]+base
    if nonlinear:
        x += [v*v for v in base] + [v*v*v for v in base]
    return np.asarray(x,float)

def build(start,stop,nonlinear=False):
    idx=np.arange(max(start,L),stop)
    X=np.vstack([feats_at(int(t),nonlinear) for t in idx])
    T=ys[idx].copy()
    return idx,X,T

fit_idx,X1f,Tf=build(fit.start,fit.stop,False)
_,X2f,_=build(fit.start,fit.stop,True)
val_idx,X1v,Tv=build(val.start,val.stop,False)
_,X2v,_=build(val.start,val.stop,True)

def ridge_fit(X,t,lam):
    A=X.T@X
    b=X.T@t
    P=np.eye(X.shape[1]); P[0,0]=0.0
    return np.linalg.solve(A+lam*P,b)

def choose(Xf,Xv):
    rows=[]
    best=None
    for lam in LAMBDAS:
        b=ridge_fit(Xf,Tf,lam)
        pred=Xv@b
        rmse=float(np.sqrt(np.mean((pred-Tv)**2)))
        rows.append({"lambda":lam,"validation_rmse_standardized":rmse})
        if best is None or rmse < best[0]:
            best=(rmse,lam,b)
    return best,rows

b1sel,grid1=choose(X1f,X1v)
b2sel,grid2=choose(X2f,X2v)
beta1=b1sel[2]; beta2=b2sel[2]

test_idx,X1t,Tt=build(test.start,test.stop,False)
_,X2t,_=build(test.start,test.stop,True)
p1=X1t@beta1; p2=X2t@beta2
pp=ys[test_idx-1]

def original_metrics(pred_std, target_std):
    pred=pred_std*sd_y+mu_y
    tgt=target_std*sd_y+mu_y
    rmse=float(np.sqrt(np.mean((pred-tgt)**2)))
    denom=float(np.std(tgt,ddof=0))
    return rmse, rmse/denom if denom>0 else math.nan

pers_rmse,pers_nrmse=original_metrics(pp,Tt)
m1_one,m1_one_n=original_metrics(p1,Tt)
m2_one,m2_one_n=original_metrics(p2,Tt)

def free_run(beta,nonlinear):
    pred=ys.copy()
    start=test.start
    score_start=start+50
    for t in range(score_start,test.stop):
        x=feats_at(t,nonlinear,y_source=pred)
        val=float(x@beta)
        if not np.isfinite(val) or abs(val)>1e9:
            return None,True,score_start
        pred[t]=val
    return pred,False,score_start

fr1,div1,score_start=free_run(beta1,False)
fr2,div2,_=free_run(beta2,True)
if div1:
    m1_free=m1_free_n=math.inf
else:
    m1_free,m1_free_n=original_metrics(fr1[score_start:test.stop],ys[score_start:test.stop])
if div2:
    m2_free=m2_free_n=math.inf
else:
    m2_free,m2_free_n=original_metrics(fr2[score_start:test.stop],ys[score_start:test.stop])

if np.isfinite(m2_one) and np.isfinite(m2_free) and m2_one < m1_one and m2_free < m1_free:
    disp="NONLINEAR_EXTENSION_ADDS_FOR_TASK"
elif m1_one <= m2_one and m1_free <= m2_free:
    disp="LINEAR_REPRESENTATION_ADEQUATE_FOR_TASK"
elif div1 or div2:
    disp="REPRESENTATION_OUT_OF_REGIME"
else:
    disp="MIXED_REPRESENTATION_RESULT"

result={
 "status":"P0-Q_EXTERNAL_MEASURED_ONLY",
 "dataset":"Wiener-Hammerstein SYSID 2009",
 "source_url":URL,
 "source_blob_sha":EXPECTED_BLOB,
 "raw_sha256":raw_sha,
 "verified_git_blob_sha":git_blob_sha,
 "shape":list(data.shape),
 "split":{"train":[5200,105200],"fit":[5200,85200],"validation":[85200,105200],"test":[105200,184000],"free_run_initialization":50},
 "standardization":{"u_mean":mu_u,"u_sd":sd_u,"y_mean":mu_y,"y_sd":sd_y},
 "lambda_grid":LAMBDAS,
 "M1":{"selected_lambda":b1sel[1],"validation":grid1,"one_step_rmse":m1_one,"one_step_nrmse":m1_one_n,"free_run_rmse":m1_free,"free_run_nrmse":m1_free_n,"divergence":div1},
 "M2":{"selected_lambda":b2sel[1],"validation":grid2,"one_step_rmse":m2_one,"one_step_nrmse":m2_one_n,"free_run_rmse":m2_free,"free_run_nrmse":m2_free_n,"divergence":div2},
 "persistence":{"one_step_rmse":pers_rmse,"one_step_nrmse":pers_nrmse},
 "disposition":disp,
 "claim_ceiling":"representation adequacy/refusal only; not SI novelty or P1"
}
(OUT/"result.json").write_text(json.dumps(result,indent=2))
with (OUT/"summary.md").open("w") as f:
    f.write("# WH2009 frozen P0-Q scoring result\n\n")
    f.write(f"Disposition: **{disp}**\n\n")
    f.write(f"Raw SHA256: \`{raw_sha}\`\n\n")
    f.write("| Model | lambda | one-step RMSE | one-step NRMSE | free-run RMSE | free-run NRMSE | diverged |\n|---|---:|---:|---:|---:|---:|---|\n")
    f.write(f"| M1 linear ARX-8 | {b1sel[1]:.3g} | {m1_one:.10g} | {m1_one_n:.10g} | {m1_free:.10g} | {m1_free_n:.10g} | {div1} |\n")
    f.write(f"| M2 polynomial NARX-8 | {b2sel[1]:.3g} | {m2_one:.10g} | {m2_one_n:.10g} | {m2_free:.10g} | {m2_free_n:.10g} | {div2} |\n")
    f.write(f"| Persistence | n/a | {pers_rmse:.10g} | {pers_nrmse:.10g} | n/a | n/a | n/a |\n")
print(json.dumps(result,indent=2))
