import base64
import copy
from datetime import datetime, timezone
import hashlib
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
class WitnessAttestationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.artifact = self.root / "artifact.bin"
        self.artifact.write_bytes(b"governed artifact")
        self.private_key = self.root / "private.pem"
        self.public_key = self.root / "public.pem"
        subprocess.run(
            ["openssl", "genpkey", "-algorithm", "Ed25519",
             "-out", str(self.private_key)], check=True)
        subprocess.run(
            ["openssl", "pkey", "-in", str(self.private_key), "-pubout",
             "-out", str(self.public_key)], check=True)
        self.now = datetime(2026, 8, 27, tzinfo=timezone.utc)
        self.issuer = "https://witness.example.test"
        self.key_id = "witness-2026-01"
        self.tenant = "tenant-a"
        self.audience = "proofpress-context-v2"
        self.principal = "resolver:alice"

    def tearDown(self):
        self.tmp.cleanup()

    def decision_bindings(self):
        return {
            "decision": {"algorithm": "sha256", "digest": "a" * 64},
            "contradiction": {
                "type": "contradicts",
                "left_claim_id": "claim-old",
                "right_claim_id": "claim-current",
            },
            "resolution": {"action": "supersede_left"},
            "policy": {
                "id": "review-policy", "digest": "b" * 64, "epoch": 7,
            },
            "ledger": {
                "previous_head": "ppe_previous",
                "resulting_head": "ppe_resulting",
            },
        }

    def origin_bindings(self):
        return {
            "handoff_manifest": {
                "algorithm": "sha256", "digest": "c" * 64,
            },
            "producer": {"id": "openwiki", "run_id": "run-42"},
        }

    def statement(
        self, profile=None, bindings=None, *, tenant=None, audience=None,
        principal=None, artifact_digest=None,
    ):
        profile = profile or witness.GOVERNANCE_DECISION_PROFILE
        bindings = bindings or self.decision_bindings()
        return {
            "_type": witness.IN_TOTO_STATEMENT_TYPE,
            "subject": [{
                "name": "artifact.bin",
                "digest": {
                    "sha256": artifact_digest or witness._sha256_file(self.artifact)
                },
            }],
            "predicateType": profile,
            "predicate": {
                "issuer": self.issuer,
                "tenant": tenant or self.tenant,
                "audience": audience or self.audience,
                "principal": principal or self.principal,
                "key_id": self.key_id,
                "statement_id": "statement-001",
                "critical": [],
                "issued_at": "2026-01-01T00:00:00Z",
                "expires_at": "2030-01-01T00:00:00Z",
                "bindings": bindings,
            },
        }

    def sign_payload(self, payload):
        payload_path = self.root / "payload.bin"
        pae_path = self.root / "pae.bin"
        signature_path = self.root / "signature.bin"
        payload_path.write_bytes(payload)
        pae_path.write_bytes(witness.dsse_pae(witness.DSSE_PAYLOAD_TYPE, payload))
        subprocess.run(
            ["openssl", "pkeyutl", "-sign", "-rawin", "-inkey",
             str(self.private_key), "-in", str(pae_path),
             "-out", str(signature_path)], check=True)
        return {
            "payloadType": witness.DSSE_PAYLOAD_TYPE,
            "payload": base64.b64encode(payload).decode("ascii"),
            "signatures": [{
                "keyid": self.key_id,
                "sig": base64.b64encode(
                    signature_path.read_bytes()).decode("ascii"),
            }],
        }

    def attestation(self, statement=None):
        statement = statement or self.statement()
        payload = json.dumps(
            statement, ensure_ascii=False, separators=(",", ":")
        ).encode("utf-8")
        return self.sign_payload(payload)

    def trust_store(self):
        return {
            "protocol": witness.TRUST_PROTOCOL,
            "protocol_version": witness.TRUST_PROTOCOL_VERSION,
            "issuers": {self.issuer: {"keys": {self.key_id: {
                "algorithm": "ed25519",
                "public_key_pem": self.public_key.read_text(),
                "status": "active",
                "not_before": "2025-01-01T00:00:00Z",
                "not_after": "2035-01-01T00:00:00Z",
                "profiles": sorted(witness.SUPPORTED_PROFILES),
                "tenants": [self.tenant],
                "audiences": [self.audience],
                "principals": [self.principal],
            }}}},
        }

    def verify(self, attestation=None, trust_store=None, *, profile=None,
               bindings=None, tenant=None, audience=None, principal=None,
               statement_id=None, statement_digest=None):
        return witness.verify_attestation(
            self.artifact,
            attestation or self.attestation(),
            trust_store or self.trust_store(),
            expected_profile=profile or witness.GOVERNANCE_DECISION_PROFILE,
            expected_bindings=bindings or self.decision_bindings(),
            expected_tenant=tenant or self.tenant,
            expected_audience=audience or self.audience,
            expected_principal=principal or self.principal,
            expected_statement_id=statement_id,
            expected_statement_digest=statement_digest,
            now=self.now,
        )

    def test_governance_profile_authenticates_only_decision_authority(self):
        attestation = self.attestation()
        self.assertEqual(
            set(attestation), {"payloadType", "payload", "signatures"})
        result = self.verify(attestation)
        self.assertTrue(result["attestation_format_valid"])
        self.assertTrue(result["signature_valid"])
        self.assertTrue(result["subject_bound"])
        self.assertTrue(result["bindings_bound"])
        self.assertTrue(result["decision_authority_authenticated"])
        self.assertFalse(result["producer_origin_authenticated"])
        self.assertEqual(result["authority_current"], "unknown")

    def test_origin_profile_authenticates_only_producer_origin(self):
        bindings = self.origin_bindings()
        attestation = self.attestation(self.statement(
            witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE, bindings))
        result = self.verify(
            attestation,
            profile=witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
            bindings=bindings,
        )
        self.assertTrue(result["producer_origin_authenticated"])
        self.assertFalse(result["decision_authority_authenticated"])
        self.assertEqual(result["authority_current"], "unknown")

    def test_decision_substitution_fails_despite_valid_signature(self):
        expected = self.decision_bindings()
        expected["decision"]["digest"] = "d" * 64
        result = self.verify(bindings=expected)
        self.assertTrue(result["signature_valid"])
        self.assertTrue(result["subject_bound"])
        self.assertFalse(result["bindings_bound"])
        self.assertFalse(result["decision_authority_authenticated"])

    def test_contradiction_endpoint_substitution_fails(self):
        expected = self.decision_bindings()
        expected["contradiction"]["left_claim_id"] = "claim-other"
        result = self.verify(bindings=expected)
        self.assertTrue(result["signature_valid"])
        self.assertFalse(result["bindings_bound"])
        self.assertFalse(result["decision_authority_authenticated"])

    def test_policy_or_ledger_substitution_fails(self):
        mutations = (
            ("policy", lambda value: value["policy"].update({"epoch": 6})),
            ("ledger", lambda value: value["ledger"].update(
                {"previous_head": "ppe_older"})),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                expected = self.decision_bindings()
                mutate(expected)
                result = self.verify(bindings=expected)
                self.assertTrue(result["signature_valid"])
                self.assertFalse(result["bindings_bound"])
                self.assertFalse(result["decision_authority_authenticated"])

    def test_cross_profile_attestation_cannot_upgrade_other_axis(self):
        origin = self.origin_bindings()
        result = self.verify(
            profile=witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
            bindings=origin,
        )
        self.assertTrue(result["signature_valid"])
        self.assertFalse(result["profile_bound"])
        self.assertFalse(result["producer_origin_authenticated"])
        self.assertFalse(result["decision_authority_authenticated"])

    def test_cross_tenant_attestation_is_rejected(self):
        attestation = self.attestation(self.statement(tenant="tenant-b"))
        result = self.verify(attestation)
        self.assertTrue(result["signature_valid"])
        self.assertFalse(result["tenant_bound"])
        self.assertFalse(result["trust_scope_authorized"])
        self.assertFalse(result["decision_authority_authenticated"])

    def test_unsigned_keyid_alias_cannot_broaden_signed_authority(self):
        statement = self.statement(tenant="tenant-b")
        attestation = self.attestation(statement)
        attestation["signatures"][0]["keyid"] = "witness-broad-alias"
        trust = self.trust_store()
        keys = trust["issuers"][self.issuer]["keys"]
        broad_alias = copy.deepcopy(keys[self.key_id])
        broad_alias["tenants"] = ["tenant-b"]
        keys["witness-broad-alias"] = broad_alias
        result = self.verify(attestation, trust, tenant="tenant-b")
        self.assertTrue(result["signature_valid"])
        self.assertFalse(result["key_id_bound"])
        self.assertFalse(result["trust_scope_authorized"])
        self.assertFalse(result["decision_authority_authenticated"])

    def test_revoked_key_cannot_authenticate(self):
        trust = self.trust_store()
        trust["issuers"][self.issuer]["keys"][self.key_id]["status"] = "revoked"
        result = self.verify(trust_store=trust)
        self.assertTrue(result["signature_valid"])
        self.assertFalse(result["key_status_allowed"])
        self.assertFalse(result["decision_authority_authenticated"])

    def test_key_outside_validity_window_cannot_authenticate(self):
        trust = self.trust_store()
        key = trust["issuers"][self.issuer]["keys"][self.key_id]
        key["not_before"] = "2024-01-01T00:00:00Z"
        key["not_after"] = "2025-12-31T23:59:59Z"
        result = self.verify(trust_store=trust)
        self.assertTrue(result["signature_valid"])
        self.assertFalse(result["key_valid_at_issuance"])
        self.assertFalse(result["decision_authority_authenticated"])

    def test_mutated_material_cannot_authenticate(self):
        attestation = self.attestation()
        self.artifact.write_bytes(b"rewritten artifact")
        result = self.verify(attestation)
        self.assertTrue(result["signature_valid"])
        self.assertFalse(result["subject_bound"])
        self.assertFalse(result["decision_authority_authenticated"])

    def test_duplicate_keys_in_signed_payload_are_rejected(self):
        payload = json.dumps(
            self.statement(), separators=(",", ":")
        ).replace(
            f'"tenant":"{self.tenant}"',
            f'"tenant":"{self.tenant}","tenant":"tenant-b"',
        ).encode("utf-8")
        result = self.verify(self.sign_payload(payload))
        self.assertFalse(result["attestation_format_valid"])
        self.assertIn("duplicate JSON key", result["checks"][0]["detail"])

    def test_nonfinite_json_numbers_are_rejected(self):
        with self.assertRaisesRegex(witness.WitnessError, "non-finite JSON"):
            witness.loads_json('{"epoch":NaN}')
        with self.assertRaisesRegex(witness.WitnessError, "non-finite JSON"):
            witness.loads_json('{"epoch":Infinity}')

    def test_unknown_or_duplicate_critical_extensions_are_rejected(self):
        unknown = self.statement()
        unknown["predicate"]["critical"] = [
            "https://proofpress.dev/extensions/unknown/v1"]
        result = self.verify(self.attestation(unknown))
        self.assertFalse(result["attestation_format_valid"])
        self.assertIn(
            "unsupported critical extension", result["checks"][0]["detail"])

        duplicate = self.statement()
        duplicate["predicate"]["critical"] = ["unknown", "unknown"]
        result = self.verify(self.attestation(duplicate))
        self.assertFalse(result["attestation_format_valid"])
        self.assertIn(
            "must not contain duplicates", result["checks"][0]["detail"])

    def test_additive_signed_fields_do_not_break_expected_subset(self):
        bindings = self.decision_bindings()
        signed_bindings = copy.deepcopy(bindings)
        signed_bindings["extension"] = {"opaque": True}
        statement = self.statement(bindings=signed_bindings)
        statement["predicate"]["extension"] = "preserved"
        result = self.verify(self.attestation(statement), bindings=bindings)
        self.assertTrue(result["bindings_bound"])
        self.assertTrue(result["decision_authority_authenticated"])

    def test_statement_identity_is_idempotent_and_detects_equivocation(self):
        attestation = self.attestation()
        first = self.verify(attestation)
        repeated = self.verify(
            attestation,
            statement_id=first["statement_id"],
            statement_digest=first["statement_digest"],
        )
        self.assertEqual(first["statement_id"], repeated["statement_id"])
        self.assertEqual(first["statement_digest"], repeated["statement_digest"])
        self.assertTrue(repeated["statement_identity_bound"])
        self.assertEqual(repeated["statement_identity_status"], "matched")
        self.assertTrue(repeated["decision_authority_authenticated"])
        self.assertFalse(witness.statement_identity_conflict(first, repeated))

        changed_statement = self.statement()
        changed_statement["predicate"]["extension"] = "different-signed-bytes"
        changed = self.verify(
            self.attestation(changed_statement),
            statement_id=first["statement_id"],
            statement_digest=first["statement_digest"],
        )
        self.assertTrue(changed["signature_valid"])
        self.assertFalse(changed["statement_identity_bound"])
        self.assertTrue(changed["statement_identity_conflict"])
        self.assertEqual(changed["statement_identity_status"], "conflict")
        self.assertFalse(changed["decision_authority_authenticated"])
        self.assertEqual(first["statement_id"], changed["statement_id"])
        self.assertNotEqual(first["statement_digest"], changed["statement_digest"])
        self.assertTrue(witness.statement_identity_conflict(first, changed))

        different_statement = self.statement()
        different_statement["predicate"]["statement_id"] = "statement-002"
        different = self.verify(
            self.attestation(different_statement),
            statement_id=first["statement_id"],
            statement_digest=first["statement_digest"],
        )
        self.assertFalse(different["statement_identity_bound"])
        self.assertFalse(different["statement_identity_conflict"])
        self.assertEqual(different["statement_identity_status"], "different")
        self.assertFalse(different["decision_authority_authenticated"])

    def test_cli_requires_external_expectations_and_rejects_duplicate_json(self):
        attestation_path = self.root / "attestation.json"
        trust_path = self.root / "trust.json"
        expected_path = self.root / "expected.json"
        attestation = self.attestation()
        attestation_path.write_text(json.dumps(attestation))
        trust_path.write_text(json.dumps(self.trust_store()))
        expected_path.write_text(json.dumps(self.decision_bindings()))
        decoded_statement = witness.loads_json(
            base64.b64decode(attestation["payload"]))
        self.assertEqual(
            decoded_statement["predicate"]["statement_id"], "statement-001")
        expected_statement_digest = hashlib.sha256(
            base64.b64decode(attestation["payload"])).hexdigest()
        command = [
            "python3", str(CLI), "witness", "verify", str(self.artifact),
            "--attestation", str(attestation_path),
            "--trust", str(trust_path),
            "--profile", witness.GOVERNANCE_DECISION_PROFILE,
            "--expected-bindings", str(expected_path),
            "--tenant", self.tenant,
            "--audience", self.audience,
            "--principal", self.principal,
            "--expected-statement-id", "statement-001",
            "--expected-statement-digest", expected_statement_digest,
            "--json",
        ]
        completed = subprocess.run(command, text=True, capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertTrue(result["decision_authority_authenticated"])
        self.assertEqual(result["statement_identity_status"], "matched")
        self.assertEqual(result["authority_current"], "unknown")

        changed_statement = self.statement()
        changed_statement["predicate"]["extension"] = "different-signed-bytes"
        attestation_path.write_text(json.dumps(
            self.attestation(changed_statement)))
        completed = subprocess.run(command, text=True, capture_output=True)
        self.assertEqual(completed.returncode, 1, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertTrue(result["statement_identity_conflict"])
        self.assertFalse(result["decision_authority_authenticated"])

        attestation_path.write_text(
            '{"payloadType":"first","payloadType":"second"}', encoding="utf-8")
        completed = subprocess.run(command, text=True, capture_output=True)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("duplicate JSON key", completed.stderr)


if __name__ == "__main__":
    unittest.main()
