[//]: # (ob:36c14089)
# PageIndex retrieval adapter — implementation contract

[//]: # (ob:19668a0b)
## Status and scope

[//]: # (ob:a856a7d9)
This is a design and implementation plan for the adapter that follows the
retrieval-evidence receipt contract. It is deliberately not an assertion that
PageIndex is already installed, evaluated, or preferred in production.

[//]: # (ob:237cdc42)
The adapter's only responsibility is candidate discovery and locator
production. Proofpress remains responsible for immutable evidence receipts,
deterministic eligibility checks, policy recommendation, and human admission.

[//]: # (ob:54ace136)
The implementation is a local Go sidecar, `tools/pageindex-sidecar`. Its
JSON request schema is `proofpress/pageindex-sidecar/v1`; it receives only
sources enumerated by the caller's corpus manifest, verifies every source
SHA-256 before indexing, and caches a tree under the source digest plus the
configuration digest. It has no hosted-retrieval fallback. PageIndex may use a
locally supplied OpenAI Platform credential to build or search its tree, but
the key is read only from the sidecar process environment and is not a
protocol field, receipt field, log field, or repository artifact.

[//]: # (ob:42b1cca2)
## Inputs

[//]: # (ob:5f28e5e2)
The adapter accepts a content-addressed document source, a task query, and an
adapter configuration. The source digest is the identity boundary: a tree,
page map, or preview derived from one digest must never be reused for another.

[//]: # (ob:0c9453f4)
The configuration must record the PageIndex package/model version, tree build
settings, query mode, maximum selected sections, and maximum selected pages.
Its canonical digest becomes `retrieval.config_digest` in the receipt.

[//]: # (ob:60425159)
## Runtime sequence

[//]: # (ob:1571ad28)
1. Verify the source bytes against `source.content_digest`.
2. Build or load a section tree keyed by that digest; cache entries are invalid
   on a digest mismatch.
3. Search the tree with the task query and return ranked section candidates.
4. Resolve each chosen section to one or more source pages and extract the
   exact evidence quote from the selected page text.
5. Emit one `proofpress/retrieval-evidence/v1` receipt per selected quote:
   - `section_span` when the section identity and section digest are available;
   - `page_span` when only page-level provenance is available;
   - `text_span` for an exact offset in canonical extracted text.
6. Send the receipt through `proofpress evidence import`; no candidate becomes
   reusable knowledge until the existing evaluation and human-admission path
   succeeds.

[//]: # (ob:cc331373)
## Governed disclosure flow

[//]: # (ob:19a12a7d)
`proofpress disclose` is the agent-facing, read-only progressive-disclosure
surface. It accepts a free-form query, actor, optional scope and graph seeds,
an explicit corpus manifest, and bounded limits. Its output is
`proofpress/governed-disclosure/v1`, with separate `governed_context`,
`lineage`, `discovered_evidence`, `gaps`, `blocked`, `actions`, `ledger_head`,
and policy/config digests.

[//]: # (ob:20fa4e69)
The command first deterministically matches only actor-eligible admitted
claims, then traverses only admitted, eligible relations within the requested
bounds. The resulting claim lineage exposes the existing conclusion,
admission, and evidence receipts. Ineligible neighbours are represented only
by opaque identifiers and a required action; their statements and evidence are
not disclosed.

[//]: # (ob:e7e35bf8)
Only an unmet or novel query may invoke the PageIndex sidecar, and only against
the caller-provided manifest. Returned `section_span` or `page_span` receipts
are source-navigation handles for the calling agent. They are labelled
`not_governed`, remain outside `governed_context`, do not write ledger events,
and cannot become a conclusion or change admission without the existing
propose → evaluate → judge → human-review path. This contract is domain-neutral:
Legal is an optional claim profile, not an assumption in retrieval or
disclosure.

[//]: # (ob:905225dc)
## Receipt mapping

[//]: # (ob:ee5211eb)
| PageIndex output | Proofpress receipt field | Deterministic check |
| --- | --- | --- |
| source bytes | `source.content_digest` | SHA-256 equals imported source identity |
| section node ID | `locator.section_id` | non-empty typed locator |
| canonical section serialization | `locator.section_digest` | SHA-256 receipt value |
| resolved page range | `locator.page_start` / `page_end` | positive, ordered page span |
| page text or rendered-page representation | `locator.page_digest` or `text_digest` | SHA-256 receipt value |
| PageIndex query and settings | `retrieval.query` / `config_digest` | typed immutable provenance |
| adapter release | `retrieval.adapter` / `version` | typed immutable provenance |

[//]: # (ob:8634da1d)
## Explicit non-goals

[//]: # (ob:db8423cc)
- Do not make PageIndex a new admission authority.
- Do not treat a tree match, embedding score, or model confidence as evidence
  integrity or as counsel approval.
- Do not silently fall back from a section locator to an unlabelled quote.
- Do not introduce a vector database as part of this adapter PR.

[//]: # (ob:4ed61524)
## Acceptance tests for the implementation PR

[//]: # (ob:ad7f8157)
- Given the same source digest and configuration, repeated indexing emits the
  same section identifiers and receipt digests.
- A changed source byte digest invalidates the cached tree and cannot reuse its
  old locators.
- A selected section produces a receipt that the #39 contract imports and that
  passes the `retrieval_receipts` deterministic check.
- A missing page mapping, malformed locator, or quote that cannot be bound to
  the adapter's extracted representation fails closed.
- A corpus digest mismatch invalidates a cached tree; a sidecar response that
  names a source outside the manifest, omits `fallback_used: false`, or emits
  an invalid receipt fails closed.
- Disclosure tests demonstrate actor/scope filtering, bounded blocked-neighbour
  projection, explicit limits, novel-evidence labelling, and no automatic
  evidence import, claim proposal, or admission.
- Existing lexical and OTLP evidence paths continue to work unchanged.

[//]: # (ob:d1c0a627)
## Follow-on evaluation boundary

[//]: # (ob:b0dd596c)
The adapter will be compared with the current lexical-chunk baseline only in
the separate retrieval-adapter evaluation PR. This document intentionally
makes no quality or cost claim for PageIndex.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzk2ZmI4ODgyNDBkYWQ5NjNiYzAzZGIwMiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjMyZTlmZmFmIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9hMDhmM2ZmN2E3ZWEzMzBhYjdjNjljOTkiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzE3ZDE3MjA1Yzk3ZjY3Njc3ZWQxYTE2NiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXFtv20iW_isF9cM-rCTzIpKi8-RFsr1ZNKaDJBgsMA7kYlVR4pgiNbzY8SYB9ml_wGJ_4fyS_U5V8SLZkR07mJ0BBDS6FYk8depcvvOdU5X-MuFVk6VcNKtMTs4nu90qDtNkuVx6C0dyGYd-IhxfJo43mU6SUt6tZLZWdYNn6w33gvA8Up7reU4QeIt0uQwjL15E_tKNIp56SerES-E7EQ8dKYMgkjKRobfwJfdk5ARyoeXKrBbljaruJudf6A_NquFrrJDzhpaa4kOicnzxR1VlacaTXLFK3WR1VhZsg-fL6o4ld-xdVZbprlJ1jXd2XFzztaJN7X1dlX9W2G5bkcBN0-zq87OzddZs2mQuyu2Z2KhimxXrhhfrpe-c7b1dqb-0GT6v2lpVK1EWtSpgi6Zq1bfpZKM4GdH3VJymPJ2Yb1bqRj8E46oVd5apn6YRjxT3fYcnkQhjEcekWVk1tLVVnhUKmnceyVduJN0IJhZxlIZRGEVKutwNQ7Mdq91K8F3d5tiwR3qKspL15PxPXyZ2-S8TeLmsavpkflZylcDkf5qIUqrPk0_YQRcNWFiWoj6rVFNl6obns13Oi_rs3cWvb97-4fWb_1i9f_Px_ds3f7z4bXXx-uLdxzfv51s5mf5QOPEGwpO2gRdXCa-zmoJK5emK17Buo7S8ttmUFel8nRUksr6rG7XFLwXfknON7lO8WFM4TM6LNs-xE7GB_5SxQJKX4pocEwp34SzJ2HBdoz7TPt_B1G8LCGH9ZhmXfNeoiv31v_6XZdtdrrYwIcdrVgkupdZuR1GobvHNL-zpcmjDjBSoyNLTSXO3o51QrCDuJt-mg8ZuHIZL7iR7Gn-AiLZmvJAMeYN3j-n1C3vg8SMr8mUQ8kjGz17xIxKS4R_OpKqzdaHfOtg8BRNLy4o1G9UbqdnwQbUdr_ieXp4fCSkW3gv06pf6p5qVRX4HR9U7pHCWZHnW3JHSAqIyCdhhPSaR9CN6LbzEFYLv6_W22LVN_Yhf-oeOeCNIvaUK1I9KH-2VcSHUriF_aAlFM8PzBBhKMuR4S15hddlWQk3xUHNkr46IF4GfLp6hDZ5Ps3VbGf9v27phBoR0CAy5Y1H7bIu0ztmNOqJN6Cy8wA32I_V9WzTZVrEaQK0K8VhuPPD4sWwMIpdLb_nsFd050yXsTu_aGB2FC1WO8TXPCljlynw7t86y5fZqflkMuuUoeXuKxU7geYEU-4opobJdw7Z8t6OdPGKJe08fMYRSgee6Knnuel9HHi_bBgHEvo6qN4WGFpVmKpf46bVCJKMoY9_ZoJmulnt6LUN_Ibkr9_R683mXZyJrWFEWs3XJ88cS88EXjlhDJsuF5wvxglVn7HWJJ8l41-N04KxQt0jlbaarGzPlEGCFeOjfORIYCyVDF8xsT7ULjQgcscqIX9U9Eh-g9CNmeqqYd-8fqTgySpdIrZ-u44z9moH7mFzj2z7hTErpqrEHS1PE3U4B_FGvjthUusLhobev77-WeV7ezqARFf7WKJeUbSE5aO1xQz727hHbJUSr41D8HF3GZeM2y3OWEHBvgbwwyS0osjalaKuKakauPmcCzFBs2uKaHQL1p2lHPCeoohS8K1Fp407sLx1FVCs3TaVKPKVcoRZBEDrcV6nnO8TyykbLtNyYWW7MwNLF9a7MikZT_UqvRNSv-xMxv09EqpGFdyMJY6I9EqIp_DM5eF2mzSqFa1S1qzJL9evEPU-CREUy9d0wUo4f-r5IhefHrrtIPD9EbQ-TRYgvoqXyfdd1IrQGEU_CRKFB8iOKsBpxrim78da5G4Hb0jcTz_HCmbOceeFHzzn3_XPX_2fHOXfIatbiFKxcLl2FAPk2-vbL35bn62A1THzD6w2FHo8C6YZxkjjUJWkZI3Ju4_gnc2q7dir9RRqnSehHqlt7RLO7tZ_Km61UJUGOPD-VIu6ljqi0lfoSboxqqPO6ph8ui8FjyF5JxKOvmp0Z5uxtQ6uBSWWJAsYpcF4qGFjAtFi0Hom-LAZLk3o5MlWCEIOQ8DxXctohCX2EaoCMVFWEChkUrkrZCpI1f4CtWfuECydypJ86vqZP2j4jSt_b5_kcnSHKOBrcy2Kk0D6p2BLFGiQCTsjO2XbbGnA5tGQ9vYRJBuohGCy57lTR6FFPmYEYTWe3cKO0tYRU2rRbsnVXvo_YB5gS-_FSOJ5YdPYZtRZDVB7rGqysZeT6bhBw6UreyRo1Evdt_cM9Aq-vGdhudWe2yYvLohO1V1Hn7OPmsOxmtanjsHRDZuwK0zkJrpSCzXeE8KCRXaxReUIUV6jmkqVVuUVo9PJ0L1GgolRUrirVktLkV45Q36jqiNGXUZIEsUrCNPI7Q416nJGhntu-aMCd6n2xpM1yeVnUqmngMASOtiCjR6fY7eds227RReRKEAOplY7g2lj43s9kohok8G2jE6IsqBR3JkkoFNFTXPUgMTcb6LoJSltS3Mb5ERMJxCCqU8x5GHcmGjVeQ1w-rZPqDO-6UoU-aqqf9Bg8NFdW6ou6JW_O_oUMTiGUlxxB2pnUeONa3cGMyZ2BVvPeK5gSWc0gCWbDKhXitID5MviNMUYEvA-7rN7yRmywlD9nHxSvhKFHWnpPloZU0X6EQ9qqYBUvrgcfD4hGHl3M0YvVZX4DPaANYKasQWJ75Usd_NjVtqx6q-hw0CvAdIT9pkhAZ_WZ_tQj219aECqTQ9qo43hiZHdoEMzZmy06F1rnahgwnt0vOWc37lVfdnbIwF6eXudcazCDl4zyq3rHiyt2u-lIud1TjwW61tovO5aOTfIbnuWE0K86gaTuWJouFfTlLAcS5FSTQDF1-0D17N77tFP7voEKa6cyTZGflB5DUlmLYlPWPiH5u5DjDMLnqmzXm7G9BqOjwoNXXr1C8R1VL5ulWiWCLV2CrovyFgUXzqB8yvUa4Nk1QcaYzvfVZTY0hzvebLS0ugWeK1nPH-hibAa6yzh2vaXnJKHbZeBoijDK66fMBazQRaD8BCTZ95c9no5GBVboS5p_Yaou-3pZfGWz2Yzt_Zu-3IOJr98DCPzy4d8uZl4QMuAVmnPrI0pKI6CPSSPVBmUBsGZvX5NgSzfmXWxnkqRSt6-2O7xHZupJiZEyxFQnDyQsA7z8p3HqA1Lv69uZh2JBGbmVwQubxRUNvseyTLI0oOxX7MzmDuKXhO7KOmtQVqnSosB2IigzjOgeFwhx0Ffph2ZmHUX-6nnr4YKd5njPpNuTtjKExgCaXcWkJYaKpn_XGzqobV-t6QdeN0IDvUjHVSqgFa_Vvlz7o5ZsC_hjMh8aSdmUcBaOiJbSl8Lv-4LRlGrIs6cOnazcOBC-q2TohwvRyR3NoazcF42VGmrXLSljutahDdgmSpIu1BJVOmyY4TraCQbu-AB9BEfoiNWahNPD-E2A8KFOMAAKbAiLj9assxwBBSxPOY0fwKZMrRqKd5dQqIOI0bbQR4N5V3HGsrCubgSgEJgYnX0x4C5PyONQA0yH8B4ISxXCRsS790cwU0o09KESInZkz9GHAdvgy5dOxrr1Fl664IFa-mroKYdhWe_j50-5KBh0YUG5rzvKYITslWZAcVVbAmNS1kivtb0vmDlsk2Pw7em-4U9Ebsz0iBiWNEGldeMFOUvzdgYtSIMy74GzW-GQF9uuk0jPqAZzzXvYL37cN8EW2I32ptdl8D1aG6PPkPmrruu7YvJ-ybF66IyBxboWhWoisfccLt4OeK8Tw3AtrZXdJRoU3e4gekmNZq_dHXjGAbKmYC9Imxw8UGo13nSEwI7g9N5-__jbu4FyEBeotRGyAtiKbLktq2vki3XVkTD3BCBLeJGfJH2rPpp5DmH-jLllh15eoJw4XTjeou92R6PMBzrUHx1HUpbTDM8wwwwNqiGc1N80ahgnzboFRlsACDA9qelb30yTB_wGVLq7LAhNayJzRB0ssIkSwS5ynm11tvdYe6-3-vSNDPHAobySWXN4JK8P-CnO733_8BG-uaGAvOt_oIsK_yBH-zCZHuc-42Q_WHChXD980enwATrrOR3lc85-LVGZpBIciX3VlGVenxEAaPyc1UfOKIXwfdfX04VBr19pZlXQaCWrKatbtDgpMumRY4Ijrx29QcBdj0fyxRqMOxv7mrrqpjnadTNEh4ZDmh7OTEtWlWu8cexc30n5QoXxi_UzY5rtltydZhWycQ_FKXMNi1F2sqgzb6Ynekf0U5HygyRdvli_3_WaRFm2SrPpoqRO1Q6BOIHUTXmtDgZKJuyO6PeTTs9A4qjKy8OyAETRoLafbqPJ9v337ZENZZ-tsSaJbAaZqg8IJ0TF16Ktm1IOc8D5_gWIIbEPLGuXea1SwLxZZ23dMhu5xU571XfkjxL0YfkfdkrQzupDUqCh3tCSriHXSxAJMIdH8-8l4ndWssWptpExHHn0VV1z4W6XzPrbjGCHGfN3suvhRd-bi2LafLKkAfmsUC2IiKlrqflhMOfFu7fz750wfzcULiRWIBYzMyRGa0x9zqgDGSJWj_SN-T6NgvrL5HZz12u8H82WeOX3EsdEW28xC0c1CPM4RnquSKSibBvDZ4lgPdQi0VHak482j9z3M8YZn1mOz-vG55hfTjXvVPNONe9vWPOefkHh8IA-mA5yz91vD5_FP3Yx4afcPlgsfE_GPBGpEImPlIiWoRPzmMtw4UfJwolD9Fwed-NlsAhdmfqShz7YvMdT6Ur_KZvbv4kQfXSc8yA49x-6idDfij7dRDjdRDjdRPi7vYkQ-cCJ2IkFEKe_PTBQjZF9nssdzC9XFBT1ZfHvH37_A7NTC4T3BrYhUeODx3vv0rnjK5Y1xjw3trpdFmb-WDNVtFsdZvaEl8aOiB5yJcjjDrkEa2QpVpzSIb3h90r7z4i4LLozikSlpT4GNqPSqR1a6pJqZ-NE-qvxGbUdfe7y1qbI_vUB87POCdic5kibkiY2swFaaPxN0-_5CHioXtKQlF8W2soIybpFcQAYs993qrh4y97lvKFB5Li_akpz84CypTbH1HrYS1ct8EtjJmPXSkc0ZZuJ9uGI2BJp-EPoU83iJqvKQs_FNGjUJpN1tDelKHNzcjfdP8ibIjTW3Ud9lqTPnuhv7nQIfroec7oec7oec7oec7oec7oe8_98PUbKAA2SCNxQeF0GjuYaQ17_2ICiq2axmyRx7HvC5QPx72cWVvpLhg8HEy7AalvhYaVJx1DOUiTjTBOGrlwJc3i5M4ddpt0wM7SK7zaIPtgNJUhHhL2wcI9R7Y9C6WhZU73usk8Gn47z5oGpLSXO1KBEf2R31T23sj3_FfS4sp0ynr7qOLiiv3FrQou-XvNdTf_VvZ-S9JGb2kEfdTBVK3LSld6XtCz6zJSE_qD7-zVApcD7ZeI6QdyXydGEZ69MPm9UQ5FPcdwgy0Am9Tx-SmFAYM2pjPYv2aemrH-xUrnOiVrbs69s9pTwstCeqg0VgT_aXOeSGW93f9sCvi67A_M-3WAgAYZLFZz4jU0z4_57_QsioOhVKlS23mDdytSQ_rhbScvjUXfKHYeK9-4fcGb_CrZkxouvSKkM0ErHDUTE6n0FOEU_EdQuheQRVyaLxENaJolwg_4C2zAMs658yVSrMvYxzjJV2hBw06DMCJkzSpwunajcUVHEVwd1gi5WjYC-szR80Re-WcFvsrWBxA3WzdUwFqMF9YibkES7_057o7tQg-SC2VZd1l1NbdtKaUx7eSghwYZ1M3BbZchYk1tMz9Jqm1z9RQgCd0OobRDpQ3Q95h5N3buB_DjwdKNB8cj--t__048D9B_-3FJpoE8G_C03JuS3R_rDtZD64LwD1fg3tQbmUUUsBgg0mYAl0ywHEx2mFu12Z8pzMZoJUdc_4NiRUDtdwDxdwDxdwDxdwDxdwPz7vYAZxUqmyomUw8PTBczTBcz-AuZF1_QcTDv2jM3Hpn5FGWQnqf2VlM4adOGNnrfe6wgWaTd0VaUOkatuMkz_ByJ5TmlaU5uD3eoYInG86PQYSvnhDl4P7arJEKm20KnRrZZuPc5M7wfWA-toI3c9ne2kZj2N1x41_18lHd99a2i6v6khyMPxkIGMfpqOth_4BzIGX5Oog8HAdKBgqJY815sdTjJOF2L_8S_Efvr2f9R2VE0)
