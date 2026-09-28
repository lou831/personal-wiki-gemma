"""The RAG workflow behind `wiki ask`: retrieve -> gate -> generate -> verify citations.

Ask is deliberately stateless. It builds a fresh two-message prompt (research
rules + question with evidence) and never sees chat history or the assistant
persona. Every answer either carries citations that map to real passages or is
replaced by an insufficient-evidence response.
"""

import re
import time
from dataclasses import dataclass, field

from . import config
from .retrieval import Hit, cite_label


@dataclass
class AskResult:
    question: str
    status: str                      # "answered" | "insufficient"
    answer: str
    reason: str = ""
    citations: list[tuple[int, Hit]] = field(default_factory=list)
    hits: list[Hit] = field(default_factory=list)
    messages: list[dict] = field(default_factory=list)   # exact prompt sent (for audits/tests)
    raw_output: str = ""
    timings: dict = field(default_factory=dict)
    generation: object = None
    saved_path: object = None


def evidence_block(hits: list[Hit]) -> str:
    return "\n\n".join(f"[{i}] ({cite_label(h.chunk)})\n{h.chunk['text']}" for i, h in enumerate(hits, 1))


def expand_with_neighbors(hits: list[Hit], chunks) -> list[Hit]:
    """A fact can straddle two passages of the same page. For the top hits, add the
    neighboring passage(s) right after the hit, so the model sees the whole context."""
    have = {h.chunk["chunk_id"] for h in hits}
    out = []
    for h in hits:
        out.append(h)
        if h.rank <= config.EXPAND_TOP_HITS:
            for nb in chunks.neighbors(h.chunk):
                if nb["chunk_id"] not in have:
                    have.add(nb["chunk_id"])
                    out.append(Hit(chunk=nb, rank=h.rank, fused=0.0, cosine=h.cosine, bm25=0.0, neighbor_of=h.chunk["chunk_id"]))
    return out


def ask(question: str, chunks, llm, k: int = config.TOP_K) -> AskResult:
    t0 = time.perf_counter()
    hits = chunks.search(question, k)
    t_retrieve = time.perf_counter() - t0

    best = max((h.cosine for h in hits), default=0.0)
    if not hits or best < config.MIN_EVIDENCE_COSINE:
        return AskResult(
            question, "insufficient",
            "Insufficient evidence: nothing in the wiki is close enough to this question to answer it.",
            reason=f"retrieval gate (best similarity {best:.2f} < {config.MIN_EVIDENCE_COSINE})",
            hits=hits, timings={"retrieve_s": t_retrieve, "total_s": time.perf_counter() - t0},
        )

    hits = expand_with_neighbors(hits, chunks)
    rules = (config.PROMPTS / "research_rules.md").read_text(encoding="utf-8")
    messages = [
        {"role": "system", "content": rules},
        {"role": "user", "content": f"Question: {question}\n\nEvidence passages:\n\n{evidence_block(hits)}"},
    ]
    gen = llm.generate(messages, max_tokens=config.ASK_MAX_TOKENS, temperature=0.0)
    text = gen.text.strip()
    timings = {"retrieve_s": t_retrieve, "generate_s": gen.seconds}

    if "INSUFFICIENT_EVIDENCE" in text.upper():
        missing = text.split(":", 1)[1].strip() if ":" in text else ""
        return AskResult(
            question, "insufficient",
            "Insufficient evidence: the retrieved passages do not answer this question."
            + (f" Missing: {missing}" if missing else ""),
            reason="model reported insufficient evidence", hits=hits, messages=messages,
            raw_output=text, generation=gen, timings={**timings, "total_s": time.perf_counter() - t0},
        )

    cited = sorted({int(n) for n in re.findall(r"\[(\d+)\]", text)})
    valid = [n for n in cited if 1 <= n <= len(hits)]
    for n in set(cited) - set(valid):
        text = text.replace(f"[{n}]", "")
    if not valid:
        return AskResult(
            question, "insufficient",
            "Insufficient evidence: the model's draft answer cited no passages, so it was withheld.",
            reason="no valid citations in model output", hits=hits, messages=messages,
            raw_output=gen.text, generation=gen, timings={**timings, "total_s": time.perf_counter() - t0},
        )

    return AskResult(
        question, "answered", re.sub(r"[ \t]{2,}", " ", text).strip(),
        citations=[(n, hits[n - 1]) for n in valid], hits=hits, messages=messages,
        raw_output=gen.text, generation=gen, timings={**timings, "total_s": time.perf_counter() - t0},
    )
