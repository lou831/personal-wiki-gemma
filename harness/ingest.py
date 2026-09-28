"""Ingest: original file -> read-only copy, retrieval chunks, and wiki notes.

Steps for one source:
  1. Hash the bytes. The hash is the source's identity, so the same file ingested
     twice is recognized and never duplicated, whatever its filename.
  2. Copy it to vault/raw/ (read-only). The file the user pointed at is only read.
  3. Extract text page by page (PyMuPDF), clean whitespace, split into passages.
  4. Ask the local model to propose a title, folder, summary, key points and
     concepts as JSON (prompts/note_writer.md). The harness validates all of it:
     names must pass the naming rules, cited pages are checked against the text.
  5. Merge into .wiki/notes.json, render notes (with reviewer corrections), embed
     passages, ask the model for cross-source concept links, rebuild index.md.
"""

import hashlib
import json
import os
import re
import shutil
from datetime import date
from pathlib import Path

from . import config, linker, vault
from .retrieval import tokenize

SUPPORTED = {".pdf", ".md", ".txt"}


class IngestError(RuntimeError):
    pass


# --- text extraction ----------------------------------------------------------------------------
def extract_pages(path: Path) -> tuple[list[str], str | None]:
    """Return (page texts, embedded document title)."""
    if path.suffix.lower() == ".pdf":
        import pymupdf

        with pymupdf.open(path) as doc:
            pages = [clean_text(p.get_text()) for p in doc]
            meta_title = (doc.metadata or {}).get("title") or None
        return pages, meta_title
    text = path.read_text(encoding="utf-8", errors="replace")
    h1 = re.search(r"^# (.+)$", text, re.M)
    return [clean_text(text)], (h1.group(1) if h1 else None)


def clean_text(raw: str) -> str:
    raw = raw.replace("​", "").replace("­", "").replace("\t", " ")
    paras, cur = [], []
    for line in (l.strip() for l in raw.splitlines()):
        if not line:
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        if line[:1] in "●•▪◦-–*" and cur:
            paras.append(" ".join(cur))
            cur = []
        if cur and cur[-1].endswith("-") and line[:1].islower():
            cur[-1] = cur[-1][:-1] + line
        else:
            cur.append(line)
    if cur:
        paras.append(" ".join(cur))
    return "\n".join(re.sub(r"\s+", " ", p).strip() for p in paras if p.strip())


def split_passages(page_text: str) -> list[str]:
    sentences = [s for s in re.split(r"(?<=[.!?])\s+|\n", page_text) if s.strip()]
    passages, cur = [], []
    for s in sentences:
        cur.append(s)
        if sum(len(x) + 1 for x in cur) >= config.CHUNK_CHARS:
            passages.append(" ".join(cur))
            cur = cur[-config.CHUNK_OVERLAP_SENTENCES :] if config.CHUNK_OVERLAP_SENTENCES else []
    if cur and (not passages or " ".join(cur) not in passages[-1]):
        passages.append(" ".join(cur))
    return [p for p in passages if len(p) >= 40]


# --- page verification ------------------------------------------------------------------------------
def best_page(claim: str, pages: list[str], claimed) -> int | None:
    """Keep the model's page number only if that page supports the claim about as
    well as the best page does; otherwise use the best-supported page."""
    if len(pages) <= 1:
        return None  # a single-page text file has no page numbers to cite
    try:
        c = int(claimed)
    except (TypeError, ValueError):
        c = 0
    words = set(tokenize(claim))
    if not words:
        return c if 1 <= c <= len(pages) else None
    scores = [len(words & set(tokenize(p))) / len(words) for p in pages]
    top = max(range(len(pages)), key=lambda i: scores[i])
    if 1 <= c <= len(pages) and scores[c - 1] >= 0.8 * scores[top]:
        return c
    return top + 1


# --- the model's note draft --------------------------------------------------------------------------
def draft_note(pages: list[str], filename: str, meta_title: str | None, llm) -> dict:
    budget = max(400, config.NOTE_INPUT_CHARS // max(1, len(pages)))
    tagged = "\n\n".join(
        f"[p. {i + 1}]\n{p[:budget]}" if len(pages) > 1 else p[: config.NOTE_INPUT_CHARS]
        for i, p in enumerate(pages) if p.strip()
    )
    rules = (config.PROMPTS / "note_writer.md").read_text(encoding="utf-8")
    rules = rules.replace("{FOLDERS}", ", ".join(config.TOPIC_FOLDERS))
    user = (
        f"Original filename: {filename}\n"
        f"Embedded document title: {meta_title or '(none)'}\n"
        f"Pages: {len(pages)}\n\nDOCUMENT TEXT\n{tagged}"
    )
    messages = [{"role": "system", "content": rules}, {"role": "user", "content": user}]
    for attempt in range(2):
        gen = llm.generate(messages, max_tokens=config.NOTE_MAX_TOKENS, temperature=0.0)
        try:
            return _parse_json(gen.text)
        except ValueError:
            messages += [
                {"role": "assistant", "content": gen.text},
                {"role": "user", "content": "That was not valid JSON. Reply with the JSON object only."},
            ]
    raise IngestError("The local model did not return a valid note draft (JSON) after 2 attempts.")


_PAGE_REF = re.compile(r"\s*[\[(](?:p|pp|page|pages)\.?\s*\d+(?:\s*[-–,]\s*\d+)*[\])]", re.I)


def strip_page_refs(text: str) -> str:
    """The harness adds verified page links itself; drop the model's inline "[p. 4]"."""
    return re.sub(r"\s+([.,;])", r"\1", _PAGE_REF.sub("", str(text))).strip()


def _parse_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("no JSON object")
    data = json.loads(m.group(0))
    if not isinstance(data, dict) or "summary" not in data:
        raise ValueError("missing fields")
    return data


# --- main entry point ------------------------------------------------------------------------------------
def ingest(path: str | Path, llm, chunks, force: bool = False) -> dict:
    src = Path(path).expanduser().resolve()
    if not src.is_file():
        raise IngestError(f"File not found: {src}")
    if src.suffix.lower() not in SUPPORTED:
        raise IngestError(f"Unsupported file type {src.suffix}. Supported: {', '.join(sorted(SUPPORTED))}")

    data = src.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    sid = f"src-{sha[:12]}"

    store = vault.load_store()
    adopted = vault.sync_from_vault(store)

    if sid in store["sources"] and not force:
        entry = store["sources"][sid]
        repaired = []
        if sid not in chunks.source_ids():  # index lost? rebuild passages, no model call
            pages, _ = extract_pages(config.VAULT / entry["original"])
            chunks.replace_source(sid, _make_chunks(sid, entry, pages))
            chunks.save()
            repaired.append("retrieval passages")
        vault.save_store(store)
        vault.render_all(store)
        return {
            "status": "already ingested", "source_id": sid,
            "note": vault.rel(vault.note_path(entry)), "repaired": repaired, "adopted": adopted,
        }

    # 1-2. read-only copy of the original inside the vault
    config.RAW.mkdir(parents=True, exist_ok=True)
    copy = config.RAW / src.name
    if copy.exists() and hashlib.sha256(copy.read_bytes()).hexdigest() != sha:
        copy = config.RAW / f"{src.stem} ({date.today().isoformat()}){src.suffix}"
    if not copy.exists():
        shutil.copy2(src, copy)
        os.chmod(copy, 0o444)
    if hashlib.sha256(copy.read_bytes()).hexdigest() != sha:
        raise IngestError("Copy verification failed: hash of the copy differs from the original.")

    # 3. text
    pages, meta_title = extract_pages(copy)
    if sum(len(p) for p in pages) < 200:
        raise IngestError("Almost no text could be extracted (scanned PDF?). Nothing was added.")

    # 4. model draft, validated by the harness
    draft = draft_note(pages, src.name, meta_title, llm)
    existing = store["sources"].get(sid)
    if existing:  # --force: refresh content, keep the human-facing name and folder
        title, folder, aliases = existing["title"], existing["folder"], existing.get("aliases", [])
    else:
        title, aliases = _choose_title(draft.get("title", ""), meta_title, src.name, store)
        folder = draft.get("folder") if draft.get("folder") in config.TOPIC_FOLDERS else config.FALLBACK_FOLDER

    entry = {
        "title": title,
        "folder": folder,
        "aliases": aliases,
        "summary": strip_page_refs(draft.get("summary", "")),
        "key_points": [
            {"point": strip_page_refs(kp.get("point", "")), "page": best_page(kp.get("point", ""), pages, kp.get("page"))}
            for kp in draft.get("key_points", [])[:8] if isinstance(kp, dict) and kp.get("point")
        ],
        "concepts": [],
        "original": vault.rel(copy),
        # provenance: where the file first came from (kept on re-ingest from vault/raw)
        "original_path": existing["original_path"] if existing else _home_relative(src),
        "sha256": sha,
        "pages": len(pages),
        "ingested": date.today().isoformat(),
    }
    store["sources"][sid] = entry
    if existing:
        vault.forget_source_mentions(store, sid)

    for c in draft.get("concepts", [])[:6]:
        if not isinstance(c, dict) or not c.get("name"):
            continue
        name, c_aliases = vault.clean_title(str(c["name"]))
        if vault.title_problems(name) or len(name.split()) > 5 or name.lower() == title.lower():
            continue
        cid = vault.find_concept(store, name) or next(
            (vault.find_concept(store, a) for a in c_aliases if vault.find_concept(store, a)), None
        )
        if cid is None:
            if name.lower() in vault.taken_titles(store):
                continue
            cid = f"c-{vault.slug(name)}"
            c_folder = c.get("folder") if c.get("folder") in config.TOPIC_FOLDERS else folder
            store["concepts"][cid] = {"title": name, "folder": c_folder, "aliases": c_aliases, "mentions": {}}
        concept = store["concepts"][cid]
        concept["aliases"] = sorted(set(concept.get("aliases", [])) | set(c_aliases) - {concept["title"]})
        definition = strip_page_refs(c.get("definition", ""))
        concept["mentions"][sid] = {"definition": definition, "page": best_page(name + " " + definition, pages, c.get("page"))}
        if cid not in entry["concepts"]:
            entry["concepts"].append(cid)

    dropped = vault.prune_concepts(store)

    # 5. write everything
    new_chunks = _make_chunks(sid, entry, pages)
    chunks.replace_source(sid, new_chunks)
    chunks.save()
    links = linker.link_concepts(store, llm)
    vault.save_store(store)
    rendered = vault.render_all(store)
    return {
        "status": "refreshed" if existing else "ingested",
        "source_id": sid,
        "note": vault.rel(vault.note_path(entry)),
        "concepts": [store["concepts"][c]["title"] for c in entry["concepts"]],
        "passages": len(new_chunks),
        "pages": len(pages),
        "notes_written": rendered["written"],
        "cross_links": links,
        "dropped_concepts": dropped,
        "stale_corrections": rendered["stale_corrections"],
        "adopted": adopted,
    }


def _home_relative(path: Path) -> str:
    """Record where the file came from without publishing the full home path."""
    return public_path(path)


def public_path(path) -> str:
    """Project-relative if inside the project, else ~/-relative: no user or drive names."""
    path = Path(path).expanduser().resolve()
    for base, prefix in ((config.ROOT, ""), (Path.home(), "~/")):
        try:
            return prefix + path.relative_to(base).as_posix()
        except ValueError:
            continue
    return str(path)


def ingest_many(paths: list[str], llm, chunks, force: bool = False):
    """Expand folders (e.g. ./vault/raw) into their supported files, in name order."""
    for p in paths:
        p = Path(p).expanduser()
        if p.is_dir():
            files = sorted(f for f in p.iterdir() if f.suffix.lower() in SUPPORTED and not f.name.startswith("."))
            if not files:
                raise IngestError(f"No supported files ({', '.join(sorted(SUPPORTED))}) in {p}")
            yield from files
        else:
            yield p


def _choose_title(proposed: str, meta_title: str | None, filename: str, store: dict) -> tuple[str, list[str]]:
    for candidate in (proposed, meta_title or "", filename):
        title, aliases = vault.clean_title(candidate)
        if title and not vault.title_problems(title):
            break
    else:
        raise IngestError(f"Could not derive a clean note name (model proposed '{proposed}').")
    base, n = title, 2
    while title.lower() in vault.taken_titles(store):
        title = f"{base} Part {n}"
        n += 1
    return title, aliases


def _make_chunks(sid: str, entry: dict, pages: list[str]) -> list[dict]:
    out = []
    for pno, text in enumerate(pages, start=1):
        for i, passage in enumerate(split_passages(text)):
            out.append({
                "chunk_id": f"{sid}:p{pno}:c{i}",
                "source_id": sid,
                "note_title": entry["title"],
                "note_path": vault.rel(vault.note_path(entry)),
                "original": entry["original"],
                "page": pno if len(pages) > 1 else None,
                "text": passage,
            })
    return out
