from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from ai_configuration.v1.services import AIConfigurationService
from chatbot.prompts.system_prompt import SYSTEM_PROMPT


class ChatService:
    """Manages a single user's chat session for the
    duration of a WebSocket connection.
    """

    def __init__(self, db: AsyncSession, user_id: int) -> None:
        """Initialise with a DB session and the authenticated user's ID."""
        self._db = db
        self._user_id = user_id
        self._history: list[dict[str, str]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        self._client = None

    async def initialize(self) -> None:
        """Fetch the user's AI configuration and build the provider client."""
        service = AIConfigurationService(self._db)
        self._client = await service.get_ai_client_for_user(self._user_id)

    async def send(self, content: str) -> str:
        """Append the user message, call the AI client, and return the reply."""
        if self._client is None:
            raise RuntimeError("ChatService not initialized. Call initialize() first.")

        self._history.append({"role": "user", "content": content})
        reply = await self._client.chat(self._history)
        self._history.append({"role": "assistant", "content": reply})
        return reply
