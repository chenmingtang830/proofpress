# Proofpress Plugin Privacy Notice

Effective date: September 8, 2026

This notice covers the public Proofpress agent plugin and its default managed
MCP endpoint. It does not replace a customer agreement or a self-hosted
operator's privacy notice.

## What the plugin does

The installed package contains local instructions, a policy template, and a
configuration for the Proofpress MCP endpoint. The package itself has no
analytics, telemetry, lifecycle hooks, embedded credentials, or hidden data
upload.

Installing the plugin does not itself transfer workspace content. When a user
asks an agent to perform a task that requires eligible Proofpress context or
produces a durable outcome, the selected skill may use the configured MCP
server to retrieve context, submit a bounded proposal, or optionally record a
task run. Policy initialization remains an explicit user request. Optional run
tracking may send and store a task summary; governed-context receipt and
reliance identifiers; output references, content digests, media types, and
user-provided summaries; plus observation kinds, sources, meanings, linked
references, and timestamps. It records references and digests, not the output
content itself, unless that content is separately submitted as bounded evidence.

The server's agent surface is limited to bounded evidence submission, claim
proposals, context and lineage reads, run start/finish/read, context capture,
reliance, output, and observation records, and review links. It does not expose
Human Approval, policy administration, or credential administration to the
agent.

## Data choices and boundaries

Before submitting anything, users and agents must apply the repository policy.
The bundled template excludes credentials, secrets, raw traces, full source
dumps, and unvalidated hypotheses. Submit only the minimum Evidence Projection
needed to support a bounded claim; do not upload raw prompts, private reasoning,
or material that is not necessary for the stated purpose.

Proofpress records the submitted evidence references, claim lifecycle, and any
optional run records described above for the configured workspace. Human
Approval, not plugin installation or model output, is the gate for downstream
reuse. An agent must not use owner or recovery credentials.

## Authentication and self-hosting

The default endpoint uses OAuth with PKCE. Each client receives a separate,
revocable agent credential; the plugin never receives the underlying owner or
recovery credential. The MCP resource URL and authorization server are
discoverable from the managed endpoint.

Self-hosted operators choose their own endpoint, storage, retention, and
privacy practices. Replacing the default MCP URL makes that operator, not the
managed endpoint, responsible for those practices.

## Contact and security reports

Use the repository's [security advisory channel](../SECURITY.md) for security
or privacy vulnerabilities. General product questions can be filed in the
Proofpress repository. Do not include secrets or private evidence in public
issues.
