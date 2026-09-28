# Test Report

- **Run:** 2026-09-27 16:49:01 · Online Run
- **Machine:** macOS 26.6.2, Apple M4, 16 GB unified memory
- **Model / runtime:** `mlx-community/gemma-4-e4b-it-4bit` (Gemma 4 E4B, 4-bit MLX) via mlx-lm 0.31.3 / mlx 0.32.2; embeddings `BAAI/bge-small-en-v1.5` via sentence-transformers 6.1.0
- **Mode:** local (in-process network guard on; no online mode configured)
- **Network (OS view):** default route via en0 (network connected)
- **Wiki:** 3 sources, 11 concepts, 14 notes, 180 passages
- **Model load:** 5.2s · **suite time:** 177.2s
- **Memory at end:** MLX peak 4.95 GB, MLX active 4.2 GB, process RSS 0.33 GB, system available 2.85 GB
- **Result:** **17/17 passed**

Evidence cards: [Test 1 - Rail Capacity](<Test 1 - Rail Capacity.md>), [Test 2 - PG&E Problem Statements](<Test 2 - PG&E Problem Statements.md>), [Test 3 - Final Presentation Format](<Test 3 - Final Presentation Format.md>), [Test 4 - Unsupported Electricity Rate](<Test 4 - Unsupported Electricity Rate.md>) · [Mode Checks](<Mode Checks.md>)

| Test | Result | Time (s) | MLX peak (GB) |
|---|---|---|---|
| search: raw passages, no generation | PASS | 0.64 | 4.2 |
| ask: Test 1 Rail Capacity | PASS | 13.88 | 4.91 |
| ask: Test 2 PG&E Problem Statements | PASS | 11.38 | 4.94 |
| ask: Test 3 Final Presentation Format | PASS | 11.42 | 4.95 |
| ask: Test 4 Unsupported Electricity Rate | PASS | 11.69 | 4.95 |
| chat: “what can we do?” explains capabilities | PASS | 12.02 | 4.95 |
| chat: “what can you help me with?” explains capabilities | PASS | 8.19 | 4.95 |
| chat: casual drafting (no forced lookup) | PASS | 6.43 | 4.95 |
| chat: “make that shorter” uses the conversation | PASS | 5.92 | 4.95 |
| chat: conversational follow-up | PASS | 6.45 | 4.95 |
| separation: ask ignores chat history | PASS | 13.21 | 4.95 |
| separation: chat-only claim is not ask evidence | PASS | 9.95 | 4.95 |
| chat: uses notes tool and cites when asked about notes | PASS | 23.76 | 4.95 |
| vault: names, H1s, links, sources, index, corrections | PASS | 0.04 | 4.95 |
| originals in raw/: unchanged and read-only | PASS | 0.0 | 4.95 |
| re-ingest: no duplicates, names kept | PASS | 0.07 | 4.95 |
| local only: no network use, no cloud fallback | PASS | 0.0 | 4.95 |

## Details

### search: raw passages, no generation — PASS

hits=5; verbatim from original page=5; paths exist=5; model calls during search=0

### ask: Test 1 Rail Capacity — PASS

expected passage retrieved=True; all expected passages given to the model=True; status is answered=True; cites the expected source=True; cites every expected passage=True; answer contains ['\\b24\\b', '\\b30\\b']=True

```text
Automation could raise practical capacity limits from 24 to 30 trains per hour or more [1]. Modernization can increase train throughput from 24 trains per hour to 30+ trains per hour [3]. Additionally, new technology allows for 30 trains per hour throughput using existing tunnel infrastructure [7].
```

### ask: Test 2 PG&E Problem Statements — PASS

expected passage retrieved=True; all expected passages given to the model=True; status is answered=True; cites the expected source=True; cites every expected passage=True; answer contains ['(graduated|retired)[^.]{0,40}\\b17\\b|\\b17\\b[^.]{0,60}(graduated|retired)', '\\b17\\b[^.]{0,20}new|added[^.]{0,20}\\b17\\b']=True

```text
Of the 67 problem statements from 2023, 17 original problem statements were "graduated" [1]. In 2024, 17 new problem statements were added [2].
```

### ask: Test 3 Final Presentation Format — PASS

expected passage retrieved=True; all expected passages given to the model=True; status is answered=True; cites the expected source=True; cites every expected passage=True; answer contains ['\\b12\\b', 'slide', 'minute']=True

```text
The final group presentation requires a 12-slide presentation and has a duration of 12 minutes, followed by an 8-minute Q&A session [1].
```

### ask: Test 4 Unsupported Electricity Rate — PASS

status is insufficient=True; no citations shown=True

```text
Insufficient evidence: the retrieved passages do not answer this question. Missing: The evidence does not contain the residential electricity rate in cents per kWh charged by PG&E in 2024.
```

### chat: “what can we do?” explains capabilities — PASS

notes searched=None; refusal=False; capability words=['draft', 'brainstorm', 'plan', 'notes']

```text
I can help you brainstorm, plan, and think through ideas. I can draft and rewrite anything—emails, outlines, or summaries—and I can answer casual questions based on my general knowledge. If you want to look something up in your notes, I can do that too.

What's on your mind? We could start by drafting an email, or maybe you have a decision you're trying to work through.
```

### chat: “what can you help me with?” explains capabilities — PASS

notes searched=None; refusal=False; capability words=['draft', 'brainstorm', 'plan', 'notes']

```text
I can help you brainstorm, plan projects, draft and revise documents, answer general knowledge questions, or look up information in your notes.

If you want to jump in, feel free to give me something to write or something to think through.
```

### chat: casual drafting (no forced lookup) — PASS

notes searched=None

```text
Sure. How about this:

"Thanks so much for all your help prepping for midterms. I really appreciate all the time and insights everyone brought to the table!"
```

### chat: “make that shorter” uses the conversation — PASS

length 297->104 chars; kept items=['laundry', 'run', 'grocer', 'read']; notes searched=None/None

```text
Here’s the quicker version:

Laundry $\rightarrow$ 5k Run $\rightarrow$ Groceries $\rightarrow$ Reading.
```

### chat: conversational follow-up — PASS

missing=[]; notes searched=None; history messages=6

```text
You're going to Lisbon with your sister.
```

### separation: ask ignores chat history — PASS

two messages (rules + question)=True; no chat text in prompt=True; no persona in prompt=True; chat history unchanged=True; research rules used=True

### separation: chat-only claim is not ask evidence — PASS

ask status=insufficient; '900' in answer=False

```text
Insufficient evidence: the retrieved passages do not answer this question. Missing: The evidence does not state PG&E's 2024 R&D budget.
```

### chat: uses notes tool and cites when asked about notes — PASS

notes searched='platform screen doors' (trigger: rule); hits=4; [n] citations in reply=True

```text
Your notes detail several points about platform screen doors (PSDs) within the context of the WMATA Rail Modernization Program:

*   **Phased Implementation:** The program allows for phasing the installation of PSDs, citing examples like the Copenhagen Metro, which opened with partial installation before adding doors to all stations [1].
*   **Installation Context:** They discuss the installation alongside different station types (e.g., below-ground vs. above-ground) and the integration with sensor systems [1].
*   **Investment Options:** The modernization program presents different investment scenarios involving PSDs, with costs and benefits varying based on the scope and automation level [2].
*   **Global Standard:** PSDs are mentioned as a global standard for rail transit systems, widely adopted in many European and Asian systems [3].
*   **Foundation for Automation:** PSDs are presented as one of the "building blocks" of modernization, interfacing with the Communications-based Train Control (CBTC) system, which provides the foundation for automating operations [4].

Let me know if you want me to elaborate on any of those points or look into something else.
```

### vault: names, H1s, links, sources, index, corrections — PASS

14 notes; problems=none

### originals in raw/: unchanged and read-only — PASS

3/3 match their ingest SHA-256 and are read-only

### re-ingest: no duplicates, names kept — PASS

status=already ingested; notes 14->14; passages 180->180; model calls=0

### local only: no network use, no cloud fallback — PASS

network attempts during tests=0; outbound probe=blocked by local-mode guard; OS network=default route via en0 (network connected)
