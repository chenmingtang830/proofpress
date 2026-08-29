[//]: # (ob:79e7e919)
# X launch thread draft

[//]: # (ob:b19917c0)
1/ Agents don't just consume enterprise knowledge.

[//]: # (ob:a51f8b80)
They create a new knowledge layer: conclusions, claims, analyses, and decisions
that future agents and humans reuse.

[//]: # (ob:36027788)
That layer needs governance.

[//]: # (ob:9426b2a6)
2/ Enterprise knowledge is what agents reason from: documents, databases,
policies, ontology, memory.

[//]: # (ob:8c792660)
Agent-produced knowledge is what their reasoning produces.

[//]: # (ob:2fd324ac)
Existing infrastructure organizes the first. Proofpress governs the second.

[//]: # (ob:79c5f044)
3/ The core question:

[//]: # (ob:9ca37aa0)
What may the next agent or human rely on?

[//]: # (ob:6beffdd9)
Why?

[//]: # (ob:538bfdc3)
And under whose authority?

[//]: # (ob:36cbaca6)
Retrievable is not the same as verified, current, in scope, or authorized.

[//]: # (ob:87c71eda)
4/ Proofpress turns selected agent work into a Governed Claim Graph:

[//]: # (ob:d68bbc32)
conclusion → claim → evidence

[//]: # (ob:0ec43c0a)
with provenance, verification, authority, scope, dependencies, contradiction,
and supersession attached.

[//]: # (ob:6e7ebf4d)
5/ The gates stay separate:

[//]: # (ob:707b2289)
1. integrity checks
2. policy recommendation / escalation
3. authorized admission

[//]: # (ob:285b58e6)
Evaluation can recommend. It cannot authorize reuse.

[//]: # (ob:4b005031)
6/ Why now: as agent adoption and autonomy rise, accumulated agent-produced
work can grow much faster than the enterprise corpus it started from.

[//]: # (ob:d2e8033e)
At some point, verification stops being workflow polish. It becomes
infrastructure.

[//]: # (ob:1e5339c7)
7/ We tested one bounded implementation across 7 models and 126 paired runs.
Rubric completion rose from 89.3% to 93.4%; observed unsafe propagation fell
from 8 to 0 in 63 stress pairs.

[//]: # (ob:bf9660cf)
Mechanism evidence, not a universal claim.

[//]: # (ob:d605a1cb)
8/ Proofpress — The Governance Layer for Agent-Produced Knowledge.

[//]: # (ob:aac86212)
Full thesis + technical repo:
https://github.com/chenmingtang830/proofpress

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzc4ZmI3YjlhMmJjOGFkM2Y5MTljYTUwNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImMxODRhM2JhIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9iZGE1MGM0MTAxYTJkOTA2MjJjZmNhNGUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzdhZjhjZGQyZDljOTkwMGE5MDZlY2VjMyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWt2O47YVfhXCRdCLeDwURUmke1EURRIUbYEgCNoCmYXBX1tZWXJFaWadwQK96gMUfcI8SQ-pH2uys8quvAjaYq5WI0s8H8_Pd85H7eNK1E1uhWp2uV5tV6fTLmNWZpILIhUTOrY84kokmK7WK1np807ne-MaeNYdBEnSLSOUUpkIHhNmpM5shpVVGTYkyXgaRwnXaaZZEsuYSaqNzFRCDYkyRoglTMK6Onequjf1ebV99H80u0bswUIhGm9qDRfSFHDjL6bObS5kYVBt7nOXVyU6wPNVfUbyjL6uq8qeauMcvHMS6rXYG7-pJ7fr6nsD221rv-ChaU5ue3u7z5tDKzeqOt6qgymPeblvRLlnMb598nZt_t7mcL1rnal3qiqdKcEXTd2at-vVwQjvRBUxKmIpVt2dnbkPD4FzzU5q8KWiEY4E0RynhICzBDUeWVU3fmu7Ii8NIB8iUuwyYZnSGl5QnGMs4D2jjIq77fTodkqcXFvAhonHqapau9X2u8dVb_5xBVGuauevup-N3klw-XertnxdVg_l6hXsYcgHMO0vVWHcLYApG3cjanOjaiMa8M6NuCnNw41_rzB6b24KcTb1zZvNUa_WH5VUomnqXLYNxHInhcudTy1T2J1w4OPGhPXa5lDVHvnrvPRLurNrzBF-KcXRh3jYwRpedT4tVtuyLQrYjzpAHE3nCVlU6jU8nXGTGYAAj0MIG_PG7_ZvqDnA5jTStbA-6XpTQuuA4eQzzjzAnV-hd55tzicPw4cbnLN6u74YkxHnUabwQmPRLfpdcD_SVfnrBn3fugb5xGuPBsF9U5_q3Bk0RmJzgXMStXiCRSSRZZItxfLtwZxRyACDBIL4X6yiEP-tR6aK1kfArZEqRH6Ef0UpihlUcYpJljG2GJVoOvMAyWiH9p5LSlGqWV9wSlJJRLrQKrlFXzzjfZQ79OABdTUDNCUckJStq-MWIqggamUzg4qpjJM0XRqhkCo3QAq6VUY_A6s5mLzuUUGmov5RN-cpYnVMqFALMX3xBhja28pLWwsHXKmatjaoqveizH8wzoNCNq9ds5lQeAjjDKqMq8RiSheiim8RpDPkKyD5ewttBlJ2O5cuSsSZEEsD81fv_KM4h72W8HaXIOAEdGiPooSQFGdUlb-dgZBKY63WfDGE89zqCbRnq0NTWZR5pUZtqaEIHw4VVERH2XkzazNOlRRqcQ1-Y6B1mPswD0CCl1XIb-SgJyDh0H2YFowGImrrGry9hhREMGqczBrN1WCmsshosRAVvZ1mMaR66RA0NBg6oCK7qD9U9WvA0lRAo18FtoKffg9sOYNKp0xKFZOFqC7EjH785786ag5X8IA2wJUzprFRNFZ4qUMeYLjyRANziCfldR8YJXzNrS-Zsh5io83JlB5UPocqhSYuLdULUSUdAez9jIlcA6XpjLfRmDkayHAmCWFLazDa-LCbvd8ugklTvXZ3JdmgU1Xk6oz8XHaEDqGDa9AtMk6JIvxxV8YTji6AUp9yNEtkwszSSvriXhRtZ1QFMupxbNAfGn_Hl1Yfpx_87A3j71zHoBLjBMfRQjTpLQKygnp-2Po67mpG6OoUAApgGsBSldURPAbdF1JIQWNtvVzQcxVEDMNxbJYyXINcBcxyqnJPJdMkhvypTg5J49ucL25bVA8hqO4QXDiDKjJJHHOVLUSVga8M8joJKKQqDZKVp2GN8uOpMH7a6BAKVVdARxk6VtoULnhxBpW0HKYQZRei-rPxc3fujiO9rAM9C-gROXjOiaKjoM0s4-FEREouxMCe8PCP__h3qPevxuEQ_SnMjBZacDc2fT2MTX-EzJubooViKYmWMvGXIEx8nwKpgz6HyKlDCWlUQFWdqu1dOS9Jfwrr1XrQdyvvVi-iugHd2wy_DBrM7IDDWcIojVKaMMUg6YjAONQDxCas2UtQ1EvQjqJCwgdFXQdLXlkNf3lh9cprV89fkxWmenaySFDKC6Wuq2yzs-CGMHT3itrJaAubSpWmILM4lZnVmIC-w5qB56OMZXHGuJGGWs6wkiyjILnTmFgrpWWcEJ9fwP9NUMZduLaEgnT0d1YEk_QGsxvCv42yLSHbCH-O8Rb7QbD3ODxlE8NJQizkyeXu4y8vpkOKdmL3INzB927KaBzR1BDrKSasMdG_ffZ-mKTtl0y5EFTJ1JJUD0tOVG6_5CcRrsMmMs25oQwLIgaLEy3bW7xGnp6dCVewf6PCwRI05sYP7bYNaqXXc_6JMLC793fBHnQEkwLXGluC4wH0ROqOoD9KvfZrE5vwWGCeCJsOa08Ebb_2NRoVvAFTiJDCO-auDAWeex8B41VFtYdp7WiOVX2eQalxKpgkOIHMGFBOBG6P8pNq1t4ylTzmNmLKWj5YnsjY3vI1ytRP9UFswKgEc9L7oQDVYiKMlNiISwGO2rWH8qFydCjBTFDgnIgTNZbgRKH2i14jOgf0KpYJ1ZnSYRYIhiY6dDR0nlkjAnYWWKRxHI9rTNTmkAYfIyD7lZmEeTylnGDGLyU2asp-5WtkIrhqnHvnoqwyBuWXxQmX4x4nOrJHco00PKKvanE6zCSF4BbDuESjJCEDholq7DEsEYKju5XQOIbM5aO7J9qwN3CN3POsDARTQ89R4fG70jOua0_QVLuTXSSaRsBIMReNVAFBitTQmI7UO5GLPdCPU4DD0pHkkcWKZxyP5XwRhUPzu0rnTVIOZM8x70603xV_Q3eM0lRrihMYgkayu-jBgew-jcQbUgHGAqIT6EByZLWJ6uttXiPkuqfHvnBXhsrw0Pc1iKtjqw7IAmkDYUCfLkNJT8YKYNJT61De-Mj6zwihv83siFOaJplljMdsrJ6LYhxY6goRKL3LDSTC03Yzg8kmGc9YDC2EjAU30Ys9pmskYERSdBJ5DU_Xbek2d-U3raxzBf7zL4f3ak_H3nuI8U38GQJu4vGGfvYbVEln6nvjidsJa3zVn8S-s2ZNUdyV3Wv-FexZNY3BS4H8vNG5Ds7iNMsiommWXYbMiyjtt36VzuwtSWlkSqEZ8UheaHOUnr2l69Tkzw24PIkzAg9jwcZJaSIzewxXKcd3P2Y-FZJvPZxnvhUanTfjl0IFmfNm9Sp8dwy7--n9n3xZnNwPU83lkyMkzv_Q98YwLn3iz42FaEvgsOePDaBEw1DyjBADb3bK5X1G3l2il_cwRnSjDmq6uRryKO_G2GfhbDpjA-bH1cPBa_wvcxBMvkm890UUPthvvBr-4NOJmS_jHfzpscNUck-PIh5_oQB8-MnKeLIwLriN3j5_dPBz5yif5LCE4wiG8RjDYKpTodIoNSwzCRdURsa3GhGnllKVKEwzQ4GXwIJKJONKSZUm79_Sc8clyTaOnzkuGf-HxH_dcQmXEew1ooxHbP645PnseTk1eTk1eTk1eTk1eTk1eTk1eTk1eTk1eTk1eTk1eTk1-X8-NXn19j8WMnS1)
