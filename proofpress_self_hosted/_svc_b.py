                "include_blocked_statements": True,
            })
        else:
            return self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
        return self._json(_status_for(envelope), envelope)

    def _login_page(self, message=""):
        note = f"<p>{escape(message)}</p>" if message else ""
        return self._page("Proofpress owner sign in", "<h1>Owner review</h1>" + note +
            "<p class=muted>Use the owner credential. It stays in an HttpOnly session and is never placed in a URL.</p>"
            "<form method=post action=/owner/login><label>Owner credential<br>"
            "<input type=password name=token required autocomplete=current-password></label><br>"
            "<button type=submit>Sign in</button></form>")

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
                credentials = self.server.proofpress_control.list_credentials(
                    self._token())
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
        if path in {"/", "/home", "/review", "/ledger", "/activity", "/admin"}:
            session = self._owner_session()
            if not session:
                return self._html(HTTPStatus.UNAUTHORIZED, self._login_page())
            return self._owner_ui(session)
        return self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_POST(self):
        path = urlparse(self.path).path
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
                if action == "issue":
                    result = control.issue_agent_credential(
                        self._token(), request.get("principal_id", ""),
                        request.get("label", ""), request.get("display_name"))
                elif action == "rotate":
                    result = control.rotate_agent_credential(
                        self._token(), request.get("credential_id", ""),
                        request.get("label"))
                elif action == "revoke":
                    control.revoke_credential(
                        self._token(), request.get("credential_id", ""))
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
            self.send_header("Location", "/review")
            self.send_header("Set-Cookie", cookie)
