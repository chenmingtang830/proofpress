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
proofpress hosted --database /var/data/proofpress.db \
  bootstrap --workspace-id workspace:personal \
  --owner-principal human:owner
```

[//]: # (ob:e7064049)
`proofpress-self-hosted` remains a deprecated 0.6 compatibility alias. New
deployment instructions and automation should use the canonical
`proofpress hosted` command.

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

### Workspace review policy and provider credentials

The owner configures LM review in **Admin → Judge & policy**. Proofpress supports OpenRouter, OpenAI, Anthropic, and a public HTTPS OpenAI-compatible endpoint. A model identifier and matching provider API key are required; customers bring the key through the owner UI and do not need access to the Render dashboard.

Set `PROOFPRESS_SECRET_ENCRYPTION_KEY` on the deployment to a Fernet key before accepting workspace credentials. The browser can replace or remove a key but can never read it back. Policy versions contain provider, model, bounded criteria, automatic/manual mode, and consent—not the key. OpenRouter workspaces may require Zero Data Retention routing.

The first-run form recommends automatic LM review with current supporting advice required. Nothing is activated until the owner reviews and saves the configuration. Deterministic checks always run first; failures become blocked candidates and are excluded from human review and model processing. A supporting LM recommendation is still advisory: human approval remains the only admission authority.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzg1MmNiMWMzOWY3YmMxNDc5MDllMWMzYyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjI5YjMyZjc1IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9kODEzYzU3OWExMjhmMDE0YjQzMTE0MjciLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzFmNGZlMTk1ZTExM2U3MTlmYjFjMDc3YiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfety3MiR7qsg5B9eh7tJ3C9UhCM0ksbWWjPSkWRvnDAnyAJQYGPVDfQB0NRwRhOx73DOE-6TnMysCwrNbpAi5VnvujbWMSIJFOqSlfnlpb76-QnrhrpixXBRl0_Onmy3F2nkF7lXBFmV5IUXJpmbcfixeLJ4krflzUVZX_F-gGf7FfOj-KxI8jIJwzj20iIMy5B7blFWYZn6CYdXsyoLEuZxaDDKgjxz04hXWc7KMA2LMEt9aLes-6K95t3Nk7Of8YfhYmBX8IU1G_BTC_hHztfwi7_yrq5qlq-50_Hruq_bxlnB82134-Q3ztuubattx_se3tmy4iO74jioya-79t85DHfXYYOrYdj2Z6enV_Ww2uUnRbs5LVa82dTN1cCaqzRwTydvd_z_7Gr498Wu591F0TY9b2Auhm7Hf1k8WXGGk-hneeBXSfRE_OaCX9NDMLn8oky9oIiSjHl-WrlemIeB54V-gj1ruwGHdrGuGw49VyuyvvCqsOJeFnHPC3jiZRWsj5skuRiO7N1Fwbb9bg0D9rGfRduV_ZOzv_38RH7-5yewym3X47_En3l5kcOU_-0JfKwZzoq25D8--QHGoWQCPl-2RX_69uW792--f_b64k9v3n94-eLi-ZvvP7x78_ri7etn37-8ePfm2Yvvnr092ZRPFl8kTmwYujrfDbCKFznr6x6Fiq-rC9bD7A6c2tsNq7bDPn-sG2yyv-kHvoG_NGyDi2v2fQGv9ygUT86a3XoNIylWsIpczEO-bouPuDxx4GYsj-FxWMCB_4jjfMu7vm3Y2vlTC-2XznP4S9eunbdr1nDn2Xq7Ys67lmGXZEdYWVIPtyiJ_BP85jfOfVvZsC28OdxscQQoIyBvT35ZGH3MWZV61P7X7eMfnPcDG3b9mQOSs217aKbebNd8A7PIcCUc_F4HK-hUbeeI906cD7DLnLHLW9axaX_92A1Kl036-4IXtEVn5-w3jvHYzIwwF5RGFAVf_IVRKTj9qt2tSwfe5U3pDCsOg8XB42T28ME1XzYgSA58Ema5MLt0a8RhnAVB5cZf3J8P8FlGawV_w27xHqZ5yxn2Ajdm04M6KWgtWIO_Wop3nbaa6U-V-EkV8j2p7toSmnLa3QAj5XcsxO2n59bDq-B7sfvQ711eXuJL582bTw3vfts7tJEdGHQJjxQgz-eN4yz_gOIJitHJ210DbTjwx5IbC4M7fyqK3PcT0DcP7Riuz1Y-3u-KgvOydz6BUUCB6UFk1jV0tHfaHJTUNYcec6fcdWSU5nZIwv04Kabd-oaBvgNtTwt9RUphboEOPD6zQnEYulEcFg_-4mfnWceZA_-5ZvWaBti0n-BnqX-EFEMjzufz5vNyudT_gx-NuSCrNula5CZlGsX-pGvfdu1PMMuiVQAE27vk9eALMxPCQ88PfBY84qufnVeNeAqm4eWP23Vd1MP6BuUKtqf6izEbOBNvGpSo-prNTUkK-IlnYTrp3AfWXfHBYV2xqgdALbvurjk5_MbMpGRxVPksKh7zXb2X396AtW6c9y_-7Jw674TW-ssr3Mji_z4b_3T-9OHD2_fO751-ZjPzuHKz0meP6d2H1-8dsF4D7wDWkZYFqIjKv-TbdXuDls_hzXXdtQ3--8SAkXMbOmBpEgdhOOnac9a0TY3WY8-qltIy9Hes370amAMOZQBKJsi_Yq8-awuNqoD2icYIn5131BJb84NK4E0zJ_NV4UZRWOV7NnRdoy_g9IC1eVPwO-HD7ednJijx4yhMkuTh33zJitX-RPbgsABuAKUKhgz-HxpCgRm4RFCkPN--W8zIU-Ym6Dd4D-_YZ8R2V6iZ5Gv0VdRT9eAUHeyVjhbxwDq5zn_-x_-bW6ogcPOE8am0SzuAThH4aWRSBF6vhxstI3cs333bmFNhrp94le9-3b4RDtjloOEdUOqdWOctu1kDwoZmN6xuegcmGTcGGkNElB1rekQrM8tclHEVFelXnshnCJ5OJXIqOg4QaajZunc27EYhKIGcCr5Q0J--w69nOusFQZGycmocXiDYqdfQtQVAaWx6QS1t6isxS3dt2Hu8P7PaVQXubxm4X69PuNJV3cHEr8Q6GIYBDEcJmylHAeBg6KWbAGs_MJjLk5nJY1XFXN-Nvl5HX9ILEp2C28AaB914WG5Y56auUHYAhRRa3ZPr3y-cT-BCH-9oFJel7-_ZjPe82JH4Ye8IvRQ3Ts66OxZ35rWZNc2jKgHM_vgefNZOMVgmEatRODXnK3Zdg0-7D8-e6-0ypwBjP_LdopzaDRGPKqRuAPV_x-wcen5mWoKMFbAF2cO_-dn5gEJRsU0NwmvMCcWNbk-FsusgIzDzc_NRlDyDXTiV7rdvnjsbznpAZLh77gI7Bx6fmY2oYFVY5O6Dv_iBMF9fXzVLGN8AbqfZA3LyABZ2Tr9iOEVXGJJE1Q5bfU6jlyxiHgujR_ULny9b6ETTgq1es3rjDK1qAXa5g4-jQurrzW4Nuoe3u96p5yIUoH7SIHOn7s6fwYMzcB-MrV6vHRnWLO9YrztfnjPSVclZsGekH96bCSj9Hnx0Aevx1xWDCaKd0UAnAI71u812MJHPnFx7RcxKlvpfqZ8fRMxg1daosMuW1pe-RS5IzoqPvCmXDd_BxlvrYDaqvH5ubYuwKOJ0HzlXdVPTSGFvlwBL7oTOB16Yi_kECXrtxSO-SqhKxTFXZhwBLK2KxjltA9qKYi4YXWkxQgRWbQ5V8TiGfVgdDPrALkJJuGf0a3x6zs1y0yoAGPfQ731oS2bmK3D0zIhGUgRyMQlKCnUEoGN_Gn5YqBD_EwlHLwABMhE_p7-oYDy_yIKoiqKUM7fEgFRWJmnm8xytGggmtSmzEI7MQoDs8uLjtq2bgZIqHX0Jw-vqJ4yu_4DpC4DKN0YLZkrDaISSJQ_MdvRtNVyAuF3xDgCBTKr0uXcWVm5eeEkRBhl4UVVeZdxPyiyJvTRhfpm6aVnlSchKgDlVnKdxnAZBllaeV7DIpUAUanlKjojVOgvdX2Cie1psP1666TLwPnjZmZecBe7vXffMRV0mZxzNQOQFfpaXICfjb3_-tXIpJJgiz7Fi_QqFLs49nkPfXY6midowUh9SZr9CzkJ-L61St8wzHpQEWMT3xjSG_N5j8g8wfzsC5ajbYb-cN39wGv5JR2uhpz1_6oCzu29JVwycKqVuzIQA78hj4j-C3u2xvQE3Jn6Pg3Hd7gaxMUtQ8_CBPfCAP8C8UeujnmooYEzRbGoRowMcnfG1jGz3aNlhgwqf8RP65WQLerbhU9Bx0L2Q083jgieR70WwPfR0j1kYtbx3pVdka1nsZxnnQRzQPqPWjIzLqOAenEohmdqSTMHGbXH1DtqBM5pKgvswL-C4fOy3DJ1W_PVqt0Gfh-aZTGS75ueNdJV_4p3wpdR04-8R2BcU9JP5hU7lF2QcX6y12YPzZrPr0cviIsCPgyMBQTQxOtEwpmK9w5ldYBhAY_KFFNrFedPvcIgiJSm6ppZ3Ka2GshW9A94fYk8QpsYR6puiSPBced5o3c_3dsuMgCQ8jaI8DKqkDNWSGkkrFUt9RDbKWHKa3PMGl8thRdf2vRL2E-eVuR9bcFgpCktLC6LgVOv6aoVecI_7yRlY_xE8VpCvTyAhuAY027BuOcfUDTq9ainBqkDvhNogiEyp_SXICDxBmkLLz8xEuVmRM5fFQZpoRWlk08addK_8mGw0xiQ_tOGGqd6eRspMNvq4JFjBpWssozmGSMrXdDxDBL9RhouJsFID7VaEcEEEruse4ee_78orLntl9OYb2SwYg3pAOcfpprVRkSuZbz9v3mPmrIfGbg3puWyk40NX82sJ9sDVRyyxEG1DpxcgG0uRT9E6UW6a8wbm7UDSQE29n7rchXmu3NHwjUlBQ_AfmuYztqME7CD6NSghsBflDpNCKOAq-NLXa5oBeIeUPf5qwIA520IHrhHniTnC2oel_uV5Q7pqC_qVlppM4_YGlVDHPjkKHPQq8oiGhTTrqKVnhB4Uux9FcVolRaknaUxRjkJ_v5yjatUFZJmVaVa6iWrVSEPKVh-XV_zjOPk9h60OIt07IskmjM0YrVVQYgFgtuLFTQFf4s0VjGbhCLi6cK46tl1pnU2jVLpZ6hPhY741zQGZavgFOJq9g1sSxHzUNUJsKUjcUgZA7A3qPaItEBlaUZiALS7vknbAHzFI325A-lWTlx2veqP-6PQjTNOaw9a8REdXCiP1qlv2oBGEyImYIKzMQgSkGQ0BpA6dzd12IfW47JsovBKdey5lHrOcS_gu7mB6et22W3ybcnaOzPLpaDe-8Gxia0VqT2whZ9dTP6uu3dxCQvTZVxR-G9B7f87WaxzMDhyBGkUBS5Zgu3RkI0lZ6XXOObgfYDFb8KDh1fdiHnDo1_DmCBKYGRtHt6Gotxgaxx0rMrYlrT80iv00o-cqKCa0U3FDckDTshR9EOgNsfdCLSA6RUv47rL_xLYKkKxBjqBTl_zHLf3rAjfPpfCtcPr-TcvOJ1xH-B8o_IE-qTT0RmjvwugNImROy7fZSfQshIx8K4oyQ9uvqafYOzO6oP08pUimdoGy2_KRhQ5TgDsrFdIgZQ0Ufi2tSFWRnpg2cyjUovR0UqZpXiZxlWsVZBQGjCrovnl-2W7uBl4appWbeoVq10j9ayX0mEy-CU21WJro9LPzHSiHGuCR_PWGb3LY-2gtrwDy_cTkpqyb63pQP8CarWnj4sKCEkIvF2zRu2-ePRcr-17uH5VehA4fQLmnU4iL25MMDGIribM2ZGzXHLR7v3BGnIXK4hrlpkKDSB151gOeWvbDDW4Ohd-0rL1UUERAFBMXS0WzFk9rFSx17qlSs-gK9WKjiLmTABNUPYcfhcw3nDTBhnUf-QBuBPb1-5YaxnBAL5A3PGFOr9hMWmuK78pug-PSEeZR4o8bGusjF46ocJVdugW5RqvQG-FG3FgYLUHRaXcdPKe81X4xxrWEmaYE3GY7iOlV8gTTAN4Qmnex0uREKQSnHFWVdxLKS-ER9XEpdIDQr3BiAMevtVOyob-M70skUoCrA1i2c_769rkjSmaVAD5ft7vSef_6mZox6QIZRR5bWGiwfNKYCK2vzQJ05wNs0vdFV29BLv7YLpzvnr-lpqsODKhwFkq2hZWAhQUd_-OsvsiiNCsKt6qqSDs0RtXMqC_uXQOjFFHoJllRZm7MKtWwURazj9UfVuQiIIG0WaONGZ-9hpbnQjEEm_e0jrZmKl0s5F48qn3WMUk9QqOyhlYGsD-dePgOF0GgJfEobVKBWf5Equ2ZhKzizwbmwIKTPUumDOAS10Hav4NTB9PxzVGrgwIvJ-T9_3pdU8SYwsoErcbdiAaS8No0a6v8fHwfZWAJSvcj7XFZC8TXMFO91F_CS6hxoxl7X82x8MtAR6zF5w6aQcJQjORc5XkPDvr3S3CM-FHVRO1I7XSHE5TnfhK5YPGKVMu0UUylnKBHlEaJHIhpfaBPRuXCTzCBApxIAPwURGMnJLLhA-1-GhhN0BoNaC2CBP2ugplD0zXjwMQ8Acc99sCn1g62UZI1aoOHVlTJ71Q8i1mSFkVO3qNwlMYiK40mHlMjBTYKHdy1Bms4jVLzGygboAJg3dEBGXczbL66NERNezvVrtGm6q3KIEqvySlBQkF2YS04Zlpgiy2l7RLgdidLRGRP8EfqsAar2lOa4H9hevp2fQ0SgMvKJbpyLrX2uqjLy6faM8rbsoZnC9bQ8hNahi-3FBEbNR6YN_YRx4QaHYQWncAbUE0AaHBzKg8c9yRueGny6LlhTP-Tq0koWSvPu4eBcy58EdIJ7Zr3TzE6RwUKYG_X_Bo_IkMx8ikyDfBDrfwbKd-0DWBCySNSc4DyvUElbC6VjnXRo-JYBI4Mu9PKkJFuXcIxqloZPSqqVhOtragybawOUcVMQqMgKoH5WYpn1e82LfQYnzfWQdWiKSdaP6x2_whHRwMlF6-Gmb6iqg5TqwNqYoYDLPtf1byTYEjq856zDbT0Z7FbCDiKj5IfjcvUtburFc7bJc0EvgjeMn61A1XKn06jufhJ6dvoki70PVs8fYLiUGrp3xqOu5I0BFisUAsiNg0hTdltoQjIWMkIhbRWsFdZDtAb45__9uw1zHJ5xIQtBNKbGlUx3IWza2pYCbG6p6alFWFbGI5CscIaoX6nGADK2Lc15kSkZSRhWhy2k86nVU22jwIglFIfzZhcEunG6w7gGt3A2sDAZSdxGDDaI_jlqZhLtBWwuRux4cCIABhlaxlpUbEZsK8FrV7HUSVVrAZPvVhTLgkUKB90dAFDjDegKyv0k24H6IwwnojVHfL3X079axmZ6EUiAUMNVIalYI2DFuQpzitF-AjkqCEx0R8RZJDDMNXyXphQRA4mgUIpVQoWEHYvsZMk5tpVMVDK4phb0_GCAyxHLSZUPulAkjt2g6ZmomPEoStyJK_bGowSDAhX4HZGTeR2xlQdAjB0epxPIAsw_8qGPNNDgn2BXmyzpzmEKzjqDyxk3Is77wWdF47Mt5RcxqRJeUtDXNamIRShvCl8xcJdsq0tTjl8qhdOrC7EnHNO8ijJvNyPeTY6J0Z5s5mOu1e5smzWY0EahHFWBYmGcUYFs2z2MRXJsGLgrpcgxhWFWc6bqv4RDawUlDVnygCuVSBpSTqzpM1crcGeihDfXLg5c6OcMZ_FTMfkjYJnjaIeV8BM-UV0OzFb3ImctdAzoo5XBHVom7BOBvMoAYDPHEtDs6Lg4KLCrm5aJfAF26r4GmWYUfNgLzzqxbGins8GFj3udiympgtkc2iLdi1WAw2WcplRU4jMq8idaNMzuupixfAQba-1Z9ttSOVdU0SlBxTQj4aT5N80tmR9AETSFjORpYp-07h9GvfUSKnIhbR-0vL14PJt2GI0IChmZM7M1xdTHWaaNnmyVUWzT80iWhGKEcM19PigHDkwMFxm3DXa1OZggRAMXXLURtLAYuyZ1PL6Rhp7yj-KBaORB0LulOOugde0hNvEzHnbDmictwtV2KSDAYu98N0YiV5I2VVZCxAKmr1TEbcedIK5n0bBBWY18K0ClGPbaiJgDCgb0xgcvAz7QoyOTJLA5BO7jU5JOQmbo0nWFhlnKaRZkmEiFcvC7u6nElTEZEmB9KFWCY66GPftQjWEERj95oLgIHjePU4WmHyHdx3ZvXWNORWYnl1Zoy99JTWb4ePivqivdp2KfX_41KqPqBiq3CbS9RpB4qEtBfpW1j2oACxOQkSTMJneSSCeo5bDEl2ZmaEnUL0u1A5f7oVMJ9EHeAp0dbPcgDHAAMQ0EKFqI3TCp9s1IIkfUSa0JwxGVuBQ9Npk9gY1KXyNekjupZAA0pgjgof9cT2ezVdQa1jdCmDSTMQ0EwdKcQVIhu-tZXkAoA6xlRTmAb1Q1TRZvINOk4hTuQEbKJoNH4W1UwBQp5_HSDjlfeUnVVy2l44b7kBzfeSWUqlsY_p3WGgkU8MoA13HC1X8gWpGpniXpGsW-5UTon5AwGN1FH8WXTAeRGGapi73tfk0TuSM6OIRp2l0XVGcJWXlsYj5o6XWB2zM7PkDD8cou3gieysKeAyvm5VlP0lraqAn5x__C19ACzcWCGG1iNRKi6lObch7U3hu9C1l7Y9qVXrnyt4DEEKn-1_fv_nedM5J8HuFmnATSMUyDbwofK32wnkjFlo5izIQ3HPo6VyYK-JB7kaFX2WxXnnjCJFcjscc_2HrHar2MW3TL0QcT5SorUEBjaUXJwKta9_AtCP4LWVE9gPDGBgVekNJ4xJngDCKnjOSEKokhpX5q1Rb1EuqR1HGtcZAo5CxEdQqDW6oGorSCNgjLBy5DzNzXXp56Acs9Uo_UHNtnIAyMPzDTjCpeqMygzUNKubHOqJoHGoydthDDyUpsFWTbyqD3fv4lkrSF0LkKSGFmUaqZZQBNhE-Q6ITmQoCk4EBvfNGNC92zwSsysk2Tx9pXEvajmLLMmul1NFTEDcZHX8LQ73qOLTvULIP67jKJZjsMU-EpXkqJm_GQuU5KPrmeSMh9z50JMi6By7H8IgO-omtOyMpYVkksZ-yMEtiXd01HvdSbtkjjmtJsKjyLlKVYt-F1h0dY0OfLaRZViE26fFTCR7_Ubh5542xZYX6UXmFXm32aUjgBBACQQsNJbDLIneDCwCzDbMiKgEWKkFDMB8hikqb5oAWsIhDBw3HX2gNcN4YKkDW4kgEb9TiKHRBVqDQ8dAp0JjzRVPP84vQ891Y1wcYR-DGbf5lZ9mU_UzzFHRGmHJfV9Iax9u0p_uYc2pGwpdS5KgAV_XVasmxze3N7TQjhX96irC1ZAOEW0ZJPOb06MNj_xcK2DoN21AeeA2QCnUAiCwfGMYtVa3M6HMoZ0RGdsxMJLnyDZEzlSJT_lSGzYxw-micexHoJqdW9_0pLv6qzsHGyqIeGcmpFLw7UNxDXflguBVylmVCFuSHkIXhID8dg1YqQI_pMZUbU7kV-OgnhoCNMpgIFXdrVcj0AqbHwSTqZhz-S3QPCo1hAND8pCyv2BlL2FFraWjXNXUEho5YV-1OmhP0W8R75NY8lVEwUNbrtQixncpKYwc82hYj4-Okq5UppYeBSMQx4JJZZq3gnI6vTSLLE20jgexCjodyDAgaxvi4gjxmrRbBcixhVJUPEjfKSXynS9IcTADDaITVUCFzmUU2HR9cP9TuJNMUfxT6ShlEFR2o16OT6NSVoSlbIzOrqrLoeTFxOcYt4QO1jItT_BK2joq4IjGagysLkzLUG47itXBoXyrvc4uFFaajrl1U2Fl9D3IMC8YrHAFlKxouM1loimfLqLLKdaMyy3ioI4_GYdVRnd3z8KnKe-ZRlOdZWiS5NnHGeVStxx5zvnRSnGZkGiV8kXG0XllQBxsHOEmxLo0a6aBEr6Ll5EjTrGJGXOgIEdg006XST5fyRmrxs_MecYQp6x_5jfTchPsxk5t46qgImZmUoOBZ09IhFSNmNE0wPAcnlIuzBWYSoXduSC-QK05ZMSrvEqEyVXF2KKFg6GCa4aO-gULFBNLRJIzlxxhMoPHogBNoteEW5O9lnJ1N0YMuncPqmFYXFL47FimqNxte1rKaTZhaalZ6UBLqG_EFaQ4RdYwFrM63jAKSchOR61sNwsvHnGKDxQhiS3EV6jPC_GSLnF0jgYYQJKPEUX6z7fulnEsKH8uowaHyYVngjuZa1JcLRV5SbLYYYxLsCr1lcYTISHbfLuSUeFKisJ7CMVLTqaCPBOCwluR1mzsGl0lU7RzAUqogg1GoYz7TEUdpmLtl7ofB6JHqw-DGcYl7ne6WrQbcDcMk89zcTTUoGw98G07RQ09w424ROFydbxE-uXHAhaTu4PkWnByC0TL8DBM8oGGq0fopSw7QGj9IWdtdY4QIYVWwPAOtg9xCOmDUL0YZPBUmHU0EuGtKESlB6icxJb3hexI-Xf8hRFDNA6Hzfu8oxoZ9lAkd2Q2HSr1lFbRoiU9Od_AelDT88rxRkcIZeJ3C7q7SsAp5qM8BGkfkjZV86Jn3pTgyNIbuxcEjWJ9KOLAwHhDajQ5EbdC5pO1OCmFfOowAEGx0UN8L0eCyFinRSdFr3euYSbmXWGPlv8PObQZ9ruQes5WnVRrwquRBMR4-Gg_uj7vpIWfvlcNTVeDquLAgoQ44GMfxD5UwfemJetPIv8LT4Eb52qmYSwzlquitSvTFMuKrM9dyU6vEIuXcrmQVsK7zlWB7jIegyapLGSsqWzIX6hOh_IQMJmAQA3etsM1GvQWo5Y_C-oCkUwwL0D99X7W-7ME8I4LCfcMJX4iefEOZKFRMg-kpwLZFM9eOfYnIHyi6my0FdBhiJpHGEpW0bQO2ZTMC3KdORRgD5Y2wDFpYPUmIiEH4yF--1gVAb2T8WppF2trlrhvnPMAJkbkB_ZhwNRS2FtVaRpxAeXhPpRUlRbKUVrsc6xOmx0l0jbXOiumFAlhCW1G4vDCFu3o9wH47dmxjghkwKvbUefPqxXMBhIyK7_FTEjWIuNKcPfNzlicuL7Mo1scQDBKIUV89mMdBOOtLkU9FRXXeQHM3IpaVc1WoUGroInNPCIdIdYvaU7XskzhggQdmyJKx8mZGz2QVY1lYVWWSJ2N9giaRMOsT7scJoWaPu75feFVRhWMkbKSJMNMFD2R9QDeOFAo5zhTl3z8aDOZzx1XNHZZIjir5aD4VUXqLVdUyzwWWByNSdx-tVGAPz5mLsjyZEhMNLXAt5MlGqhqU5xl1JEtZG_EuPFODLy7fHaugyOPowXhT8ZKyxrIeSBXvSzfYPH09WjWBVIz4Jjjvw3kj04InzvetxgMoZ4Mqf5GlYPgaKD8ZCtT5N3SndMQBJh7mD4NOtDoYI-pQamEuxyMPK67V-Yx8Bl7pcc9NMjdyNaocST1uH8KdpelQYdqqSAGFxAUvdC7LYO5QwvkILg6-d7QdrQqGs40zApPzcyo6OS1R-URn6RGX7RMBMIKVAr4yfVpSpjzpoDztqt_q49aj6hRh31osqsgkSBuIME7rEABDW5kGuEEL4AxKTQk_ZHoSiRIBEmjpMnp6GHFsqatu8dzTlrf4H3FsW1bJDWiu6MyOOhC1qvGQnPJXMYsnPU5x7k267L0o3CSQeKq36BgEmCTSzWg-YnIZc5AWQRez3JLGH35B2TlAlw52bjhMlk4E7OhVHPnrHNG6YJPn_dg0nRQ7A6wDALVcIgH9PzwdO43oMWzsX0zKu2lLKmWdI3H6clLb263e4qL9UoLO-3TUjzPf9fPs61NXfvf8rcyhC302ltjcqh-TBllstjmG0sdQeB2dDdgHtK2PisXtBiRV0XetOmFApcXvBwBBG9IAdEwZZ6DjFe-EOZejFgWqo2DJ6uaPnG8pUI06WT8s_IHdlSxcVkk0UB1HpO1oX59hTQP0aEmlg2uJTKhUSDMNVKP2V3WGpnE5OSaN8x_FNml-cD7A2tAwaWAiBiuj3TAr-KRAnkuVQy-1eKPvcHJMdvckUX7-247zn2SoAT8-iuBYytWwrgOfZmhbDJNRjf5CQS_K-RAQVVVr4zYYLcPJMRk9Oi0vUCh6eRKA6UiceYpGHkeUkyKhN_JzgNpA11bwNYj-9mNGEnlbqDJdOJmjxygFCjv7g7F7fn7yaXUjJXkUZFl5hlM2kdrhKIoWcY1BR8fGCqcVwleVGhVxD4kmyNWTdaKg6-A_y71hgeVGWaTS3_ojAjsxUchwdW_GMZYmbuUVeRIUvu_lgRuVMeI8vRwmlZhJo2XSi_1sTYc1HQdNx_357fb53bzF2PBZ-MthKre7eO2-CnldFpW5W_i8LJMkytPAL4oqj3w_dD3P5TyMK9-N_TDLQz_J3Qrm0uVh4vvgzEfM88v7DO4AkV0YnrnRASK7KKkC3K2WyM4S2VkiO0tkZ4nsLJGdJbKzRHaWyM4S2VkiO0tkZ4nsfiUiuyyMAtBjLEn9zBLZWSI7S2T39yKyWxyhsFvoLfEFGYbbtHdMphWO0d5RLxXPjEg3_OXVfw0XXuJyLyzSJPAq78FcePDvW6kOy49n-fEsP57lx7P8eJYfz_LjWX48y49n-fEsP57lx7P8eOIYkJ9FbuQlLI4tP57lx7P8eP_0_HiLW-kJMQJdyznGmx5MmXcooCVLRL8qn54cCT6Fn3gAp95TelGc3kYvYQKPtf2H8a8s2Z4l27Nke5Zsz5Lt_UOT7QV5FBRl5EdpWYxVnbqk2RD9h5YjTwsnqE_njShEM11bEVrE6i55tFgVwN-i2RNnFc4MdHvelHUvdPzidoKt3-VyH0ySiaP62y-iE6IgknvS6ggttuyp1vRYhpGAsjx90DYnMkkK82aSvWlEh0eGjZKdkXRCc1TtO4xiDOponnb2zZ1P643ZEUUehUJIiRBtBM0jG5aD0XIwWg5Gy8FoORgtB6PlYLQcjJaD0XIwWg5Gy8FoORgtB6PlYLQcjP_jOBjzwg3dIIkAIhT_czgYv6XgyJjS0dd4G-SLf5XSrHXsQUaN50gZtHCerxk4yPQT_LDrYMeQ9Ivq7j2Ciqeah29Xr0sjgS8pHhXphuWLtHyRli_S8kVavkjLF2n5Ii1f5D8bX-T7l6-_JZaeV9__8VeihaSejbSQuwbPLjb3pIQ0yH1Gsqj3GBlBU0An9_Tmm2OJMne4bnsk8nlU27cYrljIy6iKvS9r-DYB199OT384c37j_Eubn_XG60twMoqPsLO74Xcz3Ygyz6_CqNxjGtPbV1WEzXWBrPqhN2bm1U3SMgCF_JjvfiD-QTycQlhIeH5ULLm-Gctw_3Z5cgJeOhILnNywzfryh3-BX8xNSZmwwsvDx3btHX3T-QawNfF3ISToD52qU5m8HJMSu-1M1_IwzLPUix_TtcvLy36FMEdJ11KLDRij5VIH7U-vWXeKPxlMDDOcdV6ZZniI_bHThqE_dZZhEAlYQmq38mPCFGmfYG6vjYROZtc0PdT9d61Rgj629GqvUvwe9HyHtoRRh_6otm-T6R1iE3xAw7c5BQ0kbk7sAYR__94aAGps8zYqu6PBwyyxhqU4yvYJ25ZtZLBN17zL2JvO-pua1rnaAV44OWY2jn7oL1uKLzqyVgdALSYTupoWZT05Pzj5nHCipXZTYQdR7SGGfHLM0BymXdWsryNqW-qa_l4EN0-OGY3DTSKtBEXxKgxQ0_5FIIbyUDdVx0T4dtcBMBTpac3_IGo6KQp7csxgHP7mC0U7YNTZgDa96ljJNYPKkmIzumT85JjiP_yJtyK8IGuQDa2pG1Ta6-SY2r6r7zJQok-rKe0mZgaT2yLjdIjL1lBzM9JNpAJiCHvlRSIyahxgm8qdZi44Oaa2jn71uUBtej9pmuBPquqyHTsjYv9X-rz4RlaTjgHzL2c2xrptdeymzfFE0sBNjsSDR1EEOeLt43qqxmmvar7m--sxasc5bmFMbVPHqApht8FyFcFwY6qDyVIAkjg5pjSPfuq9DFr00u0RR7q2IEY1DbjmsmxB1ZJJ1YLZ7rGsbKQOE0HVIwzFz1usfxKxA4x24pt7ARolDJqreFSvqoPLbtcc0LWicA_d2VFlmU6e2vYLfaRY1vodXTgdlTz5IrLiKM6CMK2ysvKKxM1LzsAdSgN-jKxYU6XeTVZsnRrr1Finxjo11qmxTo3h1NyfLX-f4js2Kb7TXw4zeP8q_OWBVwUsZnGcZVXqgr1kaVTlCY99Lyiw5CANoEcu84qI-XkQ5iGP8jiNMj-I0uR-gzP4y7Ol631w4zMvOgviA_zlPudl4qbpHfzlj4uK3qYpdxM_jMFc5h6P52jKj5vPGVYuwCBJxOKsKO5FSX4_x3N0AGTkf8wYAMQTlN98BJdDK-GZQwF50-1DuHejUhuqNXni5g_GIJeiMYTl5N_qo65sSkZjZBDMslhM9GKD718_U0fsJXwV-7gittA5KumQV1WaxiCdOsFjYBw5jw9EK6q0nVU8cD26gEBXUY0Axsyc3hOOqNRpmodZyuOyyHTDBkIxUqcPxRvGL36HhosMsKhlUIlqrAbqeo6kqj_e6BPVgnqeobaWnK_nDX1CCMypYbxPxacO_OF3eMiBAgzij732JM4bJYS_7dHQYpobZmxYjH61qOKQTIci-KAZGzFUoQrHODKSnDeNyS48TfRqIkERyTBSXyK5Lk69i5DGeUPVA8JGzTFzB0GaulnCS3dkCB0RnLF0D8VjPZ3kXg5dfXWFp1vonCfMCfFY6SHIQ5iGv4iYRiYByxYrPXcyimUebjo5b0T5hemeoVqhU0sivS473q_4ei2PwOgsvMrpygwhaJyzmWqs2Esy0LdVUOlqLANSjgyEDweIJ2XunJ8jrdwY6FkuR9rjuhy7e6bdXPHGUoRSluPhH5GFo9_eQTrHQy9NC7B7xVj8YCBSQwweii9VvKkVR9AEDWDeDit92mKY6oe9g_vqTNSJ842oLcH8PO6lthEbcSzn14dA95km5EkAFefCMwEdVkWbJwSvuZAUEFO5qYyyA4rgDOOhZ5CsbVuL-hWk-xAF2vnNpPTqV7thIvcjP82yLK7GIoHbN0x8WB0ztvKqif7L7prAmQdl-IVXSjhHbpSYnAKfu1IClOZ97pCgrLm9RMJeImEvkbCXSNhLJOwlEvYSCXuJhL1Ewl4iYS-RsJdI2Esk7CUS9hIJe4mEvUTCXiJhL5Gwl0jYSyTsJRL2Egl7iYS9RMJeIvFll0jgxe5BFftBFeSzl0gcrxuboQQNUxbnIaztyAJy-yqJ96KS3f3P__i_Ed0eIRhIDl0eIWdM6BbJf6XujhDb_bzB2yOmqm3m-ghN2KG06JSG57wxEIqZQIONsqq36BlxxHzIoEil8jPAz8v8PA0iFhd5_ve_j-LtV7h-YqSkxKFJBSor3k1AbVKj2-so7HUU9joKex2FvY7CXkdhr6Ow11HY6yjsdRT2Ogp7HYW9jsJeR2Gvo7DXUdjrKOx1FPY6Cnsdhb2Owl5HYa-jsNdR2Oso7HUU9joKex2FvY7CXkdhr6Ow11HY6yj-u19HUeRVFsL0hXlQzl9HsRcrrbGGsR4UWc4Mt6O9pcLeUvFVb6lIkirxkRiMjwQp97ilAmvAEJvI6ymMOrOjt1OQHmvOm6lw34NQltIAoLvE6SSFLTEqP2FvmLmnwiD8uX1TxQJM7DAlBsIF7if8NNNyHFXoK0tzNaVob3CKypMVojvkYU2orGbKyRa37sFAmEDsQHs3YTy7HxuruOGDlaV57YVIlktK1IPXXsDyXO1ABuGzvB-j4ui3y5g4aoYjd2Iguj50JYbOyvyDX4DxK919YRzVuUAJ7_8eV2AUASB--N9jeCqP0piJRCiefMXY5TzzqosH-aJo0o83iiFDoh3V0Dz96m-cmffmSFjdCvwUv3x0Fz7owoUxpIKGuIM9ov2NhREUMQ5jzEwRuslJtEd3-tD-6QfJfnFBu26Ub4g4tKAR34AklLIo8350-cZqzvOW45Eo4gmbFofuDWZaV3dybNUOf0qxV5eSfJ0A_Jstb97hcnTOs7evKNqqsz8a2DfgZ8jn8UgHWKT17uookdWxtTrGCM9lXRflD6mSZSyi0qXJlGbS06DSc0eos1_oHJI-80c61hjskSnVGvwTByNKjrZxLlT368s4rv0irPKkCnhaxXnq52EWApLwimMc15pO826Oa6u1rNZ6pNa6PyH7PmVs-MthEthfhQKXe6GXMbfibub7VcKqLGNFxXhasDx0vcQvmV_gCGJWBGkAwDMEH93LiqzMWEVY49B4pqy3_gffPfOSMy87wHpbVWEclYFnWW8t661lvbWst5b11rLeWtbbf2LW2ywGbFEVLPbKMfY4AvS7tP494LbOQCR56VV-UhXByFymEbhW_V8KpVUJNgCRMnA5mO3RAIzo2hCfh8Lkhm37FewIdazyvBldMylOzuWbty-_f_fmLx9evrsA1_Tizy__96XK9ZLsGWEhBzafqEqppfwo7KGWbiETUfD3S9MeUVh2IQ-xtSr4vudnnzfvuZAUwxM2-_fdmxcvX1-azjHXjG5P5VaQGGhytS8p3UvUcKw-vdoOy-gkXKL0Qr8-repiRWhp3YvbndhW82mpmsK5SHhZ5FkM6i0bGWANH8Tk332gMzGpDRZna-VNyGQFzXMgYyWDcZhdpFv2K5kmNU9PzxtwuXuDFEaXIrUHj9YLURuv1rIU1Zai2lJUW4pqS1FtKaotRbWlqLYU1Zai2lJUW4pqS1FtKaotRbWlqLYU1Zai2lJUW4pqS1FtKaotRbWlqLYU1Zai2lJUW4pqS1FtKaotRbWlqLYU1Zai2lJUW4pqS1FtKaotRbWlqLYU1Zai2lJUW4pqS1FtKaotRbWlqLYU1Zai2lJUW4pqS1FtKaotRbWlqLYU1Zai2lJUW4pqS1FtKaotRbWlqLYU1Zai2lJUW4pqS1H9X0NRvQR34OpX4qlGub8QRwX-DgTVBjfZPaleN21JpecHziqpRnnixqEbZo_hj708TI52qd0qhlsQ1pBwlXsSO6oKrF7fj0XZGPrtoUke4b9IPrmRaU2F6YW8CoY_I4kmY4jPX786OTYl85TNvTqvpYY2DouSQeua9XuZTkm3doS2-Nma2F32SYLGEUnqQ3kw4chobh8aoG6OPNPTbn6CMaK5-hJC4zL1AiRvYZ6fVq4X5mHgeaGfHCM01kypdxMa_7NI-f0povdZar3FOOQz75fDjLS_CgUvc_MqKfyCZVWZR5lXlWGQJuBiBKGfplGZBVHqJ3Hq8qKKvAD_nvt-nCZJlMRBwu8zuFt8vN6Z550F4QE-Xh8L0asksny8lo_X8vFaPl7Lx_vfio_X85OscpMCrFD5BXy8zj82FW-ZsShieZbnpfbLDTiiRvUIcKGx5onzPf80oRetx5xVr0q_STbw-NuKvMldz6dIEsZza3IvR-B6nE_Tcg5bzmHLOWw5hy3nsOUctpzDlnPYcg5bzmHLOWw5hy3nsOUctpzDlnPYcg5bzmHLOWw5hy3nsOUctpzDlnPYcg5bzmHLOWw5hy3nsOUctpzDlnPYcg5bzmHLOWw5hy3nsOUctpzDlnPYcg5bzmHLOWw5hy3nsOUctpzDlnPYcg5bzmHLOWw5hy3nsOUctpzDlnPYcg5bzmHLOWw5hy3nsOUctpzDlnPYcg5bzmHLOWw5hy3nsOUctpzDlnPYcg7_U3EO__DL_wd7B28U)
