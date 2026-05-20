from __future__ import annotations

from ai_configuration.factory.base import AIClient


class OllamaClient(AIClient):
    """Ollama local chat client."""

    def __init__(self, api_key: str, model: str) -> None:
        from ollama import AsyncClient

        host = api_key if api_key.startswith("http") else "http://localhost:11434"
        self._client = AsyncClient(host=host)
        self._model = model

    async def chat(self, messages: list[dict[str, str]], max_tokens: int) -> str:
        """Send messages and return the assistant reply."""
        response = await self._client.chat(
            model=self._model,
            messages=messages,
            options={"num_predict": max_tokens},
        )
        return response.message.content or ""
