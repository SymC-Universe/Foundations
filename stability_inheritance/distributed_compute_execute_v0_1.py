from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

REGISTRY = Path("stability_inheritance/DISTRIBUTED_COMPUTE_REGISTRY_v0.1.json")
STATE_ROOT = Path("stability_inheritance/results/distributed")


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_task(task_id: str) -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    matches = [t for t in data.get("tasks", []) if t.get("task_id") == task_id]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one task {task_id}, found {len(matches)}")
    task = matches[0]
    if task.get("status") != "READY":
        raise RuntimeError(f"Task {task_id} is not READY")
    if not str(task.get("executor", "")).startswith("GITHUB_HOSTED"):
        raise RuntimeError(f"Task {task_id} is not assigned to GitHub-hosted execution")
    return task


def validate_path(path_text: str) -> Path:
    p = Path(path_text)
    if not path_text or ".." in p.parts:
        raise RuntimeError(f"Unsafe task script path: {path_text!r}")
    if not (path_text.startswith("stability_inheritance/") or path_text.startswith("cosmology_desi/")):
        raise RuntimeError(f"Task script outside allowed research roots: {path_text}")
    if not p.is_file():
        raise RuntimeError(f"Task script missing: {path_text}")
    return p


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task-id", required=True)
    args = ap.parse_args()

    task = load_task(args.task_id)
    script = validate_path(task["script"])
    task_root = STATE_ROOT / args.task_id
    output_dir = task_root / "output"
    checkpoint_dir = task_root / "checkpoint"
    output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    start = {
        "task_id": args.task_id,
        "state": "ACTIVE_COMPUTE",
        "started_at": utcnow(),
        "script": str(script),
        "script_sha256": sha256_file(script),
        "protocol": task.get("protocol"),
        "scientific_lane": task.get("scientific_lane"),
        "evidence_class": task.get("evidence_class"),
        "executor": task.get("executor"),
        "resource_class": task.get("resource_class"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "github_sha": os.environ.get("GITHUB_SHA"),
    }
    write_json(task_root / "runner_manifest_start.json", start)

    env = os.environ.copy()
    env["SI_DISTRIBUTED_TASK_ID"] = args.task_id
    env["SI_DISTRIBUTED_OUTPUT_DIR"] = str(output_dir.resolve())
    env["SI_DISTRIBUTED_CHECKPOINT_DIR"] = str(checkpoint_dir.resolve())

    proc = subprocess.run([sys.executable, str(script)], env=env)
    final = {
        **start,
        "state": "COMPLETE" if proc.returncode == 0 else "MECHANICAL_BLOCK",
        "completed_at": utcnow(),
        "return_code": proc.returncode,
    }
    write_json(task_root / "runner_manifest_final.json", final)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
