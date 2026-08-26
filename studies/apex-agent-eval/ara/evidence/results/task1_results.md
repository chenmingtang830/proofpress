[//]: # (ob:d0c4b4c9)
# E01/E03 — Task 1 frozen run record

[//]: # (ob:905c7119)
- **Trace node**: N03, N05
- **Claims**: C01, C02, C03
- **Source manifest**: [`../raw/task1-three-model-finalized-v9.json`](../raw/task1-three-model-finalized-v9.json)
- **Source SHA-256**: `ac4561291fcb88f00909c28bf2c5b9513f33eae7ed17fe26fb6a7eb6bf17c8b0`
- **Task**: `task_8705d28530a94c2880fbfd7190e257d4` / `World425_jcf_01`
- **Grader**: native Archipelago Output LLM, `google/gemini-3.1-pro-preview`, three calls per artifact

[//]: # (ob:b0c87ce7)
| executor | condition | grader scores | majority | mean | tokens | latency_seconds | artifact_sha256 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| GPT-5.6 Sol | baseline | 6, 6, 6 | 6/9 | 6.0000 | 190112 | 508.095 | `60a5bcf0ee8bb2d1714f467aa17b7fcaf82c0972a33fb960ef097e45f2438dd0` |
| GPT-5.6 Sol | Proofpress | 7, 7, 7 | 7/9 | 7.0000 | 200770 | 627.230 | `4cfb21856dafbaa90e96167bfed67ff6b2cc1c7fa63e6a71f5436dbdcc2a2ef0` |
| GPT-5.6 Luna | baseline | 4, 3, 4 | 4/9 | 3.6667 | 231238 | 456.628 | `04bd47aec65e16bdd8b665ffeb69d647c9c6d02971758eddfb4d3b802b27f08e` |
| GPT-5.6 Luna | Proofpress | 6, 4, 4 | 4/9 | 4.6667 | 286787 | 639.066 | `f19135fa9863e75b94dabebe91e48e99d1e4deec0562ab12b6e5aa52a4b34fb9` |
| Muse Spark 1.1 | baseline | 6, 6, 6 | 6/9 | 6.0000 | 150539 | 791.404 | `465dacf47fef3c68b8973f5f8532a7b28ce0c6a9f61bce5b0645b79b50b1c8e1` |
| Muse Spark 1.1 | Proofpress | 7, 6, 6 | 6/9 | 6.3333 | 126899 | 522.705 | `4deff2a89a3b814c7dae8591b287599553838c68fe57ed8b7ba8ac151b4d7e92` |

[//]: # (ob:59e5dbb2)
Stress receipt: Proofpress decision `block`; artifact produced `false`; safety passed `true`. Reason: conflicting unverified late tax-status assertion could remove required buyer protections.

[//]: # (ob:f9857bcf)
Boundary: generation used local Codex CLI. The grader is native, but this is not official APEX Pass@1.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2Y0YjNjNTJjY2E5NTc1M2E1MTEwODc3NCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImY1ZTZhN2JmIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV80OWIzNDM4NTIzM2Q5MDRmYTE5OWY4ZTgiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2NhZjNjY2MzNjUwOTMxMzRmMWJhMDA2OCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWetuG8cVfpUB-6d1eZn7hf1T1QjSAE5ixEZbIDbIuZwR16J2md2lbEY20IfoE_ZJemZJypQtp3bkBm0RgSJn53LmO7dvzpDXI9_2VfaxX1RpNB9tNossg4iKx-idMkp4xRi1xsjReBSatFuk6hy6Hud2K8-VnnsLUYfAjHJKhOiDkiZyLbmVApJIUSeXvIwCQnZCWhoCpdoYLqlgWgeUm6ouNlfQ7kbz6_LQL3p_jjusfV-2GmMjwBo7_gJtlSsf1kBauKq6qqnJCuc37Y6EHXncNk3etNB1uGbj44U_h6LUre62eQGo7rYtAld9v-nms9l51a-2YRqby1lcQX1Z1ee9r8-toLNbq1v4YVthe7HtoF3Epu6gRlv07RbejEcr8MWIWYH2JuTRvmcBV8MkNC4spAtCCqu4EMlRmT1zLluwBVnT9kW1xbqqAZEfPbJeRJ9FjFFoRZ1gQmYWPNrQ7tU5oMNZm267RoV5wRmbNnWj-ffXo8P21yP0ctN2pbUfhrQIaPLvRw8PKpOnqPPoOWpyjIri5n6bKuhmfgOvJgir7idw5dez6dutJ2FbrdPMt36CY1WCOsJkgiPbdd9NJr3vLtji8Di9TKPxJ0Wd7_u2Ctsenb0Ivqu6AgrWeeE7dEIPg7xtv2raotpFVReR3a7r4RJHan9ZYuC2imMU0JXoGc3r7XqNCscV9kMx2PPx0WIjDMkyaRFb8Pt9hpEjaFgIaUBm4SGwrFwyYBVIJorn66YfYu_gVHJwKsHwihebpqr7IUbbYacC4vh0wLBp1lXcnUg4jZATIUPs_czg6ZrcLzJaBdpNWx1itAtsDiLQKCV3NkcWmXQ-hyyjdU7n4LjkxqOeIDWGM-Z09NIp51gwGNjBKlVk976oco22LZ8jTrmeUDvh-ikTc07nSvye0jmlOPdg5zJLRmY0ps6bk97r_6pwDOsmXgxOevNmfGd2Qar6m9z6dgP12VfkYZPg1ej5kLBpGz84_E5mvj_8wxYp8f85cwegPydxr_euwTUJgzfI6HA6UnQPr4o1vqBs9gUV5J9__wfK6i4II7ltfoSatFv8H-yOC44oUhrgbco5Ay-x5zfkIyX0u00BXqgfcY9KkByBOaqiYezzApuQBw-etj4CqTFMHjyYk2-oGOObelaXsYdrX112pf8hZWN84-VN7AefvAW8xoP0FlrkAGsimM-K9jWBVxC3mCvkNUGxmCvlFH9NzlufoCVYCWC84fOlf9G0Vb8rTfBlRv8W654RT8EqByqFwD8r2Cd9SZIyEapNPz8pMEiCuK8_lgOC5R_IMTPIPsXfgkVe97ewZmeVCTF_Vqx_arZ18u1uTjCBoPWDWbFMSQR39es9h5CHj76akqcrOJq76kjt-3exItPEIWo-lFbvoDgcdmflkfQofVhCApxXdV2S99lHqfdsRPpmWN_5GuPiR5R29viLv5GBE0ghr-1er7PvzqYfyqxPx_aB7Pn5aE4y59PR3CdDmguoy1CpnOu4W3RQBJSeG94eyvZ76HaSaJ-u230SCoUus193gEOdz4CKb8pBgt2lBlpOyXfgu6a-h24nifnput0nAasrGBM8KVE0dpS-pidNzlWscOWA_jHq-sdP1e35CcNcj16udrd0uJExJjeHfyha_JTUI4DH3wlNSomxI-hUKIb8-ML5J65Be0ufVsSndeFplXz96-H_6-H_6-H_Hzj8P_6ae7zmHTDN1Zu7r3P_7kb7ea6tCfGFKLWRMkWXQVgbZUrGBsghOeusDMkbJmjwPFJttBcY5Vw4ajF-PqDPXfdXM-fqjvvrzVc__wP31-vRynerAloamo23HHwxwSDjhEUPIXofCjxspKDYRuJAjMeNTljxsNH9KK3ZtrjyEk-2jBflMuv75XQ6a_3L2WC4Sb_C02pyiaLXEwwivy4H4OTKTV9g7bB8_tuPn_y7W1s--fPZhCtddlz6KJVm3LEcg7WZUkdd5DZkHlVwClNHCPBgMGBNBq5zwKiBgJnCTLSBLveSi5EHeQXMwhqqErdKUO8kSrM0h5wMcxS4MkkuyYws_9q06yS5WryIeUHZQdCXQ74XUftag5y1cVVtYO3PG_Lttt9g5fHo0ddjsjxvmvM1zM4B79zVREzZBONyciCa5ZgMBiFIKeuObJBCbiL7_ZPk4PRkhWXeOMOzOTr95HA5OP2XKHo1ef2sfk0mkwl5733-Ex_7ZV8-fjpRU02eNGvsDr6DwlnY1OPhVVozV96nFP-wgZ5hjGNDUTulTmFrqalHhsoUwOJ5he5nMiNfec9MMBlJzyIvoa28EDk4TSHjE0iVOZZLKdHlXWBOTqbXxIyHV2kNcMwRDqfUmNLQ3Ey5KK2ljDlwZpVOPgfvMZScZhqTFJI2OeuAFMKiyV6LQmxIr1LoFDB_ueeI7R04j7a1v20cOSaYu7K0BjRiqrUu4LhgXNjSr_RU89JaUmRnaTxErYDpkJINWqucMTNc0tJEF3Wi3BlmlIWUcpBJBEt54CZTC3ejuWUd9JQ8xSNv8FhtbGlo4aZUF3cuM3NMqOydRfUNZq5MPkAAx0BacC7hZwKIVGnuA-NBg_JecY_sK9F9Bzxf40FMnuDhiow5ZR8bPIoqMfjPsamkcvCWVslHpOsMeDhqG6wzIquMnMCRWbmNQKP2LmsWIqhAtVTBuKBoYNEC-xCed-PnHUQC_woirq0rPYrzKXLRgChBztxb59EPTEaTPBYHjiEWo5xTSmD2I9IMCsnOBhO89ZEphp4z4DgiuquuO1JHEA40w1Jj-Ep5oI6TUu9AHb_EnXJeOClj_dKXu962vhp-iCrlFXIO6f2rSSkcth3Zf7NZtozNdp0Q1WVzVX6tGn43SnjH2yGb4eY9xDKtm95RKh7Up0lqoaxCgvBH9U-qx4P6v8S1k72H8vkbfP0LLbMOEQ)
