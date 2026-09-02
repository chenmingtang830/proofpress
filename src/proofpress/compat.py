"""0.6 console-script compatibility aliases scheduled for removal in 0.7."""
from __future__ import annotations

import sys


def _warn(old: str, new: str) -> None:
    print(
        f"warning: {old} is deprecated; use {new} (the alias is removed in 0.7)",
        file=sys.stderr,
    )


def repo_main() -> int:
    from proofpress.integrations.repository import main
    _warn("proofpress-repo", "proofpress repo")
    return main()


def mcp_main() -> None:
    from proofpress.transports.mcp import main
    _warn("proofpress-mcp", "proofpress mcp")
    return main()


def hosted_main() -> None:
    from proofpress.hosted.service import main
    _warn("proofpress-self-hosted", "proofpress hosted")
    return main()


def remote_main() -> None:
    from proofpress.hosted.remote import main
    _warn("proofpress-remote", "proofpress remote")
    return main()


def rd_main() -> None:
    from proofpress.integrations.research_blueprint import main
    _warn("proofpress-rd", "proofpress rd")
    return main()
