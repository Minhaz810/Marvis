from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ai_configuration.constants import (
    API_KEY_REQUIRED,
    MODEL_NOT_FOUND,
    PROVIDER_NOT_FOUND,
    USER_CONFIG_NOT_FOUND,
)
from ai_configuration.factory import get_ai_client
from ai_configuration.factory.base import AIClient
from ai_configuration.models import LLMModel, LLMProvider, ModelType, UserAIConfig
from ai_configuration.v1.schema import UserAIConfigCreate, UserAIConfigResponse


class AIConfigurationService:
    """Service layer handling all AI configuration business logic."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialise with an async database session."""
        self.db = db

    async def get_all_providers(self) -> list[LLMProvider]:
        """Return all available LLM providers."""
        result = await self.db.execute(
            select(LLMProvider).order_by(LLMProvider.provider_name)
        )
        return list(result.scalars().all())

    async def get_providers_by_type(self, model_type: ModelType) -> list[LLMProvider]:
        """Return all LLM providers filtered by model type (local or cloud)."""
        result = await self.db.execute(
            select(LLMProvider)
            .where(LLMProvider.model_type == model_type)
            .order_by(LLMProvider.provider_name)
        )
        return list(result.scalars().all())

    async def get_models_by_provider(self, provider_name: str) -> list[LLMModel]:
        """Return all models for the given provider name.

        Raises HTTP 404 if the provider does not exist.
        """
        result = await self.db.execute(
            select(LLMProvider).where(LLMProvider.provider_name == provider_name)
        )
        provider = result.scalar_one_or_none()
        if not provider:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=PROVIDER_NOT_FOUND
            )
        models_result = await self.db.execute(
            select(LLMModel)
            .where(LLMModel.provider_id == provider.id)
            .order_by(LLMModel.model_name)
        )
        return list(models_result.scalars().all())

    async def _enrich_config(self, config: UserAIConfig) -> dict:
        """Attach model_name, provider_name, and model_type to a config dict."""
        model_result = await self.db.execute(
            select(LLMModel).where(LLMModel.id == config.llm_model_id)
        )
        model = model_result.scalar_one()
        provider_result = await self.db.execute(
            select(LLMProvider).where(LLMProvider.id == model.provider_id)
        )
        provider = provider_result.scalar_one()
        return {
            "id": config.id,
            "llm_model_id": config.llm_model_id,
            "user_id": config.user_id,
            "api_key": config.api_key,
            "max_tokens": config.max_tokens,
            "is_active": config.is_active,
            "model_name": model.model_name,
            "provider_name": provider.provider_name,
            "model_type": provider.model_type,
            "created_at": config.created_at,
            "updated_at": config.updated_at,
        }

    async def save_user_config(self, user_id: int, payload: UserAIConfigCreate) -> dict:
        """Create or update the AI configuration for a user.

        Validates that the model exists and that an API key is provided
        for cloud models. If the user already has a config, it is updated
        in place.
        """
        model_result = await self.db.execute(
            select(LLMModel).where(
                LLMModel.id == payload.llm_model_id,
                LLMModel.is_active == True,  # noqa: E712
            )
        )
        model = model_result.scalar_one_or_none()
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=MODEL_NOT_FOUND
            )

        provider_result = await self.db.execute(
            select(LLMProvider).where(LLMProvider.id == model.provider_id)
        )
        provider = provider_result.scalar_one_or_none()
        if (
            provider
            and provider.model_type == ModelType.cloud
            and not payload.api_key.strip()
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=API_KEY_REQUIRED,
            )

        existing_result = await self.db.execute(
            select(UserAIConfig).where(UserAIConfig.user_id == user_id)
        )
        existing = existing_result.scalar_one_or_none()

        if existing:
            existing.llm_model_id = payload.llm_model_id
            existing.api_key = payload.api_key
            existing.max_tokens = payload.max_tokens
            await self.db.commit()
            await self.db.refresh(existing)
            return await self._enrich_config(existing)

        config = UserAIConfig(
            user_id=user_id,
            llm_model_id=payload.llm_model_id,
            api_key=payload.api_key,
            max_tokens=payload.max_tokens,
            is_active=True,
        )
        self.db.add(config)
        await self.db.commit()
        await self.db.refresh(config)
        return await self._enrich_config(config)

    async def get_user_config(self, user_id: int) -> dict:
        """Return the AI configuration for a user.

        Raises HTTP 404 if no configuration exists.
        """
        result = await self.db.execute(
            select(UserAIConfig).where(UserAIConfig.user_id == user_id)
        )
        config = result.scalar_one_or_none()
        if not config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=USER_CONFIG_NOT_FOUND
            )
        return await self._enrich_config(config)

    async def get_ai_client_for_user(self, user_id: int) -> AIClient:
        """Return a ready-to-use AI client for the given user.

        Fetches the user's saved configuration from the database and builds
        the appropriate provider client via the factory. The client already
        has max_tokens embedded, so callers only need to supply messages.
        """
        config_dict = await self.get_user_config(user_id)
        config = UserAIConfigResponse.model_validate(config_dict)
        return get_ai_client(config)
