from __future__ import annotations

from datetime import datetime, timezone

import httpx

from poe2_monitor.models import ContentItem, SourceChannel
from poe2_monitor.sources.base import SourceIngestor


class YouTubeIngestor(SourceIngestor):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"

    async def _resolve_channel_id(self, client: httpx.AsyncClient, channel: SourceChannel) -> str | None:
        handle = channel.channel_id.lstrip("@")
        response = await client.get(
            f"{self.base_url}/channels",
            params={
                "part": "id",
                "forHandle": handle,
                "key": self.api_key,
            },
        )
        response.raise_for_status()
        items = response.json().get("items", [])
        if items:
            return items[0].get("id")

        if channel.channel_id.startswith("UC"):
            return channel.channel_id
        return None

    async def fetch_new_items(self, channel: SourceChannel) -> list[ContentItem]:
        if not self.api_key:
            raise ValueError("youtube api key is missing")

        async with httpx.AsyncClient(timeout=20.0) as client:
            channel_id = await self._resolve_channel_id(client, channel)
            if not channel_id:
                return []

            search_response = await client.get(
                f"{self.base_url}/search",
                params={
                    "part": "snippet",
                    "type": "video",
                    "maxResults": 5,
                    "order": "date",
                    "channelId": channel_id,
                    "key": self.api_key,
                },
            )
            search_response.raise_for_status()
            data = search_response.json()

        items: list[ContentItem] = []
        for entry in data.get("items", []):
            video_id = entry.get("id", {}).get("videoId")
            snippet = entry.get("snippet", {})
            title = snippet.get("title", "")
            if not video_id or not title:
                continue
            published_raw = snippet.get("publishedAt")
            published_at = None
            if published_raw:
                published_at = datetime.fromisoformat(
                    published_raw.replace("Z", "+00:00")
                ).astimezone(timezone.utc)
            items.append(
                ContentItem(
                    source="youtube",
                    external_id=video_id,
                    channel_id=channel.channel_id,
                    title=title,
                    url=f"https://www.youtube.com/watch?v={video_id}",
                    published_at=published_at,
                    description=snippet.get("description", ""),
                    transcript="",
                    language=snippet.get("defaultAudioLanguage")
                    or snippet.get("defaultLanguage")
                    or "unknown",
                    raw_payload=entry,
                )
            )
        return items
