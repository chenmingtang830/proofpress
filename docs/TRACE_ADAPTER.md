[//]: # (ob:76e26c8c)
# TRACE decision-provenance adapter

[//]: # (ob:5c8c28d6)
## Boundary

[//]: # (ob:0813cb3c)
Proofpress imports a TRACE v0.3–v0.5 session JSON document as external
decision-provenance evidence. TRACE remains the producer of the run record;
Proofpress remains the authority for claim admission and governed context.

[//]: # (ob:d6858175)
## Import

[//]: # (ob:2e7206c4)
```sh
proofpress evidence import session.trace.json
```

[//]: # (ob:cfce713f)
The import appends one source event and one evidence receipt for each TRACE
event. Repeating the same session is idempotent. Reusing a session/event
identity with changed normalized content fails closed as an immutable source
conflict.

[//]: # (ob:b20ac71e)
## Data minimization

[//]: # (ob:081f8f23)
The adapter retains session/event identities, TRACE schema version, project
handle, timestamp, actor handle, decision disposition and revision links,
annotation/contribution metadata, and safe tool-call metadata such as server,
name, status, duration, host, and output hash.

[//]: # (ob:5af5e369)
It excludes tool inputs and outputs, raw prompts, transcripts, reasoning
summaries, state-change values, and learning-store recall data.

[//]: # (ob:eeca4c21)
## Admission boundary

[//]: # (ob:61d2b42e)
A TRACE decision disposition such as `accepted`, `revised`, or `rejected` is
an external workflow record. It is not a Proofpress claim state. TRACE import
creates no claim and no admission; an agent must explicitly propose a claim
from the imported evidence, which then independently passes deterministic
checks, configured policy, and human review.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2M2MDJhN2ExODRhNDAzOTZkMGRiMjA5OSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjExMWEyZTc5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9mNDE1NGI5M2Q1MjYyOWVhNTI3YmY1ZGIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzFmMGQ3MWIwMTAxOTdiYzBjOWZkNDViZiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNqtV91u4zYWfhXCvVwl0b8s9yq77UV70Razg72pB84RScVsJEolqWTcYIB9h33DfZI9h5JsuRt4ZpICAWLx5_yf7zt8XoFxqgbudkqsNqu-3_E8jKGAaJ1CGiZlLkJRxWFZroJV1YnDTqh7aR2etXuIs3yTxwWPIOJFWpRVVqRCVFW9jtKkSsoozrIcgGeiKuOiCqUIy7XIqzSMas7TMk5qiXKFsrx7lOaw2jzTh9s5uEcNDThSFeCPSja48C9pVK2gaiQz8lFZ1Wm2x_OdObDqwH4xXVf3RlqLd3rgD3AvyamzZdP9JtHdwZDAvXO93dzc3Cu3H6pr3rU3fC91q_S9A32_TsKbs9tG_j4o_L0brDQ73mkrNcbCmUF-ClZ7CRTEKIoglgVFjFZ28tEfwuDKXZ1GWVqVicjiPC4lZBiWGsNDlnXGkWu7RmmJls8ZaXZRHYoiqsIojMqi4iEva5FmVT26M1m349DboUGHY7KTd0bY1ebX59Wk_nmFWe6MpV_jthS7CkP-64p3Qn5cfUAP5mpAxaLj9ub9u9t_fL-7_e72l_ffv7tuxSr4qoIB54yqBod52lVglaWykU29A4vxc9LLG9y-M2TVg9Ik0h6sky3uaGgpfaN1AV60lPDVRg9Ng7byPWZIjj5WTccf8GyRyzjna47HMTlOfiRPvBNMSO4L5gpDhhEBzSUDAb2TBk9PukEIb1RP5SWfcOUb9iXX3aEnUyndWDqrT8HJpAzNibHoz0z6ezdoAVjwlzR_wxbHLmgI11HCq4R_tYZTvzDVUvlZBpO7j-F18t9__wf_ZWwKPPvxnz__xLAshhYLisHJqB4MnFkk8nW2jorszKIfvIrPeHw8dMFf7K04zHn6ldLv7u7sfqtPHcNwR0hK5Oj97Oi1M8Dl9W-201uNt07WUCmemcJrLosoqb_SlPf7o05AVNDCsk5LZrvBoDW-YRlo4RePRmLTStW7C2HHtgNeRPLMmu_AAUNAU636A6gTP5OBl85fLr56XcfJ63VSMKZOQh8dKG3nTNyMoaAAOOWUtMFUnhZRugX2eCEYGdSZTPLy9Yb94Jj8yJtBSMtc1zVM6X6gHqHMDI5-B8zAE8OSanv6wMLRlpvLWZKSQ8rj6MywW9GqscuqL4OGFy9cyFMeibhKY_kGrbd_gkKGVN13VlEcmR34noFld8C5xFyKu4DdeZL2P_8cjw_BzEsrJH6StuNGwkgJfmfml4ucqTvnZU7UySbqZFge_KHvlHZ-EjBeE_HG_EW08YE4t1H8sJCw5OGFEM_wr6Ro29VuV2M-pOmNmiYBW0WbUEQ4HIUhEmaY4VyU8RIdXedCFGlWC0iTNU9klFYA2TqWSRKVcRRVVVwj1QL3sh04z-hjtjZRhMRIK6s4jPOrcH0V5-_jcJOWm6T8WxhuwhBvTRFfjiqfFqvPf_UY4GtwJOo92D1VY5lCHPE4z4Boy8tYcPdUnq_m3klLJmWd12UikxBmLQs6nrV8jmcnaSJOIM1SkdV-aPXSFtQ7SXsbpyInfUSvNDRb_ZLXMxlcTyINoiDhpUMMxWNi4AiiXe2_zaDZOOh9u9ULs5Z3xuFLuQOrO8N4A6rFyM6gQEB3T4O5loJNqHH9ArJNAcJY57mUJZZ0PAdoMQmcwn2J5CdZMpFZXuIDI4NqlrXg_UnWX0npk-Ioj-o040UhsmxWvGD5eaR8A4H7UEtAuPQ53Gp__Jq9kz0CIMbBZ8bi8HusEmWJA1Gfm04Ols7BOU9u9USUB_aE7xk2DsiC6c600Kg_5iSibTWoxmK-O0RnqjpAHW07jCA6erHVeLhGeLyUcsTldZ4jTiEwz9FaTCGnlH_hVDGJxY4twjKqyrqIF602DxqLJLx2cBixLmDTc3CrMVaikUjhqsU3J7R9wPx7ic0bL7Ie5fj4EkVSeLDBFjsVack7eUPxnl9ArEUbBcYh8Ncs1NKPFVccmua4eSRSfCChlSiOnkEBI6Qf0A0xGC86YPvOumAxjDAK3oVc4cu8gFgUPBXhEQ1PQ9I8vL5h6KEdCdhjmM6ttkPbgvGxJ-Pl1ViP7BGagRZJYiPB0OkresP7DqFYUBwu4QxfZ2nI6zoGMTuyGKpORfelM9IkF7CIqzWKFeLY-ouxaZ6Z3jAFYTnhFxUcfmJXU60cEZ89deahbrqnCbWvGeYCOx-LCTt9AeAjTPuYzjwwYhG2rJ-h6M4M5pr6_4Tp31Kr4-SCzdEOlnLdY4sr1xwooegHttR4datrzLDHolE6IsUMZQF72iv0FDcROJCpCAJRJkmhp73F6KBT1O_WKY520SiFOSdIUfeDQVnj6DWWwX5oQbNx0Py_xH_4hH__AxkmOR0)
