[//]: # (ob:874e3c2a)
# Problem

[//]: # (ob:8fdbb3ce)
## Observations

[//]: # (ob:c4c9425a)
### O1: Cold handoffs can silently inherit stale or unsupported state

[//]: # (ob:40d78ed1)
- **Statement**: A fresh worker assembling a professional deliverable can rely on a prior worker's summary without knowing whether its conclusions remain current, supported, authorized, or in scope.
- **Evidence**: The controlled trust fixtures in the frozen panel inject stale authority, unsupported approval, and revoked approval at the S3-to-S4 boundary.
- **Implication**: Continuation quality alone cannot reveal whether unsafe state propagated.
- **Provenance**: user-revised; retrospectively compiled from the frozen study protocol.

[//]: # (ob:72e59d68)
### O2: Integrity and substantive correctness are different properties

[//]: # (ob:703aa18b)
- **Statement**: Version binding and provenance can establish which state was authorized and why, but cannot establish that a legal conclusion is substantively correct.
- **Evidence**: [`protocol.md`](protocol.md) and [`../relaybench/CLAIM_BOUNDARIES.md`](../../relaybench/CLAIM_BOUNDARIES.md).
- **Implication**: The intervention must be evaluated on state continuity and bounded work-product quality, not marketed as improved legal intelligence.
- **Provenance**: user-revised; preserved from the preregistered claim boundary.

[//]: # (ob:4255e111)
### O3: Governance can create an information and operational tax

[//]: # (ob:8e55081a)
- **Statement**: Distillation, policy judging, graph selection, evidence expansion, and compilation add tokens and latency and can omit task-relevant detail.
- **Evidence**: Invalid attempts, cap amendments, route telemetry, and per-panel operational records retained under [`../relaybench/results/`](../../relaybench/results/).
- **Implication**: A governed handoff must report quality and overhead rather than safety alone.
- **Provenance**: ai-executed; derived from retained attempts and telemetry.

[//]: # (ob:7f6acab6)
## Gaps

[//]: # (ob:5d5ccd33)
### G1: Ordinary handoff has no explicit admission boundary

[//]: # (ob:fdbff750)
- **Statement**: A summary can mix observations, proposals, superseded versions, and approvals without a machine-checkable rule for what the receiver may rely on.
- **Caused by**: O1 and O2.
- **Why it matters**: Unsupported state can become a downstream premise without an auditable transition.

[//]: # (ob:ed0d6b5e)
### G2: Safety benefit and clean-handoff tax are usually conflated

[//]: # (ob:b5f49a95)
- **Statement**: A single aggregate task score cannot distinguish clean continuation quality, protection under a trust failure, and the compute cost of verification.
- **Caused by**: O2 and O3.
- **Why it matters**: Product evaluation needs matched clean and stress cells, explicit unsafe-propagation endpoints, and retained invalid attempts.

[//]: # (ob:eb885b7d)
## Key Insight

[//]: # (ob:00f5ffa4)
- **Insight**: Keep the worker's legal task fixed while changing the handoff representation: ordinary portable summary versus a version-bound governed knowledge ledger with deterministic blocking and verified handoff receipts.
- **Derived from**: O1, O2, O3, G1, and G2.
- **Enables**: A paired 2×2 design that separately measures clean continuation, controlled protection benefit, and operational overhead.

[//]: # (ob:5a9d5738)
## Assumptions

[//]: # (ob:e2ed49ea)
- A1: The three selected LAB Contracts-derived task families are useful professional-workflow fixtures but do not represent all legal work.
- A2: The frozen rubric measures work-product coverage, not legal correctness in deployment.
- A3: Controlled perturbations model plausible handoff failures but are not estimates of their population prevalence.
- A4: Within each model/task pair, matched sender state, worker caps, task sources, tools, and evaluator make the observed paired difference interpretable for this panel.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzczNjUwOWFkOGU0MTcxN2EwYTIzNTRlOSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjEyMTc4ZmJkIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8xM2MyZjQ5ZjFmOGM2NzRkYTQ5N2Y5YWMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2QxYjRiM2UwMjYyYzVlOWQxNmJkNTkzNCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW-ty28YVfpUd5keblJRwJ8j-UpxMxpO09sS5_HA9zGL3gESFW3CRzHj8HH2gvli_swBI6EJKkTR12tHEsUVwsXuu3_nOAfRhIqsmiaVqVomeLCdluZq7gW8tpA7Js-f2XFrScX2PFpPpJCr0dqWTNdUN1tYb6fjB0lEq8ogW-C9wVCznFDu-9pwwnGtXB3Hs-raSwUJG2sbC-dzypZJqEbpO5Nmxwr46qVVxQdV2svzAH5pVI9c4IZUNHzXFDxGluPATVUmcyCglUdFFUidFLjZYX1RbEW3F66oo4rKiusY9pVTnck2s1JXLVfFPgrptxRtumqasl6en66TZtNGJKrJTtaE8S_J1I_N16FqnV-6u6Nc2wc-rtqZqpYq8phy2aKqWPk4nG5JsRNux52Ec6Ul3ZUUXZhGMSyvbVU7sLWI7DlUw97T0FvN4IdkKZVE1rNoqTXKC5INH0hUbLnLJcmBgnxbaDiLtL1yvU6eXbqVkWbcpFHZYTlVUup4s336Y9Md_mMDLRVXzT93XpFcRTP520ubneXGZT95BhyEe2MFNqxOqT9MiX882RZX8VuQzupDpqawkrq4TxdaByNlJxtr-nliSTVMlUdvAhatI1knNB1Iar2QN0zZk9msbHMsCnyc5b1lv64YyfJPLjD07CD7FrTVHw2SZt2kKNdQG7qPOAFFaqHOsDucewfwSy-G5ht6zkq87BXCtP0NqbQ4vOcLoElc-E_tFzbbkg9mviJHJx3fTwb4TBDCLsFIVyU5-881gDFr5cKIPh8vAmfvOQrrkW_HcZzfmRWMitQ8B0YeAQDCq87JI8sZEdGVOYhWHT6zhO46dNFHb0Q7jeBptYiL1gaFWF3GziqE1VWWV9BFdR_ZS2sqXNI9U5HpRFHuhbXleGFIch5pIk2tHlo8YJ0Uy8gNHBhIf3NCL57EOvJj3bmRjIrOz_tKGC_nCxIEkMyucOcEPtrP050vb_YtlLS0LN_UGZ88GnvZ8X08-jq5--K_FsgmwLtY2st5gvV74znwRB0rGbDqzxyj8-tg7GlgfP05vzV3SSbPLXPgub5aq0PR-8s6ggW7VoW-vZf2Nb39tgba7rzdtJvNllSCTKs1g-MeHByPyg9Eh1lHkKrqCDq8inHYhWYz6KER8Jq4tve7P6f4k5amF5_hXceiVvRQvilQLiKaLOK6FkrmokxROSrciyTeofY24QwqIcc99GgmYKSrR5nVbAg-Oi-xZeh6Stp9c5Jn44os3SH7KcNMXXyzFmYhRzTbisqjOqRLs7iwCTK2FFIimuPOkTIWmvcgpOMAVeecO-QsdhFfldZbiJT6sIdVWQGZRtxEMkTfJBaC2qJAgTU53m_ie-9QCEC10EsfEUC2Om3huuVLaYfTkIt8w8U8dQooIdxjDYluYFlAjc0XGiQAC1IekPmJiRLBPtn0tJNyl-Iap3H6rrhziEAREXFSZyZA7TXzPfYzsRUmV-STT4yYOyfet0JZPLvINE38FayVpam6ciq46i3-2eg2RpmJdyXIjAGdwXnIsiuMAVDkKrsj7DWjeHVDULzliCV_7SmnXvboz8vlVhbUSdLrPafxbi7wQ9L6EDshmqbO7nHfffZK6C8OizTWWHpcY6ByDLFlPLvEtCFS3WcY7cixkyXtRjKB9yqlSFrVM8eMR35G2dBD5V8vJN0jnNzIm5HJEOcUsHQJYpSTz2SB_I9_faeF77mMAqK1bmQKPlYnhIyaOfHQmcuE_uci3mRiHowDJ9bqiNSdbI-tzgTawMikIPiy4EUzyYyaOwtCP5vqKvN_SFohZJ-tNc0eWXF15xC6WFftxLL2HnMOq98tY8W-JStFsqC9vf6pFCvXTTvs4eU9aXG5QQAUzlCOq-3Kh_bl7tb6d1Qjc8j5c5erKI6qTQ9pbkHzIOTNxhvT8Aco2m4qoxzto-N3Zl-ANeVOBC9YzDZJwgaudCWSWpAndqDvgpyqVSXaQsl2Tou-nzrSuRdmikimTvTMgryZx9v2ZMOqA_4rr1O0AU3vMAQ9nZWwu7o3oEBt7uFiPYV4pPFaZRpXVqAgqcC3GsgTC72J7wNHLBES9bQTTcd7vckPIgUokTc3yqPQQd3uk0R_I0xjg0WNwGB4gaE9o9d9BxjaMDWrTBYS4RJnrOqDkN0QJ33e52U4FmqYBQfc3NhsJ3O7Bxpi8rZNDdO6RVn8gdTNF5ABbe0J7_w5mxgsAZppYD9AJmdfmmql_RVYmaa-IBnoV55TX5iueWuaqCzjWvsiQ2Yxuh7jdo7DLcL0D1O5xjnwojTvA2p4Uqe7N0ACjSDDCmaIfDNWdA2XJWYY1O3SSIpNqk-Q0MwOzbsrc4q-YMY0TCKB1iOM90tQP5HNxaiaNB0jc01r8voRt3TLgGNHNhknedmnyK8QGEBv3NF1-oc5pLjWiqdq6QfVP0raizkHMkjjLDlG-R2XNmL0doHqPs95DOR_DkFk8eL0inu5jX3PcEuSgz8jdrHjIBY7vFhA0BPqMM_IQa3yU9cYE8ABbfIz1Hk4b-_yguE2vUJYZmz5Oi0u2d4MQq02Z1IXguN2ZWCCveufwDScd7xx474cJ6iuUeGGgn4yX4qr4jXLx-nvxmesLnogymWsK5kK3qumcBGKYg-6QZ-d4iNGmIEUAnCTn0S9f7B5wYauUvydZgQKwEag-4Xn3vR8_HHn01Lln_FxhPFQfP2v48Dw7fZ6dPs9On2enz7PT59np8-z0eXb6PDv9H5id3v9FlBsvYgQfb3_R4q6XTp7kzZLI8p35fG6pwFNu4C5k7M0DTXZIygoXi3nkOAE5URRox1OWduZRKJVa-FKGMpbBQYVuvFriLi1v6Ya3vFqye5nr_-fVkuluL88J49i2bFuF9m6vPZcf9roPQe93DBWpyPdttBp62HHE2Xc7PsVI_JgcMtZe4ASxJeV8kGNExHs5_kgz8NYMp7BRJhPQqLZi3msGWJ3S09G0d9p1iIz5JZ38I2c9vu4nlazGD2Z2ApQo0pThoZuuDK0vbhz1rqXMKcU1fiuyt3Z_EM9qxlYfRmbdfAZYVZyPropuQCbeuLOmmL3xdtykl-9lVg79MIv44pbREPrvIt_VMBxA3In3hoIkKKX98Jt5hOTap_vdX-84OG_Ob2fOzBuipP-KjWCIumTCeEGmmJsGXrMFsrEpuv6dx1OFKtKTW2rIEOUE9LQc25GBGqJr1DaNo_zxzyCOhTl5ynZDR3pO7O8E2TdDh8L8Ez50wKlJPTaCcYgxwy2B_PaXnTcy_cu7P48-fW5Of_vLyckpkk9uwbDU5vTFd2cv_7b68tWPf__q7PuXX7_pbsOaO5d9fnucciqhJAH9eBwD6TPOpYgEI3zLEchp31mnH3cOnjYJwKwEWDDrXs1r9lNQthWQ4ZxMaiErM-MB3duLz0zTZM2WuEeMmwlWdTEOalwCP0Tk4h8mnTLJ9jl5OLadyJO-9N0oiJ0dcu771XFsP-ZJz7GoVq6y_FjZXkdQu7K07z8PRfUnfLQDR6QICCSupkYm6S2h_DJHwCRwdQOJywYdkJKlkBBeswL4XKE-gPBhpwyIte2kgdlmHUSPLdi_383QhmoB93aD9OvZ0M8TT29LgeG7A3F_JtbGtbQr0F3kV8TVYI_Y7FqsYy8KiMdIjbxHRnR9j0H0W-NXJjN6TwoqI3wHImuCd6fUYKruecBglyOxq2m-QMMhF2rPPkaDgD2fOdzl9zuBsHgqWEhbWztmNGr8R1nwpB37kAAoLToiy3aDHXsZNfGH2csney7GEUnMiLB4O7Ch3u8vJLAKcLhlGV_Z5phXTv_lzxtwPUZC-LqqecWP14me0SZCxGdAFqGLy7xugDMZIxzMSntJkbDg4t1jEbRISGrW_EjAxFYUu2gklIqswdCj6cPYzY97RHfM27aWEU60Qt_deXs0Tzji7U_1TK41xQ7fFjGHTxL3wHGrw53O4e5Bh7_uS2NfUVmGnAjohjUIud7IHXlq-FddhEJpRLzu0qvjhrOBFfIOgFXzKw_1wFZ7TEmuwfCR4PCsYBGii3DmalcJR3OTPZrcOQ3pN7QW9gIljOahioYNRwOSkaP_KI8P9b4KcOMC0rwmYf6uTNZxuaMqS3IOMyVMtzoQyi4wRvXDQASbvAuEr0aY3yHDFMGC_90pQLVz2zcDTHyds7B1F_elTJjSOP_-lwMBYKm845o1lWi5GwafjGRtmp2bQT8dt0ajuO_TenqDrgz17UioSN8LpdLxwvN2DcFozrQPlTunR0P9saS1CH1th0S72NsPlHah8od5VspuOnM6Yfp2qmqjCkGxc8UVHmx-4U-uqSPCQ4-wb4fQpGoq02LLcNft7nZd4-A5tEdtFXW1TWQFOnJRpkCehKN6iLkevjodWOO-RUky_t1Cxi9kS1IhHcq253w8hUMXPPDuM28pfkaoQyBCHexOOjWm5Dic7lAKVmHgNCVrOkwQ-Jfypj0uF22liD8VRdrDUg95BZfN8-6RcleyWcEuyoeeUPV9SMlQFvXlF2LVXQd_IzjffcSf_wAb9mtX)
