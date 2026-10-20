"""Fresh, synthetic localhost workspace; no authority secrets leave this process."""
import hashlib
import json
import tempfile
import sys
import threading
from pathlib import Path

from proofpress import ProofpressClient
from proofpress.hosted.service import create_hosted_server, enable_local_owner_preview

with tempfile.TemporaryDirectory(prefix="proofpress-onboarding-") as directory:
    server = create_hosted_server(Path(directory) / "hosted.db", port=0)
    control = server.proofpress_control
    owner = control.bootstrap("workspace:onboarding-test", "human:test-owner")
    # Match a restarted hosted process: no ambient legacy deployment policy.
    control.legacy_default_workspace_id = None
    enable_local_owner_preview(server, owner["token"])
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    print(json.dumps({"base": base}), flush=True)
    try:
        for command in sys.stdin:
            if command.strip() == "submit":
                agent = control.issue_agent_credential(owner["token"], "agent:fixture", "Synthetic successor")
                client = ProofpressClient.localhost(base, agent["token"])
                quote = "The synthetic fixture records a bounded research finding."
                digest = "sha256:" + hashlib.sha256(quote.encode()).hexdigest()
                evidence = client.submit_evidence({
                    "schema_version": "proofpress/retrieval-evidence/v1",
                    "source": {"uri": "fixture://onboarding", "content_digest": digest},
                    "evidence": {"quote": quote, "locator": {
                        "kind": "text_span", "start": 0, "end": len(quote), "text_digest": digest}},
                    "retrieval": {"adapter": "fixture", "version": "1", "query": "test",
                                  "config_digest": "sha256:" + "b" * 64}})
                claim = client.propose_claim(quote, evidence["evidence"], "onboarding-test", "agent:fixture",
                                             title="Synthetic onboarding finding")
                client.evaluate_claim(claim["claim"]["id"])
                print(json.dumps({"claim_id": claim["claim"]["id"]}), flush=True)
            elif command.strip() == "reuse":
                result = client.context(scope="onboarding-test", actor="agent:fixture")
                print(json.dumps({"governed_count": len(result["governed_context"])}), flush=True)
            else:
                break
    finally:
        server.shutdown()
        server.server_close()
