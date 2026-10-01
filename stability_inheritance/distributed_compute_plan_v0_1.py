from __future__ import annotations

import argparse
import json
from pathlib import Path

REGISTRY = Path("stability_inheritance/DISTRIBUTED_COMPUTE_REGISTRY_v0.1.json")
ALLOWED_PREFIXES = ("stability_inheritance/", "cosmology_desi/")


def load_registry() -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    tasks = data.get("tasks", [])
    ids = [t.get("task_id") for t in tasks]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Duplicate distributed task_id detected")
    return data


def safe_script(path_text: str) -> str:
    if not path_text or ".." in Path(path_text).parts:
        raise RuntimeError(f"Unsafe script path: {path_text!r}")
    if not path_text.startswith(ALLOWED_PREFIXES):
        raise RuntimeError(f"Script outside allowed research roots: {path_text}")
    p = Path(path_text)
    if not p.is_file():
        raise RuntimeError(f"Checked-in task script not found: {path_text}")
    return path_text


def build_matrix(data: dict) -> dict:
    include = []
    occupied = set()
    for task in data.get("tasks", []):
        if task.get("status") != "READY":
            continue
        if not str(task.get("executor", "")).startswith("GITHUB_HOSTED"):
            continue
        executor = str(task.get("executor", ""))
        if executor in occupied:
            raise RuntimeError(f"Multiple READY tasks assigned to the same GitHub slot: {executor}")
        occupied.add(executor)
        script = safe_script(task.get("script", ""))
        include.append(
            {
                "task_id": task["task_id"],
                "script": script,
                "resource_class": task.get("resource_class", "MEDIUM"),
                "executor": executor,
            }
        )
    if not include:
        include = [{"task_id": "NOOP", "script": "", "resource_class": "LIGHT"}]
    return {"include": include}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--github-output")
    args = ap.parse_args()

    matrix = build_matrix(load_registry())
    encoded = json.dumps(matrix, separators=(",", ":"))
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as fh:
            fh.write(f"matrix={encoded}\n")
    else:
        print(encoded)


if __name__ == "__main__":
    main()
