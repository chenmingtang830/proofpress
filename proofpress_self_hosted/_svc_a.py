#!/usr/bin/env python3
"""HTTP service for the single-owner Proofpress self-hosting reference."""
from __future__ import annotations

import argparse
from html import escape
import json
import os
from pathlib import Path
import secrets
import sqlite3
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

import proofpress_knowledge as knowledge
from proofpress_self_hosted.control_plane import HostedAuthError, HostedControlPlane


MAX_REQUEST_BYTES = 1024 * 1024
LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}


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
                "body{max-width:760px;margin:48px auto;padding:0 20px;font:16px/1.5 system-ui;color:#171717}"
                "pre{white-space:pre-wrap;background:#f5f1e8;padding:16px;border:1px solid #d8d0c2}"
                "input,textarea,button{font:inherit;padding:9px;margin:4px 0}button{cursor:pointer}"
                ".row{display:flex;gap:8px}.muted{color:#666}</style></head><body>"
                f"{body}</body></html>")

    @staticmethod
    def _ui_asset():
        return Path(__file__).with_name("owner_ui.html")

    def _owner_ui(self, session):
        nonce = secrets.token_urlsafe(18)
        body = (self._ui_asset().read_text(encoding="utf-8")
                .replace("__PROOFPRESS_CSRF__", session["csrf"])
                .replace("__PROOFPRESS_NONCE__", nonce))
        encoded = body.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy",
                         "default-src 'none'; style-src 'unsafe-inline'; "
                         f"script-src 'nonce-{nonce}'; connect-src 'self'; "
                         "form-action 'self'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(encoded)

    def _owner_operation(self, session, operation, parameters=None):
        return self.server.proofpress_control.execute(session["token"], {
            "schema_version": knowledge.LOCAL_OPERATION_SCHEMA,
            "operation": operation, "parameters": parameters or {},
        })

    def _owner_api(self, parsed, session):
        path = parsed.path
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
