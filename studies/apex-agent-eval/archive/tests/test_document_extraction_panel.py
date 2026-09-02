import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "studies/apex-agent-eval/retrieval_adapter"))
from freeze_document_extraction_panel_private import freeze


class DocumentExtractionPanelTests(unittest.TestCase):
    def test_freeze_is_deterministic_and_outcome_blind(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); sources = []
            for index in range(5):
                path = root / f"{index}.pdf"; path.write_bytes(f"pdf-{index}".encode())
                sources.append({"path": str(path), "uri": f"private://{index}",
                                "media_type": "application/pdf", "task_score": index})
            first = freeze({"sources": sources}, development_count=2, heldout_count=2)
            second = freeze({"sources": list(reversed(sources))}, development_count=2, heldout_count=2)
            self.assertEqual(first, second)
            self.assertFalse(first["downstream_task_outcome_access"])
            self.assertTrue(all("path" not in row and "task_score" not in row
                                for row in first["sources"]))

    def test_digest_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.pdf"; path.write_bytes(b"x")
            with self.assertRaisesRegex(ValueError, "digest mismatch"):
                freeze({"sources": [{"path": str(path), "uri": "x",
                        "content_digest": "sha256:" + "0" * 64}]},
                       development_count=1, heldout_count=1)


if __name__ == "__main__":
    unittest.main()
