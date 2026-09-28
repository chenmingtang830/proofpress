"""TypeSafe System One adapter. Typed advice only; never an admission path."""
from __future__ import annotations

import json
import os
import re
import subprocess
import time
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen

from proofpress.profiles.jev_audit import (
    VERSION as VERSION,
    RELATION_TYPE_QUESTION_VERSION as RELATION_TYPE_QUESTION_VERSION,
    RELATION_TYPE_MAPPING_VERSION as RELATION_TYPE_MAPPING_VERSION,
    RELATION_TYPES as RELATION_TYPES,
    RELATION_TYPE_CRITERIA as RELATION_TYPE_CRITERIA,
    _digest, _declared_relation_type, questions_for as questions_for, _answers,
    _verdict, validate_audit as validate_audit,
)

ENDPOINT = "https://api.typesafe.ai/v1/systemone"
DEFAULT_MODEL = "jev-latest"
MAX_BYTES = 128_000
MAX_BATCH = 32


class JevGatewayFailure(ValueError):
    """Bounded gateway failure category, never a provider response body."""

    def __init__(self, code):
        self.code = code
        super().__init__("Jev Gateway evaluation failed; no recommendation recorded")


def _gateway_failure_code(stderr):
    marker = stderr.decode("ascii", errors="ignore").strip() if isinstance(stderr, bytes) else str(stderr).strip()
    match = re.fullmatch(r"jev_gateway_failure:(http_[1-5][0-9]{2}|transport|evaluation|unavailable)", marker)
    if not match:
        return None
    value = match.group(1)
    if value == "transport":
        return "gateway_transport"
    if value in {"evaluation", "unavailable"}:
        return "gateway_evaluation"
    status = int(value.removeprefix("http_"))
    if status in {401, 403}:
        return "authentication"
    if status == 404:
        return "model_or_endpoint"
    if status == 429:
        return "rate_limited"
    if 500 <= status <= 599:
        return "provider_unavailable"
    return "provider_rejected"
def judge(packet, model=DEFAULT_MODEL, criteria="", *, opener=urlopen, gateway=False, zdr=False):
    # An explicitly injected empty workspace credential must never fall back to a host key.
    key = (os.environ.get("PROOFPRESS_JUDGE_API_KEY") if "PROOFPRESS_JUDGE_API_KEY" in os.environ
           else os.environ.get("AI_GATEWAY_API_KEY" if gateway else "TYPESAFE_API_KEY", "")) or ""
    if not key.strip():
        raise ValueError("Jev provider API key is not configured")
    schema = packet.get("schema_version")
    batch = schema == "proofpress/judge-batch-request/v1"
    if batch:
        rows = packet.get("claims", [])
        if not 1 <= len(rows) <= MAX_BATCH:
            raise ValueError("Jev batch requires 1 to 32 claims; use individual judge calls for larger scopes")
        items = [{**row, "evidence": [packet["evidence_catalog"][ref] for ref in row["evidence_refs"]]}
                 for row in rows]
    elif schema in {"proofpress/judge-request/v1", "proofpress/relation-judge-request/v1"}:
        items = [packet]
    else:
        raise ValueError("Unsupported Jev judge packet")
    if any(item.get("evaluation", {}).get("eligible") is not True for item in items):
        raise ValueError("Fix deterministic checks before requesting Jev advice")
    state = {"items": items}
    questions = {}
    groups = []
    for index, item in enumerate(items):
        group = questions_for(item, criteria, f"Evaluate only state.items[{index}]. ")
        groups.append(group)
        questions.update({f"item_{index}_{k}": v for k, v in group.items()})
    request_body = {"model": model, "state": state, "questions": questions}
    if gateway:
        if model != "typesafe-ai/jev":
            raise ValueError("Vercel Jev requires model typesafe-ai/jev")
        request_body["questions"] = {k: {**q, "type": "boolean" if q["type"] == "noul" else q["type"]}
                                     for k, q in questions.items()}
        request_body["providerOptions"] = {"gateway": {"zeroDataRetention": zdr}}
    body = json.dumps(request_body, ensure_ascii=False).encode()
    if len(body) > MAX_BYTES:
        raise ValueError("Judge evidence packet exceeds the bounded input limit")
    started = time.monotonic()
    try:
        if gateway:
            result = subprocess.run(
                ["node", str(Path(__file__).with_name("jev_gateway") / "bridge.mjs")],
                input=body, capture_output=True, timeout=50,
                env={**os.environ, "PROOFPRESS_JUDGE_API_KEY": key.strip()}, check=True)
            raw = result.stdout
        else:
            request = Request(ENDPOINT, data=body, headers={"Authorization": "Bearer " + key.strip(),
                                                          "Content-Type": "application/json"})
            with opener(request, timeout=45) as response:
                raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("oversized response")
        response = json.loads(raw)
        answers = _answers(response["answers"], questions)
        response_model = response.get("model")
        if not isinstance(response_model, str) or not 1 <= len(response_model) <= 160:
            raise ValueError("missing response model")
        usage = response.get("usage", {})
        if not isinstance(usage, dict):
            raise ValueError("invalid usage")
        clean_usage = {}
        for field in ("input_tokens", "output_tokens"):
            if field in usage:
                if type(usage[field]) is not int or usage[field] < 0:
                    raise ValueError("invalid usage")
                clean_usage[field] = usage[field]
    except subprocess.CalledProcessError as exc:
        code = _gateway_failure_code(exc.stderr) if gateway else None
        if code:
            raise JevGatewayFailure(code) from None
        raise ValueError("Jev unavailable or returned an invalid decision; no recommendation recorded") from None
    except Exception:
        raise ValueError("Jev unavailable or returned an invalid decision; no recommendation recorded") from None
    latency_ms = round((time.monotonic() - started) * 1000)
    verdicts = []
    for index, item in enumerate(items):
        subset = {k: answers[f"item_{index}_{k}"] for k in groups[index]}
        declared_relation_type = (_declared_relation_type(item)
                                  if "relation_type" in groups[index] else None)
        recommendation = _verdict(subset, declared_relation_type)
        choice = subset["recommendation"]
        rationale = (f"Template summary of Jev typed answers (not a generated explanation): "
                     f"choice={choice['choice']}; choice probability={choice['probabilities'][choice['choice']]:.3f}; "
                     f"distribution confidence={choice['confidence']:.3f}; "
                     + "; ".join(f"{k}={subset[k]['noul']:.3f}" for k in
                                 ("evidence_support", "scope_valid", "criteria_met")) +
                     f". Mapped advice: {recommendation}. Experimental thresholds; not calibrated accuracy.")
        if declared_relation_type is not None:
            relation_answer = subset["relation_type"]
            selected = relation_answer["choice"]
            rationale += (f" Relation type: declared={declared_relation_type}; "
                         f"selected={selected}; probability={relation_answer['probabilities'][selected]:.3f}; "
                         f"confidence={relation_answer['confidence']:.3f}.")
        rationale += " A recommendation does not approve a claim; only an owner decision or an explicitly enabled owner policy can admit it."
        audit = {"schema_version": "proofpress/decision-audit/v1", "backend": "jev",
                 "question_set_version": (RELATION_TYPE_QUESTION_VERSION if declared_relation_type is not None
                                          else VERSION),
                 "mapping_version": (RELATION_TYPE_MAPPING_VERSION if declared_relation_type is not None
                                     else "jev-conservative/v1"),
                 "request_digest": _digest(request_body), "requested_model": model,
                 "response_model": response_model, "questions": groups[index], "answers": subset,
                 "mapped_recommendation": recommendation,
                 "latency_ms": latency_ms, "usage": clean_usage,
                 "usage_scope": "request", "item_index": index,
                 "evaluated_at": datetime.now(timezone.utc).isoformat()}
        if declared_relation_type is not None:
            audit["declared_relation_type"] = declared_relation_type
        if gateway:
            audit["schema_version"] = "proofpress/decision-audit/v2"
            audit["transport"] = {"provider": "vercel_jev", "sdk": "ai/7.0.105;@ai-sdk/gateway/4.0.85",
                                  "response_model_source": "gateway-route", "zero_data_retention": zdr,
                                  "answer_normalization": "boolean-to-noul;typesafe-confidence-by-question/v1"}
        verdict = {"recommendation": recommendation, "rationale": rationale,
                   "adapter": VERSION, "model": response_model, "decision_audit": audit}
        if batch:
            verdict.update(claim_id=item["claim"]["id"],
                           risk_level="high" if recommendation == "escalate" else "medium")
        verdicts.append(verdict)
    if batch:
        return {"verdicts": verdicts, "adapter": VERSION, "model": response_model}
    return verdicts[0]
