from __future__ import annotations

from abc import ABC, abstractmethod


class AIClient(ABC):
    """Common interface every provider client must implement."""

    @abstractmethod
    async def chat(self, messages: list[dict[str, str]], max_tokens: int) -> str:
        """Send a list of chat messages and return the assistant reply as a string."""
        ...
