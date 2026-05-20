from __future__ import annotations

from ai_configuration.factory.base import AIClient


class WriterClient(AIClient):
    """Writer chat client."""

    def __init__(self, api_key: str, model: str, max_tokens: int) -> None:
        super().__init__(api_key=api_key, model=model, max_tokens=max_tokens)
        from writerai import AsyncWriter

        self._client = AsyncWriter(api_key=api_key)

    async def chat(self, messages: list[dict[str, str]]) -> str:
        """Send messages and return the assistant reply."""
        response = await self._client.chat.chat(
            model=self._model,
            messages=messages,
            max_tokens=self._max_tokens,
        )
        return response.choices[0].message.content or ""
