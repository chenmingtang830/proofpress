# Proofpress Plugin Terms of Use

Effective date: September 8, 2026

These terms govern use of the public Proofpress plugin distribution. The
repository code is licensed under Apache-2.0; these terms do not grant rights
in customer data or override a separate service agreement.

## Intended use

Proofpress is a governance layer for evidence-backed, agent-produced claims.
It helps an agent retrieve eligible context, submit bounded evidence, and
prepare claims for review. It is not legal, financial, medical, or compliance
advice, and it does not make an agent an approver.

Users are responsible for selecting material they are authorized to submit,
reviewing repository policy, configuring any self-hosted service, and ensuring
that their use complies with applicable obligations. Do not submit secrets,
credentials, raw private traces, or content whose disclosure is not authorized.

## Human authority and availability

Human Approval remains the sole authorization for reuse of a candidate claim.
Model or Judge output is advisory. The plugin and MCP server must not be used
to bypass review, create owner authority, or treat a candidate as governed
context before authorized human admission.

The default hosted endpoint, third-party agent clients, and OAuth providers may
be unavailable or change independently. Validate outputs and retain appropriate
human oversight for consequential work.

## Changes and termination

The plugin uses semantic versions. Marketplace and GitHub releases may update
the package, while previously installed versions can remain cached by client
runtimes. Proofpress may change, suspend, or remove an endpoint when needed to
protect users, security, or service operation. Revoking an agent credential
invalidates its derived OAuth sessions.

For self-hosted deployments, the operator controls access, availability, and
service terms.
