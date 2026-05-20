from __future__ import annotations

from ai_configuration.factory.base import AIClient


class CohereClient(AIClient):
    """Cohere chat client."""

    def __init__(self, api_key: str, model: str, max_tokens: int) -> None:
        super().__init__(api_key=api_key, model=model, max_tokens=max_tokens)
        from cohere import AsyncClientV2

        self._client = AsyncClientV2(api_key=api_key)

    async def chat(self, messages: list[dict[str, str]]) -> str:
        """Send messages and return the assistant reply."""
        response = await self._client.chat(
            model=self._model,
            messages=messages,
            max_tokens=self._max_tokens,
        )
        return response.message.content[0].text
