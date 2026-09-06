"""Persistent localhost owner workspace for reviewing the web UI by hand."""

import hashlib
import json
import os
import stat
import threading
from pathlib import Path

from proofpress import ProofpressClient
from proofpress.hosted.service import create_hosted_server


REPOSITORY = Path(__file__).resolve().parents[3]
STATE_DIRECTORY = Path(
    os.environ.get(
        "PROOFPRESS_LOCAL_PREVIEW_DIR",
        REPOSITORY / ".proofpress" / "local-preview",
    )
).expanduser().resolve()
DATABASE = STATE_DIRECTORY / "hosted.db"
CREDENTIALS = STATE_DIRECTORY / "credentials.json"
PORT = int(os.environ.get("PROOFPRESS_LOCAL_PORT", "7334"))


def create_credentials(server):
    owner = server.proofpress_control.bootstrap(
        "workspace:local-preview", "human:local-owner", "Local owner"
    )
    agent = server.proofpress_control.issue_agent_credential(
        owner["token"], "agent:local-preview", "Local preview agent"
    )
    payload = {
        "schema_version": "proofpress/local-preview-credentials/v1",
        "owner": owner["token"],
        "agent": agent["token"],
    }
    CREDENTIALS.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    CREDENTIALS.chmod(stat.S_IRUSR | stat.S_IWUSR)
    return payload


def seed_preview(base, agent_token):
    client = ProofpressClient.localhost(base, agent_token)
    statements = [
        "A durable product decision should stay connected to the minimum evidence needed for a future reviewer to understand when it applies.",
        "Long model advice should remain available for audit without displacing the human decision path in the review interface.",
        "Only authorized Human Approval admits a candidate conclusion for downstream reuse; automated checks and model advice remain inputs to that decision.",
    ]
    for index, statement in enumerate(statements, start=1):
        quote = statement + " " + (
            "This synthetic localhost example intentionally includes additional wording "
            "so typography, wrapping, progressive disclosure, and narrow viewport behavior "
            "can be inspected before a UI change is merged. " * index
        )
        evidence = client.submit_evidence(
            {
                "schema_version": "proofpress/retrieval-evidence/v1",
                "source": {
                    "uri": f"fixture://local-preview/{index}",
                    "content_digest": "sha256:" + hashlib.sha256(quote.encode()).hexdigest(),
                },
                "evidence": {
                    "quote": quote,
                    "locator": {
                        "kind": "text_span",
                        "start": 0,
                        "end": len(quote),
                        "text_digest": "sha256:" + hashlib.sha256(quote.encode()).hexdigest(),
                    },
                },
                "retrieval": {
                    "adapter": "local-preview",
                    "version": "1",
                    "query": f"preview {index}",
                    "config_digest": "sha256:" + "b" * 64,
                },
            }
        )
        proposal = client.propose_conclusion(
            statement, evidence["evidence"], "local-preview", "agent:local-preview"
        )
        client.evaluate_conclusion(proposal["conclusion"]["id"])


def main():
    STATE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    database_exists = DATABASE.exists()
    credentials_exist = CREDENTIALS.exists()
    if database_exists != credentials_exist:
        raise SystemExit(
            f"Local preview state is incomplete. Keep or remove both {DATABASE} and {CREDENTIALS}."
        )

    os.environ["PROOFPRESS_WORKSPACE_LABEL"] = "Local preview · persistent synthetic data"
    server = create_hosted_server(DATABASE, port=PORT)
    credentials = (
        json.loads(CREDENTIALS.read_text(encoding="utf-8"))
        if credentials_exist
        else create_credentials(server)
    )
    server.proofpress_control.authenticate(credentials["owner"])
    server.proofpress_control.authenticate(credentials["agent"])
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    if not database_exists:
        seed_preview(base, credentials["agent"])

    print(
        json.dumps(
            {
                "event": "local_preview_ready",
                "base": base,
                "owner_credential": credentials["owner"],
                "credential_file": str(CREDENTIALS),
                "reused": database_exists,
            }
        ),
        flush=True,
    )
    try:
        input()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
