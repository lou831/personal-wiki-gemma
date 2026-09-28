"""wiki: a personal wiki CLI running on a local Gemma model. Run `./wiki help`."""

import sys

from harness.offline import enforce_local

enforce_local()  # must run before any ML library is imported

import argparse  # noqa: E402
import time  # noqa: E402

from harness import config  # noqa: E402

HELP = f"""\
wiki — personal wiki on a local Gemma model (fully offline)

MODES
  chat                Talk with Wren, your assistant. Keeps conversation context,
                      handles casual questions and drafting, and looks in your notes
                      only when the question is about them.
                        in chat:  /ask <q>     standalone cited answer (chat history not used)
                                  /search <q>  raw passages
                                  /notes <q>   force a notes lookup inside the chat
                                  /reset  /save  /help  /exit
  ask "<question>" [--mode local]
                      One standalone, neutral, factual answer from retrieved evidence,
                      with citations — or an insufficient-evidence response.
                      Never uses chat history or the assistant persona.
                      Saved to outputs/answers/. Add --no-save to skip saving.
  search "<query>" [-k N]
                      Original passages with note and file paths. No model, no answer.
  ingest <file|folder...> [--force]
                      Add PDF/Markdown/text sources (e.g. `wiki ingest ./vault/raw`).
                      Copies each original (read-only) to vault/raw/, has local Gemma
                      draft a source note + concept notes in vault/wiki/, indexes
                      passages, links related concepts, rebuilds vault/index.md.
                      The same file again = "already ingested" (content hash), never a
                      duplicate. --force re-drafts it but keeps the note's name.
  help, --help        This text.

MAINTENANCE
  check               Lint the vault: names, H1s, links, originals, index, duplicates.
  rename "<old>" "<new>"   Rename a note; backs up, fixes links and retrieval paths.
  reindex             Rebuild passages/embeddings from vault/raw/ and re-render notes
                      with reviewer corrections (no model call).
  link                Re-run the cross-source concept linker (one model call).
  stats               Sources, notes, passages, memory, blocked network attempts.
  test                Run the assignment test suite and write a report.

CONFIGURATION (harness/config.py)
  mode        local (the only mode; no online mode is configured)
  model       {config.LLM_ID}  (MLX, 4-bit)
  embeddings  {config.EMBED_ID}
  vault       vault/  (raw/ originals, wiki/ notes, index.md)   prompts: prompts/
  reviewer corrections: review/corrections.yaml   machine index: .wiki/

REQUIRED INPUTS
  The model and embedding weights must already be in the local Hugging Face cache
  (downloaded once while online; see README). Networking is blocked in-process;
  there is no cloud fallback.
"""


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="wiki", add_help=False)
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("help")
    sub.add_parser("chat")
    p = sub.add_parser("ask"); p.add_argument("question", nargs="+"); p.add_argument("--no-save", action="store_true")
    p.add_argument("--mode", choices=["local", "online"], default="local")
    p = sub.add_parser("search"); p.add_argument("query", nargs="+"); p.add_argument("-k", type=int, default=5)
    p = sub.add_parser("ingest"); p.add_argument("paths", nargs="+"); p.add_argument("--force", action="store_true")
    sub.add_parser("check")
    p = sub.add_parser("rename"); p.add_argument("old"); p.add_argument("new")
    sub.add_parser("reindex")
    sub.add_parser("link")
    sub.add_parser("stats")
    sub.add_parser("test")

    if not argv or argv[0] in ("-h", "--help"):
        print(HELP)
        return 0
    args = parser.parse_args(argv)
    if args.cmd in (None, "help"):
        print(HELP)
        return 0

    if args.cmd == "test":
        from tests.run_tests import main as run_tests
        return run_tests()

    from harness.core import Harness, memory_snapshot  # heavy imports only after arg parsing

    h = Harness()
    if args.cmd == "search":
        return cmd_search(h, " ".join(args.query), args.k)
    if args.cmd == "ask":
        if args.mode != "local":
            print("error: online mode is not configured in this project; local is the only mode.", file=sys.stderr)
            return 2
        return cmd_ask(h, " ".join(args.question), save=not args.no_save)
    if args.cmd == "ingest":
        return cmd_ingest(h, args.paths, args.force)
    if args.cmd == "chat":
        return cmd_chat(h)
    if args.cmd == "check":
        return cmd_check(h)
    if args.cmd == "rename":
        from harness import vault
        info = vault.rename_note(args.old, args.new, chunks=h.chunks)
        for k, v in info.items():
            print(f"{k:>26}: {v}")
        return 0
    if args.cmd == "reindex":
        return cmd_reindex(h)
    if args.cmd == "link":
        from harness import linker, vault
        store = vault.load_store()
        vault.sync_from_vault(store)
        pairs = linker.link_concepts(store, h.llm)
        vault.save_store(store)
        vault.render_all(store)
        print("\n".join(f"  {p}" for p in pairs) or "  (no cross-source links proposed)")
        return 0
    if args.cmd == "stats":
        return cmd_stats(h, memory_snapshot)
    return 1


def cmd_search(h, query: str, k: int) -> int:
    print(f"[search · local · retrieval only, no language model]  “{query}”\n")
    t0 = time.perf_counter()
    hits = h.search(query, k)
    if not hits:
        print("No passages indexed yet. Run `wiki ingest <file>` first.")
        return 1
    for h_ in hits:
        print("\n".join(h.source_lines(h_.rank, h_)))
        print(f"    score:    fused {h_.fused:.4f} · cosine {h_.cosine:.2f} · bm25 {h_.bm25:.1f}")
        print(f"    passage:  {h_.chunk['text']}\n")
    print(f"({len(hits)} passages in {time.perf_counter() - t0:.2f}s · no model call)")
    return 0


def cmd_ask(h, question: str, save: bool = True) -> int:
    print(f"[ask · local · {config.LLM_ID} · standalone, no chat history]  “{question}”\n")
    r = h.ask(question, save=save)
    print(r.answer)
    if r.citations:
        print("\nSources:")
        for n, hit in r.citations:
            print("\n".join(h.source_lines(n, hit, excerpt=220, focus=r.answer)))
    g = r.generation
    speed = f" · {g.prompt_tokens} prompt tok · {g.generation_tps:.1f} tok/s" if g else ""
    print(f"\n({r.status} · {r.timings.get('total_s', 0):.1f}s{speed}"
          + (f" · model load {h.llm.load_seconds:.1f}s" if h.llm.load_seconds else "")
          + (f" · saved to {r.saved_path.relative_to(config.ROOT)}" if r.saved_path else "") + ")")
    return 0


def cmd_ingest(h, paths: list[str], force: bool) -> int:
    from harness.ingest import IngestError, ingest_many

    print(f"[ingest · local · {config.LLM_ID}]")
    status = 0
    for path in ingest_many(paths, h.llm, h.chunks, force):
        print(f"Ingesting {path} …", flush=True)
        try:
            info = h.ingest(path, force=force)
        except IngestError as e:
            print(f"  error: {e}")
            status = 1
            continue
        print(f"  {info['status']}: vault/{info['note']}")
        for key in ("concepts", "passages", "pages", "repaired", "adopted", "seconds"):
            if info.get(key):
                print(f"  {key}: {info[key]}")
    return status


def cmd_chat(h) -> int:
    session = h.chat()
    print("Loading the local model …", flush=True)
    h.llm.load()
    print(f"[chat · local · {config.LLM_ID}] Wren is ready (loaded in {h.llm.load_seconds:.1f}s). "
          "/help for commands, /exit to quit.\n")
    while True:
        try:
            line = input("you › ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        cmd, _, rest = line.partition(" ")
        if cmd == "/exit":
            break
        if cmd == "/help":
            print(HELP)
        elif cmd == "/reset":
            session.history.clear()
            print("(conversation cleared)\n")
        elif cmd == "/save":
            print(f"(saved to {h.save_chat(session)})\n")
        elif cmd == "/ask":
            print("[ask mode · standalone, chat history not used]")
            cmd_ask(h, rest)
            print()
        elif cmd == "/search":
            cmd_search(h, rest, 5)
        else:
            force = rest if cmd == "/notes" else None
            print("wren › ", end="", flush=True)
            t0 = time.perf_counter()
            turn = session.send(line if force is None else rest,
                                emit=lambda s: print(s, end="", flush=True), force_search=force)
            print()
            if turn.search_query:
                print(f"\n  (looked in notes for “{turn.search_query}”)")
                for i, hit in enumerate(turn.hits, 1):
                    c = hit.chunk
                    print(f"  [{i}] {c['note_title']}" + (f", p. {c['page']}" if c.get("page") else "")
                          + f" — vault/{c['note_path']}")
            print(f"  ({time.perf_counter() - t0:.1f}s)\n")
    path = h.save_chat(session)
    if path:
        print(f"Chat saved to {path.relative_to(config.ROOT)}")
    return 0


def cmd_check(h) -> int:
    from harness import vault

    problems = vault.check_vault(chunks=h.chunks)
    notes = vault.all_notes()
    print(f"{len(notes)} notes, {len(h.chunks.chunks)} passages checked.")
    for p in problems:
        print(f"  ✗ {p}")
    print("All checks passed." if not problems else f"{len(problems)} problem(s).")
    return 1 if problems else 0


def cmd_reindex(h) -> int:
    from harness import ingest, vault

    store = vault.load_store()
    for change in vault.sync_from_vault(store):
        print(f"  {change}")
    vault.save_store(store)
    vault.render_all(store)
    for sid, entry in store["sources"].items():
        pages, _ = ingest.extract_pages(config.VAULT / entry["original"])  # vault/raw/…
        h.chunks.replace_source(sid, ingest._make_chunks(sid, entry, pages))
    for sid in h.chunks.source_ids() - set(store["sources"]):
        h.chunks.replace_source(sid, [])
    h.chunks.save()
    print(f"Reindexed {len(store['sources'])} sources into {len(h.chunks.chunks)} passages.")
    return 0


def cmd_stats(h, memory_snapshot) -> int:
    from harness import vault
    from harness.offline import BLOCKED

    store = vault.load_store()
    print(f"sources:  {len(store['sources'])}")
    for s in store["sources"].values():
        print(f"  - {s['folder']}/{s['title']}  ({s['pages']} pages, from {s['original']})")
    print(f"concepts: {len(store['concepts'])}")
    print(f"notes:    {len(vault.all_notes())} (+ index.md)")
    print(f"passages: {len(h.chunks.chunks)}")
    print(f"memory:   {memory_snapshot()}")
    print(f"network attempts blocked this run: {len(BLOCKED)}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(130)
    except (FileNotFoundError, FileExistsError, ValueError, RuntimeError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
