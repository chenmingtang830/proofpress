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
| Existing Python SDK plus a remote HTTPS transport | TypeScript, Go, MCP, or framework adapter matrix |

[//]: # (ob:8618e948)
## Target architecture

[//]: # (ob:965f2a5c)
```text
Python SDK / Review UI
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
| 4 — remote service and Python transport | HTTPS-compatible service boundary, remote SDK transport, readiness, safe errors, limits, audit logs, and deployment configuration | Two remote clients pass the same supported conformance vectors as local clients |
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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzg1MmNiMWMzOWY3YmMxNDc5MDllMWMzYyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImQ1MTMyOWJkIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85MzVmNTU4ZWEwZDI3ZTI5ZDc4OTJlYjciLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzFmNGZlMTk1ZTExM2U3MTlmYjFjMDc3YiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq9XG1z20aS_itTug_7YUkLJEgQsKq2SpG9m9x6bZ2l2_2wSskDYCBiBQI8DCiZiVN1P-J-4f2S6-7pGQwoGXIk16WSikQB89LTL08_3cNfj2TblYXMuusyP3p9tN1ex8t5ls6yMClWaTZbrJIgUfBrdjQ5Spt8f52XN0p38Kxey_kyep1li1QFkQwXabaaR0G4yhezTM7UMlwsiyCJoiCZR_k8krMkjYJoOSsWs0Qt02geLmcyhnHzUmfNnWr3R69_xV-6607ewAyV7HCqCfyQqgo--Ltqy6KUaaVEq-5KXTa1WMPzTbsX6V6ct01TbFulNbyzldmtvFG4qcHHbfMvBdvdtTjguuu2-vXx8U3ZrXfpq6zZHGdrVW_K-qaT9U0cBseDt1v1X7sSfr7eadVeZ02tVQ2y6Nqd-m1ytFYShZgvZ-E8SfMj88m1uqOHQLjqOgmXxXIZKxnk85WaJ_kqTuYqXeHKmrbDrV1XZa1g5fZEqmuQWKFmyVLNZqFazZICzidYrVKzHV7ddSa3elfBhue4zqxpc330-p-_HvH0vx7BKTetxp_Mn1V-nYLI_3kEk9Xd66zJ1eejn2EfVidwL02mj8_ffrz48P703fWPHy4u3765Pvvw_vLjh3fX5-9O37-9_vjh9M3fTs9fbXDDv0edZNe1Zbrr4BSvU6lLjUqlquJaapBup2i8XbduWlzzbVnjkHqvO7WBv9Ryg4frr30Cr2tUiqPX9a6qYCfZGk5RGTmkVZPdwhvzKAwSmUbwOBxgpz7jPs9Vq5taVuLHBsbPxRn8pW0qcV7JWonTaruW4mMjcUm8EJnntMItaqK6h0_-TXzrKBu5hTe7_RZ3gDoC-nb028RbYyqLeEbjf981_klcdLLb6dcCNGfbaBim3GwrtQEpSjwJgfO1cIKiaFph3nslLsHKRL_krWzlcL1o-HkgB-t9ozIy0VGZ_ZvwHhuRiAySVC6X4e-eoXcKQq-bXZULeFfVuejWCjaLm0dhapiwUtMaFEnAlCDlzF_Sgx0voiQMiyD63eu5hGklnRX8DZelNIh5qySuAg2z1uBOMjoLWeNHU_OuaIqR9RSr-apYqAOtbpschhLNroOdqicO4uHTY-cxK2C-KHjufJ8-fcKXruoP97Vq_6AFGbKATefwSAb6fFULMf0Tqic4RpE2uxrGEPDHXHkHg5Y_VEU1n6_A3zx3YXg-W35c77JMqVyLewgKqDAaVKYqYaFaNCk4qTsFK1Yi37UUlMYsBLx9tMqGy_pBgr8Db08HfUNOYeyAHnl85ISixSJYRovs2TN-EaetkgL-dyfLijZYN_fwO_sfo8UwiPhyVX-ZTqfuP_jVkwVFtcHSlsEqj5fRfLC0P7fNLyBlMyoAgu1T-vroCyMCUYvZPJzL8AWzfhE_1eYpEMPbz9uqzMqu2qNegXnav3jSQEl8qFGjyjs5JpI4msUqWcSDxV3K9kZ1QrbZuuwAtezap2Ty-BsjQkmiZTGXy-wl8zpbPt9DtK7FxZu_imPx0Xit__wJDdn888X7Ufx4eXl-If4o9IgxqwgQZD6XL1nd5bsLAdGrUy3AOvKyABXR-edqWzV7jHxC1Xdl29T48ysPRo4ZdCjjVRQuFoOlncm6qUuMHgdRNefIoJ84v28aYAw45CE4mTD9jqv64iI0ugKyE4cRvoiPNJKs1KNO4EM9pvNFFiyXiyI9iKFVibmA0IC1VZ2pJ-HDw-dHBAQpynKxWq2eP-dbma0PBakhYQHcAE4VAhn8CwOhwnSKERQ5z_OPkxF9SoJVkobz2fMX9gWx3Q16Jn6NZkU_VXYia8FWWjrER84pEP_73_8zdlRhGKQrqYbaznEAkyLI0yikGLxednunI08c37eOMebCgvlqVsyD77s2wgG7FDy8AKfemnPeyn0FCBuG3ciy1gKEjIaBwRARZStrjWhl5JizPCqWWfydBXmK4OmYkVPWKoBIXSkrLTZybxGUQU6ZmljoT_Oou5HFzsIwi2U-DA5vEOyUFSxtAlAah57QSJvyxkjpKYP9hvdHTrsoIP3Nw-D7rQlPuihbEPzanIMXGCBw5GBMKSqAgkDPaQKcfSdBlq9GhCeLQgbzYPn9FvqWXmB0CmmDrAWm8XDccM51WaDuAArJnLun1F9PxD2k0F9f6DLK8_n8IGZcqGxH6oerI_SS7UUq2ycOd-S1kTNNl8UKMPvLV_DFJcUQmQxXY3FqqtbyroSc9hCenTlzGXOA0Xw5D7J8GDcMH5WxbwD3_4R0Hnt-RCxhIjMwQfn8Ob-IS1SKQm5KUF5PJsQbPRSFjeugIyD5MXlkuUrACofaff7hTGyU1IDI0HqeAjuPPD4ijWUmi0WWBs-e8ZIwny5v6insr4O0018BJXkAC1uh1xJFdIOUJLp2MPUxj57LpZzJxfJF68Ln8wYWUTcQqytZbkTX2BHAygU-jg5Jl5tdBb5HNTstyjGGAtxPHCbBMN35K2RwHu6DvZVVJZjWzJ84rydfHgvSRa5keBCkn7-aASh9Dzm6gfX4cSFBQGQZNSwC4Jjebbadj3zG9HqWRTKX8fw7rfPScAbrpkSHnTd0vjQXpSCpzG5VnU9rtQPDqxyZjS5Pj51ttsiyKD5EzkVZl7RTsO0cYMmT0PmRF8Y4n3CFWXv2glkJVVkec-3zCBBpLRsnmhq8FXEuyK40yBBBVBtDVSqKwA6LR0kfsCLUhG9kv_qnx9KsIC5CgHHPne-yyaVfr8DdS4-NJAZyMiAljTsC0HEohp8nluI_Yjh6DQhQGv6c_mLJ-NHyAygmjclVCMFVCNBdld1um7LuqKjS0kxIr9vfkF3_GcsXAJX33gh-ScMbhIolz6x26KborkHdblQLgICLKjqdvV4UQZrNVtkiTCCLKtIiUfNVnqyiWbyS8zwO4rxIVwuZA8wpojSOojgMk7iYzTK5DIiIQi9PxRFzWq8XwW8gaE2HPY-mQTwNZ5ez5PVs9ToM_hgErwP0ZSxxv-rzm_fpr_9ftRRSTFPnWEu9RqWL0plKYe2BwtBEY3ilD9bZ71Cz4PniIg7yNFFhToDFzNeXMXi-l9QfQH47AuXo28Feruo_iVrdO7YWVqrViYBk9zCSriUkVdbd-AUB1VLGpD6D39U4XoeGifMpCK7bXWcMMwc3DxMcgAf8BeRGo_d-qibCmNhsGhHZAYXJeMXMtsbIDgZqcsZ7zMspFmi5UUPQ8Wh6weJWUaZWy_lsCebhxN1XYezxPlVe4dGSaJ4kSoVRSHZGo3kVl97BPbuUQjq1JZ0Cw23w9B6NA69JlAT3QS6QuNzqrcSkFT9e7zaY85CcKUQ2lbqqOVX-RbUml7Lixs8R2GdE-nF9obX1BebxzVn7K7iqNzuNWZYyBD9ujhQE0USfRMOesmqHkp0gDeAw-YSVdnJV6x1u0ZQkzdLs8U45athYoQVkf4g9QZlqYdw3sUjwXH5VO9-vDqxlREFWKl4u00VYrPKFPVKvaGW51BdUo7wjJ-Fe1XhcQmZto7VV9lfiJ98eG0hYiYWlowVVEEVV3qwxC9ZoT6KT-hYyVtCve9AQPAOSNpxbqrB0g0mvPUqIKrA64zYIIlNpfwo6Ak-Qp3D6MyKoIMlSGcgojFfOUXrVtN6Svqk-xoNG2XKVwBjBInbm6ZXMeNCXFcEyxakxszmeSvJrjs8w5DfqcDZQVhqg2RoKF1TgrtQIP_-1y28Ur8pbzQ88LASDskM9R3HT2VjmiuvtV_UFVs40DPZgS2c8SKu6tlR3DPYg1UcsMTFjw6InoBtTU09xPpGN5qoGuT1SNLCin8eBCkDORdAHvr4o6Cn-c8t8njkyYAfVL8EJQbzId1gUQgW35IsuK5IAvEPOHj_qkDCXW1jAHeI8IyPsfZi6D69q8lVb8K901BQat3t0Qq28FxYcaMs8YmAhz9p76RGlB8c-Xy6juFhluRNSX6Lslf7bao521ACQZZLHSR6s7KheGZJHfVld8S-98LUCUweV1sIU2Uyw6dlaCyUmAGYLle0zmEnVN7CbiTBwdSJuWrldO59Nu7S-mf2JyTHP_XBAoRo-gERTCzRJUPPe1xi1JZK4oQqAsQ1aPaItUBk6URDAFo93ShbwFyTpmw1ovx3yU6sK7fUfHd-CmCoFpvkJE11WRlpVO9XgEYzKGU4QTmZiCGlJWwCtw2Rzt52wH-e1mcYrs7gz1nmsck5hXrRgerpqmi2-TTU7wVU-x3bjC6eDWGtKe8aExE7TOou22TxAQjTtT0S_dZi9n8mqws3sIBEoURWwZQnMpaUYSc7KnXOqIP2AiNlABg2vXhg54Nbv4M0eJEifG8e0ISu3SI2jxZqKbU7nD4PiOn323JJixjtle9IDEsvUrMGgN8TeE3uAmBRNYd6pvpdbC0gq0CNY1Cf1eUs_XaPxfDK5FYrvH0537vEc4T9w-B1NaT30xnjvzFsNImRFx7fZMXo2Ska5FbHMMPY7WimuzmcXXJ5nHckwLlB1mx-ZOJoC0ll2SB3rGjj8kqNIUZCfGA7zGNVi_fQqj-M0X0VF6lyQ1xjQu6BvrfPzuGkQzuJFXATxLLPjeqV_54ReUsn3oalTSx-dfhF_A-dQAjzijzdqk4LtY7S8Acj3i2SjLOu7srO_wJlVZLh4sOCEMMuFWPTxh9Mzc7IXbD-2vAgLfgTlHg8hLponBRjEVoyzNhRsKwXeXU9Ej7PQWdyh3hQYEGkhpxrw1FR3ezQOi9-crr21UMRAFB8Xs6OpzNPOBbPPPbZuFlMhbQzFyI4BJrh6Bb8ana8VeYKNbG9VB2kErvV9QwMjHaAN8oYnfPEaY3Je08zLy4bEpSXMY9UfDRr7IyfCdLjykh5Arj4qaI9uRMNCtgRVp9m18JzNVvWk57VMmKYC3GbbGfFafQIxQDaE4d2cNCVRFsHZRNXWnYzzsnjETs5KBwj9BgUDOL5yScmG_tK_z0gkg1QHsGwr_n5-JkzLrFXAs6rZ5eLi3amVGKdAXpPHFg4aIh8HE-P1XViA5VyCkV5kbbkFvfhLMxF_OzunoYsWAqhJFnK5hZOAgwUf_3nUXyTLOMmyoCiKpUtovK6Z3l98cw-MdUSLYJVkeRJEsrADe20xh1j9eU0uBhJwzOpjTP_sHYw8RsUQbD7wOi6a2XKx0XvzqMtZ-yJ1D43yEkbpIP605uEnUgSDlsyjZKQGs_xIru2UIav5s4c5sOHkIJLZADjFc-D496joQBw_fDXqoMKzQC7-411JjDHRygStemvEAEl4bVi1tXk-vo86MAWne0s2zr1AqgJJafZfJkso0dA827cyNnkZ-IjKTPdoGCQMJUnPbZ330U3_cQqJkfqqa6Jx2Ds9kQSl6Xy1DCDiZbHTaa-ZyiZBL2iNMjUQP_rAmrzOhV9AgAacMAA-AdXYGY2sVUfWTxsjAVUYQEtDEuhdAZLD0DWSwERqBYl7NIOc2iXYXktW7w2e21HF8xQqieQqzrKUskeTKPVNVg5NvKRHCmIUJriVA2soRvb8HsoGqABYt09AemsG4ytzT9VctlPsaheqzm0FkbMmkYOGgu7CWSistICJTTl2GXC74xYRXgn-Sgt2YNVlSgP8b0KPbqo70AA8VsXoSnxy3uu6zD-duMwobfISns1kTcdPaBlmbogR6z0ehDd5i3tCjw5Ki0ngHlwTABo0TpuBo02iwXPIo-e6vvxPqSahZOc8n94GytzkIuQTmkrpE2TnqEEB4m2l7nASpmL4KQoN8Etp8xvWbzIDEChlRFYGqN8bdML-UTmuix411yJwZ7ichikjNzrDMepa6TMq6lYzo62pM63vDrHNTMajICoB-UzNs_azTQMrxue9c7C9aDaJdg9b6-_haB-g-PBKkPQNdXX4Xh1Qk_QSYF5_UaqWwRD7c63kBkb6q7EWAo5mUsqj8ZjaZnezRrl9Ikngi5At46wtuFJ1MmRzcUrObVxLF-aeDd4-QXXInfZvvcTdahoCLJnZAzFGQ0iTl20cAQUrZig4WoGtyhSgN_Kf_zh9B1LOvxLCJgbpDYOq2e5E7OoSTsKc7rEfaQ1tC9uxKNZEI_TvxAGgjv25xJoIR0ZSpsnjcVLcr0uKfUSAUEm9D2N8JJzGuwXgGe3hbGDjvEjcBuz2K_jlxMgSYwUYd20MDoIIgFFZMdNiuRmIrxmdXqvQJRWyhEw9q6iWBA5UdY5dQIpxD76ywDzpIUHn0XiGq3ss3387zK-ZmdCmkIBUA7VhWVgjMIKcoFyJ4SOQY7ckzXoMycDb8N3yAU1omIMBUchaZWEBYfccF0lq7lIVD6VMvpbWtCpTAMvRixmXTz6Q9E7uMdQMfIy5dEWJ5F1TQlCCDeEJPKyomdpOX6pDAIZJj7gHXQD52xhy6rYEdoFZbH3gOUwq2PsPbGQ84J0PSOeJ4HpLrpiTJufNgTgv_UBoqLwhfMXGXYqtDYocptImiXWNmGPJSbpcJbN0HqmkT0689ma_HPdN7co87EyGcbiIkiJcORjndTDzsC_pSIYTg3Q9BzUuiGa5qovyMwZYVpRKSRsAK0skTcln5mTMRQXx1FB8Y3RzEixTKecyko6T9xqeHYp6WQMz1Rcx7cRqcWtq1sbPmD5eQ-qQmciWyTwqAOAzXytDyyxTkKKCVdeNVfhMbi2_RhVm9Dy4ihmt4mtNPV88LPr1tGMyDF2gm12TNZU5DQxYNmVGT2Eqr6Z24kJPn6qbE8NLtNp5z6bdkMu7I0ZFAwrQfeAk_feDLUUfAJFkYj6ytOw37XtO-x4GKctccPTjyKch5dvISR9AUM0onPmvT4Y-zA9tfLPVstnHfhOtoWLMdj0_3tlEDgKM4oq7Q5suHEwQgmFKjt6IAyxyz-SWqz0He6o_mgOjnYdG72zi7oDXsIXbx8xp03QYnLcT29jkyIDJAX3XM9ET1l1btQClIOkdG966cwVmPWTBDWb18K0FlP3YVhCwB9SNIQcHL4NdmN1RSDKYfBC3MSnJB7Q5hmQXkVFKC5IS00SWy8LlHpYSLGMyJSK9K22Bo8x6u53YgZCBcW9OCA5C5q1RWBDyhWpbintViTUVEM8uLzGXvmHP5uW4aBflza613PflfWMnsRwqmwmnXj1IfMykwN9y34MlYFEISxLCQLwDIl6hl8MWXa7M0BPoXifWwqcHlOmAfYCnwFfX0w0EAyQghkSE7Y1wBZ92V4Mm3qJOuEwYgqzBoZi1cfUGPSnMRiuk9NJoAHnMHsGDfdz1d_Mt1OrWDwhMkkREknikFdeAZJiv4vYAQB3GlCzmAb9QlCQs1cKiScWp3UB2xGbDpHB2FgC68nPPhFPdl6e0vKzmxA0t0D8fNilbyvbEv8NGIy4Now60rcps8we6GS7xTsnXTA47J0z_gIHH9ir-KLqQKlwu4jgO1NyFT-9GTo8uXnCbxvUVRckqL2ZyKed9pHYXbPzq-TMvx9i4-IpXaxp4vKxb5rkelDUd0GP54_9hBoxwfYMQdouwV5oMfWpN2ZvFc31uyb0_dlTOzm28ByCESfe_X3x47yfnpPjaoiY0AnYsQ-LF4mtrC1e1OWibLDIRrBWsdIzmWqowDZbZvEgid_LeFSI-jpdc_5HVDl17X7bRE8PjmRa1ChxQ33rxyqB1lxv4cQTnskHkkBhGYtT4DauNU5QAYRQnM9IQ6iSGk_k7uy1aJfWj2OBaItFodKwHtdaDe66GWBoDe0yEo_RhRNb5LF3MQxnP8nloZe3dgPIw_PNuMNl-ozyBMw0LOY8co-hdavIs7LmXkizYKik3ZbL7EN9SS_rEqDwVpLDSSL2MTLAZ-gy_6IRLQRAykNC7qs3wxnoGYJWF7d8-criWvB1xy1y1su7oBNSN2fFz2OpNq2B8QcU-7OPKpxCy-zoRtuZZTt7nQvkeFM15VTPkPoSOBFkPwGVPjzjSz5juiKYs8mwVzWO5SFaR6-7qr3vZtOwF17UYLNq6C7tSXLvxun1i7PmzCYdlS7Fxxk8teOqzSfOuas9kjfuxdQVtjX1ICbwChEDQwkEJXLKp3eABgLRBKqYTYGILNATzEaLYsmkKaAGbOBxp2H_gPMBV7bkA7sVhBO_14lh0QVEgc3zoEGiM5aLxbDbPFrN5ELn-AO8KXG_mv-8um42fcRqDz1jEau46ab3rbS7Tfck9Na_gSyVydIDr8mY9VTjmdv-wzEj0jyaGraEYYNIyKuJJoTGHx_VPLLAVtdxQHbgCSIU-AFRWdRJ5S9sr0-ccNhlhZsevRFIqX9OXM-WmUn7CtJlHp_fBWRuim5Jat_YTPPx1mUKM5aYeZnIKC-8eae6hpVx6aQVLmQuyoD-ELLwE-aQnrSxBj-UxWxuztRWY9F4iYKMKJkLFXWUbmd6AeAQWUTf99t9iepA5DAOA5hcbeY1lTMGiKg60VUkLga0j1rXWSTLBvMW8R2nNCbNg4KyrylBsx9xpLCCjbZAZ74VuTybnDAORiPDgkt9mbeGc49cGzPLA2zCQnfB-qMaAoKHnxy3k8Xu1CJZjC6PtfGDcyEL86FrSBBaAYTcmaljKnKvIfuKD54fenXSa-Efjr2xAtOxAWfVJoigLz1M2XmXWdmXR80ZwKfKWMEHJvDjxl2A6lnHFL0YTeLIglK7cKFSviSC7tNnnFhsr_ETdpahgWVqDHsOBqQJ3QNWKWnElC0PxaBtVUgTBMk8StXDMo3dZtXdn33j51NY90-UyTZM4W6UuxHn3UZ0fe8n90kFzmldpZPjCPJq2EVTg4AAnietyqJEuSmjLllMiTVLFirjxEYbY9MulnKezvpFb_CIuEEf4un6r9py5mfRjpDZxIixD5hcliDyrG7qk4nFGwwLDGSShytwt8IsIWuzJL1AqTlUxau8yVJntOHusoOD5YJLwV3MDi4oJpGNI6NuPkUyg_TjCCbxa9wDya-bZ5RA9uNY57I5pXEPhx68xReVmo_KSu9lMqKVhOYNiqO_xCxwOEXX0Daziz5IISTYiSn2LzmT5WFOssRnBmJSyVJ9H81MsEruagYZRJK_FkedstJ6yLIk-ZtbgsfZhbnDHcG36y40jz4mbzXpOQt5gtmyuEHnF7oeNnIwnGYVpomPY01nShwE4nCVl3b7F4DGZrp1HsJRtyJBEdYxXOqJlvEiDPJ0vwj4jdZfBvesS33S7m0cNVbBYrJJZkAaxA2X9hW8vKXruDW60FoPD7f0Wk5N7F1xI6x6934LCIRjN9DMIuMPAVGL0s5EcoDVOSFXbXe1RhHAq2J6B0YFNyBFGetLr4LEJ6RgiIF2zjsgqkh5wSs7gNSmf6_8wKmjlQOhcH1zF2MhbLujwMgS1enMXtBlJDW53KA1OGj68qi1TOAKvY7DuIl4UC7Vw9wC9K_LeST73zvvUXBnqqXtz8QjOpzAJLOwHlHbjiKgNJpdk7uQQDrXDI4DA0MF9T8yA09KURAdNr6V2nEl-UFiT-b_AcuvO3Sv5BmmlcRGHqshVmPWXj_qL-701PefuvU14igJSnQAOZOEIB-86_mMtTL_3Rr0f5H_C2-Be-9qxkSVSuZa9tYW-iBlfV7lmo7aFRaq53XAXsOvzZbDd8yEYssqcuaK8oXBhp1jwFEwmIImBVmtis9dvAW751kQf0HTisAD90_x29KmG8IwICu1GEb4wK_mBKlHomDo_UwCzxTDX9GtZUj6QtfstEToSMZMpY5lO2qaG2LLpAe6JKAhjoL4RlsEI64SEiBiUj_LlO9cA9IH5aw6LZNr5ru1lHqJAuDbgHjOphsXWplvL4wlshnfCUZQcyZSjdt73Jwyvk7gea1cVcwcFsIRM0aS8IMJdWXVgb1-7tjHADMiKnYgPP705M0DI6_jup2LUYHilsXg2T2W6ClSeLCN3DcH7EojeXz37exxMsj419VR0VFc1DLc3XFaqbKNC7qAL154QDpHrNr2n9tgHPGCGF2Yoksl8P-JnkkLKZFEU-Spd9f0J7ksk_P6Eb_tOCCs9Fczn2azIikXPhPVfE-GXC575rQ-YxpFDocSZWP7Dq8EQPnfK9txhi2Tvkr9aT0WU3mBXNde5IPIgI_X01UoL9vCeuWnL45KYGWiCZ8E3G6lrkO8zOibLRhvzLjxTQi7O7_ZdUJRxaAje1LxkozH3A9nmfU6D_dvXfVQzSMXjNyF5765qLgu-Eu8bhwdQzzrb_sKtYPgaOD-mAl39DdMpxziA4EF-SDrR6SBH1KLWgiz7Kw9r5dz5iH6Gs3ymZsEqCZaBQ5X9l3o8vIQ7-jUdlqYtshhQSJSpzNWyvG_usMr5gu_iUAdX2zGqIJ3t3REY3J-z7OSwReWe7tIjLjv8IgBJsNLAV-luS3LJky7Kk1X9wV237l2noX1Lc6imksAxEGGc8yEAhrZcBthjBBCddVMmDxneRKJCAAMt10ZPDyOOzV3XLd572qoG_2eubXOXXIfhiu7s2AtR6xIvydl8Fat4nHGae2-csmvTuEkg8diZaE8CDArpPpuPmJw5B44IrpnlgTb-_Bv8-3-9ZDpL)
