# Test Report

- Run: 2026-09-27 00:27:20
- Machine: macOS 26.6.2, arm64, Apple M4
- Model: `mlx-community/gemma-4-e4b-it-4bit` (local, MLX) · embeddings `BAAI/bge-small-en-v1.5` (local)
- Network (OS view): no default route (offline)
- Wiki: 3 sources, 11 concepts, 14 notes, 180 passages
- Model load: 4.5s · total suite time: 100.2s
- Memory at end: MLX peak 4.91 GB, MLX active 4.2 GB, process RSS 0.36 GB, system available 2.48 GB
- Result: **13/13 passed**

| Test | Result | Time (s) | MLX peak (GB) |
|---|---|---|---|
| search: raw passages, no generation | PASS | 0.5 | 4.2 |
| ask: Q1 rail capacity | PASS | 10.97 | 4.9 |
| ask: Q2 PG&E problem statements | PASS | 8.39 | 4.9 |
| ask: Q3 course final presentation | PASS | 7.49 | 4.9 |
| ask: Q4 unsupported | PASS | 8.93 | 4.9 |
| chat: casual drafting (no forced lookup) | PASS | 7.36 | 4.9 |
| chat: conversational follow-up | PASS | 3.86 | 4.9 |
| separation: ask ignores chat history | PASS | 9.93 | 4.91 |
| chat: uses notes tool when asked about notes | PASS | 18.56 | 4.91 |
| vault: names, H1s, links, originals, index | PASS | 0.03 | 4.91 |
| originals: unchanged and read-only | PASS | 0.0 | 4.91 |
| re-ingest: no duplicates, names kept | PASS | 0.04 | 4.91 |
| local only: no network use, no cloud fallback | PASS | 0.0 | 4.91 |

## Details

### search: raw passages, no generation — PASS

hits=5; verbatim from original page=5; paths exist=5; model calls during search=0

```text
[1] vault/Originals/3A-Rail-Modernization-Program.pdf p.32 | vault/Transportation/WMATA Rail Modernization Program.md
    26 Rail Modernization Program Washington Metropolitan Area Transit Authority Federal Capital Investment Grants can help fund Modernization The CIG Core Capacity…
[2] vault/Originals/3A-Rail-Modernization-Program.pdf p.5 | vault/Transportation/WMATA Rail Modernization Program.md
    These changes support customer satisfaction, workforce stability, and the long-term sustainability of the transit network. Metro’s Capital Improvement Program s…
[3] vault/Originals/3A-Rail-Modernization-Program.pdf p.60 | vault/Transportation/WMATA Rail Modernization Program.md
    54 Rail Modernization Program Washington Metropolitan Area Transit Authority Federal grants can help fund Modernization Based on experience from peer agencies, …
[4] vault/Originals/3A-Rail-Modernization-Program.pdf p.6 | vault/Transportation/WMATA Rail Modernization Program.md
    Board Document investments, developing estimates of project costs and benefits, and identifying funding sources that can be used as a local match. We anticipate…
[5] vault/Originals/3A-Rail-Modernization-Program.pdf p.60 | vault/Transportation/WMATA Rail Modernization Program.md
    Examples: Maryland Purple Line; Silver Line Phase 1 Small Starts: A new fixed guideway system or an extension of an existing system with a total project cost <$…
```

### ask: Q1 rail capacity — PASS

status=answered; cited files=['3A-Rail-Modernization-Program.pdf']; missing patterns=[]

```text
Automation could raise practical capacity limits from 24 to 30 trains per hour or more [1]. Signal system upgrades, platform screen doors, and automation provide benefits, including the ability to increase train throughput from 24 trains per hour to 30+ trains per hour [2]. Modernization can also allow for 30 trains per hour throughput using existing tunnel infrastructure [5].
[1] WMATA Rail Modernization Program, p. 4 — Originals/3A-Rail-Modernization-Program.pdf
[2] WMATA Rail Modernization Program, p. 30 — Originals/3A-Rail-Modernization-Program.pdf
[5] WMATA Rail Modernization Program, p. 51 — Originals/3A-Rail-Modernization-Program.pdf
```

### ask: Q2 PG&E problem statements — PASS

status=answered; cited files=['pge-rd-strategy-report-executive-summary-2024.pdf']; missing patterns=[]

```text
PG&E "graduated" 17 original problem statements in its 2024 R&D strategy [1]. In 2024, PG&E added 17 new problem statements [4].
[1] PG&E 2024 R&D Strategy Report, p. 5 — Originals/pge-rd-strategy-report-executive-summary-2024.pdf
[4] PG&E 2024 R&D Strategy Report, p. 5 — Originals/pge-rd-strategy-report-executive-summary-2024.pdf
```

### ask: Q3 course final presentation — PASS

status=answered; cited files=['Business of Energy Transition Syllabus Fall 2026.pdf']; missing patterns=[]

```text
The final group presentation requires a 12-slide presentation [1]. The presentation duration is 12 minutes, followed by an 8-minute Q&A session [1].
[1] Business of Energy Transition Syllabus, p. 3 — Originals/Business of Energy Transition Syllabus Fall 2026.pdf
```

### ask: Q4 unsupported — PASS

status=insufficient; reason=model reported insufficient evidence

```text
Insufficient evidence: the retrieved passages do not answer this question. Missing: The provided evidence does not contain the residential electricity rate in cents per kWh charged by PG&E in 2024.
```

### chat: casual drafting (no forced lookup) — PASS

notes searched=None

```text
Sure. How about this:

"Thanks so much for all your help prepping for midterms. I really appreciate you all making the tough material click for me!"
```

### chat: conversational follow-up — PASS

missing=[]; notes searched=None; history messages=6

```text
You're going to Lisbon with your sister.
```

### separation: ask ignores chat history — PASS

two messages (rules + question)=True; no chat content in prompt=True; no persona in prompt=True; chat history unchanged=True; research rules used=True

### chat: uses notes tool when asked about notes — PASS

notes searched='platform screen doors'; hits=4

```text
Your notes cover the implementation, benefits, and different installation options for Platform Screen Doors (PSDs) within the WMATA Rail Modernization Program.

Here’s a quick rundown:

*   **Implementation Examples:** You can phase PSD installation, citing examples like Copenhagen's Metro or Kastrup Station retrofits [1].
*   **Installation Options & Costs:** There are various investment options regarding PSDs (e.g., only in the Downtown Core vs. at all stations), with associated costs ranging from \$0.9b to \$8.0b depending on the scope and automation level [2].
*   **Global Standard:** PSDs are noted as a global standard for many rail systems [3].
*   **Modernization Context:** PSD installation is linked to the broader modernization effort, requiring a modern signal system (like CBTC) as a foundation, and allowing for PSDs to be added at select or every station [4].

Let me know if you want me to elaborate on any of those points!
```

### vault: names, H1s, links, originals, index — PASS

14 notes; problems=none

### originals: unchanged and read-only — PASS

3/3 originals match their ingest hash and are read-only

### re-ingest: no duplicates, names kept — PASS

status=already ingested; notes 14->14; passages 180->180; model calls=0

### local only: no network use, no cloud fallback — PASS

network attempts during tests=0; outbound probe=blocked by local-mode guard; OS network=no default route (offline)
