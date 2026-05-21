from __future__ import annotations

import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger

from chatbot.constants import AI_ERROR, NO_AI_CONFIG
from chatbot.v1.dependencies import get_ws_user_id
from chatbot.v1.schema import ErrorMessage, OutgoingMessage
from chatbot.v1.services import ChatService
from config.database import AsyncSessionLocal

router = APIRouter()


@router.websocket("/ws")
async def chat_websocket(websocket: WebSocket) -> None:
    """WebSocket endpoint for real-time chat between the user and the AI client.

    Connect with:  ws://<host>/api/v1/chatbot/ws?token=<jwt>

    Incoming frames:  JSON  {"content": "Hello!"}
    Outgoing frames:  JSON  {"role": "assistant", "content": "..."}
                      JSON  {"error": "..."}  on failure
    """
    await websocket.accept()
    logger.info("WebSocket connection accepted from {}", websocket.client)

    async with AsyncSessionLocal() as db:
        try:
            user_id = await get_ws_user_id(websocket, db)
        except ValueError:
            logger.warning("WebSocket auth failed for client {}", websocket.client)
            return

        logger.info("WebSocket authenticated — user_id={}", user_id)

        service = ChatService(db=db, user_id=user_id)
        try:
            await service.initialize()
            logger.info("ChatService initialized for user_id={}", user_id)
        except Exception:
            logger.exception("Failed to initialize ChatService for user_id={}", user_id)
            await websocket.send_text(
                ErrorMessage(error=NO_AI_CONFIG).model_dump_json()
            )
            await websocket.close()
            return

        try:
            while True:
                raw = await websocket.receive_text()
                logger.debug("Received frame from user_id={}: {!r}", user_id, raw)

                try:
                    data = json.loads(raw)
                except json.JSONDecodeError:
                    logger.warning(
                        "Invalid JSON frame from user_id={}: {!r}", user_id, raw
                    )
                    continue

                content = data.get("content", "").strip()
                if not content:
                    continue

                try:
                    reply = await service.send(content)
                    logger.debug("Reply for user_id={}: {!r}", user_id, reply)
                    await websocket.send_text(
                        OutgoingMessage(
                            role="assistant", content=reply
                        ).model_dump_json()
                    )
                except Exception:
                    logger.exception(
                        "AI call failed for user_id={} — message: {!r}",
                        user_id,
                        content,
                    )
                    await websocket.send_text(
                        ErrorMessage(error=AI_ERROR).model_dump_json()
                    )

        except WebSocketDisconnect:
            logger.info("WebSocket disconnected — user_id={}", user_id)
