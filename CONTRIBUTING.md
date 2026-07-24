# Contributing to Proofpress

Thanks for your interest. Proofpress is small on purpose; these notes keep it
that way.

## Development setup

Python 3 and Git are the only requirements for the engine. Node 18+ is needed
only for the npm launcher tests.

```sh
git clone https://github.com/chenmingtang830/proofpress.git
cd proofpress
python3 -m unittest discover -s tests -v
node --test tests/npm.test.js
```

## Architecture constraint: one file, zero dependencies

`proofpress.py` is a single Python file with no third-party runtime
dependencies. This is the distribution model, not an accident: recipients
verify handoffs on machines that have nothing but `python3` and `git`, and
skills vendor the file directly. Please do not split it into packages or add
runtime dependencies. Internal section structure (carriers → blocks → diff →
ledger → commands) keeps it navigable.

## Scope boundaries

- Proofpress versions **Markdown and static HTML knowledge artifacts**. It
  never versions source code — that is Git's job, and features that drift
  toward code files will be declined.
- The executable contract is [docs/PORTABLE_ARTIFACT_SPEC.md](docs/PORTABLE_ARTIFACT_SPEC.md).
  Behavior changes must keep the spec in sync (same PR).
- Privacy invariants live in [docs/PRIVACY_AND_DISCLOSURE.md](docs/PRIVACY_AND_DISCLOSURE.md);
  changes that would leak local-only history are not accepted.

## Wording discipline

Proofpress is **tamper-evident**, not tamper-proof. Public-facing text
(README, spec, CLI output) says *checkable record*, *tamper-evident*,
*provenance that travels* — never *immutable*, *tamperproof*, *notarized*, or
*can't be faked*. PRs that cross this line will be asked to reword.

## Docs are dogfooded

Markdown documents in this repo are Proofpress-managed (see
[AGENTS.md](AGENTS.md)). If your PR meaningfully revises a managed document,
close the loop: `python3 proofpress.py snapshot <file>` with honest actor
attribution, and sync the ledger (`python3 proofpress.py sync`) so the
revision history travels with the repo.

## Pull requests

- Include tests for behavior changes (`tests/test_portable.py` is black-box
  through the CLI; follow its style).
- Keep commits focused; explain the *why* in the message body.
- CI must pass; the full suite runs in seconds.
