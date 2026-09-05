#!/usr/bin/env python3
"""HTTP service for the single-owner Proofpress self-hosting reference."""
from __future__ import annotations

import argparse
import hashlib
from html import escape
import json
import mimetypes
import os
from pathlib import Path
import secrets
import sqlite3
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

from proofpress.kernel import operations as knowledge
from proofpress.hosted.control_plane import HostedAuthError, HostedControlPlane
from proofpress.hosted.mcp_http import handle_rpc


MAX_REQUEST_BYTES = 1024 * 1024
LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}


def _judge_demo_evidence(index, title, quote):
    quote_digest = "sha256:" + hashlib.sha256(quote.encode()).hexdigest()
    source_digest = "sha256:" + hashlib.sha256(
        f"proofpress-webmcp-demo:{index}:{title}".encode()).hexdigest()
    return {
        "schema_version": "proofpress/retrieval-evidence/v1",
        "source": {"uri": f"demo://acme-acquisition/source-{index}",
                   "content_digest": source_digest},
        "evidence": {"quote": quote, "locator": {
            "kind": "text_span", "start": 0, "end": len(quote),
            "text_digest": quote_digest}},
        "retrieval": {"adapter": "proofpress.synthetic-judge-demo", "version": "1",
                      "query": title, "config_digest": "sha256:" + "d" * 64},
    }


def seed_judge_demo(control, workspace_id, owner_principal, owner_name):
    """Create an isolated, visibly synthetic WebMCP judging workspace once."""
    bootstrap = control.bootstrap(workspace_id, owner_principal, owner_name)
    agent = control.issue_agent_credential(
        bootstrap["token"], "agent:demo-research", "Synthetic demo agent")

    def execute(token, operation, parameters, key):
        envelope = control.execute(token, {
            "schema_version": knowledge.LOCAL_OPERATION_SCHEMA,
            "operation": operation, "parameters": parameters,
            "idempotency_key": f"judge-demo-{key}",
        })
        if not envelope.get("ok"):
            raise ValueError(envelope.get("error", {}).get("message", "demo seed failed"))
        return envelope["result"]

    rows = [
        ("Acme's FY2024 revenue increased 18% year over year.", "The audited annual report records FY2024 revenue growth of 18% year over year.", "admit"),
        ("The acquisition agreement requires regulatory clearance before closing.", "Closing is conditioned on receipt of the specified regulatory clearances.", "admit"),
        ("Acme expects $120 million in cost synergies within 24 months.", "Management projects $120 million of run-rate cost synergies within 24 months.", None),
        ("Acme operates in 25 countries.", "The company website lists operations across 25 countries as of the retrieval date.", None),
        ("The target has no pending material litigation.", "The diligence summary says no material litigation was identified, subject to local-counsel confirmation.", "request_changes"),
        ("The transaction will close next week.", "The announcement states that timing remains subject to outstanding conditions.", "reject"),
        ("Customer concentration is below 10% for every account.", "The supplied schedule covers the top five accounts but omits the remaining customer population.", None),
        ("The data-security insurance cap is at least $25 million.", "The certificate shows a $25 million cyber-liability aggregate limit.", None),
    ]
    seeded = []
    for index, (statement, quote, decision) in enumerate(rows, 1):
        imported = execute(agent["token"], "evidence.submit", {
            "payload": _judge_demo_evidence(index, statement, quote)}, f"evidence-{index}")
        proposed = execute(agent["token"], "conclusion.propose", {
            "statement": statement, "evidence_refs": imported["evidence"],
            "scope": "demo:acme-acquisition", "proposer": "ignored",
            "artifact_refs": [],
            "qualifiers": {"synthetic_demo": True}}, f"conclusion-{index}")
        conclusion_id = proposed["conclusion"]["id"]
        execute(agent["token"], "conclusion.evaluate",
                {"conclusion_id": conclusion_id}, f"evaluate-{index}")
        if decision:
            execute(bootstrap["token"], "conclusion.review", {
                "conclusion_id": conclusion_id, "decision": decision,
                "reviewer": "ignored", "note": "Synthetic fixture state for WebMCP judging.",
                "request_id": f"judge-demo-review-{index}"}, f"review-{index}")
        seeded.append({"conclusion_id": conclusion_id,
                       "state": decision or "needs_review"})
    return {"workspace_id": workspace_id, "owner_principal": owner_principal,
            "owner_credential": bootstrap["token"],
            "recovery_secret": bootstrap["recovery_secret"], "seeded": seeded,
            "notice": "Synthetic judge demo only. Store owner and recovery secrets now; they are shown once."}


def _status_for(envelope):
    if envelope.get("ok"):
        return HTTPStatus.OK
    code = envelope.get("error", {}).get("code")
    if code == "invalid_credential":
        return HTTPStatus.UNAUTHORIZED
    if code == "operation_forbidden":
        return HTTPStatus.FORBIDDEN
    if code in {"ledger_head_conflict", "idempotency_conflict"}:
        return HTTPStatus.CONFLICT
    if code in {"operation_rejected", "resource_not_found"}:
        return HTTPStatus.UNPROCESSABLE_ENTITY
    if code in {"operation_io_error", "idempotency_store_invalid",
                "idempotency_store_write_failed"}:
        return HTTPStatus.INTERNAL_SERVER_ERROR
    return HTTPStatus.BAD_REQUEST


class HostedOperationHandler(BaseHTTPRequestHandler):
    server_version = "ProofpressHosted/0.1"

    def log_message(self, format, *args):
        event = {"level": "info", "event": "hosted_http_request",
                 "client": self.client_address[0], "message": format % args}
        print(json.dumps(event, separators=(",", ":")), file=sys.stderr,
              flush=True)

    def _json(self, status, value):
        body = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _token(self):
        header = self.headers.get("Authorization", "")
        return header[7:] if header.startswith("Bearer ") else ""

    def _base_url(self):
        configured = getattr(self.server, "proofpress_public_base_url", None)
        if configured:
            return configured
        proto = self.headers.get("X-Forwarded-Proto", "http").split(",", 1)[0]
        host = self.headers.get("X-Forwarded-Host") or self.headers.get("Host")
        return f"{proto}://{host}"

    def _mcp_resource(self):
        return self._base_url().rstrip("/") + "/mcp"

    def _mcp_unauthorized(self, message="MCP authorization is required"):
        body = json.dumps({"error": "invalid_token", "error_description": message}).encode()
        self.send_response(HTTPStatus.UNAUTHORIZED)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header(
            "WWW-Authenticate",
            f'Bearer resource_metadata="{self._base_url()}/.well-known/oauth-protected-resource", scope="proofpress:agent"')
        self.end_headers()
        self.wfile.write(body)

    def _request_json(self):
        if self.headers.get("Content-Type", "").split(";", 1)[0] != "application/json":
            raise HostedAuthError("unsupported_media_type",
                                  "content type must be application/json")
        try:
            length = int(self.headers.get("Content-Length", ""))
        except ValueError as exc:
            raise HostedAuthError("invalid_request", "content length required") from exc
        if length < 0 or length > self.server.proofpress_max_request_bytes:
            raise HostedAuthError("invalid_request", "invalid request length")
        try:
            value = json.loads(self.rfile.read(length))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise HostedAuthError("invalid_request", "invalid JSON") from exc
        if not isinstance(value, dict):
            raise HostedAuthError("invalid_request", "JSON body must be an object")
        return value

    def _owner_error(self, exc):
        status = HTTPStatus.UNAUTHORIZED if exc.code in {
            "invalid_credential", "owner_required"} else HTTPStatus.BAD_REQUEST
        return self._json(status, {"ok": False, "error": {
            "code": exc.code, "message": str(exc)}})

    def _html(self, status, value, *, cookie=None):
        body = value.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(body)

    def _form(self):
        content_type = self.headers.get("Content-Type", "").split(";", 1)[0]
        if content_type != "application/x-www-form-urlencoded":
            raise ValueError("form content type required")
        length = int(self.headers.get("Content-Length", "-1"))
        if length < 0 or length > 16 * 1024:
            raise ValueError("invalid form length")
        return {key: values[-1] for key, values in
                parse_qs(self.rfile.read(length).decode("utf-8"),
                         keep_blank_values=True).items()}

    def _owner_session(self):
        cookie = self.headers.get("Cookie", "")
        values = {}
        for item in cookie.split(";"):
            if "=" in item:
                key, value = item.strip().split("=", 1)
                values[key] = value
        return self.server.proofpress_owner_sessions.get(values.get("pp_owner", ""))

    @staticmethod
    def _page(title, body):
        return ("<!doctype html><html><head><meta charset=utf-8>"
                "<meta name=viewport content='width=device-width,initial-scale=1'>"
                f"<title>{escape(title)}</title><style>"
                "*{box-sizing:border-box}::selection{background:#e3eef0;color:#20222b}body{min-height:100vh;margin:0;display:grid;place-items:center;padding:24px;font:14px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#20222b;background:#faf9f5}"
                ".auth{width:min(100%,392px);border:1px solid #e3e1d9;border-radius:8px;background:#fff;padding:32px;box-shadow:0 18px 44px rgba(32,34,43,.055)}"
                ".brand{display:flex;align-items:center;gap:10px;margin-bottom:32px}.mark{display:grid;width:30px;height:30px;place-items:center;color:#20222b}.mark svg{display:block;width:30px;height:30px}"
                "h1{margin:0 0 9px;font:700 27px/1.2 Georgia,'Times New Roman',serif;letter-spacing:-.02em}.muted{margin:0 0 24px;color:#5a5d6b;font-size:13px}"
                "label{display:block;color:#20222b;font-size:12px;font-weight:600}input,textarea,button{font:inherit}input{width:100%;height:40px;margin-top:7px;border:1px solid #c9c7bf;border-radius:6px;padding:0 11px;color:#20222b;background:#fff;outline:none}input:focus{border-color:#0e5e6f;box-shadow:0 0 0 3px #e3eef0}button{width:100%;height:40px;margin-top:14px;border:0;border-radius:6px;background:#0e5e6f;color:#fff;font-weight:600;cursor:pointer}button:hover{background:#0a4b59}button:focus-visible{outline:2px solid #5fb3c4;outline-offset:2px}"
                "pre{white-space:pre-wrap;background:#f1efe8;padding:16px;border:1px solid #e3e1d9}.row{display:flex;gap:8px}</style></head><body>"
                f"{body}</body></html>")

    @staticmethod
    def _ui_asset():
        return Path(__file__).with_name("static") / "index.html"

    def _owner_ui(self, session):
        encoded = self._ui_asset().read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy",
                         "default-src 'none'; style-src 'self' 'unsafe-inline'; "
                         "script-src 'self'; connect-src 'self'; img-src 'self' data:; "
                         "form-action 'self'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(encoded)

    def _static_asset(self, path):
        root = Path(__file__).with_name("static").resolve()
        asset = (root / path.removeprefix("/")).resolve()
        if root not in asset.parents or not asset.is_file():
            return self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
        encoded = asset.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mimetypes.guess_type(asset.name)[0] or
                         "application/octet-stream")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "public, max-age=31536000, immutable"
                         if path.startswith("/assets/") else "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(encoded)

    def _owner_operation(self, session, operation, parameters=None):
        return self.server.proofpress_control.execute(session["token"], {
            "schema_version": knowledge.LOCAL_OPERATION_SCHEMA,
            "operation": operation, "parameters": parameters or {},
        })

    def _owner_api(self, parsed, session):
        path = parsed.path
        if path == "/owner/api/session":
            return self._json(HTTPStatus.OK, {"ok": True, "result": {
                "csrf": session["csrf"], "workspace": os.environ.get("PROOFPRESS_WORKSPACE_LABEL", "Proofpress internal"),
                "principal": "owner", "capabilities": {
                    "review": True, "credential_admin": True,
                    "assistant": bool(os.environ.get("OPENROUTER_API_KEY")),
                    "judge": self._owner_operation(session, "configuration.get")["result"]["judge"]["configured"],
                }}})
        if path == "/owner/api/review-policy":
            return self._json(HTTPStatus.OK, {"ok": True, "result": self.server.proofpress_control.get_review_policy(session["token"])})
        if path == "/owner/api/summary":
            envelope = self._owner_operation(
                session, "review.summary",
                {"scope": parse_qs(parsed.query).get("scope", [None])[-1]})
        elif path.startswith("/owner/api/conclusions/"):
            envelope = self._owner_operation(
                session, "review.receipt",
                {"conclusion_id": path.rsplit("/", 1)[-1]})
        elif path == "/owner/api/graph":
            envelope = self._owner_operation(
                session, "graph.get",
                {"scope": parse_qs(parsed.query).get("scope", [None])[-1]})
        elif path == "/owner/api/context":
            query = parse_qs(parsed.query)
            envelope = self._owner_operation(session, "context.get", {
                "scope": query.get("scope", [None])[-1],
                "task": query.get("task", [None])[-1],
                "include_blocked_statements": True,
            })
        elif path in {"/owner/api/activity", "/owner/api/technical-logs"}:
            try:
                limit = int(parse_qs(parsed.query).get("limit", ["100"])[-1])
                control = self.server.proofpress_control
                rows = (control.list_activity if path.endswith("/activity") else control.list_audit)(session["token"], limit)
            except ValueError:
                return self._json(HTTPStatus.BAD_REQUEST,
                                  {"error": "invalid_limit"})
            return self._json(HTTPStatus.OK,
                              {"ok": True, "result": rows})
        else:
            return self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
        return self._json(_status_for(envelope), envelope)

    def _login_page(self, message=""):
        note = f"<p style='color:#b91c1c'>{escape(message)}</p>" if message else ""
        logo = ("<svg viewBox='0 0 48 48' fill='none' aria-hidden='true'>"
                "<rect x='7' y='4' width='28' height='36' stroke='currentColor' stroke-width='3'/>"
                "<circle cx='35' cy='36' r='9' fill='#2E8FA3'/></svg>")
        return self._page("Proofpress owner sign in", "<main class=auth><div class=brand><span class=mark>" + logo + "</span><strong>Proofpress</strong></div><h1>Owner workspace</h1>" + note +
            "<p class=muted>Sign in to review what agents may rely on. Your credential stays in an HttpOnly session and never enters the URL.</p>"
            "<form method=post action=/owner/login><label>Owner credential<br>"
            "<input type=password name=token required autocomplete=current-password></label><br>"
            "<button type=submit>Continue</button></form></main>")

    def _authorize_page(self, query, message=""):
        note = f"<p style='color:#b91c1c'>{escape(message)}</p>" if message else ""
        hidden = "".join(
            f"<input type=hidden name='{escape(key)}' value='{escape(str(value))}'>"
            for key, value in query.items())
        return self._page("Connect Proofpress", "<main class=auth><div class=brand>"
            "<strong>Proofpress</strong></div><h1>Connect this agent</h1>" + note +
            "<p class=muted>Paste the credential issued for this specific agent. "
            "Owner and recovery credentials are rejected. The MCP client receives a short-lived, revocable session.</p>"
            "<form method=post action=/authorize>" + hidden +
            "<label>Agent credential<br><input type=password name=agent_token required autocomplete=current-password></label>"
            "<button type=submit>Authorize agent</button></form></main>")

    def _review_page(self, conclusion_id, session):
        control = self.server.proofpress_control
        if conclusion_id:
            envelope = control.execute(session["token"], {
                "schema_version": knowledge.LOCAL_OPERATION_SCHEMA,
                "operation": "review.receipt",
                "parameters": {"conclusion_id": conclusion_id},
            })
            if not envelope.get("ok"):
                return self._page("Review unavailable", "<h1>Review unavailable</h1><pre>" +
                                  escape(json.dumps(envelope, ensure_ascii=False, indent=2)) + "</pre>")
            receipt = envelope["result"]
            decision = ""
            if receipt["state"] == "needs_review":
                decision = ("<form method=post action=/owner/review>"
                    f"<input type=hidden name=csrf value='{escape(session['csrf'])}'>"
                    f"<input type=hidden name=conclusion_id value='{escape(conclusion_id)}'>"
                    "<label>Review note<br><textarea name=note rows=3 cols=60></textarea></label>"
                    "<div class=row><button name=decision value=admit>Admit</button>"
                    "<button name=decision value=reject>Reject</button></div></form>")
            return self._page("Review conclusion", "<p><a href=/review>All conclusions</a></p>"
                f"<h1>{escape(receipt['conclusion']['statement'])}</h1>"
                f"<p>State: <strong>{escape(receipt['state'])}</strong></p>"
                "<h2>Evidence and receipts</h2><pre>" +
                escape(json.dumps(receipt, ensure_ascii=False, indent=2)) + "</pre>" + decision)
        graph = control.execute(session["token"], {
            "schema_version": knowledge.LOCAL_OPERATION_SCHEMA,
            "operation": "graph.get", "parameters": {},
        })
        nodes = graph.get("result", {}).get("nodes", []) if graph.get("ok") else []
        conclusions = [row for row in nodes if row.get("type") == "conclusion"]
        items = "".join("<li><a href='/review?" + urlencode({"conclusion_id": row["id"]}) +
                        "'>" + escape(row.get("label", row["id"])) + "</a> — " +
                        escape(row.get("state", "unknown")) + "</li>" for row in conclusions)
        return self._page("Proofpress reviews", "<h1>Governed knowledge review</h1><ul>" +
                          (items or "<li>No conclusions yet.</li>") + "</ul>")

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/.well-known/oauth-protected-resource":
            return self._json(HTTPStatus.OK, {
                "resource": self._mcp_resource(),
                "authorization_servers": [self._base_url()],
                "scopes_supported": ["proofpress:agent"],
                "bearer_methods_supported": ["header"],
            })
        if path == "/.well-known/oauth-authorization-server":
            base = self._base_url()
            return self._json(HTTPStatus.OK, {
                "issuer": base, "authorization_endpoint": base + "/authorize",
                "token_endpoint": base + "/token",
                "registration_endpoint": base + "/register",
                "response_types_supported": ["code"],
                "grant_types_supported": ["authorization_code", "refresh_token"],
                "token_endpoint_auth_methods_supported": ["none"],
                "code_challenge_methods_supported": ["S256"],
                "scopes_supported": ["proofpress:agent"],
            })
        if path == "/authorize":
            query = {key: values[-1] for key, values in
                     parse_qs(parsed.query, keep_blank_values=True).items()}
            required = {"response_type", "client_id", "redirect_uri", "state",
                        "code_challenge", "code_challenge_method", "resource"}
            try:
                if not required <= query.keys() or query["response_type"] != "code":
                    raise ValueError("A complete authorization-code request is required.")
                if query["code_challenge_method"] != "S256":
                    raise ValueError("PKCE S256 is required.")
                if query["resource"] != self._mcp_resource():
                    raise ValueError("The requested MCP resource does not match this server.")
                self.server.proofpress_control.validate_oauth_client(
                    query["client_id"], query["redirect_uri"])
            except (ValueError, HostedAuthError) as exc:
                return self._html(HTTPStatus.BAD_REQUEST,
                                  self._authorize_page(query, str(exc)))
            return self._html(HTTPStatus.OK, self._authorize_page(query))
        if path == "/connect":
            endpoint = escape(self._mcp_resource())
            return self._html(HTTPStatus.OK, self._page(
                "Connect Proofpress", "<main class=auth><h1>Connect an agent</h1>"
                "<p class=muted>Add this remote Streamable HTTP MCP URL to your client. "
                "The client will open a browser to authorize the agent.</p>"
                f"<pre>{endpoint}</pre><p>No local server or repository checkout is required.</p></main>"))
        if path == "/mcp":
            return self._json(HTTPStatus.METHOD_NOT_ALLOWED, {
                "error": "streamable_http_get_not_supported",
                "message": "This stateless MCP endpoint accepts POST requests."})
        if path == "/healthz":
            return self._json(HTTPStatus.OK, {"status": "ok"})
        if path == "/readyz":
            connection = sqlite3.connect(self.server.proofpress_control.database)
            try:
                integrity = connection.execute("PRAGMA quick_check").fetchone()[0]
                migration = connection.execute(
                    "SELECT MAX(version) FROM schema_migrations").fetchone()[0]
            finally:
                connection.close()
            status = HTTPStatus.OK if integrity == "ok" and migration == 1 else \
                HTTPStatus.SERVICE_UNAVAILABLE
            return self._json(status, {
                "status": "ready" if status == HTTPStatus.OK else "not_ready",
                "contract": knowledge.LOCAL_OPERATION_SCHEMA,
                "database_integrity": integrity,
                "schema_version": migration,
            })
        if path == "/v1/capabilities":
            envelope = self.server.proofpress_control.execute(self._token(), {
                "schema_version": knowledge.LOCAL_OPERATION_SCHEMA,
                "operation": "capabilities.get", "parameters": {},
            })
            return self._json(_status_for(envelope), envelope)
        if path == "/v1/owner/credentials":
            try:
                session = self._owner_session()
                credentials = self.server.proofpress_control.list_credentials(
                    session["token"] if session else self._token())
            except HostedAuthError as exc:
                return self._owner_error(exc)
            return self._json(HTTPStatus.OK, {
                "ok": True, "credentials": credentials})
        if path.startswith("/owner/api/"):
            session = self._owner_session()
            if not session:
                return self._json(HTTPStatus.UNAUTHORIZED,
                                  {"ok": False, "error": {
                                      "code": "owner_session_required",
                                      "message": "Sign in as the workspace owner."}})
            return self._owner_api(parsed, session)
        if path.startswith("/assets/") or path == "/logo.svg":
            return self._static_asset(path)
        if path in {"/", "/home", "/review", "/ledger", "/activity", "/admin"}:
            session = self._owner_session()
            if not session:
                return self._html(HTTPStatus.UNAUTHORIZED, self._login_page())
            return self._owner_ui(session)
        return self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/register":
            try:
                request = self._request_json()
                result = self.server.proofpress_control.register_oauth_client(
                    str(request.get("client_name") or "MCP client"),
                    request.get("redirect_uris") or [])
            except (HostedAuthError, ValueError, TypeError) as exc:
                return self._json(HTTPStatus.BAD_REQUEST, {
                    "error": "invalid_client_metadata",
                    "error_description": str(exc)})
            return self._json(HTTPStatus.CREATED, {
                **result, "client_id_issued_at": int(__import__("time").time())})
        if path == "/authorize":
            try:
                form = self._form()
                public = {key: value for key, value in form.items()
                          if key != "agent_token"}
                if form.get("response_type") != "code" or form.get(
                        "code_challenge_method") != "S256":
                    raise HostedAuthError("invalid_request", "PKCE S256 is required")
                if form.get("resource") != self._mcp_resource():
                    raise HostedAuthError("invalid_target", "MCP resource mismatch")
                code = self.server.proofpress_control.create_oauth_code(
                    form.get("agent_token", ""), form.get("client_id", ""),
                    form.get("redirect_uri", ""), form.get("resource", ""),
                    form.get("code_challenge", ""))
                location = form["redirect_uri"] + ("&" if "?" in form["redirect_uri"] else "?") + urlencode({
                    "code": code, "state": form.get("state", "")})
            except (HostedAuthError, ValueError, UnicodeDecodeError) as exc:
                return self._html(HTTPStatus.UNAUTHORIZED,
                                  self._authorize_page(public if 'public' in locals() else {}, str(exc)))
            self.send_response(HTTPStatus.SEE_OTHER)
            self.send_header("Location", location)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return
        if path == "/token":
            try:
                form = self._form()
                grant = form.get("grant_type")
                if grant == "authorization_code":
                    result = self.server.proofpress_control.exchange_oauth_code(
                        form.get("code", ""), form.get("client_id", ""),
                        form.get("redirect_uri", ""), form.get("resource", ""),
                        form.get("code_verifier", ""))
                elif grant == "refresh_token":
                    result = self.server.proofpress_control.refresh_oauth_token(
                        form.get("refresh_token", ""), form.get("client_id", ""),
                        form.get("resource", ""))
                else:
                    raise HostedAuthError("unsupported_grant_type", "unsupported grant type")
            except (HostedAuthError, ValueError, UnicodeDecodeError) as exc:
                return self._json(HTTPStatus.BAD_REQUEST, {
                    "error": getattr(exc, "code", "invalid_request"),
                    "error_description": str(exc)})
            return self._json(HTTPStatus.OK, result)
        if path == "/mcp":
            token = self._token()
            try:
                context = self.server.proofpress_control.authenticate_oauth_access(
                    token, self._mcp_resource())
            except HostedAuthError as exc:
                return self._mcp_unauthorized(str(exc))
            try:
                request = self._request_json()
            except HostedAuthError as exc:
                return self._json(HTTPStatus.BAD_REQUEST, {
                    "jsonrpc": "2.0", "id": None,
                    "error": {"code": -32700, "message": str(exc)}})
            response = handle_rpc(
                self.server.proofpress_control, context, request,
                self._base_url())
            if response is None:
                self.send_response(HTTPStatus.ACCEPTED)
                self.send_header("Content-Length", "0")
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                return
            return self._json(HTTPStatus.OK, response)
        if path in {"/owner/api/review-policy", "/owner/api/evaluate"}:
            session = self._owner_session()
            if not session:
                return self._json(HTTPStatus.UNAUTHORIZED, {"error": "owner_session_required"})
            try:
                request = self._request_json()
                if not secrets.compare_digest(str(request.get("csrf") or ""), session["csrf"]):
                    return self._json(HTTPStatus.FORBIDDEN, {"error": "csrf_failed"})
                if path.endswith("/evaluate"):
                    envelope = self._owner_operation(session, "conclusion.evaluate", {"conclusion_id": request.get("conclusion_id", "")})
                    return self._json(_status_for(envelope), envelope)
                result = self.server.proofpress_control.save_review_policy(
                    session["token"], request.get("settings"), request.get("expected_version"),
                    request.get("api_key"), request.get("delete_key") is True)
                return self._json(HTTPStatus.OK, {"ok": True, "result": result})
            except HostedAuthError as exc:
                return self._owner_error(exc)
            except ValueError as exc:
                return self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": {"code": "invalid_policy", "message": str(exc)}})
        if path == "/owner/api/judge":
            session = self._owner_session()
            if not session:
                return self._json(HTTPStatus.UNAUTHORIZED, {"error": "owner_session_required"})
            try:
                request = self._request_json()
            except HostedAuthError as exc:
                return self._owner_error(exc)
            if not secrets.compare_digest(str(request.get("csrf") or ""), session["csrf"]):
                return self._json(HTTPStatus.FORBIDDEN, {"error": "csrf_failed"})
            if request.get("confirmed") is not True:
                return self._json(HTTPStatus.BAD_REQUEST, {"error": "Confirm sending bound evidence to the configured judge."})
            envelope = self._owner_operation(session, "conclusion.judge", {
                "conclusion_id": request.get("conclusion_id", "")})
            return self._json(_status_for(envelope), envelope)
        if path == "/owner/api/ask":
            session = self._owner_session()
            if not session:
                return self._json(HTTPStatus.UNAUTHORIZED,
                                  {"ok": False, "error": {
                                      "code": "owner_session_required",
                                      "message": "Sign in as the workspace owner."}})
            try:
                request = self._request_json()
            except HostedAuthError as exc:
                return self._owner_error(exc)
            if not secrets.compare_digest(str(request.get("csrf") or ""), session["csrf"]):
                return self._json(HTTPStatus.FORBIDDEN,
                                  {"ok": False, "error": {
                                      "code": "csrf_failed",
                                      "message": "Refresh the page and try again."}})
            from proofpress.hosted import assistant
            result = assistant.ask(request.get("question", ""), request.get("snapshot") or {})
            status = HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST
            if result.get("error", {}).get("code") == "assistant_unconfigured":
                status = HTTPStatus.SERVICE_UNAVAILABLE
            elif result.get("error", {}).get("code") in {"assistant_upstream", "assistant_unavailable"}:
                status = HTTPStatus.BAD_GATEWAY
            return self._json(status, result)
        if path == "/owner/api/reviews":
            session = self._owner_session()
            if not session:
                return self._json(HTTPStatus.UNAUTHORIZED,
                                  {"ok": False, "error": {
                                      "code": "owner_session_required",
                                      "message": "Sign in as the workspace owner."}})
            try:
                request = self._request_json()
            except HostedAuthError as exc:
                return self._owner_error(exc)
            if not secrets.compare_digest(request.get("csrf", ""), session["csrf"]):
                return self._json(HTTPStatus.FORBIDDEN,
                                  {"ok": False, "error": {
                                      "code": "csrf_failed",
                                      "message": "Refresh the page and try again."}})
            decision = request.get("decision")
            if decision not in {"admit", "reject", "request_changes"}:
                return self._json(HTTPStatus.BAD_REQUEST,
                                  {"ok": False, "error": {
                                      "code": "invalid_decision",
                                      "message": "Decision must be admit, reject, or request_changes."}})
            envelope = self._owner_operation(session, "conclusion.review", {
                "conclusion_id": request.get("conclusion_id", ""),
                "decision": decision, "reviewer": "server-derived",
                "note": request.get("note") or None,
                "request_id": "web-" + secrets.token_hex(12),
                "expected_head": request.get("expected_head"),
            })
            if not envelope.get("ok"):
                return self._json(_status_for(envelope), envelope)
            receipt = self._owner_operation(session, "review.receipt", {
                "conclusion_id": request.get("conclusion_id", "")})
            return self._json(_status_for(receipt), receipt)
        if path == "/v1/owner/credentials":
            try:
                request = self._request_json()
                action = request.get("action")
                control = self.server.proofpress_control
                session = self._owner_session()
                if session and not secrets.compare_digest(
                        str(request.get("csrf") or ""), session["csrf"]):
                    return self._json(HTTPStatus.FORBIDDEN, {"ok": False,
                        "error": {"code": "csrf_failed",
                                  "message": "Refresh the page and try again."}})
                owner_token = session["token"] if session else self._token()
                if action == "issue":
                    result = control.issue_agent_credential(
                        owner_token, request.get("principal_id", ""),
                        request.get("label", ""), request.get("display_name"))
                elif action == "rotate":
                    result = control.rotate_agent_credential(
                        owner_token, request.get("credential_id", ""),
                        request.get("label"))
                elif action == "revoke":
                    control.revoke_credential(
                        owner_token, request.get("credential_id", ""))
                    result = {"revoked": request.get("credential_id")}
                else:
                    raise HostedAuthError(
                        "invalid_request", "action must be issue, rotate, or revoke")
            except HostedAuthError as exc:
                return self._owner_error(exc)
            except ValueError as exc:
                return self._json(HTTPStatus.BAD_REQUEST, {"ok": False,
                    "error": {"code": "operation_rejected", "message": str(exc)}})
            return self._json(HTTPStatus.OK, {"ok": True, "result": result})
        if path == "/owner/login":
            try:
                form = self._form()
                context = self.server.proofpress_control.authenticate(form.get("token", ""))
                if context.role != "owner":
                    raise ValueError("owner credential required")
            except (ValueError, UnicodeDecodeError):
                return self._html(HTTPStatus.UNAUTHORIZED,
                                  self._login_page("That owner credential was not accepted."))
            session_id = secrets.token_urlsafe(32)
            self.server.proofpress_owner_sessions[session_id] = {
                "token": form["token"], "csrf": secrets.token_urlsafe(24)}
            cookie = (f"pp_owner={session_id}; Path=/; HttpOnly; SameSite=Strict"
                      + ("; Secure" if self.headers.get("X-Forwarded-Proto") == "https" else ""))
            self.send_response(HTTPStatus.SEE_OTHER)
            self.send_header("Location", "/home")
            self.send_header("Set-Cookie", cookie)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return
        if path == "/owner/review":
            session = self._owner_session()
            if not session:
                return self._html(HTTPStatus.UNAUTHORIZED, self._login_page())
            try:
                form = self._form()
            except (ValueError, UnicodeDecodeError):
                return self._json(HTTPStatus.BAD_REQUEST, {"error": "invalid_form"})
            if not secrets.compare_digest(form.get("csrf", ""), session["csrf"]):
                return self._json(HTTPStatus.FORBIDDEN, {"error": "csrf_failed"})
            conclusion_id = form.get("conclusion_id", "")
            decision = form.get("decision", "")
            if decision not in {"admit", "reject", "request_changes"}:
                return self._json(HTTPStatus.BAD_REQUEST, {"error": "invalid_decision"})
            envelope = self.server.proofpress_control.execute(session["token"], {
                "schema_version": knowledge.LOCAL_OPERATION_SCHEMA,
                "operation": "conclusion.review",
                "parameters": {"conclusion_id": conclusion_id,
                               "decision": decision,
                               "reviewer": "server-derived",
                               "note": form.get("note") or None,
                               "request_id": "web-" + secrets.token_hex(12)},
            })
            if not envelope.get("ok"):
                return self._json(_status_for(envelope), envelope)
            self.send_response(HTTPStatus.SEE_OTHER)
            self.send_header("Location", "/review?" + urlencode({"conclusion_id": conclusion_id}))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return
        if path != "/v1/operations":
            return self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
        if self.headers.get("Content-Type", "").split(";", 1)[0] != "application/json":
            return self._json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                              {"error": "content_type_must_be_application_json"})
        try:
            length = int(self.headers.get("Content-Length", ""))
        except ValueError:
            length = -1
        if length < 0:
            return self._json(HTTPStatus.LENGTH_REQUIRED,
                              {"error": "content_length_required"})
        if length > self.server.proofpress_max_request_bytes:
            return self._json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                              {"error": "request_too_large"})
        try:
            request = json.loads(self.rfile.read(length))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return self._json(HTTPStatus.BAD_REQUEST, {"error": "invalid_json"})
        envelope = self.server.proofpress_control.execute(self._token(), request)
        return self._json(_status_for(envelope), envelope)


def create_hosted_server(database, host="127.0.0.1", port=7334,
                         max_request_bytes=MAX_REQUEST_BYTES,
                         allow_public_bind=False, public_base_url=None):
    if host not in LOOPBACK_HOSTS and not allow_public_bind:
        raise ValueError(
            "hosted origin binds loopback only; terminate public HTTPS at a same-host reverse proxy")
    control = HostedControlPlane(database)
    server = ThreadingHTTPServer((host, port), HostedOperationHandler)
    server.proofpress_control = control
    server.proofpress_max_request_bytes = max_request_bytes
    server.proofpress_owner_sessions = {}
    configured_url = (public_base_url or os.environ.get("PROOFPRESS_PUBLIC_BASE_URL")
                      or os.environ.get("RENDER_EXTERNAL_URL"))
    if configured_url:
        parsed = urlparse(configured_url)
        if (parsed.scheme not in {"http", "https"} or not parsed.hostname
                or parsed.path not in {"", "/"} or parsed.query or parsed.fragment):
            raise ValueError("public base URL must be an absolute HTTP(S) origin")
        server.proofpress_public_base_url = configured_url.rstrip("/")
    else:
        server.proofpress_public_base_url = None
    control.resume_judge_jobs()
    return server


def _owner_token(args):
    token = os.environ.get(args.owner_token_env)
    if not token:
        raise SystemExit(f"missing owner credential in {args.owner_token_env}")
    return token


def main(argv=None):
    parser = argparse.ArgumentParser(prog="proofpress hosted")
    parser.add_argument("--database")
    subparsers = parser.add_subparsers(dest="command", required=True)
    bootstrap = subparsers.add_parser("bootstrap")
    bootstrap.add_argument("--workspace-id", required=True)
    bootstrap.add_argument("--owner-principal", required=True)
    bootstrap.add_argument("--owner-name", default="Owner")
    demo = subparsers.add_parser("seed-judge-demo")
    demo.add_argument("--workspace-id", default="workspace:webmcp-judge-demo")
    demo.add_argument("--owner-principal", default="human:webmcp-judge")
    demo.add_argument("--owner-name", default="WebMCP Judge")
    issue = subparsers.add_parser("issue-agent")
    issue.add_argument("--principal", required=True)
    issue.add_argument("--label", required=True)
    issue.add_argument("--owner-token-env", default="PROOFPRESS_OWNER_TOKEN")
    revoke = subparsers.add_parser("revoke")
    revoke.add_argument("credential_id")
    revoke.add_argument("--owner-token-env", default="PROOFPRESS_OWNER_TOKEN")
    rotate = subparsers.add_parser("rotate-agent")
    rotate.add_argument("credential_id")
    rotate.add_argument("--label")
    rotate.add_argument("--owner-token-env", default="PROOFPRESS_OWNER_TOKEN")
    recover = subparsers.add_parser("recover-owner")
    recover.add_argument("--workspace-id", required=True)
    recover.add_argument("--recovery-secret-env",
                         default="PROOFPRESS_RECOVERY_SECRET")
    backup = subparsers.add_parser("backup")
    backup.add_argument("target")
    backup.add_argument("--workspace-id", required=True)
    export = subparsers.add_parser("export")
    export.add_argument("--workspace-id", required=True)
    verify_export = subparsers.add_parser("verify-export")
    verify_export.add_argument("file")
    serve = subparsers.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int,
                       default=int(os.environ.get("PORT", "7334")))
    serve.add_argument(
        "--allow-public-bind", action="store_true",
        help="allow a platform-private 0.0.0.0 bind; the platform must terminate HTTPS")
    args = parser.parse_args(argv)
    if args.command == "verify-export":
        from proofpress.kernel.events import verify_history_envelopes
        bundle = json.loads(Path(args.file).read_text(encoding="utf-8"))
        if bundle.get("schema_version") != "proofpress/history-export/v1alpha1":
            raise SystemExit("unsupported history export schema")
        result = verify_history_envelopes(bundle.get("events", []))
        print(json.dumps(result, ensure_ascii=False))
        if not result["ok"]:
            raise SystemExit(1)
        return
    if not args.database:
        parser.error("--database is required for this command")
    control = HostedControlPlane(args.database)
    if args.command == "bootstrap":
        result = control.bootstrap(
            args.workspace_id, args.owner_principal, args.owner_name)
        print(json.dumps(result, ensure_ascii=False))
    elif args.command == "seed-judge-demo":
        print(json.dumps(seed_judge_demo(
            control, args.workspace_id, args.owner_principal, args.owner_name),
            ensure_ascii=False))
    elif args.command == "issue-agent":
        result = control.issue_agent_credential(
            _owner_token(args), args.principal, args.label)
        print(json.dumps(result, ensure_ascii=False))
    elif args.command == "revoke":
        control.revoke_credential(_owner_token(args), args.credential_id)
        print(json.dumps({"revoked": args.credential_id}))
    elif args.command == "rotate-agent":
        print(json.dumps(control.rotate_agent_credential(
            _owner_token(args), args.credential_id, args.label), ensure_ascii=False))
    elif args.command == "recover-owner":
        recovery_secret = os.environ.get(args.recovery_secret_env)
        if not recovery_secret:
            raise SystemExit(
                f"missing recovery secret in {args.recovery_secret_env}")
        print(json.dumps(control.recover_owner(
            args.workspace_id, recovery_secret), ensure_ascii=False))
    elif args.command == "backup":
        from proofpress.kernel.events import SQLiteEventStore
        path = SQLiteEventStore(
            args.database, args.workspace_id).backup_to(args.target)
        print(json.dumps({"backup": str(path)}))
    elif args.command == "export":
        from proofpress.kernel.events import SQLiteEventStore
        print(json.dumps(SQLiteEventStore(
            args.database, args.workspace_id).export_bundle(), ensure_ascii=False))
    else:
        server = create_hosted_server(
            args.database, args.host, args.port,
            allow_public_bind=args.allow_public_bind)
        print(json.dumps({"event": "hosted_service_ready", "host": args.host,
                          "port": server.server_port}), flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()


if __name__ == "__main__":
    main()
