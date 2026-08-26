[//]: # (ob:e7f7759c)
# Architecture

[//]: # (ob:2857a9c7)
## Protocol controller

[//]: # (ob:33b4f909)
The adjacent RelayBench stage controller freezes one S1-S3 sender state per model/task, verifies the declared S3-to-S4 cold boundary, and forks matched ordinary and Proofpress receivers. Task sources, tools, worker caps, and evaluator configuration remain matched within each pair.

[//]: # (ob:7e2812de)
Implementation pointer: [`../../../relaybench/bench/controller/stage-controller.mjs`](../../../relaybench/bench/controller/stage-controller.mjs).

[//]: # (ob:a026653c)
## Governed handoff builder

[//]: # (ob:598eb52d)
The Proofpress branch imports evidence, proposes version-bound conclusions, applies deterministic integrity and current-state checks, obtains transaction-level policy recommendations, records per-conclusion receipts, and compiles a task-relevant working set. The ordinary branch receives a strong portable handoff without ledger current-state metadata.

[//]: # (ob:bebc3271)
Implementation pointers: [`../../../relaybench/bench/real/research-propose-evaluate.py`](../../../relaybench/bench/real/research-propose-evaluate.py) and [`../../../relaybench/bench/real/research-policy-admit.py`](../../../relaybench/bench/real/research-policy-admit.py).

[//]: # (ob:45d55089)
## Paired evaluator

[//]: # (ob:86ad0b4d)
The evaluator scores both final deliverables against the same task rubric. A separate deterministic trust-stress scorer checks whether a fixture-specific unsafe state propagated. Quality and safety remain distinct endpoints.

[//]: # (ob:cfb12a94)
Implementation pointers: [`../../../relaybench/bench/evaluation/public-rubric.mjs`](../../../relaybench/bench/evaluation/public-rubric.mjs) and [`../../../relaybench/bench/evaluation/trust-stress.mjs`](../../../relaybench/bench/evaluation/trust-stress.mjs).

[//]: # (ob:7950c9ba)
## Receipt verifier

[//]: # (ob:2d3ae0a9)
The ARA receipt verifier resolves every admitted and secondary result path relative to the manifest, recomputes SHA-256 digests, and fails closed on missing or mismatched evidence.

[//]: # (ob:707cfdb2)
Implementation: [`../../src/execution/verify_receipts.py`](../../src/execution/verify_receipts.py).

[//]: # (ob:c0d3a025)
## Publication compiler

[//]: # (ob:6cbbcb3b)
The frozen aggregate, claim register, public result, and visualization are derived only from the admitted receipt set. Invalid attempts and excluded panels remain visible but cannot silently enter the published denominator.

[//]: # (ob:8f10c814)
Implementation pointers: [`../../../relaybench/scripts/bench-aggregate-model-ladder.mjs`](../../../relaybench/scripts/bench-aggregate-model-ladder.mjs) and [`../../evidence/FINAL_RESULTS_RECEIPTS.json`](../../evidence/FINAL_RESULTS_RECEIPTS.json).

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2ZlYzNhMjA1MmU2NTQ4MTM5NDJiMzFhOCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjI1MmUwZWEzIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9hNzViMDA5YzA5M2ZmYjgxYzkwY2Y1ZDMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2M2Yjg5MDUwMmYxYjdiNjMwNWMyZjc1NCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW1lv20gS_isNzcsGq4P3oTfvYHY3wGCRibP7EgSavigxpkhNdzOOYvi_b1WTlCjbom0pyWQXBoxYbnZX1_F19Vcl5mZElckzys0iF6P5aLNZZJL71HNCT0ZhkLh-GnjMd2kyGo9YJbYLkS-lNjBXr6gXRnPHSX2WZDA3zGI3yBLPT8JA-sxPHcZEEqRJGgmROpGfhZ5I3MRxeZLGsIEX-24EckWuefVJqu1ofoN_mIWhS9ihoAa3GsMHJgsY-I9UeZZTVkii5Kdc51VJVjC_UlvCtuSNqqpso6TWsGZD-RVdSjTqYFhVHyWYWysUuDJmo-ez2TI3q5pNebWe8ZUs13m5NLRcJr4zO1it5B91Dp8XtZZqwatSyxJ8YVQtb8ejlaToRA9McyT1R83IQn6yk8C5ckHjkIHHODgty1ji8tThWShw7qZSBk1bFHkpQfMuIsWCRyxJndDxMpfFLPKdkHtZHAaNOa12C043ui7AYA_15JUSejR_fzNqt78ZQZQrpfFT81iKBQOXvx_V5VVZXZejD2BDhwcMsKlFLvWsqMrlZFWp_EtVTuQnWsyoojC6zPlMV0VtIAwwxFe5Ac_WSk7XYjR-FrKoMSpnVtKCUZ1r3F4W2YJqcLSRVl5tQAlU_yovUaTeaiPX8KSka4xzZ8YYlmrExmhe1kUBRvEVBFM27mBFxa9gtoyzOA5TDtMhjkZ-RpMvelbAg3YjKoTVYIOgk9cw8hO5M9NsN6gCxhuwM7r9MO78PgJgozILriRtLLFPOrfIhaCOIxMv8tKAB1nkOkEcusIJ0bLKWAS30CAtNAiAlF9tqrw0FunK7oTGdn-hrR8QU0XOtz0JfZz1hFgEnwhBXWVmkYHVUm1U3iJdM3fORRw4oc8x2JEMYj9JfHCkdKjwmRt6mZ_QwE3TMHBS8JuMWODFTpC6KWOuH6Yo21BjEduEYO5CMHFg5DleNHGSiRe9c715GM_D9K-OA8kIFrUOxxg7goa-9Ee3vdGbPwnjFngNBldUr2B-5HPP95kM4xgnWBk9WLaYfBxrt7fjB4-5FLCqO-QQztLMeSXk59EHmzhEzY89vZMg7j39o4bEvHu8qte0nKscjpkSmDf_1zKJNeDUROIlYUxTHh8kEriKTMWrguCQqopCqsF88hN5eMXdWI_3-wJygix10nP2fbeShIqPlEN8yVtZ0O3fZMlXBM4dZpmdDJIpKb9ITapSkkt3cukTvdcOUg49UC2WXuJ6Qp6j2uv1ppBr0ItiLInNU1LNyfvfp9NZ86NQYYYKz5p_O8kDqlFIHBEkpQPV_oHso5SCQHhFlWWE1XkhHg3ZwLKBuIVpIhkwobM1wODtKQ9himLo8jVmcU1glgCnyDGBo76pAMmkTYETVtUDHmKScd-L3bP1eziCejiEcEkWs36au6dfEIowdJI7uKdAywTBnFJTyH-PHbb70wcilkRUOCwQJ--IkdpNJEB2IWCEVWZF4N6kBRGyyMG_ePVqQpc0L7UhBhZpuh7wBM-Y69E0OFmvkyLUSh46_mno8JTRA73eSi7zjUEQAod_9Gw9MH0gQp7wKfCK9OQdMUIXby-grDhcAwNwMX2SeJ6gQIFkuc4N3CIEjgHRcEuWgg55wol5Jph3sl6HEdoHRis-k58lb65MK2m7aJXX08329w9_mQ4hxwGHOV54iJyaAVtsoACV0CZ_wqX18JKBSEWcMc58dtbOGK1MVV9kCadlqeQSiPWY8ILmawjYEipCqSDvWakYwbowYxsxqBkHvJJkrsMTNzhLt2eeKc0Vhqw5W3d1A65ljTpKOO5o0ZYLF0Lo1nqrxGSpgF5bfFu7gMuRI4zjCME4fZ9zGIYs4YbBmUaSDXxaAwEtZobqq3F3eLRNk0KCmzDrXfoTU00uAxBcCMiwNRxPtW1in1XHOMrp1p1DUqSaWSdM9gPT9UeNJ_ektcdozlkYOXrvH2E05wHlVDYD0QU5vKhxQEO4oWRFbAgJ0VjnJSQESAQYm6XKzdbCgdcKC-VJAy9bC8PKihm4fY_xoa8NlKdxIS2xJJq0hk_a-1e2Wf75q4-xqfOSyV3acYRAnQeQU0mUJJg1iKoZVKlTcgG5BTOskXcgYlStERIWgnYL1UKDXK8kCFOEwnafj9Gw7wyQ1h1IARrxk9bCx_LI0MJXx7jcWfi4R3qO0Lfz8HEqhYPhhiaQDQVAob8MgImYyiJoTcs8kxpIBDZG1pvagLTLf15MvDAiTUNct5cMzQtN-DES-LXw8Twi-KSJr6bHGOJ5eeEh-nSEEJ4X-1MJYU2L_EujIHAISAgKIi-AhxRblLm2CNiBpkOXlmZKXpdwjnJAEjxagxtR5DFG-d1SwwGjnOzcMbHsaVKgAkNEY3h5w0k7cnwzul5hd_nnJrDWU20Y3rwlP_khwc7fFm_eChLnw3Z604h0HT5ynZtVVRtiG21QO7TBAlqoQAq2OHGw-c4HRBWku-AgdQPH1Ajip3feB76NaeLTb6n3-8n9NvvNS1fwpSv40hV86Qq-dAVfuoIvXcGXruB36Ao-_Q2Ce9-gh7cPf0P-2NsCX-WVgDj1khgoShhHIvJjL0ozlzJOfVQj832AgRNlkMgdEYgszETgCx4GXhq50on94JhB994J8OdOOHeCB94J2L2d83_9TsB4J5D7PJNJSLPAkkIrsEdOO4HPoJqt4DBinCdpEopsJ7jHPlvBP1L_V11pKOUNX2F5p8AerPvxUY8v2WyJuJiSd9gy0lWtoK4YE1NVBfy6BinYFKKbtuLf3-BgTJYva9UccSXXcGPv9sPCBv6UFGzfwGX8UB5uHUvTOPO5m0gviDvH9rhz69gfqfWMXaMBg2IpWBbJ1OV0h-ke495D8HnUuZUeRJ7HUzhiGdvhsMemezj8UdrLGovVUkOOwA0KSOYFaXJv01-CqAobVd00nBT2CKSa7JXoGEmLwfYGApZo-5wTCB7AEg4cohULZtutQBfsYN86oIU7rtQQTZi6e9esi0FXkhdSLBH5B4atpaGgKx2KfuSkAQQEcoPbxadXTQzC-c9pkHerX1nnPkMBG8OJZYPP3Pxw5fBhcjIai8hx2C479IqfXj5_UjWzu3agmIkiJnzX66T2CpzeIfpRWvB48U30RnK4Bjip4ThlsrsrIJQU2Z-Ykt-wvdeeSZxitl1mxheN85IbAqfNwk0PeD2CyiXknAXUzTr_9Aqtc0D8bZr4j0K3t7rv8ufsenfdEGyBG0ZwgaVhGPu7S21fEe5h-7QSr-MgfuoIx-d-JMSO3Oyrvh5sf5RvBgrIMdhcJutca0zNcJDgY0cTuotowJOh60SO7wQJ8MSdJ_cV5YNQ_DbfFxxVMfEjSEfM8xnbXfi94rKXo55cKe64EfVkGCU0sxW2ldwrHnsB_0G-DiDyM9zZUKkAfkpZ6C774P9ewFuWYbOblmUFMsD60sA2ErOG3ceqqBEYgIoKciQm3uE05UZpEgEL36fxff16Wpr6pl8o7JcfpqzuIMz-_vpfF78u3v5y-e9f313C759_ef3m3eX0o67K3YZPmXwfrx9u4ee_t1glYg)
