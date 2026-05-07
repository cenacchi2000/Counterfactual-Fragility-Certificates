from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Callable, Iterable, Sequence

import numpy as np

from .protocol import top_margin_from_probs, normalized_margin_collapse

PredictFn = Callable[[np.ndarray], np.ndarray]


@dataclass(frozen=True)
class CFCCertificate:
    predicted_label: int
    confidence: float
    group_order: list[int]
    flip_budget: int
    rcma: float
    degradation_thresholds: dict[str, float | None]
    fds: float
    margins: list[float]

    def to_dict(self) -> dict:
        return asdict(self)


def _remove_groups(x: np.ndarray, groups: Sequence[Sequence[int]], selected: Iterable[int], baseline: np.ndarray) -> np.ndarray:
    x_new = np.array(x, dtype=float, copy=True)
    for group_idx in selected:
        coords = list(groups[group_idx])
        x_new[coords] = baseline[coords]
    return x_new


def _attenuate_group(x: np.ndarray, groups: Sequence[Sequence[int]], group_idx: int, baseline: np.ndarray, lam: float) -> np.ndarray:
    x_new = np.array(x, dtype=float, copy=True)
    coords = list(groups[group_idx])
    x_new[coords] = (1.0 - lam) * x_new[coords] + lam * baseline[coords]
    return x_new


def compute_cfc_certificate(
    predict_proba: PredictFn,
    x: np.ndarray,
    groups: Sequence[Sequence[int]],
    baseline: np.ndarray,
    audit_depth: int = 10,
    severity_grid: Sequence[float] = (0.25, 0.50, 0.75, 1.0),
    phi: Callable[[float], float] | None = None,
) -> CFCCertificate:
    """Compute a compact Counterfactual Fragility Certificate for one sample.

    Parameters
    ----------
    predict_proba:
        Function mapping a transformed feature vector to class probabilities.
    x:
        Transformed feature vector.
    groups:
        Evidence groups as lists of transformed-coordinate indices.
    baseline:
        Transformed-space replacement vector estimated from the training split.
    audit_depth:
        Maximum number of groups in the deterministic hard-removal path.
    severity_grid:
        Partial-degradation severities for the default attenuation operator.
    phi:
        Monotone bounding function for FDS. Defaults to 1-exp(-u).
    """
    if phi is None:
        phi = lambda u: 1.0 - np.exp(-u)

    x = np.asarray(x, dtype=float)
    baseline = np.asarray(baseline, dtype=float)
    probs = np.asarray(predict_proba(x), dtype=float)
    y0 = int(np.argmax(probs))
    conf = float(np.max(probs))
    m0 = top_margin_from_probs(probs)

    drops: list[tuple[float, int]] = []
    for gi in range(len(groups)):
        xr = _remove_groups(x, groups, [gi], baseline)
        mr = top_margin_from_probs(predict_proba(xr))
        drops.append((m0 - mr, gi))
    order = [gi for _, gi in sorted(drops, reverse=True)]

    K = min(audit_depth, len(groups))
    margins = [m0]
    flip_budget = K + 1
    for k in range(1, K + 1):
        xr = _remove_groups(x, groups, order[:k], baseline)
        pr = np.asarray(predict_proba(xr), dtype=float)
        margins.append(top_margin_from_probs(pr))
        if int(np.argmax(pr)) != y0 and flip_budget == K + 1:
            flip_budget = k

    collapses = [normalized_margin_collapse(m0, mk) for mk in margins]
    rcma = float(np.mean(collapses))

    thresholds: dict[str, float | None] = {}
    # Default graded operator: attenuate the highest-ranked group toward baseline.
    # A production protocol can register several operators; this reference implementation
    # keeps the operator explicit and simple for auditability.
    if order:
        g0 = order[0]
        first = None
        for lam in severity_grid:
            xd = _attenuate_group(x, groups, g0, baseline, float(lam))
            if int(np.argmax(predict_proba(xd))) != y0:
                first = float(lam)
                break
        thresholds["top_group_attenuation"] = first

    # Fixed equal weights used by the paper. No-flip degradation operators contribute zero.
    deg_terms = []
    for val in thresholds.values():
        if val is not None and np.isfinite(val):
            deg_terms.append(1.0 / (float(val) + 1e-8))
        else:
            deg_terms.append(0.0)
    degradation_score = float(np.mean(deg_terms)) if deg_terms else 0.0
    u = (rcma + (1.0 / max(flip_budget, 1)) + degradation_score) / 3.0
    fds = float(phi(u))

    return CFCCertificate(
        predicted_label=y0,
        confidence=conf,
        group_order=order,
        flip_budget=flip_budget,
        rcma=rcma,
        degradation_thresholds=thresholds,
        fds=fds,
        margins=[float(v) for v in margins],
    )
