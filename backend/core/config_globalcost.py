import os
from typing import Any, Dict, List
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import create_agent


# Control token

# $ per input/output token, derived from the per-million-token list prices in
# https://platform.claude.com/docs/en/pricing (checked 2026-08-14).
MODEL_PRICING = {
    "claude-fable-5": (10.00 / 1_000_000, 50.00 / 1_000_000),
    "claude-mythos-5": (10.00 / 1_000_000, 50.00 / 1_000_000),
    "claude-opus-5": (5.00 / 1_000_000, 25.00 / 1_000_000),
    "claude-opus-4-8": (5.00 / 1_000_000, 25.00 / 1_000_000),
    "claude-opus-4-7": (5.00 / 1_000_000, 25.00 / 1_000_000),
    "claude-opus-4-6": (5.00 / 1_000_000, 25.00 / 1_000_000),
    "claude-sonnet-5": (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-sonnet-4-6": (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-haiku-4-5": (1.00 / 1_000_000, 5.00 / 1_000_000),
}

_DEFAULT_MODEL = "claude-sonnet-5"


class GlobalTokenCostTracker(BaseCallbackHandler):
    def __init__(self, model_name: str):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0.0

        prompt_price, completion_price = MODEL_PRICING.get(
            model_name, MODEL_PRICING[_DEFAULT_MODEL]
        )
        if model_name not in MODEL_PRICING:
            print(
                f" [Token Tracker] Unknown model '{model_name}', "
                f"pricing as '{_DEFAULT_MODEL}'."
            )

        self.prices = {
            "prompt": prompt_price,
            "completion": completion_price,
        }

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        for generations in response.generations:
            for generation in generations:
                message = getattr(generation, "message", None)
                usage = getattr(message, "usage_metadata", None) if message else None

                if not usage:
                    continue

                prompt = usage.get("input_tokens", 0)
                completion = usage.get("output_tokens", 0)

                self.total_prompt_tokens += prompt
                self.total_completion_tokens += completion

                cost = (prompt * self.prices["prompt"]) + (completion * self.prices["completion"])
                self.total_cost += cost

                print(f"\n [Token Tracker] LLM Call:")
                print(f" -> Prompt Tokens: {prompt} | Completion Tokens: {completion}")
                print(f" -> Cost for this call: ${cost:.6f}")

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": self.total_completion_tokens,
            "total_cost": self.total_cost,
            "total_cost_usd": round(self.total_cost, 6)
        }