from __future__ import annotations

import json

from openai import AsyncOpenAI
from openai import OpenAIError

from poe2_monitor.models import AnalysisResult, ContentItem


class Analyzer:
    def __init__(self, rules: dict[str, object], api_key: str) -> None:
        self.rules = rules
        self.client = AsyncOpenAI(api_key=api_key) if api_key else None

    def title_passes_prefilter(self, item: ContentItem) -> bool:
        title = item.title.lower()
        title_rules = self.rules.get("title_rules", {})
        exclude_groups = [
            title_rules.get("exclude_build_markers", []),
            title_rules.get("exclude_news_markers", []),
            title_rules.get("exclude_non_profit_markers", []),
        ]
        if any(marker.lower() in title for group in exclude_groups for marker in group):
            return False

        keep_groups = [
            title_rules.get("keep_profit_markers", []),
            title_rules.get("keep_mechanics", []),
            title_rules.get("keep_pattern_markers", []),
            title_rules.get("keep_item_crafting_markers", []),
            title_rules.get("keep_broken_profit_markers", []),
            title_rules.get("priority_number_markers", []),
        ]
        return any(marker.lower() in title for group in keep_groups for marker in group)

    async def analyze(self, item: ContentItem) -> AnalysisResult:
        if not self.title_passes_prefilter(item):
            return AnalysisResult(
                accepted=False,
                content_type="filtered_out",
                mechanic="unknown",
                summary="",
                todo=[],
                requirements=[],
                risks=[],
                confidence=0.0,
                language=item.language or "unknown",
                rationale="Title prefilter rejected the video.",
            )

        if not self.client:
            return AnalysisResult(
                accepted=False,
                content_type="unknown",
                mechanic="unknown",
                summary="",
                todo=[],
                requirements=[],
                risks=[],
                confidence=0.0,
                language=item.language or "unknown",
                rationale="OpenAI integration is not configured.",
            )

        prompt = f"""
You are classifying Path of Exile 2 content for profitable opportunities only.
Reject videos about builds, leveling, bossing, news, generic patch commentary, and non-profit gameplay.

Return JSON with keys:
accepted (bool),
content_type (farm|trading|abuse|craft|other),
mechanic (short string),
summary (string in the source language),
todo (array of strings in the source language),
requirements (array of strings in the source language),
risks (array of strings in the source language),
confidence (0 to 1),
rationale (short string in English).

Video title: {item.title}
Video description: {item.description}
Transcript: {item.transcript[:12000]}
"""
        try:
            response = await self.client.responses.create(
                model="gpt-5-mini",
                input=prompt,
            )
            data = json.loads(response.output_text)
            return AnalysisResult(
                accepted=bool(data["accepted"]),
                content_type=str(data["content_type"]),
                mechanic=str(data["mechanic"]),
                summary=str(data["summary"]),
                todo=[str(x) for x in data.get("todo", [])],
                requirements=[str(x) for x in data.get("requirements", [])],
                risks=[str(x) for x in data.get("risks", [])],
                confidence=float(data["confidence"]),
                language=item.language or "unknown",
                rationale=str(data.get("rationale", "")),
            )
        except (OpenAIError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            return AnalysisResult(
                accepted=False,
                content_type="analysis_unavailable",
                mechanic="unknown",
                summary="",
                todo=[],
                requirements=[],
                risks=[],
                confidence=0.0,
                language=item.language or "unknown",
                rationale=f"Analysis failed: {exc}",
            )
