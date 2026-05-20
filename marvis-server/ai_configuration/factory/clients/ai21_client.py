from __future__ import annotations

from ai_configuration.factory.base import AIClient


class AI21Client(AIClient):
    """AI21 Labs chat client."""

    def __init__(self, api_key: str, model: str) -> None:
        from ai21 import AsyncAI21Client

        self._client = AsyncAI21Client(api_key=api_key)
        self._model = model

    async def chat(self, messages: list[dict[str, str]], max_tokens: int) -> str:
        """Send messages and return the assistant reply."""
        from ai21.models.chat import ChatMessage

        chat_messages = [
            ChatMessage(role=m["role"], content=m["content"]) for m in messages
        ]
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=chat_messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
