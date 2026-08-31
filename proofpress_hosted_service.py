#!/usr/bin/env python3
"""Loopback origin service for the personal hosted Proofpress alpha."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sqlite3
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

import proofpress_knowledge as knowledge
from proofpress_hosted import HostedControlPlane


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

    def do_GET(self):
        path = urlparse(self.path).path
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
        return self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_POST(self):
        if urlparse(self.path).path != "/v1/operations":
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
                         max_request_bytes=MAX_REQUEST_BYTES):
    if host not in LOOPBACK_HOSTS:
        raise ValueError(
            "hosted origin binds loopback only; terminate public HTTPS at a same-host reverse proxy")
    control = HostedControlPlane(database)
    server = ThreadingHTTPServer((host, port), HostedOperationHandler)
    server.proofpress_control = control
    server.proofpress_max_request_bytes = max_request_bytes
    return server


def _owner_token(args):
    token = os.environ.get(args.owner_token_env)
    if not token:
        raise SystemExit(f"missing owner credential in {args.owner_token_env}")
    return token


def main(argv=None):
    parser = argparse.ArgumentParser(prog="proofpress-hosted")
    parser.add_argument("--database")
    subparsers = parser.add_subparsers(dest="command", required=True)
    bootstrap = subparsers.add_parser("bootstrap")
    bootstrap.add_argument("--workspace-id", required=True)
    bootstrap.add_argument("--owner-principal", required=True)
    bootstrap.add_argument("--owner-name", default="Owner")
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
    serve.add_argument("--port", type=int, default=7334)
    args = parser.parse_args(argv)
    if args.command == "verify-export":
        from proofpress_event_store import verify_history_envelopes
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
        from proofpress_event_store import SQLiteEventStore
        path = SQLiteEventStore(
            args.database, args.workspace_id).backup_to(args.target)
        print(json.dumps({"backup": str(path)}))
    elif args.command == "export":
        from proofpress_event_store import SQLiteEventStore
        print(json.dumps(SQLiteEventStore(
            args.database, args.workspace_id).export_bundle(), ensure_ascii=False))
    else:
        server = create_hosted_server(args.database, args.host, args.port)
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
