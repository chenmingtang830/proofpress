[//]: # (ob:a2cfa24a)
# Local Control Plane Roadmap

[//]: # (ob:cef6a910)
> Status: accepted implementation contract. The completion level and sequencing
> decisions below were approved on 2026-08-30. This document defines what “the
> open-source local control plane is complete” means. It does not claim that the
> roadmap is already implemented, and it does not define the hosted Proofpress
> Cloud product.

[//]: # (ob:443fea94)
## Decision

[//]: # (ob:054d7684)
Proofpress should productize the existing local governance kernel before
building a hosted control plane. The open-source control plane will expose one
stable lifecycle for agent-produced knowledge across direct clients, the CLI,
and later host adapters, while keeping the admitted history and verification
record local and independently checkable.

[//]: # (ob:be5b9260)
The final open-source deliverable is a **single-node, local-first governance
service suitable for real developer and design-partner workflows**. It is not
a multi-tenant enterprise service. Customer VPC and Proofpress Cloud deployments
should reuse its operation semantics and receipts rather than redefine them.

[//]: # (ob:30a4f1fe)
## Product boundary

[//]: # (ob:296dc89d)
The proposing agent may run anywhere. It sends bounded proposals and evidence
projections to a governance plane with separate policy and approval authority.
That governance plane may be a localhost service, a customer-controlled private
machine, or a future hosted service; the required separation is an authority
boundary, not necessarily a physical-machine boundary.

[//]: # (ob:fae07f23)
Proofpress governs what a next agent or human may rely on, why, and under whose
authority. It does not replace the customer's agent runtime, orchestration,
models, RAG or memory, source systems, observability backend, or full trace
store. Raw traces and retrieved documents are evidence inputs, not admission.

[//]: # (ob:131d71dd)
## Current baseline

[//]: # (ob:b203269c)
The repository already contains a substantial local kernel:

[//]: # (ob:6a47626b)
- a Git-backed append-only knowledge-event chain under
  `refs/proofpress/knowledge`;
- bounded evidence import and evidence-bound conclusion proposals;
- deterministic evaluation, advisory LM judging, and authorized Human
  Approval as the only admission path;
- typed claim relations, contradiction quarantine, supersession, expiry, and
  governed-context projection;
- disclosure and assimilation gates, portable verification, policy stored in
  `.proofpress/policy.json`, and a token-protected local review UI;
- an internal-alpha operation seam, merged in
  [PR #63](https://github.com/chenmingtang830/proofpress/pull/63), shared by
  direct Python callers and the matching CLI paths for evidence import,
  conclusion proposal/evaluation/review, and context retrieval.

[//]: # (ob:9dc1491e)
This baseline is not yet a completed control plane. The operation seam is not a
frozen public API; several CLI capabilities do not yet use it; reviewer identity
is not cryptographically authenticated; and no supported long-running local
service, recovery contract, SDK, or conformance suite has shipped.

[//]: # (ob:3005f949)
## Target architecture

[//]: # (ob:90bb8945)
```text
Customer Agent / Proofpress Producer
        │
        │ Python SDK, CLI, or later MCP adapter
        ▼
Local Proofpress Control Plane
  ├─ versioned operation API
  ├─ authentication and authority checks
  ├─ deterministic policy and lifecycle engine
  ├─ review queue and Human Approval
  ├─ idempotency, locking, recovery, and audit
  └─ receipt and governed-context projection
        │
        ▼
Governance Kernel + Local Git Ledger
  ├─ refs/proofpress/knowledge   canonical event history
  ├─ .proofpress/policy.json    local policy
  └─ .proofpress/               identities, keys, runtime metadata, cache
```

[//]: # (ob:45d39d44)
Customer documents, raw traces, prompts, credentials, and source-system state
remain in customer-controlled locations. The control plane stores only the
bounded evidence projections, digests, locators, governance events, and receipts
needed for the declared workflow. Git remains the canonical admitted-history
backend for Git workspaces; a future storage adapter may support non-Git
deployments without changing lifecycle meaning.

[//]: # (ob:3b1f3444)
## Completion contract

[//]: # (ob:699fd77b)
The open-source local control plane is complete only when all of the following
are true.

[//]: # (ob:82fb51b2)
### 1. Versioned operation contract

[//]: # (ob:5d57b67f)
- A documented `v1alpha` request, result, and error envelope covers evidence,
  conclusions, relations, evaluation, judging, review, resolution,
  supersession, disclosure, assimilation, graph traversal, and governed
  context.
- Unknown versions, fields, operations, and invalid state transitions fail
  closed with stable machine-readable error codes.
- Every write accepts an idempotency key and returns the existing result when
  the same authorized request is replayed; conflicting reuse is rejected.
- Capability discovery reports supported contract versions, operations, and
  optional features without implying Cloud availability.
- CLI and service calls pass the same validation and invoke the same kernel
  path. Equivalent requests produce equivalent events, lifecycle states,
  receipts, and failures.

[//]: # (ob:0343ca86)
### 2. Supported local service boundary

[//]: # (ob:84a583e5)
- A documented service runs on localhost by default and may use HTTP over a
  loopback socket or a Unix domain socket.
- It never listens on a non-loopback interface unless the operator explicitly
  opts in and configures authentication and transport protection.
- Workspace selection is explicit and path-confined. A request cannot escape
  its configured workspace or silently write to another ledger.
- Startup validates repository state, policy, schema compatibility, identity
  material, and write access before reporting readiness.
- Health, readiness, graceful shutdown, structured logs, and bounded request
  sizes are part of the supported contract.

[//]: # (ob:c36b71fb)
### 3. Identity, authority, and receipts

[//]: # (ob:5c10e933)
- Local identities use verifiable keys rather than self-asserted strings for
  security-relevant authorization.
- Proposer, judge, reviewer, and recorder roles remain distinct. Policy can
  prohibit self-review and self-admission even when one process holds several
  credentials.
- Human Approval remains the only admission authority. Deterministic checks and
  LM Judge results are evidence and recommendations, not admission.
- Admission, rejection, supersession, resolution, and governed-context receipts
  bind the event, evidence/version manifest, policy version, actor, authority,
  timestamp, and locally recomputed digest.
- Receipts can be verified offline without contacting Proofpress Cloud.

[//]: # (ob:dbdcde44)
### 4. Concurrency, durability, and recovery

[//]: # (ob:e34fe484)
- Concurrent writers are serialized or rejected with an explicit retryable
  conflict; no request may silently overwrite another event head.
- Compare-and-swap or equivalent expected-head semantics protect all lifecycle
  writes, not only selected review paths.
- A crash between validation and commit cannot produce a partially admitted
  state. Recovery is deterministic and tested with fault injection.
- Backup, restore, export, import, and integrity verification are documented and
  exercised against a clean workspace.
- Schema migration is explicit, forward-only where required, and never rewrites
  admitted history merely to make verification pass.

[//]: # (ob:08eb975f)
### 5. Policy and private-data boundary

[//]: # (ob:9076cc5b)
- Policy has a versioned schema covering role authority, scope, evidence
  requirements, reviewer allowlists, expiry, retention, and allowed evidence
  projection fields.
- The service defaults to data minimization and rejects oversized or disallowed
  trace payloads rather than becoming a general trace warehouse.
- Secrets and private source contents are not copied into logs, receipts, or
  portable artifacts.
- Policy changes are auditable and bind subsequent decisions to the exact policy
  version used.

[//]: # (ob:637dc39e)
### 6. SDK and operator experience

[//]: # (ob:7120931c)
- A typed Python SDK is a thin client over the versioned service contract; it
  does not contain a second governance implementation.
- CLI commands use the same client or operation layer and retain a supported
  offline mode for repository-local workflows.
- Errors include stable codes, safe messages, retryability, and remediation
  hints.
- A fresh user can initialize a workspace, start the service, propose one
  evidence-bound conclusion, review it under a distinct authority, retrieve
  governed context, stop the service, and independently verify the receipt from
  the documented quickstart.

[//]: # (ob:034a8474)
### 7. Conformance and release evidence

[//]: # (ob:22f3fe78)
- Frozen fixtures cover the happy path and failures for authorization,
  idempotency, concurrency, corrupted history, unsupported versions, policy
  changes, expiry, contradiction, supersession, and recovery.
- Direct-kernel, CLI, SDK, and service transports pass the same conformance
  vectors where their capabilities overlap.
- Supported Python and Node launcher environments pass CI; service tests cover
  macOS and Linux.
- The release artifact contains the service, SDK, schemas, fixtures, migration
  tooling, and verification documentation promised by its version.
- The repository clearly labels experimental adapters and hosted features so
  their presence cannot be mistaken for supported local-control-plane behavior.

[//]: # (ob:f26d3e7a)
## Delivery plan

[//]: # (ob:f58c85ec)
Each stage should land as a reviewable PR with its own tests and should leave
the existing local CLI usable.

[//]: # (ob:e42126fa)
### Stage 0 — shared kernel seam (complete)

[//]: # (ob:0569ca23)
[PR #63](https://github.com/chenmingtang830/proofpress/pull/63) established the
internal-alpha operation dispatcher and proved an initial direct-call/CLI
lifecycle over one ledger. This is the starting seam, not the public contract.

[//]: # (ob:73a38458)
### Stage 1 — contract freeze candidate

[//]: # (ob:c04a8c6a)
- Define versioned schemas, structured errors, capability discovery, and
  idempotency semantics.
- Move the remaining core lifecycle operations behind the dispatcher.
- Publish conformance fixtures for direct-kernel and CLI parity.

[//]: # (ob:a65655ca)
Exit criterion: every supported local lifecycle operation has one kernel path,
one machine-readable contract, and deterministic replay behavior.

[//]: # (ob:02d39d5f)
### Stage 2 — local service foundation

[//]: # (ob:5678638b)
- Add the loopback/Unix-socket service shell, workspace confinement, request
  limits, readiness, shutdown, and structured logging.
- Add a local authentication bootstrap suitable for development without
  weakening the distinction between proposer and reviewer.
- Test CLI/service parity and unsafe bind defaults.

[//]: # (ob:2cac8486)
Exit criterion: two separate local processes can safely propose and review
through the service while writing one valid ledger.

[//]: # (ob:2cf597f5)
### Stage 3 — authority and portable receipts

[//]: # (ob:a3f91160)
- Add local key-backed identities, role/authority policy, signature verification,
  policy-version binding, and offline-verifiable lifecycle receipts.
- Add key rotation and revocation behavior without rewriting prior history.

[//]: # (ob:6c0f0896)
Exit criterion: a fresh verifier can recompute the manifest digest, authenticate
the decision signature, and separately establish that the signer was authorized
under the bound policy.

[//]: # (ob:02dc2bd8)
### Stage 4 — durability and recovery

[//]: # (ob:e34acc28)
- Complete expected-head protection, idempotency persistence, writer locking,
  crash recovery, backup/restore, migration, and corruption diagnostics.
- Exercise concurrent and interrupted writes with deterministic fault tests.

[//]: # (ob:274349db)
Exit criterion: restart, replay, concurrency, and recovery tests cannot create
duplicate, partial, or silently overwritten governance decisions.

[//]: # (ob:af5c9e68)
### Stage 5 — Python SDK and end-to-end release

[//]: # (ob:6757dd86)
- Ship the typed Python client, documented quickstart, version negotiation, and
  safe error model.
- Run the same end-to-end fixture through SDK, CLI, and service, then verify the
  resulting receipt offline.
- Package and publish the first release that explicitly supports the local
  control plane.

[//]: # (ob:1eead98f)
Exit criterion: a design partner can integrate its own agent without importing
Proofpress internals, and can leave the service with a portable, independently
verifiable governance record.

[//]: # (ob:f26d2de6)
### Stage 6 — adapters after the control plane

[//]: # (ob:6ac27538)
Build a local MCP adapter and host-specific packages only after the service and
SDK contract stabilize. MCP exposes tools; it does not become the governance
system of record. Customer VPC and Proofpress Cloud are separate deployment and
operations projects over the same lifecycle contract.

[//]: # (ob:3a985ef1)
## Explicit non-goals for this roadmap

[//]: # (ob:bf3f943a)
- Multi-tenant organization management, billing, regional replication, hosted
  queues, or a Proofpress Cloud SLA.
- Replacing customer agent runtimes, orchestration, memory, RAG, observability,
  document stores, or source connectors.
- Storing complete private traces by default.
- Letting an LM Judge or deterministic checker authorize downstream reuse.
- Universal semantic truth, automatic factual correctness, or complete evidence
  capture.
- A generalized enterprise RBAC platform or connector marketplace.
- A stable MCP surface before the service and SDK contract are stable.

[//]: # (ob:3151b84c)
## Final delivered level

[//]: # (ob:1050cf6e)
When this roadmap is complete, Proofpress will provide an open-source,
single-node governance control plane that a customer can run locally or inside
its own private environment. Customer agents will be able to propose bounded
work at runtime; separate authorities will evaluate and approve it; the system
will persist an append-only local history; and later agents or humans will
receive only current, in-scope, actor-eligible governed context with portable
receipts.

[//]: # (ob:49e45e7a)
That is sufficient for serious local development and bounded design-partner
production use. It is not equivalent to a managed enterprise Cloud. The hosted
product will still need tenancy, organization-backed identity, managed policy,
review operations, retention, availability, observability, and compliance
controls.

[//]: # (ob:ac4b0dfb)
## Accepted implementation decisions

[//]: # (ob:90caddad)
Implementation proceeds under these approved constraints:

[//]: # (ob:e1242b39)
1. The open-source completion level is single-node, local-first, design-partner
   production use.
2. Git remains the required canonical backend for the first supported release;
   non-Git storage is deferred.
3. Localhost HTTP is the primary supported local transport.
4. The first SDK is Python-only until the contract and conformance suite are
   stable.
5. MCP follows the Python SDK. Customer VPC deployment is a materially later
   phase and is not part of the local control-plane completion milestone.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2UyYzViYTI1NDMxNmNjZWI3MjlhMmNmNiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjZjNzBiOTdmIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV84ZDVmN2M0Y2I4MDk4NTUxNTUzMWYwYWEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Q0NDU3ZjY0OGFhOThjNmQ4MjM1NzA5MSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfeuO3FaS5qsQ5R8705NZ4v0iATNQyx63d-S2IKt7frSM8iF5WMkWk0yTTJWqBQONfQZjf82-yT6Nn2Qj4lyZlcm6ehsY0D-6VVXMc4LnxD2-iPx8xvqxrlgxXtTl2fOz3e6C-0WUMz8KAy8uCp4nfsb8oorPVmd5V15flPUlH0Z4dtjAU_FzN4jixC1Yyt2k9MKE4dOJX1Vl7HPmpXEYu5XrscrzijKPgyiNYx6HQZSUjEUlh3XLeii6j7y_Pnv-GX8YL0Z2CTs0bMStVvCPnDfwiz_zvq5qljfc6fnHeqi71tnA811_7eTXzpu-66pdz4cBPrNjxQd2yfGlJr_uu79yeN19jwtuxnE3PH_27LIeN_v8vOi2z4oNb7d1ezmy9jIN3GeTT_f8p30N_77YD7y_KLp24C2cxdjv-c-rsw1neIhxkbh5llRn4jcX_CM9BIfLL9IyqpIiLPLUzdIo8qIo8CqXMaSs60d8tYumbjlQrm6kuSjDMEqqOEwZy9IiLlMfTs_NPPE6krqLgu2GfQMv7COdRdeXw9nzv3w-k9t_PoNb7voB_yX-zMuLHI78L2f79kPbXbVnP8A7KH6ArcuuGJ69_u7Vy9cXr77747u3372-ePP65R-_unj73csvv3355nxbnq3uxUBsHPs6349wbxc5G-oB2Yg31QUb4DxHTuvtx03XI5Uf6haXHK6HkW_hLy3b4nUqalfw0QFZ4Ox5u28aoL3YwJ1xfOsfVuq1z4Cv8KGLoudM7EB_UeTyCz_0gpyHPM5S7keeF1Vx6rPcxx27kRhI3owjb8YBHik-7Lq6HYnRetoJiVA_SRp2XVMX19YK9jVbixADPZADhq4aLypgWN7v-loy2pB7z3mQu0UY-llaFV7hhRmr8ios0iyLqzzzQz9hPPR4GIdZngVhwcIsyjIvT9LIz4E3ce2R4at8hrPF_z_zXT9eu-k68N65IPnp8yj8F9d97rrwrDxneIqxKuSZF5_9bP3282_LWXnTFR_o1H_-eXWU53lZj5rjv9vx9uU3zquu5J_OfiAxKvfFyT8fyMvNP_-0B0Wl__62Bk7sS-cdsOM_Rqhg-xZ1AvyNCDsmV5v9lrX3E6vP4pzxjmFz5oeot0ALjvwTvtvrrmANHEs79l3jvGlYy523HSu3bAfPyW1ZWRI9O9Tg_Ap-84Uz_8HxeocEoi4FNj_D-1VkFLyKWea5T0HGvzrfA7vvh-cOcMOuG3jp1Ntdw7fASgxP18EtergVp-p6R3zu3HkHBsgxVIL8swmJYRhUnGXhhMQveUHWa_ZYvnCsx2YOwY3CMonT--9g7KUzbLp9UzpCDsb6b9wZN9zhn8C4wnZOQ0d6iUa6ZW3BnQ8zb5zzCPRL7N6bnnewJWgy2KkDCVsP3b6HrUre1LAvKWA4aub87ncD0NTwdQsCuBK0rWfoCVwWVl7FJ_S8EW_q5N2-LRm4HvM3ceTxmRvxs7gERVs-eEc8CcGFePpgCtrR2bJrp9-3Dmuvrza85-fON6MD_kc5iCV5KT4ycxIVAyet8oMH02VxjGCGwbnasBEupYXFJKEgHKRbBMW8uXa6duVczdDlBV6ZeOX0vF7tezSlDug0jgbxlhs68vjMDeW-G_hxVjx4R7yhnuMFkffJGnAvymtSEaxukU2HfQ72sx1r4GchPx_gwHjzfOYgYhYmsR_nDyZrDRt_XY_rHLxfYAgGDk5brrsWLgHVe8PLS74m6whODBDqIOP071vH-bG3jqwBuZ8QlpXoQXj8EecFsqseRDkG38q55sg64HWDmgUrJRQs6Owd6mxUrRw1QT8r225UZWE2oesd6y9x5b7YgM0vxn1_G_Mc_8QM_2RunqdZGD1m3x9__BE_-L59tYcQZst75yXJzzMrkJGKR1yR-O_XX_6X_MGQWIAmnFqdqAwy8BofQ58mC3yWPVrBYeX07MpBG8jh36Bttjv8JbjWJSdGhx9YWzrDnBIKcq8KwgPSXgkesK3sbfJ-9BMzVxZnWVUmSf6YfSVHatsk5HrCtsjbiqMdEjzQ1qC1m5kjSf0qjzwKOQxp3rnzZ-E9g2SgGLB7HM8Xzu0fnzmrqIySPKYQ9kkIWjsvNRfBh3_86LFmt2E_OtJ1BsbiELyOgn1434MN4e1H3sA2M1rJDcKgYGk8IdM_d77f7zCWgp3EBUFw-bGG67qbsf_CudsSM-eXhixKAx49JWEHZ6g-Ci7BAHwmFtx0w4iZkJJXDI6TThOt8MwZFkGcJ141FYsAnAsS6fEaroQiB_FPWA-CIV6D3N92iHdcY44LC8_lWRA8KWlrGW3UYpGaD85-4M5Hk1r6wK8HUHTgAPfgBYMfgymKNaYoZo6xzMui5AdaLTzHMKQgM1kAjeUe3Ni6sekVea9bjvIe68wcJw_Ciofp05O4NkuMzhVcB2gJsDIceRSMAkQTpUMRE2be4N9X9biBxSG82DVz0p3yPEuiqRKKzp03lFUh6nZ9_ZGNfF2ykd1Zuu-2xKzxTyAIj_KnJGytPr1h6Dx-1Ip2KDZ8i04ScigEA2BouM33Q9HNnGEcJGURZFO_LQZF9OV_EJ1CjaO2_QT_qoEH-G3Hd-unZ04u8Xw3C7ziichBlYi7lc6baziQltahGHHcgG9bNDXFIx9JkLl9qLZTecyssDRMpoKSkKBA5L-lAFjIRsPBo3WAnPIuJ3e3JebiSr8KKp6kT0nY2vn3vvsbeChV_Qk9wkGwGh3YBuKHa2fHSFxLp2J1Q09g_gNZcOYMKz8uA56wgyQAhfLX5CndmvuYPjtzLFWUFmnEi4ft9RUrNg5EapdcZUEafFkSQ_EQWYU3b4Xeqkcwt1etg4m1Ycan46Hv-XE1PYDvaRvX-fXvv8BmoCJLGRQCR7Kt80_Kcfzn21jpPgvNpo4gBmYHCYEnIfIvcF5fxMEP_3SvEsuz3b5pns2cahKwIA2j9AjBHhFscnQ953_jTgF3WYMW5nc70dsXmctGuqA3ipg9LXFrEIUKg-ZDmwDB1jD2e4rjpNOMwRjbSQPulPWMgLI4iqOoeGJiv_pUjxAPogsApD4HDYQiOBy4vU1d8eK6aLgVRmzYzLW7PoazB66AINYnYqfudEUGd7w1wapu_dY15pzUOEnjIM2flDQwbGVJKrjpuh0mc579qa0_QdhZfOCjXmzY8KZZOVdd_2HYQVCOd1bN3LlfsCIND-Klx9J6eOXjVQcr4BWOKkAGAS9AutG2oDvNKkwKYrJy5sr9ooqypIqO0BoQrdoHEg6XqtHJGOBuF3-XlW4JUlhQZZ53kO1-GjoFF6jc4bVK6pnIZUXe4DOzgyg4gl6Yk_y4cCs3zeLfgOJDXmCoPIaNjK7Aq8D7x5Biu9uPosYAXgtoAwhb58W_8PPymNYPiWITtdwrrrrbEvMhFSsK_0kJW6vUFicvGCOmNe6NAoNZuxqz6cAD2x38CDGbs0O7MIxT9_Gm7CdhEGZl_pSkHl433PXIesrmgNcFfFjYoaW9qjPOXDeroiLj8bFTjYhUy9unfFFbrsduzaXne7dbv8tKbLjF4sdJlJTlUYX6WErXzvebekciMglxRFCzslNBP-3r4oM8eXISZtjA4_AaWVr9BhTfFP6SD_VlCwFEP7ZS-GvY85JMg3KkqWg0V7SCSMIv-bEzjoW6KtlOpByqUQYuVkb2btxwl5VuqynFrPCTKEh_A0J_v68hLmHSFnz76o1ai-4Is37rAVQF6NjCkcCnQSSfWTWXimcZxE2VN6H4q087MCJwlW3Xri871oh4b8QCTn-Hav4Xzt1WmKvOQZibhQF7SrrWzrf7ZqzXoCcZFSkvwfD8TfieYIPgxLYkV6ACG6AHddgl_A2Oe7YwFniRl6fhNPb8dypiy8I1er3gBje3HNqpz8wck-dGblHF_HF7_yeWJ-xTtCsYK7sWdQVHg1YIswqYv5v138KMh9FhAuDexL3D6jLQM-wr4G1K5-ClY2Kx2w9SHkpOlQK8P5IHWQ6fszBFmLvlQdL7LW0KqwmkwuBoXM8tVzf7wdk8YgHrsfIJqPg9h2Phh4AVsgnoJdJjqHlkhgPjhLrfzpWiueeHfh5kT0Ccd-58M4AG_K8JbkMYh7UyDgp6AmTvB_7r3_-P1I_9TfH7AUhqWL09CUmaUHICL3TyGQuwc_IZC3Jz8hkLBnPyGQuacvIZC0xy8hkL2HHyGQtkcZpmA4s4-YyFUTj5jAUXmHl3Xbo_vY4ps5--L1PqPr2XqTmffi9THz75jFWoPfmMVTs9zT-mcHl6L1NDPM3Ppnh3mh5TRTv5jFW9OvmMVT46_V6mZDNzp7p6cvouTNni5DNWLWHunFUm_7R8maT6afky2ezTz5gs9OkzNEnhGd2ic7Kn392kQU_zhslGnnzGSgKepsfk3k7zmEmCnT5nk3yaeUYnfU7TbBIup_nHpDjm3kslFeZ4XsX3p2k2gfVpmk1Ee5pmE0ue1uEmepvlVRkvzehwHaqc1pkmODhtL4yjfnod4yGffi_jyZ7W88ahPH3Oxq-b0T_a6zp978b5mT7zg-UNfT672lxTpYnS8-OG2_Wioeh2fCUKS-CCyRowJe3QRy0s4JEImZkMZ25HGOVHnb0c4pV2OEfU_Z17H8DiMZ4WoAGj1AsSlxVBFQbkI4jeB7upwYb2240OnxeE-IIQXxDiC0J8QYgvCPEFIb4gxBeE-IIQXxDiC0J8QYgvCPEFIb4gxBeE-IIQXxDiC0J8QYgvCPEFIb4gxBeE-IIQXxDiC0J8QYgvCPEFIb4gxBeE-IIQXxDiC0L8SRHid5_yqqacSrqex-7Px8eZ3jbR9UnGtoYuy0KvyuMINq3cgEd5Cc54yt2Y4vHIZWWU-EmR-PA2eZnxzC8j7hdJUBVllp96oWMDXLPnoXdsgCvP0yooi3_IANfPZxs2bJAnygwc58qLwyqBB2gNC1Qm-e0B0DC5vs-9NCndnLM4VOtbaDG5_mMwX8oBw2IbsMbwvv1XAYYBRh_vVydGbt9y1g6E6Sk7TvAIXJA6IbAKNQoEotHQCnGi6eWlcLFrs4IkDT-Ki6GfgI6k0eivmm6vUV_nR7SBPE0eFzyJfJCr3FOnaQHb1G3dhliTq1WFX5ZeHpaxm6vVLBCbwSU9GJ0m0pUCSfm-zdF7IiCVOoLjQBN9XdOLIrMHoRiwB_hUsN6g5kWrLBblw9GNXatRwwZt47Ci7-Adyhpin1G676CT8Q1evf5m9b7FS8Nh6D1Rp73EFXBTTeVIvkPi8QNw-_WIL6DmouNnRXBdEL--b8U0Y3kmxA9gCxEFBNuCP0hzqZH8mdv2Ai_0ijRLg8JX92OB-hSa5BFoPTA-8KbmxuBMVUprX4vTFfJmrLv0dQ-sBqa-qqa7Gn73O5KdWkoOc7a2t4figZp44Cq5de5oeMuf37yipW_IBZxb010T8gUIFDzYc6wWU-yiU5cD3yLOqxgmRehJCRkRMkoUtzNHH_tVWBVpkvt5qo7ewi8aQbsbIFGumlZVRrfpZloZWhhF60IfCjoc0B2neFGWnN63chY_uQljB5xgCagSrHFjUoU7Uz1lO_QykX9VJur8fUuu4I01kMCcq9CIBEje8AqhZfKO11KiG65Ls-_bLSs2cCUrrE0zp9pjHl0pCLnGC4n7pu8FKBWteOfI262hD5SMvIgVKd6WY8KT9TWGYM5ucz3UyPdyS31rM5xQBH4Yg_kPKr9Sd2bhN28qyXsDMjcyJ0MQQPgR9BsIjj5x2xSJhE4h9K461P8xyPWBQcZ6SwcJ6mUYxRGBZtuCyCMm7O3Lr5GILd92eEBSVYjR__DnLsfjVsknynK2JV1LtQfVS3gz1Lod8t9bjUCT0jb2NWiI0qDUCHqg-BDU326P-hbfAtUnTT-fOfc0LcMk8CNwkbg6dwufaiTwboBTuWqQlCwJ4tIr6PaESjUYVEsCnw5UKreOMh_sLaj0NNTW1sKZyq0fBRytBruGp5__8cX7dq31hLmRLfrUE22xpocoXdjs6Ys_tFahNUpwkvpt3aLBL-BTrNkLHoMr_VgPeFivv3X-ui8vKXQnHSIYGbEnf0DmR1Jfar0yiFYMypAopqBCN20nEm7C9wJ5oa2GlfQFy1pEKT_t4aDhJlCDDHtMworJ-iv0FepeCBfuKgSTl2sZRzlGM4qXq4ei6QbUPqLwPNTbWmzqXOKXpKxMDt629SulMkky0NDTdZzb5VR64PyvQ9f-KI8FdDGI11omk3VJTri2zp--IZJkog40bbMmpN7E2rHtCmS5v9R7PqbYGwf_vFJl5vwaV5Oeksp3MtDavRB2US8YUYdeovNENybSQAfctcKFjrDTM8M7z8Qrq4YdcTVSnbDm_EjORwpU7qZ-WnluVaaZEigLH61l-eGAZ3PQ6oPsfVsJmMZun8OdOi_ffPMCnkBXq6Gj0HVfRLSVnd5OuCsvdA5AlY_gqOXaRX-9G7vLnu02aKRQJEB28KEC-4pe0AG13aSK216uQeu32vvWDtzKpPhV6LTCZDKp88LCqaCjxwntNGxq0DbljE7OohSiRbeqqig0XpFGfhudfGcct_J03RziauaC22Wu0kC75cKPBmqLH6zU-opcfzwS4fhbGV3rI__7_75vRfxru6Z2KIwP__rLf_36y98tdIDhIGAS6wnrVvGPlpIcZVwwWE9PVa7lnJmwh7egbm0apBL5ac_3QpeR5tVq13rSql9RTPBBplwF6ygNXtaj-MwvYnVyrOlvMzr11AXgaX5t3Mf_EDHiv8gMA9g-5zUarX7yPicsG6xXsLZrUV4cYRVlRGZ9-oQiRmJkWZx-ab2h_Qln-p9d9EWA6kp5XaCJR4YwQ4R-FBjoA7se6QxQyqsoYz_zojLJCx3Jm2YB3dnxcOg_-nZr4dthAhI97R4CpBpNylGHHA-DLKxQgNPgm2ybrGVQGuOGO2HFGStHfH_ZIOLMkQAxVshANzVMscLv25ZzXFD1Z5YcDD9aIxVbnhNziHcQfoO5exWQr_X1S_eVlsPPaXDG8MJEGfgs1oVUFQcdc6leqbzxNTK-FX5SqNTtyfdCobu0pBATR_CbGfVZhpEfh2mVxJT7EurTdGFYLu1deyrkwiwNq7IAbsoSnSiw2iwsr_ahTRON01V05BXwSncF-0OIAgeIX6k188ZBnmdBnERx6es3tpos9Bs_sE1C7uImUVHmXsCqSDv1VueE9qwf3vsgsJiDZvYDt4ZS-9o9td1i7QorJwf26Jq9jMucA4fVeKCrifsJwoNeAYo9ksGa1UT5SmLwPc_Ra_yT-JIpZYqApKrmTYkRnjpYKXx1C7TWpdAPuHwLIQ9lChBjSus2lI0VKQLh-8rgeY1BEf1CnBVquIH2_4rcDgKgO6woOCZh0JO1sBKgOlXYuO-lNOs8orgHYj0kAf82sC23Qwl5Z8ivAuOA_hG6NQ1GBbQGOVyDRrsTZa9sUJ78OkSK9PpxsPwqnWw2J3hwckhXtxtFYbLiTCB2lXbAXPA1-caUv2If4TDlvoIM8BNJSctkG3p7AzjRw2Beli7GeAhwUxAvmD-LcBPJQN_73Pnqp30NH6E0gDibQeZp4WDN35TmNWqLrn4gZlSqeDVBGc944Jzlkc8yz_cKbcSsXiBLvB_cyaM0XJbE4OZHrhdoB9Fq7jku4vdqzUF2-cO7d28ETJ3heSjMnyPhfpSfQvwfbEKGVPyervQbzDXhJxuCANF-jGyIXoUiuQqzN_u24fKubaQ9ldWba8lbA9ppGRNV9SUx2BHXkYSWDJbBJRFF_6nRiBD7iN-jPKh9BKYMeGdN64MaOYfTU3IFlhVDEj5AOEOeJWZaNSGlBXXEKnDdiKS2EHlMMsKHMedKTlpP5HyPNdD9TvE1H-wMCzHhysDmVK_FFgisVRuMCZgcjD6pp0WwqlE1cKpyboOQaqEKkJ3gT0THHzhrxs3K_JaUa8GrPbDkZj-WoDkngN6mu5QSoVweeUikv0EbiUQXZsKVkbypSWaEKHN5CFFsHLkU64gKmWkGs4To4Z1ccquEByAyaYBpbG0oTXOXlqKHd2bRS8PhwcaUD6Az4sUeCV0jcOkjlgGUImeaWd-Isl8vLCY3pXIDV-sxO4o4y0H6gKjC4YLhcFXPTiHSSyAIG-CaUZAlgyGhb5FMnWdCZSgcHPA6FDjW2XRgKlVITybQ-NaCgybB1MQhPUhkWUncLydhnIjylCF5_a3zP_GtpeE7SJyq99-CViuVCZpmUZGql-qnlTR59M-pf2E5H8ejN-OMO05ey0wP2YyVJuiZNIoaMarzX_IPsDZ-H6jNomTGIUgCOd_uxN6kjJtrg0ItZdBAb_NWFW8Qq5Yr5kPXsKookaMdcczJCpN_WDeakTnf41jZCaMg0LlYq3PQkrnHtfwpuUvKEjx034u5dlCtLkAtdw9v3yONjkmzaxRQ6RCSM_QCU0ZKrVN8o7Q10i01p1TXMoKGFxBuCurfnq_hPdfDFdvh7rYvMUHFmuKbtEMUNWg_A0mizSTzkqQIw0QalWSU0oiCm0Hq4Ozg6scrDgJ64A2hNNTaSik_h5ESrkXqTAaEpIDQupwjTwmHD0EDE3EkO0rwGXGowjOo279a5vT3YML3O5IhDIUpu4wJTpXolF4aoirRvbQTxHSJll8ixZ5_4n1Ro3fNLlGDUEqygSjSWFdhOYU13NaXpual7nyFSvaK9bJEQLVBXScTNAm3pOfi9HHjG9XrLadqFBjuLfswTW6TVzojSW7mJ7yK3apIdZnGahi1JOnB7Z5KiLIi9vMkcpMyMDlC3QGqhejh_Zs4ScrUTR11jirvohK3DCNgPIfBlBhA9NBEKMVKj_BysprJj8hwjC4Xg3Llp0qXlMq0dC7IoFsFjhTaBpcYSHQHpRDADMr9SM2iMwO3dt10rJxa6RxVrcBfXPKWMtbiaWAgDtp0kPzGweKNg31NjgXI0KU9yll3u5rKD0CycJRMECGsvy6ZKJySeG9lscVMK1qP8oziUXS20PxgmQ1VF6F7FNYNthLhIkZoJnenzBK8xpzq51USVJlfpjHTgCerO9di2Ic02KpNwH-Lirhg3CTKrZ5bK1x5aNusiBuld_nCEQlaXSaWlUosVMKda0vPZGHGAlbpeBRVKkM8Afp6OsxUNPRWTgaj7V5F73IX5fBS7CJNNFadJXxEOfprEfpptIhIF1DHHPBQ0exLrrIMlE5YUZMS6KdhEAPepImbGOAtL2umMs5wcKMyIaLnBd5HQd7rUdhRoFir2JVAZ4pXVrUTiUITMCPndHlUaQUEe4nyPdNeqa1cVHXcLkOqlA0S0O2m-9_EC5FOvpYwCJF_r_puq_IjR7sQZqTAK_wwSqOkYl5oRe6q3dqSggc3S8udQr9KwyqLypIZzIvpn9ai8PDuZx1JkJs5qWhM-l4Qw7rfWXZvBXdmQjWT6zE6Raono-cnpedD99r2B4kFv6QK6lrkamStiapOdvJHB_CHGSCrSif0G3rVg7Tx8FTdT4uNuG_DdkKH69eSqgV3_CMKZMP2bUHOXvux7rtW5LVp51dUypRUUQaJ3kXE28V339Mir-t2_0mbLsUKSrkbjMSEn-mldbesuuOV8WmIj7uu0bCBiQ-iuFt6JMD35Dbl15SWkBdn0aTzCuhO9SA9Dct5M0jtTSs1VheIbN3A2oPK5A2dlKwaEdF8oEhMupsQjsD-I3hKrQDBTxNbqqSyVmMkN-xj3fVzwsjyzONVGFSJ9qGsvn0b1XlrL74Cm6RwG6GfhyzXiXerPV-1cjyi5V7wsPwUZ6jbjoBB0bLsh1twjn5ReVWUZXmcaBVhte1byuiR7fb6cHw_zFmQe1lkcK-6A1_u90gwhcPJkNXDhpeiYnYSyQEWY4doCmlVMa9AUYKyWBKJscaA-Rmc6PvWatxGLYnpC5lqE5joWsofWgG8DIEVQebFX0vowpHc1I2Cf-yGgRu4LEs13thq_b9xMw9q21dSEIVJ6QVpFMe6iGV18mtD8fAu_MGqah-YChO-khr5Fh6UthaTO3iEBSYVjzTMY8Jxo1Il5iaFk7snBpjgLbSBq8h1twwEXb5A01DO6LTCAHc1YQGP3SjS6FRrjoBu1Hr4DICBeErShaYXbGvXHqn9GHCJQAXbYbWozBzTgDfAfjzOw7xiuRdqdWXNGrjBZw8ZFKDwnK6X-LxKs6rQysaaHWBc8wc3_sP5iBY2K0_cQBwngkiddTbJZtKkk4Qz1gxlVs-0Gx4k__OuGxHjuZtite0mLJkko9wLR3ul8OvKRxUTjUWKRfq8yrMXwa4wqpg6AsZ8pl5bMKgErZKHTtGail9nODcKeemDleVeojPQ1jSEE5x7n1EG6LabN0Cj1Hf7y43tj0hAPyZE8ECQr0UZVOrQGUR-5keF57ml5_uGfD0g4QafPmKugXKfvSL3Us_PkkJrYGvUwYRdHzah4LIln2cKaRSROz6yVnE1XrF2z2SMt7aKAkaRqBfTHIzV3r4b7TzGx06xsdQOOqMrMlV4Mbsefy-d9bkKCk-ToIi8yg1LHdKb4QonmOo-MxFEZno1AeQJf0elJcxBKu9esCtwpXYETP8QPoxYbzZYRe33rQgh8QERaEq00ox95kGVsihhqcstvamGNNzgxweMWFCCmxfcDVKwzZ5npbDV1AUrhf3QmQkrmfPWMDRRe8EssMGj5ZSFfaaTsDqAUPBRCvGEU8Uu227QJv0rmW01MeGoU7YqLhQpUuHsTk2ZyAiT4zvDiFUS-7xIUhYERruZeQ8nGPE-0xpEVCbiEDFv_n1b7jEXLAqoIv-9mlRlVZ4fTtnOA-mE2ly_WRinzA3d0s-Z1j5mKsQN_nrUMAel8dyIpUlRJVFmwExmvoPmtIePZYDHWn7ZjbXhHCoToCETWBZqmBCFqH1rInLrTaQb5yjzYsCkVmxP3WWtlbsRWWUs8onCtEjkSGUqXEYxNUBYir1SG-g2YqeWCrdJkRjEgHLqBumxFLJwOUE1n2bbogoLNyjDikcaxmHNpzipP-8-VsJGxoiq_PvWKtepyEh9awMsRCHl1GhTuUubz9U0Qfa-tUyRxeWicjynQl2elHEVxTzO7OBbjrq4weKPmVChdGmQVH4SFWHqBqYTRA-tkFs-ZtaEokmdHXE4yqMOzdAm1ZgLPaelRVvlQDmY4cWkd5WqBuIqJo2CAlnaVeqI79DIJ4qZ0o8zsEpBnhVRyVLJYHLfJH7Gw7hD6MoqlnmsCsDNN2BLM2fDJFUePCVD3aYbR1nIoxRCGN1SZAZnaH318LEXQr2TqhJ5KhRuAncPsmnuxkl___qlrKNjvxjFr-p2Jr1iw2GzmG4Oe_vy64OOsJUoMchuawEIFpZGF4dakaOUgJ-uF4Gz9AhULUl2jRkMFj3-mo-kFEH2NR6CwpkbuAlu0r6Y-L5qgXjM_hDkTwIga4GT1GE9AlUR9QMf7LZMWHQItwj_2mMMLmIygjEqB8aq3RUgeKDtZV1BFs-o_mZ1tL79_ctXKP0jxvqyzUIcCNxwD2Ejte7JNWSVA2Vv2AtUmAQuHcitMxFbkqDxIJ92Iz2QZ0HhlykEJaZ51cxHMax_j1knSqrKsPTyuAR7YUyFGX8il37MKBONTwZ2szqWbZ0-hSyPos9S8ze58ftWA0zg-GtYqcQMnLRJihOtFLilvkhAJGnY0or3NHY6uJQosPctRv0O06L0wqg2FWbVXC4jIcHc6qoV3UB02aRJYT06C-EQU1Or1fsnjIAMhUQnkOhYkcSq1lKxH3Wfc7hUYQ-ku4sWcy3L3ITQWcPFX9bGYJqalDC2ytTK5XbjnKuYlznzstxlwGi6ocHMntEY9IfPkTnoOafOZmtUidV3bqNUqOVZaNiJtAqIEBUMlFKV64krA30D_4s9CQ7pbPTFba19EGPDX9UmMrTGU6PaoA0dtnECFir4UNOaL6-qhbWVLD93AVXJ3Sx0fZZFOviw5usYqb_vmBzll8MFwwZRaU3ysCbnKK_lyQbgKOc0Tbwq8RPumk58ayaO-U6ER422gVu3VA91K1nfHUZ68d_et4hiFnSbTpRpZ7rpSLH7T4wDPymUK3d-JcRNNpzophSwjhCN8BI2Duj17OZ6girrfFwvHxXmWJB4E6iMqWoVhaAOBKukNIsuQsJmoX5LQzcaIfm-ItASagk1XzNJb6Nsk9KAhaJz52UvbBzxs-0fWt6fvICGylo4s8P4r5MML5F9wyLaABeh5y2yrTvcQjgM-7f8326MMfoZ2U1-m9vnM1KNNNiHlxDslBf59dnzv5x9B-zx8hvnFTDWpzOcUSQnjJz4s0Ssnv6zFDn597d1sWF96bxjIHQ__Lz6bccAsXHs65yAoBc5A3uDEs969IEu4G9KFwgzhichR0qRicFvrQNvHH7ciz4TnIUkSuDim-yA-mNfVffw74iDaJzAn_cdJPaSek9uzhLSmm9uizsPCnvULncb9_WoLea-zfnmNzVbnxffTXj2Lfiuw2TqEWYtFUWo3g4QRbd8V-TNHV5JEJj5bkeELQmoIwLL2G2vf37LV0_e3PItiecgnMeDZam0wBEJJRA9O1mQhfvAMIkARrd8j-XchtxecWpiVmRX9OCNqbZfKc2rNfLK8gOVkkXdKiBzBTUjHv0uTUEM0YLoKBwgotDssoNhOoXpHlQaS_IQep_wSzfTMqqSIizy1IWgP_KiKPAql7GTX7qpxrHd_qWbiyb7B2uyu3-_qh7Sp1d7Hv58fArf_5e5gyVERyGwY5xFnBWxm8c5CxMWhWHoeXjzQZqnZR54KfjZhRflvl_FblJwP-URi_PTr3Rk8mAQPffiI5MH4yJx8yyp_ntPHkwTP-dYqE14cZfJg6esjM41yq74qTKU6X6lwHC8nwmscghjr5wrxOtpnQ8f1LfknhhhaM8vxBUfPcLwYH4hrvnwEYY35xfiessIw2WE4TLCcBlhuIwwXEYYLiMMlxGGywjDZYThMsJwGWG4jDBcRhguIwyXEYbLCMNlhOEywnAZYbiMMFxGGC4jDJcRhssIw2WE4TLCcBlhuIwwXEYYLiMMlxGGywjDZYThMsJwGWG4jDBcRhguIwyXEYbLCMNlhOEywnAZYbiMMFxGGC4jDJcRhssIw2WE4TLCcBlhuIwwXEYYLiMMlxGGywjDZYThMsJwGWG4jDBcRhguIwyXEYbLCMP_BiMMszjPec7juIhnRxjeZYzMTGm7iCqPg48e2jCMw0mG38xOhQKuH_jR2VAz_bOwa8XLIsPy_ewsw3e3jGAi_jsxC2F1g8lo2t-Ez2iU4WEryv2HGCpn_gXtcTi_kDBKYi7hOY0wfD2dFCUz_GoQ4WFWVxcVz2kk4bvJLEL47M05hNqFJTMjYcfTJkHWizGC0gDRjEI0YKInRBBkYr8Dh9By9wjioBC8VJ1T_Xa7DZPpOynINqp20q8iq2vHZhSeH5lR-MPP_w_zC_4D)
