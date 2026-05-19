from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ai_configuration.constants import PROVIDER_NOT_FOUND
from ai_configuration.models import LLMModel, LLMProvider, ModelType


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
