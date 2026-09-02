[//]: # (ob:1d9918f3)
# Proofpress study catalog

[//]: # (ob:d9f7d808)
[//]: # (ob:catalog-purpose)
Research is retained by study so historical evidence remains reconstructable without appearing to be current product code. A frozen receipt may depend on a historical path; archive moves therefore preserve the original commit and digest as the reconstruction authority.

[//]: # (ob:1d46e7d0)
[//]: # (ob:catalog)

[//]: # (ob:a05cb893)
| Study | Status | What it establishes | Start here |
| --- | --- | --- | --- |
| [Harvey LAB-derived long-horizon handoff](long-horizon-eval/) | Frozen, completed | Seven model panels and 126 paired runs; bounded mechanism evidence, not a product SLA. | [`long-horizon-eval/relaybench/README.md`](long-horizon-eval/relaybench/README.md) |
| [Artifact-version handoff](agent-handoff-artifact-provenance/) | Completed release candidate | A stale-artifact mechanism check, not general efficacy. | [`agent-handoff-artifact-provenance/README.md`](agent-handoff-artifact-provenance/README.md) |
| [APEX agent evaluation](apex-agent-eval/) | Closed, historical pilot | Restricted legal working-set development evidence. No further APEX execution is planned. | [`apex-agent-eval/README.md`](apex-agent-eval/README.md) |
| [Harvey LAB contract-negotiation plan](harvey-lab-contract-negotiation-long-horizon/) | Superseded plan | The planning predecessor replaced by `long-horizon-eval`; it has no independent result. | [`harvey-lab-contract-negotiation-long-horizon/README.md`](harvey-lab-contract-negotiation-long-horizon/README.md) |

[//]: # (ob:446c057d)
[//]: # (ob:archive-layout)

[//]: # (ob:49a64f28)
## Archive layout

[//]: # (ob:e29ff2e5)
APEX-only PageIndex, claim-construction, phase-C, private runner, receipt, and test tooling lives under `apex-agent-eval/archive/`. It is excluded from the default product package and CI. It may be reconstructed from its original commit for receipt verification; current `main` does not expose it as a product module.

[//]: # (ob:e94dd1a7)
[//]: # (ob:new-study)
New research starts in one named directory whose entry page states status, scope, evidence tier, and exclusions. Results never overwrite frozen inputs or receipts. Retired work stays discoverable here rather than being left as an ambiguous root-level module.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2IxYzk4NzNlOTFmZjAwNmNhNjg4NTIyYSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImFiNDI1NzFiIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9kZjhkNGE4OWE2MGQwNjU2MmEyZjY5YmEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Q5ZTk4ZWRlOTllYzM1NDkyNTI4MDczNSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq1WG1v28gR_isL5UuMijZJkRSpfHLTFA1wPRwuh7aAz5D3ZShtQ3HZ3aVtnZ3_3pklJdOx42uSKxDE1HJ3dl6eeZ4B72bcel1z6ddazVazrluLRFblcgFVUtdxXEhelGWepnw2nwmj9mulN-A87nVbnubFKs3ixVKUsoJllssyzaEuc7Wo6nohCiFUmpV5XMVimRV1IrO8zCFOqlwAJElaLMiu0k6aa7D72eqOfvi15xu8oeGerprjg4AGF_4BVteaiwaYhWvttGnZFvcbu2diz36yxtSdBefwTMflR74BCurRsjX_Bgy3t2Rw633nVmdnG-23vTiVZncmt9DudLvxvN2Ui_js0WkL_-k1Pq97B3YtTeugxVx428On-WwLnJLIRZbmy0TMhpU1XIdNmFxYq7pUGS8rXsQqLvIi5WldVIKy0BnrKbR1o1tAzw8VadaqgqoEBVUFcpFnVZqnZbxc5EM4o3dryTvXNxhwSn5KY5WbrS7uZuP1dzOssrGOnobXoNYCU34xw8tav5JGwe3sEuM4YIKK7HulwZ39_O78L39_d7pTs_lXQYZ7b7XoPVZqLbjTjmxCU6-5wwx6CPZ6vzWW_PqoWzLp9s7DDt-0fEcFnPo3x-OOCj9btX3ToLdyi5WCIVbRGPkRTySqqpKyXuB2LJKHW4rlAR6MwtozyT1vzAY3jRdzpYJHHaELbnDlFXvhlN935B4VGQEz-zR_cEBV9VKVcfndDlycnV2u2Cv22ojVuD3qetsZBye_tj-DA27llmmHHeE5IkdRJwzm3YOPHbf8kYOJygpYqvj_4eDJC_fyOJeirL6_MvfsQ9hKf7nvHT78c8s9054haWAjabcFN7y2nm3BArv_tb1nURSxBwdDyz3yMMsKGedL9YdmhoqkryFq-N70_qUEZcgNWZ0-Rs75cJwNx18E7Cv2ZPMLOIUUiTqF_BtvO__p3b8i0zbIvdik71vs0DmTDde7iMgReVFS689Zt-UOorf4YPU10jqz_Qs5gCpTKuHLb_RqmvgWbqJQMeyWH-EGu2TsGEewcEy3zLTAiGkUU8jtn7t1OT8w6AwliphnLS3wgbrCmwMPvsjurfHB5kjybCR5hnIjP3ZGtz5olg03EbMdfhGxXZI6NFruJxamijExErToG8XEmdqva4QIWCzTqFlOJCtZi4WoshpUJpHX6nKRV_VCKr4opKrkskhrKEAUoHgqY3yZlyBR3pNFAbVKUrKNTRq0ZyjXqkTmpoVZGqdFFFdRnP4SV6ukWC3KP8XxKiZmGhM-1dRPk9W7P1KpAvYGFUGsbnH_gsu4rnGWEQV1Y7AxEZYRll-rEKNxladFsazTRSrkwfhENEbj38X-ZpyNtOQNw95Q0EoanHa4kQ4cOzQA8gZHIOwrxhHIHKu_Yd4wgQDtLcEQG9co3MtIhk_ZOaut-Q1aMgO682zH90xBB63CfmJ8enXH_fYNGxmQ7XDSc8wTH9cGOZkSBxZf4BLDExvd4hmcxHbI5LylpqSBk_FwaOo2TX_D7KD9_vQZOhlTnScIdlVWRSXzhzoe5e_LqT75sk2-TJSAfJnFsTrYnEjbaPO7NOqZ_-nVxd84ZmvPfjj_c6RwHr7Gmjem3USUh99oIMakmbq-fD1djeCaN2cnaOivoW5zynDXANIYXU88hpVRQNVqoXEh8zif40_kRIV03bo3TJgeKV6xHdDQpd3uCKs5Q4LDsh9Q8uGH81M0fHH11AkLyOACD20fevXqOW-f23gyJuF87OxoJIOHqMOwGI0_owMDROgYxsjR1ZCFt8fo8RZAbcKmbZVWJE33iG6sTgPH05OAA9UO0eJFYKm16hpxLvdDwL9__zTqr9h9DB01l4VzjNLUc2oEtNTBbTSYO9b6bYNEoeaPmlE36Po9Q-7AyVxSBhrY4IsbY1FQN5EDj418DY3pdsMdQ4VP2Y-G1b2lzmXBB7gFGSZ74p-u4S3Sz5iDz3x5FPGX3p08wTcj8beUjxY2xusQabjp8vU27MJ5SkTP7YqmcAq5-NB3CBUg-JIFXPkF6SS4TWSHNKSQypwzFiGBy3Lg0qcAvnpD_Ys8gCDA8WEgPcoUElnf-CEDX-XeND3fdhADfG6kHcmqWlZJFotMLYPSBbKaTLnPEODvj6uj6UJkVZJXhSqTo4xNJtiDRv5vQ-losyyUqABHhzQXB5uTOfUwDn7H6IlItfODdM0D19GXBlQ8nLIQDI0mjSKus-wJmMfcnF2dsveeoA-3sukJVyiJuyBSCmqOUDiy4fgtIlz09n04R3opHsnZwYDGqfRzHawDKgelvQ4fQWSAw5ujPF-Rql8xZcAFcoJbGhIIqQjUB15Gju8beEEsMQ6VLuNlnsfZMfkP4_gzWPnqCVuG7zU3W_IPXcfnjpJDEyK48Kd3c-ak6VBWjnOL11QzymDIN5G-OyUaw0RjyMhYltFHpBucBuAwnei260M6D9kLR3yQNCI8um3v2OEDVBiEggpbHnjOIzNjmQImoB5yiUPHTuhNb1DPcfLzUUNs-aXMXn7Cf_8Fzm2KMg)
