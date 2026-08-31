[//]: # (ob:26309ab6)
# Personal Hosted Control Plane Alpha Roadmap

[//]: # (ob:2baf81ed)
> Status: proposed implementation contract for review. This document plans a
> new product phase; it does not claim that a hosted Proofpress service exists
> today. The input is a direct design-partner signal that one owner needs agents
> on several devices to read and write the same governed state.

[//]: # (ob:22603d0a)
## Decision

[//]: # (ob:a09ba553)
Proofpress should extend the completed single-node local control plane into a
personal hosted alpha: one private workspace, one human owner and sole
authorizer, and several authenticated agent or device clients. The hosted alpha
must preserve the existing evidence, conclusion, verification, review,
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
## Delivery sequence

[//]: # (ob:72654777)
Each implementation stage lands as a separate reviewable PR, includes frozen
fixtures, and leaves the local Git-backed workflow usable.

[//]: # (ob:9079b321)
| Stage | Deliverable | Exit criterion |
|---|---|---|
| 0 — plan | This roadmap and public scope boundary | Product and implementation contract accepted; no hosted capability claimed |
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
The personal hosted alpha is complete only when one owner can initialize a
private workspace, issue and revoke separate agent/device credentials, use one
client to bind evidence and propose a conclusion, review it from another client,
retrieve the admitted current context from a third client, replay requests
safely, reject stale writes, export the complete governed record, and verify it
offline. No agent may act as the owner, and no source artifact or full trace is
centralized merely to complete the workflow.

[//]: # (ob:ce66da5f)
## Product meaning

[//]: # (ob:208f35c8)
Today Proofpress is a completed local, single-node governance control plane with
a Python SDK and loopback service. This roadmap would make the same governance
state available across one person's devices and agents. It is the first managed
deployment shape, not yet a team workspace or enterprise Cloud. If the alpha
works, adding multiple people becomes an extension in membership, authority,
policy, and operations; the claim/evidence lifecycle and portable verification
contract remain unchanged.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzg1MmNiMWMzOWY3YmMxNDc5MDllMWMzYyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjU3ZjM3M2MyIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9hODcwZjFjYjczYzIyMWIzMDVkNjEwNzkiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzFmNGZlMTk1ZTExM2U3MTlmYjFjMDc3YiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXW1z20aS_iso7Yf9sKAFAgQBSlVb5cjOJrdOrLO02Q-rlDwABiJWIMADQMlKnKr7EfcL75dcd0_PYEBRlCz59rb24ErKEgnMS0-_PP0y7V8PRNMVuUi7yyI7ODpYry_j0E-TaRos8ihJp7No4S0k_JoeuAdJnd1dZsWVbDt4tl0KP5wfxfD1Iov8IFxE01TGUzHPp1k-Ex58HSaZ8MJcJsKDT-GPN_f8XHhx4mVhms380INxs6JN6xvZ3B0c_Yq_dJeduIIZStHhVC78kMgSPvhJNkVeiKSUTiNviraoK2cJz9fNnZPcOadNXefrRrYtvLMW6bW4kripwcdN_XcJ2900OOCy69bt0eHhVdEtN8mrtF4dpktZrYrqqhPVVRx4h4O3G_kfmwJ-vty0srlM66qVFdCiazbyN_dgKQUSMYzyIApS_0B9cilv6CEgrrwUceTl0zTB7_1pEnhhNp960QJXVjcdbu2yLCoJK9cnUl5O81kORA7ldBrIaLrI4Xy8KErUdnh1l6lYt5sSNuzjOtO6ydqDo7_9esDT_3oAp1w3Lf6kvpbZZQIk_9sBTFZ1R2mdyU8HP8M-NE_A9Fmdtoenbz-cvf_x9bvL796fnb99c3ny_sfzD-_fXZ6-e_3j28sP71-_-eH16atVduB-ETuJrmuKZNPBKV4moi1aZCpZ5peiBep2ksbbdMu6wTVfFxUO2d61nVzBN5VY4eHaa3fh9RaZ4uCo2pQl7CRdwilKRYekrNNreMOfB95CJHN4HA6wk59wn6eyaetKlM53NYyfOSfwTVOXzmkpKum8LtdL4XyoBS6JFyKyjFa4Rk6Ut_DJ75ynjrISa3izu1vjDpBHgN8OfnOtNSYij6c0_tdd4x-ds050m_bIAc5Z1y0MU6zWpVwBFQWehIPzNXCCTl43jnrvlXMOUub0S16LRgzX68-9IPPEYL1vZEoiupdmv3Osx_ZQRHiLRIRh8MUz9ErBaZf1pswceFdWmdMtJWwWN4_EbGHCUk4qYCQHpgQqp_aS7u14Nl8EQe7Nv3g95zCtoLOC73BZsgUyr6XAVaBgVi2ok5TOQlT40US969T5nvXkkR_lM7nF1U2dwVBOvelgp_KRg7j_9L7zmOYw39x77nwfP37Ely6q97eVbH7fOiTIDmw6g0dS4OeLynEmf0T2BMXoJPWmgjEc-DKT1sGg5A9ZUfp-BPrmuQvD81nz4-0mTaXMWucWjAIyTAssUxaw0NapE1BSNxJWLJ1s05BR2ichkfTnUTpc1jcC9B1oezroK1IK-w5ox-N7Tmg-m3nhfJY-e8bPzutGCgf-uhFFSRus6lv4nfWP4mIYxPl8UX2eTCbmf_jVogVZtcHSQi_K4nDuD5b2bVP_AlRWowIgWD_Grztf2EMQOZv6gS-CF8z62fm-Uk8BGd5-WpdFWnTlHfIViKf-xqIGUuJ9hRxV3Ih9JInn01guZvFgceeiuZKdI5p0WXSAWjbNYzTZ_cYeoizmYe6LMH3JvEaWT-_AWlfO2Zs_O4fOB6W1_vI9CrL689n60fnu_Pz0zPmD0-4RZjnPvUXmi5es7vzdmQPWq5MNwDrSsgAVUflncl3Wd2j5HFndFE1d4c-vLBi5T6ADgHLzYDYbLO1EVHVVoPXYsqoZW4b2kfN70gD7gEMWgJIJkq-4qs_GQqMqIDkxGOGz84FGEqXcqQTeV_t4Pk-9MJzlyZYNLQv0BZwWsLasUvkofLj__B4CRf48nEVR9Pw534p0uU3IFhwWwA2gVMGQwX8wEDJMJxlBkfI8_eDu4acFeAFJ4E-fv7DPiO2uUDPxazQr6qmic9IGZKWhQ9xxTp7z3__5X_uOKgi8JBJyyO1sB9ApAj-NTIrC60V3Z3jkkeN76hj7VJjnR9Pc977u2ggHbBLQ8A4o9Uad81rclYCwYdiVKKrWASKjYKAxRETZiKpFtLLnmNNsnodp_JUJ-RrB0yEjp7SRAJG6QpStsxJ3GkEp5JRKV0N_mkfe7FnsNAjSWGRD4_AGwU5RwtJcgNI4tEsjrYorRaXHBPYJ7-857TwH9zcLvK-3JjzpvGiA8Et1DpZhAMORgTAlyAASDD27CXD2nQBavtpDPJHnwvO98Ost9C29wOgU3AZROejGw3HDOVdFjrwDKCQ16p5c_9Z1bsGFfnih4TzLfH_LZpzJdEPsh6sj9JLeOYloHjncPa_tOdMkzCPA7C9fwWfjFINlUrEajVMTuRQ3Bfi02_DsxIjLPgU490PfS7Oh3VDxqJR1A6j_R6iz6_k9ZAkWIgURFM-f87NzjkyRi1UBzGvRhOJG90mh7TrwCFB-Hz3STC5ACofcffr-xFlJ0QIiQ-l5DOzseHwPNcJU5LM08Z494zlhvra4qiawvw7cTnsF5OQBLGycdimQRFcYkkTVDqK-T6NnIhRTMQtftC58PqthEVUNtroUxcrpaj0CSLmDj6NCaovVpgTdI-tN6xT7IhSgfuJg4Q3dnT-DB2fhPthbUZYOhzWzR87r0Zf3Gek8kyLYMtLPX80AlP4IPrqC9fhxLoBAJBkVLALgWLtZrTsb-ezj62k6F5mI_a-0znMVM1jWBSrsrKbzpbnIBUlEei2rbFLJDQheaYLZqPLafWebztJ0Hm8j57yoCtopyHYGsORR6LzjhX0xnyBCrz19wayEqnQcc2nHEcDS6micU1egrSjmgtGVGiNEYNX2oSo5n4Mc5juDPiBFyAlPjH71T-9zs7w4DwDGPXe-8zoTdr4Cdy-saCRFIN1BUFKpIwAd22T42dUh_gOGo5eAAIWKn9M3OhgvLxdBmIdhLIWXYUBqkUXxwpcJWjVgTBqTsxAOZyGAd2V6va6LqqOkSkMzYXhd_4bR9Z8xfQFQ-c4awU5pWINQsuSZ2Y62zrtLYLcr2QAg4KRKm0yPZrmXpNMonQUL8KLyJF9IP8oW0XwaR8LPYi_O8iSaiQxgTj5P4vk8DoJFnE-nqQg9CkShlqfkiDqto5n3GxC6pcP25xMvngTT8-niaBodBd4fPO_IQ13GFEczEE4Df5FkwCf9p7_-o3IpxJgqz7EU7RKZbp5MZQJr9ySaJhrDSn0wz36FnAXPF-exlyULGWQEWNR8fRqD53tJ_gHotyFQjrod5OWi-qNTyVsTrYWVtvLYAWd325IuBThVWt3YCQHZkMckP4HebXG8DgUT55NgXNebTglmBmoeJtgCD_gL0I1G7_VURQFjimbTiBgdkOiMlxzZbtGyg4Aqn_EW_XKyBa1YySHo2OleMLnlPJVR6E9DEA9D7j4Lo4_3sfQKj7aY-4uFlME8IDmj0ayMS6_gnp1KIZ5aE0-B4NZ4ejvtwBGRkuA-0AUcl-t2LdBpxY-XmxX6PERnMpF1KS8qdpV_kY3ypTS58XME9ikF_Ti_0Oj8Asfx1VnbK7ioVpsWvSypAvy4OWIQRBO9Ew17SssNUtbFMIDB5C4zrXtRtRvcokpJqqXp452w1dC2onXA-0PsCcxUOUp9UxQJnssuKqP75Za07GGQSMZhmMyCPMpm-kitpJWOpb4gG2UdORH3osLjckTa1G2rmf2V870tjzU4rBSFpaMFVnDysrhaohfcojw5nWivwWMF_roFDsEzIGrDuSUSUzfo9OqjBKsCq1NqgyAypfYnwCPwBGkKwz97COUt0kR4Yh7EkVGUVjatl6Qn5cd40HkaRgsYw5vFRjytlBkP-rIkWCrZNeZojsWS_JqJZ6jgN_JwOmBWGqBeqxAusMBN0SL8_Psmu5K8Kms13_CwYAyKDvkcyU1noyNXnG-_qM4wc9bCYPe2dMKDNLJrCnnDYA9cfcQSrhobFu0Cb0xUPsXoRBaaiwrotiNpoEnvx570gM651xu-PiloMf5z03yWODJgB9YvQAmBvcg2mBRCBtfBl7YoiQLwDil7_KjDgLlYwwJuEOcpGmHtw8R8eFGRrlqDfqWjJtO4vkMl1IhbR4ODVkce0bCQZu219B6mB8Xuh-E8zqM0M0TqU5Q90z8t56hH9QBZLrJ4kXmRHtVKQ_KoL8sr_qknfitB1IGlW0cl2ZSx6aO1Gkq4AGZzmd6lMJOsrmA3rqPgqutcNWK9NDqbdql1M-sT5WOe2uaATDV8AI5m66BIApv3ukaxLQWJa8oAKNmg1SPaApahEwUCrPF4JyQBf8Igfb0C7tdDfmxk3lr1R4fXQKZSgmh-REeXmZFW1Uxa0AiK5VRMEE7GVQFpQVsArkNnc7N2WY_z2lThlVrcCfM8ZjknMC9KMD1d1vUa36acncNZPhPtxhdeD2ytSu0pEXI2La0zb-rVPSRE035P4bcOvfcTUZa4mQ04AgWyApYsgbg0ZCNJWZlzTiS4H2Axa_Cg4dUzRQfc-g282YMEYcfG0W1IizWGxlFiVcY2o_OHQXGddvRcB8WUdkrviA-ILBO1BoXeEHu7-gDRKZrAvJP2Vqw1ICmBj2BRH-WnNf10icLzUflWSL6_Gt65xXOE_0HhdzSl1tArpb1TazWIkCUd32rD6FkxGflWFGWGsd_RSnF1dnTB-HlakQztAmW3-RHXhCnAnWWF1DGvgcIv2IrkOemJ4TC7Qi1aT0dZHCdZNM8To4KswoBeBT01z8_jJl4wjWdx7sXTVI9rpf6NEnpJJt-GpoYtbXT62fkBlEMB8Ig_XslVArKP1vIKIN8vgoWyqG6KTv8CZ1aS4OLBghJCLxds0YdvXp-okz1j-dHpRVjwDpR7OIS4KJ5kYBBbMc5akbEtJWj31nV6nIXK4gb5JkeDSAt53QKemrTdHQqHxm-G195qKKIgio2LWdGU6mmjglnnHmo1i65QqwRF0Y4BJqh6Cb8qnq8kaYKVaK5lB24ErvXHmgbGcECrkDc8YZNXCZPRmmpeXjY4Lg1hHs3-KNBYH-k6qsKVl3QPcvVWobXCjShYGC1B1qk3DTynvdXW7eNaykxTAm617hR5NT8BGcAbQvOuTpqcKI3gtKOq805KeWk8oidnpgOEfoWEARxfGqdkRd_07zMSScHVASzbOD-dnjiqZFYz4ElZbzLn7N1rTTF2gawijzUcNFg-NiZK6xuzAMs5ByE9S5tiDXzxp9p1fjg5paHzBgyochYysYaTgIMFHf9pr75YhPEiTb08z0Pj0FhVM72-eHINjFZEMy9apNnCm4tcD2yVxWxj9ecVuShIwDartzH9szcw8r5QDMHmLa1jrJlOFyu-V48an7VPUvfQKCtglA7sT6MefsRFUGhJPUpCqjDLd6TaXjNkVV9bmAMLTrYsmTaAEzwHtn87SQfk-OZBq4MMzwQ5-_d3BUWMKaxM0KqXRjSQhNeGWVvt5-P7yAMTULrXJONcCyRLoFTL-kt5CQUKmiX7msbKLwMdUarpdppBwlCC-FzneXdu-g8TcIzkg6qJxmHt9IgTlCR-FHpg8dLY8LRVTKWdoBeURqkciG19YE1W5cIvQEAFThgAHwNrbBRHVrIj6aeNEYFKNKCFChK0mxwoh6ZrjwMzlxE47vMp-NTGwbZKsnpt8NyKKp4nl4u5iOI0Tch7VI5SX2Rl0MRLaqTARqGDWxqwhmRkzW-hbIAKgHV7B6SXZhC-IrNYzXg7-aYypupUZxDZa3Iy4FDgXTgLiZkWELEJ2y4FbjdcIsIrwV9pwQasGk9pgP-V6Wnr8gY4AI9VMrpyPhrtdVlkH4-NZ5TUWQHPpqKi4ye0DDPXFBHrNR6YN3GNe0KNDkyLTuAdqCYANCic2gNHmUSBZ5NHz3V9-p9cTULJRnk-vg2kufJFSCfUpWyPMTpHBQpgb0t5g5NwKIafItMAvxTav2H-JjEAgpJHpGmA_L1CJWwflYl10aPqWgTuDJdTc8jIjM5wjKpWeo-KqtXUaEuqTOurQ3Qxk9IoiEqAPhP1rP5sVcOK8XnrHHQtmnaizcNa-ns42hsoPrwCKH1FVR22VgfUJCwHmNefF7JhMMT6vJViBSP9WUkLAUc1KfnReExNvblaIt0-EiXwRfCWcdYGVKk8HkZzcUr2bUxJF_qeNd4-QXbIDPevLcddcxoCLJHqA1FCQ0iTl60UARkrjlCwtQJZFQlAb4x__vX1O6By9oAJcxXSGxpVtV3X2VQFnIQ63UPb0qqwLWxHo1hljVC_UwwAeezbAnMibBmJmdzddtK5XRZk-ygAQin13ozxkbAbbxaAZ3QHZwMb50XiNmC3D-CXY0VLtBUg3JUSODAiAEZFyZEWHZsB-5rS6TUSVVIuCvDU05JySaBAZWeiCxhivANdmaOfdD9AZ4XxVKxul7__duhfc2SiVYkEDDVQGZaGNQ5akGOkK0X4COToLQm1HhVk4G3YankrTKgiB4NAIXOVhgWE3TNcJLG5cVUslOI-5NY0MpUAy1GLKZVPOpD4TtyhqRnoGHXpihzJm7oAowQbwhO4n1FTuZ0-VYcADJ0e5xZ4AeivbchrsyWQC_Riqy3NoVzBXn9gIeNW3Hkr6Ow6nG_JJMekSXmzIc4K2xCqUN4QvmLhLtnWGkkOU7XKiTWFmPuckySMFtPEn8tF75xY5c12Ou5J5co87FQEcTCbL_IgMjDOqmDmYV9SkQwnBu56BmycU5jlosqLT2hgmVFKKbQBLHUgaUI6MyNhzkuwpyrEty_cvPDCRAhfzIWJyVsFzwZFvayAmfKL6HZitrhROWulZ1QdrwrqkJiIhoN5lADAZx5KQ4s0leCiglRXtWb4VKx1fI0yzKh5cBVTWsVDRT2fLSz6sNvhDk0X8GZXp3WpTgMNlnaZUVOozKvKnRjT07vq6sTwEm1rtGfdrEjl3VBEpQUU0PaGk_jfNrZkfQBEkojZyFJHv2nfPu17aKR05IKtH1u-Fly-lXB7A4JsRubMft0d6jDbtPHNVh3NPrSLaFUoRm3X0uOdduTAwEjOuBu0acyBixAMXXLURmxgMfZMarm8Y2NP-Ud1YLTzQPGddtwN8BqWcNuYOanrDo3z2tWFTSYY4G6F7_pItMu8q7MWwBREvUMVt-5MgrkdRsEVZrXwrQaU_diaELAH5I1hDA5eBrlQuyOTpDD5wG6jU5INwuZoko1FRirNiEocJtKxLFzudipBR0wmFEjvCp3gKNJebl09EEZgzJsuwUHwvFskFph8RzYN2b2ywJwKkGeTFehLX7Fms3xclIviatPo2Pf5ba0n0TFUFhN2vXqQuEukQN9y3YMOwCIRQiLCgLyDQLxELYclupyZoSdQvbpawidbIdNB9AGeAl1dTVZgDDAAMQxE6NoIk_BpNhVw4jXyhPGEwcgqHIpeG2dvUJPCbLRCci8VB5DG7BE8yMdNfzdfQ61ueS-ASZSYEyV2lOIqkAzzlVweAKhDiZLGPKAX8oKIJRtYNLE4lRuIjqLZMCmcnQaAJv3cR8Ip78tT6rhsy44bSqB9PixSOpVtkX-DhUacGkYeaBqZ6uIPVDOc4p2QrnG3KydU_YCCx_oq_l50IWQQzuI49qRvzKd1I6dHFy-4TWPqiuaLKMunIhR-b6nNBRs7e_7MyzHaLr7i1aoCHsvrFlnWDtKaBugx_fFvmAEtXF8ghNUirJXcoU6tyHvTeK73Lbn2R4_K3rm29wCE0On-t7P3P9rOOTF-q1ETCgErlmHgReNrLQsXlTpo7SxyILiVsNJ9Ya5QBokXpn6-mJuTt64Q8XG85PqPKDeo2vu0TeuqOJ4qUStBAfWlF68UWje-gW1HcC5tRLYDwxgYVXpDc-MEKUAYxdCMOIQqieFkfmK1RaukehRtXAsMNCoe60Gt1uCWqqEojYI9ysKR-7CH1tk0mfmBiKeZH2haWzegLAz_vBtMut4oW8CZBrnw5yaiaF1qsiTsuZeSNNgqyDflYPc2vqWSdFexPCWkMNNItYwcYFPhM2x0wqkgMBkY0Luo1PBKegZglYlt3z4yuJa0HcWWOWul1dExsBtHx09hq1eNhPEdSvZhHVc2AZPd54mwNE_H5O1YKN-DojkvKobc29CRIOsWuOzDIybop0R3D6fMsjSa-7GYLaK5qe7qr3tpt-wF17UYLOq8C6tSXLvSur1jbOkzl82yDrGxx08lePKTcvMuKktklfrReYVWC_swJPAKEAJBCwMlcMkqd4MHANQGqqhKAFcnaAjmI0TRadME0AIWcZigYf-B0QAXlaUCuBaHEbxVi6PRBVmB1MRDh0Bjny8aT6d-Opv63tzUB1hX4Hox_7K7bNp-xkkMOmMWS99U0lrX24yn-5J7albCl1LkqACXxdVyInHM9d39NCOFf1qKsNVkA5RbRkk84bTow-P6XQ1snUqsKA9cAqRCHQAsKzuBcUtdK9P7HNoZ4ciOnYkkV76i5kyZypQfc9jMCqf3xrlVgW5yas3aj_Hwl0UCNpaLejiSk2t4t6O4h5ZybrkVTGVOyAL_ELKwHOTjPmilA_SYHtO5MZ1bgUlvBQI2ymAiVNyUupDpDZDHwSTqqt_-W3QPUoNhAND8oi2vkowJSFTJhrYsaCGwdcS6WjqJJui3qPfIrTnmKBgo67JUIbZDrjR2wKOtMTLeE12fTMYeBiIRx4JLdpm1hnMmvjaILA-0DQNZl_dDOQYEDX18XEMeu1aLYDmWMOrKB8aNTMQPpiTNwQQw7EZZDR0y5yyy7fjg-aF2J56m-KPSV9og6uhAUfZOolPklqasrcysrsqi5xXhEoxbwgQFx8UpfgmioyOu2BjNwZMFonTFSiJ7uQ7JpfY-11hYYTvqxkUFyWpb4GM4MJnjDihbUUnOZKEp3ltGtcg9L8wWCzkzkUfrsmqvzp54-VTnPZMwTJJFnEaJMXHWfVSjx15yv3RQnGZlGhm-cByt1RbUwcEBTlKsy6BGuijR6mg5OdJEVcyIKx2hApt2upT9dOY3UoufnTPEETavX8s79tyU-7EnN3Hs6AiZnZSg4FlV0yUVK2Y0TDCcgBMq1d0CO4nQOnekF8gVp6wYlXepUJmuONuVULB0MFH4Qd9Ao2IC6WgS-vJjDCbQfkzACbRadw_ytxxnF0P0YErnsDqmNgWFHx6KFBWrlcwKrmZTppaGZQ-Kob4VX2BziKijL2B1vhUUkGQhItc375SXjznFCosRlEhJHeqzwvxki5xNxUBDMZJV4shz1m07YVpS-JijBrvKh7nAHc21qi9Xijyj2GzaxyTEFXrL6gqRley-X8jJeJJRWEvhGNZ0OujDABzOkrxuW2LwmFTVzg4spQsyBIU69mc65mE8S7ws8WdB75Gay-DWdYkn3e7mUQPpzWbRYuolXmxAWX_h23KKnnuDG6VF4XB9v0X55NYFF-K6nfdbkDgEozn8DATu0DAVaP20JQdojRNS1nZTWSFCOBUsz0DrwCJkAkat2_PgoTLpaCLAXdOKSDNSO4gpGYFviflM_YdiQU0HQuft1lWMlbjmhA4vw6FSb66CViPJwe0O2YKShg8vKh0p3AOvY5DuPJ7lMzkz9wCtK_LWST73zvtEXRnqQ_fq4hGcT64cWNgPMO3KBKJW6FySuJNC2OYOKwAEgg7q21UDTgqVEh0UvRatiZlkW4k1kf0dJLfqzL2SJ1ArifM4kHkmg7S_fNRf3O-l6Tl377XDk-fg6nhwIDMTcLCu4-8qYfrSG_W2kf8eb4Nb5WuHipYYytXRW53om3PE12SuWah1YpFybldcBWzqfBls9_EQNFlFxrGirCZzoaeY8RQcTMAgBkqtss1WvQWo5WtlfYDTKYYF6J_m16NPWjDPiKBQbiThC7WSbygThYqpsz0FEFs0c3W_lpD8gbS5W1NARyBmUmksVUlbV2BbVj3APXZywhjIb4Rl0MIaIiEiBuYjf_nGFAC95_g1m0US7WzT9DQPkCCcGzCPKVdDY2tVrWXFCbSHd8xWlBTJhK121tcnDK-TmBprkxUzBwWwhERRubxAwk1RdiBvD13bGGAGjIodO--_f3OigJBV8d1PxahBxZX22TM_EUnkyWwRzs01BKsJRK-vnt3HQTnrE5VPRUV1UcFwdyqWlUhdqJAZ6MK5J4RDpLpV7ak-9kEcMMULM2TJRHa3R88sciEWszzPoiTq6xNMEwm7PuFpPSE09aTn--k0T_NZHwnr20TY6YJndn1AN44UCjnOFOXfvhoM5nMjdc0dlkj2KvnBfCqi9BqrqjnPBZYHI1KPX63UYA_vmauyPE6JqYFcPAu-2UhVg3yf0USytLVR78IzBfji_G5fBUUeRwvGm4qXtDXmeiBdvM9usH37urdqCqlY8U1w3ruLitOCr5wfa4MHkM86Xf7CpWD4Gig_DgWa_Bu6UybiAIQH-mHQiU4HY0QNci3Qsr_ysJRGne_hz2CaTSU2wvaoI7hClX1Tj_uXcPe26dBh2jyNAYXMU5maXJbVuUMz5wt6ccitq-1oVTCcbd0RGNyf09HJYYnKLd2lR1y23QhAEKxU8FWY25Kc8qSL8iRVvzfXrXvVqcK-hTpUlUlgG4gwzugQAENrTgPcoQVwOq2mlB8yvIlEiQAGWqaMnh5GHJuZqlu897SWNf6lrm1zlVyH5oru7OgLUcsCL8lpfxWzeOxxqntv7LK3qnCTQOKhEdE-CDBIpNvRfMTkHHNgi2CKWe5x48-_Ie_saJcOdq7b3SydGrCjV_HAt_saratu8rLth6abYkeAdQCgZhNsQP9P346ddvSSbuxf3JR3VWdUyrqvidOXN7W9P-q9XrRf2qDzKQv15wvf85PF129d-cPJKefQlT7rS2zu1Y-xQVbCtq9D6UtaeD1IDZADEusH2eL-ANyq6Ida3zCg0uKzDkDQijQAXVNGCjQyl40y57xrVaDaMxZXN19LuaZANepk87DyBzZXXLisk2igOh7gtgfX-hprGmBFEyodLBmZUKmQ6TSQ99pf1xnaxuXVQ9y4f1Ick-iD9ABrQ9ukjakYLEe7gSr4pEKeE51Dzwx7o-_w6iHe3eJEnv7bRspfONSAk_cs2JdyVaJpwKfp6hrDZFSj72roRTkfAqK6aq0Xg94yvHqIRx8kyxtkipZvAggTibNv0fB1RCYKQ2_szwFqA11b1a9BrbftM5LYt4Uq05WT2XuMzFC42J8t6fn14HZ5x5zcMzJXniHJBlzbPYiiVVyjM9GxvsJpifBVp0ZV3IPRBLl6XCcKug7-mmxtCyw38iKV_hbXCOwUobDD1ZM7ju35B0_UcditxOw2WnZ7sV9H0zGajp2m4-n97bb7u03dfuCj2W-7W7k91tfuqzSvW4RZ4qW-zLIoCpM48NM0T0Lfn3nTqSflbJ773tyfLZKZHyVeDrT05CzyfXDmQzH1s6dsbkcju9nsyAt3NLIz_3zR2MhubGQ3NrIbG9mNjezGRnZjI7uxkd3YyG5sZDc2shsb2Y2N7P4xjewWszAAPSai2F-MjezGRnZjI7v_rUZ27gMt7FwjEl-QYbjf9k5wWuGhtne0St1nRqUb_vL9_00vvMiT01kaR8E0nz67Fx78fC_VMfbHG_vjjf3xxv54Y3-8sT_e2B9v7I839scb--ON_fHG_nhjfzx1DchfhF44jcR8PvbHG_vjjf3x_t_3x3PvpSfUDkwtZx9venbLvF0BLS4R_ar99Hgn-BRO8Yyeesf0orq9jV7CAB4b-w_7X47N9sZme2OzvbHZ3ths75-62V6QhEGahX4YZ2lf1WlKmi3Wf2458rBwgtZ0UalCNNu1VaFFrO7iq8W6AP5emz11V-HIQrcXVVa0Sse79xNs7SZhORgkE3v1t11Ep1hBJffY6igtNmmp1vShDCMBZb59UFevOEkKdLObvRlEh1eGrZKdvumE6VG17TCqPeirecbZtyWfzhuzI7p5FDIhJUKMEbSvbIw9GMcejGMPxrEH49iDcezBOPZgHHswjj0Yxx6MYw_GsQfj2INx7ME49mAcezD-y_VgTFJv5gVRCBAh_dfpwfgtBUf6lI75Z7yt5os_MTcbHbuzo8YJtgxynZNSgINMv8EvmwYkhrhfVXdvNag4Nn34NkWZWQl8bvGom26M_SLHfpFjv8ixX-TYL3LsFzn2ixz7RX7FfpE___Y_IBlFgQ)
