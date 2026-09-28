# Test Report

- **Run:** 2026-09-27 16:31:43 · Online Run
- **Machine:** macOS 26.6.2, Apple M4, 16 GB unified memory
- **Model / runtime:** `mlx-community/gemma-4-e4b-it-4bit` (Gemma 4 E4B, 4-bit MLX) via mlx-lm 0.31.3 / mlx 0.32.2; embeddings `BAAI/bge-small-en-v1.5` via sentence-transformers 6.1.0
- **Mode:** local (in-process network guard on; no online mode configured)
- **Network (OS view):** default route via en0 (network connected)
- **Wiki:** 3 sources, 11 concepts, 14 notes, 180 passages
- **Model load:** 5.9s · **suite time:** 187.2s
- **Memory at end:** MLX peak 4.91 GB, MLX active 4.2 GB, process RSS 0.34 GB, system available 3.2 GB
- **Result:** **17/17 passed**

Evidence cards: [Test 1 - Rail Capacity](<Test 1 - Rail Capacity.md>), [Test 2 - PG&E Problem Statements](<Test 2 - PG&E Problem Statements.md>), [Test 3 - Final Presentation Format](<Test 3 - Final Presentation Format.md>), [Test 4 - Unsupported Electricity Rate](<Test 4 - Unsupported Electricity Rate.md>) · [Mode Checks](<Mode Checks.md>)

| Test | Result | Time (s) | MLX peak (GB) |
|---|---|---|---|
| search: raw passages, no generation | PASS | 0.64 | 4.2 |
| ask: Test 1 Rail Capacity | PASS | 14.73 | 4.9 |
| ask: Test 2 PG&E Problem Statements | PASS | 13.42 | 4.9 |
| ask: Test 3 Final Presentation Format | PASS | 10.53 | 4.9 |
| ask: Test 4 Unsupported Electricity Rate | PASS | 9.08 | 4.9 |
| chat: “what can we do?” explains capabilities | PASS | 8.81 | 4.9 |
| chat: “what can you help me with?” explains capabilities | PASS | 8.71 | 4.9 |
| chat: casual drafting (no forced lookup) | PASS | 6.66 | 4.9 |
| chat: “make that shorter” uses the conversation | PASS | 5.13 | 4.9 |
| chat: conversational follow-up | PASS | 9.38 | 4.91 |
| separation: ask ignores chat history | PASS | 15.6 | 4.91 |
| separation: chat-only claim is not ask evidence | PASS | 10.86 | 4.91 |
| chat: uses notes tool and cites when asked about notes | PASS | 25.43 | 4.91 |
| vault: names, H1s, links, sources, index, corrections | PASS | 0.04 | 4.91 |
| originals in raw/: unchanged and read-only | PASS | 0.0 | 4.91 |
| re-ingest: no duplicates, names kept | PASS | 0.07 | 4.91 |
| local only: no network use, no cloud fallback | PASS | 0.0 | 4.91 |

## Details

### search: raw passages, no generation — PASS

hits=5; verbatim from original page=5; paths exist=5; model calls during search=0

### ask: Test 1 Rail Capacity — PASS

expected passage retrieved=True; status is answered=True; cites the expected source=True; cites the expected passage=True; answer contains ['\\b24\\b', '\\b30\\b']=True

```text
Automation could raise practical capacity limits from 24 to 30 trains per hour or more [1]. Signal system upgrades, platform screen doors, and automation provide benefits, including the ability to increase train throughput from 24 trains per hour to 30+ trains per hour [2]. Modernization can also allow for 30 trains per hour throughput using existing tunnel infrastructure [5].
```

### ask: Test 2 PG&E Problem Statements — PASS

expected passage retrieved=True; status is answered=True; cites the expected source=True; cites the expected passage=True; answer contains ['\\b17\\b']=True

```text
Of the 67 problem statements identified in 2023, 17 original problem statements were "graduated" [1]. Additionally, two new focus areas were added to the 2024 strategy report [1].
```

### ask: Test 3 Final Presentation Format — PASS

expected passage retrieved=True; status is answered=True; cites the expected source=True; cites the expected passage=True; answer contains ['\\b12\\b', 'slide', 'minute']=True

```text
The final group presentation requires a 12-slide presentation [1]. The presentation duration is 12 minutes, followed by an 8-minute Q&A session [1].
```

### ask: Test 4 Unsupported Electricity Rate — PASS

status is insufficient=True; no citations shown=True

```text
Insufficient evidence: the retrieved passages do not answer this question. Missing: The provided evidence does not contain the residential electricity rate in cents per kWh charged by PG&E in 2024.
```

### chat: “what can we do?” explains capabilities — PASS

notes searched=None; refusal=False; capability words=['draft', 'brainstorm', 'plan']

```text
I can help you brainstorm, plan, and think through ideas; draft and rewrite anything from emails to outlines; answer general knowledge questions; or look up specific details in your personal documents.

If you want to jump in, tell me what you're working on, and we can go from there.
```

### chat: “what can you help me with?” explains capabilities — PASS

notes searched=None; refusal=False; capability words=['draft', 'brainstorm', 'notes', 'ask', 'wiki']

```text
I can brainstorm, draft, and revise text for you, answer general knowledge questions, or look up specific information in your personal documents using the `wiki` tool.

If you want to try something concrete, you could ask me to draft an email or compare notes from your documents.
```

### chat: casual drafting (no forced lookup) — PASS

notes searched=None

```text
Sure. How about this:

"Thanks so much for helping me prep for midterms. Your insights and group sessions really helped solidify the material, and I appreciate you all taking the time with me!"
```

### chat: “make that shorter” uses the conversation — PASS

length 198->46 chars; kept items=['laundry', 'run', 'grocer', 'read']; notes searched=None/None

```text
Laundry, 5k run, groceries, and class reading.
```

### chat: conversational follow-up — PASS

missing=[]; notes searched=None; history messages=6

```text
You're going to Lisbon, and you're going with your sister.
```

### separation: ask ignores chat history — PASS

two messages (rules + question)=True; no chat text in prompt=True; no persona in prompt=True; chat history unchanged=True; research rules used=True

### separation: chat-only claim is not ask evidence — PASS

ask status=insufficient; '900' in answer=False

```text
Insufficient evidence: the retrieved passages do not answer this question. Missing: The evidence does not state PG&E's 2024 R&D budget.
```

### chat: uses notes tool and cites when asked about notes — PASS

notes searched='platform screen doors'; hits=4; [n] citations in reply=True

```text
Your notes detail several things about Platform Screen Doors (PSDs) regarding the WMATA Rail Modernization Program:

*   **Implementation & Installation:** PSD implementation can be phased, similar to Copenhagen's Metro, which initially used partial installation and later added doors at all stations [1]. Some stations were built with PSDs, while others used sensor systems [1]. Retrofits have replaced sensor systems with PSDs at above-ground stations [1].
*   **Investment Options:** The program allows for incremental investment options regarding PSDs, with costs varying based on the scope and desired automation level [2].
*   **Global Standard:** PSDs are noted as a global standard for rail transit systems, widely adopted in many European and Asian systems [3].
*   **Building Blocks:** PSDs are presented as one of the building blocks of modernization, integrated with the CBTC system, and can be installed at select stations or every station [4].

Let me know if you want me to elaborate on any of those points or compare them to another topic!
```

### vault: names, H1s, links, sources, index, corrections — PASS

14 notes; problems=none

### originals in raw/: unchanged and read-only — PASS

3/3 match their ingest SHA-256 and are read-only

### re-ingest: no duplicates, names kept — PASS

status=already ingested; notes 14->14; passages 180->180; model calls=0

### local only: no network use, no cloud fallback — PASS

network attempts during tests=0; outbound probe=blocked by local-mode guard; OS network=default route via en0 (network connected)
