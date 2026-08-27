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
**Verified knowledge infrastructure for autonomous AI agents.**

[//]: # (ob:0e0e9d9a)
Proofpress gives the next human or agent a checkable answer to: **which
conclusions may I rely on now, and why?** It binds selected conclusions to
evidence, scope, version, policy, and review, then excludes anything rejected,
unresolved, expired, superseded, or unauthorized from governed context.

[//]: # (ob:92fbc10e)
Your product keeps its models, tools, memory, workspace, permissions, and raw
telemetry. Proofpress governs only the narrower trust record that must survive a
handoff or fresh session.

[//]: # (ob:815b673d)
**Start here:** [run the 0.5 alpha quickstart](#quickstart-governed-context) ·
[see the integration boundary](docs/VERIFIED_KNOWLEDGE_LEDGER.md) ·
[choose a design-partner integration path](docs/VERIFIED_KNOWLEDGE_LEDGER.md#design-partner-integration-path) ·
[bring us a real handoff workflow](https://github.com/chenmingtang830/proofpress/issues/new?template=design_partner.yml)

[//]: # (ob:6ef36a68)
> Git made code collaborative. Proofpress makes intelligence compound.

[//]: # (ob:df7a085e)
<p align="center">
  <img src="assets/articles/memory-table-stakes-provenance-engineering-hero.png" alt="Illustration of a provenance ledger traveling with an artifact" width="1200">
</p>

[//]: # (ob:8fb4a17c)
## Choose the path that matches your workflow

[//]: # (ob:eac911f1)
| If you are… | Start here |
|---|---|
| Building an agent or multi-agent product | [Govern selected conclusions for a fresh session](#quickstart-governed-context) |
| Shipping a high-stakes review workflow | [Try the legal cold-handoff fixture](examples/verified-knowledge-ledger/legal/) |
| Handing documents across people or systems | [Try a portable artifact handoff](examples/portable-handoff/) |
| Evaluating the mechanism or claims | [Read the published handoff study](studies/agent-handoff-artifact-provenance/) |
| Integrating memory, traces, or a workspace | [See what Proofpress owns—and does not own](docs/VERIFIED_KNOWLEDGE_LEDGER.md) |

[//]: # (ob:8f7c2d11)
## How trusted continuation works

[//]: # (ob:9317a2bd)
Proofpress sits between raw agent work and the context a future human or agent
may inherit. A bounded evidence projection becomes candidate knowledge;
deterministic checks and policy evaluation inform review; only the configured
admission authority can authorize reuse.

[//]: # (ob:70d6d4b1)
![Trusted-continuation architecture: the host keeps the workflow; Proofpress keeps the reason a conclusion may be reused.](assets/architecture/trusted-continuation-architecture.svg)

[//]: # (ob:bf4b55ec)
Proofpress is not an orchestrator, trace backend, memory store, company wiki, or
truth oracle. It records the evidence, scope, review, and lifecycle that make a
selected conclusion eligible for reuse. See the
[ledger scope and integration boundary](docs/VERIFIED_KNOWLEDGE_LEDGER.md).

[//]: # (ob:4ccd51b9)
## Quickstart: governed context

[//]: # (ob:cc376e2b)
### Install the 0.5 alpha

[//]: # (ob:d6f9f208)
Proofpress 0.5 is published on npm's `next` channel. It requires Python 3.11+,
Git, and Node 22+:

[//]: # (ob:7b197ac1)
```sh
mkdir proofpress-quickstart && cd proofpress-quickstart
git init
npm init -y
npm install --save-dev proofpress@next
npx --no-install proofpress --version
npx --no-install proofpress setup --agent codex
```

[//]: # (ob:5ae48e1b)
`setup` installs the agent adapter and writes `.proofpress/manifest.json`. Use
`--agent claude`, `cursor`, or `all` for another supported harness.

[//]: # (ob:460f8108)
Import a bounded telemetry export or artifact, propose one scoped conclusion,
evaluate it, record an explicit human admission, and request context for the
next actor:

[//]: # (ob:8b9b3369)
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
Each command prints the identifier needed by the next step. `context` excludes
rejected, unresolved, expired, superseded, and actor-mismatched conclusions by
default. `ui` opens the local review queue, governed-context preview, and
lineage graph. The 0.4 `proofpress knowledge ...` command group remains only as
a temporary migration surface.

[//]: # (ob:9c6c7f6a)
## Evidence, with the boundary attached

[//]: # (ob:30685e8d)
In one preregistered controlled handoff task where a document had changed,
ordinary handoff continued incorrectly in 12/12 trials; Proofpress-assisted
handoff did so in 0/12. Both conditions continued correctly in all 12
unchanged-document trials.

[//]: # (ob:cf466876)
[![Controlled agent-handoff study: ordinary handoff 12/12 incorrect continues; Proofpress 0/12](assets/articles/agent-handoff-study-card-2026-08.png)](studies/agent-handoff-artifact-provenance/README.md)

[//]: # (ob:aea6ced7)
This supports the version-checking mechanism on that task. It does **not** show
that Proofpress generally improves agent capability or establish customer
demand. Read the [open study package](studies/agent-handoff-artifact-provenance/)
for methods, limitations, retained evidence, and checksums. Research plans and
retrospective packages remain under `studies/` with their own claim boundaries.

[//]: # (ob:cd8c1f66)
## Portable artifact provenance

[//]: # (ob:ec2e5323)
Proofpress also maintains an open portable-artifact path. Markdown and static
HTML can carry an inspectable record of admitted revision history even when Git
does not travel with the file. A format-agnostic evidence envelope can bind
provenance to the exact bytes of other files without pretending to understand
their semantics.

[//]: # (ob:20a32f50)
Start with the [portable handoff example](examples/portable-handoff/README.md),
then use the [Portable Artifact V1 contract](docs/PORTABLE_ARTIFACT_SPEC.md) or
[Artifact Provenance Protocol](docs/ARTIFACT_PROVENANCE_PROTOCOL.md) when you
need the implementation boundary. Think C2PA for knowledge work—not a claim of
C2PA compatibility, signed authorship, or complete capture.

[//]: # (ob:22a54f46)
The example includes portable [`strategy.md`](examples/portable-handoff/strategy.md)
and [`strategy.html`](examples/portable-handoff/strategy.html), plus a
[`proposal.docx`](examples/portable-handoff/proposal.docx) with its
[`proposal.provenance.json`](examples/portable-handoff/proposal.provenance.json)
evidence record.

[//]: # (ob:226a29fd)
## What is—and is not—recorded

[//]: # (ob:cfc1c3aa)
Proofpress records selected evidence, candidate conclusions, lifecycle state,
scope, stated actor roles, policy recommendations, and explicit admission or
rejection. Portable documents also record accepted versions and computed block
changes.

[//]: # (ob:5e0b34ed)
It does not automatically store raw prompts, transcripts, private reasoning,
casual brainstorming, or every save. External workflow dispositions never
become Proofpress admission decisions automatically. See the
[privacy boundary](docs/PRIVACY_AND_DISCLOSURE.md).

[//]: # (ob:32f0ea79)
## Current status

[//]: # (ob:4902cb38)
The implemented developer wedge is:
**bounded telemetry or artifacts → evidence-bound candidate knowledge →
verification and review → governed current context for the next human or
agent.** The local ledger, CLI, review UI, artifact provenance, and portable
Markdown/static-HTML carrier are available now.

[//]: # (ob:99c9f31b)
What is not established yet: a hosted service, production connectors,
general-purpose memory, or broad efficacy across long-horizon workflows. The
next proof point is a real design-partner handoff with a measurable fresh-session
decision. If that matches your workflow, [open a private-data-free integration
conversation](https://github.com/chenmingtang830/proofpress/issues/new?template=design_partner.yml).

[//]: # (ob:8deed5b3)
## Go deeper

[//]: # (ob:17d6b002)
- [Ledger scope and integration boundary](docs/VERIFIED_KNOWLEDGE_LEDGER.md)
- [Interactive verified-knowledge-ledger demo](examples/verified-knowledge-ledger/demo.partner-style.html)
- [Two-minute portable handoff demo](examples/portable-handoff/README.md)
- [Published controlled handoff study](studies/agent-handoff-artifact-provenance/README.md)
- [Documentation map](docs/README.md)
- [Privacy boundaries](docs/PRIVACY_AND_DISCLOSURE.md)
- [Agent adapters](skills/README.md)
- [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) ·
  [Security](SECURITY.md) · [Code of Conduct](CODE_OF_CONDUCT.md)

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1NmIxMTVkZTcxMWIwY2QzM2VlZDI2MCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImEwMjVjZWRlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85ZTIwYjY5M2FhNWUwMDE4YzY0YWZhOTIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2VmM2MyZDU2NDRmOWRlZThmZmU5OWQ3ZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXdly3MiV_ZU0O8Ij0awi9oXehk3RaoZlSkNR7XCoFMVEZoKFJgooAyhSHLUi_DTzPuHwJ_gX5n0-pR8mYv5i7k0kliJZ4Nrttp0Pra4FmXlzu_fc5bA-bdCiSmLKqmnCN3Y2Foup63qRabpc-KYZGYzbthDc8oyNrY0o55dTnpyKsoJnyxm1XG_HMy07tGjgRiaPWCC4LXhEaRiZzLMjI2CR6YTcNSzhu8z2uRWbQSBY5ERGSA3Th355UrL8XBSXGzuf8E01regpjJDSCofagheRSOGDr0WRxAmNUkEKcZ6USZ6RGTyfF5ckuiRvijyPF4UoS2izoOyMngqc1MrHRf6NgOkuC-xwVlWLcmd7-zSpZstozPL5NpuJbJ5kpxXNTgPb2F5pXYg_LhN4PV2WopiyPCtFBmtRFUvxeWtjJiguIjUslwkuNupPpuJcPgSLK6ahsIzIC21KXWEYZsA8h8Y0tFCyvKhwatM0yQRI3uxIOhWxzSzueo4Th1yIII5FGHKf19NR0k0ZXZTLFCZsoZwsL3i5sfP-04Ya_tMG7HJelPiq_lrwaQRL_n7j9UJkuwdkL-fi48YHmEhzKGD8o_3dF7_bH89xsPucFVpVRRItK9iiaUTLpMQTI9J4SktYukrI_pbVLC9QoLMkwy7Ly7ISc_gmo3PcuRXBtqB9iVu-sZMt0xTEZDPYI1HPMkpzdgZNPMF834wceBy2pxIfcRLP_vcv__l_f_3Lc_hQjUQ5F_X6wTkSF_DJLxaEpslp9svJBoMFE8Vk41eTjJBfJPNTUhYMPkfRq3I7zU_zcXl-OtmAFhV8rs4ddFddLuSJowXd-LzVSQUrFIahiFakWjmua-X6YvVYqxHwYMEhXRnEdx3LCgzxgEHe_-R9tpgTuIO4wB-eNfcC5j4uZ4lIeTlO8m14Zvu8dyNwFZ4PTFt4ns_DwHuARJub9WUXnJxl-UUq-KkgSRYXtITbxqplIUicFwTOUJ7l83xZEjgpcG2yqhyQyBCGCHlIHyBR9xQ5Tc5FSaqZIBn0QGbLOc0ICoPDE0pAh4DyQTVFs_JCFGRAotCKI2Y-aNf-kC8LArvBYT3ImRCLkiRVSeZwXdJyi1R5jv-biznoxy1ykRdnJWhFsUUWYuiwBqYbeb7NH7RrbyvQEmQmCrGzuUneF8tMrpMxduGyLGaUgAJlZyU-9eHZF92b0emARB5oQI96wQMk-hV5mVRkTrkgLJf_pGBN8oJWsIfj3t2CZ85gUxPoPgU9IDImhi507FMjcB-ya3dXNKhvWSrK7XoLR9I8jIZ2Lo4cavpsRaq9WZ6XQu7CglYzeEFxQSo4pCW5xCOEJyNOB5XQF-Su3eQXw1pKUBaaZmw-uYzfkoMYnyW0EN_96a_kW9KdRfLtJPt2NBrJ_-Al-XKZpCgaXFB1a_NObLnOVxbWBwtsrgr9VX5BQBeByeIEP02yJUV7V9-0W5bz1sYDSxjapk-tiD-RNL07UKL-iER1IURGCnqh1ga7gJXicoPUkKDm4mU1cBh9g3vciZ5qzX7y_rhuN1ppRws2SyohDcKOlG-Wl402xLfY8YCUUexErivY069lUpIsr4i0DHiOK9A5eQFquQAdTCKApyLjjXomAGIHpHQY464ZhStS_lurPHfIKeLnTImLXw-fvluaDpw9BhjeE9YqkjnIoK80XdX0wyJ8QdY1Ghice3EYW0bwuMF7e4TPwz4tllGalDNYA9hjADn_UpITtOwnBCFmJtIxOagIgv-h8x6ZoU-Z-TjhTk5Oytkkm5_xRNp2Jemos5Tkpz8ljN_4XScd2roV6VwqnECYj9y3E7BLy8UJWEnZsL5hCvVwugBjJtXERQFXEtZw3Am5PR863p4RB-Zj9_Vgji4U6KUoX2bwJQFLLuaigtslPsqvEKIpH2YLF3CBRifPBBmCjEEURrbthU-yr9niIxmNsnykVrC3jQQe5Qg7SFJPZDJBWJDBTk7nAztrGXEkqCceJ98-ZTPQAPM57t-iABhUby6KVCEOLwDrClxVcLRb5AsacjEeRLfMY37sreLtfTVRwKSJNPai3jIKOwV-I0gihRtSYHfsYkCX2IYH-C3gTyrZQSaPE3xQiNMEVqdQerUA2AkvQZvwPI5JRcszciGRCSU8Z8u5yAZWkcWO5wW-96Sygs-310kmL_Goka-slvxyB-4LLBv213xuWtumBbd_QFYKZ5EJ7j-prMcz0NLlcoH3oj6XylUdSVcLgdxcoK5OyjnqcIkfcZFBcQ-tKw-YGXtX_FMVh2lVBd7Rc5HR2iMYOpW3NB1CxcwSrm3ZTyJJz8DRtMwBSMN1hv9KCUYWAO2aWNOo6xlg95j8jg6slmVQ24pd40lkrLF5exreNxK1R018pPNFKj48Uy_K7VboIRktj1phvHqrf4-nISm_-9OfUbnVuAzeNFGwWzb19tZDcClmJrMpfSp5elurYnykBCvHEKmK9pIx6DfhtJJgnaVLvCnl1sCyucKIbEc82bIBWuK5UAB4WeXgyiUM7JHEuaD00LWAczJfVKUExFnJikS-GQyjwfEzBPVXTfHesigQgIDBq5a3uV3XHh7YOyc0LBbZwQNHO55JS44QJMPt4eJcpHD7wJetg1nlziTb3LwOVhClDJnUkIWxfQXJ3V0statya8ApoQ3yvRTgC1DpPcG7UhTniQwV1eEldH7YkIcScEAHbrSqwF7mMGtRR5uGdqX_3MCGmD73IsOw7j_GiLzf7TmKEqRipOe0qP26xhh9eAbGuNzePdr76uB4f-_43dH-uJMJVqra-PxhqwmpbygjNGWFoHVIW37TxMfFNI4tO7INIxAM3GHfZK5DKXdQhcL6y4Vs9J6K-texw0UO0skkRiFHwoB38w7j3R8wXZAm7LLXQz-F0OtEJicemF0o87iaxrANopCQULYoI3OHBl5sGI4XUOYLZvqWz1jAeUiF79gmNS0PLk4YObYhQo_FnPHIA5QaxXZALVsGf_CkymREvVs7dvAZFrqUdsbyRkYwsvxjI9gxjB3H_hn8a-CqqRVHXzByAxGFPpyQ7tNPT5G6kMetzirMaDlDTRCbHvWcwGUihgdkH71EgzqJj88goFrH7-Dzi4RXM_gmCODNTCSns0q9gz5_sb341Q13UUkbuL4HC216oWE30vYSEEra2_MKqjs3FrHHY59xw22666UaVHePySB0T19cXIzhkW9KmYpTKbze488nmRoI3Y87j7KNT-NQv5aZxF_i23uPunfQtbhTvnCbSr1ZbjeB0XKbJePLebodUTAAV6b-uC5rEV-Bys5KsUN2FwipR9bYWLtGUobttG4xUg2wxShKl41wrw729g_f7j9ff9gEd-AWcd9xedCcjl7aR52Ox2RzxpubA8OD_vE9ykyHs2b4Xo7nWmD-_qmbKt8hm5sXs4SB-96DU4CqL8kBoDAANRg1yi-26tjH7PLXm5sYL4rAGvXgWb9tlU-yDq6VDGDBVnN3wOZK1V53V5uwLZQ4A0wMPXCBOP6ymqHXU4hvZO9bk2yZwQTz9BzeYLwjKfAF-EzQK_rtWzjLZVbnXJN_B4FiAGDXon_j9WttMgtUZhBbvtsqgl72Sq31Y5JS86SsoWo9dXoxyVpYtJKrqaUuYeFTFY2gRZHL7cKwrcLGKo2AH5RLwDPnsKmTrHEwYDli6GxGVFp5YObU80OTxpbnSB9czryXJWsP-cOTX2oXRmoXnpP_-W-40aWocyJ3hSpzrhpGBR4OuEUUloKmrVPVqI37qh3Yl6VANXrx60oApgW080s4h2DsprBWVSYKqYTWryD3A9djgrnCtjoL2mb11Ao-JlmHwasFrs3QCTZc4XLfE5EEE7Vl7DJ597bjNyfoYEtBuFHnB49EdgqoS-CmjOB05ONF1tn-gxS0QqV2N49hy7qWRGpKPNUUnAfcU-kxY9JKAZoeVDAtw7gDPIhNhzLme5bt-O1h7hKHDTx4fMavWfSAh65rxTxwWzjSSwKq8R6bvSvgnqdVMqrfNvrnW_L-pbxaN6thaXJWtcBt91KO_3aWLBZyfDIDZKZ2XOnqdlVw9OOi1k-pOIVrCOeZtzG2OPmIdq8X4DhXNnLU2shRvf_bsvm2Gv0r9O5hcBU3BOVKWZHDpViIHPrBtagLacpGAtoGfLowjRLjpviK-qoZb_-cppj_giFxKr1AW0FYSpN6nCPY-fqstMmUlWjih2f4vwTGWQk1thGo3n1pBj5o1J4M79UGQ2bPSmnMaGc9UIC3oCwv8Ij21ER-kTXxizYeAZ-t053f3pQDblC1GdiAoI3Ic8zu2rRp4e7aPCSz24zhcMMJfccUVqufesne62jm3vlaBFqrmGeSIZBJMrhoSTUmu232pE1HqJI5aXzArs5hHbsAU3tUfz6BVhXacDgboBZrJFVKMWpAAz3WBwk6AuyXF3N1Y37e2XEQNk5OQUo-yShXeIAo0FJd4sCkhTDQfFmKAX0fxpz6ccyj0A5b16VLS6v1fExmGe_5z_snrvsaDG-J3fQ0jsSMkZKbjz88a-1IN9R2dYMwo_4T66qu1KQtLjxwTAUPLNFMupflvn6I7p2oLjDECNYWUCgYn7MEbyMgtQL2BV5RsIgqX1oHKHExroHdBtfi8UiTWLBLaNaYmDMJ1G5Q2QSM4GmCegxVd7395G2NkgD2xMs0Xdk32X13jtqB1iiAgaPkeW4Q2BHzQqcFML2sfHf9759ab0bg1GF-bEShT5sRetn2doR7Zc5b-BXZse16DpOAtQY-XTL9-pm4d2Icq2LJG_BK4EF7bJo_A48EwFy9wYcI5izrZzsD0MwM_DD2wyjgLUroZdSVhI_KjoOqA7QLqiepMBE7l6_I6LJ5Uy_qaFQC1hpxcd7r5F9x0sPZ29FI-W_Dj8kEOnxbK2pEuR8nGUzrhgRvs3eWA9CZ2wGNW7erl81vVuYRmXmw5jFc-_E3oK9OxuRdCXfppBUxpeBynmyRE7Ysyrw4kbb3BMY4qfET6A6wHU12Tpp9OPNlOXCZXEvQwHej0BCtLe3VADQ57Efk81HJ9BXHFvrb0vqAN1VtNQ4iRZ96AcYpaUIBrbJo3O8_guNTtUYUZyx1jYweyIrqgUMtPEdw1-OG50QtZujKCVYP9UNLAwDpSvTWbegdACUHZT7Oq3QhN31yy6FtlnaESLeSCQ0ykQkOpvIO3UqDQ1JLNxq1Uu9_ffBi_3Bvf3rwAvvAzSEoAbxRXSswsgMuMziTty2G2si914d7r969PXh9CB0Pt1HQfKVFKyfuOSiCUf0QyCKPwk7zdrjn5mRcmZc8GmpS5ZIBZi3zW3paJiud3KIWLCOKXIM7HrPawFuvFKRJvD-irONETe2kjTtNsjbeRG4NN0nTi6swghtVu42r3ld0iZAxpuC3wWDL5ETmpmv50pyBv6R2Da7gEiDDVWeMLHogYpI1CRTwGBazMTmWxtEhJ70V7mKP4_H4pF2X0yIHnVyIucyRSyxKYa6UYKwDAA0onHnSxF_KZQH6ZhB1epbpmjQybbONSfbqYDqo8PAiljb46gmHCoOFXms0e3UtbS3Qw4tS0E_kpCZaYJDxWkWIQqkC82mgUkGvVim6E6pUpCoSmpZ9hDwCzItC8C4SB64EKXNsZECbMfkSLAp2zBMZ7O6NsTICXh_TwsCnkm_UCl0PO7BHkW_YvmE5NLBao9qrsumSGg8ukVGitsKvLIKcaA_-qzDSqmcsRxgxWvCRSolh3Oj5fRzpNgU24C8YyMqiATdd2iLbXhGPWorHVOCoYoDNTYAKm5uknOUY2L3iqsNcRCFLBMDG4QxKBV8YXdAoSdH7A43apqzB9IArMkf1DNoS1mBM2hDEe1nkItePqHTOvcIPE_ROYT6AZnm5BW4D2Ad5-0tEDlhKs1JugTqk9naX8xLFKAU6IWSRUllzw1FvwikqF-hGn4tGplLpHILwBjBVI-FJqw8A5eYXWR1laXQDPDFwsB1bxAZzuUN5G6rulTl1yuf-tUqN4RGcscD2qBO0I_TKl677EveuQSrOOM4alxXxRsIm2VfHv3slnX-4DqgdMYIgl1ORASWaw-ApmnIEodf4gZiZR-2WYYwZzkwTDqpDq50GjhN0X3cR6YHRAhCc5TKc0YIZkdV1HFIczPFMsl7Atsprf_cjTii6RLANYtUQGbsu5Uj5UlqvStSRPGgkjwDMFrurN77EUw0jD-22zU3HMGLuMifuQEBbpqX24jG1Vk0ssNMkW1JAOLQqNvy-PUm7zUZ-bdb2BV4rT_vN66Pj3S9f7U93j44PfrO7dzx9-2Z_TwbdEBa9b5u-6ZYSXlY5y9PWWVct3xy9_nr_cBfxJLw8fr33-pXsSG7uZb5EcC5qRdDW36zmThAdJNkZ2bPeyI3uAQMM6nz3pz_LgIi6d3k8yeSTMuZRJbUyArCTnKIeqMNR5SxZSM8IH0oFll6B14XRmoG0kmE43PX9wGEtUOgVsHV39UElaI1CEEFMfc9yDKdn6dqqtOvX9d51Zb34jXQP4ICoII98q1AgASuKgVsVC8RR5rAzvNGrOLPWF-tCNng6atCJKbpOa_WC36heGn8OgPYCh1TGqQ4_4pYs8VNZ2TFRcGHoXnlmGDhOZHLXaO9Vr0auAVaPqHJLznEZ6xgh7BisGaPlEjBvVKCWhPaYipMnSiA1mmBUYkz2PwJ8y-CxNsnAkxIcKIWUMnx2ktVh2r517RaUC5aopemL3A-jSelgj66kGt8cHXy9u_eH6e7hi-mLg7d7r16_vT1uFovIYsL0DGa2rn6vjK-XbbpDZV6j9Rwz8gC5WXHQ7k6vWK9FLI-ov1PqqCTf_cd_tRdgJJ-9KfiNj02y2t1mKnzcJu9lH10osPOY-xGF1XIEcD4QpYwBLR233lDtum-RvVcHTfyUvIOXNxjwLRV2ry_LJGts6nZtT0fKnBYFOoAUAf85TVJ5sWBKA9sp3Jg7jNte7Dqtb9MVJK5Wjj6oxhCUt-Spw41QkHC0WBYy_NDkgGDFoiIHrCdiXG44qSoBluaYYMXcgEq3yBIZ6QuqiI10BomsjEMBVXq8TmWPVCq7y5bLXCsMCzezkIsjU4UjlSpE4FnfpTEmL9enR7cUIKXNvR_B6aEj6GwltS_LS1BxyXffU4p-6KqGcLF83wqMDjr2yjq7q3pLuWZj3ULhypoJgKJNd70KTtXdYyozQfNMMuigrS36bXsfX9V5c7x0eE9U66_3jw5-c7D_Yvrbw9e_f7X_4uX-VP571HaFKUeELYjS10bPZHjmTnlbGWZTyw_-3CVAy1klq7VgrOOLfASbCZaJXENkV0YYgGOyqzdtnP4Gv_7e6dcrnb9QprbekDldqNW8KsOq1YChbrUbst1uP0gNbcqzJE2v9S79cPkHJbLTD8_2Xh8eHx18-e744PClqnqBR6RZT3P8_qvdw5f7r16_bEtiCCaIQfcCcvvw7O3-3rujg-M_dE0xQQGKAUZBTYQDvNifvv7NFAZ68W7veNWDVnXAn_Gw3_DXNQSH03zz39aQf7ADRlj79eBf5qj__ogou973lD4gxzD1v-mf7pCnqvvLHewef7Ljzn9vYJ5zec-G_uLE07DLr490nRP-KObwHaZy12r36121dep1dca6xb7eXtWkvwLfSDlQe8e7jUsLsAegagdEulhlg8XH67biLiP1lX6Ro1J84Li9fbnLuCvp4nI5n2PPDxy6t2Vrhz4CzX7ezvmcpgkH7HdxJW3dQDpZo4k7TjJ6npzK5RnXe9uciU8bFzPkARzJRVvpJoVpls1kaApYRwYUb5sUoTHmC-V9qdMzMhADD6UYSO6EA8yIgV-AyT1XQ5UEUbA2VZ1zpGWTQVBFp3V5RAq4SuAC3p1PYQrftmPqWp5ngCtmuJ7pebZrtcvbJ0r0SQJ98sQnrYV-UC10d05Mywlpe9txPt9M-riNAfMkNBcWmdDGMhkN8Y-ZBYYIYVfd2Dccnxsx4GQRm37gWJYZwMH0aRxzg7uxZTErsM14_ZRuIro4O5Z3E9EFzjqzQqGJLproookumuiiiS6a6PJ9EV0C6kfMD0zqGj82ostg7EazXjTr5cfFegmEyyLH8uMo5Jr1olkvPx7Wy7Ai1RQYTYH5u6fARF6MdF3bBgz3T0aBUaazLiO-JZk2qAk0F0ZzYTQXRnNhNBdGc2E0F0ZzYTQXRnNhNBdGc2E0F0ZzYTQXRnNhNBdGc2E0F0ZzYTQXRnNhNBfmFi5M5EWWZfsBrXXmei7Mq6cK32tijCbGaGLM3zcxxrKo68TO0_w8zXHtieG1wYhMXV7XXq_3JzLnKU4vYVlOrl6wq3ryZmpJT9wrUijqw28BjyoE1w7cy1ap0hBAcSqu1fwutDI3ijiQqkIQtYtryBCihp3STYE1qvvsCBEy3LxehrLJ47WxYJn9YyTPopwWcvzGq1Po5rSod5Tgb1bfj9UgnNj1ozgy48ClgcnBJTEMLl2Um1kNTUX47ayGH_MRuju34-pvRZifby6Q_0FIAS5jDCSLY9Ogvh1anmP5PPS8wBa-4_mW64Q8gvex4TqeEYScRTT2Y4D9DsCAwFwzn5sYAf6O5d7ACPBB0hCmrBkBmhGgGQGaEaAZAZoRoBkBmhGgGQGaEaAZAZoRoBkBmhGgGQGaEaAZAZoRoBkBmhGgGQGaEaAZAZoRoBkBmhGgGQGaEaAZAZoRoBkBmhHw42YEgL2hPMbahC5V0itn6VU2P7Qmpb-DvedAweHl6rXF0sS7tZZFjOBtpZhzgp07qRE8TcewSx8H-1h58nl9IJOqXOmku0q1O3qn_q40et7lX5Vq0LQMTcvQtAxNy9C0DE3L0LQMTcvQtAxNy9C0jLW0jO_nhznu89sRlPAlwlA08EhpaPzqEiYz9FMVNzMlsE_ZvOsUpzLqfnGiHuRiBh46OubSKqoqmGu_JlHrSBgPHMl7sSBsL7QCJ_Rjw_BDxw9iQcMokpDsRhZEWwV_Owvi6X_EYICyccNf_F_lK3Tl-z8IXyHgjh8aQcRCP_SE65l2HFIKKxtAV9SOuBUadhgJl7tB4Lowjci3Xcv3Ao_bInDWT-kGyoJp7RjmDZSFmMXC4r6vKQuasqApC5qyoCkLmrKgKQuasqApC5qyoCkLmrKgKQuasqApC5qyoCkLmrKgKQuasqApC5qyoCkLmrKgKQuasqApC5qyoCkLmrKgKQuasqApC5qyoCkLmrKgKQuasqApC5qy8E9HWQipFcU8DIKI2T8gZUHzDDTP4El5BmwNwYCtYRawdZSCIgHgUfDqeyYUqBzIFL6Toz8xp6BXn9b7O_39kt-1JepDP8nQ63YtqeBV_ZsI3W8c1Gm3um6odn6vaPK-JmncwjXsgv2Pi6YQ6Q6ddD_yoERpioEknaA2MPcjFViCGoBnIs6oE9qu61IaccNh60gFbZ367aSCp9iyu1MgbmUVdBX2PwyrwDKFz4Rlh15oM0e4pmVyxg1OWQAmj4UA8y0e2cJywsAXNjhfDpgtm9pRGPDIvBerwDF3bOsGVoHtOtwE66pZBZpVoFkFmlWgWQWaVfC9sQocZnkcJxo7f3-sAlYXhNMhFIaIT_X4Yv_twcvD6Zvdo-PD_aPpweHx_suj3eOD14eaqKCJCpqooIkKmqigiQqaqKCJCpqooIkKmqigiQqaqKCJCpqooIkKmqigiQqaqKCJCpqooIkKmqigiQqaqKCJCpqooIkKmqigiQqaqKCJCpqooIkKmqigiQqaqKCJCj8mosKeCpr1ur_SWf-HFhqF0dROXS2jux9JIRSWEXkhIHIAmYYZMM-hMQ2tdSSFtuz9b0JSGKBU3EpS6Ar2_wFJCtaOc9NPH1DDckFtCE1S0CQFTVLQJAVNUtAkhe-LpADHSTAWCc_24394ksJQj1-sdjHqdTHCLjSHQXMYNIdBcxg0h0FzGDSHQXMYNIdBcxg0h0FzGDSHQXMYNIdBcxg0h0FzGDSHQXMYNIdBcxg0h0FzGDSHQXMYNIdBcxg0h0FzGDSHQXMYNIdBcxg0h0FzGH4EHIYPn_8forbymg)
