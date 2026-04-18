from __future__ import annotations

from abc import ABC, abstractmethod

from poe2_monitor.models import ContentItem, SourceChannel


class SourceIngestor(ABC):
    @abstractmethod
    async def fetch_new_items(self, channel: SourceChannel) -> list[ContentItem]:
        raise NotImplementedError
