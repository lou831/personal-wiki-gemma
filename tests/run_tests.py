"""Assignment test suite. Run with `./wiki test`.

Everything written comes from this run: answers, retrieved passages, checks,
timings and memory are recorded as they happen. Output folder:
  outputs/runs/<date time> <Offline|Online> Run/
    Test Report.md          summary table + machine/model/network facts
    Test 1 - <name>.md …    one evidence card per ask-mode test
    Mode Checks.md          transcript of the chat / search / ask boundary checks
Set RUN_DIR to write into a specific folder (offline_test.sh does this).
"""

import hashlib
import json
import os
import platform
import re
import socket
import subprocess
import time
from datetime import datetime
from importlib.metadata import version
from pathlib import Path

import yaml

from harness import config, vault
from harness.core import Harness, memory_snapshot
from harness.ingest import extract_pages
from harness.offline import BLOCKED, NetworkBlocked
from harness.retrieval import cite_label

SPEC = yaml.safe_load((config.ROOT / "tests" / "questions.yaml").read_text(encoding="utf-8"))
REFUSAL = re.compile(r"insufficient evidence|INSUFFICIENT_EVIDENCE", re.I)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def network_status() -> str:
    """OS-level view of connectivity, independent of the in-process guard."""
    r = subprocess.run(["route", "-n", "get", "default"], capture_output=True, text=True)
    m = re.search(r"interface: (\S+)", r.stdout)
    return f"default route via {m.group(1)} (network connected)" if r.returncode == 0 and m else \
        "no default route (offline)"


def runtime_line() -> str:
    size = "E2B" if "e2b" in config.LLM_ID else "E4B" if "e4b" in config.LLM_ID else "?"
    return (f"`{config.LLM_ID}` (Gemma 4 {size}, 4-bit MLX) via mlx-lm {version('mlx-lm')} / mlx {version('mlx')}; "
            f"embeddings `{config.EMBED_ID}` via sentence-transformers {version('sentence-transformers')}")


class Suite:
    def __init__(self):
        self.results = []
        self.cards = []
        self.transcript: list[str] = []
        self.h = Harness()
        self.network = network_status()

    def record(self, name, passed, seconds, details, output=""):
        self.results.append({"test": name, "passed": bool(passed), "seconds": round(seconds, 2),
                             "details": details, "output": output, "memory": memory_snapshot()})
        print(f"{'PASS' if passed else 'FAIL'}  {name}  ({seconds:.1f}s)  {details}", flush=True)

    def log(self, *lines):
        self.transcript += list(lines)

    # --- the four ask-mode tests -----------------------------------------------------------------------
    def ask_tests(self):
        for q in SPEC["ask"]:
            t0 = time.perf_counter()
            r = self.h.ask(q["question"])
            secs = time.perf_counter() - t0
            snippets = [norm(q[k]) for k in ("evidence", "evidence_2") if q.get(k)]
            ranks = [h.rank for h in r.hits if snippets and snippets[0] in norm(h.chunk["text"])]
            in_evidence = all(any(sn in norm(h.chunk["text"]) for h in r.hits) for sn in snippets)
            cited_files = {Path(h.chunk["original"]).name for _, h in r.citations}
            cited_expected = all(any(sn in norm(h.chunk["text"]) for _, h in r.citations) for sn in snippets)
            if q.get("unsupported"):
                checks = {"status is insufficient": r.status == "insufficient",
                          "no citations shown": not r.citations}
            else:
                missing = [p for p in q["expect"] if not re.search(p, r.answer, re.I)]
                checks = {
                    "expected passage retrieved": bool(ranks),
                    "all expected passages given to the model": in_evidence,
                    "status is answered": r.status == "answered",
                    "cites the expected source": q["source"] in cited_files,
                    "cites every expected passage": cited_expected,
                    f"answer contains {q['expect']}": not missing,
                }
            passed = all(checks.values())
            self.record(f"ask: Test {q['id']} {q['name']}", passed, secs,
                        "; ".join(f"{k}={v}" for k, v in checks.items()), r.answer)
            self.cards.append(self.card(q, r, ranks, checks, passed, secs))

    def card(self, q, r, ranks, checks, passed, secs) -> tuple[str, str]:
        g = r.generation
        lines = [
            f"# Test {q['id']} — {q['name']}", "",
            f"- **Mode:** ask · **execution:** local (offline guard on) · **OS network:** {self.network}",
            f"- **Model / runtime:** {runtime_line()}",
            f"- **Run:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} · retrieval {r.timings.get('retrieve_s', 0):.2f}s"
            + (f" · generation {g.seconds:.1f}s · {g.prompt_tokens} prompt tokens · {g.generation_tokens} output tokens"
               f" · {g.generation_tps:.1f} tok/s · MLX peak {g.peak_memory_gb:.2f} GB" if g else " · no model call"),
            f"- **Kind:** {q['kind']}", "",
            "## Question", "", f"> {q['question']}", "",
            "## Expected (written before the run)", "", q["expected_behavior"], "",
        ]
        if not q.get("unsupported"):
            lines += [f"- Source: `vault/raw/{q['source']}`, p. {q['page']}",
                      *[f"- Passage must contain: “{q[k]}”" for k in ("evidence", "evidence_2") if q.get(k)], ""]
        lines += ["## Retrieved passages (inspected before the answer)", "",
                  "Numbered as shown to the model; `[n]` in the answer refers to these numbers.", ""]
        if not q.get("unsupported"):
            lines += [f"Expected passage retrieved at rank: **{', '.join(map(str, ranks)) or 'NOT RETRIEVED'}**", ""]
        for h in r.hits:
            c = h.chunk
            how = (f"same-page neighbor of rank {h.rank}, added as context" if h.neighbor_of
                   else f"cosine {h.cosine:.2f}, bm25 {h.bm25:.1f}")
            lines += [f"**[{r.hits.index(h) + 1}] {cite_label(c)}** — retrieval rank {h.rank}; {how}",
                      f"note `vault/{c['note_path']}` · original `vault/{c['original']}`"
                      + (f" p. {c['page']}" if c.get("page") else ""), "", f"> {c['text']}", ""]
        lines += ["## Actual answer (local Gemma)", "", f"Status: **{r.status}**", "", "```text", r.answer, "```", ""]
        if r.raw_output and r.raw_output.strip() != r.answer.strip():
            lines += ["Raw model output before the harness citation check:", "", "```text", r.raw_output, "```", ""]
        if r.reason:
            lines += [f"Harness reason: {r.reason}", ""]
        lines += ["## Citations", ""]
        if r.citations:
            for n, h in r.citations:
                c = h.chunk
                lines.append(f"- [{n}] {cite_label(c)} → `vault/{c['original']}`"
                             + (f"#page={c['page']}" if c.get("page") else "") + f" (retrieval rank {h.rank})")
        else:
            lines.append("- none")
        lines += ["", "## Automated checks", ""]
        lines += [f"- {'✅' if v else '❌'} {k}" for k, v in checks.items()]
        lines += ["", f"**Result: {'PASS' if passed else 'FAIL'}**", ""]
        return f"Test {q['id']} - {q['name']}.md", "\n".join(lines)

    # --- chat / search / ask boundary checks --------------------------------------------------------------
    def _chat_log(self, turn):
        self.log(f"**You:** {turn.user}", "")
        if turn.search_query:
            who = {"rule": "harness routing rule", "model": "model request", "forced": "/notes"}.get(turn.route, turn.route)
            self.log(f"*(notes tool used — trigger: {who}; query “{turn.search_query}”, {len(turn.hits)} passages)*", "")
        self.log(f"**Wren:** {turn.reply}", "")

    def capabilities(self):
        m = SPEC["modes"]
        for msg in m["capabilities"]:
            s = self.h.chat()
            t0 = time.perf_counter()
            turn = s.send(msg)
            words = [w for w in m["capability_words"] if w in turn.reply.lower()]
            ok = turn.search_query is None and not REFUSAL.search(turn.reply) and len(words) >= 2
            self.log(f"### Chat: “{msg}”", "")
            self._chat_log(turn)
            self.record(f"chat: “{msg}” explains capabilities", ok, time.perf_counter() - t0,
                        f"notes searched={turn.search_query!r}; refusal={bool(REFUSAL.search(turn.reply))}; "
                        f"capability words={words}", turn.reply)

    def casual(self):
        m = SPEC["modes"]["casual"]
        s = self.h.chat()
        t0 = time.perf_counter()
        turn = s.send(m["message"])
        ok = turn.search_query is None and all(re.search(p, turn.reply, re.I) for p in m["expect"])
        self.log("### Chat: casual drafting", "")
        self._chat_log(turn)
        self.record("chat: casual drafting (no forced lookup)", ok, time.perf_counter() - t0,
                    f"notes searched={turn.search_query!r}", turn.reply)

    def draft_then_shorten(self):
        m = SPEC["modes"]["draft_then_shorten"]
        s = self.h.chat()
        first = s.send(m["draft"])
        t0 = time.perf_counter()
        second = s.send(m["followup"])
        kept = [w for w in m["expect_any"] if w in second.reply.lower()]
        ok = (first.search_query is None and second.search_query is None
              and len(second.reply) < len(first.reply) and len(kept) >= 2)
        self.log("### Chat: draft, then “make that shorter”", "")
        self._chat_log(first)
        self._chat_log(second)
        self.record("chat: “make that shorter” uses the conversation", ok, time.perf_counter() - t0,
                    f"length {len(first.reply)}->{len(second.reply)} chars; kept items={kept}; "
                    f"notes searched={first.search_query!r}/{second.search_query!r}", second.reply)

    def followup_and_separation(self):
        m = SPEC["modes"]["followup"]
        s = self.h.chat()
        self.log("### Chat: conversational follow-up", "")
        for msg in m["turns"]:
            self._chat_log(s.send(msg))
        t0 = time.perf_counter()
        turn = s.send(m["followup"])
        self._chat_log(turn)
        missing = [p for p in m["expect"] if not re.search(p, turn.reply, re.I)]
        self.record("chat: conversational follow-up", not missing and turn.search_query is None,
                    time.perf_counter() - t0,
                    f"missing={missing}; notes searched={turn.search_query!r}; history messages={len(s.history)}",
                    turn.reply)

        before = json.dumps(s.history)
        t0 = time.perf_counter()
        q = SPEC["ask"][0]["question"]
        r = self.h.ask(q, save=False)
        prompt = json.dumps(r.messages)
        persona_head = (config.PROMPTS / "assistant.md").read_text(encoding="utf-8")[:60]
        checks = {
            "two messages (rules + question)": [x["role"] for x in r.messages] == ["system", "user"],
            "no chat text in prompt": not any(x["content"] in prompt for x in s.history if x["role"] == "user")
            and "Lisbon" not in prompt,
            "no persona in prompt": persona_head not in prompt and "Wren" not in prompt,
            "chat history unchanged": json.dumps(s.history) == before,
            "research rules used": "Research Rules" in r.messages[0]["content"],
        }
        self.log("### Ask inside the same session (standalone)", "", f"`/ask {q}`", "",
                 "Prompt roles sent to the model: " + ", ".join(x["role"] for x in r.messages), "",
                 f"**Answer:** {r.answer}", "")
        self.record("separation: ask ignores chat history", all(checks.values()), time.perf_counter() - t0,
                    "; ".join(f"{k}={v}" for k, v in checks.items()))

    def chat_claim_not_evidence(self):
        m = SPEC["modes"]["chat_claim_not_evidence"]
        s = self.h.chat()
        turn = s.send(m["chat"])
        t0 = time.perf_counter()
        r = self.h.ask(m["ask"], save=False)
        ok = r.status == "insufficient" and "900" not in r.answer
        self.log("### A claim made only in chat is not evidence for ask", "")
        self._chat_log(turn)
        self.log(f"`/ask {m['ask']}`", "", f"**Ask ({r.status}):** {r.answer}", "")
        self.record("separation: chat-only claim is not ask evidence", ok, time.perf_counter() - t0,
                    f"ask status={r.status}; '900' in answer={'900' in r.answer}", r.answer)

    def notes_tool(self):
        s = self.h.chat()
        t0 = time.perf_counter()
        turn = s.send(SPEC["modes"]["notes_tool"]["message"])
        cited = bool(re.search(r"\[\d\]", turn.reply))
        self.log("### Chat: question about the notes (tool use)", "")
        self._chat_log(turn)
        for i, h in enumerate(turn.hits, 1):
            self.log(f"- [{i}] {cite_label(h.chunk)} — `vault/{h.chunk['note_path']}`")
        self.log("")
        self.record("chat: uses notes tool and cites when asked about notes", bool(turn.search_query and turn.hits and cited),
                    time.perf_counter() - t0,
                    f"notes searched={turn.search_query!r} (trigger: {turn.route}); hits={len(turn.hits)}; "
                    f"[n] citations in reply={cited}",
                    turn.reply)

    def search_raw(self):
        calls = self.h.llm.calls
        q = SPEC["modes"]["search"]["query"]
        t0 = time.perf_counter()
        hits = self.h.search(q, 5)
        secs = time.perf_counter() - t0
        cache, verbatim, paths_ok = {}, 0, 0
        for h in hits:
            c = h.chunk
            if c["original"] not in cache:
                cache[c["original"]] = [norm(p) for p in extract_pages(config.VAULT / c["original"])[0]]
            page_text = cache[c["original"]][(c["page"] or 1) - 1]
            verbatim += norm(c["text"]) in page_text
            paths_ok += (config.VAULT / c["note_path"]).is_file() and (config.VAULT / c["original"]).is_file()
        ok = hits and verbatim == len(hits) == paths_ok and self.h.llm.calls == calls
        self.log(f"### Search: “{q}” (no language model)", "")
        for h in hits:
            self.log(f"**[{h.rank}] {cite_label(h.chunk)}** — `vault/{h.chunk['original']}` p. {h.chunk['page']}"
                     f" · note `vault/{h.chunk['note_path']}`", "", f"> {h.chunk['text']}", "")
        self.record("search: raw passages, no generation", ok, secs,
                    f"hits={len(hits)}; verbatim from original page={verbatim}; paths exist={paths_ok}; "
                    f"model calls during search={self.h.llm.calls - calls}")

    # --- vault, re-ingest, network ---------------------------------------------------------------------------
    def vault_and_reingest(self):
        t0 = time.perf_counter()
        problems = vault.check_vault(chunks=self.h.chunks)
        self.record("vault: names, H1s, links, sources, index, corrections", not problems,
                    time.perf_counter() - t0, f"{len(vault.all_notes())} notes; problems={problems or 'none'}")

        store = vault.load_store()
        ok_files = [hashlib.sha256((config.VAULT / s["original"]).read_bytes()).hexdigest() == s["sha256"]
                    and not os.access(config.VAULT / s["original"], os.W_OK) for s in store["sources"].values()]
        self.record("originals in raw/: unchanged and read-only", all(ok_files), 0.0,
                    f"{sum(ok_files)}/{len(ok_files)} match their ingest SHA-256 and are read-only")

        before = sorted(vault.rel(p) for p in vault.all_notes())
        n_chunks, calls = len(self.h.chunks.chunks), self.h.llm.calls
        t0 = time.perf_counter()
        info = self.h.ingest(str(config.RAW / SPEC["modes"]["reingest"]["file"]))
        after = sorted(vault.rel(p) for p in vault.all_notes())
        ok = (info["status"] == "already ingested" and before == after
              and n_chunks == len(self.h.chunks.chunks) and self.h.llm.calls == calls)
        self.record("re-ingest: no duplicates, names kept", ok, time.perf_counter() - t0,
                    f"status={info['status']}; notes {len(before)}->{len(after)}; "
                    f"passages {n_chunks}->{len(self.h.chunks.chunks)}; model calls={self.h.llm.calls - calls}")

    def network_guard(self):
        blocked = list(BLOCKED)
        try:
            socket.create_connection(("huggingface.co", 443), timeout=3)
            probe = "connected (guard failed)"
        except NetworkBlocked:
            probe = "blocked by local-mode guard"
        except OSError as e:
            probe = f"failed: {e}"
        self.record("local only: no network use, no cloud fallback", not blocked and probe.startswith("blocked"),
                    0.0, f"network attempts during tests={len(blocked)}; outbound probe={probe}; OS network={self.network}")

    # --- report ----------------------------------------------------------------------------------------------------
    def write(self, total: float) -> Path:
        stamp = datetime.now()
        label = "Offline Run" if "offline" in self.network else "Online Run"
        folder = Path(os.environ["RUN_DIR"]) if os.environ.get("RUN_DIR") else \
            config.OUTPUTS / "runs" / f"{stamp.strftime('%Y-%m-%d %H%M')} {label}"
        folder.mkdir(parents=True, exist_ok=True)
        store = vault.load_store()
        passed = sum(r["passed"] for r in self.results)
        mem = memory_snapshot()
        chip = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip()
        lines = [
            "# Test Report", "",
            f"- **Run:** {stamp.strftime('%Y-%m-%d %H:%M:%S')} · {label}",
            f"- **Machine:** macOS {platform.mac_ver()[0]}, {chip}, 16 GB unified memory",
            f"- **Model / runtime:** {runtime_line()}",
            f"- **Mode:** local (in-process network guard on; no online mode configured)",
            f"- **Network (OS view):** {self.network}",
            f"- **Wiki:** {len(store['sources'])} sources, {len(store['concepts'])} concepts, "
            f"{len(vault.all_notes())} notes, {len(self.h.chunks.chunks)} passages",
            f"- **Model load:** {self.h.llm.load_seconds:.1f}s · **suite time:** {total:.1f}s",
            f"- **Memory at end:** MLX peak {mem.get('mlx_peak_gb')} GB, MLX active {mem.get('mlx_active_gb')} GB, "
            f"process RSS {mem['process_rss_gb']} GB, system available {mem['system_available_gb']} GB",
            f"- **Result:** **{passed}/{len(self.results)} passed**", "",
            "Evidence cards: " + ", ".join(f"[{n[:-3]}](<{n}>)" for n, _ in self.cards) + " · [Mode Checks](<Mode Checks.md>)", "",
            "| Test | Result | Time (s) | MLX peak (GB) |", "|---|---|---|---|",
        ]
        lines += [f"| {r['test']} | {'PASS' if r['passed'] else 'FAIL'} | {r['seconds']} | {r['memory'].get('mlx_peak_gb', '')} |"
                  for r in self.results]
        lines += ["", "## Details", ""]
        for r in self.results:
            lines += [f"### {r['test']} — {'PASS' if r['passed'] else 'FAIL'}", "", r["details"], ""]
            if r["output"]:
                lines += ["```text", r["output"].strip(), "```", ""]
        (folder / "Test Report.md").write_text("\n".join(lines), encoding="utf-8")
        for name, text in self.cards:
            (folder / name).write_text(text, encoding="utf-8")
        head = [f"# Mode Checks", "", f"- Run: {stamp.strftime('%Y-%m-%d %H:%M:%S')} · {label} · local · {config.LLM_ID}",
                f"- OS network: {self.network}", ""]
        (folder / "Mode Checks.md").write_text("\n".join(head + self.transcript), encoding="utf-8")
        (config.OUTPUTS / "logs").mkdir(parents=True, exist_ok=True)
        with (config.OUTPUTS / "logs" / "tests.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps({"time": stamp.isoformat(timespec="seconds"), "network": self.network,
                                "results": self.results}, default=str) + "\n")
        return folder


def main() -> int:
    t0 = time.perf_counter()
    s = Suite()
    print(f"OS network: {s.network}")
    print("Loading local model …", flush=True)
    s.h.llm.load()
    for step in (s.search_raw, s.ask_tests, s.capabilities, s.casual, s.draft_then_shorten,
                 s.followup_and_separation, s.chat_claim_not_evidence, s.notes_tool,
                 s.vault_and_reingest, s.network_guard):
        try:
            step()
        except Exception as e:  # a crash is a failed test, not a missing one
            s.record(step.__name__, False, 0.0, f"crashed: {type(e).__name__}: {e}")
    folder = s.write(time.perf_counter() - t0)
    passed = sum(r["passed"] for r in s.results)
    # RUN_DIR may be relative (offline_test.sh); print a project-relative path either way
    print(f"\n{passed}/{len(s.results)} passed · evidence: {os.path.relpath(folder.resolve(), config.ROOT)}")
    return 0 if passed == len(s.results) else 1
