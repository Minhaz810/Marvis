from __future__ import annotations

from ai_configuration.factory.base import AIClient


class ReplicateClient(AIClient):
    """Replicate chat client."""

    def __init__(self, api_key: str, model: str, max_tokens: int) -> None:
        super().__init__(api_key=api_key, model=model, max_tokens=max_tokens)
        import replicate

        self._replicate = replicate

    async def chat(self, messages: list[dict[str, str]]) -> str:
        """Send messages and return the assistant reply."""
        import os

        os.environ["REPLICATE_API_TOKEN"] = self._api_key

        prompt = (
            "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in messages)
            + "\nAssistant:"
        )

        output = await self._replicate.async_run(
            self._model,
            input={"prompt": prompt, "max_new_tokens": self._max_tokens},
        )
        if isinstance(output, list):
            return "".join(str(t) for t in output)
        return str(output)
