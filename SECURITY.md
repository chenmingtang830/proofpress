# Security Policy

## Reporting a vulnerability

Please report vulnerabilities privately via
[GitHub security advisories](https://github.com/chenmingtang830/proofpress/security/advisories/new)
rather than public issues.

Relevant classes of issues include: capsule/metadata parsing that could
execute or inject content (transport data must stay declarative), verification
bypasses (`verify`/`inspect` reporting green on tampered input), and privacy
leaks (local-only history escaping into portable capsules or clean exports).

## Scope notes

Proofpress is **tamper-evident, not tamper-proof** by design: it does not
claim to prevent the holder of a file from rewriting their own history, and a
report demonstrating that is expected behavior, not a vulnerability. See
`docs/PORTABLE_ARTIFACT_SPEC.md` §4 for the trust boundary.
