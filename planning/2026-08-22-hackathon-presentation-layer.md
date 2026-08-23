[//]: # (ob:20c1dba7)
# Hackathon presentation layer — narrative product demo

[//]: # (ob:e13b8e72)
**Status:** Draft implementation plan for the presentation-layer PR.

[//]: # (ob:788e6d89)
## Decision

[//]: # (ob:530af484)
Build a guided, real product demo—not a separate slide deck.

[//]: # (ob:a6fbf8db)
The existing verified-knowledge-ledger demo remains the product surface and
continues to consume the backend ledger view. A lightweight presentation mode
adds a three-minute narrative path through that surface. The presenter
can follow the path on stage; a design partner can ignore it and explore the
same controls, graph, ledger, evidence, and receipts directly.

[//]: # (ob:9d649ec7)
This avoids maintaining two divergent artifacts and makes the strongest claim
honest: the story resolves into a working product interaction rather than a
mockup of one.

[//]: # (ob:82424ac8)
## Product sentence

[//]: # (ob:234ae578)
Proofpress is verified knowledge infrastructure for autonomous agents.

[//]: # (ob:c70c3949)
**Cumulative knowledge humans and agents can verify, govern, and safely build
on.**

[//]: # (ob:a210d415)
## Audience question

[//]: # (ob:b9ba5238)
A long-horizon agent finishes a task with an artifact, multiple versions,
experiments, and hundreds of traces. A fresh agent takes over:

[//]: # (ob:3ffb28dc)
> Which conclusions can I safely build on?

[//]: # (ob:21a66f6d)
The demo must answer this question before teaching the audience the data model.

[//]: # (ob:49ac0ede)
## Build Day constraints

[//]: # (ob:0c15ae22)
The event instructions require the presentation and implementation to respect
five concrete constraints:

[//]: # (ob:b3e4a788)
- the demo is three minutes;
- the demonstrated increment must be original work built at the event, though
  it may extend an existing project;
- the project must be open source;
- a project draft must be saved by 7:00pm for finalist selection;
- the final submission is due by 8:00pm and cannot be edited after submission.

[//]: # (ob:639859b2)
The pitch must therefore name the build-day delta: the existing backend ledger
and graph are the foundation; the new work is the event-specific guided
presentation, trusted-continuation interaction, and integration story.

[//]: # (ob:b89e8624)
The event primer defines long-horizon work structurally, not by wall-clock
duration: many tightly coupled decisions, feedback, and revision form one
coherent trajectory. It distinguishes H1 intra-context reasoning, H2
cross-context continuation, and H3 cross-task accumulation. Proofpress should
enter at the H2/H3 boundary: it governs which conclusions survive context and
task boundaries.

[//]: # (ob:7bf705f0)
## Three-minute narrative structure

[//]: # (ob:92908d5a)
Target timing: 20 seconds problem, 25 seconds stack, 95 seconds real product,
30 seconds trusted continuation, and 10 seconds closing.

[//]: # (ob:0cd1ec09)
### 1. Cold open — the handoff

[//]: # (ob:ac0553a6)
Show one completed artifact and a concise handoff state. State the scale in
human terms: one artifact, several experiments or revisions, and more raw
events than a new agent should reread.

[//]: # (ob:43427c4d)
Hero line:

[//]: # (ob:37d07198)
> 100 traces produced one artifact and three claims. Only one crossed into
> shared knowledge.

[//]: # (ob:946a0d38)
Do not open with graph terminology, hashes, node counts, or CLI commands.

[//]: # (ob:e7c318b1)
### 2. The missing layer

[//]: # (ob:e8da70eb)
Show the stack as a dependency, not three peer categories:

[//]: # (ob:305ab25f)
1. Observability captures activity: logs, commits, tool calls, traces, spans.
2. Memory and ontology organize context: what is remembered and how entities
   relate.
3. Proofpress governs reliance: what may be trusted, why, within which scope,
   and under whose approval.

[//]: # (ob:3fca7b53)
The short spoken version is:

[//]: # (ob:4d2280d2)
> Observability tells us what happened. Memory and ontology organize what it
> means. Proofpress decides what may become cumulative knowledge.

[//]: # (ob:661f5ff4)
The memory-layer example should be collaborative, not adversarial. Stash helps
agents learn across rollouts and accumulate useful context; Proofpress can sit
above a memory system and govern which evidence-bound claims become safe shared
knowledge. This is especially important because the event primer names the
hard memory problems directly: what to forget, context poisoning from a bad
summary, and multi-session consistency.

[//]: # (ob:1ae5eeb7)
### 3. From activity to knowledge

[//]: # (ob:76366fe9)
Reveal three candidate claims in plain language:

[//]: # (ob:c9eed237)
- one current and admitted;
- one unresolved and awaiting review;
- one rejected, expired, or superseded.

[//]: # (ob:57008899)
The audience should understand these states before seeing their implementation
details. Color communicates lifecycle state, never universal truth.

[//]: # (ob:2f49b287)
### 4. Real product interaction

[//]: # (ob:79acad14)
Use the existing workbench and its real ledger-backed read model:

[//]: # (ob:2e2f68b5)
- select a candidate;
- inspect its artifact consequence;
- open Lineage and Evidence;
- switch among Graph, Ledger, and Evidence;
- click a node to inspect its receipt and review boundary;
- admit only an eligible claim.

[//]: # (ob:41a25b90)
This is the center of the presentation. It must remain usable without
presentation mode.

[//]: # (ob:d3e70d2e)
### 5. Trusted continuation

[//]: # (ob:59aade6f)
Show the fresh-agent context before and after admission. The new agent receives
only current, in-scope, non-expired admitted knowledge, with compact provenance
handles and the ability to inspect deeper evidence.

[//]: # (ob:7d479e24)
The audience should see both outcomes:

[//]: # (ob:61453f8f)
- the ledger preserves the complete history;
- the fresh agent receives a deliberately small current-state projection.

[//]: # (ob:e7fbf9f9)
### 6. Ledger versus graph lifecycle

[//]: # (ob:28a20ff0)
Make the pruning boundary explicit:

[//]: # (ob:3f099f98)
- the ledger is append-only for consequential knowledge and lifecycle events;
- raw telemetry follows retention, allow-list, and cold-storage policy;
- the graph is a rebuildable read model that can hide, collapse, or archive
  stale branches;
- superseded knowledge remains traceable without polluting the default view;
- legal or privacy deletion leaves a redaction or tombstone receipt.

[//]: # (ob:15c1e725)
Append-only must never be presented as an infinitely noisy hot graph.

[//]: # (ob:5621c4a3)
### 7. Where it applies

[//]: # (ob:29d707ef)
Present three different kinds of proof, not three copies of the same product
story:

[//]: # (ob:f3135bb2)
1. **Harvey / effect proof:** evaluation only. It answers whether governed
   continuity improves a long-horizon baseline. Do not use Harvey as a product
   workspace mockup, and do not claim improvement until an actual evaluation
   establishes it.
2. **Finance / product proof:** the primary workflow and admin-workspace
   demonstration. Documents, calculations, model versions, and analyst review
   become approved assumptions, risks, and a navigable governed knowledge
   graph.
3. **Agentic commerce / extension proof:** a different telemetry visualization
   showing how the same ledger contract extends to policies, orders, payments,
   fulfillment, disputes, and other domains. Do not repeat the finance graph
   with renamed nodes.

[//]: # (ob:e73d2723)
Then present the current website experiment as the collaboration extension:

[//]: # (ob:1c05f044)
> A Coframe or growth-experiment team supplies OTLP traces; Proofpress turns
> selected conclusions into a reviewed, portable verified knowledge graph.

[//]: # (ob:a454d673)
This fixture demonstrates integration and design-partner motion. It is not a
fourth flagship vertical and does not imply that Coframe lacks memory or
experiment state.

[//]: # (ob:c34613a1)
The event primer identifies Coframe as an H3 system in the wild: an open-ended
growth loop that generates variants, measures a real reward, and keeps
optimizing. That makes the complementary boundary concrete. Coframe owns the
growth loop; Proofpress records which conclusions are evidence-backed,
reviewed, scoped, reversible, and safe for a future session to inherit. The
demo may connect this to verification, brand safety, and rollback without
claiming Coframe lacks those capabilities.

[//]: # (ob:5baa8eaa)
### 8. Close

[//]: # (ob:f80fa860)
> We don't just need smarter agents. We need cumulative knowledge that humans
> and agents can verify, govern, and safely build on.

[//]: # (ob:3f93e8de)
## Interaction architecture

[//]: # (ob:e2b84362)
Add presentation mode as a progressive enhancement to the existing page:

[//]: # (ob:91879a6f)
- a small **Guided demo** control starts the narrative;
- five timed beats highlight or scroll to a real product region;
- **Next**, **Back**, arrow keys, and **Exit tour** are always available;
- a visible 3:00 clock makes the event constraint operational;
- the tour never disables normal product controls;
- direct links can open a specific beat for collaborator review;
- reduced-motion users receive immediate state changes without animated camera
  movement;
- the page still works from a local static server and without new dependencies.

[//]: # (ob:04f70fd4)
Do not convert the entire page into full-screen slides. The guided layer may use
short, viewport-fitted interstitial beats, but the graph and workbench remain
the actual product UI.

[//]: # (ob:c5872ea6)
## Data and evidence contract

[//]: # (ob:5004ef0a)
The presentation layer is a client of the ledger, never a second source of
truth.

[//]: # (ob:9ca9737d)
- Continue loading `demo.ledger-view.json` for nodes, edges, states, and hashes.
- Do not invent admitted states or relationships in presentation code.
- Keep static fallback copy only for `file://` preview, clearly labeled as a
  fixture.
- Keep integrity, evidence support, and lifecycle/admission as independent
  dimensions.
- Treat the current growth-experiment data as an illustrative integration
  fixture, not Harvey, finance, or commerce evidence.

[//]: # (ob:43062757)
## Implementation sequence

[//]: # (ob:372f417d)
### P0 — narrative shell

[//]: # (ob:be5ab015)
- Add the tagline and handoff question above the current demo.
- Add a guided-demo controller and five timed narrative beats.
- Reuse the existing workbench and Lineage / Ledger / Evidence explorer.
- Add a final vertical map and closing statement.
- Label the exact build-day increment and open-source repository.

[//]: # (ob:43cb1ee8)
### P1 — continuation proof

[//]: # (ob:3e31c02f)
- Bind the pre/post fresh-agent context panel to the ledger view.
- Make admission visibly change the context projection.
- Show the source pointer and decision receipt for the inherited claim.

[//]: # (ob:b6ca9525)
### P2 — vertical fixture packs

[//]: # (ob:d8c7277f)
- Harvey: report only real evaluation evidence and label unresolved results
  honestly; no separate Harvey product UI is required.
- Finance: adapt the Apex investment-analyst artifact into the primary workflow,
  admin workspace, knowledge graph, and receipt contract.
- Commerce: build a domain-extension visualization around telemetry flowing
  into policy-constrained trusted action state when a real workflow is
  available.

[//]: # (ob:3144a33d)
P2 is not required for the first guided-demo PR to be useful.

[//]: # (ob:24a9c758)
## Acceptance criteria

[//]: # (ob:4ab84b40)
- A first-time viewer can state the problem and product category within sixty
  seconds.
- The complete guided path can be delivered within three minutes.
- The presentation identifies what was built at the event on top of the
  existing open-source Proofpress foundation.
- The first screen asks which conclusions are safe to inherit; it does not ask
  the viewer to decode a graph.
- The guided path reaches a real interactive Graph / Ledger / Evidence view.
- Every displayed lifecycle state matches the ledger view or is explicitly
  labeled fixture copy.
- The default graph excludes stale knowledge while preserving a discoverable
  supersession or rejection path.
- The product remains fully usable after exiting the guided path.
- No slide or interstitial scrolls internally at the reference viewport.
- Keyboard navigation and reduced-motion behavior work.
- The story gives Harvey, finance, and agentic commerce distinct jobs: effect
  proof, product proof, and extension proof. Growth experiments remain the
  collaboration integration example.
- No benchmark improvement, universal truth, or unsupported design-partner
  claim is implied.
- Stash is presented as a composable memory layer, not attacked as a
  competitor.
- Coframe is presented as the H3 growth system; Proofpress is the complementary
  verified-knowledge and governance layer.

[//]: # (ob:e5df1989)
## Explicit non-goals

[//]: # (ob:398cdf34)
- A standalone pitch deck with screenshots of a separate demo.
- Replacing the existing product UI or graph implementation.
- Rebuilding the backend, ledger schema, or OpenTelemetry adapter.
- Adding synthetic Harvey results to make the story look complete.
- Presenting raw observability data as organizational knowledge.

[//]: # (ob:39046702)
## Review decision for the first HTML draft

[//]: # (ob:97d99a9c)
Use **Pro mode** unless the team explicitly chooses a keynote-like Vibe mode.
Pro is the better default because the center of the experience is a technical
product interaction, and the existing light lineage explorer should remain
visually continuous with the guided narrative.

[//]: # (ob:8f7199a0)
## Event sources

[//]: # (ob:390e8366)
- [Long Horizon Agents Build Day — Day-of Instructions](https://app.agihouse.org/events/long-horizon-agents-build-day/instructions)
- [Long-Horizon Agents: A Technical Primer](https://blog.agihouse.org/posts/long-horizon-agents-a-technical-primer)

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2ZmZDYzZTFjMDI5MDA1NzBjZWZjNjA2YyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjVhN2MyZDE0IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9kYWY4MTY4N2YyODg5ZWIxOTZiNDdlZTAiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzE0ZTliNjc2NGM5YjRlOTQ5ZGE1Zjc0NSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfW1z48iR5l9BtD_srZaU8P6iiZiL9szs9sS17Y5xe_3BPdEuoAokLBDgAqDU8sRE3I-4X3i_5DKzXlCkKEgi5fF5jQ2v3SKBQqEqK_PJzCeTP71h3VCVrBg-V_zN9Zvt9nNZ8jgQXuH6metGiVuIsojduHizeJO3_P4zr1aiH-Dafs38KL4uy5gLxoI0dUXoJUHm8Yx7RSjK3M_CoAy552VukuaMRYHLiijwChaXZcgykWVxAuPyqi_aW9Hdv7n-Cf8YPg9sBU-o2YCPWsA_clHDB_8puqqsWF4LpxO3VV-1jbOG69vu3snvnQ9d25bbTvQ93LNlxQ1bCXypvY-79i8CXnfX4YDrYdj211dXq2pY7_LLot1cFWvRbKpmNbBmlQbu1d7dnfivXQX__rzrRfe5aJteNLAWQ7cTPy_erAXDRYxYUvjcC9_ITz6LW7oIFld85qxMvThNSj9NM5F7WZyHiRAuzqztBny1z3XVCJi53pH6sxeKLI-TOCyyHP4ZZpxFZRJG8nXU7D4XbNvvanhhH-dZtB3v31z_6ac36vE_vYFdbrse_yW_FvxzDkv-pze75qZp75o3P8I7aHnAR9esaWAlrnzXj5duuvT95RpXdVi3zRIfCgOzATZhWbN70V1u-JvFiwSKDUNX5Tsc4nPO-qpHsRJ1-Zn1sL6DoPF28LgOZ31TNThkf98PYgPfNGyD26tnv4BbexSJN9fNrq7hXYo17KGQq5DXbXEDV_tu4fGcodjB9g3iC77pO_1Wjv1WDr2V83__9_9xGtZ18NmtgNvUNBjnNL8tSqK4g09-5Tx_HLig5bticLjYtDDKcL_Fd0F5gRV_8_NinHGSpiLmabY3429FQeI_OZ9fOdZlE0_Ac1mGafjiJ_x6V9XcYc5qV8FXCziUrN57M3jnph3gil5sGby5cPoaLoXvipvLcVL43d6MQEHkZcrzF8_o41o44guoBHhH55bUheBLFJBa8JVY0n93NDeY7YZVTe8Ma7kdE_PJeBxmokhOmE_VO-y2rXjv4NMG-H-c2nDXOhzkoFuBlDj6zMClDYfrbgTOamI-qR_6ISvSvfl8UAuPgieaQjwhG0cun5ARPwiZiJLTnzgqZweWRG-NY7bGqZqyYz2o0mLYdcIp286Bs982rX1AHqxEAQolAJV48rwuLr7ZbXa1PJXjbNa7DWvkfjDco94pWCOnfb9wVmiumsWUBPuey0Mv2pvX2x2vcD7Of-3AsD19fI9dP7FHeZazyA_S05_51qnbZrUEhVv9FRQXvblTgsj2axBJ5gysv3HuwFjCwhipXTiwfkM1sRhBCWAg5cXpE_va-eO6KtYO3F7UOzx1ckO-d3pWihrMP6mitvmfE9PwPRbHAFdOnwaqF9Idm10Px7bp70CZDHjG9d1OLkByhTMIVqzppMMtDJ8xMbEkLxM3Kt29if3W2ApzKJ4Ql-N3TAiMW3BPFO7-4fEunW9aXMutaMho4RuAJeVtWU5P4FfOE_dOTIUVbhQFLH6Vqfx-3d6BLAgQl822FgAkjLDKE01yVPVmMFgwME6Xzu8HNrFNYRD6SRHyV5njO9G1DkK966mDk3A38bL0VZ74teO5rjN0rICzLK204LRMe4szrDsBK1ezatNfOr9r4HDZiuehbQxj5vLgdeb4besgYKDbSM-sOrZdw2nqAJO3dbsC5btmqI0WcCHHHd6Bcl44YC0m5iiSIvDS3Nubo3_p4HneVIAa4aASSntKwB-5Z0KwRcpZ4or8rEeTQOMSgpwWNw5DXcwFLBIH1XW_oDWT-7YVoJEKEOYV6HDRTwqXG7Hcj8qzZgYb_bscwPoty6u6Gu7h2VtUPDDDAlQRfHINNmUFOwRncVPhVg1tW8NldT3OrQbEdmAxCpbkUXDW3PDiHmwZAIFteyPIfJPPWE2uS8h9P3W5f9azvz5YlkHUde_seuduzQYQYXAGG8Evnd-ANQHvFQ8ePIskfEqQPQBhQuT7QDS4dP69azdmxWGFRyTzlEQ_dfOUZxIHYE9F9jqT-QEcVXAflPqBBak4OgxSEQE6dMAfrdCZalY7ACZTO1hkQnA_eKVVWkpTsus6wupoPzhIMliVrz418stdAxLf1rdoaPD7O1aRB2Ib4AcyDr6wm6bZKy3fR40zEMuA1O9A--5AP3SgMkirg0MqzVyvMUovhEQoU5ipDDPAbvtLGV46P9iuHvg1osMZP4Vof-VM3zolbBkrmIyqnD2RP8BSDLaneNd2Nzms3Jq2D7SUdGWlt7jMQefCzsJH4JxNrZXwyzjNo9eY4hJ2pxZoksezQOIGHusWP8dJGrtNkSiAoLD3dNGE1IUe86M8c19jkuTdVtKDLtDX6py2VP70GP-4dL4fJGCWHjdoQZbXE-vIA5GA_hV7U4xAAXcwCGwEflg1O_YceXv8tqmASMYYF3F57gSM2S5hOdZL6U6pEfUhJH1R4tKhVqEAFpmaKXeBh0km_PDc6R1TGaATnLwF4NXuBrDY0wgi9sIoKNOz12lJi6RiMyQ63a1QYqUQvI7zknibJUUPdULWRVLmZVbua9j40nkvn4RwACyyhJh1VYrivqifNJjPuH8qjpIy3y0PXL1zpvQbdiPUkdtRaCkHRMwZYArxZVtXRTVMYsDSzWCB0lebzt5WYuwLgQ5ftuhGYEjHaKqhAn0zxlvwGEzspBcVnkj86NXm-daaF-mmBuBHB4dSqy405Rj_wbhU1VQDBhmaturvnSlzGcW-V4RsH7cml84f1wLOejXgetSAy58SsuO3TMlVxhM3EeU5D_4g31xBsLJmq35dbXFxhwrw-qQqKAMviPLcP-f54EtcXLxjcPbvnSuQoRVICFrm64sLDDJTzG0vZCj3e1vD1k9qgYD7iX_WnoCqNEF9qZcUHLwTeQ_CgYdNdNWGEKLWXHXN8rabiih4BYZ9wvCcqX3tvAVfu-zYRqAXvOrau2G9tOYzCLZx-p0cyfndx_cfVBDgqylPg4VRyOPkzFUDDVBWXyigi3Gzph86QqAIMFadTI_g0eeir1bNEmYxNHAMN-0wdchyxlLB2N7U0kvnm7rtn1Tf1nUTx6lM3ZKlsfviR3zt_BFetW3-ZXD-ItUKSGy_gfdCC0-R5Eu8hD4v9iPPk3o6C0TK9yHR9yNKAyhYrEEOnxMmnLhtKo7h52kYxP7ZM3jL-X56bINxHAppAPxcYYYAF0Q0awa4REpwq-D6VBjKS8FFOMBsp8xviemqDatrUEb_QYktEl3QQThu19boRXWDPOQmoUe4RLAJNeSGZeKWPDx7gipGBoOgZpYrA-YUjtiWUR4Flqvc1fWyL0CPNzLl1sv4xZTTHKWJLw4isN-ygdEBhYdzwom0CJggfiLzOHXjFPR23VCULnuFWXw88ENUHhZBiVOA6gLBUt6KhCsLhQEwWzklaAXLkiDhrzDDJShuQsgwhZbWwvkzytqlcjzxssu_9G3zZ8JOGPDsFw5-1y-mXLzAjf0k2vfZv0ccvTFrod3Fp3TFo3dN7GGQ-GXoHazQB_cgA96vBYUAJ7X1o3dNpcFExHL3IPX28scvHdRUKB4DW2GgnvZXJwxMvgdM_K3YgwRcbCY3p8g9IQ4SqR7NzvaXHKJ2PLk-EzdO7ZAIkJBRnj-JpfPrSoaX8KxdbVuwece83S1rRK0VuXIPJlYpj-GURQd4_4NPE9R41CALpPo8iaifunlitXhaJH6SlK8zmaUjIe61U22Q8-OQD0LxJgpBAVa4GdUIyhzRnyjGOBUx90LwOwL-OpOEG0FPoplRlCdOGogc76qDPZaUjyUlQz_8gBsLrtOuF2B4piJkIcuKJDrIUBeF2A6MlGYHBrCr2FN58aN3TOxgyAC85KF7znNBH8h3Xw6Aqx38lFItjYyqahpJDvqSdk3H0jAZM-WdRLz0sgN6z3fKdYcdaJarFnyvJ1bk6A1TCiBLC14G4RlPxfWg2DKrMQS-rYZiTcQembiT4KNft4CUwMxaFKBp_Rhkbhgn7j7O_IEeiqNL0t--LL77-Jv3Du9Y-RQoecEwE2uXJTzLQI5ffYYYlr64-NC1BIkBcO6aGvkyZIPQidMRHdAXxboFTwShzI24bx66Sz8uNPHvjcp6fYYNYZJTR99ogp74nHqxl-RxHuZxwDOeRC4v4AXxShiZxlTcREdxE-HxsNHbFrAmUS07ehLS7vRfyLr7EUmNMOF7awSb6GgNQhTKEzmQfVsOn0vYJdFtu0pRLfvcu04jLrw48ThPPVHGWRRlQeimYezlPHF56Eecx6UfBUVahlGa50lYRiG4WjwpoiJEJIxHmyiTcreu4_RnWOieiISaFPnRD67D5NrN_s11r13UMWrFMURVpGBr4xgEaPz0p1-WZUlyK1mQmDpHdVhEcQgOdJ4HmBKnMSxipBLpV-YzqmeLuBBJ5HtRmZtnWxRH_eynuItqtMQrWeRGrIw406NZdEY12qvzFNXTwZb5ZeHGIitj_XSLuqiefg4nkVhsuw62mqDAp0ahM4yOtxRM3W2k6aEkFYIFFRFF1wE0dF2t1sOdwP9-6HV_akCsUYf01Zfl0C7psuUGxh-EvbcgAxgUbHcr_F9mpiR9Sh0w7WB2DDVfXau0B93YkoFcia-Is4BhHkeHefBy-LtVASV0n0DDEX1qDZPrMaSlnG7weyjatzDOmoZIC7qxE4WotmBrOICVAjTkxLalIo_h_4TvBr7eNovhabbtdOomMbBaJB8PMoH9qYFTBH9dqy8x569Sxr302BmFOvEBR5JwDuzEmqhmyLv71GzgRO-2aFdh1Ik39UXAC1Bwwi1z_aYWd3Q8bM8jg6pRQdOkJcvi0ksLoz5GfuhIwjyZ8Lnrdazs8Xdz45iHESi8gAk9C4sNqmZxDr2Tvrb5hZ8AGF1eXDw-J-amLAsynokyNAphZIKO6_1MZqcaFvAQcyM_jlPyiGhYi-yp8ewZ5E3w8jU7pl98asbocS9XYb1rODgBBOVk8BiVi8nBYYyORB8X7vrx9eE8EZFfgEkOjTxa5FD1ImeRPfVOFFlW5FngCmF2wuJ_Wqr5VD4n7h7-wTH0g9q0njqIRZoUAuBVXJgXt1ifo2A8m8OpBvbcBI4jAJwoN-9p0TrNwKdwM9UjojLNIpGXnDHXCPVI11SPOIdzqbynHlxUVAugLPF4Euuvv95jKC5AQ4GIgfm2RBTTHroeSMnrBvesY3efGsK6vdKcTgMYXcqrynd3AmkdU8aiwFgJywFgmLNnEUF1BckUm1NvVSo81wtCcB9SI_wjwdMI_-ksTXRk276H69GkfGq-hrdkna10J16UR3mWpSwvi9RMz-J26kDnGQTNb95_TyxAmP-UYmdlACcjTPMiK_VELAKnJdLPZ2Oad2Qej-AsSnqfHHokaNqi_FpsS_3kEvC9K3gaEZdKbv5IwBxpsyezKfHfJDVwRragyi4_Nf5xfmHbrVhT_VXo4Ny1JCVWyHraiE0uOsVjw3XA1MIA7_apcRz4HmvyYOTg0qq2U_YSb68rjKeoATfsHqNCg2SDLOBDWDwUmgpkhzR8X4AgLWhofB7x1eAr8Gwxvdi1t8xWqiZWoBVTkBR-GfpCFN5oTQxx1NLxL2CBaoXNwLNgRRCJyOyXRQw1h_V0lqfZBbn4Ax7XjcCNs5cWAwqAmu0FRVrOYerwqcPtc0AmYZJm3nimLC6pdaZO4INqlCISn7GS-SlpRmnjRoroGCg5l-Zpnscy3y19n_HAAMCR-amedxZ7E70oc1knsHIUBRlsD4ZESan1O7BDoHIFn5DUhHtBEvE4j0MjTRb905LUUymcouownmwlaz7BneCz1D3ZfaLebDa7pirofkOSkQPq3Bd8j8cDN6jbDesJiSrCQMRJkAQlM-bCIotaEvViyqeJUvhpyUFweWKgjcUCVU84h8uJoG1CwHIRhmWeFHnhGffe4ngaATuHqUmG9L2KquGEv1NuLX3b31FUlW0A2Dv_If3f98r_fXBxUVdoraTZhVNrP1-5x8pVplCl5onRvXQmZCYCcBKo8VWF4T46lRNyDbDTY4Bf8jAyQmARTG1P-kSaqCCD0e5APT4IX0xIJwinF7qJYIkwmNWilVrS-SKCqB495CVYc3DqUgMjLM7oIYw4gf1pAVXauls0wLQ9SpMtYHuX0nxSuF6pJKPcRp0tTS7BchRAtKqiQSv9CRkWvBa9ApQwG23GRuHhAoBPZ4ItE0suihKwrZ8HnI2BvZGpOqHjnsU51SA6575b5OD5hsbrt2io5kyeQSi11pyAX10BImJEAJS8ELUFS5n3UR0FcOcePyilV0Qpj8ABSNiIaQ071ZLH0-ileg_AHAoAuVkRGTfTYpyqx5xGGdUxTxaHmR9EQRxEI-gyLNJjG_BCGuhomqTvRjsEvhyiKzBvQ3evYoyo1gYcosVYDX6yxHWXqrEAX3eJO4yKVaYhzFbLJSUiSCcomKB6SmijIKOcGHNYg9wvJJdv2wuy-MTTuRWIWkEC4L68g-MExlmqbIMHrNcyYV0E6LZWw5nVu0EHFrgo2a4eHIM7JAmyRSGubllxj-IoZBBeMCmgcOpVkBBTTu0mh5cmtEIaf0Img4gFLksKL8-MfbV4tjqqdAZRFvwkWuop95qnvvBSVrq5sSAWidY6GM-mxGol7ZVeUIZlkuTmyFksWROlfDnnVauiMvJ4FgRFKYwVsGiwo0t3MqlVZyNw6QXrwRHk5CvtxfkEOEmKrQHvAtIDgE9TxNB8OzkDgIL8FcCHqPyJUgdOeVXDrknfqxh2GFIZRxI95uFk5LAapCt5cfHvFRkOnDpvwQOR8UFYpoJ8EYq-yPNjYonSwjWsvifDjoJNj1RujPTySIT63Warxuiq_kbfap2ZDUbqVPRI-qAXF29RX1cFgVvRybkBwmXgYjkUl1_Iw18JikFwRE5bdr8hE1ru6rKqa_rDOKG86reY_zAUDDVVysIqpCA1P9NBVvTL0LZOmoAg90ReiIwFuTuaAENNHu3jyURjuXNfQCXi2k95TkUcZUUZeykfvcGRimyc29OJxZYHO-y6pqdYFMFkibNMXFflPqRkoEtlUs1HMgZPKZMyCfw0jYogcI1tsnjMNhw9kZWscaoix7BPTdnuOoAuDzSHHKAV8kJ0ze6lVdFLWiMHh2S6w2CAHXRXodGp6IRfsgAJr-XoT46saEtrTtOdtap0ozTIE4_FI2ywGNBjWP5karPcP3p_mXpBgXhh9mX_eD1w1oIkLeOSg0mLR1xiWNNjhP1l9Gc9epbneQhmynfHwOHIiNa28gxqs_Jet9MxDwCQgvk8CILI2GyL-WzQ1xkUZvA3c4H7VK3WlD2m-HpfwG01ZZ3Zfv68Eyt4Vbr54uK3MIGLiwX869cg3vgvGB3coBtxrxT6xcV3Xyp8712HFhB9oPqO3WOqlVU1nnwD0_AaBTdAKeNXeJi6jfVwnR2me2TqF8PwN1KiyLmGpQBPBlRJId9Lwk-tMlXqQMEtMLAYbl_Kk458tq7XzgCc4Y3gFZEDSP2r9lIGyrGm2jDSb3C8O4YGZaPMrXklYmjDTtcSBIAeolgbWHRUGTguTJO8lY5WS4_dELdIhaBB207YGYB0LAbVnqeZsTMW93w_jn8SiVzSKBQNBG0frNOnhmKsC4KuqMOXpfRDKdrTYwyZCI4MLXK-GywcTu9pgjYSKn9qyB-VuERv9h--n0oHA2p0Mfnqxsb9tCjtFq_khcx0He9KGHPDws3y0IxvkdUt9_ZUzjlMAxQeyDxMqS1hBZ6IwEVxJPwgdjPfGxM2Iznd6ILTOeYq2KhSwJTVuURJVsJTNbcEQ3TIQYUm6UgpPAgWUQZ17TUpMHaD4_wvIbZa6EtQVxicg2-3945xFP8MAE1cX1392VE8OcCb4Pp08DXRYpX3gYdNmfRxZGnOq-F-JIsQXCE53fM0r0z0BUerGn3UBhyXo00mtEJDf0Qa3R40e4iMKCesvCLw7whfkAoZAYY1Y5lRkj7CAjP2jGgtKmSLqPZY_OXw3GdCBEEZ-0EZ5GOi0lQCWAbwJZx-jRjDIo9yX_DQE2Pu0tD8LcDxEsa-HjzNyiwRflSMiQOLxG8E-XQ-fks7h_ezPeayMh-10raSJjVOndQV3fqD2E3HmXUI90pHb65McFaTmjprErjJ9YgVN2wrgxYA1XBsOkm4RRP7jVzFNBVBwoIx9joWF9hb8rIiAZNeidw8ypgrkjHQM9YNmF05nf9PqgfXhAJS4xHETH5OHFc0sMrHUcOMwTa8cczUSrVJZFK1mYaKq2PfmpJbNWuBfG_-ZHib5UXsgspP08TAbKsywV7il1cXaLcwdMM0zlnEMoNbrYIDs8ynFw2o1JYKDqDekVy0-p7WUDv1sAFsKxXb2634Qtq9H1AIl9p_N1kMgge07ujJUMKB2ImOWWxtU-kR32jnHJ4hmSAyFk3--JUMzl2Z2eu1u1sTeqOXxMNWIq2wohcwWHFi84qMezHmJ_JgzLiPRRJjhcTJhQ5T2bGS85wnMVJdTfBpLH6wiGDPLWUwSTGRxnGQBuC_m1M_VjeMuvLkWoUV-qMqS9_DVtxToJPQiTKAZm0UNmT9Ta8S-rZrj9ge_TeZTqAz9xUG74xTDPfh2DgZNUO4Eo4tiZNy9vUDFeYkRmmHToqKfYJsmHwiaGzKkR1VwkbZfIedhinKg9iMH2ZCQRcPNPqBokJzDJIyUvBx6hqCaJFF7GKmrIO5EuWKL7AwmMmXMePRKYaFq4VOUqDyZ45uiIwSTqsvY8pSOxK8UkqQ1sM8cPTIZLQZ8fu9TqPJLBNYLxNstpaUhvhtq1jP-KY2ate-H30IqgCThFJRdKIUnVleVEwKfd3nLes4mNLbajXGUw7cq1ys4Xt4Gp5u8xaSHIvNffuHmMiEDKyQn46DyRCu9B6cMYJL90iItkcam46e6RUZtasVPV0c5skJrO0aBS7FYeQI5yNjsZgI3WC8bIot4IZukaQ84EVgwJZVJjQqj-dW_eggBmcei3lUgl4yGnEsBLJ0x6l1Pa0CS3C0Ci1mY2jDuHEynEg5mD0squ6maI--XfHaNe8bnr8G8aYF_x2A9I8mJ0TmawRZBKPu0Y1EWVEBeGUDUc9sdBJMylvdtjcmN0hjqMwAEUEYHP89oo8G-IrEQ7O3E1lTcWBehFma42YE4y6Yoqdxd8-rVtLMk7AADCcyPxmjAVYBk0WiOLXySCzrCpbyPyuwixvp2eFAKt-fi2Gg4gapC3NRMI2k96kA8miSLiFveRDFGskqNSb-HxBHFiZnbcSLYlWmQElj7pHnKRUDYMsdaTCFhpFqTnJtaUTjADww8D_-jEt7pKO64AgoVT91UlDXaMa-vPmRerST2jv-7UEv9gffkmMztmoHIbzuwNKCdsUO9f8gPdsp5ntqy3bhBXkqEv9v0LL94gLZx7ses0bf4lk6UEhIRhsP3v7yHam4kyS2xyZ_MAtVWvcW_9QnQGpzOtWERkA4jz9cRpUezvVSzkMv009v7tb3lPEHA_bIKPSKyhjyY2ugobyZCgYjP_xwiTVtz64xFF7ii7jwmFuwPEm90k98ryQOh1wIu3jQLpyzCwp_-geXj-fXXR7WHXo_H68qfKrE8lXqKMM0LHPBXRGXec7CwuMsE0KAkxonCfwrLMPYC1iZhX6RuR58GUcBmJ0yjd0olGMfeZ9jZZTpdRQfKaP0PLcI8tKfyygNRgRD6sWZy_IxZWcdBFP9dLr80uzwmD-ejJpLOedSzrmUcy7lnEs551LOuZRzLuWcSznnUs65lHMu5ZxLOedSzrmUcy7lnEs551LOuZRzLuWcSznnUs65lHMu5ZxLOedSzrmUcy7lnEs551LOuZRzLuWcSznnUs65lHMu5ZxLOedSzrmUcy7lnEs551LOuZRzLuWcSznnUs65lHMu5ZxLOedSzrmU879RKadVUWP9dvJYHaSeAbJH-YKJXxINM1a44uAH0WVx0LeMRAI99QrrBqd_E_KxeyZ-ANItvIgJ3z_v2VRLRFGXqpEEcYJaCrs-4NRICpTSsRMLkwciZEmanje5pcphb9TpJ3NMxUS9CYBa-RaMDRadDINvdhO_7hmDkYqy_BWWThozSmNjPY3k4KBQSl2FQy45oyz7wK5H_TK1dGkGiNwPX2tft4hPSGGCJuv3U72Ik0xdAGoxihxNTM4qMRgn9xE35mGVl11v8OiROvrTpqAkUh6xEx9yZDFYtxKwQxXcvrp2fFe7H9pnWTh-ZD4jkvbCyeQnE4sRx14ZleX-Tj1CIZ_cKJmzU8WO4gvD86XtTL6HKG9VbI9xRItTv3E8EhPGuR1nPDxf3VlkhJMHfXAYi4Dqdr3nD_oMaUcfbcAn9yY9KqOn7wIAcWD_NhhExuN4N_G-ViLM-gn7x9N9z3_pk34d_hnjnvMj4c8Y_uW_YP2MQdMy8QA-7g_6He2mjMI9-bPTB9dO_uK0K1JZ0H_Cs5bOn94jcfadUp9vZa55VM64zPC_S4Cg31vm9Mf_sR6G7eESHG_VYIGTh0uoujV8o22A6tlwCDNNEhhf7F-U5dS6k8zpHQzd3l0-BmaeahLRliWAdxClo3YJ9aakLz6CV44Pj84nhRnu1vfqNO8NumbbI4DkwOF7DIUcf-QPhJX7EWbwnfTb0R2sVhhTX6KNXFDmdylFRBEJdrkOLyuwtJH1pY8AjeMT-FZZZSqdoyDqIWjAcueh3Y5ejfZOpPdaEtPyyKuPKOL4k0GGGlEMB5Xh5Lra0qMUKgjRO2_hvPPly4MWVQWKj4CDR0X3B4HoiO8TBSSjYU9KjV2_fAwaPCKjNWa-B2FFcPSQ-ziWCttAFd4KU0coszOPmfjjz_vQ9pWEzL8fGNJ9exWOVkLZ3WtGjrTuucCg84NSJ0apuEcM-MRikmmTq2nFpzRWhuspnDbI7IwDWEdFzw5e0zLsjz7sbY8RKHiYCn2AlCC_z8TStNhoWSI6ApgYoemzKriGIdmW-PhjbOwxQDB9aB5YdhWUUwYen2otNOZhkRi0tzfEv5Nbc_mY6X98RUgfkghhVJxLAVIsQ5lzOhDBAkfXC1U9AiQuH0MKj07kD1tO7g8ACGRZmEyj4kqOPX1G3WI8pcvH8MPTT_PBZkp-j4EWKjSBXRNQTYEYmCyM3XGA73BCGOOjRSip_vsxpPHoRMBgwAtiwv4hApHBLQL8i3F6XVsj-4CO6kLLj2IjSO2rCmAfAyjPNozCwhTH7aEFRY6P-p5oRzjqEUghw1U6pKVh7w5LdfN7eQ4fb8Qkd1DVa-uuMKM2JgrRwZvYlpji33jh86LpRhSkEqI9eFnbJs7K1IvTpPRTMGu5l8V5mAgqxDnatsk06nm6bdMcC5pjQXMsaI4FzbGgORY0x4LmWNDfLxb0_FaVD9oYuotxba_Tn4_3LPxFmjSmkZcymLUfpSzwQPiSnOXcS7jvltjGqki9KAxDLyo9VvBE-C6L4jIRLoC7yEuyZ73dfsvG4KPrXnv-tesdadkYsaTwsbx_btk4t2z8m7RsDH0_8EWSRMXYtuIfsmXjcBxUzb0a516Nc6_GuVfj3Kvx5F6NIs3ATQ7iMvNMOYoVLRoF4wWRH63N3DKL4iQFc-eP3RpNMMi2PicGdtRHA9ol6uDyqTFJE-yWYU91YvNTrwgTN8sAymZGisfA0F6XjxODPJg7EyZvJ-MZKCyDJhfTEiwcLIBcrZFCW8lKe8pDqED5SC1FRvRYZin_Hp-ChaDSS5DtjswVsnm9vq5ntzIimwAy3W5Iz1GpToVsd6pf17WukomJM7dSi7AKfCdwgFQOQKkUQKwtDS9ZgoqKPd42QRb1QeaKwgs9wHum3c0YArOrDk8MZ1H_lz0gAhCDGNNUm6nkbcxbfmW6-dOOKZon7dXSFNpK1Lbfsmmhuycs9wqRHpA67SJ8Mr5TrSJFEgdFEsV-aaohrCDcg_P08oAa7uUd_LWkXNCnRmecr0EUm3tnQJRGbNLdthZj0RGo4lIInlM4Sjfd0izeDSIBxIVrme2Dw4GyiK-KvQVkAB6WkGzBOw9XpGNLXQIFSLhvG0qUvPNhFEyMmi_tpTW5X3kJmRRW6MJ8bGRgmX0ZsgJrIuun5Al851_B7bo70DUeQN3q8WG5B-DMW6VpaCqEfemhaoD9suUHwJwD0AHPN2Fjx66jHXKfEU2c6GXregHnWVIGI8iyYpZaYM4IOuIntrMCFjoY7x-OtBqT--SNF6kqwInFmrv-zl1_566_c9ffuevv3PV34kwFpQvwiOduGBtPxsp8WUt1ahoLrDpsliJTrUW9BYlRTjp2aTDELSwgbHea4qJBiC6k1SK51zeKqlVxgWRFP9PELIsuJCVQSZWOMS0JbuiGwmrhqA5VqsVPzbh0jm5NSr5SRYVBssCaNfvFSnv4URYnUtwLC3H0zBQ4GONa6kQgyadFRLEY69jbSoI43QAmZzCxfgdqsrtXxgx9_aWu-kS3DQ4CqqK5zfPc5nlu8zy3eZ7bPM9tnuc2z3Ob57nN89zm-Z-3zTMDJAhwi5VZkD23zfNYaIF8IUqUEdnZdvJB5yIFTVkwSm8rZAM4HTXKVJfOMmduXLLQzbzndoYWMCVNukYah9WMGTeFzKZMeqFbKCjFrLtHkyutzBoqdtWqpKfGklaIW3eCNg2i0btRM9BdSuUbwnimIMSRGeyF6mhrdZY-1lD6YTNpGm2yoTS8vkaN5v2l4qrQHxq7P2lc3yzN7Gj0MclElvXbX6w5tWxwgyf9YSdvGkp3MTrarBq3XRfVjG_OLPkcdaFsXKFajdDQYFbvUKOYuBV1FZa62Pz8skyWEfXkoA92bxph9zIWY3fD1l2w1Yu2JG6yDmhsL94BZlCZAl1URK8rxaeiTk2yfIy6Ss69sefe2L9Ab2w3424WBGHKPIPaLaLyYznBF9COAUhcO6q98BLjw6CAVS1b3bZb-Spw1IVcuVsMkpEyUk38TeeyTtyxjssjdgMIHMH_FrNOf8X0DzgIFP272YO0uhTOgDmd2b8cBfKuUdEpa1Z7ctepQtrjTdvGSBp50aAdRhEkX4T4eKRFQRhH6o2kBYEeIenRkaux-xu5PBivQBKHZE1gTaskccBlUqoLlRRDuCXHHVREDIOI1CLW-IpkhlAH7gvOQLHkgm2lpzOdeJx7qf-T9lL3yzQPY_yJ-lEjvmov9Qelpqal-thR_RdrqD6WuAbXrqtKW0flclg2iMqtU23N5obsc0P2uSH73JB9bsj-T9KQPfTDRHDwhBiP_64N2S0L-v9VV3a85T012JYPR0_7SLMG6TuPrWjQY8YGJPukxrmx-3_Lxu65nxQiDkXhR-5zGrujbOw1drd_ju2lnd2_Ag02VkapEJ_VgLcydHJ-fhP4wzAdhZMoTGd3lTkIVeyVAj3WLj5XVWAy8rQcg2V70TCYElE-rMRBTaExIo03OvR1vyzsRlwqG6i8F4kg55bzxwS5EF6QhoInPPk7tpw3GT27FTyOnwvK3t0SgU2NsleLYDVItzuRjQEfYuncATx4WH-w388L52VMja3YrdiK1eJr7pY_d8v_RbrlryiL_cL-Pn9p8_5a5Z1w3VQKbC8Ts1CVnntJiksQnAft9BWbQx2S_bi7HTtW5MK_fX99ghHES6z6gyQm6ZK2Nz8qqtu9KWbjMEj2kPZj8GoxIGxT5knGGg-HpYqJg65me1HX6kgcV_1UwUGBscVuJD2tOp7Nvxgw_2LA_IsB_1C_GGBRmmLPj0rmldLNkvXdY_8U64w-3RNFe4oicb0i9cOS24Kh26SY43lO65P--uqKbbeXbFXBuvTiEgT4SjJ2rmxygXQL-6Vxg6_s4tV_xfNB01juT-MadMdH0xfvA-XixgfndbvafzL6occfzJZGAJYyp_evD9q2_Az_-X8EXmC8)
