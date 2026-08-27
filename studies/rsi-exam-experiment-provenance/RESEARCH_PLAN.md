[//]: # (ob:076b965b)
# Research Plan — Proofpress × RSI-Exam Experiment Provenance

[//]: # (ob:54af471e)
Status: DESIGN / PROPOSAL. This protocol-only package is under internal PR
review. No real RSI-Exam rollout, hidden-set run, or efficacy result is
included.

[//]: # (ob:85368066)
Implementation boundary: this PR freezes the protocol and offline verifier;
the release-specific RSI-Exam adapter remains intentionally unimplemented.

[//]: # (ob:d519edfe)
## Decision

[//]: # (ob:4ad2ed0f)
Proofpress will propose an evaluation-integrity layer for RSI-Exam. The layer
records an existing rollout; it does not create the research task, choose the
method, change the agent budget, run the hidden evaluator, or contribute to the
leaderboard score.

[//]: # (ob:17dc5063)
The planned provenance path is:

    [//]: # (ob:9b20b9b2)
    RSI-Exam rollout
      → TRACE session
      → artifact checkpoints and score receipts
      → proofpress evidence import
      → immutable source events and evidence
      → selective claim governance
      → independently auditable experiment provenance

[//]: # (ob:bf85027b)
TRACE remains the producer of the session record. Proofpress remains the
provenance and governance layer for evidence that a later reviewer or system
may rely on.

[//]: # (ob:bd99f4df)
## Research questions

[//]: # (ob:641dc551)
1. Can a rollout be represented without losing the identity of the initial
   method, intermediate checkpoints, discarded attempts, final artifact, or
   visible and hidden evaluation receipts?
2. Can an independent verifier detect artifact/score misbinding, altered
   evaluator configuration, broken version ancestry, and omitted events when
   an official rollout manifest is available?
3. Can the record remain useful without embedding prompts, reasoning,
   transcripts, raw tool payloads, or hidden targets?
4. What storage, verification-time, and reviewer-cost overhead does the
   record add?

[//]: # (ob:bd3fdda0)
These questions concern the integrity and auditability of the experiment
record. They do not establish that Proofpress improves recursive
self-improvement, research quality, or hidden-set score.

[//]: # (ob:4fa38076)
## Units and boundaries

[//]: # (ob:d6a53c13)
One unit is one RSI-Exam task/model/replicate rollout. The rollout has one
external TRACE session identity. Each saved executable method is a checkpoint
in a parent-linked version DAG:

    [//]: # (ob:238a3631)
    starter → candidate versions → final submission → hidden evaluation

[//]: # (ob:bf778aac)
The checkpoint is an artifact, not a Markdown knowledge revision. Artifact
files and score receipts are bound by SHA-256 and locator evidence. Research
plans, reports, and other Markdown knowledge artifacts use the normal
Proofpress portable ledger workflow.

[//]: # (ob:c51ff4a1)
The profile records external workflow dispositions such as retained, discarded,
revised, invalid, timeout, and submitted. These values describe what the
experiment did; they are not Proofpress truth judgments.

[//]: # (ob:afd16c88)
Governance is selective. It is appropriate for reusable conclusions such as
“the hidden score belongs to final version v17” or “this result meets the
declared publication-integrity policy.” It is not necessary to admit every
intermediate checkpoint.

[//]: # (ob:aca9dd91)
## Data minimization and trust

[//]: # (ob:8d5caa31)
The first profile stores identity, hashes, locators, parentage, stage,
disposition, score metadata, evaluator/configuration digests, and resource
metadata. It does not store raw prompt, reasoning, transcript, tool input,
tool output, or hidden target payloads.

[//]: # (ob:45a9068e)
An official rollout manifest is the coverage anchor. Without it, the verifier
can report internal consistency but must report coverage as
unverifiable. The profile is tamper-evident relative to its supplied files and
anchors; it is not a signature of authorship and cannot prove that an
untrusted producer captured every event.

[//]: # (ob:75eb1a94)
## Planned phases

[//]: # (ob:042489f0)
### Design

[//]: # (ob:15e2f563)
- Freeze the profile and threat model in this repository.
- Keep the generic TRACE adapter from PR #33 unchanged.
- Define the narrow mapping from TRACE events to experiment checkpoints,
  receipts, and final-result bindings.

[//]: # (ob:46f3f2b9)
### Conformance

[//]: # (ob:b33cbe9a)
- Verify a complete local fixture.
- Inject artifact, receipt, version-DAG, configuration, coverage, and
  forbidden-payload faults.
- Require every fault to fail or downgrade the correct verification field.

[//]: # (ob:ce5e5a4c)
### Execute

[//]: # (ob:8b01958c)
This phase remains blocked until RSI-Exam publishes a stable task/export
contract. Then select the first three eligible public rollouts by manifest
order, not by score. Convert them through an adapter without rerunning or
altering the hidden evaluation.

[//]: # (ob:f1eac1d4)
### Admit and synthesize

[//]: # (ob:57bf762d)
- Admit only claims about record integrity, coverage, and exact result binding.
- Report task count, version count, retained/discarded/invalid counts,
  coverage denominator, exclusions, verification time, and storage overhead.
- Keep any RSI-Exam task score as an external benchmark result; do not
  attribute it to Proofpress.

[//]: # (ob:ad472bbf)
## Acceptance criteria

[//]: # (ob:3cf81643)
- No valid fixture produces a false integrity failure.
- Every declared corruption case is detected.
- A missing or partial source manifest never receives a complete-coverage
  verdict.
- Hidden targets and raw trajectory payloads are never required by the
  verifier.
- The implementation is additive to PR #33 and does not modify RSI-Exam
  scoring, task selection, agent behavior, or hidden evaluation.

[//]: # (ob:bd9842ce)
## Upstream proposal

[//]: # (ob:20225383)
Proofpress will offer this as a trajectory-integrity evaluation/pipeline
change, corresponding to RSI-Exam’s advisor or evaluation-contributor path:

[//]: # (ob:74055abe)
> We propose a TRACE-compatible Proofpress profile that binds each saved
> method version, visible-set result, final artifact, frozen verifier
> configuration, and hidden-set score receipt into an independently verifiable
> experiment provenance record, without exposing hidden data or changing
> benchmark scores.

[//]: # (ob:e7413f7d)
The proposal is prepared in [UPSTREAM_PROPOSAL.md](UPSTREAM_PROPOSAL.md).
It is not a claim that RSI-Exam has adopted the profile.

[//]: # (ob:ed13483d)
## Canonical relations

[//]: # (ob:959f9e1c)
- [Proofpress studies index](../README.md)
- [TRACE adapter](../../docs/TRACE_ADAPTER.md)
- [RSI-Exam](https://github.com/aiming-lab/RSI-Exam)
- [RSI-Exam contribution guide](https://rsi-exam.ai/contribute.html)

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzdkOGViNjQ3MDM3MWNiNjdjNTEyYWVlYiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImY0OWQ2MzUzIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9mOGZlYzJlZTM0MmIzMTY4MzYxMWY2ZjMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzQyNjE2YTJjZWMzOGNmYWU2NDQxZmYxYSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW-tu40aWfhVC-ZNgJZn3iwNkYHR7ksZOEsPdmfxoN4RiXSSOKVLhxbbSaCC_9gEWCywW2H2aeZN-kjmnqkiW3Gr6omSAwSoY9FgUq-rUuXznqvcTUjWZILRZZGxyOtlsFhGLeRr6ke1FDk3DiAaOSzhPJ9NJWrLtgmVLXjfwbr0ibhCeEh76DhO2zyI_op5HIpswJ7XdNEgc4QXEt1lsuwn3qHCdgHlMOGGYMjeM_MALPdiXZTUtb3i1nZy-xw_NoiFLOCEnDR41hT9SnsODv_IqExlJc25V_Cars7KwVvB-WW2tdGtdVGUpNhWva1izIfSaLDleaudxVf6Nw3XbCjdcNc2mPj05WWbNqk3ntFyf0BUv1lmxbEixjD37ZGd1xX9pM_h70da8WtCyqHkBvGiqln-YTlacIBOFn7DQC_Bm-GTBb-RLwFy-ELHg1OXc893Uc8LYCx1HhALf3ZRVg1db5FnBgfJOIvnCd0MnJC7l1IupQIb7jhAOUdfR1C0o2dRtDhd2kU5aVqyenL59P9HHv5-AlMuqxr_U15wtUmD520lbXBflbTF5B3fo9AEF3LQs4_VJVWczfkfW8M8GBLCG7WZwLmxLCspPLs9fn59dvvhucfGXsx_mazaZPkmpSNNUWdo2IMtFSuqsxpN5LhakBh43XO7XNquyQsqvswK3rLd1w9fwTUHWKOLuBlNYWqNaTE6LNs_hPnQFcuSKE2le0mt4247CNAkDPB1E2PA7vO0lrzmp6Mq6yElhffztvwx1sv7-39bl61ezc-CCdX4H6zQdhDFJ4AbVkd_Cky-sJ2zUsRPfUOyEvZrtBq-EqgNqOPkwHQgPfCL8yOF_BOGvG9K09an18vz1q29_sE6si8sfL358ffaXufUGbMwCiTclLfNZWeRbS1uXBV-0BRuo3pCK7JDMAifhTOyS_JJTabyjjPzCMl4bYYpPmMuZLZ58gsGm2yzP8YabsuYWcJHfkLwlqJOzDLZcVlmztXKy5ZUlygpYOnJjJ2I0sCWwPY2eNytubUCGBWfWYF_A6mYFfD4dOTJJXTuFf558pAX_9fpRlXlets1VYcn_Pv7Hf1pvLs9enFvapswvOgu3RqhKRRzYbpQ-nRHy1IqvSVbUVoNsqUrWUuB-KeRnTZGlgGy-i_yfpYclifCZ2G89v7Tga2DP-gGl3LtgRD3RO9IgcA441ZlbL0ApSSchK0X_h9cF7ABluQXvhY_zsobTJYMyBl-h0g7E5eAo7_HDE4wR-wDKQGXBYPpXLdgHpFQoEnrDIQWzCPgScG9Zjg-kFEck5QvixYDSO5T9VGRNLfdKS8AcUoFvekBWn1kyIi0WksCjjnfQyT8WHFAxaxAdS_i7t7CG1Ncn65Lx_ATkl2cUApxOqAiz8GGEK64XEwiYnINoQwOuGzBfMCY0ZApLM4Z0QABWSyHiY5EVJLfqNl1nytLw4SqD7YpRi4-imBB6EIXIBgjC6PWmBBVCHqLua7yZWkXZgCV8T6prBh7fQr-fc7ZUEeEIbRByCOET52DaAItEJiNQGWNZsBOoPHDrtqyuRV7eWhDCgiPJlEnULRgTqUclSwRzQhrHB9H2LYbQymUAzyCEgjA3u-Fz65Vi4gb9W5WhqNGHVbytZSSNNjtGGyUJY8ku316ShlgQJWfr7FfpJiWdEAbLcH3Up4-uHLHMmAWUEO93oQPFKLKqbnphYg7B6x42p9aK1IBtU8BUMFIIm6fghyv4kozBVkASO4z570HiWQEoKTKagWJ1sL8mRSYAalGciLAyacIoDIQO8fHc-lk5ghESo4CnDkn8HRIvuqADLv0gpn7y8ojMbN_140TY9yKAOls-EPph7KffGtneCbgrgk8irYe2n1l_rjj_lXeRhVQAKZRVxQmwGQEa3Bd8BkYDUKMtQ4o5vypmY_7UhzxOuGmyQ86LsgBrW6NZPnTl3VdH7p16Hk15Qp5z0MySSTQ4ZVCf9SbnAAeo4zkYxF3TVlze8lWBSbKBugB2PNuMXJ7ygEOuvwv953ects2DFx9eG7P_1HaSIH7yASp5QWXtI0q5JahwC7aeD95506ZwLbB64E0tU_ERQxIOJ9Rhu4Z0xtbg9VGV6m0B2lVnvz54-c-sGcsCI_CzocsOOnqmD5bZHM1JtoZrp4gyyq8N4du0x5mp3J_fjagBYX7kpulujH1GKd800jNR2BH0jzwAMvtXjPDEoyJ2Qt875NyZ9UNpQeKXsc4WurwDNUKQvDaDWkGyvDOX8xs-Gmcnse_SXbfw06ZuAG3WOusk-UOh7J73R_jh2q4beLH3_DPvZ8fgjSBklJBIkB9NRRAjABeNFFnnzWMOyLeDgKQHMOMb62c-5OoqRZ0hloF3xXjGILwD92YFsJ5mo4UKHvmOJyL2fMJ0cCjfs2TFhGPMgKZkvf3p4vWby_Oz7xd9WWXN3n3ZPx0jjDmeH3u7hEE-WBYZwnbFc_KYvHX_ihEVSoJEJNyhh5w7s94a4tAFReAH43fvvpzPT-DuL78_B1Z8hWb0ViX-hJENGOu7-yb1btrVMic6V1lQdNjyTPlNV2_kC8yVfNfzwzQKCWVRLDhLoggjEUggJJ91udXS5VYj55DV40qehFXE7hMWEd9hnRYSt62xg1m7NTaRVeFnlnXrUjQLyMGWvIKQXVeP69Q5jcDl2HZKqW27IuZBlJCYOYEtUpIC9iaRSz07TWzmEu4z3_G5E4YU1rAgDCOKGTW4tkZWgZW4Tr3wAzC6VqARzux45kZv7PDU8U9t-99sG_6FVZrjKGVIzYnrBKAsw9P3__zCsdRTVdjFYB2B1iepsIkdeJJkuYdR69UqfGCF9jPOWZMQRcQTacpETNOOBKNqq0k4pNYKIIx4KzPOi8urQtnaHH0XGEP-STlvqtP2Wc3Bt7fF1ILkj2NqQegWltRtjgnFVZEVNG9BI-Z7sEjfjoeURwHIXqROdzujwNsx-KHKrd4t9gNPhDS1o4R3uxnF3C45OaBKqzihKivyObJLZe24_A5gBQtmmlNfWxAPsRIACmsMClpkjlB1-oL1GwiHViUSAN9cFWsOGRfDZ9hmkG-DqEBf0pYtOQbOraqGKSF0JJeVFAPiqmx-wMpSbZgDn3iVlgRCsBpI5SPiCAHjqONGnPGegUb1WTPw6WVlvb0d2kEUhMxxnX57o9Kstz-8hDxgpip3yGvrjKOpzSVDtwsYibk61jrWiLDmW9l63Spor8u2glekb1B7d8vM9_tSiYqDrWVfSNnZFUxvwwssEIBN6nImnDFgm8HdMRNyfeYFAGVO3DHVKJR3MjugAm4uuyoMieP9h7sZhtLzUsZJxMK-a2UpYMETK0v120DdCUIG3L8sRvTSpgmNA89hiU37Ow7F9wEmHltL1_s6AP5hEAR25EbdvkZ5Xe97SLVcMzcrsiYjuRR_Z-ESdNecyQKaobJTLPdRgu1UizTApQ0-U_XTIX8uK7kZ9qxTXW3YRQQtS6nyf7oqXH2JwtQ7LNFmIgORMEjbjfz8RJnMOqsxyIVbQaaWA7mcyVN70EHAEdmyreR5UyutymsgQXtxLCOBGKqtyvNKSA-RX9p6bldcmS95oDJFbiAzQtOAa3jqGgpEZVqplNNqay7avJcFX6ecIeGo54qDAL81hJpwF3kqpBtFDVmc-o7cAmCW4AzINi8JqyWaaoY2pALkRSb6c-tn1Ggs7sn0VfGPKpfRgNGqm3aaDlkEXAEtBJVPuQJpRHC-Jh9ipj_tSfU642ZhlMZ2QMmAmEaXZQDkZzdNTLzpnJn0b1sgV_otLksXWb1S1mzgAiAlggECBG1B4jdwM-y0z_QXuOd0cHa_tCSX6X_PWhlCPOSU4pClEH2nLJZOSHn1oZ8zGP_jmzO9P3ITHhMv4LLGpqKPoV-jdz6k-aK1Gc7DpVdFX9rfcWI9XMytcwKMqskNmoksRUmXoCBD2oKBFBhhwQOVS8wgG8ASVGd6L8--HfHEwhUQwAeJnbj9zY1ukOGJD2vtGGD0eWIiHvLYDYnPuTd4sL7xY0Qdz-3iIFVz60y_fFVgDr8vNID9uFIenP55_d3ZzA1C-Z6u2veebd67GvCIEAtJfMG4odZYB5ZV7SOno7hGxJL2V2CRFVyDWWboU0lcU_WNoDEXmQaOiEjIXL_PE4wOlRm6PbPdxBvAWc4M9zRVyULNpTeTha6phSgoswTJXlQKBH1pD3BhVAdgPeMIveBHbxFSJCQaYQ8o2df4cCvlgZI1eANJMMSZf4NoGN-tx6JZzxM0FKHvpWHHEqMxpllySJcrb2uTR1fFx9_-14jNlXKlPC-LZY0BubKUzkRvnOjjb_-HaCiXydaATJ7WHNyN4grjEEJiyUfWkun93ESVDua4jSIXmVWANtc1qbZ4JJFFWY7DcIgXe0OOER6yJHB9EsWhyngVD4cGnpGgPbUNpw8g1Gex4wV2HLndAUZnztDb5_bX0E_X8v-AnYNmT7V4AFsJYBqZDlHNyU5UY6kBxbpz7SoHkJmaXCg1pc_yJF0ynlCBhxl3GDHHVIUbWbEBU7kq5AewGvz0SeTRByUjchI-Dyjnvh86fSJtdA-7-vUBPUDIZafyhS5mvCrAH2jUGyoIOMIIQQxg5BZSVtgeFKB7adgaTKUtbvrhS-UtO9EiIWQNaDBTaNvo0uCNTGrRx9ftBvwtx7K6BvKrQpFby5xbGwKxsHNHZOEdgh019Fevso2UJFCPL8lIRScqBZIldValtipBomSDWzBlRSp8HYtXSOhQnwqXOH4nCqNLOpjMYxqfHZQlth-mlNMg6RMgoxfa7zne5ux0JfIEKApzYtpnPUbnU292UFPz3znfyIVLXoCUqbVTiLUEmIZ1cWl94XkQWqlSB5MLX3LASO0XSVWBM1oDAmMcL9eobXQCAcpgOA0zg8IAu_Ppymwl8s40vuqcxrSn-4G3m8YJZZ7tctbzyGjHGgx_sMmqd_SIR4Rwo9CVxSgV5Qx9157rB3RTm2nnW2YQ_k3vJ2c7XTdkEdCdqjhcI4wlCPCnlmdcqslkrfTyC-nCIBdDhMKwZlkRxjVoVBVSZOZDQDHP2QiP7dAXjpeImEW9UhtdX4PHo_3czpFwPyS2QwPImXpHMrR4e0fy_OatCvhB5WR5SJbagPkSuwodOEhmKEeFZgLcy7OlTNCV_-5Qt8b4skPeqwJnpysVw8JzlRChYgE75ZZr3K1slysZ82oj6lLdildtgf5F1gRkmt6VIT4JwsdgK_DSICHUNjy90ZM2pPH4BrPe2mdCEJvS0B_KLEbPuVf95zeQseq3a9xah6XfQbnBkrYYDKT72EW1J31Qe6IjWfWGwpLecQE3SwhyVL2V33UB4G4hwBoKAbpQ0JcABnAkxXY3k9ThCNGVZO1OU3CkqzWkEfp6X-usHKnqBt05ujwwzSFIHjE6KhhLWRRi2b0P6IYe--CdHt0x72ppKY-EcFxOXdJtbDTReyEf0BIHHOrjYUScdiPZTdGas1rXsLQjObNkNiqtAiNBLL915ds-5CkQ3BR43kgCOsyddRJHPsNfLANDx22_2ykJqYgQa0d977oP1lTuog-QUCqTSl3-6YIouSkGPxkejI5MqRBmHoxlXdCjfSUe10ea4IDRUXRKhLuiCqlAUyqUymUQ-nULga_ITaZbBWPYcF9pYsFC5iXMh8jfqL92QwhGCeZxQwU95Dhp6EQMoKeHbGPO4DP9mqfMDcC1TjbZhmOr9EoHGlPlrSARkECB7O14-PG3_0G-Q0pbyiq10Q_qOytSnZrVSHHFpZ4Xh-COXLe_ljGloK91yNQBJO19neiq-KarD2lsm3ZVYdWhk7jxaQEZ4qlfValWR_Pf3I8XhpryUKfrIg000vJeNRlgewjpcb-9nQyN5tOhVHu3UYVzrZGYU8leFkoLnuNOAwxKKkYzISdNwxRwQsR9ydQYxdgthDxrtMJ4-hXY7ysj31D9HimnHtyx-EdYucGcwoilx64QcDCNKLEDtw-MjKGNwdwePYLRpREsobYIfI-nfT_bmMroMfqAGQt8Af7HSlqfyG8WZy_PLt6cX_bvd4x59-WeH8sB-4DmWU7Sk-693VVDixNhctlCgjhs1M0HzEl2MrRC56tmnX_1yfDHB2TMnt-ycYDd_pdsLyDLuZu8k7-LQy_1yfN7v3wznst6fP_FZQb6DEHMG1Dqf6HfxUnHMfqzuMk41ZPP_GQOMT-2w_CP-OXZq11fqrsB21PlNMCXCpnZ9n1QORqhyrbivlWCKFUs-jnq71Ghh4H-vOcENXyR7SdOVZk5udGLwKA5xDWzesMpRpZ92N8W_Q44WiEJ7Bj4fnK7wkGi78k133O0ql_t7jvr9u0JATFCpoJVlGJ3WAHr3HOU56OHpkZ-nKr4ZE5DmZNA5oTU-391_Xn8JNn9SSrnw_45qYeGxn6XyTAvjiPhJ0EU-zRKXcijeeTYIE0akwQQBv7wSZBQJ_Z4xPwU4h0I3FzXS52E25x-5j77BsOCU9fZMxjW_-75OBj2_20wzLZZkNopo5wHfTVnMHl9u0MMVaCR9OHv11fFXtTt79jBZFc1Qs4UeCrJgXH3QPk473acdzvOux3n3Y7zbsd5t-O823He7Tjvdpx3O867HefdjvNux3m347zbcd7tOO92nHc7zrsd592O827HebfjvNtx3u0473acdzvOux3n3Y7zbsd5tz9w3u3dh38ASMBuEw)
