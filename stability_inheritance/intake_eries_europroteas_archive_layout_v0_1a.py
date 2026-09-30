#!/usr/bin/env python3
import json, struct, urllib.parse, urllib.request
from pathlib import Path

OUT=Path("stability_inheritance/results/eries_europroteas_archive_layout_v0_1a")
OUT.mkdir(parents=True,exist_ok=True)
RECORDS={"RESPOND":"15518567","POLIS":"15575887"}
MAX_CD_BYTES=30*1024*1024

def get_json(url):
    req=urllib.request.Request(url,headers={"User-Agent":"SymC-ERIES-Archive-Layout/1.0a","Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))

def official_download_url(record_id,key):
    return f"https://zenodo.org/records/{record_id}/files/{urllib.parse.quote(key)}?download=1"

def range_get(url,start=None,end=None,suffix=None):
    headers={"User-Agent":"SymC-ERIES-Archive-Layout/1.0a","Accept":"*/*","Accept-Encoding":"identity"}
    if suffix is not None:
        headers["Range"]=f"bytes=-{suffix}"
    elif start is not None:
        headers["Range"]=f"bytes={start}-{'' if end is None else end}"
    req=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req,timeout=90) as r:
        data=r.read()
        return data,r.status,dict(r.headers)

def parse_eocd(tail):
    sig=b"PK\x05\x06"
    i=tail.rfind(sig)
    if i<0 or len(tail)-i<22:
        raise ValueError("EOCD_NOT_FOUND")
    vals=struct.unpack_from("<4s4H2IH",tail,i)
    _,disk,disk_cd,n_disk,n_total,cd_size,cd_off,comment_len=vals
    out={"entries":n_total,"cd_size":cd_size,"cd_offset":cd_off,"zip64":False}
    if n_total==0xffff or cd_size==0xffffffff or cd_off==0xffffffff:
        locsig=b"PK\x06\x07"
        li=tail.rfind(locsig,0,i)
        if li<0 or len(tail)-li<20:
            raise ValueError("ZIP64_LOCATOR_NOT_FOUND")
        _,disk_eocd,zip64_off,total_disks=struct.unpack_from("<4sIQI",tail,li)
        out.update({"zip64":True,"zip64_eocd_offset":zip64_off,"zip64_disk":disk_eocd,"total_disks":total_disks})
    return out

def parse_zip64_eocd(data):
    if len(data)<56 or data[:4]!=b"PK\x06\x06":
        raise ValueError("ZIP64_EOCD_INVALID")
    vals=struct.unpack_from("<4sQ2H2I4Q",data,0)
    return {"entries":vals[8],"cd_size":vals[9],"cd_offset":vals[10]}

def parse_cd(data,max_entries=200000):
    rows=[]; pos=0; sig=b"PK\x01\x02"
    while pos+46<=len(data) and len(rows)<max_entries:
        if data[pos:pos+4]!=sig:
            nxt=data.find(sig,pos+1)
            if nxt<0: break
            pos=nxt
        vals=struct.unpack_from("<4s6H3I5H2I",data,pos)
        comp_size=vals[8]; uncomp_size=vals[9]
        fname_len=vals[10]; extra_len=vals[11]; comment_len=vals[12]
        base=pos+46; end=base+fname_len+extra_len+comment_len
        if end>len(data): break
        name=data[base:base+fname_len].decode("utf-8","replace")
        rows.append({"path":name,"compressed_size":comp_size,"uncompressed_size":uncomp_size,"is_dir":name.endswith("/")})
        pos=end
    return rows

def classify(paths):
    txt="\n".join(p.lower() for p in paths)
    return {
      "foundation":any(x in txt for x in ["foundation","pile cap","pilecap","pile_group","pile group"]),
      "pile_or_substructure":any(x in txt for x in ["pile","substructure","group"]),
      "structure_or_europroteas":any(x in txt for x in ["europroteas","structure","roof"]),
      "roof":"roof" in txt,
      "soil":"soil" in txt,
      "forced":any(x in txt for x in ["forced","sweep","harmonic","shaker"]),
      "free_or_pullout":any(x in txt for x in ["free","pull","pullout","pull-out"]),
      "instrumentation_or_layout":any(x in txt for x in ["instrument","layout","drawing","sensor","channel","readme","info"])
    }

result={"status":"ZIP_CENTRAL_DIRECTORY_ONLY_NO_MEMBER_BODIES","repair_class":"MECHANICAL_TRANSPORT_ONLY","numeric_response_opened":False,"archives":{}}

for label,rid in RECORDS.items():
    rec={"record_id":rid}
    try:
        obj=get_json(f"https://zenodo.org/api/records/{rid}")
        files=obj.get("files") or []
        zips=[f for f in files if str(f.get("key") or "").lower().endswith(".zip")]
        if len(zips)!=1:
            raise ValueError(f"EXPECTED_ONE_ZIP_GOT_{len(zips)}")
        z=zips[0]
        key=z.get("key")
        url=official_download_url(rid,key)
        rec.update({"zip_key":key,"zip_size":z.get("size"),"checksum":z.get("checksum"),"download_route":"official_record_file_download"})
        tail,status,hdr=range_get(url,suffix=131072)
        rec["tail_http_status"]=status; rec["tail_bytes"]=len(tail); rec["content_range"]=hdr.get("Content-Range")
        if status!=206:
            raise ValueError(f"RANGE_NOT_HONORED_STATUS_{status}")
        eocd=parse_eocd(tail)
        if eocd.get("zip64"):
            z64,status2,h2=range_get(url,start=eocd["zip64_eocd_offset"],end=eocd["zip64_eocd_offset"]+55)
            if status2!=206: raise ValueError(f"ZIP64_RANGE_NOT_HONORED_STATUS_{status2}")
            eocd.update(parse_zip64_eocd(z64))
        rec["central_directory"]={k:eocd[k] for k in ("entries","cd_size","cd_offset","zip64")}
        if eocd["cd_size"]>MAX_CD_BYTES:
            raise ValueError(f"CENTRAL_DIRECTORY_TOO_LARGE_{eocd['cd_size']}")
        cd,status3,h3=range_get(url,start=eocd["cd_offset"],end=eocd["cd_offset"]+eocd["cd_size"]-1)
        if status3!=206: raise ValueError(f"CENTRAL_DIRECTORY_RANGE_NOT_HONORED_STATUS_{status3}")
        members=parse_cd(cd)
        rec["member_count_parsed"]=len(members)
        rec["members"]=members
        rec["layout_hints"]=classify([m["path"] for m in members])
        rec["indexed"]=len(members)>0
    except Exception as e:
        rec.update({"indexed":False,"exception_type":type(e).__name__,"exception":str(e)})
    result["archives"][label]=rec

r=result["archives"]; resp=r.get("RESPOND",{}); pol=r.get("POLIS",{})
resp_h=resp.get("layout_hints") or {}; pol_h=pol.get("layout_hints") or {}
resp_hierarchy=resp.get("indexed") and resp_h.get("foundation") and resp_h.get("structure_or_europroteas")
pol_structure=pol.get("indexed") and pol_h.get("structure_or_europroteas")
forced_both=resp_h.get("forced") and pol_h.get("forced")
if resp.get("indexed") and pol.get("indexed") and resp_hierarchy and pol_structure and forced_both:
    disposition="ERIES_ARCHIVE_LAYOUT_QUALIFIED"
elif resp.get("indexed") or pol.get("indexed"):
    disposition="ERIES_ARCHIVE_LAYOUT_PARTIAL" if (resp_hierarchy or pol_structure) else "ERIES_ARCHIVE_LAYOUT_INSUFFICIENT"
else:
    disposition="ERIES_ARCHIVE_INDEX_ROUTE_UNAVAILABLE"

result["disposition"]=disposition
result["qualification"]={
  "respond_hierarchy_path_hints":bool(resp_hierarchy),
  "polis_structure_path_hints":bool(pol_structure),
  "forced_family_hints_both":bool(forced_both),
  "polis_free_or_pullout_hint":bool(pol_h.get("free_or_pullout")),
  "numeric_response_opened":False
}
(OUT/"result.json").write_text(json.dumps(result,indent=2))
print(json.dumps({
  "disposition":disposition,
  "qualification":result["qualification"],
  "archives":{k:{"indexed":v.get("indexed"),"zip_key":v.get("zip_key"),"zip_size":v.get("zip_size"),"member_count_parsed":v.get("member_count_parsed"),"central_directory":v.get("central_directory"),"layout_hints":v.get("layout_hints"),"exception":v.get("exception")} for k,v in r.items()}
},indent=2))
