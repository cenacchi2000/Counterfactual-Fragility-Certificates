#!/usr/bin/env python
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from cfc_ref import compute_cfc_certificate


def toy_predict_proba(x: np.ndarray) -> np.ndarray:
    # A tiny deterministic classifier for artifact sanity checks.
    logit = 1.8 * x[0] + 1.3 * x[1] - 1.1 * x[2] + 0.4 * x[3]
    p1 = 1.0 / (1.0 + np.exp(-logit))
    return np.array([1.0 - p1, p1])


def main() -> None:
    x = np.array([1.3, 1.0, -0.2, 0.1, 0.0, 0.4])
    baseline = np.zeros_like(x)
    groups = [[0], [1], [2], [3], [4, 5]]
    cert = compute_cfc_certificate(toy_predict_proba, x, groups, baseline, audit_depth=5)
    out = Path("results/demo_certificate.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(cert.to_dict(), indent=2))
    print(json.dumps(cert.to_dict(), indent=2))


if __name__ == "__main__":
    main()
