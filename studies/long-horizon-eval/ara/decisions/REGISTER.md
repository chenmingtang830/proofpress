[//]: # (ob:8ff49bdc)
# Decision register

[//]: # (ob:b5aaf542)
## Status convention

[//]: # (ob:98dbebdc)
`Proposed` records a candidate design choice. `Approval-blocked` requires explicit Richard/Tommy approval before real execution. `Frozen` may be used only after that approval is recorded with the exact source/configuration identity. `Superseded` preserves a consequential rejected or replaced decision.

[//]: # (ob:3d185bb5)
## Active decisions

[//]: # (ob:b1e150ec)
| ID | Decision | Current status | Admission rule |
| --- | --- | --- | --- |
| LH-D01 | Use H4, C1 versus C2, and evolving negotiation state for Phase Zero | Proposed | Do not expand to H8+ or integrity-fault metrics without a new recorded decision. |
| LH-D02 | Candidate matter: Harvey LAB MSA playbook-escalation scenario-01 | Approval-blocked | Record the exact Harvey revision, source manifest, and approvers before real calls. |
| LH-D03 | S1–S4 release chain and intermediate rubrics | Approval-blocked | Approve the exact release/rubric files; do not silently alter them during calibration. |
| LH-D04 | C1 native continuity facilities and semantic-parity review | Approval-blocked | Document permitted state in both arms and record human semantic-parity review. |
| LH-D05 | Proofpress/Harvey source pins and formal runtime checkout | Approval-blocked | Freeze commit, package/engine identity, and acquisition checks before real calls. |
| LH-D06 | Provider, resolved model, tools, retries, budget, timeout, and telemetry | Approval-blocked | Preregister exact settings; retain invalid attempts and prohibit fallback. |

[//]: # (ob:f60692b6)
## Decision evidence rule

[//]: # (ob:36acccab)
Each transition to `Frozen` must link to a portable decision artifact, the relevant manifest hash, named approvers, and any rejected alternative that would otherwise be likely to recur. A chat transcript alone is not sufficient decision evidence.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzk2Mzc0MDFmY2FjZTlmZGFkODg0NWE0YiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjY0NzQ1MWRlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83NjlkY2Q2YTUwODc5YjdiMjg1ZTY4NjMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2E3Yzg0MWZhMDdjYzFhOTNiM2ZmMjBjOSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq9V-1u28YSfZUF-7OSxW-R6i83SZsALRrE6f1xewN5P4bS1iSX3V3aUewAfYe-YZ_kzpCUJaeqkzRAAcOglrszZ2fOnBneBtx6XXHp11oFq6Dr1mWeLNMwqiSXUFaKq6JIM56KYBYIo3ZrpTfgPO51Wx5n-SpbQliKSgIvIcyBC0h4XiZKKvpZyigUcSJjERegoiJf5nmlwoJHeYoPPCnQrtJOmmuwu2B1Sz_82vMNeqi5J1czfBBQ48J_wOpKc1EDs3CtnTYt2-J-Y3dM7NhLa0zVWXAOz3RcXvEN0KUeLFvzK-B1e0sGt953brVYbLTf9uJMmmYht9A2ut143m6KJFw8OG3ht17j87p3YNfStA5ajIW3PbyfBVvgFMQ8XaZZpCAYV9ZwPWzC4MJ6mZcYmZxnYbEsxRKjkkFe5AkhM9bT1da1bgGR7zNSr_lSFmlU8XApZcTLRCRVFYeyHK8zoVtL3rm-xgvHhFMaq1yw-uU2mNzfBphlYx09ja9BrQWG_Jfgpw7a8xfsiVHwNniDF9mTgrLse6XBLWrTbuZbY_U7087hmtcLbvlCgRyy4Bavnn3_4uL1s1dnjQpmn8Uq7r3VovdoZi240468Ql2tucMgexjs9R59E_Qr3ZJJt3MeGnzT8oZy_OAKMzzvCFawavu6xgvJLWYTxniI2sgrPFJUVVoKJXE7JtLDW7ru0-lCyK8NEgssvp1ccqUGLB1RD25w5St2arvfdYSIUo80Ct7PDi5FxnmVpfEDlxee-94xXKBEEerHXH7FTu1_xGdZKAEfXvOzfF5iXXXGgbpkE68YZ5K3SissUKbA6U3L5NZoCWfs8rxDUiJB5oTggK1DvjwAlqAcZEJkD4CdS6-vyebEq4_E4sT2x8IfQZSFIP-xxzv24im7O2T9jj3prcUIMjcG9I6dq0a7kRJYjOzuf-0dm8_n-OaAbSjzB8iqPMzLWOSnuYjuFbQSBpMficjfHnokLknOpZRcfKH3Z1xumbe8dZooxbxhl99Z8w7aS9b0zjMUtita5Wyvdfdh_5Anb2Z73QqwMdCOtbTARzUY3uyl5VFNbY0fbO7dTdKKZAV51Rnd-qFT2METacX-F0nFG9LkWsvdkYVjnT4yMnSAfyjhzlR-XWFOwHZWT53CiWjFozKNcgUVHstlVJVhHuHvqOTLUKaJLLD9VirhkINUseCACUnLPBZhVSpeEVai5aD4Y7ZWS9RCWgjiMM7nYTGP49fRcpWWqzD7OgxXYYiHpoAfd7L3R6u3_257GEg6KveWuy3uX-ZxIaoyL5KExGOwcSTmE38_WZwnq4LHaRaGQuRDEAarR3q9t_rJ-juZVVmaFFFSySIUe7NHkjyZ_RKJvRpPjYMJg7cdUlZ79kpj07Nq8do0zY7x6QQTUBlL4xM-w1uQQ989OypUjqMUMJxvFDNtjScrjBzzW-4PRrRj-xGC3eDohK8BrWFGmTO9lbDA6FR601s-KAEJiNd-h34u-g6JRFS9ZDS3gL2G4bI0S_3W0z50YIGGNIJg8bmrkRbqXivOTjSVKdp5lVZxUVZlJop9tI_6zCGJn9Y4JquJzIQKs3SZLw_UOPSSyeoXNYe__KdXPzyfPw0jXPnZAXueztiTiFEZoq0n8YwhPVCcTX2NcFkLG4OhG8JN_oBhntlLvAGw_4I1aGXPMQJpGEojkYWMoCQ_L76mWKP8wMZipuYV72vPGsDZTLohyaZHBqCfm0Pu7zNyhDemi98zt8HpDuyKPeeY5x374fxb9uPFOcOM7oQxV3NwktcTagktt9rMhyt_SHFcejW4PeLaZHT_KTCbyIdOW13hl8MYopG1GLYH3Ee3tTvGnaCHi-jP3_-4SHFHDRQ4rCDdDkYoMLYBpelSthdDVE6iHJfgCOZkbTEeY5WuwX3D1JgCh79aT3VWj3UGDVO9pZQiRC3GCjoGmlKAI9bygcHUsHXbY8oYKqqusfVSPSFkBxgHr-Uci4Rej336NOinRvYNURWLs9GeKm8kEV5fGCxwbpvR6ph7tu3R-N-4OAabjbybvlEWU8amPHW6HY1iWhqq-h6NNVN3JrqdxPqdBXhHF28Q6YxN33kLaDfYdO-lZsq9RFmcxpHB6kdIkI9waeKxM9zjsLrQaYOfFfUM68TUjpaxKAAfRK82gBAINMIdXXrMNpXN7jT6lxb27WivmOAxgxukBBomvukWj2gEj3loOj-GCA1ttUBdrxCzwDsj7FMT5b6bZSrGr2y-LJb3bedoyDwI4efMi3uRzWJQsSqSVOX3InsYISfbXzINsv2AMBvKiAroGol2X9iMkMwYffsd1feU8nZ3aB9DUU2VMrSwG9PX2FXQqr3RWOGCZsIrwPpDJMjt3p6xc6p7P2KXVncoezjeAHW9oWL7qsIOS9WiPgzeX1rTm_f4939nguS8)
