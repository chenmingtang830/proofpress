#!/usr/bin/env python3
"""Build the portable trusted-knowledge-graph demo from the real MVP fixture.

The browser artifact contains no fetches or CDN dependencies, so it can be
opened directly. Its embedded model is projected from the same OTLP fixture
and deterministic claim/gate logic used by ``proofpress knowledge``.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

import proofpress_knowledge as knowledge  # noqa: E402


TEMPLATE = HERE / "explorer.template.html"
OUTPUT = HERE / "demo.partner-style.html"
FIXTURE = HERE / "demo.otlp.json"
MARKER = "/*__PROOFPRESS_LEDGER__*/"


def demo_ledger() -> dict:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    sources = [knowledge._source_event(span) for span in knowledge._spans(payload)]
    experiments = knowledge._experiments(sources)
    claims = knowledge._claims(experiments)

    # The demo begins with one reviewed baseline. This is deliberate fixture
    # state, not an automatic admission rule; candidate-b remains reviewable.
    baseline = next(claim for claim in claims if claim["experiment_ref"] == "exp-001")
    baseline["status"] = "admitted"
    baseline["admitted_by"] = "human:demo"
    review = {
        "id": "rev_demo_baseline",
        "claim_ref": baseline["id"],
        "decision": "accept",
        "reviewer": "human:demo",
        "note": "Baseline is a reviewed reference for this explorer fixture.",
    }
    admission = {
        "claim_ref": baseline["id"],
        "status": "admitted",
        "review_ref": review["id"],
        "evidence_refs": baseline["evidence_refs"],
        "policy": baseline["gate"]["policy"],
    }
    return {
        "schema_version": knowledge.SCHEMA,
        "fixture": True,
        "source_events": sources,
        "experiments": experiments,
        "claims": claims,
        "reviews": [review],
        "admissions": [admission],
    }


def build() -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    if template.count(MARKER) != 1:
        raise ValueError(f"expected exactly one {MARKER!r} marker")
    payload = json.dumps(demo_ledger(), ensure_ascii=False, separators=(",", ":"))
    rendered = template.replace(MARKER, f"window.__PP_LEDGER__={payload};")
    # renderGraph replaces the initial SVG element; retain the lookup ID on
    # that generated element so its node listeners and view controls bind.
    rendered = rendered.replace('<svg viewBox="0 0 ${WIDTH}', '<svg id="graph" viewBox="0 0 ${WIDTH}')
    rendered = rendered.replace('<p class="side-note">', '<p class="side-note" data-proofpress-id="0ff4b2b6">')
    if "__PROOFPRESS_LEDGER__" in rendered:
        raise ValueError("ledger marker remained after build")
    return rendered


def without_proofpress_envelope(page: str) -> str:
    """Ignore the version envelope added after this deterministic build."""
    page = re.sub(r'<meta name="proofpress:(?:meta|discovery)"[^>]*>\s*', "", page)
    return re.sub(
        r'<script type="application/vnd\.proofpress\+json" data-proofpress="capsule">.*?</script>\s*',
        "",
        page,
        flags=re.DOTALL,
    )


def main() -> None:
    rendered = build()
    if "--check" in sys.argv:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if without_proofpress_envelope(current) != without_proofpress_envelope(rendered):
            raise SystemExit("explorer build is stale; run build_explorer.py")
        print("explorer build is current")
        return
    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({len(rendered):,} bytes)")


if __name__ == "__main__":
    main()
