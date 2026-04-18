from __future__ import annotations

import sqlite3
from pathlib import Path

from poe2_monitor.models import AnalysisResult, ContentItem


SCHEMA = """
CREATE TABLE IF NOT EXISTS content_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    external_id TEXT NOT NULL,
    channel_id TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    published_at TEXT,
    language TEXT,
    status TEXT NOT NULL DEFAULT 'discovered',
    UNIQUE(source, external_id)
);

CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_item_id INTEGER NOT NULL,
    accepted INTEGER NOT NULL,
    content_type TEXT NOT NULL,
    mechanic TEXT NOT NULL,
    summary TEXT NOT NULL,
    todo_json TEXT NOT NULL,
    requirements_json TEXT NOT NULL,
    risks_json TEXT NOT NULL,
    confidence REAL NOT NULL,
    language TEXT NOT NULL,
    rationale TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(content_item_id) REFERENCES content_items(id)
);
"""


class Storage:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def init_db(self) -> None:
        with self.connect() as conn:
            conn.executescript(SCHEMA)
            conn.commit()

    def upsert_content(self, item: ContentItem) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO content_items
                (source, external_id, channel_id, title, url, published_at, language)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.source,
                    item.external_id,
                    item.channel_id,
                    item.title,
                    item.url,
                    item.published_at.isoformat() if item.published_at else None,
                    item.language,
                ),
            )
            conn.commit()

    def save_analysis(
        self, item: ContentItem, analysis: AnalysisResult, todo_json: str, requirements_json: str, risks_json: str
    ) -> None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT id FROM content_items WHERE source = ? AND external_id = ?",
                (item.source, item.external_id),
            ).fetchone()
            if row is None:
                raise ValueError("content item must exist before analysis is saved")
            conn.execute(
                """
                INSERT INTO analyses
                (content_item_id, accepted, content_type, mechanic, summary, todo_json,
                 requirements_json, risks_json, confidence, language, rationale)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row[0],
                    int(analysis.accepted),
                    analysis.content_type,
                    analysis.mechanic,
                    analysis.summary,
                    todo_json,
                    requirements_json,
                    risks_json,
                    analysis.confidence,
                    analysis.language,
                    analysis.rationale,
                ),
            )
            conn.commit()
