from __future__ import annotations

from ai_configuration.factory.base import AIClient


class MistralClient(AIClient):
    """Mistral AI chat client."""

    def __init__(self, api_key: str, model: str, max_tokens: int) -> None:
        super().__init__(api_key=api_key, model=model, max_tokens=max_tokens)
        from mistralai import Mistral

        self._client = Mistral(api_key=api_key)

    async def chat(self, messages: list[dict[str, str]]) -> str:
        """Send messages and return the assistant reply."""
        response = await self._client.chat.complete_async(
            model=self._model,
            messages=messages,
            max_tokens=self._max_tokens,
        )
        return response.choices[0].message.content or ""
