[//]: # (ob:6ec771b4)
<p align="center">
  <img src="assets/logo.svg" alt="Proofpress logo" width="88" height="88">
</p>

[//]: # (ob:de7999eb)
# Proofpress

[//]: # (ob:7542280e)
[![CI](https://github.com/chenmingtang830/proofpress/actions/workflows/ci.yml/badge.svg)](https://github.com/chenmingtang830/proofpress/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

[//]: # (ob:e667d986)
**The governance layer for agent-produced knowledge.**

[//]: # (ob:92fbc10e)
Proofpress gives agents a shared, auditable answer to: **What may a future agent or human rely on, why, in what scope, and under whose authority?** Agents submit bounded evidence and propose conclusions. Deterministic checks and configured policy evaluate them. An authenticated human authorizer decides whether they may enter governed context.

[//]: # (ob:62009490)
[//]: # (ob:thesis-summary)

[//]: # (ob:53ef8f8a)
## Why this exists

[//]: # (ob:87f7edac)
Most agent infrastructure governs either the inputs to work or the execution of
work. Documents, databases, RAG, memory, and ontologies organize what an agent
can reason from. Traces and observability show what happened while it ran.

[//]: # (ob:9727fa6a)
Proofpress governs the reusable output of that work: conclusions, findings,
analyses, decisions, and artifact-backed claims that a later agent or human may
be asked to rely on. It preserves the evidence, verification, scope, authority,
and lifecycle that make a conclusion safe to reuse. It is not a generic
knowledge graph, agent orchestrator, task tracker, trace warehouse, or RAG
platform.

[//]: # (ob:86aa6033)
Read the full [product thesis](docs/THESIS.md) for the model and the
[verified-knowledge guide](docs/VERIFIED_KNOWLEDGE_LEDGER.md) for the object
and lifecycle semantics.

[//]: # (ob:41b3a522)
[//]: # (ob:governed-handoff)

[//]: # (ob:cf8ae608)
## The governed handoff

[//]: # (ob:9b444bbd)
```text
Your documents, code, runs, and systems
                  |
                  | bounded evidence projection
                  v
Agent submits evidence -> proposes conclusion -> checks / advisory policy
                                                      |
                                                      v
                                             Human owner decides
                                                      |
                                                      v
                              admitted + current + in-scope context only
                                                      |
                                                      v
                                         successor agent or human
```

[//]: # (ob:8282eb31)
Raw artifacts, traces, and agent reasoning can support a conclusion, but they
are not themselves admission. An agent can propose, evaluate, and read allowed
context; it cannot approve itself or administer owner authority.

[//]: # (ob:612fa08f)
[//]: # (ob:product-surfaces)

[//]: # (ob:57f61eb0)
## One product, four surfaces

[//]: # (ob:1aa1b52d)
- `ProofpressClient` is the canonical Python SDK.
- `proofpress` is the canonical CLI.
- localhost and hosted HTTP expose the same operation contract.
- MCP lets Cursor, Claude Code, Codex, and other clients use the safe agent surface. MCP never exposes approval, policy, or credential administration.

[//]: # (ob:ed5c57b7)
All four surfaces call the same versioned operation contract. Local Git-backed
and hosted SQLite-backed installations have different storage, but not different
governance semantics.

[//]: # (ob:8db33fda)
[//]: # (ob:quickstart)

[//]: # (ob:4ccd51b9)
## Python-first quickstart

[//]: # (ob:70af4929)
Proofpress requires Python 3.11 or newer.

[//]: # (ob:1522656b)
```sh
python -m pip install -e .
export PROOFPRESS_LOCAL_TOKEN="replace-with-at-least-16-random-characters"
proofpress hosted --help
proofpress mcp --help
```

[//]: # (ob:6b08a324)
[//]: # (ob:python-example)
The same lifecycle can run in-process for a local Git workspace or over HTTP:

[//]: # (ob:d50b7fde)
```python
from proofpress import ProofpressClient, ProofpressError

client = ProofpressClient.in_process(".")
evidence = client.import_evidence("run.otlp.json", idempotency_key="run-001")
candidate = client.propose_conclusion(
    "The bounded result is ready for review.",
    evidence["evidence"],
    scope="experiment:demo",
    proposer="agent:runner",
    idempotency_key="proposal-001",
)

# A human authorizer reviews through the owner surface. A successor agent reads:
context = client.context(scope="experiment:demo", actor="agent:successor")
```

[//]: # (ob:ea362434)
[//]: # (ob:choose-deployment)

[//]: # (ob:43d5590e)
## Choose a deployment shape

[//]: # (ob:5da4d7b8)
| Use case | Start with | What it gives you |
|---|---|---|
| One repository or an offline/local workflow | In-process client or localhost HTTP | A Git-backed ledger, local review, and governed-context reads |
| One owner working across several devices or coding agents | `proofpress hosted` | A private, single-owner workspace with durable storage, scoped credentials, owner web review, and HTTP/MCP clients |
| A workflow-specific evidence format | A profile or integration | Typed evidence validation without changing core authority or lifecycle semantics |

[//]: # (ob:9b6ded86)
The hosted reference is deliberately single-owner and single-instance. It is a
private deployment reference, not a multi-tenant Proofpress cloud or an
enterprise collaboration product. For the Render Blueprint, bootstrap flow,
credentials, backup/export, recovery, MCP, and security boundary, read
[Self-hosting](docs/SELF_HOSTING.md).

[//]: # (ob:99949965)
[//]: # (ob:authority-boundary)
Submitting evidence or proposing a conclusion never admits it. Agent credentials identify and constrain callers; they do not carry owner authority. Only admitted, current, in-scope, actor-eligible conclusions are returned as governed context.

[//]: # (ob:6bafd8a0)
[//]: # (ob:integrations)

[//]: # (ob:8641828f)
## Integrations and deployment

[//]: # (ob:5ae3101c)
- `proofpress.profiles.experiment` validates bounded metric, table-cell, and derivation evidence.
- `proofpress.integrations.repository` binds one repository change to Git and check receipts for self-dogfood.
- `proofpress.integrations.matter_catalog` and `proofpress.integrations.document_extraction` are optional evidence-entry integrations. Their output remains candidate evidence.
- `proofpress hosted` runs the single-owner hosted control plane and web review surface. See [Self-hosting](docs/SELF_HOSTING.md).

[//]: # (ob:b877cee5)
[//]: # (ob:reading-path)

[//]: # (ob:a3e02529)
## Read this next

[//]: # (ob:3159be00)
- **Understand the product:** [Thesis](docs/THESIS.md) → [governed knowledge and context](docs/VERIFIED_KNOWLEDGE_LEDGER.md) → [FAQ](docs/FAQ.md).
- **Connect an agent:** [trace integration](docs/TRACE_ADAPTER.md) → [MCP and WebMCP](docs/WEBMCP.md) → [repository dogfood](docs/REPOSITORY_DOGFOOD.md).
- **Run it privately:** [self-hosting guide](docs/SELF_HOSTING.md) → [`render.yaml`](render.yaml) → [deployment examples](deploy/self-hosted/).
- **Explore prior experiments:** [study catalog](studies/README.md). Research evidence is separately scoped; it is not a blanket product-efficacy claim.

[//]: # (ob:6ec793e2)
[//]: # (ob:limits)
The current product is Python-first and single-owner. It does not provide multi-owner workspaces, customer VPC packaging, Notion ingestion, multi-repo knowledge ingestion, or a universal OCR/RAG platform.

[//]: # (ob:e9a649ec)
[//]: # (ob:compatibility)

[//]: # (ob:6e4b22d6)
## 0.6 compatibility window

[//]: # (ob:34226b85)
The old `proofpress_sdk` imports, console aliases, and portable top-level commands remain as deprecated forwarding shims throughout 0.6. Use `proofpress legacy ...` for portable artifact ledger and provenance tools. These shims are scheduled for removal in 0.7; the legacy implementation remains maintained for integrity and security fixes.

[//]: # (ob:85117b99)
[//]: # (ob:docs-release)
See the [documentation index](docs/README.md), [study catalog](studies/README.md), and [GitHub Releases](https://github.com/chenmingtang830/proofpress/releases).

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1NmIxMTVkZTcxMWIwY2QzM2VlZDI2MCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjViZTg5YjY3IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9lMGYwNmQ5Yjk2NDk0ZGIxOWQ2YTYzYjYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzMxNTQxYmZkZjRkNzQzYTNjZTYwMmUzZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXdtyGzmS_RUs-8XWkFTdL5zp3tDI6m7HuFseyTMdE6aDBgoosVrFKk5VUTLX7tfd932YT9gP24eN2L_YTAB1oUSWrjGXHTqi3VKxkEgkEpknM5H05wEtqiSmUTVL-GAyWC5nrusx03S58E2TGRG3bSG45RmD4YDlfD3jyYUoK3i3nFPL9SZ2RP3Q8p3YFLFjOkyE3Asiwwz9iHlhzKIwcFzDEabpeCJ2Iy-OmRFapifCkPEoALo8KaP8ShTrweQz_lLNKnoBM6S0wqmG8AMTKTz4oyiSOKEsFaQQV0mZ5BmZw_t5sSZsTd4WeR4vC1GWMGZJo0t6IXBRG4-L_GcBy10VSHBeVctycnh4kVTzFRtH-eIwmotskWQXFc0uAts43BhdiD-vEvh5tipFMYvyrBQZyKIqVuKX4WAuKArRZSIImecP1JOZuJIvgXDFTBix4fGQhZ4TOpyZICzq2cxDzvKiwqXN0iQTwHm9I-nMNl3HZDGPHe47NrUj4RmWsLlajuZuFtFluUphwRbyGeUFLweT958HevrPA9jlvCjxJ_Wx4DMGIn8_gMmyahLlXHwafIB11DoB05-dHL364WS8wLkeoiq0qoqErSrYoRmjZVKiwog0ntESJFcJSW9VzfMC-blMMiRZrstKLOCTjC5w47p8DWF4iRs-mGSrNAUuoznskFBrZGkeXcIIT0S-bzIHXofNqcQnXMOL__nLf_zvf_3lJTzUE1HOhZIeaJG4hie_WRKaJhfZ19NBBJOKYjr45jfJ4oKURQTPkOuqPEzzi3xcXl1MB_B2Bc83NK5aL6W60YIOfhm2TIF8wjAUbIOpjZE72fqKbJsBtQo0dGMS33UsKzDEIyZ5_y_vj19_ePGgs3AIegCb0bds4Xk-DwPvERwdHLybC3KBNiGjWSRISteiIHFeEKkTI2CEryLByWWWX6eCX4jxwUEPL6EFhsh8lHTat8hFciVKxQH8j4ABLAQfErriiTy5hGblNfBZ5RNycPDTnPZw5JlWTI0gfsx-HR5-mJCvyIucTZQgqlG5KuBoivJlz5SuH3umYMbGlKeZIJrIEAS8KkhNqlcvvyK9A3sU1aTUZK7Fn4GLEfnYSuw4TWBfPpKkJBUoT0SzPEsimpK3azAzGTl_9bvxNIMhWolbLlPwIBssBpzZdszpM7DY3StwHdFlWYEZ7dslJ4q4a7JwY_LfN0Pv2JWNF_vMhUFjJ7QeM0vnQNTusJaxPTZNAoc0E3AMxj2LNF3L8sB7PGL6jx8_lvNptlQzjhZkmSxJksG4NCUjQWCTxSf0peTt2enpt2_PTs7PZ29Oj4_ezN6d_q7lCd3K5olkRkBty3kETxsnUjI2Ep_oYpmKl9MMTVkJDo2kSSyidZRK5STFKgO2R11FvO05XIP5MRePE5PiZJrFRb4grekmyUKJ58bRGbZPeqQEnswJQ899opSU70-q9Yjlq4zTYg2SOl-xRVJVoKsExnCBlh-0CVhf5n2mlNGYB9R4IksJDL0oqHRrfQc08BwzsG5Y7tedweAGOOFimebrBUKv_hPbP7LnCLtU2KZhRs_BR2sWQR3G8GOcpKIcw0ECxL2QdvUK8BFHQE7kjoHvXQjAeNGwx5AiHAttYT0Hi92tShPQk1KfrWhVFDC2Ns7oAJQ5GsVJUVZyij6YElLA4iJ6bh4BPy2BAEtS0PI-ffKEwyyLb-IkY-yRDQrkGibNr-9Qpp5hPZpkA3T0WOA-mQPcjjzlXWWalfzyozY55ZBgyJQjUkoTCoB-KIUrI5--E-eaps_C8Mn8dfeH51E5KkQqgA-0PUJI3PAenq9wn-Xmg4WG4OPDC3z5JoMfhnVoNQCciqHJLCoEVbGN_KQOlMQsBqxKIyZsD-K_0LaDyIG4WIKgLK8kTR39ER39EcDe0eUyT6TGwYxyJgx96t8w8vmAYWOaROsOhW4o2SEig9RHRpllHlezGNRGFMsi0cFsycyJ4HB84ti2uetywxVe7FjCC4MgCN0YoKbjew71YoNBLGAzy3csUwSu4YQuZ6FhoWEAG13JoFRt18SyIbbDJwPLsLyREY4M650RTkxvYpi_MoyJgYZeSxz1wHQBzIgQNKZ9-vk5Ylipfiq-nNNyjs4PpEI9YYMyor2QNDohp9bMJ8eSBD-D59cJr-bwSRDAL3ORXMwr_ds3vzlcfrPlxGg-A9f3YjswvdCwaz47Uajm8-7gUpOzYscNQ9v3ImbV5Drxpib3lDDy8DovLuM0vy4Po2S8XqSHjGJQB_J5-VwkXxLg8E0CW1KKCTlaUqAxssZGSx_2aFzOE5HycpzkioXDVI0Y6QE4YsTSVc3bm9fHJz-en7zcvRnC98MYjj8LKKul14mNtfSeLeSt9yx0hWE5XmRyt561EwXfCjgfHtxWZEHX8Ga8qlaFUCMRrs1XC4S3Il2TPBuS6_l6CGYU_g8jyihfCmX0EUMU8DQvYWyNBv_14IAcKRZKCQYbsNEAQukwEBHCOPAGUbrCI1-OySsBRw10AkBIEinzqXw3vBUnF8Ajeho0lkCMpiuw1GjxF2NylEkOYFoIGMF-6yVorv4N2OQigulLYFfAewWOW8vly_Ott03IqVCy4x5tcG1BPUojzwgaE9LmAuqz9MAQXxN3bdcIXTN2qGPWxDtRf33uHx6810rFeMQ92_NgFTX9Tjyv6T8pLIchW14-fvNavgUWmaagMgrV4Q8g9O_fvXtLMOYrlQuXwRbomcJvck8KMAqSwA_Hb0kK5pccr4oyL4bkOAUNF-QY4pyh_PuTUs9c7nMkuS_JqiEd15quBTaWJDPw94XmAZRuCYsBFRtqfRvisQBswFHDYDWUKzVVDI63AGgtb8ZETH2f-YHR-JtOcmKLsvTnGGo1CaLQDJgPe9nY807aoVWTu7IJmh43wcOHAY9tYTT-oU0w3LY1D84b6ImobcaeZbmxSRv97qQS9ERPyxCc_Ag-tgC4D5s7ugaPM6LVCFFiNTK9UQG6kS9GEVhHUCmAG9MBzNSuTKvkaDQX6XLjk0W0bB4Dh1tC7BpkWF5MKTeYYdDGQrS5iW0W4qEphzxCjqRvUUeKfAemFh1mCV5OBt1o0eTJmuzeDscEnQl44Phx2MCMNmXRbsfjMxHlSVHkxRTGqqNIvr719jjJZnpJL6aD8XQAAmi8xdf6CI_VVLP6A3gTpDHOq3Q5_rkE3gbgpLiAlyr4eD27FOuv5SsjwzAlSRAglwFwS1O7oVnrhl5MMwJ_pjISql0XsLpKZVwK4QFfS7mrkASYHaoRNV_vp4P6x-ngg_5Qek1gpw3HJ8Bq3gzWfBQILmXJBPjOEHbqz28vTI2gqVodvPYSRfwVObrt-hSnaJCLfHUxl2YwvwbyrQU8gh8jlH8NVuRCywkITfnDVmT6wYvdSyKyTNUspaEsN6H34BiMmp5vRi6PGuvQSVdtOTgPzkKV-JR2cIe2_GjRwU0k1VjBl461L1H88FO8rsEIGn4ARHDsUjAgv1ZggucEIkF4WBRrLd-GuzH4a0BTcpIKQZlOeSCuGtWQCqU2EhB3JAjWOsiIAJCDDQGQhgiFlg9BK75tcdPzwsjifmuLmnTbFpHelUWrLTmNmSEcgwVe69naxFrrgh6cHtMTxL4BLs0yPStqOO9kzFqo8ui8F5GweBQJCMk1Z0VypTBHrTg3oc24K54xeBnQKKxefyQsyXgJgBm3qn5KVIkTILe0z1J9ENbCK5FIlpUy4VhWHfH8Is5z3j_fgoL6FDPAuBQizI-S4M6X6zzIDCRVqJjqo1SlfIk_g8-oFzmCt4DZjdEEDGACXmRVLVdoDhag8SVpbeguAWkH-hF9lQKBeORAzOpIaPcqIV2eEnDSmYoIrgXTlqo1S5jSeX-O0sFhQEblcQ7PT958O_v-9Pzd6x-_Gy_4yx4AFlE38I3IpiKyuwG_Tmpu0f8Hpya76xuT1xVYAtA1tAUIIkFKZAHeI9ECaHw05tJWZZUv4OEf3x4Tdd0BaA3Jj7lOXeFFjQRjMEUBFauNHrufSyCwyhLMn8DGnh6fHZ4dfYfirUDDFj0GAlBJYAkaGhb1muC2zahuEdCdeVFN2YMgyXWFbzOvhUFtqrS1EA_LedYQGMItQLuMuXYDgTtpUE39KflMtMJVvgToeCVSZBD8Ki_1UUAzDIYMzrGMN0HI17RAHiHuThaNs4Xjg8sbkz9A_NE9Jam4oBDHjsfjj9IGNDPW-S0i97ioo-UroZIKVZ6n6nACQTUVHukSzApfpYoTZBGjFwzajbEv_VM9YYIAs82O1uca_67gP01AWQLcCangAo4B_hInn8C29sDJwBERRMKWHzShcSf1u0WXHpzDPWxygS-H5H1ZrQCOaXP44QX-mojNd3AB78H4fr9i5ExNVD40IaUZLF_eWvuHX3D5Wy7oCJ5U26_nyCs_MhG0_dO-qz3q_pIoW9IS7U3Am0E8w_-md38kJ-3Vn1WGhip73ms_i5wncSLn31VquPc1mnvQ2lrJ37D_f95SpLxNuDFfsIFRSuHQ7lr8TRI7Vtb3WofpW6996Czk8-B6jlWH45QWiG3x3G2sTYECWXvQVghsTnElZGygr_A1QAeXqLKdiFFgsWNM59-7vOKEnrBj34zBDfmO6UdR4IBqhk15pVs36dYMurWUz__kqnX_klVTsmkITuxfttdk7ipQPU8VygoFFdxz3dAPTOGZDotBnywTL1tCICCcMPKoDypiR7bBTBcMtOcKQWkYs4Bbu5e0rQ4VTOxgSx3KCTwj8tz4r1GHcmLTA4wVuJGIH1aHwoTAc9eiptlftRoF0Jubphky1wr_gatR02xfjtqXo_blqH056p-9HOV5pu_4pkt9y-gtR-0GOPva1L42ta9N7WtT-9rUvja1r03ta1P72tS-NrWvTe1rU_va1P-T2tQIef8HLlBZhgFgz3hity8oEHA7KldwYIvepiLXFnEQB5strD_NsU4Dhl58Al9yV4Pv7bd7WogCP_axXvDY-X6QSRQJTxMIxSCiLcApYSJPIUKgkdSpLngDHHeJ0ANdTl9zV-hbfky9R4uhm5DUfCADhViV0qRpDJHH8JiqKHVS49veFkJKPcO2H8vWGeyAZCQGlSPvaxeu1ENbk3ffn5y_PkdLIe0evr2Ao5b2VZVMZlPXsh7LVldVayA_mmNWIo77lDUCRRUqAdnO2-afMQOqiNyhsTuG9KhtyBzHYYw_aWYI_HDkNPsTZi5r-y4dMGbxEC0qY62-36JUgW_9p6fXFgIOSzDbfBJ3Z_S68bzAB-LlGgs08XCZZ-jfMQ9TrpYy7yEDyb62Se5Grs_8Z-iRPwId3nhZhp9t7lRX02C5t7OofRxS27Mc23lYjfSOps55npdi1MZ5vZ382BUX3ij4HksKIN6WBhY3luIO3e4b19ckzKnDfRY8nYcvEuhFABbIF3KOQiOYgYRfZPEFYkBVslnnK_Jlmn0ZjUbNf9OOJqkS8OYh9GCyG18U8ige8WzoMKwQsShkfiRBOJsmDFUHq0AbQVsb5fRsJAt8PxLCfe4W4UJt2AjCg3mfIlFbGJZ748satA-A1WX4oF97br3c1w1suiEThvHI2Ubk4OAPWEyDg5UpL6VNwuTggLx_t8NH_fe__yd5f5HfDHd3XHlp4dQNPnQ37RHnWDVUDpFovISBDbKjYGPNlc4QNPmmHSiqZx6kecNLYmAh7ZQW8HgXWNpO9uQThLcYvFD-M40UKEKcIStBDK_RUB1OboKl8S7ws32aVyKGuEgtoHEpGtLUSUc5p_jU1DV34ZjtM7xJsktFnwsIwjCK03uCZNsKwMUq4Te474CRO2R_0xs2woewEjD8eBfWeCzZrXvaQRLb6Z7P82tFuMlNVflIRhUjdXjw9zZZjZcFxrvgwPYp1F0sCBNJAU6_SRCj_1yVMkUrI5VO8naXS9-xhErmGsHxZqUECWCpZCQdFTkg5BqG1m58vMsd9wi-a-0hNFUCR-3AFMF4l3u9Yyc3iPbsYcdZbqf4A12Wuiil3YzOYWBqVlZl0T_KyKRfGB2Xd9fB0RN11rBxNAFdsjy_HO9yWHeJZiMboR0SQYe09fR0PNEdhDcdxnZ5dzxNn0okBWxam6ds_W5XKNKRy5xJdxEo9m23Fs8Efmmg6LoDWkrMi0mkqnFZG7cYr-e4y5dCLJF8Y9AaUIql9EyW1AQtojlZwGkpEpWsgmXpyxwbEn_YNceeLw_ces2xuZJ2j2uO-wTFPkGxT1DsExT7BMU-QbFPUOwTFPsExb0TFPdvRrn5XVem_8v2FoK_StuEw6wwNkyHUZ_7dmj5tum5niOEH8SOZRkxjZlvsFgElicCJ_Jtn0WRYXq2j9-DZe5a0M2mCcucmObE8rY0TTRflb1vmtg3TeybJvZNE_8QTRPcoaAMIUTgdts00QbQWy6D3B0X1-fUxi4224ud9op9J1RubxbdK_itLzRy5kSGQS3mNXrUiYc10adEuDp-E59EJK9VQMA5zfAT2NI23OAUtFBdRTo7-m5IFmKRF2vd4JBVOVhNTF7mxQXNYMuUuuEmIlPylrOOBQhe1h6TdzJU2JIVL-f5tRoNgGwpcFdV8gaUsaBZz9balgBMHpqOGTTtAp0YfcuRe2jUjYoOsQegE9ilcjgFS0HTtRQKaqj-XEY_2t2NGI0uUTFlIUSRpAT_cYzi5okFdZ5mDA5YiQNgd_QRlpf36g7czSz0EMOXJMZTI-_b1ce7Ps6Sw26uvlJm41JsXjaWvShyxlUp5HyJuipICfAIU0TTrL3gB8B0OR827MNJl_0n2AJTAfMyCrwUhQ4HyTUYsnkOhOV9QFCeaXaPC4CALhh1AsCK1G8v8jaZjU3k-KhcBdEIEvySkqLgo84isaqhKfzx5Oz1t69PXs1-9-PpT29OXn13MpN_n20QzRn-4yQ3JV4K2Fuwa30X1AxAgMyLPId5zQXzTrpki026TwKkbvwBjEgNi4VW20TTyYm0Vun-CY76vDHwoGZk2qHT3KTs5DzaNo0nJDDUny9bH972TfofiEmwJ-T2gKtpdqT7rZi8Vt-MG31Tu7SyeyzgsXZjh4Tyq6TMZT4ZXdg2-vf58-WxA68eOPB7aVNUHKq9598fz3XnAflVc6X5V03vQe3MwQSmf9_yvtmlUpv0O_pKIipgnCEgPmuCmk5WrjZxT0ixaUUeEraSRhHEiNdy0bIj8ipFKjFnXVxUSEz1mQApfSSGDVwb6hoJ2FyaArQXvOnE-TW6ZxgknYbsWUSHjRcz5SVw3aUIunizBWXf3rpvb32G9lYubMsPIpsbVoO9O1lkLe-nJIPH5E3d0ahBnXL1WrTnv3-TVKKGe7orVCfw5hROA09imTQEeQBUAsmoU4kHpvlomnUC0Psgh31X776rd9_Vu-_q3Xf1PrirN3Zs3_NtGnCnMUOdqt62DrP71OdqfBEKw_Eg6qLUaSxoW7JrLegDS29Ne5zr-54H8qQNNupU4zT5p1XVvkjs0-kaxf3C7FCMFYxDZQnqLC_QfN3aCn36YEALQyT2-AK73zpQ3Uw21FZF6Y4CFU2AW-uE1BHSsNV2LcrOaXWJrURsAYQ4EIpkMgqDTPmCyml-2doSikwtZYst-OSNAl5r46Tc-KqQKaLGgUu95N2m7GHNWdM3qtaDqz9E_FPjJLmSo0Z-o3IJQVqcRG1Qqr5QTXOnbqk1PXAKmnwh79bLbvyre4rxM2QY2_zkhSEZHOCdqQZ3y725naQgX7bVUmtAbnPbZJQJI-rE-015tXOF4LFl0pH0u3hbUOegKDpFuTPd89HQHeoklepDrbAZsesfQNj5iiu9BSuPqWKgJvPWgM1YrsWo4f2YfKszOWdC5sZ_m66ErLoBUsvzClHoUl7tBAu4seWozavloYIJQ-yilv8i7hAB73CzV7G-_zeUCj3NHthHfCtztP9qgv1XE-y_mmD_1QTP99UEYN2NMHa47VsNcuncUdmi_3fdNNGEzdgUALeo7UdNHbZz-aTV__vcJ6njXxrYzOUunCLRtNu3V0walX_KrRFtOdrSgLZpSPxeBQJJ59uj3-uX4Se5BagGBwfHOYDvqC2VSY5U4aSjXTVzZ0fHJ7OjV0dv33VpI65Apn4SDH7U7_508lv4pX2pc8b0yWla19-enr9-d3r2p9mr0---PT191WHvDIPAqoZH6VqyV3YUbKNQclPN1MwfC-lPx2u6SD9-eNH5Tb_Qce06KsXdkA8Pm7kEP6yZwhYbRDPAVS5zSdpylYq7u7rvx6Bh-pp34-2w00igxip4InGdzGk2hTAGB-9SVG3rUYx1t2itSnv77_rYf9fH_rs-9t_18Tf5ro8Pv_wfxbTTbA)
