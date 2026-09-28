# Test Report

- Run: 2026-09-26 23:14:04
- Machine: macOS 26.6.2, arm64, Apple M4
- Model: `mlx-community/gemma-4-e4b-it-4bit` (local, MLX) · embeddings `BAAI/bge-small-en-v1.5` (local)
- Network (OS view): default route via en0 (network connected)
- Wiki: 2 sources, 7 concepts, 9 notes, 141 passages
- Model load: 6.0s · total suite time: 73.6s
- Memory at end: MLX peak 4.88 GB, MLX active 4.2 GB, process RSS 0.2 GB, system available 2.67 GB
- Result: **8/12 passed**

| Test | Result | Time (s) | MLX peak (GB) |
|---|---|---|---|
| search: raw passages, no generation | PASS | 0.73 | 4.2 |
| ask: Q1 rail capacity | PASS | 16.35 | 4.86 |
| ask: Q2 PG&E problem statements | PASS | 16.43 | 4.86 |
| ask: Q3 course final presentation | FAIL | 16.33 | 4.88 |
| ask: Q4 unsupported | PASS | 12.12 | 4.88 |
| chat_casual | FAIL | 0.0 | 4.88 |
| chat_followup_and_separation | FAIL | 0.0 | 4.88 |
| chat_notes_tool | FAIL | 0.0 | 4.88 |
| vault: names, H1s, links, originals, index | PASS | 0.04 | 4.88 |
| originals: unchanged and read-only | PASS | 0.0 | 4.88 |
| re-ingest: no duplicates, names kept | PASS | 0.05 | 4.88 |
| local only: no network use, no cloud fallback | PASS | 0.0 | 4.88 |

## Details

### search: raw passages, no generation — PASS

hits=5; verbatim from original page=5; paths exist=5; model calls during search=0

```text
[1] vault/Originals/3A-Rail-Modernization-Program.pdf p.32 | vault/Transportation/Rail Modernization Program Strategy.md
    26 Rail Modernization Program Washington Metropolitan Area Transit Authority Federal Capital Investment Grants can help fund Modernization The CIG Core Capacity…
[2] vault/Originals/3A-Rail-Modernization-Program.pdf p.5 | vault/Transportation/Rail Modernization Program Strategy.md
    These changes support customer satisfaction, workforce stability, and the long-term sustainability of the transit network. Metro’s Capital Improvement Program s…
[3] vault/Originals/3A-Rail-Modernization-Program.pdf p.60 | vault/Transportation/Rail Modernization Program Strategy.md
    54 Rail Modernization Program Washington Metropolitan Area Transit Authority Federal grants can help fund Modernization Based on experience from peer agencies, …
[4] vault/Originals/3A-Rail-Modernization-Program.pdf p.6 | vault/Transportation/Rail Modernization Program Strategy.md
    Board Document investments, developing estimates of project costs and benefits, and identifying funding sources that can be used as a local match. We anticipate…
[5] vault/Originals/3A-Rail-Modernization-Program.pdf p.60 | vault/Transportation/Rail Modernization Program Strategy.md
    Examples: Maryland Purple Line; Silver Line Phase 1 Small Starts: A new fixed guideway system or an extension of an existing system with a total project cost <$…
```

### ask: Q1 rail capacity — PASS

status=answered; cited files=['3A-Rail-Modernization-Program.pdf']; missing patterns=[]

```text
Automation could raise practical capacity limits from 24 to 30 trains per hour or more [1]. Specifically, modernization can increase train throughput from 24 trains per hour to 30+ trains per hour [2].
[1] Rail Modernization Program Strategy, p. 4 — Originals/3A-Rail-Modernization-Program.pdf
[2] Rail Modernization Program Strategy, p. 30 — Originals/3A-Rail-Modernization-Program.pdf
```

### ask: Q2 PG&E problem statements — PASS

status=answered; cited files=['pge-rd-strategy-report-executive-summary-2024.pdf']; missing patterns=[]

```text
PG&E "graduated" 17 original problem statements in its 2024 R&D strategy [1]. In 2024, PG&E added 17 new problem statements [4].
[1] PG&E 2024 R&D Strategy Report, p. 5 — Originals/pge-rd-strategy-report-executive-summary-2024.pdf
[4] PG&E 2024 R&D Strategy Report, p. 5 — Originals/pge-rd-strategy-report-executive-summary-2024.pdf
```

### ask: Q3 course final presentation — FAIL

status=insufficient; cited files=[]; missing patterns=['\\b12\\b', 'minute']

```text
Insufficient evidence: the retrieved passages do not answer this question. Missing: The provided evidence does not contain information about the "Business of Energy Transition" course, its final group presentation requirements, slide count, or time limit.
```

### ask: Q4 unsupported — PASS

status=insufficient; reason=model reported insufficient evidence

```text
Insufficient evidence: the retrieved passages do not answer this question. Missing: The evidence does not state the residential electricity rate in cents per kWh that PG&E charges in 2024.
```

### chat_casual — FAIL

crashed: TypeError: ChatTurn.__init__() missing 1 required positional argument: 'reply'

### chat_followup_and_separation — FAIL

crashed: TypeError: ChatTurn.__init__() missing 1 required positional argument: 'reply'

### chat_notes_tool — FAIL

crashed: TypeError: ChatTurn.__init__() missing 1 required positional argument: 'reply'

### vault: names, H1s, links, originals, index — PASS

9 notes; problems=none

### originals: unchanged and read-only — PASS

2/2 originals match their ingest hash and are read-only

### re-ingest: no duplicates, names kept — PASS

status=already ingested; notes 9->9; passages 141->141; model calls=0

### local only: no network use, no cloud fallback — PASS

network attempts during tests=0; outbound probe=blocked by local-mode guard; OS network=default route via en0 (network connected)
