"""Model runtime: loads Gemma locally with mlx-lm and turns messages into text.

This is the only file that talks to the model. The harness hands it a list of
chat messages; it applies Gemma's chat template, runs generation on the Apple
GPU through MLX, and returns the text plus speed and memory numbers.
"""

import re
import time
from dataclasses import dataclass
from typing import Callable

from . import config


@dataclass
class Generation:
    text: str
    prompt_tokens: int
    generation_tokens: int
    prompt_tps: float
    generation_tps: float
    peak_memory_gb: float
    seconds: float


class LocalLLM:
    def __init__(self, model_id: str = config.LLM_ID):
        self.model_id = model_id
        self.model = None
        self.tokenizer = None
        self.load_seconds = 0.0
        self.calls = 0  # tests use this to prove search mode never calls the model

    def load(self) -> None:
        if self.model is not None:
            return
        from mlx_lm import load  # imported lazily so `wiki search` never pays for it

        start = time.perf_counter()
        try:
            self.model, self.tokenizer = load(self.model_id)
        except Exception as e:  # missing weights, corrupted cache, unsupported model type
            raise RuntimeError(
                f"The local model {self.model_id} is not available ({type(e).__name__}: {e}). "
                f"While online, download it once with:  hf download {self.model_id}"
            ) from e
        self.load_seconds = time.perf_counter() - start

    def generate(
        self,
        messages: list[dict],
        max_tokens: int,
        temperature: float = 0.0,
        on_text: Callable[[str], None] | None = None,
    ) -> Generation:
        from mlx_lm import stream_generate
        from mlx_lm.sample_utils import make_sampler

        self.load()
        self.calls += 1
        prompt = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, enable_thinking=False
        )
        sampler = make_sampler(temp=temperature, top_p=0.95 if temperature > 0 else 0.0)

        start = time.perf_counter()
        text, last = "", None
        for chunk in stream_generate(
            self.model, self.tokenizer, prompt, max_tokens=max_tokens, sampler=sampler
        ):
            text += chunk.text
            last = chunk
            if on_text:
                on_text(chunk.text)
        elapsed = time.perf_counter() - start

        self.thinking_stripped = bool(THINKING.search(text))
        return Generation(
            text=_clean(text),
            prompt_tokens=last.prompt_tokens if last else 0,
            generation_tokens=last.generation_tokens if last else 0,
            prompt_tps=last.prompt_tps if last else 0.0,
            generation_tps=last.generation_tps if last else 0.0,
            peak_memory_gb=last.peak_memory if last else 0.0,
            seconds=elapsed,
        )


THINKING = re.compile(r"<\|channel>.*?(<channel\|>|$)", re.S)


def _clean(text: str) -> str:
    # Gemma 4 can emit a hidden reasoning block ("<|channel>thought ... <channel|>")
    # even with thinking disabled; it is never part of the answer.
    text = THINKING.sub("", text)
    # Drop any stray turn markers the template might leak.
    text = re.sub(r"<\|?(end_of_turn|eos|turn\|?>)[^>]*>?", "", text)
    return text.strip()
