from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ai_configuration.models import ModelType
from ai_configuration.v1.schema import (
    LLMModelResponse,
    LLMProviderResponse,
    UserAIConfigCreate,
    UserAIConfigResponse,
)
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


@router.get("/providers/by-type", response_model=list[LLMProviderResponse])
async def list_providers_by_type(
    model_type: ModelType = Query(..., description="Filter by type: local or cloud"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[LLMProviderResponse]:
    """Return all LLM providers filtered by model type."""
    try:
        return await AIConfigurationService(db).get_providers_by_type(model_type)  # type: ignore[return-value]
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching providers by type.",
        ) from exc


@router.get("/providers/{provider_name}/models", response_model=list[LLMModelResponse])
async def list_models_by_provider(
    provider_name: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[LLMModelResponse]:
    """Return all models for the given provider."""
    try:
        return await AIConfigurationService(db).get_models_by_provider(provider_name)  # type: ignore[return-value]
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching models.",
        ) from exc


@router.post(
    "/config", response_model=UserAIConfigResponse, status_code=status.HTTP_201_CREATED
)
async def save_user_config(
    payload: UserAIConfigCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserAIConfigResponse:
    """Create or update the AI configuration for the authenticated user."""
    try:
        return await AIConfigurationService(db).save_user_config(
            current_user.id, payload
        )  # type: ignore[return-value]
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while saving configuration.",
        ) from exc


@router.get("/config", response_model=UserAIConfigResponse)
async def get_user_config(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserAIConfigResponse:
    """Return the AI configuration for the authenticated user."""
    try:
        return await AIConfigurationService(db).get_user_config(current_user.id)  # type: ignore[return-value]
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching configuration.",
        ) from exc
