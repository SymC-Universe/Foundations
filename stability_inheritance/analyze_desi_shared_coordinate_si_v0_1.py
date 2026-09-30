#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.preprocessing import StandardScaler

B = ["omegam","H0","rdrag"]
G = ["sigma8","s8h5","s8omegamp5","s8omegamp25"]
T = ["Lya_z0.loglikelihood","QSO_z0.loglikelihood","ELG_z1.loglikelihood",
     "LRG_z2.loglikelihood","LRG_z1.loglikelihood","LRG_z0.loglikelihood",
     "BGS_z0.loglikelihood"]
BLOCKS = {"B":B, "G":G, "T":T, "BG":B+G, "C":B+G+T}
KEEP = ["weight"] + BLOCKS["C"]

def header(path):
    with open(path,"r",encoding="utf-8",errors="replace") as f:
        line=f.readline()
    if not line.startswith("#"):
        raise RuntimeError(f"Missing Cobaya header: {path}")
    return line[1:].strip().split()

def load_chain(path, model, chain_id):
    names=header(path)
    missing=[c for c in KEEP if c not in names]
    if missing:
        raise RuntimeError(f"{path}: missing shared columns {missing}")
    df=pd.read_csv(path,sep=r"\s+",comment="#",names=names,usecols=KEEP,
                   dtype={c:"float64" for c in KEEP},engine="c")
    df["model"]=model
    df["chain_id"]=int(chain_id)
    df["row_id"]=np.arange(len(df),dtype=np.int64)
    return df

def load_family(root, model):
    frames=[]
    for j in range(1,5):
        p=Path(root)/f"chain.{j}.txt"
        frames.append(load_chain(p,model,j))
    return pd.concat(frames,ignore_index=True)

def neff(w):
    w=np.asarray(w,float)
    return float(w.sum()**2/np.square(w).sum())

def wmean_cov(X,w):
    X=np.asarray(X,float); w=np.asarray(w,float)
    sw=w.sum(); mu=np.sum(X*w[:,None],axis=0)/sw
    xc=X-mu
    cov=(xc*w[:,None]).T@xc/sw
    return mu,cov

def corr_from_cov(cov):
    d=np.sqrt(np.clip(np.diag(cov),1e-300,None))
    return cov/np.outer(d,d)

def invsqrt(a):
    vals,vecs=np.linalg.eigh((a+a.T)/2)
    floor=max(float(np.max(vals))*1e-10,1e-12)
    vals=np.clip(vals,floor,None)
    return (vecs*(1/np.sqrt(vals)))@vecs.T

def canonical_spectrum(df):
    X=df[B+G].to_numpy(float); w=df["weight"].to_numpy(float)
    _,cov=wmean_cov(X,w)
    nb=len(B); sbb=cov[:nb,:nb]; sgg=cov[nb:,nb:]; sbg=cov[:nb,nb:]
    m=invsqrt(sbb)@sbg@invsqrt(sgg)
    s=np.linalg.svd(m,compute_uv=False)
    return np.clip(s,0,1).tolist()

def block_stats(df, cols):
    X=df[cols].to_numpy(float); w=df["weight"].to_numpy(float)
    mu,cov=wmean_cov(X,w)
    return {"mean":mu.tolist(),"cov":cov.tolist(),"corr":corr_from_cov(cov).tolist(),
            "neff":neff(w),"weight_sum":float(w.sum()),"n_rows":int(len(df))}

def pooled_standardized_shift(a,b,cols):
    Xa=a[cols].to_numpy(float); Xb=b[cols].to_numpy(float)
    wa=a.weight.to_numpy(float); wb=b.weight.to_numpy(float)
    ma,ca=wmean_cov(Xa,wa); mb,cb=wmean_cov(Xb,wb)
    pooled=(ca+cb)/2
    sd=np.sqrt(np.clip(np.diag(pooled),1e-300,None))
    return float(np.linalg.norm((mb-ma)/sd))

def corr_distance(a,b,cols):
    _,ca=wmean_cov(a[cols].to_numpy(float),a.weight.to_numpy(float))
    _,cb=wmean_cov(b[cols].to_numpy(float),b.weight.to_numpy(float))
    return float(np.linalg.norm(corr_from_cov(cb)-corr_from_cov(ca),ord="fro"))

def within_envelope(df,cols,kind="corr"):
    vals=[]
    chains={j:df[df.chain_id==j] for j in range(1,5)}
    for i in range(1,5):
        for j in range(i+1,5):
            if kind=="corr":
                vals.append(corr_distance(chains[i],chains[j],cols))
            else:
                si=np.array(canonical_spectrum(chains[i])); sj=np.array(canonical_spectrum(chains[j]))
                n=min(len(si),len(sj)); vals.append(float(np.linalg.norm(si[:n]-sj[:n])))
    return {"max":float(max(vals)),"median":float(np.median(vals)),"all":vals}

def balanced_weights(y,w):
    out=np.zeros_like(w,dtype=float)
    for cls in (0,1):
        m=y==cls; s=w[m].sum()
        out[m]=0.5*w[m]/s
    return out

def fit_eval(train,test,cols):
    Xtr=train[cols].to_numpy(float); Xte=test[cols].to_numpy(float)
    ytr=(train.model=="mg").to_numpy(int); yte=(test.model=="mg").to_numpy(int)
    wtr=balanced_weights(ytr,train.weight.to_numpy(float))
    wte=balanced_weights(yte,test.weight.to_numpy(float))
    sc=StandardScaler().fit(Xtr,sample_weight=wtr)
    Xtr=sc.transform(Xtr); Xte=sc.transform(Xte)
    clf=LogisticRegression(penalty=None,solver="lbfgs",max_iter=300,tol=1e-8)
    clf.fit(Xtr,ytr,sample_weight=wtr)
    p=clf.predict_proba(Xte)[:,1]
    return {"log_loss":float(log_loss(yte,p,sample_weight=wte,labels=[0,1])),
            "auc":float(roc_auc_score(yte,p,sample_weight=wte))}

def losc_cv(all_df):
    out={k:[] for k in BLOCKS}
    for fold in range(1,5):
        train=all_df[all_df.chain_id!=fold]
        test=all_df[all_df.chain_id==fold]
        for k,cols in BLOCKS.items():
            m=fit_eval(train,test,cols); m["fold"]=fold; out[k].append(m)
    agg={}
    for k,rows in out.items():
        agg[k]={"mean_log_loss":float(np.mean([r["log_loss"] for r in rows])),
                "mean_auc":float(np.mean([r["auc"] for r in rows])),
                "folds":rows}
    return agg

def modulo_cv(all_df):
    out={k:[] for k in BLOCKS}
    fold_id=(all_df.row_id.to_numpy()%5)
    for fold in range(5):
        train=all_df[fold_id!=fold]; test=all_df[fold_id==fold]
        for k,cols in BLOCKS.items():
            m=fit_eval(train,test,cols); m["fold"]=fold; out[k].append(m)
    return {k:{"mean_log_loss":float(np.mean([r["log_loss"] for r in rows])),
               "mean_auc":float(np.mean([r["auc"] for r in rows])),
               "folds":rows} for k,rows in out.items()}

def ordering_count(cv,left,right):
    return sum(1 for a,b in zip(cv[left]["folds"],cv[right]["folds"]) if a["log_loss"]<b["log_loss"])

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--baseline",required=True); ap.add_argument("--mg",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    base=load_family(args.baseline,"baseline")
    mg=load_family(args.mg,"mg")
    all_df=pd.concat([base,mg],ignore_index=True)

    result={"protocol":"DESI_SHARED_COORDINATE_SI_QUALIFICATION_v0.1 + v0.1a",
            "model_only_parameters_used":False,
            "blocks":{}}
    for k,cols in BLOCKS.items():
        result["blocks"][k]={
          "baseline":block_stats(base,cols),"mg":block_stats(mg,cols),
          "mean_shift_norm":pooled_standardized_shift(base,mg,cols),
          "corr_distance_between":corr_distance(base,mg,cols),
          "corr_within_baseline":within_envelope(base,cols),
          "corr_within_mg":within_envelope(mg,cols)}
    cb=np.array(canonical_spectrum(base)); cm=np.array(canonical_spectrum(mg))
    n=min(len(cb),len(cm))
    can_diff=float(np.linalg.norm(cb[:n]-cm[:n]))
    result["canonical_BG"]={
      "baseline":cb.tolist(),"mg":cm.tolist(),"between_distance":can_diff,
      "within_baseline":within_envelope(base,B+G,kind="canonical"),
      "within_mg":within_envelope(mg,B+G,kind="canonical")}
    result["losc"]=losc_cv(all_df)
    result["modulo5_secondary"]=modulo_cv(all_df)

    cv=result["losc"]
    c_vs={x:ordering_count(cv,"C",x) for x in ["B","G","T"]}
    bg_vs={x:ordering_count(cv,"BG",x) for x in ["B","G"]}
    pooled_joint=all(cv["C"]["mean_log_loss"]<cv[x]["mean_log_loss"] for x in ["B","G","T"])
    pooled_bg=all(cv["BG"]["mean_log_loss"]<cv[x]["mean_log_loss"] for x in ["B","G"])
    folds_joint=all(v>=3 for v in c_vs.values())
    folds_bg=all(v>=3 for v in bg_vs.values())
    canon_robust=can_diff>max(result["canonical_BG"]["within_baseline"]["max"],
                             result["canonical_BG"]["within_mg"]["max"])
    cdist=result["blocks"]["C"]["corr_distance_between"]
    marginal_max=max(result["blocks"]["B"]["corr_distance_between"],result["blocks"]["G"]["corr_distance_between"])
    cdist_robust=cdist>marginal_max and cdist>max(result["blocks"]["C"]["corr_within_baseline"]["max"],
                                                  result["blocks"]["C"]["corr_within_mg"]["max"])
    result["decision_diagnostics"]={"C_vs_fold_counts":c_vs,"BG_vs_fold_counts":bg_vs,
      "pooled_joint_ordering":pooled_joint,"pooled_BG_ordering":pooled_bg,
      "fold_joint_ordering":folds_joint,"fold_BG_ordering":folds_bg,
      "canonical_reorganization_robust":canon_robust,
      "C_correlation_reorganization_robust":cdist_robust}
    if pooled_joint and pooled_bg and folds_joint and folds_bg and (canon_robust or cdist_robust):
        disp="JOINT_REORGANIZATION_ADDS"
    elif not (folds_joint and folds_bg):
        best=min(["B","G","T"],key=lambda x:cv[x]["mean_log_loss"])
        if cv[best]["mean_log_loss"]<=cv["C"]["mean_log_loss"]:
            disp="MARGINAL_BLOCK_SUFFICIENT"
        else:
            disp="REPRESENTATION_INDETERMINATE"
    elif pooled_joint and not (canon_robust or cdist_robust):
        disp="JOINT_DIFFERENCE_REDUNDANT"
    else:
        disp="REPRESENTATION_INDETERMINATE"
    result["disposition"]=disp
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2))
    print(json.dumps({"disposition":disp,"decision_diagnostics":result["decision_diagnostics"],
      "losc":{k:{"log_loss":v["mean_log_loss"],"auc":v["mean_auc"]} for k,v in cv.items()},
      "canonical_BG":result["canonical_BG"],
      "block_distances":{k:{"mean_shift":v["mean_shift_norm"],"corr_distance":v["corr_distance_between"]} for k,v in result["blocks"].items()}},indent=2))

if __name__=="__main__":
    main()
