#!/usr/bin/env python3
"""Run one frozen Proofpress projection through the native Archipelago lifecycle.

The executor is Archipelago's real MCP agent: it receives a task prompt and a
read-only projection, works in a Docker-backed world, saves a snapshot, and
is scored by the benchmark's own verifier runner.  The task rubric is withheld
from the executor and is opened only after that snapshot exists.

All task text, projections, snapshots, trajectories, rubrics, and grades stay
in a caller-owned private directory.  Stdout emits a content-free receipt.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import time
import uuid
import zipfile
from typing import Any

try:
    import httpx
except ImportError:  # Unit tests do not need network I/O; native execution does.
    httpx = None

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[2]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase_c_ablation_contract import CONDITIONS, digest, project, validate_graph
from run_claim_construction_private import Gateway


SCHEMA = "proofpress/native-apex-projection-run/v1"
AGENT_TIMEOUT_SECONDS = 3600
AGENT_MAX_STEPS = 10_000
ENVIRONMENT_START_ATTEMPTS = 3
SYSTEM_PROMPT = """You are an AI assistant that completes tasks by reasoning and using tools.

Use the available MCP tools to inspect and modify the task world as needed.
Before tool calls, state a concise plan. When complete, use final_answer.
"""
SUBSYSTEMS = ("filesystem", ".apps_data")
DOCKER_BIN = Path("/Applications/Docker.app/Contents/Resources/bin/docker")


def _http() -> Any:
    if httpx is None:
        raise RuntimeError("native APEX execution requires the harness httpx dependency")
    return httpx


def _write_private(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.parent.chmod(0o700)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    path.chmod(0o600)


def _read_object(path: Path, label: str) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def _executor_task(task: dict[str, Any]) -> dict[str, str]:
    allowed = ("task_id", "prompt", "expected_output")
    if not all(isinstance(task.get(key), str) and task[key] for key in allowed):
        raise ValueError("native task requires task_id, prompt, and expected_output")
    return {key: task[key] for key in allowed}


def _rubric(task: dict[str, Any]) -> list[dict[str, Any]]:
    rubric = task.get("rubric")
    if not isinstance(rubric, list) or not rubric:
        raise ValueError("native task requires a non-empty rubric for official post-execution grading")
    if any(not isinstance(row, dict) for row in rubric):
        raise ValueError("native task rubric entries must be objects")
    return rubric


def _with_world_id(task: dict[str, Any], world_id: str | None) -> dict[str, Any]:
    """Add private harness metadata without changing executor-visible fields."""
    existing = task.get("world_id")
    if existing is not None and (not isinstance(existing, str) or not existing):
        raise ValueError("native task world_id must be a non-empty string")
    if world_id is None:
        return task
    if not isinstance(world_id, str) or not world_id:
        raise ValueError("--world-id must be a non-empty string")
    if isinstance(existing, str) and existing != world_id:
        raise ValueError("--world-id does not match native task custody")
    return {**task, "world_id": world_id}


def _projection_message(projection: dict[str, Any]) -> str:
    return (
        "The following is a read-only Proofpress working set. It contains source-bound "
        "candidates, not admitted knowledge. Preserve the stated governance boundary; "
        "use the task tools and primary materials where needed.\n\n"
        + json.dumps(projection, ensure_ascii=False, sort_keys=True)
    )


def initial_messages(task: dict[str, Any], projection: dict[str, Any]) -> list[dict[str, str]]:
    executor_task = _executor_task(task)
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": _projection_message(projection)},
        {"role": "user", "content": executor_task["prompt"]},
    ]


def _docker_command() -> str:
    if DOCKER_BIN.is_file():
        return str(DOCKER_BIN)
    found = shutil.which("docker")
    if found:
        return found
    raise RuntimeError("Docker Desktop command is required for native APEX execution")


def _run(command: list[str], *, cwd: Path, env: dict[str, str], timeout: float | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True,
                          timeout=timeout, check=False)


def _private_process_receipt(out: Path, label: str, result: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    """Keep raw runner diagnostics private while exposing only bounded metadata."""
    receipt: dict[str, Any] = {"returncode": result.returncode}
    for stream_name, raw in (("stdout", result.stdout), ("stderr", result.stderr)):
        content = raw if isinstance(raw, str) else ""
        target = out / f"{label}_{stream_name}_private.log"
        target.write_text(content, encoding="utf-8")
        target.chmod(0o600)
        receipt[f"{stream_name}_bytes"] = len(content.encode())
        receipt[f"{stream_name}_sha256"] = "sha256:" + hashlib.sha256(content.encode()).hexdigest()
    return receipt


def _start_environment(*, harness: Path, out: Path, env: dict[str, str], endpoint: str) -> dict[str, Any]:
    environment = harness / "environment"
    docker = _docker_command()
    env_file = environment / ".env"
    if not env_file.exists():
        example = environment / ".env.example"
        if example.exists():
            shutil.copy(example, env_file)
        else:
            env_file.touch()
    # The compose definition has no persistent world volume. Force-recreating
    # the container therefore gives every cell a clean world, while avoiding a
    # separate volume teardown that can remain blocked after a Docker restart.
    # The custody setup prebuilds the exact image, so a missing image must fail
    # closed instead of triggering an unbounded local rebuild.
    attempts = []
    up = None
    for attempt in range(1, ENVIRONMENT_START_ATTEMPTS + 1):
        up = _run([docker, "compose", "up", "-d", "--force-recreate", "--no-build"],
                  cwd=environment, env=env, timeout=300)
        attempts.append({"attempt": attempt,
                         **_private_process_receipt(out, f"environment_start_{attempt}", up)})
        if up.returncode == 0:
            break
        if attempt < ENVIRONMENT_START_ATTEMPTS:
            time.sleep(attempt)
    if up is None or up.returncode:
        raise RuntimeError("native APEX environment start failed")
    started = time.monotonic()
    while time.monotonic() - started < 150:
        try:
            response = _http().get(f"{endpoint}/health", timeout=5)
            if response.status_code == 200:
                return {"attempts": attempts, "health": "ok"}
        except _http().RequestError:
            pass
        time.sleep(1)
    raise RuntimeError("native APEX environment health check timed out")


def _populate(root: Path, *, out: Path, label: str, endpoint: str) -> None:
    for subsystem in SUBSYSTEMS:
        source = root / subsystem
        if not source.exists():
            continue
        paths = list(source.rglob("*"))
        if not paths:
            continue
        archive = out / f"{label}_{subsystem.replace('.', '_')}.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            tar.dereference = True
            for path in paths:
                tar.add(path, arcname=str(path.relative_to(source)), recursive=False)
        with archive.open("rb") as stream:
            response = _http().post(f"{endpoint}/data/populate",
                                    files={"archive": (archive.name, stream.read(), "application/gzip")},
                                    params={"subsystem": subsystem}, timeout=600)
        if response.status_code != 200:
            raise RuntimeError(f"native APEX {label} {subsystem} population failed")


def _official_mcp_config(harness: Path) -> dict[str, Any]:
    """Load the native harness's all-OSS tool configuration without rewriting it."""
    config = _read_object(harness / "examples/hugging_face_task/mcp_config_all_oss_servers.json",
                          "official native MCP configuration")
    servers = config.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        raise ValueError("official native MCP configuration has no servers")
    if any(not isinstance(name, str) or not isinstance(value, dict)
           for name, value in servers.items()):
        raise ValueError("official native MCP configuration is malformed")
    return config


def _configure_mcp(*, harness: Path, endpoint: str) -> dict[str, Any]:
    config = _official_mcp_config(harness)
    response = _http().post(f"{endpoint}/apps", json=config, timeout=600)
    if response.status_code != 200:
        raise RuntimeError("official native MCP configuration failed")
    return {"config_digest": digest(config), "server_count": len(config["mcpServers"])}


def _tar_gz_to_zip(path: Path) -> Path:
    target = path.with_name(path.name.removesuffix(".tar.gz") + ".zip")
    with tarfile.open(path, "r:gz") as tar, zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for member in tar.getmembers():
            if member.isfile():
                stream = tar.extractfile(member)
                if stream is not None:
                    zf.writestr(member.name, stream.read())
    return target


def _snapshot(*, out: Path, endpoint: str) -> Path:
    target = out / "final_snapshot.tar.gz"
    with _http().stream("POST", f"{endpoint}/data/snapshot", timeout=600) as response:
        response.raise_for_status()
        with target.open("wb") as stream:
            for block in response.iter_bytes(chunk_size=65536):
                stream.write(block)
    return _tar_gz_to_zip(target)


def _route_environment(base: dict[str, str], gateway: Gateway) -> dict[str, str]:
    return {**base,
            "LITELLM_PROXY_API_BASE": f"http://127.0.0.1:{gateway.port}/v1",
            "LITELLM_PROXY_API_KEY": "private-proofpress-native-bridge"}


def _agent_config(out: Path) -> Path:
    path = out / "agent_config_private.json"
    # Do not make tool-call count an experimental constraint.  The native
    # runner still has a one-hour wall-clock timeout, which is the operational
    # safety boundary; this value is deliberately far beyond what can be
    # reached within that window under normal Gateway latency.
    _write_private(path, {"agent_config_id": "react_toolbelt_agent",
                          "agent_name": "Proofpress Native Projection Agent",
                          "agent_config_values": {"timeout": AGENT_TIMEOUT_SECONDS, "max_steps": AGENT_MAX_STEPS,
                                                  "llm_response_timeout": 900}})
    return path


def _run_agent(*, harness: Path, out: Path, task: dict[str, Any], projection: dict[str, Any],
               endpoint: str, env: dict[str, str], model: str) -> tuple[dict[str, Any] | None, Path, str, dict[str, Any]]:
    messages_path = out / "initial_messages_private.json"
    _write_private(messages_path, initial_messages(task, projection))
    output = out / "trajectory_private.json"
    trajectory_id = f"proofpress_{task['task_id']}_{uuid.uuid4().hex[:8]}"
    command = ["uv", "run", "python", "-m", "runner.main",
               "--trajectory-id", trajectory_id,
               "--initial-messages", str(messages_path), "--mcp-gateway-url", f"{endpoint}/mcp/",
               "--agent-config", str(_agent_config(out)), "--orchestrator-model", model,
               "--output", str(output)]
    result = _run(command, cwd=harness / "agents", env=env, timeout=3900)
    process_receipt = _private_process_receipt(out, "agent_runner", result)
    if result.returncode or not output.exists():
        return None, output, trajectory_id, process_receipt
    value = _read_object(output, "native trajectory")
    return value, output, trajectory_id, process_receipt


def _verifiers(task: dict[str, Any]) -> list[dict[str, Any]]:
    rubric = _rubric(task)
    world_id = task.get("world_id")
    if not isinstance(world_id, str) or not world_id:
        raise ValueError("native task requires world_id for official verifiers")
    return [{"verifier_id": row["verifier_id"], "verifier_version": 1, "world_id": world_id,
             "task_id": task["task_id"], "eval_config_id": "ec_output_llm",
             "verifier_values": {"criteria": row["criteria"], "is_primary_objective": index == 0},
             "verifier_index": index, "verifier_dependencies": None}
            for index, row in enumerate(rubric)]


def _grade_config(out: Path, model: str) -> tuple[Path, Path, Path]:
    settings = out / "grading_settings_private.json"
    evaluators = out / "eval_configs_private.json"
    scoring = out / "scoring_config_private.json"
    _write_private(settings, {"llm_judge_model": model, "llm_judge_extra_args": None})
    _write_private(evaluators, [{"eval_config_id": "ec_output_llm", "eval_config_name": "Output LLM Verifier",
                                 "eval_defn_id": "output_llm", "eval_config_values": {}}])
    return settings, evaluators, scoring


def _run_grade(*, harness: Path, out: Path, task: dict[str, Any], initial_snapshot: Path,
               final_snapshot: Path, trajectory: Path, trajectory_id: str, env: dict[str, str],
               model: str) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    verifiers = out / "verifiers_private.json"
    _write_private(verifiers, _verifiers(task))
    settings, evaluators, scoring = _grade_config(out, model)
    shutil.copy(harness / "examples/hugging_face_task/scoring_config.json", scoring)
    scoring.chmod(0o600)
    target = out / "grades_private.json"
    command = ["uv", "run", "python", "-m", "runner.main", "--grading-run-id", f"proofpress_gr_{uuid.uuid4().hex[:8]}",
               "--trajectory-id", trajectory_id, "--initial-snapshot", str(initial_snapshot),
               "--final-snapshot", str(final_snapshot), "--trajectory", str(trajectory),
               "--grading-settings", str(settings), "--verifiers", str(verifiers),
               "--eval-configs", str(evaluators), "--scoring-config", str(scoring), "--output", str(target)]
    result = _run(command, cwd=harness / "grading", env=env, timeout=3900)
    process_receipt = _private_process_receipt(out, "grading_runner", result)
    if result.returncode or not target.exists():
        return None, process_receipt
    return _read_object(target, "official native grades"), process_receipt


def _telemetry(gateway: Gateway) -> dict[str, Any]:
    rows = gateway.receipt_rows()
    costs = [row.get("cost_usd") for row in rows]
    inputs = [row.get("input_tokens") for row in rows]
    outputs = [row.get("output_tokens") for row in rows]
    return {"calls": len(rows), "terminal_receipts": len(rows),
            "terminal_statuses": dict(sorted(Counter(row.get("status") for row in rows).items())),
            "known_cost_usd": round(sum(row for row in costs if isinstance(row, (int, float))), 12),
            "missing_cost_calls": sum(not isinstance(row, (int, float)) for row in costs),
            "input_tokens": sum(row for row in inputs if isinstance(row, int)),
            "output_tokens": sum(row for row in outputs if isinstance(row, int)),
            "missing_token_calls": sum(not isinstance(left, int) or not isinstance(right, int)
                                        for left, right in zip(inputs, outputs, strict=True))}


def run(*, harness: Path, task: dict[str, Any], world_root: Path, initial_snapshot: Path,
        task_overlay: Path | None, graph: dict[str, Any], condition: str, out: Path,
        bridge: Path, executor: tuple[str, str, str], grader: tuple[str, str, str], endpoint: str) -> dict[str, Any]:
    """Execute one task × projection condition with native APEX artifacts and scoring."""
    if condition not in CONDITIONS:
        raise ValueError("unknown native projection condition")
    executor_task = _executor_task(task)
    validate_graph(graph)
    if graph.get("task_id") != executor_task["task_id"]:
        raise ValueError("frozen task graph does not match native task")
    if not harness.is_dir() or not world_root.is_dir() or not initial_snapshot.is_file() or not bridge.is_file():
        raise ValueError("native APEX harness, world, snapshot, and bridge must be readable")
    if out.exists() and any(out.iterdir()):
        raise ValueError("native APEX output directory must be fresh")
    out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    projection = project(graph, condition)
    _write_private(out / "projection_private.json", projection)
    receipt_dir = out / "terminal-receipts"; receipt_dir.mkdir(); receipt_dir.chmod(0o700)
    # The sidecars, not the Archipelago child processes, hold the Gateway key.
    # The children receive only a loopback OpenAI-compatible endpoint.
    sidecar_out = out / "sidecars"; sidecar_out.mkdir(); sidecar_out.chmod(0o700)
    executor_gateway = Gateway(str(bridge), executor[0], executor[1], sidecar_out, 900, executor[2],
                               durable_receipt_path=receipt_dir / "executor.jsonl")
    grader_gateway = Gateway(str(bridge), grader[0], grader[1], sidecar_out, 900, grader[2],
                             durable_receipt_path=receipt_dir / "grader.jsonl")
    docker_dir = str(Path(_docker_command()).parent)
    base_env = {**os.environ, "PATH": docker_dir + os.pathsep + os.environ.get("PATH", "")}
    phase = "environment_start"
    process_receipts: dict[str, Any] = {}
    mcp_receipt: dict[str, Any] | None = None
    try:
        process_receipts["environment_start"] = _start_environment(
            harness=harness, out=out, env=base_env, endpoint=endpoint)
        phase = "world_population"
        _populate(world_root, out=out, label="world", endpoint=endpoint)
        if task_overlay is not None:
            phase = "task_overlay_population"
            _populate(task_overlay, out=out, label="task", endpoint=endpoint)
        phase = "mcp_configuration"
        mcp_receipt = _configure_mcp(harness=harness, endpoint=endpoint)
        phase = "agent_execution"
        trajectory, trajectory_path, trajectory_id, agent_process = _run_agent(
            harness=harness, out=out, task=task, projection=projection, endpoint=endpoint,
            env=_route_environment(base_env, executor_gateway), model=executor[0])
        process_receipts["agent"] = agent_process
        phase = "snapshot"
        final_snapshot = _snapshot(out=out, endpoint=endpoint)
        grades = None
        if trajectory and trajectory.get("status") == "completed":
            phase = "official_grading"
            grades, grader_process = _run_grade(
                harness=harness, out=out, task=task, initial_snapshot=initial_snapshot,
                final_snapshot=final_snapshot, trajectory=trajectory_path, trajectory_id=trajectory_id,
                env=_route_environment(base_env, grader_gateway), model=grader[0])
            process_receipts["grader"] = grader_process
        score = None
        grading_status = None
        if grades is not None:
            grading_status = grades.get("grading_run_status")
            scoring = grades.get("scoring_results")
            if isinstance(scoring, dict) and isinstance(scoring.get("final_score"), (int, float)):
                score = scoring["final_score"]
        executor_telemetry = _telemetry(executor_gateway)
        grader_telemetry = _telemetry(grader_gateway)
        completed = bool(trajectory and trajectory.get("status") == "completed"
                         and grades is not None and grading_status == "completed")
        result = {"schema_version": SCHEMA, "status": "complete" if completed else "inconclusive",
                  "task_id": executor_task["task_id"], "condition": condition,
                  "graph_digest": graph["graph_digest"], "projection_digest": projection["projection_digest"],
                  "agent_status": trajectory.get("status") if trajectory else None,
                  "official_grading_status": grading_status, "official_final_score": score,
                  "executor": {"model": executor[0], "provider": executor[1], "reasoning": executor[2],
                               "telemetry": executor_telemetry},
                  "grader": {"model": grader[0], "provider": grader[1], "reasoning": grader[2],
                             "telemetry": grader_telemetry},
                  "native_processes": process_receipts,
                  "native_mcp": mcp_receipt,
                  "automatic_admission": False, "human_approval_required": True,
                  "privacy": {"task_prompt_in_receipt": False, "rubric_in_executor": False,
                              "projection_in_receipt": False, "trajectory_in_receipt": False,
                              "grade_rationale_in_receipt": False},
                  "decision_boundary": "Official native APEX lifecycle only; no candidate graph object is admitted."}
        _write_private(out / "native-apex-result-sanitized.json", result)
        return result
    except Exception as exc:
        # Native results must distinguish a harness failure from an agent
        # failure without copying private task content or raw subprocess logs.
        result = {"schema_version": SCHEMA, "status": "inconclusive", "failure_phase": phase,
                  "failure_class": type(exc).__name__, "task_id": executor_task["task_id"],
                  "condition": condition, "graph_digest": graph["graph_digest"],
                  "executor": {"model": executor[0], "provider": executor[1], "reasoning": executor[2],
                               "telemetry": _telemetry(executor_gateway)},
                  "grader": {"model": grader[0], "provider": grader[1], "reasoning": grader[2],
                             "telemetry": _telemetry(grader_gateway)},
                  "native_processes": process_receipts,
                  "native_mcp": mcp_receipt,
                  "automatic_admission": False, "human_approval_required": True,
                  "decision_boundary": "No native outcome is available from an inconclusive lifecycle."}
        _write_private(out / "native-apex-result-sanitized.json", result)
        return result
    finally:
        executor_gateway.stop()
        grader_gateway.stop()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--harness", required=True, type=Path)
    parser.add_argument("--task", required=True, type=Path)
    parser.add_argument("--world-root", required=True, type=Path)
    parser.add_argument("--initial-snapshot", required=True, type=Path)
    parser.add_argument("--world-id", help="Private native world identifier when custody omits it")
    parser.add_argument("--task-overlay", type=Path)
    parser.add_argument("--graph", required=True, type=Path)
    parser.add_argument("--condition", required=True, choices=CONDITIONS)
    parser.add_argument("--bridge", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--endpoint", default="http://localhost:8080")
    for role in ("executor", "grader"):
        parser.add_argument(f"--{role}-model", required=True)
        parser.add_argument(f"--{role}-provider", required=True)
        parser.add_argument(f"--{role}-reasoning", required=True)
    args = parser.parse_args()
    task_file = _read_object(args.task, "native task custody")
    task = task_file.get("task") if isinstance(task_file.get("task"), dict) else task_file
    task = _with_world_id(task, args.world_id)
    result = run(harness=args.harness, task=task, world_root=args.world_root,
                 initial_snapshot=args.initial_snapshot, task_overlay=args.task_overlay,
                 graph=_read_object(args.graph, "native projection graph"), condition=args.condition,
                 out=args.out, bridge=args.bridge,
                 executor=(args.executor_model, args.executor_provider, args.executor_reasoning),
                 grader=(args.grader_model, args.grader_provider, args.grader_reasoning), endpoint=args.endpoint)
    print(json.dumps({key: result.get(key) for key in ("status", "task_id", "condition", "agent_status",
                                                        "official_grading_status", "official_final_score")},
                     sort_keys=True))
    if result["status"] != "complete":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
