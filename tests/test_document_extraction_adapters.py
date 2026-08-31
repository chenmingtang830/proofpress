import unittest

from document_extraction_adapters import deepseek_markdown_to_envelope, paddle_result_to_envelope


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

    def test_deepseek_page_only_geometry_is_explicit(self):
        value = deepseek_markdown_to_envelope([{"page": 1,
            "render_digest": "sha256:" + "2" * 64,
            "markdown": "| Year | Tax |\n|---|---|\n| 2024 | $18,486 |"}], source=SOURCE)
        self.assertEqual(value["tables"][0]["geometry_status"], "page_only")
        self.assertNotIn("bbox", value["tables"][0]["locator"])


if __name__ == "__main__":
    unittest.main()
