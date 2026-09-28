# Test 2 — PG&E Problem Statements

- **Mode:** ask · **execution:** local (offline guard on) · **OS network:** no default route (offline)
- **Model / runtime:** `mlx-community/gemma-4-e4b-it-4bit` (Gemma 4 E4B, 4-bit MLX) via mlx-lm 0.31.3 / mlx 0.32.2; embeddings `BAAI/bge-small-en-v1.5` via sentence-transformers 6.1.0
- **Run:** 2026-09-27 17:17:04 · retrieval 0.03s · generation 9.5s · 1753 prompt tokens · 47 output tokens · 18.8 tok/s · MLX peak 4.94 GB
- **Kind:** paraphrased question (wording differs from the source)

## Question

> How many of PG&E's research challenges from last year were retired as solved, and how many fresh ones joined the list?

## Expected (written before the run)

Retrieves p. 5 despite 'retired as solved' vs 'graduated'; answers 17 graduated AND 17 new problem statements.

- Source: `vault/raw/pge-rd-strategy-report-executive-summary-2024.pdf`, p. 5
- Passage must contain: “we have “graduated” 17 original problem statements”
- Passage must contain: “we added 17 new problem statements”

## Retrieved passages (inspected before the answer)

Numbered as shown to the model; `[n]` in the answer refers to these numbers.

Expected passage retrieved at rank: **1**

**[1] PG&E 2024 R&D Strategy Report, p. 5** — retrieval rank 1; cosine 0.69, bm25 14.4
note `vault/wiki/Energy and Utilities/PG&E 2024 R&D Strategy Report.md` · original `vault/raw/pge-rd-strategy-report-executive-summary-2024.pdf` p. 5

> 2024 R&D strategy: What has changed since 2023? Building on the foundation of our 2023 R&D Strategy Report, PG&E has made significant strides in addressing the key challenges laid out last year. In 2023, we identified 67 problem statements, which highlighted the most critical barriers to achieving our long-term energy system goals. Through a combination of innovation, collaboration, and strategic investments, we are now on a clear path to addressing many of these challenges and have signaled that PG&E feels optimistic about our existing partnerships for resolving several problem statements. In other cases, original problem statements evolved so substantially that we replaced them with problem statements that are considered new to the 2024 report. In total, we have “graduated” 17 original problem statements. However, new challenges continue to emerge as the energy landscape evolves. Readers of our 2023 R&D Strategy Report will also observe that we have added two new focus areas to this year’s strategy report: “Net Zero Energy System & Environmental Stewardship” and “Climate Resilience.” These additions highlight our commitment to decarbonization and our recognition of the urgent need to prepare for the impacts of climate change.

**[2] PG&E 2024 R&D Strategy Report, p. 5** — retrieval rank 1; same-page neighbor of rank 1, added as context
note `vault/wiki/Energy and Utilities/PG&E 2024 R&D Strategy Report.md` · original `vault/raw/pge-rd-strategy-report-executive-summary-2024.pdf` p. 5

> Readers of our 2023 R&D Strategy Report will also observe that we have added two new focus areas to this year’s strategy report: “Net Zero Energy System & Environmental Stewardship” and “Climate Resilience.” These additions highlight our commitment to decarbonization and our recognition of the urgent need to prepare for the impacts of climate change. In 2024, we added 17 new problem statements that reflect new priority challenges, such as the growing need for climate adaptation and the elimination of residual carbon emissions. 2024 R&D STRATEGY REPORT—EXECUTIVE SUMMARY PAGE 5

**[3] PG&E 2024 R&D Strategy Report, p. 2** — retrieval rank 2; cosine 0.60, bm25 12.0
note `vault/wiki/Energy and Utilities/PG&E 2024 R&D Strategy Report.md` · original `vault/raw/pge-rd-strategy-report-executive-summary-2024.pdf` p. 2

> Our 2024 R&D Strategy: Leveraging the power of AI to achieve our True North Strategy Last year marked a bold shift in PG&E’s approach to Research and Development (R&D) and innovation. With the launch of PG&E’s inaugural R&D Strategy Report, we shared our biggest innovation challenges and invited problem solvers from all corners of the world to join us in building the energy system of the future, together. This brighter future is described by our True North Strategy (TNS), PG&E’s 10-year enterprise transformation roadmap that guides us towards a future where we play a pivotal role in California’s transition to a net zero emissions, climate-resilient future. In 2024, PG&E’s Research and Development strategy builds on the progress made in 2023 with an ambitious vision to leverage the transformative powers of Artificial Intelligence (AI) to accelerate our progress towards achieving our True North Strategy.

**[4] PG&E 2024 R&D Strategy Report, p. 2** — retrieval rank 3; cosine 0.60, bm25 7.0
note `vault/wiki/Energy and Utilities/PG&E 2024 R&D Strategy Report.md` · original `vault/raw/pge-rd-strategy-report-executive-summary-2024.pdf` p. 2

> In 2024, PG&E’s Research and Development strategy builds on the progress made in 2023 with an ambitious vision to leverage the transformative powers of Artificial Intelligence (AI) to accelerate our progress towards achieving our True North Strategy. This vision embodies our commitment to developing an intelligent and resilient energy system capable of dynamically responding to the evolving needs of both customers and the energy system. This year, we explore how integrating AI across our operations can help us tackle some of the most complex challenges faced by PG&E in building a net zero and climate-resilient future. AI offers transformative potential to drive automation, enhance predictive capabilities, and deliver personalized customer experiences. By embracing AI responsibly, we aim to accelerate our goal to provide clean and resilient energy for all. 2024 R&D STRATEGY REPORT—EXECUTIVE SUMMARY PAGE 2

**[5] PG&E 2024 R&D Strategy Report, p. 3** — retrieval rank 4; cosine 0.63, bm25 2.9
note `vault/wiki/Energy and Utilities/PG&E 2024 R&D Strategy Report.md` · original `vault/raw/pge-rd-strategy-report-executive-summary-2024.pdf` p. 3

> Our R&D strategy remains problem-focused, and the 67 problem statements identified in this report represent the critical obstacles to achieving our TNS. From managing unprecedented load growth to navigating risk across our energy system, these problem statements serve as the roadmap for our innovation efforts. Innovation at PG&E is not about technology for technology’s sake; instead, it is about using the right tools, including but not limited to AI, to address these challenges in the most effective and cost-efficient way possible to deliver for our customers, our communities, and the planet. AI can play a pivotal role in addressing the challenges that we must address to create a future-proofed PG&E capable of delivering on our responsibilities to our customers today, meeting their needs of tomorrow, and adapting to the continually evolving challenges beyond. It will enable us to anticipate operational risks and optimize energy delivery, helping us move from reactive to predictive operations.

**[6] PG&E 2024 R&D Strategy Report, p. 17** — retrieval rank 5; cosine 0.56, bm25 4.5
note `vault/wiki/Energy and Utilities/PG&E 2024 R&D Strategy Report.md` · original `vault/raw/pge-rd-strategy-report-executive-summary-2024.pdf` p. 17

> THEME 2 Operating a clean fuels system As part of our commitment to decarbonization, PG&E is exploring the integration of clean fuels like hydrogen and the increasing integration of RNG into our gas system. While clean fuels are expected to play a major role in future energy systems, there are still uncertainties about how they will interact with existing infrastructure. PG&E is investing in foundational research to understand the impacts of clean fuels on pipelines, system components, and end-user applications. This research will help identify solutions for safety risks, such as hydrogen leaks and pipeline embrittlement, and guide the transition to a cleaner, more sustainable gas system that aligns with PG&E’s True North Strategy and California’s decarbonization goals. 2024 R&D STRATEGY REPORT—EXECUTIVE SUMMARY PAGE 17

**[7] PG&E 2024 R&D Strategy Report, p. 6** — retrieval rank 6; cosine 0.61, bm25 1.7
note `vault/wiki/Energy and Utilities/PG&E 2024 R&D Strategy Report.md` · original `vault/raw/pge-rd-strategy-report-executive-summary-2024.pdf` p. 6

> Just as in 2023, PG&E remains committed to a multi-faceted approach that leverages diverse technologies and partnerships to overcome obstacles and deliver on our True North Strategy. This problem-focused approach ensures that we prioritize solutions that address the most urgent and important issues across the utility. Across these business areas, the responsible use of AI will help us supercharge progress, driving the transformation of PG&E towards a decarbonized, resilient future to deliver for our hometowns and help heal the planet. BUSINESS AREA SECTIONS Electric Vehicles Integrated Grid Planning & Transmission Strategy Supply and Load Management Undergrounding Wildfire Gas System Gas Systemwide Areas of Impact Climate Resilience Net Zero Energy System & Environmental Stewardship Electric In the following sections, we will explore how AI, alongside other innovative technologies, may be applied to challenges across eight critical business areas: 2024 R&D STRATEGY REPORT—EXECUTIVE SUMMARY PAGE 6

## Actual answer (local Gemma)

Status: **answered**

```text
Of the 67 problem statements from 2023, 17 original problem statements were "graduated" [1]. In 2024, 17 new problem statements were added [2].
```

## Citations

- [1] PG&E 2024 R&D Strategy Report, p. 5 → `vault/raw/pge-rd-strategy-report-executive-summary-2024.pdf`#page=5 (retrieval rank 1)
- [2] PG&E 2024 R&D Strategy Report, p. 5 → `vault/raw/pge-rd-strategy-report-executive-summary-2024.pdf`#page=5 (retrieval rank 1)

## Automated checks

- ✅ expected passage retrieved
- ✅ all expected passages given to the model
- ✅ status is answered
- ✅ cites the expected source
- ✅ cites every expected passage
- ✅ answer contains ['(graduated|retired)[^.]{0,40}\\b17\\b|\\b17\\b[^.]{0,60}(graduated|retired)', '\\b17\\b[^.]{0,20}new|added[^.]{0,20}\\b17\\b']

**Result: PASS**
