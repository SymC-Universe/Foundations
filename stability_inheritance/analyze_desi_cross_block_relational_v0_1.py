#!/usr/bin/env python3
from pathlib import Path
import argparse, json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.preprocessing import StandardScaler

BG=["omegam","H0","rdrag","sigma8","s8h5","s8omegamp5","s8omegamp25"]
T=["Lya_z0.loglikelihood","QSO_z0.loglikelihood","ELG_z1.loglikelihood",
   "LRG_z2.loglikelihood","LRG_z1.loglikelihood","LRG_z0.loglikelihood",
   "BGS_z0.loglikelihood"]
KEEP=["weight"]+BG+T

def header(path):
    with open(path,"r",encoding="utf-8",errors="replace") as f:
        line=f.readline()
    if not line.startswith("#"):
        raise RuntimeError(f"Missing Cobaya header: {path}")
    return line[1:].strip().split()

def load_chain(path,model,chain_id):
    names=header(path)
    miss=[c for c in KEEP if c not in names]
    if miss: raise RuntimeError(f"{path}: missing {miss}")
    df=pd.read_csv(path,sep=r"\s+",comment="#",names=names,usecols=KEEP,
                   dtype={c:"float64" for c in KEEP},engine="c")
    df["model"]=model; df["chain_id"]=int(chain_id)
    return df

def load_family(root,model):
    return pd.concat([load_chain(Path(root)/f"chain.{j}.txt",model,j) for j in range(1,5)],ignore_index=True)

def balanced_weights(df):
    y=(df.model=="mg").to_numpy(int); w=df.weight.to_numpy(float)
    out=np.zeros_like(w,float)
    for cls in (0,1):
        m=y==cls; out[m]=0.5*w[m]/w[m].sum()
    return out

def fit_residualizer(train):
    w=balanced_weights(train)
    t=train[T].to_numpy(float); s=t.sum(axis=1)
    X=np.column_stack([np.ones(len(train)),s]); sw=np.sqrt(w)
    Xw=X*sw[:,None]
    betas=[]
    for j in range(len(T)):
        betas.append(np.linalg.lstsq(Xw,t[:,j]*sw,rcond=None)[0])
    return np.asarray(betas)

def residuals(df,betas):
    t=df[T].to_numpy(float); s=t.sum(axis=1)
    pred=betas[:,0][None,:]+s[:,None]*betas[:,1][None,:]
    return s,t-pred

def fit_weighted_scaler(X,w):
    return StandardScaler().fit(X,sample_weight=w)

def shift_within_class_chain(df,R):
    out=np.empty_like(R)
    model=df.model.to_numpy(); chain=df.chain_id.to_numpy()
    for m in ("baseline","mg"):
        for c in sorted(np.unique(chain)):
            idx=np.flatnonzero((model==m)&(chain==c))
            if len(idx)==0: continue
            shift=max(1,len(idx)//3)
            out[idx]=np.roll(R[idx],shift=shift,axis=0)
    return out

def construct(train,test):
    betas=fit_residualizer(train)
    strn,Rtr=residuals(train,betas); ste,Rte=residuals(test,betas)
    bgtr=train[BG].to_numpy(float); bgte=test[BG].to_numpy(float)
    wtr=balanced_weights(train)
    sbg=fit_weighted_scaler(bgtr,wtr); sr=fit_weighted_scaler(Rtr,wtr)
    bgtrz=sbg.transform(bgtr); bgtez=sbg.transform(bgte)
    Rtrz=sr.transform(Rtr); Rtez=sr.transform(Rte)

    A_tr=np.column_stack([bgtr,strn,Rtr]); A_te=np.column_stack([bgte,ste,Rte])
    I_tr=np.einsum("ni,nj->nij",bgtrz,Rtrz).reshape(len(train),-1)
    I_te=np.einsum("ni,nj->nij",bgtez,Rtez).reshape(len(test),-1)

    Rtr_shift=shift_within_class_chain(train,Rtrz)
    Rte_shift=shift_within_class_chain(test,Rtez)
    Ish_tr=np.einsum("ni,nj->nij",bgtrz,Rtr_shift).reshape(len(train),-1)
    Ish_te=np.einsum("ni,nj->nij",bgtez,Rte_shift).reshape(len(test),-1)

    return {
      "A":(A_tr,A_te),
      "X":(np.column_stack([A_tr,I_tr]),np.column_stack([A_te,I_te])),
      "X_shift":(np.column_stack([A_tr,Ish_tr]),np.column_stack([A_te,Ish_te]))
    }

def fit_eval(train,test,Xtr,Xte):
    ytr=(train.model=="mg").to_numpy(int); yte=(test.model=="mg").to_numpy(int)
    wtr=balanced_weights(train); wte=balanced_weights(test)
    sc=StandardScaler().fit(Xtr,sample_weight=wtr)
    Xtr=sc.transform(Xtr); Xte=sc.transform(Xte)
    clf=LogisticRegression(penalty=None,solver="lbfgs",max_iter=400,tol=1e-8)
    clf.fit(Xtr,ytr,sample_weight=wtr)
    p=clf.predict_proba(Xte)[:,1]
    return {"log_loss":float(log_loss(yte,p,sample_weight=wte,labels=[0,1])),
            "auc":float(roc_auc_score(yte,p,sample_weight=wte))}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--baseline",required=True); ap.add_argument("--mg",required=True); ap.add_argument("--out",required=True)
    args=ap.parse_args()
    base=load_family(args.baseline,"baseline"); mg=load_family(args.mg,"mg")
    all_df=pd.concat([base,mg],ignore_index=True)
    store={k:[] for k in ("A","X","X_shift")}
    for fold in range(1,5):
        train=all_df[all_df.chain_id!=fold]
        test=all_df[all_df.chain_id==fold]
        mats=construct(train,test)
        for k,(Xtr,Xte) in mats.items():
            m=fit_eval(train,test,Xtr,Xte); m["fold"]=fold; store[k].append(m)
    cv={}
    for k,rows in store.items():
        cv[k]={"mean_log_loss":float(np.mean([r["log_loss"] for r in rows])),
               "mean_auc":float(np.mean([r["auc"] for r in rows])),
               "folds":rows}
    x_beats_a=sum(1 for x,a in zip(cv["X"]["folds"],cv["A"]["folds"]) if x["log_loss"]<a["log_loss"])
    x_beats_shift=sum(1 for x,s in zip(cv["X"]["folds"],cv["X_shift"]["folds"]) if x["log_loss"]<s["log_loss"])
    pooled_x_a=cv["X"]["mean_log_loss"]<cv["A"]["mean_log_loss"]
    pooled_x_shift=cv["X"]["mean_log_loss"]<cv["X_shift"]["mean_log_loss"]
    a_beats_x=sum(1 for a,x in zip(cv["A"]["folds"],cv["X"]["folds"]) if a["log_loss"]<=x["log_loss"])
    if pooled_x_a and x_beats_a>=3 and pooled_x_shift and x_beats_shift>=3:
        disp="CROSS_BLOCK_RELATIONSHIP_ADDS"
    elif cv["A"]["mean_log_loss"]<=cv["X"]["mean_log_loss"] and a_beats_x>=3:
        disp="CROSS_BLOCK_ADDITIVE_SUFFICIENT"
    elif pooled_x_a and x_beats_a>=3 and not (pooled_x_shift and x_beats_shift>=3):
        disp="INTERACTION_GAIN_PAIRING_NONESSENTIAL"
    else:
        disp="CROSS_BLOCK_RELATIONSHIP_INDETERMINATE"
    result={"protocol":"DESI_CROSS_BLOCK_RELATIONAL_QUALIFICATION_v0.1","disposition":disp,
            "cv":cv,"diagnostics":{"X_beats_A_fold_count":x_beats_a,
            "X_beats_X_shift_fold_count":x_beats_shift,"A_matches_or_beats_X_fold_count":a_beats_x,
            "pooled_X_beats_A":pooled_x_a,"pooled_X_beats_X_shift":pooled_x_shift},
            "rows":{"baseline":int(len(base)),"mg":int(len(mg))},
            "interaction_features":49,"pairing_shift_rule":"within model and source chain, circular shift max(1,n//3)"}
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2))
    print(json.dumps({"disposition":disp,"diagnostics":result["diagnostics"],
      "cv":{k:{"log_loss":v["mean_log_loss"],"auc":v["mean_auc"],"folds":v["folds"]} for k,v in cv.items()}},indent=2))

if __name__=="__main__":
    main()
