"""Analyze social content outliers and create next-topic briefs."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from statistics import mean
from typing import Any


@dataclass(frozen=True)
class VideoRow:
    platform: str
    creator: str
    title: str
    topic: str
    hook: str
    format: str
    language: str
    views: int
    followers: int
    likes: int
    comments: int


@dataclass(frozen=True)
class GrowthBrief:
    title: str
    topic: str
    format: str
    outlier_score: float
    engagement_rate: float
    reason: str
    next_topic: str
    localization_plan: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_csv(path: str | Path) -> list[VideoRow]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        return [
            VideoRow(
                platform=row.get("platform", ""),
                creator=row.get("creator", ""),
                title=row.get("title", ""),
                topic=row.get("topic", ""),
                hook=row.get("hook", ""),
                format=row.get("format", ""),
                language=row.get("language", "English"),
                views=int(row.get("views") or 0),
                followers=max(1, int(row.get("followers") or 1)),
                likes=int(row.get("likes") or 0),
                comments=int(row.get("comments") or 0),
            )
            for row in rows
        ]


def analyze_rows(rows: list[VideoRow]) -> list[GrowthBrief]:
    if not rows:
        return []
    average_view_ratio = mean(row.views / row.followers for row in rows)
    briefs = [_brief_for(row, average_view_ratio) for row in rows]
    return sorted(briefs, key=lambda item: (item.outlier_score, item.engagement_rate), reverse=True)


def dumps_json(briefs: list[GrowthBrief]) -> str:
    return json.dumps([brief.to_dict() for brief in briefs], indent=2)


def _brief_for(row: VideoRow, average_view_ratio: float) -> GrowthBrief:
    view_ratio = row.views / row.followers
    outlier_score = round(view_ratio / max(0.01, average_view_ratio), 2)
    engagement_rate = round((row.likes + row.comments * 2) / max(1, row.views), 4)
    reason_bits = []
    if view_ratio >= average_view_ratio * 1.5:
        reason_bits.append("views strongly over-indexed against follower count")
    if engagement_rate >= 0.05:
        reason_bits.append("engagement quality is high")
    if "how" in row.hook.lower() or "why" in row.hook.lower():
        reason_bits.append("curiosity hook is explicit")
    if not reason_bits:
        reason_bits.append("use as baseline, not a viral pattern")
    next_topic = f"{row.topic}: {row.hook} for a more specific audience"
    localization = (
        f"Rewrite hook in Hindi and German while keeping the {row.format} format.",
        "Create one 30-second short, one LinkedIn post, and one carousel outline.",
        "Keep claim/source notes attached before publishing.",
    )
    return GrowthBrief(
        title=row.title,
        topic=row.topic,
        format=row.format,
        outlier_score=outlier_score,
        engagement_rate=engagement_rate,
        reason="; ".join(reason_bits),
        next_topic=next_topic,
        localization_plan=localization,
    )

