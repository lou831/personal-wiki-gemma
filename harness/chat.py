"""Chat mode: a personal assistant with personality and conversation memory.

The model answers directly by default. It may ask the harness for notes by
replying with a single `<<search: query>>` line; the harness runs the retrieval
tool, sends back numbered passages, and the model answers again. Nothing forces
a lookup, so small talk and drafting never touch the wiki.
"""

import re
from dataclasses import dataclass, field

from . import config, vault
from .retrieval import Hit, cite_label

_TOOL = re.compile(r"^\s*<<\s*search\s*:\s*(.+?)\s*>>", re.I | re.S)
# Harness routing rule: a message that points at the user's own material always
# gets a notes lookup; everything else is left to the model's judgment.
_NOTES_REF = re.compile(
    r"\b(my|our|the)\s+(notes?|wiki|documents?|docs|files?|sources?|readings?|pdfs?)\b"
    r"|\bin my (vault|wiki)\b|\baccording to (my|the) (notes|sources|documents)\b", re.I)
_BOILERPLATE = re.compile(
    r"^(what|tell me what|can you tell me what)\s+(do|does|did)?\s*(my|our|the)\s+"
    r"(notes?|wiki|documents?|docs|files?|sources?)\s+(say|said|have|mention)\s+(about|on|regarding)\s+", re.I)


def notes_route(text: str) -> str | None:
    """Return a search query if the harness rule says this turn needs the notes."""
    if not _NOTES_REF.search(text):
        return None
    return _BOILERPLATE.sub("", text.strip()).rstrip("?.! ") or text


@dataclass
class ChatTurn:
    user: str
    reply: str = ""
    search_query: str | None = None
    route: str = "answer"          # "answer" | "rule" (harness) | "model" (model asked) | "forced" (/notes)
    hits: list[Hit] = field(default_factory=list)
    generations: list = field(default_factory=list)


class ChatSession:
    def __init__(self, chunks, llm):
        self.chunks = chunks
        self.llm = llm
        self.history: list[dict] = []
        self.turns: list[ChatTurn] = []

    # --- prompt assembly ---------------------------------------------------------------------
    def system_prompt(self) -> str:
        persona = (config.PROMPTS / "assistant.md").read_text(encoding="utf-8").strip()
        tools = (config.PROMPTS / "chat_tools.md").read_text(encoding="utf-8").strip()
        store = vault.load_store()
        titles = [f"- {s['title']}: {s['summary'].split('. ')[0]}" for s in store["sources"].values()]
        return persona + "\n\n" + tools.replace("{SOURCES}", "\n".join(titles) or "- (empty)")

    def _messages(self, extra: list[dict]) -> list[dict]:
        return [{"role": "system", "content": self.system_prompt()}, *self.history, *extra]

    def _trim(self) -> None:
        while sum(len(m["content"]) for m in self.history) > config.CHAT_HISTORY_CHARS and len(self.history) > 2:
            self.history = self.history[2:]
            while self.history and self.history[0]["role"] != "user":
                self.history = self.history[1:]

    # --- one turn -----------------------------------------------------------------------------------
    def send(self, text: str, emit=lambda s: None, force_search: str | None = None) -> ChatTurn:
        turn = ChatTurn(user=text)
        user_msg = {"role": "user", "content": text}

        query = force_search
        turn.route = "forced" if force_search else "answer"
        if query is None and (query := notes_route(text)) is not None:
            turn.route = "rule"
        if query is None:
            gate = _StreamGate(emit)
            gen = self.llm.generate(self._messages([user_msg]), config.CHAT_MAX_TOKENS, 0.7, on_text=gate.feed)
            turn.generations.append(gen)
            m = _TOOL.match(gen.text)
            if m:
                query = m.group(1).strip()
                turn.route = "model"
            else:
                gate.flush()
                turn.reply = gen.text
                self.history += [user_msg, {"role": "assistant", "content": gen.text}]

        if query is not None:
            turn.search_query = query
            turn.hits = self.chunks.search(query, 4)
            tool_msg = {"role": "user", "content": _tool_result(query, turn.hits)}
            call_msg = {"role": "assistant", "content": f"<<search: {query}>>"}
            gen = self.llm.generate(
                self._messages([user_msg, call_msg, tool_msg]), config.CHAT_MAX_TOKENS, 0.7, on_text=emit
            )
            turn.generations.append(gen)
            turn.reply = gen.text
            self.history += [user_msg, call_msg, tool_msg, {"role": "assistant", "content": gen.text}]

        self.turns.append(turn)
        self._trim()
        return turn

    def transcript_markdown(self) -> str:
        lines = ["# Chat with Wren", ""]
        for t in self.turns:
            lines += [f"**You:** {t.user}", ""]
            if t.search_query:
                lines += [f"*Searched notes for “{t.search_query}”*", ""]
            lines += [f"**Wren:** {t.reply}", ""]
            for i, h in enumerate(t.hits, 1):
                lines.append(f"- [{i}] [[{h.chunk['note_title']}]] ({cite_label(h.chunk)})")
            if t.hits:
                lines.append("")
        return "\n".join(lines)


def _tool_result(query: str, hits: list[Hit]) -> str:
    if not hits:
        return f"NOTES TOOL RESULT for “{query}” (sent by the harness, not typed by the user): no matching passages."
    body = "\n\n".join(f"[{i}] ({cite_label(h.chunk)})\n{h.chunk['text']}" for i, h in enumerate(hits, 1))
    return f"NOTES TOOL RESULT for “{query}” (sent by the harness, not typed by the user):\n\n{body}"


class _StreamGate:
    """Hold back the start of a reply: a tool call or a leaked reasoning block
    ("<|channel>…<channel|>") is never shown to the user."""

    OPEN, CLOSE = "<|channel>", "<channel|>"

    def __init__(self, emit):
        self.emit, self.buf, self.state = emit, "", "undecided"

    def feed(self, text: str) -> None:
        if self.state == "stream":
            self.emit(text)
            return
        if self.state == "tool":
            return
        self.buf += text
        while True:
            head = self.buf.lstrip()
            if head.startswith(self.OPEN) or (head and self.OPEN.startswith(head)):
                if self.CLOSE not in head:
                    return  # still inside (or starting) a reasoning block: keep hiding
                self.buf = head.split(self.CLOSE, 1)[1]
                continue
            break
        if len(head) >= 2:
            if head.startswith("<<"):
                self.state = "tool"
            else:
                self.state = "stream"
                self.emit(head)

    def flush(self) -> None:
        """Called when the reply was not a tool call: show whatever was held back."""
        head = self.buf.lstrip()
        if self.state == "undecided" and head and not head.startswith(self.OPEN):
            self.emit(head)
        elif self.state == "tool":  # looked like a tool call but was not one
            self.emit(head)
