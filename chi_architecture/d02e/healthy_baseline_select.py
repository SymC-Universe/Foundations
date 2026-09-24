from __future__ import annotations
import csv, hashlib, io, json, math
from pathlib import Path

import numpy as np
import requests
from scipy.signal import csd, find_peaks

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"D02E_HEALTHY_BASELINE_SELECTION_v0.1.json"
SERVER="https://dataverse.csuc.cat"
PID="doi:10.34810/data1011"
HEADERS={"User-Agent":"SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}


def api_json(url, **params):
    r=requests.get(url,params=params,headers=HEADERS,timeout=180)
    r.raise_for_status()
    x=r.json()
    if x.get("status")!="OK":
        raise RuntimeError("Dataverse API did not return OK")
    return x


def metadata():
    x=api_json(f"{SERVER}/api/datasets/:persistentId/",persistentId=PID)
    return x["data"]["latestVersion"]["files"]


def original_csv_files(files, directory):
    rows=[]
    for item in files:
        if item.get("directoryLabel","")!=directory:
            continue
        df=item["dataFile"]
        label=item["label"]
        if label.endswith(".csv") and df.get("contentType")=="text/csv":
            rows.append({
                "id":int(df["id"]),
                "filename":label,
                "md5":df.get("md5"),
                "size":int(df.get("filesize",0)),
            })
    rows.sort(key=lambda x:int(x["filename"].split("_")[1].split(".")[0]))
    return rows


def fetch_bytes(file_id):
    r=requests.get(f"{SERVER}/api/access/datafile/{file_id}",headers=HEADERS,timeout=300)
    r.raise_for_status()
    return r.content


def parse_csv(raw):
    text=raw.decode("utf-8-sig",errors="replace")
    reader=csv.reader(io.StringIO(text))
    rows=list(reader)
    if not rows:
        raise RuntimeError("empty csv")
    header=rows[0]
    data=np.asarray(rows[1:],dtype=float)
    if data.ndim!=2:
        raise RuntimeError("unexpected csv dimensionality")
    return header,data


def response_matrix(header,data):
    # Keep numeric sensor columns; exclude an explicit time/index column by name.
    keep=[]
    names=[]
    for i,name in enumerate(header):
        low=name.strip().lower()
        if low in {"time","timestamp","t","index","sample"}:
            continue
        keep.append(i); names.append(name)
    x=data[:,keep]
    if x.shape[1] < 8:
        raise RuntimeError(f"expected multichannel response, got {x.shape}")
    if not np.all(np.isfinite(x)):
        raise RuntimeError("nonfinite baseline values")
    return names,x


def fdd_first_singular(x,fs=1600.0,nperseg=8192):
    nchan=x.shape[1]
    freqs=None
    mats=None
    for i in range(nchan):
        for k in range(i,nchan):
            f,p=csd(x[:,i],x[:,k],fs=fs,window="hann",nperseg=nperseg,
                    noverlap=nperseg//2,detrend="constant",scaling="density")
            if freqs is None:
                freqs=f
                mats=np.zeros((len(f),nchan,nchan),dtype=complex)
            mats[:,i,k]=p
            mats[:,k,i]=np.conjugate(p)
    s1=np.empty(len(freqs))
    vecs=np.empty((len(freqs),nchan),dtype=complex)
    for idx,m in enumerate(mats):
        vals,vec=np.linalg.eigh(m)
        order=np.argsort(vals)
        s1[idx]=float(np.real(vals[order[-1]]))
        v=vec[:,order[-1]]
        vecs[idx]=v/np.linalg.norm(v)
    return freqs,s1,vecs


def half_power(freq,s,peak_idx,lo_idx,hi_idx):
    peak=float(s[peak_idx]); target=peak/2.0
    # PSD/singular-value power half point, equivalent -3 dB power bandwidth.
    left=peak_idx
    while left>lo_idx and s[left]>=target:
        left-=1
    right=peak_idx
    while right<hi_idx and s[right]>=target:
        right+=1
    if left<=lo_idx and s[left]>=target:
        return None
    if right>=hi_idx and s[right]>=target:
        return None
    def interp(i0,i1):
        y0=float(s[i0]); y1=float(s[i1]); x0=float(freq[i0]); x1=float(freq[i1])
        if y1==y0: return 0.5*(x0+x1)
        return x0+(target-y0)*(x1-x0)/(y1-y0)
    fl=interp(left,left+1)
    fr=interp(right-1,right)
    bw=fr-fl
    if not math.isfinite(bw) or bw<=0: return None
    fn=float(freq[peak_idx])
    return {"f_peak_hz":fn,"bandwidth_hz":float(bw),"chi":float(bw/(2*fn))}


def main():
    files=metadata()
    healthy=original_csv_files(files,"DATA/A_1/Healthy")
    if len(healthy)!=20:
        raise RuntimeError(f"expected 20 healthy A_1 csv files, got {len(healthy)}")

    readme=[x for x in files if x["label"]=="Readme.txt"]
    readme_info=None
    if len(readme)==1:
        rb=fetch_bytes(int(readme[0]["dataFile"]["id"]))
        readme_info={
            "id":int(readme[0]["dataFile"]["id"]),
            "md5":hashlib.md5(rb).hexdigest(),
            "sha256":hashlib.sha256(rb).hexdigest(),
            "text":rb.decode("utf-8",errors="replace"),
        }

    reps=[]
    baseline_header=None
    channel_names=None
    for meta in healthy:
        raw=fetch_bytes(meta["id"])
        if meta["md5"] and hashlib.md5(raw).hexdigest()!=meta["md5"]:
            raise RuntimeError(f"MD5 mismatch {meta['filename']}")
        header,data=parse_csv(raw)
        if baseline_header is None:
            baseline_header=header
        elif header!=baseline_header:
            raise RuntimeError("healthy csv headers differ")
        names,x=response_matrix(header,data)
        if channel_names is None: channel_names=names
        elif names!=channel_names: raise RuntimeError("channel names differ")
        f,s,v=fdd_first_singular(x)
        mask=(f>=0.5)&(f<=100.0)
        idx=np.where(mask)[0]
        peaks,_=find_peaks(s[idx],prominence=np.max(s[idx])*1e-4)
        global_peaks=idx[peaks]
        reps.append({"meta":meta,"freq":f,"s1":s,"vecs":v,"peaks":global_peaks})

    # Candidate peaks from median spectrum.
    S=np.vstack([r["s1"] for r in reps])
    med=np.median(S,axis=0)
    f=reps[0]["freq"]
    mask=(f>=0.5)&(f<=100.0)
    idx=np.where(mask)[0]
    p,_=find_peaks(med[idx],prominence=np.max(med[idx])*1e-4)
    cand=idx[p]
    cand=sorted(cand,key=lambda i:f[i])

    families=[]
    for ci in cand:
        fn=float(f[ci])
        # tracking window = +-5% around median candidate, capped by adjacent candidate midpoints later
        lo_f=fn*0.95; hi_f=fn*1.05
        lo=int(np.searchsorted(f,lo_f,"left"))
        hi=int(np.searchsorted(f,hi_f,"right")-1)
        entries=[]
        for r in reps:
            local=[int(q) for q in r["peaks"] if lo<=q<=hi]
            if not local:
                entries.append({"status":"NON_IDENTIFIABLE"})
                continue
            # nearest to baseline candidate frequency; ambiguity if near-equal competing peak >=90%
            q=min(local,key=lambda z:abs(float(f[z])-fn))
            competitors=[z for z in local if z!=q and r["s1"][z]>=0.9*r["s1"][q]]
            if competitors:
                entries.append({"status":"NON_IDENTIFIABLE_MODAL_OVERLAP"})
                continue
            hp=half_power(f,r["s1"],q,lo,hi)
            if hp is None:
                entries.append({"status":"NO_ADMISSIBLE_SCALAR_CHI","f_peak_hz":float(f[q])})
                continue
            entries.append({"status":"ADMITTED",**hp})
        admitted=[e for e in entries if e["status"]=="ADMITTED"]
        identifiable=sum(e["status"]!="NON_IDENTIFIABLE" for e in entries)
        if len(admitted)>=16:
            families.append({
                "median_candidate_hz":fn,
                "admitted_count":len(admitted),
                "identifiable_count":identifiable,
                "median_peak_hz":float(np.median([e["f_peak_hz"] for e in admitted])),
                "median_chi":float(np.median([e["chi"] for e in admitted])),
                "entries":entries,
            })

    if not families:
        status="NO_ADMISSIBLE_PRIMARY_MODE"
        primary=None; secondary=None
    else:
        families=sorted(families,key=lambda z:z["median_peak_hz"])
        status="PRIMARY_MODE_SELECTED"
        primary=families[0]
        secondary=families[1] if len(families)>1 else None

    out={
        "schema":"d02e-healthy-baseline-selection-v0.1",
        "status":status,
        "source_pid":PID,
        "healthy_directory":"DATA/A_1/Healthy",
        "healthy_file_count":len(healthy),
        "healthy_files":healthy,
        "csv_header":baseline_header,
        "response_channels":channel_names,
        "sample_rate_hz_assumed_from_source":1600.0,
        "candidate_eligible_family_count":len(families),
        "eligible_families":families,
        "primary_family":primary,
        "secondary_family":secondary,
        "readme":readme_info,
        "guard":"Only Healthy A_1 vibration files were opened. No 9Nm, 6Nm, or NoBolt file was accessed."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":status,
        "healthy_files":len(healthy),
        "channels":len(channel_names),
        "eligible_families":len(families),
        "primary_hz":None if primary is None else primary["median_peak_hz"],
        "secondary_hz":None if secondary is None else secondary["median_peak_hz"],
    },indent=2))

if __name__=="__main__":
    main()
