import unittest

from document_extraction_adapters import (native_text_to_envelope,
                                          paddle_result_to_envelope)


SOURCE = {"uri": "fixture/table.pdf", "content_digest": "sha256:" + "1" * 64,
          "media_type": "application/pdf"}


class DocumentExtractionAdapterTests(unittest.TestCase):
    def test_paddle_table_html_becomes_cells_with_locators(self):
        value = paddle_result_to_envelope({"page_index": 0, "width": 100, "height": 200,
            "parsing_res_list": [{"block_label": "table", "block_bbox": [1, 2, 90, 80],
                "block_content": "<table><tr><th>Year</th><th>Tax</th></tr><tr><td>2024</td><td>$18,486</td></tr></table>"}]},
            source=SOURCE, config={"device": "cpu"})
        self.assertEqual(len(value["tables"][0]["cells"]), 4)
        self.assertEqual(value["tables"][0]["cells"][3]["raw_text"], "$18,486")
        self.assertEqual(value["tables"][0]["cells"][3]["locator"]["page"], 1)

    def test_paddle_repeated_headers_on_adjacent_pages_bind_continuation(self):
        table = {"block_label": "table", "block_bbox": [1, 2, 90, 80],
                 "block_content": "<table><tr><th>Year</th><th>Tax</th></tr><tr><td>2024</td><td>$18,486</td></tr></table>"}
        value = paddle_result_to_envelope({"pages": [
            {"page_index": 0, "width": 100, "height": 200, "parsing_res_list": [table]},
            {"page_index": 1, "width": 100, "height": 200, "parsing_res_list": [table]},
        ]}, source=SOURCE)
        self.assertEqual(value["tables"][0]["continuation_id"], value["tables"][1]["continuation_id"])

    def test_native_text_control_does_not_invent_tables(self):
        value = native_text_to_envelope([{"page": 1, "text": "Revenue 120"}], source=SOURCE,
                                        config={"adapter": "native-pdf-text/v1"})
        self.assertEqual(value["extractor"]["model"], "native-pdf-text")
        self.assertEqual(value["tables"], [])
        self.assertEqual(value["blocks"][0]["locator"], {"page": 1})


if __name__ == "__main__":
    unittest.main()
