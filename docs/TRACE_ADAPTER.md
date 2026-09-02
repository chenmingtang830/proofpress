[//]: # (ob:76e26c8c)
# TRACE decision-provenance adapter

[//]: # (ob:5c8c28d6)
## Boundary

[//]: # (ob:0813cb3c)
Proofpress imports a pinned TRACE v0.5.0 session JSON document as external
decision-provenance evidence. The adapter is pinned to upstream release
`v0.5.0` / schema commit `6260cfe7089815763667d8cc869673a40ca570e0`
(`sha256:10459fb5e334889b17f9abae36de175490558f300077ba5273d2764f2cb58463`
for `trace-v0.5.json`). TRACE remains the producer of the run record;
Proofpress remains the authority for claim admission and governed context.

[//]: # (ob:d6858175)
## Import

[//]: # (ob:2e7206c4)
```sh
proofpress evidence import session.trace.json
```

[//]: # (ob:cfce713f)
The import appends one source event and one evidence receipt for each TRACE
event. Repeating the same session is idempotent. Reusing a session/event
identity with changed normalized content fails closed as an immutable source
conflict.

[//]: # (ob:b20ac71e)
## Data minimization

[//]: # (ob:081f8f23)
The adapter retains session/event identities, TRACE schema version, project
handle, timestamp, actor handle, decision disposition and revision links,
annotation/contribution metadata, and safe tool-call metadata such as server,
name, status, duration, host, and output hash.

[//]: # (ob:e1c0f001)
## Optional decision confidence

[//]: # (ob:e1c0f002)
TRACE v0.5 permits additive decision fields. When a `decision.confidence`
object is present, Proofpress imports only its interval (`lower`, `upper`, and
optional `level`), method name plus optional resample count, positive sample
size, and named SHA-256 evidence digests. The adapter rejects malformed bounds,
methods, sample sizes, or digests; it does not read the result files, rerun the
method, or infer a decision from the interval.

[//]: # (ob:5af5e369)
It excludes tool inputs and outputs, raw prompts, transcripts, reasoning
summaries, state-change values, and learning-store recall data.

[//]: # (ob:eeca4c21)
## Admission boundary

[//]: # (ob:61d2b42e)
A TRACE decision disposition such as `accepted`, `revised`, or `rejected` is
an external workflow record. It is not a Proofpress claim state. TRACE import
creates no claim and no admission; an agent must explicitly propose a claim
from the imported evidence, which then independently passes deterministic
checks, configured policy, and human review.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2M2MDJhN2ExODRhNDAzOTZkMGRiMjA5OSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImViYmNmN2RiIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8zZmYxNWZmNzIxOWQzOThkMjFmMWU0YzYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzFmMGQ3MWIwMTAxOTdiYzBjOWZkNDViZiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWUtz20YS_itTzCWppajB4E2ftJtUrfewcdmuzSF0kYN5iIjwCgaQTKtclf-w_3B_yXYPAAKUaerlQyqlk0Bgpt_dX3frdsbrJtVcNOtUzpazqlqLgDIecifyuEfdOJBUJozG8Ww-S0q5W8v0UpkGzpotZ36wjEIah6EX6FhQoVyPMUq1lIGKXJ8znnAecI8LQSULHBWrUKhEBJErfcYCLTXQlakR5bWqd7PlLf5o1g2_BA4Zb5DVHB4SlcGL_6g61SlPMkVqdZ2atCzIFs6X9Y4kO_KmLktd1coYuFNxccUvFSp18Louf1OgblsjwW3TVGZ5fn6ZNts2WYgyPxdbVeRpcdnw4jJy6fnB7Vr93qbwvG6NqteiLIwqwBZN3arP89lWcTSiShKhQ5nMujdrdW0PgXHV2tXa8bUOmRNLN44kc7SjPBGgZGXdoGrrLC0USD54JFs7msrQSahDnThMwMyxlp6f6E6dXrq14JVpM1CYoZyirKWZLX-9nfXsb2fg5bI2-NR9VnKdgMl_nYlSqo-zD6DBEA3AWJbCnL9_e_GPn9YXP168ef_T20UuZ_NHBQxvmjpN2gb8tE64SQ2Gjcr0mhuwX6MsvbbZljVKdZUWSNLsTKNy-FLwHN3XSTeHiwYdPlsWbZaBrGILHlKdjklWiis4GwaKBSIScByc06iPqIlVgkglbMCcgcnAIrwQinDJq0bVcLrnzaW0QlUYXuoG3nxHHnK92VUoKrobQmf2eT6K5IM4LJLBgUh_L9tCcgj4U5y_I5NjJzjQyHFF4opHcxjzhaQ5hp8hvFf3mi7c__3xX_jjk97w5F_vfv43gbBocwgowkehKl7zA4lkEPmRE_oHEr22LO7ReH_ohL5MhYwGwnsk9c1mY7arYswYAl-kQkd22g-KLpqaC7X4zZTFqoBbozQYigeiCC1U6Lj6kaK83-55cqgKhTSkLBQxZVuDNDZhCS-kfbkXEpJWpVVzwuyQdlyEjjqQ5kfecAIFLc3TTxwz8R4PHDt_Ovh0pJn7dJ5ojD6TQMeGp4UZPHHemQIN0KRNqsy8D08DVTrn5PqEMXyufeUG8dMFe90Q9VFkrVSGNGWZkbSoWswR9Ezb4POc1PyGQEjlFf6AwCmMqE97SSnBPcGcA8EuZJ52WZY8rDQcvXDCT4EjWeIx9QyuF3dKIQGorkqToh2JacWWcEM2APUKfCk3c7KxIG0f79rjw3zApRkAP1Jbi1rxDhLslwFf1Fp7ju8lMXYMAYsV91mYaN_ia1E2lmYPnaSHTgLhIa6qMi0a2wnUlhPixvALYeMDYm6Wit2EwhSHJ0Qswj8Rok2pm7UGf6i6qtO-EzCJs6TSCTinFACT-tAL-CIGRaNAytDzteSeGwlXOR60UH7ElOs6MXOcJGEaoJYLS7vhjUX0zltLxwFgxDczRllwRqMzFrxndOnFSzf-G6VLSuFWb3E45TgOh3IaQ6iMb2-_dRtgY7AD6i03W4zG2OPMESzwOcKWpTHB7j48n4y9PRdfKQ19qatcygcuEzgeuNyHsz01yVzu-Z6E9k0N1CbQ21N7HqYCJn0ErQqerYpjWg9gsOhJ1lAFsV42UEPhmGwFFNFS2991W5Cu0Xu1KiZiTe90zVfa7IguayIynuZg2aEoYKG7xMa8UJL0VWNxpLL1BgJbB4FSMYQ0Gww06QRGc58C-Z6WcpUfxDBg-DwZaE1wv6f1LSG9Z-wEjvZ8EYbS9wfGE5QfWspnALg1teJQLq0PV4U9viBvVQUFEOxgPWOg-d1HSWoQA4Ff059sDZ7jhzi5Knqg3JEbmGdI1yBLUpR1zrP00-BEkE3zNDPg7xKqM0YdBx553nZFtNNiVcBhDeXxlMuhLkdBAHUKCvNgrUkXMrr8gV1FTxYyFqZKJ4lhUJqk2tBoTJzw1Mahq3Vz0o-DqwJsJTMFEJ7mMHPyvJoTOy-R4cNR1EMf7ydRAIUrM19BpgIsWSXP0d7DBERykFGCHeb2muFa2bbiTPAs23_cAykMSCAlkMMxaE6w0reghmxrS3pOtqVp5pNmhKDxTvjKA1zhTIbCk3RfDccmaWhen9H04BfFIcfAnavCtHnOa2t7FF6ddfFIrnnW4kukmCle4-kznOFthqAt0A6n6oyIfI8KrRmXgyKTpmoMuof2SD1dDkGcREBWyn3qT9qmoWd6RhcE4QS_MODgJ2Q1xsq-4pObsr7SWXnTV-0FAV9A5kMwQaZPCnhXpq1NBxzoahGkrO2h8M5QzAvM_7Gmv8JUh84FkiNvDfq6ghRPm2yHDgU9IKW6q6tCg4dtLeqoQ6UYStmc3GxT0BQ-QuEApMISCDSRCo72BqwDSmG-myYVIBe2UuBzLCnpZVsDra716sJg2-a8IF2j-YXjP3xGHx3ZYiiZNvsdhtVp2W8y7F4EwfArX-_sP774-jsE6Egadz3LGvTltcSt0J9mU2LNNi5K2uKqKG-KB65KHrg1yEuZ6tTy_-pA4wiqKT0caH6uUBeI6n2eWN_b8LlntLnn6okhp5eEfRNJ9k2bTyqMZSyCEkIuvVYjKTBNJs2C_IKZwMmm_3Bk3LFJ9VUXfGntfrR5M7RqnTgD3jVl37_ZHLBSLuiAbrWCuoqZDKnVrWsXX3PYHe17pq8BtWz-dKzLuxY8Gy1oy1dhbWGgrmGv9TWXHOf1rrEVC_nYKg3a7OtNZ12rx1CooJoVZ2PbOhT2RWfjwem3s5vtrrPexHj7Tmxixd5y1lRDGz6V5ZjKfdOAOmOjBbBILgEEbe826Z4HIdEgD592T2yIO4tNx9jpCDcdbW9fUv5PkPIP32PcnePZfPTC0vl8fGS_b3_xTZYU2qNBHLpcJCIJoSsXURArFkVBQlkcwESjfV97iRCe8oXwY9eNfSdiMZcuo0KJhyg3WVjEZ5S9Z87SYUufHVlY7P-38rKwuH9hkXhOwqmOuE4eubCo0gJn_jEfEFyevbKYzGvQ1_Y8oAa3lWmgHOYDcMGI3vHckPMB00SZQz6STcACaP1VSKM4cvwwcIMglJHAsAwgTGEu4H5IFd2siu83_b8oHer5sU5g0nG9KIoTJ9QxTzgMPlI5oe_F1Pcj7VJKwzDBtHQlCwNPM5H4kRe4QAtn9o1dIpxZ0XCTsPnhZQ3zsoZ5WcO8rGEes4aJ3YQCfEcscML99mJsp0ZfPb4nGvYYwmES8l1F4x5j0iYd_Ff8ab1OsRhFgeJYJug8W9Mh-8HXc3IEVcoi2xFkA-0FGBUU-36TlTeqxh1JC-mLD2BHoDdovskggLLND3P0y7aEHMJ0rLLWjDMJ8IAwgXwRgInAuQuKa5u68HoFs8kn1TkIb0vy7p8XZ4AKY0HoRiRzCFDdmsYQSFkoFHjPTgQYWJ0suNbqGCMDY5c7PaVXoCYgpOp2N4BsskMCZdoMkj7NlN2UITLA-4GgpZAWGpjziQf2S5jeai8bvpcN319vw_fh8_8BnnzgJQ)
