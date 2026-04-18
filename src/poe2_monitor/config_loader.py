from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from poe2_monitor.models import SourceChannel
from poe2_monitor.settings import CONFIG_DIR


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_channels() -> list[SourceChannel]:
    data = _load_json(CONFIG_DIR / "channels.json")
    return [SourceChannel(**item) for item in data]


def load_rules() -> dict[str, Any]:
    return _load_json(CONFIG_DIR / "rules.json")
