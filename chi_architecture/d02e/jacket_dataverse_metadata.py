from __future__ import annotations
import json
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"D02E_JACKET_DATAVERSE_METADATA_v0.1.json"
SERVER="https://dataverse.csuc.cat"
PID="doi:10.34810/data1011"
HEADERS={"User-Agent":"SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}

def main():
    url=f"{SERVER}/api/datasets/:persistentId/"
    r=requests.get(url,params={"persistentId":PID},headers=HEADERS,timeout=180)
    r.raise_for_status()
    payload=r.json()
    if payload.get("status")!="OK":
        raise RuntimeError("Dataverse metadata request did not return OK")
    latest=payload["data"]["latestVersion"]
    files=latest.get("files",[])
    rows=[]
    for item in files:
        df=item["dataFile"]
        fm=item["label"]
        rows.append({
            "id":df["id"],
            "filename":fm,
            "directoryLabel":item.get("directoryLabel",""),
            "filesize":df.get("filesize"),
            "contentType":df.get("contentType"),
            "restricted":df.get("restricted",False),
            "md5":df.get("md5"),
        })
    rows=sorted(rows,key=lambda x:(x["directoryLabel"],x["filename"]))
    counts={}
    for row in rows:
        d=row["directoryLabel"]
        counts[d]=counts.get(d,0)+1
    out={
        "schema":"d02e-jacket-dataverse-metadata-v0.1",
        "status":"METADATA_ONLY_NO_VIBRATION_VALUES_INSPECTED",
        "server":SERVER,
        "persistent_id":PID,
        "dataset_version":latest.get("versionNumber"),
        "file_count":len(rows),
        "directory_counts":counts,
        "files":rows,
        "guard":"Only Dataverse metadata were retrieved. No CSV vibration file was opened."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":out["status"],"file_count":len(rows),"directory_count":len(counts)},indent=2))

if __name__=="__main__":
    main()
