from __future__ import annotations

from ai_configuration.constants import Provider
from ai_configuration.factory.base import AIClient

PROVIDER_BASE_URLS: dict[str, str] = {
    Provider.TOGETHER_AI: "https://api.together.xyz/v1",
    Provider.PERPLEXITY_AI: "https://api.perplexity.ai",
    Provider.XAI: "https://api.x.ai/v1",
    Provider.DEEPSEEK: "https://api.deepseek.com/v1",
    Provider.FIREWORKS_AI: "https://api.fireworks.ai/inference/v1",
    Provider.SAMBANOVA: "https://api.sambanova.ai/v1",
    Provider.LM_STUDIO: "http://localhost:1234/v1",
    Provider.LOCALAI: "http://localhost:8080/v1",
    Provider.JAN: "http://localhost:1337/v1",
    Provider.VLLM: "http://localhost:8000/v1",
    Provider.LLAMA_CPP: "http://localhost:8000/v1",
    Provider.KOBOLDCPP: "http://localhost:5001/v1",
    Provider.LLAMAFILE: "http://localhost:8080/v1",
    Provider.TEXT_GENERATION_WEBUI: "http://localhost:5000/v1",
    Provider.GPT4ALL: "http://localhost:4891/v1",
}


class OpenAICompatibleClient(AIClient):
    """Generic client for any provider that exposes an OpenAI-compatible chat API."""

    def __init__(
        self, api_key: str, model: str, max_tokens: int, base_url: str
    ) -> None:
        super().__init__(api_key=api_key, model=model, max_tokens=max_tokens)
        from openai import AsyncOpenAI

        self._client = AsyncOpenAI(api_key=api_key or "not-needed", base_url=base_url)

    async def chat(self, messages: list[dict[str, str]]) -> str:
        """Send messages and return the assistant reply."""
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            max_tokens=self._max_tokens,
        )
        return response.choices[0].message.content or ""
