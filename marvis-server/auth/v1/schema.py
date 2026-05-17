from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, model_validator

from auth.constants import PASSWORDS_DO_NOT_MATCH


class UserRegister(BaseModel):
    """Schema for user registration request."""

    username: str
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_must_match(self) -> UserRegister:
        """Validate that password and confirm_password are identical."""
        if self.password != self.confirm_password:
            raise ValueError(PASSWORDS_DO_NOT_MATCH)
        return self


class UserResponse(BaseModel):
    """Schema for user data returned in API responses."""

    id: int
    username: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    """Schema for login request."""

    username: str
    password: str


class RefreshRequest(BaseModel):
    """Schema for refresh token request."""

    refresh_token: str


class Token(BaseModel):
    """Schema for authentication token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
