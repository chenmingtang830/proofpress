import unittest

from proofpress.integrations.document_extraction.gate import evaluate_gate


def conformance(repeat=1.0):
    metric=lambda value:{"f1":value}
    return {"split":"development","documents_scored":4,"documents_expected":4,
            "metrics":{"text_blocks":metric(.9),"table_cells":metric(1),"numeric_values":metric(1),
                       "locators":{"rate":.9},"reading_order":{"rate":.8},
                       "cross_page_continuations":metric(1),"repeatability":{"rate":repeat}},
            "automatic_admission":False,"human_approval_required":True}


class DocumentExtractionGateTests(unittest.TestCase):
    def test_pass_requires_every_frozen_threshold_and_invariant(self):
        ecological={"complete":4,"attempted":4,"pending":8,"automatic_admission":False,"human_approval_required":True}
        self.assertEqual(evaluate_gate(conformance(),ecological)["status"],"pass")

    def test_ecological_timeout_blocks_heldout(self):
        ecological={"complete":2,"attempted":4,"pending":8,"automatic_admission":False,"human_approval_required":True}
        result=evaluate_gate(conformance(),ecological)
        self.assertEqual(result["status"],"block")
        self.assertFalse(result["heldout_authorized"])

    def test_missing_repeatability_blocks(self):
        ecological={"complete":4,"attempted":4,"pending":8,"automatic_admission":False,"human_approval_required":True}
        self.assertEqual(evaluate_gate(conformance(None),ecological)["status"],"block")


if __name__=="__main__": unittest.main()
