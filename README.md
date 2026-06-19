# Creator Growth Intelligence Kit

Portfolio-safe toolkit for analyzing creator/content performance and turning viral outliers into next-topic briefs.

The repo works from CSV exports or manually collected public metrics. It does not scrape private accounts or automate platform actions. It helps answer: why did this small account get big views, and what content should be tested next?

## Quick Start

```bash
PYTHONPATH=src python3 -m creator_growth.cli analyze examples/videos.csv
```

JSON output:

```bash
PYTHONPATH=src python3 -m creator_growth.cli analyze examples/videos.csv --format json
```

Optional live Kimi/ZenMux creator sprint:

```bash
export ZENMUX_API_KEY="your_api_key_here"
export ZENMUX_MODEL="moonshotai/kimi-k2.7-code-free"
PYTHONPATH=src python3 -m creator_growth.cli analyze examples/videos.csv --llm
```

The API key is read from the environment and should never be committed. Without `--llm`, the repo runs fully offline.

Run tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Output

- viral outlier score
- engagement quality score
- repeated hooks and formats
- next-topic recommendations
- multilingual repurpose plan
- review notes for human content planning
- optional Kimi/ZenMux 7-day content sprint when `--llm` is enabled

## Portfolio Signal

This repo supports work around:

- social media automation
- viral content research
- creator analytics
- AI content operations
- multilingual content growth
- Python data tooling
