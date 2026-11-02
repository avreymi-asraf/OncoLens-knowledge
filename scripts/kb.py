#!/usr/bin/env -S uv run --quiet
"""kb.py - the deterministic gatekeeper of the knowledge repo.

The LLM proposes; this script decides what is valid. Standard library only,
except `pypdf` for PDF text extraction (installed by the SessionStart hook).

Commands (run `uv run scripts/kb.py <cmd> -h` for options):

  register              Register new files in sources/raw/: hash + extract text.
  check [--strict]      Validate the whole repo. Exit 1 on any error.
  index                 Rebuild cortex/_index/ (catalog.md, graph.json, search.db).
  preflight [SRC]       Context for an ingest: source info + similar nodes.
  search QUERY          BM25 search. Returns path:lines + snippet, never whole files.
  nav NODE              Incoming and outgoing edges of a node, with annotations.
  distractor NODE MECH  Most word-similar node NOT linked to the mechanism.
  hubs                  Mechanisms with too many incoming links.
  pairs                 Claim/evidence pairs awaiting verification (no draft text).
  verdict CLAIM V       Record a verification verdict: pass | partial | fail.
  mark-ingested SRC     Mark a source as ingested in the manifest.
  log MESSAGE           Append a line to cortex/log.md.
  hook-post-write       Claude Code PostToolUse hook (reads JSON on stdin).
  hook-subagent-stop    Claude Code SubagentStop hook for the ingestor.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html.parser
import json
import os
import re
import sqlite3
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------
# Paths and vocabulary
# --------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
SRC_RAW = ROOT / "sources" / "raw"
SRC_TEXT = ROOT / "sources" / "text"
MANIFEST = ROOT / "sources" / "manifest.json"
CORTEX = ROOT / "cortex"
INDEX_DIR = CORTEX / "_index"
LOG = CORTEX / "log.md"
MISSES = INDEX_DIR / "search-misses.log"
DB = INDEX_DIR / "search.db"
STOP_STATE = INDEX_DIR / ".stop-attempts"

# folder -> type name used in frontmatter
TYPES = {
    "claims": "claim",
    "mechanisms": "mechanism",
    "concepts": "concept",
    "tensions": "tension",
    "questions": "question",
}
STATUSES = {
    "claim": {"proposed", "supported", "disputed", "superseded"},
    "mechanism": {"proposed", "supported", "retired"},
    "concept": {"active", "superseded"},
    "tension": {"open", "resolved"},
    "question": {"open", "answered"},
}
REQUIRED_FIELDS = ["type", "status", "created", "description"]
PREDICATES = {
    "derived_from",          # node -> source (claims need a quote under it)
    "supports",
    "contradicts",
    "supersedes",
    "implements_mechanism",  # claim/concept -> mechanism
    "isomorphic_to",         # mechanism <-> mechanism, or node <-> node
    "breaks_under",
    "raises",                # node -> question
    "relates_to",            # weakest link; still needs an annotation
}
VERDICTS = {"pending", "pass", "partial", "fail"}
MECH_SECTIONS = ["Structure", "Instances", "Candidate inference", "Breaks when", "Distractor check"]
MECH_STRUCTURE_KEYS = ["regulated", "driver", "causal_link"]
HUB_THRESHOLD = 8
MAX_STOP_ATTEMPTS = 5
DESC_MAX = 200

REL_RE = re.compile(r"^- ([a-z_]+)::\[\[([^\]]+)\]\]\s*$")
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
WORD_RE = re.compile(r"\w+", re.UNICODE)
PLACEHOLDER_RE = re.compile(r"\(?\s*(pending|todo|tbd|n/?a|none|-+|\.\.\.|<[^>]*>)\s*\)?\.?", re.I)
STOPWORDS = set(
    "the a an and or of to in on for with by is are was were be been this that these those it its as at "
    "from not but if then so than such can could would should may might will which who what when where how "
    "into about over under between more most less also there their they them we our you your he she his her "
    "do does did done has have had very just only other some any each all one two three new use used using".split()
)


def today() -> str:
    return dt.date.today().isoformat()


def rel(p: Path) -> str:
    return p.resolve().relative_to(ROOT).as_posix()


# --------------------------------------------------------------------------
# Text normalization (used for quote matching and search)
# --------------------------------------------------------------------------

_QUOTE_MAP = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "–": "-",
                            "—": "-", " ": " ", "״": '"', "׳": "'"})


def norm(s: str) -> str:
    s = s.translate(_QUOTE_MAP)
    s = re.sub(r"-\s*\n\s*", "", s)  # re-join words hyphenated across lines (PDF extraction)
    s = re.sub(r"\s+", " ", s)
    return s.strip().casefold()


def quote_found(quote: str, text_norm: str) -> bool:
    """A quote may elide text with '...' or '…'; segments must appear in order."""
    parts = [norm(p) for p in re.split(r"\.\.\.|…", quote)]
    parts = [p.strip(" \"'") for p in parts if p.strip(" \"'")]
    if not parts:
        return False
    pos = 0
    for p in parts:
        i = text_norm.find(p, pos)
        if i < 0:
            return False
        pos = i + len(p)
    return True


def terms(s: str) -> list[str]:
    return [w for w in WORD_RE.findall(s.casefold()) if len(w) > 2 and w not in STOPWORDS and not w.isdigit()]


# --------------------------------------------------------------------------
# Manifest and source registration
# --------------------------------------------------------------------------

def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8") or "{}")
    return {}


def save_manifest(m: dict) -> None:
    MANIFEST.write_text(json.dumps(dict(sorted(m.items())), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class _HTMLText(html.parser.HTMLParser):
    SKIP = {"script", "style", "noscript"}
    BLOCK = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "section", "article", "pre"}

    def __init__(self):
        super().__init__()
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def extract_text(p: Path) -> str:
    ext = p.suffix.lower()
    if ext in {".md", ".txt", ".markdown", ".rst", ".csv", ".json", ".srt", ".vtt"}:
        return p.read_text(encoding="utf-8", errors="replace")
    if ext in {".html", ".htm"}:
        parser = _HTMLText()
        parser.feed(p.read_text(encoding="utf-8", errors="replace"))
        text = "".join(parser.out)
        return re.sub(r"\n\s*\n\s*\n+", "\n\n", text).strip() + "\n"
    if ext == ".pdf":
        try:
            from pypdf import PdfReader  # type: ignore
        except ImportError:
            raise SystemExit(f"cannot extract {rel(p)}: pypdf is missing - run: uv sync")
        reader = PdfReader(str(p))
        pages = []
        for i, page in enumerate(reader.pages, 1):
            pages.append(f"<!-- page {i} -->\n{page.extract_text() or ''}")
        return "\n\n".join(pages) + "\n"
    raise SystemExit(f"cannot extract {rel(p)}: unsupported extension '{ext}' (convert it to .md first)")


TEXT_EXTS = {".md", ".markdown", ".txt", ".rst", ".html", ".htm", ".pdf", ".csv", ".json", ".srt", ".vtt"}


def folder_main_file(d: Path) -> Path | None:
    """A folder source (e.g. a saved web page) has one main document; the rest are assets.
    Main = the document named after the folder, else the only document at the folder's top level."""
    docs = [p for p in d.iterdir() if p.is_file() and not p.name.startswith(".") and p.suffix.lower() in TEXT_EXTS]
    named = [p for p in docs if p.stem.lower() == d.name.lower()]
    if len(named) == 1:
        return named[0]
    if len(docs) == 1:
        return docs[0]
    return None


def raw_files() -> list[Path]:
    """One path per source: plain files in sources/raw/, plus the main document of each folder."""
    if not SRC_RAW.exists():
        return []
    out = []
    for p in SRC_RAW.iterdir():
        if p.name.startswith(".") or ":" in p.name:  # skip dotfiles and Windows Zone.Identifier streams
            continue
        if p.is_file():
            out.append(p)
        elif p.is_dir():
            main = folder_main_file(p)
            if main is None:
                print(f"warning: skipped folder {rel(p)}: no single main document "
                      f"(name it {p.name}.md or keep one document at its top level)", file=sys.stderr)
            else:
                out.append(main)
    return sorted(out)


def source_id(p: Path) -> str:
    # A folder source is named after its folder; a plain file after its stem.
    return p.parent.name if p.parent != SRC_RAW else p.stem


def cmd_register(args=None, quiet=False) -> list[str]:
    m = load_manifest()
    added = []
    SRC_TEXT.mkdir(parents=True, exist_ok=True)
    for p in raw_files():
        sid = source_id(p)
        if sid in m:
            continue
        text = extract_text(p)
        (SRC_TEXT / f"{sid}.md").write_text(text, encoding="utf-8")
        m[sid] = {
            "raw": rel(p),
            "text": rel(SRC_TEXT / f"{sid}.md"),
            "sha256": sha256(p),
            "added": today(),
            "ingested": False,
        }
        added.append(sid)
    if added:
        save_manifest(m)
    if not quiet:
        print("registered: " + (", ".join(added) if added else "(nothing new)"))
    return added


# --------------------------------------------------------------------------
# Node parsing
# --------------------------------------------------------------------------

@dataclass
class Rel:
    pred: str
    target: str
    line: int
    notes: list[str] = field(default_factory=list)   # "  - annotation" lines
    quotes: list[str] = field(default_factory=list)  # "  > quote" lines


@dataclass
class Node:
    path: Path
    id: str              # e.g. "claims/foo"
    folder: str
    fm: dict
    body: str
    title: str
    rels: list[Rel]
    sections: dict[str, str]
    fm_error: str | None = None


def node_id_for(p: Path) -> str:
    return p.relative_to(CORTEX).with_suffix("").as_posix()


def parse_node(p: Path) -> Node:
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines()
    fm, fm_error, body_start = {}, None, 0
    if lines and lines[0].strip() == "---":
        try:
            end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
        except StopIteration:
            fm_error = "frontmatter has no closing '---'"
            end = 0
        for ln in lines[1:end]:
            if not ln.strip():
                continue
            if ":" not in ln:
                fm_error = f"bad frontmatter line: {ln!r}"
                continue
            k, v = ln.split(":", 1)
            fm[k.strip()] = v.strip()
        body_start = end + 1
    else:
        fm_error = "missing frontmatter (file must start with '---')"
    body_lines = lines[body_start:]
    title = next((ln[2:].strip() for ln in body_lines if ln.startswith("# ")), "")

    sections: dict[str, str] = {}
    cur = None
    buf: list[str] = []
    for ln in body_lines:
        if ln.startswith("## "):
            if cur is not None:
                sections[cur] = "\n".join(buf).strip()
            cur, buf = ln[3:].strip(), []
        elif cur is not None:
            buf.append(ln)
    if cur is not None:
        sections[cur] = "\n".join(buf).strip()

    rels: list[Rel] = []
    last: Rel | None = None
    for i, ln in enumerate(lines, 1):
        m = REL_RE.match(ln.rstrip())
        if m:
            last = Rel(m.group(1), m.group(2).strip(), i)
            rels.append(last)
            continue
        if last and ln.startswith(("  ", "\t")) and ln.strip():
            s = ln.strip()
            if s.startswith(">"):
                last.quotes.append(s[1:].strip())
            elif s.startswith("- "):
                last.notes.append(s[2:].strip())
            continue
        if ln.strip():
            last = None
    folder = p.relative_to(CORTEX).parts[0]
    return Node(p, node_id_for(p), folder, fm, "\n".join(body_lines), title, rels, sections, fm_error)


def cortex_files() -> list[Path]:
    out = []
    for folder in TYPES:
        d = CORTEX / folder
        if d.exists():
            out.extend(sorted(d.rglob("*.md")))
    return out


def load_nodes() -> dict[str, Node]:
    return {n.id: n for n in (parse_node(p) for p in cortex_files())}


def resolve_target(t: str, nodes: dict[str, Node], manifest: dict) -> tuple[str, str] | None:
    """Return (kind, key): kind is 'node' or 'source'."""
    t = t.split("|")[0].strip().removesuffix(".md")
    if t.startswith("sources/"):
        sid = t.split("/", 1)[1]
        return ("source", sid) if sid in manifest else None
    if t.startswith("cortex/"):
        t = t[len("cortex/"):]
    return ("node", t) if t in nodes else None


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def validate_node(n: Node, nodes: dict[str, Node], manifest: dict, text_cache: dict) -> list[str]:
    errs: list[str] = []
    where = rel(n.path)

    def e(msg):
        errs.append(f"{where}: {msg}")

    if n.fm_error:
        e(n.fm_error)
    expected_type = TYPES.get(n.folder)
    for k in REQUIRED_FIELDS:
        if not n.fm.get(k):
            e(f"missing frontmatter field '{k}'")
    if n.fm.get("type") and n.fm["type"] != expected_type:
        e(f"type is '{n.fm['type']}' but files in {n.folder}/ must have type '{expected_type}'")
    st = n.fm.get("status")
    if st and expected_type and st not in STATUSES[expected_type]:
        e(f"status '{st}' not allowed for {expected_type}; use one of {sorted(STATUSES[expected_type])}")
    desc = n.fm.get("description", "")
    if len(desc) > DESC_MAX:
        e(f"description is {len(desc)} chars; keep it to one line under {DESC_MAX}")
    if n.fm.get("created") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", n.fm["created"]):
        e("created must be YYYY-MM-DD")
    if not n.title:
        e("missing '# Title' line")

    # every [[link]] anywhere in the file must resolve
    for m in LINK_RE.finditer(n.body):
        if resolve_target(m.group(1), nodes, manifest) is None:
            e(f"broken link [[{m.group(1)}]]")

    for r in n.rels:
        if r.pred not in PREDICATES:
            e(f"line {r.line}: unknown predicate '{r.pred}::' (allowed: {', '.join(sorted(PREDICATES))})")
            continue
        target = resolve_target(r.target, nodes, manifest)
        if target is None:
            continue  # already reported as broken link
        if not r.notes and not r.quotes:
            e(f"line {r.line}: '{r.pred}::[[{r.target}]]' needs an indented '  - why' line under it")
        if r.pred == "derived_from" and target[0] != "source":
            e(f"line {r.line}: derived_from must point to [[sources/<id>]]")
        if r.pred in {"implements_mechanism"} and not target[1].startswith("mechanisms/"):
            e(f"line {r.line}: implements_mechanism must point to a mechanisms/ node")
        if r.quotes and target[0] == "source":
            sid = target[1]
            if sid not in text_cache:
                tp = ROOT / manifest[sid]["text"]
                text_cache[sid] = norm(tp.read_text(encoding="utf-8")) if tp.exists() else ""
            for q in r.quotes:
                if not quote_found(q, text_cache[sid]):
                    e(f"line {r.line}: quote not found verbatim in sources/text/{sid}.md: {q[:80]!r}")

    if expected_type == "claim":
        derived = [r for r in n.rels if r.pred == "derived_from"]
        if not derived:
            e("a claim needs at least one 'derived_from::[[sources/<id>]]'")
        elif not any(r.quotes for r in derived):
            e("a claim needs at least one verbatim quote ('  > ...') under a derived_from")
        v = n.fm.get("verified")
        if v not in VERDICTS:
            e(f"claims need 'verified:' in frontmatter, one of {sorted(VERDICTS)}")
        if v == "fail" and st not in {"disputed", "superseded"}:
            e("verified: fail requires status: disputed")

    if expected_type == "mechanism":
        if n.fm.get("kind") not in {"explanatory", "generative"}:
            e("mechanisms need 'kind: explanatory' or 'kind: generative'")
        for sec in MECH_SECTIONS:
            content = n.sections.get(sec, "")
            if not content:
                e(f"mechanism is missing a non-empty '## {sec}' section")
            elif PLACEHOLDER_RE.fullmatch(content.strip()):
                e(f"'## {sec}' still holds a placeholder ({content.strip()[:40]!r}); fill it or drop the mechanism")
        structure = n.sections.get("Structure", "")
        for k in MECH_STRUCTURE_KEYS:
            if not re.search(rf"^- {k}:\s*\S", structure, re.M):
                e(f"'## Structure' needs a '- {k}: ...' line")
        rows = [ln for ln in n.sections.get("Instances", "").splitlines() if ln.strip().startswith("|")]
        data_rows = [r for r in rows[2:]] if len(rows) >= 2 else []
        cols = len([c for c in rows[0].strip().strip("|").split("|")]) if rows else 0
        if cols < 3 or len(data_rows) < 2:
            e("'## Instances' needs a mapping table: a role column plus >=2 instance columns, and >=2 rows")
        else:
            mapped = []
            for r in data_rows:
                cells = [c.strip() for c in r.strip().strip("|").split("|")]
                if any(not c for c in cells):
                    e(f"'## Instances' row has an empty cell: {r.strip()[:60]}")
                mapped.append(cells[1:])
            # one-to-one: within each instance column, no element may fill two roles
            for col in zip(*mapped):
                dup = [x for x, c in Counter(x.casefold() for x in col).items() if c > 1 and x]
                if dup:
                    e(f"'## Instances' is not one-to-one: '{dup[0]}' fills two roles in one instance")

    if expected_type == "tension":
        sides = [r for r in n.rels if r.pred in {"supports", "contradicts", "derived_from"}]
        if len(sides) < 2:
            e("a tension needs at least two sides (supports/contradicts/derived_from links)")
    return errs


def validate_sources(manifest: dict) -> list[str]:
    errs = []
    on_disk = {source_id(p): p for p in raw_files()}
    for sid, p in on_disk.items():
        if sid not in manifest:
            errs.append(f"{rel(p)}: not registered (run: uv run scripts/kb.py register)")
    for sid, meta in manifest.items():
        rp = ROOT / meta["raw"]
        if not rp.exists():
            errs.append(f"manifest '{sid}': raw file {meta['raw']} is missing (sources are never deleted)")
            continue
        if sha256(rp) != meta["sha256"]:
            errs.append(f"{meta['raw']}: content changed after registration (sources are immutable)")
        if not (ROOT / meta["text"]).exists():
            errs.append(f"manifest '{sid}': text file {meta['text']} is missing")
    return errs


def changed_paths() -> set[str]:
    """Files changed vs HEAD, staged or not, plus untracked. Empty if not a git repo."""
    out = set()
    for cmd in (["git", "diff", "--name-only", "HEAD"], ["git", "ls-files", "--others", "--exclude-standard"]):
        try:
            res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
            out.update(x.strip() for x in res.stdout.splitlines() if x.strip())
        except FileNotFoundError:
            pass
    return out


def run_check(strict=False) -> list[str]:
    manifest = load_manifest()
    nodes = load_nodes()
    errs = validate_sources(manifest)
    cache: dict = {}
    for n in nodes.values():
        errs.extend(validate_node(n, nodes, manifest, cache))
    if strict:
        changed = changed_paths()
        for n in nodes.values():
            if rel(n.path) in changed and n.fm.get("type") == "claim" and n.fm.get("verified") == "pending":
                errs.append(f"{rel(n.path)}: claim is still 'verified: pending' - run the verifier "
                            f"(uv run scripts/kb.py pairs) before finishing")
    return errs


def cmd_check(args) -> int:
    errs = run_check(strict=args.strict)
    if errs:
        print(f"kb check: {len(errs)} error(s)", file=sys.stderr)
        for x in errs:
            print("  - " + x, file=sys.stderr)
        return 1
    print("kb check: OK")
    return 0


# --------------------------------------------------------------------------
# Index: catalog, graph, FTS5 search db
# --------------------------------------------------------------------------

def build_graph(nodes, manifest) -> dict:
    edges = []
    for n in nodes.values():
        for r in n.rels:
            t = resolve_target(r.target, nodes, manifest)
            if t is None or r.pred not in PREDICATES:
                continue
            key = t[1] if t[0] == "node" else f"sources/{t[1]}"
            edges.append({"from": n.id, "pred": r.pred, "to": key,
                          "note": (r.notes[0] if r.notes else (r.quotes[0] if r.quotes else ""))})
    return {
        "nodes": {nid: {"type": n.fm.get("type"), "status": n.fm.get("status"),
                        "description": n.fm.get("description", ""), "title": n.title}
                  for nid, n in sorted(nodes.items())},
        "sources": {sid: {"ingested": m["ingested"], "raw": m["raw"]} for sid, m in sorted(manifest.items())},
        "edges": sorted(edges, key=lambda x: (x["from"], x["pred"], x["to"])),
    }


def write_catalog(nodes, manifest) -> None:
    out = ["# Catalog", "", "Generated by `scripts/kb.py index`. Do not edit by hand.",
           "One line per node: link, status, description. Read this first; then search, nav, read.", ""]
    for folder, typ in TYPES.items():
        items = [n for n in nodes.values() if n.folder == folder]
        out.append(f"## {folder} ({len(items)})")
        for n in sorted(items, key=lambda n: n.id):
            extra = f", {n.fm.get('kind')}" if typ == "mechanism" else ""
            extra += f", verified: {n.fm.get('verified')}" if typ == "claim" else ""
            out.append(f"- [[{n.id}]] ({n.fm.get('status', '?')}{extra}) - {n.fm.get('description', '')}")
        out.append("")
    pending = [s for s, m in manifest.items() if not m["ingested"]]
    out.append(f"## sources ({len(manifest)}, not yet ingested: {len(pending)})")
    for sid, m in sorted(manifest.items()):
        out.append(f"- [[sources/{sid}]] {'ingested' if m['ingested'] else 'NOT INGESTED'} - {m['raw']}")
    out.append("")
    (INDEX_DIR / "catalog.md").write_text("\n".join(out), encoding="utf-8")


def chunks(text: str, max_chars=900):
    """Yield (start_line, end_line, text) chunks split on blank lines / headings."""
    lines = text.splitlines()
    start, buf = 1, []
    size = 0
    for i, ln in enumerate(lines, 1):
        boundary = (not ln.strip()) or ln.startswith("#")
        if buf and boundary and size >= max_chars // 3 or size >= max_chars:
            yield start, i - 1, "\n".join(buf)
            start, buf, size = i, [], 0
        buf.append(ln)
        size += len(ln) + 1
    if buf and "".join(buf).strip():
        yield start, len(lines), "\n".join(buf)


def build_db(nodes, manifest) -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.execute("CREATE VIRTUAL TABLE docs USING fts5(path UNINDEXED, kind UNINDEXED, l0 UNINDEXED, "
                "l1 UNINDEXED, title, body, tokenize='unicode61 remove_diacritics 2')")
    rows = []
    for n in nodes.values():
        p = rel(n.path)
        rows.append((p, "cortex-meta", 1, 1, n.title, n.fm.get("description", "")))
        for a, b, t in chunks(n.path.read_text(encoding="utf-8")):
            rows.append((p, "cortex", a, b, n.title, t))
    for sid, m in manifest.items():
        tp = ROOT / m["text"]
        if tp.exists():
            for a, b, t in chunks(tp.read_text(encoding="utf-8")):
                rows.append((m["text"], "source", a, b, sid, t))
    con.executemany("INSERT INTO docs VALUES (?,?,?,?,?,?)", rows)
    con.execute("CREATE TABLE meta (k TEXT PRIMARY KEY, v TEXT)")
    con.execute("INSERT INTO meta VALUES ('fingerprint', ?)", (fingerprint(),))
    con.commit()
    con.close()


def fingerprint() -> str:
    h = hashlib.sha256()
    files = cortex_files() + ([MANIFEST] if MANIFEST.exists() else [])
    for p in sorted(files):
        st = p.stat()
        h.update(f"{rel(p)}:{st.st_size}:{int(st.st_mtime)}".encode())
    return h.hexdigest()


def ensure_db():
    fresh = False
    if DB.exists():
        try:
            con = sqlite3.connect(DB)
            fresh = con.execute("SELECT v FROM meta WHERE k='fingerprint'").fetchone()[0] == fingerprint()
            con.close()
        except sqlite3.Error:
            fresh = False
    if not fresh:
        build_db(load_nodes(), load_manifest())


def cmd_index(args=None) -> int:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    nodes, manifest = load_nodes(), load_manifest()
    (INDEX_DIR / "graph.json").write_text(json.dumps(build_graph(nodes, manifest), indent=1, ensure_ascii=False) + "\n",
                                          encoding="utf-8")
    write_catalog(nodes, manifest)
    build_db(nodes, manifest)
    print(f"kb index: {len(nodes)} nodes, {len(manifest)} sources")
    return 0


# --------------------------------------------------------------------------
# Search and navigation
# --------------------------------------------------------------------------

def fts_query(q: str) -> str:
    toks = [t for t in WORD_RE.findall(q) if len(t) > 1]
    return " OR ".join(f'"{t}"' for t in toks)


def search(q: str, kind: str = "all", k: int = 8, exclude: set[str] | None = None):
    ensure_db()
    fq = fts_query(q)
    if not fq:
        return []
    con = sqlite3.connect(DB)
    where = ""
    if kind == "cortex":
        where = "AND kind IN ('cortex','cortex-meta')"
    elif kind == "sources":
        where = "AND kind='source'"
    rows = con.execute(
        f"SELECT path, kind, l0, l1, title, snippet(docs, 5, '[', ']', ' ... ', 18), bm25(docs, 0, 0, 0, 0, 3.0, 1.0) "
        f"FROM docs WHERE docs MATCH ? {where} ORDER BY bm25(docs, 0, 0, 0, 0, 3.0, 1.0) LIMIT ?",
        (fq, k * 4)).fetchall()
    con.close()
    out, seen = [], set()
    for path, kd, a, b, title, snip, score in rows:
        if exclude and path in exclude:
            continue
        key = (path, a)
        if key in seen:
            continue
        seen.add(key)
        out.append({"path": path, "lines": f"{a}-{b}", "kind": kd, "title": title,
                    "snippet": re.sub(r"\s+", " ", snip).strip(), "score": round(score, 2)})
        if len(out) >= k:
            break
    return out


def cmd_search(args) -> int:
    res = search(args.query, args.kind, args.k)
    if not res:
        MISSES.parent.mkdir(parents=True, exist_ok=True)
        with MISSES.open("a", encoding="utf-8") as f:
            f.write(f"{today()}\t{args.kind}\t{args.query}\n")
        print("no results (logged to cortex/_index/search-misses.log)")
        return 0
    for r in res:
        print(f"{r['path']}:{r['lines']}  [{r['kind']}]  {r['title']}")
        print(f"    {r['snippet']}")
    return 0


def find_node(name: str, nodes: dict[str, Node]) -> Node:
    key = name.removesuffix(".md").removeprefix("cortex/").strip("[]")
    if key in nodes:
        return nodes[key]
    cands = [n for nid, n in nodes.items() if nid.endswith("/" + key) or nid.split("/")[-1] == key]
    if len(cands) == 1:
        return cands[0]
    raise SystemExit(f"node not found or ambiguous: {name} ({len(cands)} matches)")


def cmd_nav(args) -> int:
    nodes, manifest = load_nodes(), load_manifest()
    n = find_node(args.node, nodes)
    g = build_graph(nodes, manifest)
    print(f"{n.id}  ({n.fm.get('type')}, {n.fm.get('status')})  {n.fm.get('description', '')}")
    print("outgoing:")
    for e in g["edges"]:
        if e["from"] == n.id:
            print(f"  {e['pred']} -> {e['to']}    # {e['note'][:120]}")
    print("incoming:")
    for e in g["edges"]:
        if e["to"] == n.id:
            print(f"  {e['from']} --{e['pred']}->    # {e['note'][:120]}")
    return 0


def top_terms(text: str, k=20) -> str:
    return " ".join(w for w, _ in Counter(terms(text)).most_common(k))


def cmd_distractor(args) -> int:
    nodes, manifest = load_nodes(), load_manifest()
    n = find_node(args.node, nodes)
    mech = find_node(args.mechanism, nodes)
    if mech.folder != "mechanisms":
        raise SystemExit(f"{mech.id} is not a mechanism")
    g = build_graph(nodes, manifest)
    linked = {e["from"] for e in g["edges"] if e["to"] == mech.id} | {e["to"] for e in g["edges"] if e["from"] == mech.id}
    exclude = {rel(nodes[x].path) for x in linked if x in nodes} | {rel(n.path), rel(mech.path)}
    content = re.sub(r"\b[a-z_]+::\[\[[^\]]*\]\]|^#+ |^---$", " ", n.body, flags=re.M)
    content += " " + n.fm.get("description", "")
    res = search(top_terms(content), "cortex", 3, exclude=exclude)
    if not res:
        print("no distractor found (nothing similar in wording outside this mechanism)")
        return 0
    d = res[0]
    print(f"distractor: {d['path']}  ({d['title']})")
    print(f"    {d['snippet']}")
    print("Write one sentence in '## Distractor check' of the mechanism: why the mapping holds for "
          f"{n.id} but NOT for this distractor, despite the shared words.")
    return 0


def cmd_hubs(args) -> int:
    nodes, manifest = load_nodes(), load_manifest()
    g = build_graph(nodes, manifest)
    inc = Counter(e["to"] for e in g["edges"] if e["to"].startswith("mechanisms/"))
    flagged = [(m, c) for m, c in inc.most_common() if c >= args.threshold]
    if not flagged:
        print(f"no mechanism has >= {args.threshold} incoming links")
    for m, c in flagged:
        print(f"{m}: {c} incoming links - check for a catch-all mechanism; split it or tighten its Structure")
    return 0


def cmd_preflight(args) -> int:
    cmd_register(quiet=True)
    m = load_manifest()
    if args.source:
        sid = Path(args.source).stem
        if sid not in m:
            raise SystemExit(f"unknown source '{args.source}'. Put the file in sources/raw/ first.")
    else:
        pending = sorted(s for s, v in m.items() if not v["ingested"])
        if not pending:
            print("PREFLIGHT: every registered source is already ingested. Nothing to do.")
            return 0
        sid = pending[0]
    meta = m[sid]
    text = (ROOT / meta["text"]).read_text(encoding="utf-8")
    n_lines = text.count("\n") + 1
    print(f"# Preflight for source '{sid}'")
    print(f"- raw: {meta['raw']}")
    print(f"- text (quote from THIS file): {meta['text']}  ({n_lines} lines, {len(text)} chars)")
    print(f"- link to it as: [[sources/{sid}]]")
    print(f"- already ingested: {meta['ingested']}")
    others = [s for s, v in m.items() if not v["ingested"] and s != sid]
    if others:
        print(f"- other sources still waiting: {', '.join(sorted(others))}")
    print()
    q = top_terms(text, 25)
    print(f"## Existing nodes most similar to this source (BM25 on: {q[:120]}...)")
    res = search(q, "cortex", 15)
    if not res:
        print("(none - the cortex is empty or unrelated)")
    for r in res:
        print(f"- {r['path']}:{r['lines']}  {r['title']}  |  {r['snippet'][:160]}")
    print()
    nodes = load_nodes()
    mechs = [n for n in nodes.values() if n.folder == "mechanisms"]
    print(f"## Existing mechanisms ({len(mechs)}) - reuse before creating a new one")
    for n in sorted(mechs, key=lambda n: n.id):
        print(f"- [[{n.id}]] ({n.fm.get('status')}, {n.fm.get('kind')}) - {n.fm.get('description', '')}")
    return 0


# --------------------------------------------------------------------------
# Verification support
# --------------------------------------------------------------------------

def context_for_quote(sid: str, quote: str, manifest: dict, radius=3) -> str:
    tp = ROOT / manifest[sid]["text"]
    lines = tp.read_text(encoding="utf-8").splitlines()
    first = norm(re.split(r"\.\.\.|…", quote)[0]).strip(" \"'")[:60]
    # find the line window containing the start of the quote
    for i in range(len(lines)):
        window = norm(" ".join(lines[i:i + 4]))
        if first and first in window:
            a, b = max(0, i - radius), min(len(lines), i + 4 + radius)
            return f"{manifest[sid]['text']}:{a + 1}-{b}\n" + "\n".join(lines[a:b])
    return f"{manifest[sid]['text']}: (location not found)"


def cmd_pairs(args) -> int:
    nodes, manifest = load_nodes(), load_manifest()
    pending = [n for n in nodes.values() if n.fm.get("type") == "claim"
               and (args.all or n.fm.get("verified") == "pending")]
    if not pending:
        print("no claims awaiting verification")
        return 0
    for n in sorted(pending, key=lambda n: n.id):
        print(f"=== CLAIM {n.id}")
        print(f"STATEMENT: {n.title}")
        for r in n.rels:
            if r.pred != "derived_from" or not r.quotes:
                continue
            t = resolve_target(r.target, nodes, manifest)
            if not t:
                continue
            for q in r.quotes:
                print(f"QUOTE: {q}")
                print("SOURCE CONTEXT:")
                print("    " + context_for_quote(t[1], q, manifest).replace("\n", "\n    "))
        print()
    print("For each claim run: uv run scripts/kb.py verdict <claim> pass|partial|fail --note \"...\"")
    return 0


def set_frontmatter(p: Path, updates: dict) -> None:
    lines = p.read_text(encoding="utf-8").splitlines()
    end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    keys_done = set()
    for i in range(1, end):
        k = lines[i].split(":", 1)[0].strip()
        if k in updates:
            lines[i] = f"{k}: {updates[k]}"
            keys_done.add(k)
    for k, v in updates.items():
        if k not in keys_done:
            lines.insert(end, f"{k}: {v}")
            end += 1
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_verdict(args) -> int:
    if args.verdict not in {"pass", "partial", "fail"}:
        raise SystemExit("verdict must be pass, partial or fail")
    nodes = load_nodes()
    n = find_node(args.claim, nodes)
    if n.fm.get("type") != "claim":
        raise SystemExit(f"{n.id} is not a claim")
    upd = {"verified": args.verdict}
    if args.verdict == "fail":
        upd["status"] = "disputed"
    set_frontmatter(n.path, upd)
    append_log(f"verify | {n.id} -> {args.verdict}" + (f" | {args.note}" if args.note else ""))
    print(f"{n.id}: verified={args.verdict}" + (" (status set to disputed)" if args.verdict == "fail" else ""))
    return 0


def cmd_mark_ingested(args) -> int:
    m = load_manifest()
    sid = Path(args.source).stem
    if sid not in m:
        raise SystemExit(f"unknown source {sid}")
    m[sid]["ingested"] = True
    m[sid]["ingested_on"] = today()
    save_manifest(m)
    print(f"{sid}: ingested")
    return 0


def append_log(msg: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    if not LOG.exists():
        LOG.write_text("# Log\n\nAppend-only. One line per operation.\n\n", encoding="utf-8")
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"- {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} | {msg}\n")


def cmd_status(args) -> int:
    m = load_manifest()
    pending = sum(1 for v in m.values() if not v.get("ingested"))
    print(f"[kb] {len(m)} sources ({pending} not ingested), {len(cortex_files())} cortex nodes. "
          f"Start with cortex/_index/catalog.md. Run kb.py only via 'uv run scripts/kb.py'. "
          f"Commands: /ingest, /ask, /consolidate.")
    return 0


def cmd_log(args) -> int:
    append_log(args.message)
    return 0


# --------------------------------------------------------------------------
# Claude Code hooks
# --------------------------------------------------------------------------

def read_hook_input() -> dict:
    try:
        return json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return {}


def cmd_hook_post_write(args) -> int:
    """PostToolUse on Write|Edit: give immediate feedback about a cortex file. Cannot block (tool already ran)."""
    data = read_hook_input()
    fp = (data.get("tool_input") or {}).get("file_path") or ""
    if not fp:
        return 0
    p = Path(fp)
    if not p.is_absolute():
        p = (Path(data.get("cwd") or ROOT) / p)
    try:
        p = p.resolve()
        p.relative_to(CORTEX)
    except (ValueError, OSError):
        return 0
    if p.suffix != ".md" or not p.exists() or p.relative_to(CORTEX).parts[0] not in TYPES:
        return 0
    nodes, manifest = load_nodes(), load_manifest()
    n = parse_node(p)
    errs = validate_node(n, nodes, manifest, {})
    if errs:
        print("kb: problems in the file you just wrote - fix them now:", file=sys.stderr)
        for x in errs:
            print("  - " + x, file=sys.stderr)
        return 2  # PostToolUse exit 2 = stderr shown to Claude
    return 0


def git(*a) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)


def cmd_hook_subagent_stop(args) -> int:
    """SubagentStop for the ingestor: fail -> exit 2 (keep working); pass -> index + commit."""
    read_hook_input()
    attempts = int(STOP_STATE.read_text()) if STOP_STATE.exists() else 0
    errs = run_check(strict=True)
    if errs:
        attempts += 1
        INDEX_DIR.mkdir(parents=True, exist_ok=True)
        if attempts >= MAX_STOP_ATTEMPTS:
            STOP_STATE.unlink(missing_ok=True)
            append_log(f"ingest | GAVE UP after {attempts} failed checks; nothing committed")
            print(f"kb: giving up after {attempts} failed checks. Changes left uncommitted for a human.", file=sys.stderr)
            return 0
        STOP_STATE.write_text(str(attempts))
        print(f"kb check failed (attempt {attempts}/{MAX_STOP_ATTEMPTS}). Fix these before finishing:", file=sys.stderr)
        for x in errs:
            print("  - " + x, file=sys.stderr)
        return 2
    STOP_STATE.unlink(missing_ok=True)
    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        return 0
    before = load_manifest()
    cmd_index()
    git("add", "-A", "sources", "cortex", "studio")
    if git("diff", "--cached", "--quiet").returncode == 0:
        return 0
    try:
        head = json.loads(git("show", "HEAD:sources/manifest.json").stdout or "{}")
    except json.JSONDecodeError:
        head = {}
    newly = sorted(s for s, v in before.items() if v.get("ingested") and not head.get(s, {}).get("ingested"))
    msg = "ingest: " + (", ".join(newly) if newly else "cortex update")
    res = git("commit", "-m", msg)
    if res.returncode != 0:
        print("kb: commit failed:\n" + res.stdout + res.stderr, file=sys.stderr)
        return 2
    print(f"kb: committed '{msg}'")
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def require_uv() -> None:
    """Refuse to run outside the project's uv environment, so every run uses the locked dependencies."""
    venv = Path(os.environ.get("UV_PROJECT_ENVIRONMENT") or ".venv")
    if not venv.is_absolute():
        venv = ROOT / venv
    try:
        ok = Path(sys.prefix).resolve() == venv.resolve()
    except OSError:
        ok = False
    if not ok:
        sys.stderr.write("kb.py runs only through uv. Use: uv run scripts/kb.py <command>\n"
                         f"(current interpreter: {sys.executable})\n")
        sys.exit(3)


def main(argv=None) -> int:
    require_uv()
    try:  # exit quietly when piped into `head`
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(prog="kb.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("register").set_defaults(fn=lambda a: (cmd_register(a), 0)[1])
    p = sp.add_parser("check")
    p.add_argument("--strict", action="store_true", help="also fail on changed claims still 'verified: pending'")
    p.set_defaults(fn=cmd_check)
    sp.add_parser("index").set_defaults(fn=cmd_index)
    sp.add_parser("status").set_defaults(fn=cmd_status)
    p = sp.add_parser("preflight")
    p.add_argument("source", nargs="?", help="source id or filename; default: next not-ingested source")
    p.set_defaults(fn=cmd_preflight)
    p = sp.add_parser("search")
    p.add_argument("query")
    p.add_argument("--kind", choices=["all", "cortex", "sources"], default="all")
    p.add_argument("-k", type=int, default=8)
    p.set_defaults(fn=cmd_search)
    p = sp.add_parser("nav")
    p.add_argument("node")
    p.set_defaults(fn=cmd_nav)
    p = sp.add_parser("distractor")
    p.add_argument("node")
    p.add_argument("mechanism")
    p.set_defaults(fn=cmd_distractor)
    p = sp.add_parser("hubs")
    p.add_argument("--threshold", type=int, default=HUB_THRESHOLD)
    p.set_defaults(fn=cmd_hubs)
    p = sp.add_parser("pairs")
    p.add_argument("--all", action="store_true", help="include already-verified claims")
    p.set_defaults(fn=cmd_pairs)
    p = sp.add_parser("verdict")
    p.add_argument("claim")
    p.add_argument("verdict")
    p.add_argument("--note", default="")
    p.set_defaults(fn=cmd_verdict)
    p = sp.add_parser("mark-ingested")
    p.add_argument("source")
    p.set_defaults(fn=cmd_mark_ingested)
    p = sp.add_parser("log")
    p.add_argument("message")
    p.set_defaults(fn=cmd_log)
    sp.add_parser("hook-post-write").set_defaults(fn=cmd_hook_post_write)
    sp.add_parser("hook-subagent-stop").set_defaults(fn=cmd_hook_subagent_stop)
    args = ap.parse_args(argv)
    return args.fn(args) or 0


if __name__ == "__main__":
    sys.exit(main())
