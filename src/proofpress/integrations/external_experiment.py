"""Compatibility import for the external-experiment evidence profile.

External producers translate into this bounded profile; validation lives in
``proofpress.profiles`` and does not grant admission authority.
"""

from proofpress.profiles.external_experiment import *  # noqa: F401,F403
