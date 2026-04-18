from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class SourceChannel:
    source: str
    channel_id: str
    enabled: bool = True
    priority: int = 1
    notes: str = ""


@dataclass(slots=True)
class ContentItem:
    source: str
    external_id: str
    channel_id: str
    title: str
    url: str
    published_at: datetime | None = None
    description: str = ""
    transcript: str = ""
    language: str | None = None
    raw_payload: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AnalysisResult:
    accepted: bool
    content_type: str
    mechanic: str
    summary: str
    todo: list[str]
    requirements: list[str]
    risks: list[str]
    confidence: float
    language: str
    rationale: str = ""

