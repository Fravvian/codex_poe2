from __future__ import annotations

import json

from poe2_monitor.analysis import Analyzer
from poe2_monitor.config_loader import load_channels, load_rules
from poe2_monitor.filters import passes_profit_filter
from poe2_monitor.settings import load_settings
from poe2_monitor.sources.youtube import YouTubeIngestor
from poe2_monitor.storage import Storage
from poe2_monitor.telegram_bot import TelegramSender, format_alert


class Pipeline:
    def __init__(self) -> None:
        self.settings = load_settings()
        self.rules = load_rules()
        self.channels = load_channels()
        self.storage = Storage(self.settings.database_path)
        self.youtube = YouTubeIngestor(api_key=self.settings.youtube_api_key)
        self.analyzer = Analyzer(self.rules, api_key=self.settings.openai_api_key)
        self.telegram = TelegramSender(
            token=self.settings.telegram_bot_token,
            chat_id=self.settings.telegram_chat_id,
        )

    async def run_once(self) -> None:
        for channel in self.channels:
            if not channel.enabled or channel.source != "youtube":
                continue

            items = await self.youtube.fetch_new_items(channel)
            for item in items:
                self.storage.upsert_content(item)
                analysis = await self.analyzer.analyze(item)
                self.storage.save_analysis(
                    item=item,
                    analysis=analysis,
                    todo_json=json.dumps(analysis.todo, ensure_ascii=False),
                    requirements_json=json.dumps(analysis.requirements, ensure_ascii=False),
                    risks_json=json.dumps(analysis.risks, ensure_ascii=False),
                )
                if passes_profit_filter(analysis, self.settings.confidence_threshold):
                    await self.telegram.send_alert(format_alert(item, analysis))
