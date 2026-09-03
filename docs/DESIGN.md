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
Shared owners: `ui/button.tsx` and `ui/badge.tsx` consume palette tokens; `ui/modal-surface.tsx` owns dialog geometry/accessibility; `review-feedback.tsx` owns DecisionNotice, RevisionPanel, clipboard handoff, and history identity; `ledger-overview.tsx` owns the bounded workspace support graph; `lineage-graph.tsx` owns focused nodes, curves, and source expansion; `governance.css` owns their visual rules and typography roles. Reuse or extend these components rather than copying page-specific markup and hardcoded tokens.

[//]: # (ob:8bd7754c)
The Ledger starts with a workspace evidence-to-conclusion graph including recorded lifecycle states, with six conclusions and twelve sources initially, scope filtering, shared-source highlighting, and incremental expansion. Selecting a conclusion opens focused provenance with at most three initial sources. A reuse-boundary node must add recorded scope, authorizer, or exclusion reasons rather than repeat a status badge. Current knowledge remains a separate eligible-only projection: showing rejected or revision history in the graph never admits it. The signed-in owner's eligibility is not a claim about every agent's eligibility. Local fixtures are visibly synthetic. Validate desktop/mobile, keyboard access, long content, clipboard denial, and real receipt states before promoting the build; record implementation, internal dogfood, and partner evidence separately.

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
Every mutation must produce immediate, consistent feedback: prevent duplicate submission, show loading/error state, and project the recorded result through queue, conclusion, history, and context. Review separates Needs review, Needs revision, and Decision history; deep links select the matching group and switching groups clears an unrelated inspector. The shared DecisionNotice appears at the top. Request changes opens the shared ModalSurface and attempts clipboard copy; claim success only after the browser confirms it. If denied, offer explicit copy or manual selection. No agent is notified or awakened automatically. The agent receives pasted instructions, submits a linked new proposal, and the owner reviews it again. RevisionPanel shows the requested change, one copy action, and actual revised proposals only; long instructions appear only for manual-copy fallback. History displays recorded proposer/verifier/judge/model/reviewer identities; missing identity is explicitly unknown. Deterministic policy evaluation, optional LM advice, and owner admission remain separate.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2QwZDM3MjMwYTVmODdkNzA3YTMzOTc2NiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImUxZjM2NTkzIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8wYzY1MjJhMWRiYmRjMDg5Y2ZhNWVhZjgiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzVhYzNmNWQ2NmJlY2FlYzBlM2Y4YjQ3YyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtveuO3EiWJvgqhBKYrFK7R5DOewiL2khdqoTOG6Ssml1UJRRG0hjBlrvT2-kuKSo7gfq1DzDdwPzpwQCzwD7BLub_zJvkE-wj7LnYjR4eVCiUqerqtUJlZoQHnTSaHTt2Lt853w8PxHbXtaLeveqaB2cPNptXTdjE-SIORdoWeZOHuYjjMs-yB7MHVd9cv2q6Szns4NrhSizS7KwpmqzKmnRRJqKo87aomjwOSyHbom6SZNFGZZjUcQ33yquiqmWblHBRKhdVEYZ5A_dtuqHu38jt9YOzH_CX3auduIQnLMUOHzWDHyq5hA_-ILdd24lqKYOtfNMNXb8OruD6fnsdVNfBt9u-bzdbOQzwnY2oX4tLiS81-njb_4OE191v8YZXu91mODs9vex2V_vqpO5Xp_WVXK-69eVOrC-LODwdfXsr_3Hfwc-v9oPcvqr79SDXMBe77V7-OHtwJQVOoozaOEvL-AF_8kq-oYtgcuWrsM7SxUJETVU1dViUdStSKdoCR9Zvd_hqr5bdWsLI9YosX6Wijtu0ybJK1kLWoYxhApO85tdRo3tVi82wX8ILL3Ccdb9thgdnf_zhgXr8Dw9glfvtgD_xn2XzqoIp_-OD_fr1un-7fvA9vIOWB3h009fD6ZOnL5__9uuTFa7Th8iK2O22XbXfwRK9qsTQDSgxctm-EgNM3U7S_fa7q36LA3rdrfGWw_Wwkyv4y1qscOX0wGbw1QFX-8HZer9cwjDrK1geyS9YLfv6NVwtZFqEWY5Ph5XZyXf4ElYmgidy6C7XwUt6SPDTX_4lYHmSTfD38Bj4mhqGaBoa3waFTL6FTz4L7n6fpWwuZfAl_nsLN9ldb_BVUBJAqh78OLMDTlIUk0z-AgN--PDlTuz2Q_CrRbjI5mE5D6Nfnz18GDzeb7cgD0G97Ydh3sFTt7CkMrjcd41Yww9tbwe9EVsxGnGZF3mW5-MRfwNblx47NYGfBc5lE3MiF1G7qNLmg5_wfB30axlsrrZikGfBw4ci2IiN3M7FuoH3fB3QumwfPjwJztVf6n7Zb2Eyh4k3zioRVkUeffB4nHU0szwEK_Fa0jirfr9uBOitpbzsYNefBfDFRuIKiPXEeGqRgu4QH74C313JoGGB4m0WdEPwtt--bpf92_la7ndbscS5gQGJZQCKpdnXOxjwdTAlEaJKFjKL6g8ez8OHOKLvtvthF3yhJ-MFKLATkNLzYNizXK7w72vQYdugW22W18HuSuwmxgNnTxIv6ng0nmdSLlHQpgXUXjUhnxVoaymKD76_Iw7DVb9fNkELXwqWHciDYGkI3vTL_UoGb-Ewgs_qawFLJcXybOJ103jRlEmbf-hwcO6vehCDJgAFC5OLkjBscMZBLEQAf3krts3nA8rM6wBPZ5p53EVTuwUMgShdNB86nCd9sO53Qb_Zdavuz6iEtsGfHiz7_vWgpwj1WHD-XAvmyZ8eBN-oy6cGJNqkLtPx9v2d--L11bZfyfeIxvFvTIhJK0pRZk38Mc-9sUbPz3Fx2m3_Z7kOxBD0bWC1-0mgJnHYV7vtxJQkLUheW5QfM7Q56NffwTWwVfFY6rcdnCkCD3vQXk1wDiLjCDz8bXv9iAYngr__9rkd3BKMt9HgwixMQzB0PmZw582q2-FM7WACl10r6-saLEYQ4Qr02wYE6I3Uf6Z7zvmeAZiZE_MWJ7EomuSjROmcFpSU6mspNwHO4ZEZOwm-g-ukVoKwIbcymBhaCOZ1KtJiNLTz5_OdXC5hA6-vaZ6nRfzI5RPynYdlLuusvfcTQbjhBTdgJsrtWp2Ljsjg1uedfylharsat_7QtzvQSlP7HU6juo4ObMAPGdccrC4wjkGWQUgut_DmIL3DLLiEUxL_Debrqt9uwOtYzUDuA7HfwtVBBd7G5YRcw4lRgR0xHpey7-ptt4MXBLnc9WCSvGedbv3SxGqhnxW1UfKRT_-PV6h34P-XaEHCNzYgpEMAjtgeLAY8QWbBdr_Gs4tvKi5FtwZ5H-ophQRHainyKv7I0YFBIWAzwlJs0YT4j3TI7mCh4DDrYPWtSLmmWUtqYGp0ZSwTcLk-fnRk6qjRPcZphIFt0Y3ZBpsebMRg19NgalAIYIzv5Ix-lW-mlHnYgMZsqo8e3QvZyi2anwMO7_ewN_HZ1Rat57ZbrngSB1JWu9HBNGWdyKiQyYGWuM_ovtnvNvsdjuzr_aqSaLS3cDXIOWxNKeorbTSBpEm5BguLPJxNMGWs5FHayrCtP3J0dEzvV2I9oxOOVpC-PQOFU4NND2Y2bhxY3WHXb9DEVnffXU2NLkwzcLbGhv5j9FiG92gIc9Gk6xnFedYuPvDu_xR817-Gd_mn4Mvu8moH_30itq_hPygw__Sn9T_N5_PRP_ARO1twzWd2SBToOFCQIMhZ-6Gvi5O_FPs1SABJ6VauUOWAJKzFVmnxrRbtWVDteYF6GJGY2vRplUe1aD9wNOzToOcNz_oahOEL3D_Gq_ktyibtIBTgul-t9uuuhouDnZxSkBL-t0jC9B5z03bvcK-I5RJPKDhmNxsQBbKvf9vtfrevgm9f0EjwlEOj6OL__a__8v8Eq765mBhQm5RNlS_G0vPd9aaHA3Nzdf0e-RxdOCGjaVwVdSySezwF7dMnfb3H1wrUvQcMf7zs15e7Lnj5ODjFBeqDlxhRwd9JgfxW9tuJU7zI8zIPD06qu42IRUOPaQYGHojCcxN-MSICA7jsRHAJgjuw-g2mNGySiTRrxdgo_VJc9_v32XvmookVKIQIK5GKD7w7zv4zeNNBNgF_iFM_wN0pcEvPAaEDZ3et9fZKvOtW-1Xwdso3KNK0jsviA0fDM_9CPfabbQPKSE_3N47j8tP_8Z-UTdOZ34f9ZjMx-02cJXXSjL3vp0v5hu_4H8BY25CSn1qIY9dPrEkm8jiTWXT_Z7rmD7iTS_Dqq2s4q1qxX-5Ogt-JboshaDDllhKOV1Lfp7XYosqa0pktDGxRhfcf2Nd9Az6PXMqavoFeEsgQSMfubT_fktBgTKRF0QquxLIn6YHlB89rYmBRmck0y9v7D4xFiEO6rNifiOGq6nFOtCi93G339W4PjhqoU0lu-irAG94-sKIC26iJxgL98grm-31HvLloSn1KOMPiuPnAu7_g1AHYnnhGo3ml45Lb_i38ihpp6PdbjM3B0bXtwPTnUzfYTsZRK7BTZfaBo3ncr9eS8hbkA6MgbOBIW6LneDWw9lj38DcYHE7CEOzXS5TsppsaTZqUWSTr8gNHw3Lwh27AiO3NqCX-sdYDRusPbOY1C9m6nzxO4zYXcXhwvq82_RqP5feae86FU07gosibLC7v8RRU6CqfUF91G9TmIOQbgfHhft1z3JCSdGDdYvQFXIPTmjMNEwq9LmTdVtHYrvmyr0GivuQcGHhxKiw5PQlwnN36tSkrOCnTWi7Cjx3AeaBydgF-QBHUNez9YQOSQNnKHfl-KLMzFQZrwRacgxm2moqtl1WWx3H1scN7vOzq16g-wep7La9Jb81h8TrUgPAxGMuoedtuC4Pcb9D1RAsa1P7QTYptni2yw_P4w4entOvoi3pLvZDrhkLPcDCswIqFLRWQscXR6CkbPqyaJC_LsUfxgh7KJnrwFTiO8Lz3idYt35mKjqV5sQjT6qMe_R2HAnp0EZbKjgIPkhdn64QJwJRdSwmqT12DhsvUxAghkzaPso8a3VPM1wervTKeKE3DoXkZdOBONB05QZgih22PZngLY0Qn5Gwy2lKjTVUkx8aGJ8-Trm2Db1XU8I4Ld-x7U3oyrsNsUciPHgJqzceUpw7o3qg2lT1zhbufD7IBzs41RgMobYwPEKBNJrSmzMq4TQ8CUn_ou5q__SU8cI_Ah_dMztFvTExLHIZSRmX7EY_FIIFK38zB60HVw4oRpnI1nIFzhmbFLHiqLI4ZhsmUjE-mRKsc5Dn6iJE9BdekG650VkDZN0v1TXKXf_8cw3UccXr85fOgp5DUbHKnVWHUFHk19p-e9J9zGO1Jv_78vaf7zasn1qhpo1Y0Mjp43vtE4Un_nqWvRJnURf0Bt2UHHAQe_Qy5fUMLf4k-B0ZkEPCz7Ac0lslMhrvWyz3BecAln5D9PJRhmCTpwUhgZt7_jnzRpNZOmzwJww-7Ob8pXAQvuwPnduck8odguAYFfr3q94P2dLfirZav9vBNv59ptM6DN3j49utXNd6SHkl_0dAb-Sot8lKGzSKORNqmVV2noUxFiaMHC4PEUQGKjHFSX8n6NYWaCR9F1hkBavRviKf5HpFIYDBcO3dw0UnOTQj3dE_gEuZyXrUdRr83207ho4YqOityEaWFaMKkieE78H6NSBMwhKKwrOuqygtRRyKrijAXVSkWZQLfKLMiyWUE16NaxEOScE68WmdZ8iNMNCKQTLp08d0iPEvyszT8uzA8ozVXM44KJS6atElTkA776Q8_GzSK5I2hS1fgRqKeyEuYqKKVBZnndA8HzaRE8ecFIalHR4UUcVuWGWxw_WgHl6Qe_TFwoq07bNCcMzAvtq-b_i04jLKW3QbTa9q8UQnP2cigxvQbIhDWspmrnRkoHB8sjfJJd4fZ8vO__-qlSsme4BAIzoJXDBRZwNAOwUlkt8VvqGDbcIWZQvxJY2OCN2CZVvsleHocQHZeh48vbZTBl8ze18f6wKaR9pDBub5cd3-mbYnXW_vo5Mg5otYoTWAXJGkiwtqIh4PE0uLxPoiVuptIqkUERpZsKDFDd3NQV-puHwOn4kWcgQf02nyIt-WFwttiHGdeLfcwCXWN8sPry0gpQct6ErzUlhHdg5Ao9barKJMPkl5bvIFrHD_CJb0mC5lhQ43K58Itb5_iMlssFhn4x5LC7DQpDvTrJjbvgzFdDQbV5ZJEAMPtDQ1pQDOeZBGUKCZOjcFjz0SWun4N0sqaeY7O97ITGNvGxFMgwOcmfCSNBQa3MxsmeK21wUnwfI0OJ08bDGvodrAN8HAe2JvCdNXAU38Fcr-7ckcRVBK-DcY97R_yD3BDcIZSvWUF7w-Cra60J53aohtJKTvaWfoiehWJuxY_nVihBRwckZR1FctEr5ADhtPB-I9AuW0vxRrBRzw88wHN1wyDXTuM_uGLwALBQd73q0d4oIOBI7b11fGbdRRcVdqK0uN8C31gaKgH4UIGHUNkDw8jBY7IwTm56jCjNZy4H4PuYqtV5eFHVqs0pvQxybKK12piK0sD57FIx1G-am03sVbPldy9xaQWPH81sXhgA8epiJs8ritzwFnkoDll7g8JhDcA61y-EUsMvKFD0a1BsYL2wJ16uQVZn2Ge4cgeJBwHvOwlxUKWuJMZmQzrh0417rQats9v9ZbSZ1AF2xzmnnamaHcqTgF_bbvLPSo9O5eXOPHDHpQdOOoTE9XUNahngQa31BPlQBqtqp8EK6qbZWGZZu2iSKQ0s-7gF28qtQ9GJqrc7nW_Zz0G0o7XzAjbIFYb8xcSoplVRrjJ4F7VvluSSkCl85xAW7iVOlpGQgRuEQq-3onlo-Af953c8cdytdld4zZm8YUhuEM3B4B8J1AMKMTFmHd1V0z_qtBXoyP5E6siiyqvRZmLPIv1RDrIS0f33BdTCUfpyW1oMHoVVMhCqXuG2w3uSdfv6Ao7v5XkNIQ-B06Cx7hq2sGFxTNWk3PoztS-EogihN2z2-9YjxhJnpglATs8lkWeFJR04DPUAkKNQ_UxUE-6HEE9ZxhD3VO-heFI8DnPDokbGHFof9CxfLkUpAHf4lzTlKGGhn0NanqNH1-zTttTqPEtqWOlAEDIbn_fuopknMV5ky6szWDxpnav3hk9qm6cVFHTgPvTpnWub-wASm8Ttw-Ah2LkfkcIPG1xn02Yn1lbl1GcRHEsjItgQaRqOB8HCbXb8E9rvBPH29S9WIbJnejWVf-OL_lSGaB0iUo2mHVj5IfZDvyNcwx5w5rq78ABuAdFgkPU55-6EKR9ra5C77TuNmIJZyM443Ca7jr6hW0x9YXR2-lvouvIsU91YszFW4rcLuX29ZEoh7Z0yki2bZvmcWksHQcXq0GNH4FyBR3J-wg2xAD61Vh-j_QJttv2Sz5oCad6gRbPXF_1v_zpAeqD3Z8eXJxQ0ksM-KJoj-LOku82S3B2ZqCwyURcizfdJZkSZDtt4ajUBwsepuBYWWseC6zksKPDwDnn6XForLAVhQppswGrK9j1k1ZHWUZiUYGAm33koHj1RH4EJldNqdjSKUkroZLELNkDaGE09u6gTVIZN1Uo6rIVxi1zcL1Wm9wNqKtlaRE1WSzLEoTK2BMWu2tVyb3BuDRVV2Bl0uuzQ6wdIZIOPqEaCRKK9mWHxie7AQQn5dkHQUWx6THAOqGK4khIcNUQt2fMIwfya1TR_TG8tJJoYJNho_ARJ7jLCawzC34ru4FFsIcX3mrcBC6LdgAGgQg03noWhvYGI9InBuFTwx86ECN7ZMPXB3Bfld9CN2FDBa5SW3KgkaC-3HWUnAfzYvua0BpGgQ40uBWaw_Uwxz0-xwWcg62MgTpUkgMJOd3rJd1Aon9z2dXzt7Ca9P2f_vX_wusQmQPeEBwlVoYDZ8dwPoNSc-pK8gUO1f2uv7xcwrt1o12N5iJcT5rsVKksZTrqVDOvz1HnhYZPkDpUDDzqnvC0ASGPUMNZ339mZJes8IFnSblMb0AFSXgzVuZPUEOBDqfXd7eBUbLoXlDcg-BCcAOy7x4-NMPEsAjdBuwwcCgucQaCRoG_BqUdxo4WPfxxv1HuDIWSh4N5nPRgMEAzDISSwRAtDd9YbXhzyq3iHAWP4Qm__fY7pb7OYE-2YCbj7FJSlSVXSfMMh1e_hgmVBJlBlc1SpndWsEFkMI2BfB-OBYDkYmQHjDPaC1Z8aC-t0HmkFWG9T2vRyN79TAzGpf798xPlF6pY261BNY0IUvdBJ2y36ocNbFV5cvuZ2-R1JMomBG_JhEEdzL7Vvh8Cv9feQ5OGcJSnIgmN9-Ag8tW9PwZcryDP7IoaS2-jwK6IOqYvgfj3GGNzMMr4IDCBJs6lMK8zIat4kcjacSI1Yt-67vcG3y_7yz4AHw439xvEdv-GtS8FEGcmXkhOy8zoT9zeRnfORlqzZUkkhTlzECr4ORVMg3nRoi6qaZgVqjDnZDNu2wyvaUW3nPLYo2qRx4uwqMrWzo-tGbDzc2_4v47g0B9xaw_8s2hAOLD0_VAZmHA4-UPaaiOblELcUrKOocAFrQCsHc0z2VnDb3B6bmqeS4Iv0wi0WsZlwVPVzuQKDUGEiI-8xjvNZAvmWtOCA1klxp9y6hvMTN6_VAHPHGO-jYJmBiOulTOITd8wwg8OPz7qlTaaeoekDBdClFUBTqCJFNgqCPMO9y9ooCD4hhcaXwBRmji7b7qe-iWo8CIdlFu5Iwg4xtJxpIg0p22Ky6IximSyzU3smv9klAjcBvT8bo_3Nh926zfkbME5_hbczqnISS2SuMrDMMnNfDh1F64re88SCsFRo-XQw5LiMQXOCaiSt2ARgUT_5k8PYCZBAQ1grFzLqaVbREmYxVUrW8KwKlPZFGHYI2CqvkJ7HiIvqqQIZZFENqtmSi7UvT6umuLZ-bPyWYo_RWmUR4_hp2-FgpAQRGoOmuQNiLm1a-mmqFWDU0rOLNR_Y7zLIlwsFl_AJ5-l5-mTjH4qviielnjnz56WT_OnIX52np2XXyT4U17kXxQ5PnfbrVB2TpXDwz-DPEusPgBTVFDEnJ5OxireMH4aPSnpwY8Xz-ICfnrBgGMDoVSy3K0Jq2byK2g1060Ik3wavIU5pwmh_-HAnkVPnz0taGqewGvl-Bm8XLp4Ap8hJg2tJKMJTjmyqAF7qLfQpaH4HN8bH6YSVafqhzn6P_iE8Gn6NKOnwhs9fRbiZ-mzL-LHNEVRHudJRFNkVals0Jk1QGc8ohpK3c7cWJx6bIOvCP-eV5c0WU_zJwk_Ln-2eHqOn2XPvnhWPKXHfREvFhl8ZpLB-sAQCpbpnplqWi8P49r0YLQyT_Hf6sFfJEkan9Ps5igM-NnjIn9aoBB9Fp8v4BDENSQXnV_ljVh28APlu_ETsNfgUUoKVeLhVP2gnmJFz66hFTizho_tGelC32bTZyIvM3q5azvBOCS4N_5HjSHL0vOC3hRG8IS32Pn5efiE3nRRLrIYp_0reheaszWfpY-UX-OmI_Gg1LaF8-RjpVD6CInTcFGlJTi1qTVFTXWUozLvW_hEke_fP0c3Cb9A00JHYzXI3RmoWnQFLj57ev60eBpeGE91o3a5euUZH_8XStrtdW7kmrbvKLxMGTjSQea-Ki24tRi7W5cRD8oLJXf2iVsldDjZRtpYD6LJcqF2yAWeFAqPxP7hG71NlLGCO-TkYGW1m7va4xPwmJW7k-B_l0uwe06Vwwn3JavByWC_MXG0mXJoZ0e9NiMTlOXW1vnxPMJJ8AVYIpRs0z5QJdmkxbKaKbskTVq4oqkTYa1UW-Q2SsDdr35tBWp6qcJfyqMNvr3zyqp8PQsHooVwxteyI7vryvUfHwWr0fJ0w8HKKBsFbzAcIAjckACsj1xtrrA10Z1iA5w_QWHoKAbcXt8q6G-kq9xx66GvIdY4LIqtuQENFcg00jcRISzqpE3aIoutH-mUBjqK4SOq_mb483_9P3GS-ed_-b_xELjg_YR_-29o9V2AKCJ8QwWYEc2H0Gx1d9Dz_9AF2CsLjgDpuDY4hXx-PgL3dLtZYmBw2VXkqi9RKDZLOpOvaXvRiGm5YQ_1AaW-QKDITFXhbZrTbkDx54DNW7HFjN9JcEEeAf5Iq38WIN7kAjeYGuW5KjPS5ol2Ga1fpA7irkb4g7Wi4BYIYZI7Guwp3wfjQwMm5WCtm14O2nqmSLoz3VPx6kWbRk3RhHlocD5OqaW1QN9XQakFBnOWYNQmlU1QOUWVTuLmvrWS6IifBt91qI6-hh3-okePUwse7KMyDMEUR-t2Fuw3KAcLOKlO1K1AZOD064YryWKkQREBO-qmFK-SKL6czZUNTbHWuJvNEvU33FgSIt1C0NSrqKAeazJ7NuJvB6HXM6f-kt7w8L3YecaBO28YpT_95Z-jYvMOJiI6yei3k4IkdwAFLXDEuugR4-HdoDeNjhxTYJgTMuISzWMMWoh118L09Mpc7KnOCgN8GFDD1ErPyTWMARPGZq7Di_wyvF8dp1jDQk7Iu9jKS0S0qbVROh3jETRcTBCijczpIBSwUX6ddTFuypXADKxGtHDiPoAZvuLU9trJ36t1eKw3GUHBjDVi0pCwBmteISeiM-dZp0AkzPgC5zhVM84Tnp8Ef4_JG1C2O5oUlXQiDQzvD0LhlLQZS195GAiGkvqUWklsLofIPffRvVIGg446thgzQYcUVLl6tz8wVhRuihuQUIw9HI_0GJh-lXpTz9QZR3zji303N2EqULUvn30Fv81f8CLNgq_ketm7kSwSz4sdwxLn6_1quHgURCFMCT_CGC3Oou43GJIVGC5RyzsVDy2iugEztExLk_N1qp9H9sL9ipr1TpwdVhMqp89kKxxFQHVVVvqMxIEufEOZiSfdADr5Wu3SkXrpdksMa7y0a2qSK060G40_Pcnsv5o_Y9hQ59Dlzp4WeKDwC4KA7bfOgQK6qA-waabekj36BoQywKQApj67Fd3ArOxUILbM4gqUt0wSE59wyr_t6TBV2a1PmqaQcdG0VZjY5bXF3s7JcN867q6B3_s2yDOUStJFOBGk3rBiEy7QOiIPMe-AlhPsnxMT0OupUtvuY6prMnOLvzjgRPz10KJca--X_mpAiviLQTq6aAP9Dhw2xYw1vq4I2qV811U3Xxn32EZ0W_09trrADQaNFCcJvLYJvdLC036Hb6yxTJK01QHCkuQeDDIzVDZBwRhpejSv1zs1Xq6VUxg8HqRJp3PM53BscUijWuBiGO13QlXxYLO3pMm2fBQMjL0zVTg0YbYQ5_F40g0o7jEHD3j9CD8EGy5YRDgNPRbtdQ0bVhTJw0Sg2u_wEWx2zP0NmM5EdIWLHjFLNGwQK_2G3hezam_x8N_2IG9sOxb4cipbZZaKtbtaBX3I4HuT6eY6A1xVaGNPeubg9XZUgTcSoAPR05GTAeELcM0jW_fCUQAyN1TpJUu2eS_UB9ICQulAMAh5fWKRbQm-RL_UUOq6b9TBW3fKFNBZMdIwYtAu0knw9B0mkxpC5GKWFiwxylhyUn7iGKjzPC1E2LR5bqEotg3D6Bi4f4cFhD67u1LvZtwvBHU9VjjEGK43CGRb9QQwAFtradwtTjP3OB2sSCw6QWwv6bya0LVZUrYVBvKLwsRvnWYPVtfesXmDCe1EcRmmYVqHkUWMmX4OR1DmH9qfAc4kMezccNdbMkXsWRhcdXDswcl5jdtAySjl74crATLHXjIiZ19f39w6OmwpmznVDFsXul32bMqpvYC-s8YFYT3EXlnq8CqM-dBAYnSalzeNWHwrc-BekrtOBr4Fm2Ogh8JrtHNpOKg9cdvYweC08ItNLHeVCCmbLA3DymR_nXYWal0-pj0FGN94AQ2yAbdiTYYiQj4xYIi3wlzgsGRdMQolaKg1fRdnD4vuQYwX6lzVYSDYG6gsNI4RdMq-hmVa9TTajc1wTaXg0rYBEy-Hf4yAOu0zRvv9fu0w4ChdX8607Go1TVt0bBf_9Jd_wZUHaw6sArQkDuEHoPQlolyuNRZmHNwxuJ8pBGck8zYVok5Tg1h1mnLYbT7Vb0NnuqJokWaLMqqz0mb-TAsOU0d8_-4aKHckDFs-ZHM40dHvxBftRklvVVrEHRrs9kBvFQ0AvFTbCwdGk93n0UJdKawWINsl6FmZgmCjIauk00ma48PbPSgUwoXwoc86xcB6Bs4foxqYG81gNq2BE04FNGWSZ3nYhjLKbcGO6TFi2lvcv32I2uZvye-lBPDbbpCEFlhV3eW-38P-1UbSfNfPHZugHj-XNfHQL8EGIsk_sQaV-iaZD87X4Ka9wtRZoJBO0p7hol4T5AsLZ65A_nUUnUPko7-oiDgboTo7w4KGA-IYuVPEcBesdxSJvCoiTO2a6XeaqowUxf36pTTS8dPhso1CaYs3cMxz_VxtWw8IfIuT4Guu-EI7R6jXw5VmT-xGnoun58AI7wY7lU7mSs-bfLfpyPkEsQXFJBuFPBNvRbfTse73TF5SFrKQaZk0C4vvtj1g3EzzdGsX7c2Bfi6qKM2ywqgep9uL483dt4kLzgrJyaNxq4l-a4kYMCLnZHdw68DwHulJPDVJGkrCNI8sbn8UOIeVpsAunqU2g6BOhmOqypp6eBpfu3kZLRCwaByl10kE7MDQ7y-vbgGsaSAgdnqAD9yp6tZke6EVjfbJ19zu5ZJhiDqPS4O3-c6t3nD8q0pU8DOejmvn8FGE6qD5JTHXFvJ-jRgaxt1YEGTwcr-CwXCp2aDKdcY20uCeKjVcsHsELhlDxNBLWXNqUBXvURAdN1ALm-PGIMnmAmWJ48QLMLpH4q8jt5wcwWIrk1tTQbCZOXNM8HJmi7N0tZkCrywxJ7LFI0bnDroVNhuhCaE30Y5m1e92YFowDGY97NCjRbjqmqwN3MoqJsqGEEgn2g86GnkEV0oxDh6M46w4JzVN4exohtmc2R1JC8LYh3E62AUuItVJt4ZJI-Polqo1p3QUq9v2Y6eY7kzH8plutrCmR47HNr63xgTYYuV923Y1WEu1UrKIxYYPdqaQ4BR8BULmB4p5gz7BDU1lFMrtHZy4xgH4zKptbRT31QDahZqAkMCjYXRi6y_4xFPWIL6cyQ2Ze1pzh88tGqsqbFIMKKZAbGa-NtNJyisSFUoC8-c7jPdj2ZoSww1Kz5xORsUyc0JliJQjDODagSwf9T6qxhMF3kmConaANVZVrur9fnt7NTvrmvVO2MpCjdwgo471MX6MVlNNM-qU-H6hTyzHHJg8uigWiyp9bhS5Ux-qvGySVrFvOt6A6GIbpavzl2Z9Cen8FnYiGPcrVWSDgT1-de7xEvCinDkNQtAk7C4piWx1CJMNzawKceMdsCiXV0sMWlHKnjKcuJGMWGN0XtnS3J5IubuHtUkoNljAYPSOpDguWg4TsZEK67wyGWM1vSlIth3NzCn-gb3J9JmexEVVJknVtBZBZtuVmdqV-zceg2XfUakzOQjgaqt0lNK32s93xOHzgRaCyqbfyDVXxX4xPnHIz8DvgIRfSja8RqhW536cXmppzSkNR10kVMSd9Mf8pu173JabsLaKNC3losnLKDNOntNZTXsKH9EjjWu8rLGq3IqGU2czDRjoUAupk8Wqdyc03Nn6fNsqwajiNSoK3RvBnMhgLanyb3X0v6vldrPT5fWkWk0dPgEnzULwV60lZ3TcjUJn-xD5Dg95Z39bzeVEd7XKejT2TTAup3FKrpCiPnlDTsI1WDlGk0xhNZs6Lso2lqIIrQVt2tGN4xT3aiy3Ht5i3OGnv_zr26trrinF1O2oH4Iujf_NT3_5LxhjZcAxG5YOAITTj6SMyXobNBZXnRN2ClXMo7qGfcaBEZpzEJ6to-XVOM3W0nlkDv1PhbniVCzSNE6j2EZzbZc8R2PdveWd9gdjGUXxoszLJDPgWdsFz8Gm3L-lnRIqF_I3KFCYPuIs_ksXhw8jDcZhb0Qtq0Of9-rGgMKUOh1BDIKhIxAL5uHRtLT2uWxcE_Ek-IbO67UzVO0_OUOgEkn0eD5EiSVRUkvs1CNyW59i-_jpprYf0ZRPhQ-DZk92BbUrqAx8f8Dqci2UZCFutyqkI2fK2NJ2HOoyQmJS4FeB7CkCcJvhpQ5hMif5JgOdRGov4UdgYO556KYrilqrmVZcM91Rh3QWNQ4CBxJLUeemJwbGEXhe2DqjmvArsvQG0rAnwTNsm_FOoMF2hvv_O07_YgZly1hyesc3kjWCqlhVlbM3l1srPFDMy31D4dldt6SGBNZx1uJ0AppkIuiSNrXImqZIclMi6jRMvLl_79j50MjYIi2TfJFHbelUoOpmiE4Y4b5dDTG_iEEBWBZQ-WB8NPMlOOhL41TARClDrF8uxQY3r5PyGZS-0zkCPbUYRaYDQ0NMCGlFfp4d3WhEM5UY0J2KbLpEBylRTsDSv0J_GITg3IZ3KA8pZ6jz4Q8vFJVi8D_--80YEF2ExZR43dAv3_AKK0QS-dIEM2f3hnJZgiHnutcJzdzaGgH63UQLx3vDFhiZLqLqlmhOOOWV7P1iIIax7NTaRIc2tA9VCXq6qsVtVbafc_xzlehWSpjVrmPxCN1_S80w54yUQ14JZQi5UUZb5LmmwoN-Ped6ButLMmJWhQGwTRT4VhRyOXRA1bU6xnMj-HMQvD5RpxlNEN_D6kQT-7Q6D-1g7PLHgraRXEuoYsLK5dPac8JLKMKkAq1dVTI3lorTwdPZs3dtyKlNoCJtZCzaOrMlJk6PTnXjj2m5-djRtS8Uvv6cC_EP1mKm1g__q9S_zg59qZU0vthNsIDJQIICR_3cc08fuTIOGg3UbEVaDzxwWorOVjPXABXLS4zuXa1UahH3F0N-Qccg2geUibhc9yiolHujN6AKfjyUuTEC91WARz18qKT14cNHB00W1CjOv32uYLGj9ggXAcZppPabL8gauJgqkgJXT4IbGTWFsK2tTFNTfbh_RI9SREEorTkOnp5YuBY7-6BJN_bkvTiva7nZzbVEXsx4Tz9Gg3CQuoiOvSLyDSXtMzzsnTS27aAHFq5Ew59xH47UTcnah4gUPECF2DCEQh6UfnMsRVJIaEGephrxoOp9jLE0mTOMUhlmEUyYsNApp8-rUyl8l86t5uiNFnVeFG0Rm5PdaebqaInberXqjGaWFW0UJm3YGGfXad86gvzerzvrYbM3gri5nid8cCNWqw4dfCT12Li1Q9fx6nZutYLijMlkXvjDznfagdTelftMAt2bgIaTELWuPoEBdVdGSXgZ3mYY4D7ioJszAPsIcQcrVcExOmZ5ktmy1T2oRo3BrC2OZxCLpS5m0r1Ejhu6N7wH55FLrHMaiTTFC68NQMJtdsk-Om8YfJPD_pZzNpVNR8sbq3mjYEW3ReE-E3ZH6x2sG_HwHlcOwLjg2KQonH5FbvsVdxBYWMwlCM2ZG0DgPn2UYKJSNBMsO8BJOQlSRgyJ5tp0wqIoz1Ls2YOhEPRVv0QA1wRsqopElod5HJfWG7ati0fb-da2xBqSIaswj8K2FqKwnrXpVDza0ffrQmzzPPoOZM-tYSp1xgbEHsE5lBQ3O0iMYezKucOVPrgdOY_3SaoeBKZtBARXxQ04m74J8CU4lQ-eT9vfJk90bxStbWwOUCF0R2lGp0jcKWjBDNOoucbh9N8snx9157hRQH-jW8d4NbiZyHRHEp0cvK1XyviOdO7jHW1NBEcrm6O9c-DWpu2MXnnqlISI3M1Vvz14RIVzTk0253Tet6DndQtNTKCBNmbEDlpO2EqTRgu2xsCBLecta90nlFPhBw9SunqFxh5l5hCjdr2G8eHRYvtaYoATFD2iKqwi0ErcdbFUa2-VCr_RovtH3JuqS_cPDwShNfAnjA7J5lV1_eDsjw9IGM_wWe8eYENtjsHov5LYnb3uVt38dYx_1-fC8W-rCIP5M518ZyDB-D4Pvv9x9rN1pob12XbVHuX-VYWwPlRJAg6ZYXiFazdwJ3JOo-NLq67oNCJsPA6HJfy6X-NOxQ8GOXD3bOwyDgNV_gL1vjbMQHkhoyoft12_e6frqd7sfzw9_f4s-Cz4VV-d8QE1Nzil-ZvFr6eY7uMMm5CHx9h-TQYn-MPCIoXuRiF963cnGtPLti6KUNY_z1i-0w3hnP6UqhJYgRxmOpQDsuPU6LSTlIk1OMNZm5U_3yDhWhjhkgAjDx_C31TIwtZDgT2GcFeFNHz48AzewG3Gc5MTJgOXqq2Tn2eQ6FwjtrReO715SUlThpgMBrTvaIAc-tUlLlOcflUTN0l1wBrxUTOJ_UaxCZDBgNIpTagSmNsojbP_-Z-jcJFwNz9d572bpMOu4wh0yAEVw8eu9wZOV9AzCjkzqMbiuhiUupVcSZ365qrpqxs8X6AyubLmNjVzMApFl3COv6pzbeItTm5TE8fv-kS2XFLnLIOqtlP1DLdutpU8uU0NvP9Z798uTmupZXNy216efpKS_juI_KgqULDjuTu5bXMef-pLNiQwKOzM5Kqv2H85lG2FezKA7UpeiTcdWCq37bb3PXXHQqpRblpYKe2nC-DZV-J685PbNszxB5lQsuNPWRWtupozxL92eiyywOst-MODt1fXdDOucLm9mYBef1VnqRwDlhstlCoA_ELiE9ljpAW_UbipE70cTzjwIi3szvqQyK1xZ66TTJRxETfVIk7TDNMfssmLgrqh8ty5JCYugYdLbPKDtz689eGtD299_OLWx92Zmg6ZivIfj_MQvY-U6WdhXmqTIsqiPA-TPC9F2BQVjKmUESiACPStzBuZx21blUm1aAXohKqMmmaRlwi8abP0lve5QbwUnYX52WJxhHipqtuqjfPKEy954qV_E8RLVQZ7VYZZvDBdkxyDQa3RPc55XdIft02dyEwIW3_mHP03GAQ-5PjW4eM6avMkThZtbMTMOdEdYNZ9T2VsICyCxQIL3p1q_S1V4zrV81qxE-Z0hLwQQVwkP_3ln5Mog3s49aNOpfr5zpwj1FtgGINUt_1bUz5vgZhq8TX8aNdfSnRCHmGyhlF_W91gUzFh6G9q-gyBcil3qnGLLk83RrjKxVYgeVfU_hp33b1zHlPQPVnlVQarFtpldGweZxnva7eotm9WEay6Zk2IHerCe6WrjrGL0pzKz7a6XSNXxrAfMacOvLb7ru2ZY-oAdwZQxWXgFtPOlavc54frHJAHoOqxPI9nettdYpvvFnEyoC_mOF3YjWMrL3E3b41GgoWUXAiimtQ4KIBdj7CR506fJjSfGJGJAWuOUyOfhtu8D7y7a9IrttP61IKlslwsorJN4oUlcTD2nwPPuK8N16t8gHLjlEcNckdwP1avOjeDcfz9YDw4bINPmTvqrWzRgLpd1ZXq2ERtO5CixxaNq23cIdQXPUbOGYglnIncA4aCG1zjeG6j9orohlhexrp44EyTKZ0Cnb6Fd5y_pv7M-usdVmZik3Ksa5zCSRZ1XbZ5usgqA3F1LNoxS9j9rFIiOFPETzZFbNpEiHcdrSBqImo6w_WwhAFGNWUpNg6VnL4ts9SM7ExU7Eq4ie5Lp3FBefXLJbbT0kEOJlJAbSItGFn1eKR9rvYu6EsCmrH-tYWxWLrHxW2WCwgTVDwNt8Za8LlxGf7P_1wkCVLqYDdvLnFWqtRym9naHL1Xbxb0UH0C6F7Ryjk48EIRp1ho2VTvhki0As7tKraF2I67MFaV9zL5ybB5zI1WsHneZ8_yZ-WzxxezMTnIhepIezEz4oOzS9-IoqhY5PgN0zDX_C1L8qT44kIVyatbPV08LZ6FF9bkIqvpVAHSVO9IrI2CXQ2n8DU-I1-EcXxxctC30VhETh_MUY2RKdQcB7WOtnM8htfQT9BxMupq4OktPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6S09v6ektPb2lp7f09Jae3tLTW3p6y4-it7xBX_n_Y3LLj-El0un2X4is5w63_xiWHef2a-oBgRPzxwfc-Bo-5Hp8EIE_PuCG1_BZSr9y32r4NXzw_fd34va7yYznPp3Z1R5zIzbqiq46rJueUk5DczY7hpEtRIUYO8l4P5UG6MYuAJsXtjG7Uqk61fc-yrmbwz3HjvqysXhU7NhOupcCJNx7fxRvdqoPOb7gFPJTVOo9bHQ3x_BCATx021dQIBT_cfqm68oqaoJtx-K29XV63aBeUmFMHOwO20MMtxDY8Xpd29WCv2KbxOXRZePlGhBP2etu0s7Yjg_tyCLdnZOuqIq6KkUclmkSJUUbx4tEVHV0Gyed4TZ6PyedVxo_u9K4O6GgobAyYzmLfzxOUvVJWLnKImojmaZt2oZJXDVZWQkEMbdNGIZ1midZJmLRpCCBeZHUaVoVjRRw0yYuS3Dmb3-lI8Rci-IsKo4QcxWLVoKMC0_M5Ym5PDGXJ-byxFyWmCsLw6IswrDJbyfmOiYmounRHeSEsLZjjG3zOUboJ41QJO5SNBcjGSBXUqM6nXSWA9lwEsnOaiq-rWFEDG2ykMcsqDNsR7HSJh6WbsyrJdYnkrWnC7S2qxFfmEuSQk0PbzaNPWQIcwC-qoss9549LKS3Nc-T9fH69anj7JgHbA1SiPmR9agl3ucDUycRpYsyfWcYT1BtKmbc5NGY5-SOj7jErMb0nGH_1jjD0hRMm7qRi6KsPWeYi0qxe_7QmVTHA0y0QkTU3D7ob5k4LC_SOApFmck4vJ047OiJr_UH7B3M5ZvO6EpXkJLZa-innVV2gLncW5ONXKjOhxcKxOGwiGHdyYVqZHiDOuxCNZe7YEsRG5xRC0JsbcRBgQvVzE81O3KX9EJ19_vrk4U5tTWeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGGeMsxThnnKME8Z5inDPGWYpwzzlGH_hinDjtNmOU-6lQPqqRKCJSLVV91O0UEZMianGwOaObcRFrgVMLc20FcNc3T_9gEGdQs51Fe4l0yIH3MgKgppxqWIoGzDcSPN7NaaLheknT-I-SlPyjwSadXGRZyHDVq_Ms-oI8dR5idDnvPXYX76_kOoq45QBUU_HmcC-iTsRw3G38KwlFVZt2WchVEdCZj_Kg_Toq3jsIjyJi6aKKqrKm0qIZqkSFIZL8oQGZFuf6Xj7EdpfIT9qGnyqK7rhWc_8uxHnv3Isx959iMjibEo8rqpwzYt_z2wH303Go5j25jM5x2NlzkaL4G284XnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW4lz63kuZU8t5LnVvLcSp5byXMreW6lvwVupdtYlW7jU7qVSenFJ-JQguVoX4GAyu0vQaDk0JVYEp27U6W8n1FnZp_lcFb8bIQ9s1-WD8i5vdNV0t7e9vq8-42cfoE3xnnQiPDuN3W6_t37puas1Dd1OrL9fCN1moLZmx7pnHb3YTo9b-wdb-0G9CErbgry7H1HBX53H6NTofOh97o5g2UimipsRvd6CcpINocuOtUtoCFrHyCahu6ulKmydt7_9SN2kB5QJEBOqir9uQZ0K5XNxVtZndJfTodtfWpPntN9d4q3PdlNzFucl2GaNcXPNUz1VRrPcIalYqdc5HayG95dcPgBPxOY_6ePVModDI6JYRZVk-dpUv-cs8nmPfkEw2S5xA0k3jA1ow6U7R5DvcO2cRIp9gG3pMDuvoEct9tRGP37R3acGtA5Q2-lBvz9hkvKKWhj1OfvnzPoVOFiqHIabV4wdyhazV4lpeTMoXVy25n6yZ99F0rEX-rZzmn8yZ_tHOCf_NnOOf_Jn-2YA5_82Y7V8Omfbe2Lv4KcGxvkkz_bsVk--bOdk-WTP9s5dD79HrNH06eXc2tXHhgT6sFPmFVo4APeElyxBUQ9YX-3v5R0zHO6jM2OrVxKrG7nAovbTMdP9kzHDvxkz3SMul_2mccYgM-X5AoZeM-YhoXijmBeb-cM03UlyqWWGz9eDZRHcaoCM9Yg_yCS4ERmaVvGYZ3VeR5meVvlsi2p_dFRkmDDMft-kmAf3_DxDR_f8PENH9_w8Q0f37hDfOPgaM6TMo9EWrVxEedhgwgLmWfU9dlwxfOSnCUzlzU--fE4KzxmXggzgA_APkLYY3Nmfnyl8j96BMtXqajjNm2yDHsPyjqUcVtUSY4vh41eX4HZBEuPXDA7-sZQRWdFmKRJnuYyKqVMRBjlTVg3aZmmhWhzuFESL_IklFHU1G1ZlUUmkiRuqha-VOV0ILz_7fDPDwyNT_xdmJ4l6VlU_F0YnlEC2L6-DItKLOr8gTspP_xsaSOuJSS7R-PJ8xJmrWhlERvAqJBpAcaV2zQ_uLslxNld3mfT5TFFAa_bxm2UW04ia4WZAgBV8PorM4OLX59x_3VlpWp4hLJWL_edQlV--yL4LApDuwNVi7qRPzS_zXqdadNVQwQdq3U2tqwN1bY2qB6pKhvCLAjNWXugCWxbeIQsqGqGRm6W_fVKJcKRfRvVv4LNmK9QSxV6aQRtMOyLivCvFSfyAUBEdY916ReEW_JjgCEa8WYxLUwPxKfQV3_4VoOgB1vif0qUE0QHxW3wJ8nNqywNJWiHeGG6mGZ5IaMqd7AQfzw9_f4s-Cz4VV-dMSxlbk7A-ZvFrydabMVtU4OfIITtBwESVYgmDI8xet1qEE_VdVV5XURNXGaGwcYx6Z1CiaNnt9CFyCOKddtHr90KJPQQwWKBDaic7llb6o7jdLPS7XypBmyEhBZBXCQ__eWfkyiDexwjYj4JzneGH5p6fQ3jorFt_9a0s7KFUUo-dDnArr-U2FfhEYKnuApnqxveK2Y6S_zMbUQEiqTcqUaKul0U972pDR1WBXJ5RXQ0CIl4HwaJwEeIQ5qQvFjmaZYv2jpsDArHcZUm_CTR9BulO0yBo-Hqsdv_cwScuvgyam63k9xDBUurkFOGuz4jcMPRqV-9PL-pTboDdfWlRucQkqUCZx7PwGlK-9bpMuR2hyQejnpPBTNysgEGw8NZphzgOPfqscKkGwQetmfmLbBBpAb373t0pDmk6QI94jU12knBErmvvKIEoZJq1UnuBKZmhFKxYFXVPWxF9PK8Kqpln-ZcrPsNHl2mFEt3EfSs95713rPee9Z7z3rvWe89671nvfes95713rPee9b7vynW-6ipQX5j0aTW5_2lWO8Vpb3TOcpA8wMbIfIk9n87JPZ1I2QSizQDx2uaxF43TbBhQids1U0y04s6iZOkqcsoujczvdNXB-MLvcNmjo0njfD9jRHTe375X5xfvpULEWVZlha2n84xfnm1xQ1pNnL6of1q3kr7405vIJuX0Nbpc9ORhmO-7ajjiN08xF_oHMKefP5nIp-vF2lcVkUVZov2U5PPn2OBeg27Cnv2wPG-7KgXO9pqM0Xig304DMXL665-TZQ3uA23zN-tqGHwQHFYAC3hBmxJOcfIcKMof9iVoMjFI96nlorIZr0wv0RdW3ZieG04BzxPveep9zz1nqf-k_HUF2C1ixB0dFpnfzWe-p00cXTqceRSt-kk1qj_mkMx5qpP3S5at-U2PfQxukRcVE5TyYHo7GkrUHODDkmr9mvwDUiujKZGumzcrWpve257z23vue09t73ntvfc9p7b3nPbe257z23vue09t73ntvfc9v_2ue3Dol1EURjWSZVMc9t_cwAiJcLt-RxDqXPjn18Ev7qdz_6U-aR_PcPv4ZDmeLeLIDop8hQOJx2BDdIwZGTWnJGScMVizPlO02-jAi3zTN84vjRZit5nDVzcXzqEaIrAjciy1OwM7ovtO3ijm1hZ5xUGvje8hfsG2c03SC1z-wfAa4nx-mBE9uHIBX0RHEzfECTEUnxkFpnkPUOSEmRqt1NFNp1C3eEB2GP0doDDg6HKdqZNUFPlTak7LINhTc5Fs1Ha2LZ69a_0NiIQCIXRb3013HLwamPBSI5NK5xCrsa2wXtQDAQp3GLYvKYN_1jRj8l3xBl1GVA9HANm3OZ1EfEt4yTNOQ-H66M8avb90a1VEkPTpamkBHi7Txzq-jeGzJ6ICA8p6w9iU-TCai5Xan88kPWqJZYyWM7ppajMXErIGWJ4VPpwUFFyrRANVvsLpMmEifkzdgykIAiV19UCYSGjaOue6AwesSBqoAQ8j_HJyGc0Yo9OUMTy1GEix8gwrdlEOFbkzSLJYdOIygQdnSLVMT9yv1SWh6H1M9aHJfoz1Y26fggzPrTXETigwKTYVfrWIk6blD6ph-FCIQObUXSDC4woy7MVq81woqwhNLdVdc8tOwcXT2tKWkGz19Tu0fY4ps217NlDg7vQwpGpcARHdQpToZLBqNTd1MkSlllcgeKXSWJiG0km0qwVYwTDl-K6309nLPOmkHHRtFVomzsXQoSVSMX4VHmmOuWz-UeccdQz_5AkXoW6VgIkbb_iWhmMuoHQKP5e1IUkZzhDeAEDZNZBHjrSaNN0TGftQCSw4tQc9EeqUQ-t0bX2nOmvozpWk20e8cupd-CQK2bamXLeVBIdvPIh9zxbbOBCIwN9kpCCUmFbh_yISOwc_jjnJXQhkRkqm69LlGo0zde69zFT_SiUHg_SwAA4XnQ4tphOnBip492CFOQyBx3cknW3JY0NX2aqq6fuhB3rlk9_uNnqnukKsZ0xTNmC9DQyW2-7xlGhmHhUpRzYrXlFuUZb6ORgV8wSER8FHCD4vpSrPdBsBb6cyo6ZpeLKlgNyb3xvMvsOesBurlxmWjVzprBhqhDa1D8rgsBHtuM4RxBwHLoHN0u2eS8EMkkLGaVTB01TJJ8y9MlklyKz5FKDrWtijnV54obDfs86R42cTT1tYjj8MCu833CGlPECUw2e8zwtRNi0eW4hNEWa1vFN_qkXasq_oX2rNf43DgoJZ8rhEaLfNTja3ZV6N-N-ITDssZbtbN4Ql8iqJ-zDjir_lKtmePu2khWJBU6I7SUp-gldmyVlW2ESoChM7Bf5Z-qkyUe69inlYHHM_wFsts3uarr9fRzFZZiGaR1GFoSWx5nMbsGhMzQCQcaqlOkk-B1s66VTsUbB5FOKo3J9oKac51DZW7JzAiR8rIhXwZQyOawUhBfgyqhBGSzEcXJj68xM6eOcitus-22p6G1pj0b-1MzuSuzXyOxOoRENNWZbiqHkc8N5Q29lTKlLcvWJ9WnM-UqhOdPn3tQF2cEQ_Q292FSxWiLAhsvAIK9MtrlqYV0WlVMP-zU-wQQFHLgF0m0TwSf5xsQtA-blsjfJb-qlgxfQIBtwu9ZkCyAoFIONeCvMIw5L1hWjMIQGY9N3cfaQxxjEeKHOVR1CUsRWGhq5pTq4Zs50sKiPTMZtIn2Xtg3YdDn8YwQ0KjOZZvmNEJMuMEVL74kp9NT7_qUGuwdc0EppKsomMFunrrZknUFbdDYyvhVH3FJco40KlsQh3AGUvkRUzbXG3owDQwaSNAUKjWTepkLUqa2DLqoka5toDAd7eQXiOJ0uklG0SLNFGdVZabOGVR7FsQOoZRolHL1S7AfGoMNgbDh2LawCXpQwI3zI5nCiFyAE-KId7VpLFLtuDJOzQwMxC6JQsd1re-EWsmm4cqGutNRCbLsQ1Arts_1OOQ6CEd8c3-R3aPegUAiHYnP6rhPEuWdUA3OjGcymNYDBqWCoBH8kD9tQRrkt6anCtJEOQOTxmJ8eNyqX-CFT6KAJLOFvMPu4pognWKLiNUXu8GLoUFHy-G03YE1EIFZVd7nv94PlpzxeFqyfqyi3iCBK1YYag0p9k8wH52tw017B_W5yg57hol4TxAxLa1zuSQ6vj_7i0D5YKgIWNMtY5ZQ53AU-HkUir4oI08Jm-tOkzCJZl4eK4g-qDP5G0cd3bP6uVaQHBBSWn-VwTdaNzeYhT5nKihs-BBXZI_0n8C00RVaDdo5Qr4crfZxLVU3PgRHeDfeicLjBiTYJMChkIdMyaRa5jRHGbS7i8CBLbTrATeJP8zhtq1I0aWqPL9v2yaHhuFfjJg3JSkQRhVmVxRY76_Ryel9Hhzt0Y6I-SE780K0ApvitKo54ro1cdS2ReoOivPhfr3RfklM4WerdRfB3ow-RYWFOxMD0-wWeUv1rDFmwMhywAoXL3JjOHZyTM1NErv0L-kp0khnWSwITjAgluLPfVdc0iKLBo491GrFPyPpqDd-4VK4QB-d0lFksiZaF8yWKmwEDaFukU1yB-_XkayLkQm-CgaXkdX65R4jFqe0qSODZa9WXRE_QCG582TsJR26DgsQIO6fkWWVUaO5VWP89hnMs8yyKyjSTtnOJ00lr3PTpXr2wKGKoAkSP6LJV32BfAz65-HKqmuNgMrxFT2bCqe4pQASC8FWVtDbkdvabmjUQTJuuVj018Pdv8fyDZV92G7Z2wK5rYHYVUxOzFhlab3iEOh3nTD1tH6BOY-otoU59fSCr018izS6XElwcRLpMTWBnEly2V6mDV8aoJ_m6e461wtxLhlMNLs8I2A-UoaNYDOpZ1GIY-HcJTchnpJc03CK8BFOyIATY0HlVV-XCWlemXZmjMD6m4RijTEmTr8cGuiZQNKkgJ_BBJbA2asIJhl4VWBMoa21IIi0L-KMAYbkcsyCyH22LU48aXQ6ri5YJI9k05OsaD4eCmpXY1Ve4NvjyiF-VWHXN--FzmIFld6nE1JLzUkeOQFToT7AnRMjU8eUnigW67d7ZQlPDGKbZYk6CP3DLJdMF4pR7GsxsjEKoJCqipR20gJF8WCJqw8HvKpYmvqUAwaoAGOGs_U4zPFNB4CNNozs-hRRuhtrG9Jdt3ysjRXd3ctowcRpjeT1Z8S0WZd5mdSstx6vtP-cEOF9aqxQjL9pqdgCrnGDYD_otVMT6C9JOjJYH0-BUV6jAipFJ9WhM7dxvR0y4R3oEPNL2xqnBQhDWobFJeOUgHbPYbcTjBkOototUYwybhzcFOcdx4hp_j8y68IE7Pd2aQhDcJOOEcoj6vS0UivxhCxnaaruTf1W5fn7G03GROT7K0k8zw54KFO3XKqci3NqD4OV-hW1Z_swxAMXUNwoVDK5zRQxKhnuNgnXrnZJRqnKn4xftSIc27Ok49AA-A44TL8AyVrICVRDPnAEzC09Be4LsXK10_nHfu6JPVcy6LFvhP5cIK9iip6XT7zcoB1W8VXUFYSTpetgR9XTLsQQmyFUwdo4HYDMprIpVKc8j5RwU6ufBODE7x2GlKZwdBWkZ17UjaUGLbRgjqtwMVkOpPpg0MpRuKe92eixYhrNx-J680zPN9kgn28HYxvfWsDqrWfZkKMHPytcw6UZdB3h6g5331KH01dHfwQnvH-C3rfeiY0N9NYDm0LqFVeOJrYIcBqc6kvmTFbziZsMY5b7RWFXJsO4yoyupZ-Zrs1tZytHOpPpuJYZIGt7M6RRVJs4J1evTCRHAtYNLMaaaIaDAOzgi6uy31u0g1Pvp3IHxfy3HLeua9U7YEny3U4vStdZHwBl1emF8oR03xyue9OC4QHbEwufk7FSwmaRV7OFE5y5IeyfMrCFALlsfRvAHLEVYaft1q3Uq8xEHvChnDkPpYLunWR3SdCBqu5lVIW7YHxbl8oo4xwn1xt3xYCMZsUbEtQop7YedzUwcFgij2ChWctY7EmyINTnQEymCCiuoMxlj2xnTuaOQdVtFBxyQbJooVlvbdOg9bQTjAlzZpGpaC8JOyrSWi9AtPdVhKFIE3cB6j6w9XgwK_OObaHgAeYHUYWktd9QThG10sP3Z21P61nT6s-LwuSLUdQzDE5UzM3POrKvwHZDwS2kbpx0rnHukuIVxzal7ArGjSqdJwPxmCOh4SGOqbihNS7lo8jLKTKxTlFWWx7FTmUEc6xyRtZyxFIjWHRXIyGYi5D1RJwzjnnc2ZqOia40mXLSVPDN9slj17mRIne6AtqeQUcVOGbsNvyFSRvVJGZP0KjOUVKtpWEO1B2Yh-KvWSjM67kZHEPsQ-Q4PeWd_O-zcNsmpVdajcYgO01Pa83aFFPWJttUddtepcoemjouyjaUoQhtIyrNFdjM9N959OgSnGqqSpFNjykEHjAnZAEbwWwyz_PSXf30LHiV1a0D80ahxkO4h85uf_vJfMNXINTtsWDoYSm4BR8qYrDcDR1LnhJ1CFfqvrmGfKaQSzjkIz9bR8mqcZmvpMA1nwKeyPXEqFmkap5EtZw-rJsnLUo411i29o29XV1EsoygGz6NMLCFumheLMK0OmkGYxmmuXcQOm5XN07EPgS6wFioXNT8oXLU-4iyEWndRGUYajLO_iJBShz7v1Y3BVSt1SkBI44EOHeFAETGjq_KVWdG4JuJJ8A2d12tnqNo3coZAHQ6Im_UDlFgexUJEZdrWlYmcOl2_NYM8ucdoJ9sAsSIoRfsZXoCUj1OeqGNAZ8SKip80e449olVYmQo4cvqVUJ7K7VZlNaTBApIpaA058noGOk7UhgALcc_PNv2_RmzXeg44NMCe5jgcpUwN0yeRiqkOzVKrqtQ9vsIg2UvVY4nMOliZFXZstT49Bn8eqUCDNu8O2h9VCpdGDuN2hc3IqCoTwwEkeW3LjiYra7wjBSnFGsNURhtQSJMra1m8LIL_LVYeopm3B39GEPRCxzH5C3RMoKG0EYSv72x7UExP42rtKHYKrrVsSMp1Xbgtq-QQNYsvdVSj6t2TcaRPBaQoBOI-BQFAS7EZcHv9TgX9wIkBu_x6sAuvSoa3p8oD3J7-wx7U1ik5MaemtZGy8jps-kpyhg9Tlp_u2IBzSYcCkdGijeL6MYo13rpFM2rYQ07el18RWl-n5fi1heNXkE1ruOQnEj5pU4usaYokt00hasREFMlRpYmPo8jBt6rjxTQyIlqkZZIv8qgtncYcYbYo5Dhe85gknPXbmebw1k2iKbdnKgaYQps8abKPuRNj8C2cs2DxNfMlbPWl2TKwwsr61avrwk0GdchofII-wDFaT6e0Bg8TQpycazu60YhUL8xRJ2qVIFShKNw0sP-IeRxO3nObWiIMlJzhQQt_eKFF7X_895v5J7oIG0fgdUO_BLV-Ah_xMMk_4vI49ik5WMmlcoOrJRzMrX430YJNpbrHk70oVKzSaSXBIQeMbHENHjVe0_Ek7bhWgp6uWpTocCvjC-cKZKdOPj7rHDNT6A2vZpjxKrY3Kp9obobTNrRYU8Fkv55zHaZ14LnSR8VesIklOLQU5zpUr-paHVi7EXE7SJyfKBOCJojvYQ8io1_tQYPOhz6IwN-X3DdB5aOVn23SFre7ZkWYVHErqkrmxjyUWRm3qYzHe_YPfacW_EvVX3A64VikjYxFW2e2NDYOQymjsh03d1bl1vOW8N3KD0PlNZwF7APPjBE_O4oytB3Nz7l50cFazNT64X_Jf7Ctz5Wxyyt6E6ho0E-gwNEm7reHiVEaqNmKtB5oZrWUGa5mrtUvlpcYUr1aKVgT7i8uVQIdgzh-TEddrnsUVML90BtQIym0hDjGzL2oBLZIV9L68OGjg8ZUahTn3z5X5TyjllIXDErXiv2CTLCLqeJu8K8l-O5RUwjbeLPKwaJyIGlPYUsidkx3pONwwqgX5e-fY2qUi98ff_kc4SGbvQJ5aa05jlhjy1KnzSqGeMTGWkoX59TTfa4l8mLGe_oxWuGD1JlidkXJIZe0z9CVchKdts05uBWSUlqUv3GkbkrWPkSk4AEqrklVF-i26jfHEmpVwSXIvVcjHlSdsrFQJ_FKETLGRDBhwsK2qxCWLne7e2NXlP5zvvOTfv357n1Hb7So86Joi9ic7E0LT2lkNNYSRHpz-43KqArbKG7a0pYqOeQ5zhn-pHciXvjixwCeFMRyHAbQiYetaOGjsbsPH9wIkKtDBx9JvZ1u7R96vJOPsq4UuYjK9B705TUZNm1HOc-kYkETRXLAWDa-QmU-leqULgmraxurH4mKmDMA2yJyf01VeTo6ZnmS2SUR1i61w7YOEJ5BLJa6CHupBH6pBX7kpdxw2ZxHLrE-eyTSqhpCgzMdyhUVGOENg2_i9qiinhYcPTbUKzdWc9wXzqkWUE217kSIYRJByP6A8aIJ2hbODKkuxBgoXe837qiwQwrXUjZnbhiH2wpTsQfV1JuQ5QFo20Fr8YhEc20gGRRrW4o9A6ooEXDVLxFNPoHhriKR5WEex6WNSYQyDJMkPdzfoCwmt3grqzCPwrYWorDxjbTJE5c4hucC7oVZPOzE43TKHjAN3a-vV_3eQOxtZM7Ntuk7kIGHFAk6bwb7AJHChNAzW0qdBjoItNQ0IPLtwe3Ihb8PwusgPWDjULgqbtjfNI2CL8ExffB80gfWV9ON4bT6sZnYmYqJuslep9uNU5mLeb5RZ7HD6b_ZB2jUmuxGJ6AbrcrGq8Gd1KbbsekU7W2N4sZ3JEMA72gbH3DMuDnaYxBubXru6ZWn9rpYHrS56rcHj6hwzpdj-hPd8RvTmAOietBYQ1MKO3_TaOWGSH1gRZ23rHVbcwbPHDxIKe9VT0RYexqsgV04bbgxzGyANAZCqzsBOz6XIuZTQLAbDHM_4t5UzLA_PBAEHcWfMEYnm1fV9YOzPz7Ap7x7gFRxHAO78bk-Gm5-Tpa2-cOLDuu0mgff_zj72djWYBW2XbVH6X5VYSUBfAOWo32FWLQtE9wyXgHfSzHu0fmLfLZwQMKvKi6CPHNyYDo45LiFUR4jsf04Ysc7EAZ-HCXjHR7wM_IcIsExUf3cNkW38mZz8EGHFw2xso4Ma2XNp66mrrA7532EzjcfqDidwXhXRoF-hE3DGQSXAxJSyVDCSC0N8Yxq9qBMKuqzgnrIdie6B4n5GvtJ6Gi-QaHRGWd1I7Yf2GiIGEWkzYmiwIRUNbqWrr8P1tSaXF4TqtV9IW7hqB6NxT7cNY8cyCHo_GqUzgx-_799EOV0WGfpYiGipqqaOizKuhWpFG1xG-W0YXB8P-W0363j3Xp3sm_DuWmZNuMfj_NofhIa0XBRt1Wa123UNFWRpEURZa3Mi0Yg0UfSijhpmyiOs0w2UYGko4u6aKTMmrgoQaRuf6Uj3KFpdhbmx7hDozZG9kzPHeq5Qz13qOcO9dyhnjvUc4d67lDPHeq5Qz13qOcO9dyhnjvUc4d67lDPHeq5Qz13qOcO9dyhnjvUc4d67lDPHeq5Qz13qOcO9dyhnjvUc4d67lDPHeq5Qz13qOcO9dyhnjvUc4d67lDPHeq5Qz13qOcO9dyhnjvUc4d67lDPHeq5Qz13qOcO9dyhnjvUc4d67lDPHeq5Qz13qOcO9dyhnjvUc4d67lDPHeq5Qz13qOcO9dyhnjvUc4eqSkswHiJZLZKwFp479IJTaXPd0sx5hNtfze4U7Q3RmT3BPar7rB_hIP33wz1axtg9qhZ1bvOdk9yj1DrBOO52Vm_p3aG5ZzRU3nTXtcBiRreqptVD925EKEbT9VYu30iHF1RRi85UzsIhzOFA51ytjyH8or9x6rHeslJe2tUzrQ2oms0ZPJOD3KQ3VW8_4jRVo9Kj5Mo6-J4FjJFvwQdp09iJoHeY2XrJ7YzlQA8CVNWAM-FKAPe6t6hx3sTBY1W_YWsErfIxiQnd4Y-J6hwmOer4ymtkUQK26Z7eeJxgUgavLXhhhhPP0-p5Wj1Pq-dp9TytnqfV87R6nlbP0-p5Wj1Pq-dp9TytnqfV87QeiVIjL-SiLUViW0n-O-VpfSFHhAOIiXULUr4-WHwi5dIWoboj-DdohiJh6aB2Io0NdCuK8iWTBrBbBALgfDawCaD6gOpqVgek41lk__ossiiMgxI2RaiiZnimmshurgNdIMMdKXd7pXAGs2eFSoc-OsJHq4xaky3liZrTjQ1ThKeq9VS1nqrWU9V6qlpPVeupaj1Vraeq9VS1nqrWU9V6qlpPVeupaj1V7S9OVfv9j_8fa0nwrA)
