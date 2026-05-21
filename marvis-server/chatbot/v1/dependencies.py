from __future__ import annotations

from fastapi import WebSocket
from jose import JWTError, jwt
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from auth.v1.services import AuthService
from chatbot.constants import INVALID_TOKEN
from config.settings import settings


async def get_ws_user_id(websocket: WebSocket, db: AsyncSession) -> int:
    """Extract and validate the JWT passed as a query parameter.

    Returns the authenticated user's ID or closes the WebSocket with a
    4001 code if the token is missing or invalid.
    """
    token = websocket.query_params.get("token")
    if not token:
        logger.warning("WebSocket connection rejected — no token provided")
        await websocket.close(code=4001, reason=INVALID_TOKEN)
        raise ValueError(INVALID_TOKEN)

    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise ValueError
    except (JWTError, ValueError) as err:
        logger.warning("WebSocket connection rejected — invalid token: {}", err)
        await websocket.close(code=4001, reason=INVALID_TOKEN)
        raise ValueError(INVALID_TOKEN) from err

    user = await AuthService(db).get_user_by_id(int(user_id))
    logger.debug("Token validated — user_id={}", user.id)
    return user.id
