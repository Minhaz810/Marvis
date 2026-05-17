from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

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
    return await AuthService(db).register(payload)  # type: ignore[return-value]


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> Token:
    """Authenticate a user and return an access token plus a refresh token."""
    access_token, refresh_token = await AuthService(db).login(
        payload.username, payload.password
    )
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)) -> Token:
    """Exchange a valid refresh token for a
    new access token and rotated refresh token.
    """
    access_token, new_refresh_token = await AuthService(db).refresh(
        payload.refresh_token
    )
    return Token(access_token=access_token, refresh_token=new_refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(payload: RefreshRequest, db: AsyncSession = Depends(get_db)) -> None:
    """Revoke the provided refresh token, logging the user out."""
    await AuthService(db).revoke_refresh_token(payload.refresh_token)


@router.get("/me/{user_id}", response_model=UserResponse)
async def get_me(user_id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    """Return the profile of the authenticated user."""
    return await AuthService(db).get_by_id(user_id)  # type: ignore[return-value]
