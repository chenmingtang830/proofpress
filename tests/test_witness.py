import base64
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import proofpress_witness as witness


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "proofpress.py"


@unittest.skipUnless(shutil.which("openssl"), "openssl is required for Ed25519 verification")
class WitnessReceiptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.artifact = self.root / "artifact.bin"
        self.artifact.write_bytes(b"governed artifact")
        self.private_key = self.root / "private.pem"
        self.public_key = self.root / "public.pem"
        subprocess.run(["openssl", "genpkey", "-algorithm", "Ed25519", "-out", str(self.private_key)], check=True)
        subprocess.run(["openssl", "pkey", "-in", str(self.private_key), "-pubout", "-out", str(self.public_key)], check=True)
        self.now = datetime(2026, 8, 27, tzinfo=timezone.utc)

    def tearDown(self):
        self.tmp.cleanup()

    def receipt(self):
        digest = witness._sha256_file(self.artifact)
        receipt = {
            "protocol": witness.PROTOCOL,
            "protocol_version": 1,
            "issuer": "https://witness.example.test",
            "key_id": "witness-2026-01",
            "issued_at": "2026-08-27T00:00:00Z",
            "expires_at": "2026-08-28T00:00:00Z",
            "bindings": {
                "material": {"algorithm": "sha256", "digest": digest},
                "decision": {"algorithm": "sha256", "digest": "a" * 64},
                "policy": {"id": "review-policy", "digest": "b" * 64, "epoch": 7},
                "ledger": {"head": "ppe_ledger_head"},
            },
        }
        payload = self.root / "payload.json"
        signature = self.root / "signature.bin"
        payload.write_bytes(witness.canonical_payload(receipt))
        subprocess.run(["openssl", "pkeyutl", "-sign", "-rawin", "-inkey", str(self.private_key), "-in", str(payload), "-out", str(signature)], check=True)
        receipt["signature"] = {"algorithm": "ed25519", "value": base64.b64encode(signature.read_bytes()).decode("ascii")}
        return receipt

    def trust_store(self):
        return {
            "protocol": witness.TRUST_PROTOCOL,
            "protocol_version": 1,
            "issuers": {"https://witness.example.test": {"keys": {
                "witness-2026-01": {"algorithm": "ed25519", "public_key_pem": self.public_key.read_text()}
            }}},
        }

    def test_receipt_authenticates_only_when_external_key_and_material_match(self):
        result = witness.verify_receipt(self.artifact, self.receipt(), self.trust_store(), now=self.now)
        self.assertTrue(result["format_valid"])
        self.assertTrue(result["material_bound"])
        self.assertTrue(result["authority_at_issuance"])
        self.assertTrue(result["origin_authenticated"])

    def test_packet_cannot_appoint_its_own_authority(self):
        receipt = self.receipt()
        result = witness.verify_receipt(self.artifact, receipt, {
            "protocol": witness.TRUST_PROTOCOL, "protocol_version": 1, "issuers": {}
        }, now=self.now)
        self.assertFalse(result["authority_at_issuance"])
        self.assertFalse(result["origin_authenticated"])
        self.assertEqual(result["checks"][2]["type"], "trusted_key")
        self.assertEqual(result["checks"][2]["status"], "failed")

    def test_mutated_material_and_expired_receipt_do_not_authenticate(self):
        receipt = self.receipt()
        self.artifact.write_bytes(b"rewritten artifact")
        result = witness.verify_receipt(self.artifact, receipt, self.trust_store(), now=self.now)
        self.assertFalse(result["material_bound"])
        self.assertFalse(result["origin_authenticated"])
        self.artifact.write_bytes(b"governed artifact")
        result = witness.verify_receipt(
            self.artifact, receipt, self.trust_store(),
            now=self.now + timedelta(days=2))
        self.assertTrue(result["authority_at_issuance"])
        self.assertFalse(result["origin_authenticated"])

    def test_tampered_receipt_signature_fails(self):
        receipt = self.receipt()
        receipt["bindings"]["ledger"]["head"] = "rewritten-head"
        result = witness.verify_receipt(self.artifact, receipt, self.trust_store(), now=self.now)
        self.assertFalse(result["authority_at_issuance"])

    def test_cli_returns_json_without_changing_local_verify(self):
        receipt_path = self.root / "receipt.json"
        trust_path = self.root / "trust.json"
        receipt_path.write_text(json.dumps(self.receipt()))
        trust_path.write_text(json.dumps(self.trust_store()))
        completed = subprocess.run(
            ["python3", str(CLI), "witness", "verify", str(self.artifact),
             "--receipt", str(receipt_path), "--trust", str(trust_path), "--json"],
            text=True, capture_output=True, check=True,
        )
        self.assertTrue(json.loads(completed.stdout)["origin_authenticated"])
