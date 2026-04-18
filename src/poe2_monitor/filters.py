from __future__ import annotations

from poe2_monitor.models import AnalysisResult


def passes_profit_filter(result: AnalysisResult, confidence_threshold: float) -> bool:
    return (
        result.accepted
        and result.confidence >= confidence_threshold
        and bool(result.todo)
        and bool(result.risks)
    )
