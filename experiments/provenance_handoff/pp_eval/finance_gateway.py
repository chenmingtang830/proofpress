"""Fixed-route Gateway client and receipt audit for Finance qualification."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import time
from typing import Any
from urllib import request


ROUTES = {
    "decomposition": {"model": "openai/gpt-5.6-luna", "provider": "openai", "reasoning": "low"},
    "atom_extraction": {"model": "deepseek/deepseek-v4-flash", "provider": "alibaba", "reasoning": "none"},
    "type_assignment": {"model": "openai/gpt-5.6-luna", "provider": "openai", "reasoning": "low"},
    "critic": {"model": "openai/gpt-5.6-sol", "provider": "openai", "reasoning": "low"},
    "completeness": {"model": "openai/gpt-5.6-luna", "provider": "openai", "reasoning": "low"},
}


class FinanceGateway:
    def __init__(self, *, repo: Path, route: dict[str, str], output: Path,
                 api_key: str, timeout: float = 180):
        self.route = route
        output.mkdir(parents=True, exist_ok=True)
        self.receipts = output / "gateway-receipts.jsonl"
        env = dict(os.environ)
        env.update({
            "AI_GATEWAY_API_KEY": api_key,
            "PROOFPRESS_FINANCE_MODEL": route["model"],
            "PROOFPRESS_FINANCE_PROVIDER": route["provider"],
            "PROOFPRESS_FINANCE_REASONING": route["reasoning"],
            "PROOFPRESS_FINANCE_TIMEOUT_MS": str(int(timeout * 1000)),
            "PROOFPRESS_FINANCE_RECEIPTS": str(self.receipts),
        })
        server = repo / "experiments/provenance_handoff/tools/finance_gateway_bridge.mjs"
        self.process = subprocess.Popen(
            ["node", str(server)], cwd=repo, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        assert self.process.stdout is not None
        deadline = time.monotonic() + 15
        line = ""
        while time.monotonic() < deadline and self.process.poll() is None:
            line = self.process.stdout.readline()
            if line:
                break
        if not line:
            self.stop()
            raise RuntimeError("Finance Gateway bridge did not become ready")
        ready = json.loads(line)
        if ready.get("type") != "ready" or ready.get("model") != route["model"]:
            self.stop()
            raise RuntimeError("Finance Gateway bridge route mismatch")
        self.url = f"http://127.0.0.1:{ready['port']}/v1/chat/completions"

    def call(self, *, system: str, prompt: str, schema: dict[str, Any],
             schema_name: str, max_tokens: int = 512) -> dict[str, Any]:
        body = json.dumps({
            "model": self.route["model"],
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": prompt}],
            "response_schema": schema,
            "response_schema_name": schema_name,
            "max_tokens": max_tokens,
        }).encode()
        req = request.Request(self.url, data=body,
                              headers={"content-type": "application/json"})
        with request.urlopen(req, timeout=240) as response:
            value = json.loads(response.read())
        return json.loads(value["choices"][0]["message"]["content"])

    def rows(self) -> list[dict[str, Any]]:
        if not self.receipts.is_file():
            return []
        return [json.loads(line) for line in self.receipts.read_text().splitlines() if line]

    def stop(self) -> None:
        if getattr(self, "process", None) is not None and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()


def audit_receipts(rows: list[dict[str, Any]], route: dict[str, str],
                   expected_calls: int) -> dict[str, Any]:
    valid = len(rows) == expected_calls and all(
        row.get("terminal") is True and row.get("status") == "ok"
        and row.get("requested_model") == route["model"]
        and row.get("resolved_model") == route["model"]
        and row.get("requested_provider") == route["provider"]
        and row.get("resolved_provider") == route["provider"]
        and row.get("fallback_used") is False
        and row.get("model_attempt_count") == 1
        and row.get("provider_attempt_count") == 1
        and row.get("input_tokens") is not None
        and row.get("output_tokens") is not None
        and row.get("cost_usd") is not None for row in rows)
    return {
        "decision": "allow" if valid else "block",
        "terminal_calls": len(rows), "expected_calls": expected_calls,
        "known_cost_usd": sum(float(row.get("cost_usd") or 0) for row in rows),
        "input_tokens": sum(int(row.get("input_tokens") or 0) for row in rows),
        "output_tokens": sum(int(row.get("output_tokens") or 0) for row in rows),
        "fallback_calls": sum(row.get("fallback_used") is not False for row in rows),
    }
