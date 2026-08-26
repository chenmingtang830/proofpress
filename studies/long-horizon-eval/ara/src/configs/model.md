[//]: # (ob:b8a26265)
# Model configuration

[//]: # (ob:42263bb3)
Seven complete panels enter the frozen aggregate. Requested/reported model and provider identity are checked per attempt; fallback is disabled.

[//]: # (ob:02ec523d)
| Panel label | Frozen result receipt | Route note |
| --- | --- | --- |
| DeepSeek | `deepseek-v9-s4-2x2-results-2026-08-24.json` | Initial complete anchor panel |
| Claude Opus 4.8 | `opus48-gateway-v9-replication-2026-08-25.json` | Vercel AI Gateway, Anthropic provider |
| GLM 5.2 | `glm52-gateway-v10-replication-2026-08-26.json` | Vercel AI Gateway, Z.ai provider |
| Muse Spark 1.1 | `muse-spark11-gateway-v10-replication-2026-08-26.json` | Vercel AI Gateway, Meta provider |
| Qwen 3.8 27B | `qwen38-27b-gateway-v10-replication-2026-08-26.json` | Vercel AI Gateway, Alibaba provider |
| Inkling | `inkling-gateway-v10-replication-2026-08-26.json` | Vercel AI Gateway, Thinking Machines provider |
| GPT-5.6 Sol | `gpt56-sol-gateway-v10-replication-2026-08-26.json` | Vercel AI Gateway, OpenAI provider |

[//]: # (ob:f3c4fe5b)
Gemini 3.7 Flash performs transaction-level policy judging and blind rubric evaluation under the frozen protocol. Where the same model family is used as worker and evaluator, the dependence must be disclosed rather than treated as independent evaluation.

[//]: # (ob:005e2183)
The exact admitted result paths and SHA-256 digests are authoritative in [`../../evidence/FINAL_RESULTS_RECEIPTS.json`](../../evidence/FINAL_RESULTS_RECEIPTS.json).

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzA3YzEwNDgxMjNlYTkwNDU1YzhhZGU0NiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjdlZjFiMTViIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83ZTQxZGEyYzM1MzFlMTcxNzIxNWY1NGMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzgyZjZhYTRhMmE3YmY5N2U0NzUzZmIwNiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWP9z27YV_1dw7C_tTZRIkCAp7Sc3azLfxa1nu93dMp8CgI8iYopkANCOavt_3wMpyYojp6m127Jd73QyBDy8r5_3Bb71uLaq4NLOVe7NvLadB6kMgzgLaQR8GsSMyYznECfeyBNNvprnagHGIq0pOWXJrMinAdIKwfOiEKFMIMxyxiImUhoWFGgSJHEUckppEEoRpTLiDKSQaR5mQciRb66MbK5Br7zZrfth55YvUELFrRM1woWACjd-Aa0KxUUFRMO1MqqpSYn0jV4RsSKnummKVoMxeKfl8oovwBn10bZu3gGa22nHsLS2NbPJZKFs2YmxbJYTWUK9VPXC8nqRRcHko9sa3ncK1_POgJ7LpjZQoy-s7uB-5JXAnRNTKEIRMuENO3O47onQuTBPIQ5zTmXEohDCNEQfsYLF0mnWaOtMm1eqBtR8E5FqntEi4TzmlKeimCKLlEWFCJLBnLV2c8lb01VoMHV6ykbnxpu9ufXW4m89jHKjjVsNx5DPBbr8jdfVV3VzU3uXaMMGDy7AtssVmEnV1Au_bLT6tal9uObVhGs-MVpO0AGFWpjJssmhGi9zb_S78MSt1Up0FsM4F9wo44RCVcy5Qfda6Pl1FkU7pa9U7VialbGwxJOaL110N8qP8KpxiPBmdVdVaIosMYQwOEFUjbxCapFxmtCEITkqb-GDM_TEqU8GYzrNnT54vpbH87xXpHWIgxvc-Ybsv2BXrVPIxRzx491fjja-9xDcTrW51MAHu_qTjZNgHkypTGQSBlmE2EmDiFOEUer0rBvbo3gND7KGB0Ggyqu2UbXt0a57Sc70zS9n-aXDVaXkaofDLtZ2mPQofiYMTVPYeYFWg261WqPdiHAGMQeaFVE8FZzGRRTGCPokSmIh0U7OCypFQUXOBQ-TLIyDLJ4GOdCYh0Ugpj1vy22P2iESsxBD6zY8GtDEDzKfJhchnbFsxtifgmAWBHhp7XAXv5RRPi2Ed7-ze_sfxXkPvgGHJTcl0meM5cE0SLE4utTveexAc43LLwba_f1ob55Druw2yzGWtZ1J5PjBu-wrR97Jp04fVYhPTt93WJm3x2W35PVMK8w4nbvC-b9RSnq1n1tJYkqTSIjokEpy7mKG5Mu2Aguk5TVUhqCrQRNbAil08ysS8MVCwwILx5icbTw_ecABZjv3HAI2qgUUJKNRfohqd-TUaUP61kvuyMtBFew0XWXxjwTVWtw_azrU3NUocvfP-o74vk_uHnQbCs6uckUk4wL67vhs5V4BdmhFonFKXlaYUaQFXTR6aYjVvDaIGWTgV-jdigzlj7zr8gUmC-Gf81vAgIbZQSG9wLDBB9SA8HypLEZq47OW29IQXufk_K9HPo5OZBilcE8DceB8rBpmmqy4Wj4JvEdarDvFUZ4b0nYC7e7V9Rca04QcnR2R3izMZHII8jS4HoGG9bnaW4TF5FrleBe_aqvsqrepby5Ih9EhmKCwbO2fScGrSuBsRpRBBxjEx1PYfb51zwHvUyB9vhaHoBR9irzxW3cC6ypxtbLrJZGuzj8OEjrfNrKpxuTvJaDb3ZHBkraOT8GXqnoK58-37hCgYwPApq6ugaiavHk7Hk_wAw5BtYTJy-Mfj17Pz344__n1xTn-ffHD8enF-fidaeq3l9_uIx5SZZOyt95N6eadF4huVcGuq07PyDcRI64drVC2bQh_wk46TsimAZEbfB4gVEjfB1x8BksNaRDxteu7bnN4iSCryp0D17J0kZZgxm74-OJZ8DNvhCE-u0Pe7oSzO_jd_tG0_mha_6Wm9eVvm8ezfXy_f3T_rWfMv-WtwtIoE9lUTIGlPBRBnKa5ZJi_URRnNJMRzyiTKcMkolSEwLKkiJI0BhbKAqLsCXs-eatEs4DN4mjPW2X7n4P_37fKaMsXAhmDDJNpWPAN3536tOb7NQ0qkI_3JOLGnDBNp2FU4KOWbczZqWlrcw6qULvfbvMvAO05wBXuvc1xbXDtX099E_v0A_XXTcrfYi8eeiiSH9fKKl49-JXXEtE0uHdg_qLiHfbCn9rOkHicORkNruPMd26-4SsnCT287Z1bMWwr5hfQEvkdHZNXw50ROaptqZsWR5ptKHpxr16fEDamTsyiWjL6ICUM9otJPifmH2OuHkk46QyQcwzbFQnHoRO0xB3fuJ0wPFDeCVj-SN7fbjCwEXqOpt87ae_xd4R8UnGgrKNKCS4eizuuryrXK1CSGpYHirkokY_jeMIlLsE8jtjphc9wSjpvqj5qrWWJb5rqQLE_tVDj7wdZ-_ryOuemWSzSKIinWI42ObfTqtc59zXN4StXTRB2OeGG3DT6ylUcZL_m2-hRfy0H9EI_4BIEqSUCXAmSVeNuYm0te8m8Rgv6IdJxQy3Xt-yOmp-pWCnlIsiB8QK2hX1nmlh772ua8_cTf_eJjZf3-PkXvqtDUA)
