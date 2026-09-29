#!/usr/bin/env python3
import json, re, struct, urllib.request
from pathlib import Path

OUT=Path("stability_inheritance/results/brb_longterm_shaker_zip_index")
OUT.mkdir(parents=True,exist_ok=True)
ARCHIVES=[
 {"round":"FirstRound_16Dec2020","url":"https://osf.io/download/p5trv/","size":4620032365},
 {"round":"SecondRound_17Dec2020","url":"https://osf.io/download/rkg4b/","size":1228105544},
 {"round":"ThirdRound_18Dec2020","url":"https://osf.io/download/4r8ku/","size":2703467720},
]
UA={"User-Agent":"SymC-Stability-Inheritance-ZipIndex/1.0","Accept":"application/octet-stream"}

def range_get(url,start,end=None):
    val=f"bytes={start}-" if end is None else f"bytes={start}-{end}"
    req=urllib.request.Request(url,headers={**UA,"Range":val})
    with urllib.request.urlopen(req,timeout=120) as r:
        status=getattr(r,"status",None)
        headers=dict(r.headers.items())
        if status!=206:
            return status,headers,b""
        return status,headers,r.read()

def total_from_probe(url):
    status,h,b=range_get(url,0,0)
    if status!=206:
        return None,status,h
    cr=h.get("Content-Range") or h.get("content-range")
    m=re.match(r"bytes\s+\d+-\d+/(\d+)",cr or "")
    return (int(m.group(1)) if m else None),status,h

def parse_cd_location(url,total):
    tail_start=max(0,total-131072)
    status,h,tail=range_get(url,tail_start,total-1)
    if status!=206: raise RuntimeError("range tail unavailable")
    sig=b"PK\x05\x06"
    i=tail.rfind(sig)
    if i<0: raise RuntimeError("EOCD not found")
    eocd=tail[i:i+22]
    if len(eocd)<22: raise RuntimeError("short EOCD")
    vals=struct.unpack("<4s4H2IH",eocd)
    _,disk,cd_disk,n_disk,n_total,cd_size32,cd_off32,comment_len=vals
    zip64=(n_total==0xffff or cd_size32==0xffffffff or cd_off32==0xffffffff)
    if not zip64:
        return int(cd_off32),int(cd_size32),int(n_total),False
    loc_sig=b"PK\x06\x07"
    j=tail.rfind(loc_sig,0,i)
    if j<0: raise RuntimeError("ZIP64 locator not found")
    loc=tail[j:j+20]
    _,disk_with,zip64_off,total_disks=struct.unpack("<4sIQI",loc)
    status,h,z=range_get(url,zip64_off,zip64_off+55)
    if status!=206 or len(z)<56: raise RuntimeError("ZIP64 EOCD unavailable")
    vals=struct.unpack("<4sQHHIIQQQQ",z[:56])
    sig64,rec_size,vmade,vneed,diskno,cdstart,n_disk64,n_total64,cd_size64,cd_off64=vals
    if sig64!=b"PK\x06\x06": raise RuntimeError("bad ZIP64 EOCD signature")
    return int(cd_off64),int(cd_size64),int(n_total64),True

def parse_central(data):
    rows=[]; pos=0
    while pos+46<=len(data):
        if data[pos:pos+4]!=b"PK\x01\x02":
            nxt=data.find(b"PK\x01\x02",pos+1)
            if nxt<0: break
            pos=nxt
        fixed=data[pos:pos+46]
        vals=struct.unpack("<4s6H3I5H2I",fixed)
        name_len,extra_len,comment_len=vals[10],vals[11],vals[12]
        comp_size,uncomp_size=vals[8],vals[9]
        name_b=data[pos+46:pos+46+name_len]
        try: name=name_b.decode("utf-8")
        except UnicodeDecodeError: name=name_b.decode("cp437","replace")
        rows.append({"name":name,"compressed_size_32":comp_size,"uncompressed_size_32":uncomp_size})
        pos += 46+name_len+extra_len+comment_len
    return rows

def classify_name(name):
    low=name.lower()
    if "randfrf_before" in low: return "RandFRF_Before"
    if "randfrf_after" in low: return "RandFRF_After"
    if "stepsine_before" in low: return "StepSine_Before"
    if "stepsine_after" in low: return "StepSine_After"
    if "singfreq" in low: return "SingFreqTest"
    return "Other"

def parse_v_idx(name):
    base=name.rsplit("/",1)[-1]
    mv=re.search(r"_V([0-9]+(?:\.[0-9]+)?)_",base,re.I)
    mi=re.search(r"(?:randfrf|stepsine|singfreq)(\d+)",base,re.I)
    return (float(mv.group(1)) if mv else None),(int(mi.group(1)) if mi else None)

result={"status":"P0Q_METADATA_ONLY","entry_bodies_accessed":False,"archives":{}}
qualified=0
identity_changed=False
range_blocked=False
for a in ARCHIVES:
    rec={"round":a["round"],"url":a["url"],"expected_size":a["size"]}
    try:
        total,status,h=total_from_probe(a["url"])
        rec["range_probe_status"]=status
        rec["observed_size"]=total
        if total is None:
            rec["disposition"]="RANGE_ACCESS_NOT_AVAILABLE"; range_blocked=True
        elif total!=a["size"]:
            rec["disposition"]="SHAKER_ZIP_IDENTITY_CHANGED"; identity_changed=True
        else:
            cd_off,cd_size,n_total,zip64=parse_cd_location(a["url"],total)
            rec.update({"zip64":zip64,"central_directory_offset":cd_off,"central_directory_size":cd_size,"central_directory_entries_declared":n_total})
            st,hh,cd=range_get(a["url"],cd_off,cd_off+cd_size-1)
            if st!=206 or len(cd)!=cd_size: raise RuntimeError(f"central directory range failed status={st} len={len(cd)} expected={cd_size}")
            rows=parse_central(cd)
            rec["entries_parsed"]=len(rows)
            groups={}
            for row in rows:
                kind=classify_name(row["name"])
                v,idx=parse_v_idx(row["name"])
                groups.setdefault(kind,[]).append({"name":row["name"],"voltage":v,"index":idx})
            summary={}
            for k,items in groups.items():
                volts=sorted({x["voltage"] for x in items if x["voltage"] is not None})
                idxs=[x["index"] for x in items if x["index"] is not None]
                summary[k]={"count":len(items),"voltages":volts,"index_min":min(idxs) if idxs else None,"index_max":max(idxs) if idxs else None}
            rec["group_summary"]=summary
            rec["entries"]=rows
            rec["disposition"]="SHAKER_ZIP_INDEX_QUALIFIED"; qualified+=1
    except Exception as e:
        rec["disposition"]="SHAKER_ZIP_INDEX_PARTIAL"
        rec["exception_type"]=type(e).__name__; rec["exception"]=str(e)
    result["archives"][a["round"]]=rec

if identity_changed:
    result["disposition"]="SHAKER_ZIP_IDENTITY_CHANGED"
elif range_blocked and qualified==0:
    result["disposition"]="RANGE_ACCESS_NOT_AVAILABLE"
elif qualified==len(ARCHIVES):
    result["disposition"]="SHAKER_ZIP_INDEX_QUALIFIED"
else:
    result["disposition"]="SHAKER_ZIP_INDEX_PARTIAL"

(OUT/"result.json").write_text(json.dumps(result,indent=2))
small={"disposition":result["disposition"],"entry_bodies_accessed":False,"archives":{}}
for k,v in result["archives"].items():
    small["archives"][k]={x:v.get(x) for x in ["disposition","expected_size","observed_size","zip64","entries_parsed","group_summary","exception_type","exception"]}
print(json.dumps(small,indent=2))
