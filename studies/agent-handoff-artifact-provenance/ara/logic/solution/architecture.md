[//]: # (ob:467804be)
# Proofpress Artifact Provenance Protocol

[//]: # (ob:ada2bef0)
## Purpose

[//]: # (ob:fb36d431)
Proofpress is an artifact provenance protocol for carrying claims, decisions, actors, and revision history across an agent handoff. It complements semantic handoff: the handoff explains prior work, while Proofpress verifies which artifact version that work belongs to before reuse.

[//]: # (ob:150568d9)
## Roles

[//]: # (ob:33bf169a)
### Originating agent

[//]: # (ob:43948670)
Produces or accepts a knowledge artifact, records the claims and decisions intended for reuse, and creates a verifiable carrier bound to the accepted artifact revision.

[//]: # (ob:c46e951c)
### Receiving agent

[//]: # (ob:cdf8b4ce)
Receives the artifact, readable handoff, and carrier; verifies them before relying on inherited state; and follows the resulting disposition.

[//]: # (ob:577af53f)
### Admission authority

[//]: # (ob:6f2a9e85)
Controls which revision is accepted for reuse. This may be a protected local ledger, signed snapshot, accepted-version pointer, or another explicitly trusted policy control. Proofpress does not infer authority from recency alone.

[//]: # (ob:ae5dfd8e)
## Protocol objects

[//]: # (ob:92c5d29f)
| Object | Purpose | Required relationship |
|---|---|---|
| Artifact revision | Immutable bytes or canonical content presented for work | Has stable content identity |
| Accepted knowledge state | Claims, decisions, rationale, actors, and relevant lineage | Declares the artifact revision for which it was accepted |
| Readable handoff | Semantic context needed for continuity | Information-matched across experimental conditions |
| Verifiable carrier | Portable representation of accepted state and binding | Integrity-protected and linked to admission state |
| Current artifact | Revision actually held by the receiver | Compared with the admitted revision before reuse |
| Disposition | Receiver action on inherited state | `proceed`, `targeted_revalidate`, or `stop/refuse` |

[//]: # (ob:1031457e)
## Operations

[//]: # (ob:4a36cba2)
### 1. Record

[//]: # (ob:d2c00d33)
Record the accepted artifact revision, declared claims and decisions, lineage, actors, and policy-relevant state. Recording states what was accepted; it does not prove the accepted content is true.

[//]: # (ob:118efe2a)
### 2. Bind

[//]: # (ob:53bf7bbc)
Bind the accepted knowledge state to immutable artifact identity and to the applicable admission control. Identity answers “which bytes?”; admission answers “which revision is authorized as the basis for reuse?”

[//]: # (ob:707e95d4)
### 3. Transfer

[//]: # (ob:b8099be9)
Transfer both the readable handoff and the verifiable carrier. The protocol does not replace semantic context with a digest: a successor needs the meaning of prior work and the means to check its applicability.

[//]: # (ob:d23136b7)
### 4. Verify

[//]: # (ob:ad206507)
Before reuse, verify carrier integrity and lineage, resolve the admitted revision under the declared control, and compare that state with the current artifact. A failed integrity or authority check cannot be repaired by persuasive prose.

[//]: # (ob:dc22da73)
### 5. Dispose

[//]: # (ob:3c1d6242)
- `proceed`: the binding holds, or a declared irrelevant change leaves the affected knowledge admissible.
- `targeted_revalidate`: the artifact changed in a way that may affect specified claims or decisions; reopen only the affected work.
- `stop/refuse`: integrity, lineage, or admission state is invalid or unavailable, so reuse is not authorized.

[//]: # (ob:5121f3c0)
## Decision invariant

[//]: # (ob:035845ae)
Inherited knowledge must not be treated as admitted solely because it is readable, plausible, recent, or cryptographically intact. It is admissible only when the receiver can establish the required relationship among the current artifact, the recorded accepted revision, and the governing admission state.

[//]: # (ob:43b00f4a)
## Trust and threat model

[//]: # (ob:10be2bb8)
Proofpress assumes stable content canonicalization and a protected accepted-version control. It addresses accidental or adversarial artifact substitution, outdated-but-plausible inherited work, and broken revision history. It does not protect against a malicious trusted authority, false claims accepted into the ledger, undisclosed external policy changes, or semantic changes that the configured affected-claim logic cannot recognize.

[//]: # (ob:12fee1c4)
## Experimental isolation

[//]: # (ob:461e894a)
The ordinary and Proofpress conditions receive the same readable semantic handoff. The treatment is executable revision binding and its receive-time verification path. This information-matched design separates continuity benefits from admission effects.

[//]: # (ob:d9da6eaf)
## Implementation mapping

[//]: # (ob:0458bd5a)
Proofpress's carrier-native workflow maps the protocol to artifact policy inspection, anchored revision records, claims attached to changed blocks, snapshots with explicit actors and reasons, portable inspection/import where required, and deterministic verification. For Markdown and static HTML, the portable form is a native in-document capsule; other supported artifact types use format-aware or sidecar evidence. The persistent implementation and experiment entry points are indexed in `../../src/artifacts.md`.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzc4ZTlkNGRjODc2NjA4Y2JhOWJjYmJmZiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImVhOTYyOWVmIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV82OWM1Y2VkYzVkZTQzYzI2M2IzOWJhMjIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzMwZjQxMDliYzBlNWIyMDg4NDQ4YmFmYSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrFWtty5LYR_RXU-CEPmRnxftE-pOx1Ut6quJxytvxib41AXGYYccgJQUqWV1vlD0l-zl-SboAgQUnLWUkPqdotjThAA2h0nz59qI8r2nalpKzblXx1uTqddmkmch5xlqVJ4mWsoHnBikLK1XpVNPxux8u9UB2MVQcaxMklTYq0iINIpmEgKJNpwX0RUy-PWZQVNPJoHPtRKMIkjrjH8ziKQj_IgyIK4jyWHtjlpWLNjWjvVpcf8Zdu19E9rFDRDpdaw4dCVPDgJ9GWsqRFJUgrbkpVNjU5wPimvSPFHflH2zTy1AqlYM6Jsmu6F3io2eO2-ZeA4_YtGjx03UldXlzsy-7QF1vWHC_YQdTHst53tN5noXcxm92Kf_clfN71SrQ71tRK1OCLru3Fp_XqICg6UdA8CXKBHsMnO3GjB4FzxS7JWcwEZzEXUciCJCzCvKBBgDtr2g6PtqvKWsDO7Y1Uu9CTke_BPXgiLgIvyyL0rKTmOMPudoyeVF_BgQPcJ2tarlaXP39cDct_XMEtN63CT-ZrwXcFuPznVV9f181tvfoAZ7DxgOf49QT-PsJshV4AM7RmYnegNW-kvKAtvaiafckuVFP1HdwFPGKHsgP39q3YHvlq_azwol3XloW2tCuoKhUGmajkjirwdie0vb47NC2e4bqs0aS6U504wjc1PeJl27OsYarCAFld1n1VwckYbBxCV_ukqBp2DaOjJM28qBAwHC6zE7_iuacwIl8P28fQGs6PH7uGNRXMGfZAOdebO2FQilt48hX5ciPd3Qk3jqECYbf6tJ62RzkNCqFzxNle354aJRaXh_XHUQv2ZREmHNLxufadw5WK0JrYayZTnOBHfUQim5Yw2rZ3sDxh045OEEGz7fixFycZz2fb-bGphDpzWDtm4ahhWEg_yenM9g9tuS9r2uHGIOPqbnmdr8hTExYWjcI8ypLUe_mi4GneM6EI-JAyJk4d-JtgiFeC78Xo-DUZUp50B0FYRcujWvA0ixKRxz6be1owUd58sS8eD1_wBOMyKyImXrqgGSrM8dxDQ4pgORhAaQ3ByHWwlaJ9Q250vVjwQ5ymVMahnG3ra34sNXQQgzZld3fOF09PWfBHIgOaiyx-zcJvYWLbVIrcHkp2mCoipqQOFcF17rUCqtWWvIdKSY4UKiV4cMEnVMRc8uwRJppkbgosn-cS8onhC87IA6iHQS5fvOI9-UEPIvcW9-DTj6ZWczg_EAlwjDqUJ3L_S32_2WzG__DrtDldf-eQ5IV-FKdzZ_wAddFYPOOG2cAlnKBhAqUwmK3ibzHFIKfPBZ87cGERHjDP42H4_EXMCJN6NrBGxLdhtyZcAO6gww386FTkS3DvZ0KKYA7JwZZ8g_s4c-Zp2MKJY8D8tCjYcxfA7-ennQBXdUBKSdeQ8njsdbxMrii5qBfOm3opgC6PZtsJITFbWisp2nNnng9dOHeReXleiPwlC9kxpGi6g3bCQ4zV94pf3Exs3CDuwtl5EPohdAqzLUVbohn9WXh1By7SpcBLYu8Fi3wjACiFQcq1OdidLSOkBFN7BGN98oGdY-0B3nsjyNKpWRBwms5TLt6Sb0t1nsJ9RWYjl7gN83kSRMELltmQK-BpTAh-dakvtYCRWJEPTcXVWtOOKbHLFrBU3NC6I8Cmp01V0IPNM88PfBmyOfH5VrChQNU3tC3pOYpBnpyw4AcvjLMopuIVq76rD3D585Q_9qojddNh4ewgGzT8AbxBte7wM4SBqKCsLgRCFBYeNHFzqHvfomGTTWiWHBsuqjM--eykBb_4XiGCosheubrD-qEj64_AxpRBQG0Vg4LWTV0yWpW_6bKnzVPsBJbKQCCF8NkcFv869p60AkLTmAp-xjefnbRUehNfZPmDm3n-6u8hdaBGAq9vDUw4zgK7vNQsAEk60lidaQoaVg2uSwCSc5oIOmdG746nSujNaR8f6emEp1r2zWcnLeVTFGcFj-krV59c8SdlQXWDDRA44rZpr2XV3KIdQ-7HthFqLG0f-ubD2uoZK0BpzOsdMym5Gr6xSsOi1gLZrG0OkosFdUA1wa5PTalBAlbUK6F-YH9D-eADajVVye4cC65-4xjRytALpR3VyG4nwbeiPbXloCCpwr_0aZSzNPHjNIkCGgZU5JkMfI9FBY3zJIM2K0qjNE7CWHpQFrhMBAcIEDIuMpohDCCL0UqQua3L0P8EjkbBJfCCZONlGz987weXQX7ppX_2vEsPoXzwuCtxfXKefvx_ikc6Zo24c6DqgF0F-CUMvSilAgUObcPRe4ZwfqVSM6wV0BT8nEoWFJ5dyxFv7FpnZJnBWFokzPeEJ2nErTFHqXmsUj1bg9H8XBN2XRrho9EGTfv8SFqlrG2UWQP7dEsEt-QdQH5j8QCqgThCeS2ZHWAYhaWNEBGwLoAgRDPsBjN_ja1rJdwrMKRS2KZ2PNQQZWARShXOhWpcNfVeIU4UDn3bPgGng2MhAbIkiWju0cw61tGcplta0JMGU0lShDwNYwCU0ZQjMY2mvlgyGuxmRSpkWAQ8SooxaCcVabr7F6tCpi2zN6_Jbc1dpWDQUDSqotlHNB97gx55Q3OmJVy4CgBlKG0szlgW2HM6opTjvy-SmWzm0CIURc4zLsdbcZSnmez0Mi3JzDpOEVfpjNL00jJH3SK-0bNlU0FxU0MfpfpKhwHXvFxTggUXhXkGaJ0HlOsOVh_G0ascF32x-mTRCmly5nk-eMpadgSpwfJr5CUNPADlMARwGUiUjst2TVS5r9FFNZT7Q9OtR1Mbm-C6cOJQjG2o0-BVDR0lKztg2R3SVrBgKrBmnrDJrQshvIFbQr5e1tjIjj4hsm2OmoLVMJMCeiyBRZyHOVTOkPpRNEL6JI05kP5FWtdg1adQFDwReN50qY78NVh9nZ41lbHxzu6B_1m5orjrDHKMbH3k7-g_-DlcrEbZe_IdfcTzUejo0KNmuc-pJPfk7eNKYwQxWomHRWdoLC0Vu8f2D9vOeZ5OZ9Jb1KFZQkWgTlTqXf34ULa4J_-09Wlgs6SGvnc4LD4q614firyr4dFRb3QDP4DQcVsEhdsaOMxer_nTY6iEG7QksxWDfw1zbuS0Y-Mv9IPtv3ETg-ywmZJpECCuhUZfOub94G_cw9u-RaI6OQxdMbgMfu1pBVl0EBXHN6YGlzQc4lbfQjHXjf5tOYg_Y5M7ut2ttWbFbyc404sN5mAxfcxH0AiDRtFhTa462u4FfLmDJaBz5DDiSmf_FbCP00UrJKx0RZ6UaYesomlIkeULKcZcdZTbKVfPCbKDvSiUNKYxNAxTdXc0Wgd6z2ivgz3p80gGXMhkooeOHDvVpRfLrFN-jfqUm10GLTdjkul7sFvHcNMPEOrpPJfeYHKNgKqZ5XyDIyQohOZF9hUkcZzRKMvD6ZImCdhx6qK4a6-IBjGNAhkleTJWx0nvHay9RsntrOJnec4Ji5AZNybeWH_eTTPULZQy8sfv_zHopPH2L3_8_t83zrxHo2bl1VSs34zOpFU5fB0-VVu09nlHe7FPBRVBLP3R0Y727Dj6rKJseRWLaQ53x1PNbrVFR2QeFaWXS8ctEginXxlDDkCzotDJqIfYrSGKEvPnKJfwSfVwx0qBjxDWjd-Ogtaan0mn6xh3gd_q_kF37BDparzksoK7XCJngsVh6DPf99mU0aPG7fj4jHZtwxlIAQ8T30vzcGogRznbhvMrZOqn0Rx4PEzF7yZYMSE90F9TEUzbZTJmrA3sQaXZkq-JpNDPcWcvjUvAjJ-BdwxqKlwu1ZQGShEgs-ohzG90FCz3cVQGkSdiT-b56PxJanecf05BHwxCp86jwPeToBi974jqg8HXaOU1AE4l6Nh1SGkKutOzGWyAlNj-Um-eLouXcypk7KK3YeFbemduCTm4sU_UCeoCNC1jrYAtjqXiDbi_OQms0NXdfFeYJWYXbgm-nK7VKTN46gc8pFRabIdN47d9TW8gKjDZgf83A3MoTXpPULd94nXCcD1FIEPfC6ikuvMxWD-9YZjK-5e-MLBlWdJUZiwRnI_NtvMOwQqer3glIBjVh9X10aLhmgCk9fqq16Yd6bQbWXt36pp9S08HZOUwH_yt8-qdnj9FiLmy24Oo5wwOMosIzdVLZRH4qaaBHhsI26dyeG0N6r8Pm8rmRD8seO7xL_Y0uD64_oXE5UERi7CAoh-kk7oxvhqZLvI5bzlsZxXEYebxWHqTaua8-Hismj37HYbl4A871okDwJY5R-NCMyjNIqBN0CmCozEmqyl_VV8o4Axa_oQI6DtMcr4p-m4zRohDno1ippuEtrmGu38o1OkduGQNd0zoHlU3-AnIgF1006uxix6heQ3IXalJI7L3DhFo2I9t4KFglIpVgKgceiFo1KGVG5tx8xd2Opinem0eGmzSIdfUstz3GJQWcDZ6WaIFYVseMAb3NSDDQjxlMkr9QCSJH4yFwHmdNMXTc94M2Z4iz6VMoP4mRTLJx-PLIst5XvHeR4fdQ83U8CCNKceBV4tfBeu7-V-92tKDSyJvGRbYdHDIgV0xE74n2h0GdaZ8oq3lAiUZ2Ab6FlsApxEuRC0kWtfCyZTmQl-bWrgYWoRSsrzI6HQxzrus6WKe81rKCjNZlsDFJGnMRunQeVP1KNGf_9LJ6ugmqiF5oIx2A_gxyBeXQA0C63rMnA4g-2D6c1ufzbuJ9ah6KcOhrKo1dGqDDEKVbuPGV1PT8hflEZ8i7rcTsq-HBhBS8VjWAAQQS24AbMnfIB2_p-01b24NmiFMw6jv3n__d4P342IYH7rUkMFVZb3hDeuPBhn1Hxi_IUaUU_0J57lNKl6aIljxTKBt6C2SR4QDwEK4BQJuA1BkYqD7iKDK9I_zQMBtTlILgf-QX1oahM21uC8OaaGpz9V2ewH_VMsu7EbU9sivHoXnh0_w738Vd9fo)
