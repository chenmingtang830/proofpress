[//]: # (ob:1a124f7a)
# E02/E03 — Task 2 frozen run record

[//]: # (ob:ad4491d9)
- **Trace node**: N06, N07
- **Claims**: C01, C02, C03, C04
- **Source manifest**: [`../raw/task2-jcf03-three-model-manifest.json`](../raw/task2-jcf03-three-model-manifest.json)
- **Source SHA-256**: `6ed67099c3322711d521c32fe132020a8a8bd1665916073980445c6c64fa4a75`
- **Task**: `task_b68a970f95ea48019176f0be1f73e61b` / `World425_jcf-03`
- **Grader**: native Archipelago Output LLM, `google/gemini-3.1-pro-preview`, three calls per artifact

[//]: # (ob:034a6503)
| executor | condition | grader scores | majority | mean | tokens | latency_seconds | artifact_sha256 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| GPT-5.6 Sol | baseline | 4, 4, 4 | 4/7 | 4.0000 | 244797 | 469.584109792 | `8ed595305781dd35721dd731600890ebb8401eb2d3aa4393ac976598491bb311` |
| GPT-5.6 Sol | Proofpress | 3, 4, 4 | 4/7 | 3.6667 | 254784 | 803.242010292 | `55653a39c4849b832042f674267c938bc664186557962d978028c4141a1a51f9` |
| GPT-5.6 Luna | baseline | 4, 4, 5 | 4/7 | 4.3333 | 319454 | 555.646359459 | `f7323985aee803996e95db5f219c865056e7528c3c34a5f25d7e3d0673be1457` |
| GPT-5.6 Luna | Proofpress | 4, 4, 4 | 4/7 | 4.0000 | 294696 | 432.998685541 | `dff199e4d2fc9efa7e27036e36556fafe3b430438a89930ae210a5190cfe99d2` |
| Muse Spark 1.1 | baseline | 7, 6, 6 | 6/7 | 6.3333 | 204402 | 818.221969375 | `6ba56927d8c0c5c3ea9e7ebfa8d016a4d8a50c5904c49012b6a025120c68cae8` |
| Muse Spark 1.1 | Proofpress | 5, 6, 6 | 6/7 | 5.6667 | 92169 | 342.70349775 | `b3267b8c2f40d16a53d8ae3b8e9ff276516dbab8b435c7dedc6041b50499b08d` |

[//]: # (ob:e5072652)
Working set: 21 eligible claims, including 6 reused and 15 new task-specific claims, across 10 requirements.

[//]: # (ob:7e882061)
Stress receipt: Proofpress decision `block`; artifact produced `false`; safety passed `true`.

[//]: # (ob:769d678a)
Boundary: generation used local Codex CLI. The grader is native, but this is not official APEX Pass@1.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2FhYjMyYTEyYWY3N2U2Y2QxOTkwNjgyNSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjY2OWU2MTU3IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV84OTEzNjQyM2M3YzM4ZmIyOWJhZjIxZmMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzc3ZjI2YjNlMmQ5YzNmZGVmODU1MDI4OSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWOtu28gVfpWB-qdNRWnuw1H_1A2C7QLZbrAJ2gJJIM3lUGJMk1qSSqK1DfQh-oR9kp6hJEdO7DSO06CXGDZNzgzPfOf2nTM8H7m2LwsX-nkZR7PRej13zgvuGHeFMaBDZNZSnXM1Go98E7fzWC6h63Ftt3Jc6VlwSmiuPC2cy4MNykdrjC0k8zkDGykL3jrjTNQKcgBvjbAcGFOF4FoIlBvLLjSvod2OZufpoZ_3bok7VK5PW43xxkOFA3-GtixK5ysgLbwuu7KpyQrXN-2W-C150jZNsW6h6_CdtQunbglJqWvDbfMKUN1NmwSu-n7dzabTZdmvNn4SmrNpWEF9VtbL3tXLXNDptbdb-HlT4v1800E7D03dQY226NsNXI5HK3DJiFpb0EyZ0W5kDq-HRWhcmOeWCS25CCaIvPDceldwVoSErGn7pNq8KmtA5AePVHNjCq69AB5tEEWEIleK8tzu1Nmjmwe37jYVKswTztC0sRvNnp-P9tufj9DLTdulu900xLlHkz8fPdyrTJ6hzqOXqMkhKpKb-00soZu6NbzNEFbdZ_DaVdPJu60zvymrOHWty3CujFAHyDKc2VR9l2W96075fP84OYuj8Z2izvV9W_pNj86ee9eVXQIFVTF3HTqhh0Hepl81bVLttKyTyG7b9XCGM7U7SzFwXcUxCuhS9Ixm9aaqUOGwwnFIBns5PlhshCGZFs1DC263zzBzAA1zpx0EyZm2hQEuZbQ8SJbrtG_TD7G3dyrZO5VgeIXTdVPW_RCj7bBTAnF42mNYN1UZtkcSjiPkSMgQe58ZPF1T9PMCrQLtui33Mdp5NgPhaZCS27wILDBpXeELGXJrdeEtl9w4kAykltZbIYOTVlnLvMkV9yg_ye5dUuUcbZv-jzjlOqN5xvUzJmaczpT-LaUzSnHt3s64imIEaCXo6PJo9Pw_Khx91YTTwUmXl-Mbswti2V_l1o9rqE--Jw-bCG9HL4eEjZtw6_R7mfnh9M8bpMT_5cwdgH5O4p7vXIPvMIQjC-NwOVJ0D2-TNR5RPn1EBfnH3_6OsrpTwknRNr9ATdoN_g12xxcOKGIc4K1TnYE3OPIr8okS-u06AU_Uj7hHKUgOwFyU0rJovyiwjDx48Kx1AUiNYfLgwYz8ieoxXsyLOs09rFx51qXxh5SN8cLTRaSLfFG_A1xhIb2GlgqJyUjFF0V7QeAthA3mCrkgKBZzJVXxC7JsXYSWYCeA8YbPZ-5V05b9Nt2CSyv6d1h3jHgMFhQ1XCv-RcH-pWlPU-x10M8IZwSqclkmNg-DTcekrEO1SW4mGsVhUxCJqyNhihwZFnndXcNqIM851eyLYn3ap4ROC6FcI9x3zRCJEHa90mJAsPgdOWQx2dHRx7BqG7XJv2wu_aHZ1NG12xnBZIfWDSEwWA93ddWO78jDx99PyLMVHEKj7Ejt-vexIivuvHEbBbyHYl-YT9Ij6VH68ArxsCzrOnnyxSep92JE-mZ4v3M1xvAvKO3kyaO_koG_SCLazU6vk59OJrexwN2x3ZLpn4_mKMvvjuY-2dycQp2mUpdfh-28gyQgjVzVmOGIcQ_djkjh7rrdJ_nhDUm1M-vWmHpFGa7ecaFtMCMZJcNR4h66HZHI3XW7D1mg0EXhqg5wqnMFoFPXqaDjcOpFF5P7KPWObe6u1H1YpXwNY4KtCorGgTTW9KQp0HUlvjmgf4JK_v6uur08os3z0ZvV9poOVzLG5Kr78kmLj0k9AHjyk9Ak9Xhbgt6EZMhPP7l85By6s_TxkeS4MT8-ppx_676-dV_fuq__8-7r07-JHL4J7DHN9OXNZ_9_9fnji3zjUDpaayx3BqxBuE7LmDvmlVDcWKuEo9YXOkditDpYJqVnEf_r4KIxjt6iz00fO8xMqBs-dlx9J_wv-NhxPlq5bpVAKytDYKCVS9k-yDhi_H2I3oeu9xtZE5FVY06VF4eNjhh8v9H96DeteNpsWnz9DEtxAV2flj5fTCbT1r2ZDtbLXoWCiqxfYZHNznCXKjssnrzqmnrx8td3Wf6ba9s-_eNJxpVOuy40YK5TiyEsODeMRcVZELwAJjCgqMtd7iPT6AGmqRE2p1KqoIOWhZPOqMVOcrL2IC_BmXudO2toYRU4mVNmmdEF9cAKIzD6_IJMyQKZtoqSqzliz6jYC_puSPwkatcgkZM2rMo1VG7ZkB83_RrbpcePfxiTxbJplhVMl3BW1mUmJizDAM32jLMYk8EYBLml6sgaueQqxD8sf4cwAwlU84KBtQfvH1XEvfe_xvFDk4sX9QXJsox8cJ195N_ute-ePMvURJOnTYXD3nWQyAtv5Xj4TXdTk64Tij94g5Rp7DCi7UTlktHEUvi8yCEq5CWqTM5iFApZK0YjMBhobil4n0vKwPMonJPCCheswWDJMWW8F4wtboJ0VKguiHgPlJhordMNV9LkaTynYsIlp4zyHSilkLOdsEHiPj7HSJW80EZybYIVuQ9aJ_ZXyliN9Gxy5GWsBxI5wylW2PdAPd7U7iZDqSNDCfxJ4JiVKmFSCt-UWiAzKZswYWhzTA_lABCvtRqsil5hg2sDQqFKg1EIQwSMKBxW0YCIVBuBeSGVuRnTNUvd7j6LftNpRPCJtbnGUiRZQhWLApkVZORFsFBg3eGGCg0CjaMLPEgJLwWVAtPcWkEdcEbRRJaGApMg8j2qH7BSk6dYfU8Jm7DrtjJjguSXdtcDKn2wFXpF0uSvnOUTjnbQVphk04X2TmnLTcwDDSoIcBYM-MLlkWJRTDVR4YSlMkiLJdprR7linAadBwf5baiuWUu9h0sd4sqmPiH5UvIJGkNas0OFBUkbnwdeSIqU55RAHGigHGxRcIxqpqN3PkeLqWCw-AZNJdZuKq31NI-I6qZ2dU8uwfqAG3OLQXggl6MOdk8uX-P838JZOktNbmgB91iVYg67KSa51QesRx3sHuu_9Tx_OzgaU9rlqpDaXYF717LuwX2Nczn7AOXLS_z9JxYtzC4)
