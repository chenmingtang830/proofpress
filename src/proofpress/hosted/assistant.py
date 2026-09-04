"""Owner-page assistant. Explains governed state; cannot admit knowledge."""
from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-5.4-mini"
MAX_QUESTION_CHARS = 2000
MAX_SNAPSHOT_CHARS = 12000

SYSTEM_PROMPT = """You are Ask Proofpress, the owner assistant for an Agent Knowledge Management System.
You help a human owner inspect candidate conclusions, evidence, deterministic checks, policy/LM recommendations, the knowledge ledger, and consumption receipts.
You cannot admit, reject, supersede, or otherwise change authority. If asked to approve or reject, refuse and tell the owner to use the Review decision bar.
Treat deterministic checks, the policy/LM recommendation, and Human Approval as three separate layers. Never collapse them into \"verified\".
Use only the workspace snapshot. If the snapshot is missing a fact, say so instead of inventing it.
Answer in the same language as the question. Keep answers short and concrete.
"""


def configured():
    return bool(os.environ.get("OPENROUTER_API_KEY", "").strip())


def model_name():
    return os.environ.get("OPENROUTER_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def ask(question, snapshot, *, opener=urlopen):
    question = " ".join(str(question or "").split())
    if not question:
        return {"ok": False, "error": {
            "code": "invalid_request", "message": "Ask a question about this workspace."}}
    if len(question) > MAX_QUESTION_CHARS:
        return {"ok": False, "error": {
            "code": "invalid_request", "message": "Question is too long."}}
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        return {"ok": False, "error": {
            "code": "assistant_unconfigured",
            "message": "Set OPENROUTER_API_KEY on the hosted service to enable Ask Proofpress."}}
    packed = json.dumps(snapshot or {}, ensure_ascii=False, default=str)
    if len(packed) > MAX_SNAPSHOT_CHARS:
        packed = packed[:MAX_SNAPSHOT_CHARS] + "…"
    body = json.dumps({
        "model": model_name(),
        "temperature": 0.2,
        "max_tokens": 700,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content":
             "Workspace snapshot:\n" + packed + "\n\nOwner question:\n" + question},
        ],
    }).encode()
    headers = {
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "X-Title": "Proofpress Ask",
    }
    public_origin = os.environ.get("PROOFPRESS_PUBLIC_ORIGIN", "").strip()
    if public_origin:
        headers["HTTP-Referer"] = public_origin
    request = Request(OPENROUTER_URL, data=body, method="POST", headers=headers)
    try:
        with opener(request, timeout=30) as response:
            payload = json.loads(response.read().decode())
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:300]
        return {"ok": False, "error": {
            "code": "assistant_upstream",
            "message": "OpenRouter rejected the request.",
            "detail": detail}}
    except (URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        return {"ok": False, "error": {
            "code": "assistant_unavailable",
            "message": "The assistant upstream is unavailable.",
            "detail": str(exc)}}
    text = (((payload.get("choices") or [{}])[0].get("message") or {}).get("content") or "").strip()
    if not text:
        return {"ok": False, "error": {
            "code": "assistant_empty", "message": "The model returned an empty answer."}}
    return {
        "ok": True,
        "result": {
            "answer": text,
            "model": payload.get("model") or model_name(),
            "can_admit": False,
        },
    }
