"""The Obsidian vault: note naming, rendering, links, index.md, rename, checks.

Rules this module enforces so the vault stays pleasant for a human:
  * filename == H1 heading == link text, short and descriptive ("Platform Screen Doors")
  * no hashes, export-task names, or full sentences as titles
  * machine IDs live only in frontmatter (id, sha256), never in names or body text
  * vault/raw/ holds unchanged originals; vault/wiki/<topic folder>/ holds notes

How notes are produced: ingest writes the model's structured draft into
.wiki/notes.json (outside the vault). render_all() applies reviewer corrections
from review/corrections.yaml and turns the result into Markdown notes. Before
rendering, sync_from_vault() reads the vault back, so a rename or move done in
Obsidian is adopted instead of being overwritten. Text under "## My Notes" in
any generated note is preserved across re-renders.
"""

import copy
import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

import yaml

from . import config

STORE_FILE = config.MACHINE / "notes.json"
MY_NOTES = "## My Notes"

_ACRONYMS = {
    "ai": "AI", "ev": "EV", "evs": "EVs", "r&d": "R&D", "pg&e": "PG&E", "cbtc": "CBTC",
    "wmata": "WMATA", "mba": "MBA", "us": "US", "u.s.": "U.S.", "psd": "PSD", "psds": "PSDs",
    "goa": "GoA", "fy": "FY", "cig": "CIG", "ato": "ATO", "llm": "LLM", "gpu": "GPU",
}
_SMALL = {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "the", "to", "vs"}
_BAD_WORDS = re.compile(r"\b(export|exported|download|downloaded|untitled|copy of|final|v\d+)\b", re.I)
_HASHY = re.compile(r"\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,}\b|\b[0-9a-f]{8}-[0-9a-f]{4}", re.I)
_UNSAFE = re.compile(r'[\\/:*?"<>|#^\[\]]')
MAX_TITLE_WORDS = 7


# --- titles ------------------------------------------------------------------------------
def title_case(text: str) -> str:
    out = []
    for i, w in enumerate(text.split()):
        low = w.lower()
        if low in _ACRONYMS:
            out.append(_ACRONYMS[low])
        elif w.isupper() and len(w) <= 5:
            out.append(w)
        elif i > 0 and low in _SMALL:
            out.append(low)
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out)


def title_problems(title: str) -> list[str]:
    problems = []
    if not title.strip():
        problems.append("empty")
    if _HASHY.search(title):
        problems.append("contains a hash-like ID")
    if _BAD_WORDS.search(title):
        problems.append("names an export/download task")
    if len(title.split()) > MAX_TITLE_WORDS:
        problems.append(f"longer than {MAX_TITLE_WORDS} words (reads like a sentence)")
    if re.search(r"[.?!]$", title):
        problems.append("ends like a sentence")
    if " " not in title and re.search(r"[-_]", title):
        problems.append("looks like a slug/filename")
    if _UNSAFE.search(title):
        problems.append("has characters that break links")
    return problems


def clean_title(raw: str) -> tuple[str, list[str]]:
    """Normalize a proposed title. Returns (title, aliases); a trailing
    parenthetical like "(CBTC)" becomes an alias rather than part of the name."""
    t = Path(raw).stem if raw.lower().endswith((".pdf", ".md", ".txt")) else raw
    t = t.replace("_", " ").replace("​", "")
    if " " not in t.strip():
        t = re.sub(r"(?<=\w)-(?=\w)", " ", t)
    aliases = [a.strip() for a in re.findall(r"\(([^)]{2,20})\)", t)]
    t = re.sub(r"\([^)]*\)", " ", t)
    t = _UNSAFE.sub(" ", t)
    t = _HASHY.sub(" ", t)
    t = re.sub(r"^\s*(\d+[A-Za-z]?|[A-Z]\d+)\s+(?=[A-Z])", "", t)  # agenda codes like "3A"
    t = re.sub(r"\s+", " ", t).strip(" .-–—:,;")
    return title_case(t), aliases


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# --- note files ----------------------------------------------------------------------------
def read_note(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            meta = yaml.safe_load(text[4:end]) or {}
            return meta, text[end + 4 :].lstrip("\n")
    return {}, text


def note_text(meta: dict, body: str) -> str:
    front = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=1000).strip()
    return f"---\n{front}\n---\n\n{body.strip()}\n"


def all_notes() -> list[Path]:
    """Every Markdown note except the landing page, raw sources and Obsidian config."""
    return sorted(
        p for p in config.VAULT.rglob("*.md")
        if ".obsidian" not in p.parts and p != config.INDEX_NOTE and config.RAW not in p.parents
    )


def rel(path: Path) -> str:
    return path.relative_to(config.VAULT).as_posix()


def notes_by_id() -> dict[str, Path]:
    found = {}
    for p in all_notes():
        meta, _ = read_note(p)
        if meta.get("id"):
            found[meta["id"]] = p
    return found


# --- machine store (.wiki/notes.json) -------------------------------------------------------------
def load_store() -> dict:
    if STORE_FILE.exists():
        store = json.loads(STORE_FILE.read_text(encoding="utf-8"))
    else:
        store = {"sources": {}, "concepts": {}}
    store.setdefault("links", [])
    return store


def save_store(store: dict) -> None:
    config.MACHINE.mkdir(parents=True, exist_ok=True)
    STORE_FILE.write_text(json.dumps(store, indent=2, ensure_ascii=False), encoding="utf-8")


def taken_titles(store: dict, except_id: str | None = None) -> set[str]:
    titles = {e["title"].lower() for k, e in {**store["sources"], **store["concepts"]}.items() if k != except_id}
    titles |= {p.stem.lower() for p in all_notes()}
    return titles


def find_concept(store: dict, name: str) -> str | None:
    key = name.lower()
    for cid, c in store["concepts"].items():
        if key == c["title"].lower() or key in (a.lower() for a in c.get("aliases", [])):
            return cid
    return None


def forget_source_mentions(store: dict, sid: str) -> None:
    """Before merging a re-drafted source, drop its old concept mentions."""
    for c in store["concepts"].values():
        c["mentions"].pop(sid, None)


def prune_concepts(store: dict) -> list[str]:
    """Delete concepts no source mentions any more (and links to them)."""
    removed = [c["title"] for c in store["concepts"].values() if not c["mentions"]]
    store["concepts"] = {k: c for k, c in store["concepts"].items() if c["mentions"]}
    for s in store["sources"].values():
        s["concepts"] = [c for c in s["concepts"] if c in store["concepts"]]
    store["links"] = [l for l in store["links"] if l["a"] in store["concepts"] and l["b"] in store["concepts"]]
    return removed


def sync_from_vault(store: dict) -> list[str]:
    """Adopt renames/moves the human made in Obsidian (matched by frontmatter id)."""
    changes = []
    on_disk = notes_by_id()
    for kind in ("sources", "concepts"):
        for nid, entry in store[kind].items():
            p = on_disk.get(nid)
            if p is None or config.WIKI not in p.parents:
                continue
            folder = p.parent.relative_to(config.WIKI).as_posix()
            if p.stem != entry["title"] or folder != entry["folder"]:
                changes.append(f"adopted {entry['folder']}/{entry['title']} -> {rel(p)}")
                entry["title"], entry["folder"] = p.stem, folder
    return changes


# --- reviewer corrections (review/corrections.yaml, outside the vault) -----------------------------------
def load_corrections() -> dict:
    if config.CORRECTIONS_FILE.exists():
        data = yaml.safe_load(config.CORRECTIONS_FILE.read_text(encoding="utf-8")) or {}
    else:
        data = {}
    return {"corrections": data.get("corrections") or [], "reviewed": data.get("reviewed") or {},
            "rejected_links": data.get("rejected_links") or [],
            "link_reasons": data.get("link_reasons") or {},
            "added_links": data.get("added_links") or []}


def _pair_key(a: str, b: str) -> frozenset:
    return frozenset((a.strip().lower(), b.strip().lower()))


def apply_corrections(store: dict) -> tuple[dict, list[str]]:
    """Return a copy of the store with reviewer corrections applied, plus a list of
    corrections that no longer match anything (reported by `wiki check`).

    The model's draft stays untouched in notes.json; corrections are replayed on
    every render, so a re-ingest cannot silently bring an error back."""
    view = copy.deepcopy(store)
    stale = []
    for fix in load_corrections()["corrections"]:
        nid, field, match = fix["id"], fix["field"], fix.get("match", "")
        entry = view["sources"].get(nid) or view["concepts"].get(nid)
        applied = False
        if entry is None:
            pass
        elif field == "summary" and match in entry["summary"]:
            entry["summary"] = entry["summary"].replace(match, fix["text"])
            applied = True
        elif field == "key_point":
            for kp in entry["key_points"]:
                if match in kp["point"]:
                    kp["point"] = fix.get("text", kp["point"])
                    kp["page"] = fix.get("page", kp["page"])
                    applied = True
        elif field == "definition":
            for sid, m in entry["mentions"].items():
                if fix.get("source", sid) == sid and match in m["definition"]:
                    m["definition"] = fix.get("text", m["definition"])
                    m["page"] = fix.get("page", m["page"])
                    applied = True
        if not applied:
            stale.append(f"correction for {nid} ({field}: “{match[:40]}”) no longer matches the draft")

    # reviewed concept links: drop rejected pairs, fix reasons, add reviewer links
    fixes = load_corrections()
    title = lambda cid: view["concepts"][cid]["title"]
    rejected = {_pair_key(*r.split("|")) for r in fixes["rejected_links"]}
    reasons = {_pair_key(*k.split("|")): v for k, v in fixes["link_reasons"].items()}
    links = []
    for l in view["links"]:
        if l["a"] not in view["concepts"] or l["b"] not in view["concepts"]:
            continue
        key = _pair_key(title(l["a"]), title(l["b"]))
        if key in rejected:
            continue
        links.append({**l, "why": reasons.pop(key, l["why"])})
    for add in fixes["added_links"]:
        a, b = find_concept(view, add["a"]), find_concept(view, add["b"])
        if not a or not b:
            stale.append(f"added link {add['a']} | {add['b']}: concept not found")
            continue
        if not any({a, b} == {l["a"], l["b"]} for l in links):
            links.append({"a": a, "b": b, "why": add["why"]})
    stale += [f"link reason for {' | '.join(sorted(k))}: no such link" for k in reasons]
    view["links"] = links
    return view, stale


# --- rendering ---------------------------------------------------------------------------------------
def note_path(entry: dict) -> Path:
    return config.WIKI / entry["folder"] / f"{entry['title']}.md"


def _page_link(original_name: str, page) -> str:
    return f"[[{original_name}#page={page}|p. {page}]]" if page else f"[[{original_name}]]"


def _kept_my_notes(path: Path) -> str:
    if not path.exists():
        return ""
    _, body = read_note(path)
    i = body.find(MY_NOTES)
    return body[i:].strip() if i != -1 else ""


def _concept_links(cid: str, store: dict) -> list[tuple[str, str]]:
    """(other concept id, reason) for every reviewed cross-source link."""
    out = []
    for l in store["links"]:
        if cid in (l["a"], l["b"]):
            out.append((l["b"] if l["a"] == cid else l["a"], l["why"]))
    return out


def render_source(sid: str, s: dict, store: dict, reviewed: dict) -> tuple[dict, str]:
    orig = Path(s["original"]).name
    meta = {
        "id": sid,
        "type": "source",
        "summary": s["summary"].split(". ")[0].rstrip(".") + ".",
        "original": s["original"],
        "original_path": s["original_path"],
        "sha256": s["sha256"],
        "pages": s["pages"],
        "ingested": s["ingested"],
        "reviewed": str(reviewed[sid]) if sid in reviewed else "not yet",
        "aliases": s.get("aliases", []),
    }
    lines = [
        f"# {s['title']}", "",
        "> [!info] Source",
        f"> Original file: [[{orig}]] ({s['pages']} pages), kept unchanged in `raw/`.",
        "> Page links below open the original at the cited page.", "",
        "## Summary", "", s["summary"], "",
        "## Key Points", "",
    ]
    lines += [f"- {kp['point']} ({_page_link(orig, kp.get('page'))})" for kp in s["key_points"]]
    concepts = [(c, store["concepts"][c]) for c in s["concepts"] if c in store["concepts"]]
    if concepts:
        lines += ["", "## Key Concepts", ""]
        for _, c in concepts:
            m = c["mentions"].get(sid, {})
            lines.append(f"- [[{c['title']}]] — {m.get('definition', '')}".rstrip(" —"))
    related = _related_sources(sid, store)
    if related:
        lines += ["", "## Related Sources", ""]
        for other_id, reasons in related:
            lines.append(f"- [[{store['sources'][other_id]['title']}]] — {'; '.join(reasons)}")
    return meta, "\n".join(lines)


def _related_sources(sid: str, store: dict) -> list[tuple[str, list[str]]]:
    mine = set(store["sources"][sid]["concepts"])
    out = []
    for other_id, o in store["sources"].items():
        if other_id == sid:
            continue
        reasons = [f"also covers [[{store['concepts'][c]['title']}]]" for c in sorted(mine & set(o["concepts"]))]
        for l in store["links"]:
            for x, y in ((l["a"], l["b"]), (l["b"], l["a"])):
                if x in mine and y in o["concepts"] and x not in o["concepts"]:
                    reasons.append(f"its [[{store['concepts'][y]['title']}]] relates to "
                                   f"[[{store['concepts'][x]['title']}]] here")
        if reasons:
            out.append((other_id, reasons))
    return out


def render_concept(cid: str, c: dict, store: dict, reviewed: dict) -> tuple[dict, str]:
    mentions = [(sid, m) for sid, m in c["mentions"].items() if sid in store["sources"]]
    first = mentions[0][1]["definition"] if mentions else ""
    srcs = [sid for sid, _ in mentions]
    meta = {
        "id": cid,
        "type": "concept",
        "summary": first,
        "aliases": c.get("aliases", []),
        "sources": srcs,
        "reviewed": str(reviewed[srcs[0]]) if srcs and all(s in reviewed for s in srcs) else "not yet",
    }
    lines = [f"# {c['title']}", "", first, "", "## In the Sources", ""]
    for i, (sid, m) in enumerate(mentions):
        s = store["sources"][sid]
        where = _page_link(Path(s["original"]).name, m.get("page"))
        said = "" if i == 0 else f": {m['definition']}"  # the first definition is the lead paragraph
        lines.append(f"- [[{s['title']}]]{said} ({where})")

    related: dict[str, str] = {}
    for other, why in _concept_links(cid, store):
        if other in store["concepts"]:
            related[store["concepts"][other]["title"]] = why
    for sid in srcs:
        for o in store["sources"][sid]["concepts"]:
            if o != cid and o in store["concepts"]:
                related.setdefault(store["concepts"][o]["title"],
                                   f"also discussed in [[{store['sources'][sid]['title']}]]")
    if related:
        lines += ["", "## Related Concepts", ""]
        lines += [f"- [[{t}]] — {why}" for t, why in sorted(related.items())]
    return meta, "\n".join(lines)


def render_all(store: dict) -> dict:
    """Write every note from the store (with reviewer corrections applied);
    only touch files whose content changed."""
    view, stale = apply_corrections(store)
    reviewed = load_corrections()["reviewed"]
    written, unchanged = [], 0
    on_disk = notes_by_id()
    for kind, render in (("sources", render_source), ("concepts", render_concept)):
        for nid, entry in view[kind].items():
            path = note_path(entry)
            old = on_disk.get(nid)
            mine = _kept_my_notes(old or path)
            meta, body = render(nid, entry, view, reviewed)
            if mine:
                body += "\n\n" + mine
            text = note_text(meta, body)
            if old and old != path:
                old.unlink()  # the store moved it; never leave a duplicate behind
            if path.exists() and path.read_text(encoding="utf-8") == text:
                unchanged += 1
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            written.append(rel(path))
    # generated notes whose concept disappeared (e.g. after a re-draft)
    live = set(view["sources"]) | set(view["concepts"])
    for nid, p in notes_by_id().items():
        meta, _ = read_note(p)
        if meta.get("type") in ("source", "concept") and nid not in live:
            p.unlink()
            written.append(f"removed {rel(p)}")
    for d in sorted(config.WIKI.glob("*/"), reverse=True):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()
    rebuild_index(view)
    return {"written": written, "unchanged": unchanged, "stale_corrections": stale}


# --- index.md ----------------------------------------------------------------------------------------
def rebuild_index(store: dict | None = None) -> Path:
    store = store or load_store()
    groups: dict[str, dict[str, list[str]]] = {}
    for p in all_notes():
        meta, _ = read_note(p)
        kind = meta.get("type", "note")
        folder = p.parent.relative_to(config.WIKI).as_posix() if config.WIKI in p.parents else "Other Notes"
        summary = (meta.get("summary") or "").strip()
        line = f"- [[{p.stem}]]" + (f" — {summary}" if summary else "")
        groups.setdefault(folder, {}).setdefault(kind, []).append(line)

    lines = [
        "# Index", "",
        "Start here. Notes live in `wiki/`, grouped into topic folders.",
        "**Source notes** summarize one original document each and cite it by page.",
        "**Concept notes** collect what the sources say about one idea, link back to every",
        "source that mentions it, and explain how they relate to other concepts.",
        "The originals are kept unchanged in `raw/` (see the source catalog below).", "",
    ]
    for folder in sorted(groups):
        lines += [f"## {folder}", ""]
        for kind, label in (("source", "Sources"), ("concept", "Concepts"), ("note", "Notes")):
            if groups[folder].get(kind):
                lines += [f"### {label}", "", *sorted(groups[folder][kind]), ""]
    if store["sources"]:
        lines += ["## Source Catalog", "",
                  "| Source note | Original file | Pages | Ingested |", "|---|---|---|---|"]
        for s in sorted(store["sources"].values(), key=lambda s: s["title"]):
            name = Path(s["original"]).name
            lines.append(f"| [[{s['title']}]] | [[{name}]] | {s['pages']} | {s['ingested']} |")
        lines.append("")
    text = "\n".join(lines).rstrip() + "\n"
    if not config.INDEX_NOTE.exists() or config.INDEX_NOTE.read_text(encoding="utf-8") != text:
        config.INDEX_NOTE.write_text(text, encoding="utf-8")
    return config.INDEX_NOTE


# --- links -----------------------------------------------------------------------------------------
_LINK = re.compile(r"\[\[([^\]|#]+)(#[^\]|]*)?(\|[^\]]*)?\]\]")


def links_in(body: str) -> list[str]:
    return [m.group(1).strip() for m in _LINK.finditer(body)]


def replace_links(text: str, old: str, new: str) -> tuple[str, int]:
    count = 0

    def sub(m):
        nonlocal count
        target = m.group(1).strip()
        if target == old or target.endswith("/" + old):
            count += 1
            return f"[[{new}{m.group(2) or ''}{m.group(3) or ''}]]"
        return m.group(0)

    return _LINK.sub(sub, text), count


# --- rename (cleaning up an existing note name) ----------------------------------------------------------
def rename_note(old_title: str, new_title: str, chunks=None) -> dict:
    """Back up every file touched, rename in the store, re-render (moves the file and
    rewrites generated links), fix links in hand-written notes, update retrieval
    paths, rebuild index.md."""
    store = load_store()
    sync_from_vault(store)
    new_title, _ = clean_title(new_title)
    if problems := title_problems(new_title):
        raise ValueError(f"'{new_title}' is not a good note name: {', '.join(problems)}")
    match = [(k, nid) for k in ("sources", "concepts") for nid, e in store[k].items()
             if e["title"].lower() == old_title.lower()]
    if not match:
        raise FileNotFoundError(f"No generated note titled '{old_title}'")
    kind, nid = match[0]
    if new_title.lower() in taken_titles(store, except_id=nid):
        raise FileExistsError(f"A note called '{new_title}' already exists")
    entry = store[kind][nid]
    old_path, old_name = note_path(entry), entry["title"]

    backup = config.BACKUPS / datetime.now().strftime("%Y-%m-%d %H%M%S rename")
    for p in all_notes() + [config.INDEX_NOTE]:
        if p == old_path or f"[[{old_name}" in p.read_text(encoding="utf-8"):
            target = backup / rel(p)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
    shutil.copy2(STORE_FILE, backup / "notes.json")

    entry["title"] = new_title
    save_store(store)
    render_all(store)

    handwritten_links = 0
    for p in all_notes():
        text = p.read_text(encoding="utf-8")
        new_text, n = replace_links(text, old_name, new_title)
        if n:
            p.write_text(new_text, encoding="utf-8")
            handwritten_links += n

    chunk_updates = 0
    if chunks is not None and kind == "sources":
        chunk_updates = chunks.update_note_path(nid, rel(note_path(entry)), new_title)
        chunks.save()
    rebuild_index()
    return {
        "from": rel(old_path), "to": rel(note_path(entry)),
        "other_links_updated": handwritten_links, "retrieval_chunks_updated": chunk_updates,
        "backup": str(backup),
    }




# --- checks ------------------------------------------------------------------------------------------------
def check_vault(chunks=None) -> list[str]:
    """Return a list of problems. An empty list means the vault passes."""
    problems = []
    notes = all_notes()
    titles = {p.stem for p in notes}
    raw_files = {p.name for p in config.RAW.glob("*")} if config.RAW.exists() else set()
    ids_seen: dict[str, str] = {}
    for p in notes:
        meta, body = read_note(p)
        for issue in title_problems(p.stem):
            problems.append(f"{rel(p)}: filename {issue}")
        h1 = re.search(r"^# (.+)$", body, re.M)
        if not h1 or h1.group(1).strip() != p.stem:
            problems.append(f"{rel(p)}: H1 heading does not match filename")
        if meta.get("id"):
            if meta["id"] in ids_seen:
                problems.append(f"{rel(p)}: duplicate of {ids_seen[meta['id']]} (same id)")
            ids_seen[meta["id"]] = rel(p)
            if meta["id"] in body:
                problems.append(f"{rel(p)}: machine id appears in note body")
        for target in links_in(body):
            name = target.split("/")[-1]
            if name not in titles and name not in raw_files:
                problems.append(f"{rel(p)}: broken link [[{target}]]")
        if meta.get("type") == "source":
            orig = config.VAULT / (meta.get("original") or "")
            if not orig.is_file():
                problems.append(f"{rel(p)}: original file missing ({meta.get('original')})")
            elif hashlib.sha256(orig.read_bytes()).hexdigest() != meta.get("sha256"):
                problems.append(f"{rel(p)}: original changed since ingest (sha256 mismatch)")
        if meta.get("type") in ("source", "concept") and config.WIKI not in p.parents:
            problems.append(f"{rel(p)}: generated note outside wiki/")
    if config.INDEX_NOTE.exists():
        for target in links_in(config.INDEX_NOTE.read_text(encoding="utf-8")):
            if target not in titles and target not in raw_files:
                problems.append(f"index.md: broken link [[{target}]]")
    else:
        problems.append("index.md is missing")
    problems += apply_corrections(load_store())[1]
    if chunks is not None:
        paths = {rel(p) for p in notes}
        missing = {c["note_path"] for c in chunks.chunks if c["note_path"] not in paths}
        problems += [f"retrieval chunks point to missing note {m}" for m in sorted(missing)]
        gone = {c["original"] for c in chunks.chunks if not (config.VAULT / c["original"]).is_file()}
        problems += [f"retrieval chunks point to missing original {g}" for g in sorted(gone)]
        ids = [c["chunk_id"] for c in chunks.chunks]
        if len(ids) != len(set(ids)):
            problems.append("retrieval index contains duplicate chunks")
    for f in config.VAULT.rglob("*"):
        if f.suffix in (".jsonl", ".npy", ".json", ".py", ".log") and ".obsidian" not in f.parts:
            problems.append(f"machine file inside vault: {rel(f)}")
    return problems
