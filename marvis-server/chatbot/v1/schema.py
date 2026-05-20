from __future__ import annotations

from pydantic import BaseModel


class IncomingMessage(BaseModel):
    """Message sent by the user over the WebSocket."""

    content: str


class OutgoingMessage(BaseModel):
    """Message sent back to the user over the WebSocket."""

    role: str
    content: str


class ErrorMessage(BaseModel):
    """Error payload sent when something goes wrong."""

    error: str
