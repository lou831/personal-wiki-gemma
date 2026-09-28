# Test Report

- **Run:** 2026-09-27 16:36:02 · Online Run
- **Machine:** macOS 26.6.2, Apple M4, 16 GB unified memory
- **Model / runtime:** `mlx-community/gemma-4-e4b-it-4bit` (Gemma 4 E4B, 4-bit MLX) via mlx-lm 0.31.3 / mlx 0.32.2; embeddings `BAAI/bge-small-en-v1.5` via sentence-transformers 6.1.0
- **Mode:** local (in-process network guard on; no online mode configured)
- **Network (OS view):** default route via en0 (network connected)
- **Wiki:** 3 sources, 11 concepts, 14 notes, 180 passages
- **Model load:** 5.2s · **suite time:** 164.7s
- **Memory at end:** MLX peak 4.95 GB, MLX active 4.2 GB, process RSS 0.43 GB, system available 3.02 GB
- **Result:** **16/17 passed**

Evidence cards: [Test 1 - Rail Capacity](<Test 1 - Rail Capacity.md>), [Test 2 - PG&E Problem Statements](<Test 2 - PG&E Problem Statements.md>), [Test 3 - Final Presentation Format](<Test 3 - Final Presentation Format.md>), [Test 4 - Unsupported Electricity Rate](<Test 4 - Unsupported Electricity Rate.md>) · [Mode Checks](<Mode Checks.md>)

| Test | Result | Time (s) | MLX peak (GB) |
|---|---|---|---|
| search: raw passages, no generation | PASS | 0.72 | 4.2 |
| ask: Test 1 Rail Capacity | PASS | 15.49 | 4.91 |
| ask: Test 2 PG&E Problem Statements | PASS | 11.64 | 4.94 |
| ask: Test 3 Final Presentation Format | PASS | 11.7 | 4.95 |
| ask: Test 4 Unsupported Electricity Rate | PASS | 11.12 | 4.95 |
| chat: “what can we do?” explains capabilities | PASS | 8.0 | 4.95 |
| chat: “what can you help me with?” explains capabilities | PASS | 8.88 | 4.95 |
| chat: casual drafting (no forced lookup) | PASS | 7.28 | 4.95 |
| chat: “make that shorter” uses the conversation | PASS | 5.36 | 4.95 |
| chat: conversational follow-up | PASS | 4.74 | 4.95 |
| separation: ask ignores chat history | PASS | 11.2 | 4.95 |
| separation: chat-only claim is not ask evidence | PASS | 9.32 | 4.95 |
| chat: uses notes tool and cites when asked about notes | FAIL | 21.94 | 4.95 |
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

notes searched=None; refusal=False; capability words=['draft', 'brainstorm', 'notes', 'wiki']

```text
I can help you brainstorm, draft and revise documents, answer general knowledge questions, or look things up in your personal wiki if you have a specific question about your documents.

Want to try having me draft an email, or maybe you want to see what your notes say about the "Business of Energy Transition"?
```

### chat: “what can you help me with?” explains capabilities — PASS

notes searched=None; refusal=False; capability words=['draft', 'brainstorm', 'plan', 'search', 'notes', 'ask', 'wiki']

```text
I can help you brainstorm, plan things out, draft or rewrite documents, and answer general knowledge questions. If you want to look up specific details from your saved notes, I can use the `wiki search` or `wiki ask` commands.

What's on your mind? We could start by drafting an email or planning out a project.
```

### chat: casual drafting (no forced lookup) — PASS

notes searched=None

```text
Hey! Sure thing. How about this:

"Thanks so much for all your help prepping for midterms; I honestly couldn't have done it without you guys. Really appreciate all the time and brains you brought to the table!"
```

### chat: “make that shorter” uses the conversation — PASS

length 304->75 chars; kept items=['laundry', 'run', 'grocer', 'read']; notes searched=None/None

```text
Laundry $\rightarrow$ 5k run $\rightarrow$ Groceries $\rightarrow$ Reading.
```

### chat: conversational follow-up — PASS

missing=[]; notes searched=None; history messages=6

```text
You and your sister are going to Lisbon.
```

### separation: ask ignores chat history — PASS

two messages (rules + question)=True; no chat text in prompt=True; no persona in prompt=True; chat history unchanged=True; research rules used=True

### separation: chat-only claim is not ask evidence — PASS

ask status=insufficient; '900' in answer=False

```text
Insufficient evidence: the retrieved passages do not answer this question. Missing: The evidence does not state PG&E's 2024 R&D budget.
```

### chat: uses notes tool and cites when asked about notes — FAIL

notes searched=None; hits=0; [n] citations in reply=False

```text
<|channel>thought
Thinking Process:

1.  **Analyze the Request:** The user is asking what their notes say about "platform screen doors."
2.  **Identify the Goal:** I need to check the user's personal wiki/notes for information on this topic.
3.  **Determine the Tool:** The `Notes Tool` is appropriate for this factual lookup.
4.  **Formulate the Search Query:** The query should be specific: "platform screen doors."
5.  **Execute the Action (Internal Monologue/Tool Call):** I must use the exact format: `<<search: short search query>>`.
6.  **Check Document Relevance (Pre-check):** The documents are:
    *   WMATA Rail Modernization Program
    *   PG&E 2024 R&D Strategy Report
    *   Business of Energy Transition Syllabus
    *   "Platform screen doors" sounds highly relevant to the "WMATA Rail Modernization Program."
7.  **Generate the Response:** Since I need to search first, I must initiate the search action.

*(Self-Correction/Refinement):* I must use the precise command format.

**Final Output Generation:** Call the search tool.<channel|><<search: platform screen doors>>
```

### vault: names, H1s, links, sources, index, corrections — PASS

14 notes; problems=none

### originals in raw/: unchanged and read-only — PASS

3/3 match their ingest SHA-256 and are read-only

### re-ingest: no duplicates, names kept — PASS

status=already ingested; notes 14->14; passages 180->180; model calls=0

### local only: no network use, no cloud fallback — PASS

network attempts during tests=0; outbound probe=blocked by local-mode guard; OS network=default route via en0 (network connected)
