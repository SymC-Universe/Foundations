#!/usr/bin/env python3
import hashlib, json, math, urllib.request, zipfile, tempfile
from pathlib import Path
import numpy as np
from scipy.io import loadmat

URL="https://data.4tu.nl/file/b6dc643b-ecc6-437c-8a8a-1681650ec3fe/5414dfdc-6e8d-4208-be6e-fa553de9866f"
EXPECTED_SIZE=148455295
EXPECTED_SHA256="2278429b1f15f15448e6f101d395a5587d58ac23d32052fd42f8b33a894c0afa"
OUT=Path("stability_inheritance/results/f16_gvt_specialodd_replication")
OUT.mkdir(parents=True,exist_ok=True)

LEVEL_FORCE={1:12.2,2:49.0,3:97.1}
N=16384
P=3
FS=400.0

def normerr(pred,ref,mask):
    a=pred[mask]
    b=ref[mask]
    den=np.sum(np.abs(b)**2)
    if not np.isfinite(den) or den<=np.finfo(float).tiny:
        return math.nan
    return float(np.sqrt(np.sum(np.abs(a-b)**2)/den))

def frf_from_blocks(u,y):
    # u: realizations x periods x N
    # y: outputs x realizations x periods x N
    U=np.fft.rfft(u,axis=2)
    Y=np.fft.rfft(y,axis=3)
    den=np.sum(np.abs(U)**2,axis=(0,1))
    num=np.sum(Y*np.conj(U)[None,:,:,:],axis=(1,2))
    H=(num/np.maximum(den[None,:],np.finfo(float).tiny)).T
    return H,den

with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    zpath=td/"F16GVT_Files.zip"
    req=urllib.request.Request(URL,headers={"User-Agent":"SymC-Stability-Inheritance-P0Q/1.0"})
    with urllib.request.urlopen(req,timeout=120) as resp, zpath.open("wb") as f:
        while True:
            chunk=resp.read(1024*1024)
            if not chunk:
                break
            f.write(chunk)
    b=zpath.read_bytes()
    if len(b)!=EXPECTED_SIZE:
        raise RuntimeError(f"source size changed {len(b)} != {EXPECTED_SIZE}")
    sha=hashlib.sha256(b).hexdigest()
    if sha!=EXPECTED_SHA256:
        raise RuntimeError(f"source hash changed {sha} != {EXPECTED_SHA256}")
    with zipfile.ZipFile(zpath,"r") as z:
        z.extractall(td/"unz")
    root=td/"unz"/"F16GVT_Files"/"BenchmarkData"

    est={}
    test={}
    names={}
    for lev in [1,2,3]:
        main_candidates=list(root.rglob(f"*SpecialOddMSine_Level{lev}.mat"))
        val_candidates=list(root.rglob(f"*SpecialOddMSine_Level{lev}_Validation.mat"))
        if len(main_candidates)!=1 or len(val_candidates)!=1:
            raise RuntimeError(f"file identity mismatch level {lev}: main={main_candidates}, val={val_candidates}")
        mp=main_candidates[0]; vp=val_candidates[0]
        names[str(lev)]={"estimation":mp.name,"test":vp.name}
        dm=loadmat(mp)
        dv=loadmat(vp)
        for d,p,label in [(dm,mp,"estimation"),(dv,vp,"test")]:
            if "Force" not in d or "Acceleration" not in d or "Fs" not in d:
                raise RuntimeError(f"missing arrays {p.name}")
            fs=float(np.asarray(d["Fs"]).squeeze())
            if abs(fs-FS)>1e-9:
                raise RuntimeError(f"sampling rate mismatch {fs} {p.name}")
        um=np.asarray(dm["Force"],float)
        ym=np.asarray(dm["Acceleration"],float)
        uv=np.asarray(dv["Force"],float)
        yv=np.asarray(dv["Acceleration"],float)
        if um.shape!=(9,P*N) or ym.shape!=(3,9,P*N):
            raise RuntimeError(f"estimation shape mismatch level {lev}: {um.shape}, {ym.shape}")
        if uv.shape!=(1,P*N) or yv.shape!=(3,1,P*N):
            raise RuntimeError(f"test shape mismatch level {lev}: {uv.shape}, {yv.shape}")
        # Reshape without inspecting values. Discard first period.
        um=um.reshape(9,P,N)[:,1:,:]
        ym=ym.reshape(3,9,P,N)[:,:,1:,:]
        uv=uv.reshape(1,P,N)[:,1:,:]
        yv=yv.reshape(3,1,P,N)[:,:,1:,:]
        est[lev]=(um,ym)
        test[lev]=(uv,yv)

    freq=np.fft.rfftfreq(N,d=1/FS)

    Hspec={}
    Ein={}
    for lev in [1,2,3]:
        Hspec[lev],Ein[lev]=frf_from_blocks(*est[lev])

    # Frozen pooled representation across all three estimation amplitudes.
    all_u=np.concatenate([est[lev][0] for lev in [1,2,3]],axis=0)
    all_y=np.concatenate([est[lev][1] for lev in [1,2,3]],axis=1)
    Hpool,Epool=frf_from_blocks(all_u,all_y)

    Htest={}
    Etest={}
    for lev in [1,2,3]:
        Htest[lev],Etest[lev]=frf_from_blocks(*test[lev])

    def estimation_support(lo,hi):
        band=(freq>=lo)&(freq<=hi)&(freq>0)
        mx=float(np.max(Epool[band])) if np.any(band) else 0.0
        return band & (Epool > 1e-12*mx)

    sup_primary=estimation_support(6.5,8.2)
    sup_full=estimation_support(1.0,15.0)
    if int(sup_primary.sum())<3:
        raise RuntimeError(f"insufficient estimation-only primary support {int(sup_primary.sum())}")

    # The frozen task prohibits test-driven support selection. We therefore score
    # exactly the estimation-defined support. A held-out FRF with numerically
    # zero input energy on those bins is an invalid test rather than a reason to
    # change support after exposure.
    tiny=np.finfo(float).tiny
    for lev in [1,2,3]:
        if np.any(Etest[lev][sup_primary] <= tiny):
            raise RuntimeError(f"held-out realization lacks frozen primary support at level {lev}")

    scores={}
    winners={}
    for lev in [1,2,3]:
        ref=Htest[lev]
        e_spec=normerr(Hspec[lev],ref,sup_primary)
        e_pool=normerr(Hpool,ref,sup_primary)
        e_cross={str(k):normerr(Hspec[k],ref,sup_primary) for k in [1,2,3] if k!=lev}
        e_all={"SPECIFIC":e_spec,"POOLED":e_pool}
        for k,v in e_cross.items():
            e_all[f"LEVEL_{k}"]=v
        winner=min(e_all,key=e_all.get)
        winners[str(lev)]=winner
        scores[str(lev)]={
          "force_rms_N":LEVEL_FORCE[lev],
          "primary":{"specific":e_spec,"pooled":e_pool,"cross":e_cross,"winner":winner},
          "secondary_1_15Hz":{
            "specific":normerr(Hspec[lev],ref,sup_full),
            "pooled":normerr(Hpool,ref,sup_full),
            "cross":{str(k):normerr(Hspec[k],ref,sup_full) for k in [1,2,3] if k!=lev}
          },
          "per_output_primary":{
            str(j+1):{
              "specific":normerr(Hspec[lev][:,j],ref[:,j],sup_primary),
              "pooled":normerr(Hpool[:,j],ref[:,j],sup_primary),
              "cross":{str(k):normerr(Hspec[k][:,j],ref[:,j],sup_primary) for k in [1,2,3] if k!=lev}
            } for j in range(3)
          }
        }

    if all(winners[str(lev)]=="SPECIFIC" for lev in [1,2,3]):
        disp="SPECIALODD_AMPLITUDE_SPECIFIC_REPLICATES"
        role="ARCHITECTURE_SUPPORTING_NATIVE_REPLICATION"
    elif all(winners[str(lev)]=="POOLED" for lev in [1,2,3]):
        disp="SPECIALODD_POOLED_SUFFICIENT"
        role="LIMIT_NATIVE_EVIDENCE"
    else:
        disp="SPECIALODD_MIXED_TRANSPORT"
        role="MIXED_NATIVE_EVIDENCE"

    rel={}
    distances={}
    for lev in [1,2,3]:
        rel_est=Hspec[lev][:,2]-Hspec[lev][:,1]
        rel_test=Htest[lev][:,2]-Htest[lev][:,1]
        rel[str(lev)]={
          "heldout_specific_error":normerr(rel_est,rel_test,sup_primary),
          "heldout_pooled_error":normerr(Hpool[:,2]-Hpool[:,1],rel_test,sup_primary)
        }
        distances[str(lev)]={
          str(k):normerr(Hspec[k],Hspec[lev],sup_primary) for k in [1,2,3] if k!=lev
        }

    out={
      "status":"PUBLIC_EXTERNAL_P0Q_REPLICATION",
      "protocol":"F16_GVT_SPECIALODD_REPLICATION_PROTOCOL_v0.1",
      "source_sha256":sha,
      "files":names,
      "sampling_hz":FS,
      "estimation_realizations_per_level":9,
      "heldout_realizations_per_level":1,
      "periods_total":3,
      "periods_scored":"2-3",
      "primary_band_hz":[6.5,8.2],
      "primary_support_bins":int(sup_primary.sum()),
      "secondary_support_bins":int(sup_full.sum()),
      "scores":scores,
      "winners":winners,
      "interface_relative":rel,
      "representation_distances":distances,
      "disposition":disp,
      "architecture_evidence_role":role,
      "novelty_role":"NATIVE_MODEL_COMPATIBLE_NO_SI_NOVELTY_CLAIM",
      "notation":{"chi":"NOT_ADMITTED","Chi":"NOT_FORCED_NATIVE_FRF_USED","Chi_arc":"NOT_AUTOMATICALLY_ASSIGNED"}
    }
    (OUT/"result.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
