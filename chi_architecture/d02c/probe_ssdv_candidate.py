from __future__ import annotations

import hashlib, json, re, zipfile
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/"results"/"d02c_candidate_probe_ssdv"
ARCHIVE=CACHE/"Zenodo_dataset.zip"
OUT=ROOT/"results"/"D02C_CANDIDATE_SSDV_SCHEMA_v0.1.json"
URL="https://zenodo.org/records/18595556/files/Zenodo_dataset.zip?download=1"
EXPECTED_MD5="c4c38cc41034648c74b90f167c3aa153"
HEADERS={"User-Agent":"SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}

def digest(path,alg):
    h=hashlib.new(alg)
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(4*1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def download():
    CACHE.mkdir(parents=True,exist_ok=True)
    if ARCHIVE.exists() and digest(ARCHIVE,"md5")==EXPECTED_MD5: return
    with requests.get(URL,headers=HEADERS,stream=True,timeout=600) as r:
        r.raise_for_status()
        with ARCHIVE.open("wb") as f:
            for chunk in r.iter_content(chunk_size=4*1024*1024):
                if chunk: f.write(chunk)

def text_schema(data,name):
    text=None
    for enc in ("utf-8-sig","utf-8","cp1252","latin1"):
        try:
            text=data.decode(enc); break
        except UnicodeDecodeError: pass
    if text is None: return {"path":name,"text_probe":"UNDECODABLE"}
    lines=text.splitlines()
    meta=[]
    for line in lines[:120]:
        s=line.strip()
        if s and re.search(r"[A-Za-z]",s):
            meta.append(s[:240])
        if len(meta)>=30: break
    return {"path":name,"line_count":len(lines),"header_like_lines_only":meta}

def main():
    download()
    md5=digest(ARCHIVE,"md5")
    if md5!=EXPECTED_MD5: raise RuntimeError("MD5 mismatch")
    files=[]
    with zipfile.ZipFile(ARCHIVE) as z:
        for info in z.infolist():
            if info.is_dir(): continue
            item={"path":info.filename,"size_bytes":info.file_size,"extension":Path(info.filename).suffix.lower()}
            if info.file_size<=1_500_000 and item["extension"] in {".txt",".csv",".dat",".md",".m",".py"}:
                item["text_schema"]=text_schema(z.read(info.filename),info.filename)
            files.append(item)
    result={
      "schema":"d02c-ssdv-candidate-schema-v0.1",
      "status":"CANDIDATE_STRUCTURE_ONLY_NO_DECISIVE_RESULT_INTERPRETATION",
      "source":{"url":URL,"md5":md5,"sha256":digest(ARCHIVE,"sha256"),"size_bytes":ARCHIVE.stat().st_size},
      "file_count":len(files),"files":files,
      "guard":"File paths and small text headers only; no outcome-direction summary."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"file_count":len(files),"output":str(OUT)},indent=2))
if __name__=="__main__": main()
