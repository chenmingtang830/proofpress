[//]: # (ob:d16948ea)
# Proofpress documentation

[//]: # (ob:aeed01a6)
Proofpress is the trust layer for multiplayer AI: an open, agent-native ledger
that travels with the artifact. The public documentation set stays deliberately
small and describes behavior that users and compatible implementations can rely
on.

[//]: # (ob:c6e0b8d1)
“Think C2PA, but for knowledge work” is a category analogy, not a claim of C2PA
compatibility, signed authorship, or complete capture.

[//]: # (ob:717c12e2)
- [Portable handoff demo](../examples/portable-handoff/) provides a neutral

[//]: # (ob:c2dd735b)
  artifact whose embedded v1 → v2 ledger can be inspected, imported, and
  verified in a clean receiver repository.

[//]: # (ob:62ae0597)
- [Portable Artifact V0](PORTABLE_ARTIFACT_SPEC.md) is the executable protocol

[//]: # (ob:12d546c8)
  contract: policy, identity, carrier, actors, integrity, import, and commands.

[//]: # (ob:115b73d9)
- [Privacy Boundaries](PRIVACY_AND_DISCLOSURE.md) defines what admitted history

[//]: # (ob:18d76a56)
  may contain, what stays local, and what a distributed file cannot promise.

[//]: # (ob:08d1b5c2)
The implementation is the zero-dependency [`proofpress.py`](../proofpress.py)
CLI. Harness installation and attribution rules are documented under
[`skills/`](../skills/).

[//]: # (ob:aef7f16a)
Product strategy, competitive research, launch drafts, and experiments are not
normative protocol documentation and are intentionally excluded from the public
repository tree.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzRlNTAxMDZkY2JmYWQxOGUzYWIwNjY4YyIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)
