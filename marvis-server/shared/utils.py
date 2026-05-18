from __future__ import annotations

from jose import jwt

from config.settings import settings


def decode_access_token(token: str) -> dict:
    """Decode a JWT access token and return the full payload.

    Raises jose.JWTError if the token is invalid or expired.
    """
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])


def get_user_id_from_token(token: str) -> int:
    """Extract the user ID from a JWT access token.

    Raises jose.JWTError if the token is invalid or expired.
    Raises ValueError if the sub claim is missing.
    """
    payload = decode_access_token(token)
    sub = payload.get("sub")
    if sub is None:
        raise ValueError("Token is missing the sub claim.")
    return int(sub)


def get_username_from_token(token: str) -> str:
    """Extract the username from a JWT access token.

    Raises jose.JWTError if the token is invalid or expired.
    Raises ValueError if the username claim is missing.
    """
    payload = decode_access_token(token)
    username = payload.get("username")
    if username is None:
        raise ValueError("Token is missing the username claim.")
    return str(username)
