[//]: # (ob:427abbfb)
# Upstream proposal — RSI-Exam trajectory integrity

[//]: # (ob:10537f85)
## Contribution type

[//]: # (ob:c5a3d90c)
Evaluation/pipeline proposal. This is an advisor-style contribution to the
evaluation record, not a new RSI-Exam task and not a competing score.

[//]: # (ob:0fe6b43e)
## Problem

[//]: # (ob:d91a65a5)
RSI-Exam evaluates whether an agent improves an executable method: the agent
starts from a working artifact, iterates on visible data, and submits an
artifact that is rerun on a hidden set. The resulting score is meaningful only
when reviewers can connect it to the exact final artifact and understand the
trajectory that produced it.

[//]: # (ob:f7334657)
## Proposed contribution

[//]: # (ob:a1d97761)
Add an optional, post-rollout trajectory-integrity export contract that is
compatible with TRACE and can be imported into Proofpress. The export binds:

[//]: # (ob:5d64164a)
- one rollout to one session identity;
- every saved method version to its parent and artifact digest;
- visible evaluation receipts to the exact version evaluated;
- retained, discarded, invalid, and interrupted attempts to source events;
- the final artifact to the hidden evaluation receipt;
- the hidden receipt to frozen verifier and calibration digests.

[//]: # (ob:bb27ea16)
The export does not expose hidden targets, does not change the agent or
evaluator, and does not alter benchmark scoring.

[//]: # (ob:428100ce)
## Deliverables from Proofpress

[//]: # (ob:19858c72)
- a profile specification;
- a deterministic offline conformance verifier;
- valid and fault-injected fixtures;
- an import mapping built on the existing TRACE adapter;
- a short audit report after the official export contract is available.

[//]: # (ob:c48a8af9)
## What the verifier can and cannot say

[//]: # (ob:c8d3ba8c)
It can say whether supplied artifacts, receipts, IDs, parentage, and declared
anchors are internally consistent. With an official manifest it can also say
whether declared source events are covered.

[//]: # (ob:1c026da3)
It cannot say that a method is scientifically good, that a hidden score is
semantically correct, that the producer is honest, or that every event was
captured when no trusted manifest exists.

[//]: # (ob:1c72e1ee)
## Requested review

[//]: # (ob:bc10a58c)
Please advise whether RSI-Exam would accept a profile at the export boundary,
which fields are stable enough to expose, and whether the project can provide a
manifest digest and event list for coverage auditing. Proofpress can then
adapt the profile to the released task schema without changing the benchmark
protocol.

[//]: # (ob:e74fc0fc)
## Status

[//]: # (ob:68203d9e)
This is a proposal prepared for internal PR review. Submit it to RSI-Exam only
after that review; it is not an accepted contribution and contains no RSI-Exam
result.

[//]: # (ob:d851c0a9)
External submission remains out of scope for this PR and follows the internal
review gate described in the research plan.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2Y5MjQ3ODJjOTg2MWI3ZTA4MGEyODVmMiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImM2OGFkOTgzIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9hNDI5OTE2MjhlZWNmZDMyODI3ZTQ4OWIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzRmNjgyMjk1NTE3MmZkMDAxZjMwMGQxNiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWltv28gV_iuE9rGyzftF-xRk8xC0xQZOtvuwDoTDmUOLNUWyw6EdrRGgP6K_sL-k5wyHlOQ4jBOn6BYQsPBK1My5fufK3C9A6bIAodelXKwWbbsuMj9MUl9kaezlCbqpC34aFf5iucgbuVvL8ho7TWe7DfhRvIpQpjlkSR6mmcjASyCBOIndKAogDdPUcyW6QepHwqU_XoB-mqV5Xrh-6mZenhFdWXaiuUW1W6zu-Ytea7gmDhVoZrWkDzlW9OBvqMqihLxCR-Ft2ZVN7WzofKN2Tr5z3qimKVqFXUd3WhA3cI2s1NFj1fwdSd1eMcGN1m23uri4LvWmz89Fs70QG6y3ZX2tob5OA_fi6LbCf_QlfV73Haq1aOoOa7KFVj1-XC42CGxEEacgszRYDE_WeGsOkXFxDaGfZV7sp4iikIGf-gmS4XKWrFGaVVtXZY0k-eiRah0Wcer7WRR5iV9I1_WKwHWlFw_qWOnWAtqur0hhn-UUjZLdYvXb_cKyv1-QlxvV8afhZ5TrnEz-26Kvb-rmrl68Jx1GPLCDdS9L7C5UV57hB9jSn5YcsCVyZ8SXyEIt8OKXN2_fXb568df1m8uf3_z89sVfzrdysfwqYIHWqsx7Tf5c59CVHXPHqlhDR3bWaOj1etMolv6mrJlkt-s0bumXGrbs5lGLJV3tGBqLVd1XFekkNuRLHKyRV424odOhnwChkA1PbtT4gTX-pe20Qtg6pF7bdFA5__7nv5zLt6_PXpH-jlbA2GG00TUrBkhp5GsZkXhHT35wnk6nJNbXqtQ7oqB3LevBmCH8LT4u99J6bhQkRRodSfuSPo1mc8zlOaF-cB47P8NTRBDIzBXfzvPVLVQ98NGLtmyRcT1Z5Nx5R5Hr0H9QOyApmBt11ukdhTZzU3vZWlBwJJhbYJyHAR4JRrFPsbP9ggn2p2YUl5kHcQTR19Kf_IuD3tg5dxvUG1RGx2uKG6fcmsgxWuMHFL0JeWc7o26RBEEYR8lDcciMKAdjWYd8WflH78yYAjyZJUnsPY_3CylZ36blg1AtHbquz1RTVU2vD6LhbIoGsg2nQ-IwY5hIxqEXh_A84c6chmA5CdOYrzaDOKUkp5E8P17VZ-RWKlFOB7dEfUt-baSzl66iMnQkXZ5TageTpJ8h3bsNjraQDcGmbrT53iEVPjpNQQjqGnW33P8-pDtHz5gu9Kkuu-I4hH6iCCUVGZCdU6hme1xQ56D1hatzmS1Lo1Qk_neR5MwBTjBFSSHVtSioWRAm_xj_gSNRo6LiTr4qhdMUhUlJxLdo1HbGlyJMIYUiOxLy1w0QXsg_t6YroSgXHOa15P-zHzrYfcFsTyQxl6RTGeSQiu8q2WttLtCpKYF1PTUiJQF3LOsEOOoisGz50-uf6A-BjBuNz4POE64fSwj-C7Lag0SIqMEYnVRcOlFyBDMOqmrnXDeNXI6nNrOyJj56eBwgl9T9UUNKVrDs5737yPEZT-bCcyF64Mmv4fimQqC0YGopTo6bitJd01fkPiGw1QdhMlh_xhKYhIVwi2O53mrQ_ZeSwnRoRmtqbF3qMvArqU-9w77Doh8ZgdKhWDZtlaJS47y5tJY7d972-bakCvxQ1_fLsUVeEAY57a8FNW9D12l-GVtYXLvS9SCMkiyDlAzjxrnA2PW5NhMEDU3bxTu2i6dsjOKmbUoTGjZGTGM6fuO-9D23_1UpdgcUDkeCAyJm2PjGaaFrCr0uyAeoWlXaoaTLvZWXSI-msSL3MC6oaEU-ROAmaZBlvnAjGWCUpiGGbuFBnhV5KrzQExGFiBvwR6ZNTjPDxeCtlZdS581PFj6F_ZmbnvnJOzdeeeHKDf_kuivXpVvW4lzNMyl9HyOCx_7p_f9mHjHoHOaFDXQb7glF6svMz1M0zZChcTBCWOB-x85_5CtDN6dC7UcyGvkeDAMj3yc395ZsGoSARYiRSNKR7EG_b8k-p3-fRGk4v1zVONFyhulzaXoVcGq8O7APdDcm-Q-_0TzeoibZKY83Cs8fSVNWocjNqBRGEY3SYlToYE7Y22l2ArDE4jh0gwgzEYf-SOxgKBhz8zPafVOfVqbumYNXNYWP0rbZAUrW6obVHkG7dEpKaIYHGZA3H0xGgoalMVdnchuzuarHO0OZIwcpVH3N92DsGTvU7D_eonR9tTcwn94i1PSg6Cu6Uu2ualKqtkmUwtKUZ_JwTTAmoax_STnmSKmFED8JwJL1taRbmj8aHBxEgJGP7CN7QWm71DPuzQNIgApR4Mpk9MjBXHTk3qfOOJZ04UcBel4RZSmMpA_GHkv6OSMM67x3x1XNqKZIYA_elXrjvLt88fLV2PI4OTJqGt56cI5oDlrfwWeWbk61sVt93mRegkh5GyisJxAfTExWr2dNPzZN8zUG31DOjCITBIZtoSEwovY4E5gO8hhFI9kxrqS5rlADJSDKG7wuBF5fUVTUdKaUQxCYoq_6li0HWuPWUu6aXgnmy8XW0GJeD7BqJbAB8qmM0z17wj7mexSzv9OTqYEdPFmVuRooDDbozh8ZMMYs7yEXXyFiGY6-Opgfra-eMwuOicZp1JSLGzXYbToMFRmQAFiLzRbUjckJFC0zcSk8GSYYR2Eo831ZnGbLfVx-_YBoOWDqRXnhU4bIJ9MczIwTjJ8x-HHXMHlvgCqDytimAMqPFNQc3txblh90TzIPZGsbqc4W2paTaN6XleZMO4CZudFTG98SCJnKCtRt-B5QQ6MJSoYIFGx9vknylaIkdD5MIVxtb6Gs2IwzcErDGJOceraoiKfqvh9h91759vnTcgoLrwiTKIsDGUyc9iOp5fSceZJQa1GKouL-_oq7PLIemYILlm30abbjbTwZgu6cO79yXuV8PVqSnFwWFIVcsoyOVdewQKa8GYlG-sfpwjAxLydQzsRBTM22iDwXMS0mlO7H3SM7fNusagu3rdLULyCppO1RekrG0_Y0O9SWVcV0N5TTO_qxUcPvQyY3-jl3wAWJkNmz6qbU15QJVW-GzslqBsvdnAGgELnIPd-P933qfobeQ-5pQ7GlmiVxHkEWAabulBf3c_K4VHvG4DtV04YaFVC7JQOiFBuKdKzk4P5uaNqwbvrrDSf8IekOsBzZWaNznjAA476P6qcDV_VkxaEQmGuD9TlwzbxqEMbToskInHMP8qOhR_S5t-MkMvIyati6pdAYQQ4ddEfz4hZMd8Fl3RQBzkR8ckrvVzXR0I1oqhm_0nTr-ZiCn4ls9MDBRmDv17lhf2ziQipymIpwmPcNrYP5f6py3z7am3I8OX5oX8e0Ctoe_5HPlbbi1RYYDzrGIQfSA2o5-ORE9KoeWuZPTPb-I2v6yLs2JIdOb9peNhI_LN6b93am7X34_MGbuYPnNmzsD5eEUeqBnHfk2f-z93amD5l9bbeYl3zxmVd6Mo0o50L2lbukVx8soMwQNXS-isKHPc_R0xScdls06NOMTkKe6Q2a6pFdElWRcvtZwR5IYZdGf0ZsO0ornwoyK0COm3KYq_ZRMajlXFPffD7IM5rifnG32Vlm38zrAZ9z9sWTt2czL78HQxyuxQ5XQoersvs_sO-fvi38ZFv28fFd2JcWg99l-wciKYos90IZYQSBD57g4RplLGQeyLQIQHgi9LxcujKIIykBklikeRZ6mZ_Lz-jz2PIvWvnRI8u_6Z9MnJZ_p-Xfafl3Wv6dln-n5d9p-Xda_p2Wf6fl32n5d1r-nZZ_p-XfH3f5d1DMExn7EGQ4gHSYHva7iXG2esbaoWruuqOVD0s17Xwok3WCFDH9owVHh6AI1G0F9WNry_cf_wMrddmo)
