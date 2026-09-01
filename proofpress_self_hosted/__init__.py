"""Single-owner self-hosting reference for Proofpress."""

from .control_plane import HostedAuthError, HostedControlPlane

__all__ = ["HostedAuthError", "HostedControlPlane"]
