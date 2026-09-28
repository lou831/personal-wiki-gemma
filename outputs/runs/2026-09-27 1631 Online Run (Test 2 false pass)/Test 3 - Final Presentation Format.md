# Test 3 — Final Presentation Format

- **Mode:** ask · **execution:** local (offline guard on) · **OS network:** default route via en0 (network connected)
- **Model / runtime:** `mlx-community/gemma-4-e4b-it-4bit` (Gemma 4 E4B, 4-bit MLX) via mlx-lm 0.31.3 / mlx 0.32.2; embeddings `BAAI/bge-small-en-v1.5` via sentence-transformers 6.1.0
- **Run:** 2026-09-27 16:29:25 · retrieval 0.09s · generation 10.4s · 1420 prompt tokens · 39 output tokens · 14.3 tok/s · MLX peak 4.90 GB
- **Kind:** known evidence, source ingested offline

## Question

> In the Business of Energy Transition course, how many slides and how many minutes are allowed for the final group presentation?

## Expected (written before the run)

Answers 12 slides, 12 minutes plus an 8-minute Q&A, citing p. 3 of the syllabus.

- Source: `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf`, p. 3
- Passage must contain: “Format: A 12-slide presentation”

## Retrieved passages (inspected before the answer)

Expected passage retrieved at rank: **1**

**[1] Business of Energy Transition Syllabus, p. 3** — cosine 0.79, bm25 22.2
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 3

> Students will form groups of 4 to 5 members (subject to minor adjustments based on final enrollment) to develop and deliver a professional investment or business thesis tied to the energy transition. Imagine your team is pitching to an investment committee at a financial firm. Your goal is to make a compelling case for investing in or developing a specific category or sector within the energy transition space. Note: Your presentation should focus on the broader sector or category opportunity, rather than pitching a single, specific company or startup. Deliverables & Timing ● Format: A 12-slide presentation. ● Duration: 12 minutes for the presentation, followed by an 8-minute Q&A session with the committee (20 minutes total per group). ● Participation: All group members are expected to contribute equally to the conceptual development and participate equally during the oral presentation. Your presentation must explicitly address the following five elements: 1.

**[2] Business of Energy Transition Syllabus, p. 2** — cosine 0.67, bm25 25.2
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 2

> This course features guest speakers who are leaders in the fields of climate change entrepreneurship, policymaking, finance, and investment. To ensure a vibrant discussion with these speakers, students are expected to come to class prepared with questions for our guest speakers in addition to responses to assigned study questions. Laptops are not allowed in class during guest presentations except as an approved accommodation. Final Group Presentation Requirements

**[3] Business of Energy Transition Syllabus, p. 2** — cosine 0.70, bm25 9.6
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 2

> II. Course Description The energy transition is the largest capital reallocation in human history, and it is generating careers, companies, and investment opportunities at a pace no other sector can match. Using a combination of instructor-led discussion, readings, and guest speakers, this course prepares MBA students to compete for, and create, those opportunities. The course is organized in three phases: the landscape, the toolkit, and the frontier. The landscape is an overview of our traditional energy economy, the work underway and progress in the energy transition, and a vision for what our energy system can look like in the coming decades. In the toolkit phase, we work sector by sector through power, buildings, and transport. Each sector introduces a distinct set of technologies, business models and financial structures that range from large-scale project finance to behavioral economics.

**[4] Business of Energy Transition Syllabus, p. 6** — cosine 0.67, bm25 16.2
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 6

> What’s more, we are making this transition more quickly than any energy transition in human history. We will touch on the basics of electricity systems and fundamental financial concepts necessary for the course. The session will also establish a lens that runs throughout the entire course: energy is a regulated industry, not a free market, and policy creates and destroys business models as surely as technology does. Speakers: Kate Gordon, Cisco DeVries Materials ● Nathaniel Bullard,Decarbonization: Parameters, Dollars and Sense, Electrons Photons Molecules (presentation deck) (https://www.nathanielbullard.com/presentations) ● BNEF: New Energy Outlook 2026 (PDF) slides 1-6: https://about.bnef.com/insights/clean-energy/new-energy-outlook/#download-report-sum mary ● RMI Insight: The Great Reallocation (https://rmi.org/resources/the-great-reallocation/) ● Vaclav Smil: ENERGY AND CIVILIZATION: A HISTORY.

**[5] Business of Energy Transition Syllabus, p. 5** — cosine 0.68, bm25 14.1
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 5

> Written Memos: ● Wednesday, September 16, 2026 - Memo 1 is due ● Wednesday, October 14, 2026 - Memo 2 is due ● Wednesday, November 4 - Memo 3 is due Final Project: ● Thursday, November 4: Notify instructors of team formation and tentative topic ● Thursday, Nov. 12: Sign up for your preferred date (Dec 3 or 10) ● Thursday, Dec 3: All final slide decks due prior to the start of class ● Thursday, Dec. 3: Final Presentations ● Thursday, Dec. 10: Final Presentations Prerequisites and Class Participants No prior background in energy, engineering, or finance is required. Class Format & Materials Some lecture, discussion, guest speakers. Will include a mix of written memos, in-class debates, and a final group presentation. Students are required to read / watch / listen to the items listed under “Materials.” Items listed as “Recommended” are optional, and included for students who are interested in taking a deeper dive into particular subjects.

**[6] Business of Energy Transition Syllabus, p. 4** — cosine 0.67, bm25 7.6
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 4

> outstanding analysis, unique synthesis of course concepts, or a highly compelling and unique approach. Two-Page Memo Topics ● Memo 1: Analyzing the Transition Landscape. Select a single slide from Nathaniel Bullard’s 2026 slideshow (available at nathanielbullard.com/presentations). Address the following in your analysis: ○ What critical story does this slide tell us about the current state of the energy transition? ○ What key nuances, data points, or perspectives do you think this slide misses? ○ Suggest a startup business thesis that leverages the trend shown in the slide, drawing on class readings and discussions to support your case. ● Memo 2: The Role of Policy and Regulations in the Energy Transition sector. Select a single sector within the energy transition landscape (e.g., building retrofits, low-carbon fuels, EV charging infrastructure, or grid storage). Address the following in your analysis:

## Actual answer (local Gemma)

Status: **answered**

```text
The final group presentation requires a 12-slide presentation [1]. The presentation duration is 12 minutes, followed by an 8-minute Q&A session [1].
```

## Citations

- [1] Business of Energy Transition Syllabus, p. 3 → `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf`#page=3 (retrieval rank 1)

## Automated checks

- ✅ expected passage retrieved
- ✅ status is answered
- ✅ cites the expected source
- ✅ cites the expected passage
- ✅ answer contains ['\\b12\\b', 'slide', 'minute']

**Result: PASS**
