"""Grounded architecture-vocabulary index for the ARA package.

# Grounding: transcribed from ``proofpress.py`` command and function names.

This file contains no executable protocol logic. It maps the paper's Purpose,
Roles, Operations, and Transfer terminology to the persistent implementation
exposed as ``src/execution/proofpress.py``. The implementation entry points are
``do_snapshot``/``cmd_snapshot``, ``cmd_inspect``, ``cmd_import``, and
``cmd_verify`` in the repository-root ``proofpress.py``.
"""

ARCHITECTURE_VOCABULARY = {
    "Purpose": "portable admitted-history and artifact-provenance handoff",
    "Roles": ("originating agent", "receiving agent", "admission authority"),
    "Operations": ("record", "bind", "transfer", "verify", "dispose"),
    "Transfer": ("cmd_inspect", "cmd_import", "cmd_verify"),
}
