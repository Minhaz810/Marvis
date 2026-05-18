from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ai_configuration.models import LLMModel, LLMProvider

MODELS_BY_PROVIDER: dict[str, list[str]] = {
    "OpenAI": [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo",
        "o1",
        "o1-mini",
        "o3-mini",
    ],
    "Anthropic": [
        "claude-opus-4-7",
        "claude-sonnet-4-6",
        "claude-haiku-4-5-20251001",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
    ],
    "Google": [
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.0-ultra",
    ],
    "Mistral AI": [
        "mistral-large-latest",
        "mistral-medium-latest",
        "mistral-small-latest",
        "mixtral-8x22b-instruct",
        "mixtral-8x7b-instruct",
        "codestral-latest",
        "mistral-embed",
    ],
    "Cohere": [
        "command-r-plus",
        "command-r",
        "command",
        "command-light",
        "command-nightly",
    ],
    "AI21 Labs": [
        "jamba-1.5-large",
        "jamba-1.5-mini",
        "j2-ultra",
        "j2-mid",
        "j2-light",
    ],
    "Amazon Bedrock": [
        "amazon.nova-pro-v1",
        "amazon.nova-lite-v1",
        "amazon.nova-micro-v1",
        "amazon.titan-text-premier-v1",
        "amazon.titan-text-express-v1",
    ],
    "Azure OpenAI": [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-35-turbo",
    ],
    "Groq": [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-3.2-90b-vision-preview",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
        "deepseek-r1-distill-llama-70b",
    ],
    "Together AI": [
        "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "meta-llama/Llama-3.1-8B-Instruct-Turbo",
        "mistralai/Mixtral-8x22B-Instruct-v0.1",
        "Qwen/Qwen2.5-72B-Instruct-Turbo",
        "deepseek-ai/DeepSeek-R1",
        "google/gemma-2-27b-it",
    ],
    "Perplexity AI": [
        "llama-3.1-sonar-huge-128k-online",
        "llama-3.1-sonar-large-128k-online",
        "llama-3.1-sonar-small-128k-online",
        "llama-3.1-sonar-large-128k-chat",
        "llama-3.1-sonar-small-128k-chat",
    ],
    "xAI": [
        "grok-2-latest",
        "grok-2-vision-latest",
        "grok-beta",
    ],
    "DeepSeek": [
        "deepseek-chat",
        "deepseek-reasoner",
        "deepseek-coder",
    ],
    "Fireworks AI": [
        "accounts/fireworks/models/llama-v3p3-70b-instruct",
        "accounts/fireworks/models/mixtral-8x22b-instruct",
        "accounts/fireworks/models/qwen2p5-72b-instruct",
        "accounts/fireworks/models/deepseek-r1",
    ],
    "Aleph Alpha": [
        "luminous-supreme-control",
        "luminous-supreme",
        "luminous-extended",
        "luminous-base",
    ],
    "Writer": [
        "palmyra-x-004",
        "palmyra-x-003-instruct",
        "palmyra-med",
        "palmyra-fin",
    ],
    "Cerebras": [
        "llama3.3-70b",
        "llama3.1-70b",
        "llama3.1-8b",
        "deepseek-r1-distill-llama-70b",
    ],
    "SambaNova": [
        "Meta-Llama-3.3-70B-Instruct",
        "Meta-Llama-3.1-405B-Instruct",
        "DeepSeek-R1",
        "Qwen2.5-72B-Instruct",
    ],
    "Hugging Face": [
        "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "google/gemma-2-27b-it",
        "Qwen/Qwen2.5-72B-Instruct",
        "microsoft/phi-4",
    ],
    # ── Local models (seeded under Ollama as the canonical local runner) ──────
    "Ollama": [
        "llama3.3",
        "llama3.2",
        "llama3.1:8b",
        "llama3.1:70b",
        "mistral",
        "mixtral:8x7b",
        "mixtral:8x22b",
        "phi4",
        "phi3.5",
        "gemma2:9b",
        "gemma2:27b",
        "qwen2.5:7b",
        "qwen2.5:72b",
        "deepseek-r1:7b",
        "deepseek-r1:14b",
        "deepseek-r1:32b",
        "deepseek-r1:70b",
        "codellama:7b",
        "codellama:13b",
        "codellama:34b",
        "starcoder2:7b",
        "starcoder2:15b",
        "dolphin-phi",
        "neural-chat",
        "orca-mini",
        "wizardcoder:7b",
        "wizardcoder:13b",
        "openchat",
        "vicuna:7b",
        "vicuna:13b",
        "stablelm2",
    ],
}


async def seed_llm_models(db: AsyncSession) -> None:
    """Insert LLM models for each provider if they do not already exist."""
    for provider_name, model_names in MODELS_BY_PROVIDER.items():
        result = await db.execute(
            select(LLMProvider).where(LLMProvider.provider_name == provider_name)
        )
        provider = result.scalar_one_or_none()
        if provider is None:
            continue

        for model_name in model_names:
            exists = await db.execute(
                select(LLMModel).where(
                    LLMModel.provider_id == provider.id,
                    LLMModel.model_name == model_name,
                )
            )
            if exists.scalar_one_or_none() is None:
                db.add(
                    LLMModel(
                        provider_id=provider.id, model_name=model_name, is_active=True
                    )
                )

    await db.commit()
