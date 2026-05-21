from __future__ import annotations

from abc import ABC, abstractmethod


class AIClient(ABC):
    """Common interface every provider client must implement."""

    def __init__(self, api_key: str, model: str, max_tokens: int) -> None:
        """Initialise with credentials and the token budget for every request."""
        self._api_key = api_key.strip()
        self._model = model.strip()
        self._max_tokens = max_tokens

    @abstractmethod
    async def chat(self, messages: list[dict[str, str]]) -> str:
        """Send a list of chat messages and return the assistant reply as a string."""
        ...
