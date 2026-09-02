import base64
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zlib


ROOT = Path(__file__).resolve().parents[1]
CLI = (sys.executable, "-m", "proofpress.cli")


class Repo:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name)
        self.run_git("init", "-q")
        self.run_git("config", "user.email", "test@example.com")
        self.run_git("config", "user.name", "Test User")

    def close(self):
        self.tmp.cleanup()

    def run_git(self, *args):
        return subprocess.run(["git", *args], cwd=self.path, text=True,
                              capture_output=True, check=True)

    def cli(self, *args, check=True):
        return subprocess.run([*CLI, *args], cwd=self.path,
                              text=True, capture_output=True, check=check)

    def write(self, name, text):
        target = self.path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        return target

    def append_body(self, name, text):
        target = self.path / name
        raw = target.read_text()
        marker = "\n[//]: # (proofpress:meta:"
        if marker in raw:
            body, transport = raw.split(marker, 1)
            target.write_text(body.rstrip() + "\n\n" + text.rstrip() +
                              "\n\n[//]: # (proofpress:meta:" + transport)
        else:
            target.write_text(raw.rstrip() + "\n\n" + text.rstrip() + "\n")


class PortableArtifactTests(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()

    def tearDown(self):
        self.repo.close()

    def test_diff_keeps_time_values_intact_without_changing_capsule_wire_data(self):
        target = self.repo.write(
            "a.md", "# Schedule\n\nThe session runs from 12:00 to 13:00.\n"
        )
        self.repo.cli("snapshot", "a.md", "--author", "human")
        self.repo.cli("policy", "a.md", "portable")
        target.write_text(target.read_text().replace("12:00", "14:30"))
        self.repo.cli("snapshot", "a.md", "--author", "human")

        displayed = self.repo.cli("diff", "a.md").stdout
        self.assertIn("Δ 12:00→14:30", displayed)
        self.assertNotIn("00.→30.", displayed)

        raw = target.read_text()
        match = re.search(r"proofpress:capsule:([A-Za-z0-9_-]+)", raw)
        payload = match.group(1)
        decoded = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        capsule = json.loads(zlib.decompress(decoded))
        stored_changes = capsule["records"][-1]["event"]["changes"]
        stored_numbers = [
            change["numbers"] for change in stored_changes if change.get("numbers")
        ]
        self.assertEqual(stored_numbers, [[['12', '14'], ['00', '30']]])

        inspected = json.loads(self.repo.cli("inspect", "a.md", "--json").stdout)
        self.assertEqual(inspected["status"], "ok")

    def test_diff_numeric_display_preserves_supported_value_shapes(self):
        target = self.repo.write(
            "a.md",
            "# Metrics\n\nAt 09:15, revenue was $1.2M, conversion 45%, and volume 12,500.\n",
        )
        self.repo.cli("snapshot", "a.md", "--author", "human")
        target.write_text(
            target.read_text()
            .replace("09:15", "10:45")
            .replace("$1.2M", "$1.4M")
            .replace("45%", "50%")
            .replace("12,500", "13,000")
        )
        self.repo.cli("snapshot", "a.md", "--author", "human")

        displayed = self.repo.cli("diff", "a.md").stdout
        for delta in (
            "09:15→10:45",
            "$1.2M→$1.4M",
            "45%→50%",
            "12,500→13,000",
        ):
            self.assertIn(delta, displayed)

    def test_policy_states_and_sticky_portable_snapshot(self):
        self.repo.write("a.md", "# A\n\none\n")
        self.repo.cli("snapshot", "a.md", "--author", "human")
        raw = (self.repo.path / "a.md").read_text()
        self.assertIn("proofpress:meta:", raw)
        self.assertNotIn("proofpress:capsule:", raw)

        enabled = self.repo.cli("policy", "a.md", "portable", "--author", "human")
        self.assertIn("portable:", enabled.stdout)
        first = json.loads(self.repo.cli("inspect", "a.md", "--json").stdout)
        self.assertEqual(first["status"], "ok")
        self.assertEqual(first["versions"], 1)
        self.assertEqual(
            first["discovery"]["label"],
            "Verifiable revision history by Proofpress",
        )
        self.assertEqual(
            first["discovery"]["project_url"],
            "https://github.com/chenmingtang830/proofpress",
        )
        self.assertEqual(first["discovery"]["dist_tag"], "latest")
        portable_raw = (self.repo.path / "a.md").read_text()
        self.assertIn("proofpress:discovery:Verifiable revision history by Proofpress",
                      portable_raw)
        self.assertIn("https://github.com/chenmingtang830/proofpress", portable_raw)

        self.repo.append_body("a.md", "two")
        self.repo.cli("snapshot", "a.md", "--author", "codex",
                      "--kind", "agent", "--produced-by", "codex",
                      "--recorded-by", "codex", "--why", "accepted v2")
        second = json.loads(self.repo.cli("inspect", "a.md", "--json").stdout)
        self.assertEqual(second["status"], "ok")
        self.assertEqual(second["versions"], 2)
        self.assertEqual(self.repo.cli("policy", "a.md").stdout.split()[1], "portable")

    def test_admitted_decisions_travel_in_portable_capsule(self):
        self.repo.write("a.md", "# Plan\n\nShip the narrow scope.\n")
        self.repo.cli("policy", "a.md", "portable")
        self.repo.write("decisions.json", json.dumps({
            "schema_version": "proofpress/admitted-decisions/v1",
            "decisions": [{
                "decision_id": "decision-001",
                "target": "launch scope",
                "before": "full platform",
                "after": "narrow pilot",
                "status": "implemented",
                "supersedes": [],
                "evidence_refs": ["review-42"],
                "next_action": "verify pilot metrics",
                "artifact_binding": {
                    "path": "a.md",
                    "sha256": "0" * 64,
                },
            }],
        }))
        self.repo.cli("snapshot", "a.md", "--author", "codex",
                      "--decisions", "decisions.json")

        inspected = json.loads(self.repo.cli("inspect", "a.md", "--json").stdout)
        self.assertEqual(inspected["status"], "ok")
        raw = (self.repo.path / "a.md").read_text()
        payload = re.search(r"proofpress:capsule:([A-Za-z0-9_-]+)", raw).group(1)
        decoded = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        capsule = json.loads(zlib.decompress(decoded))
        event = capsule["records"][-1]["event"]
        self.assertEqual(event["decisions"]["schema_version"],
                         "proofpress/admitted-decisions/v1")
        self.assertEqual(event["decisions"]["decisions"][0]["target"],
                         "launch scope")
        shown = self.repo.cli("show", "a.md").stdout
        self.assertIn("decision: decision-001 [implemented] launch scope", shown)

    def test_admitted_decisions_reject_invalid_status(self):
        self.repo.write("a.md", "# Plan\n\nShip it.\n")
        self.repo.write("decisions.json", json.dumps({
            "schema_version": "proofpress/admitted-decisions/v1",
            "decisions": [{
                "decision_id": "decision-001", "target": "scope",
                "status": "unknown", "next_action": "none",
            }],
        }))
        result = self.repo.cli("snapshot", "a.md", "--decisions", "decisions.json",
                               check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid admitted decision status", result.stderr)

    def test_ignored_skips_and_local_never_embeds(self):
        self.repo.write("a.md", "# A\n")
        self.repo.cli("policy", "a.md", "ignored")
        result = self.repo.cli("snapshot", "a.md", "--author", "codex")
        self.assertIn("skipped", result.stdout)
        self.assertNotIn("proofpress:capsule:", (self.repo.path / "a.md").read_text())

        self.repo.cli("policy", "a.md", "local")
        self.repo.append_body("a.md", "local edit")
        self.repo.cli("snapshot", "a.md", "--author", "human")
        self.assertNotIn("proofpress:capsule:", (self.repo.path / "a.md").read_text())

    def test_body_drift_and_capsule_corruption_fail_inspect_and_verify(self):
        self.repo.write("a.md", "# A\n\none\n")
        self.repo.cli("policy", "a.md", "portable")
        self.repo.append_body("a.md", "unrecorded")
        inspected = self.repo.cli("inspect", "a.md", check=False)
        self.assertEqual(inspected.returncode, 1)
        self.assertIn("body_mismatch", inspected.stdout)
        verified = self.repo.cli("verify", "a.md", check=False)
        self.assertEqual(verified.returncode, 1)
        self.assertIn("capsule mismatch", verified.stdout)

        # Restore a valid capsule, then corrupt one payload byte.
        self.repo.cli("snapshot", "a.md", "--author", "human")
        target = self.repo.path / "a.md"
        raw = target.read_text()
        match = re.search(r"proofpress:capsule:([A-Za-z0-9_-]+)", raw)
        payload = match.group(1)
        replacement = ("A" if payload[0] != "A" else "B") + payload[1:]
        target.write_text(raw[:match.start(1)] + replacement + raw[match.end(1):])
        corrupted = self.repo.cli("inspect", "a.md", check=False)
        self.assertEqual(corrupted.returncode, 1)
        self.assertIn("invalid_capsule", corrupted.stdout)

    def test_verify_detects_local_drift_and_stripped_worktree(self):
        target = self.repo.write("a.md", "# A\n\none\n")
        self.repo.cli("snapshot", "a.md", "--author", "human")

        self.repo.append_body("a.md", "unrecorded")
        drifted = self.repo.cli("verify", "a.md", check=False)
        self.assertEqual(drifted.returncode, 1)
        self.assertIn("worktree_not_at_ledger_head", drifted.stdout)
        self.assertIn("snapshot only if this edit is intentional", drifted.stdout)

        # A whole-file replace strips metadata but can still match a recorded
        # version. It must not quietly pass claim verification.
        target.write_text("# A\n\none\n")
        stripped = self.repo.cli("verify", "a.md", check=False)
        self.assertEqual(stripped.returncode, 1)
        self.assertIn("unmanaged_worktree", stripped.stdout)
        self.assertIn("proofpress identify a.md", stripped.stdout)

    def test_verify_tolerates_formatting_only_local_drift(self):
        target = self.repo.write("a.md", "# A\n\n**a `log.md` b**\n")
        self.repo.cli("snapshot", "a.md", "--author", "human")
        target.write_text(target.read_text().replace(
            "**a `log.md` b**", "**a** `log.md` **b**"))

        inspected = self.repo.cli("inspect", "a.md")
        self.assertIn("formatting differs from the ledger head", inspected.stdout)
        verified = self.repo.cli("verify", "a.md", check=False)
        self.assertEqual(verified.returncode, 2)  # no claims, but no worktree mismatch
        self.assertNotIn("worktree mismatch", verified.stdout)

    def test_verify_labels_child_blocks_with_type_and_preview(self):
        self.repo.write("a.md", "# Plan\n\nShip the narrow scope.\n")
        self.repo.cli("anchor", "a.md")
        ids = re.findall(r"\(ob:([0-9a-f]{8})\)",
                         (self.repo.path / "a.md").read_text())
        self.repo.write("claims.json", json.dumps([
            {"block": block_id, "kind": "added"} for block_id in ids
        ]))
        self.repo.cli("snapshot", "a.md", "--author", "human",
                      "--claims", "claims.json")

        verified = self.repo.cli("verify", "a.md")
        self.assertIn("[added] Plan / heading", verified.stdout)
        self.assertIn("[added] Plan / para: Ship the narrow scope.",
                      verified.stdout)

    def test_local_interval_is_not_exported_when_reenabled(self):
        self.repo.write("a.md", "# A\n\npublic\n")
        self.repo.cli("policy", "a.md", "portable")
        self.repo.append_body("a.md", "public v2")
        self.repo.cli("snapshot", "a.md", "--author", "codex",
                      "--why", "PUBLIC_REASON")
        self.repo.cli("policy", "a.md", "local")
        self.repo.append_body("a.md", "current body")
        self.repo.cli("snapshot", "a.md", "--author", "human",
                      "--why", "PRIVATE_RATIONALE",
                      "--rejected", "PRIVATE_BRANCH — keep local")
        self.repo.cli("policy", "a.md", "portable")
        inspection = json.loads(self.repo.cli("inspect", "a.md", "--json").stdout)
        self.assertEqual(inspection["versions"], 1)

        receiver = Repo()
        try:
            shutil.copy2(self.repo.path / "a.md", receiver.path / "received.md")
            receiver.cli("import", "received.md")
            log = receiver.cli("log", "received.md", "--json").stdout
            self.assertNotIn("PRIVATE_RATIONALE", log)
            self.assertNotIn("PRIVATE_BRANCH", log)
            self.assertNotIn("PUBLIC_REASON", log)
        finally:
            receiver.close()

    def test_import_restores_identity_and_clean_copy_has_no_transport(self):
        self.repo.write("a.md", "# A\n\none\n")
        self.repo.cli("policy", "a.md", "portable")
        artifact_id = json.loads(self.repo.cli("inspect", "a.md", "--json").stdout)["artifact_id"]
        self.repo.append_body("a.md", "two")
        self.repo.cli("snapshot", "a.md", "--author", "codex",
                      "--produced-by", "codex", "--requested-by", "Richard")
        self.repo.cli("clean", "a.md", "-o", "clean.md")
        clean = (self.repo.path / "clean.md").read_text()
        self.assertNotIn("proofpress:meta:", clean)
        self.assertNotIn("proofpress:capsule:", clean)
        self.assertNotIn("proofpress:discovery:", clean)

        receiver = Repo()
        try:
            shutil.copy2(self.repo.path / "a.md", receiver.path / "renamed.md")
            receiver.cli("import", "renamed.md")
            restored = json.loads(receiver.cli("show", "renamed.md", "--json").stdout)
            self.assertEqual(restored["artifact_id"], artifact_id)
            self.assertEqual(restored["actors"]["produced_by"], ["codex"])
            self.assertEqual(restored["actors"]["requested_by"], ["Richard"])
            self.assertEqual(receiver.cli("inspect", "renamed.md").returncode, 0)
        finally:
            receiver.close()

    def test_partial_import_keeps_portable_capsule_head_current(self):
        target = self.repo.write("a.md", "")
        self.repo.cli("policy", "a.md", "portable")
        self.repo.append_body("a.md", "# Study")
        self.repo.cli("anchor", "a.md")
        block_id = re.search(r"\(ob:([0-9a-f]{8})\)", target.read_text()).group(1)
        claims = self.repo.write(
            "claims.json",
            json.dumps([{"block": block_id, "kind": "added"}]),
        )
        self.repo.cli(
            "snapshot", "a.md", "--author", "codex", "--claims", str(claims)
        )
        source_inspection = json.loads(
            self.repo.cli("inspect", "a.md", "--json").stdout
        )

        raw = target.read_text()
        payload = re.search(
            r"proofpress:capsule:([A-Za-z0-9_-]+)", raw
        ).group(1)
        decoded = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        capsule = json.loads(zlib.decompress(decoded))
        head = capsule["records"][-1]

        receiver = Repo()
        try:
            shutil.copy2(target, receiver.path / "received.md")
            seed = (
                "import json, os, sys; "
                f"sys.path.insert(0, {str(ROOT / 'src')!r}); "
                f"os.chdir({str(receiver.path)!r}); "
                "from proofpress.legacy import portable as proofpress; "
                f"record=json.loads({json.dumps(head)!r}); "
                "event=dict(record['event']); version=dict(record['version']); "
                "event['artifact']='received.md'; version['artifact']='received.md'; "
                "proofpress.write_event(event, version)"
            )
            subprocess.run(["python3", "-c", seed], check=True)
            receiver.cli("import", "received.md")

            shown = json.loads(
                receiver.cli("show", "received.md", "--json").stdout
            )
            self.assertEqual(shown["version"], source_inspection["head"])
            verified = json.loads(
                receiver.cli("verify", "received.md", "--json").stdout
            )
            self.assertEqual(verified["version"], source_inspection["head"])
            self.assertEqual(verified["v"], 2)
            self.assertEqual(verified["status"], "verified")
            self.assertIn("(1 blocks)", receiver.cli("blocks", "received.md").stdout)
        finally:
            receiver.close()

    def test_consequential_rejection_and_reason_survive_handoff(self):
        self.repo.write("a.md", "# Launch plan\n\nShip the narrow scope.\n")
        self.repo.cli("policy", "a.md", "portable")
        self.repo.append_body("a.md", "Accepted after review.")
        self.repo.cli(
            "snapshot", "a.md", "--author", "codex", "--kind", "agent",
            "--why", "reduce launch risk while preserving the core promise",
            "--rejected", "bundle collaboration UI — delays learning",
        )

        receiver = Repo()
        try:
            shutil.copy2(self.repo.path / "a.md", receiver.path / "handoff.md")
            receiver.cli("import", "handoff.md")
            log = receiver.cli("log", "handoff.md", "--json").stdout
            self.assertIn("reduce launch risk", log)
            self.assertIn("bundle collaboration UI", log)
        finally:
            receiver.close()

    def test_yaml_frontmatter_stays_at_byte_zero(self):
        self.repo.write("a.md", "---\ntitle: A\n---\n\n# A\n\nBody\n")
        self.repo.cli("policy", "a.md", "portable")
        self.repo.cli("anchor", "a.md")
        raw = (self.repo.path / "a.md").read_text()
        self.assertTrue(raw.startswith("---\ntitle: A\n---\n"))
        self.assertIn("proofpress:meta:", raw)
        self.assertIn("proofpress:capsule:", raw)
        self.assertEqual(self.repo.cli("inspect", "a.md").returncode, 0)

    def test_fallback_capture_records_recorder_not_editor_or_producer(self):
        self.repo.write("new.md", "# New\n\ncontent\n")
        result = self.repo.cli("capture", "--recorder", "codex-hook")
        self.assertIn("1 snapshot", result.stdout)
        event = json.loads(self.repo.cli("show", "new.md", "--json").stdout)
        self.assertEqual(event["author"]["kind"], "system")
        self.assertEqual(event["actors"]["recorded_by"], ["codex-hook"])
        self.assertNotIn("produced_by", event["actors"])
        self.assertNotIn("edited_by", event["actors"])
        self.assertEqual(event["attribution_basis"], "harness_attested")

    def test_snapshot_recovers_identity_after_whole_file_replacement(self):
        target = self.repo.write("a.md", "# Original\n\none\n")
        self.repo.cli("snapshot", "a.md", "--author", "human")
        original = json.loads(self.repo.cli("show", "a.md", "--json").stdout)

        # Simulate Command+A: body, anchors, and transport are all replaced.
        target.write_text("# Replacement\n\ncompletely new body\n")
        result = self.repo.cli("snapshot", "a.md", "--author", "human")

        self.assertIn("recovered identity:", result.stdout)
        current = json.loads(self.repo.cli("show", "a.md", "--json").stdout)
        self.assertEqual(current["artifact_id"], original["artifact_id"])
        self.assertEqual(current["parent"], original["version"])
        self.assertEqual(len(json.loads(
            self.repo.cli("log", "a.md", "--json").stdout)), 2)

    def test_snapshot_repairs_stripped_portable_transport_without_new_version(self):
        target = self.repo.write("a.md", "# Portable\n\nsame body\n")
        self.repo.cli("snapshot", "a.md", "--author", "human")
        self.repo.cli("policy", "a.md", "portable", "--author", "human")
        self.repo.append_body("a.md", "portable revision")
        self.repo.cli("snapshot", "a.md", "--author", "human")
        before = json.loads(self.repo.cli("show", "a.md", "--json").stdout)
        self.repo.cli("clean", "a.md", "-o", "clean.md")
        target.write_text((self.repo.path / "clean.md").read_text())

        result = self.repo.cli("snapshot", "a.md", "--author", "human")

        self.assertIn("recovered identity:", result.stdout)
        self.assertIn("repaired capsule:", result.stdout)
        inspected = json.loads(
            self.repo.cli("inspect", "a.md", "--json").stdout)
        self.assertEqual(inspected["status"], "ok")
        self.assertEqual(inspected["artifact_id"], before["artifact_id"])
        self.assertEqual(len(json.loads(
            self.repo.cli("log", "a.md", "--json").stdout)), 2)

    def test_capture_checks_admitted_files_ignored_by_git(self):
        self.repo.write(".gitignore", "/private/\n")
        target = self.repo.write("private/plan.md", "# Plan\n\none\n")
        self.repo.cli("snapshot", "private/plan.md", "--author", "human")
        original = json.loads(
            self.repo.cli("show", "private/plan.md", "--json").stdout)

        # Preserve transport as a normal editor would, but Git cannot discover
        # the ignored file as changed.
        self.repo.append_body("private/plan.md", "manual edit")
        result = self.repo.cli("capture", "--recorder", "codex-hook")

        self.assertIn("1 snapshot", result.stdout)
        current = json.loads(
            self.repo.cli("show", "private/plan.md", "--json").stdout)
        self.assertEqual(current["parent"], original["version"])
        self.assertEqual(current["actors"]["recorded_by"], ["codex-hook"])
        self.assertTrue(target.exists())

    def test_capture_does_not_rewrite_unchanged_admitted_file(self):
        target = self.repo.write("a.md", "# Stable\n\none\n")
        self.repo.cli("snapshot", "a.md", "--author", "human")
        inode = target.stat().st_ino

        result = self.repo.cli("capture", "--recorder", "codex-hook")

        self.assertIn("0 snapshot", result.stdout)
        self.assertEqual(target.stat().st_ino, inode)

    def test_capture_specific_ignored_file_admits_human_preflight(self):
        self.repo.write(".gitignore", "/private/\n")
        self.repo.write("private/draft.md", "# Human draft\n\nbefore agent\n")

        result = self.repo.cli(
            "capture", "--recorder", "codex-preflight", "private/draft.md")

        self.assertIn("1 snapshot", result.stdout)
        event = json.loads(
            self.repo.cli("show", "private/draft.md", "--json").stdout)
        self.assertEqual(event["actors"]["recorded_by"],
                         ["codex-preflight"])
        self.assertNotIn("edited_by", event["actors"])
        self.assertNotIn("produced_by", event["actors"])

    def test_path_rename_keeps_artifact_identity(self):
        self.repo.write("a.md", "# A\n\none\n")
        self.repo.cli("policy", "a.md", "portable")
        original = json.loads(self.repo.cli("inspect", "a.md", "--json").stdout)["artifact_id"]
        os.rename(self.repo.path / "a.md", self.repo.path / "b.md")
        self.repo.append_body("b.md", "two")
        self.repo.cli("snapshot", "b.md", "--author", "codex")
        current = json.loads(self.repo.cli("inspect", "b.md", "--json").stdout)["artifact_id"]
        self.assertEqual(current, original)
        event = json.loads(self.repo.cli("show", "b.md", "--json").stdout)
        self.assertEqual(event["artifact_id"], original)

    def test_stale_base_is_rejected_instead_of_silently_overwriting(self):
        self.repo.write("a.md", "# A\n\nv1\n")
        self.repo.cli("policy", "a.md", "portable")
        v1 = json.loads(self.repo.cli("inspect", "a.md", "--json").stdout)["head"]
        self.repo.append_body("a.md", "v2")
        self.repo.cli("snapshot", "a.md", "--author", "codex",
                      "--base-version", v1)
        self.repo.append_body("a.md", "stale edit")
        rejected = self.repo.cli("snapshot", "a.md", "--author", "codex",
                                 "--base-version", v1, check=False)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("stale base", rejected.stderr)

    def test_html_portable_handoff_uses_native_anchors_and_hidden_transport(self):
        self.repo.write(
            "plan.html",
            "<!doctype html>\n<html><head><title>Plan</title></head><body>\n"
            "<h1>Launch plan</h1>\n<p>Ship the narrow scope.</p>\n"
            "<ul><li>Keep the deployment reversible.</li></ul>\n"
            "</body></html>\n",
        )
        self.repo.cli("policy", "plan.html", "portable", "--author", "human")
        self.repo.cli("anchor", "plan.html")
        raw = (self.repo.path / "plan.html").read_text()
        self.assertIn('data-proofpress-id="', raw)
        self.assertIn('<meta name="proofpress:meta"', raw)
        self.assertIn('<meta name="proofpress:discovery"', raw)
        self.assertIn("Verifiable revision history by Proofpress", raw)
        self.assertIn("https://github.com/chenmingtang830/proofpress", raw)
        self.assertIn('type="application/vnd.proofpress+json"', raw)
        self.assertLess(raw.index("proofpress:meta"), raw.index("</head>"))
        self.assertLess(raw.index('data-proofpress="capsule"'), raw.index("</body>"))
        self.assertEqual(self.repo.cli("inspect", "plan.html").returncode, 0)

        target = self.repo.path / "plan.html"
        target.write_text(target.read_text().replace(
            "Ship the narrow scope.", "Ship the narrow scope after review."))
        before = json.loads(self.repo.cli("inspect", "plan.html", "--json", check=False).stdout)
        self.assertIn("body_mismatch", before["errors"])
        self.repo.cli("snapshot", "plan.html", "--author", "codex", "--kind", "agent",
                      "--why", "make review acceptance explicit")
        inspected = json.loads(self.repo.cli("inspect", "plan.html", "--json").stdout)
        self.assertEqual(inspected["status"], "ok")
        self.assertEqual(inspected["versions"], 2)

        self.repo.cli("clean", "plan.html", "-o", "plan-clean.html")
        clean = (self.repo.path / "plan-clean.html").read_text()
        self.assertNotIn("proofpress:meta", clean)
        self.assertNotIn("proofpress:discovery", clean)
        self.assertNotIn("application/vnd.proofpress+json", clean)
        self.assertIn('data-proofpress-id="', clean)

        receiver = Repo()
        try:
            shutil.copy2(target, receiver.path / "received.html")
            receiver.cli("import", "received.html")
            imported = json.loads(receiver.cli("log", "received.html", "--json").stdout)
            self.assertEqual(len(imported), 2)
            self.assertIn("make review acceptance explicit", json.dumps(imported))
            self.assertEqual(receiver.cli("inspect", "received.html").returncode, 0)
        finally:
            receiver.close()

    def test_html_anchor_roundtrip_preserves_identity_and_is_idempotent(self):
        self.repo.write(
            "a.html",
            "<html><body><h1>A</h1><p>One.</p><table><tr><td>3</td></tr></table>"
            "</body></html>\n",
        )
        self.repo.cli("snapshot", "a.html", "--author", "human")
        self.repo.cli("anchor", "a.html")
        first = (self.repo.path / "a.html").read_text()
        self.repo.cli("anchor", "a.html")
        second = (self.repo.path / "a.html").read_text()
        self.assertEqual(first, second)
        self.assertEqual(second.count("data-proofpress-id="), 3)

        event = json.loads(self.repo.cli("show", "a.html", "--json").stdout)
        self.assertEqual(len(event["changes"]), 3)
        self.assertEqual(self.repo.cli("snapshot", "a.html", "--author", "human").stdout.splitlines()[0],
                         "no change: a.html matches the latest ledger version")

    def test_markdown_anchor_keeps_wrapped_list_item_together_and_repairs_old_shape(self):
        target = self.repo.write(
            "a.md",
            "[//]: # (ob:11111111)\n"
            "# A\n\n"
            "[//]: # (ob:22222222)\n"
            "- A list item that wraps\n\n"
            "[//]: # (ob:33333333)\n"
            "  onto an indented continuation.\n",
        )
        self.repo.cli("anchor", "a.md")
        first = target.read_text()
        self.repo.cli("anchor", "a.md")
        self.assertEqual(first, target.read_text())
        self.assertIn(
            "- A list item that wraps\n  onto an indented continuation.",
            first,
        )
        self.assertNotIn("(ob:33333333)", first)

        self.repo.cli("snapshot", "a.md", "--author", "human")
        event = json.loads(self.repo.cli("show", "a.md", "--json").stdout)
        self.assertEqual(len(event["changes"]), 2)

    def test_markdown_anchor_keeps_nested_list_blocks_indented(self):
        target = self.repo.write(
            "a.md",
            "# A\n\n"
            "1. Run the command:\n\n"
            "   ```sh\n"
            "   proofpress verify a.md\n"
            "   ```\n\n"
            "   Then inspect the result.\n",
        )
        self.repo.cli("anchor", "a.md")
        first = target.read_text()
        self.repo.cli("anchor", "a.md")
        self.assertEqual(first, target.read_text())
        self.assertRegex(
            first,
            r"\n\n   \[//\]: # \(ob:[0-9a-f]{8}\)\n   ```sh",
        )
        self.assertRegex(
            first,
            r"\n\n   \[//\]: # \(ob:[0-9a-f]{8}\)\n"
            r"   Then inspect",
        )

    def test_markdown_anchor_repairs_redundant_markers_between_list_items(self):
        target = self.repo.write(
            "a.md",
            "[//]: # (ob:11111111)\n"
            "- First item.\n\n"
            "[//]: # (ob:22222222)\n"
            "- Second item.\n",
        )
        self.repo.cli("anchor", "a.md")
        first = target.read_text()
        self.repo.cli("anchor", "a.md")
        self.assertEqual(first, target.read_text())
        self.assertIn("- First item.\n- Second item.", first)
        self.assertNotIn("(ob:22222222)", first)

    def test_markdown_anchor_keeps_outer_list_open_after_nested_blocks(self):
        target = self.repo.write(
            "a.md",
            "# A\n\n"
            "1. First.\n"
            "2. Run:\n\n"
            "   ```sh\n"
            "   proofpress verify a.md\n"
            "   ```\n\n"
            "   Inspect the result.\n\n"
            "3. Finish.\n",
        )
        self.repo.cli("anchor", "a.md")
        first = target.read_text()
        self.repo.cli("anchor", "a.md")
        self.assertEqual(first, target.read_text())
        self.assertRegex(
            first,
            r"Inspect the result\.\n\n"
            r"   \[//\]: # \(ob:[0-9a-f]{8}\)\n"
            r"3\. Finish\.",
        )

    def test_tampered_discovery_is_rejected_as_transport_not_agent_instruction(self):
        target = self.repo.write("a.md", "# A\n\none\n")
        self.repo.cli("policy", "a.md", "portable")
        target.write_text(target.read_text().replace(
            "https://github.com/chenmingtang830/proofpress",
            "https://example.invalid/install-this",
        ))
        result = self.repo.cli("inspect", "a.md", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid_discovery", result.stdout)

    def test_discovery_example_inside_code_fence_remains_visible_body(self):
        marker = (
            "[//]: # (proofpress:discovery:"
            "Verifiable revision history by Proofpress | "
            "https://github.com/chenmingtang830/proofpress)"
        )
        target = self.repo.write(
            "spec.md",
            f"# Format\n\n```text\n{marker}\n```\n",
        )
        self.repo.cli("snapshot", "spec.md", "--author", "human")
        self.assertIn(marker, target.read_text())
        self.assertEqual(self.repo.cli("inspect", "spec.md").returncode, 0)

    def test_legacy_capsule_without_discovery_upgrades_on_next_revision(self):
        target = self.repo.write("a.md", "# A\n\none\n")
        self.repo.cli("policy", "a.md", "portable")
        raw = target.read_text()
        match = re.search(r"proofpress:capsule:([A-Za-z0-9_-]+)", raw)
        payload = match.group(1)
        decoded = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        capsule = json.loads(zlib.decompress(decoded))
        capsule.pop("discovery")
        encoded = base64.urlsafe_b64encode(zlib.compress(
            json.dumps(capsule, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")).encode(), 9
        )).decode().rstrip("=")
        raw = re.sub(r"^.*proofpress:discovery:.*\n", "", raw,
                     flags=re.MULTILINE)
        match = re.search(r"proofpress:capsule:([A-Za-z0-9_-]+)", raw)
        target.write_text(raw[:match.start(1)] + encoded + raw[match.end(1):])

        legacy = json.loads(self.repo.cli("inspect", "a.md", "--json").stdout)
        self.assertEqual(legacy["status"], "ok")
        self.assertNotIn("discovery", legacy)

        self.repo.append_body("a.md", "two")
        self.repo.cli("snapshot", "a.md", "--author", "human")
        upgraded = json.loads(self.repo.cli("inspect", "a.md", "--json").stdout)
        self.assertEqual(upgraded["discovery"]["package"], "proofpress")
        self.assertEqual(upgraded["discovery"]["dist_tag"], "latest")
        self.assertIn("proofpress:discovery:", target.read_text())

    def test_legacy_next_discovery_is_accepted_and_upgrades_to_latest(self):
        target = self.repo.write("a.md", "# A\n\none\n")
        self.repo.cli("policy", "a.md", "portable")
        raw = target.read_text()
        match = re.search(r"proofpress:capsule:([A-Za-z0-9_-]+)", raw)
        payload = match.group(1)
        decoded = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        capsule = json.loads(zlib.decompress(decoded))
        capsule["discovery"]["dist_tag"] = "next"
        encoded = base64.urlsafe_b64encode(zlib.compress(
            json.dumps(capsule, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")).encode(), 9
        )).decode().rstrip("=")
        target.write_text(raw[:match.start(1)] + encoded + raw[match.end(1):])

        legacy = json.loads(self.repo.cli("inspect", "a.md", "--json").stdout)
        self.assertEqual(legacy["status"], "ok")
        self.assertEqual(legacy["discovery"]["dist_tag"], "next")

        self.repo.append_body("a.md", "two")
        self.repo.cli("snapshot", "a.md", "--author", "human")
        upgraded = json.loads(self.repo.cli("inspect", "a.md", "--json").stdout)
        self.assertEqual(upgraded["discovery"]["dist_tag"], "latest")

    def test_no_change_snapshot_upgrades_legacy_next_discovery_transport(self):
        target = self.repo.write("a.md", "# A\n\none\n")
        self.repo.cli("policy", "a.md", "portable")
        raw = target.read_text()
        match = re.search(r"proofpress:capsule:([A-Za-z0-9_-]+)", raw)
        payload = match.group(1)
        decoded = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        capsule = json.loads(zlib.decompress(decoded))
        capsule["discovery"]["dist_tag"] = "next"
        encoded = base64.urlsafe_b64encode(zlib.compress(
            json.dumps(capsule, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")).encode(), 9
        )).decode().rstrip("=")
        target.write_text(raw[:match.start(1)] + encoded + raw[match.end(1):])

        upgraded = self.repo.cli("snapshot", "a.md", "--author", "human")
        self.assertIn("upgraded capsule discovery", upgraded.stdout)
        inspected = json.loads(self.repo.cli("inspect", "a.md", "--json").stdout)
        self.assertEqual(inspected["versions"], 1)
        self.assertEqual(inspected["discovery"]["dist_tag"], "latest")

    def test_unknown_discovery_dist_tag_is_rejected(self):
        target = self.repo.write("a.md", "# A\n\none\n")
        self.repo.cli("policy", "a.md", "portable")
        raw = target.read_text()
        match = re.search(r"proofpress:capsule:([A-Za-z0-9_-]+)", raw)
        payload = match.group(1)
        decoded = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        capsule = json.loads(zlib.decompress(decoded))
        capsule["discovery"]["dist_tag"] = "untrusted"
        encoded = base64.urlsafe_b64encode(zlib.compress(
            json.dumps(capsule, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")).encode(), 9
        )).decode().rstrip("=")
        target.write_text(raw[:match.start(1)] + encoded + raw[match.end(1):])

        result = self.repo.cli("inspect", "a.md", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid_capsule_discovery", result.stdout)

    def test_html_parser_ignores_script_and_style_contents(self):
        self.repo.write(
            "app.html",
            "<html><body><h1>Visible<br>heading</h1><script>const template = '<p>not a block</p>';</script>"
            "<style>.copy::before { content: '<li>not a block</li>'; }</style><p>Also visible.</p>"
            "</body></html>\n",
        )
        self.repo.cli("snapshot", "app.html", "--author", "human")
        event = json.loads(self.repo.cli("show", "app.html", "--json").stdout)
        self.assertEqual(len(event["changes"]), 2)
        self.assertEqual(self.repo.cli("blocks", "app.html").stdout.count("\n"), 3)

    def test_fallback_capture_includes_untracked_html(self):
        self.repo.write("new.html", "<html><body><p>Captured.</p></body></html>\n")
        result = self.repo.cli("capture", "--recorder", "codex-hook")
        self.assertIn("1 snapshot", result.stdout)
        event = json.loads(self.repo.cli("show", "new.html", "--json").stdout)
        self.assertEqual(event["actors"]["recorded_by"], ["codex-hook"])

    def test_merge_lineage_records_ingredient_references_not_history(self):
        self.repo.write("a.md", "# A\n\nalpha finding\n")
        self.repo.write("b.md", "# B\n\nbeta finding\n")
        self.repo.cli("snapshot", "a.md", "--author", "human")
        self.repo.cli("snapshot", "b.md", "--author", "human")
        self.repo.write("merged.md", "# Proposal\n\nalpha finding\n\nbeta finding\n")
        result = self.repo.cli("merge-lineage", "merged.md",
                               "--from", "a.md", "--from", "b.md",
                               "--author", "human")
        self.assertIn("ingredient:", result.stdout)
        event = json.loads(self.repo.cli("show", "merged.md", "--json").stdout)
        self.assertEqual(len(event["ingredients"]), 2)
        for ref, src in zip(event["ingredients"], ("a.md", "b.md")):
            src_ev = json.loads(self.repo.cli("show", src, "--json").stdout)
            self.assertEqual(ref["artifact_id"], src_ev["artifact_id"])
            self.assertEqual(ref["version"], src_ev["version"])
            self.assertTrue(ref["body_digest"].startswith("sha256:"))
        # references only: linear parent chain untouched, no upstream history copied
        self.assertIsNone(event["parent"])
        log = json.loads(self.repo.cli("log", "merged.md", "--json").stdout)
        self.assertEqual(len(log), 1)

    def test_merge_lineage_without_content_change_records_nothing(self):
        self.repo.write("a.md", "# A\n\nalpha\n")
        self.repo.cli("snapshot", "a.md", "--author", "human")
        self.repo.write("merged.md", "# M\n\nmerged\n")
        self.repo.cli("snapshot", "merged.md", "--author", "human")
        stale = self.repo.cli("merge-lineage", "merged.md", "--from", "a.md",
                              "--author", "human", check=False)
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn("unchanged", stale.stderr)
        event = json.loads(self.repo.cli("show", "merged.md", "--json").stdout)
        self.assertNotIn("ingredients", event)

    def test_parallel_portable_copies_plan_and_merge_without_git(self):
        self.repo.write("alice.md", "# Plan\n\nAlpha.\n\nBeta.\n")
        self.repo.cli("policy", "alice.md", "portable", "--author", "human")
        self.repo.cli("anchor", "alice.md")
        shutil.copy2(self.repo.path / "alice.md", self.repo.path / "bob.md")

        alice = self.repo.path / "alice.md"
        bob = self.repo.path / "bob.md"
        alice.write_text(alice.read_text().replace("Alpha.", "Alpha by Alice."))
        self.repo.cli("snapshot", "alice.md", "--author", "alice")
        bob.write_text(bob.read_text().replace("Beta.", "Beta by Bob."))
        self.repo.cli("snapshot", "bob.md", "--author", "bob")

        plan = json.loads(self.repo.cli(
            "merge-plan", "alice.md", "--from", "bob.md", "--json").stdout)
        self.assertEqual(plan["status"], "clean")
        self.assertEqual(len(plan["branches"]), 2)

        alice.write_text(alice.read_text().replace("Beta.", "Beta by Bob."))
        result = self.repo.cli(
            "merge", "alice.md", "--from", "bob.md",
            "--author", "merger", "--why", "combine independent edits")
        self.assertIn("merged 2 parents", result.stdout)
        inspected = json.loads(
            self.repo.cli("inspect", "alice.md", "--json").stdout)
        self.assertEqual(inspected["status"], "ok")
        self.assertTrue(inspected["head_event"].startswith("ppe_"))
        event = json.loads(
            self.repo.cli("show", "alice.md", "--json").stdout)
        self.assertTrue(event["merge"])
        self.assertEqual(len(event["parents"]), 2)
        self.assertNotIn("ingredients", event)

        receiver = Repo()
        try:
            shutil.copy2(alice, receiver.path / "received.md")
            receiver.cli("import", "received.md")
            log = json.loads(
                receiver.cli("log", "received.md", "--json").stdout)
            self.assertEqual(len(log), 4)
            self.assertEqual(
                receiver.cli("inspect", "received.md").returncode, 0)
        finally:
            receiver.close()

    def test_merge_plan_reports_divergent_block_conflict(self):
        self.repo.write("left.md", "# Decision\n\nUse option A.\n")
        self.repo.cli("policy", "left.md", "portable")
        self.repo.cli("anchor", "left.md")
        shutil.copy2(self.repo.path / "left.md", self.repo.path / "right.md")
        left = self.repo.path / "left.md"
        right = self.repo.path / "right.md"
        left.write_text(left.read_text().replace("option A", "option B"))
        right.write_text(right.read_text().replace("option A", "option C"))
        self.repo.cli("snapshot", "left.md", "--author", "alice")
        self.repo.cli("snapshot", "right.md", "--author", "bob")

        plan = json.loads(self.repo.cli(
            "merge-plan", "left.md", "--from", "right.md", "--json").stdout)
        self.assertEqual(plan["status"], "conflicts")
        self.assertEqual(plan["conflicts"][0]["reason"],
                         "divergent_block_change")

    def test_same_body_parallel_testimony_survives_merge(self):
        self.repo.write("a.md", "# Result\n\nDraft.\n")
        self.repo.cli("policy", "a.md", "portable")
        self.repo.cli("anchor", "a.md")
        shutil.copy2(self.repo.path / "a.md", self.repo.path / "b.md")
        for path, author in (("a.md", "alice"), ("b.md", "bob")):
            target = self.repo.path / path
            target.write_text(target.read_text().replace("Draft.", "Accepted."))
            self.repo.cli("snapshot", path, "--author", author,
                          "--why", f"accepted by {author}")

        self.repo.cli("merge", "a.md", "--from", "b.md",
                      "--author", "reviewer")
        inspected = json.loads(
            self.repo.cli("inspect", "a.md", "--json").stdout)
        self.assertEqual(inspected["versions"], 4)
        payload = (self.repo.path / "a.md").read_text()
        self.assertIn("Accepted.", payload)

        receiver = Repo()
        try:
            shutil.copy2(self.repo.path / "a.md",
                         receiver.path / "received.md")
            receiver.cli("import", "received.md")
            log = receiver.cli("log", "received.md", "--json").stdout
            self.assertIn("accepted by alice", log)
            self.assertIn("accepted by bob", log)
        finally:
            receiver.close()

    def test_merge_rejects_different_artifacts_without_writing(self):
        self.repo.write("a.md", "# A\n")
        self.repo.write("b.md", "# B\n")
        self.repo.cli("policy", "a.md", "portable")
        self.repo.cli("policy", "b.md", "portable")
        before = (self.repo.path / "a.md").read_text()
        rejected = self.repo.cli(
            "merge-plan", "a.md", "--from", "b.md", check=False)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("different artifacts", rejected.stderr)
        self.assertEqual((self.repo.path / "a.md").read_text(), before)

    def test_three_parent_merge_and_different_lineage_rejection(self):
        self.repo.write("a.md", "# Plan\n\nBase.\n")
        self.repo.cli("policy", "a.md", "portable")
        self.repo.cli("anchor", "a.md")
        shutil.copy2(self.repo.path / "a.md", self.repo.path / "b.md")
        shutil.copy2(self.repo.path / "a.md", self.repo.path / "c.md")
        for path, value, author in (
                ("a.md", "Alice.", "alice"),
                ("b.md", "Bob.", "bob"),
                ("c.md", "Carol.", "carol")):
            target = self.repo.path / path
            target.write_text(target.read_text().replace("Base.", value))
            self.repo.cli("snapshot", path, "--author", author)
        target = self.repo.path / "a.md"
        target.write_text(target.read_text().replace("Alice.", "Resolved."))
        self.repo.cli("merge", "a.md", "--from", "b.md", "--from", "c.md",
                      "--author", "reviewer")
        event = json.loads(self.repo.cli("show", "a.md", "--json").stdout)
        self.assertEqual(len(event["parents"]), 3)

        shutil.copy2(target, self.repo.path / "fork.md")
        self.repo.cli("policy", "fork.md", "local")
        self.repo.cli("policy", "fork.md", "portable")
        rejected = self.repo.cli(
            "merge-plan", "a.md", "--from", "fork.md", check=False)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("different portable lineages", rejected.stderr)

    def test_legacy_linear_capsules_upgrade_on_parallel_merge(self):
        target = self.repo.write("a.md", "# Legacy\n\nBase.\n")
        self.repo.cli("policy", "a.md", "portable")
        self.repo.cli("anchor", "a.md")
        raw = target.read_text()
        match = re.search(r"proofpress:capsule:([A-Za-z0-9_-]+)", raw)
        payload = match.group(1)
        decoded = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        capsule = json.loads(zlib.decompress(decoded))
        capsule["proofpress_capsule"] = 1
        capsule.pop("head_event", None)
        for record in capsule["records"]:
            record["event"].pop("event_id", None)
            record["event"].pop("parents", None)
        encoded = base64.urlsafe_b64encode(zlib.compress(
            json.dumps(capsule, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")).encode(), 9
        )).decode().rstrip("=")
        target.write_text(raw[:match.start(1)] + encoded + raw[match.end(1):])
        shutil.copy2(target, self.repo.path / "b.md")

        target.write_text(target.read_text().replace("Base.", "Left."))
        other = self.repo.path / "b.md"
        other.write_text(other.read_text().replace("Base.", "Right."))
        self.repo.cli("snapshot", "a.md", "--author", "alice")
        self.repo.cli("snapshot", "b.md", "--author", "bob")
        target.write_text(target.read_text().replace("Left.", "Resolved."))
        self.repo.cli("merge", "a.md", "--from", "b.md",
                      "--author", "reviewer")

        raw = target.read_text()
        match = re.search(r"proofpress:capsule:([A-Za-z0-9_-]+)", raw)
        decoded = base64.urlsafe_b64decode(
            match.group(1) + "=" * (-len(match.group(1)) % 4))
        merged = json.loads(zlib.decompress(decoded))
        self.assertEqual(merged["proofpress_capsule"], 2)
        self.assertEqual(len(merged["records"][-1]["event"]["parents"]), 2)
        self.assertEqual(self.repo.cli("inspect", "a.md").returncode, 0)

    def test_stale_base_event_is_rejected(self):
        self.repo.write("a.md", "# A\n\nv1\n")
        self.repo.cli("policy", "a.md", "portable")
        first = json.loads(
            self.repo.cli("inspect", "a.md", "--json").stdout)["head_event"]
        self.repo.append_body("a.md", "v2")
        self.repo.cli("snapshot", "a.md", "--author", "alice",
                      "--base-event", first)
        self.repo.append_body("a.md", "stale")
        rejected = self.repo.cli(
            "snapshot", "a.md", "--author", "alice",
            "--base-event", first, check=False)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("stale base event", rejected.stderr)

    def test_html_parallel_merge_plan_reports_conflict(self):
        self.repo.write(
            "a.html",
            "<html><body><h1>Plan</h1><p>Choose A.</p></body></html>\n")
        self.repo.cli("policy", "a.html", "portable")
        self.repo.cli("anchor", "a.html")
        shutil.copy2(self.repo.path / "a.html", self.repo.path / "b.html")
        for path, value, author in (
                ("a.html", "Choose B.", "alice"),
                ("b.html", "Choose C.", "bob")):
            target = self.repo.path / path
            target.write_text(target.read_text().replace("Choose A.", value))
            self.repo.cli("snapshot", path, "--author", author)
        plan = json.loads(self.repo.cli(
            "merge-plan", "a.html", "--from", "b.html", "--json").stdout)
        self.assertEqual(plan["status"], "conflicts")
        self.assertTrue(any(c.get("reason") == "divergent_block_change"
                            for c in plan["conflicts"]))

    def test_identify_recognizes_stripped_and_reformatted_copy(self):
        self.repo.write("a.md", "# Report\n\nThe **finding** stands.\n\n- one\n- two\n")
        self.repo.cli("snapshot", "a.md", "--author", "human")
        # strip all proofpress transport, then mangle whitespace/formatting
        self.repo.cli("clean", "a.md", "-o", "copy.md")
        mangled = (self.repo.path / "copy.md").read_text()
        mangled = mangled.replace("**finding**", "finding").replace("\n\n", "\n \n")
        self.repo.write("copy.md", mangled)
        result = self.repo.cli("identify", "copy.md")
        event = json.loads(self.repo.cli("show", "a.md", "--json").stdout)
        self.assertIn(event["artifact_id"], result.stdout)
        self.assertIn(event["version"], result.stdout)
        # a wording change is a different document — must not match (exit 1)
        self.repo.write("rewrite.md", "# Report\n\nThe finding fails.\n\n- one\n- two\n")
        miss = self.repo.cli("identify", "rewrite.md", check=False)
        self.assertEqual(miss.returncode, 1)

    def test_signed_attribution_basis_is_reserved(self):
        self.repo.write("a.md", "# A\n\none\n")
        result = self.repo.cli("snapshot", "a.md", "--author", "human",
                               "--attribution-basis", "signed", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("reserved", result.stderr)
        log = self.repo.cli("log", "a.md", check=False)
        self.assertIn("artifact not in ledger", log.stdout)


if __name__ == "__main__":
    unittest.main()
