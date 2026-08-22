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
adds a six-to-eight-minute narrative path through that surface. The presenter
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

[//]: # (ob:7bf705f0)
## Narrative structure

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
Present three flagship verticals:

[//]: # (ob:f3135bb2)
1. **Harvey / legal work:** a governed knowledge graph plus separately measured
   long-horizon evaluation results. Do not claim baseline improvement until an
   actual evaluation establishes it.
2. **Finance:** documents, calculations, model versions, and analyst review
   become approved assumptions, risks, and a traceable memo handoff.
3. **Agentic commerce:** catalog facts, policies, order, payment, fulfillment,
   and dispute evidence become the trusted state an agent may act on.

[//]: # (ob:e73d2723)
Then present the current website experiment as the collaboration extension:

[//]: # (ob:1c05f044)
> A Coframe or growth-experiment team supplies OTLP traces; Proofpress turns
> selected conclusions into a reviewed, portable verified knowledge graph.

[//]: # (ob:a454d673)
This fixture demonstrates integration and design-partner motion. It is not a
fourth flagship vertical and does not imply that Coframe lacks memory or
experiment state.

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
- each beat highlights or scrolls to a real product region;
- **Next**, **Back**, arrow keys, and **Exit tour** are always available;
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
- Add a guided-demo controller and eight narrative beats.
- Reuse the existing workbench and Lineage / Ledger / Evidence explorer.
- Add a final vertical map and closing statement.

[//]: # (ob:43cb1ee8)
### P1 — continuation proof

[//]: # (ob:3e31c02f)
- Bind the pre/post fresh-agent context panel to the ledger view.
- Make admission visibly change the context projection.
- Show the source pointer and decision receipt for the inherited claim.

[//]: # (ob:b6ca9525)
### P2 — vertical fixture packs

[//]: # (ob:d8c7277f)
- Harvey: import only real benchmark evidence and label unresolved results
  honestly.
- Finance: adapt the Apex investment-analyst artifact into the same node and
  receipt contract.
- Commerce: add a compact order/policy/evidence fixture when a real workflow is
  available.

[//]: # (ob:3144a33d)
P2 is not required for the first guided-demo PR to be useful.

[//]: # (ob:24a9c758)
## Acceptance criteria

[//]: # (ob:4ab84b40)
- A first-time viewer can state the problem and product category within sixty
  seconds.
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
- The story names Harvey, finance, and agentic commerce as the three main
  verticals and growth experiments as the collaboration extension.
- No benchmark improvement, universal truth, or unsupported design-partner
  claim is implied.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2ZmZDYzZTFjMDI5MDA1NzBjZWZjNjA2YyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjExMGMzYmYyIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9lMTcyZTZjMWEwY2FiNzgxZjI3MjFmNGUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzE0ZTliNjc2NGM5YjRlOTQ5ZGE1Zjc0NSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXetu68iRfhXC82MBr2TzfvEAsziZmWQGmWQOJifJj3jgafZFYkyRCi_2UQ4G2IfYJ9wn2arqZpOyfWhbchYIoAU28ZHI7urq6qqvqr5WPp2xpisU491NIc6uzrbbG6VEHEiPu37mulHicql47Mb8bHGW12J3I4qVbDt4tl0zP4qv4jDP04irMEqDjOdMJVnmh770OVeB72ZZHgdK-J4bKaFiFrAwSaJEKD8Ow0x4PowripbXd7LZnV19wn90Nx1bwQwl63CqBfyRyxI--ItsClWwvJROI--KtqgrZw3P183OyXfO-6au1baRbQvvbBm_ZSuJi9r7uKn_LmG5fYMDrrtu215dXq6Kbt3nF7zeXPK1rDZFtepYtUoD93Lv7Ub-oy_g75u-lc0Nr6tWVqCLrunlr4uztWSoRM9zeZArXBl-ciPv6CFQrryRXuLLmHvM5SxPUk_5ie-pUKJkddPh0m7KopIg-bAj5Y0XStBiEoc8y-FPUBuLVBJGejlGuhvOtm1fwoJ9lJPXjWjPrv726cxM_-kMdrluWvxLfy3FTQ4q_9tZX91W9X119jOsYbAHnLpkVQWauPRdP1666dL3l2vUareuqyVOCgOzDjZhWbKdbC424mzxKoNiXdcUeY9D3OSsLVo0K1mqG9aCfjtJ4_UwXYNS3xYVDtnu2k5u4JuKbXB7B-kX8GqLJnF2VfVlCWvha9hDqbWQlzW_had9l3siZwk8DtvXyY-40u-GVTnTVTm0Kud___t_nIo1DXx2h_tkxGBCkHxbtER5D5984bx8HHigFj3vHCE3NYzS7ba4FrQX0PjZr4tR4iRNZSzSbE_ibyQn85-V5wtn8tjMDFHgMhWm4atn-E1flMJhzqov4KsFHEpW7q0M1lzVHTzRyi2DlUunLeFR-I7fXoxC4Xd7ErFY5SoV-asl-rCWjvwILgHW6NyRu5BiiQZSSrGSS_rPhmQDaTesqFqnW-vtmJEnE3GYSZ4cIE_ROuyuLkTr4Gwd_D-K1t3XjgA7aFZgJc5wZuDRSsBztxKlmpEnBQ8bMp7uyfPeKB4NT1ZcPmMbTzw-YyN-EDIZJYfPODpnB1QybI1jt8YpKtWwFlwp7_pGOqpuHDj7dVVPD8gjTXBwKAG4xIPlOj__ut_0pT6VozTrfsMqvR8M96h1OKu02LuFs8JwVS3mLBgingi9aE-ud70oUB7nHz0EtueP71PPz-xRnuUs8oP08DnfOWVdrZbgcIt_guOilTsKTLZdg0kyp2PtrXMPwRIUY6124YD-umJGGYFSuZ8KfrhgXzl_XRd87cDrvOzx1OkN-d5pmZIlhH9yRXX1XzNi-B6LYxWLw8VA90K-Y9O3cGyr9h6cSYdnfHjbySVYrnQ6yfiaTjq8wnCOGcGSXCWAj9w9wf5oY4U9FM-Yy9NvzBiMy4Unubt_eLwL5-sadbmVFQUtXAFEUlErNS_AF84z786IwrgbRQGL30SUP63re7AFCeay2ZYSgIQ1Vn2iyY6K1g4GCoPgdOH8qWMz2xQGoZ_wULyJjN_JpnYQ6l3NHZxEuImXpW8y41eO57pO1zAOZ1lHaSlITXvK6daNBM2VrNi0F86PFRyuqeN5HBvDmLkieBsZv6kdBAz0GvmZVcO2azhNDWDyuqxX4HzXDL3RAh4UuMM9OOeFA9FiRkaZ8MBLc29PRv_CwfO8KQA1wkEllPacgX_mnRnDlqlgiSvzo6Ymg0YVgp3yW4ehLxYSlCTAde0WpDO9b1sJHomDMa_Ah8t21rjciOV-pI6SDDb6xxzA-h3Li7LodjD3Fh0PSMjBFcEnVxBTVrBDcBY3BW5VV9clPFaWo2wlILYHEYOzJI-Co2TDh1uIZQAEtvWtpPBNOWMxq5dQ-H7qCv-oub96oJZOlmXr9K1zv2YdmDAkg5UUF84fIJpA9ooHD-YiC58zZA9AmJT5PhANLpzfNvXGahw0PCKZ5yz6uZfnMpM4gHgqs7cR5idIVCF9MO4HFFIITBi0IwJ06EA-WmAyVa16ACZzO8gzKYUfvJGWljqU9E1DWB3jhwBLhqjy5XWlv-wrsPi6vMNAg9_fs4IykGkAfmTjkAu7aZq9kfo-DDgDsQxYfQ_etwf_0IDLIK8OCakOc-2AUVopNUKZw0wqzAC77asyvHB-mqZ6kNfIBiV-DtF-4cy_OmdsGeNMeOFbCPJnUEU3zRTv6-Y2B82tafvAS-lUVmeLyxx8LuwsfATJ2ZyupK_iNI_eQsQl7E4pMSSPZ4HMDTLWLX6OQtq4TZUogKCw9_TQjNWFHvOjPHPfQkjKbgudQXPMtRqnViafHusfF873nQbMOuMGL8jyckaPIpAJ-F-5J2IEDriBQWAj8MOi6tlL7O3zr80VRDLGhIzVsQLYsK1AHeulTqfMiMMhJH-hUHXoVaiARaFmLl0QYZJJPzxWvKdcBvgEJ68BeNV9BxF7HkHEXhgFKj1aT0tSkqnNkOk0d9KYlUHwQ52XzNuqFDPUGVuXicpVpvY9bHzh_KBnQjgAEVlDzLJQku94-WzAfMH7c3WUlPmuepDqHSPSH9itNEeup9JSDohYMMAU8uO2LHjRzWJA5WagoPTNxNnbSqx9IdARyxrTCCzpWE_VFeBvxnoLHoOZnfQi7snEj95MzncTucg3VQA_GjiUg-vCUI71H6xLFVXRYZGhqot258yFyyj2PR6yfdyaXDh_XUs460WH-igBlz9nZE-_MmdXmUjcRKpjJn6vV24gmCrZql0XW1RuVwBen3UFKvCCKM_9Y-aHXOL8_DsGZ3_nXIINrcBCMDJfnZ9jkZlqbnslQ73f2xK2ftYLBMJP_KP2BFylLeprv2Tg4L3MWzAOPGyyKTaEEAfPVZYsr5u5ioLHsewThseI9pXzDnJt1bCNxCx41dT33Xo5kaeTbOO0vR7J-fHDD-9NEeDLuUyDhVEo4uRIrYEHUMVHKuhi3axqu4YQKAKMVaPbI3j0hWyLVbUEKboKjuGm7uYOWc5YKhnbEy29cL4u6_ZZ9z15buY4qdRVLI3dV0_xlfNXWGpd_Ufn_F27FbDYdgPrwghPleQLfIQ-5_uV51k_nQUyFfuQ6PsRpQEU5Guww5eUCWdem6tj-HkaBrF_tATvhNhvj22wjkMlDYCfK-wQoEJktWaAS7QF1wauz5WhvBRShAeY7RD5ltiu2rCyBGf0O2pskemCD8Jxm7rELKrp9CG3DT3CJZLNuCE3VImrRHi0gKZGBoOgZ9aagXAKR2zLqI8C6lJ9WS5bDn680i23Vtcv5pLmKE18-aAC-w3rGB1QmFwQTiQlYIP4mc7j3Itz0Nt1Q6lc9gZSfHiQh5g-LIISh4PrAsMy2YqGKwuDAbBbOWdonGVJkIg3kHAJjpsQMohQky6cX9DWLkziiY9d_L2tq18IO2HBs104-F27mEvxAjf2k2g_Z_8ecfTG6mJIF5_zFZ99a2YPg8RXofdAQ-_dBx3wdi2pBDjrrT_71lwbTEYsdx-03l4__dJBT4Xm0bEVFuppf4eGge33QIi_k3uQQMjN7Obw3JPyQSPVI-mm-ZJD1I5n9TPz4twOyQAJGep4IZbObwpdXsKzdrmtIeY9le1uWSXLwZGb9GBGS3kMpyx6gPff-yTggEctskCqz7OI-rmXZ7QlUp74SaLeRpiloyHulVNskPPjUA5C9SYqQQFWuB3dCNoc0Z-oxjhXMfdCyDsC8TZCwovgJzHMGMqTIA9EiXfRwB5ryseSmqHvf8KNhdSpbyUEnrkKWcgynkQPOtScy23HyGk2EACbgj3XF3_yjZkdDBmAlzx0j5kX_IFe-7IDXO3gp9RqqXRVdaCR5OAvadeGWho2Y-ayk0goL3tA7_nWpO6wA9VyVUPu9YxGnnxhzgFkKRcqCI-YFfVBtWVWYgl8W3R8TcQe3bjT4KNd14CUIMxOKEDz_jHI3DBO3H2c-RNNiqNr0t--LX734Q8_OKJh6jlQ8ophZnSXJSLLwI7fXEIsS5-fv29qgsQAOPuqRL4MxSBM4oaKDvgLvq4hE0Eocyt31eN06efFQPw7M12vG9gQpjl19M1A0JM3qRd7SR7nYR4HIhNJ5AoOC8QnYWQa03ATHcNNhOlho7c1YE2iWjY0E9Luhn8h6-5nJDWCwLvJCFOi42QQolAeyIFsa9XdKNgl2WybwlAt29y7SiMhvTjxhEg9qeIsirIgdNMw9nKRuCL0IyFi5UcBT5G-mudJqKIQUi2R8IiHiITxaBNlUu_WVZz-CopuiUg4kCI_-MFVmFy52X-67pWLPsZoHEtUPIVYG8dgQOOnn_5_WZZkt5oFia1zdIc8ikNIoPM8wJY4jTEhRhqTfmM-o5lbxlwmke9FKrdzTyiOw9zPcRfNaImnWORGTEWCDaNN6IxmtDfnKZrZIZb5iruxzFQ8zD6hLprZj-EkEoutb2CrCQpcVwadYXW8pmJqv9Ghh5pUCBZMRRRTB_DQZbFad_cS__Nx1n1dgVmjD2mLj8uuXtJjyw2M38np3oINYFGw7lf438yKpHPKoWDagHQMPV9ZmrYHvVhTgFzJL4mzgGUeZyjz4OPw79oUlDB9Ag9H9Kk1CNdiScsk3ZD3ULVvYZO1ASIt6MVGcllsIdYIACscPOTMtqUyj-H_pO8G_rBtE4an3bbDqZvEwKqRfNzpBvZ1BacI_nVlvsSev2kZtzpjZ1TqxAmeaMI5sBNropoh7-662sCJ7rcYV2HUmZX6MhAcHJx0VT6sdMIdHQ_by8igZlTwNKliWay8lFv3MfJDRxLmwYTPvh1qZZ9fmxvHIozA4QVMDlJM2KBGimPonfT1lF94DcDo4vz88zIxN2VZkIlMqtA6hJEJOur7hcxOMyzgIeZGfhynlBHRsBOy54BnjyBvQpY_sGPaxXU1Vo9brYV1XwlIAgjK6eIxOhfbg8MaHZk-Ku7q8_oRIpGRzyEkh9YeJ-RQs5CjyJ7DTvAs43kWuFLanZjwPyeu-VA-J-4e_kNg6Qe9aTl3EHmacAnwKuZ24RPW52gYL-ZwmoE9N4HjCAAnyu06J7ROO_Ah3EwzRaTSLJK5Eoy51qhHuqaZ4hjOpcmeWkhR0S2As8TjSay_9mqPobgADwUmBuF7YqLY9hjuAxl73eCeNez-uiKs2xrP6VSA0bW9mn53I5HWMRcsONZKWA4Aw569CRF0uEEyx-YctiqVnusFIaQPqTX-keBpjf9wliYmsnXbwvMYUq6rr2CVrJk63ZmFiijPspTliqdWvAm3cyh0HkHQ_PqH74kFCPLPOXamAjgZYZrzTA2CTAicE5N-ORvTrpF5IoKzqOl9euiRoDk15bdiWw4zK8D3rhRpRFwqvfkjAXOkzR7MpsS_yWrgjGzBlV1cV_7T_MK6WbGq-KccinNXmpRYIOtpIze5bAyPDfWArYUO1nZdOQ58j3fyYOTgYnLbzsRLfL0ssJ5iBtywHVaFOs0GWcCHoDw0mgJshzx8y8GQFjQ0zkd8NfgKMltsLzb1HZs6VVsrGBxTkHBfhb6U3BujiSWOTnz8K1igg8NmkFkwHkQysvs1IYbaw3o4y9PuglZ-h8d1I3HjpqrFggKg5qlCkZbzsHX43OH2BSCTMEkzbzxTEy7p5EwdwAcdUIpMfMYU81PyjDrGjRTRsVByLM3Tzscy31W-z0RgAeDI_DTzHcXexCzKPtZIvDmKhgyxB0ui5NTaHuIQuFwpZiw1EV6QRCLO49Ba04T-ObHUQymcsmiwnjxp1lzDm5CzlC3FfaLebDZ9VXB635Jk9IBD7wu-x-OBG9T03XrGongYyDgJkkAxGy4mZNGJRb2a8mmrFH6qBBiuSCy0mbBAzQzHcDkRtM0YWC7DUOUJz7ln0_sJx9Ma2DFMTQqkP5iqGgr8rUlr6dv2nqqqbAPA3vmdzn9_MPnvo4d5WWC00mEXTu10fpMem1SZSpUDT4zepTOhOxGAk8CNrwos99GpnLFrgJ0eA_ySh5E1ggnBdJpJH0gTlRQw6h7c46PyxYx1gnF6oZtIlkiLWSe00ol1voogOoweCgXRHJK61MKICWf0IYw4gP05Aaq0dXcYgGl7jCdbwPYudfikcr1xSda5jT5bh1yC5WiAGFVlhVH6GhkWopStAZQgzRDGRuMREoBPY4stMyqXXAG29fNAsLGwNzJVZ3zcizinA4jOhe_yHDLf0Gb9ExqqPZNHEEonOifgVxaAiBgRADUvxGzBUvd9zC8K4M59_qAoj0epiCABSNiIaS07dWKPh9FLhz2AcCgB5GY8smnmhHFqpjmMMjrUPFkcZn4QBXEQjaDLskif2oBX0kDH0KRzN9ohyOUQXUF465qdqTGiW-twiBprNfjJEvWuXSOHXHeJO4yOVbch7FZrlRIRpJFUTDC_KTEEBV3lxJrDGux-obl821ZSxCeezp1E1AoWAO_lDRwnCM7aZVs8MFmWLesiQJ96NZSs7LuhsCCkYn3ZORZ3aBJkjUZc3DG-Q3OUuggvmTZQOPWmSIgtp3qTw6IJrZDHn7HJIGKByxLu5ZmNrxOe7VBVOoIoC3kSqXouvRapL72UKTe3EWRCop0cjBdTYgcn7SkvUKFKktweuQlL1lYpX895HVyRijyRBQFX0kaBCQ12TOkOJrUO3QhUvWQtJIKCcqW9Op-EJMmwNWAtYD0A-AaKGIZvJ2cAUJC_AvgQnT9R6iApL0rYNZ178a7Hkso4kmyxD6crh0WnU8nz898WFDhQdFFDBqLrg6AmTrkIVV_0-bG1RB3hKlbuKLCjYdOUJo3RWR6ZUNtvtmaMpmhvh1cnZ2aDlTpTPdI56Pn5O_TXBSdwKxstGyBcBimWQ3X5hT78haQahEDktGW7DYVQ1ZeqKEv6h01CRdFusf9hKRhGVOrCGqSgPT8biqyYl2FsnQ0BQe7JnMuMBbk7hgBLTR7j48FEY71zH8Elou7nMiceRxlXsZeKMRscqcg2uT2cWDzJYLu-qVqqRRFM1jjL1nVN70NbBqZUttX8RMfgOWeiksBP04gHgWtj04THPIWjB7KSB5xqyDHsulJ13wB0eeQ59AC11A9iarbTUWVQaYkcHLLpBosB06K7KY3OVSd8xQIkvKoxnxxZ0ROvOU93HlylG6VBnngsHmHDhAE9luUPpjbr_aP169YLGsQruy_7x-tRshYkqYqVgJAWj7jEsqbHCvvr6M_D6Fme5yGEKd8dC4cjI3qIlUdQm032up2veQCAlMwXQRBENmZPmM8WfR1BYYZ8M5e4T8VqTd1jqq-3HF4rqevM9vvnjVzBUunl8_M_ggDn5wv46zdg3vgXjA5p0K3cGYd-fv7txwLX3TcYATEHKu_ZDlutrCjx5FuYhs8YuAFOGb_Cw9RsJpMP3WF6R7d-sQx_qy2KkmtQBWQy4Eq4XpeGn4PLNK0DA7cgwGK5falPOvLZmnZIBuAMb6QoiBxA7t_8vJSFcqwqNoz8GxzvhmFA2Zhwa5dEDG3Y6VKDAPBDVGuDiI4uA8cFMSlbaUhbw9gVcYtMCRq87UycAUjHYnDteZrZODPhnu_X8Q8ikWsahaGBYOwDPV1XVGNdEHRFH75UOg-lak-LNWQiODKMyHnfTXA4rdMWbTRUvq4oH9W4ZNjsP38_1w4G1Ohi89WNbfo5obRPeCWvZKYP9a6EMTfkbpaHdvwJWX2S3h7KOQcxwOGBzYNItQINPFOBi-JI-kHsZr43NmxGcrr1BYdzzE2x0bSAqatzgZZsjKeo7giGDCUHU5qkI2XwIEREXdSd6oRj7QbH-b2U28HoFbgrLM7Bt9udYxPFXwCgyavLy18cw5MDvAmpTwNfEy3WZB942ExIH0fW4bzodiNZhOAK2elepnlpqy84WlENR63DcQXGZEIrNPQHpNHtQbPHyIh6wiYrgvyO8AW5kBFgTCTWHSWdIyywY8-I1mJKtohqn6q_PDz3mZRBoGI_UEE-NirtTYBJAHwNp39AjCHPo9yXIvTk2Lu0NP8J4HgNY38YPM1Ulkg_4mPjYELit4Z8OB-_pp3D99kec9mEj9J4W02TGkUnd0Wv_iT7-TrzUMK9HKo3l7Y4O5CamokQuMnliBU3bKuLFgDVcGw6SbhFM_uNXMU0lUHCgrH2Ol4umG7J6y4J2PZK5OZRxlyZjIWe8d6A3ZXD-f_kelAnVJAajyB28nPiuGKANTmOGWYstuGLY6dWu00ik5rNtFTcofY9UHKLai2R7y2eLW-znMcuuPw0TSzMntxMmKr49bcLhrQwdMM0zlnEMotbJxcOrJoPvzRgWlumOIB-R3PRyh3pcEjqYQPYVju2d1v5kbx726ERLof83XYxCB6Q3jGToYYDsRMdq-whptIUXw_JOcyhmSC6Fk35-KUuzl1a6Qfd3a8JvdEi8bAppBUWtACLFWc2j2fCi7E_kQdjx328JDHekDj4osNcd0wJkYskRqqrLT6Nlx8mRLCXXmWwTTGZxnGAv7VrU_fJ7YbRVx58V2GF-ajp0rewFTsqdBI6MQHQ6sZgQ9betqahP03tEdtj_qbbCXTmvsTinU2K4T0cG4UxEsKTcGzJnEyyP0xoMCcxShtMUkztE2zD9hPBY1OP7EknbJ3Nt_hLw1TlQWwmHnZCwRd3NPoDR4XhGCxlpOCj6AMEGUwWsYsVeSjmapQrP4JisJOva8ZjUgyKK-XQpEDnz5zhB5HRwkn7uqasvSPBK-MESR92wjEj09VmxO-7oY2mu0wQvWyxeaJSGuKPtWE940qnqH3I_ehDcAXYJNSOopFKNla96JgM-trlNWsEhNK7YjXWUx6kV7lcw_cwG55uuwpNjsUf920fYyJbMpiU_IY6mC7h6uzBGSu49I6GaHuksfnq2aCR0btOqqeLh31yAmt9ZcClfFg5Qnl0LRYboRusl82xBdzQ5UkqAsEDC7Ym14RG5_HSWz9DEUMwj8UiUuCXrEccLwJNfMeh93pqA5bgaPHBzMbShk3jdDmRejB7WNS8TdWe4XXDax943zD_GsybFP4jgPQPtidE4WsEWQSjdphGoq2YAryJgehnNkMTTNtbWde3tjdIY5jOABFBGBz_PaLPAPANiYeknzay5urAgodZmuNmBOMu2EtP4-4ed1tpYJ6EHDCczPxkrAZMLjBNSBSH3jySy7IAVf6lgLi40ZkdDmT6_bnsOrrcoH1hLjkbkPQ-FUAfTfIllC13kq-RrFJi4_8RcWRhe9bWvKhWZS8oDZh75HlqxwDYsicPZtAwUs3Jrice0SYAjwL8z7-iap_4RXUpEFCa31MnB3WFYezj2c_0G-3k9p7-9sFvsT_6lhKb8afawQivGoi04F3xF-r_TX6znWq-h_5ku_SCPJWJ_y_4yfbzc2Qf9y12jb7Bs_TAISEZbTx4--p74sadJrF9TvgHUpirde_wn8MJ0N6cTjWhETDOpyfXVaXHsl5oOQY1fTq7X--o4w8B7DOj0BJNMBRP6WCA8lYULEa-_-kC77S9-I7hzP_wgVbE9PLg9OLc9ELhp39z-3j5vcuH9w69X5--VfjcFcs3uUcZpqHKpXBlrPKchdwTLJNSQpIaJwn8Faow9gKmstDnmevBl3EUQNhRaexGoR77ifU8dY0yvYriJ65R2v9JjdM1ygEjQiD14sxl-diymxwEe_vpcPsl6fCYf74ZdbrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrKebrK-S-8yvnzr_8H6KZFgg)
