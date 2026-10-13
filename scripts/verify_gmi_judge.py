"""Opt-in live GMI check through an isolated Proofpress hosted claim workflow."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

from cryptography.fernet import Fernet

from proofpress.hosted.control_plane import HostedControlPlane
from proofpress.hosted.review_policy import PROVIDERS


def operation(name, parameters):
    return {"schema_version": "proofpress/local-operation/v1alpha1",
            "operation": name, "parameters": parameters}


def result(control, token, name, parameters):
    response = control.execute(token, operation(name, parameters))
    if not response["ok"]:
        raise RuntimeError(f"{name} failed: {response['error']['code']}")
    return response["result"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Allow one real GMI model request")
    parser.add_argument("--model", default=os.environ.get("GMI_MODEL") or
                        PROVIDERS["gmi_cloud"]["default_model"])
    args = parser.parse_args()
    if not args.live:
        parser.error("Pass --live to authorize a real provider call and its possible charge.")
    key = os.environ.get("GMI_API_KEY", "").strip()
    if not key:
        parser.error("Set GMI_API_KEY in the environment; no credential is supplied by this script.")

    quote = "The sample agreement limits liability to one year of fees."
    evidence = {
        "schema_version": "proofpress/retrieval-evidence/v1",
        "source": {"uri": "workspace://gmi-verification/sample-agreement",
                   "content_digest": "sha256:" + hashlib.sha256(quote.encode()).hexdigest()},
        "evidence": {"quote": quote, "locator": {
            "kind": "text_span", "start": 0, "end": len(quote),
            "text_digest": "sha256:" + hashlib.sha256(quote.encode()).hexdigest()}},
        "retrieval": {"adapter": "gmi-verification", "version": "1",
                      "query": "What is the liability cap?",
                      "config_digest": "sha256:" + hashlib.sha256(b"gmi-verification/v1").hexdigest()},
    }
    prior_encryption_key = os.environ.get("PROOFPRESS_SECRET_ENCRYPTION_KEY")
    os.environ["PROOFPRESS_SECRET_ENCRYPTION_KEY"] = Fernet.generate_key().decode()
    try:
        with tempfile.TemporaryDirectory(prefix="proofpress-gmi-check-") as directory:
            control = HostedControlPlane(Path(directory) / "hosted.db")
            owner = control.bootstrap("workspace:gmi-check", "human:verification")["token"]
            agent = control.issue_agent_credential(owner, "agent:verification", "GMI check")["token"]
            settings = {"mode": "manual", "provider": "gmi_cloud", "endpoint": "",
                        "model": args.model, "rubric": "evidence-support/v1",
                        "criteria": "Escalate if the quoted evidence does not support the statement.",
                        "zdr": False, "external_consent": True,
                        "require_judge": False, "auto_admit_new_claims": False}
            control.save_review_policy(owner, settings, 0, api_key=key)
            refs = result(control, agent, "evidence.submit", {"payload": evidence})["evidence"]
            claim = result(control, agent, "claim.propose", {
                "title": "Sample agreement liability cap", "statement": quote,
                "evidence_refs": refs, "scope": "gmi-verification",
                "proposer": "agent:verification"})["claim"]
            evaluation = result(control, agent, "claim.evaluate", {"claim_id": claim["id"]})
            if not evaluation["eligible"]:
                raise RuntimeError("Proofpress deterministic checks did not pass.")
            result(control, agent, "claim.judge", {"claim_id": claim["id"]})
            receipt = result(control, owner, "review.receipt", {"claim_id": claim["id"]})
            recommendation = receipt.get("recommendation") or {}
            if (recommendation.get("adapter") != "proofpress-gmi_cloud-judge/v1"
                    or recommendation.get("model") != args.model
                    or recommendation.get("recommendation") not in {"accept", "reject", "escalate"}):
                raise RuntimeError("Proofpress did not record a GMI advisory recommendation.")
            if receipt["state"] != "needs_review":
                raise RuntimeError("The verification claim crossed the approval boundary.")
            context = result(control, agent, "context.get", {"scope": "gmi-verification"})
            if context["governed_context"]:
                raise RuntimeError("An unapproved verification claim appeared in governed context.")
            print(json.dumps({"workflow": "evidence.submit -> claim.propose -> claim.evaluate -> claim.judge -> review.receipt -> context.get",
                              "provider": "gmi_cloud", "model": args.model,
                              "advisory_recommendation": recommendation["recommendation"],
                              "receipt_state": receipt["state"], "governed_context_count": 0}))
    finally:
        if prior_encryption_key is None:
            os.environ.pop("PROOFPRESS_SECRET_ENCRYPTION_KEY", None)
        else:
            os.environ["PROOFPRESS_SECRET_ENCRYPTION_KEY"] = prior_encryption_key


if __name__ == "__main__":
    main()
