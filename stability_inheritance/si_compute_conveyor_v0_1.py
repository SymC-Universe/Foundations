#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "stability_inheritance" / "COMPUTE_CONVEYOR_QUEUE_v0.1.json"
STATE = ROOT / "stability_inheritance" / "CONTINUITY_STATE.json"
OUT = ROOT / "stability_inheritance" / "results" / "compute_conveyor"
OUT.mkdir(parents=True, exist_ok=True)

RUN_ID = os.environ.get("GITHUB_RUN_ID")
RUN_ATTEMPT = os.environ.get("GITHUB_RUN_ATTEMPT")
GITHUB_SHA = os.environ.get("GITHUB_SHA")
GITHUB_REF_NAME = os.environ.get("GITHUB_REF_NAME", "stability-inheritance")

def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def sha256_path(path):
    p = ROOT / path
    if not p.exists() or not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_disposition(path, key="disposition"):
    p = ROOT / path
    if not p.exists():
        return None
    try:
        obj = json.loads(p.read_text())
        cur = obj
        for part in key.split("."):
            if not isinstance(cur, dict) or part not in cur:
                return None
            cur = cur[part]
        return cur
    except Exception:
        return None

def checkpoint_identity(task, disposition):
    identity = {
        "task_id": task.get("id"),
        "protocol": task.get("protocol") or task.get("parent_protocol"),
        "protocol_sha256": sha256_path(task.get("protocol") or task.get("parent_protocol") or ""),
        "script": task.get("script"),
        "script_sha256": sha256_path(task.get("script") or ""),
        "result_json": task.get("result_json"),
        "result_sha256": sha256_path(task.get("result_json") or ""),
        "disposition": disposition,
        "source_identity": task.get("scientific_identity"),
        "protected_boundary": task.get("protected_boundary") or task.get("numeric_response_access") or task.get("member_body_access"),
        "branch": GITHUB_REF_NAME,
        "execution_commit": GITHUB_SHA,
        "workflow_run_id": int(RUN_ID) if RUN_ID and RUN_ID.isdigit() else RUN_ID,
        "workflow_run_attempt": int(RUN_ATTEMPT) if RUN_ATTEMPT and RUN_ATTEMPT.isdigit() else RUN_ATTEMPT,
    }
    return identity

queue = json.loads(QUEUE.read_text())
report = {
    "queue_version": queue.get("version"),
    "started_unix": time.time(),
    "started_at": utc_now(),
    "execution_commit": GITHUB_SHA,
    "workflow_run_id": int(RUN_ID) if RUN_ID and RUN_ID.isdigit() else RUN_ID,
    "tasks": [],
    "final_state": "COMPLETE_NO_READY_TASKS",
}

executed = None
for task in queue.get("tasks", []):
    if task.get("status") != "READY":
        report["tasks"].append({"id": task.get("id"), "queue_status": task.get("status"), "action": "SKIP"})
        continue

    executed = task
    task["status"] = "ACTIVE"
    task["active_run_id"] = int(RUN_ID) if RUN_ID and RUN_ID.isdigit() else RUN_ID
    task["active_execution_commit"] = GITHUB_SHA
    task["started_at"] = utc_now()

    cmd = [sys.executable, str(ROOT / task["script"])]
    started = time.time()
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    disposition = read_disposition(task.get("result_json", ""), task.get("disposition_key", "disposition"))
    item = {
        "id": task["id"],
        "queue_status": "READY",
        "action": "EXECUTED",
        "returncode": proc.returncode,
        "duration_s": time.time() - started,
        "disposition": disposition,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
    }
    report["tasks"].append(item)

    task["last_run_id"] = int(RUN_ID) if RUN_ID and RUN_ID.isdigit() else RUN_ID
    task["last_execution_commit"] = GITHUB_SHA
    task["last_disposition"] = disposition
    task["completed_at"] = utc_now()
    task["result_sha256"] = sha256_path(task.get("result_json", ""))
    task["checkpoint_identity"] = checkpoint_identity(task, disposition)
    task.pop("active_run_id", None)
    task.pop("active_execution_commit", None)

    if proc.returncode != 0:
        task["status"] = "COMPLETE_MECHANICAL_FAILURE"
        report["final_state"] = "STOP_MECHANICAL_FAILURE"
        report["stopped_at"] = task["id"]
        break

    allowed = task.get("continue_on_dispositions")
    if allowed is not None and disposition not in allowed:
        task["status"] = "COMPLETE_UNLISTED_DISPOSITION"
        report["final_state"] = "STOP_SCIENTIFIC_GATE"
        report["stopped_at"] = task["id"]
        report["gate_disposition"] = disposition
        break

    task["status"] = "COMPLETE_EXECUTED"
    if task.get("stop_after", False):
        report["final_state"] = "STOP_DECLARED_CHECKPOINT"
        report["stopped_at"] = task["id"]
        break

    report["final_state"] = "COMPLETE_READY_TASKS"

report["finished_unix"] = time.time()
report["finished_at"] = utc_now()
(OUT / "run_summary.json").write_text(json.dumps(report, indent=2))

# Durable queue reconciliation is mechanical provenance only.
QUEUE.write_text(json.dumps(queue, indent=2) + "\n")

ready = [t for t in queue.get("tasks", []) if t.get("status") == "READY"]
last_task = executed.get("id") if executed else None
last_checkpoint = executed.get("checkpoint_identity") if executed else None

prior_state = {}
if STATE.exists():
    try:
        prior_state = json.loads(STATE.read_text())
    except Exception:
        prior_state = {}

permitted_states = {"ACTIVE_COMPUTE", "ADVANCED_CHECKPOINT", "SCIENTIFIC_GATE", "EXTERNAL_BLOCK", "USER_ACTION_REQUIRED"}

if executed and executed.get("continuity_state_on_allowed_completion") in permitted_states and report["final_state"] == "STOP_DECLARED_CHECKPOINT":
    continuity_state = executed.get("continuity_state_on_allowed_completion")
elif report["final_state"] == "STOP_SCIENTIFIC_GATE":
    continuity_state = "SCIENTIFIC_GATE"
elif report["final_state"] == "STOP_MECHANICAL_FAILURE":
    continuity_state = "ADVANCED_CHECKPOINT"
elif not executed and prior_state.get("continuity_state") in permitted_states:
    # A no-op/support workflow must not erase a legitimate active or stopped state or reset liveness.
    continuity_state = prior_state.get("continuity_state")
else:
    continuity_state = "ADVANCED_CHECKPOINT"

next_action = None
if ready:
    next_action = f"Execute READY queue task {ready[0].get('id')}."
elif executed:
    next_action = executed.get("next_authorized_action")
if not next_action:
    next_action = queue.get("next_authorized_action") or "Reconcile completed checkpoint against WORKING_INVESTIGATION.md and determine the next already-authorized action without creating new scientific authority."

blocker = None
boundary_type = "MECHANICAL_EXECUTION"
if continuity_state == "SCIENTIFIC_GATE":
    if executed and executed.get("scientific_gate_on_completion"):
        blocker = executed.get("scientific_gate_on_completion")
    elif report["final_state"] == "STOP_SCIENTIFIC_GATE":
        blocker = f"Unlisted disposition at {last_task}: {report.get('gate_disposition')}"
    else:
        blocker = prior_state.get("scientific_gate")
    boundary_type = "NEW_SCIENTIFIC_DECISION"

state = {
    "schema_version": "1.0",
    "governance": {
        "gom": "SymC General Operations Manual v1.0",
        "continuity_extension": "Mandatory Continuity Hardening Addendum",
        "binding": "stability_inheritance/SI_CONTINUITY_HARDENING_BINDING_v1.0.md",
    },
    "branch": GITHUB_REF_NAME,
    "scientific_lane": queue.get("scientific_lane", "STABILITY_INHERITANCE"),
    "authorized_stage": last_task or queue.get("authorized_stage"),
    "continuity_state": continuity_state,
    "last_completed_durable_checkpoint": last_checkpoint or prior_state.get("last_completed_durable_checkpoint"),
    "active_workflow_or_computation_id": None,
    "last_workflow_run_id": int(RUN_ID) if RUN_ID and RUN_ID.isdigit() else RUN_ID,
    "last_execution_commit": GITHUB_SHA,
    "next_exact_authorized_action": next_action,
    "execution_ceiling": queue.get("execution_ceiling"),
    "scientific_gate": blocker if continuity_state == "SCIENTIFIC_GATE" else None,
    "external_block": prior_state.get("external_block") if continuity_state == "EXTERNAL_BLOCK" else None,
    "user_action_required": prior_state.get("user_action_required") if continuity_state == "USER_ACTION_REQUIRED" else None,
    "last_productive_advancement": report["finished_at"] if executed else prior_state.get("last_productive_advancement") or queue.get("last_productive_advancement"),
    "liveness_clock": {
        "lane": queue.get("scientific_lane", "STABILITY_INHERITANCE"),
        "reset_only_by_authoritative_lane_advancement": True,
        "default_stagnation_threshold_minutes": 90,
        "last_reset": report["finished_at"] if executed else (prior_state.get("liveness_clock") or {}).get("last_reset") or queue.get("last_productive_advancement"),
        "support_or_monitoring_activity_does_not_reset": True,
    },
    "duplicate_suppression": {
        "rule": "Suppress a completed computation only when scientific input/configuration identity is proven unchanged.",
        "current_checkpoint_identity": last_checkpoint or (prior_state.get("duplicate_suppression") or {}).get("current_checkpoint_identity"),
    },
    "protected_inputs": queue.get("protected_inputs", []),
    "five_question_test": {
        "what_scientific_lane_are_we_advancing": queue.get("scientific_lane", "STABILITY_INHERITANCE"),
        "what_is_actually_running_or_just_completed": f"Completed durable checkpoint {last_task} in workflow {RUN_ID}." if executed else prior_state.get("five_question_test", {}).get("what_is_actually_running_or_just_completed", "No substantive task executed in this workflow."),
        "what_is_the_next_already_authorized_action": next_action,
        "what_prevents_that_action_immediately": blocker if blocker is not None else prior_state.get("five_question_test", {}).get("what_prevents_that_action_immediately"),
        "does_crossing_the_boundary_require_mechanical_execution_or_new_scientific_decision": boundary_type if executed or continuity_state == "SCIENTIFIC_GATE" else prior_state.get("five_question_test", {}).get("does_crossing_the_boundary_require_mechanical_execution_or_new_scientific_decision", boundary_type),
    },
}

STATE.write_text(json.dumps(state, indent=2) + "\n")
print(json.dumps(report, indent=2))
if report["final_state"] == "STOP_MECHANICAL_FAILURE":
    raise SystemExit(2)
