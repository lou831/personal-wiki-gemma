"""The harness: one object that owns the model, the index and the modes.

It decides which mode runs, which prompt file each mode gets, what context goes
into each model call (chat history for chat only; retrieved evidence for ask
only), when the retrieval tool runs, how citations are checked and printed,
how errors surface, and where outputs and measurements are saved.
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path

from . import config, ingest as ingest_mod, rag, vault
from .chat import ChatSession
from .llm import LocalLLM
from .offline import BLOCKED
from .retrieval import ChunkStore, cite_label

_QSTOP = set(
    "a an and are as at be by can could did do does for from has have how i in is it its me my "
    "of on or should tell that the their them there these this to was were what when where which "
    "who whom why will with would according many much".split()
)


def memory_snapshot() -> dict:
    import psutil

    snap = {
        "process_rss_gb": round(psutil.Process().memory_info().rss / 1e9, 2),
        "system_available_gb": round(psutil.virtual_memory().available / 1e9, 2),
    }
    try:
        import mlx.core as mx

        snap["mlx_active_gb"] = round(mx.get_active_memory() / 1e9, 2)
        snap["mlx_peak_gb"] = round(mx.get_peak_memory() / 1e9, 2)
    except Exception:
        pass
    return snap


def short_title(question: str, words: int = 6) -> str:
    kept = [w for w in re.findall(r"[A-Za-z0-9&'\-]+", question) if w.lower() not in _QSTOP]
    title, _ = vault.clean_title(" ".join(kept[:words]) or "Question")
    return title


def best_excerpt(text: str, focus: str, limit: int) -> str:
    """The sentence of a passage that overlaps most with `focus` (e.g. the answer)."""
    if len(text) <= limit:
        return text
    from .retrieval import tokenize

    sentences = re.split(r"(?<=[.!?])\s+|\s(?=▪)", text)
    want = set(tokenize(focus))
    best = max(range(len(sentences)), key=lambda i: len(want & set(tokenize(sentences[i]))))
    out = sentences[best]
    i = best + 1
    while i < len(sentences) and len(out) + len(sentences[i]) < limit:
        out += " " + sentences[i]
        i += 1
    out = out if len(out) <= limit else out[:limit].rsplit(" ", 1)[0]
    return ("… " if best > 0 else "") + out + (" …" if i < len(sentences) or len(out) < len(text) else "")


class Harness:
    def __init__(self):
        self.chunks = ChunkStore()
        self.llm = LocalLLM()

    # --- logging / saved outputs --------------------------------------------------------------
    def log(self, event: dict) -> None:
        path = config.OUTPUTS / "logs" / "runs.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        event = {"time": datetime.now().isoformat(timespec="seconds"), "model": config.LLM_ID,
                 "network_blocked": list(BLOCKED), **event, "memory": memory_snapshot()}
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def _save(self, kind: str, title: str, text: str) -> Path:
        folder = config.OUTPUTS / kind
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{datetime.now().strftime('%Y-%m-%d %H%M')} {title}.md"
        n = 2
        while path.exists():
            path = folder / f"{datetime.now().strftime('%Y-%m-%d %H%M')} {title} {n}.md"
            n += 1
        path.write_text(text, encoding="utf-8")
        return path

    # --- modes ------------------------------------------------------------------------------------------
    def search(self, query: str, k: int = 5):
        t0 = time.perf_counter()
        hits = self.chunks.search(query, k)
        self.log({"mode": "search", "query": query, "hits": [h.chunk["chunk_id"] for h in hits],
                  "seconds": round(time.perf_counter() - t0, 3), "model_calls": self.llm.calls})
        return hits

    def ask(self, question: str, save: bool = True) -> rag.AskResult:
        result = rag.ask(question, self.chunks, self.llm)
        g = result.generation
        record = {
            "mode": "ask", "question": question, "status": result.status, "reason": result.reason,
            "citations": [h.chunk["chunk_id"] for _, h in result.citations],
            "timings": {k: round(v, 2) for k, v in result.timings.items()},
            "load_s": round(self.llm.load_seconds, 2),
        }
        if g:
            record.update(prompt_tokens=g.prompt_tokens, generation_tokens=g.generation_tokens,
                          prompt_tps=round(g.prompt_tps, 1), generation_tps=round(g.generation_tps, 1))
        if save:
            result.saved_path = self._save("answers", short_title(question), self.render_ask_md(result))
            record["saved"] = str(result.saved_path.relative_to(config.ROOT))
        self.log(record)
        return result

    def ingest(self, path: str, force: bool = False) -> dict:
        t0 = time.perf_counter()
        info = ingest_mod.ingest(path, self.llm, self.chunks, force=force)
        info["seconds"] = round(time.perf_counter() - t0, 1)
        self.log({"mode": "ingest", "path": ingest_mod.public_path(path), **info})
        return info

    def chat(self) -> ChatSession:
        return ChatSession(self.chunks, self.llm)

    def save_chat(self, session: ChatSession) -> Path | None:
        if not session.turns:
            return None
        path = self._save("chats", "Chat with Wren", session.transcript_markdown())
        self.log({"mode": "chat", "turns": len(session.turns),
                  "searches": [t.search_query for t in session.turns if t.search_query],
                  "saved": str(path.relative_to(config.ROOT))})
        return path

    # --- rendering ----------------------------------------------------------------------------------------
    @staticmethod
    def source_lines(n: int, hit, excerpt: int = 0, focus: str = "") -> list[str]:
        c = hit.chunk
        page = f"#page={c['page']}" if c.get("page") else ""
        lines = [f"[{n}] {cite_label(c)}",
                 f"    note:     vault/{c['note_path']}",
                 f"    original: vault/{c['original']}{page}"]
        if excerpt:
            lines.append(f"    passage:  “{best_excerpt(c['text'], focus, excerpt)}”")
        return lines

    def render_ask_md(self, r: rag.AskResult) -> str:
        lines = [f"# {short_title(r.question)}", "", f"**Question:** {r.question}", "",
                 f"**Status:** {r.status}", "", "## Answer", "", r.answer, ""]
        if r.citations:
            lines += ["## Sources", ""]
            for n, h in r.citations:
                c = h.chunk
                page = f"#page={c['page']}" if c.get("page") else ""
                lines += [f"{n}. [[{c['note_title']}]] — [[{Path(c['original']).name}{page}|{cite_label(c)}]]",
                          f"   > {c['text']}", ""]
        lines += ["## Run Details", "", f"- Model: `{config.LLM_ID}` (local)",
                  f"- Timings: {', '.join(f'{k} {v:.2f}s' for k, v in r.timings.items())}"]
        if r.reason:
            lines.append(f"- Reason: {r.reason}")
        return "\n".join(lines) + "\n"
