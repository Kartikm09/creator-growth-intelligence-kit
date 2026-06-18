"""CLI for creator growth intelligence."""

from __future__ import annotations

import argparse

from .analyzer import analyze_rows, dumps_json, load_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze creator content outliers.")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("analyze")
    analyze.add_argument("csv_path")
    analyze.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    briefs = analyze_rows(load_csv(args.csv_path))
    if args.format == "json":
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


if __name__ == "__main__":
    main()

