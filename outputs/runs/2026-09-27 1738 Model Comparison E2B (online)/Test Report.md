# Test Report

- **Run:** 2026-09-27 17:39:31 · Online Run
- **Machine:** macOS 26.6.2, Apple M4, 16 GB unified memory
- **Model / runtime:** `mlx-community/gemma-4-e2b-it-4bit` (Gemma 4 E2B, 4-bit MLX) via mlx-lm 0.31.3 / mlx 0.32.2; embeddings `BAAI/bge-small-en-v1.5` via sentence-transformers 6.1.0
- **Mode:** local (in-process network guard on; no online mode configured)
- **Network (OS view):** default route via en0 (network connected)
- **Wiki:** 3 sources, 11 concepts, 14 notes, 180 passages
- **Model load:** 5.6s · **suite time:** 68.6s
- **Memory at end:** MLX peak 3.34 GB, MLX active 2.6 GB, process RSS 0.4 GB, system available 3.27 GB
- **Result:** **15/17 passed**

Evidence cards: [Test 1 - Rail Capacity](<Test 1 - Rail Capacity.md>), [Test 2 - PG&E Problem Statements](<Test 2 - PG&E Problem Statements.md>), [Test 3 - Final Presentation Format](<Test 3 - Final Presentation Format.md>), [Test 4 - Unsupported Electricity Rate](<Test 4 - Unsupported Electricity Rate.md>) · [Mode Checks](<Mode Checks.md>)

| Test | Result | Time (s) | MLX peak (GB) |
|---|---|---|---|
| search: raw passages, no generation | PASS | 0.79 | 2.6 |
| ask: Test 1 Rail Capacity | PASS | 5.26 | 3.33 |
| ask: Test 2 PG&E Problem Statements | FAIL | 4.13 | 3.33 |
| ask: Test 3 Final Presentation Format | PASS | 4.09 | 3.33 |
| ask: Test 4 Unsupported Electricity Rate | PASS | 4.03 | 3.33 |
| chat: “what can we do?” explains capabilities | PASS | 3.34 | 3.33 |
| chat: “what can you help me with?” explains capabilities | PASS | 3.04 | 3.33 |
| chat: casual drafting (no forced lookup) | PASS | 2.86 | 3.33 |
| chat: “make that shorter” uses the conversation | PASS | 2.4 | 3.33 |
| chat: conversational follow-up | PASS | 1.86 | 3.33 |
| separation: ask ignores chat history | PASS | 2.93 | 3.33 |
| separation: chat-only claim is not ask evidence | PASS | 3.29 | 3.33 |
| chat: uses notes tool and cites when asked about notes | FAIL | 4.08 | 3.34 |
| vault: names, H1s, links, sources, index, corrections | PASS | 0.06 | 3.34 |
| originals in raw/: unchanged and read-only | PASS | 0.0 | 3.34 |
| re-ingest: no duplicates, names kept | PASS | 0.08 | 3.34 |
| local only: no network use, no cloud fallback | PASS | 0.0 | 3.34 |

## Details

### search: raw passages, no generation — PASS

hits=5; verbatim from original page=5; paths exist=5; model calls during search=0

### ask: Test 1 Rail Capacity — PASS

expected passage retrieved=True; all expected passages given to the model=True; status is answered=True; cites the expected source=True; cites every expected passage=True; answer contains ['\\b24\\b', '\\b30\\b']=True

```text
Automation can raise practical capacity limits from 24 to 30 trains per hour or more [1], [3].
```

### ask: Test 2 PG&E Problem Statements — FAIL

expected passage retrieved=True; all expected passages given to the model=True; status is answered=False; cites the expected source=False; cites every expected passage=False; answer contains ['(graduated|retired)[^.]{0,40}\\b17\\b|\\b17\\b[^.]{0,60}(graduated|retired)', '\\b17\\b[^.]{0,20}new|added[^.]{0,20}\\b17\\b']=False

```text
Insufficient evidence: the model's draft answer cited no passages, so it was withheld.
```

### ask: Test 3 Final Presentation Format — PASS

expected passage retrieved=True; all expected passages given to the model=True; status is answered=True; cites the expected source=True; cites every expected passage=True; answer contains ['\\b12\\b', 'slide', 'minute']=True

```text
The final group presentation is a 12-slide presentation and is allotted 12 minutes for the presentation, followed by an 8-minute Q&A session with the committee [1].
```

### ask: Test 4 Unsupported Electricity Rate — PASS

status is insufficient=True; no citations shown=True

```text
Insufficient evidence: the retrieved passages do not answer this question. Missing: The provided passages do not state the residential electricity rate in cents per kWh charged by PG&E in 2024.
```

### chat: “what can we do?” explains capabilities — PASS

notes searched=None; refusal=False; capability words=['draft', 'brainstorm', 'plan', 'wiki']

```text
I can brainstorm, plan, and think through ideas, draft and rewrite things like emails or summaries, answer general knowledge questions, or look things up in your personal wiki.

We could start by brainstorming a project or drafting an email. What's on your mind?
```

### chat: “what can you help me with?” explains capabilities — PASS

notes searched=None; refusal=False; capability words=['draft', 'brainstorm', 'plan', 'wiki']

```text
I can help you brainstorm, plan things out, draft or rewrite text, answer general knowledge questions, or look things up in your personal wiki.

How about we start with a draft? Tell me what you're working on.
```

### chat: casual drafting (no forced lookup) — PASS

notes searched=None

```text
Hey. I can definitely whip that up. How about something like this?

"Seriously, thanks to all of you for the intense prep sessions. I feel way more confident walking into these midterms now!"
```

### chat: “make that shorter” uses the conversation — PASS

length 459->53 chars; kept items=['laundry', 'run', 'grocer', 'read']; notes searched=None/None

```text
Laundry, 5k run, groceries, reading. That's the core.
```

### chat: conversational follow-up — PASS

missing=[]; notes searched=None; history messages=6

```text
You mentioned you and your sister are taking a train trip to Lisbon.
```

### separation: ask ignores chat history — PASS

two messages (rules + question)=True; no chat text in prompt=True; no persona in prompt=True; chat history unchanged=True; research rules used=True

### separation: chat-only claim is not ask evidence — PASS

ask status=insufficient; '900' in answer=False

```text
Insufficient evidence: the retrieved passages do not answer this question. Missing: The evidence does not state PG&E's 2024 R&D budget.
```

### chat: uses notes tool and cites when asked about notes — FAIL

notes searched='platform screen doors' (trigger: rule); hits=4; [n] citations in reply=False

```text
Platform screen doors are a topic covered in the WMATA Rail Modernization Program. Some systems, like Copenhagen's, have used them, while others have used sensor systems instead. The program discusses the potential for installing PSDs at select stations or every station, depending on the level of automation desired.
```

### vault: names, H1s, links, sources, index, corrections — PASS

14 notes; problems=none

### originals in raw/: unchanged and read-only — PASS

3/3 match their ingest SHA-256 and are read-only

### re-ingest: no duplicates, names kept — PASS

status=already ingested; notes 14->14; passages 180->180; model calls=0

### local only: no network use, no cloud fallback — PASS

network attempts during tests=0; outbound probe=blocked by local-mode guard; OS network=default route via en0 (network connected)
