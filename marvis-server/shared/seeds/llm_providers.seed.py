from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ai_configuration.models import LLMProvider, ModelType

PROVIDERS: list[dict] = [
    # ── Cloud ────────────────────────────────────────────────────────────────
    {"provider_name": "OpenAI", "model_type": ModelType.cloud},
    {"provider_name": "Anthropic", "model_type": ModelType.cloud},
    {"provider_name": "Google", "model_type": ModelType.cloud},
    {"provider_name": "Mistral AI", "model_type": ModelType.cloud},
    {"provider_name": "Cohere", "model_type": ModelType.cloud},
    {"provider_name": "AI21 Labs", "model_type": ModelType.cloud},
    {"provider_name": "Amazon Bedrock", "model_type": ModelType.cloud},
    {"provider_name": "Azure OpenAI", "model_type": ModelType.cloud},
    {"provider_name": "Groq", "model_type": ModelType.cloud},
    {"provider_name": "Together AI", "model_type": ModelType.cloud},
    {"provider_name": "Perplexity AI", "model_type": ModelType.cloud},
    {"provider_name": "xAI", "model_type": ModelType.cloud},
    {"provider_name": "DeepSeek", "model_type": ModelType.cloud},
    {"provider_name": "Fireworks AI", "model_type": ModelType.cloud},
    {"provider_name": "Replicate", "model_type": ModelType.cloud},
    {"provider_name": "Aleph Alpha", "model_type": ModelType.cloud},
    {"provider_name": "Writer", "model_type": ModelType.cloud},
    {"provider_name": "Cerebras", "model_type": ModelType.cloud},
    {"provider_name": "SambaNova", "model_type": ModelType.cloud},
    {"provider_name": "Hugging Face", "model_type": ModelType.cloud},
    # ── Local ────────────────────────────────────────────────────────────────
    {"provider_name": "Ollama", "model_type": ModelType.local},
    {"provider_name": "LM Studio", "model_type": ModelType.local},
    {"provider_name": "LocalAI", "model_type": ModelType.local},
    {"provider_name": "GPT4All", "model_type": ModelType.local},
    {"provider_name": "llama.cpp", "model_type": ModelType.local},
    {"provider_name": "vLLM", "model_type": ModelType.local},
    {"provider_name": "Jan", "model_type": ModelType.local},
    {"provider_name": "KoboldCpp", "model_type": ModelType.local},
    {"provider_name": "llamafile", "model_type": ModelType.local},
    {"provider_name": "Text Generation WebUI", "model_type": ModelType.local},
]


async def seed_llm_providers(db: AsyncSession) -> None:
    """Insert LLM providers if they do not already exist."""
    for data in PROVIDERS:
        result = await db.execute(
            select(LLMProvider).where(
                LLMProvider.provider_name == data["provider_name"]
            )
        )
        if result.scalar_one_or_none() is None:
            db.add(LLMProvider(**data))
    await db.commit()
