from pathlib import Path
import shutil
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples/openwiki-witness-boundary"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(DEMO))

import proofpress_witness as witness
import boundary
import run_demo


@unittest.skipUnless(shutil.which("openssl"), "OpenSSL is required")
class OpenWikiWitnessBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.snapshot = self.root / "snapshot"
        self.keys = self.root / "keys"
        self.snapshot.mkdir()
        self.keys.mkdir()
        run_demo.materialize_fixture(self.snapshot)
        self.producer_private, self.producer_public = run_demo.generate_keypair(
            self.keys, "producer"
        )
        self.decision_private, self.decision_public = run_demo.generate_keypair(
            self.keys, "decision"
        )
        self.trust = run_demo.trust_store(
            self.producer_public, self.decision_public
        )
        (
            self.inspection,
            self.digest,
            self.manifest,
            self.manifest_artifact,
        ) = run_demo.manifest_subject(self.snapshot)

    def tearDown(self):
        self.tmp.cleanup()

    def issue(self, profile, predicate, private_key, key_id):
        statement = boundary.make_statement(
            profile=profile,
            subject_name=run_demo.MANIFEST_RELATIVE,
            subject_sha256=self.digest,
            predicate=predicate,
        )
        return boundary.sign_statement(statement, private_key, key_id=key_id)

    def verify_producer(self, envelope, **identity):
        return run_demo.verify_manifest(
            self.manifest_artifact,
            envelope,
            self.trust,
            profile=witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
            bindings=run_demo.producer_bindings(self.digest),
            principal=run_demo.PRODUCER_PRINCIPAL,
            **identity,
        )

    def verify_decision(self, envelope, bindings=None):
        return run_demo.verify_manifest(
            self.manifest_artifact,
            envelope,
            self.trust,
            profile=witness.GOVERNANCE_DECISION_PROFILE,
            bindings=bindings or run_demo.governance_bindings(self.digest),
            principal=run_demo.DECISION_PRINCIPAL,
        )

    def test_end_to_end_demo_uses_real_verifier_and_proves_all_invariants(self):
        result = run_demo.execute_demo(self.root / "e2e")
        self.assertEqual(result["verifier"], "proofpress_witness.verify_attestation")
        self.assertTrue(all(result["assertions"].values()))
        self.assertTrue(result["fresh"]["producer_origin_authenticated"])
        self.assertTrue(result["fresh"]["decision_authority_authenticated"])
        self.assertEqual(result["fresh"]["proofpress_admission"], "not_performed")

    def test_producer_profile_authenticates_only_origin_and_never_admits(self):
        envelope = self.issue(
            witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
            run_demo.producer_predicate(self.digest),
            self.producer_private,
            run_demo.PRODUCER_KEY_ID,
        )
        result = self.verify_producer(envelope)
        axes = boundary.compose_trust_axes(
            self.inspection, handoff_manifest_digest=self.digest,
            producer_origin=result)
        self.assertTrue(result["producer_origin_authenticated"])
        self.assertFalse(result["decision_authority_authenticated"])
        self.assertEqual(result["authority_current"], "unknown")
        self.assertEqual(axes["proofpress_admission"], "not_performed")

    def test_decision_profile_cannot_authenticate_openwiki_origin(self):
        envelope = self.issue(
            witness.GOVERNANCE_DECISION_PROFILE,
            run_demo.decision_predicate(self.digest),
            self.decision_private,
            run_demo.DECISION_KEY_ID,
        )
        decision = self.verify_decision(envelope)
        wrong_profile = run_demo.verify_manifest(
            self.manifest_artifact,
            envelope,
            self.trust,
            profile=witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
            bindings=run_demo.producer_bindings(self.digest),
            principal=run_demo.PRODUCER_PRINCIPAL,
        )
        self.assertTrue(decision["decision_authority_authenticated"])
        self.assertFalse(decision["producer_origin_authenticated"])
        self.assertFalse(wrong_profile["producer_origin_authenticated"])
        self.assertFalse(wrong_profile["profile_bound"])

    def test_decision_must_match_winner_policy_and_ledger_transition(self):
        envelope = self.issue(
            witness.GOVERNANCE_DECISION_PROFILE,
            run_demo.decision_predicate(self.digest),
            self.decision_private,
            run_demo.DECISION_KEY_ID,
        )
        mutations = (
            run_demo.governance_bindings(
                self.digest, resolution_action="supersede_right"),
            run_demo.governance_bindings(self.digest, policy_epoch=6),
            run_demo.governance_bindings(
                self.digest, resulting_head="ppe_conflicting_head"),
        )
        for expected in mutations:
            with self.subTest(expected=expected):
                result = self.verify_decision(envelope, expected)
                self.assertTrue(result["signature_valid"])
                self.assertFalse(result["bindings_bound"])
                self.assertFalse(result["decision_authority_authenticated"])

    def test_independently_valid_axes_cannot_join_different_manifests(self):
        producer = self.issue(
            witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
            run_demo.producer_predicate(self.digest),
            self.producer_private,
            run_demo.PRODUCER_KEY_ID,
        )
        decision = self.issue(
            witness.GOVERNANCE_DECISION_PROFILE,
            run_demo.decision_predicate(self.digest),
            self.decision_private,
            run_demo.DECISION_KEY_ID,
        )
        producer_result = self.verify_producer(producer)
        decision_result = self.verify_decision(decision)
        snapshot_b = self.root / "snapshot-b"
        shutil.copytree(self.snapshot, snapshot_b)
        (snapshot_b / ".openwikiignore").write_text(
            "# distinct but valid handoff manifest\n", encoding="utf-8")
        inspection_b, digest_b, _, _ = run_demo.manifest_subject(snapshot_b)

        axes = boundary.compose_trust_axes(
            inspection_b,
            handoff_manifest_digest=digest_b,
            producer_origin=producer_result,
            decision_authority=decision_result,
        )

        self.assertTrue(inspection_b["inspection_passed"])
        self.assertNotEqual(digest_b, self.digest)
        self.assertTrue(producer_result["producer_origin_authenticated"])
        self.assertTrue(decision_result["decision_authority_authenticated"])
        self.assertFalse(axes["producer_manifest_joined"])
        self.assertFalse(axes["decision_manifest_joined"])
        self.assertFalse(axes["producer_origin_authenticated"])
        self.assertFalse(axes["decision_authority_authenticated"])

    def test_statement_identity_is_idempotent_and_equivocation_fails(self):
        envelope = self.issue(
            witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
            run_demo.producer_predicate(self.digest),
            self.producer_private,
            run_demo.PRODUCER_KEY_ID,
        )
        first = self.verify_producer(envelope)
        repeated = self.verify_producer(
            envelope,
            expected_statement_id=first["statement_id"],
            expected_statement_digest=first["statement_digest"],
        )
        self.assertTrue(repeated["statement_identity_bound"])
        self.assertEqual(repeated["statement_identity_status"], "matched")
        self.assertTrue(repeated["producer_origin_authenticated"])

        changed_predicate = {
            **run_demo.producer_predicate(self.digest),
            "additive_note": "same id, different signed bytes",
        }
        changed = self.issue(
            witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
            changed_predicate,
            self.producer_private,
            run_demo.PRODUCER_KEY_ID,
        )
        conflict = self.verify_producer(
            changed,
            expected_statement_id=first["statement_id"],
            expected_statement_digest=first["statement_digest"],
        )
        self.assertTrue(conflict["signature_valid"])
        self.assertTrue(conflict["statement_identity_conflict"])
        self.assertFalse(conflict["statement_identity_bound"])
        self.assertFalse(conflict["producer_origin_authenticated"])

    def test_authentic_stale_packet_stays_stale_and_unadmitted(self):
        evidence = self.snapshot / "evidence/gravitational-evidence.json"
        evidence.write_text(
            evidence.read_text(encoding="utf-8").replace(
                '"dt": 86400.0', '"dt": 86000.0', 1
            ),
            encoding="utf-8",
        )
        inspection, stale_digest, _, artifact = run_demo.manifest_subject(self.snapshot)
        envelope = boundary.sign_statement(
            boundary.make_statement(
                profile=witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
                subject_name=run_demo.MANIFEST_RELATIVE,
                subject_sha256=stale_digest,
                predicate=run_demo.producer_predicate(
                    stale_digest, statement_id="producer-origin-stale-test"
                ),
            ),
            self.producer_private,
            key_id=run_demo.PRODUCER_KEY_ID,
        )
        origin = run_demo.verify_manifest(
            artifact,
            envelope,
            self.trust,
            profile=witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
            bindings=run_demo.producer_bindings(stale_digest),
            principal=run_demo.PRODUCER_PRINCIPAL,
        )
        axes = boundary.compose_trust_axes(
            inspection, handoff_manifest_digest=stale_digest,
            producer_origin=origin)
        self.assertTrue(axes["producer_origin_authenticated"])
        self.assertFalse(axes["evidence_current"])
        self.assertFalse(axes["inspection_passed"])
        self.assertEqual(axes["proofpress_admission"], "not_performed")

    def test_dsse_payload_type_is_bound_and_offline_currentness_is_unknown(self):
        envelope = self.issue(
            witness.OPENWIKI_PRODUCER_ORIGIN_PROFILE,
            run_demo.producer_predicate(self.digest),
            self.producer_private,
            run_demo.PRODUCER_KEY_ID,
        )
        envelope["payloadType"] = "application/json"
        result = self.verify_producer(envelope)
        self.assertFalse(result["attestation_format_valid"])
        self.assertFalse(result["producer_origin_authenticated"])
        self.assertEqual(result["authority_current"], "unknown")


if __name__ == "__main__":
    unittest.main()
