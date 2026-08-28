import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "studies/apex-agent-eval/retrieval_adapter/run_gateway_role_canary_private.py"
sys.path.insert(0, str(PATH.parent))
SPEC = importlib.util.spec_from_file_location("role_canary", PATH)
canary = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(canary)


class GatewayRoleCanaryTests(unittest.TestCase):
    def test_routes_are_exact_and_provider_pinned(self):
        self.assertEqual(canary.MODELS["ling"],
                         ("inclusionai/ling-3.0-flash-fin", "novita", "high"))
        self.assertEqual(canary.MODELS["deepseek"][1], "alibaba")
        self.assertEqual(canary.MODELS["gemini"][1], "vertex")
        self.assertEqual(set(canary.ROLES), {"decomposition", "atom_extraction",
                                             "claim_proposal", "claim_critic"})

    def test_schema_is_closed_and_role_bounded(self):
        self.assertFalse(canary.OUTPUT_SCHEMA["additionalProperties"])
        self.assertEqual(set(canary.OUTPUT_SCHEMA["properties"]["role"]["enum"]),
                         set(canary.ROLES))

    def test_retry_selection_remains_inside_frozen_routes(self):
        self.assertTrue({"gemini", "glm", "muse"} <= set(canary.MODELS))


if __name__ == "__main__":
    unittest.main()
