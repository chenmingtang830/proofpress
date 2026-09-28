"""Guards for operation authority and one-way adapter dependencies."""
from __future__ import annotations

import ast
from pathlib import Path
import unittest

from proofpress.kernel import operations
from proofpress.kernel.contracts import (
    AGENT_OPERATIONS, LOCAL_ONLY_OPERATIONS, OWNER_ONLY_OPERATIONS,
    operation_authority, validate_operation_contracts,
)


ROOT = Path(__file__).resolve().parents[1] / "src/proofpress"
AUTHORITY_CALLS = {
    "review_v2", "review_relation_v2", "auto_admit_v2", "supersede_v2",
    "withdraw_v2", "reassess_v2", "resolve_contradiction_v2",
    "review_claim", "review_relation",
}


class ArchitectureBoundaryTests(unittest.TestCase):
    def test_every_operation_has_one_authority_class(self):
        validate_operation_contracts(operations.LOCAL_OPERATION_SPECS)
        self.assertEqual(operation_authority("claim.review"), "owner")
        self.assertEqual(operation_authority("claim.propose"), "agent")
        self.assertIsNone(operation_authority("evidence.import"))
        self.assertIsNone(operation_authority("future.operation"))
        self.assertIsNone(operation_authority(["claim.review"]))
        self.assertTrue(OWNER_ONLY_OPERATIONS.isdisjoint(AGENT_OPERATIONS))
        self.assertEqual(LOCAL_ONLY_OPERATIONS, {"evidence.import"})
        with self.assertRaisesRegex(RuntimeError, "unclassified"):
            validate_operation_contracts({**operations.LOCAL_OPERATION_SPECS,
                                          "future.operation": {}})

    def test_kernel_does_not_import_source_or_hosted_adapters(self):
        for path in (ROOT / "kernel").glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imports = [node.module or "" for node in ast.walk(tree)
                       if isinstance(node, ast.ImportFrom)]
            imports += [alias.name for node in ast.walk(tree)
                        if isinstance(node, ast.Import)
                        for alias in node.names]
            self.assertFalse([name for name in imports if name.startswith(
                ("proofpress.integrations", "proofpress.hosted"))], path.name)

    def test_source_and_transport_adapters_cannot_call_admission(self):
        for folder in ("integrations", "transports"):
            for path in (ROOT / folder).rglob("*.py"):
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                calls = [node.func.attr for node in ast.walk(tree)
                         if isinstance(node, ast.Call)
                         and isinstance(node.func, ast.Attribute)]
                self.assertFalse(AUTHORITY_CALLS.intersection(calls), path.name)
                imports = [node.module or "" for node in ast.walk(tree)
                           if isinstance(node, ast.ImportFrom)]
                imports += [alias.name for node in ast.walk(tree)
                            if isinstance(node, ast.Import)
                            for alias in node.names]
                self.assertFalse([name for name in imports if name.startswith(
                    ("proofpress.hosted.control_plane", "proofpress.hosted.review_policy"))], path.name)

    def test_hosted_mcp_delegates_only_agent_operations(self):
        path = ROOT / "hosted/mcp_http.py"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        call_tool = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                         and node.name == "call_tool")
        operations_called = {
            node.args[2].value for node in ast.walk(call_tool)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "_execute" and len(node.args) >= 3
            and isinstance(node.args[2], ast.Constant)
        }
        self.assertTrue(operations_called)
        self.assertLessEqual(operations_called, AGENT_OPERATIONS)


if __name__ == "__main__":
    unittest.main()
