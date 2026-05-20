from __future__ import annotations

from ai_configuration.factory.base import AIClient


class OllamaClient(AIClient):
    """Ollama local chat client."""

    def __init__(self, api_key: str, model: str, max_tokens: int) -> None:
        super().__init__(api_key=api_key, model=model, max_tokens=max_tokens)
        from ollama import AsyncClient

        host = api_key if api_key.startswith("http") else "http://localhost:11434"
        self._client = AsyncClient(host=host)

    async def chat(self, messages: list[dict[str, str]]) -> str:
        """Send messages and return the assistant reply."""
        response = await self._client.chat(
            model=self._model,
            messages=messages,
            options={"num_predict": self._max_tokens},
        )
        return response.message.content or ""
