from __future__ import annotations

import numpy as np

EPS_PROB = 1e-12
EPS_MARGIN = 1e-8


def clipped_probabilities(probs: np.ndarray, eps: float = EPS_PROB) -> np.ndarray:
    """Clip and renormalize a probability vector for fair scoring across model classes."""
    p = np.asarray(probs, dtype=float)
    if p.ndim != 1:
        raise ValueError("probs must be a one-dimensional class-probability vector")
    p = np.maximum(p, eps)
    total = p.sum()
    if not np.isfinite(total) or total <= 0:
        raise ValueError("invalid probability vector after clipping")
    return p / total


def probability_to_pseudologits(probs: np.ndarray, eps: float = EPS_PROB) -> np.ndarray:
    """Convert probabilities to centered pseudo-logits.

    This is the standardized conversion used for neural and non-neural models so that
    margin and energy scores do not depend on whether a model exposes native logits.
    """
    p = clipped_probabilities(probs, eps=eps)
    logp = np.log(p)
    return logp - logp.mean()


def top_margin_from_probs(probs: np.ndarray) -> float:
    """Top-class pseudo-logit margin."""
    z = probability_to_pseudologits(probs)
    order = np.argsort(z)[::-1]
    if len(order) < 2:
        return 0.0
    return float(z[order[0]] - z[order[1]])


def normalized_margin_collapse(original_margin: float, stressed_margin: float, eps: float = EPS_MARGIN) -> float:
    """One-sided normalized margin collapse. Margin gains contribute zero."""
    return max(0.0, (original_margin - stressed_margin) / (abs(original_margin) + eps))


def brittle_label(confidence: float, original_label: int, stressed_label: int,
                  original_margin: float, stressed_margin: float,
                  confidence_threshold: float = 0.90, collapse_threshold: float = 0.50) -> int:
    """High-confidence brittle label used in the paper's held-out evaluation protocol."""
    if confidence < confidence_threshold:
        return 0
    kappa = normalized_margin_collapse(original_margin, stressed_margin)
    return int((stressed_label != original_label) or (kappa >= collapse_threshold))
