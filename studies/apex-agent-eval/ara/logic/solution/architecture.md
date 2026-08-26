[//]: # (ob:992c338f)
# Architecture

[//]: # (ob:deb49a37)
## Corpus identity and deterministic ingest

[//]: # (ob:122f6d7e)
- **Purpose**: establish the accepted World425 archive, file inventory, source hashes, extraction status, and search index.
- **Inputs**: public APEX archive and frozen task metadata.
- **Outputs**: source manifest, text/OCR state, lexical/entity index.
- **Design choice**: every file receives a cheap deterministic pass; only task-relevant material is deeply read.

[//]: # (ob:e842d8c7)
## Task decomposition and targeted retrieval

[//]: # (ob:59e88810)
- **Purpose**: separate factual, risk, and contract-allocation requirements and select relevant documents or sections.
- **Inputs**: task instructions and corpus index.
- **Outputs**: bounded evidence set and explicit coverage rows.
- **Design choice**: retrieval gaps, genuinely absent evidence, and negotiated drafting inputs follow different repair paths.

[//]: # (ob:a0846abb)
## Candidate proposal and coverage criticism

[//]: # (ob:7bcfd0b5)
- **Purpose**: convert selected evidence into atomic candidate claims, typed relations, uncertainty, and requirement mappings.
- **Inputs**: evidence blocks, source metadata, and task requirements.
- **Outputs**: candidate claims, typed relations, and residual gaps.
- **Design choice**: an independent critic rejects topic-only coverage and reopens actionable gaps.

[//]: # (ob:1683a12e)
## Deterministic verification and policy recommendation

[//]: # (ob:810fc144)
- **Purpose**: verify source identity, hash and quote binding, claim/evidence role, version conflicts, and task scope before an LM judge recommends a use mode.
- **Inputs**: candidate claims and evidence receipts.
- **Outputs**: integrity state and non-authoritative recommendation receipts.
- **Design choice**: recommendations cannot admit knowledge.

[//]: # (ob:c99cdc7c)
## Staging, task selection, and bounded graph traversal

[//]: # (ob:fdbbba36)
- **Purpose**: create a non-authoritative evaluation context from policy-eligible candidates and related claims.
- **Inputs**: recommendations, task scope, typed relations, and current event projection.
- **Outputs**: hash-bound governed working set.
- **Design choice**: staging is permitted for the MVP without waiting for lawyer admission, but it remains excluded from trusted admitted context.

[//]: # (ob:15fca107)
## Execution gate

[//]: # (ob:e9f1671a)
- **Purpose**: stop artifact generation when current state violates a material reliance policy.
- **Inputs**: governed working set, stress additions, and task impact.
- **Outputs**: allow/block receipt and, only on allow, executor prompt.
- **Design choice**: hard stops are evaluated as safety behavior rather than zero-quality artifacts.

[//]: # (ob:8ce2841d)
## Executor and native output verifier

[//]: # (ob:d98bb43e)
- **Purpose**: generate the legal deliverable and apply task-native rubric judgments.
- **Inputs**: full corpus in baseline or governed working set in treatment.
- **Outputs**: DOCX, trajectory, telemetry, verifier receipts.
- **Design choice**: provenance identifiers remain in sidecars and must not leak into the client deliverable.

[//]: # (ob:c8b61196)
## Authority flow

[//]: # (ob:a92a7da7)
```text
source bytes → evidence receipt → candidate claim → integrity state
                                            ↓
                                    LM recommendation
                                            ↓
                                      staging context
                                            ↓
                                    evaluation execution

separate production path: authorized lawyer review → admission receipt → trusted context
```

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzNkNjdhZjU0MmE1MTk4Mjc3Y2ZhODk1NiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjBkNDkyMjU4IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9mODhhYzRjMGU0ZTg0MjVjMmFhM2RhOWEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2YyYzMzNDZlYjBhYjBlNzlhZmJlZGU1ZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW9tu40YS_ZWG8jYrjXm_eJ8GkzwE2CCDbJANkBkoze6i1DFFcrpJexRjXvMBu3-YL9mqJilRsi1LlmcRLDwXWCK7q6urTlWdatK3E64blXPRzJWcXE7qeu7LKOZ5GHg8dNPEi2OR8yQNo8l0klVyPZdqAabBsWbJvTC6jPzESWJweORx30m4BJ44EMVpnPiRm_AsE3ka5BnkAUQCnDwVGcoPEz-LojQMUK5URlTXoNeTy1v60swbvsAVCt7QUlP8kEGBF34CrXLFswKYhmtlVFWyJY6v9Jpla_ZOV1VeazAG59RcXPEF0KZ2LuvqN8DttpoELpumNpcXFwvVLNvstahWF2IJ5UqVi4aXi8R3LnZma_jYKvw8bw3ouahKAyXaotEtfJ5OlsDJiI4MUs8Lk0l3ZQ7XdhAaF-Z5knARCAcCSAIvFB7nvuQpJ80q3dDW5oUqATUfPFLMc0_4fhBB5vDMgTjlaE0Joey202s3F7w2bYEb9khPUWlpJpe_3E765W8n6OVKG_rU3QY5z9Dkv0ze9ltmP-KeJx9wJwMqyM1NKxWYC17DpxmqVTYzuObFxevt0rOsVYW84JrPZkW1UGI2M1XRNuie2YxrsVQNmrzV8HpFOp8COd40WmVW1DzjRhnSCIp8zg16oAErr22WlaZ9XamSRJq1aWCFd0q-IgDs7m-KAgxBZ3JZtkWBuxVLvA5krQ_TwVwTxCMNmgsNvFvH3hmUhnkqhHCD3ImiGP9LB3iaOdKlkWXVWOD1HmW9RxliS1zVlSobC1BtVyIlhm-9DnVVKLEeSRjDYyTEAu-JyDFV3sxztAroWqseoCZzL8HPHBEEXprkwsUd0qQ8EEmaRnmWeoEXcwhcCKIgzVI_EDxIwzR1szgJvSwJQ5LdcNrKLdqWfk48x4tmTjLzoh9d_9ILLgPnb45z6Tg4trczjgql9AII0snn0dXbvw4Ws6ISV9ZDnz9P740rkCh9iKrvayjffMveVhI-TT7YUJWtePD2Xkzevf2xxWT4fxuzVsunhOxt5xeck6aE9iTH4ZiZG_hEpngz2greGFaTErr0iWUEbvDKV2xvZLOuSRHK4KjHhDw-LCQhw6jw452F3la6bg1TEvehmjXjpWQSGtC4DSxRSjCKNVvOHlbiK3aCmAMaup6XRzKGZ9dwxl69etfqujLw6tUlw9GYeJRZsmYJjAsBNfqX_avShcTyxiyQrmHKclWMjIozmh19qRjKROxa9EdurlBBLMq4nCI4WZUbrhdAq2hAnCGuH7HosWKKwyYNU0iSxHWeXcU9kxrAUoAVh1G4tbyYMq3M1dTKpYU1Xp7xArXijTpgUu4kQYTsaxcCKEVJko6ZAFfkRS8X860tUBo3IZR5DKRHilkdNmmM1FA6WfjsKu6ZFIXj5AZNW2B4o1twHAaBAAR8UzHeVCsEv-gWPmBSN0p87nq7UfX1TgRdW4ZKrumh0JVy9kjy-YodKwahtoJS2juHrYtYxQIeBM-u7Z51rZA1M1WryaJ9dpmyJce0QEI_tkiHWIbiVHnAuiJNhRSx2NH3n9gJ4MamGFIYaZ0DUdkuHLKqLVE5ttCP5YBjxdSYyDQn8vFYOshllmXcj55d233sWvrJOCuxMHdVUyG7wqTKKGe1ne8GFQ5gN8wFd53dDPvNJxC2TrMFLvKIDe8MPmAdSHM3il3-xNX2U2JT1WxgIAyJAmYCK-cGWQITrSbqzIh0Ars-YINEgJcElqHva1Vp66Oys2zVNnXb9OEB-ijDPCbhEJ9IkywLfHhOvfZM2BsNbJ0uYIFZVUKhKKdSg0JrcGwY1ha5h4I0ySLXTXdh_6aH5ZrlRXXziLXuDD5gGJ56PJY8fuJqv_76K815X_a5KVs3YNiff_x7WwAwoYKqG3tRbCqPKLha2Wtb_QQy8clnZOL25oPMc0-ZvhN8Q1-t7e0UlgHmiZL47fsdhvp-wrAg0TjDS6xzv-OsN----ZlZejyO-Dc_vHn9ECk9XYdjqeEZ-o0o6en6PZVyotrUpVUa61EPAipLYKYMgUFUinSlzNGaM_Y2oq-n7-1ofnqGgiPyepbxTyKnqEh_Xraiow07qKuJeL1AdVFpWYmW7p6xtxHRfQLwj2WyZyg4orlnGf8kGjtkMUQ6JTCCUWH1wwstztENx1lr67pzonpLiU_f21M47xm6jgjxWX44ifAiGbR-uNiWnKrA7NQfcJFTc9xmg27hZ-xtRJ5P39tT2PEZuo6o83nxcAo1ZrmuVj2kZsh8Fop4zyZYuuxkYwTOioctzT59b7sE-Zx6tKXf56X7U4i3qorOkGyFP7XCVIr2VJww39n99TnBu-XuTzXsQS59DvPa0vezrH0SR5_129BtpjF5_tbKha2y59h4RO6fQGN3aPk59XxL-k_XYqD8Jy7_YdRg3E5uluudZTYyppuSOxvS4oNSBwXe_eBHjA7k0W8agPZ6_DOmA48LO2OMHx6NH6GMHyjdvpyWv5yWv5yWv5yWv5yWv5yWv5yWv5yWv5yWv5yW_69Oy49_aWp4aahX7dKNP9__dtBjL0g9y1tQcRi7ied7XhiiyjyRbuyE0o9SCJ00Df1UiiR1kzCgouwHWRaCDPM0TRxIozD0H9rQfe9DpZdBdM_7UJv3CP_q70PdTqh64fjIF57vZxDGMb39aGWM-oweksc0D73AwA-l50QuOKE7CBz1E4PAcxuBfrWUp7FwOGTc4cNqo96gX-0cUn_K84hpf2BOAnCehE-v35e0-LclpjVDa9ctriz6HrRbx07KdfU75npbV1fQcAxT3k_-3iZFO7tXYIXdbY67wDqMOlx8__aHrjhMMfN9QrpTXPQ2HevwNRi1wGqyrJTozEDv73Z7tFni2p4ECbRyveeImhvzd1aVw0HG5lnA5thIGZwClF-xnMvX9yTYwWGh6zlOHkVBIgaHjZqjLTzO7Gr65ZwsDrnjur7Ig2G5UaNzPz6-2CMTw7DcmY4zmTvQsL5XpWl0243oF-zCZOTJESAGzrXJ9wYaOw0-1Ygz1Wz7Cl3dmIegsDEmMpcaYYx5qcWUjO7kmekOSjr5nRFKWFSNovMPJjXPGzrIUXYfLK_QLjdMqjwHy1o0GlNphFCzNAdwgUzTCbzISWUgB0eNOrxR2jivNeuX8xwehEmSO4m_wcWoW7sfF1_sac4YQRhTdY3a3sXHZrUui2_S0ZAupn2AIIrGiLwLmiM07JQySrY9Jh5CDi8tNGts2Uj5zvo4ld7YNwx5LZYvmzg2DupEVzgDAW6BbhmaXeRhfPgiybFMRYl08k2i37arW3w8X5_Zr5wINwr8KIuwGxpWHrWe90Pliz1wGjxsBFqQZZBXmkzK_vGdPVCG7c4ombcG4YG87g6W9iHQ5Yw90ngPdBCysLDctOtGbDa407jtWndf3D3ZZzzckHJlhWlMrjB_XZXVTQG4swPgyDCYo0h4Objx4KJRt70Fx_O1yUPa4k6apWEYB9Emj4w65wfyyJd6CtY784639ww8HUHogdgfek7bC7D-N3Dw9l1EkCG6o3W2oBAvUdhNpa-oJmAxesjnpvMEEYea4rUh9RHMlpJ999M7dqPQLtgL3nBl6wvdK_jNGrQFhn23fMoyHKGoyKwwmxqseqJoyYfWaFhI6fX7DkjWPJ1JD5WhKPaiIHUiP0w3aWZ7srBF0jGHBb3MOOBBmkepF_rehvJszw8e4CDP_RxvDxL3-QorSkMNCBpMqhEYOmKyqlGTu_4nHnRz0T3WGZpNnDTt6CJlXRpAZLlv9xFMq_pBXCy5lnbzqIXexAM50TDDc8DMk8GS45Y1Q4ssgRCD-e930NXsI1Yr20r0djtUULBrEEnoBuB4GyI6Oj_Z9_QTTj8GSHmBn0mZhI7cVK7Rgcj97n-mB4t7Ts_botgSSpZxzIBI84iV3ocHGtNQriJpdz3_9fdvf55SnqTcYPujBhMqshH6OJjm0eSPcMAcY6HalUmaZfqIJg2QhIDgukt0K4xoRsWhAH7V0S6ykCgUhcPIRAc872YyidPIcXxLHbpqsT322Xr-mJOcXibkfs6zELGzzRujw51e5jOc1-wV4PclO-HPn3_857gJyCb23uH5MuuwTR3oU_MXWmdUVmFI3O_x76bT637Tyw6gTgXTWud7egrdV53u1M06YVOAdtw1lJvNVtDdd47XPuO__wJuAwoL)
