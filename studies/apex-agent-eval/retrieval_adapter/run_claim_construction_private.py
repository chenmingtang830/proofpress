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
    LIFECYCLE_CHECKLIST,
    MODEL_ROLES,
    coverage_pass,
    freeze_requirements,
    validate_candidate_claims,
    validate_decomposition,
)

SCHEMA = "proofpress/private-claim-construction/v1"
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_'-]*", re.I)
ALLOWED_CLAIM_TYPES = {"observed_fact", "risk_signal", "legal_conclusion", "contract_allocation"}
ALLOWED_RELATION_TYPES = {"supports", "depends_on", "qualifies", "contradicts", "supersedes", "same_as"}
ALLOWED_STATUS = {"covered", "partial", "gap"}


def digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def sha_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


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


class Gateway:
    """A fixed local OpenAI-compatible gateway route with aggregate telemetry."""

    def __init__(self, server: str, model: str, provider: str, private_dir: Path, timeout: float,
                 reasoning: str) -> None:
        self.model = model
        self.provider = provider
        self.timeout = timeout
        self._lock = threading.Lock()
        self.calls: list[dict[str, Any]] = []
        self._tmp = tempfile.mkdtemp(prefix="proofpress-claim-gateway-")
        env = os.environ.copy()
        env.update({
            "PROOFPRESS_PAGEINDEX_MODEL": model,
            "PROOFPRESS_PAGEINDEX_PROVIDER": provider,
            "PROOFPRESS_PAGEINDEX_PORT": "0",
            "PROOFPRESS_PAGEINDEX_RECEIPTS": str(Path(self._tmp) / "receipts.jsonl"),
            "PROOFPRESS_PAGEINDEX_ERROR_LOG": str(Path(self._tmp) / "errors.jsonl"),
            "PROOFPRESS_CLAIM_MODEL": model,
            "PROOFPRESS_CLAIM_PROVIDER": provider,
            "PROOFPRESS_CLAIM_PORT": "0",
            "PROOFPRESS_CLAIM_RECEIPTS": str(Path(self._tmp) / "receipts.jsonl"),
            "PROOFPRESS_CLAIM_ERROR_LOG": str(Path(self._tmp) / "errors.jsonl"),
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
        line = self.proc.stdout.readline() if self.proc.stdout else ""
        try:
            ready = json.loads(line)
            self.port = int(ready["port"])
            if ready.get("model") != model or ready.get("provider") != provider:
                raise ValueError("gateway readiness route mismatch")
        except Exception as exc:
            self.stop()
            raise RuntimeError(f"fixed gateway did not become ready for {model}/{provider}") from exc
        self.private_dir = private_dir

    def call(self, system: str, prompt: str, max_tokens: int) -> dict[str, Any]:
        started = time.monotonic()
        body = {"model": self.model, "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ], "max_tokens": max_tokens}
        request = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/v1/chat/completions",
            data=json.dumps(body, ensure_ascii=False).encode(),
            headers={"content-type": "application/json"},
        )
        record: dict[str, Any] = {
            "model": self.model, "provider": self.provider,
            "fallback_used": False, "request_digest": digest(body),
        }
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
        finally:
            record["latency_ms"] = round((time.monotonic() - started) * 1000, 3)
            with self._lock:
                self.calls.append(record)

    def stop(self) -> None:
        if getattr(self, "proc", None) and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()

    def receipt_rows(self) -> list[dict[str, Any]]:
        path = Path(self._tmp) / "receipts.jsonl"
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

    def search(self, query: str, max_documents: int = 10, max_sections: int = 6) -> list[dict[str, Any]]:
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


def _model_call(gateway: Gateway, system: str, prompt: str, max_tokens: int) -> dict[str, Any]:
    """Retry at most twice on the same fixed model/provider route."""
    last: dict[str, Any] | None = None
    for attempt in range(1, 4):
        last = gateway.call(system, prompt, max_tokens)
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


def _safe_additions(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, dict): return []
    if isinstance(value.get("output"), dict):
        value = value["output"]
    raw = value.get("additions", value.get("requirements", []))
    return _safe_requirements({"requirements": raw})[:8] if isinstance(raw, list) else []


def _evidence(requirement_id: str, hit: dict[str, Any], query: str) -> dict[str, Any]:
    section = hit["section"]; source = section["source"]
    evidence_id = "ev_" + hashlib.sha256(
        (section["representation_digest"] + "\n" + section["id"]).encode()
    ).hexdigest()[:20]
    receipt = {"evidence_id": evidence_id, "source": {
        "uri": source["uri"], "content_digest": source["content_digest"], "media_type": source["media_type"]},
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
                       current_relations: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Run bounded proposer/repair batches after requirements and retrieval freeze."""
    batches = [model_requirements[i:i + 4] for i in range(0, len(model_requirements), 4)]
    audit_by_requirement = {row.get("requirement_id"): row for row in audit}
    supplemental_ids = [evidence_id for row in audit if row.get("supplemental")
                        for evidence_id in row.get("evidence_ids", [])]

    def run(batch_index: int, batch: list[dict[str, Any]]) -> dict[str, Any]:
        requirement_ids = {row["requirement_id"] for row in batch}
        evidence_ids = [evidence_id for requirement_id in requirement_ids
                        for evidence_id in audit_by_requirement.get(requirement_id, {}).get("evidence_ids", [])[:2]]
        if critic is not None:
            evidence_ids.extend(supplemental_ids[:16])
        seen = set()
        compact = []
        for evidence_id in evidence_ids:
            if evidence_id in seen or evidence_id not in evidence_by_id:
                continue
            seen.add(evidence_id); evidence = evidence_by_id[evidence_id]
            compact.append({"evidence_id": evidence_id, "source_uri": evidence["source"]["uri"],
                            "locator": evidence["locator"], "quote": evidence["quote"][:300]})
        payload: dict[str, Any] = {
            "task": task["prompt"], "frozen_requirements": batch,
            "evidence_receipts": compact,
            "output_schema": {
                "claims": "complete array for this batch <=4; exactly one atomic claim per covered requirement; fields requirement_id, claim_type, statement, evidence_ids, scope, category, effective_date, status=unresolved",
                "relations": "array <=10; allowed types supports|depends_on|qualifies|contradicts|supersedes|same_as",
            },
            "instruction": "Return compact JSON only. Every covered requirement needs at least one atomic evidence-bound claim. Preserve honest gaps and conflicts; all claims remain unresolved.",
        }
        if critic is not None:
            batch_claims = [row for row in (current_claims or []) if row.get("requirement_id") in requirement_ids]
            payload.update({"current_claims": batch_claims, "current_relations": current_relations or [],
                            "critic": critic,
                            "output_schema": {
                                "claims": "complete replacement array for this batch <=8 and <=2 per requirement; split only where the critic requires atomicity repair; fields requirement_id, claim_type, statement, evidence_ids, scope, category, effective_date, status=unresolved",
                                "relations": "array <=10; allowed types supports|depends_on|qualifies|contradicts|supersedes|same_as",
                            },
                            "instruction": "Repair only the critic findings for this requirement batch. Return complete replacement claims for the batch and any valid relations. Preserve honest gaps and conflicts; all claims remain unresolved."})
        result = _model_call(glm, system, json.dumps(payload, ensure_ascii=False), 8000)
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
    first = _model_call(glm, system, prompt, 16000)
    if not first["ok"]: return {"status": "inconclusive", "reason": first["record"]}, {"raw": first.get("raw_content")}
    try:
        requirements = _safe_requirements(first["value"])
        validate_decomposition(task["prompt"], inventory, requirements)
    except Exception as exc:
        return {"status": "inconclusive", "reason": {"type": type(exc).__name__, "digest": sha_text(str(exc))}}, {"raw": first["value"]}
    coverage_prompt = json.dumps({"task": task["prompt"], "source_inventory": inventory,
                                  "checklist": list(LIFECYCLE_CHECKLIST), "requirements": requirements,
                                  "instruction": "Add only omitted atomic requirements; <=8 additions; do not use rubric/gold/quotes."}, ensure_ascii=False)
    coverage = _model_call(glm, system, coverage_prompt, 8000)
    if not coverage["ok"]:
        return {"status": "inconclusive", "stage": "coverage", "reason": coverage["record"]}, {
            "raw": {"decomposition": first["value"], "coverage": coverage.get("raw_content")}
        }
    additions: list[dict[str, Any]] = []
    try:
        additions = _safe_additions(coverage["value"])
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
    for repair_round in range(3):
        current_compact_evidence = [{"evidence_id": e["evidence_id"], "source_uri": e["source"]["uri"],
                                     "locator": e["locator"], "quote": e["quote"][:300]}
                                    for e in evidence_by_id.values()]
        critic_prompt = json.dumps({"task": task["prompt"], "requirements": model_requirements,
                                    "claims": claims, "relations": relations,
                                    "evidence_receipts": current_compact_evidence,
                                    "output_limits": {"requirement_updates": 8, "repair_instructions": 8,
                                                      "supplemental_queries": 8},
                                    "instruction": "Independently audit completeness, atomicity, fidelity, unsupported assertions, relation correctness, conflicts, and honest gaps. Return compact JSON with decision, requirement_updates, repair_instructions, supplemental_queries."}, ensure_ascii=False)
        critic = _model_call(sol, "You are an independent coverage critic. Do not use rubric or gold response. Return compact JSON only.", critic_prompt, 8000)
        if not critic["ok"]:
            return {"status": "ok", "requirements": requirements, "claims": claims, "relations": relations,
                    "evidence": list(evidence_by_id.values()), "retrieval_audit": audit,
                    "critic_status": "inconclusive", "critic_reason": critic["record"],
                    "repair_rounds": repair_round, "batch_failure_count": len(batch_failures)}, {"retrieval": audit, "proposal": value,
                                                     "critic_history": critic_history,
                                                     "repair_history": repair_history}
        critic_value = critic["value"] if isinstance(critic["value"], dict) else {}
        critic_history.append(critic_value)
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
    return {"status": "ok", "requirements": requirements, "claims": claims, "relations": relations,
            "evidence": list(evidence_by_id.values()), "retrieval_audit": audit,
            "critic_status": "insufficient_after_repairs", "critic": critic_history[-1],
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
    parser.add_argument("--critic-provider", default="openai")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--glm-reasoning", default="none")
    parser.add_argument("--critic-reasoning", default="low")
    parser.add_argument("--max-tasks", type=int, default=0)
    parser.add_argument("--exclude-task-id", action="append", default=[])
    parser.add_argument("--budget-usd", type=float, default=100.0)
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
    index = SectionIndex(catalog)
    private = out / "raw"
    glm = sol = None
    try:
        glm = Gateway(args.gateway_server, MODEL_ROLES["decomposition"], args.gateway_provider, out, args.timeout, args.glm_reasoning)
        sol = Gateway(args.gateway_server, MODEL_ROLES["coverage_critic"], args.critic_provider, out, args.timeout, args.critic_reasoning)
        def run(row: dict[str, Any]) -> tuple[str, dict[str, Any]]:
            decomposition, decomp_raw = _decompose(row, index, glm)
            if decomposition["status"] != "ok":
                result = {"task_id": row["task_id"], "task_name": row.get("task_name"), "status": "inconclusive", "decomposition": decomposition}
                _write_private(private / (row["task_id"] + ".json"), {"task": row, "decomposition": decomposition, "raw": decomp_raw})
                return row["task_id"], result
            construction, construct_raw = _construct(row, decomposition, index, glm, sol)
            construction_status = construction.get("status")
            critic_status = construction.get("critic_status")
            overall_status = "ok" if construction_status == "ok" and critic_status == "ok" else "inconclusive"
            result = {"task_id": row["task_id"], "task_name": row.get("task_name"), "status": overall_status,
                      "construction_status": construction_status,
                      "decomposition_requirement_count": len(decomposition["requirements"]),
                      "requirement_count": len(construction.get("requirements", [])),
                      "critic_added_requirement_count": sum(bool(row.get("critic_added")) for row in construction.get("requirements", [])),
                      "claim_count": len(construction.get("claims", [])), "relation_count": len(construction.get("relations", [])),
                      "evidence_count": len(construction.get("evidence", [])), "critic_status": critic_status,
                      "repair_rounds": construction.get("repair_rounds"),
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
        if sol: sol.stop()
    all_calls = (glm.calls if glm else []) + (sol.calls if sol else [])
    gateway_receipts = (glm.receipt_rows() if glm else []) + (sol.receipt_rows() if sol else [])
    numeric_costs = [float(r["cost_usd"]) for r in gateway_receipts if isinstance(r.get("cost_usd"), (int, float))]
    missing_receipt_costs = sum(not isinstance(r.get("cost_usd"), (int, float)) for r in gateway_receipts)
    latencies = sorted(float(r["latency_ms"]) for r in all_calls if isinstance(r.get("latency_ms"), (int, float)))
    def percentile(values: list[float], p: float) -> float | None:
        if not values:
            return None
        index = min(len(values) - 1, max(0, math.ceil(p * len(values)) - 1))
        return round(values[index], 3)
    report = {"schema_version": SCHEMA, "catalog_digest": catalog.get("catalog_digest"),
              "task_set_digest": digest([row["task_id"] for row in tasks]),
              "excluded_development_task_ids": sorted(excluded_task_ids),
              "source_count": len(catalog.get("sources", [])), "unique_source_uri_count": len(index.doc_meta),
              "section_count": len(index.sections),
              "models": MODEL_ROLES, "providers": {"glm": args.gateway_provider, "critic": args.critic_provider},
              "fallback": "forbidden", "tasks": [results[k] for k in sorted(results)],
              "denominators": {"tasks": len(tasks), "completed_construction": sum(r.get("status") == "ok" for r in results.values()),
                               "inconclusive_tasks": sum(r.get("status") != "ok" for r in results.values()),
                               "quality_metrics_with_frozen_silver_locators": 0},
              "telemetry": {"calls": len(all_calls), "ok_calls": sum(r.get("status") == "ok" for r in all_calls),
                            "inconclusive_calls": sum(r.get("status") != "ok" for r in all_calls),
                            "gateway_receipts": len(gateway_receipts),
                            "known_cost_usd": round(sum(numeric_costs), 8),
                            "cost_usd": round(sum(numeric_costs), 8) if not missing_receipt_costs and len(gateway_receipts) == len(all_calls) else None,
                            "latency_ms": {"p50": percentile(latencies, 0.50), "p95": percentile(latencies, 0.95)},
                            "cost_status": "ok" if not missing_receipt_costs and len(gateway_receipts) == len(all_calls) else "inconclusive_missing_call_cost",
                            "budget_usd": args.budget_usd,
                            "budget_status": "within" if not missing_receipt_costs and len(gateway_receipts) == len(all_calls) and sum(numeric_costs) <= args.budget_usd else "inconclusive"},
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
