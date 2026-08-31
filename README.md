[//]: # (ob:6ec771b4)
<p align="center">
  <img src="assets/logo.svg" alt="Proofpress logo" width="88" height="88">
</p>

[//]: # (ob:de7999eb)
# Proofpress

[//]: # (ob:7542280e)
[![npm version](https://img.shields.io/npm/v/proofpress.svg)](https://www.npmjs.com/package/proofpress)
[![npm next](https://img.shields.io/npm/v/proofpress/next.svg?label=next)](https://www.npmjs.com/package/proofpress)
[![CI](https://github.com/chenmingtang830/proofpress/actions/workflows/ci.yml/badge.svg)](https://github.com/chenmingtang830/proofpress/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

[//]: # (ob:e667d986)
**Proofpress — The Governance Layer for Agent-Produced Knowledge.**

[//]: # (ob:0e0e9d9a)
Agents don't just consume enterprise knowledge. They create a new knowledge
layer. Proofpress governs it.

[//]: # (ob:92fbc10e)
Proofpress gives a checkable answer to: **What may a future agent or human rely
on, why, and under whose authority?** It governs selected conclusions, claims,
and decisions produced through agent research, reasoning, and work—not the
enterprise knowledge agents start from.

[//]: # (ob:815b673d)
> Existing knowledge infrastructure organizes what agents reason from.
> Proofpress governs what their reasoning produces.

[//]: # (ob:2e6c722b)
![Agent-produced knowledge can outgrow enterprise knowledge as agent adoption and autonomy increase](assets/architecture/agent-produced-knowledge-growth.png)

[//]: # (ob:4ccd51b9)
## Quickstart

[//]: # (ob:d6f9f208)
Proofpress 0.5 is published on npm's `next` channel. It requires Python 3.11+,
Git, and Node 22+. Start with a clearly labeled synthetic ledger so the review
queue, admission boundary, and downstream context are visible immediately:

[//]: # (ob:7b197ac1)
```sh
mkdir proofpress-quickstart && cd proofpress-quickstart
git init
npm init -y
npm install --save-dev proofpress@next
npx --no-install proofpress setup --agent codex
npx --no-install proofpress demo
npx --no-install proofpress ui --scope demo
```

[//]: # (ob:33500636)
`demo` creates one admitted conclusion, one awaiting review, and one rejected
conclusion. It only runs when no Proofpress knowledge ledger exists, so synthetic
records cannot be mixed into an existing ledger by accident. To govern your own
agent output instead, replace the last two commands with the minimal real-data
flow:

[//]: # (ob:e719e2b5)
```sh
npx --no-install proofpress evidence import \
  node_modules/proofpress/examples/verified-knowledge-ledger/demo.otlp.json
npx --no-install proofpress propose --statement "The current conclusion" \
  --evidence EVIDENCE_ID --scope demo --proposer agent:runner
npx --no-install proofpress evaluate CONCLUSION_ID
npx --no-install proofpress review CONCLUSION_ID \
  --admit --reviewer human:reviewer
npx --no-install proofpress context --scope demo --actor agent:successor
npx --no-install proofpress ui --scope demo
```

[//]: # (ob:20fbea6e)
Each command prints the identifier needed by the next step. For the review UI,
agent adapters, legal fixture, and full walkthrough, see the
[verified-knowledge ledger guide](docs/VERIFIED_KNOWLEDGE_LEDGER.md).

[//]: # (ob:a62af198)
### What the quickstart creates

[//]: # (ob:f44cdb35)
This is a **local, Git-backed governance ledger**, not a hosted service or a
JSON database. Evidence, proposals, evaluations, and human decisions are
appended as auditable events on `refs/proofpress/knowledge`. The JSON fixture is
input; the `context` command returns a JSON projection containing only admitted,
current, in-scope conclusions eligible for the requested actor.

[//]: # (ob:c9727fd8)
`ui` starts a token-protected server on `127.0.0.1:7331`. Keep that command
running and open the complete URL it prints, including `?token=...`. The Local
UI exposes the review queue, admission receipts, trusted-context preview, and
claim lineage from the same Git event projection.

[//]: # (ob:19441b49)
### Local service and Python SDK

[//]: # (ob:125385d7)
The supported integration boundary is the same versioned operation contract
used by the CLI. Start its loopback-only HTTP transport with an explicit Git
workspace and a token supplied through the environment:

[//]: # (ob:1522656b)
```sh
python -m pip install ./node_modules/proofpress
export PROOFPRESS_LOCAL_TOKEN="replace-with-at-least-16-random-characters"
npx --no-install proofpress service --workspace "$PWD"
```

[//]: # (ob:36d2266c)
The service binds to `127.0.0.1:7332`, rejects non-loopback hosts, caps request
bodies at 1 MiB, and exposes `/healthz`, `/readyz`, `/v1/capabilities`, and
`/v1/operations`. The Python SDK is a thin client over that contract:

[//]: # (ob:ca86b456)
```python
from proofpress_sdk import ProofpressClient

client = ProofpressClient.localhost(
    "http://127.0.0.1:7332",
    token="replace-with-at-least-16-random-characters",
)

evidence = client.import_evidence(
    "run.otlp.json", idempotency_key="import-run-001"
)
candidate = client.propose_conclusion(
    "The current conclusion",
    evidence["evidence"],
    scope="demo",
    proposer="agent:runner",
    idempotency_key="proposal-001",
)
client.evaluate_conclusion(candidate["conclusion"]["id"])
client.review_conclusion(
    candidate["conclusion"]["id"],
    "admit",
    reviewer="human:reviewer",
    review_request_id="review-001",
    idempotency_key="review-envelope-001",
)
context = client.context(scope="demo", actor="agent:successor")
```

[//]: # (ob:346d1b52)
`ProofpressClient.in_process(workspace)` provides the same methods for an
offline repository-local process. Both transports return the same results and
raise `ProofpressError` with a stable code, safe message, retryability, and
details. Transport authentication does not authorize admission: proposer,
deterministic verifier, advisory LM Judge, and Human Approval remain separate
roles, and only Human Approval can admit a candidate for reuse.

[//]: # (ob:08c573d5)
### Repository self-dogfood

[//]: # (ob:fff1b499)
Proofpress can use that same control plane to govern capability, boundary, and
limitation claims about one Git repository. First create a small JSON receipt
for each completed check. A receipt contains only allowlisted metadata and a
digest of any retained output; it does not capture raw prompts, credentials, or
full agent traces:

[//]: # (ob:9f34f9e6)
```json
{
  "name": "python tests",
  "status": "pass",
  "commit": "40-character-head-commit",
  "command": "python3 -m unittest discover -s tests",
  "output_digest": "sha256:64-lowercase-hex-characters"
}
```

[//]: # (ob:59cf6f0f)
Build a bounded bundle for one base-to-head change:

[//]: # (ob:10b4639c)
```sh
proofpress-repo bundle \
  --workspace "$PWD" \
  --base-ref origin/main \
  --head-ref HEAD \
  --check .proofpress/receipts/python-tests.json \
  --pr-number 72 \
  --pr-url https://github.com/chenmingtang830/proofpress/pull/72 \
  --output .proofpress/receipts/pr-72.bundle.json
```

[//]: # (ob:42ccc558)
The bundle binds repository identity, base and head commits, the exact Git diff
digest, changed paths, PR identity, and test or CI receipts. It fails closed for
credential-bearing remotes, mismatched commits, changed diffs, failed checks,
and unsupported receipt fields. Import and propose through the Python SDK; the
helper deliberately stops before Human Approval:

[//]: # (ob:297e9681)
```python
from proofpress_repo import propose_candidate
from proofpress_sdk import ProofpressClient

client = ProofpressClient.in_process(".")
prepared = propose_candidate(
    client,
    ".proofpress/receipts/pr-72.bundle.json",
    statement="The repository self-dogfood profile binds PR evidence.",
    claim_kind="capability",
    scope="repo:proofpress",
    proposer="agent:coder",
    idempotency_prefix="pr-72-repo-dogfood",
)
```

[//]: # (ob:f6f42549)
An independent reviewer uses `review_conclusion` to admit or reject the
candidate. Only admitted current claims enter `client.context(...)`. A later
admitted claim may explicitly supersede an older one. Claims classified as
`roadmap` remain auditable candidates but are deterministically ineligible for
admission, preventing planned work from appearing as a shipped capability.

[//]: # (ob:4d9cb39c)
This MVP is intentionally single-repository. It does not ingest Notion, scan
Git history into trusted knowledge, combine multiple repositories, or add MCP,
Cloud, customer-VPC packaging, and runtime-adapter ecosystems.

[//]: # (ob:e98261ca)
The screenshots below are the state created by `proofpress demo`. Repository
contributors can generate the same synthetic ledger in a disposable directory
with [`scripts/seed_local_ui_demo.py`](scripts/seed_local_ui_demo.py).

[//]: # (ob:08b34ea5)
**Review queue**

[//]: # (ob:e299976d)
![Synthetic Local UI review queue showing admitted, needs-review, and rejected conclusions](assets/quickstart/local-ui-review-queue.png)

[//]: # (ob:e463dbdd)
**Context projected for the next agent**

[//]: # (ob:2fb7d73d)
![Synthetic trusted-context preview showing one eligible and two blocked conclusions](assets/quickstart/local-ui-trusted-context.png)

[//]: # (ob:0fc538bf)
**Expanded claim lineage**

[//]: # (ob:5810510f)
![Synthetic Local UI lineage showing raw sources, bound evidence, conclusions, human review, and governed knowledge](assets/quickstart/local-ui-lineage.png)

[//]: # (ob:1423b1c1)
## How it works

[//]: # (ob:821f22af)
Proofpress turns selected agent work into governed knowledge through five
steps: **extraction → evidence binding → verification → admission or review →
governed claim graph**. The three governance gates have distinct jobs:
**Deterministic Checks** enforce fixed requirements, **LM Judge** evaluates the
conclusion with organizational policy, and **Human Approval** is the only gate
that can admit it for downstream reuse.

[//]: # (ob:836f405e)
```mermaid
flowchart LR
  W["Agent Work<br/>claims · evidence"] --> D["Deterministic Checks<br/>fixed rules · required evidence"]
  D --> J["LM Judge<br/>with organizational policy"]
  J --> R["Human Approval<br/>authorized admission"]
  R --> C["Governed Claim Graph<br/>claims ↔ evidence ↔ provenance<br/>dependencies · contradiction · supersession"]
  C --> E["Eligible Context<br/>current · scoped · authorized"]
  E --> H["Humans"]
  E --> A["Agents"]
```

[//]: # (ob:09cd9aa3)
The governed claim graph is about agent-produced conclusions, not enterprise
entities. It preserves evidence and provenance, verification and review,
authority and scope, dependencies, and later contradiction or supersession.

[//]: # (ob:4fe9b290)
## Core objects

[//]: # (ob:9b060e32)
```mermaid
flowchart LR
  C["Conclusion"] -->|depends_on| K["Claim"]
  K -->|supported_by| E["Evidence"]
  C -->|scoped_by| A["Authority"]
  C -->|supersedes| P["Previous Conclusion"]
```

[//]: # (ob:b5752df0)
Proofpress does not turn a source or model output into truth. It makes the basis
and current eligibility for reliance inspectable. Rejected, unresolved,
expired, superseded, unauthorized, or dependency-blocked conclusions remain
auditable but stay out of default context.

[//]: # (ob:3ce2d48b)
## Current surfaces

[//]: # (ob:827e8ea8)
Available now: local ledger and CLI, the loopback local operation service,
Python SDK with in-process and localhost transports, a single-repository
self-dogfood evidence profile, local review and context UI, supported agent
adapters, artifact provenance, and portable
Markdown/static-HTML carriers. The `context` command and SDK project admitted,
current conclusions that match the requested scope and actor.

[//]: # (ob:76acc27a)
MCP, a hosted service, customer-VPC packaging, and production connectors are
**planned, not shipped**. The local UI's endpoints remain implementation
details; the localhost operation service is the supported local integration
contract.

[//]: # (ob:9c6c7f6a)
## Evidence, with the boundary attached

[//]: # (ob:30685e8d)
The strongest current product evidence is a frozen panel of **7 models, 3
Harvey LAB-derived legal task families, and 126 valid paired runs**. Across that
bounded panel, Proofpress governed handoffs raised rubric completion from
**89.3% to 93.4%** (+4.1 percentage points) and reduced observed unsafe
propagation from **8 to 0** across 63 controlled stress pairs.

[//]: # (ob:cf466876)
[![Frozen Proofpress product study: seven Harvey LAB-derived task models, rubric completion from 89.3% to 93.4%, and observed unsafe propagation from 8 to 0.](assets/articles/harvey-proofpress.png)](studies/long-horizon-eval/relaybench/PUBLIC_RESULTS.md)

[//]: # (ob:aea6ced7)
This is a descriptive product-mechanism result for frozen,
Proofpress-composed handoff episodes derived from public Harvey LAB Contracts
materials—not an official Harvey leaderboard score, a population-level causal
claim, statistical-significance result, or evidence of improved legal
intelligence. Read the [results, boundaries, and retained receipts](studies/long-horizon-eval/relaybench/PUBLIC_RESULTS.md).
Additional bounded evidence includes the [Athena/APEX working-set pilot](studies/apex-agent-eval/)
and the [artifact version-check study](studies/agent-handoff-artifact-provenance/).

[//]: # (ob:226a29fd)
## Product boundary

[//]: # (ob:cfc1c3aa)
Proofpress records selected evidence, candidate conclusions, lifecycle state,
scope, stated actor roles, policy recommendations, and explicit admission or
rejection. It does not automatically store raw prompts, transcripts, private
reasoning, casual brainstorming, or every save. Traces and external workflow
dispositions may supply evidence, but never become admission decisions
automatically. See the [privacy boundary](docs/PRIVACY_AND_DISCLOSURE.md).

[//]: # (ob:8deed5b3)
## Go deeper

[//]: # (ob:17d6b002)
- [Why agent-produced knowledge needs governance](docs/THESIS.md)
- [Ledger scope and integration boundary](docs/VERIFIED_KNOWLEDGE_LEDGER.md)
- [Two-minute portable handoff demo](examples/portable-handoff/README.md)
- [Results and evidence boundaries](studies/long-horizon-eval/relaybench/PUBLIC_RESULTS.md)
- [Documentation map](docs/README.md)

[//]: # (ob:fd00d6e6)
Portable fixture: [`strategy.md`](examples/portable-handoff/strategy.md),
[`strategy.html`](examples/portable-handoff/strategy.html),
[`proposal.docx`](examples/portable-handoff/proposal.docx), and
[`proposal.provenance.json`](examples/portable-handoff/proposal.provenance.json).

[//]: # (ob:44e3611e)
For a real handoff workflow, [open a design-partner conversation](https://github.com/chenmingtang830/proofpress/issues/new?template=design_partner.yml).

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1NmIxMTVkZTcxMWIwY2QzM2VlZDI2MCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjVhNTkxNWRlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9lN2M2NjYyN2ZmZTRhODc0YmE0YWZiNGUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2VmM2MyZDU2NDRmOWRlZThmZmU5OWQ3ZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrsvetyG0eaNngr1er4vrbZBFTnA3ume2mK7dZYtrWS7N4J0StlVWaRaIEABwWI5rQcMb9m_25sTHyX8N3C_t9L6R8bsXex75uZlZUFVBUAkpIl--2DTRKozKw8vofnefLvD9hiOSlZsXw14Q-OHlxdvYqiOPe8iIvE83K34EEgBPdj98Hhg3zOb17xybmolvDd6oL5UXyU-17k85jFrOA-C0KfFXERux5z_dILo8gv_CxOAvhvVPiREKKMozj2eRIxt-RlDuXySVXM34rFzYOjv-Mvy1dLdg41TNkSqzqEH3IxhT98LxaTcsLyqXAW4u2kmsxnzgV8f764cfIb5-liPi-vFqKq4JkrVrxh5wJfqvXnxfxvAl53tcACL5bLq-ro4cPzyfJilY-L-eXD4kLMLiez8yWbnaeB-7D19EL822oCP79aVWLxqpjPKjGDvlguVuKnwwcXgmEnRizKsAMfqL-8Em_ll6BzxSuRFDG8fVKWImRpEuYsZGUe4nev5oslvtqr6WQmoOX1iExfiTIofB7FYVhmXIgUHs4ynnD1Orp1rwp2Va2m8MI-trOYL3j14Ojl3x_o6v_-AEZ5vqjwJ_Wx4K9y6PKXD769ErPjx87JnIsfH_wAL1JPCqj_2enxo69Px5dY2T5zhS2Xi0m-WsIQvcpZNalwxohp-YpV0HVLIctbLS_mC2zQm8kMi6xuqqW4hE9m7BJHrtWwQ3i-wiF_cDRbTafQzOICxkiot8yn8-INPBKLIkm8PISvw_AsxY_4Ep_9v__j__j__uf_-Bz-qGtinAvVfzCPxDX85Z-uHDadnM_--exBAR0mFmcP_ng2c5x_mlyeO9WigL9j05fVw-n8fD6u3p6fPYAnlvB3Pe-guOXNlZxxbMEe_HTYtAp6KMsykbda1Zquve36bXta6xpwYsEkbVWSRKHvp664RSUvf_NydnXpwBrEDv7hs3pdwLuPq4uJmPJqPJk_hO88fGutCOyFzwdeW8RxwrM0vkWLDg7UYhfceTObX08FPxfOZFYuWAWrrViuFsIp5wsH5tB8Nr-cryoHZgosm9myGmiRK1yR8YzdokXNt5zzyVtROcsL4cygBOdidclmDjYGq3eYA3sIbD64TbFZdS0WzkCLMr_MC-9Wo_av89XCgdHg0B_OGyGuKmeyrJxLWC7T6tBZzuf4r0txCfvjoXM9X7ypYFcUh86VGJqsqRflsGPzW43a8yXsEs6FWIijgwPn5WI1k_3kjiNYLFcXzIENtHhT4bd--Oy3zS-j84EWxbADwgmT3qJFf3S-nCydS8aFU8zlP6ZwmswXbAljOLbWFnznDQzqBIqfwj4gZoUYWtBlwtw0us2o7b7R4H5bTEX1UA3hSB4Po6GRg6OEeUnRatXJxXxeCTkKV2x5AT8w7JAlTNLKucEphDOjnA5uQr91di1mfj28SwlWZJ5XevfexnfO4xK_67CF-Md__E_nndPMRefd2ezdaDSS_4cfnS9Wkyk2DRaoXrXzptmyn9c6NoET2Gs3-i_zawf2IjiyuIN_ncxWDM87tdK2dOfWhwe6MAu8hPk5v6fWWGugwv0jF8trIWbOgl3rvsEioKe4HCBdJWxz5Wo5MBkTl8c8zO-rz37z8oV6btR6ji2Ki8lSyAPhSLbvYl7VuyH-igUPtDIvwzyKRHH_fTmpnNl86ciTAefxEvac-QK25QXswU4O5qmY8Xp7dsCIHWhlWBQ88vKs1cr_1WyeR8452s8z3Vz8eHj2bXl0YO4VRZDEwm9bMo9nUNZ02t7ph5vwW6fvoYHKeVxmpe-md6vcGiP8PozT1SqfTqoL6AMYYzByflc5r_Fkf-2giTkT07HzeOmg8T8033MvS1jh3a1xr1-_ri7OZpdv-ESe7bqlo-akdP77f3cK3vlZ0zo861qti5gIU-Hdcdxew7m0unoNp6R8UK0wbfVwdgWHmdwmrhewJKEPx00jH14OTe_YLVPvruP6-BJdKNiX8vlqBh86cJKLS7GE1SV-lB-hiaZ9mEPswCs8dOYz4QyZjGme5UEQZ_cyrrOrH53RaDYf6R60htGBr3I0O5yJepGzMzQLZjCSry4HRtZ3y1ywWNytfaesuIAd4PISx-9qAWaQGlxs0hLt8AXYugJ7FRxtY_nCDnk1HrRui7hIyrhtb5_qFwWbdCIPe6GGjMFIgd8ILZGNG9rAdixiYC8J3Bjst5Tfa8sez-R0gj8sxPkEemeh99UFmJ3wI-wmfF6WzpJVb5xraZkwh8-L1aWYDfRiUYZxnCbxvbYVfL6TpmVyEY_q9lXLFb85gvUC3Ybl1X_3_IeeD6t_oK0M5mIheHKvbX1xAbt0tbrCdaHmpXZVR9LVQkPuUuBePakucQ-X9iN2MmzcQ_3K08Ir4zX_VMdhzFaBa_StmDHlEQzNyi2PDlnFhS-iwA_upSXWAcem1RwMaVjO8P9KGiNXYNrVsaZRUzKY3WPnazbQW77LAr-M3Htpo7LNzWx4WbfITDXxI7u8moofPtM_VA9No4fa6MfMz8r2qv4rzoZJ9Y__-C_c3JRdBr_UUbAtg7r96SFzqSy8ImDsvtpjDa2O8TkVnHIFWqrCLLICyp1wtpTGejFd4UqpDge6LRJuHoTi3roNrCU-F9oAXi3n4MpNCjiPpJ0Lmx66FjBPLq-WlTSIZ1WxmMhfBsNoMP1cwZL2UXyyWizQAIEDb7na5nZtfHlg7MLM9Ys8SG9Z24sLeZKjCTLD4eHirZjC6gNfVgWzqqOz2cHBprGCVsrQkZoVWRmsWXK7N0uPqhwacEpYbfneCPAFmPSe4LdKLN5OZKhIhZfQ-SmGPJSUg3UQ5e0N7Ms5vLVQ0aahUbG_NzAgXsLj3HX9_esYOS-PLUdRGqkY6TlfKL-uPox--AwO4-rh8bOTvzx-cXry4rtnp-OmTdBTywc__XBYh9Qf6EPoVbEQTIW05Sd1fFy8Kks_yAPXTUUB7nDiFVHIGA9xC4X-lx1Z73s66q9ih1dzaJ1MYixkTRjwrn_DePcPmC6YToobqwQ7hWAVIpMTt8wuVPNy-aqEYRALaRLKJ6rcO2JpXLpuGKesSEThJX5SFCnnGRNJGHjM82NYOFkeBq7I4qLkBc9jsFLzMkiZH8jgD85UmYxQo3UUpD9BR1fynPHjkZuO_OSFmx657lEY_B7-6WKv6R5HXzCPUpFnCcyQ5q9_v4_UhZxuKqtwwaoL3AlKL2ZxmEaFKOELsgwr0aBn4t0zCLit42fw9-sJX17AJ2kKv1yIyfnFUv8GZf7Tw6s_dqxF3do0SmLoaC_O3KBurZWA0K3dnlfQxUWlKGNeJgV3o7o4K9Wgi7tLBqH59vX19Ri-8rdKpuJ0Cs_6-udnM10Ruh871_IQv41V_UlmEv8Zf9271pPHzRM75QsfMrlvVg_rwGj1sJiMby6nD3MGB8Daq9-tSNXEJ7Blzypx5BxfoUk98sdubx_JNjycqidG-gF8YpRPV3Xjnjw-Of3m-enn_ZNN8BBWEU_CiKf17LDSPnp23CWbMz44GKge9p8kZoUX8qKu3srxbATm90_dLOdHzsHB9cWkAPfdMqfAqr5xHoMVBkYNRo3m14cq9nFx86eDA4wX5XAaWeaZ_exyfjZrzLWqALPgsF47cObKrV0Vp46wQ2zxDGxiKIELtONvlhfo9SzE32Tph2ez1QxecD59C79gvGOywB_AZ4JS0W8_xLdczVTOdfLv0KASDLCN6N-4v6-9woctMy39JDIbgZW90n19l6TU5aRSpqp6dXZ9NjNmUStXo1pdQcdPdTSCLRZzOVwYttW2sU4j4B-qFdgzb2FQz2a1gwHdUUJhF45OKw-8OYuTzGOlH4fSB5dvbmXJzCS_ffJLj8JIj8Lnzv_zf8OKroTKiexqqlxy_WC-wMkBq4hBV7CpcarqbWPfbQfGZSVwG73-01KATQvWzj_DPITD7hX01XImFnIT6u9BnqRRXIgiEoHfnKAmq6d78C7JOgxeXWHfDM1gNxIRT2KRS2NCnYxNJm_vc7w7QQdDCo0bNX7wSMzOweoSOCgjmB3z8dWsOfsfT2FXWOrRnZcwZM2TjtwpcVYzcB5wTKXHjEkrbdBYpoLnu-4O5kHphawoktgPwsRM5iZxWJsHd8_41Z2e8iyK_JKnkTFHrCSgru-u2bsFrPPpcjJSv9b7zzvn5ZdyaXVvw_LIae8C29alrP_5xeTqStbvXIBlpkdc79WmV7D2Fwu1P03FOSxDmM_cxNjKyY947lkBjrf6jByZM3Kkxv-hfPyhrv0v6N1D5TpuCJsrKxZzWBRXYg7lYF8oIE1Vt4CZgE8TptHN6Iqv6I_q-k7fsinmv6BKfBUr0LZwiimbqHqewciruWKSKa1o4g-f4b8mUE8r1GgiUNZ6qSt-XG97MrynDgyZPavkYcaa0wMb8Bw2y2ucotY2Mb-e1fELE4-Av_Xtne-6csC1Ve2lAVjQbh6HXrNsTFq4WTa3yezWdYTcDbMk9IRv9icr2btpzeydr0VDq23znM3QkJnMYKFNlmPn2GRPTDpCQ-bk4QPn6iX0YxNgMlP1D2fw1BLPcJgbsC0qS6qSzVAGDZSoJhIUBLbffHGpV8wfmnMcGltOzqGV_GzGuLYHHG20LG-wYseYMPD4qhID-31WcpaUJc-zIDOuS5OW1v15l8wyrvM_2DOu-RgO3gqLsXYcaTPmut18_MNn5hxpqnq47GjMyP5GH-pKv7TPRQyOqeCpL-qXtrLcm5No70T1AkOMcNqCFQqHz5sJrkaw1BYwLvATgxNR50tVgBI7Y8PYre1anB7TSSmKG3isPmLeSEOtY8t24BA8n-A-hlu3Gn7nubKSwOwpV9Npa9xk8c08MhX1bAADUymOozQN8iLOQmPAWFn5Zvnvn1qva-AsLJLSzbOE1TVY2XZTw16Zc2N-5UEZRHFYSINVGT5NMn1zTuydGEdUrPMUvBL4YjD2vN-DRwLGnBrgb9CY8_3fHw2YZl6aZGWS5Sk3VoKVUdctvFN2HLY6sHZh65ksMRF7KX9yRjf1L6pTR6MKbK0RF2-tQv4XfOnh7O1opP234a_JBDp8qjZqtHJ_PJvBa3UkeOux80MwnXmQstK4XVY2v-6ZO2Tm4TQvYdmP_wb71eux810Fa-m1aeKUgcv5-tB5XawW1XzxWp69r6GO18p-gr0Dzo46OyePfZjzVTWwmCJfsDSJ8swV5iy1MAB1DvsO-XzcZOyN4xD9bXn6gDe1PKwdRIY-9RUcTpM6FGA2i9r9_jdwfJbmEMU3lnuNjB5IRPXApBZxKHgUczcOc2MzNHCC9qS-LTQALF1pvTUDuoNByWEzH8-X0ys56GdbJm3dtSO0dJcyoeGcyQRHofMOTU-DQ6JaNxqZVp9-__jR6Tcnp68eP8IycHAcbAH8oovWxsgRuMzgTG7rDD2QJ99-c_Lku-ePv_0GCh5-RpvmrSdMO3HMYSMYqS9BW-RUOKp_HS65nhlr7yWnhn6palWAzVrNt5S0mrQK2bIt-G6eRy4P48I3gTcLClIn3u8A63itX-21iTudzUy8ydkabpJHL_bCCFaUchvb3ld-gyZjycBvg8pWk9cyN63aN50X4C_pUYMluAKTYd0Zc64sI-JsVidQwGO4uhg7L-ThGDqvrR5uYo_j8fi16ZfzxRz25IW4lDlyaYsyeFfmYKwDDBrYcC4ndfylWi1gvxm0OmPfizyWe4FnYpIWDqYxFW4PYjHB11iETLhFFptD08K1GCzQ7UEp6CdyRxEtMMi4gQjRVqrAfBpsqbCvLqfoTmioyHIxYdPKtpBHYPNiI3gTiQNXwqnm-JALz4ydL-BEwYL5RAa7rTpaNeDy8XwMfOr2jUyjVbUDY5QnbpC4fshS3xyqFsqmSWrcGiKjm2oa3-oE-aKW-a_DSG3PWNYwKtiCj3RKDONGn-_jSJsU2IC_4IKNyVnKvYgZy9YC8eiuuAsCR4MBDg7AVDg4cKqLOQZ211x1eBexkBABOOPwDSptvhTsiuWTKXp_sKOalDUcPeCKXOL2DLsl9MHYMSGIlxLkIvvP0emcvcIPZ-idwvuANcurQ3Ab4HyQq79CywGhNC24Be4hyttdXVbYjEqgE-JcTZnE3HDcN2EWVVfoRr8VdZsqvec4aN6ATVW38LXZD8DKnV_PVJSl3hvgGwMTOwxE6RYRDxk3oWoL5tRsPvtjleqDR_CiSIOYhampwYIvbfoSe2OQFm84vjV2K9obk-Js9pcXXz-Rzj8sB9wdMYIgu1OTAaU1h8FTPMrRCN3gB2JmHne3GcaYYc7U4SAVWm124HKC7usxWnpwaIERPJvLcIYxZsRM4ThkczDHczazArbLufJ3f8QXym_Q2IZmKRMZi65kTfOVPL2WQkXy4CE5BeBtsTg18BXOaqh5aLQD7oWuW_KoCMvGCDAwLT0Wd8Fa1bHAZic5lA2ESatjwy_NTDquB_J7T50v8LP2tJ9---zF8RdPTl8dP3vx-M_HJy9ePX96eiKDbmgWvTSPPm26En5czov51Djr-smnz779_vSbY7Qn4ccX3558-0QWJAf3Zr5C41yojcDgb9q5E7QOJrM3zon_VA60ZRhgUOcf__FfMiCi1928PJvJb8qYx3KiNiMwdibnuA-ocFR1MbmSnhF-aSoQegVeF0ZrBtJKrhvyKEnSsDCGggVga9bqrSBo9YYg0pIlsR-6oXXSGVTa5nLdG1dmxW-kewATRAd55K_aCnTgFMXArY4FYi2XMDK83lfxzYwv1oRscHYooxNTdM2uZQW_cXup_TkwtK-wSn04qfAjDskK_yqRHWfaXBhaV7GXpWGYezxyzbqyMHK1YXUHlNvkLXajihHCiEGfFaxagc2bL3CXhOcxFSdnlEBqtINRibFz-iOYbzP4mkky8EkFDpS2lGb43bOZCtPap2vToVwUE901dpPtMJpsHYzRWqrx6bPH3x-f_Our428evXr0-PnJk2-fb4-blSL3C-HFbuEZV9-C8VnZph2QefWuF3p5DJabX6ZmdCywnrFY7oC_09tR5fzjP_8vswBG8rtdwW_82tlMuduFDh-b5L0sowkFNh6zHVFowxHA-UArZQzW0gvjDSnX_dA5efK4jp8638GPHQf4oQ67q8VyNqvP1IfqPB3p43SxQAeQocH_lk2mcmHBKw0Mp4hKHhY8iMsoNL5NA0hsI0dvhTGEzVvy1GFFaJNwdLVayPBDnQOCHssXc7D1RIndDTNVJ8Cmc0ywYm5Ap1skREb6gjpiI51BRyLjsIE6Pa5S2SOdym6y5TLXCtXCylzIzpGpwpFOFaLhqdbSGJOX_enRQ22Qsnrdj2D2sBEU1krtS3gJblzyt_eUoh9aqhksrCTxU7cxHS1YZ7NUt8A169MtE5HETIApWhdnITh1cXdBZsLOczaDAgy26CuzHp-ovDkuOlwn-unvT589_vPj00evvvrm278-OX305ekr-c9npihMOaLZglZ6b_RMhmd2ytvKMJvufvDnbsC0vFhKtBbU9eJ6PoLBhJPJ2bDI1moYMMdkUU9NnL7Dr987_bpW-CN91KoBuWRXujfX29A-NaCqreeGfO7YDlLDM9WbyXS6Ubr0w6WgxOz8h89Ovv3mxbPHX3z34vE3X2rUC3xFHuvTOX7-l-Nvvjx98u2XBhLjYIIY9l6w3H747PnpyXfPHr_41-ZRTFDAxgC14E6EFTw6ffXtn19BRY--O3nR9qA1DvgnnOwd6hqCw2zu1taQgh1QQ-_Hg8ocSn9EVE3pJ3o_cF7Aq_-s0h1yVjXKHcUekh076w1czrlcZ0OKE_fDLt-saZMTfifm8A6vsivafbMog1NX6Iy-zt58XmPSn4BvpB2okxfHtUsLZg-Yqo0h0sQqa1t83DcUu9Rkb_qLOW6Kt6zXGpdd6m2li6vV5SWWfMuqrSHrrfoZ7OxvzTu_ZdMJB9vvei1tXZt0EqOJI-7M2NvJueyesRrbek78_cH1BfIAnslOaxUzhdes6pdhU7B1ZEBx20s5rMR8oVwvKj0jAzHwpSkGkpvGgc2IgV8wky1XQ0OCGJw2S5VzZFWdQdCgUwWPmIJdJbADd-dTeCIJgpJFfhy74Iq5UezFcRD5pnttooRNErDJE3-nXeiD7kK7c2IMJ8SUdhT-1E362MaAuReaS5F78IzvFSwr4iBPXZHBqEZl4oYJd0uwk0XpJWno-14KEzNhZcldHpW-X_hp4JX9r9RFdAmP_LiL6AJzvfAzQUQXIroQ0YWILkR0IaLL-yK6pCzJiyT1WOR-bESXwdgNsV6I9fJxsV5SERV56CdlnnFivRDr5eNhvQxvpESBIQrMJ0-ByeMS6bpBADbcr4wCo49OBSPekkwb3AmIC0NcGOLCEBeGuDDEhSEuDHFhiAtDXBjiwhAXhrgwxIUhLgxxYYgLQ1wY4sIQF4a4MMSFIS7MFi5MHue-HyQpU3tmPxfmyX2F74kYQ8QYIsZ82sQY32dRWIb3cz3NC-WJ4bLBiIyC15nl9fK1zHmK8xvoltfrC2x9n-ymlljNXWuFpj58BfaotuBMxVa2SkNDwIrTca36Xmh93GjiwFQDQfQo9pAhhDI7pZsCfaTKbAgRMtzc34aqzuOZWLDM_hXOfJbP2ULWX3t12ro5X6gRdfDO6v1YDSIsoyQvc69MI5Z6HFwS1-XSRelmNdSI8O2sho95Cu3O7Vi_K8L7qRsg_0FIAVFRFNCysvRclgSZH4d-wrM4TgORhHHiR2HGc_i9dKMwdtOMFzkrkxLM_hDMgNTreZ8uRkBy5EcdjIAEWprBKxMjgBgBxAggRgAxAogRQIwAYgQQI4AYAcQIIEYAMQKIEUCMAGIEECOAGAHECCBGADECiBFAjABiBBAjgBgBxAggRgAxAogRQIwAYgR83IwAOG8YLxGb0KRKLDiLhWy-LSbFHkHre7DB4eKynkVo4m5PSxAjeFtTzDnByL1WFjybjmGUfhwso_XNz9WEnCyrViHNUlLu6E7lrT30eZN_1VsD0TKIlkG0DKJlEC2DaBlEyyBaBtEyiJZBtIxeWsb7uZhjn7sjmMNXaIbiAY-UhtqvruBlhq6q6GZKYJny8aZQfJVRc-OEquT6Ajx0dMzlqahRMBu3Sag9EuoDR3IvFkQQZ34aZknpukkWJmkpWJbn0iTrZEEYFPx2FsT9X2IwQNnoUPxv8xUa-P4H4SukPEwyN82LLMliEcVeUGaMQc-mUBQLcu5nbpDlIuJRmkYRvEaeBJGfxGnMA5GG_a_UQVnw_CPX66AslEUpfJ4kRFkgygJRFoiyQJQFoiwQZYEoC0RZIMoCURaIskCUBaIsEGWBKAtEWSDKAlEWiLJAlAWiLBBlgSgLRFkgygJRFoiyQJQFoiwQZYEoC0RZIMoCURaIskCUBaIsEGWBKAu_OspCxvy85Fma5kXwASkLxDMgnsG98gyKHoJB0cMsKPooBYsJGB4LvnzPhAKdA3kFn8na75lTYOHTLJ1-G_LbC1EfupLBKraXVPBE3YnQ3HGg0m4KN6Sc37Wd3N5Jarewh11w-uNVDUTaoZDmkgfdlBoMJOkE6oDZj1TgC-aCPZPzgoVZEEURYzl3w6KPVGBw6ttJBfcxZLtTILayChqE_YdhFfieSArhB1mcBUUoIs_3eMFdzooUjrwiAzPf53kg_DBLExGA8xXCsRWwIM9Snnt7sQpC7yjwO1gFQRRyD05XYhUQq4BYBcQqIFYBsQreG6sgLPyY44uW4afHKigUIJwNWWFo8ekSH50-f_zlN6-eHj978c3ps1ePv3lx-uWz4xePv_2GiApEVCCiAhEViKhARAUiKhBRgYgKRFQgogIRFYioQEQFIioQUYGICkRUIKICERWIqEBEBSIqEFGBiApEVCCiAhEViKhARAUiKhBRgYgKRFQgogIRFYioQESFj4mocKKDZlbxa4XZFy3UG0aNnVqH0e1HUsiE7-ZxBhY5GJmulxZxyEqW-X0kBQN7_1lICgOUiq0khQaw_wskKfhHYdfVB8z1I9g2BJEUiKRAJAUiKRBJgUgK74ukANNJFEUu4iApf_EkhaESf9suYmQVMcIiiMNAHAbiMBCHgTgMxGEgDgNxGIjDQBwG4jAQh4E4DMRhIA4DcRiIw0AcBuIwEIeBOAzEYSAOA3EYiMNAHAbiMBCHgTgMxGEgDgNxGIjDQBwG4jAQh4E4DJ8gh8FC1TSg-F1RPEOQ-Qb_UFdlxRObqnaMXG5B5lu1WLG3e6hltrrMBc6ily8feLjPpdk4-G8wHfSvWTAO1a84fmnzgTt-8MMP_a20wmLvsS_SIopKEQZ3qIVx5ZHoCLk2xF4eo-POHh4_Pf3fmmg6TgqEq1UCTubJdL609rgr8eOInQ-0NQSj0s1S797bWgmsC_b0l8ayagUc-7bjgbZa-L-mrU07FnBWvF1ryV0BggOtsQApu7bmLoiV3UhM1r7SS2J6Nl9hVMtC9YD5hsGrOvZVLub_juFX3NNHEoxsUHpy0MZ9o7Lx6nWN8g-V5kcVGiWKgME55g3wz2rvhrO6krkOPDvmmAMA5wNmxriv53ep0e5elVxC4ta8hW9x3k6k31jnkPCzClzt4YZYW2tvb4P7eDlf6qZ09KwKcuueB8v2EheZuXRGN2_ct9f2D7IA47XQ1ZrAvkpJoM_Cm6X9F7Z4K26cJ8dfjGAWwMCgy1WtpuC3qV4Z9-2hvbU_x5BF1XolWfPvKvQSpP-OE6DZVCSaCLl1CIwDU0Cghz_u21XXNh5d6THXoKXaGf0aI5ziRzB3MIkp3ZwJ9OaNDPzBiJqrfuxtVe6g4749srvmZ2JpZs1GKkt1OassHESTaFEd3UMI_BoBVT3TpmPQ9Eyy-lwvqib0pHIfph3yha1-wWFob9LrLdUhppWGaTSrwwI46GWyO_kwyX0eFGHkFZ4bJkHMgjwocpb2kQ8NnW07-ZDsLLKzyM4iO-tOdtbuXGlD1VVjdeQfWqTd8NA09sj_qZuf-0E4yVnguog7SeEp4eeZl_AkEJHvMZEEWRoKlkY8CrMy9EXIEdfJ4zD20yCJwW2WLvNeL7rBVM6OXP_ITTuYynmShp4fFMRUJqYyMZWJqUxMZWIqE1OZmMofMVP5Q5N0vSiNIwb-cdncAkgk3U-XpFv37Taybl_ssHHt7MT9CMO7D-EcYzc5zOSLh0-_-wLO_VfPTp9_9-TFc0WbJeYuMXfvl7lLJFYisRKJlUisRGIlEiuRWInESiTWXz6JNcr90g-LLPSKtJ_EKnNVy8UcU7RLs2LXgQ4KTqxdHbDxwMmZl87BQWJCTcHZrCP3rfxBSYAt2eVkOhE63OT5sQMrdQLzjuHscGBtVwcHYHYrHw-NvrNZvbfLGg83Y1INihQWMZtUspx8gTa3YgvhmGDkDbHwMoeKiA6ZPT04cD77fTj2MBKGCQScHBI5XX2u93YJh3TmOSK54QdoHyuF5KRdsXNmioZeSLFUF0rUDmoc2DhX6F25TcJ7DhIMwyL0GZx6eRM16WTO_lmNwtPWDtyggI6UK9qFRJDjUA9Yd0c57V5Sg7XWB85GF6gOGG8Sby9kI0ZWCqLNtN3TNe7vvYInrEzjMmRxvIVsK6eyDXfR3TdaB1XI81zNebAQLKa1jD5VFoRZXE2qOYaK656WvaLFopuBcE40ea9CXxOsLiRT16Q4VK5DxAczIJKphH_lc0QFwc6PHhZGOK5WUxUDnCLnAxzBVcWmZzMZmlCsJOl2sukIY3aSs6EIW_hOmnOjVzWsYU0K1kv1bGaH2Wzmr8GZNPjp2gjSvN0aHnTr0R1Unko85jKRum4Tc2hgBtZedluMAGbfZRNh-SNgicn8g2LKI45mHaV0VC92DDwsr-fG8FDLDDpHwpyew5u8cbyxdzZDjSonSHF5ldKQODgwIChFBsG6YBdZzt8ITe4K47H_32Bo0LDR33UwIAvtwBwEsptxdKy9YIloHrTB4Ny4mIBTfMn-JiMGIzmFOJyXTHK-URwAJx4XBR6O47OZzfhq6OBTGekHb3-0nI-EJJxV4L2aenCrU3klTQyCjsOOGcndhl2CRTr59xrPKFnZyOFXXE44SxX_RAxFcrMsTCIvYCIozZFp4Tbsg-yWoItByjos7amBzck-n960aPlH6P92KEFsiCdAh9xa6kFOh0G1ByPz8Fiyf5rdrImzSF52B56xhrsR-53Y78R-J_Y7sd-J_U7sd2K_E_ud2O_Efif2O7Hfif3-S2S_qwxMHwd-7dM1JvzGp20-PPgxi6MPRIoHc658haHXRQ8jXp49DSN-NcO1MNuVE98AjG93UZxFGrHQwvd5R6DVxG3MS-XBsbySfuQ6LHrJzjEY1ni1jM-l0aljuTDkGDbBM-bQ-bI-9xtboazTemskSeu9ext4MmUatS2PG2NVLMR0Ij1XhZGuFNDLSN9PJxKAgeE-jWJWccHrC4lDrQFDPVzGY3w_BTiaCrAWFvWb1oYnBhJ-N_imv9OBRhxBPPYx8iBxwWt9y-rkHTJfRgiQcnQwpQZo6Q2cyWjOmpNtMmv7MBijIkrjsEiy0o29NGWZKyLBM97HYDQ0lx0YjB_Zqtidu9lxb2Gb9tSQfT4I7Ymn4HtlcRKxJCiyOPPBUIkCUUBBLmdeGZd54DE_yVMWh5HvJ1GYh24ZhKWfMhjN_ldqE5zSF156FLlHftxBcIqKkEUJY0RwIoITEZx-PoKTmxduHnGXhWKI4DR89A5xmBIvjnxwdUWeiJ-fwzR8ZtvUpk7oq5QG2Z_adDYb4DY5-1KbzmbEbSJuE3GbiNtE3CbiNhG3ibhNxG0ibhNxm4jbRNwm4jYRt4m4TcRtIm4TcZuI20TcJuI2EbeJuE3EbSJuE3GbiNtE3CbiNhG3ibhNxG0ibhNxm4jbRNwm4jYRt4m4TcRtIm7Th-E2vSc-0i50n2eiXECTa_gOHGaykyXoQ9uTYJGZu9BkBFKSawxaTp26mHdCtx6Rhd0cn--026mKgP1A8QkwlAvmmo64OmaQzdEuG2XCjIaGVDdzPyoOdIjwArzQJst5yMAIytLSlyjvTiqOIWRsp-K8B_rMAHGog2vi_dRNJfkg9Bk3F16RuaHvc5aKPHFDj8EjcVQWMuLkujH8sUiDNIpKvGEocHkSh36WBiH8LPpfqYs-Exz5XfcDgVlc5ElC9BmizxB95pdMn4lhY4rdhJdh6u1Bn-mlyfy15rIaX3LteEO6zNlsPvuT89eduTL3eQ0QcWWIK0NcGeLKEFeGuDLElSGuDHFliCtDXBniyhBXhrgyxJUhrgxxZYgrQ1wZ4soQV4a4MsSVIa4McWWIK0NcGeLKEFeGuDLElSGuDHFliCtDXBniyhBXhrgyxJUhrgxxZYgr8764Mjqn-go-k03oosvI5jZ0GdVuiywDLz-Kkgefwl1AVlkWIvbOZVkY0zuXZcEdm7JgS7HMiim7gRU1VKq98ZpGNgjG2xe80VwLp3j7Uk0OsmmrAYU1pf714kYbTNIbr3FU7TuD9u0VCxp2jzVtdJOFmLrHajb6rYxDBrM6uks1jCvnUWdB27mPyUL5XGzaoBwxK6QChE2AAn5czZA5NtAnXugHuVesTR0LPznP0cND29CwD05k-V8u2FB7wRjZtZiriy2LxvdK32flvbfRjruvECJvHGt1jtcHisIhgu0zhyq0uzC0E4ENHrqRuPf2vn79-lIsLtkECQlgveLptHRefIEn8MnLswcnDajuofEmzx78ID8_xi8MTFs3K2BXZ8G9txrLkHn7-qoxRSzBR39noV8UiKFxk6ThN9DLYSmy3M_cVnsRs2pBR-tldr5OnNkyc3ctRmzZ13I3dhWK_n6beNw8P6lnLSz0KYKnZIBVJiPkdN1AwQ50qS_iIvElIvF-2_vyNy-_MkdRE_Aw0akj1cymkXUtzKmGNvQoiXxe3v8UOG0AvoUkM-mI2B-cyRL_osNKLfSu80zBZwbaGxTC52Ha7t9HCPTGdNylTMWtLq-w3i0TtPehwW00Ealg6R1rfzHnDDx93jyorHOViJFliI6VAk74Yj7QN0nMisJP2B1bd2xhFXUC__jp44fPH30lN5ivT57K4IaOrRwcgDc-myGiCYZ06JiMsiL2wqzVul2ZJ1vG8q4EFjO-WSCYHyf33sa7kl66yAjNqZPChpPl997ouxDM7vP20uVkOdV5J-UzQi_Kvc6yBg2Js7E4zLrZ_0LS1o2pMlCHOCHM02DGE1Ep1j2pPbVi7Ho5mRW1YECny9bbgucKoWukB6xXhTOplaBQ_aqCok38W8sRIG6x2crHfe5ebzuOOdfdIKnkV4tJJUaT2dVK4QowVyXff75a4t9MH5mMYJ9TuFvfV9P5OawC09nL67kdxZIeGexGHZ1suYm9VT0SpcTtNK-mUJl9I6qyODJT2HpImmaHDiy-ObT3ppNuKlFkhkgikz_XMK8wvTnu80R36yO1vmV4Tsd0O3tJ51MYNPZy3Oel7qbZUc6nUBjuULrr8eLa613cs3Gf07rDBLSdtvPF_BpeVfUkm3au_80Jb3mvO9Sn6yhWi7fCMKhm89kIttELoXNLI_Ut6ORrmPxvYc2N-zzZtX12o74ur84g85Tn0PQ3rvWusbRckG31GWhYM8GvJldC3gKt8jsSr6VQF3IvO-8yPB2JeBz32UnbWmHtkoa9xvjbSaWwJcaIlAvTsMmbhoz7TKDuiutgsZWr4p0WUg1kXrvO2rJiuivAZFS_4QTrRJtLOHcvJHgN9jfcBa4QAdZjjHRX9UzITKzqR5MylduB4mDDkiiXos7AXctjQ1wtMRE7wTC8zkuN-8yJHaq1mEXryY1C8WzmDtNz1rTFbmKPco-6EvxG2S0dTHwbKK_EG_RSEa2OtTZpaxtX31fpaQlU1YdnDVOrZ4Y-4eoR65sdu0sBxZynQcAClmdhKoqCRTwPeOpu7LO3M3QeWCpCRpfmE7vQm0LbFNqm0DaFtim0TaFtCm1TaJtC2xTaptA2hbY_6tD27oqvRnBUtenIiw5t7VH3p25t0Q-ip5p6ccRy-GdZIqA5dIOiTOIgjF03KFPhRh4XYPUHRehFcBiEvEhCHqVBWmYeT9Nwt9dra6tmLzz3yA-OvC5tVZRczAsRkbYqaauSturPpq0ahSIJ09hPg0Z5qUtb1Zrh__iP_5IO3peNU_sEYwwyfCXt09HT2n0ytt-g_GoeJ-DpidwrvbxffvVYhfb4fPa7pfO3lVKmkTZHVyRQYudvdKoMrEmMkZoPz2YyKtKpAzoZYopy2BNhqw1FHLn9uqW3EIo1qm09QrHId95BKLZ-iS6hRJNNVES2Jp1onF001FbnF7oN6LKxRXFxaJF9lJBSQ_eTtJuhQKwKH2Mcdoh_W_hhxL28CBo9vE1N1D86p3WqoqmmHUaBfjtnM7DMK6UXuBkNHp_N_tg16vLrikNq3rbumCG-VQZGPSvhPzAv-tVAMSTSHZQboAy7YLOXQR5Eadiv8Hna1fcTxebOYdxnUitxUXeMzqm18p56uMGTQV6RoaeBoc_AAGGV4b5JUQQ-lyz3Jh-KM0LlRMd69dfz6WzWahKsQCSY3SATtpKJHpxIR90Jb7BhsENk6ptNb7ARa9O2c_FK_RwEii-kw2Z0_hSXuJmodtN6MrxafrOV6JUd2QgGDsl8FTAreJQUYKX166V2h3WePEOz4_Srl2f28Jqt9J_yxcM_mrHFQUIeQUMrhF_q4ZJfXRsx_Fy9oY4PYXhI7a3y6_Wyx-_phQM_YSfU33_6Vf1Ex0Yvy7AzOPCw1hWFn-phld-qR1Y2vx5WXcnTpy9ts0p-38QI4Pstxhr8bjZCVbIJNMBHJtagi_7yGNtvIlkqorLWfp0kgqe1nFpTBepdq4IeYc9ZjiprOhFnqtzA6_c5_coZjf7oHKt_PlW_PX0q_wUNkv9-dLxF9yqDOcWKlKFpPqhNumvMeYB8G3huCA5OnidRv0TpcWV09uZXdip3PptfosgDHr-VOFwXl-g6MVBCZCU5qJh2x017ynRoC9YhNBB-UJofEplTwHRHqZg1Ya36fKo5eMtarkaFb2TZzuUKpnfJUMli7Hw9r09d1BKX7NcV7kT5AvoOhdGRxlufhA2EZDkf1cckkvpRzwz8IiORY5HjtXSBUoqU5eELwEw6n0jtlaYvivniaiXTqrKZ6kRyKswZ4psMbDc-T_yIp0EWNEb-pgIqTK6lFHM8tnoP2y8NE7sbH-pOdJz_Hf_xztnjP30ZzL0KGo9-t_P3d_3uLt-D78h__-M__88WLusC-ZPzKT8aLKF-uv6PVFdobVXdS7G30KbJnUaW88r6D37x96N9__PH9RX8sFm_-P7OcnIptu1LPIiyKAvDnJnDzsqFbcpT7Z3HquCbNjQHlrdC8EzZtdK7y-fL5RSWPMrgXExKOAfVnQTW7UKVZNlXcoFZ0ck5FCZHutbGtiOXxoUYOuvjkMdZWLphYeinVnbNsgHvmBarnZDIT_NSuH7GmisEmkzZphOyd4qL6xHQeoLHkuBbJ5gmmq2vfDDmSFARjBXWe6T2WaRnV_XtTChvoIUWoY6_reRWACtDmmRsI5ws3SF0e1B3aNAZK0O_jN2AuRFrNPCbDNygjbVP6kx2xXH9py_Mn76oz3b81hetNEb9yRd9n2jzppZt2WrRKI6xNJSuxAxLmijDSctOVnarpTVxomyN02PrT1-oP31R_2nkPN2ytEPBE9d3s0KFl5Vr3uQLrWThbRN9m7IDeODirDm0BMGlrpHS5rB7QJ_IsxupG7bQCjp8olBJKEdg948Uj2pEjGBVYJppvloUQqnOK4F7jXeVS0JKfEtfQt7ToM5uyUxVAh3aUFQi3VLjRut0a2yvpbg0MJPd2PPikpduIIwXaWU526Lzd0hP1loIXukWGfyv4I1KZ5OxtOMtt0w1NlryWlLvDL_YOxFkdKQWTpVCSUaTCiMhYsp1r0rpCGlIqpFodOSbuTJ2vpUyprqEw3qQDqG1WmO2JcUq-7A-A3a6vSbN0igtSua5zcZjZVCbkOqtU59aw7nW6zjEEWgk-JqlUvdZLaw_c6SehN58m0qNtqocsI1XtaQtweRdCmmUPGxgxqagkWm9jjBu1zYYiJ0ErPRTzxduYMJ-VmK3jnDcISPb1urFS496xHrt24xas0OL-rEVnygYdr6SSi83uEuczfDYQ6CrkvLdZer4vh-XgV8WuZk6VnK4Wen75HnN1UJRmbOo8IK4aOwCk_qt9-o7ZHExOGgkis9mWpICO1BKu2yoFysNIyUXg4IvTYa2Jc9eaRljI0XRqfpi1GK0_IuSR7GkmhutZ7n5VBg37doI2vdnmQyjtlfq-yIbVQ_ZP0OCcmnqJWD7xXlkYuhWUrveTu-Qn65BxCghLCVhVC9_9_h36uaghXIkuZL4lQWsqbhx1DFFYVxlYKsGKD1Ug-nV6nNGUMn5ILdLdN1kZCXdP8hNRlYCnW4yopuMfhk3GXXdNGeBLuimuY_9pjm6d4fu3aF7d-jeHbp3h-7doXt36N4duneH7t2he3fo3h26d4fu3aF7d-jeHbp3h-7doXt36N4duneH7t2he3fo3h26d4fu3aF7d-jeHbp3h-7doXt36N6dj-benRGacLDEe67f6VQi62JFHLUAP4pBsbcOX5ek2H1UtpsY2H3UtCHg1SmI9WcMFltYcRv3a8PE99Pr69K1unNNu8lR3X81nSpS919Np_gTIvn5OnfU4G8nu83rbuV1az31SiF_zbjoVyZWUSHtWrUn5rhvNfVWpeReJzLKoSmNiiuCnSGjbOsETo3e6xF7xSzycrIu3muttt6WnP54xWa1OLHFcKrllnGsqwsYGJvH0MlWsagph_28lBb3pG_F7iaO38RdjUy0ko-VyunoKU6axNm22TvuW9Pbp0sJVtIIc_UtT8mKCutZM-5bz_tME61S3StMjV0-KWp4QVd7xn3rfYtGuBnLm5F8eA1GYAKnSi9-BCfnqKEIyCDG2vS09oDdBtzaG9ZGvIZxGVJAj8zy1-yN6DhZDq0xNP1U3zBQv7XV02YfmMzsaxrMbQAzcAolUXs_ueQw9fIwSTyWZUy4ZeLlaRAlaWBdkwBvD46LJLXgWh2ptSoxHoaP0p55bMY0S8JoJRudqe1ayWSHkB1Cdsgt7ZDd1dCNjlwjHpf-1C0N92Gk8VxYhn4U8jhORBjwzGNpmJS5yEQufOYXocdcmNUiZFkuYiF8D7pRuGHKRKEo2D2v1CWHF8L_OuTw3DgLkwx8MZLDIzk8ksMjOTySwyM5PJLDIzk8ksMjOTySwyM5PJLDIzk8ksMjObyPXw4vdlnGYz_LvKAYlMPbIwY5YBdmvEi4V6SceR9EDO-xFJaRDVNKK-v7rUkuVarDVFQdDA7tJHSlss5mmjVptOi2i-g5_Rp6SATaUUSPFx7L48iP8oYG8bOJ6NXsROdYid4paTZl39T2S5OSs0X2zJNf7PHk9_Dg9_Z29LBWoNOm3Xdo2RkNut8r60d_-AStHVuM7_e31-L7Xv1J1dn8_ERK9J2QRN9HINEXlFEguJ97ceEPSvTtGrfv39IKL05yPw7dULJbeuT5XvTlPPUVzpXM80ledXUkWWGS44CdbkNUJSsEt_pNQCp-zcZVd6NTm71REm1t0UAY2luqBv7Baav7nc2seTZFVhRuMlwGNupNUIsI2pso7oJyuzXtlZDJLRptAedBHKa5z7N8UN7vsdX9HWJ5ttRf8_K_Wrk_HoJNxJOcMZf9jHJ_ttSfDGFsyfUreiFOwC4JQGdvBUDPK3gZxEEQN1T9TgXAHTJzpAVIWoCkBUhagKQFSFqApAVIWoCkBUhagKQFSFqApAVIWoCkBUhagKQFSFqApAVIWoCkBUhagKQFSFqApAVIWoCkBUhagKQFSFqApAVIWoCkBUhagKQFSFqApAVIWoCkBUhagB9CCxDcW7BUqj4xQIum1YiU7Erg-2hEcTqE2V6ts9DkF7SpoUWVYP9Q8Pw6T2ZTg64vbkb4BYVXYnj-NKQ-1atKFusQzTpcKCvYE9BNl4TBG4t4MrLpvpI4JMPJigPYkAmlCV02lLg1rkwX0dBECbAli6UConWTlhyLs9SMzat1BordTZ1idbV4mzQZrtH7Ne0alZNFhVahmiJQp7R74J1qYnXjnljzSzsxh40YnaZfSl9DdW6haPw1xRq6rXFkdIt6dLm-k1AmJYkJr9KMYT3Ak0t2rs4yE200nKJRzeGw52PTkg7s-X6yXKyIWYKAATdkHgf3rxBuEiWerVIG5kFhJg7sqW9F3VFwDt60hPXsxWkkuYzWzXZJrl_MbrC7-lmHlpD_U7dU0AeRR0rcKPPdNMpKr2SZcAs39uPSS6ERaRCmLIq9MHd5IZK0jJMwzQomktwP0jgQeczD_lfqkEcKgiPP65BHgtMpDUtfkDwSySORPBLJI5E8EskjkTwSySORPBLJI5E8EskjkTzSPvJIcQjeQeKCby_Cfnmk37z8qw5IKB8flfH7hkM2AT-E7ZGrcVG9b_f8LuEjzMFO5UjICNdO00Wmb1SkqUujCPEVC7GL7lAPMb7dbivKr0IgEnA6cOaTGhCpAX0qakAhi1iQunnO8uzXpgb0pTnnrSCwfL7XfDBHvi7imXkREy9WRpWtE4QmTksDBwvpUQ56p55EVsg76Lqev6uOl9bCu4YHl9-8qxWHvuj66Atd2njkfNn8-IzUhkhtiNSGSG2I1IZIbYjUhkhtiNSGSG2I1IZIbYjUhkhtiNSGSG2I1IZIbYjUhkhtiNSGSG2I1IZIbYjUhkhtiNSGSG2I1IZIbYjUhkhtiNSGSG2I1IZIbYjUhkhtiNSGSG2I1IZIbYjUhkhtiNSGSG3ow6sNWaIpIxt_2ic_ZJFF7lcJ5ENrjlg1WWjupqZdgeNbXqhD6Kjdi5vPax2ZEy0XI-MATTQOVhyeEYeSvyVG52i7NKyuQ80qWEtcW5DSBtXt2OM97uv73vbVOjeSVAetgv3QwnqD-Q82Mv5Un7wSdIdJamg69BAfSWOrU7HIbphTQUGSXbW60q_QokcY7pDCwFpvqlP4NcdQI2glU27cN_69b_tIlJOZetnGRZLZD6U09e9zsNK5kU_C78kBshl35zKquGAyigMmBloRfIVukqTz2S89rJD0_ELqOEl7p6dfW6XJ7ESv5bvWg1aD9QE-rxEUAz3aRJ_f1PC_jX4C-7iQQXHsCJ3NwA7bT4EpSZEq5wrX556bpH4Sh6lflnkzVqc491pciHZ3KNpZ1-DYKkxGUme7ChNtintvirvLanWIIwU_dWsffRC9pwjMYBRugonne34c-KEnogwaXXqslBGaKC69LC9ZCaaFC_9zWVDi-4Cfm0v8f88rdeg9hf6RH3XoPcVeGIKpUJLeE-k9kd4T6T2R3hPpPZHeE-k9kd4T6T2R3hPpPZHeE-k9kd4T6T1lfuAJnrAotMygT1Dv6WQ9Wql0RBqFeVEu9cTXoT2jQr8e49OWkMZVGO1-FSecSVS3In2UkiZnjq0mpj52nstjTSL2dDC9UgIgEsYB3bMehq6avQ-LV4IGGNYYmClJWYS8iJiwQg-7ak0pI6ha5eq1vjMmR2so9ekK56t3WzkpeNa_raAU2ClY79rYGtkr-Njv-PgLq9W2bFP1Doqrm7T-gY8fCERFtvrl-5dIXOuKBJtKvscmeth-xSevjSQuYHpcTmYSe68cVOshbLiPDz2V8UhtGmqYFP5dVLAxQUXNIwE8EuBHxxvG2FJZkzjVrHZJq-d7X_0r6H7BL21bzdpITDEnXluPrOn8E7_9SdPvX-EzxzVEdn3QvvI3P7WeDTY_PTGfHsuJarSFft8SD4P58EyZtTW08_eGg2C9z4b811de_0d-_a6bHwX1y67NpfqZr3zUA_vju0ZBq2qeOtEfGgocfHbi1S8JJY42fvXrd5S_1o2uf-0Z30fQIWozsrccKy_TdAy6BKdSdWsqasTSurkOjo6CbqDBrth6iqpnivkLlPIXuaPpOS0zXtoF4fWDzYCue0e1R2T7STUe3mqrnNR_af123OqBp3r6y2566lu_fB_IAevauOsxGP6KHIgv5Tf0_g5_fEqyb78u2TeRcQT0-kmYJST79r5k36Q1Xl9QlAu0njCTXulJ1Z9FR-cL2RsqhtpO7-bwZRKUI0E5EpQjQTkSlCNBORKUI0E5EpQjQTkSlCNBORKUI0E5EpQjQTkSlCNBORKUI0E5EpQjQTkSlCNBORKUI0E5EpQjQTkSlCNBORKUI0E5EpQjQTkSlCNBORKUI0E5EpQjQTkSlCNBORKU20FQDnb04s0Ipt-owgPWnHl9gnIu7CxBkQQtnaG_SuyVZaJUGCRTaF9H1tCIDDGurFydrqmN4h0K6Nie6lbFQVaEai-6r1bBOVPV0gUYaVCcTrASJ2Up5Kkvw7HSL2d5VePE5QE1oAhV-EGZCukj3FdL32lFkndQggrzKEIf_OEETVc5T3GzsMFxNUDuoAum1IhKwYnMY36Pjf1WphaY5hRg7AOhAoh014bZH2pFAoU3hskP3axMroFuteArTUu3gG92l_GyoCd3L31DusvK076HtltJkab0HXONu9diRe6aWrbEBncv3XKkrdJ1LLNu-FCJXXuG5TjfrtCNZlp-S1Pihi-0e3mWhWWrxzUGW29R6ky0i2pgu01RTQkLWHJvN7flu-J6jQxeA-Ldtfa7onyHtjULarlrc-6CxRw6DRpE3-7Dshfkr67JwojtWtNdQGRDq6SBdu3akrtgv4bUGRvw1c59cjd01sApYGU3d23MXdKfQwPUpNr2acltc3FD-36Tg9i1JXdJUgyeQCaevk-f3DbgPtASK3S58_K5Q2xzoCVWrGjXltwlmLSbVLPln6zZoFpt9phzTMnMZwVqVij3pw664hFS6fB0n3_RXeqfF6hbowS5pMfAqlrhBQvtdBXWpIVNbpbNcO2O-9yG7gacYFIJNeFs-_rQhNnWBMCktldL1Myy55W2CjRjNWULDUOQGtFvZYzepjAaOQ4rhzDucyF6Gm50s9vcC5UAU2kBu6MWSscaw-B_Y4X0w2SPj_vsnY3paASx8Q-aWsbR3NMkXLRnRou5DG7U08HRZ-q4z67ZoZaNsjV_USCiR31FBQkwbgv7VaUxBjp1j1ntPjNmh9ob5WpllkhDaorpSxw4FIfqs0x2KBxxughqxYZa6PtqlXf2m2WM9BX-Z1Q-qs0MBZNXRLmGalyu4OA9X6GMgT1Bmn4c99kdg5W2OovbryO3RrlRNI2wPp5grE_vV-M-Q6Ov6q_F4lyLs9fnaJOKq6GpsjxVN06Nc2iuUESZ9lfGfZZFb-31QMJ0nys3UNkVjTWje98i2UpsTz1j2WIhBczGfabEHlW3zYa7tcAyIbbMY1W8aFItGISVyAFpAWvAU9WIGHVNMstO2GHZGGtAM_wktANqw40WQyCDVVmGwPZJNRPnsnN0chV3nzYrHeeTBCYUBgw8Mt_ACamA1H0GwHALNGFW8QXUDQftLA18fr5iUuFUr6u6LTrFNlLuc19LrPBP75UAj_XyVH4BSgFdsukmjFwtKuXvSjPSJLIl2gvWeyX9HYmTXS0xOTvuCxb1XxYBE2k-VYlH7UI0mcaNdV81Q4SMCDljrH2nY8lbIaWtF0KYeV9vIa3ZrvNm8qCw912de5Hb77gv4NRb91dCXLWAadI3sGJQshugymZTMNtAIzGo5inOZYxAgj94MefSpBn3xaYGBuRSQ6sHYlbYAVhTncOU-mjXc_MSME9xsUhQ-bgvgDUwHrPahmwWaW1-yEsrZKJULIylaHBIfXGtodfN8X4MZfi-Va9i9ggNObJyR1riRmngqBNS67UpNcLltRCztiBOI7_WFyPrbd1TrGjWkBNk5WoLqQkXMuBs71nD-4MVSRvof7k5KPkIDLCNFsp2cTCahmNfYsQLBhvhtVKGaG3Au-7-OIXdg-nguG37T9EM1op4LZvdqDnoMLjE0nRLVsJrWuY40wDvfpnKGiFcXSA1z0gi6gNU7zD1ZG42mMO2HYom-qHp93V0uN09vJWqxPVc7Xl3SMFElOWlJ8KQlyz1RczyMhDWVNGeW5N8UHhPlcu6sd7PvivEXMew_a4QyndRvovyXZTvonwX5bso30X5Lsp3Ub6L8l2U7_pZ8l27X61orqxTFulReGhdXpcdmsYeee3L-ZqL6j7I5Xy5iN08LBI3d0ORgl8fBm7iFUmUe1GRRdzjIgvDqCi8IBB-mSapW0ZJGbihm_quH-79pht39sVHUXgUpl139uWBn3kspjv76M4-urOP7uyjO_vozj66s4_u7KM7--jOPrqzr-fOvrQIktxP07CRcrQyKDYL_nYJkJq6GoYBy724TLLGXm5yIg1r-NYpjRvYnCZTOMuurtkCJ_9WUBy23I5ct3XM68NT8tJQDepGqeUP6EXGeRp7iQtOp9dosDTpFCOHfZdsyEErPwFH9DvnmbwQsBZKXs7nKDk1nRpa_9qbv1OKBhcMPFJ8c-vWQnOtheB_cnR9X8uFrSrSyY5GiN4kEJV0urZF6yqqi_lK47Pq8x-2iVws1DUbjEub3dT01Rrk8aHZYGTtp5sXlx3KYRMyEqAo3wqVgaIcphUysqDuNGwOLHlc4U0WeL8KdAq89LR552aay5qPBxK09enS6DToSwP1PR7YiIkUcWzmF84l2zarjHEm75W8UZe1Sbvo4uZPg8LUMQ-jnEeuVzSiPFZSTE-5u-S01hbHH9SZOZTgtspvX-DXaTv1IEiX9laQ1_eF1hlwA2NdK_xsJi9l2cXKostK6bJSuqyULiuly0rpslK6rJQuK6XLSumyUrqslC4rpctK6bJSuqyULiuly0rpslK6rJQuK6XLSt_TZaXv_0o-1_c8kWc5nNzpvV6bZ-4W2-naPKk6XhkCqwSq4xFfWUkDjQhW9lF9Gkg9AXk81tegGX3oztvO6vmvDavGsm_p3Gp524E8Vi5Sz_MTP_Dc7JO8zK_zlr6f9YI2up7t07qeLQxhl0jzJMrz8v1cz_ZnvSQbLWm9MK3DUV3OpbUG1BqXXO5rNn2jj2U4W410-OZ0bLG-77hf071odC8a3Yt27_eiuVGeJSWD-R2VdC_aJ3ov2tnsmJubyDaCKIZcs1znQ-1z65nKVMki7u3urJ_1QqnMDZKIp3FYliFdKPUhLpRy7vdGKLwpTeG42oU1Dvuul0ENuYl-GZZFmuR-ng7e09PBjO6fe4Ub-n6S-WHQXL_76V7Mc-e7cLA0A8jf6S6cFwul6Sfbt3YtDiwK-14cDPmu4c0OZVxNXphT5947LsmRIeaOW3Kcj_6SHL8UcIYLV0TN5rl5Sc7BwbF98wvStu3LZpr4mn3fzHr8TK81e-9oX0DjDN0_A3vCwcFTK-J0NtMhJ2zNbnfFrEW1DuuwFuYaMK7VgtXX-Hmn-34ZDZFX7pG-IEZvPArb177SZU2V7Bd1hQsPC5enUZZnWfQBr3C5x2tVninLS8e06kyIdb_JLc2tHa9VoRtH7ufGER1_GEk9qL5rRt6Dvkq3XvAu4nBPbeEzI5K4YSaiJy43VoXGhIdgRkgQZ33iylc2MnqoJ2JFN3W_VHUk2ER5FkIefridtRW1TKS9W3rMiOxpvS9b2tI0uhaY08pg6DOVNw0u2tRc16USHero3my8znhVGlg5xVuHYSOBb-srtzb0LHcXA4s9LxBRFrgJg30sLFgciSDKUlvBTdkn9RB1tE9NOlsKrGZ5b5cCez9zcnfJM8N0b_jt3k_djPUPQt5PRJIUeVyGeZy4LC-yUvihSP0k4GkSxizKPS7gz0WYJnEQ-wkL0jjnqZuLMOWp3_9KXSz9uJulz5LES0NoKLH0iaVPLH1i6RNLn1j6xNInlj6x9ImlTyx9YukTS59Y-sTSJ5Y-sfSJpU8sfWLpE0ufWPrE0ieWPrH0iaVPLH1i6RNLn1j6xNInlj6x9ImlTyx9YukTS59Y-sTSJ5Y-sfSJpU8sfWLpE0ufWPrE0ieWPrH074Wlj3SBhLks8lKXWPq_bpa-8m5rapZZMMNXxdqtsr73Oex51oMXy8vpbo_iN9XDym5m0zG0-8fBh1vf_FxtLBPcJq1CmlGV3sBu5a09BJ1tJo6apaRsQMoGpGxAygakbEDKBj-zskGfpkGfmsGgjsH71C6Ak6h8ha7eoke4QMamGuGClST1zGzpgtlqOu1RKrCi1zJuNVu-Ws3UF6Hs5WIlbLr4lrC2oYu_7YuW1NVaIe33Va1ZtnWdVjj4fdVpQnJ1nVb87YO9pwXGbIrGZN1EpdSrIWJ_12BZeMv9C9xonoUA3L-0jQ62ICr30DYLitGUJhkuGhG6b9dZgIv9C9x4WSsbvX9pGy9rJXWt0mrjZ7Uo0fLbf66YHO7tCt1ctk128p5KtE7XpkT7sO4tSh0w9oQJRRB7nthWFONclnOlTDz4y6bh4-xs9wy8m8W6bRrUtGMh6t2jacletFwzzg0Hd9d67kLSHXhji0-6a0vuSDgd2o4aHuIe3X9boqIZ9IaVuGutd6EtDgyGRR3ctSV34xZ28cyazdeQynZtzF1YZ0NnXsPS2mta3JrGZbqg4WztWvFdSF0DXWDRkXZtyV34SgMtsbg6u6-W25N5BlpigfZ2bcldUH1D67aJku8xQfcPow-KUQ3Xd5eg-pAV1ISA9njzXWJExkZoAkK71nCXiNFuwnGWk9ArHPdMwEZziSFMCWoocMEtRXExwzidsVbGfb5Cb7knc4QzYkrP2t1MPnDc5y0MtPNqyhQBEZfGjxqhLlMGl5gldmwc6bjPf-hv75QpkEInXtmEXsZ9rkRvwY8xbV1zJxsrvla1G_e5Ett7oglKw4qsFAtViWQo5LtGLI_73Isdxs4g35tcTZ97MdDemZxgFsCzVvRbzg0-ojbyx32exg6t1dHOnrIsH6O3rK_EFWwoKoRqijFB-3Gfh9Fb3jG6BJIzDgcLCvs5StgFLX6ntvjh9TcmVuNyrDkXrYLXCsLIOvYp65hZ1jG0sSeZgZJ_cPgKX1faipvnjQPm27mWSWwkEjuNkb56vpa1XOtjny3OZexPJxaho8Z9Bt5wgdKGbkktyIFjM1bPta7irY27t3ixOFflwzGg0OzDs9Yy1XdpMm7AOkna1ULL3dilNGttdZVmeVLDpS2v5yPpOhjmQ0-J1uG6pQeL1oHavQNaRsrWeSohxJZkqGWZdBduObTDL4-z_1yqmco6-l7dMvl3m-zadOgdnA2l143ynsAmgqNjjmgJoaskNBUz3mCULsSVYFI8TLV-3GcZD7dZ09EL9law3tVp-YLDpamppIappywrrLF1am5EMrbNe8s12em11TZnF9alXwvW07xYVetKtGpjlFoIHUaV3O8VNE5Jis1r3d561ukDQ5OfYKeX2zE3ylf7qdKyTAg_9pkf-HkYukmS5XnhlqV5c0wdWHqzRq90u94sZRYos0CZBcosUGaBMguUWaDMAmUWKLNAmQXKLFBm4ReUWdj9khNzV4YyWI68Q_vWDPkbtvUoPDTtPvLin7ovy_ggF4SIOE9LVsaRG8Q8j4oo4S7PRBGEXuFmURm4PjgvrkhhK2RgGxW4EfEs4qHvMfjXXV564wqR5MgPjtyg6woR4Qs3SnK6QoSuEKErROgKEbpChK4Q-QSvECFpFZJWIWkVklYhaZVPQ1olzeIsTlweFEEyKAO-ljIZkPrOXC9PwzTJGmmyvaW-LYXvAV041LQ8m-0jaunsqmlZy6tviloa-WUttqzZm5IQLHpUBSUDuJZa_oPSVWz0LC3Z1ELv_0udVtbSlUqiFDUI-0cS1kvp54mPaii3k-n-ay2S6_wVel9p8prLjurePHvwg7rnxyg6S4v3SzzZ5CMT0z_13U03rTuN6ouLZCknPbrQduX_-M__asYSf2liSFoBu9GXrWV8G01ZvPXIkpTVtZ_I2k9tKeKTbinigSuTTpU6sFEibv25URyWfx7cl-BkTkXkuUkYx1tEe7uQixh3lNfJsIHbYtqa9tJIVaL2aCY3KsD7av8etsRYh0R_uwV_W4MzaBKDl5FkIYvjclBxdy3b2b9PJUWCHhXL4yzrF9YdWi8nLWFyvTBq8e5XUrwbv4EjpafGV7aGt6SevlOTsFlcZna-UzNPfufYliNvf8kS9la3jMGwzFeV02rYlvlXwt7BGOzXzA37JVOtLbtfk7lHkVnOMqnI7BhBZuV27aXI_DMrsO6uvloUXl6ykIk8HVZf7chT909Z8HtikcQZcwuvX221HRnuiQvvppm6abx0BPJ30C8Ad2dHAdUdpFOlDtQdtFMLH--Dc0uWBOlttFMPLeHUww3RBf0yWnhB-nlaeWG7yKpjaay2pFXPZrtoqzqd0qokq0eyeiSrR7J6JKv3K5fVI2kukuZ6v9Jc96uoVOS5G7l57LIyHFRUQhjUmuvbxIowVFdZKCn9gi_-cvr8cSNPRKJMu4ky2TcQJHnOwsgXuQk3WWBXPTp3AbF-SFkwEpu6g9jUGjVhJ0R4N53ZKrmXcPn8Ap2ymSJdOlZeqmZelXLONWScLg6jlTBcI020mEJW6bko5RWzvRRkK5e2Y5G171vh7FAAzi11WMmKHevAHAHrL7uL8XSizHB1QGie02SmtGTRNGldciSZTfkNMmqL-ipSq_oJnMF8AqvQXGTZYkFVq8tLTbneg-wUge-eRmHpJnGcoFRwIbJS4ru7yU41smp_stMtZ_bu7CyDLLPwZD91w8I-CFgu4hE0Ls3d2I_TOBReUoSB65acRREYYVEkWMbdLPPClHuwJZV-mRReEAmUbE7lRbo9r9QFhQuPgqwLCpclXgQ9RFA4gsIRFI6gcASFIyjcJwiFi9Ii89Icdtd4VygcAd8I-EbANwK-EfCNgG8EfCPgGwHfCPhGwDcCvhHwjYBvBHwj4BsB3wj4RsA3Ar4R8I2AbwR8I-AbAd8I-EbAtw8GfFsXJd4DHjR0iUcXGG0D9QYb-HIdXQVDL9N2sE2KWrYeDJYF5pAN_K3C4NdMKdh3wb2ezjE7KItuHrIqaWBbGgsG800nVWEq7gfd8uIy4QFHR9TLg9znYejlQsb6uqFbNRJoO3TrPsZmd6DZdtyWwTB9ENxWWHA3dnM3EEXKI-jhDEyTHP4fwL4Ue1GclFBQVIa-F4Ys4UmBiqhlmKaCc6huP9xWBP_rwG2VfhElMXhOhNsi3Bbhtgi3Rbgtwm0RbksEQcDSMgbjxLtX3Jb02gm3Rbgtwm0RbotwW4TbItwW4bYIt0W4LcJtEW6LcFuE2yLcFuG2CLdFuC3CbRFui3BbhNsi3Bbhtgi3RbitXxtuq-QurHAR738Js7nAUke_j5yXr_GuW1hrN_Dmr4cWxm7gL6tta63QyC9YULiTc2lt4omrbhiFQ2b2pkLbUe3NZt1aiS_d6DpHKOP_CyG3Z3lDrQwH98HCdIStrs68Xl0obPQFblL1XbjXFxOo_Q10aa0DpvFieDROKrEfUqyMysTPilD4cR5kOaxd4bncC_uQYgZ7tB0p9tHMht3BcRsXUP7Ujbv6IFgzL-axVwY8hE4UblGyMPWSjDGPh7Eb8Cwq0WtOwJ7y8zj0mBCJDzaciIrC9UOX9bxPF9AsOYq67srMEi_jXpYQ0IyAZgQ0I6AZAc0IaEZAMwKaEdCMgGYENCOgGQHNCGhGQDMCmhHQjIBmBDQjoBkBzQhoRkAzApoR0IyAZgQ0I6AZAc0IaEZAMwKavR-gWRH7IvSjMHSl7SdHx8Kc1Ov-DlgS63ufw5q3HrxYXk53exS_qR5WQXM2HcMb_jj4cOubn8udo1VAs93KNMBuZa09NLSMfo0QPhX07wPyrX26Bufb-HQT1HcE5iXYfxzf69MF-PkCfDPfz1uQrhbGpRfT9ZuXx30bJIac56vl-WJ-3QkTcHZD-FmN60b4gT2l7KXerRqbAO4lOH5gCWPkqEHXXYjF3JmxBe7Ib_uu9Hw6hZNUPiXqNPhudU1mG3Upc1Id-vjZlY6roSWgfPamsFFz4jamytuJPPubAIVOFmGMSVqpi_2gglmRRlERBlywPCxy7hZpwYKi6IMKGvTYdqjgxzOvdodHDmMFG-jcB8EKCld4aSLCxI1jPwh5kGVlwGOfu4EnfNjHeZyCoZ2XIvSC3IXN3HUjzsPc9SLwqvmuWMH0yA2Pwi6soEgjL3aLkrCChBUkrCBhBQkrSFjBTxArWIQpL3w_KeAAMiGqxjrRTb-L0cEqp05pza9MLhujI7P55Q0G9rDBwgofN9fAP2xbkxY-TFmTMqBMQEgCQhIQkoCQBIQkICQBIQkISUBIAkISEJKAkASEJCAkASEJCElASAJCEhCSgJAEhCQgJAEhCQhJQEgCQhIQkoCQBITcHQjJYp-VXta-BfWvOudsSwMqvMIggu23sA0PP9qxMRuRPXAQeB5E99GQxg4-OJDu76Hz5WQ5ypmMzzT7to5gHBzUPi843h1rqG5ikSV-UvJ76avXq8lrhUHAZi7nb8QMT5qlMl9UIACTyq89Pxm78F_vKAkC7_XY-UoMNFFkqR97BbufXgTjCL4nZtXFHJqZC9gHHGkOSPsfdwq1qGSs--CguplBLWAPdEJq6ia6aR6Egt3LQL8DC15Gm2B5roTzrg6416EfdFWshLbOA707m71zRqOmjQrK2IPGtVZINxr3MbrCEo4hK8K9YfQWbCTsFLQO2UydheCNNHAEHc5EMc3uRdBd1ymWN9FBK1kd2LdzdQVzKyinvUCO0XXoBZj-MFrloRbd_Jfn336DX1lVuocmM2yMjQ1AE2_cN_23Nk5sTGnZOgxsOd89VtbQsk4HH9a-1WEdMdTRfQUoNXHMcd9U727Oo0lVTCVUwnQWWr4IsOLYCDDjGXaCmbZ1pW8q3ThrdldCxgPRMB_3TefuZjy_mF9X6lB9okNxrWVVT9CmGQt7TktEFOznGGZhlyak2oxSD4Ibq5VzUQ0HOj_gyoqmDf0FK3NXJ6KtKQu-E-LAZ8bnQRembvVhu7_UNNwPl81KP4wilmdRycMsjN2MRTz2sj5ctkHqbsdl0zFHxxwdc-aY250QsQ6mj37qxsp_GCHhMA-jkokgKt2SxUGWJ4GbswzWVMxL10_LVIQsxFaVIvWitIyEl6c85WHEsiDveZ8OcoAXHLldN9YHnkh9n2dEDiByAJEDiBxA5AAiBxA5gMgBRA4gcgCRA4gcQOSAbeSALCl9dNWKODC7qRWdMbvzLWIs9X5dspTHeZi5Ta7LCrtsYGX2D55Y4Dy0edjZTAZUMaCYw6E2tsBtdbIOhqEB8mvogNp9G4tGgvLYlQSUcnmCGtSodNgrGSlZiLK1jZhReq3wfrIp9Z1LiIiVsd0_yJ7cxEguhKJKMPVcE1aUa4ZNpEUhuQUGRAlHidpQDmGH1WvBxlOaY6M0c7MGVG6DUfp5JGDFxKly1hXwowlH1UfGHYJK4kpFg_X7n81wM1NhTTinMcOpoqUSNSac7549QYaKWpSHGqODX3_9J1nvP4_HY93vMrB6NvvuMYZHddhZtGK5hxaMokYTIeJjhX0zagKwOigum6cw-XUkXAakZLCYgQOBQX05MVrR4H4PXRRlXILTkgpzHluBNBswectwWL1PSESnNDrqSePY1gd8YhNR2DWbSPvYenH5nYUGZtu2y9j5UsDhgyeL6Qd53lUoPYKx6cur5Y3a4K2by7BFMt2voDUPMZz_Si77V6vJK3nMXt28_uGzwc8HcSqJ8NNQuJhoN85gEwLUnXunQN7I0f_EX3_z8rnJF5iQfitxAMN3LSe2AT9L2MrI7uW6h-31a0zyZtt9KHtitJroh0eyBmmGO-2m9Exm0xgcVrM_SKTa9dzpAM4PNmKtEt2OjTgnEdKIkEaENCKkESGNCGlESCNCGhHSiJBGhDQipBEhjQhpREgjQhoR0oiQRoQ0IqQRIY0IaZ86IU0nw38JjDQLWtMAp1tQHV0LGNYyTz0AwrbgJvuWZcJHdVlBELluHMRby-pAweN--LpOXsskSG9ibD0bNoSCT7xM-Hl0mxYp1M1twSwD3XR7aH7feHbTsqxpsvm8pt58bWJxNR-rIdnIDKHkBOl4Vwnu4nIEbrGCVqEvougzGA7A2Bim98d906u3DeauBo3w5apmySfC884k76ZsNWtwIBV6eM1Yjvum4i5MrIuFsN_cwjbozGltodd3PWj4kYPO5xLNzBJdnnHf5Otuw1MTbpd3NWjYWj2rRsu5dddDvakj6EFFvMCbkvwsNpXWor6qYpD-tdn3Jyospcq0k9p8Atsr0pf01RhmbKz5L4dJj0YPxwrnl3y-mTstuhT0G5i5F_KUwrkEhxha3Wt3aigiWn4j54T8qwNuAFtA8yRwHMNo4O5OpRvQDKMeo1yUMhkAZyE-u7xoKF77sa84zzgPszIUcRkmRcLSmHlF_60YhgqxnX1FWzpt6VvuJxng_q1TdvzDptyj4Kdues4H4SOlZermJQuYz4pMJFFRBnnme2mRCy_zs9CLQ5-leYo3lIBlVcDKKpIy8AteJJlfJLu8XBc5Ke0mJ2VpxlkaBkROInISkZOInETkJCInETnpl01OcssE1kmUhUIUPys56bmclTJ1vuG_bHot1dxCR5_NNuDRdTT6sE-mAmEGtVM_ubwExwn2pOnNAB3Jc6OSJYJ5grFfBx1JEVTuj82SBUXixbCLMM_AaC0Xqu7BO3hGW6DfMCMlqhSxC8qvBmfamtsbhBXpaMMuDdPNTEFMXqnkHOwTuOHmGJ34UXCF5JLyJnpPrF1sOEuKQrJx4AiswbrOzXy1cGBm1vghgwerlrBOpR6KuUVzChuqxDqb8I4BmdSRERPzUBi8gZkMHg7sIhkvg9Ls7Zbj2J7JxFcjvhrx1YivRnw14qt9Wny1iIk0zTlHsse-fDWm75qWR4tehXI7er1mH71GzFVNE5PWhsp3IpQV_YjzTbbZui07kUloCWGRc18lF2Rx8pAn1hmxzoh1RqwzYp0R64xYZ8Q6I9YZsc6IdUasM2KdEeuMWGfEOiPWGbHOiHVGrDNinRHrjFhnxDoj1tnPwDq7_XUdO3AWhJ9lWRLz-7gL5C4pmKEmhnHAc34vTTw42CXBNHh7il_mCVdQxXvtsX0zRbtx0TbvgNrkIj1TaKDK5Gtx6QuZioLWTFeXMyuN6aidXaPpEPwwkuh3x86EKXTduG-m9V6KhTdgNTSr3nunlgp0oZawAt-P-6ZMd11PsH2qpg4En_W2k1mdrJWRQ2jffLVGebMmxP4vtjnqBjXQ85pdbC89gjCF2WJU_duKoatmjeTavV5y8KAhXA6lFx9lYLRe4UmtTA75ttjay96-3p28FeH0E14WuGUQlSzk4HjkqQTxdJK3DFVkO3mLdkbaGXfbGXcnFK6zngKb9eT91E1q-iCUrtLNheeVKROBH8d5IYIgETzM4ywAhz4QUQ4_Mi9JEz9J4atuBlWAFyVy3xNRGu3ych2ULt878rIOSleZpCJlLCZKF1G6iNJFlC6idBGliyhdROkiShdRuojSRZQuonQRpYsoXUTpIkoXUbqI0vVLoHTxoox9ryigp_x-StfBgU3pGowaFMzHIGKR5AbqYUXdjev1cRC7BqB_cRoWeSiyLDQIGCs0b_rl1gH2GsrFeMgyFmR5ZnwKK-be0V8_G_tsIDhK1DOinhH1jKhnRD0j6hlRz4h6RtQzop4R9YyoZ0Q9I-oZUc-IekbUM6KeEfWMqGdEPSPqGVHPfl7qmRVGbxD9a4H53RkVVnB4_9JUCKmb5GQ1s5fk9A28P9qocOAhBgatxFaIEdOPb8GShWPyydfO31b8_FImcTVWT4d1dFa6OfEY3tiE-J1C4i2v4OxTQSWMdPa9_W5MLJZX0mC2zpLRuUQ5IWZGecbt91H5AWzzxsvoQAGrX-BK7g-LbbdHWZl-efUYmkkLTP3KO6FwhCV0qacZt-jQ_bhFqReKIooSL0g4Y7nnZ3GY8Mjr4xYZzsJ2btHHOPV3Z1YZokdD7_B_6mZvfBDuCuNpHsLAeGEe89xPE9dNyszlQc6LKAvLvIRBjHwGxfEkKTyRxQHzc9d3IxZ6cdr_Sl2MFf8o8jsYK0HghWkaMmKsEGOFGCvEWCHGCjFWiLFCjBVirBBjhRgrxFghxgoxVoixQowVYqwQY4UYK8RYIcYKMVbeC2MlyJif5bEXJ7n4JTJWHnWkg1SxN07D1mhoLH9Ar-LJ12czmanaYLI4a0QWzBdtJJB0QssmtNjO0U6MltRPQi_xWJo2y-I9MloewZfbXXUiu6qP1aJx-I_kw_8CDz_52vkX7DH5gMm2tZFI-qF_kQ89q6kjzrHuL_WoIVQg66Qebf3kM-LNEG-GeDPEmyHeDPFmiDdDvBnizRBvhngzxJsh3gzxZog3Q7wZ4s0Qb4Z4M79c3swa-0UCa2ABi3KKEOP3SW4BS3AGr_QKPpO-Yxe_pbqBTy4bgst68z5dosvuLAhWch-co5i7hR_yqORBypjMeGleSQ7dNxJliSCWEg4WzIrXV778wUFilGP1v9OQhAxzwmDnfxHMiQHeyFbmRMMi-CDMCc4TT0SsiHmRwgEtEnBW4iByo9QXEY-CMIkCPxMlS1iWQslFKXgZcFZEXhKwMtiPOREeRVEHc8L13TIMM4-YE8ScIOYEMSeIOUHMCWJOEHOCmBPEnCDmBDEniDlBzAliThBzgpgTxJwg5gQxJ4g5QcyJ98KciOJMgHkKpkSa_NqYExaoRVMD1ngTtaVZ6Z3bcB_kZqGjLUxDZWrmxSaj4mzWS6mYLHfiUYQ8C5I0CV0vDX5uHsVmrw3TKPr7ipgUxKQgJgUxKYhJQUwKYlIQk4KYFMSkICYFMSmISUFMCmJSEJOCmBTEpCAmBTEpdryBpO_ukb5bR3rvG6GbRj6um0ZO4ciF008eNt13g9yg6dcVsT506li0Or3tCDOsqL3vE_mustKLy4sFHIF4g4gzk5eh2DdxtLd9Rzffhic6uM567gv5boYJCnxCzThpdrBZEznlEwZHyyV69liF_Kpqzwom1AjmJeZQLKyBvOjk6JadtAd1JoCFl4WZl7pZkbM08MMyYmHZd4GIIUL8Mmgw_cShrTSYhhLyQWgwwk1Kr0hy1w_doijjOE7SOApiVrguYuKRICPckAduyjyesIzFZQwnM0vCAKwnbz8aTHLkuR00GOalaRjBEUU0GKLBEA2GaDBEgyEaDNFgiAZDNBiiwRANhmgwRIMhGgzRYIgGQzQYosEQDYZoMESDIRrM-6DBZCzOIh9MUj9Nf4k0mBcmPbSeEnIuwLVr0mp_m-fVEcILuxJFBweOmMF8K2QuXmKkpLeNljDsswcHdR4Jv2hzZ8A9FcwcAr3XkahldnDQTkBBYRO11ctT8lwiZNQR01xN4qzdTGI54NvINUmIpksa-xkLf25yje5WdGTwWd2_3C7knm8sYVObZ4P3vxDLhlg2xLIhlg2xbIhlQywbYtkQy4ZYNsSyIZYNsWyIZUMsG2LZEMuGWDbEsvm1smxULr-Pa7P26RrjZuPTNu9G4w1-CewbtyyiIM3bXIXhdLuulnEu26PTLDLpc_oj-DLcxBJ1rrIzzVM3IEo9NwLX-T4a0Jk9qxOmdRoIz1sVXKrNPbkLbkyyThaQ1V1rrdC8mycIy1NGnGh1xqhuhwqPVJoIMwHr1zS1SbaO-_qou9bn8G51khmKsvKodrbYevP25l9nfGoQr2xiZ3KohwV0UifJsQkNvBLfqc7CGTdfdM6ROhUvIxtVM0CWJWfbb3ZLlSHW2dY9-EBhLskpcR4zN-Jg1WZeEIV-0McHMoyQ7XwgWmP9a2x3VpYh8ag2rZGSGoLOByElFXkZ-0ka5sg6cuMwKmI3cEUsihg5Cnma5tD8MESWEk-yoExC38uSjPlemhSq7I736WAkBd5R0MVISrw0LHgREyOJGEnESCJGEjGSiJFEjCRiJBEjiRhJxEgiRhIxkoiRRIwkYiQRI4kYScRIIkYSMZKIkSRz7J7wvJCHeQPQtPITprP2yDI0gEwBO2HhB6mZTlbiYWg67Zg-uGUeaLD3dNXE4yIeF_G4iMdFPC7icRGPi3hcxOMiHhfxuIjHRTwu4nERj4t4XMTjIh4X8biIx0U8LuJxEY-LeFx0i9J7v0VJWVB1uBkRBzVGYXbecvyl46mBq0ybZfVRz6AMzPGB3Qrfhgdx85bnqAldq8D4fDqHPWHva5Ysupdp6UB79OVKVkpk4GqlZxpSNthkVZu6dmoK02JluFQYwcVGNcgOdH-623V9MZmKOtSL3aTyao25YAK5-5GqYgFndOIX3E2yLHQLz0vz0JPp6k5SlSG1_CIuWRqglG29ZKmh93wQPlPo-X6UpAEPvThifsQ9wUIWsczPghy2tbCIvahgJbwFfpIVnihcL8lEmOdZnom9LlkKkqMg66A0lS6L_QA8DqI0EaWJKE1EaSJKE1GaiNJElCaiNBGliShNRGkiShNRmojSRJQmojQRpYkoTURpIkoTUZqI0vTxUJoKP4Mu84s4J0rTe6A0WYyj_hzj7SlNk-W-RKaQxXkQ-y7zok-cyNTfn8RlIi4TcZmIy0RcJuIyEZeJuEzEZSIuE3GZiMtEXCbiMhGXibhMxGUiLhNxmYjLtBOXqY_F1Mdf6mUufSycJbkfNZwl1d4db57KfFfkMrFy50tpXj58-MOR81vns3l-pPIgFX9j4do-H6B-eFkYenmY_f_tXdluI8cV_ZWGkAcPIFK9LzTmYazYsWGPR3AGzkNoSL1GhCVSIKnxKIH_PffWTrKblERl4jHOgwBJvVXXcuvc5ZzeaIfM4-iaA7ZKqoKQHON9DeE6igPX9uwEpilhEuWJgM_HN0W4mca37zP0OiUg0sIKkbUiK7-vuxICU4nI8BzfRlXjxQl8GuiLn969--aCrPffL394d_7mh8v3777_-sfX0xNViTZit3xUrgmGl6v1KOiJ9OlWRmlDzUzrl-tJdRWnlFbse20WO4RXpyohzKCKHIXF4o5LW7w9PVmXeVrFSfpSPXknTpzOpSdkTNolLQVdIGfx6fnNjFbulCM3_Nu-rozTJqiS8GWaud2C8YwM63LBpWBfiBTjHQ30qysRd5tp10NM0Nt99C0bHbRt7Ik5Pp4Q5kTKjrnjwFfkrOnr_56bRizy7c0iFqaNI3EDPT8eMmz9T1FES_kQ2k7oCRtWYCfENmCr-u9-IUdQlo_q5aDbLazy_Z2Oi46HTMyB7tG3c6KInJspu3atsP5qPGQXDrfadqzjmykQNB5aygdaPBOlU7UMT5lsEs8ZAr7L5WK53WC7-oYaLHNaosWbuUlLBTEmfzy0bIYZrgSInYn37fv3F1uzTlTOmWC8XhvjoeU0-KS3BB1levrt-YWOOJ96P1-cn-rQvQwxm2ewHVZx5gEO7eZCklFo523sJHcX1PqaFoX7fh2n9ExoWleviVThA_8lPGRhYOWYPo0kG5Zd6ldhnftF42dZVyRB14RNOUSSNTTJR3x5EBgLGAsYCxjrT46xHi87sP3Vzex0kIJv6eifhILfhmVLp_lpE1Vd0mY0cVO_K6u69eMipw2hbfIgbgNaE1VZtFUSFXlQNlEQ1zFtG9FjXm6DjB8F7_1sEueTIOoh46eJoNv6IOODjA8yPsj4IOODjA8yPsj4IOODjA8yPsj4IOODjA8yPsj4IOODjP8ZkPHzKohqP6iatLZMc5sd0VGWZ-Q4tLUr0qCofXqMLRB10h7O0n567kLD86YIkiLx87wyvoyTznDpBc_MSWxlfKfz-5U1vOc_fKeR-Wy9MjndkVggIi9o82ASus9tKerfGMWa4LN0keTslaWeM8e95Ye18w-z5WLOG_ke8MKMriJMo7ZtDbnNSZ5sgpdnZkDS0ZILz25HXHFFnUL9NT05BK7l2I5G9o2nJ3-5-Mdf-cq9m2bix11ZllXoW1fbSbS4Y_zMbAmbcI41lHcrbZyY9sHVlR7ZhsB7O_vK1BGLpXx1RpPxZn39b7rl1RltQs2D_PVDcEa3KQWdjS6_UstWHDCzaaVMhJNQFTuPyLKKxAih3Q9SpXltpt4-xNp15CPUSRzVZhk4eR476Mcka9be652DY5M4_oJhmUdjysG_ydnZZs9PT07lcWklnzaz6NJX3AoDTV-rThrLJl_qA6YNZMQdmHxyytCJTl0zA_Dy1_aBGiAvHdGZI98PeBK-Yq6aLkM3j1BY99LuaOYpQ1havapu1T-nJw7jWh0U2yQ1Q4BGfYXG1Ry2d5G1Pr77FhpOyHeQHaUarhG323LzftQmt8W_0N8zJjfby-Wus_vaB29xqrtHAATTdg3MqdFbSH3zjEu1AC9njZgmQiBEv11_J6iTyD62N9SrG32hNlEznOofX2z1v0Qipt8t-D95dcA6ZUkYRXFMm2ZiSt-d3KVeekckIFtasmTOGD2VtAoWXcfbP7u_SuNmJMmD6nZj76sFu75641kpTGfvuLSV5YR3mLHmOe37mkturnSkaSXxJr_1qagiovasVtRLbErXywdp6R6UmVPkREFtUNseh3vZbVH8cZdjIRm6FgRNzAI4FbdyVA2UD7I8tYrvWqxAGuatMh_J6KUNgS2l4GZIjoiMf_DmvHn-xldsjRGQbOT9gg-QNIKkESSNIGkESSNIGkHSCJJGkDSCpBEkjSBpBEmjA2mZJG6jOAsycpXSIyWNNvg08pQdGgOLZ9hwm9gJHOKJWNOGA2F952G5JI7sO3pJ3pPlkqbzPr0k75BcEv_wGyhnoCcNsyOb5B2nmtSmcRt2flnlVTKsmiQIKuWOKFJNGH9BRmf088W5J-scTVGWFUvyNrWSGFU9WSxJufybckkmJPGlmiTDNBedAdiklrnZAuV4Q1oJ0kqQVoK0EqSVIK0EaSVIK0FaCdJKkFaCtBKklT43aSVLpCXnkUHScez-xyqb2IcpmYefxD-Y8UVmZl4K0HpbLn_VFUC_ce2nqpAX--ZMxj7btawL1UQN8Wbz9eDH0-VT5s69ep5oagqXHF9i102O8e4X0fkkDkU0rsV7mtBD6Sd5XWdRk_l1XjGJL627sgiGhB4MBfeZQg8vP-KPV64wVGT96Enwez-9-JOQq_28ytK8C7qasGsQ501VZZ0fxVVKV-Z-2nVJk5R-mORBFGcVnZ21IZ3cBlEdhMKK9r9RH6O6mIR9jOooC8okjxIwqsGoBqMajGowqsGoBqMajGowqsGoBqMajGowqsGoBqMajGowqsGo_gwY1SA8g_AMwjMIzyA8g_AMwjMIzyA8g_AMwjMIzyA8g_AMwjMIzyA8g_AMwjMIzyA8g_AMwjMIzyA8g_AMwjMIzyA8g_AMwjMIzyA8g_AMwjMIzyA8g_B8LOH5iA9m735VWIac-vnNzoMGv2NPKEj6miLSZMqltIuvs3uKtee26tBH7K8XvzEZxLunl1oZwoLwLcm63WzcSxR88nbPZs8cUHGFp_GWfT8J06Yr46ItgiIOi6jxu6hMh3jLhuh6mLf8vxm4x_OuDanXfid5k6dsSbuf5iPQEXmRdVl3SRvXYV40ZRv6QdPFcVU3DQfq0iTO05K9Tb_t0iJJsiJvq5Ye0gVdNvxKPUTlJJj4fg9RucnSmrBoBqIyiMogKoOoDKIyiMogKoOoDKIyiMogKoOoDKIyiMogKoOoDKIyiMogKoOo3F8olZA1KvMwrZODRGXJW_VGt97d7M7g2_HZAIIAsxnMZjCbwWwGsxnMZjCbwWwGsxnMZjCbwWwGsxnMZjCbwWwGsxnMZjCbwWwGsxnMZjCbwWwGsxnMZjCbwWwGsxnMZjCbwWwGsxnMZjCb_7jMZpnLHuI3bx3dYjnvHN3kOjNzdqIIz6P_O-NZJFMs4_l-zpZq_tiPPOd1kkVNskGdtdlW3lK7UbP4V7dYNJY1WzbN1neAufBt-LIei6wb0HUdl9AVxzbAgQMc7qchkt6_yAcrf8Vjt7r1TN7FU8VKPQtHN6_oorgrhP05qnlXV1eyCP0_HPCbisGankzoN1W2tqYJtlJlHlNBv71fqRNo8M2Buif0p9uaFHWXdiJtd1Rbv7qf3XD5nsaokhYu_AVOfXKR7mi9GPFoenJOTfb0YOBXcRoV9Qv0oKjys44K14DoxulC9936OnOoKvf0XRzWdZ0k-bGtfG9o9KoOzxaqqIp0LhfhLpRFzKIPCVbOCPDt6cSwyNoizYMX6MShIjjRm6oKzpR9afQsT9_TfzTxeOs-ehm_mRNO0tHdtamb4vW84urtrbKsK17MMrW3WO7pv7gp6uoFJqFwsd_-fMFu9kx8OV64cwzmybDRLm2HexP5s9kbbp4T-bXN64knD4oWmG-r96hNOCZ-470GrPDgOY4pHDzHMUGD5zgGYfAcZzkOnuOsieH3stNy-Fl2bgye4wzQ9hjsF9tgj6is6_ZOxIW358jGvON5dSpKr7dROVmMrYotTm6fbiTcyFW7Lj_MFsstv7T9qL3ep8l1tFmdpmmYdV0bl3kWE3wsuypuh-Q6jNzDYbkOYA5gDmAOYA5gjj8H5ni80JNRFZJvOSlOByWTrHzQJ5FMipOyDPysi4IwDMKoKRrfD-umDtKqqdMqCfzI96uuSprEb6s4bMMwD5Oqples606s4YMvtyOelE-idBJHPeJJSZkUHCKAeBLEkyCeBPEkiCdBPAniSRBPgngSxJMgngTxJIgnQTwJ4kkQT4J4EsSTIJ4E8SSIJ0E8CeJJEE-CeBLEkyCe9JmIJ0VRXZdlUTZRFVhlIFMb46CiJ1W5aEBURXEZEiTKKhNOdApfdsOJTy5hkWUFbnhvOr-ZUU8ooCQ1H6SeAUeCGDS6uepvZsvV2uYgVre88QtfQEHUKYuIeK3yUQUsbmSuYOy90Sdpb2GlfIWbG3JKZgLz0_wv2TOSiIqZL4IGuujoHw-W2iWjPV8y2jZzjF5ReDEb7BxqqvCLhU_F7rrwZaXPuxacm30bbdDVbeAHfp6a0XYqfexG-zI1O6K-Qx6IfbsnigqakT7qnMyj5zwnYih4P2e3i3qsmZHRY1QxWm01QPbdpexZeYPVNU27dJLGZFzISNdcunPdftxCfL8fEtJg25i3benb7nKKjVR3vUzZkM5WZDQ4flXEQWS9FFtJtAWYj6gJWnHNRkcziLzV-ZkwN_qgGB4--O3Xb2wESlL3xo7rrZ24MzlcIzEqArOYi-6Wo_n9bUWjloXuP--XN97T8rJ3NM3PnJuo8Gh_e5ajLBzL3lChw73jXLd1TnicRjYzkWinMMqB6M8tcZIu00emQrIFamZdp03BqZoUzMFeX9OpFz85txNUSmEwlt75d8ZvFsHrjjcrMnGCKNuxLbDGYVS15VKGwm8JbdBtaZcSKgSt0yr9ZG4P_ck31NZNJyHv59ZX1daukzlu7zsJuZWSgAi_ui6i9Q--lLG16_aGfAivaW9mlVDLkwTEO1bj65iHuLmt7VkmWZWFfhNnvFGZyKKtFTvsMTyi6utFHAwHJ01PxgKP0WGuTm3o9J0na5QqLjZQ9JGTXENMEwB_LUH-UK0v3bWbmdlM007j_LG5ldg_L7n8imtuzJZrH6VwKD9i4rjmgy4BL71-j4Au7GYfhVNALyYMmm6phsN7F3GYM2ePcYtFsk51ni5ROKLOTnnfSiRMD9nYe-fGB61LJaGHyBh7V1v4fTwev7piACFkjGilmatFwIvrDXRk5ubBytAIDvtNI-J79OBz-Qi6hgAox6y9ckW9tFzQ7cq7Kw0jbRzVNHol-LWc9dwAqqKij_CIE8KUbVvJJBsH59i-cOZdqoNIHTmxXDh0K22O_GCjVAxxgNq-yGcdlE1TplFWmyCJU7voBq2fWYXINvTHxVq8xqpmT4QNMd1Q2m8lLSQgmwkps2LgbcXeyi15HDMCf3YtCXY--zRN47HyynR-frO4b_brrZBDvJ7dtiOVnPDaerF6oGferqBvCn1T6JtC3xT6ptA3hb4p9E2hbwp9U-ibQt8U-qbP1zcN24YAaJ5zAfMfWN-03PVeCZO4gRpjZVTEZlgT1euRRGUPHpqo0ESFJio0UaGJCk1UaKJCExWaqNBEhSYqNFGhiQpN1JfURP3l9_8Cp1Y1dQ)
