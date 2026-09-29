#!/usr/bin/env python3
import json, re, urllib.request
from pathlib import Path

OUT=Path("stability_inheritance/results/rivet_mendeley_metadata_structure")
OUT.mkdir(parents=True,exist_ok=True)

DATASETS={
  "small":"https://data.mendeley.com/api/datasets/sgmxhdc599",
  "large":"https://data.mendeley.com/api/datasets/dy66vm8t95"
}
KEY_HINTS=("file","name","id","url","href","download","content","mime","size","checksum","hash","uuid")
VALUE_HINTS=("data.h5","structure_images")

def get_json(url):
    req=urllib.request.Request(url,headers={"User-Agent":"SymC-Stability-Inheritance-Metadata-Audit/1.0","Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=45) as r:
        return json.loads(r.read().decode("utf-8"))

def walk(obj,path="",out=None):
    if out is None:
        out=[]
    if isinstance(obj,dict):
        for k,v in obj.items():
            p=f"{path}.{k}" if path else str(k)
            kl=str(k).lower()
            if any(h in kl for h in KEY_HINTS):
                if isinstance(v,(str,int,float,bool)) or v is None:
                    sv=v
                    if isinstance(sv,str) and len(sv)>500:
                        sv=sv[:500]
                    out.append({"path":p,"value":sv})
                elif isinstance(v,(list,dict)):
                    out.append({"path":p,"value_type":type(v).__name__,"length":len(v)})
            walk(v,p,out)
    elif isinstance(obj,list):
        for i,v in enumerate(obj):
            walk(v,f"{path}[{i}]",out)
    elif isinstance(obj,str):
        low=obj.lower()
        if any(h in low for h in VALUE_HINTS):
            sv=obj if len(obj)<=1000 else obj[:1000]
            out.append({"path":path,"value":sv,"matched_value_hint":True})
    return out

result={"status":"PUBLIC_METADATA_STRUCTURE_ONLY","datasets":{}}
for key,url in DATASETS.items():
    try:
        data=get_json(url)
        hits=walk(data)
        text_blob=json.dumps(data)
        has_data=("data.h5" in text_blob.lower())
        has_id_url=any(
            isinstance(x.get("value"),(str,int)) and any(h in x["path"].lower() for h in ("id","url","href","download","uuid"))
            for x in hits
        )
        if has_data and has_id_url:
            disp="FILE_DESCRIPTOR_DISCOVERED"
        elif has_data:
            disp="FILE_NAME_ONLY"
        else:
            disp="METADATA_STRUCTURE_INSUFFICIENT"
        result["datasets"][key]={
          "endpoint":url,
          "top_level_keys":list(data.keys()) if isinstance(data,dict) else None,
          "hits":hits,
          "contains_data_h5":has_data,
          "disposition":disp
        }
    except Exception as e:
        result["datasets"][key]={"endpoint":url,"disposition":"METADATA_STRUCTURE_INSUFFICIENT","exception_type":type(e).__name__,"exception":str(e)}

disps=[v["disposition"] for v in result["datasets"].values()]
if "FILE_DESCRIPTOR_DISCOVERED" in disps:
    result["disposition"]="FILE_DESCRIPTOR_DISCOVERED"
elif "FILE_NAME_ONLY" in disps:
    result["disposition"]="FILE_NAME_ONLY"
else:
    result["disposition"]="METADATA_STRUCTURE_INSUFFICIENT"

(OUT/"result.json").write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
