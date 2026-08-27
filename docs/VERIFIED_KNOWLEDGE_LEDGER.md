[//]: # (ob:87dd93fc)
# Verified Knowledge Ledger

[//]: # (ob:b71e5de6)
> Status: local MVP in `proofpress@0.5.0-alpha.1`. This overview describes the
> append-only ledger, context gate, and local review UI. It is not yet a frozen interchange
> specification or a claim of general long-horizon agent efficacy.

[//]: # (ob:24505103)
## What it is

[//]: # (ob:1e12da99)
The verified knowledge ledger turns **bounded** agent telemetry or artifacts
into candidate knowledge that a later human or agent can inspect before relying
on it. It is the trust layer above observability and memory:

[//]: # (ob:e2507278)
| Layer | Primary question |
|---|---|
| Logs, traces, commits, artifacts | What happened? |
| Memory and ontology | What does the system remember and how is it structured? |
| Proofpress | What may be relied on, why, by whom, and within what scope? |

[//]: # (ob:a0ce3955)
**Memory is retrieval. Ontology is structure. Proofpress is trust.**

[//]: # (ob:5e5ed818)
The ledger does not make a claim universally true. It records the source,
selected evidence, declared policy, review receipt, lifecycle state, scope, and
expiry or supersession semantics that determine whether an organization may
reuse it.

[//]: # (ob:7a1cac9c)
## Current workflow

[//]: # (ob:c3d2a28d)
```text
bounded OTLP-style telemetry or artifact
  → append-only source and evidence events
  → evidence-bound conclusions
  → deterministic checks + LM recommendation + human review
  → governed current context for a fresh human or agent
```

[//]: # (ob:2ef561dc)
The reference fixture is
[`examples/verified-knowledge-ledger/demo.otlp.json`](../examples/verified-knowledge-ledger/demo.otlp.json).

[//]: # (ob:5c8c136b)
```sh
proofpress evidence import demo.otlp.json
proofpress propose --statement "The current conclusion" \
  --evidence EVIDENCE_ID --scope demo --proposer agent:runner
proofpress evaluate CONCLUSION_ID
proofpress review CONCLUSION_ID --admit --reviewer human:reviewer
proofpress context --scope demo --actor agent:successor
proofpress ui --scope demo
```

[//]: # (ob:58bffc74)
`context` returns only admitted, current, in-scope and actor-eligible knowledge.
Rejected, unresolved, expired, superseded, and unresolved contradictory
conclusions remain in the append-only audit history but are excluded by default.
`ui` renders review, receipt, context-preview, and lineage views from the same
Git event projection.

[//]: # (ob:727d3616)
## Claim relations and profiles

[//]: # (ob:8bbc19d7)
The general ledger can record typed relationships between evidence-bound
claims: `supports`, `qualifies`, `contradicts`, `supersedes`, `depends_on`, and
`same_as`. Relationship structure is checked deterministically for valid
endpoints, shared scope, duplicates, and directed cycles. Those checks do not
establish semantic correctness. An external judge may recommend, but an
independent human must admit a relationship before it appears in governed
context. An admitted `contradicts` relationship quarantines both otherwise
eligible claims from default context until an explicit human resolution either
supersedes one claim or records that both must remain withheld. The local MVP's
reviewer identity is `self_asserted`; a policy allowlist can restrict the
declared resolver, but is not authentication.

[//]: # (ob:fdc2073a)
```sh
proofpress relation propose CLAIM_A --to CLAIM_B --type qualifies \
  --proposer agent:resolver --confidence 0.82
proofpress relation evaluate RELATION_ID
proofpress relation judge RELATION_ID
proofpress relation review RELATION_ID --admit --reviewer human:reviewer
proofpress relation resolve RELATION_ID --disposition supersede \
  --winner CLAIM_A --reviewer human:resolver
proofpress graph --scope matter-123
```

[//]: # (ob:c82e0806)
Core claims remain domain-neutral. Optional profiles add bounded validation
without making domain fields universal. The first profile is
`proofpress/profile/legal/v1`; it requires jurisdiction, authority, and a
citation locator, and permits effective dates, document type, and legal status.
APEX-specific rubrics and task logic remain outside Proofpress core.

[//]: # (ob:5d269544)
## Relationship to artifact provenance

[//]: # (ob:1acc88ee)
Artifact provenance remains the portable trust primitive: it binds a durable
artifact to revision history, evidence, actors, and decisions. The knowledge
ledger generalizes the same trust semantics across bounded workflow activity so
that a fresh agent can start from governed conclusions rather than raw context.

[//]: # (ob:067a97a0)
The two surfaces are compatible. A portable artifact can be a materialized view
of governed knowledge; it does not need to carry the full telemetry graph.

[//]: # (ob:d228259c)
## Non-goals

[//]: # (ob:9a909f30)
- Not a full OpenTelemetry collector or real-time trace backend.
- Not a generic RAG, company brain, or replacement for memory.
- Not a semantic truth oracle or a guarantee that every relevant event was
  captured.
- Not a complete RBAC, connector marketplace, or hosted governance service.
- Not evidence of general agent capability improvement.

[//]: # (ob:0c8c8244)
## Design-partner integration path

[//]: # (ob:894f0ece)
The 0.5 alpha is CLI-first: the local append-only ledger and portable artifacts
are the canonical trust core. A partner should start with a small project-local
wrapper that invokes the CLI around one bounded handoff workflow; the partner
keeps raw telemetry, prompts, workspace state, and credentials, while
Proofpress imports only the selected evidence and requires explicit human
admission before reuse.

[//]: # (ob:ad275218)
An SDK is the future stable, typed integration contract when repeated partner
workflows require the same operations and lifecycle semantics. MCP is a
host-facing tool-discovery adapter, useful only when an agent host needs
structured tool calls. A plugin or skill is host-specific installation and UX
packaging, not the system of record. The intended order is therefore: **CLI
core, SDK contract, MCP adapter, host plugin.** None of the SDK, MCP server, or
hosted ledger is a shipped public product surface today.

[//]: # (ob:7f3b61a3)
A two-to-four-week design-partner pilot should qualify one concrete continuity
failure, govern two to five conclusions, compare the ordinary and governed
handoff, and measure whether the next actor reached the right current context
and whether review changed a real decision. Only after observed friction should
we choose a CLI wrapper, SDK, MCP adapter, or host plugin. A hosted layer is a
later collaboration feature for cross-machine review, organization-backed
identity, policy, checkpoints, or retention; it must not make local or
portable verification depend on the service being available.

[//]: # (ob:b47338ab)
## Evidence boundary and current focus

[//]: # (ob:b324002e)
In the published controlled agent-handoff study, ordinary handoff reused stale
work in 12/12 trials and Proofpress-assisted handoff did so in 0/12; both
conditions continued unchanged work correctly in 12/12 trials. This supports a
version-checking mechanism on that task, not a general product-efficacy claim.
See the [open study package](../studies/agent-handoff-artifact-provenance/README.md).

[//]: # (ob:c8235573)
The next public proof point is a design-partner workflow: select two to five
conclusions from a real long-horizon or multi-agent run, bind them to evidence,
apply the review path, and measure whether governed context changes the next
decision. Until then, finance and agentic-commerce interfaces are illustrative
product fixtures, not customer validation.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzQ0NTQ2YTFiZjE4NzUyZGIzNGJjMWViNyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjJjM2I0MzhlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9jNzc3NmJhNTU4Njg4MzUyMzJlMWI4ZGYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2YxMTNkN2FlYmE0MjJlM2U0NzQ1NTFjZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXety20aWfpUuzY_dVUgK9wtTNbsaW5tyxY5TjpOZqtAlNbobJCIQYHCRrDj-uw-wj7hPsuf0BQApipIlZ5KZQZWjC4nuPn0u37mG-nBEqyZLKWvOM340P9pszj3P9wJqJ6kdhb7DE9dLmC2S8GhylJT85pxnS1E38Gy9oo4fzFMm3NT2uPDDyE-ZGzLfhe_cF5YIA4f5gRXZAWWhn8BOARe247tuwHhse4EtUtiXZzUrr0R1czT_gL805w1dwgk5bfCoCfyQiBxe-EFUWZrRJBekEldZnZUFWcHzZXVDkhvybVWW6aYSdQ1rNpRd0qXAS229XJU_CbhuW-GGq6bZ1POTk2XWrNpkxsr1CVuJYp0Vy4YWy8i1TrZWV-LnNoOfz9taVOesLGpRAC-aqhUfJ0crQZGJDnMTz43EkXrlXFzJh4C54pyFYRgk1PejIIpc33EdYScRRy5syqrBq53nWSGAciOR_Dy1bZeHVCTUcxzhCi_0fN9mQl1HU3fO6KZuc7iwg3SysuL10fzHD0f6-A9HIOWyqvEn9bbg5wmw_Mejtrgsyuvi6B3cwegDHM1LVp_8cPbmxX-_OHt-_vU3r__68uz5V2fn8uub2ZofTT5JfWjTVFnSNiC184TWWY1KJPL0nNbAzUbI_dpmVVZI42VW4Jb1Td2INbxT0DUK09A6gaU1KsDRvGjzHChnK5CYUHdO8pJdwtNRyHnspgweB2E14n3TaZHg5GvYKRd8KchL_FrBU_pUyrkkZ4NqJq7hlT-RQ8uamw0Sh-IG1Tn6OOlJSEJb-FwETyfhz-S7hjZtPSewNc3Jqx--JVlBLnod-C9r5s-sKc03KzqzL2bkLVgHQdPqadzQim4R6Hi-5duWu0XgX1e0IRn8qw8y5U9k68EDbLDB7jmN40ec8nYlyJVh2GXHMPm1Ik1bFTU5Pk7KtoCVx8cEbKdoSCNysRYH7i0c3wqdMHoERb-Sl_QGzv4VICdbU0Cfn1tAKoSjXxfFr9PpVP4HP5KX5bKekKaiTMB3AJh11tMk7X2LKGoBnMa-_wiijo9fiTUiIYi8EmBq4ormM_K6aMq8XMqXawAqBgwTswFW4hsH2OQLX_DIjh4pOC0lXoqaFGVD1vRSEEpYTrM1aYsMBFvTPL8hiKEz8qIhCpwOUBRSm1EWbxv1s7aqUOzXZXWZ5uX1PWq75_EDystc7lAn4o8-8eLiAlctCq2l5PXbl99O6-YGPJlS1AYEV1bE4OmiIOT__ud_CQWnUfBpTx4r-bbGOCL1A5s_nhsopUqkAhYwQdLsPSoISHZR_Hgh3tP1Jhf1ibG_aWd_U_n1kOKwiNlukDyFafVqUfTwRuAdLqnM1ugtCQeFn5VNvpn9VJfF1qObAyzzoyRNWeg9njK97AINTeJPWYAKU77OGvBjYOdqswng8xRimw2ofMGJdMCHOMadIPa9bbreCAiDAFnqVbYhTdlpCIHLgmenhYwDDun6w3Y4hN2UsSgS4nPSdXr7cWDmmmbAzAY00kRDiAs1PpUBbwEt5gA7B1hoBSGNQ2p9TlLRQJrrktRtlSKMw3qBSL6BTYHCGTntqe22ZrQgiTgErNxxIsffgbFvymK6LGl-n9sdPndAcjGNrTh1rU8_YwpHNADUKQRX5DWA0NsOpliZ5wJVGQGrEjSfNtlaKB9HEgi7e5pyCM63oyEvdN2IboPCmTFriY7oTtFatA2RtGTtfex42A6HojTX8SzLEZ-TrheF0uQ2ATasAPRx5wqZx1WMMoWIlZdpCn655TcTYCfQhces6AG9YZHj-n7ofk5SUcUL2EkRy4gEUtDqrEAfD2rARZ0tiykQ0xTgzg1Izkl9ywW8m5iU4widO0b7DLRExffyHZMsiHPXtiBLBHqYJZjN3SByUogTMViGYEHuaSxLZ0UE8jN2KSmTSV4lT8IUwPyGGcA7TKfgIjeDHYYp1mATmbw9Mvuqy7Q5T0GXRAUApZO8OrHnMUsjP2KJEH7gOoFjRa7nOcwORRp6XgQbxIkdxMwJ7cCj3I9dy2JB4gfcTmzPw_vXEOvLZE1Ja-5YkOPgK0eO5QRTK5o6_lvHmcM_K_7CsuYWWrnmOIa3vgitmMWgO_2rH37L_E4qqMq_VrRewfOuG4e-FYUidDCilXsMUjKtu5-cWunduc1SFjuOz1Nhdh9kW3r3p2RNaB2o-gzyViH90qL4s4nJpMtX4e2EaEskS9DzibQ9dZqyMPL9CxnaZioGvhESWavyF1EALY2oVO6Km9cbwYAXTDosGRHqWBnsETBDVLBpXhbLKaTJ2S_wiMp2RIpr2M1sD3BodjnUsy3fj6zY9Qy7BrmfEcb9KZ3ez3JSzhIegsZGZr9Blqf3e0rythMTQ0QKzCrRtfKMA6MH-zVIMyVYMarIql1TxTu5GbpiCCuAsQ245LSsMNLIb-A6iwIYmDVGNojWKtzIZXpHE1ACUiY1aAJNsjxrFKyuZZ41v5vVzA5SJ0xTT_ihYc0g3dSseVoW2cAPHWdgDym1ldRNwf9T7kB0Qog0lyYN1E_KhAwvrAosGHuJdYKXhodX5TXyA3SgyxjNloO8Ue-0pjcY6QBLUcRlMSHXK3BmyQ18L9fKGK6zZgVGd43Py3gYdtuXBmv-QcQS0cANIRnucGOQGWv-PSXhlWKeHR_fLUMK8CIC3-W-lxgaBrnwQL0fm-Jq_pdtxcRkUdQCoypgoclyJgA9sAnwnihnNjFwAutFtoH0Is9SwW4YuEd0F7BCMlfyfAH-fJMpC6rbDdCg6mXgscE6mozVymi4AJNZg9MD6QggCDUA1ixpkf2iQAgEvCgq0dYCbeVujiVpnKaub6dhZBuODXL1HmAelnwblOdhJNIoCcOg04VBPq53fWqCLcFciUIqbJdpyoClNk-bl6fyGER9lrfI1e4Jw04IfCGOknFGTb4gL19Joa_XcJji6hcappRIzfIlup1C9KGbcSypdAUp6O9qB98WBVx-T7ar-eczF8IKgZpLO9jvawYDPX50EaA62U7EL979-2x28snL_uOAblFK7diBq8QJ76yxLzD0WvCEikFVbkrQ8elU2tIaub-QjBnIQot7cUQWC5TZdNqdcPbDi-dn3zw7O3_xHPeQWT8eB7_orbXA5lVbgCPfoZPmLbq0Z6-_efby--9evP4G9tl6RNv-1gOwtyw6wHf1tvF-c_Pr1hZGmXbIk3UJTVvdMvAxdbm9sM221tyjchDTMpBTQtMw7oTV11yMsJ5QRJmCs1li8t2HALNF8Ub8JBF0AqgLZJf5Ff4sYRB_wNUaCbnYMl5decC4UMZ4Q1CgLQf-dl2mtpHpv3gPa3EXcHNcpLTNIYq4aDO8DOBPZcQ1QeTUYK3vO9Vplw4TdVqDr9QYE66VV6CQUX8FB0v8IbprBbQesBHhejE4zDRx7C7qGJSUevx9dEHIQDKNAJO5sNwg6CK_vkakD3pKhYckkKnKvLOt8BkQidkN6N3t_U0GLlM1uRRvwX3K52oM6Qeqsii0y9YBdfaLiYXo2pDTe0nKqhJMwDgW47TwpOwKQ8Ia7EHHnwqf-7ATkARAR0q1R_ah3lHpcWE1OAJ6bVTkgJAtzxMWpI0QTnZCHhS9BnD-2JIVBYcPPiyTfOFEeSfMPswFOj5-iZLqwp5CwHsyPK_AUJCdsnbUe99lRTerA1dLE0jmPO75Ke1gY1Ak6_X3nuKX0VKLM98RPLRkk1luN6iH6e2eUucCSwfUMTtIZQKf_-b0q4nidQF4UYG-T9QGmxwWrlU9ptJJxGC90ThUwGYFSyjGddLtL1tgFWiGznME9sox4AavURiIuKYyBmF0I8P1wcZISw5hCXnzl9NnEoYKdS3IOS5FI8mSJK7KGuNPJWhpr5j5ZEx0m3XObpCNGm3fmBQJXC1aPN50tqcUaKQtaMiSILACv4tLBtXBXtqPru3pg4LEswIKGYXLnO6gvtynD3pKsU69LiNkjiaPeIUwgf7Edk5sB0QK5lRLwvs8ZEohIJccN1tAWgtogsssWPUl3LiBcAYoARck8QKJyooWlrSFqhkoQII3gB2sAX-1c6auZoDfQ4MHEhaFrgZNZXAKzAJVxL2yeg0eWGlYQ-vLibRq2skZhMohmZqaUoNKcEA1vpN6KciP4KILxR6ipy9kIIivZBAHbrFxamBn2ruHkzdnp89fnc3W_FAoGHqOJSLX813P6hKCviY6QMDHVjTR6iV8Apql4JGkCDrMlmhOJSBsV2LQoiAOyKbKIiDKm0g_hsxZ416dl5IRRq5AUod1gMyria4u0BqDb5OODR2HjN70oINcXcikxzi6Gfke9CPHd-DsNFNGLKMmJCljU5mCYJIjy069b8hyuB4gWyOvq0Vt8oBaqQIYWlPCagKxaqaymFtievcRJbVn5ESACncDJxgwvj96J8dX4KDbr-8MqPSR6JTlmXpA1kq6J3TQmwFvKv57DLKI4iqrygJB7xzel7Ttm2eRgujHWdSNHzbMEjohdwN7e5LkmawyVCaik8IGdqUZZF739cAPLz3QLYkS4EXMw89CCVpqV9lUcRmTeTGqAEEqeL8rRKwQionmWgDUiKsDbZKUM8cKXfpZaLydWJo9urTx2cvTF6_OTyFPAktXv_wFf7k51IkG3BJWZH0ekT7DyqYE5S6h4SV-mxaiBdvG2tgGt1RgLveDdIujY93TxFE73aWBO1Tobs1z8MYywkFs2j5c18M6vnWlq9ldqvWAI3alMOkS6Qn5qQVdMiUzBa0yAgXhvCAI9bO79OUBB5eGkS_FsmdnF6LM7pLy_q2_FmJDTr89-5t0vOBVluCxyrapwV8MC5dgEciudwNt-XB0vbrZpc6Y0w7LcfmkjzMx01YlQUO24tL-u-GVHt7YCxkkibEf2HGS8thlNKLCCbywu_OwYzfsVg27eB9GGBxh8PeGwYd3rHc7tt7H_f3Y-5rTn6UDHcZu6jmh7TsO2J9DIVp2uQBqY8h_UxrGlp2GDmzs-l7kJr6DmweQkYHhBhGz7rjP_ga0E-5pQHuxG4rYisYG9NiAHhvQYwN6bECPDeixAT02oMcG9NiAHhvQ_4wN6JALJwwY8_y46wsPsvUB_n5yym1a3JHt-laa-JboEH6QhQ-w5LGp9BBeF4VKI-fkwvRPLibk4ueW5ogn8hfZJgI6mXqvE6_8jQsUY30OiKRd4gXy9ZzWEORvdeG7OAFjAwnagm9DuXTgCMKy-g7OteCymwFRWL2SPlq7Xt5ucgzfhemCZ5Vy69JPy4YQooz2DLzEkAG2qzEIygDcu_qQ7inBW7DoFJjzvsG-YK4qazLs6lzKRClmgRGyujVqjfITawxoFUrQLb6bYBjfAIWnoLRgAMYDya7LPd1wD9I7N_K8QLBO4wYVjztR-RPKFoJ08u4gdxdOlalX8A6QnGo4tmaRs__QDmvfnL08fbsXafWTitP3PqaRefDcJ-KyKowahF1jA6Oa2o57D856qePEAsIri0aDVpyp5ZhCzhMKMjKU6vtNiwID-bKVMS62LtVGEC-IHMLZLtZVAx9pVsnBElWbxVhikHSf6NdPcqxynlzZF3Kcwfwf3sD6KqvRrjPMKFQfB_IvZVMUlDNrdCEb8myAZvXGBg0W0iFIhxEuIXvjyhJ5V5-92ZgEXZZXa1kcAOeB9d-pyb5J1SaVnD7B_mFfFNb8u7M2PA4HjcNB43DQOBw0DgeNw0HjcNA4HPQPOBykYuq7RoR23t0ZFLr17vaUEH5qjxkSmuIH_PyRJ4VkuP7YD775xI84WJdcVsgONJKf0Ox-wO5PaFPf3l2lKftHWAaMub3eTHqoekpnU8B3U2-pB5Ud0uf-pYwIOhi4b6Rlz5E6PagHm2IQ-7Ny7lkhZB0JwErmKEBAqxMTrCmJPJ2aD1EiXb6HeNKAz71vzuU2Nadc9wa6I1Umv0XbtCdDNoSAkvtmU-66m6p4b5812B0jol2g-7RxFHAHaeq4lIWQnIQ05ZZwwVKdu8ZRut71_eMoo6XtmZI4MP7TTRV0u83dj_vnBv4ugxKxlaSe5aQJT9MotbyI-yJ14zj1Ii9IvVg4NIxiFgbci1xQI2ZRwSNhu5bFRSyjxjuutD0rEb61nLkdzD17z6wE9SmjnCfjrMQ4KzHOSoyzEuOsxDgrMc5KjLMS46zEOCvxG89KCOH6NGSBsKLoDzQr0c9JKKd0V9q9XX7bGqMgj5uiAH7tGaMgj56iWBR_uDEKC4fDGYuoFYpxjOJfZYwCDzcGu83x7e36ukwtmwykxEjjOqtBlTtT1v18qel8p17WyjozLQ6UdESGe0Ic1QkaAEWY7KkaBF0Q9Ugi5PW1fWOEuhI5V63bLlX8txpDn53qF2rCxdbHjF98CQxUQRoBdQBIAs3Qqg0KlLFGJY9dQGfmO5R0dF6I9VpZNqf3mDOLvDjx0iiyUzrOqDx-RmWwk7zKzlY8q-G-shXWO4-OG9cZevEBC2-dqNgzTsWMUzHjVMw4FTNOxYxTMeNUzDgVM07FjFMx_5AfmXPnDIwef_m9pl_gbMyEf6vPyLFYBIq98yc0nm_rLcpxWencCnTons-HuH_1oY-IiL3UEkx8LnrQRq2ZT2T_E63y2csXUxnRz6Vyq1z4dtMTNfrAUADlDghv54_8PIHM04J89_xr06ZLW1mSkaURcJuqcjTcTtUiwHrAgItDf_kndZPApu5nIxMhC7LpaVq21fRaiMtdjNtkOZhxDclVznWSfaMqFQ_7xJyBPu7_6Bc5anMLWoeXqE3B8A69uuPTakQqCzidfmjVkKA-hX-Y3yugA1yiJlIApzO7SzPuOAjLasWyxRCgJhAZFQi8IP0JefXsW53_5e0SnCzEBmJQHDXxCJA4u0vMhy9nEgwlJe0Fat0VRXSZYkBKk9LoGeSqGKbfMaf0LAcGpMrH7OoBaJIuA3bXxagtlzEbkCA_VAhvpusuQxao608GdJFtukzO8WlDTQf-luDeoaZuyOT-oaYRRkcY_d1g9OGze4c_cacfqvr7fOIO9T0LAjMrskIWxG7guKHlQioeeTz0Y2r5XFCPR3aCCbrL09ChNAjT2PIC16fBgz5xJ3xrRXPPmbv7_uRL94dHxymycYpsnCIbp8jGKbJximycIhunyMYpsnGKbJwiG6fIximycYpsnCIbp8jGKbJximycIhunyMYpsnGKbJwi-xebIuM2S7yE-kHQV1cG_b5e2o_q2HUTZMwKUxGEYV8pHjTxBtby2DbcbTuqEazUXBVYVFlgmK5BRQI42p6-i-5EKZRAt4dqsIYwzuRWU3k0uMQKT6-U-LPiqrzUiIX9XlrJkhCGnAakzFiaAasvFeKqYxfFpRCbWgJOZ50TPHK9wdQBF9UbVHJd2pNTe6BTGCGC1WGZNUNMHhY212pITXJHQuluTVHu0rne7WAaONb_ERhTJ2_rg86OQ9QpqGX7NusKtX3f0_igJ3Qu0WJly7vnm2FnbS7Sew0IqqpB5joojxpHMsMuvJxgWxRoaVNQFoxvmrLMMeBjpTRrysGCMTyH-wMoKY5KeqhpueBqCbegan2ZXG5EMCespY6pYQeswV5moFFwsDy1Cz_ADzfwsLo50vz93yBglNN_QJYaHBuU6ctU5zHKmSLbpKrhtFelOVxJ2c3J8THoJeZq-Id-UACGsXISob-ivIgidHZ8jLgukQVPNWMLEoLwWawLaYDS1ieHATGGQTH2w4Jy_k07PuAJp4daU7FLYy4iO0rtbiRx0Jc2avSEzjJ4-wrBVw-AAkAuipRmeYu8UVA7nFgchgfajWg168ZW5Z-Q6hJiber7JxDNoKEKi9CJMZyQldOL2XLV7BZ7wRCxZ6JX6yzHjKvqycl-ZPG1rEWl2PhSrSp4KK30x-ooXoDNYFmhxJSPSrTSUDbpJdypg3ZBRiNAiY3AZbdKmY5qtG0PrqRgp3ht9KsyWpuu4aLYWTBlrWFbYSp9N5BmsupJ1-WQBRBTQpEMa_CRspChjszauz6L8gqyXGlcgKo36w6qKnmowdzOkwK8oc3TK9AAXHIoHBrHrMcx63HM-p9vzPrdx_8HEO6MBw)
