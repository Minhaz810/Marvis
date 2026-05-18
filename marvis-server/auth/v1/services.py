from __future__ import annotations

from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.constants import (
    INVALID_CREDENTIALS,
    INVALID_REFRESH_TOKEN,
    USERNAME_ALREADY_EXISTS,
    USERNAME_NOT_FOUND,
)
from auth.models import RefreshToken, User
from auth.v1.schema import UserRegister
from auth.v1.utils import (
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_token,
    verify_password,
)
from config.settings import settings


class AuthService:
    """Service layer handling all authentication business logic."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialise with an async database session."""
        self.db = db

    async def get_user_by_id(self, user_id: int) -> User:
        """Return a user by ID, raising HTTP 404 if not found."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=USERNAME_NOT_FOUND
            )
        return user

    async def get_user_by_username(self, username: str) -> User | None:
        """Return a user by username, or None if not found."""
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def register(self, payload: UserRegister) -> User:
        """Register a new user.

        Raises HTTP 409 if the username is already taken.
        Stores only the hashed password — confirm_password is never persisted.
        """
        if await self.get_user_by_username(payload.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=USERNAME_ALREADY_EXISTS
            )
        user = User(
            username=payload.username,
            hashed_password=hash_password(payload.password),
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def login(self, username: str, password: str) -> tuple[str, str]:
        """Authenticate a user and issue both an access token and a refresh token.

        Returns a tuple of (access_token, refresh_token).
        Raises HTTP 401 on invalid credentials.
        """
        user = await self.get_user_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS
            )

        raw_token = generate_refresh_token()
        expires_at = datetime.now(UTC) + timedelta(
            days=settings.refresh_token_expire_days
        )

        self.db.add(
            RefreshToken(
                user_id=user.id,
                token_hash=hash_token(raw_token),
                expires_at=expires_at,
            )
        )
        await self.db.commit()

        access_token = create_access_token(
            {"sub": str(user.id), "username": user.username}
        )
        return access_token, raw_token

    async def refresh(self, raw_token: str) -> tuple[str, str]:
        """Rotate a refresh token and issue a new access token.

        Revokes the provided refresh token and issues a new one (token rotation).
        Raises HTTP 401 if the token is invalid, expired, or already revoked.
        """
        token_hash = hash_token(raw_token)
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.is_revoked == False,  # noqa: E712
                RefreshToken.expires_at > datetime.now(UTC),
            )
        )
        stored = result.scalar_one_or_none()
        if not stored:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_REFRESH_TOKEN
            )

        stored.is_revoked = True

        new_raw = generate_refresh_token()
        new_expires = datetime.now(UTC) + timedelta(
            days=settings.refresh_token_expire_days
        )
        self.db.add(
            RefreshToken(
                user_id=stored.user_id,
                token_hash=hash_token(new_raw),
                expires_at=new_expires,
            )
        )
        await self.db.commit()

        user = await self.get_user_by_id(stored.user_id)
        access_token = create_access_token(
            {"sub": str(user.id), "username": user.username}
        )
        return access_token, new_raw

    async def revoke_refresh_token(self, raw_token: str) -> None:
        """Revoke a refresh token, effectively logging the user out."""
        token_hash = hash_token(raw_token)
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        stored = result.scalar_one_or_none()
        if stored:
            stored.is_revoked = True
            await self.db.commit()
