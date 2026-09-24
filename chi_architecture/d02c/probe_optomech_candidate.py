from __future__ import annotations
import hashlib, json, requests
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"D02C_CANDIDATE_OPTOMECH_SCHEMA_v0.1.json"
ARTICLE_ID=28795412
API=f"https://api.figshare.com/v2/articles/{ARTICLE_ID}"
HEADERS={"User-Agent":"SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}

def sha256_bytes(data: bytes)->str:
    h=hashlib.sha256(); h.update(data); return h.hexdigest()

def main():
    r=requests.get(API,headers=HEADERS,timeout=120)
    r.raise_for_status()
    meta=r.json()
    files=[]
    for f in meta.get("files",[]):
        files.append({
            "id":f.get("id"),
            "name":f.get("name"),
            "size":f.get("size"),
            "download_url":f.get("download_url"),
            "supplied_md5":f.get("supplied_md5"),
            "computed_md5":f.get("computed_md5"),
            "mimetype":f.get("mimetype"),
        })
    result={
        "schema":"d02c-optomech-candidate-schema-v0.1",
        "status":"CANDIDATE_METADATA_ONLY_NO_DECISIVE_OUTCOME_INSPECTION",
        "article_id":ARTICLE_ID,
        "title":meta.get("title"),
        "doi":meta.get("doi"),
        "description":meta.get("description"),
        "files":files,
        "file_count":len(files),
        "guard":"Metadata and file manifest only; no scientific file contents opened.",
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"title":result["title"],"file_count":result["file_count"],"output":str(OUT)},indent=2))
if __name__=="__main__": main()
