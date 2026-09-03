import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER_UI = ROOT / "web" / "owner" / "src" / "main.tsx"


class WebmcpOwnerSurfaceTests(unittest.TestCase):
    def setUp(self):
        self.page = OWNER_UI.read_text(encoding="utf-8")

    def test_registers_document_or_navigator_model_context(self):
        self.assertIn("document as any).modelContext", self.page)
        self.assertIn("navigator as any).modelContext", self.page)
        self.assertIn("registerTool", self.page)

    def test_required_governance_tools_are_declared(self):
        for name in (
            "get_current_context",
            "get_review_state",
            "get_lineage",
            "respond_to_review",
        ):
            self.assertRegex(self.page, rf'name:\s*"{name}"')

    def test_approval_is_not_exposed_as_a_webmcp_tool(self):
        names = re.findall(r'name:\s*"([a-z_]+)"', self.page)
        self.assertNotIn("approve", names)
        self.assertNotIn("approve_conclusion", names)
        self.assertNotIn("admit", names)
        self.assertIn("Approve is not exposed", self.page)

    def test_tools_return_structured_text_content(self):
        self.assertIn("const toolText", self.page)
        self.assertRegex(self.page, r'type:\s*"text"')

    def test_react_renders_untrusted_text_without_inner_html(self):
        self.assertNotIn("dangerouslySetInnerHTML", self.page)

    def test_mvp_has_no_assistant_calls_or_entry_points(self):
        self.assertNotIn('/owner/api/ask', self.page)
        self.assertNotIn('Ask Proofpress', self.page)

    def test_evidence_is_readable_without_html_injection(self):
        self.assertIn('EvidenceContent', self.page)
        self.assertIn('Technical receipt', self.page)
        self.assertNotIn("innerHTML", self.page)

    def test_pending_and_recommendation_surfaces_are_neutral(self):
        for stale_token in ("#8A6210", "#F5EEDC", "#F5C", "yellow"):
            self.assertNotIn(stale_token, self.page)
        css = (ROOT / "web" / "owner" / "src" / "index.css").read_text()
        self.assertIn("--wash: #f1efe8", css)
        self.assertIn("background: var(--wash)", css)
        self.assertNotIn("yellow", css)

    def test_owner_chrome_uses_consistent_svg_icons_and_accessible_controls(self):
        for icon in ("Home", "ShieldCheck", "BookOpen", "Activity", "KeyRound"):
            self.assertIn(icon, self.page)
        self.assertIn('aria-label="Activity pages"', self.page)
        self.assertIn("disabled={busy}", self.page)


if __name__ == "__main__":
    unittest.main()
