#!/usr/bin/env python3
"""Run the private v8 claim-construction panel.

This runner deliberately keeps the APEX task prompts, section text, and model
responses in a caller-owned private directory.  The repository only contains
the protocol; the emitted sanitized report contains digests/counts and
telemetry, never corpus bytes, quotes, prompts, or gold responses.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import select
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from legal_pipeline_contract import (
    EVIDENCE_ATOM_SCHEMA,
    LIFECYCLE_CHECKLIST,
    MODEL_ROLES,
    claimability_gate,
    coverage_pass,
    freeze_requirements,
    validate_candidate_claims,
    validate_decomposition,
    validate_evidence_atom,
)

SCHEMA = "proofpress/private-claim-construction/v1"
PR36_V7_PROTOCOL = {
    "source_revision": "proofpress-pr36@9f6e3f1",
    "implementation": "frozen-reimplementation-v1",
    "decomposition_model": "gpt-5.6-luna",
    "retrieval": "bounded-lexical",
    "retrieval_config": {"max_documents_per_requirement": 10, "max_sections_per_requirement": 6},
    "proposer_model": "deepseek/deepseek-v4-flash",
    "critic_model": "gpt-5.6-sol",
}
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_'-]*", re.I)
ALLOWED_CLAIM_TYPES = {"observed_fact", "risk_signal", "legal_conclusion", "contract_allocation"}
ALLOWED_RELATION_TYPES = {"supports", "depends_on", "qualifies", "contradicts", "supersedes", "same_as"}
REQUIREMENT_ITEM_SCHEMA = {
    "type": "object",
    "required": ["requirement_id", "requirement", "rationale", "evidence_search_queries", "applicability"],
    "properties": {
        "requirement_id": {"type": "string", "maxLength": 96},
        "requirement": {"type": "string", "maxLength": 500},
        "type": {"type": "string", "maxLength": 64},
        "lifecycle_category": {"type": "string", "maxLength": 96},
        "rationale": {"type": "string", "maxLength": 500},
        "evidence_search_queries": {"type": "array", "items": {"type": "string", "maxLength": 300}, "maxItems": 4},
        "applicability": {"type": "string", "enum": ["applicable", "not_applicable", "uncertain"]},
    },
    "additionalProperties": False,
}
DECOMPOSITION_SCHEMA = {
    "type": "object", "required": ["requirements"],
    "properties": {"requirements": {"type": "array", "items": REQUIREMENT_ITEM_SCHEMA, "maxItems": 32}},
    "additionalProperties": False,
}
COVERAGE_SCHEMA = {
    "type": "object", "required": ["additions"],
    "properties": {"additions": {"type": "array", "items": REQUIREMENT_ITEM_SCHEMA, "maxItems": 8}},
    "additionalProperties": False,
}
CLAIM_SCHEMA = {
    "type": "object",
    "required": ["requirement_id", "claim_type", "statement", "evidence_ids"],
    "properties": {
        "id": {"type": ["string", "null"], "maxLength": 96},
        "claim_id": {"type": ["string", "null"], "maxLength": 96},
        "requirement_id": {"type": "string", "maxLength": 96},
        "claim_type": {"type": "string", "enum": sorted(ALLOWED_CLAIM_TYPES)},
        "statement": {"type": "string", "maxLength": 800},
        "evidence_ids": {"type": "array", "items": {"type": "string", "maxLength": 96}, "maxItems": 6},
        "scope": {"type": ["string", "null"], "maxLength": 160},
        "category": {"type": ["string", "null"], "maxLength": 96},
        "effective_date": {"type": ["string", "null"], "maxLength": 96},
        "status": {"type": ["string", "null"], "maxLength": 32},
    },
    "additionalProperties": False,
}
RELATION_SCHEMA = {
    "type": "object", "required": ["from", "to", "type"],
    "properties": {"from": {"type": "string", "maxLength": 96},
                   "to": {"type": "string", "maxLength": 96},
                   "type": {"type": "string", "enum": sorted(ALLOWED_RELATION_TYPES)}},
    "additionalProperties": False,
}
CANDIDATE_SCHEMA = {
    "type": "object", "required": ["claims", "relations"],
    "properties": {"claims": {"type": "array", "items": CLAIM_SCHEMA, "maxItems": 8},
                   "relations": {"type": "array", "items": RELATION_SCHEMA, "maxItems": 10}},
    "additionalProperties": False,
}
CRITIC_SCHEMA = {
    "type": "object", "required": ["decision", "requirement_updates", "repair_instructions", "supplemental_queries"],
    "properties": {
        "decision": {"type": "string", "maxLength": 96},
        "requirement_updates": {"type": "array", "items": REQUIREMENT_ITEM_SCHEMA, "maxItems": 8},
        "repair_instructions": {"type": "array", "maxItems": 8, "items": {
            "type": "object", "required": ["category", "instruction"],
            "properties": {
                "category": {"type": "string", "enum": ["claim_atomicity", "conflict_or_version",
                    "evidence_fidelity", "honest_gap", "other", "relation_correctness",
                    "requirement_completeness", "unsupported_assertion"]},
                "requirement_id": {"type": ["string", "null"], "maxLength": 96},
                "claim_id": {"type": ["string", "null"], "maxLength": 96},
                "instruction": {"type": "string", "maxLength": 500},
            }, "additionalProperties": False,
        }},
        "supplemental_queries": {"type": "array", "maxItems": 8, "items": {
            "anyOf": [
                {"type": "string", "maxLength": 300},
                {"type": "object", "required": ["query"], "properties": {
                    "requirement_id": {"type": ["string", "null"], "maxLength": 96},
                    "query": {"type": "string", "maxLength": 300},
                }, "additionalProperties": False},
            ],
        }},
    },
    "additionalProperties": False,
}
ATOM_ITEM_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["requirement_id", "evidence_id", "exact_excerpt", "subject", "predicate",
                 "value", "effective_date", "qualification", "document_version", "support_mode"],
    "properties": {
        "requirement_id": {"type": "string", "maxLength": 96},
        "evidence_id": {"type": "string", "maxLength": 96},
        "exact_excerpt": {"type": "string", "maxLength": 1200},
        "subject": {"type": "string", "maxLength": 300},
        "predicate": {"type": "string", "maxLength": 200},
        "value": {"type": "string", "maxLength": 500},
        "effective_date": {"type": ["string", "null"], "maxLength": 96},
        "qualification": {"type": ["string", "null"], "maxLength": 500},
        "document_version": {"type": ["string", "null"], "maxLength": 160},
        "support_mode": {"type": "string", "enum": ["explicit", "inferred"]},
    },
}
EVIDENCE_ATOMS_OUTPUT_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["atoms", "conflicts"],
    "properties": {
        "atoms": {"type": "array", "items": ATOM_ITEM_SCHEMA, "maxItems": 16},
        "conflicts": {"type": "array", "maxItems": 8, "items": {
            "type": "object", "additionalProperties": False,
            "required": ["requirement_id", "evidence_ids"],
            "properties": {"requirement_id": {"type": "string", "maxLength": 96},
                           "evidence_ids": {"type": "array", "items": {"type": "string"}, "maxItems": 6}},
        }},
    },
}
V9_CRITIC_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["verdicts"],
    "properties": {"verdicts": {"type": "array", "maxItems": 64, "items": {
        "type": "object", "additionalProperties": False,
        "required": ["claim_id", "verdict", "reason_category"],
        "properties": {
            "claim_id": {"type": "string", "maxLength": 96},
            "verdict": {"type": "string", "enum": ["supported", "partially_supported", "unsupported", "conflicted", "misclassified"]},
            "reason_category": {"type": "string", "enum": ["atomicity", "classification", "conflict", "evidence_fidelity", "unsupported_assertion"]},
        },
    }}},
}
ALLOWED_STATUS = {"covered", "partial", "gap"}
CRITIC_FINDING_KEYS = ("requirement_updates", "repair_instructions", "supplemental_queries")
CRITIC_CATEGORIES = {"requirement_completeness", "claim_atomicity", "evidence_fidelity",
                     "unsupported_assertion", "relation_correctness", "conflict_or_version",
                     "honest_gap", "other"}


def digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def sha_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


def _critic_diagnostic(critic: dict[str, Any], requirements: list[dict[str, Any]],
                       claims: list[dict[str, Any]], round_index: int) -> dict[str, Any]:
    """Produce a quote-free, stable account of why a critic round did not pass."""
    decision = str(critic.get("decision", "missing")).strip().lower().replace(" ", "_")
    targets = _critic_target_requirement_ids(critic, requirements, claims)
    counts = {key: len(critic.get(key, [])) if isinstance(critic.get(key), list) else 0
              for key in CRITIC_FINDING_KEYS}
    claim_ids = {str(row.get("id")) for row in claims if row.get("id")}
    requirement_ids = {str(row.get("requirement_id")) for row in requirements
                       if row.get("requirement_id")}
    unbound = 0
    category_counts = Counter()
    repairs = critic.get("repair_instructions", [])
    for row in repairs if isinstance(repairs, list) else []:
        if isinstance(row, dict):
            category = str(row.get("category", "other"))
            category_counts[category if category in CRITIC_CATEGORIES else "other"] += 1
        if isinstance(row, dict) and not ({str(row.get("requirement_id"))} & requirement_ids
                                         or {str(row.get("claim_id"))} & claim_ids):
            unbound += 1
    supplemental = critic.get("supplemental_queries", [])
    for row in supplemental if isinstance(supplemental, list) else []:
        if not isinstance(row, dict) or str(row.get("requirement_id")) not in requirement_ids:
            unbound += 1
    return {"round": round_index, "decision": decision, "finding_counts": counts,
            "category_counts": dict(sorted(category_counts.items())),
            "target_requirement_ids": sorted(targets), "unbound_finding_count": unbound,
            "critic_digest": digest(critic)}


def _preserve_open_critic_gaps(requirements: list[dict[str, Any]], claims: list[dict[str, Any]],
                               critic: dict[str, Any]) -> list[str]:
    """Turn unresolved critic scope into honest partial/gap state.

    The critic is a coverage gate, not an admission authority. After the two
    permitted repair rounds it must not erase the whole construction artifact;
    the contract requires unresolved content to remain visible as a gap.
    """
    targets = _critic_target_requirement_ids(critic, requirements, claims)
    claim_requirements = {
        str(claim.get("requirement_id")) for claim in claims if claim.get("requirement_id")
    }
    changed = []
    for requirement in requirements:
        requirement_id = str(requirement.get("requirement_id", ""))
        if requirement_id not in targets:
            continue
        requirement["status"] = "partial" if requirement_id in claim_requirements else "gap"
        requirement["critic_open"] = True
        requirement["critic_finding_digest"] = digest(critic)
        changed.append(requirement_id)
    return sorted(changed)


def _write_private(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    path.chmod(0o600)


def _parse_json_completion(content: str) -> Any:
    """Parse a JSON completion without accepting arbitrary prose as output.

    GLM occasionally wraps an otherwise valid object in a markdown fence or a
    short preamble.  Only the first bounded object/array candidate is accepted;
    schema validators still decide whether the parsed value is usable.
    """
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    stripped = content.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped, flags=re.I)
        stripped = re.sub(r"\s*```$", "", stripped)
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            content = stripped
    candidates = []
    for left, right in (("{", "}"), ("[", "]")):
        start, end = content.find(left), content.rfind(right)
        if start >= 0 and end > start:
            candidates.append(content[start:end + 1])
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    raise ValueError("model completion was not bounded JSON")


def _tokens(value: str) -> list[str]:
    return TOKEN_RE.findall(value.lower())


def _read_ready_line(stream: Any, timeout: float) -> str:
    """Read one sidecar readiness line without permitting an infinite startup hang."""
    ready, _, _ = select.select([stream], [], [], max(0.001, timeout))
    if not ready:
        raise TimeoutError("gateway readiness timed out")
    return stream.readline()


class Gateway:
    """A fixed local OpenAI-compatible gateway route with aggregate telemetry."""

    def __init__(self, server: str, model: str, provider: str, private_dir: Path, timeout: float,
                 reasoning: str, structured_output: bool = False,
                 min_output_tokens: int = 0,
                 durable_receipt_path: Path | None = None) -> None:
        self.model = model
        self.provider = provider
        self.reasoning = reasoning
        self.timeout = timeout
        self.structured_output = structured_output
        self.min_output_tokens = max(0, min_output_tokens)
        self._lock = threading.Lock()
        self.calls: list[dict[str, Any]] = []
        self._tmp = tempfile.mkdtemp(prefix="proofpress-claim-gateway-")
        self.private_dir = private_dir
        self._durable_receipt_path = durable_receipt_path
        self._attempt_journal_path: Path | None = None
        self._attempt_sequence = 0
        if durable_receipt_path is not None:
            durable_receipt_path.parent.mkdir(parents=True, exist_ok=True)
            durable_receipt_path.parent.chmod(0o700)
            self._attempt_journal_path = durable_receipt_path.with_name(
                durable_receipt_path.stem + "-attempts.jsonl")
            self._attempt_sequence = len(self.durable_attempt_rows())
        self._receipt_path = (durable_receipt_path
                              if durable_receipt_path is not None
                              else Path(self._tmp) / "receipts.jsonl")
        env = os.environ.copy()
        env.update({
            "PROOFPRESS_PAGEINDEX_MODEL": model,
            "PROOFPRESS_PAGEINDEX_PROVIDER": provider,
            "PROOFPRESS_PAGEINDEX_PORT": "0",
            "PROOFPRESS_PAGEINDEX_RECEIPTS": str(self._receipt_path),
            "PROOFPRESS_PAGEINDEX_ERROR_LOG": str(Path(self._tmp) / "errors.jsonl"),
            "PROOFPRESS_CLAIM_MODEL": model,
            "PROOFPRESS_CLAIM_PROVIDER": provider,
            "PROOFPRESS_CLAIM_PORT": "0",
            "PROOFPRESS_CLAIM_RECEIPTS": str(self._receipt_path),
            "PROOFPRESS_CLAIM_ERROR_LOG": str(Path(self._tmp) / "errors.jsonl"),
            # Abort the upstream request before urllib reaches its own deadline,
            # so every attempt produces one terminal gateway receipt.
            "PROOFPRESS_CLAIM_TIMEOUT_MS": str(max(1_000, int(timeout * 1_000) - 5_000)),
            "PROOFPRESS_REASONING": reasoning,
            "PROOFPRESS_CLAIM_REASONING": reasoning,
        })
        node_path = os.environ.get("NODE_PATH")
        if node_path:
            env["NODE_PATH"] = node_path
        self.proc = subprocess.Popen(
            ["node", server], env=env, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True,
        )
        try:
            line = _read_ready_line(self.proc.stdout, min(15.0, max(1.0, timeout))) if self.proc.stdout else ""
        except TimeoutError as exc:
            self.stop()
            raise RuntimeError(f"fixed gateway did not become ready for {model}/{provider}") from exc
        try:
            ready = json.loads(line)
            self.port = int(ready["port"])
            if (ready.get("model") != model or ready.get("provider") != provider
                    or ready.get("reasoning") != reasoning):
                raise ValueError("gateway readiness route mismatch")
        except Exception as exc:
            self.stop()
            raise RuntimeError(f"fixed gateway did not become ready for {model}/{provider}") from exc

    def _append_attempt_event(self, row: dict[str, Any]) -> None:
        """Persist a content-free Stage-A recovery event when configured."""
        if self._attempt_journal_path is None:
            return
        serialized = json.dumps(row, ensure_ascii=False, sort_keys=True)
        with self._lock:
            self._attempt_journal_path.parent.mkdir(parents=True, exist_ok=True)
            self._attempt_journal_path.parent.chmod(0o700)
            with self._attempt_journal_path.open("a", encoding="utf-8") as handle:
                handle.write(serialized + "\n")
            self._attempt_journal_path.chmod(0o600)

    def durable_attempt_rows(self) -> list[dict[str, Any]]:
        if self._attempt_journal_path is None or not self._attempt_journal_path.exists():
            return []
        rows = []
        for line in self._attempt_journal_path.read_text(encoding="utf-8").splitlines():
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                rows.append(value)
        return rows

    def attempt_count(self) -> int:
        if self._attempt_journal_path is None:
            return len(self.calls)
        return sum(row.get("event") == "attempt_started" for row in self.durable_attempt_rows())

    def call(self, system: str, prompt: str, max_tokens: int,
             schema: dict[str, Any] | None = None, schema_name: str | None = None) -> dict[str, Any]:
        started = time.monotonic()
        body = {"model": self.model, "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ], "max_tokens": max(max_tokens, self.min_output_tokens)}
        if self.structured_output and schema is not None:
            body["response_schema"] = schema
            body["response_schema_name"] = schema_name or "proofpress_output"
        request = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/v1/chat/completions",
            data=json.dumps(body, ensure_ascii=False).encode(),
            headers={"content-type": "application/json"},
        )
        record: dict[str, Any] = {
            "model": self.model, "provider": self.provider,
            "reasoning": self.reasoning,
            "requested_max_output_tokens": body["max_tokens"],
            "fallback_used": False, "request_digest": digest(body),
        }
        self._attempt_sequence += 1
        attempt_id = f"attempt-{self._attempt_sequence:06d}"
        self._append_attempt_event({
            "event": "attempt_started", "attempt_id": attempt_id,
            "model": self.model, "provider": self.provider, "reasoning": self.reasoning,
            "requested_max_output_tokens": body["max_tokens"],
            "request_digest": record["request_digest"], "fallback_used": False,
        })
        request.add_header("x-proofpress-attempt-id", attempt_id)
        content: str | None = None
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                envelope = json.loads(response.read())
            content = envelope.get("choices", [{}])[0].get("message", {}).get("content")
            finish_reason = envelope.get("choices", [{}])[0].get("finish_reason")
            if not isinstance(content, str):
                raise ValueError("gateway response did not contain text content")
            parsed = _parse_json_completion(content)
            usage = envelope.get("usage", {}) if isinstance(envelope, dict) else {}
            cost = usage.get("cost_usd") if isinstance(usage, dict) else None
            record.update({"status": "ok", "output_digest": digest(parsed),
                           "output_bytes": len(content.encode()),
                           "response_model": envelope.get("model"),
                           "structured_output_mode": (envelope.get("proofpress") or {}).get("structured_output_mode"),
                           "finish_reason": finish_reason,
                           "cost_usd": cost if isinstance(cost, (int, float)) else None})
            return {"ok": True, "value": parsed, "record": record}
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            record.update({"status": "inconclusive", "error_type": type(exc).__name__,
                           "error_digest": sha_text(str(exc)),
                           "output_bytes": len(content.encode()) if isinstance(content, str) else None,
                           "finish_reason": locals().get("finish_reason")})
            # Keep the raw completion only in the caller-owned private record;
            # sanitized reports contain the digest/error class, never text.
            return {"ok": False, "value": None, "record": record, "raw_content": content}
        except BaseException as exc:
            # Do not swallow Ctrl-C or process-termination signals.  The durable
            # attempt ledger makes this explicitly unresolved rather than silently
            # dropping a potentially billable in-flight request.
            record.update({"status": "aborted_client", "error_type": type(exc).__name__,
                           "error_digest": sha_text(str(exc)),
                           "output_bytes": len(content.encode()) if isinstance(content, str) else None,
                           "finish_reason": locals().get("finish_reason")})
            raise
        finally:
            record["latency_ms"] = round((time.monotonic() - started) * 1000, 3)
            with self._lock:
                self.calls.append(record)
            self._append_attempt_event({
                "event": "attempt_outcome", "attempt_id": attempt_id,
                "model": self.model, "provider": self.provider,
                "status": record.get("status", "aborted_client"),
                "error_type": record.get("error_type"),
                "output_digest": record.get("output_digest"),
                "latency_ms": record["latency_ms"],
            })

    def stop(self) -> None:
        if getattr(self, "proc", None) and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()

    def receipt_rows(self) -> list[dict[str, Any]]:
        path = self._receipt_path
        if not path.exists():
            return []
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                rows.append(value)
        return rows


class SectionIndex:
    def __init__(self, catalog: dict[str, Any]) -> None:
        self.sections: list[dict[str, Any]] = []
        self.doc_meta: dict[str, dict[str, Any]] = {}
        for representation in catalog.get("representations", []):
            source = representation["source"]
            uri = source["uri"]
            self.doc_meta[uri] = {"uri": uri, "media_type": source["media_type"],
                                  "content_digest": source["content_digest"],
                                  "representation_digest": representation["representation_digest"],
                                  "section_count": len(representation.get("sections", [])),
                                  # The full 39k-section catalog remains the
                                  # retrieval substrate.  Decomposition only
                                  # needs a bounded inventory sample; sending
                                  # every heading makes otherwise-valid gateway
                                  # calls queue for minutes.
                                  "headings": [s.get("heading") for s in representation.get("sections", []) if s.get("heading")][:2]}
            for section in representation.get("sections", []):
                row = dict(section)
                row["source"] = source
                row["representation_digest"] = representation["representation_digest"]
                row["uri"] = uri
                row["_tokens"] = _tokens((section.get("heading") or "") + " " + section.get("text", ""))
                row["_tf"] = Counter(row["_tokens"])
                self.sections.append(row)
        self.df: Counter[str] = Counter()
        self.postings: defaultdict[str, list[int]] = defaultdict(list)
        total_len = 0
        for i, row in enumerate(self.sections):
            total_len += len(row["_tokens"])
            for token in row["_tf"]:
                self.df[token] += 1
                self.postings[token].append(i)
        self.avgdl = total_len / max(1, len(self.sections))

    def inventory(self) -> list[dict[str, Any]]:
        # Decomposition needs a compact inventory, not custody digests (those
        # remain bound to every later evidence receipt).  Keeping the title,
        # media type, section count, and a tiny heading sample stays within the
        # gateway's practical context window while still covering all sources.
        return [{"title": row["uri"].rsplit("/", 1)[-1],
                 "media_type": row["media_type"]}
                for row in sorted(self.doc_meta.values(), key=lambda r: r["uri"])]

    def search(self, query: str, max_documents: int = 10, max_sections: int = 6,
               allowed_uris: set[str] | None = None,
               allowed_spans: dict[str, list[tuple[int, int]]] | None = None) -> list[dict[str, Any]]:
        terms = _tokens(query)
        if not terms:
            return []
        unique = Counter(terms)
        scores: defaultdict[int, float] = defaultdict(float)
        n = len(self.sections)
        k1, b = 1.2, 0.75
        candidate_ids = set()
        for term in unique:
            candidate_ids.update(self.postings.get(term, []))
        for index in candidate_ids:
            row = self.sections[index]; length = len(row["_tokens"])
            if allowed_uris is not None and row["uri"] not in allowed_uris:
                continue
            if allowed_spans is not None:
                spans = allowed_spans.get(row["uri"], [])
                if not any(row.get("page_start", 0) <= end and row.get("page_end", 0) >= start
                           for start, end in spans):
                    continue
            score = 0.0
            for term, qtf in unique.items():
                tf = row["_tf"].get(term, 0)
                if not tf: continue
                idf = math.log(1 + (n - self.df[term] + 0.5) / (self.df[term] + 0.5))
                score += idf * ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * length / max(self.avgdl, 1)))) * min(qtf, 2)
            scores[index] = score
        ranked = sorted(scores, key=lambda i: (-scores[i], self.sections[i]["uri"], self.sections[i]["id"]))
        # Select at most one leading section per source first, then fill by rank.
        chosen: list[int] = []; seen_sources: set[str] = set()
        for index in ranked:
            if self.sections[index]["uri"] not in seen_sources:
                chosen.append(index); seen_sources.add(self.sections[index]["uri"])
            if len(chosen) >= max_sections: break
        if len(chosen) < max_sections:
            for index in ranked:
                if index not in chosen:
                    chosen.append(index)
                if len(chosen) >= max_sections: break
        # Document ranking is retained in the audit even though section selection
        # is what binds the evidence receipts.
        doc_scores: defaultdict[str, float] = defaultdict(float)
        for index, score in scores.items(): doc_scores[self.sections[index]["uri"]] = max(doc_scores[self.sections[index]["uri"]], score)
        docs = sorted(doc_scores, key=lambda uri: (-doc_scores[uri], uri))[:max_documents]
        return [{"section": self.sections[i], "score": scores[i], "rank": rank + 1,
                 "considered_documents": docs} for rank, i in enumerate(chosen)]


def _model_call(gateway: Gateway, system: str, prompt: str, max_tokens: int,
                schema: dict[str, Any] | None = None, schema_name: str | None = None,
                max_attempts: int = 3) -> dict[str, Any]:
    """Retry at most twice on the same fixed model/provider route."""
    if max_attempts < 1 or max_attempts > 3:
        raise ValueError("max_attempts must be between one and three")
    last: dict[str, Any] | None = None
    for attempt in range(1, max_attempts + 1):
        last = gateway.call(system, prompt, max_tokens, schema, schema_name)
        last["record"]["attempt"] = attempt
        if last["ok"]:
            return last
    assert last is not None
    return last


def _safe_requirements(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        value = {"requirements": value}
    if not isinstance(value, dict) or not isinstance(value.get("requirements"), list):
        if (isinstance(value, dict) and isinstance(value.get("output"), dict)
                and isinstance(value["output"].get("requirements"), list)):
            value = {"requirements": value["output"]["requirements"]}
        elif isinstance(value, dict) and isinstance(value.get("output_requirements"), list):
            value = {"requirements": value["output_requirements"]}
        else:
            raise ValueError("model decomposition lacked requirements")
    rows = []
    for index, row in enumerate(value["requirements"][:32], 1):
        if not isinstance(row, dict): continue
        item = dict(row)
        item.setdefault("requirement_id", item.pop("id", None) or f"req_{index:02d}")
        item.setdefault("requirement", "")
        applicability = item.get("applicability")
        if applicability not in {"applicable", "not_applicable", "uncertain"}:
            # Keep the model's richer conditional wording in rationale while
            # projecting the contract field to its three-valued enum.
            item["applicability"] = "applicable" if str(applicability).lower() in {"always", "yes", "true"} else "uncertain"
        item.setdefault("applicability", "uncertain")
        item.setdefault("rationale", "")
        item.setdefault("evidence_search_queries", [item.get("requirement", "")])
        refs = item.pop("lifecycle_refs", None)
        item.setdefault("lifecycle_category", (refs[0] if isinstance(refs, list) and refs else "missing_evidence_negotiated_inputs"))
        rows.append(item)
    return rows


def _safe_additions(value: Any, existing_ids: set[str] | None = None) -> list[dict[str, Any]]:
    if not isinstance(value, dict): return []
    if isinstance(value.get("output"), dict):
        value = value["output"]
    raw = value.get("additions", value.get("requirements", []))
    rows = _safe_requirements({"requirements": raw})[:8] if isinstance(raw, list) else []
    # A per-call JSON Schema cannot enforce uniqueness against IDs emitted by
    # the preceding decomposition call. IDs are syntactic handles, so repair
    # collisions deterministically without changing requirement semantics.
    used = set(existing_ids or set())
    for index, row in enumerate(rows, 1):
        candidate = str(row.get("requirement_id") or "")
        if not candidate or candidate in used:
            suffix = index
            candidate = f"coverage_req_{suffix:02d}"
            while candidate in used:
                suffix += 1
                candidate = f"coverage_req_{suffix:02d}"
            row["requirement_id"] = candidate
        used.add(candidate)
    return rows


def _evidence(requirement_id: str, hit: dict[str, Any], query: str) -> dict[str, Any]:
    section = hit["section"]; source = section["source"]
    evidence_id = "ev_" + hashlib.sha256(
        (section["representation_digest"] + "\n" + section["id"]).encode()
    ).hexdigest()[:20]
    source_record = {key: source[key] for key in
                     ("uri", "content_digest", "media_type", "official_authority")
                     if key in source}
    receipt = {"evidence_id": evidence_id, "source": source_record,
        "representation_digest": section["representation_digest"],
        "quote": section.get("text", ""),
        "locator": {"kind": "section_span", "section_id": section["id"],
                    "section_digest": section["text_digest"], "page_start": section["page_start"],
                    "page_end": section["page_end"], "line_start": section.get("line_start"),
                    "line_end": section.get("line_end")},
        "retrieval": {"adapter": "bm25-section/v1", "query": query,
                       "rank": hit["rank"], "score": round(hit["score"], 8)},
    }
    receipt["receipt_digest"] = digest(receipt)
    return receipt


def _normalize_candidate_output(value: Any, requirements: list[dict[str, Any]],
                                evidence_by_id: dict[str, dict[str, Any]],
                                audit: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    value = value if isinstance(value, dict) else {}
    raw_claims = [dict(row) for row in value.get("claims", []) if isinstance(row, dict)][:64]
    relations = [dict(row) for row in value.get("relations", []) if isinstance(row, dict)][:80]
    requirement_ids = {row["requirement_id"] for row in requirements}
    requirement_types = {row["requirement_id"]: row.get("type", "factual_input") for row in requirements}
    claims = []
    for claim in raw_claims:
        requirement_id = str(claim.get("requirement_id"))
        if requirement_id not in requirement_ids:
            continue
        valid_evidence_ids = list(dict.fromkeys(
            evidence_id for evidence_id in claim.get("evidence_ids", [])
            if evidence_id in evidence_by_id))
        # Claims are evidence-bound by contract.  A hallucinated or entirely
        # missing reference invalidates this candidate only; the frozen
        # requirement remains an explicit partial/gap for later review.
        if not valid_evidence_ids or not str(claim.get("statement", "")).strip():
            continue
        claim["evidence_ids"] = valid_evidence_ids
        claims.append(claim)
    claim_handles: dict[str, str] = {}
    requirement_handles: dict[str, str] = {}
    for index, claim in enumerate(claims):
        stable_id = f"candidate_{index + 1:03d}"
        for handle in (claim.get("id"), claim.get("claim_id")):
            if handle:
                claim_handles[str(handle)] = stable_id
        claim_handles[f"claim_{index}"] = stable_id
        claim["id"] = stable_id
        requirement_id = str(claim.get("requirement_id"))
        requirement_handles.setdefault(requirement_id, claim["id"])
        label = str(claim.get("claim_type", "observed_fact")).lower()
        if label not in ALLOWED_CLAIM_TYPES:
            if any(term in label for term in ("risk", "gap", "missing", "conflict", "triage")):
                label = "risk_signal"
            elif any(term in label for term in ("contract", "transfer", "allocation", "clause")):
                label = "contract_allocation"
            elif any(term in label for term in ("legal", "rule", "analysis", "conclusion")):
                label = "legal_conclusion"
            else:
                label = "observed_fact"
        claim["claim_type"] = label
        claim["status"] = "unresolved"
        claim.setdefault("scope", "matter")
        claim.setdefault("category", requirement_types[requirement_id])
        claim.setdefault("effective_date", None)
        claim.setdefault("evidence_ids", [])
    normalized_relations = []
    seen_relations = set()
    stable_claim_ids = {claim["id"] for claim in claims}
    for relation in relations:
        relation["from"] = claim_handles.get(
            relation.get("from"), requirement_handles.get(str(relation.get("from")), relation.get("from")))
        relation["to"] = claim_handles.get(
            relation.get("to"), requirement_handles.get(str(relation.get("to")), relation.get("to")))
        relation_type = relation.get("type")
        relation["type"] = {
            "blocks": "depends_on", "conflicts_with": "contradicts",
            "addresses": "supports", "related": "same_as",
            "curable_via": "depends_on", "gap_flagged_by": "supports",
        }.get(relation_type, relation_type)
        relation_key = (relation.get("from"), relation.get("to"), relation.get("type"))
        if (relation["type"] in ALLOWED_RELATION_TYPES
                and relation["from"] in stable_claim_ids and relation["to"] in stable_claim_ids
                and relation_key not in seen_relations):
            seen_relations.add(relation_key)
            normalized_relations.append(relation)
    evidence_ids_by_requirement = {
        row["requirement_id"]: set(row["evidence_ids"])
        for row in audit if row.get("requirement_id") in requirement_ids
    }
    claimed_requirements = {
        claim["requirement_id"] for claim in claims if claim.get("evidence_ids")
    }
    for row in requirements:
        requirement_id = row["requirement_id"]
        if requirement_id in claimed_requirements:
            row["status"] = "covered"
        elif evidence_ids_by_requirement.get(requirement_id):
            row["status"] = "partial"
        else:
            row["status"] = "gap"
    validate_candidate_claims(requirements, claims, normalized_relations)
    return claims, normalized_relations


def _candidate_batches(task: dict[str, Any], model_requirements: list[dict[str, Any]],
                       evidence_by_id: dict[str, dict[str, Any]], audit: list[dict[str, Any]],
                       glm: Gateway, system: str, *, critic: dict[str, Any] | None = None,
                       current_claims: list[dict[str, Any]] | None = None,
                       current_relations: list[dict[str, Any]] | None = None,
                       evidence_atoms: list[dict[str, Any]] | None = None,
                       max_attempts: int = 3) -> dict[str, Any]:
    """Run bounded proposer/repair batches after requirements and retrieval freeze."""
    batches = [model_requirements[i:i + 4] for i in range(0, len(model_requirements), 4)]
    audit_by_requirement = {row.get("requirement_id"): row for row in audit}

    def run(batch_index: int, batch: list[dict[str, Any]]) -> dict[str, Any]:
        requirement_ids = {row["requirement_id"] for row in batch}
        evidence_ids = [evidence_id for requirement_id in requirement_ids
                        for evidence_id in audit_by_requirement.get(requirement_id, {}).get("evidence_ids", [])[:2]]
        if critic is not None:
            evidence_ids.extend(evidence_id for row in audit
                                if row.get("supplemental") and row.get("requirement_id") in requirement_ids
                                for evidence_id in row.get("evidence_ids", [])[:4])
        seen = set()
        compact = []
        for evidence_id in evidence_ids:
            if evidence_id in seen or evidence_id not in evidence_by_id:
                continue
            seen.add(evidence_id); evidence = evidence_by_id[evidence_id]
            compact.append({"evidence_id": evidence_id, "source_uri": evidence["source"]["uri"],
                            "locator": evidence["locator"], "quote": evidence["quote"][:300]})
        batch_atoms = [row for row in (evidence_atoms or [])
                       if row.get("requirement_id") in requirement_ids]
        payload: dict[str, Any] = {
            "task": (task["prompt"] if evidence_atoms is None else None),
            "task_digest": sha_text(task["prompt"]), "frozen_requirements": batch,
            "evidence_receipts": compact,
            "evidence_atoms": batch_atoms,
            "output_schema": {
                "claims": "complete array for this batch <=4; exactly one atomic claim per covered requirement; fields requirement_id, claim_type, statement, evidence_ids, scope, category, effective_date, status=unresolved",
                "relations": "array <=10; allowed types supports|depends_on|qualifies|contradicts|supersedes|same_as",
            },
            "instruction": ("Return compact JSON only. Every covered requirement needs at least one atomic evidence-bound claim. Preserve honest gaps and conflicts; all claims remain unresolved."
                            if evidence_atoms is None else
                            "Return compact JSON only. Use only the validated evidence atoms and their bound receipts. The task digest is not evidence. Do not invent a claim for a missing, partial, conflicting, or analysis-only requirement; all returned claims remain unresolved."),
        }
        if critic is not None:
            batch_claims = [row for row in (current_claims or []) if row.get("requirement_id") in requirement_ids]
            batch_claim_ids = {str(row.get("id")) for row in batch_claims if row.get("id")}
            batch_relations = [row for row in (current_relations or [])
                               if str(row.get("from")) in batch_claim_ids or str(row.get("to")) in batch_claim_ids]
            critic_refs = requirement_ids | batch_claim_ids
            compact_critic: dict[str, Any] = {"decision": critic.get("decision")}
            for key in ("requirement_updates", "repair_instructions", "supplemental_queries"):
                rows = critic.get(key, []) if isinstance(critic.get(key), list) else []
                compact_critic[key] = [row for row in rows
                                       if any(ref in json.dumps(row, ensure_ascii=False) for ref in critic_refs)][:8]
            payload.update({"current_claims": batch_claims, "current_relations": batch_relations,
                            "critic": compact_critic,
                            "output_schema": {
                                "claims": "complete replacement array for this batch <=8 and <=2 per requirement; split only where the critic requires atomicity repair; fields requirement_id, claim_type, statement, evidence_ids, scope, category, effective_date, status=unresolved",
                                "relations": "array <=10; allowed types supports|depends_on|qualifies|contradicts|supersedes|same_as",
                            },
                            "instruction": "Repair only the critic findings for this requirement batch. Return complete replacement claims for the batch and any valid relations. Preserve honest gaps and conflicts; all claims remain unresolved."})
        result = _model_call(glm, system, json.dumps(payload, ensure_ascii=False), 8000,
                             CANDIDATE_SCHEMA, "proofpress_candidate_claims", max_attempts)
        return {"batch_index": batch_index, "requirement_ids": sorted(requirement_ids), "result": result}

    outputs = []
    with ThreadPoolExecutor(max_workers=min(2, max(1, len(batches)))) as pool:
        futures = [pool.submit(run, index, batch) for index, batch in enumerate(batches)]
        for future in as_completed(futures):
            outputs.append(future.result())
    outputs.sort(key=lambda row: row["batch_index"])
    failures = [row for row in outputs if not row["result"]["ok"]]
    claims, relations = [], []
    raw = []
    for row in outputs:
        if not row["result"]["ok"]:
            raw.append(row["result"].get("raw_content"))
            continue
        value = row["result"]["value"] if isinstance(row["result"]["value"], dict) else {}
        batch_claims = [dict(claim) for claim in value.get("claims", []) if isinstance(claim, dict)]
        handle_map = {}
        for index, claim in enumerate(batch_claims):
            scoped_id = f"batch_{row['batch_index']}_claim_{index}"
            for handle in (claim.get("id"), claim.get("claim_id"), f"claim_{index}"):
                if handle:
                    handle_map[str(handle)] = scoped_id
            claim["id"] = scoped_id
        batch_relations = [dict(relation) for relation in value.get("relations", []) if isinstance(relation, dict)]
        for relation in batch_relations:
            relation["from"] = handle_map.get(str(relation.get("from")), relation.get("from"))
            relation["to"] = handle_map.get(str(relation.get("to")), relation.get("to"))
        claims.extend(batch_claims)
        relations.extend(batch_relations)
        raw.append(value)
    failed_requirement_ids = {requirement_id for row in failures for requirement_id in row["requirement_ids"]}
    if critic is not None and failed_requirement_ids:
        retained = [dict(claim) for claim in (current_claims or [])
                    if claim.get("requirement_id") in failed_requirement_ids]
        claims.extend(retained)
    if critic is not None:
        selected_requirement_ids = {row["requirement_id"] for row in model_requirements}
        claims.extend(dict(claim) for claim in (current_claims or [])
                      if claim.get("requirement_id") not in selected_requirement_ids)
        relations.extend(dict(relation) for relation in (current_relations or []))
    return {"ok": True, "value": {"claims": claims[:64], "relations": relations[:80]}, "raw": raw,
            "failed_requirement_ids": sorted(failed_requirement_ids),
            "batch_failures": [row["result"]["record"] for row in failures]}


def _critic_target_requirement_ids(critic: dict[str, Any], requirements: list[dict[str, Any]],
                                   claims: list[dict[str, Any]]) -> set[str]:
    """Resolve compact critic findings to their affected frozen requirements."""
    known = {row["requirement_id"] for row in requirements}
    claim_to_requirement = {row["id"]: row["requirement_id"] for row in claims}
    findings = {key: critic.get(key, []) for key in ("repair_instructions", "supplemental_queries", "requirement_updates")}
    serialized = json.dumps(findings, ensure_ascii=False, sort_keys=True)
    targets = {requirement_id for requirement_id in known if requirement_id in serialized}
    targets.update(requirement_id for claim_id, requirement_id in claim_to_requirement.items() if claim_id in serialized)
    for collection in findings.values():
        if not isinstance(collection, list):
            continue
        for row in collection:
            if not isinstance(row, dict):
                continue
            direct = row.get("requirement_id")
            if direct in known:
                targets.add(direct)
            for requirement_id in row.get("requirement_ids", []) if isinstance(row.get("requirement_ids"), list) else []:
                if requirement_id in known:
                    targets.add(requirement_id)
    return targets


def _decompose(task: dict[str, Any], index: SectionIndex, glm: Gateway) -> tuple[dict[str, Any], dict[str, Any]]:
    inventory = index.inventory()
    # Keep all sources and deterministic heading inventory; section text never
    # enters decomposition, preventing accidental evidence leakage.
    heading_sample = []
    for row in index.sections:
        heading = row.get("heading")
        if heading and heading not in heading_sample:
            heading_sample.append(heading)
        if len(heading_sample) >= 8:
            break
    prompt = json.dumps({"task": task["prompt"], "source_inventory": inventory,
                         "section_heading_sample": heading_sample,
                         "legal_profile": "legal", "lifecycle_checklist": list(LIFECYCLE_CHECKLIST),
                         "output": {"requirements": "array <=32; each item must be compact (<=40 words) with fields requirement_id, requirement, type, lifecycle_category, rationale, evidence_search_queries (<=2), applicability"}},
                        ensure_ascii=False)
    system = "You are a legal task decomposer. Return only JSON. Do not answer the task. Do not use any rubric, gold response, or source quotes."
    first = _model_call(glm, system, prompt, 16000, DECOMPOSITION_SCHEMA, "proofpress_task_decomposition")
    if not first["ok"]: return {"status": "inconclusive", "reason": first["record"]}, {"raw": first.get("raw_content")}
    try:
        requirements = _safe_requirements(first["value"])
        validate_decomposition(task["prompt"], inventory, requirements)
    except Exception as exc:
        return {"status": "inconclusive", "reason": {"type": type(exc).__name__, "digest": sha_text(str(exc))}}, {"raw": first["value"]}
    coverage_prompt = json.dumps({"task": task["prompt"], "source_inventory": inventory,
                                  "checklist": list(LIFECYCLE_CHECKLIST), "requirements": requirements,
                                  "instruction": "Add only omitted atomic requirements; <=8 additions; do not use rubric/gold/quotes."}, ensure_ascii=False)
    coverage = _model_call(glm, system, coverage_prompt, 8000, COVERAGE_SCHEMA, "proofpress_coverage_additions")
    if not coverage["ok"]:
        return {"status": "inconclusive", "stage": "coverage", "reason": coverage["record"]}, {
            "raw": {"decomposition": first["value"], "coverage": coverage.get("raw_content")}
        }
    additions: list[dict[str, Any]] = []
    try:
        additions = _safe_additions(coverage["value"], {row["requirement_id"] for row in requirements})
    except Exception as exc:
        return {"status": "inconclusive", "stage": "coverage", "reason": {
            "type": type(exc).__name__, "digest": sha_text(str(exc))
        }}, {"raw": {"decomposition": first["value"], "coverage": coverage.get("value")}}
    try:
        merged = coverage_pass(requirements, additions)
        frozen = freeze_requirements(merged)
    except Exception as exc:
        return {"status": "inconclusive", "reason": {"type": type(exc).__name__, "digest": sha_text(str(exc))}}, {"raw": {"decomposition": first["value"], "coverage": coverage.get("value")}}
    frozen["requirements"] = merged
    return {"status": "ok", "requirements": merged, "frozen": frozen,
            "coverage_status": "ok", "decomposition_digest": digest(requirements),
            "coverage_digest": digest(additions)}, {"raw": {"decomposition": first["value"], "coverage": coverage.get("value")}}


def _decompose_v7(task: dict[str, Any], index: SectionIndex, luna: Gateway) -> tuple[dict[str, Any], dict[str, Any]]:
    """Frozen PR36-v7 comparator: Luna, inventory-only decomposition, no v8 lifecycle coverage pass."""
    inventory = index.inventory()
    prompt = json.dumps({"task": task["prompt"], "source_inventory": inventory,
                         "output": {"requirements": "array <=32 with requirement_id, requirement, rationale, evidence_search_queries, applicability"}},
                        ensure_ascii=False)
    first = _model_call(luna, "Decompose the task into bounded retrieval requirements. Return JSON only; do not answer the task and do not use rubric, gold, or source quotes.", prompt, 12000)
    if not first["ok"]:
        return {"status": "inconclusive", "reason": first["record"]}, {"raw": first.get("raw_content")}
    try:
        requirements = _safe_requirements(first["value"])
        validate_decomposition(task["prompt"], inventory, requirements)
        frozen = freeze_requirements(coverage_pass(requirements, []))
    except Exception as exc:
        return {"status": "inconclusive", "reason": {"type": type(exc).__name__,
                "digest": sha_text(str(exc))}}, {"raw": first.get("value")}
    return {"status": "ok", "requirements": requirements, "frozen": frozen,
            "coverage_status": "not_applicable_v7", "decomposition_digest": digest(requirements)}, {
                "raw": {"decomposition": first.get("value")}}


def _extract_evidence_atoms(requirements: list[dict[str, Any]],
                            evidence_by_id: dict[str, dict[str, Any]],
                            audit: list[dict[str, Any]], gateway: Gateway
                            ) -> tuple[list[dict[str, Any]], set[str], list[dict[str, Any]]]:
    """Extract source-bound atoms without exposing the task prompt as evidence."""
    audit_by_requirement = {row["requirement_id"]: row for row in audit}
    batches = [requirements[index:index + 4] for index in range(0, len(requirements), 4)]

    def run(batch_index: int, batch: list[dict[str, Any]]) -> dict[str, Any]:
        allowed: dict[str, set[str]] = {}
        receipts = []
        for requirement in batch:
            requirement_id = requirement["requirement_id"]
            ids = audit_by_requirement.get(requirement_id, {}).get("evidence_ids", [])[:3]
            allowed[requirement_id] = set(ids)
            for evidence_id in ids:
                evidence = evidence_by_id[evidence_id]
                receipts.append({"requirement_id": requirement_id, "evidence_id": evidence_id,
                                 "receipt_digest": evidence["receipt_digest"],
                                 "source_uri": evidence["source"]["uri"],
                                 "locator": evidence["locator"],
                                 "quote": evidence["quote"][:1200]})
        payload = {"requirements": [{key: row.get(key) for key in
                                      ("requirement_id", "requirement", "type", "lifecycle_category")}
                                     for row in batch],
                   "evidence_receipts": receipts,
                   "instruction": "Extract only atomic information explicitly present in each bound quote. exact_excerpt must be a verbatim substring. Mark inference as inferred. Report material contradictions in conflicts. Do not answer any task and do not assign authority."}
        result = _model_call(gateway,
                             "You extract evidence atoms from quoted receipts. Return structured records only; source text, never the task prompt, is the factual boundary.",
                             json.dumps(payload, ensure_ascii=False), 10000,
                             EVIDENCE_ATOMS_OUTPUT_SCHEMA, "proofpress_evidence_atoms", 2)
        return {"batch_index": batch_index, "allowed": allowed, "result": result}

    outputs = []
    with ThreadPoolExecutor(max_workers=min(2, max(1, len(batches)))) as pool:
        futures = [pool.submit(run, index, batch) for index, batch in enumerate(batches)]
        for future in as_completed(futures):
            outputs.append(future.result())
    outputs.sort(key=lambda row: row["batch_index"])
    atoms: list[dict[str, Any]] = []
    conflicts: set[str] = set()
    diagnostics: list[dict[str, Any]] = []
    for output in outputs:
        result = output["result"]
        if not result["ok"]:
            diagnostics.append({"batch": output["batch_index"], "status": "inconclusive",
                                "reason": result["record"]})
            continue
        value = result["value"] if isinstance(result["value"], dict) else {}
        for conflict in value.get("conflicts", []):
            requirement_id = str(conflict.get("requirement_id", ""))
            evidence_ids = set(map(str, conflict.get("evidence_ids", [])))
            if requirement_id in output["allowed"] and len(evidence_ids & output["allowed"][requirement_id]) >= 2:
                conflicts.add(requirement_id)
        for raw in value.get("atoms", []):
            requirement_id = str(raw.get("requirement_id", ""))
            evidence_id = str(raw.get("evidence_id", ""))
            if evidence_id not in output["allowed"].get(requirement_id, set()):
                continue
            evidence = evidence_by_id[evidence_id]
            atom = {**raw, "schema_version": EVIDENCE_ATOM_SCHEMA,
                    "receipt_digest": evidence["receipt_digest"],
                    "locator": evidence["locator"]}
            atom["atom_id"] = "atom_" + digest({key: atom.get(key) for key in
                ("requirement_id", "evidence_id", "exact_excerpt", "subject", "predicate", "value",
                 "effective_date", "qualification", "document_version", "support_mode")})[7:27]
            try:
                validate_evidence_atom(atom, evidence_by_id)
            except ValueError as exc:
                diagnostics.append({"batch": output["batch_index"], "status": "rejected_atom",
                                    "reason_type": type(exc).__name__, "reason_digest": sha_text(str(exc))})
                continue
            atoms.append(atom)
        diagnostics.append({"batch": output["batch_index"], "status": "ok",
                            "atom_count": sum(row.get("requirement_id") in output["allowed"] for row in atoms)})
    return atoms, conflicts, diagnostics


def _construct_v9(task: dict[str, Any], decomposition: dict[str, Any], index: SectionIndex,
                  proposer: Gateway, sol: Gateway, *, atom_gateway: Gateway | None = None,
                  claimability_mode: str = "strict_atom_preproposal",
                  frozen_atom_bundle: tuple[list[dict[str, Any]], set[str],
                                            list[dict[str, Any]]] | None = None,
                  ) -> tuple[dict[str, Any], dict[str, Any]]:
    if claimability_mode not in {
        "strict_atom_preproposal", "receipt_preproposal", "postproposal_binding",
    }:
        raise ValueError("unsupported claimability mode")
    requirements: list[dict[str, Any]] = []
    evidence_by_id: dict[str, dict[str, Any]] = {}
    audit: list[dict[str, Any]] = []
    for req in decomposition["requirements"]:
        queries = req.get("evidence_search_queries") or [req.get("requirement", "")]
        query = " ".join(str(value) for value in queries[:4])
        hits = index.search(query)
        selected = [_evidence(req["requirement_id"], hit, query) for hit in hits]
        for evidence in selected:
            evidence_by_id.setdefault(evidence["evidence_id"], evidence)
        audit.append({"requirement_id": req["requirement_id"], "query_digest": sha_text(query),
                      "considered_documents": sorted({doc for hit in hits for doc in hit["considered_documents"]}),
                      "ranked_section_count": len(hits), "evidence_ids": [row["evidence_id"] for row in selected]})
        requirements.append({**req, "status": "partial" if selected else "gap"})

    atoms, conflicts, atom_diagnostics = (frozen_atom_bundle if frozen_atom_bundle is not None
                                          else _extract_evidence_atoms(
                                              requirements, evidence_by_id, audit,
                                              atom_gateway or proposer))
    gates = [claimability_gate(requirement, atoms,
                               conflict=requirement["requirement_id"] in conflicts)
             for requirement in requirements]
    gate_by_requirement = {row["requirement_id"]: row for row in gates}
    evidence_requirement_ids = {
        row["requirement_id"] for row in audit if row.get("evidence_ids")
    }
    if claimability_mode == "strict_atom_preproposal":
        eligible_requirement_ids = {
            row["requirement_id"] for row in gates if row["state"] == "claimable"
        }
    else:
        # The relaxed pre-proposal and post-proposal conditions intentionally
        # isolate placement of the deterministic gate. Both admit only
        # requirements with valid retrieval receipts; post-proposal relies on
        # normalisation to reject every unbound generated claim.
        eligible_requirement_ids = evidence_requirement_ids - conflicts
    claimable = [{key: row.get(key) for key in
                  ("requirement_id", "requirement", "type", "lifecycle_category", "applicability")}
                 for row in requirements
                 if row["requirement_id"] in eligible_requirement_ids]
    system = ("You are an evidence-first candidate claim proposer. Use only validated atoms and bound receipts. "
              "Return unresolved candidate records, never an answer or admitted fact.")
    proposal = _candidate_batches(task, claimable, evidence_by_id, audit, proposer, system,
                                  evidence_atoms=atoms, max_attempts=2) if claimable else {
                                      "ok": True, "value": {"claims": [], "relations": []},
                                      "raw": [], "batch_failures": []}
    value = proposal["value"] if isinstance(proposal.get("value"), dict) else {}
    try:
        claims, relations = _normalize_candidate_output(value, requirements, evidence_by_id, audit)
    except Exception as exc:
        return {"status": "inconclusive", "reason": {"type": type(exc).__name__,
                "digest": sha_text(str(exc))}}, {"retrieval": audit, "atoms": atom_diagnostics,
                                                  "proposal": value}
    atom_by_id = {row["atom_id"]: row for row in atoms}
    critic_payload = {"requirements": requirements, "claimability_gates": gates,
                      "claims": claims, "relations": relations,
                      "evidence_atoms": atoms,
                      "instruction": "Return exactly one verdict for every claim. Judge evidence fidelity, atomicity, classification, conflicts, and unsupported assertions. Do not repair or rewrite claims."}
    critic = _model_call(sol,
                         "You are an independent claim verdict gate. Return verdicts only; you cannot repair, admit, or rewrite a claim.",
                         json.dumps(critic_payload, ensure_ascii=False), 10000,
                         V9_CRITIC_SCHEMA, "proofpress_claim_verdicts", 2)
    if not critic["ok"]:
        return {"status": "ok", "requirements": requirements, "claims": [], "relations": [],
                "evidence": list(evidence_by_id.values()), "evidence_atoms": atoms,
                "claimability_gates": gates, "retrieval_audit": audit,
                "critic_status": "inconclusive", "critic_reason": critic["record"],
                "repair_rounds": 0, "batch_failure_count": len(proposal.get("batch_failures", []))}, {
                    "retrieval": audit, "atoms": atom_diagnostics, "proposal": value}
    verdict_rows = critic["value"].get("verdicts", []) if isinstance(critic["value"], dict) else []
    verdict_by_claim = {str(row.get("claim_id")): row for row in verdict_rows}
    supported = [claim for claim in claims
                 if verdict_by_claim.get(claim["id"], {}).get("verdict") == "supported"]
    supported_ids = {row["id"] for row in supported}
    relations = [row for row in relations if row.get("from") in supported_ids and row.get("to") in supported_ids]
    supported_requirements = {row["requirement_id"] for row in supported}
    proposed_requirements = {row["requirement_id"] for row in claims}
    verdict_by_requirement: dict[str, set[str]] = defaultdict(set)
    for claim in claims:
        verdict_by_requirement[claim["requirement_id"]].add(
            verdict_by_claim.get(claim["id"], {}).get("verdict", "unsupported"))
    for requirement in requirements:
        requirement_id = requirement["requirement_id"]
        gate = gate_by_requirement[requirement_id]
        if requirement_id in supported_requirements:
            requirement["status"] = "covered"
        elif gate["state"] == "conflict" or "conflicted" in verdict_by_requirement[requirement_id]:
            requirement["status"] = "gap"; requirement["resolution"] = "conflict"
        elif gate["state"] in {"partial", "needs_legal_analysis"} or verdict_by_requirement[requirement_id]:
            requirement["status"] = "partial"; requirement["resolution"] = gate["state"]
        else:
            requirement["status"] = "gap"; requirement["resolution"] = gate["state"]
    validate_candidate_claims(requirements, supported, relations)
    verdict_counts = Counter(verdict_by_claim.get(claim["id"], {}).get("verdict", "missing")
                             for claim in claims)
    atom_requirement_ids = {row["requirement_id"] for row in atoms}
    explicit_atom_requirement_ids = {
        row["requirement_id"] for row in atoms if row.get("support_mode") == "explicit"
    }
    stage_counts = {
        "frozen_requirements": len(requirements),
        "requirements_with_receipts": len(evidence_requirement_ids),
        "requirements_with_valid_atoms": len(atom_requirement_ids),
        "requirements_with_explicit_atoms": len(explicit_atom_requirement_ids),
        "preproposal_eligible_requirements": len(eligible_requirement_ids),
        "requirements_with_normalized_claims": len(proposed_requirements),
        "critic_supported_requirements": len(supported_requirements),
    }
    return {"status": "ok", "requirements": requirements, "claims": supported,
            "relations": relations, "evidence": list(evidence_by_id.values()),
            "evidence_atoms": atoms, "claimability_gates": gates,
            "retrieval_audit": audit, "critic_status": "ok", "critic_verdicts": verdict_rows,
            "critic_diagnostics": [{"round": 1, "decision": "per_claim_verdicts",
                                     "verdict_counts": dict(sorted(verdict_counts.items()))}],
            "repair_rounds": 0, "batch_failure_count": len(proposal.get("batch_failures", [])),
            "rejected_claim_count": len(claims) - len(supported),
            "claimability_mode": claimability_mode, "stage_counts": stage_counts}, {
                "retrieval": audit, "atoms": atom_diagnostics, "proposal": value,
                "critic": critic["value"], "atom_index_digest": digest(atom_by_id)}


def _construct(task: dict[str, Any], decomposition: dict[str, Any], index: SectionIndex, glm: Gateway, sol: Gateway) -> tuple[dict[str, Any], dict[str, Any]]:
    requirements = []
    evidence_by_id: dict[str, dict[str, Any]] = {}
    audit = []
    for req in decomposition["requirements"]:
        queries = req.get("evidence_search_queries") or [req.get("requirement", "")]
        query = " ".join(str(x) for x in queries[:4])
        hits = index.search(query)
        selected = [_evidence(req["requirement_id"], hit, query) for hit in hits]
        for evidence in selected:
            evidence_by_id.setdefault(evidence["evidence_id"], evidence)
        audit.append({"requirement_id": req["requirement_id"], "query_digest": sha_text(query),
                      "considered_documents": sorted({d for hit in hits for d in hit["considered_documents"]}),
                      "ranked_section_count": len(hits), "evidence_ids": [x["evidence_id"] for x in selected]})
        row = dict(req); row["status"] = "partial" if not selected else "covered"; requirements.append(row)
    model_requirements = [{k: row.get(k) for k in ("requirement_id", "requirement", "type", "lifecycle_category", "applicability")}
                          for row in requirements]
    system = "You are a candidate claim proposer. Return candidate records only; they are not admitted facts and do not answer the user."
    proposal = _candidate_batches(task, model_requirements, evidence_by_id, audit, glm, system)
    batch_failures = list(proposal.get("batch_failures", []))
    if not proposal["ok"]:
        return {"status": "inconclusive", "reason": proposal["record"], "retrieval_audit": audit}, {"retrieval": audit, "proposal": proposal.get("raw")}
    value = proposal["value"] if isinstance(proposal["value"], dict) else {}
    try:
        claims, relations = _normalize_candidate_output(value, requirements, evidence_by_id, audit)
    except Exception as exc:
        return {"status": "inconclusive", "reason": {"type": type(exc).__name__, "digest": sha_text(str(exc))},
                "retrieval_audit": audit}, {"retrieval": audit, "proposal": value}

    critic_history: list[dict[str, Any]] = []
    repair_history: list[dict[str, Any]] = []
    critic_diagnostics: list[dict[str, Any]] = []
    for repair_round in range(3):
        current_compact_evidence = [{"evidence_id": e["evidence_id"], "source_uri": e["source"]["uri"],
                                     "locator": e["locator"], "quote": e["quote"][:300]}
                                    for e in evidence_by_id.values()]
        critic_prompt = json.dumps({"task": task["prompt"], "requirements": model_requirements,
                                    "claims": claims, "relations": relations,
                                    "evidence_receipts": current_compact_evidence,
                                    "output_limits": {"requirement_updates": 8, "repair_instructions": 8,
                                                      "supplemental_queries": 8},
                                    "instruction": "Independently audit completeness, atomicity, fidelity, unsupported assertions, relation correctness, conflicts, and honest gaps. Return compact JSON with decision, requirement_updates, repair_instructions, supplemental_queries. Every repair instruction must include one category: requirement_completeness, claim_atomicity, evidence_fidelity, unsupported_assertion, relation_correctness, conflict_or_version, honest_gap, or other; bind it to requirement_id and/or claim_id."}, ensure_ascii=False)
        critic = _model_call(sol, "You are an independent coverage critic. Do not use rubric or gold response. Return compact JSON only.", critic_prompt, 8000,
                             CRITIC_SCHEMA, "proofpress_coverage_critic")
        if not critic["ok"]:
            return {"status": "ok", "requirements": requirements, "claims": claims, "relations": relations,
                    "evidence": list(evidence_by_id.values()), "retrieval_audit": audit,
                    "critic_status": "inconclusive", "critic_reason": critic["record"],
                    "repair_rounds": repair_round, "batch_failure_count": len(batch_failures)}, {"retrieval": audit, "proposal": value,
                                                     "critic_history": critic_history,
                                                     "repair_history": repair_history}
        critic_value = critic["value"] if isinstance(critic["value"], dict) else {}
        critic_history.append(critic_value)
        diagnostic = _critic_diagnostic(critic_value, requirements, claims, repair_round + 1)
        critic_diagnostics.append(diagnostic)
        added_requirement_ids = set()
        raw_updates = critic_value.get("requirement_updates", [])
        if isinstance(raw_updates, list) and raw_updates:
            try:
                updates = _safe_requirements({"requirements": raw_updates})[:8]
            except Exception:
                updates = []
            existing_requirement_ids = {row["requirement_id"] for row in requirements}
            for update in updates:
                if len(requirements) >= 40 or update["requirement_id"] in existing_requirement_ids:
                    continue
                update.setdefault("type", "factual_input")
                queries = update.get("evidence_search_queries") or [update.get("requirement", "")]
                query = " ".join(str(value) for value in queries[:4])
                hits = index.search(query)
                selected = [_evidence(update["requirement_id"], hit, query) for hit in hits]
                for evidence in selected:
                    evidence_by_id.setdefault(evidence["evidence_id"], evidence)
                audit.append({"requirement_id": update["requirement_id"], "query_digest": sha_text(query),
                              "considered_documents": sorted({doc for hit in hits for doc in hit["considered_documents"]}),
                              "ranked_section_count": len(hits), "evidence_ids": [row["evidence_id"] for row in selected],
                              "critic_added": True})
                requirement = dict(update); requirement["status"] = "partial" if selected else "gap"; requirement["critic_added"] = True
                requirements.append(requirement)
                model_requirements.append({key: requirement.get(key) for key in (
                    "requirement_id", "requirement", "type", "lifecycle_category", "applicability")})
                existing_requirement_ids.add(update["requirement_id"]); added_requirement_ids.add(update["requirement_id"])
        decision = str(critic_value.get("decision", "")).lower().replace(" ", "_")
        repair_instructions = critic_value.get("repair_instructions", [])
        supplemental_queries = critic_value.get("supplemental_queries", [])
        needs_repair = decision not in {"pass", "accept", "accepted", "approved", "sufficient", "no_repair"}
        needs_repair = needs_repair or bool(repair_instructions) or bool(supplemental_queries) or bool(added_requirement_ids)
        if not needs_repair:
            return {"status": "ok", "requirements": requirements, "claims": claims, "relations": relations,
                    "evidence": list(evidence_by_id.values()), "retrieval_audit": audit,
                    "critic_status": "ok", "critic": critic_value,
                    "critic_diagnostics": critic_diagnostics,
                    "repair_rounds": repair_round, "batch_failure_count": len(batch_failures)}, {"retrieval": audit, "proposal": value,
                                                     "critic_history": critic_history,
                                                     "repair_history": repair_history}
        if repair_round == 2:
            break

        for query_index, query_row in enumerate(supplemental_queries[:8], 1):
            query = query_row.get("query") if isinstance(query_row, dict) else query_row
            if not isinstance(query, str) or not query.strip():
                continue
            bound_requirement = query_row.get("requirement_id") if isinstance(query_row, dict) else None
            audit_id = (bound_requirement if bound_requirement in {row["requirement_id"] for row in requirements}
                        else f"critic_round_{repair_round + 1}_query_{query_index}")
            hits = index.search(query)
            selected = [_evidence(audit_id, hit, query) for hit in hits]
            for evidence in selected:
                evidence_by_id.setdefault(evidence["evidence_id"], evidence)
            audit.append({"requirement_id": audit_id, "query_digest": sha_text(query),
                          "considered_documents": sorted({d for hit in hits for d in hit["considered_documents"]}),
                          "ranked_section_count": len(hits), "evidence_ids": [x["evidence_id"] for x in selected],
                          "supplemental": True})
        target_ids = _critic_target_requirement_ids(critic_value, requirements, claims) | added_requirement_ids
        if not target_ids:
            # An unbound global critic finding is still actionable; fail
            # conservatively to the full set instead of silently dropping it.
            target_ids = {row["requirement_id"] for row in model_requirements}
        repair_requirements = [row for row in model_requirements if row["requirement_id"] in target_ids]
        diagnostic["repair_scope_requirement_ids"] = sorted(target_ids)
        diagnostic["pre_repair_claim_count"] = len(claims)
        diagnostic["pre_repair_claim_digest"] = digest(claims)
        repair = _candidate_batches(task, repair_requirements, evidence_by_id, audit, glm, system,
                                    critic=critic_value, current_claims=claims,
                                    current_relations=relations)
        batch_failures.extend(repair.get("batch_failures", []))
        if not repair["ok"]:
            return {"status": "ok", "requirements": requirements, "claims": claims, "relations": relations,
                    "evidence": list(evidence_by_id.values()), "retrieval_audit": audit,
                    "critic_status": "inconclusive", "critic_reason": repair["record"],
                    "repair_rounds": repair_round, "batch_failure_count": len(batch_failures)}, {"retrieval": audit, "proposal": value,
                                                     "critic_history": critic_history,
                                                     "repair_history": repair_history}
        try:
            claims, relations = _normalize_candidate_output(repair["value"], requirements, evidence_by_id, audit)
        except Exception as exc:
            return {"status": "ok", "requirements": requirements, "claims": claims, "relations": relations,
                    "evidence": list(evidence_by_id.values()), "retrieval_audit": audit,
                    "critic_status": "inconclusive", "critic_reason": {"type": type(exc).__name__,
                                                                         "digest": sha_text(str(exc))},
                    "repair_rounds": repair_round, "batch_failure_count": len(batch_failures)}, {"retrieval": audit, "proposal": value,
                                                     "critic_history": critic_history,
                                                     "repair_history": repair_history}
        repair_history.append(repair["value"])
        diagnostic["post_repair_claim_count"] = len(claims)
        diagnostic["post_repair_claim_digest"] = digest(claims)
    open_gap_requirement_ids = _preserve_open_critic_gaps(
        requirements, claims, critic_history[-1])
    return {"status": "ok", "requirements": requirements, "claims": claims, "relations": relations,
            "evidence": list(evidence_by_id.values()), "retrieval_audit": audit,
            "critic_status": "open_gaps_after_repairs", "critic": critic_history[-1],
            "critic_diagnostics": critic_diagnostics,
            "open_gap_requirement_ids": open_gap_requirement_ids,
            "repair_rounds": 2, "batch_failure_count": len(batch_failures)}, {"retrieval": audit, "proposal": value,
                                  "critic_history": critic_history, "repair_history": repair_history}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--tasks-json", required=True)
    parser.add_argument("--world-id", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--gateway-server", required=True)
    parser.add_argument("--gateway-provider", default="zai")
    parser.add_argument("--v8-construction-model", default=MODEL_ROLES["decomposition"],
                        help="Frozen v8 decomposition and candidate proposer/repair model.")
    parser.add_argument("--system-version", choices=("v8", "evidence-first-v9", "pr36-v7"), default="v8")
    parser.add_argument("--v9-proposer-model", default=MODEL_ROLES["candidate_proposer_repair"])
    parser.add_argument("--v9-proposer-provider", default="novita")
    parser.add_argument("--v9-proposer-reasoning", default="high")
    parser.add_argument("--v7-decomposition-provider", default="openai")
    parser.add_argument("--v7-proposer-provider", default="deepseek")
    parser.add_argument("--critic-provider", default="openai")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--glm-reasoning", default="none")
    parser.add_argument("--construction-min-output-tokens", type=int, default=0,
                        help="Minimum output-token cap for v8 decomposition/proposal/repair calls.")
    parser.add_argument("--critic-reasoning", default="low")
    parser.add_argument("--max-tasks", type=int, default=0)
    parser.add_argument("--exclude-task-id", action="append", default=[])
    parser.add_argument("--budget-usd", type=float, default=100.0)
    parser.add_argument("--qualification", action="store_true",
                        help="Run a pre-scoring qualification block; requires one or two tasks and reports fail-closed readiness.")
    args = parser.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True); out.chmod(0o700)
    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    tasks_all = json.loads(Path(args.tasks_json).read_text(encoding="utf-8"))
    tasks_all = tasks_all.get("tasks", tasks_all) if isinstance(tasks_all, dict) else tasks_all
    excluded_task_ids = set(args.exclude_task_id)
    tasks = [row for row in tasks_all if row.get("world_id") == args.world_id and row.get("prompt")
             and row.get("task_id") not in excluded_task_ids]
    tasks.sort(key=lambda row: row["task_id"])
    if args.max_tasks:
        tasks = tasks[:args.max_tasks]
    if args.qualification and not 1 <= len(tasks) <= 4:
        parser.error("--qualification requires a one-to-four-task block (use --max-tasks 4)")
    index = SectionIndex(catalog)
    private = out / "raw"
    glm = proposer = sol = None
    try:
        decomposition_model = (PR36_V7_PROTOCOL["decomposition_model"] if args.system_version == "pr36-v7"
                               else args.v8_construction_model)
        proposer_model = (PR36_V7_PROTOCOL["proposer_model"] if args.system_version == "pr36-v7"
                          else args.v9_proposer_model if args.system_version == "evidence-first-v9"
                          else args.v8_construction_model)
        decomposition_provider = (args.v7_decomposition_provider if args.system_version == "pr36-v7"
                                  else args.gateway_provider)
        proposer_provider = (args.v7_proposer_provider if args.system_version == "pr36-v7"
                             else args.v9_proposer_provider if args.system_version == "evidence-first-v9"
                             else args.gateway_provider)
        proposer_reasoning = (args.v9_proposer_reasoning if args.system_version == "evidence-first-v9"
                              else args.glm_reasoning)
        structured_output = args.system_version != "pr36-v7"
        glm = Gateway(args.gateway_server, decomposition_model, decomposition_provider, out, args.timeout, args.glm_reasoning,
                      structured_output=structured_output,
                      min_output_tokens=args.construction_min_output_tokens if structured_output else 0)
        proposer = (glm if proposer_model == decomposition_model and proposer_provider == decomposition_provider else
                    Gateway(args.gateway_server, proposer_model, proposer_provider, out, args.timeout, proposer_reasoning,
                            structured_output=structured_output,
                            min_output_tokens=args.construction_min_output_tokens if structured_output else 0))
        sol = Gateway(args.gateway_server, MODEL_ROLES["coverage_critic"], args.critic_provider, out, args.timeout, args.critic_reasoning,
                      structured_output=structured_output)
        def run(row: dict[str, Any]) -> tuple[str, dict[str, Any]]:
            decomposition, decomp_raw = ((_decompose_v7(row, index, glm)) if args.system_version == "pr36-v7"
                                         else _decompose(row, index, glm))
            if decomposition["status"] != "ok":
                result = {"task_id": row["task_id"], "task_name": row.get("task_name"), "status": "inconclusive", "decomposition": decomposition}
                _write_private(private / (row["task_id"] + ".json"), {"task": row, "decomposition": decomposition, "raw": decomp_raw})
                return row["task_id"], result
            construction, construct_raw = (_construct_v9(row, decomposition, index, proposer, sol)
                                           if args.system_version == "evidence-first-v9"
                                           else _construct(row, decomposition, index, proposer, sol))
            construction_status = construction.get("status")
            critic_status = construction.get("critic_status")
            overall_status = ("ok" if construction_status == "ok" and
                              critic_status in {"ok", "open_gaps_after_repairs"} else "inconclusive")
            result = {"task_id": row["task_id"], "task_name": row.get("task_name"), "status": overall_status,
                      "construction_status": construction_status,
                      "decomposition_requirement_count": len(decomposition["requirements"]),
                      "requirement_count": len(construction.get("requirements", [])),
                      "critic_added_requirement_count": sum(bool(row.get("critic_added")) for row in construction.get("requirements", [])),
                      "claim_count": len(construction.get("claims", [])), "relation_count": len(construction.get("relations", [])),
                      "evidence_atom_count": len(construction.get("evidence_atoms", [])),
                      "claimability_gate_count": len(construction.get("claimability_gates", [])),
                      "rejected_claim_count": construction.get("rejected_claim_count", 0),
                      "evidence_count": len(construction.get("evidence", [])), "critic_status": critic_status,
                      "repair_rounds": construction.get("repair_rounds"),
                      "critic_diagnostic_digest": digest(construction.get("critic_diagnostics", [])),
                      "critic_diagnostics": construction.get("critic_diagnostics", []),
                      "batch_failure_count": construction.get("batch_failure_count", 0),
                      "requirement_digest": digest(construction.get("requirements", [])),
                      "claim_digest": digest(construction.get("claims", [])),
                      "retrieval_audit_digest": digest(construction.get("retrieval_audit", []))}
            _write_private(private / (row["task_id"] + ".json"), {"task": row, "decomposition": decomposition, "construction": construction,
                                                                     "raw": {"decomposition": decomp_raw, "construction": construct_raw}})
            return row["task_id"], result
        results: dict[str, dict[str, Any]] = {}
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            futures = {pool.submit(run, row): row for row in tasks}
            for future in as_completed(futures):
                row = futures[future]
                try:
                    task_id, result = future.result()
                except Exception as exc:
                    task_id = row["task_id"]
                    result = {"task_id": task_id, "task_name": row.get("task_name"),
                              "status": "inconclusive", "stage": "runner",
                              "reason": {"type": type(exc).__name__, "digest": sha_text(str(exc))}}
                    _write_private(private / (task_id + ".json"),
                                   {"task": row, "runner_error": result["reason"]})
                results[task_id] = result
    finally:
        if glm: glm.stop()
        if proposer and proposer is not glm: proposer.stop()
        if sol: sol.stop()
    all_calls = ((glm.calls if glm else []) + (proposer.calls if proposer and proposer is not glm else []) +
                 (sol.calls if sol else []))
    gateway_receipts = ((glm.receipt_rows() if glm else []) +
                        (proposer.receipt_rows() if proposer and proposer is not glm else []) +
                        (sol.receipt_rows() if sol else []))
    numeric_costs = [float(r["cost_usd"]) for r in gateway_receipts if isinstance(r.get("cost_usd"), (int, float))]
    missing_receipt_costs = sum(not isinstance(r.get("cost_usd"), (int, float)) for r in gateway_receipts)
    latencies = sorted(float(r["latency_ms"]) for r in all_calls if isinstance(r.get("latency_ms"), (int, float)))
    def percentile(values: list[float], p: float) -> float | None:
        if not values:
            return None
        index = min(len(values) - 1, max(0, math.ceil(p * len(values)) - 1))
        return round(values[index], 3)
    completed = sum(r.get("status") == "ok" for r in results.values())
    telemetry_complete = (not missing_receipt_costs and len(gateway_receipts) == len(all_calls))
    qualification_checks = {
        "all_tasks_completed": completed == len(tasks),
        "all_critics_terminal": all(r.get("critic_status") in {"ok", "open_gaps_after_repairs"}
                                     for r in results.values()),
        "all_calls_have_terminal_cost_receipts": telemetry_complete,
        "all_structured_logical_outputs_valid": (
            all(int(row.get("batch_failure_count", 0)) == 0 for row in results.values())
            if structured_output else True),
        "no_fallback": all(not row.get("fallback_used") for row in all_calls),
    }
    structured_modes = Counter(
        str(row.get("structured_mode") or "missing") for row in gateway_receipts
        if structured_output
    )
    terminal_failure_types = Counter(
        str(row.get("error_type") or "unknown") for row in gateway_receipts
        if row.get("status") != "ok"
    )
    schema_failure_types = {"StructuredToolCallMissingError", "AI_NoObjectGeneratedError"}
    critic_failure_counts = Counter()
    critic_category_counts = Counter()
    critic_decisions = Counter()
    unbound_critic_findings = 0
    for result in results.values():
        for row in result.get("critic_diagnostics", []):
            critic_decisions[str(row.get("decision", "missing"))] += 1
            unbound_critic_findings += int(row.get("unbound_finding_count", 0))
            for key, count in row.get("finding_counts", {}).items():
                critic_failure_counts[key] += int(count)
            for key, count in row.get("category_counts", {}).items():
                critic_category_counts[key] += int(count)
    configuration = {
        "decomposition": {"model": decomposition_model, "provider": decomposition_provider,
                          "reasoning": args.glm_reasoning},
        "candidate_proposer_repair": {"model": proposer_model, "provider": proposer_provider,
                                      "reasoning": proposer_reasoning},
        "coverage_critic": {"model": MODEL_ROLES["coverage_critic"],
                            "provider": args.critic_provider, "reasoning": args.critic_reasoning},
        "fallback": "forbidden",
        "output_protocol": "provider-structured-json-schema/v1" if structured_output else "prompt-only-json/v1",
        "construction_min_output_tokens": args.construction_min_output_tokens,
    }
    configuration["config_digest"] = digest(configuration)
    report = {"schema_version": SCHEMA, "system": args.system_version,
              "protocol": (PR36_V7_PROTOCOL if args.system_version == "pr36-v7" else {
                  "implementation": ("evidence-first-claim-construction-v9"
                                     if args.system_version == "evidence-first-v9"
                                     else "legal-claim-construction-v8"),
                  "decomposition_model": decomposition_model,
                  "candidate_proposer_repair_model": proposer_model,
                  "coverage_critic_model": MODEL_ROLES["coverage_critic"],
                  "construction_model_override": decomposition_model != MODEL_ROLES["decomposition"],
                  "construction_min_output_tokens": args.construction_min_output_tokens,
                  "evidence_atom_schema": EVIDENCE_ATOM_SCHEMA if args.system_version == "evidence-first-v9" else None,
                  "semantic_repairs": 0 if args.system_version == "evidence-first-v9" else 2,
              }),
              "catalog_digest": catalog.get("catalog_digest"),
              "task_set_digest": digest([row["task_id"] for row in tasks]),
              "excluded_development_task_ids": sorted(excluded_task_ids),
              "source_count": len(catalog.get("sources", [])), "unique_source_uri_count": len(index.doc_meta),
              "section_count": len(index.sections),
              "models": {"decomposition": decomposition_model, "candidate_proposer_repair": proposer_model,
                         "coverage_critic": MODEL_ROLES["coverage_critic"]},
              "providers": {"decomposition": decomposition_provider, "proposer": proposer_provider,
                            "critic": args.critic_provider},
              "configuration": configuration,
              "output_protocol": "provider-structured-json-schema/v1" if structured_output else "prompt-only-json/v1",
              "fallback": "forbidden", "tasks": [results[k] for k in sorted(results)],
              "denominators": {"tasks": len(tasks), "completed_construction": completed,
                               "inconclusive_tasks": sum(r.get("status") != "ok" for r in results.values()),
                               "quality_metrics_with_frozen_silver_locators": 0},
              "telemetry": {"calls": len(all_calls), "ok_calls": sum(r.get("status") == "ok" for r in all_calls),
                            "inconclusive_calls": sum(r.get("status") != "ok" for r in all_calls),
                            "structured_output_modes": dict(sorted(structured_modes.items())),
                            "terminal_failure_types": dict(sorted(terminal_failure_types.items())),
                            "parse_or_schema_failure_count": sum(
                                count for kind, count in terminal_failure_types.items()
                                if kind in schema_failure_types),
                            "transport_or_timeout_failure_count": sum(
                                count for kind, count in terminal_failure_types.items()
                                if kind not in schema_failure_types),
                            "gateway_receipts": len(gateway_receipts),
                            "known_cost_usd": round(sum(numeric_costs), 8),
                            "cost_usd": round(sum(numeric_costs), 8) if not missing_receipt_costs and len(gateway_receipts) == len(all_calls) else None,
                            "latency_ms": {"p50": percentile(latencies, 0.50), "p95": percentile(latencies, 0.95)},
                            "cost_status": "ok" if not missing_receipt_costs and len(gateway_receipts) == len(all_calls) else "inconclusive_missing_call_cost",
                            "budget_usd": args.budget_usd,
                            "budget_status": "within" if not missing_receipt_costs and len(gateway_receipts) == len(all_calls) and sum(numeric_costs) <= args.budget_usd else "inconclusive"},
              "qualification": {"requested": args.qualification,
                                "status": ("pass" if all(qualification_checks.values()) else "fail") if args.qualification else "not_run",
                                "checks": qualification_checks if args.qualification else {}},
              "critic_diagnostics": {"rounds": sum(len(r.get("critic_diagnostics", [])) for r in results.values()),
                                     "decisions": dict(sorted(critic_decisions.items())),
                                     "finding_counts": dict(sorted(critic_failure_counts.items())),
                                     "category_counts": dict(sorted(critic_category_counts.items())),
                                     "unbound_finding_count": unbound_critic_findings},
              "scoring_boundary": "Construction never receives rubric, gold response, or frozen silver locators. A separate post-output scorer binds this run to pre-frozen model-adjudicated silver.",
              "raw_private_dir": str(private)}
    _write_private(out / "sanitized-report.json", report)
    # Copy only aggregate gateway receipts into the private workspace.
    _write_private(out / "gateway-call-summary.json", {"calls": all_calls})
    print(json.dumps({"ok": True, "schema_version": SCHEMA, "task_count": len(tasks),
                      "completed": report["denominators"]["completed_construction"],
                      "inconclusive": report["denominators"]["inconclusive_tasks"],
                      "calls": len(all_calls), "report": str(out / "sanitized-report.json")}))


if __name__ == "__main__":
    main()
