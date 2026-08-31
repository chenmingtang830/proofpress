[//]: # (ob:a2cfa24a)
# Local Control Plane Roadmap

[//]: # (ob:cef6a910)
> Status: proposed implementation contract for review. This document defines
> what “the open-source local control plane is complete” means. It does not
> claim that the roadmap is already implemented, and it does not define the
> hosted Proofpress Cloud product.

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
## Review decisions requested

[//]: # (ob:90caddad)
Before implementation starts, reviewers should confirm:

[//]: # (ob:e1242b39)
1. Is “single-node, design-partner production use” the correct open-source
   completion level?
2. Should Git remain the required canonical backend for the first supported
   release, with non-Git storage deferred?
3. Is a localhost HTTP service preferred, or should Unix domain sockets be the
   primary local transport?
4. Should the first SDK remain Python-only until conformance is stable?
5. Are MCP and customer VPC deployment correctly placed after the local service
   and SDK contract rather than inside the first completion milestone?

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2UyYzViYTI1NDMxNmNjZWI3MjlhMmNmNiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImFlYjhmM2RjIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85ZmRhZThjMmYzNTgxMzcwYWMzZjQzZGQiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Q0NDU3ZjY0OGFhOThjNmQ4MjM1NzA5MSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfety5MaR7qsgqB9n19vNwf0yE7Eb45FW1u7ImhjJ3h-mgioABTY8aKCFy3DoCUU4zjMozq89b3KeRk9yMrOuaLJBsknH_mmHw-aw0VWJrLznl8XPZ6wf64oV42Vdnr082-0uuV9EOfOjMPDiouB54mfML6r4bHWWd-XNZVlf8WGEZ4cNPBW_zKKiSPwqSvIsLn0vyJMgj-LILUvuBn4SlwVLoioJWOXBOiHjeVj5ucvyKvPhmRLWLeuh6D7y_ubs5Wf8x3g5sivYoWEjbrWCH3LewC_-zPu6qlnecKfnH-uh7lpnA893_Y2T3zjv-q6rdj0fBvjOjhUf2BXHl5r9uu_-yuF1px4X3Izjbnj54sVVPW6m_Lzoti-KDW-3dXs1svYqDdwXs2_3_Oephp8vp4H3l0XXDrwFXoz9xH9ZnW04QybCK6ZVUBZn4jeX_CM9BMzll1lVMp4WfhVEqRckLiuCKgxK5MKu60d8tcumbjlQrk6kuSzDMEqqOEwZy9IiLlM_iBI388TrSOouC7YbpgZe2Ec6i64vh7OXf_l8Jrf_fAan3PUD_iQ-5uVlDiz_y9nUfmi76_bsR3gHJQ-wddkVw4u33715_fbyzXd__OH9d28v3719_cevLt9_9_rLb1-_O98i2Y8RIDaOfZ1PI5zbZc6GekAx4k11yQbg50jCwKZx0_VI5Ye6xSWHm2HkW_ikZVs8TkXtCr46oAicvWynpgHaiw2cGce3_nGlXvsM5Aofuix6zsQO9Ikil1_6IQgtD3mcpdyPPC-q4tRnuY87diMJkDwZR56MAzJSfNh1dTuSoPW0ExKh_iVp2HVNXdxYK9jHbC1CAnSkBAxdNV5WILC83_W1FLQh917yIHeLMPSztCq8wgszVuVVWKRZFld55od-wnjo8TAOszwLwoKFWZRlXp6kkZ-nUYRrjwxf5TPwFv__zHf9eO2m68D7wY1fuunLKPwX133puvCs5DPKP6tCnnnx2S_Wbz__YyUrb7riA3H9l19Wd8o8L-tRS_x3O96-_sZ505X809mPpEblVBz8eE9fbn_88wSGSn_-vgZJ7EvnBxDH_xmlgu1btAnwGRF2l15tpi1rH6dWnwWf8Yxhc-aHDB4HKzjyT_hub7uCNcCWduy7xnnXsJY77ztWbtkOnpPbMmn0d2jB-TX85gtn-YvjzQ4JRFsKYn6G56vIKHgVs8xzn4OMf3W-B3GfhpcOSMOuG3jp1Ntdw7cgSgy56-AWPZyKU3W9I7537vwADsgxVIL-sxmJYRhUnGXhjMQveUHea5EtXzjWYwtMcKOwTOL08TsYf-kMm25qSkfowVj_jTvjhjv8EzhX2M5piKVX6KRb1hbc-bDwxjmPwL7E7qPp-QG2BEsGO3WgYeuhm3rYquRNDfuSAQZWM-d3vxuApoavW1DAlaBtvUBP4LKw8io-o-edeFMn76a2ZBB6LJ_EHY8vnIgPoRAY2vLoHZETQgqR--AK2tHZshunn1qHtTfXG97zc-eb0YH4oxzEkrwUX1ngRMW4m1R-cDRdlsQIYRic6w0b4VBaWEwSCspBtkVQzJsbp2tXzvUCXV7glYlXzvn1ZurRlTpg0zg6xHtO6I7HF04o9yE4jbPi6B3xhHqOB0TRJ2sgvChvyESwukUxHaYc_Gc71iDPQn8-AMN483KBETELk9iP86PJWsPGX9fjOofoFwSCQYDTluuuhUNA897w8oqvyTtCEAOEOig4_UXrOD_1Fssa0PsZYVmJEYTHn8Av0F31IOoxxFbODUfRgagbzCx4KWFgwWbv0GajaeVoCfpF3XajKguzGV0_sP4KV-6LDfj8Ypz6-4Tn7m8syE_m5nmahdFT9v3pp5_wixftmwlSmC3vndekPy-sREYaHnFE4j-__fq_5T8MiQVYwrnXicogg6jxKfRpsiBmmdALDiunZ9cO-kAOP4O12e7wlxBal5wEHf7B2tIZloxQkHtVEO6R9kbIgO1l79P3O7-xcGRxBslXkuRP2VdKpPZNQq9nYouyrSTaIcUDaw1Wu1lgSepXeeRRymFI886dP4voGTQD1YA9gj1fOPd_fYFXUQn5fJxUz0XQ2nmtpQi-_NNHjzW7DfvJkaEzCBaH5HUU4sP7HnwIbz_yBrZZsEpuEAYFS-MZmf658_20w1wKdhIHBMnlxxqO62HO_gvnYUss8C8NWZQGPHpOwvZ4qL4KIcEAciYW3HTDiJWQklcM2EncRC-8wMMiiPPEq-ZqEUBwQSo93sCRUOYgfoT1IBniNej9fUx84BpLUlh4Ls-C4FlJW8tsoxaL1HxwpoE7H01p6QO_GcDQQQDcQxQMcQyWKNZYolhgY5mXRcn3rFp4jmlIQW6yABrLCcLYurHpFXWve1j5iHUW2MmDsOJh-vwkrs0So3MNxwFWArwMRxkFpwDZROlQxoSVN_j5uh43sDikF7tmSbtTnmdJNDdC0bnzjqoqRN2urz-yka9LNrIHa_fDllh0_gkk4VH-nISt1bc3DIPHj9rQDsWGbzFIQgmFZAAcDbflfii6BR7GQVIWQTaP22IwRF_-J9EpzDha20_wUw0ywO9j373fXuBc4vluFnjFM5GDJhF3K513N8CQltahHHHcQGxbNDXlIx9JkbnNVDuovMutsDRM5oqSkKJA5r-lBFjoRsMhonWAnPIhnHvYEkt5pV8FFU_S5yRs7fx73_0NIpSq_oQR4SBEjRi2gfzhxtkxUtfSqVjd0BNY_0ARXOBh5cdlwBO2VwSgVP6GIqV7ax_zZxfYUkVpkUa8OG6vr1ixcSBTu-KqCtLgy5IaiofIK7x7L-xWPYK7vW4dLKwNCzEdD33Pj6s5A76nbVznt7__CpuBiSxlUggSybbOP6nA8Z_vE6XHLLRYOoIcmO0VBJ6FyL8Av76Igx__6VEtlhe7qWleLHA1CViQhlF6B8EeEWxqdD3nf-NOAWdZgxXmD-Po_YssVSNdsBtFzJ6XuDWoQoVJ875PgGRrGPuJ8jgZNGMyxnbSgTtlvaCgLI7iKCqemdivPtUj5IMYAgCpL8ECoQoOe2FvU1e8uCkabqURG7Zw7K6P6exeKCCI9YnYeThdkcMd7y2wqlO_d42lIDVO0jhI82clDRxbWZIJbrpuh8WcF39q60-QdhYf-KgXGza8aVbOddd_GHaQlOOZVQtn7hesSMO9fOmptO4f-XjdwQp4hKNKkEHBC9Bu9C0YTrMKi4JYrFw4cr-ooiypojtoDYhWHQOJgEv16GQO8LCDf8hK9yQpLKgyz9urdj8PnUIKVO3wRhX1TOayomjwhdlBNBzBLixpfly4lZtm8T-A4n1ZYGg8ho3MriCqwPPHlGK7m0bRY4CoBawBpK3L6l_4eXmX1Q-JYpO1PCqvetgSyykVKwr_WQlbq9IWpygYM6Y17o0Kg1W7GqvpIAPbHfwTcjZnh35hGOfh423dT8IgzMr8OUndP24465H1VM2BqAvksLBTS3tVZ1w4blZFRcbju7gaEalWtE_1orZcj92ay8j3Yaf-kJXYcI_Hj5MoKcs7DepTKV0732_qHanILMURSc3KLgX9PNXFB8l5ChIWxMDj8BpZWv0DKL6t_CUf6qsWEoh-bKXy17DnFbkGFUhT02ipaQWZhF_yu3gcC3NVsp0oOVSjTFysiuzDpOEhK93XU4pZ4SdRkP4DCP39VENewqQv-PbNO7UWnRFW_dYDmAqwsYUjgU-DKD6zaqkUzzLImypvRvFXn3bgROAo265dX3WsEfneiA2c_gHd_C-ch62w1J2DNDcLA_acdK2db6dmrNdgJxk1Ka_A8fxNxJ7gg4BjW9IrMIEN0IM27Ao-A3YvNsYCL_LyNJznnv9OTWzZuMaoF8Lg5h6mHfrOAps8N3KLKuZP2_u_sD1hc9HuYKzsXtQ1sAa9EFYVsH63GL-FGQ-j_QLAo4n7AbvLQM8wVSDbVM7BQ8fCYjcNUh9KTp0CPD_SB9kOX_IwRZi75V7R-z1tCqsJpMLgaFzPPUe3-MXFOmIB67HyGaj4PQe28H3ACvkEjBLpMbQ8ssKBeULdb5da0dzzQz8Psmcgzjt3vhnAAv73DLchnMNaOQcFPQGyp4H_9vf_K-1jf1v9fgSSGlZvD0KSZpQcwAsdfMYC7Bx8xoLcHHzGgsEcfMaCphx8xgKTHHzGAnYcfMYCWRym2cAiDj5jYRQOPmPBBRbeXbfuD69j2uyHz8u0ug_vZXrOh9_L9IcPPmM1ag8-Y_VOD8uPaVwe3sv0EA_Ls2neHabHdNEOPmN1rw4-Y7WPDr-XadksnKnunhw-C9O2OPiM1UtY4rOq5B_WL1NUP6xfppp9-BlThT7MQ1MUXrAtuiZ7-N1NGfSwbJhq5MFnrCLgYXpM7e2wjJki2GE-m-LTwjO66HOYZlNwOSw_psSx9F6qqLAk8yq_P0yzSawP02wy2sM0m1zysA032duirMp8acGG61TlsM00ycFhf2EC9cPrmAj58HuZSPawnTcB5WE-m7huwf7oqOvwuZvgZ_7Mj1Y09PnsenNDnSYqz48bbveLhqLb8ZVoLEEIJnvAVLTDGLWwgEciZWYynbkfYZTfGezlkK-0wzmi7h88-7AwjiJmH-yhBhvabw86fD4hxE8I8RNC_IQQPyHETwjxE0L8hBA_IcRPCPETQvyEED8hxE8I8RNC_IQQPyHETwjxE0L8hBA_IcRPCPETQvyEED8hxE8I8RNC_IQQPyHETwjxE0L8hBA_IcRPCPETQvyEEH9WhPjDb3lVt5xKul7G7i93X2d6342uz3Jta-iyLPSqPI5g08oNeJSXEIyn3I0pH49cVkaJnxSJD2-TlxnP_DLifpEEVVFm-aEXuusC1-xl6N11gau6wPh_4gLXz2cbNmxQJsoMAufKi8MqgQdoDQtUJuXtCGiYXN_nXpqUbs5ZHKr1LbSYXP8pmC8VgGGzDURjuGj_VYBhQNDHx_WJUdq3nLUDYXrKjhM8AhekSQjsQo0CgWgstEKcaHp5KULs2qwgScOv4mIYJ2AgaSz6m6abNOrr_A5rILnJ44InkQ96lXuKmxawTZ3WfYg1uVpV-GXp5WEZu7lazQKxGVzS0eg0Ua4USMqLNsfoiYBUigV3A030cc0PitwepGIgHhBTwXqDui9aVbGoHo5h7FpdNWzQNg4r-g7eoawh9xll-A42Gd_gzdtvVhctHhpeht4TdTpKXIE01dSO5DskHr8Ap1-P-ALqXnT8rkiuC5LXi1bcZix5QvIAvhBRQLAtxIN0LzWSv3DaXuCFXpFmaVD46nwsUJ9CkzwBrQfOB97UnBjwVJW0plpwV-ib8e4y1t3zGlj6qpruevjd70h3aqk5zNna0R6qB1rigavi1rmj4S1_fveGlr6lF8C3prsh5AsQKGSw59gtptxFly4HvkWcVzHMmtCzFjIiZJQqbhdYH_tVWBVpkvt5qlhv4ReNoj0MkChXTasqo9N0M20MLYyidaDHgg4HDMcpX5Qtp4tW3sVPYcLYgSRYCqoUa9yYUuHOdE_ZDqNMlF9ViTq_aCkUvLUGEphzlRqRAskTXiG0TJ7xWmp0w3Vr9qLdsmIDR7LC3jRzqgnr6MpAyDVeSdw3_V2AUtGKZ46y3Rr6wMjIg1iR4W05FjxZX2MK5uw2N0ONci-31Ke2IAlF4IcxuP-g8it1ZhZ-87aRfDQgcyNrMgQBhH-CfQPF0Ry3XZEo6BTC7iqm_q9Brg8CMtZbYiSYl2EULALLtgWVR0zY-9dfIxFbvu2QQdJUiKv_4eMuR3ar4hNVOduSjqWawPQS3gytbofy914j0KS2jX0NFqI0KDWCHig5BPO3m9De4lug-aTbzxf4nqZlmAR-BCESV3y38KlGAx8GOJWrBknJkiAuvYJOT5hUg0G1NPD5QKVy6yjzwd-CSU9D7W0tnKnc-knA0Wqwe3j6-Z9eXbRrbSfMiWwxpp5ZizU9ROXCZqI__KGtCq1RQpDUb-sWHX4B32LNJGQMjvRjPSCz3n7r_HUqryh1JxsiBBmxJ39A4UdSX2u7MohRDKqQKKGgRjdtJwpuIvYCfaGthpWMBctaZCk_T8BoOAm0IMOERVhxs_4KY4W6F8qFuwrF5OVa5lGOsYzi5eqhaLoBrY9oPA_1thabOlf4R1JWpgZv-_qVMpmkGejo6TjO7XYqPXD-16Frf5JsAVsM6rWWxWTdkhOhrfOnb4gkWagDS9usCak383ZsuwJd7q_0nk9p9sbBP69Umzm_wdVkpKTqnQysdi-UXfQLRrShVxg80YmJMtCedK1woTvE6YWRnRfildXAjjgaaU5Yc35HzUcqVO6mflp5blWmmVIoCx-tdfl4wLNhtPoiu2grAdPYTTmcqfP63Tev4AkMtRpihe77IqKt7PR2Ilx5pWsAqn0ErJZrF_3NbuyuerbboJNClQDdwYcKnCt6RQxqu1kXt71ag9VvdfStA7iVKfGr1GmFxWQy54WFU8FAjxPaadjUYG3KBZucRSlki25VVVFooiKN_DY2-cE4bhXpujnk1cyFsMscpYF2y4WfDNQW_7BK6ysK_ZElIvC3KrrWV_7P_7toRf5rh6Z2KowP__brf__2698tdICRIBAS6wnrVPFDy0iOMi8YrKfnJtcKzkzaw1swtzYN0oj8PPFJ2DKyvNrsWk9a_SvKCT7IkqsQHWXBy3oU3_lVrE6BNX22YFMPHQBy82sTPv6nyBH_RVYYwPc5b9Fp9bP3OeDZYL2CtV2L-uIIrygzMuvbBwwxEiPb4vRL6w3tbzjz_9hNXwSorlTUBZZ4ZAgzROhHgYk-iOsdkwHKeBVl7GdeVCZ5oTN5MyygJzuOh_5jbLcWsR0WIDHS7iFBqtGl3BmQIzPIwwoDOE--ybfJXgaVMW6FE1aesXLE3y8bRJ45EiDGShnopIY5VviibTnHBdV8ZsnB8aM3UrnlOQmHeAcRN5izVwn5Wh-_DF9pOfyeBmcMr0yWgc9iX0h1cTAwl-aV2htfo-Bb6SelSt1EsRcq3ZWlhVg4gt8smM8yjPw4TKskptqXMJ9mCsMKaR86UyEXZmlYlQVIU5boQoE1ZmFFtccOTTROVxHLK5CV7hr2hxQFGIh_UmvhjYM8z4I4ieLS129sDVnoNz5yTELu4iZRUeZewKpIB_XW5ISOrI-ffRBYzEEL-15YQ6V9HZ7aYbEOhVWQA3t0zSTzMmcvYDUR6GoWfoLyYFSAao9ksGY1M76SGHzPc4wa_yT-yJRyRUBSVfOmxAxPMVYqX90CrXUp7AMu30LKQ5UCxJjSug1VY0WJQMS-MnleY1JEvxC8Qgs30P5fUdhBAHSHFQXHIgxGshZWAkynShunXmqzriOKcyDRQxLws4FtuZ1KyDNDeRUYB4yPMKxpMCugNSjgGjTanSh7Y4Py5J9DpEyvHwcrrtLFZsPBPc4hXd1uFI3JijOB2FXWAWvBNxQbU_2KfQRmyn0FGRAnkpGWxTaM9gYIoofBvCwdjIkQ4KQgXzAfi3QTycDY-9z56uephq9QGUDwZpB1WmCs-UxZXmO26OgHEkZlilczlPFCBM5ZHvks83yv0E7MmgWy1PvoSR5l4bIkhjA_cr1AB4jWcM_dKv6o0RwUlz_88MM7AVNnyA-F-XMk3I_qU4j_g03IkYrf05F-g7Um_GZDECDaj5EP0atQJldh9WZqGy7P2kbaU1u9uZGyNaCfljlRVV-RgN0ROpLSksMyuCSi6L80GhFyH_F71Ae1j8CUgeysaX0wI-fAPaVX4FkxJeEDpDMUWWKlVRNSWlBH7ALXjShqC5XHIiN8GWuuFKT1RM732AOddkqu-WBXWEgIVwY2p2YttkBgrcZgTMLkYPZJMy1CVI2pAa7KexuEVgtTgOIEHxEdf-CsGTcr81syrgWvJhDJzTSWYDlngN6mu5IaoUIeySSy32CNRKELK-HKSd62JAtKlLk8hCw2jlzKdUSHzAyDWUp0_CSX3CrhAahMGmAZWztKM9yltej4ySx6aWAebEz1AOIRLyYkdI3ApY_YBlCGnGlhfSfafr3wmNy0yg1crcfqKOIsBxkDogmHAwbmqpmdQpSXQBE2IDWjIEsmQ8LeIpm6zoTGUAQ4EHUocKyz6cBVqpSeXKCJrYUEzZKpWUC6V8iyirhfztI4keUpR_L2W-c_8K2l49srnKr334JVK5ULmldRkarX6l8r6fLox3l8YQUfd2dvJhh3nLyWlR7yGStN0AvpFDViVNe_5AewNv49UFtEyY1DkgR6vt2JvckYNzcGhVrKpIHe5r1q3iBWLVfCh6FhVVEhRwfiWJMVLn-_b7Sgc77HsbMTRkGga7HW5KClc08b-VN6l5QlROi-F3MdoFpTgFrvjh_fI4uORbMbVFAZEFIw9ApLRsqsU36jrDXSLS2nNNcyg4YXEGEK2t-er-E918M12-HudiwxQ8Wa5pv0Q5Q16DgDSaLNpPCSpgjHRBaVdJTKiEKaQeuAd3D04zUHBd2LhlAbau2lVJzDyAjXonQmE0IyQOhdzlGmRMCHoIGZOpIfJfiMYKqIDOr2r5Y7_T248GlHOoSpMFWXscCpCp0ySkNUJYaXdoGYDtGKS6Ta80-8L2qMrtkVWhAqSTaQRRrvKjyn8Ibb-sr0vNSZr9DIXrNetgioN6j7ZIImEZb0XHAfN77Vvd5y6kaB496yD_PiNkWlC5rkZn7Cq9itilS3aayBUUuTjh73VEqUFbGfJ5GblIGpEeoJUK1Ex89v4k1Spm_qKD6quosq3DLMgJEPg2kxgOqhi1CGlR7h5Ww1Ux-R6RgdLiblKk6VISm1aYkvKKBbBY4U1gaXGEh1B2UQwA3K_cjMYjADp3bTdKyce-kcTa3AX1zxlirW4mkQIA7WdJDyxsHjjYN9TI4FyNCtPapZd7ua2g9AsgiUTBIhvL9umSicknhv5bHFnVa0HtUZxaMYbKH7wTYbmi5C9yisG2wl0kXM0EztTrkleI0l08-rJKgyv0xjpgFP1nSuJbDHDNiqTSB-i4q4YNwUyq2ZWytdOXZsVuSNMrp85YgCrW4Ty04lNirhzLWnZ7IxYwGrdD6KJpUhngBjPZ1mKhp6qyaD2Xavsne5iwp4KXeRLhq7zhI-ogL9tUj9NFpElAtoYg5kqGimkqsqA5UTVjSkBPZpGMQFb9LFzRzwlpc1UxVnYNyoXIiYeYH3UZD3ehR-FCjWJnYl0JnilVXvRKLQBMzIOdweVVYBwV6ifc90VGobF9Udt9uQqmSDBHS7-f638UJkk28kDELU36u-26r6yJ1TCAta4BV-GKVRUjEvtDJ3NW5tacHRw9Jyp9Cv0rDKorJkBvNi5qe1Khw__awzCQozZx2N2dwLYlinneX3VnBmJlUztR5jU6R5MnZ-1nreD6_teJBE8EvqoK5FrUb2mqjrZBd_dAK_XwGyunTCvmFUPUgfD0_V_bzZiPs2bCdsuH4taVpwxz-iQjZsagsK9tqPdd-1oq5NO7-hVqakiipI9C4i3y6--54WeVu30yftupQoKONuMBIzeaaX1tOy6oxXJqYhOe66RsMGZjGIkm4ZkYDcU9iU31BZQh6cRZOuK2A41YP2NCznzSCtN63UWFMgcnQDew-qkjd0UrNqRETzgTIxGW5COgL7jxAptQIEPy9sqZbKWl0juWEf665fUkaWZx6vwqBKdAxlze3bqM57Z_EV2CSF0wj9PGS5Lrxb4_lqlOMJI_dChuW3OEPbdgcYFD3LNNyDc_SLyquiLMvjRJsIa2zfMkZPHLfXzPH9MGdB7mWRwb3qCXy53xPBFA4nR1YPG16KjtlBJAd4jB2iKaRXxboCZQnKY0kkxhoT5hfA0YvWGtxGK4nlC1lqE5joWuofegE8DIEVQeHFX0vowh21qVsN_9gNAzdwWZZqvLE1-n_rZI4a21daEIVJ6QVpFMe6iWVN8mtHcfwU_mB1tfdchUlfyYx8Cw9KX4vFHWRhgUXFOwbmseC4UaUSc5IiyJ1IAGZ4C-3gKgrdLQdBhy_QNFQzOmwwIFxNWMBjN4o0OtW6R0APah1_B8BAMiXpQtcLvrVr7-j9GHCJQAXbabXozNxlAW-B_Xich3nFci_U5sq6a-CWnB1zUYDCc7pe4vMqzapCGxvr7gATmh89-A_8ESNsVp24gTxOJJG66myKzWRJZwVn7BnKqp4ZN9wr_uddNyLGczfHattDWLJIRrUXjv5K4ddVjCpuNBYlFhnzqsheJLvCqWLpCATzhXptIaAStEoROmVrKn9dkNwo5KUPXpZ7ia5AW7chHJDcx1xlgGG7eQN0Sn03XW3seEQC-rEgggxBuRZtUGlDFxD5mR8VnueWnu8b8vUFCbfk9An3Gqjw2StyL_X8LCm0BbauOpiJ63E3FFy1FPPMIY0ic8dH1iqvxiPW4ZnM8dZWU8AYEvViWoKx29t3o13H-NgpMZbWQVd0RaUKD2bX4-9lsL7UQeFpEhSRV7lhqVN6c7nCAaF6zJ0IojK9mgHyRLyjyhKGkSq6F-IKUqkDATM_hA8j1psNVlP7ohUpJD4gEk2JVlrwzzyoUhYlLHW5ZTfVJQ235PGIKxaU4uYFd4MUfLPnWSVsdeuCVcI-9s6Elax5axia6L1gFdjg0XKqwr7QRVidQCj4KKV4IqhiV203aJf-lay2mpxw1CVblReKEqkIdueuTFSEKfBdEMQqiX1eJCkLAmPdzH0PBwTxMbc1iKxM5CHivvmLtpywFiwaqKL-vZp1ZVWdH7hs14F0QW1p3iyMU-aGbunnTFsfcyvELfl60mUOyuK5EUuTokqizICZzP0OWtKOv5YBHmv5VTfWRnKoTYCOTGBZaGBCNKKm1mTk1pvIMM5R7sWASa3cnqbLWqt2I6rK2OQTjWlRyJHGVISM4tYA4SkmZTYwbMRJLZVukyExiAEV1A0yYilk43KGaj4stkUVFm5QhhWPNIzDup_ioP18-LUSNjJGdOUvWqtdpzIj9VcbYCFKKedOm9pd2n2u5gWyi9ZyRZaUi87xkgl1eVLGVRTzOLOTb3nVxS0Rf8oNFcqWBknlJ1ERpm5gJkH0pRVyy6fcNaFoUrwjCUd91KkZ-qQaa6HntLQYqxyoBjO8ms2uUtdAHMVsUFAgS7tKsfgBg3yimSnjOAOrFORZGZVslQym9k3qZyKMB6SurGKZx6oAwnwDtjT3bJiiytG3ZKjTdOMoC3mUQgqjR4rMxRnaXh1_7YUw72SqRJ0KlZvA3YMcmrvF6e_fvpZ9dJwXo_xVnc5sVmzYHxbTw2HvX3-9NxG2Ei0GOW0tAMHC0-jmUCtqlBLw0_UicZYRgeolyakxg8Gix9_ykYwi6L7GQ1A6cws3wU3ZFwvf1y0Qj9UfgvxJAGQtcJI6rUegKqJ-4IvdlgmPDukW4V97zMFFTkYwRhXAWL27AhQPrL3sK8jmGfXfrInW979__Qa1f8RcX45ZCIbACfeQNtLonlxDdjlQ94ZJoMIkcGlPb52Z2pIGjXv1tFvlgTwLCr9MISkxw6vmfhQj-o-460RpVRmWXh6X4C-MqzDXn8iln3KVicYng7hZE8u2TZ9DlkcxZ6nlm8L4qdUAE2B_DSuVWIGTPklJolUCt8wXKYgkDUda8ZzGTieXEgV20WLW7zCtSq-MaVNpVs3lMhISzK2pWjENRIdNlhTWI16IgJiGWq3ZP-EEZCokJoHExIokVo2Wiv1o-pzDoQp_IMNd9Jhr2eYmhM4aDv6qNg7T9KSEs1WuVi63G5dCxbzMmZflLgNB0wMN5u4ZjUE__h6ZvZlzmmy2riqx5s5tlAqNPAsLO9NWARGihoEyqnI9cWRgb-B_cSbBIZuNsbhttfdybPhUbSJTa-Qa9QZt6LCNE7BQwfuW1vzxqlp4WynySwdQldzNQtdnWaSTD-t-HaP1j70mR8XlcMCwQVRaN3lYN-eoqOXZLsBRwWmaeFXiJ9w1k_jWnTjmbyI86WobOHXL9NC0kvW3w8gu_ttFiyhmQbeZRJlPppuJFHv-xATws0a5CudXQt3kwIkeSgHvCNkIL2HjgF7PHq4nqLKux_XyUeGOBYm3gcpYqlZZCNpA8ErKsugmJGwW6rc0dKMTku8rEi1hltDyNbPyNuo2GQ1YKDp3XvfCx5E82_GhFf3JA2iorYV3dpj4dVbhJbJveUQb4CLsvEW2dYZbSIdh_5b_261rjH6B__5_txPpTg)
