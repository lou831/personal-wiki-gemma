"""Paths and tunable settings for the personal wiki harness.

Everything the human browses lives in vault/. Everything only the machine
needs (chunks, embeddings, manifest, backups) lives in .wiki/, outside the vault.
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VAULT = ROOT / "vault"                 # Obsidian vault (open this folder in Obsidian)
RAW = VAULT / "raw"                    # original sources, read-only, never modified
WIKI = VAULT / "wiki"                  # generated + reviewed notes, in topic folders
INDEX_NOTE = VAULT / "index.md"        # grouped, human-readable landing page

MACHINE = ROOT / ".wiki"               # retrieval data, never shown in Obsidian
CHUNKS_FILE = MACHINE / "chunks.jsonl"
EMBEDDINGS_FILE = MACHINE / "embeddings.npy"
BACKUPS = MACHINE / "backups"

PROMPTS = ROOT / "prompts"
CORRECTIONS_FILE = ROOT / "review" / "corrections.yaml"   # reviewer fixes, applied at render time
OUTPUTS = ROOT / "outputs"             # saved answers, chat transcripts, logs, test reports

# --- Models (local only) ----------------------------------------------------
# Gemma 4 E4B, 4-bit MLX weights (~5.1 GB). WIKI_MODEL overrides it for the model
# comparison run (e.g. WIKI_MODEL=mlx-community/gemma-4-e2b-it-4bit ./wiki test).
LLM_ID = os.environ.get("WIKI_MODEL", "mlx-community/gemma-4-e4b-it-4bit")
EMBED_ID = "BAAI/bge-small-en-v1.5"            # 33M-param sentence embedder (~130 MB)
EMBED_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

# --- Retrieval ----------------------------------------------------------------
CHUNK_CHARS = 900          # target passage length; passages never cross a page boundary
CHUNK_OVERLAP_SENTENCES = 1
TOP_K = 6                  # passages handed to the model in ask mode
RRF_K = 60                 # reciprocal-rank-fusion constant for BM25 + vector ranks
MIN_EVIDENCE_COSINE = 0.55 # below this for every hit, ask refuses without calling the model
EXPAND_TOP_HITS = 3        # ask: also include the same-page neighbors of the top N hits
                           # (added 2026-09-27 after Test 2 missed the second half of p. 5)

# --- Generation -----------------------------------------------------------------
CHAT_MAX_TOKENS = 600
ASK_MAX_TOKENS = 450
NOTE_MAX_TOKENS = 1400
NOTE_INPUT_CHARS = 36_000  # how much source text the note writer sees per document
CHAT_HISTORY_CHARS = 12_000

# --- Vault layout -----------------------------------------------------------------
# A few topic folders. The note writer must pick one of these for every note.
TOPIC_FOLDERS = [
    "Energy and Utilities",
    "Transportation",
    "Climate Finance",
    "Coursework",
    "Technology",
]
FALLBACK_FOLDER = TOPIC_FOLDERS[0]
