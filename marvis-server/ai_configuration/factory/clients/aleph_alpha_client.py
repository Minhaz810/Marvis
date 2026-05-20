from __future__ import annotations

import asyncio

from ai_configuration.factory.base import AIClient


class AlephAlphaClient(AIClient):
    """Aleph Alpha client using the completion API (no native chat endpoint)."""

    def __init__(self, api_key: str, model: str) -> None:
        from aleph_alpha_client import Client

        self._client = Client(token=api_key)
        self._model = model

    async def chat(self, messages: list[dict[str, str]], max_tokens: int) -> str:
        """Send messages and return the assistant reply."""
        from aleph_alpha_client import CompletionRequest, Prompt

        prompt_text = (
            "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in messages)
            + "\nAssistant:"
        )

        request = CompletionRequest(
            prompt=Prompt.from_text(prompt_text),
            maximum_tokens=max_tokens,
        )
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, lambda: self._client.complete(request, model=self._model)
        )
        return response.completions[0].completion.strip()
