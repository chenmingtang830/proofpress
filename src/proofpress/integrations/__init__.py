"""Optional bounded-input integrations for Proofpress."""

# ``kernel.operations`` imports ``integrations.repository`` during bootstrap.
# Keep this package surface lazy so the receipt helper can in turn use the
# kernel's public normalizer without a package-initialization cycle.
def __getattr__(name):
    if name in __all__:
        from . import content_addressed
        return getattr(content_addressed, name)
    raise AttributeError(name)

__all__ = [
    "ContentAddressedReceiptAdapter",
    "ContentAddressedReceiptError",
    "build_retrieval_evidence",
]
