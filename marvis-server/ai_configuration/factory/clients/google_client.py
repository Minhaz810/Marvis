from __future__ import annotations

from ai_configuration.factory.base import AIClient


class GoogleClient(AIClient):
    """Google Gemini chat client."""

    def __init__(self, api_key: str, model: str) -> None:
        from google import genai

        self._client = genai.Client(api_key=api_key)
        self._model = model

    async def chat(self, messages: list[dict[str, str]], max_tokens: int) -> str:
        """Send messages and return the assistant reply."""
        from google.genai import types

        contents = []
        for m in messages:
            role = "model" if m["role"] == "assistant" else "user"
            contents.append(
                types.Content(role=role, parts=[types.Part(text=m["content"])])
            )

        config = types.GenerateContentConfig(max_output_tokens=max_tokens)
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=contents,
            config=config,
        )
        return response.text or ""
