"""The retrieval tool: find original passages for a query. No generation here.

Hybrid search over passage chunks stored in .wiki/:
  * BM25 (rank_bm25) catches exact terms, numbers and acronyms ("CBTC", "67").
  * Dense vectors (sentence-transformers, bge-small) catch paraphrases.
  * Reciprocal rank fusion merges the two rankings into one list.

Used three ways: `wiki search` prints hits directly, `wiki ask` feeds them to
the RAG workflow, and chat calls it as a tool when the model asks for notes.
"""

import json
import re
from dataclasses import dataclass

import numpy as np

from . import config

_STOP = set(
    "a an and are as at be by did do does for from has have how i in is it its of on or "
    "that the their this to was were what when where which who why will with".split()
)


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+(?:[&'.\-][a-z0-9]+)*", text.lower())
    return [w for w in words if w not in _STOP]


@dataclass
class Hit:
    chunk: dict
    rank: int
    fused: float
    cosine: float
    bm25: float
    neighbor_of: str | None = None   # set when added as same-page context for another hit


class Embedder:
    _model = None

    @classmethod
    def get(cls):
        if cls._model is None:
            from sentence_transformers import SentenceTransformer

            cls._model = SentenceTransformer(config.EMBED_ID, device="cpu")
        return cls._model

    @classmethod
    def passages(cls, texts: list[str]) -> np.ndarray:
        vecs = cls.get().encode(texts, batch_size=32, normalize_embeddings=True)
        return np.asarray(vecs, dtype=np.float32)

    @classmethod
    def query(cls, text: str) -> np.ndarray:
        vec = cls.get().encode([config.EMBED_QUERY_PREFIX + text], normalize_embeddings=True)
        return np.asarray(vec[0], dtype=np.float32)


class ChunkStore:
    """chunks.jsonl + embeddings.npy, kept row-aligned."""

    def __init__(self):
        self.chunks: list[dict] = []
        self.vectors = np.zeros((0, 384), dtype=np.float32)
        self._bm25 = None
        self.load()

    def load(self) -> None:
        if config.CHUNKS_FILE.exists():
            with config.CHUNKS_FILE.open(encoding="utf-8") as f:
                self.chunks = [json.loads(line) for line in f if line.strip()]
        if config.EMBEDDINGS_FILE.exists():
            self.vectors = np.load(config.EMBEDDINGS_FILE)
        if len(self.chunks) != len(self.vectors):
            raise RuntimeError(
                "Index is out of sync (chunks vs embeddings). Run `wiki reindex` to rebuild it."
            )
        self._bm25 = None

    def save(self) -> None:
        config.MACHINE.mkdir(parents=True, exist_ok=True)
        with config.CHUNKS_FILE.open("w", encoding="utf-8") as f:
            for c in self.chunks:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        np.save(config.EMBEDDINGS_FILE, self.vectors)
        self._bm25 = None

    # --- editing ---------------------------------------------------------------
    def replace_source(self, source_id: str, new_chunks: list[dict]) -> None:
        """Drop every chunk from this source, then add the new ones (no duplicates)."""
        keep = [i for i, c in enumerate(self.chunks) if c["source_id"] != source_id]
        self.chunks = [self.chunks[i] for i in keep]
        self.vectors = self.vectors[keep] if len(keep) else np.zeros((0, 384), np.float32)
        if new_chunks:
            vecs = Embedder.passages([c["text"] for c in new_chunks])
            self.chunks.extend(new_chunks)
            self.vectors = np.vstack([self.vectors, vecs])

    def update_note_path(self, source_id: str, note_path: str, note_title: str) -> int:
        n = 0
        for c in self.chunks:
            if c["source_id"] == source_id:
                c["note_path"], c["note_title"] = note_path, note_title
                n += 1
        return n

    def neighbors(self, chunk: dict) -> list[dict]:
        """Passages directly before/after this one on the same page."""
        m = re.match(r"(.+):p(\d+):c(\d+)$", chunk["chunk_id"])
        if not m:
            return []
        base, page, i = m.group(1), m.group(2), int(m.group(3))
        wanted = {f"{base}:p{page}:c{i - 1}", f"{base}:p{page}:c{i + 1}"}
        return [c for c in self.chunks if c["chunk_id"] in wanted]

    def source_ids(self) -> set[str]:
        return {c["source_id"] for c in self.chunks}

    # --- searching -----------------------------------------------------------
    def _bm25_index(self):
        if self._bm25 is None:
            from rank_bm25 import BM25Okapi

            corpus = [tokenize(c["note_title"] + " " + c["text"]) for c in self.chunks]
            self._bm25 = BM25Okapi(corpus)
        return self._bm25

    def search(self, query: str, k: int = config.TOP_K) -> list[Hit]:
        if not self.chunks:
            return []
        bm25_scores = np.asarray(self._bm25_index().get_scores(tokenize(query)))
        cos_scores = self.vectors @ Embedder.query(query)

        bm25_rank = np.argsort(-bm25_scores)
        cos_rank = np.argsort(-cos_scores)
        fused = np.zeros(len(self.chunks))
        for rank, idx in enumerate(bm25_rank):
            if bm25_scores[idx] > 0:
                fused[idx] += 1.0 / (config.RRF_K + rank + 1)
        for rank, idx in enumerate(cos_rank):
            fused[idx] += 1.0 / (config.RRF_K + rank + 1)

        order = np.argsort(-fused)[:k]
        return [
            Hit(
                chunk=self.chunks[i],
                rank=r + 1,
                fused=float(fused[i]),
                cosine=float(cos_scores[i]),
                bm25=float(bm25_scores[i]),
            )
            for r, i in enumerate(order)
        ]


def cite_label(chunk: dict) -> str:
    page = f", p. {chunk['page']}" if chunk.get("page") else ""
    return f"{chunk['note_title']}{page}"
