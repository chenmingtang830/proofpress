[//]: # (ob:2a96ef32)
# Study configuration

[//]: # (ob:ec1521ae)
This is an evaluation rather than a training run. The filename is retained for ARA Seal compatibility; it records the frozen execution controls.

[//]: # (ob:8ade7156)
| Parameter | Frozen value |
| --- | --- |
| Task families | Credit lending, master services agreement, software license agreement |
| Design | Clean/stress 2×2 × ordinary/Proofpress |
| Receiver repeats | 3 per cell |
| Sender reuse | One S1-S3 state per model/task |
| Cold boundary | Immediately before S4 |
| S1-S3 output cap | 32,000 tokens |
| S4 output cap | 64,000 tokens |
| Trace/graph selection cap | 8,000 tokens |
| Working-set compiler cap | 24,000 tokens |
| Completeness supplement cap | 12,000 tokens |
| Transaction-level batch judge cap | 64,000 tokens |
| Pair invalidation | Cap hit, invalid/truncated JSON, provider timeout/socket failure, identity mismatch, or condition cap mismatch |

[//]: # (ob:7ba64149)
Canonical machine-readable sources:

[//]: # (ob:4f9a1c53)
- [`../../../relaybench/bench/experiments/treatment-effect-protocol-v9.json`](../../../relaybench/bench/experiments/treatment-effect-protocol-v9.json)
- [`../../../relaybench/bench/experiments/cross-model-replication-v1.json`](../../../relaybench/bench/experiments/cross-model-replication-v1.json)
- [`../../../relaybench/bench/experiments/portability-amendment-v10.json`](../../../relaybench/bench/experiments/portability-amendment-v10.json)

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2Q2NTE3NDg1NjZiMDlhNmQ2MWQ0MDQxOSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImZmNWJmZDkyIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8zMDA4YzAwNjkyZTJkMzhjNmYzYjMzYmIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzZhMjA3ODEwN2U1MTIzYmIzZjRjNTUzMiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWNtuIzcS_RWi87JBJKvv6tY-DWaxQPZhMxgbuw8TQ-GlqOa4xe6QbHkU29-RD8qPbZHdsjVje-KxN0F2EUAQWs1isS6nThV1FVHjlKTcrZWIVlHfr0VZJMu8KsqSxTUtRZmIPM6TOppFrBP7tVAbsA5lbUPTolwVvEhFmqSSLpdlvCygKildZoJLUUOag2R5ncqqrHIoBE2qQtKMQ8nrSkJR1YB6hbK824HZR6sr_8OtHd3gCS11_qgZPjBo8cW_wCipKGuBGNgpqzpNGpTvzJ6wPXljuk72BqzFPT3lF3QD3qmPXpvuPaC7g_EKG-d6u1osNso1Azvh3XbBG9BbpTeO6k2VxYuPdhv4cVD4vB4smDXvtAWNsXBmgJtZ1AD1QZSyYOh8Go1v1rALQhhcWGdxXPE4LusUUpFVvJQZyzLGvGWdcd61das0oOWHjLTrkqbxskriJRRJisKZzHlRZOnozmTdmtPeDi06nHo7eWeEjVbvrqLp-KsIs9wZ65_GZRBrhiF_Fw36QneXOjpHHw548Al2g1BgF22nN_OmM-qnTs9hR9sFNXRhDV9gAKTa2IUzVGmM2clWRLMvghR1zig2OMzkmlGrrD8XWrmmFiPsIOgbHJ7u7b5Q2qu0e-tgiyuabn2CD_bPcKv1oIhWemhb9IY3mEUY48Dajl-gdErrEmSIHtrv4IP39RR93ZPRn8FQbw-uT-dRIYIhvQcdXOKbr8jDG9y-9wb5tGM4opvz2SH8EeLbm7bmBujoV1g5BAnWdRzzHARgLRUsjuu04CzmlHs_OxeAPCGETAghiFV-0XdKuwB4E07yrh9-ec_PPbRaxfdHGo7hdqQkAPmZSLSddGuJXoPpjZoAb1myksuyimmWxFWZ1HUssriu0D9aLlmdLKGuIIEUCvSdo0yKTstMxjGTqWSMgS8N66gLwB0zsUowtf5FlMZpOY-reVqeJemqqFZ59k0cr-IYN00BRymkGpbnZRLdHL29-r2hHvA3QrGhtkH5uOSQZ7FYirhCgaDjCJ0TNJ-MtZub2YPVDkK521rHdGq34p2AD9F54A8x8MdWP-GJe6s_DsjPt8vNsKV6ZRQWnRGePv9nCCVY_lw-QdgWaULhJXxyhl2M4Idq4uMxhA0E9zVgiMNDCSWHmBAz6BNy1gCRqgVN76CANU8jD4KDaRUVsEyK8iWmXZM3qHYLDi25Jn833U-gibcRyPX3-prM53MyffufZ9ReEEm3qsVMk-s740beObZuyWiZJ3n9EuteU91pxWlLtpQ3SFdzpFcRSNJ2g-FgV5-JTy5rmvAie4kFc_Luh5OTxfgx0NI9A82bxfgNH3qcWbaeihHUyPz-cQ5S4gwy7-9Ma3GKCe2Ct1RtHwXYJ1ZMfeGVEJb0A0OSD-bONwYTT169fUWCW1i05CUI24LfacDhMggiOxN0nwKGHUemHnUxzLfb_5UoR6bZA5Xi_hEu8AF4KMlgj3kMo8_37nMgfQxzzz_tKaB7BGbPP_QlODOd63jXznf1yXvb6R_O__IyTSNSDxVzFV02frh4jVBAvBwn_s1b8lVWEBtKCoeCDlH2sJ_pSUkOPE8ucRzvBkcC3QZAAo62zhJEntK-w_mX4-Qf8oDrQA1vPIQx_Ce-0z958PrMTD7m53iiOh4njqesqz97w5-94TfuDU-_MHw6MOc3D8_Dv3Y3-O9cAGrBK17JhGdQZ3lV58skhjItBS9w3GVVUuesTFgiRQoZypUSEpalvK6XOA2Xj_hz7wKQreJilZUPXABub-T_1xeA2a1eyDJeZRVDYMBB7xEVTXr_SCNB1yJp3y_GyZ9qKSHjOS-TZXLw54i_Jn9exkbktfEXJYLe-XDOkDSs14S3hp1CriB0YwB8ic6Ih_olUj9exDloC3dro-q_gVUb7XW2QPXCOv8HDUl_-Tklv_yMTQwPoGa_uPu_atz2FjgoxCfGq0c68EZlBDmCcGjbUeQUrQsCA556Tb7TQE6T-WlGfIVAEN7i_axdOO9d2PK6awVh3aAFnol7vt1u0VGUbveEAWYOVeST9qAKO2_vmy_tvQHpLI5j4roLdHSSyj8WKfN7Ime-DS-wu_cNBrBFQguZDuLVPel_dwYpdDO34AJ4EGFmEk7v6_ZjRotJ1j5udkBWGiM_bkjSh4zRlgYT5i1yaEsYdTgrvB-E_w_lMR_eUBWmDdoqMZYGno3CjUIETO-RDQbN_VhB_nH63T9nBAeknfIZckjsGKWFxZpHtyRV7WAANwo_vbg92Sq79WbM_FCDNYDYO8TosPRwi5xqgjEOS5BIw1V2qImjrjnVxPN64HSElKlgkkrk2PxwxFFbnI74Iw2mt5q-_l4_3S5uOmvnoW4wPP3tdLpLvsyqX9HzRTaNLThQ6Bw5TYvg7S6Jv8ykz6v5-t6QcYOf_wB9shEl)
