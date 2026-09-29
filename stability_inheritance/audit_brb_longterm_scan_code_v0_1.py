#!/usr/bin/env python3
import hashlib, json, re, urllib.request
from pathlib import Path

OUT=Path("stability_inheritance/results/brb_longterm_scan_code_audit")
OUT.mkdir(parents=True,exist_ok=True)
FILES={
 "scan_a_rawdat2meshsort.m":"https://osf.io/download/65802b3e8ed0a61c869f9828/",
 "scan_b_visdata.m":"https://osf.io/download/65802b414a0e901eaf8e9185/",
 "scan_c_elemaspID.m":"https://osf.io/download/65802b428e942d1df8a0f0e0/"
}
TERMS=[
 "csv","read","load","save","outlier","nan","median","mean","std","rms","skew","kurt",
 "asper","peak","max","min","area","volume","height","mesh","element","sort","patch",
 "plane","detrend","filter","smooth","interp","hist","rough","contact","segment"
]
result={"status":"P0Q_SOURCE_CODE_ONLY","raw_scan_data_accessed":False,"files":{}}
ok=True
for name,url in FILES.items():
    rec={"url":url}
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"SymC-Stability-Inheritance-Scan-Audit/1.0"})
        with urllib.request.urlopen(req,timeout=60) as r:
            b=r.read()
        rec["sha256"]=hashlib.sha256(b).hexdigest()
        rec["size_bytes"]=len(b)
        txt=b.decode("utf-8","replace")
        lines=txt.splitlines()
        hits=[]
        for i,line in enumerate(lines,1):
            low=line.lower()
            if any(t in low for t in TERMS):
                hits.append({"line":i,"text":line[:500]})
        rec["line_count"]=len(lines)
        rec["semantic_hits"]=hits
        rec["save_targets"]=sorted(set(re.findall(r"save\s*\(\s*['\"]([^'\"]+)",txt,re.I)))
        rec["load_targets"]=sorted(set(re.findall(r"load\s*\(\s*['\"]([^'\"]+)",txt,re.I)))
    except Exception as e:
        ok=False; rec["exception_type"]=type(e).__name__; rec["exception"]=str(e)
    result["files"][name]=rec

if not ok:
    disp="SCAN_SOURCE_AUDIT_BLOCKED"
else:
    a=result["files"]["scan_a_rawdat2meshsort.m"].get("semantic_hits",[])
    c=result["files"]["scan_c_elemaspID.m"].get("semantic_hits",[])
    texta="\n".join(x["text"].lower() for x in a)
    textc="\n".join(x["text"].lower() for x in c)
    sufficient=(("mesh" in texta or "element" in texta or "sort" in texta) and
                ("asper" in textc or "peak" in textc or "height" in textc))
    disp="SCAN_NATIVE_PROCESSING_ROUTE_IDENTIFIED" if sufficient else "SCAN_NATIVE_PROCESSING_ROUTE_INCOMPLETE"
result["disposition"]=disp
(OUT/"result.json").write_text(json.dumps(result,indent=2))
print(json.dumps({
 "disposition":disp,
 "files":{k:{"sha256":v.get("sha256"),"size_bytes":v.get("size_bytes"),"line_count":v.get("line_count"),"semantic_hit_count":len(v.get("semantic_hits",[])),"exception":v.get("exception")} for k,v in result["files"].items()}
},indent=2))
