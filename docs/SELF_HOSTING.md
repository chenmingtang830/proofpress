[//]: # (ob:26309ab6)
# Self-hosting Proofpress

[//]: # (ob:2baf81ed)
> Status: experimental open-source self-hosting reference. It is available for
> one operator to deploy on infrastructure they control. It is not a
> Proofpress-operated cloud service, a multi-tenant enterprise workspace, or an
> SLA-backed production offering.

[//]: # (ob:a4ed5f61)
[//]: # (ob:self-hosting-quickstart)

[//]: # (ob:5912f45d)
## Deployment boundary

[//]: # (ob:078d3e10)
The repository intentionally includes [`../render.yaml`](../render.yaml) and
provider-neutral reverse-proxy and service examples under
[`../deploy/self-hosted/`](../deploy/self-hosted/). A fork deploys into the
operator's own account, storage, domain, and billing relationship. It receives
no Proofpress credentials, customer data, deployment access, or support
entitlement.

[//]: # (ob:5d7ac1b4)
The Render Blueprint uses persistent storage and disables upstream-triggered
automatic deployments. The operator reviews and adopts updates deliberately.
After deployment, open a private Render shell and initialize the workspace once:

[//]: # (ob:b44b9816)
```sh
proofpress-self-hosted --database /var/data/proofpress.db \
  bootstrap --workspace-id workspace:personal \
  --owner-principal human:owner
```

[//]: # (ob:1d8907d8)
The command prints an owner bearer credential and a recovery secret once. Store
both outside the repository and deployment manifest. Before relying on the
instance, configure backup/export, test recovery, restrict administrative shell
access, and verify that the public endpoint is protected by platform TLS.

[//]: # (ob:c3ffa3ff)
[//]: # (ob:self-hosting-owner-assistant)

[//]: # (ob:5014c855)
### Optional owner assistant

[//]: # (ob:00f7592d)
The owner workspace can route bounded, read-only workspace snapshots through
OpenRouter. Store `OPENROUTER_API_KEY` as a secret environment variable in the
hosting platform, never in `render.yaml`, Git, logs, or client configuration.
Set the non-secret `OPENROUTER_MODEL` model slug explicitly; the reference
deployment uses `openai/gpt-5.4-mini`, which is also the application default.

[//]: # (ob:ceed7516)
The assistant may explain evidence, checks, recommendations, and current ledger
state. It cannot admit, reject, supersede, issue credentials, or change policy;
those operations remain on authenticated owner-only surfaces.

[//]: # (ob:22603d0a)
## Decision

[//]: # (ob:a09ba553)
The self-hosting reference extends the completed single-node local control plane
into one private workspace, one human owner and sole authorizer, and several
authenticated agent or device clients. It must preserve the existing evidence,
conclusion, verification, review,
supersession, and governed-context meanings rather than create a second
governance implementation.

[//]: # (ob:46933f06)
The alpha addresses repeated reconstruction and re-review of completed agent
work across devices. It does not coordinate work in flight, assign tasks, show
presence, or become an agent orchestration or project-management workspace.

[//]: # (ob:f727f4e6)
## Product outcome

[//]: # (ob:a1f7f460)
```text
Owner's agent on device A
  -> import bounded evidence and propose a conclusion
  -> hosted deterministic verification and optional advisory judge
Owner on device B
  -> admit, reject, or request changes
Successor agent on device C
  -> retrieve only current, admitted, in-scope governed context
```

[//]: # (ob:2e227c39)
The product succeeds when these clients observe one durable governance history
without duplicate events, silent overwrites, stale approval, agent self-approval,
or dependence on copying raw artifacts and traces into Proofpress.

[//]: # (ob:27e267c9)
## Baseline and gap

[//]: # (ob:6440564c)
| Area | Available now | Hosted alpha gap |
|---|---|---|
| Governance semantics | One local operation contract, lifecycle engine, policy, graph, review, and context projection | Preserve the same results under a workspace-scoped remote request |
| Persistence | Append-only Git commits under `refs/proofpress/knowledge` | Durable server-side event ordering, transactions, backup, and remote recovery |
| Clients | In-process and loopback HTTP Python transports | Authenticated HTTPS client usable from several devices |
| Identity | Caller-supplied actor strings and one local bearer token | Server-derived owner and agent/device principals with scoped, revocable credentials |
| Concurrency | Process-local write lock, Git compare-and-swap, and selected `expected_head` checks | Workspace-wide idempotency and optimistic concurrency for every mutation |
| Portability | Local Git history and portable artifact verification | Exportable, backend-independent event chain and offline verification |

[//]: # (ob:507d8562)
## Frozen alpha scope

[//]: # (ob:e41232a3)
| In scope | Explicitly out of scope |
|---|---|
| One private workspace and one human owner | Multiple human members, organizations, invitations, billing, or enterprise RBAC |
| Several separately authenticated agent/device clients | Agent task assignment, leases, presence, activity feeds, or Asana-style coordination |
| Evidence import, conclusion and relation lifecycle, graph/context reads, and owner review | Generic connector marketplace, Notion ingestion, or organization-wide knowledge graph |
| External artifact locators, digests, and bounded evidence projections | Default storage of source documents, complete traces, prompts, or private reasoning |
| Single hosted service instance with durable storage | Multi-region replication, multi-instance writes, customer VPC packaging, or Cloud SLA |
| Existing Python SDK, remote HTTPS transport, and one thin Streamable HTTP MCP reference adapter | TypeScript, Go, a broad framework adapter matrix, or hosted plugin UI |

[//]: # (ob:8618e948)
## Target architecture

[//]: # (ob:965f2a5c)
```text
Python SDK / Review UI / MCP-capable agent
        |
        | HTTPS + scoped bearer credential
        v
Personal Hosted Control Plane
  - workspace and principal authorization
  - existing versioned operation dispatcher
  - deterministic verification and policy
  - owner-only Human Approval
  - transactional idempotency and expected-head checks
        |
        v
Backend-independent event store
  - SQLite on persistent storage for the single-instance alpha
  - hash-linked event envelopes and reproducible projections
  - export bundle for offline verification and later migration
        |
        +--> external artifact locators and digests
```

[//]: # (ob:e6f09d2a)
TLS is terminated by the deployment environment. Proofpress still authenticates
and authorizes every request; trusting network location alone is not sufficient.

[//]: # (ob:3a876344)
## Canonical implementation decisions

[//]: # (ob:2d37c93b)
| Decision | Alpha contract | Rationale |
|---|---|---|
| One kernel | Local and hosted transports invoke the same operation validation and lifecycle functions | Prevent semantic drift between open-source local use and hosted use |
| Workspace context | Authentication resolves one explicit `workspace_id`; request bodies cannot select another workspace | Make future tenancy possible without exposing multi-tenant behavior now |
| Principal context | Authentication resolves the actor and roles; security-relevant proposer and reviewer identity is not trusted from request parameters | Prevent an agent from asserting the owner's identity |
| Event identity | Each event has a canonical payload digest, prior-event digest, monotonic workspace sequence, policy digest, and authenticated principal | Make integrity independent of a Git commit identifier |
| Storage seam | Kernel reads and appends through an `EventStore` interface; the existing Git backend remains supported | Add hosted persistence without replacing the local ledger |
| Alpha store | One SQLite database in WAL mode on persistent storage, with transactional append, unique event/idempotency constraints, and verified backups | Fit a single-owner, single-instance alpha while preserving a migration seam |
| Idempotency | Keys are unique within workspace and principal; replay returns the original result and conflicting reuse fails closed | Let devices retry safely without duplicate governance events |
| Concurrency | Every mutation supplies or derives an expected head; a stale head returns a retryable conflict | Prevent silent overwrite and stale approval |
| Artifact custody | Store bounded projections, locators, digests, and receipts; source content stays in the owner's systems | Avoid turning hosted Proofpress into a document or trace warehouse |
| Approval | Only an authenticated owner principal may admit, reject, request changes, supersede, or resolve contradictions | Preserve Human Approval as the sole admission authority |

[//]: # (ob:fc0554fb)
## Implementation sequence

[//]: # (ob:72654777)
Stages 0–5 landed as separate reviewable changes with frozen fixtures while
leaving the local Git-backed workflow usable. Stage 6 remains design-partner
validation rather than a shipped efficacy claim.

[//]: # (ob:9079b321)
| Stage | Deliverable | Exit criterion |
|---|---|---|
| 0 — plan | Public scope boundary | Product and implementation contract accepted without claiming a managed Proofpress service |
| 1 — backend-neutral history | Canonical hash-linked event envelope, `EventStore` protocol, and Git adapter over the current ledger | Existing local tests and conformance vectors pass through the storage seam with unchanged lifecycle results |
| 2 — transactional hosted store | SQLite schema, migrations, append transaction, projections, idempotency records, backup/export, and fault tests | Concurrent and replayed writes cannot duplicate, partially append, or silently replace an event |
| 3 — personal identity and authority | Workspace bootstrap, owner credential, agent/device credentials, scope policy, rotation/revocation, and server-derived actor context | An agent credential cannot perform owner review or impersonate another principal; revoked credentials fail closed |
| 4 — remote service, Python transport, and thin MCP adapter | HTTPS-compatible service boundary, remote SDK transport, Streamable HTTP MCP mapping, readiness, safe errors, limits, audit logs, and deployment configuration | Python and MCP clients pass the same supported conformance vectors; MCP exposes no independent approval path |
| 5 — owner review and portable exit | Remote review flow, current-context reads, export bundle, clean-machine offline verifier, and recovery runbook | A decision made on one client is readable on another and independently verifiable without the hosted service |
| 6 — design-partner POC | One real work item and artifact profile exercised across at least two devices or agent clients | The partner completes proposal, owner review, and successor-context reuse; observed correction, replay, stale-write, and re-review outcomes are recorded |

[//]: # (ob:330b7ae4)
## Hosted request and authority contract

[//]: # (ob:90271f20)
The public operation payload remains versioned and transport-neutral. Hosted
authentication adds server-side request context containing workspace,
principal, credential, and permission identifiers. The context is not accepted
from JSON parameters and is included in audit and lifecycle receipts without
recording the bearer secret.

[//]: # (ob:cd6f5c84)
Agent/device credentials may import evidence, propose and evaluate conclusions,
and read allowed context. Only the owner credential may perform Human Approval
or other authority-bearing lifecycle transitions. Verifier and judge identities
remain separate configured service roles and cannot admit.

[//]: # (ob:269202b9)
The MCP server is a transport adapter over the hosted operation contract, not a
second governance kernel. Its first surface is deliberately narrow: capability
discovery, bounded evidence submission, conclusion proposal, governed-context
and graph reads, review-status reads, and owner review-link creation. Agent MCP
credentials cannot call approval, rejection, request-changes, supersession,
policy mutation, credential administration, or owner-recovery operations.

[//]: # (ob:133c8adc)
## Durability, export, and migration

[//]: # (ob:fffb1d30)
The first hosted deployment is deliberately single-instance. SQLite is an alpha
implementation choice, not a promise that future multi-user Cloud runs on
SQLite. The `EventStore` and canonical event envelope are the durable contract;
a later PostgreSQL or managed-log adapter must reproduce the same ordered event
history, idempotency results, projections, and verification receipts.

[//]: # (ob:affa0205)
Export produces an ordered manifest of canonical events, workspace policy
versions, public principal identifiers, and integrity digests. It excludes
credential secrets and disallowed source content. A clean verifier can check the
hash chain, event schemas, evidence bindings, policy bindings, lifecycle
transitions, and current projection without contacting the hosted service.

[//]: # (ob:56dd223b)
## Security and privacy bar

[//]: # (ob:b5f77c3b)
| Control | Required alpha behavior |
|---|---|
| Credential storage | Generate high-entropy bearer credentials, display once, store only a slow hash, support naming, last-used metadata, revocation, and rotation |
| Authorization | Deny by default; derive actor and permissions from the credential; prohibit owner actions for agent/device principals |
| Transport | Require HTTPS outside local tests; document trusted TLS termination and forwarded-header rules |
| Data minimization | Enforce request-size and evidence-field allowlists; redact secrets from logs and errors; reject full trace/session uploads by default |
| Audit | Record principal, workspace, operation, request/idempotency identifiers, outcome, and event head without recording bearer tokens or raw private payloads |
| Recovery | Back up the database and export bundle, test restore to a clean instance, and fail readiness if integrity or migration checks fail |
| Abuse resistance | Apply bounded body sizes, timeouts, rate limits, pagination, and safe error messages before internet exposure |

[//]: # (ob:62520cd7)
## Verification plan

[//]: # (ob:39ac133a)
| Test family | Required proof |
|---|---|
| Contract parity | Local Git and hosted SQLite backends produce equivalent lifecycle states and stable error codes for frozen operation vectors |
| Replay | Same idempotency key and request returns the original result; changed reuse fails with no new event |
| Concurrency | Competing expected heads yield one committed append and one retryable conflict |
| Authority | Agent/device credentials cannot approve, self-approve, change policy, mint owner credentials, or read disallowed scope |
| Revocation | Revoked credentials fail immediately and prior receipts remain verifiable |
| Crash recovery | Faults before and after commit never expose partial admission or an unprojectable event chain |
| Cross-device | Proposal, review, and context retrieval succeed from distinct clients against one workspace |
| Portability | Export verifies on a clean machine and can seed an equivalent read-only projection without network access |

[//]: # (ob:cde9d305)
## POC measurements

[//]: # (ob:5caf4cb0)
The design-partner POC measures whether shared governed state reduces repeated
reconstruction or re-review of completed work. It records setup time, evidence
coverage, unsupported candidates, owner corrections, admission/rejection,
idempotent retries, stale-write conflicts, revalidation, and whether the
successor agent makes the correct proceed, revalidate, reject, or escalate
decision.

[//]: # (ob:da5a1a45)
The POC does not claim to measure or prevent simultaneous in-flight duplicate
work. If that problem remains material after shared governed context is in use,
work-intent coordination is evaluated as a separate adjacent product decision.

[//]: # (ob:ffa83903)
## Known decisions still required

[//]: # (ob:9fdea320)
| Decision | Needed by | Default planning assumption |
|---|---|---|
| Initial artifact/work-item profile | Stage 6 | One bounded partner workflow; no generic ingestion |
| First MCP client matrix | Stage 4 | Validate against the partner's actual Codex, Claude Code, Cursor, or custom-agent surfaces; do not build separate runtime adapters |
| Deployment provider and domain | Stage 4 | One managed runtime with persistent disk and platform TLS; no provider-specific core code |
| Backup destination and retention | Stage 5 | Encrypted daily backup plus on-demand export; final values follow partner data sensitivity |
| Owner recovery procedure | Stage 3 | Offline recovery secret and explicit credential rotation; never agent-mediated approval recovery |
| External identity provider | After alpha | Built-in owner and agent/device credentials first; OIDC and organization identity remain later |

[//]: # (ob:1c6ada82)
These choices do not block the backend-neutral history and storage-seam work.
They must be resolved before a remotely accessible partner deployment is called
ready.

[//]: # (ob:fc4cc68b)
## Definition of done

[//]: # (ob:a378562c)
The implementation is suitable for experimental self-hosting only when one owner can initialize a
private workspace, issue and revoke separate agent/device credentials, use one
client to bind evidence and propose a conclusion, review it from another client,
retrieve the admitted current context from a third client, replay requests
safely, reject stale writes, export the complete governed record, and verify it
offline. No agent may act as the owner, and no source artifact or full trace is
centralized merely to complete the workflow.

[//]: # (ob:ce66da5f)
## Product meaning

[//]: # (ob:208f35c8)
Today Proofpress ships a local, Git-backed governance control plane and an
experimental single-owner self-hosting reference. The latter makes the same
governance state available across one operator's devices and agents, but the
operator owns deployment, credentials, storage, backups, upgrades, security,
and availability. It is not a managed Proofpress service, a team workspace, or
enterprise Cloud. A future managed or multi-user product would add membership,
authority, policy, and operational guarantees without changing the
claim/evidence lifecycle or portable verification contract.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzg1MmNiMWMzOWY3YmMxNDc5MDllMWMzYyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImZmNDY1ZDMxIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8yYzRmYjdmM2U4ZjZiODJiNDk0NmVmMWMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzFmNGZlMTk1ZTExM2U3MTlmYjFjMDc3YiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfXtz3MiR51dByH94He4m8X5QEY7QaDT2rDUjnUh748KcoApAgQ2rG-gD0NRwRhOx3-HuE-4nucysBwrNbpAi5TnfujbWMSLZXShkZWX-8lG_-vkZ64a6YsVwVZfPzp5tt1dp5Be5VwRZleSFFyaZm3H4sXi2eJa35e1VWV_zfoDP9ivmR_EZ84I4L-Bf3I-TPGZxGLpuXrhlXuVhlBSVWxZV7MdBCn_MMi-t4tBlURDl8P9e4sG4Zd0X7Q3vbp-d_Yw_DFcDu4YnrNmAj1rAP3K-hl_8lXd1VbN8zZ2O39R93TbOCj7fdrdOfuu87dq22na87-E7W1Z8YNccX2ry6679O4fX3XU44GoYtv3Z6el1Pax2-UnRbk6LFW82dXM9sOY6DdzTybc7_r92Nfz7atfz7qpom543IIuh2_FfFs9WnKEQqyqMozLAN8PfXPEb-hAIl1_5RVjlSRVwEEOe-nmYhTGvPJTutu0GfLWrdd1wmLlakfWVV4UV97KIe17AEy-rYH3cJMnF68jZXRVs2-_W8MI-zrNou7J_dva3n5_Jx__8DFa57Xr8l_gzL69yEPnfnsHDmuGsaEv-47Mf4D2UTsDjy7boT9--enf-5vsXr6_-9Ob84tXXVy_ffH_x7s3rq7evX3z_6urdmxdff_fi7cmmfLb4LHViw9DV-W6AVbzKWV_3qFR8XV2xHqQ7cBpvN6zaDuf8oW5wyP62H_gG_tKwDS6uOfcFfL1HpXh21uzWa3iTYgWryIUc8nVbfIBvgCq6Gctj-Dgs4MB_xPd8y7u-bdja-VML45fOS_hL166dt2vWcOfFertizruW4ZTkRFhZ0gy3qIn8I_zmN85DR9mwLXxzuN3iG6COgL49-2VhzDFnVerR-F92jn9wzgc27PozBzRn2_YwTL3ZrvkGpMhwJRx8Xgcr6FRt54jvnTgXsMucccpb1rHpfP3YDUqXTeb7NS9oi87K7DeO8bEZiTA3y1kUBZ_9hNEoOP2q3a1LB77Lm9IZVhxeFl8ehdnDA9d82YAiOfBIkHJhTunOG4dxFgSVG3_2fC7gsYzWCv6G0-I9iHnLGc4CN2bTgzkpaC1Yg79aiu86bTUznyrxkyrke1rdtSUM5bS7Ad6U37MQdz89tx5eBc-L3cc-7_379_ily-bNx4Z3v-0d2sgOvHQJHylAny8bx1n-AdUTDKOTt7sGxnDgjyU3FgZ3_lQVue8nYG8eOzFcn638eL8rCs7L3vkITgEVpgeVWdcw0d5pczBSNxxmzJ1y15FTmtshCfrHYjqtrxjYO7D2tNDXZBTmFujAx2dWCB1xFIfFo5_4yXnRcebAf25YvaYXbNqP8LO0P0KLYRDn02Xzablc6v_Bj4YsyKtNpha5SZlGsT-Z2jdd-xNIWYwKgGB7n74e_MKMQHjo-YHPgic89ZPzbSM-BWJ49eN2XRf1sL5FvYLtqf5iSAMl8aZBjapv2JxI0thLeRamk8ldsO6aDw7rilU9AGrZdffJ5PA3ZoSSxVHls6h4ynP1Xn57C966cc6__rNz6rwTVusv3-JGFv_3yfin86eLi7fnzu-dfmYz87hys9JnT5ndxetzB7zXwDuAdWRlASqi8S_5dt3eoudzeHNTd22D_z4xYOTchg5YmsRBGE6m9pI1bVOj99jzqqX0DP096_egAeaAQxmAkQnyLzirT9pDoymgfaIxwifnHY3E1vygEXjTzOl8VbhRBHh4z4eua4wFnB6wNm8Kfi98uPv5GQElfhyFSZI8_pmvWLHaF2QPAQvgBjCq4Mjg_2EgVJiBSwRFxvPtu8WMPmVukuWB7z1-Yp8Q212jZZJfo6einaoHp-hgr3S0iAfWyXX-6z__z9xSBYGbJ4xPtV36AQyKIE4jlyLwej3cah25Z_keOsacCXP9xKt898vOjXDALgcL74BR78Q6b9ntGhA2DLthddM7IGTcGOgMEVF2rOkRrcwsc1HGVVSkX1iQLxA8nUrkVHQcINJQs3XvbNitQlACORV8oaA_PYffzEzWC4IiZeXUOXyNYKdew9QWAKVx6AWNtKmvhZTu27AP-P7MalcVhL9l4H65OeFKV3UHgl-JdTAcAziOEjZTjgrAwdHLMAHWfmAgy5MZ4bGqYq7vRl9uoq_oCxKdQtjAGgfDeFhuWOemrlB3AIUU2txT6N8vnI8QQh-faBSXpe_v-YxzXuxI_XB2hF6KWydn3T2LO_O1mTXNoyoBzP70GXzSQTF4JpGrUTg15yt2U0NMuw_PXurtMmcAYz_y3aKc-g2RjyqkbQDzf490Dn1-RixBxgrYguzxz_zkXKBSVGxTg_IaMqG80V1RKL8OOgKSn5NHUfIMduFUu9--eelsOOsBkeHuuQ_sHPj4jDSiglVhkbuPfuIFYb6-vm6W8H4DhJ3mDCjIA1jYOf2KoYiuMSWJph22-pxFL1nEPBZGT5oXfr5sYRJNC756zeqNM7RqBNjlDn4cDVJfb3ZrsD283fVOPZehAPOTBpk7DXf-DBGcgfvg3er12pFpzfKe9br3y3NOuio5C_ac9ONnMwGl30OMLmA9_rpiICDaGQ1MAuBYv9tsBxP5zOm1V8SsZKn_heZ5IXIGq7ZGg122tL70LApBclZ84E25bPgONt5aJ7PR5PVza1uERRGn-8i5qpua3hT2dgmw5F7ofOALczmfIMGovXjCUwlVqTzmyswjgKdV2TinbcBaUc4FsystZojAq82hKh7HsA-rg0kf2EWoCQ_Mfo2fnguz3LQKAMY99nkXbcnMegW-PTOykZSBXEySksIcAejYF8MPC5Xifybh6BUgQCby5_QXlYznV1kQVVGUcuaWmJDKyiTNfJ6jVwPFpDFlFcKRVQjQXV582LZ1M1BRpaMnYXpd_YTZ9R-wfAFQ-dYYwSxpGINQseSR1Y6-rYYrULdr3gEgkEWVPvfOwsrNCy8pwiCDKKrKq4z7SZklsZcmzC9TNy2rPAlZCTAHCy9xnAZBllaeV7DIpUQUWnkqjojVOgvdX0DQPS22Hy_ddBl4F1525iVngft71z1z0ZZJiaMbiLzAz_IS9GT87c-_Vi2FFFPUOVasX6HSxbnHc5i7y9E10RhG6UPq7BeoWcjnpVXqlnnGg5IAi3jeWMaQz3tK_QHktyNQjrYd9stl8wen4R91thZm2vPnDgS7-550xSCoUubGLAjwjiIm_iPY3R7HG3Bj4vM4ONftbhAbswQzDw_YAw_4A8iNRh_tVEMJY8pm04iYHeAYjK9lZrtHzw4bVMSMHzEuJ1_Qsw2fgo6D4YUUN48LnkS-F8H20OIeqzBqee8rr8jRstjPMs6DOKB9RqMZFZfRwD26lEI6tSWdgo3b4uod9ANnJEqC-yAXCFw-9FuGQSv-erXbYMxDciYX2a75ZSND5Z94J2IpJW78PQL7gpJ-sr7QqfqCzOOLtTZncNlsdj1GWVwk-PHlSEEQTYxBNLxTsd6hZBeYBtCYfCGVdnHZ9Dt8RVGSFFNTy7uUXkP5it6B6A-xJyhT4wjzTVkk-Fx52Wjbz_d2y4yCJDyNojwMqqQM1ZIaRSuVS31CNcpYchLuZYPL5bCia_teKfuJ8625H1sIWCkLS0sLquBU6_p6hVFwj_vJGVj_ASJW0K-PoCG4BiRtWLecY-kGg161lOBVYHbCbBBEptL-EnQEPkGWQuvPjKDcrMiZy-IgTbShNKpp4056UH1MDhoXUZLBGG6Y6u1plMzkoE8rghVchsYym2OopPyazmeI5DfqcDFRVhqg3YoULqjATd0j_Pz7rrzmclbGbL6Sw4IzqAfUcxQ3rY3KXMl6-2VzjpWzHga780ov5SAdH7qa30iwB6E-YomFGBsmvQDdWIp6iraJctNcNiC3A0UDJXo_dbkLcq7c0fGNRUFD8R9b5jO2owTsoPo1GCHwF-UOi0Ko4Cr50tdrkgB8h4w9_mrAhDnbwgRuEOcJGWHvw1L_8rIhW7UF-0pLTa5xe4tGqGMfHQUOepV5RMdClnW00jNKD4bdj6I4rZKi1EIaS5Sj0j-s5qhGdQFZZmWalW6iRjXKkHLUp9UV_zgKv-ew1UGle0cU2YSzGbO1CkosAMxWvLgt4Em8uYa3WTgCri6c645tV9pm01sq2yztiYgx35rugFw1_AICzd7BLQlqPtoaobaUJG6pAiD2Bs0e0RaoDK0oCGCLy7ukHfBHTNK3G9B-NeT7jle90X90-gHEtOawNd9joCuVkWbVLXuwCELlRE4QVmYhEtKMXgG0DoPN3XYh7bicm2i8EpN7KXUeq5xLeC7uYPr0um23-G2q2Tmyyqez3fiFFxNfK0p7Ygs5u57mWXXt5g4Sosd-S-m3AaP3l2y9xpfZQSBQoypgyxJsl458JBkrvc45h_ADPGYLETR89VzIAV_9Br45ggRm5sYxbCjqLabGcceKim1J6w-D4jzN7LlKignrVNySHpBYlmIOAr0h9l6oBcSgaAnPXfYf2VYBkjXoEUzqPf9xS_-6ws3zXsRWKL7_0LrzEdcR_gcGf6BHKgu9Eda7MGaDCJnT8m12Ej0LJaPYirLMMPZrminOzswu6DhPGZKpX6DqtvzIQqcpIJyVBmmQugYGv5ZepKrITkyHOZRqUXY6KdM0L5O4yrUJMhoDRhP00Dq_HDd3Ay8N08pNqa2OxjVK_9oIPaWSb0JTrZYmOv3kfAfGoQZ4JH-94Zsc9j56y2uAfD8xuSnr5qYe1A-wZmvauLiwYIQwygVf9O6rFy_Fyp7L_aPKizDhAyj3dApxcXuSg0FsJXHWhpztmoN17xfOiLPQWNyg3lToEGkiL3rAU8t-uMXNofCb1rVXCooIiGLiYmlo1uLT2gRLm3uqzCyGQr3YKEJ2EmCCqefwo9D5hpMl2LDuAx8gjMC5ft_SwJgO6AXyhk-Y4hWbSVtN8Vw5bQhcOsI8Sv1xQ2N_5MIRHa5ySncg1-gVeiPdiBsLsyWoOu2ug8-paLVfjHkt4aapALfZDkK8Sp9ADBANoXsXK01BlEJwKlBVdSdhvBQeUQ-XSgcI_RoFAzh-rYOSDf1l_L5EIgWEOoBlO-evb186omVWKeDLdbsrnfPXL5TEZAhkNHlsYaHB80lnIqy-dgswnQvYpOdFV29BL_7YLpzvXr6loasOHKgIFkq2hZWAhQUb_-OsvciiNCsKt6qqSAc0RtfMaC8e3AOjDFHoJllRZm7MKjWw0Razj9Uf1-QiIIH0WaOPGT97AyPPpWIINu9ZHe3NVLlY6L34qI5ZxyL1CI3KGkYZwP904sP3hAgCLYmP0iYVmOVPZNpeSMgq_mxgDmw42fNkygEucR2k_zsoOhDHV0e9Diq8FMj5_3hdU8aY0soErcbdiA6S8Nq0aqvifPw-6sASjO4H2uOyF4ivQVK9tF8iSqhxoxl7X8lYxGVgI9bicQfdIGEoRnqu6rwHX_r3SwiM-FHTRONI63RPEJTnfhK54PGKVOu00UylgqAntEaJGojpfWBORufCTyBAAU4kAH4OqrETGtnwgXY_vRgJaI0OtBZJgn5XgeTQdc0EMDFPIHCPPYipdYBttGSN1uCxHVXyORXPYpakRZFT9CgCpbHJSqOJp_RIgY_CAHetwRqKUVp-A2UDVACsOwYg426GzVeXhqrpaKfaNdpVvVUVRBk1OSVoKOgurAXHSgtssaX0XQLc7mSLiJwJ_kgT1mBVR0oT_C9cT9-ub0ADcFm5RFfOe229rury_XMdGeVtWcNnC9bQ8hNahie3lBEbLR64N_YB3wktOigtBoG3YJoA0ODmVBE47knc8NLl0eeGsfxPoSahZG08738NlLmIRcgmtGveP8fsHDUogL9d8xt8iEzFyE-Ra4AfahXfSP2mbQACpYhIyQD1e4NG2Fwqneuij4pjEfhmOJ1Wpoz06BKOUdfKGFFRt5oYbUWdaWN3iGpmEhYFUQnIZyk-q363aWHG-HljHVQvmgqi9YfV7h_h6Oig5OLVIOlr6uowrTqgJmYEwHL-Vc07CYakPe8528BIfxa7hYCjeCjF0bhMXbu7XqHc3pMk8IsQLeNTOzCl_Pk0m4uPlLGNbunC2LPF0yeoDqXW_q0RuCtNQ4DFCrUgYtMQ0pTTFoaAnJXMUEhvBXuV5QC9Mf_5Hy9eg5TLIy5sIZDe1KmK1104u6aGlRCre2p6WpG2hddRKFZ4I7TvlANAHfumxpqI9IykTIvDftL5uKrJ91EChErqoxuTSyLDeD0BXKNbWBt4cTlJfA142yP45bmQJfoK2NyN2HDgRACMsrXMtKjcDPjXglav42iSKlZDpF6sqZYEBpQPOruAKcZbsJUVxkl3E3RGGk_k6g7F-6-m8bXMTPSikICpBmrDUrDGQQ_yHOVKGT4COeqVmJiPSDLI1zDN8l6aUGQOJolCqVUKFhB2L3GSpOY6VDFQyuJYWNPxggMsRysmTD7ZQNI7douuZmJjxKErCiRv2hqcErwQrsDdipqo7YylOgRgGPQ4H0EXQP7Kh7zQrwT7AqPYZs9yiFBwtB_YyLiXd95LOi8cWW8pucxJk_GWjrisTUcoUnlT-IqNu-RbWxQ5PKoXQaxuxJwLTvIoybzcj3k2BidGe7NZjntQu7Ic1mNBGoRxVgWJhnFGB7Mc9ikdybBiEK6XoMYVpVkum6r-ER2sVJQ1Z8oBrlUiaUk2s6TNXK3Bn4oU31y6OXOjnDGfxUzn5I2GZ42intbATPVFDDuxWtyJmrWwM6KPVyR1aJuwTibzqACAnzlWhmZFwSFEhV3dtErhC7ZV-TWqMKPlwVl4NItjTT2fDCx6POxYTF0X6ObQFu1arAY6LBUyo6UQlVdRO9GuZwzVxYrhIdpeW8-225DJu6GMSg8ooB8dJ-m_6WzJ-wCIpC1mIkuV_ab39um9p05KZS6k95Oer4eQb8MWowNBNSN3Zn59MbVhpmuTJ1tVNvvUbKIVqRjxuoYdH1QgBw6Gy4q7RpvaHSwQgmFIjtZIOljMPZNZXt9KZ0_1R7Fg9OaB0DsVuGvgNW3hNjFz3rYDOuftQjU26WTAYi99N2aiF1J3VdUClIKkdyry1oMuMPfTLLjArAa-VYByHFsJAt4BdWOag4Mvw74Qb0cuSWDyid_GoKScpM3RJWuPjFIKSUoyTaRyWTjd_VKCypgsKZE-1KrAURfjvl2ogTADo7-5IDgIkXePwgKX7_CuI7-3rrGmAuLZlTXG0tfSshkxLu6L-nrXqdz3xcdWPUTlUOU2kaHXCBIPbSmwt7LvQSVgUQgRCWEi3kkinqOVwxZdWZmhT6B5XagdvtxLmU6yD_ApsNXNcgPOABMQ00SE6o3QBZ9u14AmfkCd0JEwOFmBQzFqk9UbtKTwNJohhZdCA8hijgge9sfNeDZfQa1hdSeBSZKISRIHWnEFSIbnrWV7AKAOsZUU5gG7UNUkLN7BpEnFqd2ADZTNhofC2ikAqMvPYyac6r7ykSov28vADXeguT5yS6lStiH-HTYaydIw6kDX8UI1f6CZkSXeJdmaxX7nhOgfEPBYHcWfRReMB1GYpqnLfe0-jRM5I7p4wmka3VcUZ0lZeSxi_uip9QEbs3r-yMMxyi-eyNmKBh4j6mZl2U_KmhroSfnjf-EJ6OHGBiHsFpFWaTG1qQ1FbwrPjbGl7P1Ro8roXPl7AEIYdP_7-ZvvzeCcFL9XqAk3gTQs08SLwtdqL1w2YqFVsCgTwT2Hmc6luSIe5G5U-FUW65U3jhDJ5XjK8R-23qFpH8s2_ULk8USL2hoM0Nh6cSLQuo4NTD-Cz1JOZD8xjIlRYTeUNi5RAoRRtMxIQ6iTGFbmr9Js0SypH0U51xoTjULHRlCrLLhhaihLI2CP8HAUPszIuvTy0A9Y6pV-oGRtnIAyMPzjTjCpfqMygzUNKubHOqNoHGoydthjDyUpsFVTbCqT3fv4llrSF0LlqSCFlUbqZZQJNpE-Q6ITWQoCl4EJvctGDC92zwSsSmGbp480riVrR7llWbVS5ug5qJvMjr-FV73uOIzvULEP-7jKJbjssU6ErXkqJ2_mQuU5KHrmZSMh9z50JMi6By7H9IhO-omtO6MpYVkksZ-yMEti3d01HvdSYdkTjmtJsKjqLtKU4tyF1R0DY8OeLaRbVik2GfFTCx7_UYR5l42xZYX5UXWFXm32aUrgBBACQQsNJXDKonaDCwDSBqmIToCFKtAQzEeIosqmOaAFbOLQScPxF9oCXDaGCZC9OBLBG704Cl2QFyh0PnQKNOZi0dTz_CL0fDfW_QHGEbhxm3_eWTblP9M8BZsRptzXnbTG8TYd6T7lnJpR8KUSORrAVX29WnIcc3t7t8xI6Z-eMmwt-QARllERjzk9xvA4_4UCtk7DNlQHXgOkQhsAKssHhnlL1SszxhwqGJGZHbMSSaF8Q-RMpaiUP5dpMyOdPjrnXiS6KajVc3-Oi7-qc_CxsqlHZnIqBe8ONPfQVC6MsEJKWRZkQX8IWRgB8vMxaaUS9FgeU7UxVVuBh35kCNiogolQcbdWjUxfg3gcLKJuxtd_heFBoTEMAJqflOcVO2MJO2otHe26ponAqyPWVbuTZIJxi_gehTXPZRYMjPV6LVJsp7LT2IGItsXM-Ch0tTKljDAQiTgGXDLbrBWc0_m1SWZ5Ym0kkF3I96EaA4KGMT-uII_Zq0WwHFsYVeeDxI1SiO90S5qDBWB4G-E1VMpcVpHNwAfXD6076TTlH4W9Ug5RZQfq9RgkOnVlWMrWqMyqriz6vBBcjnlLeEAt8-KUv4StozKuSIzm4MqCUIZ6w1G9Fg7tSxV9brGxwgzUdYgKO6vvQY9hwXiFb0DViobLSha64tk2qqxy3ajMMh7qzKNxWHU0Zw88fKrqnnkU5XmWFkmuXZxxHlXbsaecL500pxmVRglfZB6tVx7UwcEBTlKuS6NGOijRq2w5BdIkVayICxshEptmuVTG6VLfyCx-cs4RR5i6_oHfyshNhB8ztYnnjsqQmUUJSp41LR1SMXJG0wLDSwhCuThbYBYReueW7AKF4lQVo_YukSpTHWeHCgqGDSYJH40NFComkI4uYWw_xmQCvY9OOIFVG-5A_l7m2dkUPejWOeyOaXVD4btjmaJ6s-FlLbvZhKulYWUEJaG-kV-Q7hBRx9jA6nzDKCEpNxGFvtUgonysKTbYjCC2FFepPiPNT77I2TUSaAhFMloc5TPbvl9KWVL6WGYNDrUPywZ3dNeiv1wY8pJys8WYk2DXGC2LI0RGsftuI6fEkxKF9ZSOkZZOJX0kAIe1pKjb3DG4TKJr5wCWUg0ZjFId85WOOErD3C1zPwzGiFQfBjeOSzzodLccNeBuGCaZ5-ZuqkHZeODbCIoee4Ibd4vA4ep8i4jJjQMupHUHz7egcAhGy_QzCHhAx1Sj91OeHKA1PpCqtrvGSBHCqmB7BnoHuYV0wqhfjDp4Klw6uggI15QhUorUT3JKesP3pHy6_0OooJIDofN-7yjGhn2QBR05DYdavWUXtBiJT0538B6MNPzyslGZwhl4ncLurtKwCnmozwEaR-SNlXzsmfelODI0pu7FwSNYn0oEsPA-oLQbnYjaYHBJ250Mwr52GAkg2OhgvhdiwGUtSqKTpte61zmTcq-wxsq_w85tBn2u5AHSytMqDXhV8qAYDx-NB_fH3fSYs_cq4KkqCHVcWJBQJxyM4_iHWpg-90S96eS_xdPgRvvaqZAlpnJV9lYV-mKZ8dWVa7mpVWGRam7XsgtY9_lKsD3mQ9Bl1aXMFZUtuQv1iFA-QiYTMImBu1b4ZqPfAszyB-F9QNMphwXon56vRl_24J4RQeG-4YQvxEy-okoUGqbBjBRg26Kba8e5RBQPFN3tlhI6DDGTKGOJTtq2Ad-yGQHuc6cijIH6RlgGPawWEiJiUD6Kl290A9Abmb-WbpG2drnrRpkHKBBZG9AfE6GGwtaiW8vIE6gI77n0omRIltJrl2N_wvQ4ie6x1lUxvVAAS2gripAXRLir1wPst2PHNiaYAbNiz5033379UgAho-N7fJREDSKvNOfP_JzlicvLLIr1MQSDBGK0V4_mcRDB-lLUU9FQXTYw3K3IZeVcNSqUGrrI2hPCITLdovdULfskD1jggRnyZKy8nbEzWcVYFlZVmeTJ2J-gSSTM_oSHcUIo6XHX9wuvKqpwzISNNBFmueCRrA8YxpFBocCZsvz7R4PBfe646rnDFsnRJB-tpyJKb7GrWta5wPNgRur-o5UK7OE5c9GWJ0tiYqAFroU82Uhdg_I8o85kKW8jvgufqSEWl98du6Ao4ujBeVPzkvLGsh9INe_LMNg8fT16NYFUjPwmBO_DZSPLgifO963GA6hng2p_ka1g-DUwfjIVqOtvGE7pjAMIHuSHSSdaHcwRdai1IMvxyMOKa3M-o5-BV3rcc5PMjVyNKkdSj7uHcGdpOlSatipSQCFxwQtdyzKYO5RyPoGLg-8dbUevguls44zA5Pycyk5OW1Q-0ll6xGX7RACMYKWAr0yflpQlTzooT7vqt_q49Wg6Rdq3FosqKgnSByKM0zYEwNBWlgFu0QM4gzJTIg6ZnkSiQoAEWrqNnj6MOLbUXbd47mnLW_yPOLYtu-QGdFd0ZkcdiFrVeEhOxatYxZMRpzj3JkP2XjRuEkg81Vt0TAJMCulmNh8xucw5SI-gm1nuaOMPv6DuHKBLBz83HCZLJwJ2jCqO_HWOaF2wyfN-HJpOip0B1gGAWi6RgP6fno6d3ugpbOyfTcq7aUtqZZ0jcfp8Utu7o97hov1cgs6HTNSPM9_18-zLU1d-9_KtrKELeza22NzpH5MOWWy2OYbSp1B4HZUG7APa1kfV4u4Akqrou1adMKDW4vMBQNCGLAAdU0YJdLzinXDn8q1Fg-qoWLK7-QPnW0pUo03WHxbxwO5aNi6rIhqYjiPadnSuL7CnAWa0pNbBtUQm1CqkmQaq0fqrPkPTuZwc08b5h-KYJB-UB3gbek16MZGDldlukAp-UiDPpaqhl1q9MXY4Oaa7e5ooH_9Nx_lPMtWADx9VcGzlaljXQUwztC2myahHf6GgF9V8CIiqrrVxG4ye4eSYjh4Vy9eoFL08CcB0Js48RSOPI0qhSOiN_BxgNjC0FXwNYr79WJFE3hbqTBdB5hgxSoXCyf5g7J6fn31c3UpNHhVZdp6hyCZaOxxF0SKvMejs2NjhtEL4qkqjIu8h0QSFerJPFGwd_Ge591rguVEXqfW3_oDATggKGa4ezDjG0sStvCJPgsL3vTxwozJGnKeXw6QSM2m0THqxn63rsK7joOt4OL_dPr-btxgHPgt_OUzldh-v3Rchr8uiMncLn5dlkkR5GvhFUeWR74eu57mch3Hlu7EfZnnoJ7lbgSxdHia-D8F8xDy_fMjLHSCyC8MzNzpAZBclVYC71RLZWSI7S2RniewskZ0lsrNEdpbIzhLZWSI7S2Rniewskd2vRGSXhVEAdowlqZ9ZIjtLZGeJ7P5RRHaLIxR2C70lPqPCcJf2jsmywjHaO5ql4pkR5Ya_fPv_hgsvcbkXFmkSeJX3aC48-PedUoflx7P8eJYfz_LjWX48y49n-fEsP57lx7P8eJYfz_LjWX48cQzIzyI38hIWx5Yfz_LjWX68f3l-vMWd8oR4A93LOeabHk2ZdyihJVtEvyifnnwT_BQ-4hGces_pi-L0NkYJE3is_T-8_8qS7VmyPUu2Z8n2LNnePzXZXpBHQVFGfpSWxdjVqVuaDdV_bDvytHGC5nTZiEY0M7QVqUXs7pJHi1UD_B2aPXFW4cxAt5dNWffCxi_uFtj6XS73waSYOJq__SY6oQqiuCe9jrBiy556TY9VGAkoy9MHbXMii6QgN5PsTSM6PDJstOyMpBOao2o_YBTvoI7m6WDf3Pm03lgdUeRRqIRUCNFO0DyyYTkYLQej5WC0HIyWg9FyMFoORsvBaDkYLQej5WC0HIyWg9FyMFoORsvB-N-OgzEv3NANkgggQvHfh4PxG0qOjCUdfY23Qb74V6nN2sYeZNR4iZRBC-flmkGATD_BD7sOdgxpv-ju3iOoeK55-Hb1ujQK-JLiUZFuWL5Iyxdp-SItX6Tli7R8kZYv0vJF_qvxRZ6_ev0NsfR8-_0ffyVaSJrZSAu5a_DsYvNASkiD3GckizrHzAi6Ajq5pzffHEuUucP12CORz5PGvsNwxUJeRlXsfd7Adwm4_nZ6-sOZ8xvn39r8rDe-voQgo_gAO7sbfjczjSjz_CqMyj2mMb19VUfY3BTIqx_6xoxc3SQtAzDIT3nuBfEP4uEUwkIi8qNmyfXt2Ib7t_cnJxClI7HAyS3brN__8G_wizmRlAkrvDx86tTe0TOdrwBbE38XQoL-0Kk6VcnLsSix285MLQ_DPEu9-ClTe__-fb9CmKO0a6nVBpzRcqmT9qc3rDvFnwwmhhnOOq9MMzzE_lSxYepPnWUYRAGWkNqd-phwRTommNtrI6GTOTVND_XwXWu0oI8jfbvXKf4Aer5DW8LoQ3_S2HfJ9A6xCT5i4LucggYSNwV7AOE_fLYGgBrHvIvK7hnwMEus4SmOsn3CtmUbmWzTPe8y96ar_qalda53gBdOjrmNow_6y5byi47s1QFQi8WErqZFWU_OD04eJ4Joad1U2kF0e4hXPjnmaA7TrmrW1xG1LXVPfy-SmyfHnMbhIZFWgrJ4FSaoaf8iEEN9qJuqYyJ9u-sAGIrytOZ_ED2dlIU9OeYwDj_za0U7YPTZgDW97ljJNYPKknIzumX85JjhP_yItyK9IHuQDaupB1TW6-SY2b5v7jJRok-rKesmJIPFbVFxOsRla5i5Ge0mUgHxCnvtRSIzahxgm-qdZi44OWa2jj71pUBtej9pmuCPquuyHScjcv_X-rz4RnaTjgnzz2c2xr5tdeymzfFE0sBNjsSDR1EEOeLd43qqx2mva77m--sxWsc5bmEsbdPEqAtht8F2FcFwY5qDyVIAkjg5ZjSPPupcJi16GfaII11bUKOaXrjmsm1B9ZJJ04LV7rGtbKQOE0nVIwzFL1vsfxK5A8x24jf3EjRKGTRX8Whe1QSX3a45YGtF4x6Gs6PJMoM8te0X-kix7PU7unA6K3nyWWTFUZwFYVplZeUViZuXnEE4lAb8GFmxpkq9n6zYBjU2qLFBjQ1qbFBjgxojqHk4W_4-xXdsUnynvxxm8P5V-MsDrwpYzOI4y6rUBX_J0qjKEx77XlBgy0EawIxc5hUR8_MgzEMe5XEaZX4QpcnDXs7gL8-WrnfhxmdedBbEB_jLfc7LxE3Te_jLn5YVvUtT7iZ-GIO7zD0ez9GUH3efM6xcgEGSiMVZUTyIkvxhgecYAMjM_1gxAIgnKL_5CC6HVsIzhxLyZtiHcO9WlTbUaPLEzR-Ml1yKwRCWU3yrj7qyKRmNUUEw22Kx0IsDnr9-oY7YS_gq9nFFbKFzVNIhr6o0jUE7dYHHwDhSjo9EK6q1nVU8cD26gEB3UY0AxqycPhCOqNJpmodZyuOyyPTABkIxSqePxRvGL36HjoscsOhlUIVq7Abqeo6kqj_e6hPVgnqeobWWnK-XDT1CKMyp4bxPxaMO_OF3eMiBEgzij72OJC4bpYS_7dHRYpkbJDYsxrhadHFIpkORfNCMjZiqUI1jHBlJLpvGZBeeFno1kaDIZBilL1FcF6feRUrjsqHuAeGj5pi5gyBN3SzhpTsyhI4Izli6x-Kxnk5yL4euvr7G0y10zhNkQjxW-hXkIUwjXkRMI4uAZYudnjuZxTIPN51cNqL9wgzP0KzQqSVRXpcT71d8vZZHYHQVXtV0ZYUQLM7ZTDdW7CUZ2NsqqHQ3lgEpRwbCxwPEkzJ3Li-RVm5M9CyXI-1xXY7TPdNhrvjGUqRSluPhH1GFo9_eQzrHQy9NC_B7xdj8YCBSQw0eiy9VvqkVR9AEDWDeDit92mKY2oe9g_vqTNSJ85XoLcH6PO6lthEbcWzn14dA95km5EkAlefCMwEddkWbJwRvuNAUUFO5qYy2A8rgDOOhZ9CsbVuL_hWk-xAN2vntpPXqV7thIvcjP82yLK7GJoG7N0xcrI45W3nVRP95d02g5MEYfuaVEs6RGyUmp8DnrpQAo_mQOySoam4vkbCXSNhLJOwlEvYSCXuJhL1Ewl4iYS-RsJdI2Esk7CUS9hIJe4mEvUTCXiJhL5Gwl0jYSyTsJRL2Egl7iYS9RMJeImEvkbCXSHzeJRJ4sXtQxX5QBfnsJRLH-8ZmKEHDlMV5CGs7soDcvUriXHSyu__1n_87otsjBAPJocsjpMSEbZH8V-ruCLHdLxu8PWJq2mauj9CEHcqKTml4LhsDoZgFNNgoq3qLkRFHzIcMitQqPwP8vMzP0yBicZHn__j7KN5-gesnRkpKfDVpQGXHuwmoTWp0ex2FvY7CXkdhr6Ow11HY6yjsdRT2Ogp7HYW9jsJeR2Gvo7DXUdjrKOx1FPY6Cnsdhb2Owl5HYa-jsNdR2Oso7HUU9joKex2FvY7CXkdhr6Ow11HY6yjsdRT2Ogp7HcX_79dRFHmVhSC-MA_K-eso9nKlNfYw1oMiy5nhdrS3VNhbKr7oLRVJUiU-EoPxkSDlAbdUYA8YYhN5PYXRZ3b0dgqyY81lM1XuBxDKUhkAbJc4naSwJWblJ-wNM_dUGIQ_d2-qWICLHabEQLjA_YSfZtqOoxp9ZWuuphTtDU5RebJCTIcirAmV1Uw72eLOPRgIE4gdaO8mjBcPY2MVN3ywsjSvvRDFckmJevDaC1ie6x3oIDyW92NWHON2mRNHy3DkTgxE14euxNBVmX_yCzB-pbsvjKM6V6jh_T_iCowiAMQP_3sKT-VRGjNRCMWTr5i7nGdedfEgXxRN5vFGMWRItKMGmqdf_Y0z8705Ela3gjjFL588hQvduDCmVNARd7BHdLyxMJIixmGMGRFhmJxEe3Snj52f_iD5Ly5o1432DZGHFjTiG9CEUjZlPowu31jNed5yPBJFPGHT5tC9l5n21Z0cW7XDj1Ls1aUkXycA_2bLm3e4HJ3z4u23lG3V1R8N7BuIM-Tn8UgHeKT17vookdWxtTrGCM9lXxfVD6mTZWyi0q3JVGbSYlDluSPU2V_rGpI-80c21njZIyLVFvwjBydKgbZxLlTP6_M4rv0irPKkCnhaxXnq52EWApLwimMc15pO836Oa2u1rNV6otV6OCH7PmVs-MthEthfhQKXe6GXMbfibub7VcKqLGNFxXhasDx0vcQvmV_gG8SsCNIAgGcIMbqXFVmZsYqwxqH3mbLe-he-e-YlZ152gPW2qsI4KgPPst5a1lvLemtZby3rrWW9tay3_8Kst1kM2KIqWOyVY-5xBOj3Wf0HwG1dgUjy0qv8pCqCkblMI3Bt-j8XSqsWbAAiZeBycNujAxjRtaE-j4XJDdv2K9gR6ljlZTOGZlKdnPdv3r76_t2bv1y8encFoenVn1_9z_eq1ku6Z6SFHNh8oiullvqjsIdauoUsRMHf35v-iNKyC3mIrVXJ9704-7I550JTjEjYnN93b75-9fq9GRxzzej2XG4FiYEmV_uS0X2PFo7Vp9fbYRmdhEvUXpjXx1VdrAgtrXtxuxPbaj4t1VM4lwkvizyLwbxlIwOsEYOY_LuPDCYmvcHibK28CZm8oHkOZOxkMA6zi3LLfifTpOfp-WUDIXdvkMLoVqT24NF6oWrj1VqWotpSVFuKaktRbSmqLUW1pai2FNWWotpSVFuKaktRbSmqLUW1pai2FNWWotpSVFuKaktRbSmqLUW1pai2FNWWotpSVFuKaktRbSmqLUW1pai2FNWWotpSVFuKaktRbSmqLUW1pai2FNWWotpSVFuKaktRbSmqLUW1pai2FNWWotpSVFuKaktRbSmqLUW1pai2FNWWotpSVFuKaktRbSmqLUW1pai2FNWWotpSVFuKaktR_S9FUf3DL_8Xo2Yjfg)
