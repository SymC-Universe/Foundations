from __future__ import annotations
import csv, hashlib, io, json, zipfile
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"D02C_WIND_RAW_HEADER_v0.1.json"
URL="https://zenodo.org/records/18427836/files/MO04_acceleration_20221115_130000.zip?download=1"
EXPECTED="50e32f0e7e711b89128a895d5c0c9481"
HEADERS={"User-Agent":"SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}

def main():
    r=requests.get(URL,headers=HEADERS,timeout=300)
    r.raise_for_status()
    data=r.content
    md5=hashlib.md5(data).hexdigest()
    if md5!=EXPECTED: raise RuntimeError("MD5 mismatch")
    z=zipfile.ZipFile(io.BytesIO(data))
    members=sorted([n for n in z.namelist() if n.lower().endswith(".csv")])
    raw=z.read(members[0]).decode("utf-8-sig",errors="replace")
    reader=csv.reader(io.StringIO(raw))
    header=next(reader)
    result={
      "schema":"d02c-wind-raw-header-v0.1",
      "status":"HEADER_ONLY_NO_ACCELERATION_VALUES_EMITTED",
      "source_member":members[0],
      "header":header,
      "member_count":len(members),
      "md5":md5,
      "guard":"Only the CSV header was read; no acceleration values emitted."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
