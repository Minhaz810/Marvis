from __future__ import annotations

from ai_configuration.factory.base import AIClient


class GroqClient(AIClient):
    """Groq chat client."""

    def __init__(self, api_key: str, model: str) -> None:
        from groq import AsyncGroq

        self._client = AsyncGroq(api_key=api_key)
        self._model = model

    async def chat(self, messages: list[dict[str, str]], max_tokens: int) -> str:
        """Send messages and return the assistant reply."""
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
