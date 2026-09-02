import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER_UI = ROOT / "proofpress_self_hosted" / "owner_ui.html"


class WebmcpOwnerSurfaceTests(unittest.TestCase):
    def setUp(self):
        self.page = OWNER_UI.read_text(encoding="utf-8")

    def test_registers_document_or_navigator_model_context(self):
        self.assertIn("document.modelContext||navigator.modelContext", self.page)
        self.assertIn("registerTool", self.page)

    def test_required_governance_tools_are_declared(self):
        for name in (
            "get_current_context",
            "get_review_state",
            "get_lineage",
            "respond_to_review",
        ):
            self.assertIn(f'name:"{name}"', self.page)

    def test_approval_is_not_exposed_as_a_webmcp_tool(self):
        names = re.findall(r'name:"([a-z_]+)"', self.page)
        self.assertNotIn("approve", names)
        self.assertNotIn("approve_conclusion", names)
        self.assertNotIn("admit", names)
        self.assertIn("approve is not exposed", self.page)

    def test_tools_return_structured_text_content(self):
        self.assertIn("function toolText", self.page)
        self.assertIn('type:"text"', self.page)

    def test_html_escape_helper_keeps_entity_replacements(self):
        line = next(row for row in self.page.splitlines() if row.startswith("const esc="))
        for name in ("amp;", "lt;", "gt;", "quot;"):
            self.assertIn("&" + name, line)
        self.assertIn("&#39;", line)
        self.assertNotIn(r'"\"":""', line)


if __name__ == "__main__":
    unittest.main()
