import contextlib
import io
import unittest
from unittest.mock import Mock, patch

from proofpress.hosted.remote import main


class RevisionInstructionsTests(unittest.TestCase):
    def test_prints_read_only_handoff(self):
        client = Mock()
        client.review_receipt.return_value = {
            "revision_request": {"event_id": "evt_request"},
            "review": {"note": "Limit to population A."},
        }
        output = io.StringIO()
        with patch("proofpress.hosted.remote._client", return_value=client), contextlib.redirect_stdout(output):
            main(["--base-url", "https://example.test", "revision-instructions", "knw_original"])
        self.assertIn('"revision_of": "knw_original"', output.getvalue())
        self.assertIn('"revision_request_ref": "evt_request"', output.getvalue())
        self.assertIn("Limit to population A.", output.getvalue())
        self.assertIn("Do not approve or overwrite", output.getvalue())
        client.review_conclusion.assert_not_called()

    def test_missing_request_fails_without_fabricated_instructions(self):
        client = Mock()
        client.review_receipt.return_value = {}
        with patch("proofpress.hosted.remote._client", return_value=client), self.assertRaisesRegex(SystemExit, "No revision request"):
            main(["--base-url", "https://example.test", "revision-instructions", "knw_original"])
