[//]: # (ob:1d9918f3)
# Proofpress study catalog

[//]: # (ob:bc80c24e)
This is the directory map for experiments, research packages, and evaluation scaffolding in this repository. Start here when a folder name alone does not make clear whether work is frozen, developmental, or merely proposed. A study’s folder name is retained when it is referenced by a frozen receipt, published artifact, or historical branch; this catalog provides the human-readable name, status, and correct entry point instead of renaming evidence paths.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2IxYzk4NzNlOTFmZjAwNmNhNjg4NTIyYSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6Ijg0MGIxOGZjIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV80ODY1MjA4ZTU3NzFhMzFlYTRjYjkyY2QiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2MzZmRhOGM1MzkxZjNjMjllOGEzYTMxOSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWetu20YWfpWB-me7K9q8iDfll9tk2wJpGqTZ7iU15OFwKHFNkSxnaFt1A-xr7Ovtk-x3hqRExYpdx0WxWKgIGpscnjnX7zvn5HbCG51nXOhFnk7mk7peJI6Io9CTsZNlth0IHkSR77p8Mp0kVbpZpPlSKo2zasVdP5j7ri0c4cz8SIgkdm3PF04SuHYQOYH0_CiNPe6m6cwJbM_2oyC2fZt7mSt4GoZB4EFumitRXclmM5nf0i96ofkSNxRc01VT_JDIAg9-kE2e5TwpJGvkVa7yqmQrnK-aDUs27HVTVVndSKXwTc3FJV9KMmrvcVP9U8LctiGBK61rNT89XeZ61SYnolqfipUs13m51LxcRp59uvd1I39qc_y8aJVsFqIqlSzhC9208v10spKcnBjN7MSJMjHpnizklTkE58rFLArgsEj6Yehwz5F8Rk4TKWlWNZpMWxR5KaH5EJFiIbws5ZHwPcTEE24sI-7h47gzp9duIXit2gIGu6SnqJpUTebvbif99bcTRLlqFP3UvZbpIoHL303a8rKsrsvJOWwY8oECrNs0l-r0zYuz59--OFmTko9JF651kyetRpQWCVe5IpmyyBZcwXtaGnmtXlUN6XSZlyRSbZSWa7wp-ZqCN-g2xaeKAj6Zl21RQFOxQoRkZ2NSVOISp500juF6SioER8sbsmOXFoxM2jDBNS-qJQ71l_I0NdrUlFXyGk8-Y_d8pTc1qUbBRaJM3k93CiQisoU7k09W4C3ymuGPXkmWIuWESfI1r1lWNUze1CiFNQKrpigFJXkjVqxPebVTseYN39MvFDKTrufu6fcGhlD9KM11q-51y2fszuF7vMFtXyRR7H3ibb-w74276G86ix_-uuKa5ZoBF1AruVpJ1b1uNFvJRrJffix_YZZlsZ1mpqr29IpcyUMRZXt6Pd96Gc-oZpBsDznjY9_c45MssWdunNpPu9tiF9uyvJiyi-_f_uX53xdfnr153j1AjuDA9y_O3nz59eL1y7NX9LjPp51-cKDeU84WdpKKVHwQsLpSeQeyVVumHED9UI4c-uIep_hRnDizLHvKvW9RKSg0bRVAvIJdpJVoqUIWkNYAsgiG_nhSby4YL1N2Ua-4kguxQHJwfU_FJDPfc0TK91Q7S8kE8nIjdd7Qz7yr7Qc8c--H9zjIiwM7jmf2b6DFK3nNrqvmkq1bpVkil3nJ8IczQty0R6gd5FyDGllVSspM8aGfzqcDvUzA3wTPC9FI3mG7eTMQhVzEaeryQIpAztJYOnYoHdcNRUJYX2kjs2dA1jMgAxeLy7rKS20IvTE3EfwPvxH6nxN1FrnYjCSM6XQkxBD1JzKtqjK9yOBj2dRN3hO6Spy5zwUaGpGFvh2kQeC6Qey4URSnTgBqTEI39SMvchCHmR14Qsxc7s8SIdLQCX0ZhCQb8GaIuYvW3LHBb_Rk4tpuYNmxZbtv7WjuBXMn_JNtz21KhN7jRHt-xJ3IJ5DbPb39Lbnc5GHHtaibFWUkzM4yP_WSIMIBI2NEv32KPpZHe-EydH074eglTSYZ4SNq7YU_hSOnBgXkFS9aTtDAlOBZVhWmolAOmmQ3WwQ6YWed-v_5178Vo3OyMQXDzDHNkUkpu0bvSOxknmWgoxL6E9dxljXVz3gJJWVe6ymr246-UjaEwYB2183mghcsaXgpVs86TXqnMfR7V3kqO5tX7ZqXFuotNVVD6kx7Wu3MQ5dHXmHwARxjagC2ocECA1cZlMEnZK8kmdAV3tErdXIADfu4BGHsRrMoi1N3G5dRSzEE_dd1Cb3MmXDxX2rHM1cMMkeNQy_zSb3Agf_Tq3df0dRBgSuqcmmhEc1_pokCrquy7PwP46cWpcrp5_j8zyaSUzh3XRcSUIdnXxA_4SdERjSIb34l2VpSh5qr9c69XDQV1QEhI1tXKWiq5qUslImW4wb4FXmcsqYt1Qnkvru4q8OO9w9puH37eW_jWZ9eVg8MO_NQBqW2-l-tIQ0tSjEkBvQ15n45mElFVEiQJpKxTPMUKI_XZ8jkBlUiraTNC00BL-RW2MgJBoafMUA9w72yQYbjprSl9MwyZLzYdBY_rNbYA484vfXI6xd_Y-a7Uf1DUi1vrE7cNtbPqZWoagIRVucFdCeLASaYbASFvpBLGEJ0iqy2lByOGdakDIHxVblDA6CTBirxovPE4AFUvgAbV2ugCu4m5-Kz3h8f6LVn_cfeDbZ-zZsruWEvz74g_jZ9kFXKZaXz3uqVOWBhwrYOHbDGGWZcAjyncCMdyAAkqnFJ1uoWFbdXR4fkjYC44OUzKl8C2UYriKOXbaE7sx-l2J1W95GGffg9DD00P_SIhZFdBrbNE9t3B8QajRQ7FHzEeNCL9n3HzmaOkL7jD6JHE0Mv-ind_5gMTjqczqkNBGVKpql5M31kuWEl0hwpnuXgFg6IGsLzY4n7QQynW5FnJgNfcYN7b4YID8gzRz-XSbERBehJFDxfg562mIg2Vd5MB2LsiYsWFOCppjVtO2WaVN29nQ4Kd1NUQbtqoFawvUXpCOP5ctmgMLXsVd5W3Qn7xrAzpS7vOFhYql2vMVvsWojhJhQ5VdUC_Frj-_GdphewVC1FDuxi_YkOx9EeXuG-0xFMEEBkRXXNdIVWtVzu66HamkoA50bNEkzROfUX6PaXTYcHRq-X3736avH1d2---cd3rxYvfjh7iamGwgsyNK1CN_6gPR43E1RtJQW23wyZDolCt2OxvdolhZ91B3hZlUbG9qjVNXJ7XYViB6jq4uTArNlnuhPYgQxSzxOG5k2mj8bPcSvxK4fJXnDmuGgcE7Tb3rY6R_Pltnf89GnRjDk9ppgjVCIKSbaBE6vLUee5zZApS1qKD7CYIpOvt7PO641eVaYbaElIq7qOkVyPrEVSDb3flP3UghqIKk1RUD511UJbUrQLb0l6I9ecpjlz2aiBNcaaqBtW0nmSF7neMMqygnJQUq-nZbFh3aQINfpema3zPgEZpaYErlLZgwR6O7q050UxVLFlAvVgNynlzA8Fj2TkBtsufzdu71LgsVPzAKbcSX1vlsSxt-1WR4N0L_8p83Cu9vDUtLtmgNBq24grUdVyBHg6l00_fdyIoqWeTNF4savE7kpKJ8yDW5xiPU51qWSUJfigFva6yYF12xHDQJ7JSQJ4bTpK-A4wA4iSaY9HTK2qtkiHjBmW8CYpTftsLN1ZwpADeI7I8xJuIjMV7ig1UgadLGl-J9bn7ykcBzbQMoXGw_5ZoBO-mZybbTbaobvPP9hXj57_1BqS6l8A60D7qUW7-99jmy3Lq7ypSoMbVKvqI0ttM6h96k77E1fKABRghdHnw5VNx8Efu-Tu9_165sUNWITIb0VEZqihG0qhRlUQKPB1ki_bqlV3qoYsVyajqpZaPsrYQ5OnUW-w8nZyvaKtzrf8Uu5dCIBFQeSUeebmhy9eURPTo1dPg3eB6v0jtln3_ENO567xmmq8ohmvrm5_p4D_-k3cdhO1lTZ33h9eNT20d_ttlms2D8AIMrRjfGeHdhj5voj8OIjFLPJD23bDOIxckYiZn4ksiNFQBGjGvSTyRBh93KRD67Vw7toH1mvbf9D7v1mvZZkbBWnKQ2n_j6zXRmsbs0Xje0s2WATGTSvZtcxrAgSME7yhw4aVDKPlwzAwBSNtJ3demIkIszV1N3U_vx43eseN3nGjd9zoHTd6x43ecaN33OgdN3rHjd5xo3fc6B03eg9t9M7f_xeJgSlG)
