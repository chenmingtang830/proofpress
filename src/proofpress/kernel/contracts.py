"""Authority classification for the canonical operation contract.

The transport may expose fewer operations, but it cannot grant an operation a
different authority class. New operations must be classified deliberately.
"""
from __future__ import annotations

from typing import Mapping, Any


OWNER_ONLY_OPERATIONS = frozenset({
    "claim.review", "claim.supersede", "claim.withdraw", "claim.reassess",
    "relation.review", "relation.resolve",
})

AGENT_OPERATIONS = frozenset({
    "capabilities.get", "configuration.get", "evidence.submit", "experiment.ingest",
    "claim.propose", "claim.evaluate", "claim.judge",
    "claim.judge_batch", "relation.propose", "relation.evaluate",
    "relation.judge", "graph.get", "graph.traverse", "context.get", "context.discover",
    "review.summary", "review.receipt",
    "run.start", "run.finish", "run.get", "run.list", "context.capture",
    "reliance.record", "output.record", "observation.record",
})

# Local-only operations remain outside the hosted credential surface. An
# operation added to the kernel must be placed in exactly one class.
LOCAL_ONLY_OPERATIONS = frozenset({"evidence.import"})


def operation_authority(operation: object) -> str | None:
    """Return the minimum hosted authority, or None for unavailable operations."""
    if not isinstance(operation, str):
        return None
    if operation in OWNER_ONLY_OPERATIONS:
        return "owner"
    if operation in AGENT_OPERATIONS:
        return "agent"
    return None


def validate_operation_contracts(specs: Mapping[str, Mapping[str, Any]]) -> None:
    """Fail closed when a kernel operation lacks an explicit authority class."""
    classes = (OWNER_ONLY_OPERATIONS, AGENT_OPERATIONS, LOCAL_ONLY_OPERATIONS)
    if any(left & right for index, left in enumerate(classes)
           for right in classes[index + 1:]):
        raise RuntimeError("operation authority classes overlap")
    missing = set(specs) - set().union(*classes)
    unknown = set().union(*classes) - set(specs)
    if missing or unknown:
        raise RuntimeError(
            "operation authority classification mismatch: "
            f"unclassified={sorted(missing)}, unknown={sorted(unknown)}")
