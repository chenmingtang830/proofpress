"""Execution controls for a locally pinned, official APEX runner.

This module deliberately does not modify Archipelago's task, world, agent,
system prompt, MCP configuration, or grader.  It supplies only the host-side
controls that a reliable experiment needs: a direct-provider canary, a
process-group watchdog, a clean Compose world, and immutable run records.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import signal
import subprocess
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .storage import write_json


FINANCE_QUALIFICATION_TASK = "task_3e2e533b49374381acf2056fe479e3ba"
DEFAULT_WATCHDOG_SECONDS = 3_900
CANARY_TIMEOUT_SECONDS = 120


def _stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_env_file(path: Path | None) -> dict[str, str]:
    """Read simple KEY=VALUE entries without logging any secret values."""
    if path is None:
        return {}
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.removeprefix("export ").strip()
        if key:
            values[key] = value.strip().strip('"').strip("'")
    return values


def _environment(env_file: Path | None) -> dict[str, str]:
    env = dict(os.environ)
    env.update(_load_env_file(env_file))
    # Docker Desktop on macOS can leave an obsolete /usr/local/bin/docker
    # symlink behind an App Translocation path. Prefer its installed CLI when
    # present so attempt-recording never fails after the agent has finished.
    docker_cli_dir = Path("/Applications/Docker.app/Contents/Resources/bin")
    if (docker_cli_dir / "docker").is_file():
        env["PATH"] = f"{docker_cli_dir}{os.pathsep}{env.get('PATH', '')}"
    # LiteLLM's direct Gemini adapter accepts GEMINI_API_KEY.  Retain the
    # existing GOOGLE_API_KEY alias for runners that inspect it instead.
    if env.get("GEMINI_API_KEY") and not env.get("GOOGLE_API_KEY"):
        env["GOOGLE_API_KEY"] = env["GEMINI_API_KEY"]
    return env


def _git_commit(checkout: Path) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=checkout, text=True, capture_output=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _compose_down(checkout: Path, env: dict[str, str]) -> None:
    try:
        subprocess.run(
            ["docker", "compose", "down", "-v"],
            cwd=checkout / "environment",
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        # Teardown must not erase the attempt manifest when Docker itself has
        # become unavailable (for example after a host ENOSPC event).
        return


def _image_id(env: dict[str, str]) -> str | None:
    try:
        result = subprocess.run(
            ["docker", "image", "inspect", "environment-environment", "--format", "{{.Id}}"],
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def gemini_tool_canary(
    checkout: Path,
    model: str,
    output_path: Path,
    *,
    env_file: Path | None = None,
    timeout_seconds: int = CANARY_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Call Gemini directly with a representative function-tool request.

    It exercises exactly the provider route used by the official runner, while
    avoiding any APEX task/world data and therefore never counts as a task run.
    """
    env = _environment(env_file)
    code = """
import asyncio, json, os, sys
from litellm import acompletion
model = sys.argv[1]
async def main():
    kwargs = dict(
        model=model,
        messages=[{"role": "user", "content": "Call the readiness tool once."}],
        tools=[{"type": "function", "function": {"name": "readiness", "description": "Returns readiness.", "parameters": {"type": "object", "properties": {"ready": {"type": "boolean"}}, "required": ["ready"]}}}],
        tool_choice={"type": "function", "function": {"name": "readiness"}},
        timeout=110,
        num_retries=0,
    )
    if os.environ.get("LITELLM_PROXY_API_BASE") and os.environ.get("LITELLM_PROXY_API_KEY"):
        kwargs["api_base"] = os.environ["LITELLM_PROXY_API_BASE"]
        kwargs["api_key"] = os.environ["LITELLM_PROXY_API_KEY"]
        # The Gateway speaks the OpenAI-compatible protocol while exposing a
        # canonical provider/model ID such as ``google/gemini-*``.
        kwargs["custom_llm_provider"] = "openai"
    response = await acompletion(**kwargs)
    choice = response.choices[0]
    print(json.dumps({"has_tool_call": bool(getattr(choice.message, "tool_calls", None))}))
asyncio.run(main())
"""
    started = time.monotonic()
    try:
        result = subprocess.run(
            ["uv", "run", "python", "-c", code, model],
            cwd=checkout / "agents",
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
        # Some OpenAI-compatible proxies write informational banners before the
        # canary's final JSON line.  Treat the last valid JSON object as the
        # probe result rather than turning a successful call into a parser crash.
        parsed = {}
        for line in reversed(result.stdout.splitlines()):
            try:
                candidate = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(candidate, dict):
                parsed = candidate
                break
        status = "passed" if result.returncode == 0 and parsed.get("has_tool_call") else "failed"
        reason = "tool_call_completed" if status == "passed" else "missing_tool_call_or_nonzero_exit"
    except subprocess.TimeoutExpired:
        result = None
        parsed = {}
        status, reason = "failed", "canary_timeout"
    record = {
        "schema_version": "proofpress/apex-gemini-canary/v1",
        "model": model,
        "status": status,
        "reason": reason,
        "timeout_seconds": timeout_seconds,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "provider_key_present": bool(env.get("GEMINI_API_KEY")),
        "returncode": result.returncode if result else None,
        "response": parsed,
        "stderr_tail": result.stderr[-1000:] if result else None,
    }
    write_json(output_path, record)
    return record


def run_official_attempt(
    checkout: Path,
    task_id: str,
    results_root: Path,
    *,
    env_file: Path | None = None,
    watchdog_seconds: int = DEFAULT_WATCHDOG_SECONDS,
) -> dict[str, Any]:
    """Run the pinned official launcher once under a host-only watchdog."""
    launcher = checkout / "examples" / "hugging_face_task"
    if not (launcher / "run.sh").is_file():
        raise ValueError(f"not an Archipelago Hugging Face example: {launcher}")
    if watchdog_seconds < 3_600:
        raise ValueError("watchdog must not be shorter than the official 3600s agent timeout")
    env = _environment(env_file)
    run_dir = results_root / f"official-{task_id}-{_stamp()}-{uuid.uuid4().hex[:8]}"
    run_dir.mkdir(parents=True, exist_ok=False)
    output_dir = launcher / "output" / task_id
    if output_dir.exists():
        shutil.move(str(output_dir), str(run_dir / "preexisting_output"))
    _compose_down(checkout, env)
    log_path = run_dir / "launcher.log"
    started_at = datetime.now(UTC).isoformat()
    started = time.monotonic()
    timed_out = False
    with log_path.open("w", encoding="utf-8") as log:
        process = subprocess.Popen(
            ["bash", "./run.sh", task_id],
            cwd=launcher,
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        try:
            returncode = process.wait(timeout=watchdog_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                returncode = process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                returncode = process.wait(timeout=30)
    elapsed = round(time.monotonic() - started, 3)
    image_id = _image_id(env)
    captured_output = run_dir / "output"
    if output_dir.exists():
        shutil.copytree(output_dir, captured_output)
    trajectory_path = captured_output / "trajectory.json"
    grades_path = captured_output / "grades.json"
    trajectory: dict[str, Any] = {}
    grades: dict[str, Any] = {}
    if trajectory_path.exists():
        trajectory = json.loads(trajectory_path.read_text(encoding="utf-8"))
    if grades_path.exists():
        grades = json.loads(grades_path.read_text(encoding="utf-8"))
    complete = (
        not timed_out
        and returncode == 0
        and trajectory.get("status") == "completed"
        and grades.get("grading_run_status") == "completed"
    )
    record = {
        "schema_version": "proofpress/apex-official-attempt/v1",
        "track_label": "APEX official-runner qualification",
        "official_score_claim": False,
        "task_id": task_id,
        "model": json.loads((launcher / "orchestrator_config.json").read_text(encoding="utf-8")).get("model"),
        "judge_model": json.loads((launcher / "grading_settings.json").read_text(encoding="utf-8")).get("llm_judge_model"),
        "archipelago_commit": _git_commit(checkout),
        "dataset_manifest_sha256": _sha256(Path.home() / ".cache" / "huggingface" / "hub" / "datasets--mercor--apex-agents" / "snapshots" / "92c86856cf1b11f9833a8a076b3a45a63afa3929" / "tasks_and_rubrics.json"),
        "docker_image_id": image_id,
        "started_at": started_at,
        "elapsed_seconds": elapsed,
        "watchdog_seconds": watchdog_seconds,
        "watchdog_status": "timeout" if timed_out else "completed",
        "launcher_returncode": returncode,
        "trajectory_status": trajectory.get("status"),
        "native_grading_status": grades.get("grading_run_status"),
        "native_score": grades.get("scoring_results", {}).get("final_score"),
        "status": "completed" if complete else "infrastructure_abort_or_incomplete",
        "counted_as_benchmark_attempt": complete,
        "artifacts": {
            "launcher_log": "launcher.log",
            "output_captured": captured_output.exists(),
            "trajectory": trajectory_path.exists(),
            "grades": grades_path.exists(),
        },
    }
    write_json(run_dir / "manifest.json", record)
    _compose_down(checkout, env)
    return record | {"run_dir": str(run_dir)}
