#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.preprocessing import StandardScaler

T = ["Lya_z0.loglikelihood","QSO_z0.loglikelihood","ELG_z1.loglikelihood",
     "LRG_z2.loglikelihood","LRG_z1.loglikelihood","LRG_z0.loglikelihood",
     "BGS_z0.loglikelihood"]
KEEP=["weight"]+T

def header(path):
    with open(path,"r",encoding="utf-8",errors="replace") as f:
        line=f.readline()
    if not line.startswith("#"):
        raise RuntimeError(f"Missing Cobaya header: {path}")
    return line[1:].strip().split()

def load_chain(path,model,chain_id):
    names=header(path)
    missing=[c for c in KEEP if c not in names]
    if missing:
        raise RuntimeError(f"{path}: missing {missing}")
    df=pd.read_csv(path,sep=r"\s+",comment="#",names=names,usecols=KEEP,
                   dtype={c:"float64" for c in KEEP},engine="c")
    df["model"]=model; df["chain_id"]=int(chain_id)
    return df

def load_family(root,model):
    return pd.concat([load_chain(Path(root)/f"chain.{j}.txt",model,j) for j in range(1,5)],ignore_index=True)

def balanced_weights(y,w):
    out=np.zeros_like(w,float)
    for cls in (0,1):
        m=y==cls; out[m]=0.5*w[m]/w[m].sum()
    return out

def fit_residualizer(train):
    y=(train.model=="mg").to_numpy(int)
    w=balanced_weights(y,train.weight.to_numpy(float))
    s=train[T].sum(axis=1).to_numpy(float)
    X=np.column_stack([np.ones(len(train)),s])
    sw=np.sqrt(w)
    Xw=X*sw[:,None]
    coefs={}
    for col in T:
        yy=train[col].to_numpy(float)*sw
        beta=np.linalg.lstsq(Xw,yy,rcond=None)[0]
        coefs[col]=beta.tolist()
    return coefs

def make_features(df,kind,coefs=None,exclude=None,single=None):
    arr=df[T].to_numpy(float)
    s=arr.sum(axis=1)
    if kind=="S":
        return s[:,None]
    if kind=="T":
        return arr
    if kind=="single":
        return df[[single]].to_numpy(float)
    if kind=="loo":
        cols=[c for c in T if c!=exclude]
        return df[cols].to_numpy(float)
    if kind in ("R","SR"):
        if coefs is None:
            raise RuntimeError("residual coefficients required")
        residual=np.empty_like(arr)
        for j,col in enumerate(T):
            a,b=coefs[col]
            residual[:,j]=arr[:,j]-(a+b*s)
        if kind=="R":
            return residual
        return np.column_stack([s,residual])
    raise KeyError(kind)

def eval_model(train,test,kind,coefs=None,exclude=None,single=None):
    Xtr=make_features(train,kind,coefs,exclude,single)
    Xte=make_features(test,kind,coefs,exclude,single)
    ytr=(train.model=="mg").to_numpy(int); yte=(test.model=="mg").to_numpy(int)
    wtr=balanced_weights(ytr,train.weight.to_numpy(float))
    wte=balanced_weights(yte,test.weight.to_numpy(float))
    sc=StandardScaler().fit(Xtr,sample_weight=wtr)
    Xtr=sc.transform(Xtr); Xte=sc.transform(Xte)
    clf=LogisticRegression(C=np.inf,solver="lbfgs",max_iter=300,tol=1e-8)
    clf.fit(Xtr,ytr,sample_weight=wtr)
    p=clf.predict_proba(Xte)[:,1]
    return {"log_loss":float(log_loss(yte,p,sample_weight=wte,labels=[0,1])),
            "auc":float(roc_auc_score(yte,p,sample_weight=wte))}

def aggregate(rows):
    return {"mean_log_loss":float(np.mean([r["log_loss"] for r in rows])),
            "mean_auc":float(np.mean([r["auc"] for r in rows])),
            "folds":rows}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--baseline",required=True); ap.add_argument("--mg",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    base=load_family(args.baseline,"baseline"); mg=load_family(args.mg,"mg")
    all_df=pd.concat([base,mg],ignore_index=True)
    store={"S":[],"T":[],"R":[],"SR":[]}
    for col in T:
        store[f"single::{col}"]=[]; store[f"loo::{col}"]=[]
    residual_coefs={}
    for fold in range(1,5):
        train=all_df[all_df.chain_id!=fold]
        test=all_df[all_df.chain_id==fold]
        coefs=fit_residualizer(train)
        residual_coefs[str(fold)]=coefs
        for kind in ("S","T","R","SR"):
            m=eval_model(train,test,kind,coefs=coefs); m["fold"]=fold; store[kind].append(m)
        for col in T:
            m=eval_model(train,test,"single",single=col); m["fold"]=fold; store[f"single::{col}"].append(m)
            m=eval_model(train,test,"loo",exclude=col); m["fold"]=fold; store[f"loo::{col}"].append(m)
    cv={k:aggregate(v) for k,v in store.items()}
    scalar_beats=sum(1 for s,t in zip(cv["S"]["folds"],cv["T"]["folds"]) if s["log_loss"]<=t["log_loss"])
    vector_beats=4-scalar_beats
    r_beats_intercept=sum(1 for r in cv["R"]["folds"] if r["log_loss"]<math.log(2) and r["auc"]>0.5)
    single_matches=[col for col in T if cv[f"single::{col}"]["mean_log_loss"]<=cv["T"]["mean_log_loss"]]
    loo_erases={}
    for col in T:
        count=sum(1 for loo,s,t in zip(cv[f"loo::{col}"]["folds"],cv["S"]["folds"],cv["T"]["folds"])
                  if t["log_loss"]<s["log_loss"] and loo["log_loss"]>=s["log_loss"])
        loo_erases[col]=count
    t_pooled_better=cv["T"]["mean_log_loss"]<cv["S"]["mean_log_loss"]
    t_robust=t_pooled_better and vector_beats>=3
    r_robust=r_beats_intercept>=3
    dependent=bool(single_matches) or any(v>=3 for v in loo_erases.values())
    if cv["S"]["mean_log_loss"]<=cv["T"]["mean_log_loss"] and scalar_beats>=3:
        disposition="TRACER_SIGNAL_SCALAR_COMPRESSIBLE"
    elif t_robust and dependent:
        disposition="TRACER_VECTOR_SINGLE_TRACER_DEPENDENT"
    elif t_robust and r_robust and not dependent:
        disposition="TRACER_VECTOR_ADDS_OVER_SCALAR_FIT"
    elif t_robust and not r_robust:
        disposition="TRACER_VECTOR_DISTRIBUTED_BUT_WEAK"
    else:
        disposition="REPRESENTATION_INDETERMINATE"
    result={
      "protocol":"DESI_TRACER_CONGLOMERATION_QUALIFICATION_v0.1",
      "disposition":disposition,
      "cv":cv,
      "diagnostics":{
        "T_beats_S_fold_count":vector_beats,
        "S_matches_or_beats_T_fold_count":scalar_beats,
        "R_beats_balanced_intercept_fold_count":r_beats_intercept,
        "single_tracer_matches_or_beats_T":single_matches,
        "leave_one_tracer_out_erases_T_over_S_fold_counts":loo_erases,
        "SR_minus_T_mean_log_loss":float(cv["SR"]["mean_log_loss"]-cv["T"]["mean_log_loss"])
      },
      "residual_coefficients_by_fold":residual_coefs,
      "rows":{"baseline":int(len(base)),"mg":int(len(mg))}
    }
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2))
    compact={
      "disposition":disposition,
      "primary":{k:{"log_loss":cv[k]["mean_log_loss"],"auc":cv[k]["mean_auc"]} for k in ("S","T","R","SR")},
      "diagnostics":result["diagnostics"],
      "single":{col:{"log_loss":cv[f"single::{col}"]["mean_log_loss"],"auc":cv[f"single::{col}"]["mean_auc"]} for col in T},
      "leave_one_out":{col:{"log_loss":cv[f"loo::{col}"]["mean_log_loss"],"auc":cv[f"loo::{col}"]["mean_auc"]} for col in T}
    }
    print(json.dumps(compact,indent=2))

if __name__=="__main__":
    main()
