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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzg1MmNiMWMzOWY3YmMxNDc5MDllMWMzYyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjJlZWQ3MDg4IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV81NjkzNDhmOWRmMWM3MGJkZWE3YmM4M2UiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzFmNGZlMTk1ZTExM2U3MTlmYjFjMDc3YiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfely3EiS5qvA1D962jqTxJG4KLM2U6lU3dpWlbQiu-dHs4wKAAEmWkggF0BSxSqV2bzD7hPOk6y7x4lkJkiRmtrZGYzNTIkkEBHw8OPzIzx-eca6oSpZPlxVxbOzZ9vtVRL6eeblQVrGWe6t4tRNOfyYP1s8y9ri9qqornk_wLP9mvlhdJZkfup7gQv_z1v5jHtR6fl57Hu5G0Z-FPo8DMMkWRVZXrI049xjiZfA81FUrPwghHGLqs_bG97dPjv7BX8YrgZ2DTPUbMCpFvCPjNfwi7_zriorltXc6fhN1Vdt46zh-ba7dbJb513XtuW2430P72xZ_pFdc_yo0a-79p8cPnfX4YDrYdj2Z6en19Ww3mUnebs5zde82VTN9cCaa1jm6ejtjv-vXQX_vtr1vLvK26bnDdBi6Hb818WzNWdIRJ_zInaT5Jn4zRW_oYeAuPwqjNJglZRpUXp57GYFZ0DlJOC4srYb8NOu6qrhsHK1I_WVV65K7qUh97yAx15awv64cZyJz5Gru8rZtt_V8ME-rjNvu6J_dvaPX57J6X95Brvcdj3-S_yZF1cZkPwfz2CyZjjL24L_9OxH-A7FEzB90eb96btX78_f_vDizdVf3p5fvPr26uXbHy7ev31z9e7Nix9eXb1_--Lb71-8O9kUzxZfxE5sGLoq2w2wi1cZ66semYrX5RXrgboDp_F2w7rtcM0fqwaH7G_7gW_gLw3b4Obaa1_A6z0yxbOzZlfX8CX5GnaRCzpkdZt_xO2JgPlYFsHjsIED_wm_8x3v-rZhtfOXFsYvnJfwl66tnXc1a7jzot6umfO-ZbgkuRBWFLTCLXIi_wS_-Z3z0FE2bAtvDrdb_ALkEeC3Z78urDVmrEw8Gv_rrvFPzvnAhl1_5gDnbNsehqk225pvgIoMd8LB-TrYQadsO0e8d-JcgJQ5Zslb1rHxev3IDQqXjdb7Lc9JRCdp9jvHemyCIsxNMxaGwRfPYJSC06_bXV048C5vCmdYc_hY_HgkZg8T1nzZACM5MCVQObeXdOeLVyDIQelGX7yeC5iW0V7B33BZvAcybznDVaBgNj2ok5z2gjX4q6V412nLifWUsR-XK77H1V1bwFBOuxvgS_k9G3H36an98EqYL3IfO9-HDx_wpcvm7aeGd7_vHRJkBz66gEdy4OfLxnGWf0L2BMXoZO2ugTEc-GPBrY1ByR-zIvf9GPTNYxeG-7OVj_e7PAdl3jufwCggw_TAMnUFC-2dNgMldcNhxdwpdh0ZpSkJibkfxfl4Wd8w0Heg7Wmjr0kpTG3QgccndiharcACr_JHz_jZedFx5sB_blhV0wc27Sf4WeofwcUwiPP5svm8XC71_8GPFi3Iqo2WFrpxkQA6GC3tu679GagsRgVAsL2PXw--MEEQvvL8wGfBE2b97LxuxFNAhlc_besqr4b6FvkKxFP9xaIGUuJtgxxV3bApkiSRl_B0lYwWd8G6az44rMvX1QCoZdfdR5PDb0wQJY3C0mdh_pR5tSy_uwVr3Tjn3_7VOXXeC631t9coyOJ_Plv_dP5ycfHu3Pmj008IM49KNy189pTVXbw5d8B6DbwDWEdaFqAiKv-Cb-v2Fi2fw5ubqmsb_PeJBSOnBDpgSRwFq9VoaS9Z0zYVWo89q1pIy9Dfs38PGmAKOBQBKJkg-4qr-qwtNKoCkhONET4772kkVvODSuBtM8XzJbgI4arM9mxoXaEv4PSAtXmT83vhw93nJwgUg0uyiuP48XO-Yvl6n5A9OCyAG0CpgiGD_4WBkGEGLhEUKc937xcT_JS6cZoFvvf4hX1GbHeNmkm-RrOinqoGJ-9AVjraxAP75Dr__m__Z2qrgsDNYsbH3C7tADpF4KeRSRF4vRpuNY_cs30PHWNKhbl-7JW--3XXRjhgl4GGd0Cpd2Kft-y2BoQNw25Y1fQOEBkFA40hIsqONT2ilYltzouoDPPkKxPyBYKnU4mc8o4DRBoqVvfOht0qBCWQU84XCvrTPPxmYrFeEOQJK8bG4VsEO1UNS1sAlMahFzTSproWVLpPYB_w_sRulyW4v0Xgfr014U6XVQeEX4t9sAwDGI4ChClDBuBg6KWbAHs_MKDlyQTxWFky13fDr7fQV_SCRKfgNrDGQTcethv2ualK5B1AIblW9-T69wvnE7jQxxcaRkXh-3s245znO2I_XB2hl_zWyVh3z-ZOvDaxp1lYxoDZn76Cz9opBsskYjUKp2Z8zW4q8Gn34dlLLS5TCjDyQ9_Ni7HdEPGoXOoGUP_3UOfQ8xNkCVKWgwiyx8_52blApijZpgLmtWhCcaO7pFB2HXgEKD9Fj7zgKUjhmLvfvX3pbDjrAZGh9NwHdg48PkGNMGflKs_cR894QZivr66bJXzfAG6nvQJy8gAWdk6_ZkiiawxJomoHUZ_S6AULmcdW4ZPWhc8XLSyiacFW16zaOEOrRgApd_BxVEh9tdnVoHt4u-udaipCAeonCVJ37O78FTw4C_fBt1V17ciwZnHPft378pSRLgvOgj0j_fjVjEDpD-CjC1iPvy4ZEIgko4FFABzrd5vtYCOfKb728ogVLPG_0jovRMxg3VaosIuW9pfmIhckY_lH3hTLhu9A8GodzEaV10_tbb7K8yjZR85l1VT0pSDbBcCSe6HzgRemYj5BjF57_oRZCVWpOObajiOApVXROKdtQFtRzAWjKy1GiMCqTaEqHkUgh-XBoA9IEXLCA6Nf5ukpN8tNygBg3GPnu2gLZucr8OuZFY2kCORiFJQU6ghAxz4ZflyoEP8zCUevAAEyET-nv6hgPL9Kg7AMw4Qzt8CAVFrESerzDK0aMCaNKbMQjsxCAO_y_OO2rZqBkiodzYThdfUTRtd_xPQFQOVbawQ7pWENQsmSR2Y7-rYcroDdrnkHgEAmVfrMO1uVbpZ7cb4KUvCiyqxMuR8XaRx5Scz8InGTosziFSsA5pRRlkRREgRpUnpezkKXAlGo5Sk5InbrbOX-CoTuabP9aOkmy8C78NIzLz4L3D-67pmLukxSHM1A6AV-mhXAJ-a3v_xWuRRiTJHnWLN-jUwXZR7PYO0uR9NEY1ipD8mzXyFnIedLysQtspQHBQEWMZ9JY8j5npJ_APrtCJSjbgd5uWz-5DT8k47Wwkp7_twBZ3ffkq4ZOFVK3dgJAd6Rx8R_Ar3b43gDCibOx8G4bneDEMwC1DxMsAce8AegG41u9FRDAWOKZtOIGB3g6IzXMrLdo2UHARU-4yf0y8kW9GzDx6DjoHshyc2jnMeh74UgHprcJgujtve-9IocLY38NOU8iAKSMxrNyrgYBffoVArx1JZ4CgS3xd07aAfOiJQE94Eu4Lh87LcMnVb89Xq3QZ-H6Ewmsq35ZSNd5Z95J3wpRW78PQL7nIJ-Mr_QqfyCjOOLvbZXcNlsdj16WVwE-PHjiEEQTRgnGr4pr3dI2QWGATQmX0imXVw2_Q4_UaQkxdLU9i6l1VC2onfA-0PsCczUOEJ9UxQJnisuG637-Z60TDBIzJMwzFZBGRcrtaVW0krFUp-QjbK2nIh72eB2OSzv2r5XzH7ivLblsQWHlaKwtLXACk5ZV9dr9IJ7lCdnYP1H8FiBvz4Bh-AeELVh3zKOqRt0etVWglWB1Qm1QRCZUvtL4BF4gjSF5p8JQrlpnjGXRUESa0VpZdOMJD0oPyYHjfIwTmEMd5Vo8bRSZnLQpyXBci5dYxnNsVhSvqbjGSL4jTycj5iVBmi3IoQLLHBT9Qg__7krrrlclbWab-SwYAyqAfkcyU17oyJXMt9-2Zxj5qyHwe580ks5SMeHruI3EuyBq49YYiHGhkUvgDeWIp-idaIUmssG6HYgaaBI7ycud4HOpWsMn0kKWoz_2DSfJY4SsAPrV6CEwF4UO0wKIYOr4Etf1UQBeIeUPf5qwIA528ICbhDnCRph7cNS__KyIV21Bf1KW02mcXuLSqhjnxwFDnoVeUTDQprVaOkJpgfF7odhlJRxXmgimRSlYfqH5RzVqC4gy7RI0sKN1ahWGlKO-rS84p8N8XsOog4s3TsiySaMjYnWKiixADBb8vw2h5l4cw1fs3AEXF041x3brrXOpq9UulnqE-FjvrPNAZlq-AU4mr2DIglsbnSNYFsKEreUARCyQatHtAUsQzsKBNji9i5JAv6MQfp2A9yvhvzQ8bK36o9OPwKZag6i-QEdXcmMtKpu2YNGECwnYoKwMwsRkGb0CcB16Gzutgupx-XaROGVWNxLyfOY5VzCvCjB9HTdtlt8m3J2jszy6Wg3vvBiZGtFak-IkLPraZ1l127uICGa9jWF3wb03l-yusaP2YEjUCErYMkSiEtHNpKUld7njIP7ARazBQ8aXj0XdMBPv4E3DUhgdmwc3Ya82mJoHCVWZGwL2n8YFNdpR89VUExop_yW-IDIshRrEOgNsfdCbSA6RUuYd9l_YlsFSGrgI1jUB_7Tlv51hcLzQfhWSL5_1bzzCfcR_g8U_kBTKg29Edo7t1aDCJnT9m12Ej0LJiPfiqLMMPYbWimuzo4uaD9PKZKxXaDstnxkocMU4M5KhTRIXgOFX0krUpakJ8bDHAq1KD0dF0mSFXFUZloFWYUBRgU9NM8vx83cwEtWSekmXq7GtVL_Wgk9JZNvQ1PNljY6_ex8D8qhAngkf73hmwxkH63lNUC-n5kUyqq5qQb1A-xZTYKLGwtKCL1csEXvv3nxUuzsuZQflV6EBR9AuadjiIviSQYGsZXEWRsytjUH7d4vHIOzUFncIN-UaBBpIS96wFPLfrhF4VD4TfPaKwVFBESxcbFUNLV4WqtgqXNPlZpFV6gXgiJoJwEmqHoOPwqebzhpgg3rPvIB3Ahc6w8tDYzhgF4gb3jCJq8QJq01xbxy2eC4dIR5FPujQGN95MIRFa5ySXcgl7EKvRVuRMHCaAmyTrvr4DnlrfYLE9cSZpoScJvtIMir-AnIAN4Qmnex0-REKQSnHFWVdxLKS-ERNblkOkDo10gYwPG1dko29BfzvkQiObg6gGU75-_vXjqiZFYx4Mu63RXO-ZsXimLSBbKKPLaw0WD5pDERWl-bBVjOBQjped5VW-CLP7cL5_uX72josgMDKpyFgm1hJ2BjQcf_NKkv0jBJ89wtyzLUDo1VNWP0xYNrYJQiWrlxmhepG7FSDWyVxexj9ccVuQhIIG2WsTHm2RsYeSoUQ7B5T-toa6bSxYLvxaPaZzVJagONigpGGcD-dOLhe1wEgZbEoySkArP8hVTbCwlZxZ8tzIEFJ3uWTBnAJe6DtH8HSQfk-Oao1UGGlwQ5_59vKooYU1iZoJWRRjSQhNfGWVvl5-P7yANLULofScZlLRCvgVK91F_CS6hQ0CzZVzQWfhnoiFpMd9AMEoZixOcqz3vwo_-4BMeIH1VNNI7UTvc4QVnmx6ELFi9PNE9bxVTKCXpCaZTIgdjWB9ZkVS78DAQU4EQC4OfAGjvBkQ0fSPrpw4hANRrQSgQJ-l0JlEPTNeHARDwGxz3ywKfWDrZVkmW0wWMrquQ8JU8jFid5npH3KBwlU2Sl0cRTaqTARqGDW2uwhmSUmt9C2QAVAOsaB8RIMwhfVVispr2dctdoU_VOZRCl1-QUwKHAu7AXHDMtIGJLabsEuN3JEhG5EvyRFqzBqvaURvhfmJ6-rW-AA3BbuURXzgetva6q4sNz7RllbVHBszlraPsJLcPMLUXEjMYD88Y-4jehRgemRSfwFlQTABoUTuWBo0yiwEuTR88NJv1PriahZK087_8MpLnwRUgntDXvn2N0jgoUwN7W_AYnkaEY-RSZBvihUv6N5G8SAyAoeUSKBsjfG1TC9lbpWBc9Ko5F4JfhcloZMtKjSzhGVSvGo6JqNTHamirTTHWIKmYSGgVRCdBnKZ5Vv9u0sGJ83toHVYumnGj9sJJ-A0eNgZKbVwGlr6mqw9bqgJqY5QDL9ZcV7yQYkvq852wDI_1VSAsBRzEp-dG4TV27u14j3T4QJfBF8JZx1g5UKX8-jubilNK30SVd6Hu2ePoE2aHQ3L-1HHfFaQiwWK42RAgNIU25bKEIyFjJCIW0ViCrLAPojfHPf33xBqhcHDFhC4H0xkZVfO7C2TUV7ITY3VPb0oqwLXyOQrHCGqF-pxgA8th3FeZEpGUkZloctpPOp3VFto8CIJRSN2ZMbol04_UCcI9uYW_gw-Ui8TPga4_gl-eClmgrQLgbIXBgRACMslpGWlRsBuxrTrvXcVRJJavAU89ryiWBAuWDji5giPEWdGWJftLdAJ0VxhOxukP-_quxfy0jE71IJGCogcqwFKxx0II8R7pShI9AjvokJtYjggzyM2y1vBcmFJGDUaBQcpWCBYTdC1wksbl2VSyUsjjm1nQ85wDLUYsJlU86kPiO3aKpGekYceiKHMmbtgKjBB-EO3A3oyZyOyZVhwAMnR7nE_AC0F_ZkBf6k0Au0Itt9jSHcAWN_sBCxr24817QeeHIfEvBZUyalLc0xEVlG0IRyhvDVyzcJdvaIslhql44sboQc8o5ycI49TI_4qlxTqzyZjsd96ByZTmsx4IkWEVpGcQaxlkVzHLYp1Qkw46Bu14AG5cUZrlsyuonNLCSUWrOlAGsVSBpSTqzIGEua7CnIsQ3FW5O3TBjzGcR0zF5q-BZo6inFTBTfhHdTswWdyJnLfSMqOMVQR0SE9bJYB4lAPCZY2loluccXFSQ6qZVDJ-zrYqvUYYZNQ-uwqNVHCvq-Wxh0eNux2JsuoA3hzZva7EbaLCUy4yaQmReRe5Emx7jqosdw0O0vdaebbchlXdDEZUeUEBvDCfxv21syfoAiCQRs5Glin7Td_v03WMjpSIX0vpJy9eDy7dhC2NAkM3InNmvL8Y6zDZt8mSrimaf2kW0IhQjPtfS44Ny5MDAcJlx12hTm4MFQjB0yVEbSQOLsWdSy_WtNPaUfxQbRl8eCL5TjrsGXuMSbhszZ207oHHeLlRhkw4GLPbCdyYSvZC8q7IWwBREvVMRtx50grkfR8EFZrXwrQKUZmxFCPgG5I1xDA5eBrkQX0cmSWDykd1Gp6QYhc3RJGuLjFRaEZVkmEjFsnC5-6kEFTFZUiB9qFSCo8qN3C7UQBiB0W8uCA6C590jscDkO7zryO7VFeZUgDy7okJf-lpqNsvHRbmornedin1ffGrVJCqGKsVEul4GJB4SKdC3su5BBWCRCCERYUTeUSCeo5bDEl2ZmaEnUL0ulIQv90Kmo-gDPAW6ulluwBhgAGIciFC1ETrh0-0a4MSPyBPaEwYjK3Aoem0ye4OaFGajFZJ7KTiANKZB8CAfN-ZsvoJaw_pOAJMoERElDpTiCpAM89WyPABQhxAlhXlAL5QVEYt3sGhicSo3YANFs2FS2DsFAHX62UTCKe8rp1Rx2V46biiB9v5IkVKpbIv8Oyw0kqlh5IGu47kq_kA1I1O8S9I1i_3KCVE_IOCxOoo_iS4YD8JVkiQu97X5tE7kGHTxhNM0uq4oSuOi9FjIfGOp9QEbO3v-yMMxyi6eyNWKAh7L62ZF0Y_SmhroSfrjf2EGtHCmQAirRaRWWox1akPem8JzxreUtT9qVOmdK3sPQAid7v9x_vYH2zknxu8VakIhkIplHHhR-FrJwmUjNlo5izIQ3HNY6VSYK-RB5oa5X6aR3nnrCJHcjqcc_2H1DlW7Sdv0CxHHEyVqNSggU3pxItC69g1sO4JzKSOyHxjGwKjQG4obl0gBwiiaZsQhVEkMO_N3qbZolVSPooxrhYFGwWMG1CoNbqkaitII2CMsHLkPE7QuvGzlByzxCj9QtLZOQFkY_nEnmFS9UZHCngYl8yMdUbQONVkS9thDSQpsVeSbymD3Pr6lkvSFYHlKSGGmkWoZZYBNhM-w0YlMBYHJwIDeZSOGF9IzAquS2PbpI41rSdtRbFlmrZQ6eg7sJqPj7-BTrzsO4zuU7MM6rmIJJtvkibA0T8Xk7VioPAdFc142EnLvQ0eCrHvg0oRHdNBPiO4Ep6yKPI78hK3SONLVXea4l3LLnnBcS4JFlXeRqhTXLrSucYwtfbaQZlmF2KTHTyV4_Cfh5l02lsgK9aPyCr0S9nFI4AQQAkELDSVwySJ3gxsA1AaqiEqAhUrQEMxHiKLSphmgBSzi0EFD8wutAS4bSwXIWhyJ4K1aHIUuyArkOh46BhpTvmjieX6-8nw30vUB1hE4I-ZfdpZN2c8kS0BnrBLu60pa63ib9nSfck7NSvhSihwV4Lq6Xi85jrm9vZtmpPBPTxG2lmyAcMsoicecHn14XP9CAVunYRvKA9cAqVAHAMvygWHcUtXKGJ9DOSMysmNnIsmVb6g5UyEy5c9l2MwKpxvj3ItANzm1eu3PcfPXVQY2Vhb1yEhOqeDdgeIeWsqF5VZIKsuELPAPIQvLQX5uglYqQI_pMZUbU7kVmPQTQ8BGGUyEirtaFTJ9C-RxMIm6MZ__Ct2DXGMYADQ_K8srJGMJElVLQ1tXtBD4dMS6SjqJJui3iPfIrXkuo2CgrOtahNhOZaWxAx5ti5FxQ3S1M4X0MBCJOBZcssusFZzT8bVRZHmkbSSQXcjvoRwDggYTH1eQx67VIliOJYyq8kHiRknE97okzcEEMHyNsBoqZC6zyLbjg_uH2p14muKPQl8pg6iiA1VtnESnKi1N2VqZWVWVRc8LwmUYt4QJKhkXp_gliI6KuGJjNAd3FogyVBuO7LVwSC6V97nFwgrbUdcuKkhW3wMfw4bxEr-AshUNl5ksNMWTZVRp6bphkaZ8pSOP1mFVo84eePhU5T2zMMyyNMnjTJs46zyq1mNPOV86Kk6zMo0Svsg4Wq8sqIODA5ykWJdGjXRQolfRcnKkiaqYERc6QgQ27XSp9NMlv5Fa_OycI46wef0jv5Wem3A_JnITzx0VIbOTEhQ8a1o6pGLFjMYJhpfghHJxtsBOIvTOLekFcsUpK0blXSJUpirODiUULB1MFD7qGyhUTCAdTYIpP8ZgAn2PDjiBVhvuQP5extnZGD3o0jmsjml1QeH7Y5GiarPhRSWr2YSppWGlByWhvhVfkOYQUYcpYHW-YxSQlEJErm85CC8fc4oNFiMIkeIq1GeF-ckWObtGAg3BSFaJo5yz7fulpCWFj2XU4FD5sCxwR3Mt6suFIi8oNpubmAS7Rm9ZHCGykt13CzklnpQorKdwjNR0KugjATjsJXndtsTgNomqnQNYShVkMAp1TGc6ojBZZW6R-avAeKT6MLh1XOJBp7vlqAF3V6s49dzMTTQoMwe-LafosSe4UVoEDlfnW4RPbh1wIa47eL4FiUMwWoafgcADGqYKrZ-y5ACtcULK2u4aK0QIu4LlGWgdpAjpgFG_MDx4Kkw6mghw15QiUozUj2JKWuB7Yj5d_yFYUNGB0Hm_dxRjwz7KhI5chkOl3rIKWozER6c7eA9KGn552ahI4QS8TkC6y2RVrvhKnwO0jshbO_nYM-9LcWTIhO7FwSPYn1I4sPA9wLQbHYjaoHNJ4k4KYZ87rAAQCDqo74UYcFmJlOio6LXqdcyk2EusseKfILnNoM-VPIBaWVImAS8LHuTm8JE5uG-k6TFn75XDU5bg6riwISsdcLCO4x8qYfrSE_W2kX-Np8Gt8rVTQUsM5arorUr0RTLiqzPXUqhVYpFybteyCljX-UqwbeIhaLKqQsaKipbMhZpiJaeQwQQMYqDUCtts1VuAWv4orA9wOsWwAP3T_Gr0ZQ_mGREUyg0nfCFW8g1lolAxDbanAGKLZq41awnJH8i72y0FdBhiJpHGEpW0bQO2ZWMA7nOnJIyB_EZYBi2sJhIiYmA-8pdvdAHQWxm_lmaRRLvYdYbmARJE5gb0Y8LVUNhaVGtZcQLl4T2XVpQUyVJa7cLUJ4yPk-gaa50V0xsFsIREUbi8QMJdVQ8gb8eObYwwA0bFnjtvX3_7UgAhq-LbTCVRg4grTdkzP2NZ7PIiDSN9DMFqAmH01aP7OAhnfSnyqaioLhsY7lbEsjKuChUKDV1k7gnhEKluUXuqtn0UB8zxwAxZMlbcTuiZtGQsXZVlEWexqU_QTSTs-oSH9YRQ1OOu7-demZcrEwkzbSLsdMEjuz6gG0cKhRxnivLvHw0G87njquYOSySNSj6aT0WU3mJVtcxzgeXBiNT9RysV2MNz5qIsT6bExEAL3At5spGqBuV5Rh3JUtZGvAvPVOCLy3dNFRR5HD0YbypeUtZY1gOp4n3pBtunr41VE0jFim-C8z5cNjIteOL80Go8gHw2qPIXWQqGr4Hyk6FAnX9Dd0pHHIDwQD8MOtHuYIyoQ64FWpojD2uu1fkEfwZe4XHPjVM3dDWqNE097h7CnWzTocK0ZZ4AColynutcltW5QzHnE3px8L2j7WhVMJxtnREYnZ9T0clxiconOkuPuGy_EQAjWCngK9OnJWXKkw7Kk1T9Xh-3NqpThH0rsakikyBtIMI4rUMADG1lGuAWLYAzKDUl_JDxSSRKBEigpcvo6WHEsYWuusVzT1ve4n_EsW1ZJTeguaIzO-pA1LrCQ3LKX8UsnvQ4xbk36bL3onCTQOKpFlETBBgl0u1oPmJyGXOQFkEXs9zhxh9_Rd450C4d7NxwuFk6NWBHr-LIX6carYtu8rw3Q9NJsTPAOgBQiyU2oP9P346dvugp3di_uCnvpi2olHWqidOXN7W9O-qdXrRf2qDzIQv1o9R3_Sz9-q0rv3_5TubQhT4zJTZ36sekQRbCNtWh9CktvI5SA-SAxPooW9wdQLYq-r5VJwyotPh8ABC0IQ1Ax5SRAh0veSfMufxqUaBqGEtWN3_kfEuBatTJ-mHhD-yuZeGySqKB6jjCbUfX-gJrGmBFSyodrCUyoVIh3WmgNNpf1RnaxuXkGDdOT4pjEn2QHmBt6DPpw0QMVka7gSr4pECeS5VDLzR7o-9wcox39zhRTv9dx_nPMtSAkxsWNKVcDes68GmGtsUwGdXoLxT0opwPAVFVtWbEwFiGk2M8epQs3yJT9PIkANOROPsUjTyOKIkioTf25wC1ga6t6Ncg1tubjCT2baHKdOFkGo9RMhQu9kdLen559ml9KznZMLKsPEOSjbh2OIqiRVxj0NExU-G0RviqUqMi7iHRBLl6sk4UdB38Z7n3WWC5kRep9Lf6iMBOEAo7XD244xhLYrf08iwOct_3ssANiwhxnt4Ou5WY3UbLbi_2y2w6ZtNx0HQ8vL_dfn83b2EGPlv9eriV23197b5K87o0LDI393lRxHGYJYGf52UW-v7K9TyX81VU-m7kr9Js5ceZWwItXb6KfR-c-ZB5fvGQjzvQyG61OnPDA43swrgMUFrnRnZzI7u5kd3cyG5uZDc3spsb2c2N7OZGdnMju7mR3dzIbm5k9xs1sktXYQB6jMWJn86N7OZGdnMju_-oRnaLIy3sFlokviDDcLftHZNphWNt72iVqs-MSDf87fX_m154scu9VZ7EgVd6j-6FB_--k-qY--PN_fHm_nhzf7y5P97cH2_ujzf3x5v748398eb-eHN_vLk_njgG5KehG3oxi6K5P97cH2_uj_ffvj_e4k56QnyBruU08aZHt8w7FNCSJaJftZ-e_BJ8Cqd4RE-95_SiOL2NXsIIHmv7D9-_npvtzc325mZ7c7O9udnef-pme0EWBnkR-mFS5KaqU5c0W6z_2HLkceEEremyEYVotmsrQotY3SWPFqsC-Dtt9sRZhTML3V42RdULHb-4m2Drd5mUg1Ey0ai__SI6wQoiuSetjtBiy55qTY9lGAkoy9MHbXMik6RAN7vZm0Z0eGTYKtkxTSd0j6p9h1F8gzqap519W_JpvzE7oppHIRNSIkQbQfvIxtyDce7BOPdgnHswzj0Y5x6Mcw_GuQfj3INx7sE492CcezDOPRjnHoxzD8a5B-N_uR6MWe6u3CAOASLk_3V6MH5HwRGT0tHXeFvNF_8uuVnr2IMdNV5iy6CF87Jm4CDTT_DDrgOJIe4X1d17DSqe6z58u6ourAS-bPGomm7M_SLnfpFzv8i5X-TcL3LuFzn3i5z7Rf536xd5_urNd9Sl5_UPf_6N2kLSykxbyF2DZxebB7aEtJr7mGZR5xgZQVNAJ_e08E11ibIlXI9tGvk8aew7Ha7YihdhGXlfNvDdBlz_OD398cz5nfMvbXbWW68vwcnIP4Jkd8MfJpYRpp5frsJir9OYFl9VETa1BLLqh96YoKsbJ0UACvkp815Q_0E8nEJYSHh-VCxZ35oy3H98ODkBLx0bC5zcsk394cd_gV9MkaSIWe5lq6cu7T3N6XwD2Jr6dyEk6A-dqlOZvAyTErvtxNKy1SpLEy96ytI-fPjQrxHmKO5aarYBY7Rc6qD96Q3rTvEnqxPDRM86r0hSPMT-VLJh6E-dZRhEApaQ2p38mDBF2ieYkjXT0Mlemm4P9XCptUrQzUiv9yrFH9Ce75BIWHXoTxr7bjO9Q90EHzHw3Z6CFhK3CXsA4T98tRaAMmPeRWX3DHi4S6xlKY52-wSxZRsZbNM17zL2prP-tqZ1rneAF06OmY2jE_1tS_FFR9bqAKjFZEJX0abUo_ODo-mEEy21mwo7iGoP8cknxwzN4baruuurQW1LXdPfi-DmyTGjcXhIbCtBUbwSA9QkvwjEkB-qpuyYCN_uOgCGIj2t-z-Imk6Kwp4cMxiH5_xWtR2w6mxAm153rOC6g8qSYjO6ZPzkmOI_PMU7EV6QNciW1tQDKu11ckxt37d2GSjRp9WUdhOUweS2yDgd6mVrqbkJ7qamAuIT9sqLRGTUOsA25jvdueDkmNo6OutLgdq0POk2wZ9U1WVrFiNi_9f6vPhGVpOagPmXdzbGum117KbN8ETSwO0eiQePoojmiHeP66kap72q-Yrv74fRjlO9hTG1TQujKoTdBstVRIcbWx2MtgKQxMkxpXl0qnMZtOil2yOOdG2BjSr64IrLsgVVSyZVC2a7TVmZaR0mgqpHOhS_bLH-ScQOMNqJb-4FaBQz6F7FRr2qBS67XXNA14rCPXRnjcqynTwl9gt9pFjW-h3dOB2VPPmiZsVhlAarpEyL0stjNys4A3coCfixZsW6Ver9zYpnp2Z2amanZnZqZqdmdmosp-bh3fL3W3xHdovv5NfDHbx_k_7lgVcGLGJRlKZl4oK9ZElYZjGPfC_IseQgCWBFLvPykPlZsMpWPMyiJEz9IEzih32c1b88XbrehRudeeFZEB3oX-5zXsRuktzTv_xpUdG7bcrd2F9FYC4zj0dTbcqPm8-JrlyAQeKQRWmeP6gl-cMcT-MAyMi_yRgAxBMtv7kBl0Mr4ZlDAXnb7UO4d6tSG2o0eeLmT9ZHLsVgCMvJv9VHXdm4GY2VQbDLYjHRiwOev3mhjthL-CrkuKRuoVOtpFe8LJMkAu7UCR4L40g6PhKtqNJ2VvLA9egCAl1FZQCMnTl9IBxRqdMkW6UJj4o81QNbCMVKnT4Wb1i_-AMaLjLAopZBJaqxGqjrOTZV_elWn6gWrecZamvZ8_WyoSkEw5xaxvtUTHXgD3_AQw4UYBB_7LUncdkoJvx9j4YW09xAsWFh_GpRxSE7HYrgg-7YiKEKVTjGsSPJZdPY3YXHiV7dSFBEMqzUl0iui1PvIqRx2VD1gLBRU525gyBJ3DTmhWs6hBoEZ23dY_FYTye5l0NXXV_j6RY65wk0oT5W-hPkIUzLX0RMI5OARYuVnjsZxbIPN51cNqL8wnbPUK3QqSWRXpcL79e8ruURGJ2FVzldmSEEjXM2UY0VeXEK-rYMSl2NZUFK04Hw8QDxpMicy0tsK2cCPculaXtcFWa5Z9rNFW8sRShlaQ7_iCwc_faepnN85SVJDnYvN8UPFiK12OCx-FLFm1pxBE20AczaYa1PWwxj_bB3cF-diTpxvhG1JZifR1lqGyGIppxfHwLd7zQhTwKoOBeeCeiwKto-IXjDBacAm0qhssoOKIIzmEPPwFnbthL1K9juQxRoZ7ej0qvf7IaJzA_9JE3TqDRFAndvmLhYHzO28qqJ_svumkDKgzL8wislnCM3SoxOgU9dKQFK8yF3SFDWfL5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5EYr5E4ssukcCL3YMy8oMyyCYvkTheNzbREnSVsChbwd6aLiB3r5I4F5Xs7r__2_8O6fYI0YHk0OURkmJCt8j-V-ruCCHulw3eHjFWbRPXR-iGHUqLjtvwXDYWQrETaCAo62qLnhFHzIcdFKlUfgL4eamfJUHIojzL_uPvo3j3Fa6fMC0p8dOkApUV7zagtlujz9dRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdRzNdR_P9-HUWelekKyLfKgmL6Ooq9WGmFNYzVoJrlTPR2nG-pmG-p-Kq3VMRxGfvYGIybBikPuKUCa8AQm8jrKaw6s6O3U5Aeay6bMXM_oKEspQFAd4nTSQpbYlR-1L1h4p4Kq-HP3ZsqFmBih3FjINzgftSfZlyOowp9ZWmubinaWz1F5ckKsRzysEatrCbKyRZ37sFAmEDdgfZuwnjxsG6s4oYPVhT2tRciWS5boh689gK253oHPAjT8t5ExdFvlzFx1AxH7sRAdH3oSgydlTl0AcaPv_5fH5MTPQ)
