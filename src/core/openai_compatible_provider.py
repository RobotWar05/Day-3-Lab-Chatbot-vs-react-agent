import time
from typing import Any, Dict, Generator, Optional

from openai import OpenAI

from src.core.llm_provider import LLMProvider


class OpenAICompatibleProvider(LLMProvider):
    """
    Provider for APIs that follow the OpenAI Chat Completions protocol.

    Examples:
    - OpenCode endpoint
    - MiMo endpoint
    - OpenRouter-compatible endpoints
    """

    def __init__(
        self,
        provider_name: str,
        model_name: str,
        api_key: Optional[str],
        base_url: str,
    ):
        super().__init__(model_name=model_name, api_key=api_key)
        self.provider_name = provider_name
        self.base_url = base_url
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        start_time = time.time()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )

        latency_ms = int((time.time() - start_time) * 1000)
        usage_obj = getattr(response, "usage", None)

        usage = {
            "prompt_tokens": getattr(usage_obj, "prompt_tokens", 0) if usage_obj else 0,
            "completion_tokens": getattr(usage_obj, "completion_tokens", 0) if usage_obj else 0,
            "total_tokens": getattr(usage_obj, "total_tokens", 0) if usage_obj else 0,
        }

        return {
            "content": response.choices[0].message.content or "",
            "usage": usage,
            "latency_ms": latency_ms,
            "provider": self.provider_name,
        }

    def stream(self, prompt: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            stream=True,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content
