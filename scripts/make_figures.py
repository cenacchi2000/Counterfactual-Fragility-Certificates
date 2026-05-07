#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "precomputed"
OUT = ROOT / "results" / "figures"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA / "score_comparison.csv")
    agg = df.dropna(subset=["aggregate_auroc"])
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.bar(agg["score"], agg["aggregate_auroc"].astype(float))
    ax.set_ylabel("Held-out brittle AUROC")
    ax.set_ylim(0, 1.0)
    ax.set_title("CFC-FDS identifies brittle high-confidence cases")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    fig.savefig(OUT / "recreated_score_comparison.png", dpi=220)
    plt.close(fig)

    gd = pd.read_csv(DATA / "greedy_exact_beam.csv")
    gd = gd[gd["dataset"] != "Mean"]
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.plot(gd["dataset"], gd["exact_match"], marker="o", label="ExactMatch")
    ax.plot(gd["dataset"], gd["beam_improve"], marker="o", label="BeamImprove")
    ax.set_ylabel("Rate")
    ax.set_title("Greedy path versus stronger subset search")
    ax.tick_params(axis="x", rotation=35)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "recreated_greedy_diagnostics.png", dpi=220)
    plt.close(fig)

    print(f"wrote figures to {OUT}")


if __name__ == "__main__":
    main()
