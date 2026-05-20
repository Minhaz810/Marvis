from __future__ import annotations

from fastapi import HTTPException, status

from ai_configuration.factory.base import AIClient
from ai_configuration.factory.clients.openai_compatible_client import PROVIDER_BASE_URLS
from ai_configuration.v1.schema import UserAIConfigResponse


def get_ai_client(config: UserAIConfigResponse) -> AIClient:
    """Return the appropriate AIClient for the user's saved configuration."""
    provider = config.provider_name
    model = config.model_name
    api_key = config.api_key

    match provider:
        case "OpenAI":
            from ai_configuration.factory.clients.openai_client import OpenAIClient

            return OpenAIClient(api_key=api_key, model=model)

        case "Anthropic":
            from ai_configuration.factory.clients.anthropic_client import (
                AnthropicClient,
            )

            return AnthropicClient(api_key=api_key, model=model)

        case "Google":
            from ai_configuration.factory.clients.google_client import GoogleClient

            return GoogleClient(api_key=api_key, model=model)

        case "Mistral AI":
            from ai_configuration.factory.clients.mistral_client import MistralClient

            return MistralClient(api_key=api_key, model=model)

        case "Cohere":
            from ai_configuration.factory.clients.cohere_client import CohereClient

            return CohereClient(api_key=api_key, model=model)

        case "AI21 Labs":
            from ai_configuration.factory.clients.ai21_client import AI21Client

            return AI21Client(api_key=api_key, model=model)

        case "Amazon Bedrock":
            from ai_configuration.factory.clients.bedrock_client import BedrockClient

            return BedrockClient(api_key=api_key, model=model)

        case "Azure OpenAI":
            from ai_configuration.factory.clients.azure_openai_client import (
                AzureOpenAIClient,
            )

            return AzureOpenAIClient(api_key=api_key, model=model)

        case "Groq":
            from ai_configuration.factory.clients.groq_client import GroqClient

            return GroqClient(api_key=api_key, model=model)

        case "Replicate":
            from ai_configuration.factory.clients.replicate_client import (
                ReplicateClient,
            )

            return ReplicateClient(api_key=api_key, model=model)

        case "Aleph Alpha":
            from ai_configuration.factory.clients.aleph_alpha_client import (
                AlephAlphaClient,
            )

            return AlephAlphaClient(api_key=api_key, model=model)

        case "Writer":
            from ai_configuration.factory.clients.writer_client import WriterClient

            return WriterClient(api_key=api_key, model=model)

        case "Cerebras":
            from ai_configuration.factory.clients.cerebras_client import CerebrasClient

            return CerebrasClient(api_key=api_key, model=model)

        case "Hugging Face":
            from ai_configuration.factory.clients.huggingface_client import (
                HuggingFaceClient,
            )

            return HuggingFaceClient(api_key=api_key, model=model)

        case "Ollama":
            from ai_configuration.factory.clients.ollama_client import OllamaClient

            return OllamaClient(api_key=api_key, model=model)

        case _ if provider in PROVIDER_BASE_URLS:
            from ai_configuration.factory.clients.openai_compatible_client import (
                OpenAICompatibleClient,
            )

            return OpenAICompatibleClient(
                api_key=api_key,
                model=model,
                base_url=PROVIDER_BASE_URLS[provider],
            )

        case _:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Unsupported provider: {provider}",
            )
