"""CLI for creator growth intelligence."""

from __future__ import annotations

import argparse
import json

from .analyzer import analyze_rows, dumps_json, load_csv
from .llm import LLMConfigurationError, LLMRequestError, generate_text


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze creator content outliers.")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("analyze")
    analyze.add_argument("csv_path")
    analyze.add_argument("--format", choices=["text", "json"], default="text")
    analyze.add_argument("--llm", action="store_true", help="Add optional Kimi/ZenMux content sprint.")
    args = parser.parse_args()

    briefs = analyze_rows(load_csv(args.csv_path))
    llm_analysis = _optional_llm_analysis(args.llm, briefs)
    if args.format == "json":
        if llm_analysis:
            print(json.dumps({"briefs": [brief.to_dict() for brief in briefs], "llm_analysis": llm_analysis}, indent=2))
        else:
            print(dumps_json(briefs))
        return

    print("Creator Growth Intelligence Kit")
    for index, brief in enumerate(briefs[:5], start=1):
        print(f"\n{index}. {brief.title}")
        print(f"Outlier: {brief.outlier_score}x | Engagement: {brief.engagement_rate:.2%}")
        print(f"Reason: {brief.reason}")
        print(f"Next: {brief.next_topic}")
        print("Localization:")
        for item in brief.localization_plan:
            print(f"- {item}")
    if llm_analysis:
        print("\nKimi Creator Sprint")
        print(llm_analysis)


def _optional_llm_analysis(enabled: bool, briefs: list[object]) -> str | None:
    if not enabled:
        return None
    prompt = (
        "Turn these deterministic creator analytics briefs into a practical 7-day creator growth sprint. "
        "Keep the plan platform-safe, based on public metrics, and suitable for a freelancer portfolio demo.\n\n"
        f"TOP BRIEFS:\n{json.dumps([brief.to_dict() for brief in briefs[:5]], indent=2)}\n\n"
        "Return: 1) winning pattern summary, 2) 7-day publishing plan, "
        "3) five hook rewrites, 4) multilingual repurpose plan, 5) measurement checklist. "
        "Keep the full answer under 350 words with compact bullets."
    )
    try:
        return generate_text(
            prompt,
            system="You are a creator-growth analyst who turns metrics into safe content experiments.",
            max_tokens=6000,
        )
    except (LLMConfigurationError, LLMRequestError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
