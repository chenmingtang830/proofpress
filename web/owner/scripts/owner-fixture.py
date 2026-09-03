"""Ephemeral owner UI fixture; credentials are emitted only to the test runner pipe."""
import hashlib
import json
import tempfile
import threading
from pathlib import Path
from proofpress.hosted.service import create_hosted_server
from proofpress import ProofpressClient

with tempfile.TemporaryDirectory(prefix="proofpress-browser-") as directory:
    server = create_hosted_server(Path(directory) / "hosted.db", port=0)
    owner = server.proofpress_control.bootstrap("workspace:browser-test", "human:browser-test")
    agent = server.proofpress_control.issue_agent_credential(owner["token"], "agent:browser-test", "Browser test")
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    client = ProofpressClient.localhost(base, agent["token"])
    ids = []
    for name in ["approve", "reject", "clarify"]:
        quote = f"Browser fixture {name}: only human admission permits reuse."
        evidence = client.submit_evidence({
            "schema_version": "proofpress/retrieval-evidence/v1",
            "source": {"uri": f"fixture://{name}", "content_digest": "sha256:" + "a" * 64},
            "evidence": {"quote": quote, "locator": {"kind": "text_span", "start": 0, "end": len(quote),
                "text_digest": "sha256:" + hashlib.sha256(quote.encode()).hexdigest()}},
            "retrieval": {"adapter": "browser-fixture", "version": "1", "query": name, "config_digest": "sha256:" + "b" * 64},
        })
        proposal = client.propose_conclusion(quote, evidence["evidence"], "browser-test", "agent:browser-test")
        cid = proposal["conclusion"]["id"]
        client.evaluate_conclusion(cid)
        ids.append(cid)
    print(json.dumps({"base": base, "owner": owner["token"], "agent": agent["token"], "ids": ids}), flush=True)
    try:
        input()
    finally:
        server.shutdown()
        server.server_close()
