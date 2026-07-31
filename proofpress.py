#!/usr/bin/env python3
"""proofpress — verifiable version ledger for Markdown and static HTML knowledge artifacts.

The Git ledger stores local history on refs/proofpress/ledger. A portable
artifact additionally carries a compact, path-independent capsule inside the
carrier file, so admitted versions and decision context can survive handoff.

Commands:
  snapshot <file> [--author] [--kind agent|human|system] [--session] [--note]
                  [--claims claims.json] [--why TEXT] [--rejected TEXT]...
  log <file> [--json]
  diff <file> [<vA> <vB>] [--json]
  show <file-or-version> [--json]
  verify <file> [<version>] [--json]     claim check: exit 0 ✓ / 1 ⚠ / 2 no claims
  ingest <file>                          backfill ledger versions from Git history
  merge-plan <file> --from copy.md [...]        analyze parallel portable copies
  merge <file> --from copy.md [...]             record a multi-parent document merge
  merge-lineage <file> --from a.md --from b.md  record other documents as ingredients
  identify <file>                        recover identity after capsule stripping
  provenance create|verify               format-aware evidence for any file type
  policy / inspect / import / clean / capture
  anchor / blocks / init / sync
"""

import argparse, base64, difflib, hashlib, html, json, os, re, secrets, subprocess, sys, tempfile, zlib
from datetime import datetime, timezone
import proofpress_evidence

__version__ = "0.2.0"
LEDGER_REF = "refs/proofpress/ledger"

# ---------- terminal rendering ----------
# Dark-theme palette from docs/internal/DESIGN.md, emitted as 24-bit truecolor
# so the film, terminal, and future UI share one semantic system:
# accent = edit/modified, add = verified/added, del = rejected/removed,
# move = why/moved.
# Non-tty / NO_COLOR output stays plain text, so piped (agent) consumption is
# identical to the historical format.

TERM_HEX = {"accent": "5FB3C4", "add": "6FBF8E", "del": "C87E82",
            "move": "D7B56D", "dim": "787B87"}


def _color_on():
    return sys.stdout.isatty() and "NO_COLOR" not in os.environ


def C(role, s, bold=False, strike=False):
    """Wrap `s` in the palette color for `role` when writing to a tty."""
    if not _color_on():
        return str(s)
    codes = []
    h = TERM_HEX.get(role)
    if h:
        codes.append(f"38;2;{int(h[0:2], 16)};{int(h[2:4], 16)};{int(h[4:6], 16)}")
    if bold:
        codes.append("1")
    if strike:
        codes.append("9")
    if not codes:
        return str(s)
    return f"\x1b[{';'.join(codes)}m{s}\x1b[0m"


def B(s):
    return f"\x1b[1m{s}\x1b[0m" if _color_on() else str(s)


KIND_GLYPH = {"added": ("add", "+"), "removed": ("del", "−"),
              "modified": ("accent", "●"), "moved": ("move", "⇄")}


def stats_text(stats):
    if not stats:
        return "initial snapshot", "dim"
    order = ["modified", "added", "removed", "moved"]
    parts = [f"{KIND_GLYPH[k][1]} {k} {stats[k]}" for k in order if k in stats]
    color = next(KIND_GLYPH[k][0] for k in order if k in stats)
    return "  ".join(parts), color


def stats_summary(stats):
    order = ["modified", "added", "removed", "moved"]
    kinds = [k for k in order if k in stats]
    if len(kinds) == 1:
        k, n = kinds[0], stats[kinds[0]]
        return f"{n} block{'s' if n > 1 else ''} {k}"
    return ", ".join(f"{stats[k]} {k}" for k in kinds)


_MD_BOLD = re.compile(r"\*\*(.+?)\*\*")
_MD_CODE = re.compile(r"`([^`]+)`")


def md_term(s):
    """Minimal inline markdown → ANSI for terminal reading (bold, code).
    Plain text passes through untouched when color is off, so piped output
    keeps the raw markdown."""
    if not _color_on():
        return s
    s = _MD_BOLD.sub(lambda m: B(m.group(1)), s)
    s = _MD_CODE.sub(lambda m: C("accent", m.group(1)), s)
    return s


def git(*args, input=None):
    r = subprocess.run(["git", *args], capture_output=True, text=True, input=input)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


# ---------- carriers → block tree ----------

# Canonical anchor form is a markdown link-reference-definition comment,
# invisible in every CommonMark renderer (GitHub, Claude preview, etc.).
# The legacy HTML-comment form is still accepted on parse.
ANCHOR = re.compile(
    r"^\s*(?:\[//\]: # \(ob:([0-9a-f]{8})\)|<!-- ob:([0-9a-f]{8}) -->)\s*$"
)

PP_META = re.compile(r"^\s*\[//\]: # \(proofpress:meta:([A-Za-z0-9_-]+)\)\s*$")
PP_CAPSULE = re.compile(r"^\s*\[//\]: # \(proofpress:capsule:([A-Za-z0-9_-]+)\)\s*$")
PP_DISCOVERY = re.compile(r"^\s*\[//\]: # \(proofpress:discovery:(.*?)\)\s*$")
HTML_META = re.compile(
    r'<meta\s+name=["\']proofpress:meta["\']\s+content=["\']([A-Za-z0-9_-]+)["\']\s*/?>',
    re.I)
HTML_DISCOVERY = re.compile(
    r'<meta\s+name=["\']proofpress:discovery["\']\s+content=["\']([^"\']*)["\']\s*/?>',
    re.I)
HTML_CAPSULE = re.compile(
    r'<script\s+type=["\']application/vnd\.proofpress\+json["\']\s+'
    r'data-proofpress=["\']capsule["\']\s*>([A-Za-z0-9_-]+)</script>', re.I)
HTML_BLOCK_START = re.compile(r"(?is)<(h[1-6]|p|li|pre|blockquote|td|th|figcaption)\b[^>]*>")
HTML_ANCHOR_ATTR = re.compile(
    r"\s+data-proofpress-id\s*=\s*(?:\"([0-9a-f]{8})\"|'([0-9a-f]{8})'|([0-9a-f]{8}))",
    re.I)
HTML_VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                  "link", "meta", "param", "source", "track", "wbr"}
POLICIES = ("ignored", "local", "portable")
ATTRIBUTION_BASES = ("signed", "environment_attested", "harness_attested",
                     "self_asserted", "unknown")
DISCOVERY_LABEL = "Verifiable revision history by Proofpress"
DISCOVERY_URL = "https://github.com/chenmingtang830/proofpress"
DISCOVERY_TEXT = f"{DISCOVERY_LABEL} | {DISCOVERY_URL}"
CAPSULE_DISCOVERY = {
    "label": DISCOVERY_LABEL,
    "project_url": DISCOVERY_URL,
    "package": "proofpress",
    "dist_tag": "latest",
    "requires_user_consent": True,
}
LEGACY_CAPSULE_DISCOVERIES = ({
    **CAPSULE_DISCOVERY,
    "dist_tag": "next",
},)


def valid_capsule_discovery(discovery):
    """Accept canonical discovery plus exact historical Proofpress values."""
    return (discovery == CAPSULE_DISCOVERY or
            discovery in LEGACY_CAPSULE_DISCOVERIES)


def _b64e(data):
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _b64d(value):
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def encode_meta(meta):
    raw = json.dumps(meta, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode()
    return _b64e(raw)


def decode_meta(value):
    return json.loads(_b64d(value))


def encode_capsule(capsule):
    raw = json.dumps(capsule, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode()
    return _b64e(zlib.compress(raw, 9))


def decode_capsule(value):
    return json.loads(zlib.decompress(_b64d(value)))


def carrier_for_path(path):
    return "html" if os.path.splitext(path)[1].lower() in (".html", ".htm") else "markdown"


def split_markdown_transport(text):
    """Return visible projection, metadata, capsule, and decode errors.

    Proofpress transport markers are excluded without touching block anchors.
    Duplicate markers are invalid because ambiguity is unsafe.
    """
    visible, metas, capsules, discoveries = [], [], [], []
    fence = None
    for line in text.splitlines():
        fm = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fm:
            marker = fm.group(1)
            if fence is None:
                fence = (marker[0], len(marker))
            elif marker[0] == fence[0] and len(marker) >= fence[1]:
                fence = None
            visible.append(line)
            continue
        if fence is not None:
            visible.append(line)
            continue
        mm, cm, dm = PP_META.match(line), PP_CAPSULE.match(line), PP_DISCOVERY.match(line)
        if mm:
            metas.append(mm.group(1)); continue
        if cm:
            capsules.append(cm.group(1)); continue
        if dm:
            discoveries.append(dm.group(1)); continue
        visible.append(line)
    errors, meta, capsule = [], None, None
    if len(metas) > 1:
        errors.append("duplicate_meta")
    if len(capsules) > 1:
        errors.append("duplicate_capsule")
    if len(discoveries) > 1:
        errors.append("duplicate_discovery")
    if discoveries and discoveries[-1] != DISCOVERY_TEXT:
        errors.append("invalid_discovery")
    if discoveries and not capsules:
        errors.append("discovery_without_capsule")
    if metas:
        try:
            meta = decode_meta(metas[-1])
        except Exception:
            errors.append("invalid_meta")
    if capsules:
        try:
            capsule = decode_capsule(capsules[-1])
        except Exception:
            errors.append("invalid_capsule")
    body = "\n".join(visible).rstrip() + "\n"
    return body, meta, capsule, errors


def split_html_transport(text):
    """Return an HTML projection without Proofpress's non-rendering payloads.

    This carrier deliberately recognises only the exact, declarative tags that
    Proofpress writes.  It never interprets a script as instructions.
    """
    metas = HTML_META.findall(text)
    capsules = HTML_CAPSULE.findall(text)
    discoveries = HTML_DISCOVERY.findall(text)
    errors, meta, capsule = [], None, None
    if len(metas) > 1:
        errors.append("duplicate_meta")
    if len(capsules) > 1:
        errors.append("duplicate_capsule")
    if len(discoveries) > 1:
        errors.append("duplicate_discovery")
    if discoveries and discoveries[-1] != DISCOVERY_TEXT:
        errors.append("invalid_discovery")
    if discoveries and not capsules:
        errors.append("discovery_without_capsule")
    if metas:
        try:
            meta = decode_meta(metas[-1])
        except Exception:
            errors.append("invalid_meta")
    if capsules:
        try:
            capsule = decode_capsule(capsules[-1])
        except Exception:
            errors.append("invalid_capsule")
    # Transport tags may occupy their own lines. Trim only carrier-edge
    # whitespace so repeated read/write cycles do not accumulate blank lines.
    body = HTML_META.sub(
        "", HTML_DISCOVERY.sub("", HTML_CAPSULE.sub("", text))).strip() + "\n"
    return body, meta, capsule, errors


def split_transport(text, carrier="markdown"):
    return split_html_transport(text) if carrier == "html" else split_markdown_transport(text)


def new_meta(policy="local"):
    return {"proofpress": 1, "artifact_id": "pp_" + secrets.token_hex(12),
            "policy": policy}


def read_artifact(path, create_meta=False):
    raw = open(path).read()
    body, meta, capsule, errors = split_transport(raw, carrier_for_path(path))
    if meta is None and create_meta and "invalid_meta" not in errors:
        meta = new_meta()
    if meta is not None:
        if meta.get("policy") not in POLICIES:
            errors.append("invalid_policy")
        if not meta.get("artifact_id"):
            errors.append("missing_artifact_id")
    return body, meta, capsule, errors


def atomic_write(path, text):
    directory = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(prefix=".proofpress-", dir=directory, text=True)
    try:
        with os.fdopen(fd, "w") as f:
            f.write(text)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise


def write_html_artifact(path, body, meta=None, capsule=None):
    """Embed transport data without rendering it or executing it in a browser."""
    out = body.rstrip() + "\n"
    if meta is not None:
        marker = f'<meta name="proofpress:meta" content="{encode_meta(meta)}">'
        if re.search(r"</head\s*>", out, re.I):
            out = re.sub(r"</head\s*>", marker + "\n</head>", out, count=1, flags=re.I)
        else:
            out = marker + "\n" + out
    if capsule is not None:
        discovery = f'<meta name="proofpress:discovery" content="{DISCOVERY_TEXT}">'
        if re.search(r"</head\s*>", out, re.I):
            out = re.sub(r"</head\s*>", discovery + "\n</head>", out,
                         count=1, flags=re.I)
        else:
            out = discovery + "\n" + out
        marker = ('<script type="application/vnd.proofpress+json" '
                  f'data-proofpress="capsule">{encode_capsule(capsule)}</script>')
        if re.search(r"</body\s*>", out, re.I):
            out = re.sub(r"</body\s*>", marker + "\n</body>", out, count=1, flags=re.I)
        else:
            out = out.rstrip() + "\n" + marker + "\n"
    atomic_write(path, out)


def write_artifact(path, body, meta=None, capsule=None):
    if carrier_for_path(path) == "html":
        write_html_artifact(path, body, meta, capsule)
        return
    out = body.rstrip() + "\n"
    markers = []
    if meta is not None:
        markers.append(f"[//]: # (proofpress:meta:{encode_meta(meta)})")
    if capsule is not None:
        markers.append(f"[//]: # (proofpress:discovery:{DISCOVERY_TEXT})")
        markers.append(f"[//]: # (proofpress:capsule:{encode_capsule(capsule)})")
    if markers:
        out = out.rstrip() + "\n\n" + "\n".join(markers) + "\n"
    atomic_write(path, out)


def format_anchor(block_id):
    return f"[//]: # (ob:{block_id})"


def is_leading_yaml_frontmatter(block, index):
    """True when block is YAML frontmatter that must remain at byte zero.

    Agent-skill loaders require the opening `---` to be the first line. The
    frontmatter still participates in the ledger and inherits identity by
    exact hash/similarity; only its serialized anchor is omitted.
    """
    if index != 0 or block.get("type") != "para":
        return False
    lines = block.get("text", "").splitlines()
    return len(lines) >= 2 and lines[0].strip() == "---" and lines[-1].strip() == "---"


def _html_block_type(tag):
    if tag.startswith("h") and len(tag) == 2 and tag[1].isdigit():
        return "heading"
    if tag == "li":
        return "list"
    if tag == "pre":
        return "code"
    if tag in ("td", "th"):
        return "table"
    return "para"


def parse_html_blocks(text):
    """Extract stable, leaf-level blocks from a static HTML document.

    The persisted text is the outer HTML of each block, with Proofpress's own
    identity attribute removed.  Thus anchors never affect digests or diffs.
    Containers (div/section/article) intentionally are not blocks: their
    semantic children remain independently movable and reviewable.
    """
    text, _, _, _ = split_html_transport(text)
    blocks, active, order, raw_text_tag = [], [], 0, None
    token = re.compile(r"(?is)<!--.*?-->|<![^>]*>|</?[A-Za-z][^>]*>|[^<]+")
    for match in token.finditer(text):
        raw = match.group(0)
        start = re.match(r"(?is)<([A-Za-z][\w:-]*)\b[^>]*>", raw)
        end = re.match(r"(?is)</\s*([A-Za-z][\w:-]*)\s*>", raw)
        if raw_text_tag:
            if end and end.group(1).lower() == raw_text_tag:
                raw_text_tag = None
            continue
        if start and start.group(1).lower() in ("script", "style"):
            raw_text_tag = start.group(1).lower()
            continue
        for block in active:
            block["parts"].append(raw)
            if start and start.group(1).lower() not in HTML_VOID_TAGS:
                block["depth"] += 1
            elif end:
                block["depth"] -= 1
        if start:
            tag = start.group(1).lower()
            if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "pre", "blockquote", "td", "th", "figcaption"):
                am = HTML_ANCHOR_ATTR.search(raw)
                clean = HTML_ANCHOR_ATTR.sub("", raw)
                order += 1
                active.append({"tag": tag, "depth": 1, "parts": [clean],
                               "anchor": (am.group(1) or am.group(2) or am.group(3)) if am else None,
                               "order": order})
        if end:
            completed = [b for b in active if b["depth"] == 0]
            active = [b for b in active if b["depth"] != 0]
            for block in completed:
                value = "".join(block["parts"]).strip()
                if value:
                    item = {"type": _html_block_type(block["tag"]), "text": value}
                    if block["anchor"]:
                        item["anchor"] = block["anchor"]
                    blocks.append((block["order"], item))
    return [item for _, item in sorted(blocks)]


def parse_blocks(text, carrier="markdown"):
    """Coarse block parser: heading / code / table / list / para.
    Anchor lines ([//]: # (ob:xxxxxxxx), legacy <!-- ob:xxxxxxxx -->) attach identity to the NEXT block
    and are excluded from block text (so they never affect hashing)."""
    if carrier == "html":
        return parse_html_blocks(text)
    text, _, _, _ = split_markdown_transport(text)
    lines = text.splitlines()
    blocks, cur, kind = [], [], None
    pending_anchor = None

    def emit(block):
        nonlocal pending_anchor
        if pending_anchor:
            block["anchor"] = pending_anchor
            pending_anchor = None
        blocks.append(block)

    def flush():
        nonlocal cur, kind
        if cur:
            body = "\n".join(cur).rstrip()
            if body.strip():
                emit({"type": kind or "para", "text": body})
        cur, kind = [], None

    i = 0
    while i < len(lines):
        ln = lines[i]
        if kind == "code":
            cur.append(ln)
            if ln.strip().startswith("```"):
                flush()
            i += 1
            continue
        m = ANCHOR.match(ln)
        if m:
            # Older ``anchor`` releases treated an indented continuation of a
            # Markdown list item as a separate paragraph. They consequently
            # inserted a redundant anchor between the item and its wrapped
            # continuation. Fold that shape back into the list block so one
            # more ``anchor`` pass repairs the source without changing prose.
            if kind == "list":
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if (j < len(lines) and
                        re.match(r"^\s*([-*+]|\d+\.)\s", lines[j])):
                    i = j
                    continue
                if (j < len(lines) and
                        not lines[j].strip().startswith("```") and
                        re.match(r"^\s+\S", lines[j]) and
                        not re.match(r"^\s*([-*+]|\d+\.)\s", lines[j])):
                    i = j
                    continue
            flush(); pending_anchor = m.group(1) or m.group(2); i += 1; continue
        if ln.strip().startswith("```"):
            flush(); kind = "code"; cur = [ln]; i += 1; continue
        if re.match(r"^#{1,6} ", ln):
            flush(); emit({"type": "heading", "text": ln.rstrip()}); i += 1; continue
        if not ln.strip():
            if kind == "list":
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                marker = ANCHOR.match(lines[j]) if j < len(lines) else None
                if marker:
                    j += 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                if (marker and j < len(lines) and
                        re.match(r"^\s*([-*+]|\d+\.)\s", lines[j])):
                    i = j
                    continue
                if (j < len(lines) and
                        not lines[j].strip().startswith("```") and
                        re.match(r"^\s+\S", lines[j]) and
                        not re.match(r"^\s*([-*+]|\d+\.)\s", lines[j])):
                    i = j
                    continue
            flush(); i += 1; continue
        this = "table" if ln.lstrip().startswith("|") else (
            "list" if (re.match(r"^\s*([-*+]|\d+\.)\s", ln) or
                       (kind == "list" and re.match(r"^\s+\S", ln)))
            else "para")
        if kind not in (None, this):
            flush()
        kind = kind or this
        cur.append(ln)
        i += 1
    flush()
    return blocks


def bhash(b):
    return hashlib.sha1((b["type"] + "\0" + b["text"]).encode()).hexdigest()[:12]


def body_digest(version):
    visible = [{"type": b["type"], "text": b["text"]}
               for b in version.get("blocks", [])]
    raw = json.dumps(visible, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def version_id(version):
    """Content ID independent of the projection path."""
    canonical = {"artifact_id": version.get("artifact_id"),
                 "blocks": version.get("blocks", [])}
    return hashlib.sha1(json.dumps(canonical, sort_keys=True,
                                   ensure_ascii=False).encode()).hexdigest()[:8]


# ---------- soft binding (deterministic identity after metadata stripping) ----------

_FP_RAWTEXT = re.compile(r"(?is)<(script|style)\b[^>]*>.*?</\1>")
_FP_TAG = re.compile(r"<[^>]+>")
_FP_MD_LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")


def soft_fingerprint(blocks):
    """Tier-1 exact soft binding: hash of the visible text skeleton.

    Deterministic, model-free. Normalization is deliberately harsh — strip
    HTML tags, markdown link targets and all syntax/punctuation, collapse
    whitespace — so the fingerprint survives formatting drift (plain-text
    copy, re-rendering, whitespace mangling) but flips on any wording
    change. It proves identity ("this is pp_xxx"), never tamper-freedom."""
    text = "\n".join(b["text"] for b in blocks)
    text = _FP_RAWTEXT.sub(" ", text)
    text = _FP_TAG.sub(" ", text)
    text = _FP_MD_LINK.sub(r"\1", text)
    text = html.unescape(text)
    skeleton = " ".join(re.findall(r"[^\W_]+", text))
    return "ppsb1:" + hashlib.sha256(skeleton.encode()).hexdigest()


# ---------- block identity matching (similarity fallback without anchors) ----------

def assign_ids(new_blocks, old_version):
    """Give each new block an id: exact-hash match → inherit; else best
    same-type similarity > 0.6 among unmatched → inherit (modified); else new."""
    old = old_version["blocks"] if old_version else []
    used = set()
    # pass 0: explicit anchors — identity is declared, trust it
    for nb in new_blocks:
        a = nb.pop("anchor", None)
        if a and a not in used:
            nb["id"] = a; used.add(a)
    # pass 1: exact content
    by_hash = {}
    for ob in old:
        by_hash.setdefault(ob["hash"], []).append(ob)
    for nb in new_blocks:
        h = bhash(nb)
        nb["hash"] = h
        if "id" in nb:
            continue
        cands = [ob for ob in by_hash.get(h, []) if ob["id"] not in used]
        if cands:
            nb["id"] = cands[0]["id"]; used.add(nb["id"])
    # pass 2: similarity
    for nb in new_blocks:
        if "id" in nb:
            continue
        best, score = None, 0.0
        for ob in old:
            if ob["id"] in used or ob["type"] != nb["type"]:
                continue
            s = difflib.SequenceMatcher(None, ob["text"], nb["text"]).ratio()
            if s > score:
                best, score = ob, s
        if best and score > 0.6:
            nb["id"] = best["id"]; used.add(nb["id"])
        else:
            nb["id"] = hashlib.sha1(f"{nb['text']}{len(new_blocks)}{datetime.now()}".encode()).hexdigest()[:8]
    return new_blocks


# ---------- semantic diff (structure plus numeric extraction) ----------

# The lookbehind rejects date/range separators ("2026-07-18") and identifier
# digits ("v0", "sha1") — a data number never starts mid-word.
NUM = re.compile(r"(?<![\w-])[+-]?[$€¥]?\d[\d,.]*%?[MKB]?")

_ORDINAL = re.compile(r"(?m)^\s*\d+[.)]\s")


def extract_nums(text):
    """Numbers that are data, not numbering: list ordinals stripped first."""
    return NUM.findall(_ORDINAL.sub("", text))

def heading_context(blocks, idx):
    for j in range(idx, -1, -1):
        if blocks[j]["type"] == "heading":
            return re.sub(r"^#+\s*", "", blocks[j]["text"])[:40]
    # Preserve the legacy wire label used by existing capsule change records.
    return "(\u6587\u9996)"


def lis_ids(seq):
    """ids forming a longest increasing subsequence of old positions."""
    import bisect
    pos = [p for _, p in seq]
    tails, tidx = [], []
    prev = [-1] * len(pos)
    for i, p in enumerate(pos):
        k = bisect.bisect_left(tails, p)
        if k == len(tails):
            tails.append(p); tidx.append(i)
        else:
            tails[k] = p; tidx[k] = i
        prev[i] = tidx[k - 1] if k > 0 else -1
    out, i = set(), tidx[-1] if tidx else -1
    while i != -1:
        out.add(seq[i][0]); i = prev[i]
    return out


def semantic_diff(old_v, new_v):
    old = old_v["blocks"] if old_v else []
    new = new_v["blocks"]
    old_by_id = {b["id"]: (i, b) for i, b in enumerate(old)}
    new_ids = {b["id"] for b in new}
    changes = []
    common = [(b["id"], old_by_id[b["id"]][0]) for b in new if b["id"] in old_by_id]
    stable = lis_ids(common) if common else set()
    for i, nb in enumerate(new):
        ctx = heading_context(new, i)
        if nb["id"] not in old_by_id:
            changes.append({"kind": "added", "block": nb["id"], "type": nb["type"],
                            "context": ctx, "preview": nb["text"][:60]})
            continue
        oi, ob = old_by_id[nb["id"]]
        moved = nb["id"] not in stable
        if ob["hash"] != nb["hash"]:
            nums_o, nums_n = extract_nums(ob["text"]), extract_nums(nb["text"])
            # positional pairing is only meaningful when the number counts
            # match — otherwise it pairs unrelated values and reports noise
            numchg = ([[a, b] for a, b in zip(nums_o, nums_n) if a != b]
                      if len(nums_o) == len(nums_n) else [])
            ch = {"kind": "modified", "block": nb["id"], "type": nb["type"], "context": ctx}
            if moved:
                ch["also_moved"] = True
            if numchg:
                ch["numbers"] = numchg[:6]
            changes.append(ch)
        elif moved:
            changes.append({"kind": "moved", "block": nb["id"], "type": nb["type"],
                            "context": ctx, "content_unchanged": True})
    for ob in old:
        if ob["id"] not in new_ids:
            changes.append({"kind": "removed", "block": ob["id"], "type": ob["type"],
                            "context": "", "preview": ob["text"][:60]})
    stats = {}
    for c in changes:
        stats[c["kind"]] = stats.get(c["kind"], 0) + 1
    return changes, stats


def word_diff(a, b, width=100, color=False):
    aw, bw = a.split(), b.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, aw, bw).get_opcodes():
        if op in ("delete", "replace"):
            seg = " ".join(aw[i1:i2])
            out.append(C("del", seg, strike=True) if color else "[-" + seg + "-]")
        if op in ("insert", "replace"):
            seg = " ".join(bw[j1:j2])
            out.append(C("add", seg) if color else "{+" + seg + "+}")
    s = " ".join(out)
    return s if color else s[:width * 3]


# ---------- ledger I/O (commit chain at refs/proofpress/ledger) ----------

def ledger_events():
    try:
        shas = git("rev-list", LEDGER_REF).split()
    except RuntimeError:
        return []
    evs = []
    for sha in shas:  # newest first
        ev = json.loads(git("show", f"{sha}:event.json"))
        ev["_commit"] = sha
        if ev.get("event") == "version_created" and not ev.get("event_id"):
            try:
                ev["event_id"] = stable_event_id(
                    ev, json.loads(git("show", f"{sha}:version.json")))
            except RuntimeError:
                pass
        evs.append(ev)
    return evs


def read_version(commit_sha):
    return json.loads(git("show", f"{commit_sha}:version.json"))


def artifact_id_at(path):
    if not os.path.isfile(path):
        return None
    try:
        _, meta, _, _ = read_artifact(path)
        return (meta or {}).get("artifact_id")
    except OSError:
        return None


def versions_of(path):
    aid = artifact_id_at(path)
    out = []
    for e in ledger_events():
        if e.get("event") != "version_created":
            continue
        if aid and e.get("artifact_id") == aid:
            out.append(e)
        elif e.get("artifact") == path and (not aid or not e.get("artifact_id")):
            out.append(e)
    return out


def latest_at_recorded_path(path):
    """Return the newest event projected at path, even if file metadata is gone.

    Normal edits carry artifact identity in the file.  A whole-file replace can
    strip that transport, so path continuity is the deterministic local
    fallback: the replacement is another version of the artifact last recorded
    at that path.
    """
    target = os.path.normcase(os.path.abspath(path))
    for event in ledger_events():
        if event.get("event") != "version_created":
            continue
        recorded = event.get("artifact")
        if recorded and os.path.normcase(os.path.abspath(recorded)) == target:
            return event
    return None


def read_artifact_for_update(path):
    """Read a carrier and recover stripped identity from its recorded path."""
    body, meta, capsule, errors = read_artifact(path)
    recovered = False
    if meta is None and "invalid_meta" not in errors:
        prior = latest_at_recorded_path(path)
        if prior and prior.get("artifact_id"):
            policy = prior.get("policy", "local")
            meta = new_meta(policy if policy in POLICIES else "local")
            meta["artifact_id"] = prior["artifact_id"]
            recovered = True
        else:
            meta = new_meta()
    return body, meta, capsule, errors, recovered


def latest_for(path):
    vs = versions_of(path)
    return vs[0] if vs else None


def write_event(event, version=None):
    entries = []
    files = [("event.json", event)] + ([("version.json", version)] if version else [])
    for name, obj in files:
        blob = git("hash-object", "-w", "--stdin",
                   input=json.dumps(obj, ensure_ascii=False, indent=1)).strip()
        entries.append(f"100644 blob {blob}\t{name}")
    tree = git("mktree", input="\n".join(entries) + "\n").strip()
    parent = []
    try:
        parent = ["-p", git("rev-parse", LEDGER_REF).strip()]
    except RuntimeError:
        pass
    msg = f"{event['event']}: {event['artifact']} {event.get('version', '')}".rstrip()
    commit = git("commit-tree", tree, *parent, "-m", msg).strip()
    git("update-ref", LEDGER_REF, commit)
    return commit


# ---------- commands ----------

def check_attribution_basis(basis):
    # `signed` is the reserved top rung of the attribution ladder. Until
    # cryptographic signing lands, accepting it would grade attribution
    # above what is actually attested — a false claim by construction.
    if basis == "signed":
        raise SystemExit("attribution_basis 'signed' is reserved until "
                         "signing is implemented; use harness_attested or below")


def do_snapshot(path, author, kind, session, note, claims=None, context=None,
                text=None, ts=None, source_commit=None, artifact_id=None,
                policy="local", actors=None, attribution_basis="unknown",
                ingredients=None, force_event=False,
                prev_event_override=None, prev_version_override=None):
    """Core snapshot: file → block tree → ledger. Returns event or None (no change).

    `claims` is the author's structured self-description of the change
    (list of {"block", "kind", "note"?}); it is stored verbatim so `verify`
    can check it against the computed diff — claims are input to be
    verified, never trusted.

    `text`/`ts`/`source_commit` let `ingest` replay historical git commits
    into the ledger with their original content, author date and commit sha.

    `ingredients` is a list of upstream-artifact references (id + head +
    digest, never copied history) recorded when this version merges other
    Proofpress artifacts; the linear `parent` chain is unaffected."""
    check_attribution_basis(attribution_basis)
    if text is None:
        text = open(path).read()
    prev_ev = (prev_event_override if prev_event_override is not None
               else latest_for(path))
    prev_v = (prev_version_override if prev_version_override is not None
              else (read_version(prev_ev["_commit"]) if prev_ev else None))
    blocks = assign_ids(parse_blocks(text, carrier_for_path(path)), prev_v)
    version = {"artifact": path, "artifact_id": artifact_id, "blocks": blocks}
    vid = version_id(version)
    if prev_ev and prev_ev["version"] == vid and not force_event:
        return None
    changes, stats = semantic_diff(prev_v, version)
    event = {
        "event": "version_created",
        "artifact": path,
        "artifact_id": artifact_id,
        "version": vid,
        "parent": prev_ev["version"] if prev_ev else None,
        "author": {"name": author, "kind": kind, "session": session},
        "note": note,
        "ts": ts or datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "stats": stats,
        "changes": changes,
        "policy": policy,
        "soft_fingerprint": soft_fingerprint(blocks),
    }
    if ingredients:
        event["ingredients"] = ingredients
    if actors:
        event["actors"] = actors
    event["attribution_basis"] = attribution_basis
    if source_commit:
        event["source_commit"] = source_commit
    if claims is not None:
        event["claims"] = claims
    if context is not None:
        # Decision context is attributed testimony, not verified data: the
        # engine can check WHAT changed against claims, but WHY is the
        # author's account, recorded at submit time while it is still hot.
        event["context"] = context
    event["event_id"] = stable_event_id(event, version)
    event["_commit_new"] = write_event(event, version)
    event["_version_new"] = version
    return event


def _public_event(event):
    return {k: v for k, v in event.items() if not k.startswith("_")}


_EVENT_ID_EXCLUDED = {
    "event_id", "artifact", "parent", "parents", "changes", "stats",
    "policy", "portable_lineage_id", "imported_from_capsule",
}


def stable_event_id(event, version):
    """Return a path- and graph-independent identity for public testimony.

    Version IDs identify body states. Event IDs identify admissions of those
    states, so two collaborators who independently reach identical text still
    retain their distinct actors, reasons and timestamps after a DAG merge.
    Graph edges and computed diffs are excluded because portable projection can
    legitimately recompute them relative to a different public parent.
    """
    testimony = {
        k: v for k, v in _public_event(event).items()
        if k not in _EVENT_ID_EXCLUDED
    }
    payload = {
        "testimony": testimony,
        "version": version_id(version),
        "body_digest": body_digest(version),
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode()
    return "ppe_" + hashlib.sha256(raw).hexdigest()[:24]


def _parent_edge(parent_event, parent_version, child_version):
    changes, stats = semantic_diff(parent_version, child_version)
    return {
        "event_id": parent_event["event_id"],
        "version": parent_event["version"],
        "changes": changes,
        "stats": stats,
    }


def _v2_record(record, prior=None):
    """Normalize a legacy/v2 record without mutating the carrier payload."""
    event = dict(record["event"])
    version = dict(record["version"])
    event["event_id"] = event.get("event_id") or stable_event_id(event, version)
    if "parents" not in event:
        event["parents"] = []
        if prior is not None:
            event["parents"].append(_parent_edge(
                prior["event"], prior["version"], version))
    if event["parents"]:
        event["parent"] = event["parents"][0]["version"]
        event["changes"] = event["parents"][0]["changes"]
        event["stats"] = event["parents"][0]["stats"]
    else:
        event["parent"] = None
    return {"event": event, "version": version}


def capsule_v2(capsule):
    """Return a deterministic DAG projection of either capsule generation."""
    records = []
    prior = None
    for raw in capsule.get("records") or []:
        record = _v2_record(raw, prior)
        records.append(record)
        prior = record
    out = dict(capsule)
    out["proofpress_capsule"] = 2
    out["records"] = records
    if records:
        event_ids = {r["event"]["event_id"] for r in records}
        requested = capsule.get("head_event")
        out["head_event"] = (requested if requested in event_ids
                             else records[-1]["event"]["event_id"])
        by_event = {r["event"]["event_id"]: r for r in records}
        out["head"] = by_event[out["head_event"]]["event"]["version"]
    return out


def _record_map(capsule):
    normalized = capsule_v2(capsule)
    return {
        r["event"]["event_id"]: r
        for r in normalized.get("records", [])
    }


def _actors_from_args(a):
    actors = {}
    for field in ("requested_by", "produced_by", "edited_by", "recorded_by"):
        values = getattr(a, field, None)
        if values:
            actors[field] = values
    if "recorded_by" not in actors and getattr(a, "author", None):
        actors["recorded_by"] = [a.author]
    return actors


def make_checkpoint_capsule(path, body, meta, recorded_by=None,
                            attribution_basis="self_asserted"):
    check_attribution_basis(attribution_basis)
    prev_ev = latest_for(path)
    prev_v = read_version(prev_ev["_commit"]) if prev_ev else None
    blocks = assign_ids(parse_blocks(body, carrier_for_path(path)), prev_v)
    version = {"artifact": path, "artifact_id": meta["artifact_id"],
               "blocks": blocks}
    vid = version_id(version)
    changes, stats = semantic_diff(None, version)
    lineage = meta.get("portable_lineage_id") or "ppl_" + secrets.token_hex(12)
    meta["portable_lineage_id"] = lineage
    event = {
        "event": "version_created", "artifact": path,
        "artifact_id": meta["artifact_id"], "version": vid, "parent": None,
        "author": {"name": recorded_by or "unknown", "kind": "system",
                   "session": None},
        "actors": ({"recorded_by": [recorded_by]} if recorded_by else {}),
        "attribution_basis": attribution_basis,
        "note": "portable lineage checkpoint", "policy": "portable",
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "stats": stats, "changes": changes,
        "soft_fingerprint": soft_fingerprint(blocks),
        "portable_checkpoint": True,
        "portable_lineage_id": lineage,
        "parents": [],
    }
    event["event_id"] = stable_event_id(event, version)
    return {
        "proofpress_capsule": 2,
        "artifact_id": meta["artifact_id"],
        "portable_lineage_id": lineage,
        "head": vid,
        "head_event": event["event_id"],
        "body_digest": body_digest(version),
        "discovery": dict(CAPSULE_DISCOVERY),
        "records": [{"event": event, "version": version}],
    }


def validate_capsule(body, meta, capsule, carrier="markdown"):
    errors = []
    if not meta:
        return ["missing_meta"]
    if not capsule:
        return ["missing_capsule"]
    schema = capsule.get("proofpress_capsule")
    if schema not in (1, 2):
        errors.append("unsupported_capsule")
    if ("discovery" in capsule and
            not valid_capsule_discovery(capsule.get("discovery"))):
        errors.append("invalid_capsule_discovery")
    if capsule.get("artifact_id") != meta.get("artifact_id"):
        errors.append("artifact_id_mismatch")
    if capsule.get("portable_lineage_id") != meta.get("portable_lineage_id"):
        errors.append("lineage_id_mismatch")
    records = capsule.get("records")
    if not isinstance(records, list) or not records:
        return errors + ["missing_records"]
    malformed = [
        i for i, record in enumerate(records)
        if (not isinstance(record, dict) or
            not isinstance(record.get("event"), dict) or
            not isinstance(record.get("version"), dict))
    ]
    if malformed:
        return errors + [f"invalid_record:{i}" for i in malformed]
    if schema == 1:
        prev_id = None
        for i, record in enumerate(records):
            event = record.get("event") if isinstance(record, dict) else None
            if isinstance(event, dict) and event.get("parent") != prev_id:
                errors.append(f"chain_mismatch:{i}")
            version = record.get("version") if isinstance(record, dict) else None
            if isinstance(version, dict):
                prev_id = version_id(version)

    normalized = capsule_v2(capsule)
    records = normalized["records"]
    seen, referenced = {}, set()
    for i, record in enumerate(records):
        event, version = record.get("event"), record.get("version")
        if not isinstance(event, dict) or not isinstance(version, dict):
            errors.append(f"invalid_record:{i}"); continue
        vid = version_id(version)
        if event.get("version") != vid:
            errors.append(f"version_id_mismatch:{i}")
        if event.get("artifact_id") != capsule.get("artifact_id"):
            errors.append(f"record_artifact_mismatch:{i}")
        expected_event_id = stable_event_id(event, version)
        if event.get("event_id") != expected_event_id:
            errors.append(f"event_id_mismatch:{i}")
        if event.get("event_id") in seen:
            errors.append(f"duplicate_event:{i}")
        parents = event.get("parents")
        if not isinstance(parents, list):
            errors.append(f"invalid_parents:{i}")
            parents = []
        if not parents:
            computed, stats = semantic_diff(None, version)
            if event.get("changes") != computed or event.get("stats") != stats:
                errors.append(f"change_mismatch:{i}")
        for j, edge in enumerate(parents):
            parent = seen.get(edge.get("event_id")) if isinstance(edge, dict) else None
            if parent is None:
                errors.append(f"missing_or_late_parent:{i}:{j}")
                continue
            referenced.add(edge["event_id"])
            if edge.get("version") != parent["event"]["version"]:
                errors.append(f"parent_version_mismatch:{i}:{j}")
            computed, stats = semantic_diff(parent["version"], version)
            if edge.get("changes") != computed or edge.get("stats") != stats:
                errors.append(f"parent_change_mismatch:{i}:{j}")
        if parents:
            primary = parents[0]
            if (event.get("parent") != primary.get("version") or
                    event.get("changes") != primary.get("changes") or
                    event.get("stats") != primary.get("stats")):
                errors.append(f"primary_parent_mismatch:{i}")
        seen[event.get("event_id")] = record

    tips = set(seen) - referenced
    head_event = normalized.get("head_event")
    if len(tips) != 1:
        errors.append("multiple_heads")
    if head_event not in tips:
        errors.append("head_event_mismatch")
    head_record = seen.get(head_event)
    head_version = head_record["version"] if head_record else None
    head_id = head_record["event"]["version"] if head_record else None
    if capsule.get("head") != head_id:
        errors.append("head_mismatch")
    if head_version and capsule.get("body_digest") != body_digest(head_version):
        errors.append("capsule_body_digest_mismatch")
    current_blocks = assign_ids(parse_blocks(body, carrier), head_version)
    current_v = {"artifact": head_version.get("artifact") if head_version else "",
                 "artifact_id": meta.get("artifact_id"), "blocks": current_blocks}
    if head_version and body_digest(current_v) != capsule.get("body_digest"):
        errors.append("body_mismatch")
    return errors


def append_capsule(path, body, meta, capsule, event, version):
    if capsule is None:
        return make_checkpoint_capsule(
            path, body, meta,
            recorded_by=(event.get("actors", {}).get("recorded_by") or [None])[0],
            attribution_basis=event.get("attribution_basis", "unknown"))
    errors = validate_capsule(body, meta, capsule, carrier_for_path(path))
    # body mismatch is expected immediately before appending a new snapshot;
    # every other inconsistency means the prior history is unsafe to extend.
    blocking = [e for e in errors if e != "body_mismatch"]
    if blocking:
        raise SystemExit("cannot extend invalid capsule: " + ", ".join(blocking))
    capsule["discovery"] = dict(CAPSULE_DISCOVERY)
    normalized = capsule_v2(capsule)
    prior_record = _record_map(normalized)[normalized["head_event"]]
    prior_v = prior_record["version"]
    if version_id(version) == capsule["head"]:
        capsule["body_digest"] = body_digest(version)
        return capsule
    changes, stats = semantic_diff(prior_v, version)
    portable_event = _public_event(event)
    portable_event["parent"] = capsule["head"]
    portable_event["changes"] = changes
    portable_event["stats"] = stats
    portable_event["policy"] = "portable"
    portable_event["portable_lineage_id"] = capsule["portable_lineage_id"]
    if capsule.get("proofpress_capsule") == 2:
        edge = _parent_edge(prior_record["event"], prior_v, version)
        portable_event["parents"] = [edge]
        portable_event["event_id"] = stable_event_id(portable_event, version)
    capsule["records"].append({"event": portable_event, "version": version})
    capsule["head"] = portable_event["version"]
    if capsule.get("proofpress_capsule") == 2:
        capsule["head_event"] = portable_event["event_id"]
    capsule["body_digest"] = body_digest(version)
    return capsule


def cmd_snapshot(a):
    body, meta, capsule, errors, recovered = read_artifact_for_update(a.file)
    if errors:
        raise SystemExit("invalid Proofpress metadata: " + ", ".join(errors))
    if meta["policy"] == "ignored":
        print(f"skipped: {a.file} policy is ignored")
        return
    if recovered:
        print(f"recovered identity: {a.file} -> {meta['artifact_id']} "
              "(matched previous ledger path)")
    if getattr(a, "base_version", None):
        current = (capsule or {}).get("head")
        if current is None:
            latest = latest_for(a.file)
            current = latest.get("version") if latest else None
        if current != a.base_version:
            raise SystemExit(
                f"stale base: expected {a.base_version}, current "
                f"{current or '∅'}; inspect and reconcile before snapshot")
    if getattr(a, "base_event", None):
        current_event = (capsule_v2(capsule).get("head_event")
                         if capsule else None)
        if current_event != a.base_event:
            raise SystemExit(
                f"stale base event: expected {a.base_event}, current "
                f"{current_event or '∅'}; inspect and reconcile before snapshot")
    # Persist identity even for local artifacts; this is not a portable capsule.
    if artifact_id_at(a.file) is None:
        write_artifact(a.file, body, meta, capsule)
    claims = None
    if a.claims:
        claims = json.load(open(a.claims))
        if not isinstance(claims, list):
            raise SystemExit("--claims file must be a JSON array of "
                             '{"block", "kind", "note"?} objects')
    context = None
    if a.why or a.rejected:
        context = {}
        if a.why:
            context["why"] = a.why
        if a.rejected:
            context["rejected"] = a.rejected
    actors = _actors_from_args(a)
    force_event = False
    portable_prev_event = portable_prev_version = None
    if meta["policy"] == "portable" and capsule is not None:
        cap_state = validate_capsule(
            body, meta, capsule, carrier_for_path(a.file))
        force_event = "body_mismatch" in cap_state
        normalized = capsule_v2(capsule)
        head_record = _record_map(normalized)[normalized["head_event"]]
        portable_prev_event = head_record["event"]
        portable_prev_version = head_record["version"]
    ev = do_snapshot(a.file, a.author, a.kind, a.session, a.note,
                     claims=claims, context=context, text=body,
                     artifact_id=meta["artifact_id"], policy=meta["policy"],
                     actors=actors, attribution_basis=a.attribution_basis,
                     ingredients=getattr(a, "ingredients", None),
                     force_event=force_event,
                     prev_event_override=portable_prev_event,
                     prev_version_override=portable_prev_version)
    if not ev:
        if meta["policy"] == "portable" and capsule is None and recovered:
            capsule = make_checkpoint_capsule(
                a.file, body, meta,
                recorded_by=(actors.get("recorded_by") or [a.author])[0],
                attribution_basis=a.attribution_basis)
            meta["portable_head"] = capsule["head"]
            meta["portable_head_event"] = capsule.get("head_event")
            write_artifact(a.file, body, meta, capsule)
            print(f"repaired capsule: {a.file} -> {capsule['head']}")
            return
        if meta["policy"] == "portable" and capsule is not None:
            discovery = capsule.get("discovery")
            if (discovery is None or
                    (valid_capsule_discovery(discovery) and
                     discovery != CAPSULE_DISCOVERY)):
                capsule["discovery"] = dict(CAPSULE_DISCOVERY)
                write_artifact(a.file, body, meta, capsule)
                print(f"upgraded capsule discovery: {a.file} -> "
                      f"{CAPSULE_DISCOVERY['package']}@"
                      f"{CAPSULE_DISCOVERY['dist_tag']}")
                return
            latest = latest_for(a.file)
            if latest and capsule.get("head") != latest.get("version"):
                version = read_version(latest["_commit"])
                current_v = {"artifact": a.file,
                             "artifact_id": meta["artifact_id"],
                             "blocks": assign_ids(parse_blocks(body, carrier_for_path(a.file)), version)}
                if body_digest(current_v) == body_digest(version):
                    capsule = append_capsule(a.file, body, meta, capsule,
                                             latest, version)
                    meta["portable_head"] = capsule["head"]
                    meta["portable_head_event"] = capsule.get("head_event")
                    write_artifact(a.file, body, meta, capsule)
                    print(f"repaired capsule: {a.file} -> {capsule['head']}")
                    return
        print(f"no change: {a.file} matches the latest ledger version"); return
    if meta["policy"] == "portable":
        capsule = append_capsule(a.file, body, meta, capsule, ev,
                                 ev["_version_new"])
        meta["portable_head"] = capsule["head"]
        meta["portable_head_event"] = capsule.get("head_event")
        write_artifact(a.file, body, meta, capsule)
    n = f"v{len(versions_of(a.file))}"
    print(f"✓ {n} ({ev['version']}) ← {ev['parent'] or '∅'}   [{ev['_commit_new'][:8]} @ {LEDGER_REF}]")
    if ev["stats"]:
        print("  " + "  ".join(f"{k} {v}" for k, v in sorted(ev["stats"].items())))
    if a.note:
        print(f"  note: {a.note}")
    if claims is not None:
        print(f"  claims: {len(claims)} recorded — run `proofpress verify {a.file}` to check them")


def cmd_log(a):
    evs = versions_of(a.file)
    if not evs:
        print("artifact not in ledger"); return
    if a.json:
        out = []
        for i, ev in enumerate(evs):
            e = {k: v for k, v in ev.items() if k != "_commit"}
            e["v"] = len(evs) - i
            out.append(e)
        print(json.dumps(out, ensure_ascii=False, indent=2)); return
    namew = max(len(ev["author"]["name"]) for ev in evs)
    stat_plain = [stats_text(ev.get("stats", {})) for ev in evs]
    statw = max(len(t) for t, _ in stat_plain)
    for i, ev in enumerate(evs):
        n = len(evs) - i
        who = ev["author"]
        ts = ev["ts"][5:16].replace("T", " ")
        txt, color = stat_plain[i]
        line = (f'{C("accent", f"v{n}")}  {ev["version"]}  {C("dim", ts)}  '
                f'{who["name"]:<{namew}} {C("dim", who["kind"])}   '
                f'{C(color, txt.ljust(statw))}')
        if ev.get("note"):
            line += f"  {ev['note']}"
        if len(ev.get("parents") or []) > 1:
            line += C("dim", f"  merge={len(ev['parents'])} parents")
        if who.get("session"):
            line += C("dim", f"  session={who['session']}")
        print(line)


def _find(evs, prefix):
    for ev in evs:
        if ((ev.get("event_id") or "").startswith(prefix) or
                ev["version"].startswith(prefix)):
            return ev
    raise SystemExit(f"version not found: {prefix}")


def _primary_parent_event(event, events):
    parents = event.get("parents") or []
    if parents:
        parent_id = parents[0].get("event_id")
        return next((e for e in events if e.get("event_id") == parent_id), None)
    parent_version = event.get("parent")
    return next((e for e in events if e.get("version") == parent_version), None)


def change_label(c):
    """Row title + secondary context for a change — one formatter shared by
    the tty and markdown renderers (the Action must never re-implement this)."""
    ctx = c.get("context", "")
    if c["kind"] in ("added", "removed"):
        title = (c.get("preview") or "").strip().replace("\n", " ")[:56] or ctx
        same = ctx and title.lstrip("# ").startswith(ctx[:24])
        return title, ("" if same or not ctx else ctx)
    return (ctx or c.get("preview", "")[:48]), ""


def verify_label(change, fallback):
    """Make a claim target distinguishable from its heading context.

    A Markdown heading and every block beneath it share ``context``.  Verify
    output therefore needs the block type and, for non-headings, a short
    preview so adjacent rows are not mistaken for duplicate blocks.
    """
    if not change:
        return fallback
    ctx = change.get("context", "")
    block_type = change.get("type", "block")
    preview = (change.get("preview") or "").strip().replace("\n", " ")[:56]
    if block_type == "heading" or not preview:
        return f"{ctx or fallback} / {block_type}"
    return f"{ctx + ' / ' if ctx else ''}{block_type}: {preview}"


def cmd_diff(a):
    evs = versions_of(a.file)
    if len(evs) < 2 and not (a.va and a.vb):
        print("_fewer than two ledger versions — nothing to diff yet_" if a.md
              else "fewer than two versions")
        return
    ev_b = _find(evs, a.vb) if a.vb else evs[0]
    base_note = ""
    if a.base_commit and not a.va:
        hit = next((e for e in evs if (e.get("source_commit") or "").startswith(a.base_commit)), None)
        ev_a = hit or _primary_parent_event(ev_b, evs) or evs[1]
        if not hit:
            base_note = "base commit not in ledger — showing last recorded change"
    else:
        ev_a = (_find(evs, a.va) if a.va else
                (_primary_parent_event(ev_b, evs) or evs[1]))
    va, vb = read_version(ev_a["_commit"]), read_version(ev_b["_commit"])
    changes, stats = semantic_diff(va, vb)
    if a.json:
        print(json.dumps({"artifact": a.file, "from": ev_a["version"],
                          "to": ev_b["version"], "stats": stats,
                          "changes": changes}, ensure_ascii=False, indent=2))
        return
    if a.md:
        # GitHub markdown can't render our palette (no custom text color),
        # so we approximate with circle emoji — but yellow is reserved
        # exclusively for a real alarm (⚠️ claim mismatch below), never for
        # "this block changed". add/del keep the obvious green/red; modified
        # gets blue (closest emoji match to our terminal accent teal); moved
        # gets purple so it never reads as a warning either.
        emoji = {"added": "🟢 new", "removed": "🔴 del",
                 "modified": "🔵 mod", "moved": "🟣 mov"}
        stat_str = "  ".join(f"{v} {k}" for k, v in sorted(stats.items())) or "no block changes"
        out = [f"`{ev_a['version']} → {ev_b['version']}` ▍ {stat_str}"]
        if base_note:
            out.append(f"_{base_note}_")
        for c in changes[:20]:
            title, ctx = change_label(c)
            row = f"- {emoji[c['kind']]} · {title}" + (f"  _· {ctx}_" if ctx else "")
            if c.get("numbers"):
                row += "  **Δ " + "  ".join(f"{x}→{y}" for x, y in c["numbers"]) + "**"
            out.append(row)
        if len(changes) > 20:
            out.append(f"- _…and {len(changes) - 20} more_")
        if ev_b.get("note"):
            out.append(f"> changelog: {ev_b['note']}")
        ctx_b = ev_b.get("context") or {}
        if ctx_b.get("why"):
            out.append(f"> why: {ctx_b['why']}")
        print("\n".join(out))
        return
    # numeric deltas are the highest-risk signal — surface them in the header
    allnums = [d for c in changes for d in c.get("numbers", [])]
    head = (f'{C("dim", ev_a["version"] + " → " + ev_b["version"])}  '
            + C("accent", "▍ " + stats_summary(stats)))
    if allnums:
        head += "  " + C("move", "Δ " + "  ".join(f"{x}→{y}" for x, y in allnums[:4]))
    print(head)
    print()
    tagmap = {"added": ("add", "[new]"), "removed": ("del", "[del]"),
              "modified": ("accent", "[mod]"), "moved": ("move", "[mov]")}
    old_by_id = {b["id"]: b for b in va["blocks"]}
    new_by_id = {b["id"]: b for b in vb["blocks"]}
    if base_note:
        print("  " + C("dim", base_note))
    for c in changes:
        color, tag = tagmap[c["kind"]]
        title, ctx = change_label(c)
        where = C("dim", "(" + c["block"] + (f" · {ctx}" if ctx else "") + ")")
        line = f'  {C(color, "▍ " + tag)} {B(md_term(title))} {where}'
        if c.get("numbers"):
            line += "  " + C("move", "Δ " + "  ".join(f"{x} → {y}" for x, y in c["numbers"]))
        if c.get("also_moved"):
            line += C("dim", "  (also moved)")
        if c.get("content_unchanged"):
            line += C("dim", "  — content unchanged")
        print(line)
        if c["kind"] == "modified":
            body = word_diff(old_by_id[c["block"]]["text"],
                             new_by_id[c["block"]]["text"], color=_color_on())
            for ln in body.splitlines() or [body]:
                print("        " + ln)
    # this version's self-description travels with the diff (provenance layer v0)
    if ev_b.get("note") or ev_b.get("context"):
        n_b = len(evs) - next(
            i for i, e in enumerate(evs)
            if e.get("event_id") == ev_b.get("event_id"))
        who = ev_b["author"]
        print()
        if ev_b.get("note"):
            print("  " + C("dim", f'changelog (v{n_b}, {who["kind"]}:{who["name"]}): ')
                  + ev_b["note"])
        ctx_b = ev_b.get("context") or {}
        if ctx_b.get("why"):
            print("  " + C("move", "why: ") + ctx_b["why"])
        for r in ctx_b.get("rejected", []):
            print("  " + C("del", "rejected: ") + r)
    if ev_b.get("claims") is not None:
        print("  " + C("dim", f'claims: {len(ev_b["claims"])} recorded — `proofpress verify {a.file} {ev_b["version"]}`'))


def cmd_ingest(a):
    """Backfill ledger versions from the file's git commit history.

    This is the no-install rail: teammates who never heard of proofpress
    just commit markdown as usual; the next `ingest` run turns each of
    their commits into a ledger version signed with the commit's author
    and date. Idempotent — commits already ingested (by sha) or identical
    in content to the ledger tip are skipped. When the ledger already has
    versions, only commits newer than the latest ledger entry are
    considered, so rewritten/older history is never replayed on top.
    Renames are not followed (v0)."""
    body, meta, _, errors = read_artifact(a.file, create_meta=True)
    if errors:
        raise SystemExit("invalid Proofpress metadata: " + ", ".join(errors))
    if artifact_id_at(a.file) is None:
        write_artifact(a.file, body, meta, None)
    out = git("log", "--format=%H%x00%an%x00%aI%x00%s", "--", a.file)
    entries = [ln.split("\x00", 3) for ln in out.strip().splitlines() if ln]
    entries.reverse()  # oldest → newest
    if not entries:
        print(f"no git history for {a.file}"); return
    evs = versions_of(a.file)
    known = {e.get("source_commit") for e in evs if e.get("source_commit")}
    floor_ts = evs[0]["ts"] if evs else None
    made = skipped = 0
    for sha, author, ts, subject in entries:
        if sha in known or (floor_ts and ts <= floor_ts):
            skipped += 1
            continue
        try:
            content = git("show", f"{sha}:{a.file}")
        except RuntimeError:
            skipped += 1
            continue  # path did not exist at that commit (rename/add later)
        ev = do_snapshot(a.file, author, "human", None, subject,
                         text=content, ts=ts, source_commit=sha,
                         artifact_id=meta["artifact_id"], policy="local",
                         actors={"recorded_by": ["git-ingest"],
                                 "edited_by": [author]},
                         attribution_basis="environment_attested")
        if ev:
            made += 1
            n = f"v{len(versions_of(a.file))}"
            print(f"✓ {n} ({ev['version']})  {ts[:16]}  {author}  {subject[:50]}")
        else:
            skipped += 1  # identical content to ledger tip
    print(f"ingested {made}, skipped {skipped} (already known / older than ledger / no content change)")


def _portable_merge_input(path, allow_body_mismatch=False):
    if not os.path.isfile(path):
        raise SystemExit(f"merge input not found: {path}")
    body, meta, capsule, errors = read_artifact(path)
    if errors:
        raise SystemExit(f"merge input {path}: invalid metadata: " + ", ".join(errors))
    if not meta or meta.get("policy") != "portable" or not capsule:
        raise SystemExit(f"merge input {path} must be a portable Proofpress artifact")
    cap_errors = validate_capsule(body, meta, capsule, carrier_for_path(path))
    blocking = [e for e in cap_errors
                if not (allow_body_mismatch and e == "body_mismatch")]
    if blocking:
        raise SystemExit(f"merge input {path}: invalid capsule: " + ", ".join(blocking))
    normalized = capsule_v2(capsule)
    records = _record_map(normalized)
    return {
        "path": path, "body": body, "meta": meta, "capsule": normalized,
        "records": records, "head_event": normalized["head_event"],
        "head_record": records[normalized["head_event"]],
        "body_mismatch": "body_mismatch" in cap_errors,
    }


def _merge_inputs(target, sources, target_may_drift=True):
    paths = [target] + list(sources)
    if len(set(os.path.abspath(p) for p in paths)) != len(paths):
        raise SystemExit("merge inputs must be distinct files")
    items = [_portable_merge_input(target, target_may_drift)]
    items.extend(_portable_merge_input(p) for p in sources)
    artifact_ids = {x["meta"]["artifact_id"] for x in items}
    lineages = {x["meta"].get("portable_lineage_id") for x in items}
    carriers = {carrier_for_path(x["path"]) for x in items}
    if len(artifact_ids) != 1:
        raise SystemExit("merge inputs are different artifacts; use merge-lineage "
                         "when one document incorporates another")
    if len(lineages) != 1 or None in lineages:
        raise SystemExit("merge inputs have different portable lineages; "
                         "use merge-lineage or start from a shared portable copy")
    if len(carriers) != 1:
        raise SystemExit("merge inputs must use the same carrier type")
    heads = [x["head_event"] for x in items]
    if len(set(heads)) != len(heads):
        raise SystemExit("merge inputs contain duplicate heads")
    return items


def _ancestor_ids(records, head):
    out, stack = set(), [head]
    while stack:
        event_id = stack.pop()
        if event_id in out:
            continue
        record = records.get(event_id)
        if record is None:
            continue
        out.add(event_id)
        stack.extend(edge["event_id"]
                     for edge in record["event"].get("parents", []))
    return out


def _merge_base(items):
    combined = {}
    for item in items:
        for event_id, record in item["records"].items():
            previous = combined.get(event_id)
            if previous and previous != record:
                raise SystemExit(f"event {event_id} differs between capsules")
            combined[event_id] = record
    common = set.intersection(*(
        _ancestor_ids(combined, item["head_event"]) for item in items))
    if not common:
        raise SystemExit("merge inputs have no common portable ancestor")
    lowest = []
    ancestry = {event_id: _ancestor_ids(combined, event_id)
                for event_id in common}
    for candidate in common:
        if not any(candidate != other and candidate in ancestry[other]
                   for other in common):
            lowest.append(candidate)
    if len(lowest) != 1:
        raise SystemExit("merge inputs have multiple merge bases; merge a smaller "
                         "set of copies first")
    return lowest[0], combined


def _block_state(version):
    return {b["id"]: b for b in version["blocks"]}


def _merge_plan_data(target, sources):
    items = _merge_inputs(target, sources)
    base_event, records = _merge_base(items)
    base_record = records[base_event]
    base_states = _block_state(base_record["version"])
    heads = [_block_state(x["head_record"]["version"]) for x in items]
    all_ids = set(base_states)
    for states in heads:
        all_ids.update(states)
    compatible, conflicts = [], []
    for block_id in sorted(all_ids):
        base = base_states.get(block_id)
        changed = []
        for item, states in zip(items, heads):
            state = states.get(block_id)
            if state != base:
                changed.append({"path": item["path"], "state": state})
        if not changed:
            continue
        distinct = {
            json.dumps(c["state"], ensure_ascii=False, sort_keys=True)
            for c in changed
        }
        entry = {
            "block": block_id,
            "base": base,
            "branches": changed,
        }
        if len(changed) == 1 or len(distinct) == 1:
            entry["reason"] = ("single_branch_change" if len(changed) == 1
                               else "identical_result")
            compatible.append(entry)
        else:
            entry["reason"] = "divergent_block_change"
            conflicts.append(entry)

    # Distinct concurrently-added blocks are content-compatible, but their
    # relative placement cannot be inferred safely from the block tree alone.
    additions = {}
    for item in items:
        changes, _ = semantic_diff(base_record["version"],
                                   item["head_record"]["version"])
        for change in changes:
            if change["kind"] == "added":
                additions.setdefault(change.get("context", ""), []).append(
                    {"path": item["path"], "block": change["block"]})
    for context, entries in additions.items():
        if len({e["path"] for e in entries}) > 1:
            conflicts.append({
                "kind": "parallel_insert_order",
                "context": context,
                "branches": entries,
                "reason": "parallel_insert_order",
            })

    return {
        "status": "conflicts" if conflicts else "clean",
        "artifact_id": items[0]["meta"]["artifact_id"],
        "portable_lineage_id": items[0]["meta"]["portable_lineage_id"],
        "base_event": base_event,
        "base_version": base_record["event"]["version"],
        "branches": [
            {"path": x["path"], "head_event": x["head_event"],
             "head": x["head_record"]["event"]["version"]}
            for x in items
        ],
        "compatible": compatible,
        "conflicts": conflicts,
    }


def cmd_merge_plan(a):
    plan = _merge_plan_data(a.file, a.source)
    if a.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return
    print(f"merge-plan {a.file}: {plan['status']}")
    print(f"  common ancestor: {plan['base_version']} "
          f"({plan['base_event']})")
    for branch in plan["branches"]:
        print(f"  branch: {branch['path']} -> {branch['head']} "
              f"({branch['head_event']})")
    print(f"  compatible changes: {len(plan['compatible'])}")
    print(f"  conflicts: {len(plan['conflicts'])}")
    for conflict in plan["conflicts"]:
        if conflict.get("kind") == "parallel_insert_order":
            print(f"    insertion order under {conflict.get('context') or '(document start)'}")
        else:
            print(f"    block {conflict['block']}: divergent changes")


def _topological_records(records):
    pending = dict(records)
    emitted, out = set(), []
    while pending:
        ready = [
            record for record in pending.values()
            if all(edge["event_id"] in emitted
                   for edge in record["event"].get("parents", []))
        ]
        if not ready:
            raise SystemExit("cannot order merged capsule records (missing parent or cycle)")
        ready.sort(key=lambda r: (
            r["event"].get("ts", ""), r["event"]["event_id"]))
        for record in ready:
            event_id = record["event"]["event_id"]
            out.append(record)
            emitted.add(event_id)
            pending.pop(event_id)
    return out


def cmd_merge(a):
    items = _merge_inputs(a.file, a.source)
    _merge_base(items)  # Validate the shared history before writing anything.
    target = items[0]
    primary = target["head_record"]
    blocks = assign_ids(parse_blocks(target["body"], carrier_for_path(a.file)),
                        primary["version"])
    version = {
        "artifact": a.file,
        "artifact_id": target["meta"]["artifact_id"],
        "blocks": blocks,
    }
    vid = version_id(version)
    parent_edges = [
        _parent_edge(item["head_record"]["event"],
                     item["head_record"]["version"], version)
        for item in items
    ]
    claims = None
    if a.claims:
        claims = json.load(open(a.claims))
        if not isinstance(claims, list):
            raise SystemExit("--claims file must be a JSON array")
    context = None
    if a.why or a.rejected:
        context = {}
        if a.why:
            context["why"] = a.why
        if a.rejected:
            context["rejected"] = a.rejected
    event = {
        "event": "version_created",
        "merge": True,
        "artifact": a.file,
        "artifact_id": target["meta"]["artifact_id"],
        "version": vid,
        "parent": parent_edges[0]["version"],
        "parents": parent_edges,
        "author": {"name": a.author, "kind": a.kind, "session": a.session},
        "note": a.note or "merged parallel portable copies",
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "stats": parent_edges[0]["stats"],
        "changes": parent_edges[0]["changes"],
        "policy": "portable",
        "portable_lineage_id": target["meta"]["portable_lineage_id"],
        "soft_fingerprint": soft_fingerprint(blocks),
        "actors": _actors_from_args(a),
        "attribution_basis": a.attribution_basis,
    }
    check_attribution_basis(a.attribution_basis)
    if claims is not None:
        event["claims"] = claims
    if context is not None:
        event["context"] = context
    event["event_id"] = stable_event_id(event, version)

    union = {}
    for item in items:
        for event_id, record in item["records"].items():
            if event_id in union and union[event_id] != record:
                raise SystemExit(f"event {event_id} differs between capsules")
            union[event_id] = record
    if event["event_id"] in union:
        raise SystemExit("this merge event is already present")
    union[event["event_id"]] = {"event": event, "version": version}
    records = _topological_records(union)
    capsule = {
        "proofpress_capsule": 2,
        "artifact_id": target["meta"]["artifact_id"],
        "portable_lineage_id": target["meta"]["portable_lineage_id"],
        "head": vid,
        "head_event": event["event_id"],
        "body_digest": body_digest(version),
        "discovery": dict(CAPSULE_DISCOVERY),
        "records": records,
    }
    meta = dict(target["meta"])
    meta["portable_head"] = vid
    meta["portable_head_event"] = event["event_id"]
    write_event(event, version)
    write_artifact(a.file, target["body"], meta, capsule)
    print(f"✓ merged {len(parent_edges)} parents -> {vid} "
          f"({event['event_id']})")
    for edge, item in zip(parent_edges, items):
        print(f"  parent: {item['path']} @ {edge['version']} "
              f"({edge['event_id']})")


def _ingredient_ref(path):
    """Reference + digest for an upstream artifact — never its history."""
    if not os.path.isfile(path):
        raise SystemExit(f"ingredient not found: {path}")
    _, meta, capsule, errors = read_artifact(path)
    if errors:
        raise SystemExit(f"ingredient {path}: invalid metadata: " + ", ".join(errors))
    if not meta:
        raise SystemExit(f"ingredient {path} is not proofpress-managed "
                         "(snapshot or import it first)")
    ref = {"artifact": path, "artifact_id": meta["artifact_id"]}
    latest = latest_for(path)
    if latest:
        ref["version"] = latest["version"]
        ref["body_digest"] = body_digest(read_version(latest["_commit"]))
    elif capsule:
        ref["version"] = capsule.get("head")
        ref["body_digest"] = capsule.get("body_digest")
    else:
        raise SystemExit(f"ingredient {path} has no ledger history or capsule "
                         "to reference")
    if meta.get("portable_lineage_id"):
        ref["portable_lineage_id"] = meta["portable_lineage_id"]
    return ref


def cmd_merge_lineage(a):
    """Record that this version merges multiple upstream Proofpress artifacts.

    C2PA-ingredient style: each --from source is stored as a reference
    (artifact_id + head version + body digest) on the merge event only.
    Upstream history is never copied, and the target artifact's parent graph
    is untouched — ingredients are additive provenance."""
    a.ingredients = [_ingredient_ref(p) for p in a.source]
    if a.note is None:
        a.note = "merged lineage from " + ", ".join(
            r["artifact_id"] for r in a.ingredients)
    cmd_snapshot(a)
    latest = latest_for(a.file)
    if not latest or latest.get("ingredients") != a.ingredients:
        raise SystemExit(
            "merge-lineage records ingredients on a new version, but the file "
            "content is unchanged from the ledger tip — write the merged "
            "content into the file first, then re-run")
    for r in a.ingredients:
        print(f"  ingredient: {r['artifact_id']} @ {r.get('version', '?')}"
              f"  ({r['artifact']})")


def cmd_identify(a):
    """Soft-binding lookup: recognize a file whose Proofpress metadata and
    capsule were stripped, using the local ledger as the fingerprint index.

    Answers identity ("this is pp_xxx"), not integrity — a match does not
    prove the content was never altered, only that this exact visible text
    skeleton was admitted before. Exit 0 found, 1 not found."""
    carrier = carrier_for_path(a.file)
    body, meta, _, _ = split_transport(open(a.file).read(), carrier)
    fp = soft_fingerprint(parse_blocks(body, carrier))
    matches = {}
    for ev in ledger_events():  # newest first — keep first hit per artifact
        if ev.get("event") != "version_created":
            continue
        evfp = ev.get("soft_fingerprint") or soft_fingerprint(
            read_version(ev["_commit"])["blocks"])  # pre-fingerprint events
        if evfp == fp:
            matches.setdefault(ev.get("artifact_id") or ev.get("artifact"), ev)
    found = list(matches.values())
    if a.json:
        print(json.dumps({
            "file": a.file, "soft_fingerprint": fp,
            "status": "identified" if found else "not_found",
            "matches": [{"artifact_id": e.get("artifact_id"),
                         "artifact": e.get("artifact"),
                         "version": e["version"], "ts": e["ts"]}
                        for e in found]}, ensure_ascii=False, indent=2))
        sys.exit(0 if found else 1)
    if not found:
        print(f"identify {a.file}: no ledger version matches this content "
              "(rewritten, or never admitted here)")
        sys.exit(1)
    print(f"identify {B(a.file)} " + C("dim", f"({fp[:22]}…)"))
    for e in found:
        marker = ""
        if meta and meta.get("artifact_id") == e.get("artifact_id"):
            marker = C("dim", "  (identity intact in file)")
        print(f'  {C("add", "✓")} {e.get("artifact_id") or "?"} @ {e["version"]}'
              f'  {C("dim", e["ts"][:16].replace("T", " "))}'
              f'  {e.get("artifact", "")}{marker}')
    sys.exit(0)


def cmd_export(a):
    """Write an artifact's ledger chain as one self-contained JSON bundle.

    The sidecar answers who/what/when/why (+ claims, verification inputs,
    rejected alternatives) without access to this repo or its git refs —
    the transport representation of the ledger. v0 includes everything;
    external-clean redaction is a later, mandatory share-flow feature."""
    evs = versions_of(a.file)
    if not evs:
        raise SystemExit("artifact not in ledger")
    bundle = {
        "proofpress_export": 1,
        "artifact": a.file,
        "head": evs[0]["version"],
        "exported_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "versions": [],
    }
    for i, ev in enumerate(reversed(evs)):  # oldest → newest
        e = {k: v for k, v in ev.items() if k != "_commit"}
        e["v"] = i + 1
        bundle["versions"].append(e)
    dest = a.output or (os.path.basename(a.file) + ".proofpress.json")
    with open(dest, "w") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=1)
    print(f"exported {len(evs)} versions ({bundle['head']} head) -> {dest}")


def anchor_file(path, quiet=False):
    """Write carrier-native identity anchors (idempotently).

    Markdown writes invisible link-reference comments. Static HTML writes a
    `data-proofpress-id` attribute directly onto each supported leaf block.
    Ids come from the ledger's latest version when one exists.
    """
    body, meta, capsule, errors = read_artifact(path)
    if errors:
        raise SystemExit("invalid Proofpress metadata: " + ", ".join(errors))
    if capsule:
        normalized = capsule_v2(capsule)
        head_record = _record_map(normalized)[normalized["head_event"]]
        prev_v = head_record["version"]
    else:
        prev_ev = latest_for(path)
        prev_v = read_version(prev_ev["_commit"]) if prev_ev else None
    carrier = carrier_for_path(path)
    blocks = assign_ids(parse_blocks(body, carrier), prev_v)
    if carrier == "html":
        cursor = 0

        def put_anchor(match):
            nonlocal cursor
            if cursor >= len(blocks):
                return match.group(0)
            block = blocks[cursor]
            cursor += 1
            start = HTML_ANCHOR_ATTR.sub("", match.group(0)).rstrip()
            return start[:-1] + f' data-proofpress-id="{block["id"]}">'

        anchored_body = HTML_BLOCK_START.sub(put_anchor, body)
        if cursor != len(blocks):
            raise SystemExit("could not anchor every HTML block; file changed while parsing")
    else:
        out = []
        for i, b in enumerate(blocks):
            if not is_leading_yaml_frontmatter(b, i):
                # Keep anchors for nested list content at the same indentation
                # as the block. An unindented marker would close the list in
                # CommonMark/GitHub rendering even though it is invisible.
                indent = re.match(r"^(\s*)", b["text"]).group(1)
                if b["type"] == "list" and not indent and i:
                    j = i - 1
                    while (j >= 0 and
                           re.match(r"^\s+", blocks[j]["text"])):
                        j -= 1
                    if j >= 0 and blocks[j]["type"] == "list":
                        previous_indent = re.match(
                            r"^(\s*)", blocks[i - 1]["text"]).group(1)
                        if previous_indent:
                            # This is the next outer item after nested content.
                            # Keep its marker inside the previous item so the
                            # ordered/unordered list remains open.
                            indent = previous_indent
                out.append(indent + format_anchor(b["id"]))
            out.append(b["text"])
            out.append("")
        anchored_body = "\n".join(out).rstrip() + "\n"
    write_artifact(path, anchored_body, meta, capsule)
    if not quiet:
        print(f"anchored {len(blocks)} blocks -> {path} (content hashes unchanged; ledger unaffected)")
    # id inventory for claim-writing: which identities carried over vs are new.
    # Deliberately silent about whether an inherited block's content changed —
    # that is what the author must declare and `verify` will check.
    if prev_v:
        prev_ids = {b["id"] for b in prev_v["blocks"]}
        cur_ids = [b["id"] for b in blocks]
        inherited = [i for i in cur_ids if i in prev_ids]
        new = [i for i in cur_ids if i not in prev_ids]
        gone = [i for i in prev_ids if i not in set(cur_ids)]
        if inherited:
            print(f"  inherited {len(inherited)}: " + " ".join(inherited))
        if new:
            print(f"  new {len(new)}: " + " ".join(new))
        if gone:
            print(f"  gone {len(gone)} (claim as removed): " + " ".join(gone))
    return blocks


def cmd_anchor(a):
    anchor_file(a.file)


def cmd_policy(a):
    body, meta, capsule, errors, _ = read_artifact_for_update(a.file)
    if errors:
        raise SystemExit("invalid Proofpress metadata: " + ", ".join(errors))
    if a.policy is None:
        print(f"{a.file}: {meta['policy']} ({meta['artifact_id']})")
        return
    old = meta.get("policy", "local")
    if a.policy == "portable":
        if old == "portable" and capsule is not None:
            cap_errors = validate_capsule(body, meta, capsule, carrier_for_path(a.file))
            if cap_errors:
                raise SystemExit("invalid existing capsule: " + ", ".join(cap_errors))
            print(f"unchanged: {a.file} is already portable")
            return
        meta["policy"] = "portable"
        meta["portable_lineage_id"] = "ppl_" + secrets.token_hex(12)
        capsule = make_checkpoint_capsule(
            a.file, body, meta, recorded_by=a.author,
            attribution_basis=a.attribution_basis)
        meta["portable_head"] = capsule["head"]
        meta["portable_head_event"] = capsule.get("head_event")
        write_artifact(a.file, body, meta, capsule)
        print(f"portable: {a.file} ({meta['artifact_id']}, head {capsule['head']})")
        return
    meta["policy"] = a.policy
    meta.pop("portable_lineage_id", None)
    meta.pop("portable_head", None)
    meta.pop("portable_head_event", None)
    write_artifact(a.file, body, meta, None)
    print(f"{a.policy}: {a.file} (capsule removed from this copy; old copies unchanged)")


def _matching_ledger_version(events, digest):
    """Return the newest recorded version with this visible-body digest."""
    for event in events:
        if body_digest(read_version(event["_commit"])) == digest:
            return event
    return None


def _worktree_ledger_state(path, body, meta):
    """Compare a local carrier with the ledger head, even without transport.

    Portable artifacts already have a capsule body digest. Local artifacts do
    not, which used to let ``verify`` validate an old event while silently
    ignoring an overwritten worktree. A stripped carrier falls back to the
    last recorded path so the warning remains useful after whole-file replace.
    """
    latest = latest_for(path) if meta else latest_at_recorded_path(path)
    if not latest:
        return None
    expected = read_version(latest["_commit"])
    current_blocks = parse_blocks(body, carrier_for_path(path))
    actual_digest = body_digest({"blocks": current_blocks})
    expected_digest = body_digest(expected)
    expected_fp = latest.get("soft_fingerprint") or soft_fingerprint(expected["blocks"])
    actual_fp = soft_fingerprint(current_blocks)
    events = (versions_of(path) if meta else
              [e for e in ledger_events()
               if e.get("event") == "version_created" and
               e.get("artifact_id") == latest.get("artifact_id")])
    matched = _matching_ledger_version(events, actual_digest)
    errors = []
    if meta is None:
        errors.append("unmanaged_worktree")
    elif meta.get("artifact_id") != latest.get("artifact_id"):
        errors.append("ledger_identity_mismatch")
    # Exact digest intentionally sees carrier formatting. The soft fingerprint
    # is the documented formatting-tolerant boundary: different Markdown table
    # spacing or emphasis placement is not a content drift.
    formatting_drift = actual_digest != expected_digest and actual_fp == expected_fp
    if actual_digest != expected_digest and not formatting_drift:
        errors.append("worktree_not_at_ledger_head")
    if not errors and not formatting_drift:
        return None
    return {
        "ledger_head": latest["version"],
        "observed_version": (matched.get("version") if matched else
                             (latest["version"] if formatting_drift else None)),
        "errors": errors,
        "formatting_drift": formatting_drift,
    }


def inspect_result(path):
    body, meta, capsule, errors = read_artifact(path)
    result = {"artifact": path, "managed": meta is not None,
              "policy": (meta or {}).get("policy", "unmanaged"),
              "artifact_id": (meta or {}).get("artifact_id"),
              "capsule": capsule is not None, "status": "ok", "errors": list(errors)}
    if meta and meta.get("policy") == "portable":
        result["errors"].extend(validate_capsule(body, meta, capsule, carrier_for_path(path)))
        if capsule:
            result["head"] = capsule.get("head")
            result["head_event"] = capsule_v2(capsule).get("head_event")
            result["versions"] = len(capsule.get("records", []))
            if valid_capsule_discovery(capsule.get("discovery")):
                result["discovery"] = capsule["discovery"]
    elif capsule is not None:
        result["errors"].append("capsule_on_nonportable_artifact")
    # A portable mismatch is already reported by capsule validation. For local
    # and stripped carriers, compare the visible worktree to the ledger head.
    if not (meta and meta.get("policy") == "portable"):
        worktree = _worktree_ledger_state(path, body, meta)
        if worktree:
            result["ledger_head"] = worktree["ledger_head"]
            result["observed_version"] = worktree["observed_version"]
            result["formatting_drift"] = worktree["formatting_drift"]
            result["errors"].extend(worktree["errors"])
    if result["errors"]:
        result["status"] = "mismatch"
    return result


def cmd_inspect(a):
    result = inspect_result(a.file)
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"inspect {a.file}: {result['status']}")
        print(f"  policy: {result['policy']}")
        if result.get("artifact_id"):
            print(f"  artifact: {result['artifact_id']}")
        if result.get("head"):
            print(f"  capsule: {result['versions']} version(s), head {result['head']}")
            if result.get("head_event"):
                print(f"  head event: {result['head_event']}")
        if result.get("ledger_head"):
            observed = result.get("observed_version") or "unrecorded/unknown"
            print(f"  ledger head: {result['ledger_head']} (worktree: {observed})")
        if result.get("formatting_drift"):
            print("  note: formatting differs from the ledger head; visible content matches")
        if result.get("discovery"):
            print(f"  provenance: {result['discovery']['label']}")
            print(f"  learn more: {result['discovery']['project_url']}")
            print(f"  package: {result['discovery']['package']}@"
                  f"{result['discovery']['dist_tag']} (user consent required)")
        for error in result["errors"]:
            print(f"  error: {error}")
        if "unmanaged_worktree" in result["errors"]:
            print(f"  action: run `proofpress identify {a.file}`; reconcile the file before snapshotting")
        elif "worktree_not_at_ledger_head" in result["errors"]:
            print("  action: restore or reconcile the ledger head; snapshot only if this edit is intentional")
    if result["status"] != "ok":
        sys.exit(1)


def cmd_import(a):
    body, meta, capsule, errors = read_artifact(a.file)
    if errors:
        raise SystemExit("invalid Proofpress metadata: " + ", ".join(errors))
    cap_errors = validate_capsule(body, meta, capsule, carrier_for_path(a.file))
    if cap_errors:
        raise SystemExit("invalid capsule: " + ", ".join(cap_errors))
    known = {
        e.get("event_id") or stable_event_id(e, read_version(e["_commit"]))
        for e in versions_of(a.file)
    }
    made = skipped = 0
    for record in capsule_v2(capsule)["records"]:
        event = dict(record["event"])
        version = dict(record["version"])
        if event["event_id"] in known:
            skipped += 1; continue
        event["artifact"] = a.file
        event["imported_from_capsule"] = True
        version["artifact"] = a.file
        write_event(event, version)
        known.add(event["event_id"]); made += 1
    print(f"imported {made}, skipped {skipped} -> {a.file} ({meta['artifact_id']})")


def cmd_clean(a):
    body, _, _, _ = read_artifact(a.file)
    if os.path.abspath(a.output) == os.path.abspath(a.file):
        raise SystemExit("clean output must differ from the source artifact")
    atomic_write(a.output, body)
    print(f"clean copy -> {a.output} (capsule and artifact metadata removed)")


def changed_artifact_files():
    """Find carriers that the fallback hook can safely reconcile.

    Git remains useful for discovering never-admitted files.  Already-admitted
    artifacts also come from the ledger, so ignored files and manual edits are
    still checked when a hook runs.
    """
    paths = set()
    for pattern in ("*.md", "*.html", "*.htm"):
        commands = [
            ("diff", "--name-only", "HEAD", "--", pattern),
            ("diff", "--cached", "--name-only", "HEAD", "--", pattern),
            ("ls-files", "--others", "--exclude-standard", "--", pattern),
        ]
        for args in commands:
            try:
                paths.update(p for p in git(*args).splitlines() if p)
            except RuntimeError:
                continue
    seen = set()
    for event in ledger_events():
        if event.get("event") != "version_created":
            continue
        identity = event.get("artifact_id") or event.get("artifact")
        if identity in seen:
            continue
        seen.add(identity)
        path = event.get("artifact")
        if path and os.path.isfile(path):
            paths.add(path)
    return sorted(p for p in paths if os.path.isfile(p) and carrier_for_path(p) in ("markdown", "html"))


def matches_latest(path, body, meta):
    latest = latest_for(path)
    if not latest:
        return False
    previous = read_version(latest["_commit"])
    blocks = assign_ids(parse_blocks(body, carrier_for_path(path)), previous)
    current = {"artifact": path, "artifact_id": meta["artifact_id"],
               "blocks": blocks}
    return version_id(current) == latest["version"]


def cmd_capture(a):
    paths = sorted(set(a.files)) if a.files else changed_artifact_files()
    captured = skipped = 0
    for path in paths:
        body, meta, _, errors, recovered = read_artifact_for_update(path)
        if errors:
            print(f"capture warning: {path}: " + ", ".join(errors))
            skipped += 1; continue
        if meta["policy"] == "ignored":
            print(f"capture skipped: {path} is ignored")
            skipped += 1; continue
        if not recovered and matches_latest(path, body, meta):
            skipped += 1; continue
        anchor_file(path, quiet=True)
        ns = argparse.Namespace(
            file=path, author=a.recorder, kind="system", session=a.session,
            note="best-effort fallback capture; edit attribution unknown",
            claims=None, why=None, rejected=None,
            requested_by=None, produced_by=None, edited_by=None,
            recorded_by=[a.recorder], attribution_basis="harness_attested")
        before = latest_for(path)
        cmd_snapshot(ns)
        after = latest_for(path)
        if after and (not before or after["version"] != before["version"]):
            captured += 1
        else:
            skipped += 1
    print(f"capture complete: {captured} snapshot(s), {skipped} skipped/no-op")


def cmd_init(a):
    try:
        git("remote", "get-url", "origin")
    except RuntimeError:
        print("no remote origin yet; re-run proofpress init after adding one and the ledger will sync with push/fetch")
        return
    # Deliberately NOT forced (no leading +): a forced refspec lets any
    # `git fetch` silently rewind the local ledger to the remote's older
    # state, orphaning unsynced events (this happened — 2026-07-22, live).
    # Unforced, a divergent fetch fails loudly instead; run `proofpress
    # sync` first and the fetch fast-forwards.
    spec = "refs/proofpress/*:refs/proofpress/*"
    forced = "+" + spec
    cur = subprocess.run(["git", "config", "--get-all", "remote.origin.fetch"],
                         capture_output=True, text=True).stdout
    if forced in cur:
        git("config", "--unset-all", "remote.origin.fetch", re.escape(forced))
        git("config", "--add", "remote.origin.fetch", spec)
        print("fetch refspec de-forced: a stale remote can no longer clobber local ledger events")
    elif spec not in cur:
        git("config", "--add", "remote.origin.fetch", spec)
        print("fetch refspec written: clone/pull will carry the ledger automatically")
    else:
        print("fetch refspec already present")
    print("push side: run `proofpress sync` (or git push origin 'refs/proofpress/*')")


def cmd_sync(a):
    git("push", "origin", "refs/proofpress/*:refs/proofpress/*")
    print("ledger pushed to origin")


def cmd_blocks(a):
    evs = versions_of(a.file)
    if not evs:
        print("artifact not in ledger"); return
    ev = _find(evs, a.version) if a.version else evs[0]
    v = read_version(ev["_commit"])
    print(f"{a.file} @ {ev['version']}  ({len(v['blocks'])} blocks)")
    for b in v["blocks"]:
        first = b["text"].splitlines()[0]
        indent = "  " if b["type"] != "heading" else ""
        print(f"  {b['id']}  {b['type']:<7} {indent}{first[:56]}")


def _resolve_show_ref(ref):
    """`show` accepts an artifact path (→ latest version) or a version prefix."""
    lat = latest_for(ref)
    if lat:
        return lat, versions_of(ref)
    for ev in ledger_events():
        if ev["event"] == "version_created" and ev["version"].startswith(ref):
            return ev, versions_of(ev["artifact"])
    raise SystemExit("not found")


def cmd_show(a):
    ev, evs = _resolve_show_ref(a.ref)
    if a.json:
        e = {k: v for k, v in ev.items() if k != "_commit"}
        print(json.dumps(e, ensure_ascii=False, indent=2)); return
    idx = next(i for i, e in enumerate(evs)
               if e.get("event_id") == ev.get("event_id"))
    n = len(evs) - idx
    v = read_version(ev["_commit"])
    parent_ev = _primary_parent_event(ev, evs)
    parent_v = read_version(parent_ev["_commit"]) if parent_ev else None
    changes, stats = semantic_diff(parent_v, v) if parent_v else ([], {})
    chg_by_id = {c["block"]: c for c in changes if c["kind"] != "removed"}
    who = ev["author"]
    ts = ev["ts"][:16].replace("T", " ")
    print(f'{B(ev["artifact"])} '
          + C("dim", f'@ v{n} · {ev["version"]} · {who["name"]} ({who["kind"]}) · {ts}'))
    if parent_v:
        line = C("accent", f"▍ {stats_summary(stats)} vs v{n - 1}")
        if ev.get("note"):
            line += C("dim", f' — {ev["note"]}')
        print(line)
    elif ev.get("note"):
        print(C("dim", ev["note"]))
    ctx_ev = ev.get("context") or {}
    if ctx_ev.get("why"):
        print(C("move", "why: ") + md_term(ctx_ev["why"]))
    for r in ctx_ev.get("rejected", []):
        print(C("del", "rejected: ") + md_term(r))
    for ing in ev.get("ingredients", []):
        print(C("dim", "ingredient: ")
              + f'{ing.get("artifact_id", "?")} @ {ing.get("version", "?")}'
              + C("dim", f'  ({ing.get("artifact", "")})'))
    for edge in ev.get("parents", [])[1:]:
        print(C("dim", "parent: ")
              + f'{edge.get("version", "?")} ({edge.get("event_id", "?")})')
    print()
    tagcolor = {"added": "add", "modified": "accent", "moved": "move"}
    for b in v["blocks"]:
        c = chg_by_id.get(b["id"])
        text = B(b["text"]) if b["type"] == "heading" else md_term(b["text"])
        if c:
            color = tagcolor[c["kind"]]
            print(f'{C(color, "▍ " + c["kind"])} {C("dim", "(" + b["id"] + ")")}')
            for ln in text.splitlines():
                print(f'{C(color, "▍")} {ln}')
        else:
            print(text)
        print()


def cmd_verify(a):
    """Check the author's structured claims against the computed diff.

    Deterministic data comparison — same inputs, same verdict, no model in
    the loop. Exit codes: 0 all claims check out, 1 mismatch/undisclosed,
    2 version carries no claims (unverifiable)."""
    if os.path.isfile(a.file):
        inspection = inspect_result(a.file)
        if inspection["policy"] == "portable" and inspection["status"] != "ok":
            if a.json:
                print(json.dumps({"artifact": a.file, "status": "capsule_mismatch",
                                  "errors": inspection["errors"]},
                                 ensure_ascii=False, indent=2))
            elif a.md:
                print("⚠️ **capsule mismatch** — " + ", ".join(inspection["errors"]))
            else:
                print(f"verify {a.file}")
                print("  capsule mismatch: " + ", ".join(inspection["errors"]))
            sys.exit(1)
    evs = versions_of(a.file)
    if not evs:
        raise SystemExit("artifact not in ledger")
    ev = _find(evs, a.version) if a.version else evs[0]
    n = len(evs) - next(
        i for i, e in enumerate(evs)
        if e.get("event_id") == ev.get("event_id"))
    # ``verify file`` means the current worktree as well as the recorded
    # claims. ``verify file <version>`` remains an historical claim check.
    if (os.path.isfile(a.file) and not a.version and
            inspection["status"] != "ok"):
        if a.json:
            print(json.dumps({"artifact": a.file, "version": ev["version"],
                              "status": "worktree_mismatch",
                              "errors": inspection["errors"],
                              "ledger_head": inspection.get("ledger_head"),
                              "observed_version": inspection.get("observed_version")},
                             ensure_ascii=False, indent=2))
        elif a.md:
            print("⚠️ **worktree mismatch** — " + ", ".join(inspection["errors"]))
        else:
            print(f"verify {a.file} @ {ev['version']} (v{n})")
            print("  worktree mismatch: " + ", ".join(inspection["errors"]))
            if inspection.get("ledger_head"):
                observed = inspection.get("observed_version") or "unrecorded/unknown"
                print(f"  ledger head: {inspection['ledger_head']} (worktree: {observed})")
            if "unmanaged_worktree" in inspection["errors"]:
                print(f"  action: run `proofpress identify {a.file}`; reconcile the file before snapshotting")
            else:
                print("  action: restore or reconcile the ledger head; snapshot only if this edit is intentional")
        sys.exit(1)
    computed = {c["block"]: c for c in ev.get("changes", [])}
    claims = ev.get("claims")
    if claims is None:
        if a.md:
            print("⚪ _no claims recorded for this version (snapshot ran without --claims)_")
        elif a.json:
            print(json.dumps({"artifact": a.file, "version": ev["version"],
                              "status": "no_claims"}, ensure_ascii=False))
        else:
            print(f'verify {a.file} @ {ev["version"]} (v{n})')
            print(C("dim", "  no claims recorded for this version "
                           "(snapshot ran without --claims) — nothing to verify"))
        sys.exit(2)
    results, claimed_ids = [], set()
    for cl in claims:
        bid = cl.get("block", "")
        claimed_ids.add(bid)
        comp = computed.get(bid)
        if cl.get("kind") == "unchanged":
            ok = comp is None
        else:
            ok = comp is not None and comp["kind"] == cl.get("kind")
        results.append({"claim": cl, "computed": comp, "ok": ok})
    undisclosed = [c for bid, c in computed.items() if bid not in claimed_ids]
    n_ok = sum(1 for r in results if r["ok"])
    n_bad = len(results) - n_ok
    status = "verified" if not n_bad and not undisclosed else "mismatch"
    if a.md:
        # yellow/red only shows up here — a real alarm, never decoration
        if status == "verified":
            print(f"🟢 **claims verified** ({len(results)} claims, deterministic check)")
        else:
            print(f"⚠️ **claim mismatch** — {n_bad} claim(s) do not match the computed diff; "
                  f"{len(undisclosed)} undisclosed change(s)")
        sys.exit(0 if status == "verified" else 1)
    if a.json:
        print(json.dumps({"artifact": a.file, "version": ev["version"], "v": n,
                          "status": status, "results": results,
                          "undisclosed": undisclosed}, ensure_ascii=False, indent=2))
    else:
        ver = ev["version"]
        print(f'verify {B(a.file)} ' + C("dim", f"@ {ver} (v{n})"))
        print()
        for r in results:
            cl, comp = r["claim"], r["computed"]
            ctx = (comp or {}).get("context", "")
            note = f' — "{cl["note"]}"' if cl.get("note") else ""
            if r["ok"]:
                what = cl.get("kind")
                label = verify_label(comp, cl.get("block", "?"))
                print(f'  {C("add", "✓")} [{what}] {label} '
                      f'{C("dim", "(" + cl.get("block", "?") + ")")}{C("dim", note)}')
            else:
                actual = comp["kind"] if comp else "unchanged"
                print(f'  {C("move", "⚠")} claimed {B(cl.get("kind", "?"))} but computed '
                      f'{B(actual)}: {verify_label(comp, "?")} {C("dim", "(" + cl.get("block", "?") + ")")}{C("dim", note)}')
        for c in undisclosed:
            print(f'  {C("move", "⚠")} undisclosed change: [{c["kind"]}] '
                  f'{verify_label(c, "?")} {C("dim", "(" + c["block"] + ")")}')
        print()
        verdict = (C("add", f"{n_ok} verified") if not n_bad and not undisclosed
                   else C("move", f"{n_ok} verified, {n_bad} mismatch, {len(undisclosed)} undisclosed"))
        print(f"  {verdict}")
    sys.exit(0 if status == "verified" else 1)


def cmd_provenance_create(a):
    context = None
    if a.context:
        with open(a.context, encoding="utf-8") as stream:
            context = json.load(stream)
        if not isinstance(context, dict):
            raise proofpress_evidence.EvidenceError(
                "provenance context must be a JSON object")
    envelope = proofpress_evidence.create_evidence(
        a.file, level=a.level, provider_id=a.provider,
        adapter_id=a.adapter, context=context)
    payload = proofpress_evidence.dump_evidence(envelope)
    if a.output:
        with open(a.output, "w", encoding="utf-8") as stream:
            stream.write(payload)
        print(f"provenance evidence written: {a.output}")
    else:
        print(payload, end="")


def cmd_provenance_verify(a):
    with open(a.evidence, encoding="utf-8") as stream:
        envelope = json.load(stream)
    result = proofpress_evidence.verify_evidence(a.file, envelope)
    if a.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        verdict = "verified" if result.ok else "failed"
        verdict_color = "add" if result.ok else "del"
        print(
            f"provenance {C(verdict_color, verdict, bold=True)}: {B(a.file)} "
            f"{C('dim', f'({result.level}; {result.provider}; {result.adapter})')}")
        for check in result.checks:
            check_color = "add" if check["status"] == "passed" else "del"
            print(
                f"  {C(check_color, check['status'])}: "
                f"{C('dim', check['type'])}")
    sys.exit(0 if result.ok else 1)


def main():
    p = argparse.ArgumentParser(prog="proofpress")
    p.add_argument("--version", action="version",
                   version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("snapshot"); s.add_argument("file")
    s.add_argument("--author", default="unknown"); s.add_argument("--kind", default="human", choices=["human", "agent", "system"])
    s.add_argument("--session", default=None); s.add_argument("--note", default=None)
    s.add_argument("--base-version", default=None,
                   help="refuse the snapshot unless this is the current head")
    s.add_argument("--base-event", default=None,
                   help="refuse the snapshot unless this is the exact DAG head event")
    s.add_argument("--claims", default=None,
                   help='JSON file: [{"block", "kind": added|removed|modified|moved|unchanged, "note"?}]')
    s.add_argument("--why", default=None,
                   help="decision context: why this change was made (recorded as testimony)")
    s.add_argument("--rejected", action="append", default=None, metavar="OPTION — REASON",
                   help="an alternative considered and rejected (repeatable)")
    s.add_argument("--requested-by", action="append", default=None)
    s.add_argument("--produced-by", action="append", default=None)
    s.add_argument("--edited-by", action="append", default=None)
    s.add_argument("--recorded-by", action="append", default=None)
    s.add_argument("--attribution-basis", choices=ATTRIBUTION_BASES,
                   default="self_asserted")
    s.set_defaults(f=cmd_snapshot)
    l = sub.add_parser("log"); l.add_argument("file")
    l.add_argument("--json", action="store_true"); l.set_defaults(f=cmd_log)
    d = sub.add_parser("diff"); d.add_argument("file")
    d.add_argument("va", nargs="?"); d.add_argument("vb", nargs="?")
    d.add_argument("--json", action="store_true")
    d.add_argument("--md", action="store_true",
                   help="markdown output (PR-comment section; used by the Action)")
    d.add_argument("--base-commit", default=None, metavar="SHA",
                   help="pick the from-version by its source git commit (fallback: last change)")
    d.set_defaults(f=cmd_diff)
    vf = sub.add_parser("verify"); vf.add_argument("file")
    vf.add_argument("version", nargs="?")
    vf.add_argument("--json", action="store_true")
    vf.add_argument("--md", action="store_true",
                    help="one-line markdown verdict (used by the Action)")
    vf.set_defaults(f=cmd_verify)
    an = sub.add_parser("anchor"); an.add_argument("file"); an.set_defaults(f=cmd_anchor)
    ig = sub.add_parser("ingest"); ig.add_argument("file"); ig.set_defaults(f=cmd_ingest)
    mp = sub.add_parser(
        "merge-plan",
        help="analyze parallel copies of one portable artifact without writing")
    mp.add_argument("file", help="primary/target copy")
    mp.add_argument("--from", dest="source", action="append", required=True,
                    metavar="COPY", help="parallel copy (repeatable)")
    mp.add_argument("--json", action="store_true")
    mp.set_defaults(f=cmd_merge_plan)
    mg = sub.add_parser(
        "merge",
        help="record a resolved multi-parent merge of one portable artifact")
    mg.add_argument("file", help="resolved target; its embedded head is primary")
    mg.add_argument("--from", dest="source", action="append", required=True,
                    metavar="COPY", help="other parallel copy (repeatable)")
    mg.add_argument("--author", default="unknown")
    mg.add_argument("--kind", default="human",
                    choices=["human", "agent", "system"])
    mg.add_argument("--session", default=None); mg.add_argument("--note", default=None)
    mg.add_argument("--claims", default=None)
    mg.add_argument("--why", default=None)
    mg.add_argument("--rejected", action="append", default=None)
    mg.add_argument("--requested-by", action="append", default=None)
    mg.add_argument("--produced-by", action="append", default=None)
    mg.add_argument("--edited-by", action="append", default=None)
    mg.add_argument("--recorded-by", action="append", default=None)
    mg.add_argument("--attribution-basis", choices=ATTRIBUTION_BASES,
                    default="self_asserted")
    mg.set_defaults(f=cmd_merge)
    ml = sub.add_parser("merge-lineage",
                        help="snapshot a file that merges other Proofpress artifacts, recording ingredient references")
    ml.add_argument("file")
    ml.add_argument("--from", dest="source", action="append", required=True,
                    metavar="ARTIFACT", help="upstream artifact merged into this file (repeatable)")
    ml.add_argument("--author", default="unknown")
    ml.add_argument("--kind", default="human", choices=["human", "agent", "system"])
    ml.add_argument("--session", default=None); ml.add_argument("--note", default=None)
    ml.add_argument("--base-version", default=None)
    ml.add_argument("--claims", default=None)
    ml.add_argument("--why", default=None)
    ml.add_argument("--rejected", action="append", default=None)
    ml.add_argument("--requested-by", action="append", default=None)
    ml.add_argument("--produced-by", action="append", default=None)
    ml.add_argument("--edited-by", action="append", default=None)
    ml.add_argument("--recorded-by", action="append", default=None)
    ml.add_argument("--attribution-basis", choices=ATTRIBUTION_BASES,
                    default="self_asserted")
    ml.set_defaults(f=cmd_merge_lineage)
    idn = sub.add_parser("identify",
                         help="recognize a stripped file by its soft-binding fingerprint")
    idn.add_argument("file")
    idn.add_argument("--json", action="store_true"); idn.set_defaults(f=cmd_identify)
    ex = sub.add_parser("export"); ex.add_argument("file")
    ex.add_argument("-o", "--output", default=None); ex.set_defaults(f=cmd_export)
    ini = sub.add_parser("init"); ini.set_defaults(f=cmd_init)
    sy = sub.add_parser("sync"); sy.set_defaults(f=cmd_sync)
    b = sub.add_parser("blocks"); b.add_argument("file")
    b.add_argument("version", nargs="?"); b.set_defaults(f=cmd_blocks)
    sh = sub.add_parser("show"); sh.add_argument("ref", metavar="file-or-version")
    sh.add_argument("--json", action="store_true"); sh.set_defaults(f=cmd_show)
    po = sub.add_parser("policy"); po.add_argument("file")
    po.add_argument("policy", nargs="?", choices=POLICIES)
    po.add_argument("--author", default="unknown")
    po.add_argument("--attribution-basis", choices=ATTRIBUTION_BASES,
                    default="self_asserted")
    po.set_defaults(f=cmd_policy)
    ins = sub.add_parser("inspect"); ins.add_argument("file")
    ins.add_argument("--json", action="store_true"); ins.set_defaults(f=cmd_inspect)
    imp = sub.add_parser("import"); imp.add_argument("file"); imp.set_defaults(f=cmd_import)
    cl = sub.add_parser("clean"); cl.add_argument("file")
    cl.add_argument("-o", "--output", required=True); cl.set_defaults(f=cmd_clean)
    ca = sub.add_parser("capture")
    ca.add_argument("--recorder", required=True); ca.add_argument("--session", default=None)
    ca.add_argument("files", nargs="*",
                    help="specific Markdown/HTML files to reconcile; "
                         "default: Git candidates plus admitted ledger paths")
    ca.set_defaults(f=cmd_capture)
    pr = sub.add_parser(
        "provenance",
        help="create or verify format-aware artifact evidence")
    prs = pr.add_subparsers(dest="provenance_cmd", required=True)
    pc = prs.add_parser(
        "create", help="create the strongest built-in evidence for a file")
    pc.add_argument("file")
    pc.add_argument("-o", "--output", default=None)
    pc.add_argument("--level", default=proofpress_evidence.AUTO_LEVEL,
                    choices=(proofpress_evidence.AUTO_LEVEL,
                             *proofpress_evidence.VERIFICATION_LEVELS),
                    help="verification level; auto selects semantic for DOCX")
    pc.add_argument("--provider", default=None,
                    help="provider ID; default follows the selected adapter")
    pc.add_argument("--adapter", default=None)
    pc.add_argument("--context", default=None, metavar="JSON_FILE",
                    help="optional work/outcome identifiers as a JSON object")
    pc.set_defaults(f=cmd_provenance_create)
    pv = prs.add_parser(
        "verify", help="verify byte or semantic evidence against a file")
    pv.add_argument("file")
    pv.add_argument("--evidence", required=True)
    pv.add_argument("--json", action="store_true")
    pv.set_defaults(f=cmd_provenance_verify)
    a = p.parse_args()
    try:
        a.f(a)
    except proofpress_evidence.EvidenceError as exc:
        p.error(str(exc))


if __name__ == "__main__":
    main()
