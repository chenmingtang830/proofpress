[//]: # (ob:88bec44c)
# Changelog

[//]: # (ob:a0ac1671)
Proofpress follows [Semantic Versioning](https://semver.org/). This file records
user-visible changes; GitHub Releases provide the corresponding tagged source
archives.

[//]: # (ob:45d5f7f4)
## Unreleased

[//]: # (ob:7943f01b)
### Added

[//]: # (ob:4412f40b)
- A local append-only knowledge-event ledger on `refs/proofpress/knowledge`.
- Flat `evidence`, `propose`, `evaluate`, `judge`, `review`, `supersede`,
  `context`, `import-v1`, and `ui` commands.
- A provider-neutral LM policy-judge adapter and a localhost review UI with
  trusted-context and lineage views.
- An illustrative legal cold-handoff fixture based on the workflow shape in
  PR 22; it is not a Harvey result or legal advice.

[//]: # (ob:5662006b)
### Compatibility

[//]: # (ob:f39f974e)
- The 0.4 file-backed `proofpress knowledge ...` group remains available for
  one alpha migration window. `import-v1` performs a one-way, idempotent import.

[//]: # (ob:ca6a4032)
## 0.4.0 — 2026-08-23

[//]: # (ob:f86ccfe9)
### Added

[//]: # (ob:bc0bc211)
- Verified knowledge ledger CLI: ingest bounded OTLP-style telemetry, bind
  evidence to candidate knowledge, apply policy and human review, and project
  governed current context for a fresh agent.
- A minimal telemetry fixture is included in the npm package for the
  end-to-end ledger quickstart.

[//]: # (ob:de2f1030)
### Changed

[//]: # (ob:94b5cc40)
- npm package messaging now describes Proofpress as verified knowledge
  infrastructure for agent-native workflows.

[//]: # (ob:389b1927)
## 0.3.0 — 2026-07-31

[//]: # (ob:b4cefe13)
### Added

[//]: # (ob:3bb7f15f)
- Draft Artifact Provenance Protocol with a format-agnostic evidence envelope,
  explicit verification levels, and adapter/provider registry boundaries.
- `provenance create` and `provenance verify` commands for conservative
  byte-level evidence on any file type.
- Built-in OOXML Word adapter and semantic provider with canonical DOCX
  verification that survives ZIP repackaging while detecting content changes.
- Built-in PDF recognition with version, encryption, linearization, and page
  count hints while conservatively retaining byte-level verification.
- A two-minute multi-format quickstart with portable Markdown and HTML history,
  DOCX semantic evidence, and reproducible CLI screenshots.

[//]: # (ob:cef1396e)
### Changed

[//]: # (ob:acea2835)
- Terminal output now uses semantic colors for native-ledger and provenance
  verification results while preserving plain piped output.
- Numeric deltas keep times such as `12:00` intact in display output without
  changing the capsule wire format used by existing portable artifacts.

[//]: # (ob:8961592f)
### Documentation

[//]: # (ob:a74eed7f)
- Expanded the FAQ to distinguish artifact provenance from workspace memory,
  local vaults, Git, C2PA, knowledge formats, and documentation systems.

[//]: # (ob:20b043a7)
### Compatibility

[//]: # (ob:5ce920e4)
- Existing Markdown and static HTML ledger, capsule, snapshot, and verification
  behavior is unchanged. Generic binary and PDF evidence never claim render,
  semantic, or native provenance; DOCX callers can still request exact `byte`
  verification explicitly.

[//]: # (ob:c8e27e08)
## 0.2.0 — 2026-07-26

[//]: # (ob:2918d404)
### Added

[//]: # (ob:0930bd81)
- Portable capsule V1 with stable event IDs and multi-parent history.
- `merge-plan` and `merge` for parallel Markdown and static HTML copies,
  including workflows that do not use Git.
- Portable, English-language official documentation and agent adapters.

[//]: # (ob:51f72ac8)
### Changed

[//]: # (ob:7cdcc2e1)
- npm and Python CLI versions are aligned at `0.2.0` for this stable
  release.
- The public documentation is action-first and includes explicit trust,
  privacy, and tamper-evidence boundaries.

[//]: # (ob:ec1e29fd)
## 0.1.0 — 2026-07-24

[//]: # (ob:ea2a7d0d)
- First stable npm release.
- Portable Markdown and static HTML revision history.
- Zero-dependency Python engine and npm-based agent setup.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzg5YzhhYjE5ZmY0ZmQ5MjQzZWE1NDQwNiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImRmN2Y5ZjkxIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9kZWUyMDcwNGJmYjdjNGFhYmViYzRjY2YiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhmNmFhMWFmNGRmMWQ3ZTU4OGVmOTU4OSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXemO28aWfhWi82cGI8lVZHEp5ZfH2Qw4iW_GyVzcxOiutcWYIhWS6rauYWAeYp5wnmROFRdRErXa3ddOCMSIWqJqO6fO-b7vFKl3VywvY81EeR3Lq-nVYnEdURExjqnWREvqEk8xnxAUXI2ueCZX1zK-VUUJ1xYz5vrB1HdVoKMw9JEXRb7HIhG6IQsRDb1AEubB24pQL6SY84hKz4tCKbBi2EeCES2gXRkXIrtT-epq-s78UV6X7BZ6SFhpuhrBC64SeOMXlcc6ZjxRTq7u4iLOUmcG12f5yuEr52WeZXqRq6KA7yyYeMNulZnUxtt59ruC6S5z0-CsLBfF9MmT27icLflEZPMnYqbSeZzeliy9jTz0ZOPbufpjGcPr62Wh8muRpYVKYS3KfKnej65miplFlDrUVFN8Vb1zre7sRbC46loq5aIQEa55KAiDeXFBhNBmZFlemqldJ3GqYOSNRZLrSAeMYaaJ1FiGyo8ipakf0Wo69eiuBVsUywQm7JpxiiyXxdX013dXdffvrsDKWV6YV9XHSl5zWPJfr5bpmzS7T69ewxwaf4Cun3339Idvv37x47eTubwaneUprCzzmC9LMNA1Z0VcGH9Rib5mBSxcqWx7y3KW5WY4b-LUNFmsilLN4ZOUzY3dmmGN4KuFsfXVNF0mCQxSzMA4qpoeTzLxBq6OIq4EIcafwC6lemunYC9Mslt4t-6FSWm7XxgPUvfwzhdO97JytTCdG8uBF1y9H627YIgJHIT4_C7WnunoLEmy-8L59b_UnKVlLBzwajM76O31vzUOWag5bIhJlt8-WY9pwXK2MSARKTdUKNoY0M9prhLFCjuE_ZP-wtm48MC0XYojSRDZ6OVp3eKBDr5wmosONI6oh7iM8HmNj52X9W5xard3fsHOPexip6jetl7vPP-qcFgqnfkyKeMxrJ_ZCu14Eggdm-upQs6JS88bjOPEqUiWZmrOfZa_0da-5YyVjsycNCsdiBbOt3E5OWBKzxM-w4hdug4j5-v0FiY0Gyfgj0uIH06mdSxilsAoxHIOM2dmP9r1gI_TA-vgYx26TEQ9jn7U5uvLDlg9FFIIV-FzOxg76WJuZ_ByBdEjdZ69eO7cVfsHLJ0rhyXxbapghqVzgybuBN3AjsvBGurQfBWlhEfhucNxnHoHHbJsQCBmyJCeP9dXM-UsljyBGLFpwhjmKsyrsY7zorQLUvmgKhz1dpEcmCvkphCyiT5_ros8vmNiNbLdlWy-UPkYPpUqFcrh2TKVLI9VcWgtFGR-l2q50Tma4Aly_u9__tdxkRuMUTh2yZHQtecrBzxOMZeFEn1Yz2PnG7vedYwxvtg4wG9pJyZ9z_I3ElKXXanCGE04323b5PWoSc1XtQdfi1yxKjnaT5pMq64ZrJrSLgcwFbKAiRBLJr3AGBHii13qpu8aPTiAY8SbRRbbgFdHPps_m79M-nxtYAf416rTQheKdBqxIOdClFJkurzWYBKVgxPVYKjgeMpJCOAwRFhgEjJXUO2hKBCB1lEAAJFG0pVUCyUilyIlUOhSLxJBBGkYhyIw0dIsrwU1lbmmmABAMO9ctTYNXmF3iiOAqv-B0BQh-Fa94sYHJA0YFgq8Zf3uu4-Eg6z3VThlxoqZifNYCA4hgSlpoIptowNdasc8Cknq1ljg-dRVxJXr1joopW7tQ9DHv08gDEG80bEF3RZW_pYa-Ds2ANxm4AqNfWlS3HdL7vxUbYkCAkZmwoMJvg58EQawyFKbJgHfQ7hximyZC_VbynIxi-_6Q0c9U_AoohkNBLJZw860A3-adTuOapqV8zwGLYaERn7TXgfotO0dBDGNTbVPwgAGAlSoaauDa-q2PgSzNCzHhpmbucpv1XgBif7GXlm9USU6s25JopL-GPTq-xdgiQVE6VFPimimQ0LNEBeubwN1tdRrZFRP54NQT90T95QMdOChgLU9dYDQzsKdD3IgN0q2KMHHJ_sn7BNfeaGnXYHbYXQgUMcXDoKbujUXMU9oHLoud5vWOninndTlSMZJoY3aafbPSmrfF4wj7JPWKztApzXjAQjTzChwIfx61Bfaa1rqoJp2RpfjFTBh6UCCKcoDfsmiKECSh1Qz1i7sGs20E_oAnFL3FEJAdSHfcE-0E-5Al3WwOR2HNHNQGIVgmBAx3ba8hibtUn4AzjB7fFsdsV_7h8qzsVQLlZqlWDWOp9JbSOW2CehozE3orPdOocrlYmfjvH5vJtQjKygZl62oIDKp3l69thKFXIrd97dEiM77fyxVsW4ojyHB5NLoMf9qhcKuylqgqIZ8mjzRS9Xttt50n2CNP-eZjHX8MQj0bku7tOAkRnZCQ6fRnRMa6iXj6xZyNc_uHoKJ95LBY_2ewAN7idexdi-NZbCPRMLi-V4n3LVDTSSeZfNFomAD2EwDYxnXIT1hy1TM1qHFjChXCxbncK2xHrwjYL_A4k_2eegj9tpx6EfsteP9j9hrZ6vseNODddrZJ4_XaWcTPXCnrzvb9N3V_WxlA_4lTbdZerMPQzhPFgAi149CzSNGQ49g4QfM9z2FRTvtLrPvstou2383ZKYhM30Cmel0casVd1qrTMmoHdDUe9-v5ByTtT6KduVLHPqCShxEEQyeQueEuZqHsJ38AIeSCxkR7vku0Zj4oSK-ZExoX8E_aP-06e0oWd4UhVPs9yhZfigJxa47KFmftJIVEeIGfuAGPPQPKll7YvDjaFo-ItiTXsSIJz8bTeu39JI4u60z_ClVKV9pLXzMCSH-g6hSsLMqkxsj7Cad7dmFvg4oIZS6WD-4pmSGdH6-2hnyoAoNqtDHVYU-NYjcewrhMBJ8oCMIvWD92Eg-XsG8Xz85Rcn4IcvnECT_abaL_J0Js2M2GeAc_oKQauOmBROibABHbnbhZVrGQ_TbcYd9bPshut0VUR6u2z6an36Uxs_i9z5zI4SkCBDxPQ4QTmAuABLv4_ct1j_O74cY8-nGmNNVnh6q6Haoovu-nwl-xkx4e3o9TBi7U9J3poNEricRogMTHpjwBzNhaIJILwwjX6s_JRPukofPgstKMAhEERER--1H4rJmmQY2OrDRPjb6U8VGH5iJQhepudMDPrOdf2QyClnZ16EmD3s3ASdCaYW9B7mbwOM81NjX556i_ypnunSe1vYxNxKB5zCzF-FlmYksqUI5MwFizsoxu02zwrjyAXjpIo6Ix7ZOlWfzBewBHidxuTp6ln7r4gMz94WiEA7IZZ2Nna_fwvBNrti7XxMlAfmNmvQ2cooUXs2y06hzx7m2RlEzOrCSyYwdP4KtbUPqZJ__9Df0bZ4tF4WTqnsDVirjwZiZXQUbU_d4TH9zP1X4yAKeNkKr9A5w3AIWIVe3MGtz_1kVtOuQbnKNyOaAx-RWhx2vOLQQ5ttr2_UvRcfmh8duitM2rTopNHkHGUbN2F0Muc6mHwvlUoB_d9WnEEKAwQpnOyGt9vDlJhXWZxM7614sc9hQVeCOy8LhTLy5h0BZjDen13QAA4MNpppMch6FJkAsPe4xSgUgci09oojCfHs5YDVaD2sisoW19Y7v-krn6PyaVByn3EMkHSLpx4mkp8tE2_dB-O_7GfHjKAKKMamRcgMPudj1OPytvVB5rgwAskaaM1dSJUNEXQ_2KA4DFiJga4oBjldsz3w2JQD6Cpi_H02R1yMBeNIFOo70IAF8drd1dKLnR7mtoxMnzyL-UkcoEC7BZH2QvxMWWx50ecjbxROGG7Z08c7e7i4qhplAKEiKCl3UjPtJbYl8B4UYmGPFhG5es4mz1hQ679teVjctXKlF7TUeMGPiq1KN7RDWg7YiwKpyIbOKB8iqVi5jYQh7PWo1lE5Q7_L_44G6aZNTjSOX04Cu729Yx-7WPJfH47Ja7a4Z7Fo04CnuIKuJ822NmnicGiTTLlMKqwYLaiFxXR2wZi7qrTpyoKkal63NcmAxB9lskM0G2WyQzT5_2czgjU9AM5stIRJf-tyRU4jSCVXRc1jHvub6lZddhWP38EBlMOerH5_9vc1LVQz46psatbTx6ogEsds4jMkgjC1FYzuzOkLBB-lt0a8x1NzdKgxVrrSDbcZYD67ZSw14nZylIEDyozryPayRloJISpVGgXb3FeFbjnFcEfi0vOR05aSvLvu-n2c9CrHEAkCPUj5FUcCQqTZrijgwYRFhznwBg9fCjxTHmmuBXc4psAmfCdeVnubR_intcMtgiijQyz5uSb2AYikHbjlwywu5ZcR0RCMVKoAHA7c8gVuaHv9zGSflOE6dH3_8OyCh_zYJoQn8FiY1DtqO3a6NYCk4qwAoblKG6XFj8hbbF8v8zriT84_nL-2dW-bhcZYDzMwQpCqNAA9_27AL-KlJMBvjMpnIOPxtGtumbfd1hBiBIUS-WpT2tQ2GefxPVv1pRr-A4GgGJ2CZDbeBdFL33l2wZAU9lCw2u6-7ct0pPTIRJ5EnwyDgivr0EyTiDUToI-Sn8_EvK7whDI_MC-NTMPI4SZwa08LOMhv0xpjkZsfHmm2XrAZeP_D6gdcPvP4T4fX9TP3zfcoGCxhBnrt1L7O3ZXEPH32-XO9XPrBeetKtxRp7NFAP9uRFJsB3I1sxPPdphCqfQ0ZNnGxZLpYlxMx7EzOLNewCNJrVh-Kr_DmuEvqB-UY0wEBHNpftq24sOTbr7YsPzT0kSsnwws4MgFnAlqvv_v_m6d-cMnNkhWmWkCN6TxPoPJs796cpNR3v7T_P8WxZnbFgAsa8NI9H3jjNYPKaw4rOc5ArRz524mVXsnlexWrbWZWaaxHoj2UM7LSEmTbPOLASoCV1JqEUwARUaiBbAQHffr-RZEzTxWSft-89CwPUpj78Yh1rg0aaHlsQ2JF8et29v4fG_GsvLhs_r93ZzPM-zlV7ZMWEd_iOgZhgfUAmhqe83e6549mH5raZN5uZgmMdWbqOLx86-1MdW2r8tuOX8Gn1vOUKfql51jnDZJx7z1mfhSFHeb0HKoyr5OZArZ22ffAsIQ4rj2GPUE-FCJgKjSLEvUhGe4W4RpA54WkXQ4YYMsTnkSFOV6d3zsqMOuImft-vXT6KXhu4LvFdoETcFwoxTBFVIfVC5lOpwgjjIAxF6CJNzF8c5hQphFyPUuCm2kenTG5DufXwKxxNPXNvUN-NQcolEVFsUG7_UsotCRBYigrKUUvhOomgSw5PjeoPoAkzn5NAYC8UkRg04UET_riasBnUU6e8z8aQo5flflxvB7jo1SusUFHrE9Z1NgvGjaVGR7nBmdpYB_OcqY0JP5JIh5QSEbYxcw1w1o8ZuRi6VHZq3XvHlSAQwkI3ZjOBGcxmDAXEAdxjES8gNla9Whv90FALlZTA5d4otXDKeG6GshQzQ-9usAt57Qb4VWn2PzTS0JB68MaC8NI6jlkjG4RnayXWsJmmqr80xJGvIAjU4nxr-Sb1HTKWJJqHRFCfq1Z67AC2jrFOAGHtuT7hMrCQp_DaZGtc1iknXIq1gCYXC3NbQkV7rCdD7gbr3zFjq5FJbiPnmfvy6cgxZ0GspesVq0PiFm-zVKoYCi9D4WUovAyFl6HwMhRezjlQaVuY7jtWufXpVslm59PNI5b2bOO0flrW-BEel_XgBy73KHhkw7misev1C9zLOTeHGKe__lrJfvCe_fLV69cHpSEdBUJoRR_kbjsuzO9t4LN_Be2XRoBdo5QalUKQmTpGkIGtYfcxXPTjqxcvx0W5MvzpgOImlasx8tCDKYyUcF8Igi779a_6hx0BvBVFxccMWIf4JsAX1Ub1A8ByI1EfeiBRRMG93fCRJOH-2k_HvfaXCwzSrTy9EdzrVif7vOlobeDukAetn-O4xz8ONm_zjo2sma4O7oL1Smhxrox0oOO35TLfarvjGoeXoQad46Zi0rsQHcseHOlyIW0trde9JkcPJG8IZJV96jVszFRx-arh-p7o844m4wDmgTxPBZRoRBBCOPAo1_sqIq3QeXFFZIinQzz9XOLp6eXDMyol61rBo1RKXADR2Py6URiEyPVEFLnm1DqgX0UU8SKstIykwgpgsdI-DgJXBYJxD8sA_qRnVkrMhn6FyNT3pjjsqZTwKPD8wB8eJv7XqpRoqn0ZMuQTSo9USnoTxHlSSCcHnCWFhBSGhLFClXhWVV3WIb9lhpeH8waljIyYJW2VpGHFZWZEKBkbyLBuGBg07PyVUwUKm_Aty3GqiDZqZGLz4-OmuVvzg-eG9ItlbrWXOlRa5s8cDV4xq5hlrdzP4zSes2QXQBnOX1N82Zy56cb1-kfj7BxSoIDZGP7XrMNa9z9TNekktTNVExxJ7gOK0VK2rXUy2IZqclluWlulkp90zooyXwq7WnZ9zbqOa6mxFaUOrEBfAbGT5oYC4lBAHAqIQwFxKCAOBcShgDgUEIcC4lBAHAqIQwFxKCA-xP1hH1Q9DCnxNLLPtvj4sjMh2NUE8XNl56c1emAL4y_jLAVA3sKGcRVva7AIPnSTK10YKgXU99CzQoLARSjgj_LQTO1RTQFjXfrQzFdVZctys7F5SqyqOF_D7tcgajKZ3Di35hm_sPHmLD7t1qqO2Y-WxNDEhzjDksWM1Xb5_peX_QWmjsGPNgsZqplZ16IjRycQtyGmj1oN6BZ4bxVRq_5_fj7ZZ9qj3ZYzIE2QBFeWdZsFd-aw15MKl2EnnhvArvLJPnse7QGwFGSDvMJdibqFATd5ulPkO6-G5u-s_0VlM6mUi0JEOLAMQRjjigsixN6yWat6Hy-bDYHkzx9ITi_CbpdeyPv-YsqjlJKU9lBocL0rkWKIYxJSpSLMgogHLhea8kh7kSbY_hf6IaMsQubHehANXLlnPpvVI_IKeVOXTlHfT9FKHWqwIx6qR3_5JyR14uRZbNWVHCHpai7WnLoTFlvwfnnIM7Z70l56Y2H7NyYX3zQE5mZkY8ciK-xLdceSpZGk4fXvS_OdkWnQxB7zqlgC-YElgrcNM7qp45f5qEqy4zt8U6X1m2W81q9rZbXRl8epWkI2TZwX39fVpLHtbEOVrjPjLAPiUmf1n59blm66tvRMyXGDJyySqCKLY66tu0z7UrfIEjkG55NAl9sSU8VTsqq41Cb3YsYWkP6tovPyJ8d1v3SAG4JfG1LOnO9YfqdWtX5ppJmqAybvYnHuw4I7OegipQuc0EPac4Fcs7b6uE41Gz83e1n6MFT8jsWJ5YrAvs2iZIbqWRwzj29zVsv3sLT3k65POOA3Rhs0P_sAXxnfM-DT4ApwgS0LVFceWrGhajtUbYeq7VC1Haq2Q9V2qNoOVduhajtUbYeq7VC1Haq2Q9V2qNr-S6q2r9__P9TOVcg)
