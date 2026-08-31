#!/usr/bin/env python3
"""Loopback-only HTTP transport for the Proofpress local operation contract."""
from __future__ import annotations

import hmac
import json
import os
import subprocess
import sys
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import proofpress_knowledge as knowledge


MAX_REQUEST_BYTES = 1024 * 1024
LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}
_WRITE_LOCK = threading.Lock()


def validate_workspace(workspace):
    root = Path(workspace).resolve()
    if not root.is_dir():
        raise ValueError("service workspace must be an existing directory")
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        text=True, capture_output=True)
    if result.returncode:
        raise ValueError("service workspace must be a Git repository")
    if Path(result.stdout.strip()).resolve() != root:
        raise ValueError("service workspace must be the Git repository root")
    runtime = root / ".proofpress" / "runtime"
    runtime.mkdir(parents=True, exist_ok=True)
    probe = runtime / ".write-probe"
    try:
        probe.write_text("ready", encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        raise ValueError("service workspace runtime directory is not writable") from exc
    return root


def _status_for(envelope):
    if envelope.get("ok"):
        return HTTPStatus.OK
    code = envelope.get("error", {}).get("code")
    if code in {"ledger_head_conflict", "idempotency_conflict"}:
        return HTTPStatus.CONFLICT
    if code in {"operation_rejected", "resource_not_found"}:
        return HTTPStatus.UNPROCESSABLE_ENTITY
    if code in {"operation_io_error", "idempotency_store_invalid",
                "idempotency_store_write_failed"}:
        return HTTPStatus.INTERNAL_SERVER_ERROR
    return HTTPStatus.BAD_REQUEST


def _service_transport(envelope):
    if (envelope.get("ok") and envelope.get("operation") == "capabilities.get"):
        result = dict(envelope["result"])
        result["transport"] = "localhost_http"
        result["not_available"] = [item for item in result["not_available"]
                                   if item != "localhost_http"]
        envelope = {**envelope, "result": result}
    return envelope


class LocalOperationHandler(BaseHTTPRequestHandler):
    server_version = "ProofpressLocal/0.1"

    def log_message(self, format, *args):
        event = {"level": "info", "event": "http_request",
                 "client": self.client_address[0], "message": format % args}
        print(json.dumps(event, separators=(",", ":")), file=sys.stderr,
              flush=True)

    def _json(self, status, value):
        body = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self):
        header = self.headers.get("Authorization", "")
        supplied = header[7:] if header.startswith("Bearer ") else ""
        return hmac.compare_digest(supplied, self.server.proofpress_token)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/healthz":
            return self._json(HTTPStatus.OK, {"status": "ok"})
        if path == "/readyz":
            return self._json(HTTPStatus.OK, {
                "status": "ready",
                "workspace": str(self.server.proofpress_workspace),
                "contract": knowledge.LOCAL_OPERATION_SCHEMA,
            })
        if path == "/v1/capabilities":
            if not self._authorized():
                return self._json(HTTPStatus.UNAUTHORIZED,
                                  {"error": "unauthorized"})
            envelope = knowledge.execute_local_operation({
                "schema_version": knowledge.LOCAL_OPERATION_SCHEMA,
                "operation": "capabilities.get", "parameters": {},
            })
            envelope = _service_transport(envelope)
            return self._json(_status_for(envelope), envelope)
        self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_POST(self):
        if urlparse(self.path).path != "/v1/operations":
            return self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
        if not self._authorized():
            return self._json(HTTPStatus.UNAUTHORIZED,
                              {"error": "unauthorized"})
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
        with _WRITE_LOCK:
            envelope = knowledge.execute_local_operation(request)
        envelope = _service_transport(envelope)
        self._json(_status_for(envelope), envelope)


def create_local_server(workspace, token, host="127.0.0.1", port=7332,
                        max_request_bytes=MAX_REQUEST_BYTES):
    if host not in LOOPBACK_HOSTS:
        raise ValueError("local service only supports loopback hosts")
    if not isinstance(token, str) or len(token) < 16:
        raise ValueError("local service token must contain at least 16 characters")
    root = validate_workspace(workspace)
    if Path.cwd().resolve() != root:
        raise ValueError("service process working directory must equal --workspace")
    server = ThreadingHTTPServer((host, port), LocalOperationHandler)
    server.proofpress_token = token
    server.proofpress_workspace = root
    server.proofpress_max_request_bytes = max_request_bytes
    return server


def serve(workspace, token, host="127.0.0.1", port=7332):
    root = validate_workspace(workspace)
    os.chdir(root)
    server = create_local_server(root, token, host, port)
    ready = {"event": "service_ready", "host": host,
             "port": server.server_port, "workspace": str(root)}
    print(json.dumps(ready, separators=(",", ":")), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def run_from_args(args):
    token = os.environ.get(args.token_env)
    if not token:
        raise ValueError("local service token environment variable is not set")
    serve(args.workspace, token, args.host, args.port)
