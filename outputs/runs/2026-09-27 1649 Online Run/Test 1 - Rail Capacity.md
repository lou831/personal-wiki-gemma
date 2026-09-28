# Test 1 — Rail Capacity

- **Mode:** ask · **execution:** local (offline guard on) · **OS network:** default route via en0 (network connected)
- **Model / runtime:** `mlx-community/gemma-4-e4b-it-4bit` (Gemma 4 E4B, 4-bit MLX) via mlx-lm 0.31.3 / mlx 0.32.2; embeddings `BAAI/bge-small-en-v1.5` via sentence-transformers 6.1.0
- **Run:** 2026-09-27 16:46:29 · retrieval 0.02s · generation 13.8s · 1729 prompt tokens · 67 output tokens · 15.3 tok/s · MLX peak 4.91 GB
- **Kind:** direct question, one source

## Question

> According to Metro's Rail Modernization Program, how many trains per hour could automation raise practical capacity to?

## Expected (written before the run)

Answers 30 or more trains per hour (up from 24), citing p. 4 of the rail plan.

- Source: `vault/raw/3A-Rail-Modernization-Program.pdf`, p. 4
- Passage must contain: “raise practical capacity limits from 24 to 30 trains per hour or more”

## Retrieved passages (inspected before the answer)

Numbered as shown to the model; `[n]` in the answer refers to these numbers.

Expected passage retrieved at rank: **1**

**[1] WMATA Rail Modernization Program, p. 4** — retrieval rank 1; cosine 0.81, bm25 25.2
note `vault/wiki/Transportation/WMATA Rail Modernization Program.md` · original `vault/raw/3A-Rail-Modernization-Program.pdf` p. 4

> Capacity: Automation increases train throughput using existing infrastructure, helping avoid or delay costly expansion projects. By optimizing operations with the same fleet and rail lines, Metro can increase capacity substantially. Throughput improvements will raise practical capacity limits from 24 to 30 trains per hour or more; equivalent to trains approximately every 2 minutes. Faster turnbacks enabled by automation further increase capacity. These enhancements make the system more attractive to riders, supporting projected ridership growth and increase fare revenue potential over time. Efficiency: End-to-end travel times are expected to decrease with automation, driven by optimized acceleration and deceleration. 9 of 187

**[2] WMATA Rail Modernization Program, p. 4** — retrieval rank 1; same-page neighbor of rank 1, added as context
note `vault/wiki/Transportation/WMATA Rail Modernization Program.md` · original `vault/raw/3A-Rail-Modernization-Program.pdf` p. 4

> Platform screen doors (PSDs) further improve safety by virtually eliminating track intrusions, trespassing incidents, and fatalities from persons struck by trains. Automation also leads to smoother acceleration and braking, reducing the risk of passenger falls onboard. Reliability: Automation improves on-time performance, achieving 95–99% reliability. It enables more consistent and optimized dwell times, supports higher speeds, and allows for faster recovery from delays. Service is no longer constrained by operator availability and can adjust quickly to disruptions or demand surges. The new system will require fewer repairs and experience fewer critical incidents, reducing the likelihood of extended service delays. Together, these improvements reduce waiting times for customers and increase overall system resilience. Capacity: Automation increases train throughput using existing infrastructure, helping avoid or delay costly expansion projects.

**[3] WMATA Rail Modernization Program, p. 30** — retrieval rank 2; cosine 0.77, bm25 18.5
note `vault/wiki/Transportation/WMATA Rail Modernization Program.md` · original `vault/raw/3A-Rail-Modernization-Program.pdf` p. 30

> 24 Washington Metropolitan Area Transit Authority Rail Modernization Program Benefits of Modernization address Metro’s needs Signal system upgrades, platform screen doors, and automation provide benefits across four key areas of Metrorail service Benefits Capacity ▪Increase train throughput from 24 trains per hour to 30+ trains per hour Reliability ▪Increased on-time performance up to 98% with automated operations ▪Reduced signal incidents, delays Efficiency ▪Faster cycle times ▪Lower marginal costs / revenue hour Safety ▪Reduce fatalities and trespass incidents by 80% to 100% with platform screen doors Benefit estimates based on international benchmarking of capabilities of similar systems, rail operations simulations of Metro’s system, and analysis of Metro internal data 35 of 187

**[4] WMATA Rail Modernization Program, p. 35** — retrieval rank 3; cosine 0.77, bm25 17.4
note `vault/wiki/Transportation/WMATA Rail Modernization Program.md` · original `vault/raw/3A-Rail-Modernization-Program.pdf` p. 35

> 29 Washington Metropolitan Area Transit Authority Rail Modernization Program Efficiencies reduce capital needs for yards and facilities Modernization can deliver increased Red Line service more efficiently than the current signal system, reducing the need for fleet and facilities expansion Red Line scenarios Cycle time (minutes) 4-minute service requirements (15 trains per hour) 3-minute service requirements (20 trains per hour) Current storage capacity Storage deficit Trains Railcars Trains Railcars Railcars Railcars ATC (Current) 136 36 346 48 462 388 -74 CBTC 126 34 328 44 424 388 -36 Automation 118 32 308 42 404 388 -16 Reduced vehicle requirements with modernization would require a smaller scope of yard improvement projects to maximize efficiency. Train requirements include revenue service trains and gap trains. Railcar requirements assume 100% eight-car trains on the Red Line during peak service and a 20% spare ratio.

**[5] WMATA Rail Modernization Program, p. 35** — retrieval rank 3; same-page neighbor of rank 3, added as context
note `vault/wiki/Transportation/WMATA Rail Modernization Program.md` · original `vault/raw/3A-Rail-Modernization-Program.pdf` p. 35

> Railcar requirements assume 100% eight-car trains on the Red Line during peak service and a 20% spare ratio. 58 fewer railcars would realize approximately $320 million in lifetime capital purchase and renewal savings 40 of 187

**[6] WMATA Rail Modernization Program, p. 47** — retrieval rank 4; cosine 0.78, bm25 14.1
note `vault/wiki/Transportation/WMATA Rail Modernization Program.md` · original `vault/raw/3A-Rail-Modernization-Program.pdf` p. 47

> 41 Rail Modernization Program Washington Metropolitan Area Transit Authority Rail modernization is the path to world-class transit Investment in modern, automated systems can transform the way Metro operates Metro has a unique opportunity to align needed investments in our major systems (railcars and signals) by upgrading our capabilities with next-generation technology. Automation’s benefits can transform Metro’s operations 1. Safer: reduce staff on roadway, keep trespassers off tracks, reduce track fires 2. More reliable: increase service reliability up to 99% with precision operation and dynamic adjustments, less physical infrastructure to maintain 3. Greater capacity: faster trips and more trains running per hour 4. More efficient: more productive service with the same assets and lower operating costs; growing ridership and revenue Metro is mobilizing to pursue federal funding opportunities, including core capacity grants and low interest financing.

**[7] WMATA Rail Modernization Program, p. 51** — retrieval rank 5; cosine 0.76, bm25 20.6
note `vault/wiki/Transportation/WMATA Rail Modernization Program.md` · original `vault/raw/3A-Rail-Modernization-Program.pdf` p. 51

> 45 Washington Metropolitan Area Transit Authority Rail Modernization Program How Rail Modernization increases capacity Modern signal systems can safely increase throughput for existing tracks Current Service Service operating below maximum scheduled throughput of 24 trains per hour Potential Service Delivery vs. Tunnel Capacity (trains per hour) Add Capacity via Expansion (Blue Line Loop concept) Building a new tunnel adds capacity but inefficiently uses it. Tunnels limited to same maximum throughput Add Capacity via Modernization New technology increases throughput and capacity; efficiently uses Metro’s existing tunnel infrastructure B O S 24 tph 6 tph 6 tph 8 tph 24 tph 10 tph 24 tph 10 tph 10 tph 30 tph 10 tph 10 tph 10 tph Same capacity increase Same total service delivered (30 trains per hour) 20 trains per hour Capacity utilization: 83% 30 trains per hour Capacity utilization: 100% 30 trains per hour Capacity utilization: 63% Blue Line service limited by shared tracks with the Yellow Line New tunnel has the same throughput as the current tunnel 56 of 187

**[8] WMATA Rail Modernization Program, p. 52** — retrieval rank 6; cosine 0.77, bm25 10.6
note `vault/wiki/Transportation/WMATA Rail Modernization Program.md` · original `vault/raw/3A-Rail-Modernization-Program.pdf` p. 52

> 46 Washington Metropolitan Area Transit Authority Rail Modernization Program Modernization can deliver more service from existing infrastructure Efficient fleet utilization reduces demand for railcar storage expansion Modernization and Automation can: ▪ Add Red Line service without the need to increase rail yard storage and maintenance capacity ▪ Automate yard operations with automatic coupling and uncoupling of trains to more effectively use existing storage tracks ▪ Automated dispatching can enable train length optimization during the day Example: Shady Grove Yard ▪ 166 total railcar storage spaces; 72% of railcars can be stored as 8-car trains Estimated rail yard capital needs: • $1.3 billion estimated total system cost • $300-400 million for Red Line rail yard projects 57 of 187

## Actual answer (local Gemma)

Status: **answered**

```text
Automation could raise practical capacity limits from 24 to 30 trains per hour or more [1]. Modernization can increase train throughput from 24 trains per hour to 30+ trains per hour [3]. Additionally, new technology allows for 30 trains per hour throughput using existing tunnel infrastructure [7].
```

## Citations

- [1] WMATA Rail Modernization Program, p. 4 → `vault/raw/3A-Rail-Modernization-Program.pdf`#page=4 (retrieval rank 1)
- [3] WMATA Rail Modernization Program, p. 30 → `vault/raw/3A-Rail-Modernization-Program.pdf`#page=30 (retrieval rank 2)
- [7] WMATA Rail Modernization Program, p. 51 → `vault/raw/3A-Rail-Modernization-Program.pdf`#page=51 (retrieval rank 5)

## Automated checks

- ✅ expected passage retrieved
- ✅ all expected passages given to the model
- ✅ status is answered
- ✅ cites the expected source
- ✅ cites every expected passage
- ✅ answer contains ['\\b24\\b', '\\b30\\b']

**Result: PASS**
