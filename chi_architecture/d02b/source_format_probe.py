from __future__ import annotations
import io, json, zipfile
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"D02B_SOURCE_FORMAT_PROBE_v0.1.json"
BASE="https://zenodo.org/records/20038951/files/"
HEADERS={"User-Agent":"SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}

TARGETS={
 "01_documentation.zip":["01_documentation/raw_export_format.md","01_documentation/README.md"],
 "04_scripts.zip":["04_scripts/_common.py","04_scripts/01_build_processed_tables.py","04_scripts/README.md"],
}

def fetch(name):
 r=requests.get(BASE+name+"?download=1",headers=HEADERS,timeout=180)
 r.raise_for_status()
 return r.content

def main():
 out={"schema":"d02b-source-format-probe-v0.1","files":{}}
 for archive,paths in TARGETS.items():
  z=zipfile.ZipFile(io.BytesIO(fetch(archive)))
  for p in paths:
   txt=z.read(p).decode("utf-8",errors="replace")
   out["files"][p]=txt
 OUT.parent.mkdir(parents=True,exist_ok=True)
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 print("wrote",OUT)

if __name__=="__main__":
 main()
