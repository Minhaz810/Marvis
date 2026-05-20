from __future__ import annotations

from ai_configuration.factory.base import AIClient


class AzureOpenAIClient(AIClient):
    """Azure OpenAI client.

    api_key is expected as "API_KEY:ENDPOINT[:API_VERSION]"
    e.g. "sk-xxx:https://my-resource.openai.azure.com/:2024-02-01"
    """

    def __init__(self, api_key: str, model: str) -> None:
        from openai import AsyncAzureOpenAI

        parts = api_key.split(":", 2)
        key = parts[0]
        endpoint = parts[1] if len(parts) > 1 else ""
        api_version = parts[2] if len(parts) > 2 else "2024-02-01"
        self._client = AsyncAzureOpenAI(
            api_key=key,
            azure_endpoint=endpoint,
            api_version=api_version,
        )
        self._model = model

    async def chat(self, messages: list[dict[str, str]], max_tokens: int) -> str:
        """Send messages and return the assistant reply."""
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
