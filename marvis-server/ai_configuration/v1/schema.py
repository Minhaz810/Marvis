from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from ai_configuration.models import ModelType


class LLMProviderResponse(BaseModel):
    """Schema for LLM provider data returned in API responses."""

    id: int
    provider_name: str
    model_type: ModelType
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
