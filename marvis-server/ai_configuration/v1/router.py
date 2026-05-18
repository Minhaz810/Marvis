from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ai_configuration.v1.schema import LLMProviderResponse
from ai_configuration.v1.services import AIConfigurationService
from auth.models import User
from auth.v1.dependencies import get_current_user
from config.database import get_db

router = APIRouter()


@router.get("/providers", response_model=list[LLMProviderResponse])
async def list_providers(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[LLMProviderResponse]:
    """Return all available LLM providers."""
    try:
        return await AIConfigurationService(db).get_all_providers()  # type: ignore[return-value]
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching providers.",
        ) from exc
