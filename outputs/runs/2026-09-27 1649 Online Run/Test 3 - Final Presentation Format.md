# Test 3 — Final Presentation Format

- **Mode:** ask · **execution:** local (offline guard on) · **OS network:** default route via en0 (network connected)
- **Model / runtime:** `mlx-community/gemma-4-e4b-it-4bit` (Gemma 4 E4B, 4-bit MLX) via mlx-lm 0.31.3 / mlx 0.32.2; embeddings `BAAI/bge-small-en-v1.5` via sentence-transformers 6.1.0
- **Run:** 2026-09-27 16:46:51 · retrieval 0.03s · generation 11.4s · 1977 prompt tokens · 37 output tokens · 16.5 tok/s · MLX peak 4.95 GB
- **Kind:** known evidence, source ingested offline

## Question

> In the Business of Energy Transition course, how many slides and how many minutes are allowed for the final group presentation?

## Expected (written before the run)

Answers 12 slides, 12 minutes plus an 8-minute Q&A, citing p. 3 of the syllabus.

- Source: `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf`, p. 3
- Passage must contain: “Format: A 12-slide presentation”

## Retrieved passages (inspected before the answer)

Numbered as shown to the model; `[n]` in the answer refers to these numbers.

Expected passage retrieved at rank: **1**

**[1] Business of Energy Transition Syllabus, p. 3** — retrieval rank 1; cosine 0.79, bm25 22.2
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 3

> Students will form groups of 4 to 5 members (subject to minor adjustments based on final enrollment) to develop and deliver a professional investment or business thesis tied to the energy transition. Imagine your team is pitching to an investment committee at a financial firm. Your goal is to make a compelling case for investing in or developing a specific category or sector within the energy transition space. Note: Your presentation should focus on the broader sector or category opportunity, rather than pitching a single, specific company or startup. Deliverables & Timing ● Format: A 12-slide presentation. ● Duration: 12 minutes for the presentation, followed by an 8-minute Q&A session with the committee (20 minutes total per group). ● Participation: All group members are expected to contribute equally to the conceptual development and participate equally during the oral presentation. Your presentation must explicitly address the following five elements: 1.

**[2] Business of Energy Transition Syllabus, p. 3** — retrieval rank 1; same-page neighbor of rank 1, added as context
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 3

> Your presentation must explicitly address the following five elements: 1. Thesis Overview: A concise, clear statement of your investment or business thesis. 2. Market & Data Justification ("Why it Matters"): Robust data and analytical evidence that supports the urgency and viability of your thesis. 3. Value Proposition: An analysis of both the economic returns and the broader societal/environmental benefits provided by this sector. 4. Competitive Landscape: An overview of existing or emerging business sectors, categories, or benchmark companies operating in this or similar spaces. 5. Risk & Implementation Challenges: A realistic assessment of the key technical, regulatory, financial, or societal hurdles associated with development and implementation. Written Submission of 3 Memos We require participation through both in-class comments and written memos. Students are required to submit three written memos over the course of the semester (one for each third of the term).

**[3] Business of Energy Transition Syllabus, p. 2** — retrieval rank 2; cosine 0.67, bm25 25.2
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 2

> This course features guest speakers who are leaders in the fields of climate change entrepreneurship, policymaking, finance, and investment. To ensure a vibrant discussion with these speakers, students are expected to come to class prepared with questions for our guest speakers in addition to responses to assigned study questions. Laptops are not allowed in class during guest presentations except as an approved accommodation. Final Group Presentation Requirements

**[4] Business of Energy Transition Syllabus, p. 2** — retrieval rank 2; same-page neighbor of rank 2, added as context
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 2

> Guest speakers throughout are working practitioners, not observers. No prior background in energy, engineering, or finance is required. III. Requirements Attendance and Participation Students must attend every class session, complete all of the assigned readings and participate in class discussions. Please notify instructors in advance of any planned absences or if you require special accommodations. If it is absolutely necessary to miss a class, contact the class reader to provide you with the Zoom recording one time. To receive attendance credit for a missed class, you must write a memo on that class, including answers to discussion questions. Memos used to make up a missed class do NOT count towards the required 3 Class memos. Grades for all students will be based in part on class attendance and class participation. This course features guest speakers who are leaders in the fields of climate change entrepreneurship, policymaking, finance, and investment.

**[5] Business of Energy Transition Syllabus, p. 2** — retrieval rank 3; cosine 0.70, bm25 9.6
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 2

> II. Course Description The energy transition is the largest capital reallocation in human history, and it is generating careers, companies, and investment opportunities at a pace no other sector can match. Using a combination of instructor-led discussion, readings, and guest speakers, this course prepares MBA students to compete for, and create, those opportunities. The course is organized in three phases: the landscape, the toolkit, and the frontier. The landscape is an overview of our traditional energy economy, the work underway and progress in the energy transition, and a vision for what our energy system can look like in the coming decades. In the toolkit phase, we work sector by sector through power, buildings, and transport. Each sector introduces a distinct set of technologies, business models and financial structures that range from large-scale project finance to behavioral economics.

**[6] Business of Energy Transition Syllabus, p. 2** — retrieval rank 3; same-page neighbor of rank 3, added as context
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 2

> Each sector introduces a distinct set of technologies, business models and financial structures that range from large-scale project finance to behavioral economics. We examine the broader investment landscape —including carbon markets and blended public-private finance — and the specific ways clean energy investing differs from conventional finance. We also do a deep dive on some of the most important and topical issues, including corporate clean energy procurement strategies and the grid implications of load growth from data centers and advanced manufacturing. The final frontier phase looks forward: asking what the energy system actually looks like as we adapt to a changing climate, emerging new technologies from long-duration storage to carbon removal, and a closing practitioner panel of Berkeley alumni leading organizations at the center of the transition. Guest speakers throughout are working practitioners, not observers.

**[7] Business of Energy Transition Syllabus, p. 6** — retrieval rank 4; cosine 0.67, bm25 16.2
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 6

> What’s more, we are making this transition more quickly than any energy transition in human history. We will touch on the basics of electricity systems and fundamental financial concepts necessary for the course. The session will also establish a lens that runs throughout the entire course: energy is a regulated industry, not a free market, and policy creates and destroys business models as surely as technology does. Speakers: Kate Gordon, Cisco DeVries Materials ● Nathaniel Bullard,Decarbonization: Parameters, Dollars and Sense, Electrons Photons Molecules (presentation deck) (https://www.nathanielbullard.com/presentations) ● BNEF: New Energy Outlook 2026 (PDF) slides 1-6: https://about.bnef.com/insights/clean-energy/new-energy-outlook/#download-report-sum mary ● RMI Insight: The Great Reallocation (https://rmi.org/resources/the-great-reallocation/) ● Vaclav Smil: ENERGY AND CIVILIZATION: A HISTORY.

**[8] Business of Energy Transition Syllabus, p. 5** — retrieval rank 5; cosine 0.68, bm25 14.1
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 5

> Written Memos: ● Wednesday, September 16, 2026 - Memo 1 is due ● Wednesday, October 14, 2026 - Memo 2 is due ● Wednesday, November 4 - Memo 3 is due Final Project: ● Thursday, November 4: Notify instructors of team formation and tentative topic ● Thursday, Nov. 12: Sign up for your preferred date (Dec 3 or 10) ● Thursday, Dec 3: All final slide decks due prior to the start of class ● Thursday, Dec. 3: Final Presentations ● Thursday, Dec. 10: Final Presentations Prerequisites and Class Participants No prior background in energy, engineering, or finance is required. Class Format & Materials Some lecture, discussion, guest speakers. Will include a mix of written memos, in-class debates, and a final group presentation. Students are required to read / watch / listen to the items listed under “Materials.” Items listed as “Recommended” are optional, and included for students who are interested in taking a deeper dive into particular subjects.

**[9] Business of Energy Transition Syllabus, p. 4** — retrieval rank 6; cosine 0.67, bm25 7.6
note `vault/wiki/Coursework/Business of Energy Transition Syllabus.md` · original `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf` p. 4

> outstanding analysis, unique synthesis of course concepts, or a highly compelling and unique approach. Two-Page Memo Topics ● Memo 1: Analyzing the Transition Landscape. Select a single slide from Nathaniel Bullard’s 2026 slideshow (available at nathanielbullard.com/presentations). Address the following in your analysis: ○ What critical story does this slide tell us about the current state of the energy transition? ○ What key nuances, data points, or perspectives do you think this slide misses? ○ Suggest a startup business thesis that leverages the trend shown in the slide, drawing on class readings and discussions to support your case. ● Memo 2: The Role of Policy and Regulations in the Energy Transition sector. Select a single sector within the energy transition landscape (e.g., building retrofits, low-carbon fuels, EV charging infrastructure, or grid storage). Address the following in your analysis:

## Actual answer (local Gemma)

Status: **answered**

```text
The final group presentation requires a 12-slide presentation and has a duration of 12 minutes, followed by an 8-minute Q&A session [1].
```

## Citations

- [1] Business of Energy Transition Syllabus, p. 3 → `vault/raw/Business of Energy Transition Syllabus Fall 2026.pdf`#page=3 (retrieval rank 1)

## Automated checks

- ✅ expected passage retrieved
- ✅ all expected passages given to the model
- ✅ status is answered
- ✅ cites the expected source
- ✅ cites every expected passage
- ✅ answer contains ['\\b12\\b', 'slide', 'minute']

**Result: PASS**
