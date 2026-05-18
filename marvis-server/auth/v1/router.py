from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.v1.dependencies import get_current_user
from auth.v1.schema import (
    LoginRequest,
    RefreshRequest,
    Token,
    UserRegister,
    UserResponse,
)
from auth.v1.services import AuthService
from config.database import get_db

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    payload: UserRegister, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Register a new user account.

    Validates that password and confirm_password match, then creates the user
    with a securely hashed password.
    """
    try:
        return await AuthService(db).register(payload)  # type: ignore[return-value]
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration.",
        ) from exc


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> Token:
    """Authenticate a user and return an access token plus a refresh token."""
    try:
        access_token, refresh_token = await AuthService(db).login(
            payload.username, payload.password
        )
        return Token(access_token=access_token, refresh_token=refresh_token)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login.",
        ) from exc


@router.post("/refresh", response_model=Token)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)) -> Token:
    """Exchange a valid refresh token for a
    new access token and rotated refresh token.
    """
    try:
        access_token, new_refresh_token = await AuthService(db).refresh(
            payload.refresh_token
        )
        return Token(access_token=access_token, refresh_token=new_refresh_token)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during token refresh.",
        ) from exc


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(payload: RefreshRequest, db: AsyncSession = Depends(get_db)) -> None:
    """Revoke the provided refresh token, logging the user out."""
    try:
        await AuthService(db).revoke_refresh_token(payload.refresh_token)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during logout.",
        ) from exc


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Return the profile of the authenticated user."""
    try:
        return current_user  # type: ignore[return-value]
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the user profile.",
        ) from exc
