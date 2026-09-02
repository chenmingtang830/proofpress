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

[//]: # (ob:612fa08f)
[//]: # (ob:product-surfaces)

[//]: # (ob:57f61eb0)
## One product, four surfaces

[//]: # (ob:1aa1b52d)
- `ProofpressClient` is the canonical Python SDK.
- `proofpress` is the canonical CLI.
- localhost and hosted HTTP expose the same operation contract.
- MCP lets Cursor, Claude Code, Codex, and other clients use the safe agent surface. MCP never exposes approval, policy, or credential administration.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1NmIxMTVkZTcxMWIwY2QzM2VlZDI2MCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjQ4NjBjNjVmIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV80OTZlM2Y3MWYwMmE3NDE3Y2M4NDVkZTkiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzMxNTQxYmZkZjRkNzQzYTNjZTYwMmUzZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWuuS27iVfhWs5o_bkdi8X5SZSbl6nBlXPGPH9mZ_tLrUIABKTFOkQpDd1rr8e99gHmEfbavyFvsBJEXKrZanL5VUKnKVbQoEDg4OzuU75_DTiJZVmlBWzVM-mo7W67nn-bFleVwElhWbjDuOENz2zdF4FBd8M-fpQsgKc-WS2p4_pVHAfd-OYuEzYVGXRyLxQzsKIi-wk9ihPLTdgAuTewkLvZiZcWA7kWt7LHbcKABdnkpWXItyM5p-Uj-qeUUX2CGjldpqjIdYZBj4iyjTJKVxJkgprlOZFjlZYn5Rbki8IW_LokjWpZASa9aUXdGFUIfaGS6Lvwocty4VwWVVreX09HSRVss6NlixOmVLka_SfFHRfBE65unO6lL8rU7xPK-lKOesyKXIIYuqrMXn8WgpqBKiG_om871k1IzMxbWeBOGKuRv5wkkCKzFtGrhWwFjoQtaR4qwoK3W0eZbmApx3N5LNHctzrTjhicsD16EOE75pC4c3x2m5mzO6lnWGA9uKT1aUXI6m559G7fafRrjlopTqqXkt-DyGyM9H2Cyvpqzg4uPoAufodALbv3v54oefXxortdd9VIVWVZnGdYUbmsdUplIpjMiSOZWQXCU0vbpaFqXi5yrNFUm5kZVY4U1OV-rihnyNsVyqCx9N8zrLwCVb4oZEc8Y4K9gVVviCBYEVu5iOy6nER3WGZ__36__8_X9_PcFguxHlXDTSgxaJG4x8uyY0Sxf5d7MRw6ainI2-_zZdLYgsGcYU15U8zYpFYcjrxWyE2RXGdzSu2qy1utGSjj6Pe6YgnyiKRLzD1M7KO9n6huzbQWkVNHRnk8BzbTs0xQM2Of-P87NXF8_uZQun0ANcxqFjC98PeBT6D-Do-fMPS0EWyifkNGeCZHQjSpIUJdE6MQEjvGaCk6u8uMkEXwjj-fMDvETwRMx6kHT6WWSRXgvZcID_CBxgKfiY0Jqn2nIJzeUN-KyKKXn-_L-W9ABHvmUn1AyTh9zX6enFlHxDnhXxtBFENZF1CdMU8uTAll6Q-JaIzZ0t3-SCtETGEHBdko7UQb38hhxceEBRLUqt2LP5E3AxIZe9xM6yFPdySVJJKigPo3mRp4xm5O0GbiYn73_4kzHLsaRV4p7LDBFkh8WQx46TcPoELA7vCqGDXckKbvTQLbmMcc-Ko53N_7xd-pVb2Zl4yF2YNHEj-yG7DAyiC4edjB3DsgiMNBcwA-PAIS3Ptn1Ejwdsf3l5KZezfN3sOFmRdbomaY51WUYmguCSxUcVS8nbd2_e_PHtu5fv389fvzl78Xr-4c2fep5UWNm1yNgMqWO7D-BpxyI1YxPxka7WmTiZ5cqVSQQ0kqWJYBuWaeUkZZ2D7clQEW9HDg9gKeHiYWJqOJnlSVmsSO-6SbpqxPOF6Yz7kQNSQiRzo8j3HimlJvan1WYSF3XOabmBpN7X8SqtKugqwRoulOeHNoH1dXHIlcY04SE1H8lSiqWLkuqwdshAQ9-1QvsLz_1qsBhhgBMu1lmxWSnoddhiD688YMIeFY5lWuwp-OjdItTBwGOSZkIaMCQg7pX2q9fAR1wBcqJvDLF3JYDx2PiAI1VwLHKE_RQsDq8qS6EnsrUtVpcl1nbOWQWAxh1NkrSUld7iEEyJqO9Ggj01j8BPaxCI0wxafkiffOHGts13cZJp-GSHArnBpsXNV5TpwLIDmuQAOvpx6D2aA3UdRcaHyjSX_OqydTlyTFTKVCiklKUUgH6shaszn0MW51lWEEfRo_kb3g8vmJyUIhPgQ_keITRuOMd4re5ZXz48NJKPi2dq8pcMXoy71GoEnKpSkzkrBW1yG_2mS5TEPAFWpSwWjm8mZuQ4IXNZFGoQlBeVptlmf6TN_giwN7taF6nWOOyod1KpT_dLZT4XKm3MUrYZUBimkgMiOkl9YJYpi6SaJ1AbUa7LtE1mZWxNBVJXmiSOwz2Pm57wE9cWfhSGYeQlgJpu4LvUT8wYuYAT24FrWyL0TDfyeByZtnIM8NGVTkqb65raDnI7NTKyTdufmNHEtD-Y0dTyp6b1O9OcmsrRtxJXemB5ADPIoD8PRj89RQ6r1a_JL5dULlXwg1QoEngoo_IXmsYg5Ww189G5JFHvMH6T8mqJN2GIH0uRLpZV--v7b0_X3--xmJbP0Av8xAktPzKdjs9BFtry-fXksiVnJ64XRU7gs9juyA3yzZbcY9LI05uivEqy4kaestTYrLLTmKqkDvI5eSqSJwQcvk5xJVJMyYs1BY2JbZg9fdyRIZepyLg00qJh4TRrVkzaBWrFJM7qjrfXr85e_vL-5cndlyGCIEpg_nFI4056g9y4ld6TpbzdnUWeMG3XZxb3ul0HWfCthPP-yW1FVnSDmUld1aVoViq4tqxXCt6KbEOKfExulpsx3Cj-xwrJirVonL7CECVGC4m1HRr8w_Pn5EXDgtRgcAs2toBQBwyFCLEO0YBltTJ5aZAfBEwNOgEQkrLGfTaxG7OSdAEeVaRRzhLEaFbDUyuPvzLIi1xzgG2RMMJ_t0doufpvsMkFw_YS7ArMK9W6jT6-tu_22oTeSknWOKANniOoTynzzXDrQvpaQGdL90zxW-Ke45mRZyUuda2O-CDr7-z-_sl7p1QxZ9x3fB-n6OgP8vmW_qPScizZM_ns9Ss9Cx6ZZlCZBtWpBwj9pw8f3hKV88kmhOtkC3rW4Dd9JyWcgibw89lbksH9krO6lEU5JmcZNFyQM-Q5Y_3vx0Y9C33PTHMvSb0lnXSa3grM0CRzxPuy5QFKt8ZhoGLjVt_GyiyADbjSMJyG8kZNGwaNPQC6lXcci4QGQRyE5jbeDIoTe5TlcI2hU5OQRVYYB7jLrT8flB16NflaNaGlxy1E-CjkiSPMbXzoCwy3fc296wbtRtSxEt-2vcSiW_0elBLajR5XIXj5C2JsCbiPy53cIOJMaDVRKLGaWP6khG4UqwmDd4RKAW7MRtipP1mrkpPJUmTrnTcrtt4Og8M9KXYHMmw_oZSbsWnSrYfoaxP7PMR9Sw4FUxzp2NKYFPkRrlYFTIkop5Nu5dG0ZU3vvg7Xgs6EPHSDJNrCjL5k0V_HwysR8mVZFuUMaxtTJN_dmm2k-bw90rPZyJiNIIBttPiuNWGj2WrevcBMSMMoqmxt_FWCtxGCFBeYVOH1Zn4lNt_pKRPTtDRJCJDrBLin2YaheR-Gns1ygj8znQl1oQus1pnOS5Ee8I2We5OSgNlxs6Lj63w26h5no4v2pY6aYKdPx6dgtdgubvkoFbjULRPwnSvY2b6_fbBmBc2a02HaiRLxN-TF7dDXcKocclnUi6V2g8UNyPce8AUemZJ_B1b0QeUUQmviYS-yduDZ3Uciuk21PcqWsr6Eg4ZjxtTyA4t5nG29w6Bctcdw7l2FkmqUDnBH6_mVR0eYSCujgS8Dby-V-PGUbDowohw_ABHMLoMD-X0DJnhBkAlisCw3rXy33BmI10BTepNKgbK25KFw1aSDVEpqE4G8I1VgbYCMCIAcLgQgTSEUKu-DVgLH5pbvR8zmQe-LtuW2PSL9WhWt8-Q0iU3hmnHo95GtL6z1Ieje5bF2gyQwEdJsy7fZlvNBxayHKg-uexENiydMICVvOSvT6wZzdIrzJbQxhuIxEGWgUap7fUniNOcSgFldVTdKmhYnILf2z1p9FKzFFCbSddW4cNVWnfBikRQFP7zfikJ9yjkwLkWGeakJ3jm5q4PMIamyyakutSoVa_WMmNEdcoJZYHZnNYEDTBFF6mpdK3ewgsZL0vvQuwTUBtBLFasaEKhMDmJuTKINrxrSFRlBkM6bjOBGxK2n6t2SKumcv1fSUctApqnjnL5_-fqP85_evP_w6pcfjRU_OQDAGPXCwGQOFcwZJvxtUXOP_t-7NDk8n0FeVfAE0DXlCxSIhJTICtEjbQWwjdGqllbLqlhh8C9vz0jzuQNojckvRVu6Uh9qpCoHaygoxeqzx-F7DQTqPFX1E1zsm7N3p-9e_KjEW0HDVgccBFBJaAsamTb1t8ltX1HdI6Cv1kVbyj6SJM8TgRP7PQzqS6W9h7hfzbODwEi3gHbj2HO2EHhQBm2pP6aeqbxwVawBHa9FphhEXOWyNQXlhuHIYMc634SQb2ipeETena62wRbmo45nkP9E_jG0kkwsKPJYwzAutQ_Y7tjVt4i-47LLlq9FU1SoiiJrjBMEm62USUu4FV5nDSeKRZW9qKTdNAIdn7oNUwUw--poZ9fq3wp_WwKNJ1A3oRVcwAzUjyT9CN96AE6GrmDIhO0g3KbGg9LvHl26dw33dFsLPBmTc1nVgGOtO7x4pn6mYneOOsA5nO9PdUzeNRvJ-xakWgblya2zX3xWx9_zgY7gabX_8xz9yY8uBO1_e-jTnub7JSF70hrtTRHNkM_wf-q3P5qT_tOfOleOKn_az35WBU-TVO9_V6vhN39G8xto7e3k7_j_v-1pUt4mvHVfuECWURjtXYf_ksQdJzs0bcD0rWkXg4N8Gt0sVdfhLKOlwrbK7nbO1oAC3XtovRB8TnktdG7QfsK3BTrqiE21U2EUHNZQ5fzf3F458FVd014Z9k2GPYNhL-XTv7lq_faW1bZlsyU4dT7v78l8rUH1NF0oOxJUcN_zoiC0hG-5cQJ9si1w7iMREG7EfBpARRzmmLHlwUH7nhCURkkccvvuI-3rQ4VTJ9zTh9p-9fkP6EO5ieUDY4UeE8n9-lCqIPDUvahZ_g_tRgF6c8uyotizo3_hbtQsP7ajju2oYzvq2I76d29H-b4VuIHl0cA2D7aj7gY4x97UsTd17E0de1PH3tSxN3XsTR17U8fe1LE3dexNHXtTx97UY3pTF5__HzS7dkw)
