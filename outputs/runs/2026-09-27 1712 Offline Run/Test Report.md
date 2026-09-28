# Test Report

- **Run:** 2026-09-27 17:18:55 · Offline Run
- **Machine:** macOS 26.6.2, Apple M4, 16 GB unified memory
- **Model / runtime:** `mlx-community/gemma-4-e4b-it-4bit` (Gemma 4 E4B, 4-bit MLX) via mlx-lm 0.31.3 / mlx 0.32.2; embeddings `BAAI/bge-small-en-v1.5` via sentence-transformers 6.1.0
- **Mode:** local (in-process network guard on; no online mode configured)
- **Network (OS view):** no default route (offline)
- **Wiki:** 3 sources, 11 concepts, 14 notes, 180 passages
- **Model load:** 4.6s · **suite time:** 141.7s
- **Memory at end:** MLX peak 4.95 GB, MLX active 4.2 GB, process RSS 0.47 GB, system available 3.36 GB
- **Result:** **17/17 passed**

Evidence cards: [Test 1 - Rail Capacity](<Test 1 - Rail Capacity.md>), [Test 2 - PG&E Problem Statements](<Test 2 - PG&E Problem Statements.md>), [Test 3 - Final Presentation Format](<Test 3 - Final Presentation Format.md>), [Test 4 - Unsupported Electricity Rate](<Test 4 - Unsupported Electricity Rate.md>) · [Mode Checks](<Mode Checks.md>)

| Test | Result | Time (s) | MLX peak (GB) |
|---|---|---|---|
| search: raw passages, no generation | PASS | 0.5 | 4.2 |
| ask: Test 1 Rail Capacity | PASS | 11.88 | 4.91 |
| ask: Test 2 PG&E Problem Statements | PASS | 9.52 | 4.94 |
| ask: Test 3 Final Presentation Format | PASS | 9.43 | 4.95 |
| ask: Test 4 Unsupported Electricity Rate | PASS | 9.32 | 4.95 |
| chat: “what can we do?” explains capabilities | PASS | 7.68 | 4.95 |
| chat: “what can you help me with?” explains capabilities | PASS | 6.84 | 4.95 |
| chat: casual drafting (no forced lookup) | PASS | 5.89 | 4.95 |
| chat: “make that shorter” uses the conversation | PASS | 4.47 | 4.95 |
| chat: conversational follow-up | PASS | 4.86 | 4.95 |
| separation: ask ignores chat history | PASS | 10.0 | 4.95 |
| separation: chat-only claim is not ask evidence | PASS | 7.71 | 4.95 |
| chat: uses notes tool and cites when asked about notes | PASS | 21.55 | 4.95 |
| vault: names, H1s, links, sources, index, corrections | PASS | 0.05 | 4.95 |
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

notes searched=None; refusal=False; capability words=['draft', 'brainstorm', 'plan', 'search', 'notes']

```text
I can help you brainstorm, plan things out, draft or rewrite documents, or answer general knowledge questions. If you want to dig into your notes or documents, I can search those too.

What's on your mind? We could start by outlining a project or drafting an email.
```

### chat: “what can you help me with?” explains capabilities — PASS

notes searched=None; refusal=False; capability words=['draft', 'brainstorm', 'plan', 'notes']

```text
I can help you brainstorm, plan projects, draft or rewrite documents, and answer general knowledge questions. If you want to look something up in your notes, I can do that too.

What's on your mind? We could start by outlining something or drafting an email.
```

### chat: casual drafting (no forced lookup) — PASS

notes searched=None

```text
Hey! Sure, I can do that. How about this:

"Thanks so much for all your help with the midterms prep! Your insights and support really made a difference in getting me ready."
```

### chat: “make that shorter” uses the conversation — PASS

length 134->47 chars; kept items=['laundry', 'run', 'grocer', 'read']; notes searched=None/None

```text
Laundry, 5k run, groceries, and finish reading.
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

notes searched='platform screen doors' (trigger: rule); hits=4; [n] citations in reply=True

```text
My notes detail the implementation of Platform Screen Doors (PSDs) within the context of the WMATA Rail Modernization Program.

Here’s a summary of what I found:

*   **Implementation Examples:** The program allows for phased installation, referencing examples like Copenhagen's Metro, which opened with partial PSD installation and later added doors at all stations [1]. In contrast, some stations were built with PSDs, while others used sensor systems [1]. Retrofits have replaced older sensor systems with PSDs [1].
*   **Investment Options:** The modernization program presents different investment options regarding PSDs, including scenarios with no PSDs, PSDs only in the downtown core, or PSDs at all stations, each with varying costs and benefits [2].
*   **Standard Practice:** PSDs are noted as a global standard for rail transit systems, commonly seen in many European and Asian systems [3].
*   **Modernization Foundation:** PSD installation is presented as one of several "building blocks" of modernization alongside a new signal system and operational transformation. PSDs and obstacle detection sensors interface with the CBTC system, and they can be installed at select or every station [4].

Let me know if you want to compare these options or dive into any specific aspect of the program!
```

### vault: names, H1s, links, sources, index, corrections — PASS

14 notes; problems=none

### originals in raw/: unchanged and read-only — PASS

3/3 match their ingest SHA-256 and are read-only

### re-ingest: no duplicates, names kept — PASS

status=already ingested; notes 14->14; passages 180->180; model calls=0

### local only: no network use, no cloud fallback — PASS

network attempts during tests=0; outbound probe=blocked by local-mode guard; OS network=no default route (offline)
