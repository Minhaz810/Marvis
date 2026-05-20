from __future__ import annotations

from ai_configuration.factory.base import AIClient

PROVIDER_BASE_URLS: dict[str, str] = {
    "Together AI": "https://api.together.xyz/v1",
    "Perplexity AI": "https://api.perplexity.ai",
    "xAI": "https://api.x.ai/v1",
    "DeepSeek": "https://api.deepseek.com/v1",
    "Fireworks AI": "https://api.fireworks.ai/inference/v1",
    "SambaNova": "https://api.sambanova.ai/v1",
    "LM Studio": "http://localhost:1234/v1",
    "LocalAI": "http://localhost:8080/v1",
    "Jan": "http://localhost:1337/v1",
    "vLLM": "http://localhost:8000/v1",
    "llama.cpp": "http://localhost:8000/v1",
    "KoboldCpp": "http://localhost:5001/v1",
    "llamafile": "http://localhost:8080/v1",
    "Text Generation WebUI": "http://localhost:5000/v1",
    "GPT4All": "http://localhost:4891/v1",
}


class OpenAICompatibleClient(AIClient):
    """Generic client for any provider that exposes an OpenAI-compatible chat API."""

    def __init__(self, api_key: str, model: str, base_url: str) -> None:
        from openai import AsyncOpenAI

        self._client = AsyncOpenAI(api_key=api_key or "not-needed", base_url=base_url)
        self._model = model

    async def chat(self, messages: list[dict[str, str]], max_tokens: int) -> str:
        """Send messages and return the assistant reply."""
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
