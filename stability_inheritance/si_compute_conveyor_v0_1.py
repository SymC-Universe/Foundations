#!/usr/bin/env python3
import json, subprocess, sys, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"stability_inheritance"/"COMPUTE_CONVEYOR_QUEUE_v0.1.json"
OUT=ROOT/"stability_inheritance"/"results"/"compute_conveyor"
OUT.mkdir(parents=True,exist_ok=True)

def read_disposition(path,key="disposition"):
    p=ROOT/path
    if not p.exists():
        return None
    try:
        obj=json.loads(p.read_text())
        cur=obj
        for part in key.split("."):
            if not isinstance(cur,dict) or part not in cur:
                return None
            cur=cur[part]
        return cur
    except Exception:
        return None

queue=json.loads(QUEUE.read_text())
report={
    "queue_version":queue.get("version"),
    "started_unix":time.time(),
    "tasks":[],
    "final_state":"COMPLETE_NO_READY_TASKS"
}

for task in queue.get("tasks",[]):
    if task.get("status")!="READY":
        report["tasks"].append({"id":task.get("id"),"queue_status":task.get("status"),"action":"SKIP"})
        continue
    cmd=[sys.executable,str(ROOT/task["script"])]
    started=time.time()
    proc=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    disposition=read_disposition(task.get("result_json",""),task.get("disposition_key","disposition"))
    item={
      "id":task["id"],"queue_status":"READY","action":"EXECUTED",
      "returncode":proc.returncode,"duration_s":time.time()-started,
      "disposition":disposition,
      "stdout_tail":proc.stdout[-4000:],
      "stderr_tail":proc.stderr[-4000:]
    }
    report["tasks"].append(item)
    if proc.returncode!=0:
        report["final_state"]="STOP_MECHANICAL_FAILURE"
        report["stopped_at"]=task["id"]
        break
    allowed=task.get("continue_on_dispositions")
    if allowed is not None and disposition not in allowed:
        report["final_state"]="STOP_SCIENTIFIC_GATE"
        report["stopped_at"]=task["id"]
        report["gate_disposition"]=disposition
        break
    if task.get("stop_after",False):
        report["final_state"]="STOP_DECLARED_CHECKPOINT"
        report["stopped_at"]=task["id"]
        break
    report["final_state"]="COMPLETE_READY_TASKS"

report["finished_unix"]=time.time()
(OUT/"run_summary.json").write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if report["final_state"]=="STOP_MECHANICAL_FAILURE":
    raise SystemExit(2)
