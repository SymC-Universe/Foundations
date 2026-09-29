#!/usr/bin/env python3
import hashlib, json, math, urllib.request, zipfile, tempfile
from pathlib import Path
import numpy as np
from scipy.io import loadmat

URL="https://data.4tu.nl/file/b6dc643b-ecc6-437c-8a8a-1681650ec3fe/5414dfdc-6e8d-4208-be6e-fa553de9866f"
EXPECTED_SIZE=148455295
EXPECTED_SHA256="2278429b1f15f15448e6f101d395a5587d58ac23d32052fd42f8b33a894c0afa"
OUT=Path("stability_inheritance/results/f16_gvt_cross_excitation_exploratory")
OUT.mkdir(parents=True,exist_ok=True)

FS=400.0
NF=8192
NS=16384
FULL_FORCE={1:12.4,3:36.8,5:73.6,7:97.8}
SPEC_FORCE={1:12.2,2:49.0,3:97.1}

def empirical_frf(u,y):
    # u: realization x period x N; y: output x realization x period x N
    U=np.fft.rfft(u,axis=2)
    Y=np.fft.rfft(y,axis=3)
    den=np.sum(np.abs(U)**2,axis=(0,1))
    num=np.sum(Y*np.conj(U)[None,:,:,:],axis=(1,2))
    H=(num/np.maximum(den[None,:],np.finfo(float).tiny)).T
    return H,den

def normerr(pred,ref,mask):
    a=pred[mask]; b=ref[mask]
    den=np.sum(np.abs(b)**2)
    if not np.isfinite(den) or den<=np.finfo(float).tiny:
        return math.nan
    return float(np.sqrt(np.sum(np.abs(a-b)**2)/den))

def interp(a,b,target,H):
    w=(target-FULL_FORCE[a])/(FULL_FORCE[b]-FULL_FORCE[a])
    return (1-w)*H[a]+w*H[b]

with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    zpath=td/"F16GVT_Files.zip"
    req=urllib.request.Request(URL,headers={"User-Agent":"SymC-Stability-Inheritance-P0D/1.0"})
    with urllib.request.urlopen(req,timeout=120) as resp, zpath.open("wb") as f:
        while True:
            chunk=resp.read(1024*1024)
            if not chunk: break
            f.write(chunk)
    b=zpath.read_bytes()
    if len(b)!=EXPECTED_SIZE:
        raise RuntimeError(f"source size changed {len(b)}")
    sha=hashlib.sha256(b).hexdigest()
    if sha!=EXPECTED_SHA256:
        raise RuntimeError(f"source hash changed {sha}")
    with zipfile.ZipFile(zpath,"r") as z:
        z.extractall(td/"unz")
    root=td/"unz"/"F16GVT_Files"/"BenchmarkData"

    # FullMSine estimation representations only.
    Hfull={}; Efull={}
    for lev in [1,3,5,7]:
        cand=list(root.rglob(f"*FullMSine_Level{lev}.mat"))
        cand=[p for p in cand if "Validation" not in p.name]
        if len(cand)!=1:
            raise RuntimeError(f"FullMSine identity mismatch level {lev}: {cand}")
        d=loadmat(cand[0])
        force=np.asarray(d["Force"],float).squeeze()
        acc=np.asarray(d["Acceleration"],float)
        fs=float(np.asarray(d["Fs"]).squeeze())
        if abs(fs-FS)>1e-9 or force.size!=9*NF:
            raise RuntimeError(f"FullMSine shape/fs mismatch level {lev}")
        if acc.shape==(3,9*NF):
            yy=acc
        elif acc.shape==(9*NF,3):
            yy=acc.T
        else:
            raise RuntimeError(f"FullMSine acceleration shape {acc.shape}")
        u=force.reshape(1,9,NF)[:,1:,:]
        y=yy.reshape(3,1,9,NF)[:,:,1:,:]
        Hfull[lev],Efull[lev]=empirical_frf(u,y)

    # SpecialOdd estimation support and held-out targets.
    Hspec_est={}; Espec_est={}; Hspec_test={}; Espec_test={}
    for lev in [1,2,3]:
        mc=list(root.rglob(f"*SpecialOddMSine_Level{lev}.mat"))
        mc=[p for p in mc if "Validation" not in p.name]
        vc=list(root.rglob(f"*SpecialOddMSine_Level{lev}_Validation.mat"))
        if len(mc)!=1 or len(vc)!=1:
            raise RuntimeError(f"SpecialOdd identity mismatch level {lev}")
        dm=loadmat(mc[0]); dv=loadmat(vc[0])
        um=np.asarray(dm["Force"],float); ym=np.asarray(dm["Acceleration"],float)
        uv=np.asarray(dv["Force"],float); yv=np.asarray(dv["Acceleration"],float)
        if um.shape!=(9,3*NS) or ym.shape!=(3,9,3*NS):
            raise RuntimeError(f"SpecialOdd estimation shape mismatch level {lev}")
        if uv.shape!=(1,3*NS) or yv.shape!=(3,1,3*NS):
            raise RuntimeError(f"SpecialOdd test shape mismatch level {lev}")
        um=um.reshape(9,3,NS)[:,1:,:]
        ym=ym.reshape(3,9,3,NS)[:,:,1:,:]
        uv=uv.reshape(1,3,NS)[:,1:,:]
        yv=yv.reshape(3,1,3,NS)[:,:,1:,:]
        Hspec_est[lev],Espec_est[lev]=empirical_frf(um,ym)
        Hspec_test[lev],Espec_test[lev]=empirical_frf(uv,yv)

    ff=np.fft.rfftfreq(NF,d=1/FS)
    fspec=np.fft.rfftfreq(NS,d=1/FS)
    if not np.allclose(ff,fspec[::2],rtol=0,atol=1e-12):
        raise RuntimeError("DFT frequency grids do not map exactly")

    full_pool=sum(Efull.values())
    spec_pool=sum(Espec_est.values())

    def common_mask(lo,hi):
        band=(ff>=lo)&(ff<=hi)&(ff>0)
        mxF=float(np.max(full_pool[band])) if np.any(band) else 0.0
        supportF=band & (full_pool>1e-12*mxF)
        spec_on_full=spec_pool[::2]
        mxS=float(np.max(spec_on_full[band])) if np.any(band) else 0.0
        supportS=band & (spec_on_full>1e-12*mxS)
        return supportF & supportS

    primary=common_mask(6.5,8.2)
    secondary=common_mask(2.0,15.0)
    if int(primary.sum())<3:
        raise RuntimeError(f"insufficient common estimation support {int(primary.sum())}")

    # Held-out support must already exist on the frozen estimation-defined intersection.
    for lev in [1,2,3]:
        if np.any(Espec_test[lev][::2][primary] <= np.finfo(float).tiny):
            raise RuntimeError(f"held-out target lacks common support level {lev}")

    predictors={
      1:Hfull[1],
      2:interp(3,5,SPEC_FORCE[2],Hfull),
      3:interp(5,7,SPEC_FORCE[3],Hfull)
    }
    fixed=Hfull[1]

    scores={}
    ratios={}
    for lev in [1,2,3]:
        ref=Hspec_test[lev][::2]
        ep=normerr(predictors[lev],ref,primary)
        ef=normerr(fixed,ref,primary)
        ratio=ep/ef if np.isfinite(ep) and np.isfinite(ef) and ef>0 else math.nan
        ratios[str(lev)]=ratio
        scores[str(lev)]={
          "force_rms_N":SPEC_FORCE[lev],
          "conditioned_or_anchor_primary":ep,
          "fixed_level1_primary":ef,
          "ratio":ratio,
          "secondary_2_15Hz":{
            "conditioned_or_anchor":normerr(predictors[lev],ref,secondary),
            "fixed_level1":normerr(fixed,ref,secondary)
          },
          "per_output_primary":{
            str(j+1):{
              "conditioned_or_anchor":normerr(predictors[lev][:,j],ref[:,j],primary),
              "fixed_level1":normerr(fixed[:,j],ref[:,j],primary)
            } for j in range(3)
          }
        }

    r49=ratios["2"]; r97=ratios["3"]
    if not np.isfinite(r49) or not np.isfinite(r97):
        disp="INDETERMINATE"
    elif r49<1 and r97<1:
        disp="CROSS_EXCITATION_ARCHITECTURE_TRANSPORTS"
    elif (r49<1) ^ (r97<1):
        disp="CROSS_EXCITATION_MIXED"
    else:
        disp="CROSS_EXCITATION_CONDITIONING_NOT_SUPPORTED"

    out={
      "status":"P0D_POST_RESULT_EXPLORATORY",
      "protocol":"F16_GVT_CROSS_EXCITATION_TRANSPORT_PROTOCOL_v0.1",
      "exposure_correction_commit":"7e9b876a34bcc1cc32074c793185a7025882ce86",
      "source_sha256":sha,
      "primary_band_hz":[6.5,8.2],
      "primary_common_support_bins":int(primary.sum()),
      "secondary_common_support_bins":int(secondary.sum()),
      "scores":scores,
      "primary_ratios":{"49N":r49,"97.1N":r97},
      "disposition":disp,
      "architecture_evidence_role":"EXPLORATORY_ARCHITECTURE_MAPPING",
      "promotion_debt":"SPECIALODD_VALIDATION_TARGETS_ALREADY_SEEN_BEFORE_PROTOCOL_COMMIT",
      "claim_ceiling":"cannot increase confirmatory ceiling; fresh untouched target required",
      "notation":{"chi":"NOT_ADMITTED","Chi":"NOT_FORCED_NATIVE_FRF_USED","Chi_arc":"NOT_AUTOMATICALLY_ASSIGNED"}
    }
    (OUT/"result.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
