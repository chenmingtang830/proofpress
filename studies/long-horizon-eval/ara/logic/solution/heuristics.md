[//]: # (ob:b06181ef)
# Heuristics

[//]: # (ob:c7ffb944)
## H01: Freeze once, fork many

[//]: # (ob:a87a94e9)
- **Rationale**: Reusing one sender state for both conditions and all receiver repeats removes sender sampling as a condition-specific source of variation.
- **Sensitivity**: Regenerating sender work per condition would mix handoff treatment with sender variance.
- **Bounds**: Applies within each frozen model/task; it does not remove receiver or evaluator variance.
- **Code ref**: [src/execution/verify_receipts.py].

[//]: # (ob:9998f564)
## H02: Keep clean tax and protection benefit separate

[//]: # (ob:4478761a)
- **Rationale**: Clean cells measure whether governance harms ordinary continuation; stress cells measure whether it blocks a defined trust failure.
- **Sensitivity**: Aggregating the arms can hide a clean-handoff regression or overstate protection.
- **Bounds**: The two arms may share rubric denominators only in explicitly bounded descriptive summaries.
- **Code ref**: [src/execution/verify_receipts.py].

[//]: # (ob:f5ee07e9)
## H03: Fail closed and retain every invalid attempt

[//]: # (ob:42d9a21c)
- **Rationale**: Transport, parser, cap, or identity failures are properties of the evaluated route and must not disappear through fallback or selective retry.
- **Sensitivity**: Silent retries or provider fallback would make route validity and operational cost uninterpretable.
- **Bounds**: Invalid attempts do not enter quality or unsafe-propagation denominators.
- **Code ref**: [src/execution/verify_receipts.py].

[//]: # (ob:56d0070d)
## H04: Batch policy review, preserve item-level governance

[//]: # (ob:dee706c1)
- **Rationale**: One transaction-level judge call reduces inference overhead while independent verdicts and receipts preserve conclusion-level auditability.
- **Sensitivity**: A single transaction-level verdict would erase which conclusion was rejected or escalated.
- **Bounds**: Deterministic checks remain per item and higher-risk escalations may receive separate review.
- **Code ref**: [src/execution/verify_receipts.py].

[//]: # (ob:02932426)
## H05: Publish from content-addressed receipts

[//]: # (ob:946b4dcd)
- **Rationale**: The result set should be reproducible from explicit paths and digests rather than whichever files happen to exist in a results directory.
- **Sensitivity**: Directory-wide aggregation could silently absorb later or invalid panels.
- **Bounds**: Digest validity proves file identity, not correctness of the underlying evaluation.
- **Code ref**: [src/execution/verify_receipts.py].

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzFlZmRlZGRlN2M0MWM3NDQwOGI5ZjRjNiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjI5OGEyMWJiIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85ZTM3ZTBjM2M3ODYyMzIwZGQ2ZjgxZjEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2E5MWUxMTU3ZjA2YjU0NDkwM2I0ODA5NyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWltv20YW_isD9S0r2bxf1Kc0xWIX-7BBWuxL1hCGM4cSa4pUOKQdxfB_73eGpCxblmPHAtJdpGhRm5dz_c75zhn6ZiKbtsilaheFnswnm83CpVyT1hSrwFVxEDhJluaBiibTSVbr7UIXSzItnjUr6YXR3MkS35FEUuepQ2lCrpY6zp2c3Jh8rfIwjNxQB24oKdAqTCPHz1KtojR2k0z7kKsLo-oraraT-Q3_0i5auYSGUrasaoofMipx4T_UFHkhs5JEQ1eFKepKrPB83WxFthXvm7rONw0Zg3c2Ul3KJbFT9y439R8Ed7uGBa7admPm5-fLol112Zmq1-dqRdW6qJatrJbw7Pze2w196gr8vOgMNQtVV4YqxKJtOrqdTlYIAoR6aSI9N8sm_ZUFXdmHEFxapOTH5ChfxUnk-Z6jdZQnbu6yZXXTsmuLsqgIlo8ZKRcydcl1QwQ1ysIgSBHAIHHSuHdnsG6h5MZ0JRz22E5VN9pM5h9vJoP6mwmyXDeGf-pvk15kCPnHSVddVvV1NbmADyMeOMFtpwsy52VdLWeruim-1NWMrmR5LhuJq8tCnZu67Fqk4XxFXYNMFMqcrfVk-iJcybZtiszKWWTSFIaVU5kvpEGYW7LyuhYmsPGXRcUizda0tMadSq45y6MTU7xqGBmTedWVJVxSK6SS-mBkZa0u8XTmRG4Ck_A4stjSZ3b4HzsfcHlQI2GytoEG4OgaV34S955rtxtWz5kGaia3F9Mx4hNAmg1ZqIZk74W9M4aEFigEGcWJRpWk0guQY88J3ZytqurWYncAhRhAIQBPdbmpi6q1GG-sJnZ0_I39vGA0lYXa7knYR9ieEIvdbwSfqfN2kcNrajZNMWDcZO48p8h1gsjNw0hLmWc6yOM4VVGU60D6DsCvtK-zKAmdPA99J0xzP8l8FSonw9Mhy25la7HaJ2DuIpF8YeI5XjRzkpkX_e568zCZ-97fHGfuOHhpCDieCrwoDsJITW73rt58F3RbyPXoW0mzYkyFFPtZ5MdKpXjAytgD5IDGr-Hs9nb6aHGTLtpdaSOVVTtXtabPkwvbLnSnjt190BYO7n7q0I53t1fdWlbzpkB5NZq75f9W_7Dmf2v7UHGeZ2kQ3G8fjjsXf2-IvpCoK0VTkdfNpYCa7ZP9BIl-8s2HmZ_e2SGTWKYBpaewYybevPkgOYiypDdv5uIDdQYKIYMEeE5TI7gqicWJrG5XAjoBNg7WzsoSSbxnYpqmCfrAw1B5c_Evoo1QJclKtPKzkJUWwGcLdmZez6iy1fB03J4npmjhANojjH86nkEQJ3HkypMbexDcd1aUorI0Yk3SdA2J6xW1K0R5ycNQJZE6gdpaPxHcPCRy4oP8-8i_LErYWxvS1tiGWllUgnjMEkWFKiy-GtznicGNFky8ab8SWk-D41x1clMPQvt7IyvDhDYVyDk6wFRgNpoKoLbQaGlFuxU5dCLkT4QW1OU4saMf2BvMxS-yVSvRE6zozYAmzGDUXJFA813Pvhra54kpEYNyDw5PR1gTxU6k3JNbfBDhf6MjtBxlaeE_2PlHp3lAkWUJHUwzBtl7IsKOl_oeiPqBveFcvO8yPL0SeVOvhb1XtTPYxXMuMUBsKJ6O8PPEFJvWPB3VNIgy7C365FYe4nbFaw1meO5W-G9Vd6VGa8HFnrcLHgSttodRBT2rUhbroyz1wIphunyrtREbdkNZQ2bLRmoSbz-8Hf2Zi6_Q0xE2-nZ9r6EhY_tHD0DkFmXDscPwbfD_NcrI7CTI9aZkqRLv3AmYmQ0prJhKmLpr1DEie2U0X05aRzjqhFF-AR8ZdFKUiUR3ZnlF1VlBPyMtDP0jQuBOPwkj3hreVSgR7B7HCe2VQX4peR3hqhOG-AW8hCAhdEDEBvMrZmhR5wJRFDw9d7xLiqbuUALs1RoxFLBL6MJIbJWywaO4vURnQilkEi4dIbZXhvgbSewIZ50w0i_gp5ywNAPYbB63f-C1QJeFLWgcFadF4I4uVGsGDPWkceckzFBlZwY9xxjulaF-AZsdIa9TAvn5REWf0WYVan8j21Ufwf4AER1Z2r7QYr3ioKsV16XIEX2DNgMgozXWEACCQzrQNVhlT3UjD99Mrld8xvGuXm84a1wiUPsFr77_IH7yQ8E7KNc6JMkjfnpnkRi3TXFdYE3sWmGXPuaH3k9ji7TiZZsv9meOEMVIMqg41ADwBkSd8YHDs89_njgN7POzf7Czf6qxf9hz82ND_bGh_thQf2yoPzbUHxvqX3lDff7Hj4PDf-f28cP9r33oOMnXDKlSPJ1FXkZO6ju-60nKEsriSEuXVOC7qY4pC2PpODLVOvaSxPMc2O5kkUyzYw4dfM7w50ia5z_yOWP3SfH_9nPGdCcul6HOEif3M0-P4vammVHcN8wkowKd5GmWSN9Pg1HB3pgyKPgrnUMQ739XsimsPWf_rdi436gyePgKZNGbtwTFY4BgaYP0a44HVsg7wbjEJbsuPoO4K13n2Ct5Ol3zosPD7_iq1YagDsp-qbtKG9bzFmXEGyk_zBwo1Wqcude1pvK8lebyZ173dY3HeDHtfb6LBeI1LLL1gaJ3kIEnc1b10TTqnD6T6lF7xV__t4uxKZ5tthdnjzTvIcsozEy5Se6R745Z3pv09mF0ohFtUIzelEWxikL8Myrem9qOwev7HcCMo8bjuHq7XDa07GHF-5XVryT_4QUyJfugzUYw4dGm_37GWWaz-xq5C-YBoJhU2uu6F7yWW9AKH340XYYNC5ZW9Rq-8tdNlF7J89Zuq8RvGcuBJ5qMagALAEyYbr0GqrCNnRhTqRskbhKliUO71O4NuPuYOslkOqhNEoJCSlxH0w5Rd8PqMUR9v_MmVmGo5ITbum-b7ePg-g1be9XaJ6zWhm24KrgB7WQNHUte0mCEDRwbz9awxYPTKAZY1lXgbqZwsiPAAdz-eT_wBm3KekP8lvjU4SZEw5IOw2NOMw6KXFoV98B4amxloR-qTAaYj5MxyXsT_j62TjmaD9pj0G0sYx2nYTRq35vWj0HsOx60QY_EyIMkF5yxI81LMGWXjxk5KBvgBRAZ6o-h9vSIa8mMzX8whhJg2jLwiuvhAFa_EuADbNgBp_8rHUv2XPEb231pbf1aFUt04xkmoctRnJ0YuPMNDLnjmSGzp4YauhjlygMRBvGY7L1VZx9qr91RxhExdjOdRLkXe96OjO_WlqMd7PsdNPKZny7gHP9x4ePg-nW8Pbu2VDgSJXCjrKHGdjeQlMxM3WSCkdMMJ4m2B21kRaU5xJI1_K7PcU-Erbmtl6FzT23TUnXDNlTM-kPLZjpsyi3T9dC970j3lQi6uMW_fwKGTSI3)
