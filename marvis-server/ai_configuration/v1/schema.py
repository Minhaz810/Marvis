from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from ai_configuration.models import ModelType


class LLMProviderResponse(BaseModel):
    """Schema for LLM provider data returned in API responses."""

    id: int
    provider_name: str
    model_type: ModelType
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LLMModelResponse(BaseModel):
    """Schema for LLM model data returned in API responses."""

    id: int
    provider_id: int
    model_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserAIConfigCreate(BaseModel):
    """Schema for creating a user AI configuration."""

    llm_model_id: int
    api_key: str = ""
    max_tokens: int = Field(ge=1, le=32768)


class UserAIConfigUpdate(BaseModel):
    """Schema for updating an existing user AI configuration."""

    llm_model_id: int
    api_key: str = ""
    max_tokens: int = Field(ge=1, le=32768)


class UserAIConfigResponse(BaseModel):
    """Schema for user AI configuration returned in API responses."""

    id: int
    llm_model_id: int
    user_id: int | None
    api_key: str
    max_tokens: int
    is_active: bool
    model_name: str
    provider_name: str
    model_type: ModelType
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
