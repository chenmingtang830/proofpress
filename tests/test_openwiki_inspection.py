import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import proofpress_openwiki as openwiki


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "proofpress.py"
FIXTURE = ROOT / "examples" / "openwiki-conflict-gate" / "openwiki-fixture.json"


class OpenWikiInspectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.snapshot = Path(self.tmp.name)
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        for name, row in fixture["files"].items():
            target = self.snapshot / name
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("w", encoding="utf-8", newline="") as stream:
                stream.write(row["content"])

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args, check=True):
        return subprocess.run(
            [sys.executable, str(CLI), "openwiki", "inspect", str(self.snapshot), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=check,
        )

    def inspect(self, *args, check=True):
        return json.loads(self.cli(*args, "--json", check=check).stdout)

    def sidecars(self):
        return sorted((self.snapshot / "openwiki" / ".claims").rglob("*.json"))

    def read_json(self, path):
        return json.loads(path.read_text(encoding="utf-8"))

    def write_json(self, path, value):
        with path.open("w", encoding="utf-8", newline="") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")

    def tree_digest(self):
        rows = []
        for path in sorted(item for item in self.snapshot.rglob("*") if item.is_file()):
            rows.append(
                path.relative_to(self.snapshot).as_posix().encode()
                + b"\0"
                + hashlib.sha256(path.read_bytes()).digest()
            )
        return hashlib.sha256(b"".join(rows)).hexdigest()

    def test_real_openwiki_042_fixture_is_independently_rechecked_read_only(self):
        before = self.tree_digest()
        report = self.inspect()
        self.assertTrue(report["inspection_passed"])
        self.assertEqual(report["summary"]["page_count"], 2)
        self.assertEqual(report["summary"]["claim_count"], 10)
        self.assertTrue(report["summary"]["format_valid"])
        self.assertTrue(report["summary"]["page_bound"])
        self.assertTrue(report["summary"]["evidence_current"])
        self.assertFalse(report["summary"]["origin_authenticated"])
        self.assertTrue(report["summary"]["proofpress_review_required"])
        self.assertEqual(before, self.tree_digest())
        persisted = {
            claim["id"]: claim["statement"]
            for sidecar in self.sidecars()
            for claim in self.read_json(sidecar)["claims"]
        }
        for page in report["pages"]:
            for claim in page["claims"]:
                self.assertEqual(claim["statement"], persisted[claim["id"]])
                self.assertEqual(claim["lineage"], "exact_producer_claim")
                self.assertEqual(claim["proofpress_admission"], "not_inherited")

    def test_selected_page_inspection_does_not_expand_to_the_full_tree(self):
        report = self.inspect("--page", "quickstart.md")
        self.assertTrue(report["inspection_passed"])
        self.assertEqual(report["summary"]["page_count"], 1)
        self.assertEqual(report["summary"]["claim_count"], 4)
        self.assertEqual(report["pages"][0]["page"], "openwiki/quickstart.md")

    def test_handoff_manifest_is_deterministic_and_binds_consumed_files(self):
        report = openwiki.inspect_openwiki_snapshot(self.snapshot)
        first = openwiki.build_handoff_manifest(self.snapshot, report)
        second = openwiki.build_handoff_manifest(self.snapshot, report)
        self.assertEqual(first, second)
        self.assertEqual(
            openwiki.handoff_manifest_digest(first),
            openwiki.handoff_manifest_digest(second),
        )
        rows = {row["path"]: row for row in first["materials"]}
        self.assertIn("openwiki/index.md", rows)
        self.assertIn("openwiki/geometry/index.md", rows)
        self.assertIn("openwiki/quickstart.md", rows)
        self.assertIn("openwiki/.claims/quickstart.json", rows)
        self.assertIn("evidence/gravitational-evidence.json", rows)
        self.assertIn("README.md", rows)
        self.assertIn("openwiki/.last-update.json", rows)
        self.assertIn("source_evidence", rows["README.md"]["roles"])
        self.assertEqual(
            [row["path"] for row in first["materials"]],
            sorted(rows),
        )
        self.assertTrue(all(not Path(path).is_absolute() for path in rows))

    def test_handoff_manifest_digest_changes_without_granting_admission(self):
        before_report = openwiki.inspect_openwiki_snapshot(self.snapshot)
        before = openwiki.build_handoff_manifest(self.snapshot, before_report)
        sidecar = self.sidecars()[0]
        payload = self.read_json(sidecar)
        payload["producerExtension"] = {"mode": "future"}
        self.write_json(sidecar, payload)
        after_report = openwiki.inspect_openwiki_snapshot(self.snapshot)
        after = openwiki.build_handoff_manifest(self.snapshot, after_report)
        self.assertNotEqual(
            openwiki.handoff_manifest_digest(before),
            openwiki.handoff_manifest_digest(after),
        )
        self.assertTrue(after_report["summary"]["proofpress_review_required"])
        self.assertTrue(
            all(
                claim["proofpress_admission"] == "not_inherited"
                for page in after_report["pages"]
                for claim in page["claims"]
            )
        )

    def test_handoff_manifest_selection_mode_matches_inspected_pages(self):
        selected = openwiki.inspect_openwiki_snapshot(
            self.snapshot, ["openwiki/quickstart.md"]
        )
        manifest = openwiki.build_handoff_manifest(
            self.snapshot, selected, selection_mode="selected_pages"
        )
        self.assertEqual(manifest["selection"]["pages"], ["openwiki/quickstart.md"])
        self.assertNotIn(
            "openwiki/geometry/physical-horizon-control.md",
            {row["path"] for row in manifest["materials"]},
        )
        with self.assertRaisesRegex(
            openwiki.OpenWikiInspectionError, "every discovered Claims sidecar"
        ):
            openwiki.build_handoff_manifest(
                self.snapshot, selected, selection_mode="full_snapshot"
            )
        with self.assertRaisesRegex(
            openwiki.OpenWikiInspectionError, "unsupported handoff selection mode"
        ):
            openwiki.build_handoff_manifest(
                self.snapshot, selected, selection_mode="invented"
            )

    def test_unknown_additive_fields_are_preserved_hashed_and_require_review(self):
        sidecar = self.sidecars()[0]
        payload = self.read_json(sidecar)
        payload["producerExtension"] = {"mode": "future"}
        payload["claims"][0]["claimExtension"] = ["future"]
        payload["claims"][0]["evidence"][0]["evidenceExtension"] = True
        payload["verification"]["verificationExtension"] = 2
        self.write_json(sidecar, payload)

        report = self.inspect()
        self.assertTrue(report["inspection_passed"])
        self.assertTrue(report["summary"]["extension_fields_present"])
        page = next(row for row in report["pages"] if row["sidecar"].endswith(sidecar.name))
        fields = {(row["path"], row["field"]) for row in page["extension_fields"]}
        self.assertIn(("$", "producerExtension"), fields)
        self.assertIn(("$.claims[0]", "claimExtension"), fields)
        self.assertIn(("$.claims[0].evidence[0]", "evidenceExtension"), fields)
        self.assertIn(("$.verification", "verificationExtension"), fields)
        self.assertTrue(all(row["digest"].startswith("sha256:") for row in page["extension_fields"]))

    def test_page_version_drift_fails_downstream_binding(self):
        page = self.snapshot / "openwiki" / "quickstart.md"
        page.write_bytes(page.read_bytes() + b"\nchanged after finalization\n")
        result = self.cli("--json", check=False)
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertTrue(report["summary"]["format_valid"])
        self.assertFalse(report["summary"]["page_bound"])
        self.assertIn(
            "page_version_mismatch",
            {issue["code"] for row in report["pages"] for issue in row["issues"]},
        )

    def test_changed_evidence_fails_currentness(self):
        source = self.snapshot / "evidence" / "gravitational-evidence.json"
        source.write_text(
            source.read_text(encoding="utf-8").replace(
                '"schema": "ektorus.paired-evidence.v1"',
                '"schema": "tampered.evidence.v2"',
            ),
            encoding="utf-8",
        )
        report = self.inspect(check=False)
        self.assertFalse(report["inspection_passed"])
        self.assertFalse(report["summary"]["evidence_current"])
        codes = {issue["code"] for row in report["pages"] for issue in row["issues"]}
        self.assertTrue(
            {"evidence_version_mismatch", "evidence_range_unresolved"} & codes
        )

    def test_unchanged_line_evidence_can_relocate_without_becoming_stale(self):
        source = self.snapshot / "evidence" / "gravitational-evidence.json"
        source.write_bytes(b"\n" + source.read_bytes())
        report = self.inspect()
        self.assertTrue(report["summary"]["evidence_current"])

    def test_missing_source_fails_currentness_without_forging_a_format_error(self):
        (self.snapshot / "README.md").unlink()
        report = self.inspect(check=False)
        self.assertTrue(report["summary"]["format_valid"])
        self.assertFalse(report["summary"]["evidence_current"])
        self.assertIn(
            "missing_file",
            {issue["code"] for row in report["pages"] for issue in row["issues"]},
        )

    def test_unsupported_schema_version_fails_closed(self):
        sidecar = self.sidecars()[0]
        payload = self.read_json(sidecar)
        payload["schemaVersion"] = 2
        self.write_json(sidecar, payload)
        report = self.inspect(check=False)
        self.assertFalse(report["summary"]["format_valid"])
        self.assertIn(
            "unsupported_schema_version",
            {issue["code"] for row in report["pages"] for issue in row["issues"]},
        )

    def test_unsupported_evidence_version_fails_closed(self):
        sidecar = self.sidecars()[0]
        payload = self.read_json(sidecar)
        payload["claims"][0]["evidence"][0]["version"] = "repo-lines-v2:opaque"
        self.write_json(sidecar, payload)
        report = self.inspect(check=False)
        self.assertFalse(report["summary"]["format_valid"])
        self.assertFalse(report["summary"]["evidence_current"])
        self.assertIn(
            "unsupported_evidence_version",
            {issue["code"] for row in report["pages"] for issue in row["issues"]},
        )

    def test_missing_required_claim_field_fails_closed(self):
        sidecar = self.sidecars()[0]
        payload = self.read_json(sidecar)
        del payload["claims"][0]["statement"]
        self.write_json(sidecar, payload)
        report = self.inspect(check=False)
        self.assertFalse(report["summary"]["format_valid"])
        self.assertIn(
            "missing_required_field",
            {issue["code"] for row in report["pages"] for issue in row["issues"]},
        )

    def test_evidence_path_traversal_fails_closed(self):
        sidecar = self.sidecars()[0]
        payload = self.read_json(sidecar)
        payload["claims"][0]["evidence"][0]["resource"] = "repo://../secret.txt#L1-L1"
        self.write_json(sidecar, payload)
        report = self.inspect(check=False)
        self.assertFalse(report["summary"]["format_valid"])
        self.assertFalse(report["summary"]["evidence_current"])
        self.assertIn(
            "path_traversal",
            {issue["code"] for row in report["pages"] for issue in row["issues"]},
        )

    def test_selected_page_path_traversal_fails_closed(self):
        report = self.inspect("--page", "../secret.md", check=False)
        self.assertFalse(report["inspection_passed"])
        self.assertEqual(report["summary"]["page_count"], 0)
        self.assertIn("path_traversal", {issue["code"] for issue in report["issues"]})

    def test_duplicate_json_keys_fail_closed(self):
        sidecar = self.sidecars()[0]
        raw = sidecar.read_text(encoding="utf-8")
        raw = raw.replace('"schemaVersion": 1,', '"schemaVersion": 1,\n  "schemaVersion": 1,', 1)
        sidecar.write_text(raw, encoding="utf-8")
        report = self.inspect(check=False)
        self.assertFalse(report["summary"]["format_valid"])
        self.assertIn(
            "duplicate_json_key",
            {issue["code"] for row in report["pages"] for issue in row["issues"]},
        )

    def test_claim_ids_must_be_globally_unique_across_pages(self):
        first, second = self.sidecars()
        first_payload, second_payload = self.read_json(first), self.read_json(second)
        second_payload["claims"].append(first_payload["claims"][0])
        self.write_json(second, second_payload)
        report = self.inspect(check=False)
        self.assertFalse(report["summary"]["format_valid"])
        duplicates = [
            issue
            for row in report["pages"]
            for issue in row["issues"]
            if issue["code"] == "duplicate_claim_id"
        ]
        self.assertEqual(len(duplicates), 2)

    @unittest.skipIf(not hasattr(os, "symlink"), "symbolic links unavailable")
    def test_evidence_symlink_is_not_a_source_snapshot_boundary(self):
        source = self.snapshot / "README.md"
        real = self.snapshot / "README-real.md"
        source.rename(real)
        source.symlink_to(real.name)
        report = self.inspect(check=False)
        self.assertFalse(report["summary"]["evidence_current"])
        self.assertIn(
            "filesystem_alias",
            {issue["code"] for row in report["pages"] for issue in row["issues"]},
        )

    @unittest.skipIf(not hasattr(os, "symlink"), "symbolic links unavailable")
    def test_openwiki_directory_symlink_fails_before_sidecar_discovery(self):
        real = self.snapshot / "openwiki-real"
        (self.snapshot / "openwiki").rename(real)
        (self.snapshot / "openwiki").symlink_to(real.name, target_is_directory=True)
        report = self.inspect(check=False)
        self.assertFalse(report["inspection_passed"])
        self.assertEqual(report["summary"]["page_count"], 0)
        self.assertIn("filesystem_alias", {issue["code"] for issue in report["issues"]})


if __name__ == "__main__":
    unittest.main()
