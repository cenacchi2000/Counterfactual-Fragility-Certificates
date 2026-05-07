#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "precomputed"
OUT = ROOT / "results" / "tables"


def as_markdown_table(csv_name: str, title: str) -> str:
    df = pd.read_csv(DATA / csv_name)
    return f"## {title}\n\n" + df.to_markdown(index=False) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sections = [
        ("score_comparison.csv", "Brittle-case identification"),
        ("attribution_baselines.csv", "Perturbation and attribution-style baselines"),
        ("component_ablation_curated.csv", "Curated component ablation"),
        ("design_stability_curated.csv", "Design stability checks"),
        ("greedy_exact_beam.csv", "Greedy exact/beam diagnostics"),
        ("naturalistic_proxy.csv", "Naturalistic field-unavailability proxy"),
    ]
    report = "# Reproduced Result Tables\n\nGenerated from bundled anonymous review CSV files.\n\n"
    for csv_name, title in sections:
        report += as_markdown_table(csv_name, title) + "\n"
    (OUT / "tables.md").write_text(report)
    print(f"wrote {OUT / 'tables.md'}")


if __name__ == "__main__":
    main()
