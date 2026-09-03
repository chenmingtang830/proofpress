[//]: # (ob:ae580676)
# Proofpress Design System — Verified Knowledge Ledger

[//]: # (ob:4565936e)
**Status (2026-09-02):** Canonical product design guidance. PR #100 implements the accepted owner-UI typography, Hugeicons, shared feedback components, and Ledger reference direction; local validation is implementation evidence, not Render deployment or partner outcome evidence. Product hosts may supply their own brand shell, but trust states and evidence semantics remain consistent. The owner MVP excludes assistant/chat entry points.

[//]: # (ob:678e1b70)
[//]: # (ob:hosted-workspace-v2)

[//]: # (ob:9368ad00)
## Hosted Workspace V2 direction

[//]: # (ob:efc880ec)
The owner workspace uses a compact, three-part operating frame: a 224px navigation rail, a flexible primary work surface, and a 384–416px contextual inspector. At desktop widths the selected row and its inspector remain visible together; on smaller screens the inspector becomes a sheet. This spatial contract is the benchmark for Home, Review, Ledger, Activity, and Admin.

[//]: # (ob:cfee6f69)
Hosted Workspace V2 adopts the original dashboard reference's **information architecture only**. The later Proofpress MSA Ledger reference is the accepted Ledger visual baseline: warm paper, near-black ink, fine rules, restrained teal, curved evidence-to-conclusion connections, and a persistent node inspector. Georgia is reserved for owner page titles; native system sans carries conclusions, evidence excerpts, controls, and metadata. Legal-specific vocabulary and demonstration claims are not copied into the product.

[//]: # (ob:06711fc4)
Use shadcn primitives as accessible construction material, not as a visual preset. Reduce their default radius and shadow, keep one consistent control height, and build hierarchy primarily with type, alignment, and rules. A component that looks recognizable as an unmodified starter-kit component is unfinished.

[//]: # (ob:bd3d4bba)
The desktop reference viewport is 1536×1024. The primary table begins on the same vertical axis as its title and filter row; the contextual inspector begins at the application header and owns its own scroll. Selection is expressed through the canonical accent-soft wash and a one-pixel cyan marker, never a glow. The mobile reference viewport is 390×844, where tables become structured records and the decision controls form a safe-area-aware bottom bar.

[//]: # (ob:c3130a45)
Hosted Workspace V2 does not define a second palette. It uses the canonical tokens below: paper `#FAF9F5`, card `#FFFFFF`, ink `#20222B`, secondary ink `#5A5D6B`, line `#E3E1D9`, accent `#0E5E6F`, and accent-soft `#E3EEF0`. Green and red remain reserved for admitted and rejected terminal state. Pending review and model recommendation remain neutral ink on wash.

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
The hosted owner workspace is a steward's desk over that ledger. Home orients the human without a chat entry. Cyan is the seal and the interaction, never a substitute for admission.

[//]: # (ob:66d5152d)
Do not optimize for "looks like a 2026 AI product." Optimize for this: a future agent or human can tell, in one glance, what they may rely on, why, and under whose authority.

[//]: # (ob:6af4c951)
## Hosted owner chrome

[//]: # (ob:fa9a96d3)
The current owner MVP navigation is:

[//]: # (ob:4ffeef89)
- **Home** — orientation and next actions; no assistant or chat entry
- **Review** — governance inbox
- **Ledger** — current authoritative knowledge
- **Activity** — consumption receipts
- **Admin** — principals, credentials, policy

[//]: # (ob:0605066b)
Admit is the lifecycle verb. Approve is the owner-chrome label for that same decision; the control must keep `data-decision="admit"`. The assistant may explain, query, navigate, and draft a bounded clarification request. It must never admit, reject, or appear to.

[//]: # (ob:343a8d41)
A future host may add an assistant through a separate product decision. It is not part of the current owner MVP or an admission authority.

[//]: # (ob:03c75a58)
## AI-tell denylist

[//]: # (ob:7097ec6f)
These patterns make Proofpress look like generic AI software and hide the trust boundary. They are defects, including when a host is exploring:

[//]: # (ob:b42cc176)
- Decorative gradients, glow, glassmorphism, or aurora backgrounds. Paper is flat.
- Ad hoc font families, sizes, weights, uppercase kickers, or tracked labels in operating UI. Use the role-based type system below; keep editorial typography outside task content.
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
**Taste bar.** Would this still look like Proofpress if the logo were covered? Paper, ink, one teal accent, an editorial page title, consistent sans-serif task content, and monospace only for raw proof identifiers. If the page mixes unrelated typographic treatments, it fails.

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
- **Owner page title:** `--font-editorial` (Georgia / Times New Roman / serif), `--type-page` 1.875rem, weight 500, line-height 1.2. This is the only editorial face in the operating UI.
- **Section, dialog, inspector, and scope headings:** `--font-ui` (native system sans), `--type-section` 1rem, weight 600, line-height 1.5.
- **Conclusions, evidence excerpts, controls, and prose:** `--font-ui`, `--type-body` .875rem, weights 400–500, line-height 1.5–1.6. Dense operating text uses this role; sustained editorial documents may retain their separate reading typography.
- **Metadata and labels:** `--font-ui`, `--type-meta` .75rem, weight 400, line-height 1.5. No decorative uppercase or letter spacing. Compact existing badges are an explicit 11px dense-label exception, not a new heading role.
- **Raw IDs, hashes, versions, code and receipts:** monospace only when literal values need inspection. Do not use it for status chips, lane labels, or ordinary metadata. Browser zoom and text scaling must remain usable; prose should stay within approximately 45–75 characters per line.

[//]: # (ob:877970b3)
**The Role, Not Component Rule.** Components consume shared font and size tokens in `web/owner/src/components/governance.css`; they do not invent local type ramps. Brand films and editorial documents may use Georgia for sustained reading, but that exception does not apply to owner conclusions, evidence rows, or inspectors.

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

[//]: # (ob:b94adb0d)
### Shared implementation and icons

[//]: # (ob:1a3a8bb5)
The owner workspace uses `web/owner/src/components/ui/icon.tsx` as the only application icon entry. It renders the official `@hugeicons/react` + `@hugeicons/core-free-icons` Stroke Rounded set, bundled locally: default 20px, stroke 1.6, currentColor, decorative icons hidden from assistive technology when their control already has a label. No runtime CDN, API key, or mixed Lucide/Hugeicons family. The official Proofpress logo remains a brand asset, never a generic icon replacement.

[//]: # (ob:379056d8)
Shared owners: `ui/button.tsx` and `ui/badge.tsx` consume palette tokens; `ui/modal-surface.tsx` owns dialog geometry/accessibility; `review-feedback.tsx` owns DecisionNotice, RevisionPanel, clipboard handoff, and history identity; `lineage-graph.tsx` owns nodes, curves, and bounded source expansion; `governance.css` owns their visual rules and typography roles. Reuse or extend these components rather than copying page-specific markup and hardcoded tokens.

[//]: # (ob:8bd7754c)
The Ledger keeps evidence → conclusion → governed context stable while node selection changes only the inspector. Show a bounded scope overview, then focused provenance; initially show at most three sources and reveal additional sources in batches. The signed-in owner's eligibility is not a claim about every agent's eligibility. Local fixtures are visibly synthetic. Validate desktop/mobile, keyboard access, long content, clipboard denial, and real receipt states before promoting the build; record implementation, internal dogfood, and partner evidence separately.

[//]: # (ob:0287d639)
- **Status chip:** compact sans-serif label using the shared Badge. Admitted/current is green; needs review or revision is neutral ink on wash; blocked/rejected is red. Pending and recommendation surfaces must not use yellow/orange. Never express authority through confidence percentages.
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
Every mutation must produce immediate, consistent feedback: prevent duplicate submission, show loading/error state, and project the recorded result through queue, conclusion, history, and context. The shared DecisionNotice appears at the top. Request changes opens the shared ModalSurface and attempts clipboard copy; claim success only after the browser confirms it. If denied, offer explicit copy or manual selection. No agent is notified or awakened automatically. The agent receives pasted instructions, submits a linked new proposal, and the owner reviews it again. RevisionPanel keeps long instructions collapsed. History displays recorded proposer/verifier/judge/model/reviewer identities; missing identity is explicitly unknown. Deterministic policy evaluation, optional LM advice, and owner admission remain separate.

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
- **Do** keep current owner navigation as Home, Review, Ledger, Activity, and Admin; do not restore assistant/chat entry points as a design cleanup.
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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2QwZDM3MjMwYTVmODdkNzA3YTMzOTc2NiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImUwOGJhMmM3IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV80ZTY1ZjkzMGM2Yzc3MDY3ZmI3ZWY5YWYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzVhYzNmNWQ2NmJlY2FlYzBlM2Y4YjQ3YyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtveuOJMeVJvgqjiIwlKojMt3D71lYaJN1kQpNigSL0mAhCZXm7uaZ3hURHh0eUVkpNgH9mgeYbmD-9GCAXWCfYBfzf-ZN-AT7CHsudvPISK_MLIrd2jVBJDMjPdzNzY4dO5fvnO_7J2K761pR7952zZOzJ5vN2yZs4nwRhyJti7zJw1zEcZln2ZPZk6pvbt423aUcdnDtcCUWaXaWhXlSh1GZCrFIRBtHizJtpQjlIpdVVeVhEaZlk8IHMqsiWYo2qao6bNpWlpVMW7hv0w11_15ub56cfY-_7N7uxCU8YSl2-KgZ_FDJJXzwe7nt2k5USxls5ftu6Pp1cAXX99uboLoJvtn2fbvZymGA72xE_U5cSnyp0cfb_h8kvO5-ize82u02w9np6WW3u9pXJ3W_Oq2v5HrVrS93Yn1ZxOHp6Ntb-Y_7Dn5-ux_k9m3drwe5hrnYbffyh9mTKylwEmVYVGJR50_4k7fyPV0EkyvfJjJL2zIO66zO8zDL2yqXLcwJjqzf7vDV3i67tYSR6xVZvk1FHbdpk2WVrIWsQxm3RZXkNb-OGt3bWmyG_RJeeIHjrPttMzw5-8P3T9Tjv38Cq9xvB_yJ_yybtxVM-R-e7Nfv1v31-smf4B20PMCjm74eTl-8fPP61789WTVPZg-SFbHbbbtqv4MleluJoRtQYuSyfSsGmLqdpPvtd1f9Fgf0rlvjLYebYSdX8Je1WOHK6YHN4KsDrvaTs_V-uYRh1lewPJJfsFr29Tu4Wsi0gCnFp8PK7OQHfAkrE8ELOXSX6-ANPST48S__ErA8ySb4e3gMfE0NQzQNjW-DQiav4ZPPgvvfZymbSxl8if_ewk12Nxt8FZQEkKonP8zsgJM0S8s4k3-FAT99-mYndvsh-MUiXGTzsJyH0S_Pnj4Nnu-3W5CHoN72wzDv4KlbWFIZXO67Rqzhh7a3g96IrRiNuMyLPMvz8Yi_hq1Lj52awM8C57KJOZGLqF1UafPgJ7xeB_1aBpurrRjkWfD0qQg2YiO3c7Fu4D3fBbQu26dPT4Jz9Ze6X_ZbmMxh4o2zSoRVkUcPHo-zjmaWh2Al3kkaZ9Xv140AvbWUlx3s-rMAvthIXAGxnhhPLdKmqsTDV-C7Kxk0LFC8zYJuCK777bt22V_P13K_24olzg0MSCwDUCzNvt7BgG-CKYkQVbKQWVQ_eDxPn-KIvtvuh13whZ6Mb0GBnYCUngfDnuVyhX9fgw7bBt1qs7wJdldiNzGePA6TeFHHo_G8knKJgjYtoPaqCfmspIDTrXjw_R1xGK76_bIJWvhSsOxAHgRLQ_C-X-5XMriGwwg-q28ELJUUy7OJ103jRVMmbf7Q4eDcX_UgBk0AChYmFyVh2OCMg1iIAP5yLbbN5wPKzLsAT2eaedxFU7sla9IoXTQPHc6LPlj3u6Df7LpV92dUQtvgj0-Wff9u0FOEeiw4f60F8-SPT4Kv1eVTAwJzoy7T8fb9jfvi9dW2X8mPiMbxb0yISStKUWZN_CnPvbVGr89xcdpt_2e5DsQQ9G1gtftJoCZx2Fe77cSUJGB5ybYoP2Voc9Cvv4FrYKvisdRvOzhTBB72oL2a4BxExhF4-Nv25hkNTgR__81rO7glGG-jwYVZmIZg6HzK4M6bVbfDmdrBBC67VtY3NViMIMIV6LcNCNB7qf9M95zzPQMwMyfmLU5iUTTJJ4nSOS0oKdV3Um4CnMMjM3YSfAfXSa0EYUNuZTAxtDCu81SkxWho56_nO7lcwgZe39A8T4v4kcsn5DsPy1zWWfvoJ4JwwwtuwEyU27U6Fx2Rwa3PO_9SwtR2NW79oW93oJWm9jucRnUdHdiADxnXHKwuMI5BlkFILrfw5iC9wyy4hFMS_w3m66rfbsDrWM1A7gOx38LVQQXexuWEXMOJUYEdMR6Xsu_qbbeDFwS53PVgknxkne780sRqhWHeRG2UfOLT_-MV6h34_yVakPCNDQjpEIAjtgeLAU-QWbDdr_Hs4puKS9GtQd6HekohwZFairyKP3F0YFAI2IywFFs0If4jHbI7WCg4zDpYfStSrmnWkhqYGl0ZywRcrk8fHZk6anTPcRphYFt0Y7bBpgcbMdj1NJgaFAIY4zs5o1_l-yllHjagMZvqk0f3rWzlFs3PAYf3O9ib-Oxqi9Zz2y1XPIkDKavd6GCask5kVMjkQEs8ZnRf73eb_Q5H9tv9qpJotLdwNcg5bE0p6ittNIGkSbkGC4s8nE0wZazkUdrKsK0_cXR0TO9XYj2jE45WkL49A4VTg00PZjZuHFjdYddv0MRWd99dTY0uTDNwtsaG_nP0WIaPaAhz0aTrGcV51i4eePd_Cr7r38G7_FPwZXd5tYP_vhDbd_AfFJh_-uP6n-bz-egf-IidLbjmMzskCnQcKEgQ5Kx96Ovi5C_Ffg0SQFK6lStUOSAJa7FVWnyrRXsWVHteoB5GJKY2fVrlUS3aB46GfRr0vOFZvwVh-AL3j_Fqfo2ySTsIBbjuV6v9uqvh4mAnpxSkhP8tkjB9xNy03QfcK2K5xBMKjtnNBkSB7Otfd7vf7Kvgm29pJHjKoVF08f_8t3_5v4NV31xMDKhNyqbKF2Pp-e5m08OBubm6-Yh8ji6ckNE0roo6FskjnoL26Yu-3uNrBereA4Y_3vTry10XvHkenOIC9cEbjKjg76RAfi377cQpXuR5mYcHJ9X9RsSiocc0AwMPROG1Cb8YEYEBXHYiuATBHVj9BlMaNslEmrVibJR-KW76_cfsPXPRxAoUQoSVSMUD746z_wredJBNwB_i1A9wdwrc0nNA6MDZXWu9vRIfutV-FVxP-QZFmtZxWTxwNDzz36rHfr1tQBnp6f7acVx-_E__Wdk0nfl92G82E7PfxFlSJ83Y-365lO_5jv8BjLUNKfmphTh2_cSaZCKPM5lFj3-ma_6AO7kEr766gbOqFfvl7iT4jei2GIIGU24p4Xgl9X1aiy2qrCmd2cLAFlX4-IH9tm_A55FLWdM30EsCGQLp2F338y0JDcZEWhSt4Eose5IeWH7wvCYGFpWZTLO8ffzAWIQ4pMuK_YUYrqoe50SL0pvddl_v9uCogTqV5KavArzh3QMrKrCNmmgs0G-uYL4_dsSbi6bUp4QzLI6bB979W04dgO2JZzSaVzouue2v4VfUSEO_32JsDo6ubQemP5-6wXYyjlqBnSqzB47meb9eS8pbkA-MgrCBI22JnuPVwNpj3cPfYHA4CUOwXy9RsptuajRpUmaRrMsHjobl4PfdgBHb21FL_GOtB4zWH9jMaxaydT95nMZtLuLw4Hxfbfo1HssfNfecC6ecwEWRN1lcPuIpqNBVPqG-6jaozUHINwLjw_2657ghJenAusXoC7gGpzVnGiYUel3Iuq2isV3zZV-DRH3JOTDw4lRYcnoS4Di782tTVnBSprVchJ86gPNA5ewC_IAiqGvY-8MGJIGylTvy_VBmZyoM1oItOAczbDUVWy-rLI_j6lOH93zZ1e9QfYLV907ekN6aw-J1qAHhYzCWUfO23RYGud-g64kWNKj9oZsU2zxbZIfn8cOHp7Tr6It6S30r1w2FnuFgWIEVC1sqIGOLo9FTNnxYNUlelmOP4lt6KJvowVfgOMLzPiZad3xnKjqW5sUiTKtPevR3HAro0UVYKjsKPEhenK0TJgBTdi0lqD51DRouUxMjhEzaPMo-aXQvMV8frPbKeKI0DYfmZdCBO9F05ARhihy2PZrhLYwRnZCzyWhLjTZVkRwbG548L7q2Db5RUcN7Ltyx703pybgOs0UhP3kIqDWfU546oHuj2lT2zBXufj7IBjg71xgNoLQxPkCANpnQmjIr4zY9CEj9vu9q_vaX8MA9Ah8-MjlHvzExLXEYShmV7Sc8FoMEKn0zB68HVQ8rRpjK1XAGzhmaFbPgpbI4ZhgmUzI-mRKtcpDn6BNG9hJck2640lkBZd8s1TfJXf7dawzXccTp-Zevg55CUrPJnVaFUVPk1dh_etF_zmG0F_3684-e7revnlijpo1a0cjo4HkfE4UX_UeWvhJlUhf1A27LDjgIPPoZcvueFv4SfQ6MyCDgZ9kPaCyTmQx3rZd7gvOASz4h-3kowzBJ0oORwMx8_B35okmtnTZ5EoYPuzm_KVwEL7sD53bnJPKHYLgBBX6z6veD9nS34lrLV3v4pn-aabTOk_d4-PbrtzXekh5Jf9HQG_k2LfJShs0ijkTaplVdp6FMRYmjBwuDxFEBioxxUl_J-h2FmgkfRdYZAWr0b4in-RMikcBguHHu4KKTnJsQ7umRwCXM5bxtO4x-b7adwkcNVXRW5CJKC9GESRPDd-D9GpEmYAhFYVnXVZUXoo5EVhVhLqpSLMoEvlFmRZLLCK5HtYiHJOGceLXOsuQHmGhEIJl06eK7RXiW5Gdp-HdheEZrrmYcFUpcNGmTpiAd9tPvfzJoFMkbQ5euwI1EPZGXMFFFKwsyz-keDppJieJPC0JSj44KKeK2LDPY4PrRDi5JPfpT4ERbd9igOWdgXmzfNf01OIyylt0G02vavFEJz9nIoMb0GyIQ1rKZq50ZKBwfLI3ySXeH2fLzv__qjUrJnuAQCM6CVwwUWcDQDsFJZLfFb6hg23CFmUL8SWNjgvdgmVb7JXh6HEB2XoePL22UwZfM3tfH-sCmkfaQwbm-XHd_pm2J11v76OTIOaLWKE1gFyRpIsLaiIeDxNLi8TGIlbqbSKpFBEaWbCgxQ3dzUFfqbp8Cp-JFnIEH9M58iLflhcLbYhxnXi33MAl1jfLD68tIKUHLehK80ZYR3YOQKPW2qyiTD5JeW7yBaxw_wyW9IQuZYUONyufCLe-e4jJbLBYZ-MeSwuw0KQ706zY278GYrgaD6nJJIoDh9oaGNKAZT7IIShQTp8bgsWciS12_BmllzTxH53vZCYxtY-IpEOBzEz6SxgKD25kNE7zT2uAkeL1Gh5OnDYY1dDvYBng4D-xNYbpq4Km_ArnfXbmjCCoJ3wbjnvYP-Qe4IThDqd6ygvcHwVZX2pNObdGNpJQd7Sx9Eb2KxF2Ln06s0AIOjkjKuoplolfIAcPpYPwnoNy2l2KN4CMenvmA5muGwa4dRv_wRWCB4CDv-9UzPNDBwBHb-ur4zToKriptRelxvoU-MDTUg3Ahg44hsoeHkQJH5OCcXHWY0RpO3I9Bd7HVqvLwI6tVGlP6mGRZxWs1sZWlgfNYpOMoX7W2m1ir50rurjGpBc9fTSwe2MBxKuImj-vKHHAWOWhOmcdDAuENwDqX78USA2_oUHRrUKygPXCnXm5B1meYZziyBwnHAS97SbGQJe5kRibD-qFTjTuthu3za72l9BlUwTaHuaedKdqdilPAX9vuco9Kz87lJU78sAdlB476xEQ1dQ3qWaDBLfVEOZBGq-onwYrqZllYplm7KBIpzaw7-MXbSu3ByESV273p96zHQNrxmhlhG8RqY_5CQjSzygg3Gdyr2ndLUgmodF4TaAu3UkfLSIjALULB1zuxfBb8476TO_5Yrja7G9zGLL4wBHfo5gCQHwSKAYW4GPOu7orpXxX6anQkf2JVZFHltShzkWexnkgHeenonsdiKuEoPbkLDUavggpZKHXPcLvBPen6HV1h57eSnIbQ58BJ8BxXTTu4sHjGanIO3ZnaVwJRhLB7dvsd6xEjyROzJGCHx7LIk4KSDnyGWkCocag-BepJlyOo5wxjqHvKtzAcCT7n2SFxAyMO7Q86li-XgjTgNc41TRlqaNjXoKbX-PEN67Q9hRqvSR0rBQBCdvf71lUk4yzOm3RhbQaLN7V79d7oUXXjpIqaBtyfNqUiErqxAyi9S9weAA_FyP2OEHja4j6bMD-zti6jOIniWBgXwYJI1XA-DRJqt-Ef13gnjrepe7EMkzvRrav-A1_ypTJA6RKVbDDrxsgPsx34G-cY8oY11d-BA3APigSHqM8_dSFI-1pdhd5p3W3EEs5GcMbhNN119AvbYuoLo7fT30TXkWOf6sSYi2uK3C7l9t2RKIe2dMpItm2b5nFpLB0HF6tBjZ-AcgUdyfsINsQA-tVYfs_0Cbbb9ks-aAmneoEWz1xf9b_88Qnqg90fn1ycUNJLDPiiaI_izpIfNktwdmagsMlEXIv33SWZEmQ7beGo1AcLHqbgWFlrHgus5LCjw8A55-lxaKywFYUKabMBqyvY9ZNWR1lGYlGBgJt95KB49UR-AiZXTanY0ilJK6GSxCzZA2hhNPbuoU1SGTdVKOqyFcYtc3C9VpvcD6irZWkRNVksyxKEytgTFrtrVcmjwbg0VVdgZdLrs0OsHSGSDj6hGgkSivZlh8YnuwEEJ-XZB0FFsekxwDqhiuJISHDVELdnzCMH8mtU0eMxvLSSaGCTYaPwESe4ywmsMwt-LbuBRbCHF95q3AQui3YABoEINN56Fob2HiPSJwbhU8MfOhAje2TD1wdwX5XfQjdhQwWuUltyoJGgvtx1lJwH82L7jtAaRoEONLgVmsP1MMc9PscFnIOtjIE6VJIDCTnd6w3dQKJ_c9nV82tYTfr-j__6f-J1iMwBbwiOEivDgbNjOJ9BqTl1JfkCh-p-119eLuHdutGuRnMRridNdqpUljIddaqZ1-eo80LDJ0gdKgYedU942oCQR6jhrO8_M7JLVvjAs6RcpveggiS8GSvzF6ihQIfT67vbwChZdC8o7kFwIbgB2XdPn5phYliEbgN2GDgUlzgDQaPAX4PSDmNHix7-vN8od4ZCycPBPE56MBigGQZCyWCIloZvrDa8OeVWcY6C5_CEX3_znVJfZ7AnWzCTcXYpqcqSq6R5hsOr38GESoLMoMpmKdM7K9ggMpjGQL4PxwJAcjGyA8YZ7QUrPrSXVug80oqw3qe1aGTvfiYG41L_7vWJ8gtVrO3OoJpGBKn7oBO2W_XDBraqPLn7zG3yOhJlE4K3ZMKgDmbfat-HwO-199CkIRzlqUhC4z04iHx1708B1yvIM7uixtLbKLAroo7pSyD-PcbYHIwyPghMoIlzKczrTMgqXiSydpxIjdi3rvujwffL_rIPwIfDzf0esd2_Yu1LAcSZiReS0zIz-hO3t9Gds5HWbFkSSWHOHIQKfk4F02BetKiLahpmhSrMOdmM2zbDa1rRLac89qha5PEiLKqytfNjawbs_Dwa_q8jOPRH3NoD_ywaEA4sfT9UBiYcTv6QttrIJqUQt5SsYyhwQSsAa0fzTHbW8Cucntua55LgyzQCrZZxWfBUtTO5QkMQIeIjr_FeM9mCuda04EBWifGnnPoGM5OPL1XAM8eYb6OgmcGIa-UMYtM3jPCDw4-PeqWNpt4hKcOFEGVVgBNoIgW2CsK8w-MLGigIvuGFxhdAlCbO7vuup34JKrxIB-VW7ggCjrF0HCkizWmb4rJojCKZbHMTu-Y_GSUCtwE9v9vjvc2H3fo9OVtwjl-D2zkVOalFEld5GCa5mQ-n7sJ1ZR9ZQiE4arQcelhSPKbAOQFVcg0WEUj0r_74BGYSFNAAxsqNnFq6RZSEWVy1siUMqzKVTRGGPQKm6iu05yHyokqKUBZJZLNqpuRC3evTqilenb8qX6X4U5RGefQcfvpGKAgJQaTmoEneg5hbu5Zuilo1OKXkzEL9N8a7LMLFYvEFfPJZep6-yOin4oviZYl3_uxl-TJ_GeJn59l5-UWCP-VF_kWR43O33Qpl51Q5PPwzyLPE6gMwRQVFzOnpZKziDeOX0YuSHvx88Sou4KdvGXBsIJRKlrs1YdVMfgWtZroVYZJPg2uYc5oQ-h8O7FX08tXLgqbmBbxWjp_By6WLF_AZYtLQSjKa4JQjixqwh3oLXRqKz_G98WEqUXWqfpij_4NPCF-mLzN6KrzRy1chfpa--iJ-TlMU5XGeRDRFVpXKBp1ZA3TGI6qh1O3MjcWpxzb4ivDveXVJk_Uyf5Hw4_JXi5fn-Fn26otXxUt63BfxYpHBZyYZrA8MoWCZ7pmppvXyMK5ND0Yr8xT_rR78RZKk8TnNbo7CgJ89L_KXBQrRZ_H5Ag5BXENy0flV3otlBz9Qvhs_AXsNHqWkUCUeTtUP6ilW9OwaWoEza_jcnpEu9G02fSbyMqOXu7YTjEOCe-N_1BiyLD0v6E1hBC94i52fn4cv6E0X5SKLcdq_onehOVvzWfpM-TVuOhIPSm1bOE8-Vgqlj5A4DRdVWoJTm1pT1FRHOSrzsYVPFPn-3Wt0k_ALNC10NFaD3J2BqkVX4OKzl-cvi5fhhfFUN2qXq1ee8fF_oaTdXudGrmn7jsLLlIEjHWTuq9KCW4uxu3MZ8aC8UHJnn7hVQoeTbaSN9SCaLBdqh1zgSaHwSOwfvtfbRBkruENODlZWu7mrPT4Bj1m5Own-N7kEu-dUOZxwX7IanAz2exNHmymHdnbUazMyQVlubZ0fzyOcBF-AJULJNu0DVZJNWiyrmbJL0qSFK5o6EdZKtUVuowTc4-rXVqCmlyr8pTza4Jt7r6zK17NwIFoIZ3wtO7K7rlz_8VmwGi1PNxysjLJR8AbDAYLADQnA-sjV5gpbE90rNsD5ExSGjmLA7c2dgv5eusodtx76GmKNw6LYmhvQUIFMI30TEcKiTtqkLbLY-pFOaaCjGD6h6m-GP_-3_wMnmX_-l_8LD4EL3k_4t_8drb4LEEWEb6gAM6L5EJqt7g56_h-6AHtlwREgHdcGp5DPz2fgnm43SwwMLruKXPUlCsVmSWfyDW0vGjEtN-yhPqDUFwgUmakqvE1z2g0o_hywuRZbzPidBBfkEeCPtPpnAeJNLnCDqVGeqzIjbZ5ol9H6Reog7mqEP1grCm6BECa5o8Ge8n0wPjRgUg7WuunloK1niqQ70z0Vr160adQUTZiHBufjlFpaC_RjFZRaYDBnCUZtUtkElVNU6SRuHlsriY74afBdh-rot7DDv-3R49SCB_uoDEMwxdG6nQX7DcrBAk6qE3UrEBk4_brhSrIYaVBEwI66KcWrJIovZ3NlQ1OsNe5ms0T9DTeWhEi3EDT1Kiqox5rMno3420Ho9cypv6Q3PHwvdp5x4M4bRumPf_nnqNh8gImITjL67aQgyR1AQQscsS56xHh4N-hNoyPHFBjmhIy4RPMYgxZi3bUwPb0yF3uqs8IAHwbUMLXSc3INY8CEsZnr8CK_DO9XxynWsJAT8i628hIRbWptlE7HeAQNFxOEaCNzOggFbJRfZ12Mm3IlMAOrES2cuA9ghq84tb128vdqHZ7rTUZQMGONmDQkrMGaV8iJ6Mx51ikQCTO-wDlO1YzzhOcnwd9j8gaU7Y4mRSWdSAPD-4NQOCVtxtJXHgaCoaQ-pVYSm8shcs99dK-UwaCjji3GTNAhBVWu3u33jBWFm-IGJBRjD8cjPQamX6Xe1DN1xhHf-GLfzU2YClTtm1dfwW_zb3mRZsFXcr3s3UgWiefFjmGJ8_V-NVw8C6IQpoQfYYwWZ1H3GwzJCgyXqOWdiocWUd2AGVqmpcn5OtXPI3vhcUXNeifODqsJldNnshWOIqC6Kit9RuJAF76nzMSLbgCdfKN26Ui9dLslhjXe2DU1yRUn2o3Gn55k9l_NnzFsqHPocmdPCzxQ-AVBwPZb50ABXdQH2DRTb8kefQNCGWBSAFOf3YpuYFZ2KhBbZnEFylsmiYlPOOXf9nSYquzWJ01TyLho2ipM7PLaYm_nZHhsHXfXwO99G-QZSiXpIpwIUm9YsQkXaB2Rh5h3QMsJ9s-JCej1VKlt9zHVNZm5xV8ccCL-emhRrrX3S381IEX8xSAdXbSBfgcOm2LGGl9XBO1Sfuiq26-Me2wjuq3-Hltd4AaDRoqTBF7bhF5p4Wm_wzfWWCZJ2uoAYUlyDwaZGSqboGCMND2a1-udGi_XyikMHg_SpNM55nM4tjikUS1wMYz2O6GqeLDZW9JkWz4KBsbemSocmjBbiPN8POkGFPecgwe8foQfgg0XLCKchh6L9rqGDSuK5GEiUO13-Ag2O-b-BkxnIrrCRY-YJRo2iJV-T--LWbVrPPy3Pcgb244FvpzKVpmlYu2uVkEfMvjeZLq5zgBXFdrYk545eL0dVeCNBOhA9HTkZED4AlzzzNa9cBSAzA1VesmSbd4L9YG0gFA6EAxCXp9YZFuCL9EvNZS67ht18NadMgV0Vow0jBi0i3QSvPyAyaSGELmYpQVLjDKWnJSfOAbqPE8LETZtnlsoim3DMDoGHt9hAaHP7q7Uuxn3C0FdjxUOMYbrPQLZVj0BDMDWWhp3i9PMPU4HKxKLThDbSzqvJnRtlpRthYH8ojDxW6fZg9W192zeYEI7UVyGaZjWYWQRY6afwxGU-UP7M8CZJIadG-66JlPEnoXBVQfHHpycN7gNlIxS_n64EiBz7CUjcvbdze2to8OWsplTzbB1odtlz6ac2gvoO2tcENZD7JWlDq_CmA8NJEaneXnbiMW3MgfuJbnrZOBbsDkGeii8RjuXhoPaE7eNHQxOC7_YxHJXiZCyydIwrEz212lnodblU9pTgPGNF9AgG3Ar1mQoIuQTA4Z4K8wFDkvWFaNQgoZa03dx9rDoHsR4oc5VHQaCvYHKQuMYQafsa1imVU-j3dgM11QKLm0bMPFy-McIqNM-Y7TfH9cOA47S9eVMy65W07RFx3bxj3_5F1x5sObAKkBL4hB-AEpfIsrlRmNhxsEdg_uZQnBGMm9TIeo0NYhVpymH3eZT_TZ0piuKFmm2KKM6K23mz7TgMHXEj--ugXJHwrDlQzaHEx39TnzRbpT0VqVF3KHBbg_0VtEAwEu1vXBgNNl9Hi3UlcJqAbJdgp6VKQg2GrJKOp2kOT683YNCIVwIH_qsUwysZ-D8MaqBudEMZtMaOOFUQFMmeZaHbSij3BbsmB4jpr3F49uHqG1-TX4vJYCvu0ESWmBVdZf7fg_7VxtJ810_d2yCevxc1sRDvwQbiCT_xBpU6ptkPjhfg5v2ClNngUI6SXuGi3pDkC8snLkC-ddRdA6Rj_6iIuJshOrsDAsaDohj5E4Rw32w3lEk8qqIMLVrpt9pqjJSFI_rl9JIx0-HyzYKpS3ewzHP9XO1bT0g8C1Ogt9yxRfaOUK9Hq40e2K38lw8PQdGeDfYqXQyV3re5IdNR84niC0oJtko5Jm4Ft1Ox7o_MnlJWchCpmXSLCy-2_aAcTPN061dtDcH-rmoojTLCqN6nG4vjjf32CYuOCskJ8_GrSb6rSViwIick93BrQPDe6Yn8dQkaSgJ0zyzuP1R4BxWmgK7eJbaDII6GY6pKmvq4Wl84-ZltEDAonGUXicRsANDv7-8ugOwpoGA2OkBPnCnqluT7YVWNNonv-V2L5cMQ9R5XBq8zXdu9YbjX1Wigp_xclw7h48iVAfNL4m5tpD3a8TQMO7GgiCDN_sVDIZLzQZVrjO2kQb3VKnhgt0zcMkYIoZeyppTg6p4j4LouIFa2By3Bkk2FyhLHCdegNE9En8dueXkCBZbmdyaCoLNzJljgpczW5ylq80UeGWJOZEtHjE6d9CtsNkITQi9iXY0q363A9OCYTDrYYceLcJV12Rt4FZWMVE2hEA60X7Q0cgjuFKKcfBgHGfFOalpCmdHM8zmzO5IWhDGPozTwS5wEalOujVMGhlHd1StOaWjWN22HzvFdGc6ls90s4U1PXI8tvG9NSbAFivv27arwVqqlZJFLDZ8sDOFBKfgKxAyP1DMG_QJbmgqo1Bu7-DENQ7AZ1Zta6O4rwbQLtQEhAQeDaMTW3_BJ56yBvHlTG7I3NOaO3xu0VhVYZNiQDEFYjPztZlOUl6RqFASmD_fYbwfy9aUGG5QeuZ0MiqWmRMqQ6QcYQDXDmT5qPdRNZ4o8E4SFLUDrLGqclXv9-u7q9lZ16x3wlYWauQGGXWsj_FjtJpqmlGnxPcLfWI55sDk0UWxWFTpc6PInfpQ5WWTtIp90_EGRBfbKF2dvzTrS0jna9iJYNyvVJENBvb41bnHS8CLcuY0CEGTsLukJLLVIUw2NLMqxI13wKJcXi0xaEUpe8pw4kYyYo3ReWVLc3si5e4e1iah2GABg9E7kuK4aDlMxEYqrPPKZIzV9KYg2XY0M6f4A3uT6TM9iYuqTJKqaS2CzLYrM7Urj288Bsu-o1JnchDA1VbpKKVvtZ_viMPnAy0ElU2_l2uuiv1ifOKQn4HfAQm_lGx4jVCtzv04vdTSmlMajrpIqIg76Y_5bdv3uC03YW0VaVrKRZOXUWacPKezmvYUPqFHGtd4WWNVuRUNp85mGjDQoRZSJ4tV705ouLP1-bZVglHFa1QUujeCOZHBWlLl3-ro_1DL7Wany-tJtZo6fAJOmoXgr1pLzui4W4XO9iHyAx7yzv62msuJ7mqV9Wzsm2BcTuOUXCFFffKenIQbsHKMJpnCajZ1XJRtLEURWgvatKMbxyke1VhuPVxj3OHHv_zr9dUN15Ri6nbUD0GXxv_qx7_8V4yxMuCYDUsHAMLpR1LGZL0NGourzgk7hSrmUd3APuPACM05CM_W0fJqnGZr6Twyh_6nwlxxKhZpGqdRbKO5tkueo7Hu3_JO-4OxjKJ4UeZlkhnwrO2C52BTHt_STgmVC_kbFChMH3EW_6WLw4eRBuOwN6KW1aHPe3VjQGFKnY4gBsHQEYgF8_BoWlr7XDauiXgSfE3n9doZqvafnCFQiSR6PA9RYkmU1BI79Yjc1qfYPn66qe0nNOVT4cOg2ZNdQe0KKgPfH7C6XAslWYjbrQrpyJkytrQdh7qMkJgU-FUge4oA3GV4qUOYzEm-yUAnkdpL-BEYmHseuumKotZqphXXTHfUIZ1FjYPAgcRS1LnpiYFxBJ4Xts6oJvyKLL2BNOxJ8ArbZnwQaLCd4f7_jtO_mEHZMpac3vG9ZI2gKlZV5ezt5dYKDxTzct9QeHbXLakhgXWctTidgCaZCLqkTS2ypimS3JSIOg0Tb-_fe3Y-NDK2SMskX-RRWzoVqLoZohNGeGxXQ8wvYlAAlgVUPhgfzXwJDvrSOBUwUcoQ65dLscHN66R8BqXvdI5ATy1GkenA0BATQlqRn2dHNxrRTCUGdKcimy7RQUqUE7D0r9AfBiE4t-EdykPKGep8-MO3ikox-B___XYMiC7CYkq8buiX73mFFSKJfGmCmbN7Q7kswZBz3euEZm5tjQD9bqKF471hC4xMF1F1SzQnnPJK9n4xEMNYdmptokMb2oeqBD1d1eK2KtvPOf65SnQrJcxq17F4hO6_pWaYc0bKIa-EMoTcKKMt8lxT4UG_nnM9g_UlGTGrwgDYJgp8Kwq5HDqg6lod47kV_DkIXp-o04wmiO9hdaKJfVqdh3YwdvljQdtIriVUMWHl8mntOeElFGFSgdauKpkbS8Xp4Ons2fs25NQmUJE2MhZtndkSE6dHp7rxp7TcfO7o2m8Vvv6cC_EP1mKm1g__q9S_zg59qZU0vthtsIDJQIICR_3cc08fuTIOGg3UbEVaDzxwWorOVjPXABXLS4zuXa1UahH3F0N-Qccg2geUibhc9yiolHujN6AKfjyUuTEC91WARz19qqT16dNnB00W1CjOv3mtYLGj9ggXAcZppPabL8gauJgqkgJXT4IbGTWFsK2tTFNTfbh_Qo9SREEorTkOnp5YuBY7-6BJN_bkvTiva7nZzbVEXsx4Tz9Hg3CQuoiOvSLyDSXtMzzsnTS27aAHFq5Ew59xH47UTcnaQ0QKHqBCbBhCIQ9KvzmWIikktCBPU414UPU-xliazBlGqQyzCCZMWOiU0-fVqRS-T-dWc_RGizoviraIzcnuNHN1tMRdvVp1RjPLijYKkzZsjLPrtG8dQX4f1531sNkbQdxczxM-uBWrVYcOPpJ6bNzZoet4dTu3WkFxxmQyL_xh5zvtQGrvyn0mge5NQMNJiFpXn8CAuiujJLwMbzMMcB9x0M0ZgH2EuIOVquAYHbM8yWzZ6h5Uo8Zg1hbHM4jFUhcz6V4ixw3dW96D88gl1jmNRJrihTcGIOE2u2QfnTcMvslhf8s5m8qmo-Wt1bxVsKLbonCfCbuj9Q7WjXh4jysHYFxwbFIUTr8it_2KOwgsLOYShObMDSBwnz5KMFEpmgmWHeCknAQpI4ZEc2M6YVGUZyn27MFQCPqqXyKAawI2VUUiy8M8jkvrDdvWxaPtfGdbYg3JkFWYR2FbC1FYz9p0Kh7t6Md1IbZ5Hn0HsufWMJU6YwNij-AcSoqbHSTGMHbl3OFKH9yOnMfHJFUPAtM2AoKr4gacTd8E-BKcygfPp-1vkye6N4rWNjYHqBC6ozSjUyTuFLRghmnUXONw-m-Xz4-6c9wqoL_VrWO8GtxMZLojiU4O3tUrZXxHOvfxjrYmgqOVzdHeOXBr03ZGrzx1SkJE7uaq3x48osI5pyabczrvW9DzuoUmJtBAGzNiBy0nbKVJowVbY-DAlvOWte4TyqnwgwcpXb1CY48yc4hRu1nD-PBosX0tMcAJih5RFVYRaCXuuliqtbdKhd9q0f0D7k3Vpfv7J4LQGvgTRodk87a6eXL2hyckjGf4rA9PsKE2x2D0X0nszt51q27-Lsa_63Ph-LdVhMH8mU6-M5BgfJ8nf_ph9pN1pob12XbVHuX-bYWwPlRJAg6ZYXiLazdwJ3JOo-NLq67oNCJsPA6HJfy6X-NOxQ8GOXD3bOwyDgNV_gL1vjbMQHkhoyoft12_f6frqd7sfzg9_dNZ8Fnwi7464wNqbnBK8_eLX04x3ccZNiEPj7H9mgxO8PuFRQrdj0L6zu9ONKaXbV0Uoax_mrF8pxvCOf0pVSWwAjnMdCgHZMep0WknKRNrcIazNit_ukHCtTDCJQFGnj6Fv6mQha2HAnsM4a4Kafj06Rm8gduM5zYnTAYuVVsnP80g0blGbGm9dnrzkpKmDDEZDGjf0QA59KtLXKY4_aombpLqgDXik2YS-41iEyCDAaVTmlAlMLdRGmf_879E4SLhbn66zns3SYddxxHokAMqhk9d7w2crqBnFHJmUI3FdTEodSu5kjr1zVXTV7d4vkBlcmXNXWrmYBSKLuEcf1Xn2sRbnNylJo7f9YVsuaTOWQZVbafqGe7cbCt5cpca-PizPr5dnNZSy-bkrr08_SQl_fcQ-VFVoGDHc3dy1-Y8_tQ3bEhgUNiZyVVfsf9yKNsK92QA25W8Eu87sFTu2m0fe-qOhVSj3LSwUtpPF8Czr8T15id3bZjjDzKhZMefsipadTVniH_t9Fhkgddb8Psn11c3dDOucLm7mYBef1VnqRwDlhstlCoA_K3EJ7LHSAt-q3BTJ3o5nnDgRVrYnfUhkVvj3lwnmSjjIm6qRZymGaY_ZJMXBXVD5blzSUxcAg-X2OR7b31468NbH976-KtbH_dnajpkKsp_OM5D9DFSpp-EealNiiiL8jxM8rwUYVNUMKZSRqAAItC3Mm9kHrdtVSbVohWgE6oyappFXiLwps3SO97nFvFSdBbmZ4vFEeKlqm6rNs4rT7zkiZf-XRAvVRnsVRlm8cJ0TXIMBrVGjzjndUl_3DZ1IjMhbP2Zc_TfYhB4yPGtw8d11OZJnCza2IiZc6I7wKzHnsrYQFgEiwUWvDvV-luqxnWq57ViJ8zpCHkhgrhIfvzLPydRBvdw6kedSvXznTlHqLfAMAapbvtrUz5vgZhq8TX8aNdfSnRCnmGyhlF_W91gUzFh6G9q-gyBcil3qnGLLk83RrjKxVYgeVfU_hp33aNzHlPQPVnlVQarFtpldGweZxkfa7eotm9WEay6Zk2IHerCe6WrjrGL0pzKz7a6XSNXxrAfMacOvLb7ru2ZY-oAdwZQxWXgFtPOlavc54frHJAHoOqxPI9nettdYpvvFnEyoC_mOF3YjWMrL3E3b41GgoWUXAiimtQ4KIBdj7CR106fJjSfGJGJAWuOUyOfhtu8D7y7G9IrttP61IKlslwsorJN4oUlcTD2nwPPeKwN16t8gHLjlEcNckdwP1avOjeDcfz9YDw4bINPmTvqrWzRgLpd1ZXq2ERtO5CixxaNq23cIdQXPUbOGYglnIncA4aCG1zjeG6j9orohlhexrp44EyTKZ0Cnb6Fd5y_o_7M-usdVmZik3Ksa5zCSRZ1XbZ5usgqA3F1LNoxS9jjrFIiOFPETzZFbNpEiA8drSBqImo6w_WwhAFGNWUpNg6VnL4ts9SM7ExU7Eq4ie5Lp3FBefXLJbbT0kEOJlJAbSItGFn1eKR9rvYu6EsCmrH-tYWxWLrHxW2WCwgTVDwNd8Za8LlxGf7P_1IkCVLqYDdvLnFWqtRym9naHL1Xbxf0UH0C6F7Ryjk48EIRp1ho2VTvhki0As7tKraF2I67MFaVjzL5ybB5zo1WsHneZ6_yV-Wr5xezMTnIhepIezEz4oOzS9-IoqhY5PgN0zDX_C1L8qT44kIVyatbvVy8LF6FF9bkIqvpVAHSVO9IrI2CXQ2n8A0-I1-EcXxxctC30VhETh_MUY2RKdQcB7WOtnM8htfQT9BxMupq4OktPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6y0-it7xFX_n_Y3LLT-El0un2vxJZzz1u_yksO87t19QDAifmD0-48TV8yPX4IAJ_eMINr-GzlH7lvtXwa_jkT3-6F7ffbWY89-nMrvacG7FRV3TVYd30lHIamrPZMYxsISrE2EnG-6k0QDd2Adi8sI3ZlUrVqb6PUc7dHu45dtSXjcWjYsd20r0UIOHe-6N4s1N9yPEFp5CfolIfYaO7PYZvFcBDt30FBULxH6dvuq6soibYdixuW1-n1w3qJRXGxMHusD3EcAeBHa_XjV0t-Cu2SVweXTZergHxlL3uJu2M7fjQjizS_Tnpiqqoq1LEYZkmUVK0cbxIRFVHd3HSGW6jj3PSeaXxkyuN-xMKGgorM5az-IfjJFU_CytXWURtJNO0TdswiasmKyuBIOa2CcOwTvMky0QsmhQkMC-SOk2ropECbtrEZQnO_N2vdISYa1GcRcURYq5i0UqQceGJuTwxlyfm8sRcnpjLEnNlYViURRg2-d3EXMfERDQ9uoOcENZ2jLFtPscI_aQRisRdiuZiJAPkSmpUp5POciAbTiLZWU3FtzWMiKFNFvKYBXWG7ShW2sTD0o15tcT6RLL2dIHWdjXiC3NJUqjp4e2msYcMYQ7AV3WR5d6zh4X0tuZ5sj5evz51nB3zgK1BCjE_sh61xPt8YOokonRRpu8M4wmqTcWMmzwa85zc8RGXmNWYnjPs3xtnWJqCaVM3clGUtecMc1Epds8fOpPqeICJVoiImtsH_S0Th-VFGkehKDMZh3cThx098bX-gL2DuXzTGV3pClIyew39tLPKDjCXe2uykQvV-fBCgTgcFjGsO7lQjQxvUYddqOZyF2wpYoMzakGIrY04KHChmvmpZkfukl6o7n7_9mRhTm2NpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGXYv2PKsOO0Wc6T7uSAeqmEYIlI9VW3U3RQhozJ6caAZs5dhAVuBcydDfRVwxzdv32AQd1BDvUV7iUT4scciIpCmnEpIijbcNxIM7u1pssFaecHMT_lSZlHIq3auIjzsEHrV-YZdeQ4yvxkyHP-bZif_vQQ6qojVEHRD8eZgH4W9qMG429hWMqqrNsyzsKojgTMf5WHadHWcVhEeRMXTRTVVZU2lRBNUiSpjBdliIxId7_ScfajND7CftQ0eVTX9cKzH3n2I89-5NmPPPuRkcRYFHnd1GGblv9fYD_6bjQcx7Yxmc97Gi9zNF4CbecLz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSn8L3Ep3sSrdxad0J5PStz8ThxIsR_sWBFRu_xoESg5diSXRuT9VyscZdWb2WQ5nxU9G2DP76_IBObd3ukra29ten_e_kdMv8NY4DxoR3v-mTte_R9_UnJX6pk5Htp9upE5TMHvTI53T7j9Mp-eNveOd3YAesuKmIM_ed1Tgd_8xOhU6D73X7RksE9FUYTO61xtQRrI5dNGpbgENWfsA0TR0d6VMlbXz8a8fsYP0gCIBclJV6U81oDupbC6uZXVKfzkdtvWpPXlO990p3vZkNzFvcV6GadYUP9Uw1VdpPMMZloqdcpHbyW74cMHhB_xMYP6fPlIpdzA4JoZZVE2ep0n9U84mm_fkEwyT5RK3kHjD1Iw6ULZHDPUe28ZJpNgH3JECu_8GctxuR2H0Hx_ZcWpA5wy9kxrwdxsuKaegjVGfv3vNoFOFi6HKabR5wdyhaDV7lZSSM4fWyV1n6s_-7PtQIv61nu2cxj_7s50D_Gd_tnPO_-zPdsyBn_3ZjtXw8z_b2hf_BnJubJCf_dmOzfKzP9s5WX72ZzuHzs-_x-zR9PPLubUrD4wJ9eAXzCo08AFvCa7YAqKesL_ZX0o65jldxmbHVi4lVrdzgcVdpuPP9kzHDvzZnukYdX_dZx5jAD5fkitk4D1jGhaKO4J5vZ0zTNeVKJdabvx4NVAexakKzFiD_EEkwYnM0raMwzqr8zzM8rbKZVtS-6OjJMGGY_bjJME-vuHjGz6-4eMbPr7h4xs-vnGP-MbB0ZwnZR6JtGrjIs7DBhEWMs-o67PhiuclOUtmLmt88sNxVnjMvBBmAB-AfYSwx-bM_PhW5X_0CJZvU1HHbdpkGfYelHUo47aokhxfDhu9vgWzCZYeuWB29I2his6KMEmTPM1lVEqZiDDKm7Bu0jJNC9HmcKMkXuRJKKOoqduyKotMJEncVC18qcrpQPj42-Gfnxgan_i7MD1L0rOo-LswPKMEsH19GRaVWNT5E3dSvv_J0kZcS0h2j8aT5yXMWtHKIjaAUSHTAowrt2l-cH9LiLO7vM-my2OKAl63jdsot5xE1gozBQCq4PUXZgYXvzzj_uvKStXwCGWtXu47har85tvgsygM7Q5ULepG_tD8Lut1pk1XDRF0rNbZ2LI2VNvaoHqmqmwIsyA0Z-2BJrBt4RGyoKoZGrlZ9jcrlQhH9m1U_wo2Y75CLVXopRG0wbAvKsK_UZzIBwAR1T3WpV8QbsmPAYZoxJvFtDA9EJ9CX_3-Gw2CHmyJ_ylRThAdFLfBnyQ3r7I0lKAd4oXpYprlhYyq3MFC_OH09E9nwWfBL_rqjGEpc3MCzt8vfjnRYitumxr8BCFsPwiQqEI0YXiM0etOg3iqrqvK6yJq4jIzDDaOSe8UShw9u4UuRB5RrNs-eu1WIKGHCBYLbEDldM_aUnccp5uVbudLNWAjJLQI4iL58S__nEQZ3OMYEfNJcL4z_NDU62sYF41t-2vTzsoWRin50OUAu_5SYl-FZwie4iqcrW54r5jpLPEztxERKJJypxop6nZR3PemNnRYFcjlFdHRICTiYxgkAh8hDmlC8mKZp1m-aOuwMSgcx1Wa8JNE02-U7jAFjoarx27_zxFw6uLLqLndTnIPFSytQk4Z7vqMwA1Hp3715vy2NukO1NWXGp1DSJYKnHk8A6cp7Vuny5DbHZJ4OOo9FczIyQYYDA9nmXKA49yrxwqTbhB42J6Zt8AGkRrcv-_ZkeaQpgv0iNfUaCcFS-S-8ooShEqqVSe5E5iaEUrFglVV97AV0cvzqqiWfZpzse43eHSZUizdRdCz3nvWe89671nvPeu9Z733rPee9d6z3nvWe89671nv_6ZY76OmBvmNRZNan_evxXqvKO2dzlEGmh_YCJEnsf_bIbGvGyGTWKQZOF7TJPa6aYINEzphq26SmV7USZwkTV1G0aOZ6Z2-Ohhf6B02c2w8aYTvb4yY3vPL_9X55Vu5EFGWZWlh--kc45dXW9yQZiOnH9qv5q20P-70BrJ5CW2dvjYdaTjm2446jtjNQ_yFziHsyed_IvL5epHGZVVUYbZof27y-XMsUK9hV2HPHjjelx31YkdbbaZIfLAPh6F4edfV74jyBrfhlvm7FTUMHigOC6Al3IAtKecYGW4U5Q-7EhS5eMb71FIR2awX5peoa8tODO8M54Dnqfc89Z6n3vPU_2w89QVY7SIEHZ3W2b8ZT_1Omjg69Thyqdt0EmvUf82hGHPVp24Xrdtymx76GF0iLiqnqeRAdPa0Fai5QYekVfs1-AYkV0ZTI1027la1tz23vee299z2ntvec9t7bnvPbe-57T23vee299z2ntvec9t7bvt__9z2YdEuoigM66RKprntvz4AkRLh9nyOodS58c8vgl_czWd_ynzSv5zh93BIc7zbRRCdFHkKh5OOwAZpGDIya85ISbhiMeZ8p-m3UYGWeaZvHV-aLEXvswYu7i8dQjRF4EZkWWp2BvfF9h280W2srPMKA98b3sJ9g-z2G6SWuf0B8FpivD4YkX04ckFfBAfTNwQJsRQfmUUmec-QpASZ2u1UkU2nUHd4APYYvR3g8GCosp1pE9RUeVPqDstgWJNz0WyUNratXv0rvY0IBEJh9DtfDbccvNpYMJJj0wqnkKuxbfAeFANBCrcYNq9pwz9X9GPyA3FGXQZUD8eAGbd5XUR8yzhJc87D4fooj5p9f3RrlcTQdGkqKQHe7guHuv69IbMnIsJDyvqD2BS5sJrLldofD2S9aomlDJZzeikqM5cScoYYHpU-HFSUXCtEg9X-AmkyYWL-jB0DKQhC5XW1QFjIKNq6JzqDZyyIGigBz2N8MvIZjdijExSxPHWYyDEyTGs2EY4VebNIctg0ojJBR6dIdcyP3C-V5WFo_Yz1YYn-THWjrh_CjA_tdQQOKDApdpW-s4jTJqVP6mG4UMjAZhTd4AIjyvJsxWoznChrCM1tVd1zx87BxdOaklbQ7DW1e7Q9jmlzLXv20OAutHBkKhzBUZ3CVKhkMCp1N3WyhGUWV6D4ZZKY2EaSiTRrxRjB8KW46ffTGcu8KWRcNG0V2ubOhRBhJVIxPlVeqU75bP4RZxz1zD8kiVehrpUASduvuFYGo24gNIq_F3UhyRnOEF7AAJl1kIeONNo0HdNZOxAJrDg1B_2RatRDa3StPWf666iO1WSbR_xy6h045IqZdqacN5VEB698yD3PFhu40MhAnySkoFTY1iE_IhI7hz_OeQldSGSGyubrEqUaTfO17n3MVD8KpceDNDAAjhcdji2mEydG6ni3IAW5zEEHt2TdbUljw5eZ6uqlO2HHuuXTH263ume6QmxnDFO2ID2NzNbbrnFUKCYeVSkHdmteUa7RFjo52BWzRMRHAQcIvi_lag80W4Evp7JjZqm4suWA3Bvfm8y-gx6wmyuXmVbNnClsmCqENvXPiiDwme04zhEEHIfuwc2Sbd4LgUzSQkbp1EHTFMmnDH0y2aXILLnUYOuamGNdnrjhsN-zzlEjZ1NPmxgOP8wK7zecIWW8wFSD5zxPCxE2bZ5bCE2RpnV8m3_qWzXlX9O-1Rr_aweFhDPl8AjR7xoc7e5KvZtxvxAY9ljLdjZviEtk1RP2YUeVf8pVM7x9W8mKxAInxPaSFP2Ers2Ssq0wCVAUJvaL_DN10uQjXfuScrA45v8ANttmdzXd_j6O4jJMw7QOIwtCy-NMZnfg0BkagSBjVcp0EvwGtvXSqVijYPIpxVG5PlBTznOo7JrsnAAJHyviVTClTA4rBeEFuDJqUAYLcZzc2jozU_o4p-I2635bKnpb2qORPzWzuxL7NTK7U2hEQ43ZlmIo-dxw3tBbGVPqklx9Yn0ac75SaM70uTd1QXYwRH9DLzZVrJYIsOEyMMgrk22uWliXReXUw_4Wn2CCAg7cAum2ieCTfGPilgHzctmb5Df10sELaJANuF1rsgUQFIrBRrwV5hGHJeuKURhCg7Hpuzh7yGMMYrxQ56oOISliKw2N3FIdXDNnOljURybjNpG-S9sGbLoc_jECGpWZTLP8VohJF5iipffCFHrqff9Gg90DLmilNBVlE5itU1dbss6gLTobGd-KI24pbtBGBUviEO4ASl8iquZGY2_GgSEDSZoChUYyb1Mh6tTWQRdVkrVNNIaDvbkCcZxOF8koWqTZoozqrLRZwyqP4tgB1DKNEo5eKfYDY9BhMDYcuxZWAS9KmBE-ZHM40QsQAnzRjnatJYpdN4bJ2aGBmAVRqNjutb1wB9k0XLlQV1pqIbZdCGqF9tl-pxwHwYhvjm_yO7R7UCiEQ7E5fdcJ4twzqoG50Qxm0xrA4FQwVII_kodtKKPclvRUYdpIByDyfMxPjxuVS_yQKXTQBJbwN5h9XFPEEyxR8Zoid3gxdKgoeXzdDVgTEYhV1V3u-_1g-SmPlwXr5yrKLSKIUrWhxqBS3yTzwfka3LRXcL_b3KBnuKg3BDHD0hqXe5LD66O_OLQPloqABc0yVjllDveBj0eRyKsiwrSwmf40KbNI1uWhovi9KoO_VfTxHZu_axXpAQGF5Wc5XJN1Y7N5yFOmsuKGD0FF9kj_CXwLTZHVoJ0j1OvhSh_nUlXTc2CEd8OjKBxucaJNAgwKWci0TJpFbmOEcZuLODzIUpsOcJP40zxO26oUTZra48u2fXJoOB7VuElDshJRRGFWZbHFzjq9nD7W0eEe3ZioD5ITP3QrgCl-q4ojXmsjV11LpN6gKC_-1yvdl-QUTpZ6dxH83ehDZFiYEzEw_X6Bp1T_DkMWrAwHrEDhMjemcwfn5MwUkWv_gr4SnWSG9ZLABCNCCe7sd9U1DaJo8OhjnUbsE7K-WsM3LpUrxME5HWUWS6Jl4XyJ4mbAANoW6RRX4H69-C0RcqE3wcBS8jq_3CPE4tR2FSTw7I3qS6InaAQ3vuydhCO3QUFihJ1T8qwyKjT3Kqz_EcM5lnkWRWWaSdu5xOmkNW769KheWBQxVAGiZ3TZqm-wrwGfXHw5Vc1xMBneoicz4VT3FCACQfiqSlobcjv7Tc0aCKZNV6ueGvj7N3j-wbIvuw1bO2DXNTC7iqmJWYsMrTc8Qp2Oc6aetg9QpzH1llCnvj6Q1ekvkWaXSwkuDiJdpiawMwku26vUwStj1JN83T3HWmHuJcOpBpdnBOwHytBRLAb1LGoxDPy7hCbkM9JLGm4RXoIpWRACbOi8qqtyYa0r067MURif0nCMUaakyddjA10TKJpUkBP4oBJYGzXhBEOvCqwJlLU2JJGWBfxZgLBcjlkQ2Y-2xalHjS6H1UXLhJFsGvJ1jYdDQc1K7OorXBt8ecSvSqy65v3wOczAsrtUYmrJeakjRyAq9CfYEyJk6vjyE8UC3XYfbKGpYQzTbDEnwe-55ZLpAnHKPQ1mNkYhVBIV0dIOWsBIPiwRteHgdxVLE99SgGBVAIxw1n6nGZ6pIPCZptEdn0IKN0NtY_rLtu-VkaK7OzltmDiNsbyZrPgWizJvs7qVluPV9p9zApxvrFWKkRdtNTuAVU4w7Af9Fipi_QVpJ0bLg2lwqitUYMXIpHo2pnbutyMm3CM9Ap5pe-PUYCEI69DYJLxykI5Z7DbicYshVNtFqjGGzcObgpzjOHGNv0dmXfjAnZ5uTSEIbpJxQjlE_d4WCkX-sIUMbbXdyb-qXD8_4-W4yBwfZemnmWFPBYr2a5VTEW7tQfBmv8K2LH_mGIBi6huFCgbXuSIGJcO9RsG69U7JKFW50_GLdqRDG_ZyHHoAnwHHiRdgGStZgSqIZ86AmYWnoD1Bdq5WOv-4713RpypmXZat8J9LhBVs0dPS6fdblIMq3qq6gjCSdD3siHq65VgCE-QqGDvHA7CZFFbFqpTnkXIOCvXzYJyYneOw0hTOjoK0jOvakbSgxTaMEVVuBquhVB9MGhlKd5R3Oz0WLMPZOHxP3umZZnukk-1gbON7a1id1Sx7MpTgZ-VrmHSjrgM8vcXOe-pQ-uro7-CE9w_w29Z70bGhvhpAc2jdwqrxxFZBDoNTHcn8yQpecbthjHLfaKyqZFh3mdGV1DPztdmdLOVoZ1J9txJDJA1v5nSKKhPnhOr16YQI4NrBpRhTzRBQ4B0cEXX2W-t2EOr9dO7A-L-W45Z1zXonbAm-26lF6VrrI-CMOr0wvtCOm-MVT3pwXCA7YuFzcnYq2EzSKvZwonMXpL0TZtYQIJetDyP4A5YirLT9utU6lfmIA16UM4ehdLDd06wOaToQtd3MqhA37A-LcnlFnOOEeuPueLCRjFgj4lqFlPbDzmYmDguEUWwUKznrHQk2xJoc6IkUQYUV1JmMse2M6dxRyLqtogMOSDZNFKutbTr0kTaCcQGubFI1rQVhJ2Vay0Xolp7qMBQpgm5gvUfWHi8GBf7xTTQ8gLxA6rC0ljvqCcI2Otj-7O0pfWs6_Vlx-FwR6jqG4YnKmZk5Z9ZV-A5I-KW0jdOOFc49U9zCuObUPYHYUaXTJGB-OwR0PKQxVTeUpqVcNHkZZSbWKcoqy-PYqcwgjnWOyFrOWApE644KZGQzEfKeqBOGcc87G7NR0bVGEy7aSp6ZPlmsencypE53QNtTyKhip4zdht8QKaP6pIxJepUZSqrVNKyh2gOzEPxVa6UZHXerI4h9iPyAh7yzvx12bpvk1Crr2ThEh-kp7Xm7Qor6RNvqDrvrVLlDU8dF2cZSFKENJOXZIrudnhvvPh2CUw1VSdKpMeWgA8aEbAAj-BrDLD_-5V-vwaOkbg2IPxo1DtI9ZH7141_-K6YauWaHDUsHQ8kt4EgZk_Vm4EjqnLBTqEL_1Q3sM4VUwjkH4dk6Wl6N02wtHabhDPhUtidOxSJN4zSy5exh1SR5Wcqxxrqjd_Td6iqKZRTF4HmUiSXETfNiEabVQTMI0zjNtYvYYbOyeTr2IdAF1kLlouYHhavWR5yFUOsuKsNIg3H2FxFS6tDnvboxuGqlTgkIaTzQoSMcKCJmdFW-Misa10Q8Cb6m83rtDFX7Rs4QqMMBcbM-QInlUSxEVKZtXZnIqdP1WzPIk3uMdrINECuCUrSf4QVI-TjliToGdEasqPhJs-fYI1qFlamAI6dfCeWp3G5VVkMaLCCZgtaQI69noONEbQiwEPf8bNP_a8R2reeAQwPsaY7DUcrUMH0SqZjq0Cy1qkrd4ysMkr1RPZbIrIOVWWHHVuvTY_DnmQo0aPPuoP1RpXBp5DBuV9iMjKoyMRxAkte27GiyssY7UpBSrDFMZbQBhTS5spbFyyL4r7HyEM28PfgzgqAXOo7JX6BjAg2ljSB8fWfbg2J6GldrR7FTcK1lQ1Ku68JtWSWHqFl8qaMaVe-ejCN9KiBFIRD3KQgAWorNgNvrNyroB04M2OU3g114VTK8PVUe4Pb0H_agtk7JiTk1rY2Ulddh01eSM3yYsvx0xwacSzoUiIwWbRTXj1Gs8dYtmlHDHnLyvvyK0Po6LcevLRy_gmxawyU_kfBJm1pkTVMkuW0KUSMmokiOKk18HEUOvlEdL6aREdEiLZN8kUdt6TTmCLNFIcfxmuck4azfzjSHt24STbk9UzHAFNrkSZN9zJ0Yg2_gnAWLr5kvYasvzZaBFVbWr15dF24yqENG4xP0AY7RejqlNXiYEOLkXNvRjUakemGOOlGrBKEKReGmgf1HzONw8p7b1BJhoOQMD1r4w7da1P7Hf7-df6KLsHEEXjf0S1DrJ_ARD5P8Iy6PY5-Sg5VcKje4WsLB3Op3Ey3YVKp7PNmLQsUqnVYSHHLAyBbX4FHjNR1P0o5rJejpqkWJDrcyvnCuQHbq5OOzzjEzhd7waoYZr2J7o_KJ5mY4bUOLNRVM9us512FaB54rfVTsBZtYgkNLca5D9aqu1YG1WxG3g8T5iTIhaIL4HvYgMvrVHjTofOiDCPx9yX0TVD5a-dkmbXG3a1aESRW3oqpkbsxDmZVxm8p4vGd_33dqwb9U_QWnE45F2shYtHVmS2PjMJQyKttxc2dVbj1vCd-t_DBUXsNZwD7wzBjxs6MoQ9vR_JybFx2sxUytH_6X_Afb-lwZu7yit4GKBv0EChxt4n57mBilgZqtSOuBZlZLmeFq5lr9YnmJIdWrlYI14f7iUiXQMYjjx3TU5bpHQSXcD70BNZJCS4hjzNyLSmCLdCWtT58-O2hMpUZx_s1rVc4zail1waB0rdgvyAS7mCruBv9agu8eNYWwjTerHCwqB5L2ErYkYsd0RzoOJ4x6Uf7uNaZGufj9-ZevER6y2SuQl9aa44g1tix12qxiiEdsrKV0cU493edaIi9mvKefoxU-SJ0pZleUHHJJ-wxdKSfRaducg1shKaVF-RtH6qZk7SEiBQ9QcU2qukC3Vb85llCrCi5B7r0a8aDqlI2FOolXipAxJoIJExa2XYWwdLnb3Ru7ovSf851f9OvPdx87eqNFnRdFW8TmZG9aeEojo7GWINKbu29URlXYRnHTlrZUySHPcc7wF70T8cIXPwbwpCCW4zCATjxsRQsfjd19-OBWgFwdOvhI6u10Z__Q4518lHWlyEVUpvegL6_JsGk7ynkmFQuaKJIDxrLxFSrzqVSndElYXdtY_UhUxJwB2BaR-2uqytPRMcuTzC6JsHapHbZ1gPAMYrHURdhLJfBLLfAjL-WWy-Y8con12SORVtUQGpzpUK6owAhvGHwTt0cV9bTg6LGhXrm1muO-cE61gGqqdS9CDJMIQvYHjBdN0LZwZkh1IcZA6Xq_cUeFHVK4lrI5c8M43FaYij2opt6ELA9A2w5ai0ckmhsDyaBY21LsGVBFiYCrfolo8gkMdxWJLA_zOC5tTCKUYZgk6eH-BmUxucVbWYV5FLa1EIWNb6RNnrjEMTwXcC_M4mEnHqdT9oBp6H59s-r3BmJvI3Nutk3fgQw8pEjQeTPYB4gUJoSe2VLqNNBBoKWmAZHXB7cjF_4xCK-D9ICNQ-GquGF_0zQKvgTH9MHzSR9YX003htPqx2ZiZyom6iZ7nW43TmUu5vlGncUOp_92H6BRa7JbnYButSobrwZ3Uptux6ZTtHc1ihvfkQwBvKNtfMAx4-Zoj0G4tem5p1ee2utiedDmqt8ePKLCOV-O6U90x29MYw6I6kFjDU0p7PxNo5UbIvWBFXXestZtzRk8c_AgpbxXPRFh7WmwBnbhtOHGMLMB0hgIre4E7PhciphPAcFuMcz9AP__fwGezNju)
