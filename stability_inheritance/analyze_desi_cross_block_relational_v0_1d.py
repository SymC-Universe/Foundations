#!/usr/bin/env python3
from pathlib import Path
import argparse, gc, json, tempfile, warnings
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import log_loss, roc_auc_score

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
    if miss:
        raise RuntimeError(f"{path}: missing {miss}")
    df=pd.read_csv(path,sep=r"\s+",comment="#",names=names,usecols=KEEP,
                   dtype={c:"float64" for c in KEEP},engine="c")
    df["model"]=model
    df["chain_id"]=int(chain_id)
    return df

def load_family(root,model):
    return pd.concat(
        [load_chain(Path(root)/f"chain.{j}.txt",model,j) for j in range(1,5)],
        ignore_index=True
    )

def balanced_weights(df):
    y=(df.model=="mg").to_numpy(int)
    w=df.weight.to_numpy(float)
    out=np.zeros_like(w,float)
    for cls in (0,1):
        m=y==cls
        out[m]=0.5*w[m]/w[m].sum()
    return out

def fit_residualizer(train):
    w=balanced_weights(train)
    t=train[T].to_numpy(float)
    s=t.sum(axis=1)
    X=np.column_stack([np.ones(len(train)),s])
    sw=np.sqrt(w)
    Xw=X*sw[:,None]
    betas=np.empty((len(T),2),dtype=np.float64)
    for j in range(len(T)):
        betas[j]=np.linalg.lstsq(Xw,t[:,j]*sw,rcond=None)[0]
    return betas

def residuals(df,betas):
    t=df[T].to_numpy(float)
    s=t.sum(axis=1)
    pred=betas[:,0][None,:]+s[:,None]*betas[:,1][None,:]
    return s,t-pred

def weighted_standardize_train_test(Xtr,Xte,wtr):
    sw=float(wtr.sum())
    p=Xtr.shape[1]
    mu=np.empty(p,dtype=np.float64)
    scale=np.empty(p,dtype=np.float64)
    for j in range(p):
        col=Xtr[:,j]
        m=float(np.dot(col,wtr)/sw)
        d=col-m
        v=float(np.dot(d*d,wtr)/sw)
        sc=float(np.sqrt(max(v,1e-300)))
        col-=m
        col/=sc
        Xte[:,j]-=m
        Xte[:,j]/=sc
        mu[j]=m
        scale[j]=sc
        del d
    return mu,scale

def standardize_copy(Xtr,Xte,wtr):
    a=np.array(Xtr,dtype=np.float64,copy=True,order="C")
    b=np.array(Xte,dtype=np.float64,copy=True,order="C")
    weighted_standardize_train_test(a,b,wtr)
    return a,b

def shift_within_class_chain(df,R):
    out=np.empty_like(R)
    model=df.model.to_numpy()
    chain=df.chain_id.to_numpy()
    for m in ("baseline","mg"):
        for c in (1,2,3,4):
            idx=np.flatnonzero((model==m)&(chain==c))
            if len(idx)==0:
                continue
            shift=max(1,len(idx)//3)
            out[idx]=np.roll(R[idx],shift=shift,axis=0)
    return out

def build_interactions_direct(bg,R):
    n=len(bg)
    out=np.empty((n,len(BG)*len(T)),dtype=np.float64)
    k=0
    for i in range(len(BG)):
        for j in range(len(T)):
            np.multiply(bg[:,i],R[:,j],out=out[:,k])
            k+=1
    return out

def equivalence_guard(bg,R):
    n=min(1024,len(bg))
    old=np.einsum("ni,nj->nij",bg[:n],R[:n]).reshape(n,-1)
    new=build_interactions_direct(bg[:n],R[:n])
    ok=bool(np.allclose(old,new,rtol=0,atol=0))
    max_abs=float(np.max(np.abs(old-new))) if old.size else 0.0
    del old,new
    if not ok:
        raise RuntimeError(f"INTERACTION_BUILDER_EQUIVALENCE_FAILED max_abs={max_abs}")
    return {"rows":n,"exact_allclose":ok,"max_abs_difference":max_abs}

def fit_eval_inplace(train,test,Xtr,Xte):
    ytr=(train.model=="mg").to_numpy(int)
    yte=(test.model=="mg").to_numpy(int)
    wtr=balanced_weights(train)
    wte=balanced_weights(test)
    weighted_standardize_train_test(Xtr,Xte,wtr)
    clf=LogisticRegression(penalty=None,solver="lbfgs",max_iter=2000,tol=1e-8)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        clf.fit(Xtr,ytr,sample_weight=wtr)
    conv=[w for w in caught if issubclass(w.category,ConvergenceWarning)]
    p=clf.predict_proba(Xte)[:,1]
    result={
        "log_loss":float(log_loss(yte,p,sample_weight=wte,labels=[0,1])),
        "auc":float(roc_auc_score(yte,p,sample_weight=wte)),
        "n_iter":int(clf.n_iter_[0]),
        "convergence_warning":bool(conv)
    }
    del clf,p,ytr,yte,wtr,wte
    return result

def base_components(train,test):
    betas=fit_residualizer(train)
    strn,Rtr=residuals(train,betas)
    ste,Rte=residuals(test,betas)
    bgtr=train[BG].to_numpy(float)
    bgte=test[BG].to_numpy(float)
    wtr=balanced_weights(train)
    bgtrz,bgtez=standardize_copy(bgtr,bgte,wtr)
    Rtrz,Rtez=standardize_copy(Rtr,Rte,wtr)
    A_tr=np.column_stack([bgtr,strn,Rtr])
    A_te=np.column_stack([bgte,ste,Rte])
    return A_tr,A_te,bgtrz,bgtez,Rtrz,Rtez

def build_X_memmap(A,bg,R,path):
    n=len(A)
    p=A.shape[1]+len(BG)*len(T)
    X=np.memmap(path,dtype=np.float64,mode="w+",shape=(n,p),order="C")
    X[:,:A.shape[1]]=A
    k=A.shape[1]
    for i in range(len(BG)):
        for j in range(len(T)):
            np.multiply(bg[:,i],R[:,j],out=X[:,k])
            k+=1
    X.flush()
    return X

def close_memmap(X,path):
    X.flush()
    mmap_handle=getattr(X,"_mmap",None)
    if mmap_handle is not None:
        mmap_handle.close()
    del X
    gc.collect()
    Path(path).unlink()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--baseline",required=True)
    ap.add_argument("--mg",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    base=load_family(args.baseline,"baseline")
    mg=load_family(args.mg,"mg")
    all_df=pd.concat([base,mg],ignore_index=True)
    del base,mg
    gc.collect()

    store={k:[] for k in ("A","X","X_shift")}
    guard=None

    with tempfile.TemporaryDirectory(prefix="desi_cross_block_v01c_") as td:
        td=Path(td)
        for fold in range(1,5):
            train=all_df[all_df.chain_id!=fold].reset_index(drop=True)
            test=all_df[all_df.chain_id==fold].reset_index(drop=True)
            A_tr,A_te,bgtrz,bgtez,Rtrz,Rtez=base_components(train,test)

            if guard is None:
                guard=equivalence_guard(bgtrz,Rtrz)

            Atr_fit=np.array(A_tr,copy=True,order="C")
            Ate_fit=np.array(A_te,copy=True,order="C")
            m=fit_eval_inplace(train,test,Atr_fit,Ate_fit)
            m["fold"]=fold
            store["A"].append(m)
            del Atr_fit,Ate_fit
            gc.collect()

            xtr_path=td/f"fold{fold}_Xtr.dat"
            xte_path=td/f"fold{fold}_Xte.dat"
            Xtr=build_X_memmap(A_tr,bgtrz,Rtrz,xtr_path)
            Xte=build_X_memmap(A_te,bgtez,Rtez,xte_path)
            m=fit_eval_inplace(train,test,Xtr,Xte)
            m["fold"]=fold
            store["X"].append(m)
            close_memmap(Xtr,xtr_path)
            close_memmap(Xte,xte_path)

            Rtr_shift=shift_within_class_chain(train,Rtrz)
            Rte_shift=shift_within_class_chain(test,Rtez)
            xstr_path=td/f"fold{fold}_Xstr.dat"
            xste_path=td/f"fold{fold}_Xste.dat"
            Xstr=build_X_memmap(A_tr,bgtrz,Rtr_shift,xstr_path)
            Xste=build_X_memmap(A_te,bgtez,Rte_shift,xste_path)
            m=fit_eval_inplace(train,test,Xstr,Xste)
            m["fold"]=fold
            store["X_shift"].append(m)
            close_memmap(Xstr,xstr_path)
            close_memmap(Xste,xste_path)

            del Rtr_shift,Rte_shift
            del A_tr,A_te,bgtrz,bgtez,Rtrz,Rtez,train,test
            gc.collect()

    cv={}
    for k,rows in store.items():
        cv[k]={
            "mean_log_loss":float(np.mean([r["log_loss"] for r in rows])),
            "mean_auc":float(np.mean([r["auc"] for r in rows])),
            "folds":rows
        }

    x_beats_a=sum(1 for x,a in zip(cv["X"]["folds"],cv["A"]["folds"])
                  if x["log_loss"]<a["log_loss"])
    x_beats_shift=sum(1 for x,s in zip(cv["X"]["folds"],cv["X_shift"]["folds"])
                      if x["log_loss"]<s["log_loss"])
    a_beats_x=sum(1 for a,x in zip(cv["A"]["folds"],cv["X"]["folds"])
                  if a["log_loss"]<=x["log_loss"])
    pooled_x_a=cv["X"]["mean_log_loss"]<cv["A"]["mean_log_loss"]
    pooled_x_shift=cv["X"]["mean_log_loss"]<cv["X_shift"]["mean_log_loss"]

    if pooled_x_a and x_beats_a>=3 and pooled_x_shift and x_beats_shift>=3:
        disp="CROSS_BLOCK_RELATIONSHIP_ADDS"
    elif cv["A"]["mean_log_loss"]<=cv["X"]["mean_log_loss"] and a_beats_x>=3:
        disp="CROSS_BLOCK_ADDITIVE_SUFFICIENT"
    elif pooled_x_a and x_beats_a>=3 and not (pooled_x_shift and x_beats_shift>=3):
        disp="INTERACTION_GAIN_PAIRING_NONESSENTIAL"
    else:
        disp="CROSS_BLOCK_RELATIONSHIP_INDETERMINATE"

    result={
        "protocol":"DESI_CROSS_BLOCK_RELATIONAL_QUALIFICATION_v0.1 + memory repairs v0.1a/v0.1b/v0.1c + convergence audit v0.1d",
        "repair_class":"MECHANICAL_RESOURCE_ALLOCATION_PLUS_CONVERGENCE_VALIDITY",
        "storage_repair":"disk-backed float64 memmap for X and X_shift; scientific design unchanged",
        "convergence_audit":"DESI_CROSS_BLOCK_CONVERGENCE_VALIDITY_AUDIT_v0.1",
        "solver":"lbfgs",
        "penalty":null,
        "tol":1e-8,
        "max_iter":2000,
        "equivalence_guard":guard,
        "disposition":disp,
        "cv":cv,
        "diagnostics":{
            "X_beats_A_fold_count":x_beats_a,
            "X_beats_X_shift_fold_count":x_beats_shift,
            "A_matches_or_beats_X_fold_count":a_beats_x,
            "pooled_X_beats_A":pooled_x_a,
            "pooled_X_beats_X_shift":pooled_x_shift,
            "all_required_fits_converged":all(not r.get("convergence_warning",False) for rows in store.values() for r in rows),
            "max_observed_iterations":max(r.get("n_iter",0) for rows in store.values() for r in rows)
        },
        "rows":{"total":int(len(all_df))},
        "interaction_features":49,
        "pairing_shift_rule":"within model and source chain, circular shift max(1,n//3)"
    }

    out=Path(args.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2))
    print(json.dumps({
        "disposition":disp,
        "equivalence_guard":guard,
        "diagnostics":result["diagnostics"],
        "cv":cv
    },indent=2))

if __name__=="__main__":
    main()
