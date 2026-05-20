from __future__ import annotations

from ai_configuration.factory.base import AIClient


class CohereClient(AIClient):
    """Cohere chat client."""

    def __init__(self, api_key: str, model: str) -> None:
        from cohere import AsyncClientV2

        self._client = AsyncClientV2(api_key=api_key)
        self._model = model

    async def chat(self, messages: list[dict[str, str]], max_tokens: int) -> str:
        """Send messages and return the assistant reply."""
        response = await self._client.chat(
            model=self._model,
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.message.content[0].text
