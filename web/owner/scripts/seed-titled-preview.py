"""Submit synthetic title examples using only the existing preview agent key."""
import hashlib
import json
from pathlib import Path
from proofpress import ProofpressClient

state = Path(__file__).resolve().parents[3] / ".proofpress/local-preview/credentials.json"
client = ProofpressClient.localhost("http://127.0.0.1:7334", json.loads(state.read_text())["agent"])
examples = [
    ("Keep evidence with the decision", "A durable product decision should stay connected to the minimum evidence needed for a future reviewer to understand when it applies."),
    ("Model advice supports human review", "Long model advice should remain available for audit without displacing the human decision path in the review interface."),
    ("Human admission authorizes reuse", "Only authorized Human Approval admits a candidate claim for downstream reuse; automated checks and model advice remain inputs to that decision."),
]
for index, (title, statement) in enumerate(examples):
    quote = statement + " Synthetic localhost UI example only; not a production finding."
    evidence = client.submit_evidence({
        "schema_version": "proofpress/retrieval-evidence/v1",
        "source": {"uri": f"fixture://local-preview/titles/{index}", "content_digest": "sha256:" + hashlib.sha256(quote.encode()).hexdigest()},
        "evidence": {"quote": quote, "locator": {"kind": "text_span", "start": 0, "end": len(quote), "text_digest": "sha256:" + hashlib.sha256(quote.encode()).hexdigest()}},
        "retrieval": {"adapter": "local-preview", "version": "1", "query": title, "config_digest": "sha256:" + "b" * 64},
    })
    result = client.propose_claim(statement, evidence["evidence"], "local-preview", "agent:local-preview", title=title)
    client.evaluate_claim(result["claim"]["id"])
    print(json.dumps({"title": title, "claim_id": result["claim"]["id"], "status": "pending human review"}))
