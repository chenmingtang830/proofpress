[//]: # (ob:ae580676)
# Proofpress Design System — Verified Knowledge Ledger

[//]: # (ob:4565936e)
**Status (2026-08-26):** Current cross-interface guidance for Proofpress CLI, Markdown receipts, review surfaces, lineage views, and governed-context projections. Product hosts may supply their own brand shell and workflow vocabulary, but Proofpress trust states and evidence semantics must remain recognizable and consistent.

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
| move / move-bg | #8A6210 / #F5EEDC | #D7B56D / #332B18 | Needs review, why, moved, attention without alerting |

[//]: # (ob:6b8dbcc8)
## Light and Dark Visual Languages

[//]: # (ob:98479562)
Proofpress has two deliberately composed visual languages, not one palette mechanically inverted. Both preserve the same paper-and-ink hierarchy, typography, trust-state meanings, and cyan interaction language.

[//]: # (ob:029a26dc)
- **Light — public paper.** Use Light by default for the public landing page, investor and editorial narratives, documentation, and daylight reading. The page is warm paper (`#FAF9F5`), working surfaces are white, text is near-black ink, and primary actions use solid cyan-teal (`#0E5E6F`) with white text. The feeling is clear, authored, and archival—not a generic white SaaS dashboard.
- **Dark — cinematic ledger.** Use Dark for brand films, immersive campaign moments, and focused review or lineage surfaces where reduced ambient light and concentrated attention support the task. The page is charcoal paper (`#15171C`), content is warm white, and interaction cyan becomes brighter (`#5FB3C4`).
- **Contained contrast is intentional.** A Light page may hold a Dark film frame or other explicitly cinematic object. The boundary must be visible; do not alternate themes section by section for decoration.
- **Theme choice follows the scene.** Public landing pages remain Light even when the visitor's operating system prefers Dark. If a product later offers a theme control, the user's explicit choice may override the product default.

[//]: # (ob:dcdb14ef)
Primary buttons use the accent as a filled surface in both themes and must meet text contrast requirements. Green, red, and orange retain exactly the same semantic roles in either language; never introduce them merely to make a theme feel more colorful.

[//]: # (ob:a8d606fe)
The launch film remains the canonical palette for dark UI: white `#EAE8E0` carries primary content, cyan `#5FB3C4` carries Proofpress and interaction, orange `#D7B56D` carries why or review attention, red `#C87E82` carries rejected or blocked, and green `#6FBF8E` is reserved for verified or admitted. Adjacent diff states use the same meanings: modified is cyan, moved orange, removed red, and added green. Both themes must be proofread.

[//]: # (ob:b5b71caf)
**The State, Not Brand Rule.** Green, red, and orange communicate ledger state. Do not use them for decorative emphasis, generic success, or visual variety. Cyan may identify Proofpress and interactive selection, but it cannot make a candidate appear admitted.

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
- **Status chip:** compact monospace pill. Admitted/current is green; needs review or revision is orange; blocked/rejected is red; agent or interactive scope is cyan. Never express authority through confidence percentages.
- **Diff tag:** compact inline marker. New is green, modified cyan, removed red, and moved orange.
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
- **Decision bar:** when a focused single-column review needs persistent actions, use a sticky bottom bar with solid green Approve and solid cyan Request changes. State must change immediately after submission to prevent repeated action without feedback.

[//]: # (ob:e693f5e3)
### Voice and Language

[//]: # (ob:300ee19f)
Use product-facing trust terms: Source, Evidence, Candidate Conclusion, Review, Admit, Request changes, Reject, Receipt, Ledger, Lineage, and Governed Context. Reserve storage or implementation terms such as event, ref, blob, projection algorithm, and lock for developer diagnostics.

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
- **Do** fail closed: unavailable data or invalid lineage must render as blocked or not ready, never as a plausible placeholder.

[//]: # (ob:70e00445)
### Don't

[//]: # (ob:755d7400)
- **Don't** treat evidence as synonymous with a raw source file.
- **Don't** use an unbounded force-directed graph as the default ledger view.
- **Don't** show pending, blocked, rejected, expired, superseded, or needs-revision knowledge as available to an agent or API.
- **Don't** make evaluation metrics, model confidence, or recommendation the visual equivalent of admission.
- **Don't** bake legal-specific matter, counsel, or data-room concepts into Proofpress core components.
- **Don't** expose mock counts, synthetic receipts, or hardcoded lineage without an explicit preview label.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2QwZDM3MjMwYTVmODdkNzA3YTMzOTc2NiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6Ijk3ZDRlYzUyIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9mYjc4NmVjNDEzY2U3ODUxMjFkYzJhYzYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2I5MmQ1MmQ2NDEzNjE0NzgwYTJjZWJjNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfetu5Fa23qtsyEB8plNVzTtZ6h9Bt6T2NI7HY3T3OD_OMaRNcrOKIxZZw4vUim3Av_IAyfxMcIDkFRLkfx7FT5BHyFprX7gpqamW5CAJUMaMJbFY-7L2unzrspd_OuJtXxY868_L_Oj4aL8_z53cjz3f4WGRxHnsxNz313EUHS2O0ia_Oc_Ljeh6eLfbci-MjuPUW_tZHqR-EYVOEok8XPPQicIw416ccZEVXMBQa54GSSzcfB366yCN8zDJ_SwqYNy87LLmSrQ3R8c_4R_9ec83MEPFe5xqAb-kooIHP4i2LEqeVoK14qrsyqZmW3i_aW9YesO-b5um2Lei6-A7e55d8o3ATU0et81fBWx3aHHAbd_vu-OXLzdlvx3SVdbsXmZbUe_KetPzepP4zsvJt1vxt6GE38-HTrTnWVN3ogZa9O0gflkcbQVHIq7jPBBZ6B3JJ-fiil4C4orzIo2BRFng-pmIk9D13DzzeIbU3Tdtj1s7r8pawMr1iVTn6drLQy-P4FuRG8SJw71MpFkst6NWd57xfTdUsGEP15k1bd4dHf_TT0dq-p-O4JSbtsPf5MciP0-B5P90NNSXdXNdH_0Ie9D8AFPnTda9PD378O6b71a7_GjxKF7hfd-W6dDDEZ2nvCs75BhRFee8A9L1gsYb-m3T4oIuyxqH7G66Xuzgk5rv8OT0whbw1Q5P--i4HqoKlplt4XiE3GBaNdklvM1FmDhRjLPDyfTiE25i5Al2KrpyU7MPNAn77de_M8lPImf_CNPA19QyeJ7T-vbIZOIannzFvnycSuQbwb7Ff7cwSH-zx60gJwBXHf2yGBcchFG49iPxf2DBL1586Hk_dOwfPMeLlk6y9KI_HL94wU6GtgV-YFnbdN2yhFlbOFLBNkOZ8xp-KZpx0Xve8smK13ESR3E8XfGfQXRp2jkCfsWs12ZoIjy38NIwf_QM72rW1ILtty3vxDF78YKzPd-LdsnrHPZ5yehc2hcvVuy1-iRrqqYFYnYzO45S7qRJ7D56PdY5Gip3bMcvBa0zbYY656C3KrEpQeqPGXwxF3gCvJ5ZT8bDPE3540_g41awXDKUFDNWduy6aS-Lqrle1mLoW14hbWBBvGKgWPIh62HBN2yOI0CreyJys0ev58ULXNHHduh69kYT4z0osBVw6WvWDZIvd_h5DTqsZeVuX92wfsv7mfXEThgBj07pc4IH3T3An-alWYl1_TgqvEeO_jP72FyKmv3Mvi032x5-nvL2En78pRPs53-uf14ul5P_wyPJo_DOV-OSyD5MyZ_kkRMVj90ukr7iQ51tWVFWO7CmO17WHRBXsIzXTV1myAO8En2PKqFlOS74L--O2fUM8dMwjd2MF49cjWQFVFhiwb5rgB9aEFrDDN-0QtQLWGO-YPi8aVH3MzDWu2FOVAT84wVO-ATaFOUn0AsFr6oUYAQIwX4PrECE-Kbs_zik7Pv3tABQpR0K0sX_-pe__3e2a_KLmQUVwTpPY2_KPR9v9s2m5fvtzQP8OXlxhkdDP00ynwdPmGUJavO0yQbcFlNjd2g1PjQAiEr24YS9xANq2Ac0RPj3NSAn9o1oLFNXASKbrCiJ43XspP4TViRZQ69pweCvmr0zVsuwCCxgU3K2Ka9AyabEPnOsEUQ8jAo-1erf8ptm6B84BfPSzAkkHGwGD_kjR0fqv4WddsB68iGSvoPRCe_SPMB01bCrJdk5MOancjfsbKG8Q30nASjur5NHrkZS_r2a9s8AF1tD7j-3JZwGR3DHfvv3_wGNxb7pSvN3N-z3M9TP_SjIgjyerOisEldyxH8FwGffbx84iPvenzmTiMeAtCL36XPaBr1jBTgn6HPkouBD1a_YH3nZInJnLRCpW0j1_TLjbQ5nNqczC1iYlzpPX9h3TS4YYGtwa_AbaLGBh4A7-utm2RLT3PAalBewFtvyqiHugeNn2XZmYe46EmEUF09fmGQhiYSlYj_l3TZtkCaalT6A75T1Q0v6HGS3aBtAJnU-s7AkDaIid6cM_WEL9H7IxJuX5tSnABvm-_kjR38vPa4FIxsNPw2ca5vrThqurhlahDRg59oS7Ku0uqydhZ-pE-YieuRqTpq6FuTuMQ6kRUbYg0lDk95vO6k96gY-g8UhETo21BVydl7OrSYM1pErsvUjVyP54Afw19FzvwP28MNML3iBILUva8lkdTNrTv0CPE7nln3f7QFfg1l-EO5ZL87wg-OBaxv56yfMggpduWHZttyjNgcm33OE1U3ddHs0YfuyQtid70qAWvnLTPlnMwo9S0RWpO4U13zbIGL7VoYO2L8FXE_DzxMBzNlnvzaHgoN1mAnPee4CwNdQr-MD1KqgpgCG7oETKMjTk3eAPLsAVuhBpRWABZcAw3ZzLsk6jWLfT5-7vJOqzC5RfQLquxQ3pLeWcHglakB4zGFNOWLFFhY57HOMVsFDUPtdOcu2ceRFt-3x45entOvki1qk3osa7TXC-W4HKBZEihHYIveJ8ZnlOWkexOv11KN4T5NKiM7-xIGb6wdZ6zPfmeGrOIwTzwnTZ039ceLCyMes6-XhtPRZXuJZAZSthQDVp95B4DJHGM5FUMRu9KzVnWGYE5xaBZ7Iu5WutgD_difykpwgjCyC2KMiKGCN6IQcszkQkSGmSoL71oaW57QsCvY9Bw3T1t0XHtx935vTk37mRF4inr0E1JonFN5jNDaqTYVntij90pB1YDvrvswYRdtwAg7aZEZrimjtF6GYOiE_NGUmv_0tTDhgvPgB4tz7jRmy-I4jhLsunjEtBglUOGYJXg-qHqkYgZS77hicM4QVC3amEMeCnRgen40kpTHws_uMlZ2Ba1J2W9TcpGokvqnUN8ld_ss7ED4EoYCBTr59xwB27gdw5OYkLXXcPInTqf902nzdSUZq6q8ftO533545o7xwC54L99Z8D7HCafPA0ad8HWRJ9ohhpQMODI9-hmiv6OA36HOAY8swT1I1HYJlgskwalYNlAUBl3yG92NHOE4QhLdWApR5eI_ypVmtHeZx4DiPG1zuFF6Czfbg3PZW_LNj3Q0o8JtdM3Ta0235teav4vZOf1zoJMfRFRrfpj7PcEiakj7RGQtxHgZF5Lt-unYKkfqYVskFh-PHpEPTEzuqPIwBJ9lWZJf7pqx7Siu1NBPmIfRfmIb4ERM4ABhurBHspI41CKWLnpjv6ZqiPy_gCES7b0uVVupS97jIHD_KfC7CFFBxlnppzF035mEB3oPjBusgiUSaAENyYAZXwKad3Et5FLlJEXtoOdBIUnpIntZxEP4ChMbEjc4h-O5HJzwO42Mn-deOc0xnriiOYhQGyGU-cMf49KffLaNE_CYzPltwI1FPxOvML5JCJATPaQwrCaRY8ffN3aipeRSDH5TxrIgCPbWVzlFTPycL09rLBs25AHjRXubNNTiMIhPlvu8WBt7IYDk8sAG18jo3mFqtRb5U0slUChSOp1vhJBTn3zZd31HsAIM3FGcXZctwOhlO67aiqmhAnTRgV4A906ECX27B0qG3FywNlIZd8CUj3dpwdxL8aB8Y3OdNXf47Ejx8f0RAq3sshTqFMPB8NwgD7mSGAawUlWaAh3JP-kyD1AOJC0ROWWkazUpHqdGek2eSx7QAH-fSPMRhVVwbhsVIzTKtBiBCliGHyNOTKSROh7ZiHzT2oTE69Jiztkzh1ImXM4ktcUgb_r7CI70hDCzzKTmGLOjdGRKvI8_zIvCABQXSiShWTuxu0vLRya4cw-aiIhbAgHpOS-oQqBMvgpoE_T_C9tHqSa5rauBWqXuX6F5XJcfo9QA0Yhzcakoc01pgcb0RB3ap5X3F3tXoUkqywbK6sgcxQPPbSX8JKEXFBkD6LfB9v7VXwVIB3wb4TvJDHgAKBL5kdpnC_oGx1ZujLVMiuoddI6xDydIv0VYE2DB6OnNCXhrEoM-z1BdGFVlZQh1uf0b6r91wEE2hlmceEL0WGM7qMb6HG4EDAlPdNLtXaLIBwvA2294_WEnhU6WLQJMNtRxCm4QV-wg6SZBiQggpo4TSh8NYgMVyYAl3ZY-h_5X9GHSXxKVXZTfAnia4VBiwfB9njap11LUjL3UyU0U6TpCqGoVYK-BU9NdC1Dj_bubwAOX6Iffz2M9SY8LGlKqxI0_PlcIOAH-LK15haA1dhrIGxQraAyV10wKvLzCTcI8MLjDyAZvdULSjQkmWJRtwfug2o6RlID7faJHSFiYFMQfak2TyoleRCPi0KDcDKr2RlhskfDeAsgNXfI7L3cCJ_LQQBYXKiVBWrndU9XNpXDUWwIsiKniaZk4xGm-T2VVjPS9p-_b12_XbEH9zQzd2T-C377nyVCkSswS-uwKoi779psVDpUHRNrCXZCE89dPHUQBAeN4bePJV-Do8jei35E1ytsaRvzpbn8VnDj57Hb1evwnwN7CDb5IY5wXxQIZ5CToNziCXvwMwF5jk3Imek9jS7JTBwAH9M_d0TROfeG_9BH57L_MaJlKrdFdZU0jMKPkSWIOGotTHS3YNNCeC0D-4sLfu2duzhEhzCtuK8RlsLvRO4RmGvpDdNKSBD_82lKLXcUHgSJx1iyynxsbJlLV8qX5ZIk7GGZyz8CyiWWFHZ28dfBa-feOfEInc2I8Dl0iktcaCibwEWTb5lAWKBiHEhW2F1bQ5bhH-vUw3RKyz-DSQ08VvvbPX-Cx6--ZtckbTvfHBlsIzgznJK1C6BcO_o1GCZ5Ksm9vCRROjsL7Ef6uJ34B3578m6sbIDPjsJInPEmSir_zXnu_h3t8L1LZyK6ARSviFYDU-ASQGUykuxF_hm_hDzZC8jjyXWOxteHZ2Smx3Gr8Jo1OawffeuHim31khtQW73t4saBBM3feI5pB0Ov3EK9FSJPXn-0oclLA6cZaBq5KmTmKE1ap6sMzbUwsatiU8uvjq7PVZcuZcIN8SE--V2BDdMfdMWbQLxT7je5bFkfJgeGShSxUuFKXGLwFhULkqI2NIQ1UO8Lo8uvH1Vp0bfsccmFQlaGQuFJNdoFFXkYOcdnmlOQ3lRjEZZhv-yklecgzKKZSOMTaK4vAdmBIBVhqT_4b7cWikgDpPtbWRbUx5BnmPcmErsFb9lmygUHg_pZBGU2A-e0bdR5EIXceNfED3-tSt6pKJXXxa4QjCZKHAuiTBip02BC0UJXaSTxRKBnkQu_0WSxkXbCMA5IEJJcOFSgNJLVHGFarA_mbFTpBdEPIg0ABMc_NZTrkStrpBTAvgCLgW10IY2oa_fL8HVDUe5ox3lGRBERRJ5Du-8WfGmhhLcp5R7rLA3__lvyJTyN___t9QLV1IiuNn_wUgyfUFsAJ6NSpSiGEszEmo0YGF_loyrK0FpYR82TfyNSSh1Oiv2H5oARDj4ODqwIkIABet2FdkJW7AOQVkjitW6qZrMJvUtGD8UYpJocHsRNOyQ_bDQBMHG9Iip6_YBfm5-Cu5VccM3TCQqFqv8rXKr2uDiYqhbSqFc3C9yjSUGXoFo12HIdB3Fz0t9qUcp2MYvOpe4VnnjZArU0Pa5J4Dj14RunmSO7Fj3F-rxmjERA-VDmmGyfg6BpgFfrDx9axqIjXec4qEsEbnJftYojr4DhTf-wa9NM14IEdrx2HXAvHWgg175AMPFMxKDQUsA-ah7LZCspH2FVD87BqUVCD7ik8csK7IicTq6IGzK1RmMLCgVMwYe1FbWf1zjTuUmgRYR8k-_mWMM04Gzr9VeEQ7vL0vCpvQwq0duuFvv_5HN9l_AkK4q4j-WiXEuR0oSI4r1tU-6AOVnRYaVWrCrihGj18AaI6ArUMnrC4LIE-jAExDBQZ73nUAOuHZ34ZGppy6hXI9l7k-Q9qMlFcSgSVZUO0trQjvtmKDgR51Niq2AF6ZXC78pEwphRgYMhjrwMJXOWavKuU0oFCCrwj4Xzt64CtfYY6Ow7fQRSB5xdLvugdfVJ7DiRYyUuB7FHwbHuIZ1PKElFvb8bpbSqoDNbNLoLiHNA4VxSXB4xX7RyH2qGx7IkrNr8qN8npg_8AUVi2HwZ4K82KMQGjjvRNYjI4BLXvqRimDTke4Ct6RXutAlau9_SCDpDAoCiCF7xqwSjQNkB8RTSoqNad2RHHHF0O5NBUEoGo_vP0T_LV8Lw9pwf4k6qpZWEUGxJ4XvYzWLeth1128Yq4DJJFTmKIh61AHMDRtxtEWquNd3ZNiUKojT9wsd7x0Ha65Vh1W2d_EXj-tmk9L4uJ2GY1yQ3YUT5fsrBUBFRSM3Gc4DnThVYk2-rTsQCffKCmdqJeyrzCe8GE8U8l9SvWomMaK_ckQWXpU5uOmMICiE_1oLdCgyA0Cgw2tZVBAFzUML9lokSSESJl8cL43YDV5uaMBzMnOWAdnDf4yKG8RBMZjtuoeR-swV9KoLU2eCD_JwfcOxuMdqxwty_DUAsYyh7-bgsURciXpIiQEqTcsVYIXtI6IHfCbOCInkB-pnpDkDZUojnJMCX1DW_zDitnhn9Ngh4w6kz9Gn5rYHf5hAoBScFVaW-1BhhoxkIHb5ayoxKcyvbtllLE9L1v9PYm6wDEDjeQHAWxbTyMPnuQdvlGLSmmrW4FH4nsAZGapEoICGMkbsHwgDGq9skhEhabkIslbR69SRiFur813aFUeHobRfisqBwXMXJAma6Up6GRIyqSfiWBjBvpkSnQTKzqR7qw8Pw4KPQWBY56LZGiwWqXMJbC6RiVR9kbe4REIe9ugbgAZ6NHQNWNBqjmibo8phCvaL-g4QIdg_NsG-E1ixwQ3t5BGwhyV1O7qFLSRwX0TdLOdAVlOM0ZDNOWu0KdFck8Y6BbraV--A8yL77waE77kiki4oWqOJGebfaE-EGOclAyCSQ1pi0XYEnyJptIZhqzJleHNSgUFdAaGNAyco_J0V-zsE2hQFGIO5g2GBiSGxVmIQGCzM2Ygi-Mw4U5exLFx26z644kZeHppMWYEbKnU0ozyQhHg-zLmyOGglASczA7j6zlohrIy7paMnTZIDqlICMlQxJW3G7JXc-5qsC5Sj_N1krh631aV86hrv7BqWQ0b-K6_dkInzBwzrFXIfE_y5bGFyWCTAJdIvpBxtmuCIqMtZNsSzB5YzhsUA8WjWFMGEI8Dz3USugLPX97cFR0dSBP5korlRhe6qBoJ5ZQsoO8McBUYihKglIVEpA5b4ZQE0PF1dJqruyAWd2UM7obcdQL4Yw4G4yaoWaXk0nJQe6LYjItBssiNzRx3GnAh8ih0nDQx0Ymxjludy3PqsgF84wu0yBzcirqT6do_UtwTh4KDq7tK6opJKEFnIOi7SD2sNgU29pRd1WEYkA1UFgD0SP5BpwwZHNOuodUCPxWgZ2pUf58nRBEWOUC8GP5vGNSqG5_I-9PqwMGU1puF5l2tpklEp7j4t1__jicPaA5QASIJQaJGJk4WZsMDgAPAEn1Jg02DO8AVefmAw525Ii5CzrOQMsISBo3V6KOYzxWaq7GE63ph5K3dLDLOu1V7bgronl5WjnxHzNBKIxuDRUe_EzdaktRmtnOlS5NH8UBvFQEAvqrxwi3QNMq566k3-agFCLsgnQmfDZgI0tx5rUtc5R6KARQKlkKraIrUKaZ0uqP4JamBpdEMRmi12pjT0IEI4ih2Cke48ZjHNsX1pq776XXzSsyvye9t0KW9LjtMBDK-S8vN0AwgvxokLftmaWGCbDqv1MRdUwEGIs5fjYBKfZPgg_U1GBTlnaIiJrmm8-7HeKignVG15xjwBqSlcs4y4jz5RAWYJQjV-QLJaLggGXK2cntmvhnyuy6P08T109gx5LduE0wUxdMuCuTC8tPhtf2NCjNcgZmXZSXZWHPLcRcr9p0shECcw9X28KSlJ3Yn8yLJcwuEg8k1pLRyKZpu4tO-JOcT2BYUk8jxd2Tma14S8-pGBnO8u05EIsJ1kHvxGOczlx_s3Of8nQattdd55Oa56waF8Qytaw6WN_fU2wtAFGKTV9MSa5Xx0HST8fhXmmwvTZaDshj5KzglHAy-NQmVw9kKnY3QRwhklnF1mZ_uMR7bNsNmK7POUmViPAPB5QYESqJpKkqGB_bmyprQEuJeRBTfyZsJG5lLMNkQmQq5k_ywcyNqjrNpEQhOhSwkSUKMqTHtUAMQlSp0ZLAV-zDsYDGyZqKTMn0L1XS2Hcjghf4VOFGEhMivwIj61lShUNgbWb4Adr6zSEJJoN5wnfgCxuOIYXWsVaYzsGrAJJdU2GphrIQJNy7GKgNdNiFrtbMKsxgtGgUd7S93WBdPBKGdaNcwbfoewAAqQpTwHn1QsO8Ee3KBwqeimBK6gAVEi6_jh_dUd1BUQi7Gci8s20okXNyphqAD1la2JG5ZsXd9NymzmpS1YTOTsgaiEZz5TPmFVQOFZRrD1I2lkcmQHuu64JqmnK5tOrbOK49Vd0NRlBngm0ypRRCYCh707PWefGn2EtA9OKOdQp-UeZfpYqrFU45qZ0UiZNzDGPtR0WoY26QdKASqVyeGRyij9vXa2CiF33BzJptjxhwBirQ0tFZeaeCH0EgRX5BBkF9b6LTelliFsqDyeY8R-p7v9ooN98g9S7Jlqo_MiuppKKvH4N2OsIrajypWQoa30oaoHeCMVbmW2t83ny-6lLqm7vlYIqOz_wTDpArFx4hzMqKoVav2RtsYy4DPGhuKnqIWXhrdaxU6Kb-YuJUPeSkFEJ1i4xHrjKM5X5BXDDZ0WLdNVegd-GCt1qnyOgKTh3Js1bKjwi_BrUHhMTpEthNajCrEjlDAoWy2FYaZMM56RTlJFCTD1hhPV-hX3qRRDqoVD5IFdsA28JVR7wiKvKKtn4lmpNk6dCPhY1moqawbL98Zu_vIa3Q6phr4SboOgjQvjO9k3axToz_njhwce081ewTpwTlWCSSlb7VnbrHD1x0dBNX_XYHqp_KuN1OLQ54Bfgc4fCMkVFJlFnc0rUwIFXTmlDijgmcVIyf9sbyLVu9HXzP4KAnDtfDyeO1Gxi2zLgFqbP-M63zyKtYIL5UjkMtk10Kn-EvUQsqyjOrdCuaWY6HpWPNrVHGNikIX-RqLDGhHFbIo0_8pE-2-13WipFpNQSmqr_Eg5FdH8GV03J2KvXES8QmNvCXfo-ay4rFaZb2aehMYSdOlNzaToj65Ilh_AyjHaJK5er8885N14QueOCPmNTcnp5GFJ92BrLtrjBT89ut_wmIcrDbuMdk6KezVNZ7_5rdf_zNGRfHINLC0SjZkwpCUMaG3TuB2xvKSkYQqSpHegJzJUAbRHJintbS8WqcRLZ35lcH6ucCUH3IvDP3Q9cf463ih09JYX347U3twvnBd31vH6yAyBZjjhU2rmuTpty8VUy2sjzpVFaVN3FgAhaxOb0w0mAxU1zCiMvpSVvemKkqp00lRAOtKKjvBzDlCyxGfi9yGiCv2Z7LXtbVU7fJYS0CTKtBjeYwSC9wgE4L7BY9NTNG6cqr7Lzzj_qgK-LF8IFxBdbepUr4LTNhfG6YkhNi2KggjFgpsaRyHugyLFq8oVKtKrMln_xzwUkaY4KQcpCNLpGQJHwHAHOTSTXm_OquFVlwLfTWEdBbdcVmx7ytQN0tT3I2ev6SLRGfXKOxbQnodadgVe4v13584ArZjlP-PMmGLOQ9U7VUl93glpEZoJS6Wtuye49YKDxRzNeQUUO3LigrgR19Xs9MKNMlMmCTMMx7leRLEptjRutt7V36_8JKuhhxhFDlx5gaJMGlc696u5fg_9QIuZgQxgwDHAiofwEe-rMBBr4xTAYRSQKypKr5H4bWSNJ3Sdzqqr0mLcV8yGLoohGqjyM8bVzdZ0UKF8vWVmzHBocOKyCeA9LfoDwMTvB4DMpQ5FAvU-fDBe9Uskf3P_3E3akMvATvRe11TXckTVjVE5EtTqbJ0byj7xGXZsi7aJ8rVIwjQe-MFmPdcIjCCLjwtK4QTVpW_9H4ZAmXKC1CNvg5taB8q5TS7NNsy24B3kSgrv1SpaaWEpdq1EI-qYVloCsssj3LIU66AkB0X1O7kGC-kJMct33KlDA_tRT4b1ZcJLI7qCSEr3h2VPLGnu506nqe9M63oZgB94mCbUp6mIjagwroXbonXl17z1vm_2E8KN8t4EBosb938VgM_5yL3iaUW36vqagq7LW7TdqHcdvypNLVOvXyr9Slu7G4m3qT3QNeiKm3kPRKxM74ULdRIDZ0H2oaCQp_pwsaKvNpgIG67U3k7FAVZTwvqAEtpQO75pm6Qp-YgjQAvSYAH5uYJH683mavr2i4-4yY6pvyVwpkmNVZjbZL0k0EJ7UejdfE6y8S-X2oOuVhIcThBLNVRnE16P-hQkFsliO_RTlo52_EWJYBDgZhZFjlYXDB39o85YphARacw-kDOh9453gRRZb-cnDS14k5dtzA4YzZB5obCiVwgGB_rhKzb_GOk-ovu5xtk5HpZnCRF4hujaF3Zt6T2czfyddybJ4SO42AUf-uS_qS-9Wl38G9f-KN6Lttpgwd3wpxKX-OUlxhb--wtrfvvaMmrj8jOmDmVB3_79qP2vbRjYs9JFeYmFmBl_0YvmSrf9M1cQcUh41WBe3xbo5NbUObkctfyrurUQkkiS1DImW5KbC17hLFoEyRb6qsllWL4-zHiHeBtTVmJXuUSzc1ETleedTWAfeFZurdSYHAnt-84LyXKNLea7YkKcHNlqXt-bLu98pokpTXoEo4J8dyqx7EScbIyhec3C2X6KYi_r_ggcTcFTrdNhYVCM-U5qcuj2Il9fz36cGNviIkkfbbvgx6rSMTa4cLnqT_6g6YVxESYntbmYcxO6BEIhdRASp1nAI7DIhBKvhrm5dNyaeWSINfcGo5cnqck726FU0e_HU_FDpOiEOoc1uvv392anyRvDPljsWILLKQFfcxcqUrQSebduthqXZzAvIhJx05nS3E2ut27JCNTgHLRd3cx4QEqQNZEAHMu8Q4v6TYwcJ0MRFicn-kLyjLZeGsipSB2aPEpk4JVQDc1LBj12XihFgNSoF0wbz2KgLkbZkFi1TVE1irfYe8ff0GuvKfLOXrzpsc5HcMxzvXp6Efqm07lLvd_eqs_-p1PCW-N7dPBShzDweFmsGv8__0-6qT-n9pGPUqTPM2yW_3JTNk_XYL9QTKeRj4PdeN5-Nsz_WXW4Ayvw8j7vdZj8fEWVcV1M71TRHyNLtKta-N4SWCub5q35l6UZ7_XMqlul76OXUr2QwqyoKrcQMbQlZCfjqV-8koIxjKGdKYZUJ7lqRuI4vejp7wnqa5SmHuE6kouGSrQ5dXYAAMr2FO6GHibniBdssj9cxx5axWqZc93fKdyCtPTnMDsW6e5-hyT3T_Fh16V_oMJu0WsbouRTQTTql4Ug8TmxpW6l7L6HLPcP92pKKjy_dZUSNsOyKouYqvbQtMyzp6uwpJRW-5RpepK0M9xwfwK1DXYpTxeM5eK6OnMXjdpScLapiIK_2jx2E9H19sbM7De2dRW22w-em9m--pt8JwFAs1M23b9JhhxjpKrzKNMF2M9SX2Fd6NaRQ9dq4UU-fLOUTP_6Q5JMrsllN0OyW4T9dNB5R5U7v9rKvfLW6TdaRH2y_0NwB7qhva7tDwLAhHm68RN0jjiAQ_CNPB8v0i9xA-8IBFinTtFKMK174W8iAvg6LRIRR4Ix4UvhJ_Zz52OZ9Gx48P_7ul4Zv5LP4eOZ4eOZ4eOZ4eOZ4eOZ4eOZ4eOZ4eOZ4eOZ4eOZ4eOZ4eOZ0_qeMYdEaciLfLM9UYAYiIEVuOGp_j45saym4JCcHM_NGrYcvvvopxHO-5NL2Gj6rmm26TIC_xYPEytyKhBmMm0mqTiFGCaK8gLK7C2mCTgdMMyVSJ2wycIcuxmM3OXlTueC94i6Fgx3ooyEQYrofX0GAG-rGJzbE8BKx2aki6D6dxj2p3AhibFCRp13MhaK6tRkKARCeTwdqf08j9cKL188YcFoZmJpkFkQe3vFgTKqR4SAAzAceyJAJTXhXtSneqONhSFNLU9yx6rmmAiqXku_iBzebKtniwsoR5jAhgHK4Q7WYO_sBuzWO2AVIUsNz3W5EAfOP9A1xQpI60zTsj2eA63I4L6LOgFur5KHh02NsJ2Pju8roCqJuO7PUeEuGuo2Za6jDrpYYKQQGMcQ7nrrUBYK-9M0wVPVMaVEUhKnWGklAqVjB7Q6J5C1by7nJ4bZpCyhvo2qbOTlhTPTvVmMMerju1Wx0HJ-KmQd6hT6tAhR1JdC_9gtVWaBo_lNRa1UADGhLMkL9P6EMpighlORlIVm0QVrbodRvddTcYONYM5kSZFDSx3atwifQld1Y2a62ocC6lrFGjVNLBT5UTpjfnV7spnspwf8XWgoOqNhd3gVCkQhstxN9_fFT_TnEnuE-Ngsk5Ol7SCNH7d2W2npCMhL8d3RAjwpQpMxSvEjzfygRwFfc7lLvQ1JukiYbrw627Mbqo1k6sAWrEt1TVePaIJ3382re-7aeblWRKsA6PLrZCj0eVPDxrKszDdA3ZC9EzfQJbco_7L2LJl3ec6L6q6I7pioFrmkbY32QPKG-C0oiSG0mr7lQb5SEcqdqb-jCDGaIX6RrdJlOSmpmM76VICNC6Gaq5N0qG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6KG_6P-3_UV__OV_AzjMboI)
