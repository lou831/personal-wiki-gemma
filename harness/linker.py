"""Cross-source concept links.

The harness proposes candidates, the model judges them:
  1. For every pair of concepts that come from *different* sources, compare their
     (reviewer-corrected) definitions with the local embedding model and keep the
     most similar pairs as candidates.
  2. One local-Gemma call judges each candidate: related or not, and why, in one
     sentence based only on the two definitions (prompts/link_rules.md).
  3. The harness keeps a pair only if the model said related, gave a reason, and a
     reviewer has not rejected it in review/corrections.yaml.

(A first version asked the model to find cross-source pairs on its own; it only
returned pairs from the same document, so candidate selection moved into code.)
"""

import itertools
import json
import re

from . import vault
from . import config
from .retrieval import Embedder

MAX_CANDIDATES = 8
MIN_SIMILARITY = 0.55


def candidate_pairs(view: dict) -> list[tuple[str, str, float]]:
    concepts = view["concepts"]
    ids = list(concepts)
    if len(ids) < 2:
        return []
    texts = [f"{concepts[c]['title']}: {next(iter(concepts[c]['mentions'].values()))['definition']}" for c in ids]
    vecs = Embedder.passages(texts)
    pairs = []
    for i, j in itertools.combinations(range(len(ids)), 2):
        a, b = ids[i], ids[j]
        if set(concepts[a]["mentions"]) & set(concepts[b]["mentions"]):
            continue  # same source: already linked as "also discussed in"
        sim = float(vecs[i] @ vecs[j])
        if sim >= MIN_SIMILARITY:
            pairs.append((a, b, sim))
    return sorted(pairs, key=lambda p: -p[2])[:MAX_CANDIDATES]


def link_concepts(store: dict, llm) -> list[str]:
    view, _ = vault.apply_corrections(store)
    candidates = candidate_pairs(view)
    if not candidates:
        store["links"] = []
        return []

    c = view["concepts"]

    def describe(cid):
        src = ", ".join(view["sources"][s]["title"] for s in c[cid]["mentions"])
        return f"{c[cid]['title']} (from {src}): {next(iter(c[cid]['mentions'].values()))['definition']}"

    listing = "\n\n".join(
        f"{n}. A = {describe(a)}\n   B = {describe(b)}" for n, (a, b, _) in enumerate(candidates, 1)
    )
    rules = (config.PROMPTS / "link_rules.md").read_text(encoding="utf-8")
    gen = llm.generate(
        [{"role": "system", "content": rules}, {"role": "user", "content": f"CANDIDATE PAIRS\n\n{listing}"}],
        max_tokens=900, temperature=0.0,
    )
    m = re.search(r"\[.*\]", gen.text, re.S)
    try:
        verdicts = json.loads(m.group(0)) if m else []
    except json.JSONDecodeError:
        verdicts = []

    rejected = {frozenset(x.strip().lower() for x in r.split("|"))
                for r in vault.load_corrections()["rejected_links"]}
    links, kept = [], []
    for v in verdicts if isinstance(verdicts, list) else []:
        try:
            a, b, _ = candidates[int(v.get("pair")) - 1]
        except (TypeError, ValueError, IndexError, AttributeError):
            continue
        why = str(v.get("why", "")).strip().rstrip(".")
        if v.get("related") is not True or len(why) < 15:
            continue
        if frozenset((c[a]["title"].lower(), c[b]["title"].lower())) in rejected:
            continue
        if any({a, b} == {l["a"], l["b"]} for l in links):
            continue
        links.append({"a": a, "b": b, "why": why + "."})
        kept.append(f"{c[a]['title']} ↔ {c[b]['title']}: {why}.")
    store["links"] = links
    return kept
