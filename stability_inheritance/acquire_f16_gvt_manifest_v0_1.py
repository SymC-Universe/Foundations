#!/usr/bin/env python3
import hashlib, json, urllib.request, zipfile
from pathlib import Path

URL="https://data.4tu.nl/file/b6dc643b-ecc6-437c-8a8a-1681650ec3fe/5414dfdc-6e8d-4208-be6e-fa553de9866f"
EXPECTED_SIZE=148455295
OUT=Path("stability_inheritance/results/f16_gvt_intake")
OUT.mkdir(parents=True,exist_ok=True)
raw=OUT/"F16GVT_Files.zip"

result={
  "status":"P0Q_EXTERNAL_MEASURED_INTAKE_ONLY",
  "source_url":URL,
  "expected_size_bytes":EXPECTED_SIZE,
  "raw_values_scored":False
}

try:
    req=urllib.request.Request(URL,headers={"User-Agent":"SymC-Stability-Inheritance-P0Q/1.0"})
    with urllib.request.urlopen(req,timeout=120) as resp, raw.open("wb") as f:
        result["final_url"]=resp.geturl()
        result["http_status"]=getattr(resp,"status",None)
        while True:
            chunk=resp.read(1024*1024)
            if not chunk:
                break
            f.write(chunk)
except Exception as e:
    result.update({"disposition":"INTAKE_BLOCKED_SOURCE","exception_type":type(e).__name__,"exception":str(e)})
    (OUT/"manifest.json").write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
    raise SystemExit(0)

b=raw.read_bytes()
result["size_bytes"]=len(b)
result["sha256"]=hashlib.sha256(b).hexdigest()

try:
    with zipfile.ZipFile(raw,"r") as z:
        bad=z.testzip()
        result["zip_test_bad_member"]=bad
        members=[]
        counts={"benchmark_data":0,"validation":0,"special_odd_msine":0,"other_benchmark":0}
        for info in z.infolist():
            name=info.filename
            rec={"name":name,"size":info.file_size,"compressed_size":info.compress_size,"crc":info.CRC}
            members.append(rec)
            if "F16GVT_Files/BenchmarkData/" in name and not name.endswith("/"):
                counts["benchmark_data"]+=1
                low=name.lower()
                if "validation" in low:
                    counts["validation"]+=1
                elif "specialoddmsine" in low:
                    counts["special_odd_msine"]+=1
                else:
                    counts["other_benchmark"]+=1
        result["member_count"]=len(members)
        result["benchmark_counts"]=counts
        result["members"]=members
        layout_ok=counts["benchmark_data"]>0
        size_ok=(len(b)==EXPECTED_SIZE)
        if bad is not None:
            result["disposition"]="INVALID_ARCHIVE"
        elif size_ok and layout_ok:
            result["disposition"]="INTAKE_PASS"
        else:
            result["disposition"]="INTAKE_IDENTITY_CHANGED"
except zipfile.BadZipFile as e:
    result.update({"disposition":"INVALID_ARCHIVE","exception_type":type(e).__name__,"exception":str(e)})

(OUT/"manifest.json").write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!="members"},indent=2))
raw.unlink(missing_ok=True)
