from __future__ import annotations

import httpx

from poe2_monitor.models import AnalysisResult, ContentItem


def format_alert(item: ContentItem, analysis: AnalysisResult) -> str:
    todo_text = "; ".join(analysis.todo) if analysis.todo else "-"
    requirements_text = "; ".join(analysis.requirements) if analysis.requirements else "-"
    risks_text = "; ".join(analysis.risks) if analysis.risks else "-"
    return "\n".join(
        [
            f"Тип: {analysis.content_type}",
            f"Механика: {analysis.mechanic}",
            f"Содержание: {analysis.summary}",
            f"To-do: {todo_text}",
            f"Требования: {requirements_text}",
            f"Риски: {risks_text}",
            f"Источник: {item.url}",
        ]
    )


class TelegramSender:
    def __init__(self, token: str, chat_id: str) -> None:
        self.token = token
        self.chat_id = chat_id

    async def send_alert(self, text: str) -> None:
        if not self.token or not self.chat_id:
            raise ValueError("telegram credentials are missing")
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "disable_web_page_preview": True,
                },
            )
            response.raise_for_status()
