[//]: # (ob:ae580676)
# Proofpress Design System — Verified Knowledge Ledger

[//]: # (ob:4565936e)
**Status (2026-09-01):** Current cross-interface guidance for Proofpress CLI, Markdown receipts, review surfaces, lineage views, governed-context projections, and the hosted owner AKMS chrome. Product hosts may supply their own brand shell and workflow vocabulary, but Proofpress trust states and evidence semantics must remain recognizable and consistent.

[//]: # (ob:678e1b70)
[//]: # (ob:hosted-workspace-v2)

[//]: # (ob:9368ad00)
## Hosted Workspace V2 direction

[//]: # (ob:efc880ec)
The owner workspace uses a compact, three-part operating frame: a 224px navigation rail, a flexible primary work surface, and a 384–416px contextual inspector. At desktop widths the selected row and its inspector remain visible together; on smaller screens the inspector becomes a sheet. This spatial contract is the benchmark for Home, Review, Ledger, Activity, Admin, and Ask Proofpress.

[//]: # (ob:cfee6f69)
The V2 world is **precision editorial infrastructure**: cool white surfaces, midnight ink, hairline blue-gray rules, compact system-sans controls, and serif only for the proposition currently under examination. It borrows the rigor of a well-typeset register and the speed of a mature developer tool. It does not imitate legal-matter IA or generic analytics dashboards.

[//]: # (ob:06711fc4)
Use shadcn primitives as accessible construction material, not as a visual preset. Reduce their default radius and shadow, keep one consistent control height, and build hierarchy primarily with type, alignment, and rules. A component that looks recognizable as an unmodified starter-kit component is unfinished.

[//]: # (ob:bd3d4bba)
The desktop reference viewport is 1536×1024. The primary table begins on the same vertical axis as its title and filter row; the contextual inspector begins at the application header and owns its own scroll. Selection is expressed through a quiet cool-gray row wash and a two-pixel ink marker, never a glow. The mobile reference viewport is 390×844, where tables become structured records and the decision controls form a safe-area-aware bottom bar.

[//]: # (ob:c3130a45)
The V2 palette removes paper-yellow from the application chrome. Canvas is `#F7F9FC`, surfaces are `#FFFFFF`, primary ink is `#111827`, secondary ink is `#64748B`, rules are `#E2E8F0`, and the brand/action color is deep navy `#172033`. Green and red remain reserved for admitted and rejected terminal state. Pending review and model recommendation remain neutral slate.

[//]: # (ob:9787677e)
## Overview

[//]: # (ob:e21f2b5d)
In one phrase: **a paper-and-ink ledger**. A paper-colored surface, ink-colored text, and one cyan-blue accent govern interaction. Semantic colors describe verification and review state; they are never decoration.

[//]: # (ob:6ba0b871)
Proofpress interfaces make one boundary legible: evidence and model recommendations can support a candidate conclusion, but only policy-compliant human admission makes it governed knowledge. Information density serves that decision. Show the conclusion before its machinery, the evidence bundle before raw sources, and pending work before completed work.

[//]: # (ob:ca5dbbae)
The design system is workflow-neutral. A legal product may organize work by organization, matter, and data room; a research product may organize it by project, run, and artifact. Those host structures are not Proofpress primitives. Proofpress owns the visual language for evidence, candidate conclusions, review receipts, admission state, trusted context, and lineage between them.

[//]: # (ob:ab42e61c)
**The Trust Boundary Rule.** A surface must never imply that retrieval, deterministic integrity, a model recommendation, or staging alone authorizes reliance. Governed context begins only after the configured admission gate succeeds.

[//]: # (ob:730432c3)
## Feeling

[//]: # (ob:beafea83)
Proofpress should feel like a bound volume with a cyan seal: paper you can sit with, a stamp you can trust, knowledge worth building on. It is archival, not ornamental; quiet, not empty. A reviewer should feel they are examining a record, not operating a dashboard.

[//]: # (ob:532d94f7)
The hosted owner workspace is a steward's desk over that ledger. Home and Ask Proofpress are how a human orients; they are not how knowledge becomes governed. Cyan is the seal and the interaction, never a substitute for admission.

[//]: # (ob:66d5152d)
Do not optimize for "looks like a 2026 AI product." Optimize for this: a future agent or human can tell, in one glance, what they may rely on, why, and under whose authority.

[//]: # (ob:6af4c951)
## Hosted owner chrome

[//]: # (ob:fa9a96d3)
The hosted owner IA is frozen as of 2026-09-01. Do not subtract these surfaces:

[//]: # (ob:4ffeef89)
- **Home** — orientation and Ask Proofpress entry; not a KPI dashboard
- **Review** — governance inbox
- **Ledger** — current authoritative knowledge
- **Activity** — consumption receipts
- **Admin** — principals, credentials, policy
- **Ask Proofpress** — persistent context-aware clerk

[//]: # (ob:0605066b)
Admit is the lifecycle verb. Approve is the owner-chrome label for that same decision; the control must keep `data-decision="admit"`. The assistant may explain, query, navigate, and draft a bounded clarification request. It must never admit, reject, or appear to.

[//]: # (ob:343a8d41)
A host may keep Home and Ask Proofpress. Those surfaces are chrome around the ledger, not a second authority.

[//]: # (ob:03c75a58)
## AI-tell denylist

[//]: # (ob:7097ec6f)
These patterns make Proofpress look like generic AI software and hide the trust boundary. They are defects, including when a host is exploring:

[//]: # (ob:b42cc176)
- Decorative gradients, glow, glassmorphism, or aurora backgrounds. Paper is flat.
- Inter, Geist, or other default AI-product sans as the narrative voice. Georgia carries knowledge prose; system sans operates controls.
- KPI tiles, sparkline dashboards, or metrics-that-look-important as Home.
- Sparkle, magic-wand, or ✦ as a mark of authority. A host may use a small mark on the Ask Proofpress toggle; it must never sit on Admit/Approve, a status chip, or a candidate conclusion.
- Green, red, or orange used for decoration, generic success, or visual variety.
- **Draft** as a Proofpress lifecycle term. A proposal is a **candidate**. Draft belongs to documents, not admission state.
- Copy that treats Ask Proofpress, a model recommendation, or a passing check as admission.
- Linear or ChatGPT chrome: infinite chat as the product, stacked elevated cards, gradient pills, or confidence percentages as authority.
- Image generation or video generation as product UI. Trust states must remain recognizable without generated atmosphere.

[//]: # (ob:a83b0b86)
## Design critic protocol

[//]: # (ob:007d1f14)
When an agent proposes visual work, run a critic against screenshots only. Do not put the stop criterion in the critic prompt.

[//]: # (ob:bea9a7b3)
**Taste bar.** Would this still look like Proofpress if the logo were covered? Paper, ink, one cyan seal, Georgia for knowledge, system sans for controls, monospace for proof. If it could be a generic AI workspace, it fails.

[//]: # (ob:b93e40e3)
**Trust bar.** Can a stranger point to the candidate, the evidence, the checks, the advisory recommendation, and the human decision — and see that only the last one admits? If Ask Proofpress, a green check, or a cyan glow could be mistaken for admission, it fails.

[//]: # (ob:40d605db)
**References.** Use the brand-film stills and the hosted owner surfaces as the visual references, not a moodboard of other products.

[//]: # (ob:5e18e46f)
**Output.** Numbered findings, each with a screenshot crop description, the rule it violates, and a concrete fix. Separate taste misses from trust-boundary misses. Do not congratulate. Do not invent a new IA.

[//]: # (ob:715fe0fc)
The human, not the critic, decides when to stop. A critic that is also asked "are we done?" will say yes.

[//]: # (ob:7056876e)
## Colors

[//]: # (ob:451376f2)
| Token | Light | Dark | Use |
|---|---|---|---|
| paper | #FAF9F5 | #15171C | Page and graph-canvas background |
| ink / ink-2 / ink-3 | #20222B / #5A5D6B / #8B8E9C | #E9E7E0 / #A6A9B4 / #787B87 | Primary / secondary / indexed metadata |
| line | #E3E1D9 | #2C2F38 | Rules, connectors, and inactive boundaries |
| card / wash | #FFFFFF / #F1EFE8 | #1D2027 / #22252D | Working surfaces / quiet inspector and hover wash |
| accent / accent-soft | #0E5E6F / #E3EEF0 | #5FB3C4 / #173741 | Proofpress, edit, selection, modified, interaction |
| add / add-bg | #2E7D4F / #E7F2EA | #6FBF8E / #1B3226 | Verified checks, admitted knowledge, active governed context |
| del / del-bg | #B4453A / #F7E9E7 | #C87E82 / #3A2320 | Rejected, invalid, blocked, removed |
| review / review-bg | #5A5D6B / #F1EFE8 | #A6A9B4 / #22252D | Candidate, needs review, advisory recommendation, and quiet attention |
| move / move-bg | #665A8A / #EFEDF5 | #AAA0D2 / #29263A | Moved content only; never review state or generic attention |

[//]: # (ob:a8d606fe)
The launch film remains a narrative reference, but the operating UI uses a quieter subset: white `#EAE8E0` carries primary content, cyan `#5FB3C4` carries Proofpress and interaction, neutral ink carries pending review and advisory recommendation, red `#C87E82` carries rejected or blocked, and green `#6FBF8E` is reserved for verified or admitted. Moved content may use muted violet. Yellow/orange is not an interactive control, status, recommendation, or attention color in the hosted owner workspace. Both themes must be proofread.

[//]: # (ob:b5b71caf)
**The State, Not Brand Rule.** Green and red communicate terminal ledger state. Pending review and advisory recommendation are neutral because neither has authority; moved content is muted violet. Do not use semantic colors for decorative emphasis, generic success, or visual variety. Cyan may identify Proofpress and interactive selection, but it cannot make a candidate appear admitted.

[//]: # (ob:eeee2405)
The fixed fallback mapping for GitHub PR comments is `🔵 mod`, `🟣 mov`, `🔴 del`, and `🟢 new`. Blue is the closest GitHub emoji equivalent to the cyan accent; purple deliberately replaces yellow for moved, so an ordinary move is not misread as a warning. `branding.color: blue` in GitHub Action metadata controls only the action icon background in Marketplace/Actions lists; it does not control PR comments.

[//]: # (ob:f49db722)
## Typography

[//]: # (ob:53b8c3a4)
- **Document headings:** Songti SC / Noto Serif SC with Georgia / Times New Roman fallbacks, 900 weight, up to 2rem. Serif establishes the artifact or proposition being examined; it is not applied to every interface heading.
- **Brand narrative and knowledge prose:** Georgia with Times New Roman and serif fallbacks, 15–18px / 1.65–1.8 for sustained reading. This is the default voice for taglines, manifestos, editorial passages, quotations, source-document prose, and brand-film language. Use regular weight and restrained tracking; the type should feel authored, mature, and archival rather than ornamental.
- **Controls and operating surfaces:** native system sans-serif stack, 12–15px / 1.5–1.7. Keep buttons, navigation, filters, tables, inspectors, and dense review mechanics sans-serif so actions remain fast to scan.
- **Versions, hashes, locators, lane labels, and receipts:** `ui-monospace`, SFMono-Regular, Menlo, monospace with `tabular-nums`; 10px labels may use restrained uppercase tracking.

[//]: # (ob:877970b3)
**The Document, Then Interface Rule.** Georgia gives brand narrative, source material, and important propositions an authored, archival gravity. Display serif establishes titles. Sans-serif operates the product. Monospace indexes the proof. Do not set controls in Georgia, turn metadata into body prose, or render long claims in monospace.

[//]: # (ob:46a56fa1)
## Layout

[//]: # (ob:8aa0ba5a)
- **Focused review:** single reading column with a maximum width of 760px and body lines no wider than 70 characters. Use the order navigation → metadata → conclusion → recommendation and checks → evidence → decision.
- **Review with a human gate:** a flexible reading column may pair with a fixed 320–344px decision or receipt panel. Keep the conclusion and its evidence visually dominant.
- **Local lineage:** a bounded canvas may pair with a 300–320px inspector. Read left to right as Bound Evidence → Candidate Conclusion → Governed Context. Use a subtle 21px dot grid only when it materially improves spatial orientation.
- **Responsive:** below approximately 820px, stack reading and decision surfaces. Replace decorative graph connectors with a vertical evidence → conclusion → context sequence; preserve state and keyboard order.
- **Rendered artifacts:** Markdown tables, lists, bold text, code, and citations must render as content. Exposed raw markup is a defect.

[//]: # (ob:0855c398)
**The Reading Order Rule.** Orientation → proposition → support → decision → receipt. Progressive disclosure may reveal more detail, but it must not reorder the trust argument.

[//]: # (ob:d364c4d7)
## Elevation & Depth

[//]: # (ob:6a736e61)
Proofpress is flat by default. Hairline rules, paper/card contrast, and quiet washes establish hierarchy. Reserve small shadows for sticky decision surfaces, selected-node emphasis, floating contextual assistance supplied by a host, and literal source-document paper. Do not give every evidence block or graph node its own floating card shadow.

[//]: # (ob:bf7362b0)
Node selection may use a two-ring cyan focus halo without changing node dimensions. Hover may translate an interactive lineage node by at most 2px and must be disabled under reduced-motion preferences.

[//]: # (ob:196e567f)
**The Ledger, Not Dashboard Rule.** Structure comes from indexing, rules, reading order, and receipts—not layers of elevated cards, telemetry tiles, or decorative gradients.

[//]: # (ob:8b46fd18)
## Shapes

[//]: # (ob:5eb7133d)
Records, tables, evidence rows, and source material remain rectilinear. Use 7–8px radii for controls and compact graph nodes, 10px for bounded recommendation surfaces, 12px for a decision panel or the outer lineage workspace, and full pills only for status chips or a host-supplied floating assistant.

[//]: # (ob:6bb05de6)
Connectors are two-pixel paths with no arrowheads unless direction would otherwise be ambiguous. Evidence-to-conclusion connectors are quiet solid rules. Candidate-to-context connectors encode the admission boundary: gray dashed while pending, red dashed while blocked or rejected, and solid green only after admission.

[//]: # (ob:54961ec9)
**The Visible Boundary Rule.** The connector, destination node, inspector copy, and available action must agree. Never draw a solid path into governed context while the conclusion is pending, blocked, rejected, expired, superseded, or awaiting revision.

[//]: # (ob:f43f7a30)
## Components

[//]: # (ob:0287d639)
- **Status chip:** compact monospace label. Admitted/current is green; needs review or revision is neutral ink on wash; blocked/rejected is red; agent or interactive scope is cyan. Pending and recommendation surfaces must not use yellow/orange. Never express authority through confidence percentages.
- **Diff tag:** compact inline marker. New is green, modified cyan, removed red, and moved violet.
- **Evidence bundle:** the reviewable support unit for a conclusion. Summarize its bound evidence blocks and source count; do not present the bundle as a raw file.
- **Evidence block row:** filename or artifact identity, verified locator, bounded quotation, integrity state, and a clear route to the immutable source. Use a bottom rule instead of an independent promotional card.
- **Candidate conclusion:** state, proposition, evidence count, recommendation, and material impact. Its review state must remain distinct from deterministic integrity and model evaluation.
- **Review panel:** presents recommendation, deterministic checks, evidence sufficiency, and explicit Approve / Request changes / Reject consequences. Keep the human decision available without obscuring the record.
- **Admission receipt:** replaces decision controls after approval and records reviewer, decision, ledger head or version, timestamp, and append-only history. A success message without projected ledger state is incomplete.
- **Governed-context projection:** contains only admitted and currently applicable knowledge. Blocked, pending, rejected, expired, superseded, and needs-revision conclusions may remain auditable but must not appear available to downstream consumers.
- **Source viewer:** preserves original identity, digest, locator, and citation highlight. Moving from evidence to source must preserve orientation and provide a clear return path.

[//]: # (ob:c8ecfb15)
### Local Lineage Workspace

[//]: # (ob:4495ce20)
A lineage view is an inspectable trust path, not a free-form network graph. Default to the selected conclusion's local provenance. Bound evidence nodes converge into the candidate conclusion; the final edge crosses the human-admission boundary into governed context.

[//]: # (ob:a9b6733b)
Clicking or keyboard-activating a node first updates a persistent inspector with node type, identifier, state, integrity or receipt information, and one explicit next action. Evidence opens the bound excerpt before the raw source. A candidate opens review or history. Governed context opens the exact downstream projection only when admitted; while pending it remains inspectable but visibly unavailable.

[//]: # (ob:f4762698)
**The Local Lineage Rule.** Render the smallest graph that answers “why can this conclusion be trusted?” Expand through selection, filtering, or a separate ledger projection—not by loading the entire knowledge graph into the default canvas.

[//]: # (ob:0bd4799e)
### Review State Machine

[//]: # (ob:7578205b)
The canonical review states are candidate / needs review → admitted, needs revision, rejected, or blocked. A revised conclusion is a new version with preserved lineage; it is not a silent edit of the reviewed proposition. Only an admitted, current conclusion may enter governed context.

[//]: # (ob:aae4f716)
Every mutation must produce immediate, consistent feedback: disable duplicate submission, show loading and error state, record the receipt, advance the visible ledger head or version, and project the result through the queue, conclusion, lineage, history, and context views. Plain-language copy must state what happens next. For example: “The proposer will receive this request; the current conclusion remains excluded until a revision is reviewed.”

[//]: # (ob:bcd36484)
### Review and Diff Patterns

[//]: # (ob:03c0628e)
- **Change block:** use a three-pixel semantic edge and a light wash. Put word-level changes inside a collapsed disclosure so the document remains readable.
- **Comment card:** use a semantic edge, card surface, and quiet status copy such as “Awaiting response,” “Recorded · awaiting revision,” or “Resolved.”
- **Block hover:** reveal a wash surface and an explicit Comment affordance. Clickability must never depend on hover alone.
- **Decision bar:** when a focused single-column review needs persistent actions, use a sticky bottom bar with solid green Approve, an ink-on-paper Reject control, and a cyan-outline Request changes control. Never use yellow/orange for a decision. State must change immediately after submission to prevent repeated action without feedback.

[//]: # (ob:e693f5e3)
### Voice and Language

[//]: # (ob:300ee19f)
Use product-facing trust terms: Source, Evidence, Candidate Conclusion, Review, Admit, Request changes, Reject, Receipt, Ledger, Lineage, and Governed Context. Reserve storage or implementation terms such as event, ref, blob, projection algorithm, and lock for developer diagnostics. Host chrome may label Admit as **Approve**; the lifecycle event, API, and `data-decision` value remain `admit`.

[//]: # (ob:cab7f711)
English is the source language for UI strings, CLI output, and documentation surfaces. Interfaces may adapt through `Accept-Language`, with Chinese as the first locale. Stable Proofpress vocabulary—especially Evidence, Conclusion, Review, Admit, Receipt, Ledger, Lineage, and Governed Context—must retain one documented mapping across locales and host products.

[//]: # (ob:b01d87ba)
## Do's and Don'ts

[//]: # (ob:df1fade1)
### Do

[//]: # (ob:3ba94c8c)
- **Do** preserve progressive disclosure from conclusion to evidence bundle to bound excerpt to immutable source.
- **Do** keep deterministic integrity, model recommendation, policy outcome, and human admission visibly separate.
- **Do** make selected graph nodes keyboard-operable and expose the same receipt information without relying on color alone.
- **Do** project a recorded admission consistently across review, ledger, lineage, history, and governed context.
- **Do** let a host product apply its own brand shell while retaining Proofpress trust-state semantics.
- **Do** keep the hosted owner chrome as Home, Review, Ledger, Activity, Admin, and Ask Proofpress; do not subtract those surfaces.
- **Do** fail closed: unavailable data or invalid lineage must render as blocked or not ready, never as a plausible placeholder.

[//]: # (ob:70e00445)
### Don't

[//]: # (ob:755d7400)
- **Don't** treat evidence as synonymous with a raw source file.
- **Don't** use an unbounded force-directed graph as the default ledger view.
- **Don't** show pending, blocked, rejected, expired, superseded, or needs-revision knowledge as available to an agent or API.
- **Don't** make evaluation metrics, model confidence, or recommendation the visual equivalent of admission.
- **Don't** treat Ask Proofpress, a passing check, or a cyan glow as admission.
- **Don't** use Draft as a Proofpress lifecycle term for a candidate conclusion.
- **Don't** use Inter as narrative type, decorative gradients, or KPI tiles as the Home metaphor.
- **Don't** bake legal-specific matter, counsel, or data-room concepts into Proofpress core components.
- **Don't** expose mock counts, synthetic receipts, or hardcoded lineage without an explicit preview label.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2QwZDM3MjMwYTVmODdkNzA3YTMzOTc2NiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImJjZmJmMzdiIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV82YTkzODNkYjIzNTU2ZDg0N2VkNzg4NmIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzVhYzNmNWQ2NmJlY2FlYzBlM2Y4YjQ3YyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfetu5FiS3qsQasCzW85Mkcm7CsZApVL1FKanu1HVMwtjelA6JA8zuWKSuSRTKk1PA_3LD-AdYP-ssYAN-Als-L_3TfoJ_AiOiHPNlMQqpXoBA2ZjpjuVycu5xD2-iPPDCeuGqmT58KEqTs5OttsPhVv48dJ3WVgmcRG7MfP9NI6ik9lJ1hZ3H4pqxfsBru3XbBlGZ3GZ-Xm-zJPUzUrGYu6yIgq8lKcxZ2HM0zDLPK8seBxnRcq9JMsDNyg4j9KgDF0Gzy2qPm9veHd3cvYD_jF8GNgK3lCzAV81gw8Zr-GLP_CuKiuW1dzp-E3VV23jrOH6trtzsjvn265ty23H-x7u2bL8mq04Tmrv6679ew7T3XX4wPUwbPuz09NVNax32SJvN6f5mjebqlkNrFklvnu6d3fH_2FXwecPu553H_K26XkDazF0O_7j7GTNGS5ilpdZ6cfZifjmA7-hi2Bx-YeIpX7iF9nSD8OoSIKYF3GSRHjttu0GnNqHumo4jFztSP0hZLlfhkUUZTxnPHe5XyZZEOdiOnJ0H3K27Xc1THiJ48zbruhPzv74w4l8_Q8nsMtt1-Mn8TMvPmSw5H882TXXTXvbnPwJ5qDoAV5dtHl_-vry_dsvv15sipPZk2iFDUNXZbsBtuhDxvqqR4rhdfmB9bB0A6fn7YZ12-GArqsGH9nf9QPfwC8N2-DOqYHN4NYed_vkrNnVNQwzX8P2cDHBrG7za7ia8TBxoxjfDjsz8I84CUMTzmveV6vGeU8vcX7-6a-OoCdeOL-F18BtchisKGh8WyQyfgvffOF8_nNqXqy48xX-u4OHDHdbnApSAlDVyY8zM-AgjMLUj_i_wYBfvHg_sGHXO3-zdJfR3E3nrve3Zy9eOBe7rgN6cPKu7ft5BW_tYEu5s9pVBWvgQ9maQW9Zx_ZGnMZJHMXx_oi_Adal144t4BeOddnImvClVy6zsHjyG942TttwZ7vuWM_PnBcvmLNlW97NWVPAPK8d2pfuxYuFcy5_ydu67WAx-5EZRxlzsyT2njweax_1KvfOhl1zGmfW7pqCgdyq-aoCrj9z4MaC4w6wZmQ8OQuLLGNP34Hv1twpBEEJNnOq3rltu-uybm_nDd8NHatxbWBArHZAsBS7fIAB3zljFMGyYMkjL3_yeF68wBF91-36wXmlFuMdCLAFUOm50-8EXW7w9wZkWOdUm2195wxrNoyMJ_bdwF_m_t543nBeI6GNE6i5aoQ-M85KzpInP98ih37d7urCKeEmp66AHpigBuemrXcb7tyCMoLv8jsGW8VZfTYy3dBfFqBH46cOB9d-3QIZFA4IWFhcpIR-iysOZMEc-OWWdcWveqSZawe1M608ctEYt0RF6IXL4qnDed06TTs47XaoNtWfUQh1zvcnddte92qJUI45528VYS6-P3G-kZePDYiVQZ6G--z7G3vi-bprN_wTpPHwHSNkUrKUpVHhP-e99_bo7TluTtm1f-aNw3qnLR0j3ReOXMR-lw3dyJIEJVBemaTPGdoc5Otv4BpgVVRLbVeBTmGo7EF6Fc45kIxF8PBbd_eSBsec33771gyuBuNtb3Bu5IZuRPbQ0YM7LzbVgCs1wALWVcnzuxwsRiDhDOTbFgjohquf6Zlz8UwHzMyRdfMDnyVF8CxSOqcNJaF6zfnWwTV8YMUWzndwHVdCEBiy487I0Fw_j0MWJntDO387H3hdAwM3d7TO4yT-wOUj9B27YN7nUXn0G4G4YYJbMBN510i9aJEMsr7g_BWHpa1yZP2-LQeQSmP8Dtooz70DG_Ap45qD1QXGMdAyEMmqg5kD9fYzZwVaEv8N5uum7bbgdWxmQPcO23VwtZOBt7EaoWvQGBnYEfvjkvZd3lUDTBDocmjBJPnEPj1608huuW5ceKUXPPPtf7dGuQP_W6EFCXdsgUh7BxyxHVgMqEFmTrdrUHeJh7IVqxqg9z4fE0igUlMWZ_4zRwcGBQNmhK3o0IT4O1KyA2wUKLMKdt-QlG2alSQGxkaX-jwAl-v5oyNTR47uApcRBtahG9M52xZsRGdoaTA5CAQwxgc-oz_5zZgwdwuQmEX27NG94yXv0PzscXi_B97Ed2cdWs9lVW_EIvYkrIY9xTRmnYC7z4MDKXHM6L7ZDdvdgCP7erfJOBrtJVwNdA6syVm-VkYTUBrnDVhY5OFsnTFjJfbCkrtl_szRkZrebVgzIw1HO0h3z0Dg5GDTg5mNjAO72w_tFk1s-fRhPTY6N4zA2do39C_QY-k_ISH0RaOup-fHUbl84tP_4nzXXsNc_uJ8Va3WA_z3Neuu4T9IMH_5vvnLfD7f-z98JZwtuOYLMyQKdBwISCDkqHzqdHHxa7ZrgAKISju-QZEDlNCwTkrxTpH2zMl2YoNaGBEbY_owi72clU8cjfBp0POGd30NxPAK-Ud7NV8ibRIHIQHn7Waza6ocLnYGPiYgOfyzDNzwiLUpq4_IK6yuUUOBmt1ugRTIvv6yGn6zy5xv39FIUMuhUXT1f_7lr__T2bTF1ciAyiAtsni5Tz3f3W1bUJjb9d0n6HPvwhEaDf0syX0WHPEWtE9ft_kOp-XIZ_cY_njfNquhct5fOKe4Qa3zHiMq-DcJkC95241o8SSO09g90FSfNyJBGmpMMzDwgBTe6vCLJhEYwKpizgoItxfi1xmTsEHEwqhk-0bpV-yu3X3K3tMXjexAwpibsZA98em4-m9gpj0vHPElLn0PT6fALb0HiA6c3UbJ7Q37WG12G-d2zDdIwjD30-SJoxEr_06-9puuAGGklvsby3H5-T_9Z2nTVPrvfrfdjqx-4UdBHhT73vdlzW_EE_8dGGtbEvJjG_HQ9SN7ErHYj3jkHf9O2_wBd7IGrz67A11Vsl09LJzfsKrDEDSYcjUH9Uri-zRnHYqsMZlZwsCWmXv8wL5uC_B5eM1zugO9JKAhoI7htp13RDQYEymRtJw1q1uiHth-8LxGBualEQ-juDx-YIKEREhXCPbXrF9nLa6JIqX3Q7fLhx04aiBOObnpGwcf-PjAkgxso8LbJ-j3a1jvT6l4fdGY-OSgw3y_eOLT34nUAdieqKPRvFJxya69hT9RIvXtrsPYHKiurgLTX2hdpxuNo2Zgp_LoiaO5aJuGU96CfGAkhC2otBo9x3UvpEfTwm8wOFyE3tk1NVJ2UY2NJgzSyON5-sTRCDr4Q9VjxPZ-1BJ_zNWA0foDm7kRRNa0o-rUL2Pmuwf6fbNtG1TLnzT3rAvHnMBlEheRnx7xFhToMp-Qr6stSnMg8i3D-HDbtCJuSEk6sG4x-gKuwWkuMg0jAj1PeF5m3r5d81WbA0V9JXJg4MXJsOT4IoA6e_S2MSs4SMOcL93nDuDckTk7B7-gCGoDvN9vgRIoWzmQ74c0O5NhsBJswTmYYZux2HqaRbHvZ88d3kVd5dcoPsHqu-Z3JLfmsHkVSkD4GoxllLxl1cEgd1t0PdGCBrHfV6NkG0fL6FAfP314Urru3ahY6h1vCgo9g2LYgBULLOWQsSWi0WM2vJsVQZym-x7FO3qpMNGd34HjCO_7FGk9cs9YdCyMk6UbZs969XciFNCii1BLOwo8SLE5nRUmAFO24RxEn7wGDZexhWGMB2XsRc8a3SXm653NThpPlKYRoXnuVOBOFBU5QZgiB7ZHM7yEMaITcjYabcnRpkqCh8aGmud1VZbOtzJq-Jkb99B9Y3LSz91omfBnDwGl5gXlqR16NopNac-skfuFIutBdzYYDaC0Mb6AgTQZkZo8Sv0yPAhI_aGtcnH3V_DCHQIfPrE4D94xsiy-63LupeUzXotBApm-mYPXg6JHCEZYyk1_Bs4ZmhUz51JaHDMMk0kaH02JZjHQs_eMkV2Ca1L1a5UVkPZNLe8kd_n3bzFcJyJOF1-9dVoKSc1GOS1zvSKJs33_6XX7KxFGe902v_qkdr9_9cgeFaVXsoJ7B-_7FCm8bj-x9RlLgzzJn_BY4YADwaOfwbsb2vgV-hwYkUHAT932aCyTmQxPzesdwXnAJR-h_djlrhsE4cFIYGU-PUdx0ajUDos4cN2nPVzMFC6CyQ7g3A5WIr93-jsQ4HebdtcrT7djt4q-ysOZ_mmm0DonN6h82-ZDjo-kV9IvCnrDP4RJnHK3WPoeC8swy_PQ5SFLcfRgYRA5SkCRNk7yNc-vKdRM-CiyzghQo_5CPM2fEIkEBsOd9QQbnWQ9hHBPRwKXMJfzoaww-r3tKomP6jPvLImZFyascIPCh3tgfgULAzCEPDfN8yyLE5Z7LMoSN2ZZypZpAHekEUKpPLgexSIqScI5id06i4IfYaERgaTTpcvvlu5ZEJ-F7r933TPac7niKFD8pAiLMATqMN_-8ItBo4jeBHRpDW4kyok4hYVKSp6QeU7PsNBMkhR_WRCSfLWXcOaXaRoBg6tXW7gk-ernwIk6e9ggOWdgXnTXRXsLDiPPebXF9Joyb2TCc7ZnUGP6DREIDS_mkjMdieODrZE-6XCYLT__7e_ey5TsAodAcBa8oqfIAoZ2CE7Cqw7vkMG2fo2ZQvyksDHODVim2a4GT08EkK3pCPWljDK4SfO-Uuu9MI2UhwzO9aqp_kxsidcb-2jxgB6RexQGwAVBGDA31-RhIbEUeXwKYiWfxoJs6YGRxQtKzNDTLNSVfNpz4FRiE2fgAV3rL_GxYqPwsRjHmWf1DhYhz5F-xP4KpBSjbV0475VlRM8gJEreVRll8oHSc4M3sI3jl7ild2QhC9hQIfO58MjHlziNlstlBP4xpzA7LYoF_bqPzXsypqvAoDqviQQw3F7QkHo044kWQYhi4lQbPEYnCqprG6BWIZnn6HzXFcPYNiaeHAY-N-EjaSwwuEEzjHOtpMHCedugwymWDYbVVwOwASrnXnhTmK7qxdKvge6HtT0KJ-NwNxj3xD_kHyBDiAylnGUG8wfCllcaTSdZdMspZUecpS6iqXDkWvx2ZIeWoDg8zvPM54HaIQsMp4Lxz0C5dSvWIPhIDE9_Qes1w2DXgNE_nAhsECjytt28RIUOBg7r8vXDD6souCqlFaXHxSOUwlBQD8KF9CqGKDw8jBRYJAd6clNhRqtf2F-D7BJWq8zD71mtXJvSD1GWEbxGEhta6kUei2Qc5asaw8RKPGd8uMWkFrx_M7J5YAP7IfOL2M8zreAMclBrmeMhgTADsM75Dasx8IYORdWAYAXpgZy66oDWZ5hneIAHCccBk11RLKRGThbIZNg_dKqR03Jgny8VSykdlAGbw9oTZ7JykHEK-LWsVjsUemYtV7jw_Q6EHTjqIwtV5DmIZ4YGN1cLZUEajagfBSvKh0VuGkblMgk416tu4RfvC7UnIxNlbveu3Qk5BtSO18wI28A2W_0LEdHMCCNkMnhWtqtqEgkodN4SaAtZqaJtJERgh1DwZmD1S-cfdhUfxNd8sx3ukI0F-cIQ7KFrBcA_MiQDCnEJzLt8KqZ_ZeirUJH8kV3hSRbnLI1ZHPlqIS3kpSV7jsVUgipdPIYGo6mgQGZS3Au4XW9runagK8z6ZlykIZQeWDgXuGvKwYXN01aTpXRnkq8YogiBe4bdIOSIpuSRVWLA4T5P4iChpIPQoQYQqh2q50A96XIE9ZxhDHVH-RYBR4LvxeoQuYERh_YHqeVVzUgC3uJa05KhhAa-BjHd4Nd3QqbtKNR4S-JYCgAgssfnm2ce9yM_LsKlsRkM3tTw6mejR-WDg8wrCnB_yjCP1YMtQOlj5PYEeChG7gdC4CmL-2zE_IzKPPX8wPN9pl0EAyKVw3keJNSw4fcNPknE2-SzBA2TO1E1WftRXPKVNEDpEpls0PsmkB-aHcQd5xjyhj1V94AC3IEgwSEq_ScvBGpv5FXonebVltWgG8EZB206VPSHsMXkDXuzU3ei6yhin1JjzNktRW5r3l0_EOVQlk7q8bIsw9hPtaVj4WIVqPEZKFeQkYKPgCF6kK_a8nupNNjQtbVQtIRTvUKLZ66u-g_fn6A8GL4_uVpQ0ov1OFG0R5Gz-MdtDc7ODAQ2mYgNu6lWZEqQ7dSBqlSKBZUpOFbGmscCK94PpAwsPU-vQ2NFWFEokLZbsLqcoR21OtLUY8sMCFzzkYXiVQv5DEyuXFLWkZaknZBJYkHZPUhhNPY-Q5qE3C8yl-VpybRbZuF6jTT5PKCuoqWlV0Q-T1MgKm1PGOyuESVHg3FpqdZgZdL0hUOsHCGiDqGhCg4UivZlhcancAMITipWHwgVyabFAOuIKPI9xsFVQ9yeNo8syK8WRcdjeGkn0cAmw0biIxbI5QTWmTlf8qoXJNjChDuFm8BtUQ5AzxCBJljPwNBuMCK90AifHH6ogIyMyobbe3Bfpd9CDxGGClwlWbKnkaC8HCpKzoN50V0TWkML0J4Gt0FzOO_nyONz3MA52MoYqEMh2ROR07Pe0wM4-jerKp_fwm7S_T__83_H6xCZA94QqBJDw47FMSKfQak5eSX5AofifmhXqxrmVu1xNZqLcD1JslMpsqTpqFLNYn8edF5o-ASpQ8EgRt0SntYh5BFKOOP7zzTtkhXei1WSLtMNiCAOMxPC_DVKKJDhNH2bDbSQRfeC4h4EF4IHkH334oUeJoZF6DFgh4FDscIVcAoJ_uqldNh3tOjlF-1WujMUSu4P1nHUg8EATd8TSgZDtDR8bbXhwym3imvkXMAbvvz2Oym-zoAnSzCTcXUpqSooV1LzDIeXX8OCcoLMoMgWVKY4y9kiMpjGQL6PiAUA5WJkB4wz4gVDPsRLG3QeaUeE3Ke9KHhrf8d67VL__u1C-oUy1vZoUE0hguRz0AkbNm2_BVbli8d1bhHnHksLF7wlHQa1MPtG-j4Ffq-8hyJ0QZWHLHC192Ah8uWznwOul5Bn4YpqS28rwa6IOqabgPxbjLFZGGV8EZhAI3rJjfOI8cxfBjy3nEiF2Deu-9Hg-7pdtQ74cMjcN4jt_rWQvhRAnOl4ITktMy0_kb217JztSc1SUCIJzJmFUMHvqWAazIsSZVFOw8xQhFmaTbttM7ymZFU95rF72TL2l26SpaVZH1MzYNbnaPi_iuDQj8javfjMCiAOLH0_FAY6HE7-kLLayCalEDfnQsZQ4IJ2APaO1pnsrP7XuDz3Jc-K4Ms0AiWWcVtQq5qV3KAhiBDxPa_xs1ayBHOtKMGBzALtT1n1DXoljy9VQJ2jzbe9oJnGiCvhDGTTFgLhB8pPqHopjcbmEKTukrE0S8AJ1JECUwWh53B8QQMFwbdio3ECiNLE1b2pWuqXIMOLpCg7PhAEHGPpOFJEmhOb4rYojCKZbHMduxY_aSECjwE5P-zw2frLqrkhZwv0-C24nWORk5wFfha7bhDr9bDqLmxX9sgSCiaiRnXfwpaimgLnBETJLVhEQNG__v4EVhIEUA_Gyh0f27qlF7iRn5W8JAyrNJV1EYZRAWP1FcrzYHGSBYnLk8AzWTVdciGf9bxqijfnb9I3IX7yQi_2LuDTt0xCSAgiNQdJcgNkbuxaeihKVeeUkjNL-V8fn7J0l8vlK_jmi_A8fB3Rp-RVcpnik7-4TC_jSxe_O4_O01cBfoqT-FUS43u7aoO0cyodHvEZ6Jlj9QGYoowi5vR2Mlbxgf6l9zqlF18s3_gJfHonAMcaQilpuWoIq6bzK2g106MIk3zq3MKa04LQPziwN97lm8uEluY1TCvG72By4fI1fIeYNLSStCQ4FZFFBdhDuYUuDcXnxLPxZTJRdSo_zNH_wTe4l-FlRG-FGV2-cfG78M0r_4KWyIv9OPBoiYwo5QU6sxrojCqqoNTtzI7FydcWOEX49zxb0WJdxq8D8br4zfLyHL-L3rx6k1zS6175y2UE3-lksFIYTMIybZ0pl3V1GNemF6OVeYr_li9-FQShf06rGyMx4HcXSXyZIBF94Z8vQQniHpKLLqZyw-oKPlC-G78Bew1eJalQJh5O5Qf5FkN6Zg8Nwek9vDA60oa-zcZ1othm9HIbs8A4JHg2_keOIYrC84RmCiN4LVjs_PzcfU0zXabLyMdl_x3NhdasEbr0pfRr7HQkKkplW1hvfqgUSqkQP3SXWZiCUxsaU1RXR1ki89jCJ4p8__4tukl4Ay0Lqcas58MZiFp0Ba6-uDy_TC7dK-2pbiWXyynPhPq_ktRurrMj18S-e-FlysCRDNLPlWnBzmDsHt1GVJRXku7MGztJdLjYmtqEHEST5UpyyBVqColHEv7hjWITaawghywOdla5uZsdvgHVLB8Wzn_kNdg9p9LhhOeS1WBlsG90HG0mHdrZg16bpgnKcivr_OE8wsJ5BZYIJduUD5RxYdJiWc2YXRIGJVxR5AEzVqopcttLwB1Xv7YBMV3L8Jf0aJ1vP3tnZb5eEAeihXDFG16R3bW2_ceXzmZve6r-YGekjYIP6A8QBHZIAPaHb7ZrbE30WbEBkT9BYqgoBlzePUroN9wW7sh66GuwBodFsTU7oCEDmZr6RiKESR6UQZlEvvEjrdJASzA8o-pvhp__5b_hIovPf_0fqASuBD_hb_8Vrb4rIEWEb8gAM6L5EJotnw5y_u8rB3tlgQrglmuDSyj050twT7ttjYHBusrIVa-RKLY16eQ7Yi8aMW038FDrUOoLCIrMVBnepjWteiR_EbC5ZR1m_BbOFXkE-JF2_8xBvMkVMpgc5bksM1LmiXIZjV8kFXGVI_zBWFHwCIQw8YEGeyqeg_GhHpNysNdFy3tlPVMk3VrusXj1sgy9Iinc2NU4H6vU0lign6qgVASDOUswaoPMJKisokorcXNsrSQ64qfOdxWKo6-Bw9-16HEqwgM-Sl0XTHG0bmfObot0sARNtZCPApIB7Vf1ay7ISIEiHOGo61K8jCP5imwuL2iJlcTdbmuU3_BgToh0A0GTU5FBPSHJjG7Evw5Cr2dW_SXN8HBewnnGgVsz9MKff_pHL9l-hIXwFhH9tUiIcnsQ0AxHrIoeMR5e9YppVOSYAsMiIcNWaB5j0II1VQnL00pzsaU6KwzwYUANUyutSK5hDJgwNnMVXhSTEfxqOcUKFrIg76LjK0S0yb2RMh3jETRcTBCijSzSQUhge_l1IYuRKTcMM7AK0SIS9w6s8Fqkthsrfy_34UIxGUHBtDWi05CwB43YISuiMxerToFIWPElrnEoV1wseLxwfovJGxC2Ay2KTDqRBIb5A1FYJW3a0pceBoKhuNJSG47N5RC5Z7-6lcKgV1HHEmMm6JCCKJdz-4PAisJDkQEJxdiCeqTXwPLL1Jt8p8o44oyvdtVch6lA1L5_8zv4a_5ObNLM-R1v6taOZBF5Xg0Cljhvdpv-6qXjubAk4hXaaLE2dbfFkCzDcInc3rF4aOLlBZihaZjqnK9V_bxnLxxX1Kw4cXZYTSidPp2tsAQB1VUZ6tMUB7LwhjITr6seZPKd5NI98VINNYY13ps91ckVK9qNxp9aZOG_6p8xbKhy6Hww2gIVipggENiusxQKyKLWwaaZiiVb9A0IZYBJAUx9Vht6gN7ZsUBsGvkZCG8eBDo-YZV_G-0wVtmtNE2RcD8pyswNzPaaYm9LMxxbx10V8HdbOnGEVEmyCBeCxBtWbMIFSkbELuYd0HIC_lnogF5LldqGj6muSa8t_mGBE_HPQ4uyUd4v_apBiviHRjraaAM1BxE2xYw1Tpc5Zc0_Vtn9KSOPbVnVqfuE1QVuMEgkPwhg2jr0ShtP_A53NFgmSdLqAGFJdA8GmR6qMEHBGClaNK-bQY5X1MpJDJ4YpE6ni5jP4dh8l0a1xM3Q0m9BVfFgs5ckyTqhCnqBvdNVOLRgphDnYn_RNSjuQgQPxP4RfggYzll6uAwtFu1VhTCsKJKHiUDJ7_AVMDvm_npMZyK6wkaP6C3qt4iVvqH5YlbtFpV_1wK9CdsxwcnJbJXeKiHd5S4oJYPzJtPNdgZEVaGJPamVg-kNVIG3R0AHpKciJz3CF-Cal6buRUQByNyQpZeCsvW8UB5wAwglhaAR8kpjkW0JvkRbKyh13hZS8eaVNAVUVowkDOuVi7RwLj9iMqkgRC5macESo4ylSMqPqIE8jsOEuUUZxwaKYtow7KmB4zssIPTZ5krFzcgvBHV9qHBIYLhuEMi2aQlgALZWrd0tkWZucTmEIDHoBNatSF-NyNooSMsMA_lJouO3VrMHI2s_s3mDDu14fuqGbpi7nkGM6X4OD6DMn9qfAXQS6wc73HVLpojRhc66ArUHmvMO2UDSKOXv-zUDmhNeMiJnr-_us44KW_JiTjXDxoUu61aYcpIX0HdWuCCsh9hJSx2mIjAfCkiMTnN934jFWWmFuyJ3nQx8AzbHQA-F14hzaTgoPZFtzGBwWcTERrY7CxjnRRS6bqazv1Y7C7kvz2lPAcY3XkCDLMCtaMhQRMgnBgzxUZgL7GshK_ZCCQpqTffi6mHRPZDxUupVFQYC3kBhoXCMIFN2OWzTpqXRbk2GaywFF5YFmHgx_F8TqNU-Y4_fj2uHAaq0Wc0U7SoxTSy6bxf__NNfcefBmgOrAC2JQ_gBCH2OKJc7hYXZD-5o3M8YgtPjcRkyloehRqxaTTkMm4_121CZLs9bhtEy9fIoNZk_3YJD1xEf310D6Y6IoRNKNgaNjn4nTrTaS3rL0iLRocGwB3qraADgpcpeODCaDJ97S3klM1KAbBenFcIUCBsNWUmdVtIcX17uQKAQLkQofSFTNKynF_ljFANzLRk002o44VhAkwdxFLuly73YFOzoHiO6vcXx7UMkm9-S30sJ4Nuq54QW2GTVatfugH-VkTQf2rllE-T77xWSuG9rsIGI8hfGoJJ3kvlg3QYPbSWmzgCFVJL2DDf1jiBfWDizBvpXUXQRIt_7RUbEhRGqsjOC0HBAIkZuFTF8Dtbb81icJR6mdvXyW01V9gTFcf1SCm756XDZVqK02Q2oeVE_l5vWAwxnsXC-FhVfaOcwOT3caeGJ3ctzieU5MMKr3iyllblS68Y_bityPoFsQTDxQiLP2C2rBhXr_sTiBWnCEx6mQbE0-G7TA8bONI-3dlHeHMjnJPPCKEq06LG6vVje3LFNXHBViE5e7reaaDtzEANG5KzsDrIODO-lWsRTnaShJEzx0uD29wLnsNMU2EVdajIIUjM8JKqMqYfa-M7OyyiCgE0TUXqVRMAODO1utX4EsKaAgNjpAb6wl6pqyPZCKxrtk69Fu5eVgCGqPC4N3uQ7O8Vw4k-ZqBDvuNyvncNXEaqD1pfIXFnIuwYxNAJ3Y0CQzvvdBgYjSs16Wa6zbyP1tlbJ4YLhJbhkAiKGXkojUoOyeI-C6MhAJTDHvUGSzQXCEseJF2B0j8hfRW5FcgSLrXRuTQbBZlrn6ODlzBRnqWozCV6pMSfSoYpRuYNqg81GaEFoJsrRzNphANNCwGCafkCPFuGqDVkbyMoyJioMIaBOtB9UNPIBXCnFOMRgLGfF0tS0hLMHM8xaZ1dELQhj7_fTwTZwEY86qRpYNDKOHqlas0pHsbptt-8U05NJLZ-pZgsNvXJ_bPvPVpgAU6y8K8sqB2spl0IWsdjwxaALCU7BVyBkviNP3qBvkKGpjEK6vb0V1zgAnxmxrYziNutBulATECJ4NIwWpv5CaDxpDeLkdG5IP9OYO0Jv0VhlYZM8AUUXiM30bTOVpFwTqVASWHw_YLwfy9YkGW6ReuakGeUpMwsqQ6QcoQPX9mT5yPnIGk8keCsJitIB9lhWucr5ffl4NbuQNc3ATGWhQm6QUSfkMX6NVlNOK2qV-L5SGssyB0ZVF8ViUaTPtSC36kOll03UynZFJRgQXWwtdFX-Uu8vIZ1vgRPBuN_IIhsM7Impix4vjtiUM6tBCJqE1YqSyEaGiMOGZkaE2PEO2JTVusagFaXsKcOJjKTJGqPz0pYW7Ymku3tYm4RkgwUMWu5wiuOi5TASG8mwziviPlbT64Jk09FMa_En9iZTOj3wkywNgqwoDYLMtCvTtSvHNx6DbR-o1JkcBHC1ZTpKylvl51vk8KueNoLKpm94I6piX-1rHPIz8B6g8BUXhtceqtV6nkgvlbTnlIajLhIy4k7yY37f9n3YlhuxtpIwTPmyiFMv0k6e1VlNeQrP6JEmaryMsSrdikKkzmYKMFChFJKaxYh3KzRcmfp80ypBi-IGBYXqjaA1MlhLsvxbqv6POe-2gyqvJ9Gq6_AJOKk3QtxqLDkt4-4VOpuX8I-o5C3-NpLLiu4qkfVy3zfBuJzCKdlEivLkhpyEO7BytCQZw2oWuZ-kpc9Z4hoLWrej249THNVYrulvMe7w80__fLu-EzWlmLrd64egSuN__fNP_wVjrAJwLAxLCwAi0o8kjMl66xUWV-oJs4Qy5pHdAZ-JwAitORBPZ0l5OU7NWiqPLEL_Y2EuP2TLMPRDzzfRXNMlz5JYn9_yTvmDPvc8f5nGaRBp8KzpgmdhU45vaSeJyob89RIUplScwX-p4vB-T4KJsDeilqXSF7y61aAwKU73IAZOXxGIBfPwaFoa-5wXtom4cL4hfd1YQ1X-kzUEKpFEj-cpQizwgpxjpx4Wm_oU08dPNbV9RlM-GT50ih3ZFdSuINPw_R6ryxVRkoXYdTKkw2fS2FJ2HMoyQmJS4FeC7CkC8JjhJZUwmZPiIT1pIslL-BUYmDsxdN0VRe7VTAmumeqoQzKLGgeBA4mlqHPdEwPjCGJdhHVGNeFrsvR6krAL5w22zfjI0GA7Q_7_TqR_MYPSCSw5zfGGC4kgK1Zl5ez97VYCDwRzvSsoPDtUNTUkMI6zIqcFSJKRoEtY5Cwq8NhAXSJqNUy8z7-f2flQ09gyTIN4GXtlalWgqmaIVhjh2K6GmF_EoABsC4h8MD6KeQ0Oeq2dClgoaYi1dc22yLxWyqeX8k7lCNTSYhSZFIaCmBDSivw8M7q9Ec1kYkB1KjLpEhWkRDoBS3-N_jAQwbkJ71Aeks9Q5sMP7-RRis7__l_3Y0B0ERZT4nV9W9-IHZaIJPKlCWYu3BvKZTEBOVe9TmjlGmMEqLmxEtR7ISwwMl1YVtVoTljllcL7xUCMwLJTaxMV2lA-VMbo7bIWt5TZfpHjn8tEtxTCQuxaFg9T_bfkCouckXTIMyYNITvKaIo8Gyo8aJu5qGcwvqRAzMowALaJAt-KQi6HDqi8VsV47gV_DoLXC6nNaIHEM4xM1LFPI_PQDsYuf4LQtlzUEsqYsHT5lPQc8RISN8hAamcZj7WlYnXwtHj2cxtyKhMoCQvuszKPTImJ1aNTPvg5LTcvLFn7TuLrz0Uh_sFezOT-4X-l-FfZoa-UkMaJ3QcL6AwkCHCUz63o6cM32kGjgWpWpP1AhVNSdDab2QYoq1cY3VtvZGoR-UtAfkHGINoHhAlbNS0SKuXeaAZUwY9KWTRGEH0V4FUvXkhqffHi5UGTBTmK82_fSljsXnuEKwfjNFz5zVdkDVyNFUmBq8fBjfSKhJnWVrqpqVLuz-hRiigIKTX3g6cLA9cSzj5I0q3RvFfnec63w1xR5NVM8PQFGoQ9V0V0wisi35ATn6Gyt9LYpoMeWLgcDX-B-7CobozWnkJS8AIZYsMQCnlQauZYiiSR0Iw8TTniXtb7aGNpNGfohdyNPFgwZqBTVp9Xq1L4czq3atXrLfM4ScrE15rdauZqSYnHerWqjGYUJaXnBqVbaGfXat-6B_k9rjvrYbM3grjZnid8cS9WK5UOvpJ6bDzaoevh6nbRagXJGZPJYuMPO98pB1J5V_Y7CXSvAxpWQtS4-gQGVF0ZOeFlBJthgPsBB13rAOwjJDpYyQqOPTUrFllYtqoH1V5jMGOLow4SZKmKmVQvkYcN3Xveg_XKGuuc9kia4oV3GiBhN7sUPrpgGJzJYX_LuTCVdUfLe7t5r2BFtUURfSYMRysOVo14BI9LB2C_4FinKKx-RXb7FXsQWFgsShCKMzuAIPr0UYKJStF0sOwAJ2UlSAViiBV3uhMWRXlqthMeDIWg122NAK4R2FTmsSh2Y99PjTdsWhfvsfOjbYkVJINnbuy5Zc5YYjxr3al4j6OP60Js8jzqCWTPNbCUKmMDZI_gHEqKaw5i-zB26dzhTh88jpzHY5KqB4FpEwHBXbEDzrpvAtwEWvng_cT-JnmieqMoaWNygBKhu5dmtIrErYIWzDDtNdc4XP775fN73TnuFdDf69axvxuimch4RxKVHHysV8r-E0nv4xNNTYSIVhYP9s6BR-u2M2rnqVMSInK367Y7eEWGa05NNuek70uQ86qFJibQQBoLxA5aTthKk0YLtkYvAlvWLHPVJ1Skwg9eJGX1Bo09yswhRu2ugfGhajF9LTHACYIeURVGECghbrtYsrW3TIXfa9H9I_Km7NL9wwkjtAZ-wugQLz5kdydnfzwhYjzDd308wYbaIgajfiWyO7uuNtX82sfflV54-G4ZYdA_k-Y7AwrG-Zz86cfZL9aZGvanq7Id0v2HDGF9KJIYKJm-_4B714tO5CKNjpOWXdFpRNh4HJQl_LlrkFPxi573ons2dhmHgUp_gXpf65OB4oR7Wbzfdv3zO12P9Wb_4-npn86cL5y_abMzoaDmGqc0v1n-7dhJ936ETcjdh0771Rkc5w9LgxT6vCOkH713pDE9L_MkcXn-y4zlO9UQzupPKSuBJchhpkI5QDtWjU45emRiDs5wVEbpLzdIuBZGWBNg5MUL-E2GLEw9FNhjCHeVSMMXL85gBnYznvtnwkTgUpV58MsMEp1rxJbmjdWbl4Q0ZYjJYED7jgYoQr-qxGXsTL-s8IsgOzg14lkrif1GsQmQxoCSliZUCaytF_rRv_6T5y4D0c1P1XkPo8dh574HMuTgKIbn7vcWtCvIGYmc6WVjcVUMSt1K1lylvkXV9PreOV8gMkVlzWNi5mAU8riEc_xT6rWRWSweExMPP_U1L0VJnbUNstpO1jM8ymwbvnhMDHz6XZ9mF6u1VF0sHuPl8TdJ6v8Mkt-rCmTC8RwWjzHnw299LwwJDApbK7lpM-G_HNK2xD1pwHbG1-ymAkvlMW771FsHQaQK5aaIldJ-qgBe-Eqi3nzxGMM8_CIdSrb8KSOiZVdzAfHPrR6LguAVC_5wcru-o4eJCpfHmwmo_Zd1ltIxEHSjiFIGgN9xfKPwGGnD7xVuqkSviCcceJEGdmd8SDxb47PPOolY6id-kS39MIww_cGLOEmoG6pYO_sQE_sAD_tgkx8m62OyPibrY7I-_s2tj88_qenwpKL4x4fPIfrUoUy_yMlLZZB4kRfHbhDHKXOLJIMxpdwDAeCBvOVxwWO_LLM0yJYlA5mQpV5RLOMUgTdlFD4yn3sHL3lnbny2XD5w8FKWl1npx9l08NJ08NL_EwcvZRHwKncjf6m7JlkGg9yjI_S8Kun3yyIPeMSYqT-zVP-9EwSeor5V-Dj3yjjwg2XpazKzNLoFzDpWK2MDYeYsl1jwblXrd1SNa1XPK8FOmNM95AVz_CT4-ad_DLwInmHVj1qV6ueD1iPUW6DfB6l27a0unzdATLn5Cn40tCuOTshLTNYI1F-nGmzKkzDUner4DIZ0yQfZuEWVp2sjXOZiM6C8NbW_Rq47OucxBt3jWZxFsGuu2UbL5rG28Vi7RbZ9M4JgUxUNIXaoC-9aVR1jF6U5lZ91ql2jqIwRfsScOvCa7rumZ46uAxw0oEqUgRtMu6hcFX1-RJ0DngOQtVieJ1a6q1bY5rtEnAzIizkuF3bj6PgKubnTEgk2kotCENmkxkIBDC3CRt5afZrQfBKITAxYizg1nqdhN-8D7-6O5IrptD62YSFPl0svLQN_aQ5x0PafBc841oZrZT5AunHSowa6I7ifEK8qN4Nx_F2vPThsg0-ZO-qtbNCAql3VWnZsorYdeESPKRqXbFwh1Bc9RpEzYDXoRNEDhoIbosbx3ETt5UE3dMrLvizuRaZJl06BTO9gjvNr6s-sbq-wMhOblGNd4xhOMsnztIzDZZRpiKtl0e6fEnacVUoHnMmDn0yKWLeJYB8r2kGURNR0RtTDEgYYxZQ5YuNQyKnHilNq9uxMFOySuOm4L5XGBeHV1jW201JBDnGQAkoTbsDIsscj8bnkXZCXBDQT8tcUxmLpnihuM2cBYYJKLMOjsRZ8r5-6__pPSRDgkTrYzVuUOEtRas42M7U5ilfvF_RQfQLIXlbyOTjwTB6cYqBlY70bPFYy0NuZbwqxLXdhX1QeZfKTYXMhGq1g87wv3sRv0jcXV7P9w0GuZEfaq5kmH1xdusPzvGQZ4x26Ya7-LQriIHl1JYvk5aMul5fJG_fKmFxkNZ1KQJrsHYm1UcDVoIXv8B3x0vX9q8VB30ZtEVl9MPdqjHSh5n5Q68F2jg_hNdQbVJyMuhpMx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1tOx1v-_3285Z9-_L-d7oF1)
