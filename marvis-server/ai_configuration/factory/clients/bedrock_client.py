from __future__ import annotations

from ai_configuration.factory.base import AIClient


class BedrockClient(AIClient):
    """Amazon Bedrock client using the Converse API (supports all Nova/Titan models)."""

    def __init__(self, api_key: str, model: str) -> None:
        import boto3

        parts = api_key.split(":")
        access_key = parts[0]
        secret_key = parts[1] if len(parts) > 1 else ""
        region = parts[2] if len(parts) > 2 else "us-east-1"
        self._client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
        self._model = model

    async def chat(self, messages: list[dict[str, str]], max_tokens: int) -> str:
        """Send messages and return the assistant reply."""
        import asyncio

        system_parts = [
            {"text": m["content"]} for m in messages if m["role"] == "system"
        ]
        converse_messages = [
            {"role": m["role"], "content": [{"text": m["content"]}]}
            for m in messages
            if m["role"] != "system"
        ]
        kwargs: dict = {
            "modelId": self._model,
            "messages": converse_messages,
            "inferenceConfig": {"maxTokens": max_tokens},
        }
        if system_parts:
            kwargs["system"] = system_parts

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, lambda: self._client.converse(**kwargs)
        )
        return response["output"]["message"]["content"][0]["text"]
