from __future__ import annotations

import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from chatbot.constants import AI_ERROR, NO_AI_CONFIG
from chatbot.v1.dependencies import get_ws_user_id
from chatbot.v1.schema import ErrorMessage, OutgoingMessage
from chatbot.v1.services import ChatService
from config.database import get_db

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

    db: AsyncSession = await anext(get_db())
    try:
        user_id = await get_ws_user_id(websocket, db)
    except ValueError:
        return

    service = ChatService(db=db, user_id=user_id)
    try:
        await service.initialize()
    except Exception:
        await websocket.send_text(ErrorMessage(error=NO_AI_CONFIG).model_dump_json())
        await websocket.close()
        return

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            content = data.get("content", "").strip()
            if not content:
                continue

            try:
                reply = await service.send(content)
                await websocket.send_text(
                    OutgoingMessage(role="assistant", content=reply).model_dump_json()
                )
            except Exception:
                await websocket.send_text(
                    ErrorMessage(error=AI_ERROR).model_dump_json()
                )

    except WebSocketDisconnect:
        pass
    finally:
        await db.close()
