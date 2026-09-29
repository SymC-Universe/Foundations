#!/usr/bin/env python3
import csv, io, json, math, re, struct, urllib.request, urllib.error, zlib, binascii, time
from pathlib import Path
import numpy as np

OUT=Path("stability_inheritance/results/brb_longterm_sampling_audit")
OUT.mkdir(parents=True,exist_ok=True)
ARCH={
 "First":{"url":"https://osf.io/download/p5trv/","size":4620032365},
 "Second":{"url":"https://osf.io/download/rkg4b/","size":1228105544},
 "Third":{"url":"https://osf.io/download/4r8ku/","size":2703467720},
}
STATES={
 "S0":{"archive":"First","prefix":"RandFRF_Before/"},
 "S1":{"archive":"First","prefix":"RandFRF_After/"},
 "S2":{"archive":"Second","prefix":"RandFRF_After/"},
 "S3":{"archive":"Third","prefix":"RandFRF_Before/"},
 "S4":{"archive":"Third","prefix":"RandFRF_After/"},
}
VOLTAGES=[0.01,0.1,1.0]
UA={"User-Agent":"SymC-Stability-Inheritance-BRB-Sampling-Audit/1.0","Accept":"application/octet-stream"}

def _open_range(url, range_header, attempts=5):
    last=None
    for attempt in range(1,attempts+1):
        req=urllib.request.Request(url,headers={**UA,"Range":range_header})
        try:
            return urllib.request.urlopen(req,timeout=120)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            last=e
            code=getattr(e,"code",None)
            if code is not None and code not in (429,500,502,503,504):
                raise
            if attempt==attempts:
                raise
            time.sleep(min(2**(attempt-1),8))
    raise last

def rg(url,start,end):
    with _open_range(url,f"bytes={start}-{end}") as r:
        if getattr(r,"status",None)!=206:
            raise RuntimeError(f"range unsupported status={getattr(r,'status',None)}")
        return r.read()

def probe_total(url):
    with _open_range(url,"bytes=0-0") as r:
        cr=r.headers.get("Content-Range")
        m=re.match(r"bytes\s+\d+-\d+/(\d+)",cr or "")
        if getattr(r,"status",None)!=206 or not m:
            raise RuntimeError("range probe failed")
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
        nl,xl,cl=vals[10],vals[11],vals[12]; lo32=vals[16]
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
    off=e["local_offset"]; hdr=rg(url,off,off+29)
    vals=struct.unpack("<4s5H3I2H",hdr)
    if vals[0]!=b"PK\x03\x04": raise RuntimeError("bad local header")
    nl,xl=vals[9],vals[10]; start=off+30+nl+xl
    comp=rg(url,start,start+e["compressed_size"]-1)
    if e["method"]==0: raw=comp
    elif e["method"]==8: raw=zlib.decompress(comp,-15)
    else: raise RuntimeError(f"unsupported compression method {e['method']}")
    if len(raw)!=e["uncompressed_size"] or (binascii.crc32(raw)&0xffffffff)!=e["crc"]:
        raise RuntimeError("entry integrity mismatch")
    return raw

def clean(x):
    return str(x).lstrip("".join(chr(i) for i in range(32))).strip()

def fnum(x):
    try: return float(clean(x))
    except: return math.nan

indexes={}
for k,a in ARCH.items():
    total=probe_total(a["url"])
    if total!=a["size"]: raise RuntimeError(f"{k} archive identity changed {total} != {a['size']}")
    indexes[k]=central_entries(a["url"],total)

records=[]
for s,sp in STATES.items():
    idx=indexes[sp["archive"]]; url=ARCH[sp["archive"]]["url"]
    for v in VOLTAGES:
        matches=[]
        for name,e in idx.items():
            if not name.lower().startswith(sp["prefix"].lower()) or not name.lower().endswith(".csv"): continue
            m=re.search(r"_V([0-9]+(?:\.[0-9]+)?)_randfrf(\d+)\.csv$",name,re.I)
            if not m: continue
            if abs(float(m.group(1))-v)<1e-12 and 0<=int(m.group(2))<=9:
                matches.append((int(m.group(2)),name,e))
        matches=sorted(matches)
        if [x[0] for x in matches]!=list(range(10)):
            raise RuntimeError(f"{s} voltage {v} missing realization indices")
        for ii,name,e in matches:
            raw=extract_entry(url,e)
            txt=raw.decode("utf-8-sig","replace")
            reader=csv.reader(io.StringIO(txt))
            row1=next(reader); row2=next(reader)
            names=[clean(x) for x in row1]
            dts=[fnum(x) for x in row2]
            if names.count("F1")!=1:
                raise RuntimeError(f"{name}: force F1 not unique")
            accel=["A1","X1","Y1","Z1","X2","Y2","Z2"]
            if any(names.count(x)!=1 for x in accel):
                raise RuntimeError(f"{name}: accel mapping incomplete")
            sel=[names.index("F1")]+[names.index(x) for x in accel]
            vals=[dts[i] if i<len(dts) else math.nan for i in sel]
            within=all(np.isfinite(x) and x>0 for x in vals) and (max(vals)-min(vals)<=max(1e-12,1e-9*max(vals)))
            line_count=raw.count(b"\n")
            approx_samples=max(0,line_count-2)
            records.append({
              "state":s,"voltage":v,"index":ii,"name":name,
              "uncompressed_bytes":e["uncompressed_size"],
              "selected_dt":vals[0] if within else None,
              "selected_dt_values":vals,
              "within_file_timing_consistent":within,
              "approx_samples":approx_samples,
              "selected_channels":["F1"]+accel
            })

if any(not r["within_file_timing_consistent"] for r in records):
    disp="WITHIN_FILE_TIMING_INVALID"
else:
    uniq=sorted(set(round(r["selected_dt"],15) for r in records))
    if not uniq:
        disp="SAMPLING_GRID_AMBIGUOUS"
    else:
        disp="SAMPLING_GRID_MAPPING_QUALIFIED"

uniq=sorted(set(r["selected_dt"] for r in records if r["selected_dt"] is not None))
counts={}
for r in records:
    key=f"{r['selected_dt']:.15g}" if r["selected_dt"] else "None"
    counts.setdefault(key,{"total":0,"states":{},"sample_min":None,"sample_max":None})
    x=counts[key]; x["total"]+=1; x["states"][r["state"]]=x["states"].get(r["state"],0)+1
    n=r["approx_samples"]; x["sample_min"]=n if x["sample_min"] is None else min(x["sample_min"],n); x["sample_max"]=n if x["sample_max"] is None else max(x["sample_max"],n)

ratios=[]
if uniq:
    base=max(uniq)
    for dt in uniq:
        ratios.append({"dt":dt,"ratio_to_largest_dt":dt/base,"inverse_rate_ratio_to_largest_dt":base/dt})

out={
 "status":"P0Q_SCHEMA_AUDIT_ONLY",
 "protocol":"BRB_LONGTERM_SAMPLING_GRID_AUDIT_v0.1",
 "record_count":len(records),
 "unique_dt":uniq,
 "dt_groups":counts,
 "dt_ratios":ratios,
 "records":records,
 "signal_statistics_computed":False,
 "disposition":disp
}
(OUT/"result.json").write_text(json.dumps(out,indent=2))
print(json.dumps({k:out[k] for k in ["record_count","unique_dt","dt_groups","dt_ratios","signal_statistics_computed","disposition"]},indent=2))
