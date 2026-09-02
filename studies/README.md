[//]: # (ob:1d9918f3)
# Proofpress study catalog

[//]: # (ob:bc80c24e)
This is the directory map for experiments, research packages, and evaluation scaffolding in this repository. A study’s folder name is retained when it is referenced by a frozen receipt, published artifact, or historical branch; this catalog provides the human-readable name, status, and correct entry point instead of renaming evidence paths.

[//]: # (ob:7cefe232)
## Read by status

[//]: # (ob:a05cb893)
| Study | Status | What it establishes | Start here |
| --- | --- | --- | --- |
| [Governed long-horizon handoff](long-horizon-eval/) | Frozen, completed | Bounded descriptive mechanism evidence across seven model panels and 126 paired runs. | [`long-horizon-eval/README.md`](long-horizon-eval/README.md) |
| [Artifact-version handoff](agent-handoff-artifact-provenance/) | Completed, release candidate | A purpose-built stale-artifact mechanism check; not general product efficacy. | [`agent-handoff-artifact-provenance/README.md`](agent-handoff-artifact-provenance/README.md) |
| [APEX agent evaluation](apex-agent-eval/) | Development pilot | A restricted legal working-set pilot with companion reference material; not product or customer validation. | [`apex-agent-eval/README.md`](apex-agent-eval/README.md) |
| [Harvey LAB contract-negotiation](harvey-lab-contract-negotiation-long-horizon/) | Proposed, not run | A future long-horizon contract-negotiation research plan; it reports no result. | [`harvey-lab-contract-negotiation-long-horizon/RESEARCH_PLAN.md`](harvey-lab-contract-negotiation-long-horizon/RESEARCH_PLAN.md) |

[//]: # (ob:82ea7c8f)
## Directory conventions

[//]: # (ob:fb0429d0)
- `README.md`, `STUDY_CARD.md`, or `RESEARCH_PLAN.md` is the entry point. Read it before treating any nested file as a result.
- `ara/` is the Agent-Native Research Artifact: lifecycle, claims, evidence index, receipts, and reconstruction notes.
- `results/` contains frozen per-run or aggregate result material. It is not a public-summary directory.
- `retrieval_adapter/` contains study-specific adapters and private/restricted workflow tooling. It is not a supported Proofpress runtime integration.
- `LONG_HORIZON_EVAL_*.md` at this level are historical planning records for the completed long-horizon work; the canonical completed-study entry point is `long-horizon-eval/`.

[//]: # (ob:0c0bdcdc)
## Repository boundary

[//]: # (ob:589b14ff)
The root-level `document_extraction_*.py` and `phase_c_ablation_contract.py` files may look experiment-specific, but they are importable Python modules used by the matter catalog, qualification flow, and tests. They remain at the repository root for compatibility until a separately reviewed package migration preserves those imports and all receipt-bound paths.

[//]: # (ob:b4531cda)
## Adding or retiring a study

[//]: # (ob:39609940)
New work must begin in a named study directory with one concise entry point stating its status, scope, evidence tier, and exclusions. A completed study may add a public summary, but must not overwrite frozen result files. Retired or superseded work should remain discoverable here with its status rather than being silently deleted.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2IxYzk4NzNlOTFmZjAwNmNhNjg4NTIyYSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjE1OGExODVlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85ZGQyYTZlYzZlNGQ5ZTEwN2UxMjI3Y2IiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2MzZmRhOGM1MzkxZjNjMjllOGEzYTMxOSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNqtWOty2zYWfhWM-me7K9q8iBSp_HKTbNOZ1Mk42e4lzdAgcChhTZEsANpRk8zsa-zr7ZPsOSApUYnr1HE7nkYigYNz-c73Hej9jGurSi5sruRsNWvbvAhEli4jyIKy9P1E8CRN4zDks_msaOQul2oNxuJas-FhnKxSEaeRKLgEkIsiFksRc16kURxxgCyRi9KPl3EEkJYijARfBkmR-nRGCkmxlGhXKiOaa9C72eo9fbG55Ws8oeKWjprjhwIqfPATaFUqXlTANFwro5qabXB9o3es2LGXumnKVoMxuKfl4oqvgYI6eqybfwOG22kyuLG2NavT07Wym644Ec32VGyg3qp6bXm9TiP_9Gi3hl86hZ_zzoDORVMbqDEXVnfwcT7bAKckBnHKgzSGWf8kh2u3CJMLeSZlyBMQCSxkBoG_hCAMl6IgzxptKbS8UjWg52NFqlxEpeSY5whrEokwg5RHPAqyPpzBu1zw1nQVBhySn6LR0sxWb97PhuPfz7DKjTb0qX8NMi8w5W9mXX1VNzf17C3GMOKBCmw7qcCcXjw9e_Lj05Mtleo-cOHWalV0FquUF9woQzahKnNuMHsWnL3ObhpNPl2pmkyanbGwxTc131LxRt_muNVQwWeruqsq9FRssELQx1hUjbii1MssC9IywuVYHAvvKI4DLBiFtGOCW141a1w0HMqldN60hCq4wSffsDt22V1LrlFxESizj_ODA4VAbIcLeLADrxHXDP_sBphEyAkH8i1vWdloBu9abIUtFtbMsRUMcC02bIC8ObjYcs2P_FsKKCGMwiP_LjAQ6h9jue3MnWn5hn22-I5scD8WRZpFX3naB_bKpYv-pbX44e8bbpmyDHkBe0WZDZj-tbZsAxrYh5_rD8zzPHbwzHXVkV9pCHwp0vLIryf7LOMz6hkE25eS8Vt77shJWfiLMJP-w8722OW-LS_n7PLV6789-Wf--OziSf8AMYILXj09u3j8LH_5_OycHg94OviHCbRHzvnCL6SQ4pOCtY1RPck2XS05EvWXMHLbjjuSEqdZESzK8iHnvsZOwUazXoWMV7FL2YiOOiRHaxopi2jozyft7pLxWrLLdsMN5CJHcHB7R8cUizgKhORHrp1JCoGyrMEqTZ9539tfyMydG-9IUJQlfpYt_D_Ai3O4YTeNvmLbzlhWwFrVDP84I8aVA0MdKOcGpZE1NRAyxad5ejsf5WWG-k30nAsNvOd292YUijulr26sszkoIBsUkKEWi6u2UbV1gq7dSUT_4zdi_7cknZUSu4mFqZxOjDih_kqlNU1p8xJzDLrVahB0UwSrmAufR6Jcxn4ikyQMkywI0zSTQYLSWCxDiQNSGmAdFn4SCbEIebwohJDLYBlDsiTbSG9OmPtqrQIf9Y2ezEI_TDw_8_zwtZ-uomQVLP_i-yufgDBkfDpxfJw8ff9HarnDYa-12DcbQiSGXZaxjIokxQXOxkR-B4jeV0cH47AMY7_gUSwckpzxibQOxh-ikXPHAnDNq44TNTAjeFk2lesobAdLtvWegU7YWe_-__7zX8NoHWjXMMwtsxyRJNkNzo6kTu5ZiXJUo_-kdZyVuvkVX6KToFo7Z23Xy5dkYxkcaffTrBK8YoXmtdg86j0ZksZw3rtWEvqYN92W1x72m3RdQ-7MB1ntw8Mpj7LCMAeYGNcDGBsOWKjATYnO4BaKF8gm-orZsRtzcgsbDnVJllmYLtIyk-G-LpORYiz675sSBpsLEeJ_0s8WoRhtTgaHweaDZoFb_k-v3nxPtw4qXNXUaw8HUfUr3SgwdU1Zvv3T9KlHUDn9Frf_1VVyjsndthUg1eGz70if8BNWRmisr7oGtgWaUJXZHtLLhW6oD4gZ2baRKFMtr6EyrlpBmOBXxLFkuqvNCdp9c_m5Dwfdv83D_dtvhxjPBnh5AzEcwsM2qK03fPVGGHoEMQQG-uvCfTyGSU1UAYomgrGWSiLL4-szRLLGLgGv6FRlqeAV7I1NkuBo-BFDqmd4LmhEOJ4kO4JnWSLixa6P-MtuTTNwj9X7jLx8-g_m9k36Hy218M7rze1r_YRGiaYlEmGtqtB3ihjJBG82gkpfwRoDITlFVHsGxmVONQkhGHxTH9gA2ckiK_Gqz8SYAex8gWrcbJFV8GxKLm4b8vGJX0fR_9a7MdZnXF_Djj0_-470281BXg3rxqoh6o1b4OEN27ttgTdFmEsJ8jmVG-FAASBQXUrKznbYcUd9dJu9CRFXvH5E7Uskq61Bc_Syq2wf9r0c-2zUvWdgn-7HQG-7PwyMJYoMEt_nhR-HI2NNrhQHFrzH9WAwHceBXy4CAXEQj6YnN4bB9EOm_6kYnPQ8rWgMRMkEZml4c3NkvWM1whwhXirUFo4UNZbn5xrPR2E43Zs8cwg85473LsYKj8yzwnmuBLETFcqTqLjaojztORHHVHg3H4VxEC76gQJ1SndubCekgenP7X0weDZVFWXXjNKKau8RHDF4vl5rbEwLg8v7rjthPzh1JujyXoOFZ7rtFu8WhxFiPAmbnLoqR31tcf_0TDcLeKYFoZC72LCi53EcD6_xvNMJTRBBlFVzw2yDo2q9PvbDdC21AK6bDEsYilU0X-C0v9Y9Hzi_nr84_z5_9uLih3-9OM-f_nT2HG81VF4UQzcq9NcfHI-nwwR1W02FHX4ZchMSle6gYke9Sw4_6hfwuqmdjf1Srx_kjqYKw26RqsuTW-6aA9KDxE8gkVEknMw7pE-un9NR4ndeJgfDZRDi4FjguB3tu3Nyv9zPjl9_W3TXnIFT3BJqEYMg22ESm6vJ5LlHyJwVHdUHuZgqo7b7u87Lnd00bhroyEhn-omRUo-oRVCNs9-c_dKhNJBUuqYgPPXdQr-S4rjwmqxr2HK6zbnDJgOsC9ZV3amSVYWqlN0xQllFGASa9SxUO9bfFNGNYVZmWzUAkBE0AXmV2h5FYIijhz2vqrGLPVeoL06TAIt4KXgKaZjsp_zDdfsAgfvemkcy5YGMo0WRZdF-Wp1cpAf7D7kPK3PEp27cdRcIa_aDuBFNCxPCswr0cPt4J6qOZjJD14tDJ_ZHEpzwPrjnKTbwVA8l5yzRB42wN1oh1-2vGI7yHCaJ4K2bKDF3SDNIUSAHPmJm03SVHBEz_gjvQOnGZxfpIRKGGMDnWHleY5ooTINn1BYhg5Msef5Zrd9-xL__A2_sVRg)
