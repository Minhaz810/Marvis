from __future__ import annotations

from ai_configuration.factory.base import AIClient


class ReplicateClient(AIClient):
    """Replicate chat client."""

    def __init__(self, api_key: str, model: str) -> None:
        import replicate

        self._replicate = replicate
        self._api_key = api_key
        self._model = model

    async def chat(self, messages: list[dict[str, str]], max_tokens: int) -> str:
        """Send messages and return the assistant reply."""
        import os

        os.environ["REPLICATE_API_TOKEN"] = self._api_key

        prompt = (
            "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in messages)
            + "\nAssistant:"
        )

        output = await self._replicate.async_run(
            self._model,
            input={"prompt": prompt, "max_new_tokens": max_tokens},
        )
        if isinstance(output, list):
            return "".join(str(t) for t in output)
        return str(output)
