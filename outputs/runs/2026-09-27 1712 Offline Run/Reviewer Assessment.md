# Reviewer Assessment — 2026-09-27 1712 Offline Run

Written **after** the run, by comparing each evidence card with the original PDF page
it cites. The cards themselves are unchanged. Model: `mlx-community/gemma-4-e4b-it-4bit`,
local mode, offline. Retrieval is inspected first, then the answer.

## Test 1 — Rail Capacity (direct question, one source)

- **Retrieval:** the expected passage (rail plan p. 4, "raise practical capacity limits
  from 24 to 30 trains per hour or more") was retrieved at rank 1. ✅
- **Answer:** "…from 24 to 30 trains per hour or more [1]… from 24 trains per hour to
  30+ trains per hour [3]… 30 trains per hour throughput using existing tunnel
  infrastructure [7]."
- **Citations:**
  - [1] p. 4 states the claim verbatim. ✅
  - [3] p. 30: "Increase train throughput from 24 trains per hour to 30+ trains per
    hour". ✅
  - [7] p. 51: "New technology increases throughput… efficiently uses Metro's existing
    tunnel infrastructure… 30 trains per hour". ✅
- **Assessment: correct and fully supported.** The answer is a little repetitive
  (three sentences, one fact), but nothing is invented.

## Test 2 — PG&E Problem Statements (paraphrased wording)

- **Retrieval:** the question says "retired as solved" and "fresh ones joined". The
  source says "graduated" and "added… new". p. 5 (first half) was retrieved at rank 1,
  and its second half was added as same-page context. ✅
- **Answer:** "Of the 67 problem statements from 2023, 17 original problem statements
  were 'graduated' [1]. In 2024, 17 new problem statements were added [2]."
- **Citations:**
  - [1] p. 5: "In 2023, we identified 67 problem statements… we have 'graduated' 17
    original problem statements." ✅
  - [2] p. 5: "In 2024, we added 17 new problem statements." ✅
- **Assessment: correct and fully supported.** Earlier failure, kept as evidence:
  before same-page expansion (run 2026-09-27 1631), the second half of p. 5 was not
  retrieved. The answer then said "two new focus areas", which a weak automated check
  passed.

## Test 3 — Final Presentation Format (source ingested offline)

- **Retrieval:** syllabus p. 3 ("Format: A 12-slide presentation") at rank 1. ✅
- **Answer:** "…a 12-slide presentation and has a duration of 12 minutes, followed by an
  8-minute Q&A session [1]."
- **Citation:** [1] p. 3: "Format: A 12-slide presentation. Duration: 12 minutes for the
  presentation, followed by an 8-minute Q&A session". ✅
- **Assessment: correct and fully supported.**

## Test 4 — Unsupported Electricity Rate (expected: insufficient evidence)

- **Retrieval:** six PG&E passages about bills, affordability and AI. None states a rate.
  That's the correct behavior: the closest material, not a false match.
- **Answer:** "Insufficient evidence: the retrieved passages do not answer this question.
  Missing: The evidence does not contain the residential electricity rate in cents per
  kWh charged by PG&E in 2024."
- **Assessment: correct refusal.** No number was invented and no citation was shown.

## Mode checks (see `Mode Checks.md`)

All passed:
- the capability questions (no search, no refusal)
- casual drafting (no lookup)
- "make that shorter" (134 → 47 characters, items kept)
- the follow-up (remembered "Lisbon" and "sister")
- ask/chat separation (rules + question only)
- the chat-only claim ("$900 million R&D budget"), refused by ask
- the notes tool with `[n]` citations
- raw search (verbatim passages, 0 model calls)

One weakness in the separate piped chat demo in `Terminal Log.txt` (step 7):
"make that shorter" produced a tightened version of the first draft option that is
only modestly shorter.
