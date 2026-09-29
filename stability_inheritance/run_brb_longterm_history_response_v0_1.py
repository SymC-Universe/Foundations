#!/usr/bin/env python3
import csv, hashlib, io, json, math, os, re, struct, tempfile, urllib.request, zlib, binascii
from pathlib import Path
import numpy as np

OUT=Path("stability_inheritance/results/brb_longterm_history_response")
OUT.mkdir(parents=True,exist_ok=True)

ARCH={
 "First":{"url":"https://osf.io/download/p5trv/","size":4620032365},
 "Second":{"url":"https://osf.io/download/rkg4b/","size":1228105544},
 "Third":{"url":"https://osf.io/download/4r8ku/","size":2703467720},
}
STATES={
 "S0":{"archive":"First","prefix":"RandFRF_Before/","history":"initial_before"},
 "S1":{"archive":"First","prefix":"RandFRF_After/","history":"after_4h"},
 "S2":{"archive":"Second","prefix":"RandFRF_After/","history":"after_8h"},
 "S3":{"archive":"Third","prefix":"RandFRF_Before/","history":"after_reassembly_before_final4h"},
 "S4":{"archive":"Third","prefix":"RandFRF_After/","history":"after_final4h"},
}
VOLTAGES=[0.01,0.1,1.0]
FIT={0,2,4,6,8}
TEST={1,3,5,7,9}
UA={"User-Agent":"SymC-Stability-Inheritance-BRB-History/1.0","Accept":"application/octet-stream"}

def rg(url,start,end):
    req=urllib.request.Request(url,headers={**UA,"Range":f"bytes={start}-{end}"})
    with urllib.request.urlopen(req,timeout=120) as r:
        if getattr(r,"status",None)!=206:
            raise RuntimeError(f"range unsupported status={getattr(r,'status',None)}")
        return r.read()

def probe_total(url):
    req=urllib.request.Request(url,headers={**UA,"Range":"bytes=0-0"})
    with urllib.request.urlopen(req,timeout=120) as r:
        if getattr(r,"status",None)!=206:
            raise RuntimeError("range probe failed")
        cr=r.headers.get("Content-Range")
        m=re.match(r"bytes\s+\d+-\d+/(\d+)",cr or "")
        if not m: raise RuntimeError("missing content-range")
        return int(m.group(1))

def cd_location(url,total):
    start=max(0,total-131072); tail=rg(url,start,total-1)
    i=tail.rfind(b"PK\x05\x06")
    if i<0: raise RuntimeError("EOCD not found")
    vals=struct.unpack("<4s4H2IH",tail[i:i+22])
    n_total,cd_size,cd_off=vals[4],vals[5],vals[6]
    if n_total!=0xffff and cd_size!=0xffffffff and cd_off!=0xffffffff:
        return int(cd_off),int(cd_size)
    j=tail.rfind(b"PK\x06\x07",0,i)
    if j<0: raise RuntimeError("ZIP64 locator missing")
    _,_,zoff,_=struct.unpack("<4sIQI",tail[j:j+20])
    z=rg(url,zoff,zoff+55)
    vals=struct.unpack("<4sQHHIIQQQQ",z[:56])
    return int(vals[9]),int(vals[8])

def zip64_fields(extra,need_u,need_c,need_o):
    u=c=o=None; pos=0
    while pos+4<=len(extra):
        hid,ln=struct.unpack("<HH",extra[pos:pos+4]); dat=extra[pos+4:pos+4+ln]; pos+=4+ln
        if hid!=0x0001: continue
        q=0
        if need_u: u=struct.unpack("<Q",dat[q:q+8])[0]; q+=8
        if need_c: c=struct.unpack("<Q",dat[q:q+8])[0]; q+=8
        if need_o: o=struct.unpack("<Q",dat[q:q+8])[0]; q+=8
        break
    return u,c,o

def central_entries(url,total):
    off,size=cd_location(url,total); data=rg(url,off,off+size-1)
    rows={}; pos=0
    while pos+46<=len(data):
        if data[pos:pos+4]!=b"PK\x01\x02":
            nxt=data.find(b"PK\x01\x02",pos+1)
            if nxt<0: break
            pos=nxt
        vals=struct.unpack("<4s6H3I5H2I",data[pos:pos+46])
        flag,method,crc,cs32,us32=vals[3],vals[4],vals[7],vals[8],vals[9]
        nl,xl,cl=vals[10],vals[11],vals[12]
        lo32=vals[16]
        nb=data[pos+46:pos+46+nl]; extra=data[pos+46+nl:pos+46+nl+xl]
        name=nb.decode("utf-8","replace")
        need_u=us32==0xffffffff; need_c=cs32==0xffffffff; need_o=lo32==0xffffffff
        u64,c64,o64=zip64_fields(extra,need_u,need_c,need_o)
        rows[name]={
          "name":name,"flag":flag,"method":method,"crc":crc,
          "compressed_size":int(c64 if need_c else cs32),
          "uncompressed_size":int(u64 if need_u else us32),
          "local_offset":int(o64 if need_o else lo32)
        }
        pos += 46+nl+xl+cl
    return rows

def extract_entry(url,e):
    if e["flag"] & 1: raise RuntimeError("encrypted zip entry")
    off=e["local_offset"]
    hdr=rg(url,off,off+29)
    vals=struct.unpack("<4s5H3I2H",hdr)
    if vals[0]!=b"PK\x03\x04": raise RuntimeError("bad local header")
    nl,xl=vals[9],vals[10]
    start=off+30+nl+xl
    comp=rg(url,start,start+e["compressed_size"]-1)
    if e["method"]==0: raw=comp
    elif e["method"]==8: raw=zlib.decompress(comp,-15)
    else: raise RuntimeError(f"unsupported compression method {e['method']}")
    if len(raw)!=e["uncompressed_size"]: raise RuntimeError("uncompressed size mismatch")
    if (binascii.crc32(raw)&0xffffffff)!=e["crc"]: raise RuntimeError("CRC mismatch")
    return raw

def parse_float(x):
    try: return float(str(x).strip())
    except: return math.nan

def parse_csv_bytes(raw):
    sha=hashlib.sha256(raw).hexdigest()
    text=raw.decode("utf-8-sig","replace")
    rows=list(csv.reader(io.StringIO(text)))
    rows=[r for r in rows if any(str(x).strip() for x in r)]
    if len(rows)<5: raise RuntimeError("too few CSV rows")
    names=[str(x).strip() for x in rows[0]]
    dt=[parse_float(x) for x in rows[1]]
    ncol=len(names)
    if len(dt)<ncol: dt += [math.nan]*(ncol-len(dt))
    data=[]
    for r in rows[2:]:
        if len(r)<ncol: continue
        vals=[parse_float(r[j]) for j in range(ncol)]
        if all(np.isfinite(vals)): data.append(vals)
    a=np.asarray(data,float)
    if a.ndim!=2 or a.shape[0]<256: raise RuntimeError(f"insufficient numeric samples {a.shape}")
    force_candidates=[i for i,n in enumerate(names) if "force" in n.lower()]
    if len(force_candidates)!=1: raise RuntimeError(f"force channel mapping ambiguous {force_candidates} names={names}")
    fi=force_candidates[0]
    accel_candidates=[i for i,n in enumerate(names) if ("accel" in n.lower() or "acceleration" in n.lower())]
    if len(accel_candidates)!=7:
        pos=list(range(4,min(11,ncol)))
        if len(pos)==7 and all(("acc" in names[i].lower()) for i in pos):
            accel_candidates=pos
        else:
            raise RuntimeError(f"acceleration mapping not seven channels: {accel_candidates} names={names}")
    sel=[fi]+accel_candidates
    dvals=[dt[i] for i in sel]
    if not all(np.isfinite(x) and x>0 for x in dvals): raise RuntimeError(f"invalid selected sampling intervals {dvals}")
    if max(dvals)-min(dvals) > max(1e-12,1e-9*max(dvals)): raise RuntimeError(f"selected channel sampling mismatch {dvals}")
    return {
      "sha256":sha,"names":names,"force_idx":fi,"accel_idx":accel_candidates,"dt":dvals[0],
      "force":a[:,fi],"accel":a[:,accel_candidates],"n":a.shape[0]
    }

# Build remote central indexes and freeze selected files by structural name only.
indexes={}
for k,a in ARCH.items():
    total=probe_total(a["url"])
    if total!=a["size"]: raise RuntimeError(f"{k} archive identity changed {total} != {a['size']}")
    indexes[k]=central_entries(a["url"],total)

selection={}
for s,sp in STATES.items():
    idx=indexes[sp["archive"]]
    selection[s]={}
    for v in VOLTAGES:
        matches=[]
        for name,e in idx.items():
            if not name.lower().startswith(sp["prefix"].lower()) or not name.lower().endswith(".csv"): continue
            m=re.search(r"_V([0-9]+(?:\.[0-9]+)?)_randfrf(\d+)\.csv$",name,re.I)
            if not m: continue
            vv=float(m.group(1)); ii=int(m.group(2))
            if abs(vv-v)<1e-12 and 0<=ii<=9: matches.append((ii,name,e))
        matches=sorted(matches)
        if [x[0] for x in matches] != list(range(10)):
            raise RuntimeError(f"{s} voltage {v} does not have indices 0-9: {[x[0] for x in matches]}")
        selection[s][str(v)]=matches

# Selective extraction. Raw bodies remain ephemeral and are not uploaded.
records={}
manifest=[]
n_common=None; dt_common=None; output_names=None
for s,byv in selection.items():
    records[s]={}
    url=ARCH[STATES[s]["archive"]]["url"]
    for vs,matches in byv.items():
        records[s][vs]={}
        for ii,name,e in matches:
            parsed=parse_csv_bytes(extract_entry(url,e))
            if n_common is None or parsed["n"]<n_common: n_common=parsed["n"]
            if dt_common is None: dt_common=parsed["dt"]
            elif abs(parsed["dt"]-dt_common)>max(1e-12,1e-9*dt_common): raise RuntimeError(f"cross-file dt mismatch {parsed['dt']} vs {dt_common}")
            names=[parsed["names"][j] for j in parsed["accel_idx"]]
            if output_names is None: output_names=names
            elif names!=output_names: raise RuntimeError(f"accel channel names/order changed {names} vs {output_names}")
            records[s][vs][ii]=parsed
            manifest.append({"state":s,"voltage":float(vs),"index":ii,"name":name,"sha256":parsed["sha256"],"samples":parsed["n"]})

if n_common is None: raise RuntimeError("no records")
fs=1.0/dt_common
win=np.hanning(n_common)
freq=np.fft.rfftfreq(n_common,d=dt_common)

def fft_record(rec):
    f=(rec["force"][:n_common]-np.mean(rec["force"][:n_common]))*win
    y=rec["accel"][:n_common,:]-np.mean(rec["accel"][:n_common,:],axis=0,keepdims=True)
    y=y*win[:,None]
    F=np.fft.rfft(f)
    Y=np.fft.rfft(y,axis=0)
    return F,Y,float(np.sqrt(np.mean(rec["force"][:n_common]**2)))

# Cache FFTs.
FFTs={}; force_rms={}
for s in STATES:
    FFTs[s]={}; force_rms[s]={}
    for vs in records[s]:
        FFTs[s][vs]={}; force_rms[s][vs]={}
        for ii,rec in records[s][vs].items():
            F,Y,rms=fft_record(rec)
            FFTs[s][vs][ii]=(F,Y); force_rms[s][vs][ii]=rms

# Fit-only support.
fit_energy=np.zeros(freq.size)
for s in STATES:
  for vs in records[s]:
    for ii in FIT:
      F,_=FFTs[s][vs][ii]; fit_energy += np.abs(F)**2
band=(freq>=140.0)&(freq<=200.0)&(freq>0)
if not np.any(band): raise RuntimeError("no 140-200 Hz bins")
mx=float(np.max(fit_energy[band]))
support=band & (fit_energy>1e-12*mx)
if int(support.sum())<10: raise RuntimeError(f"insufficient support {int(support.sum())}")

def H_from_members(members):
    num=None; den=None
    for s,vs,ii in members:
        F,Y=FFTs[s][vs][ii]
        n=Y*np.conj(F)[:,None]; d=np.abs(F)**2
        num=n if num is None else num+n
        den=d if den is None else den+d
    return num/np.maximum(den[:,None],np.finfo(float).tiny)

Hfit={}; Htest={}; input_psd_fit={}; input_rms_med={}
for s in STATES:
    Hfit[s]={}; Htest[s]={}; input_psd_fit[s]={}; input_rms_med[s]={}
    for vs in records[s]:
        Hfit[s][vs]=H_from_members([(s,vs,i) for i in sorted(FIT)])
        Htest[s][vs]=H_from_members([(s,vs,i) for i in sorted(TEST)])
        input_psd_fit[s][vs]=np.mean([np.abs(FFTs[s][vs][i][0])**2 for i in sorted(FIT)],axis=0)
        input_rms_med[s][vs]={
          "fit":float(np.median([force_rms[s][vs][i] for i in FIT])),
          "test":float(np.median([force_rms[s][vs][i] for i in TEST]))
        }

def err(pred,target):
    a=pred[support,:]; b=target[support,:]
    den=np.sum(np.abs(b)**2)
    return float(np.sqrt(np.sum(np.abs(a-b)**2)/den)) if den>np.finfo(float).tiny else math.nan

def concat_err(pairs):
    num=den=0.0
    for pred,target in pairs:
        a=pred[support,:]; b=target[support,:]
        num+=float(np.sum(np.abs(a-b)**2)); den+=float(np.sum(np.abs(b)**2))
    return float(np.sqrt(num/den)) if den>np.finfo(float).tiny else math.nan

# LOSO same-voltage representation.
Hloso={}
for target_s in STATES:
    Hloso[target_s]={}
    for vs in records[target_s]:
        members=[]
        for s in STATES:
            if s==target_s: continue
            members += [(s,vs,i) for i in sorted(FIT)]
        Hloso[target_s][vs]=H_from_members(members)

# Input-only spectrum matcher.
input_match={}
Hmatch={}
for ts in STATES:
    Hmatch[ts]={}; input_match[ts]={}
    for vs in records[ts]:
        targ=input_psd_fit[ts][vs][support]
        targ=np.log(np.maximum(targ/np.sum(targ),1e-300))
        best=None
        for cs in STATES:
            if cs==ts: continue
            for cvs in records[cs]:
                cand=input_psd_fit[cs][cvs][support]
                cand=np.log(np.maximum(cand/np.sum(cand),1e-300))
                d=float(np.linalg.norm(targ-cand))
                key=(d,cs,float(cvs))
                if best is None or key<best[0]:
                    best=(key,cs,cvs)
        _,cs,cvs=best
        Hmatch[ts][vs]=Hfit[cs][cvs]
        input_match[ts][vs]={"state":cs,"voltage":float(cvs),"log_spectrum_distance":best[0][0]}

self_pairs=[]; loso_pairs=[]; match_pairs=[]
detail={}
for s in STATES:
    detail[s]={}
    for vs in records[s]:
        target=Htest[s][vs]
        e_self=err(Hfit[s][vs],target); e_loso=err(Hloso[s][vs],target); e_match=err(Hmatch[s][vs],target)
        detail[s][vs]={"E_SELF":e_self,"E_LOSO":e_loso,"E_INPUTMATCH":e_match,"input_match":input_match[s][vs],"force_rms":input_rms_med[s][vs]}
        self_pairs.append((Hfit[s][vs],target)); loso_pairs.append((Hloso[s][vs],target)); match_pairs.append((Hmatch[s][vs],target))

E_self_all=concat_err(self_pairs); E_loso_all=concat_err(loso_pairs); E_match_all=concat_err(match_pairs)
R_loso=E_self_all/E_loso_all; R_input=E_self_all/E_match_all

transitions=[("S0","S1","T01"),("S1","S2","T12"),("S2","S3","T23"),("S3","S4","T34")]
trans={}
for a,b,label in transitions:
    own=[]; prior=[]; byv={}
    for vs in records[b]:
        t=Htest[b][vs]
        es=err(Hfit[b][vs],t); ep=err(Hfit[a][vs],t)
        byv[vs]={"E_SELF":es,"E_PRIOR":ep,"ratio":es/ep if ep>0 else math.nan}
        own.append((Hfit[b][vs],t)); prior.append((Hfit[a][vs],t))
    eo=concat_err(own); ep=concat_err(prior)
    trans[label]={"from":a,"to":b,"E_SELF":eo,"E_PRIOR":ep,"ratio":eo/ep if ep>0 else math.nan,"by_voltage":byv}

def dist_state(a,b):
    num=den=0.0
    for vs in records[a]:
        A=Hfit[a][vs][support,:]; B=Hfit[b][vs][support,:]
        num+=float(np.sum(np.abs(A-B)**2)); den+=float(np.sum(np.abs(B)**2))
    return float(np.sqrt(num/den)) if den>0 else math.nan

D20=dist_state("S2","S0"); D30=dist_state("S3","S0"); D23=dist_state("S3","S2")
r23=trans["T23"]["ratio"]
if not np.isfinite(r23):
    reassembly="INDETERMINATE"
elif r23>=1:
    reassembly="REASSEMBLY_CHANGE_NOT_RESOLVED"
elif D30<D20:
    reassembly="REASSEMBLY_PARTIAL_RESET_TOWARD_INITIAL"
else:
    reassembly="REASSEMBLY_REORGANIZATION_NOT_RESET"

wear=[trans[x]["ratio"]<1 for x in ["T01","T12","T34"]]
conditions=[R_loso<1,R_input<1]+wear
if not all(np.isfinite([R_loso,R_input]+[trans[x]["ratio"] for x in ["T01","T12","T34"]])):
    disposition="INDETERMINATE"
elif all(conditions):
    disposition="HISTORY_CONDITIONED_RESPONSE_ARCHITECTURE"
elif not any(conditions):
    disposition="STATE_HISTORY_NOT_REQUIRED_FOR_DECLARED_TASK"
else:
    disposition="MIXED_HISTORY_RESPONSE_ARCHITECTURE"

# State distances from initial and response-norm peak frequencies.
state_dist={"S0":0.0}
peak_hz={}
for s in STATES:
    if s!="S0": state_dist[s]=dist_state(s,"S0")
    peak_hz[s]={}
    for vs in records[s]:
        h=Hfit[s][vs][support,:]
        norm=np.linalg.norm(h,axis=1)
        inds=np.where(support)[0]
        peak_hz[s][vs]=float(freq[inds[int(np.argmax(norm))]])

out={
 "status":"PUBLIC_EXTERNAL_P0Q",
 "protocol":"BRB_LONGTERM_HISTORY_RESPONSE_PROTOCOL_v0.1",
 "disposition":disposition,
 "reassembly_disposition":reassembly,
 "architecture_evidence_role":"ARCHITECTURE_SUPPORTING_NATIVE_HISTORY" if disposition=="HISTORY_CONDITIONED_RESPONSE_ARCHITECTURE" else "MIXED_OR_LIMIT_NATIVE_HISTORY_EVIDENCE",
 "novelty_role":"NATIVE_WEAR_TRIBOMECHADYNAMICS_SUFFICIENT_NO_SI_NOVELTY",
 "states":STATES,
 "voltages":VOLTAGES,
 "fit_indices":sorted(FIT),"test_indices":sorted(TEST),
 "sample_count_common":int(n_common),"sampling_hz":float(fs),
 "acceleration_outputs":output_names,
 "primary_band_hz":[140.0,200.0],"support_bins":int(support.sum()),
 "E_SELF_ALL":E_self_all,"E_LOSO_ALL":E_loso_all,"E_INPUTMATCH_ALL":E_match_all,
 "R_LOSO":R_loso,"R_INPUT":R_input,
 "detail":detail,"transitions":trans,
 "reassembly_distances":{"D20_S2_vs_S0":D20,"D30_S3_vs_S0":D30,"D23_S3_vs_S2":D23},
 "distance_from_initial":state_dist,
 "peak_hz":peak_hz,
 "selected_file_manifest":manifest,
 "notation":{"chi":"NOT_ADMITTED","Chi":"NOT_FORCED_FROM_GENERIC_FRF","Chi_arc":"NOT_AUTOMATICALLY_IDENTIFIED"},
 "raw_archives_committed":False
}
(OUT/"result.json").write_text(json.dumps(out,indent=2))
small={k:out[k] for k in ["disposition","reassembly_disposition","architecture_evidence_role","sampling_hz","sample_count_common","support_bins","E_SELF_ALL","E_LOSO_ALL","E_INPUTMATCH_ALL","R_LOSO","R_INPUT","transitions","reassembly_distances","distance_from_initial"]}
print(json.dumps(small,indent=2))
