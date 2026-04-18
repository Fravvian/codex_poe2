from __future__ import annotations

from poe2_monitor.models import ContentItem, SourceChannel
from poe2_monitor.sources.base import SourceIngestor


class RedditIngestor(SourceIngestor):
    async def fetch_new_items(self, channel: SourceChannel) -> list[ContentItem]:
        """Reserved for a future Reddit integration."""
        return []
