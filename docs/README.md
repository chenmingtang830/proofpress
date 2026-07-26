[//]: # (ob:d16948ea)
# Proofpress documentation

[//]: # (ob:aeed01a6)
Proofpress is the trust layer for multiplayer AI: an open, agent-native ledger
that travels with the artifact. The public documentation set stays deliberately
small and describes behavior that users and compatible implementations can rely
on.

[//]: # (ob:c6e0b8d1)
“Think C2PA, but for knowledge work” is a category analogy, not a claim of C2PA
compatibility, signed authorship, or complete capture.

[//]: # (ob:717c12e2)
- [Portable handoff demo](../examples/portable-handoff/) provides a neutral

[//]: # (ob:c2dd735b)
  artifact whose embedded v1 → v2 ledger can be inspected, imported, and
  verified in a clean receiver repository.

[//]: # (ob:62ae0597)
- [Portable Artifact V0](PORTABLE_ARTIFACT_SPEC.md) is the executable protocol

[//]: # (ob:12d546c8)
  contract: policy, identity, carrier, actors, integrity, import, and commands.

[//]: # (ob:115b73d9)
- [Privacy Boundaries](PRIVACY_AND_DISCLOSURE.md) defines what admitted history

[//]: # (ob:18d76a56)
  may contain, what stays local, and what a distributed file cannot promise.

[//]: # (ob:08d1b5c2)
The implementation is the zero-dependency [`proofpress.py`](../proofpress.py)
CLI. Harness installation and attribution rules are documented under
[`skills/`](../skills/).

[//]: # (ob:aef7f16a)
Product strategy, competitive research, launch drafts, and experiments are not
normative protocol documentation and are intentionally excluded from the public
repository tree.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzRlNTAxMDZkY2JmYWQxOGUzYWIwNjY4YyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImFjYjA5NzhmIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85ZmI2YmY1YjEzMGNhNGJiNzc3ZTg0MTAiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzdhNjNlNWExMzE2YWQ5OTljNDM3MTIzZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNqtV9tu20gS_ZUG9yXByFbzTulN43iwBrIbw_EGGNgG05ei2GvetpuUrTUCzNN-wD7v_Fy-ZKpJUZInWQGxDBiw2OyuPnXqdvjkMN2qjIk2VdKZO02TBhBSl0ZS8IxJNwGfcRpFiXAmDq_lOpVqCabFvSZnXhjNgyALYi5nrgfSjwS4PoTgez6L4yCjM1-6QTILqUd9l9Ig89BWEDKPhWIm3dgL0K5URtQr0Gtn_mQf2rRlS7yhgscWXxeMQ4GPn0CrTDFeANGwUkbVFclxd63XhK_Jpa7rrNFgDJ5pmLhnS7AuPVvW9T8Bne20NZi3bWPm0-lStXnHT0VdTkUOVamqZcuqZeLT6bPTGv7VKfyddgZ0KurKQIVMtLqDLxMnB2YpZILTWZxkzrCSwqrfhNRCOst4xLOQuz4VLOA8jmNIApdaZLVurWtpoSpA5GM8ijRmEVLKXN-NmJzNZiLwY9fz5eDOBl0qWGO6Ah32LE5Ra2mc-c2Ts7n-CXEhUcb-Gl6DTDkSfuOIWsKjc4cejLmAF8tamOnV-eLd385PS3vVj-QJa1uteNdigFLOjDKWa6YrixPfYfpAb7Jr81pbRPeqslbNGt-U-KZipQ3dgGziGDyItpx51RUF4hQ5RgcG_3hRi3sL2I1mQQIMt2NgWps5c2eXEgQd6kqkgllUuGlzJZMSBiYxo-ABV_5CDpxq140FZgOLSeJ8mewAMABJXRYdDWDvjDKkzYFggpmWFGwNmmS1JmVXtKoZnhcXc8IqUjdQTQjbQWyYZs_wiQgoT6R7NL6vv_3vOlfVPTnzLhcTgnHuQd1X9UMBcgnkodb3X3_73aJnRLAWlrZCWcWKermekAMYYzcW2Ee8ozGekJvLTUERTBZZZxmRUNZ3b05Pp_DIyqYAMx1r7mSzZfqWYEXt8BXYXJ5z6EkZ-yE_Gh8hYz2Rh7w2QKDkYHeRlUu-_ue_ZOWRnkyNBFaEA1GVabBzgZwQdYDByGNAw1n8qgwuRqyf6N2byw9X14uf35-ni6vri18WZ9fpx8vzM2wSb8d0hQMMup4Mg0gkr8CgPa8R1Zw0daEEZpaSeFK1-EswrRVorIi-6-ErvGup-3eqPMCf64Y89uXsVfjTasXEmvxcd5VkiMcge1cXnxZnv6aLv79L3118PHv_4eM_rs579iRk2PoNJsQh_hIZRyyMXoG_kq17DpnCzvGQs5aYlq0NwZtYgcxVclhlxI7kvqFjfmaqgAP8UewwPBTHV_A1JpKyZbrdPabXv0HXJxKw4WG4kd6bz7sxeNqsP9-9OYCPQRZnOEhfo0vLTljOtO1wNufqsgFMP7Wy-sQA0yKfYNfuKpETqVnWmoHVb_i7m4xj2kEVZEddKjSwYUr2b8ape1BCVHXb2xzLdqMkCGoacd_UWAK9MNL9TXaUjk92kt5ZCWLLaM_CvizZM9ILnhcqFlNnbYp5jp2t0WojjAx355TGEATgusJzkxjCiDEqaSD9WUR9zhJcAB5HQiYzjnIT1SMwHgtKIYiSkNmWjOnb9gJniNbcdVEr2BXHo150QuMTL7qm8Tzw5178E6V4J57aML6v3L7srT69mirqU3AQLTkzuS0WkYXgxiEVgR3LvY09HbPJzh8VJKPxxA28kPLMc-PR-J5G-Tb1f1hsLBHHScX6hB-G1W3V2o6BJbGCAjsZ6ure5kjTKbFl3XQcE-25K8TA2H8kFIqDrapifVuZkhVFXzYSjMAuhB2SQ85WCrH1t1kxbvodtgLRms39563D9FNU9wbr6vQ7_WFDGsQRj4HOQi8QI2l7wmlD2rEKCAvVrhdMlaTOeiu31QheFf2UMmpZYbsdNLLJVTMheIXdVECLNc2attNwwBXKfR4ABDwJvdGVPX21ceUYobTCeWsdrKDDiBffmVobKNyfUcl9gV9-yZbVnZTaQDlOE5UWo_2FCG8rQlb9xyIeVlXPNfQJIACTVeOPpjbKfjgeIDAGP-Ey86k74yPqPXn1HQJ_VCc9guiGk8hmW4v6AIcJQIJdFPtJIkc0e2Jqy-HLVZElcDLWUYn_zQFyfJ_GEux3frYlZ0877ZHzUhFklYcsVWtFx-Yr__-zEyQi4xgYCXxbt3tSacvOyzWPzTlbtxipUplDhcfcIMNg0SSJttTsyaINlmP0DZbms6W3t9XZ-4tT8tfhG9vWRYtdc7Bqfdr7ICe6K2zVatg2YPQQY2O7981nc6-KwkyHSzYPbw84y4XHcUpzCb7cTZmtxtpNmReLpccGK9nCHEBjDG4xELoc5s5YOH-aJr3TGvoEr-wK0rFGW6LobEPJMIg918Mouq12DQGHF3wb3bsv-PcHi5Jp-A)
