from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ai_configuration.models import LLMProvider


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
