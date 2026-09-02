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
                         allow_public_bind=False):
    if host not in LOOPBACK_HOSTS and not allow_public_bind:
        raise ValueError(
            "hosted origin binds loopback only; terminate public HTTPS at a same-host reverse proxy")
    control = HostedControlPlane(database)
    server = ThreadingHTTPServer((host, port), HostedOperationHandler)
    server.proofpress_control = control
    server.proofpress_max_request_bytes = max_request_bytes
    server.proofpress_owner_sessions = {}
    return server


def _owner_token(args):
    token = os.environ.get(args.owner_token_env)
    if not token:
        raise SystemExit(f"missing owner credential in {args.owner_token_env}")
    return token


def main(argv=None):
    parser = argparse.ArgumentParser(prog="proofpress-self-hosted")
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
    serve.add_argument("--port", type=int,
                       default=int(os.environ.get("PORT", "7334")))
    serve.add_argument(
        "--allow-public-bind", action="store_true",
        help="allow a platform-private 0.0.0.0 bind; the platform must terminate HTTPS")
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
