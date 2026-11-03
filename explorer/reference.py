"""New paper-aligned reference examples; separate from legacy src/cfc_ref.
Not recovered original benchmark code. Affine guarantee assumes partitioned groups,
fixed baseline replacement and exact arithmetic; this implementation uses floats.
"""
import numpy as np

def removal_path(scores, x, baseline, groups, depth=None):
    x = np.asarray(x, dtype=float)
    baseline = np.asarray(baseline, dtype=float)
    original = int(np.argmax(scores(x)))
    current = x.copy()
    remaining = list(range(len(groups)))
    def margin(row):
        values = np.asarray(scores(row))
        return float(values[original] - np.max(np.delete(values, original)))
    records = [{"removed": None, "margin": margin(current), "label": original}]
    for _ in range(len(groups) if depth is None else min(depth, len(groups))):
        candidates = []
        for g in remaining:
            changed = current.copy()
            changed[groups[g]] = baseline[groups[g]]
            candidates.append((margin(changed), g, changed))
        value, g, current = min(candidates, key=lambda t: (t[0], t[1]))
        remaining.remove(g)
        records.append({"removed": g, "margin": value, "label": int(np.argmax(scores(current)))})
    return records

def graded_tests(scores, x, baseline, groups, severities=(.2, .4, .6, .8, 1.)):
    # Each group starts from the original row, independently of the removal path.
    x = np.asarray(x, dtype=float)
    baseline = np.asarray(baseline, dtype=float)
    original = int(np.argmax(scores(x)))
    records = []
    for g, columns in enumerate(groups):
        for severity in severities:
            if not 0 <= severity <= 1:
                raise ValueError("Severity must be in [0,1]")
            changed = x.copy()
            changed[columns] = (1 - severity) * x[columns] + severity * baseline[columns]
            values = np.asarray(scores(changed))
            records.append({"group": g, "severity": severity,
                            "margin": float(values[original] - np.max(np.delete(values, original))),
                            "flip": int(np.argmax(values)) != original})
    return records

def affine_minimum_removals(weights, bias, x, baseline, groups):
    weights, bias, x, baseline = map(np.asarray, (weights, bias, x, baseline))
    flat = [j for g in groups for j in g]
    if sorted(flat) != list(range(len(x))):
        raise ValueError("Groups must partition all input columns")
    values = weights @ x + bias
    original = int(np.argmax(values))  # smallest class index wins ties
    best = None
    for rival in range(len(values)):
        if rival == original:
            continue
        contributions = [float(np.sum((weights[original, g] - weights[rival, g]) * (x[g] - baseline[g]))) for g in groups]
        order = sorted([g for g, a in enumerate(contributions) if a > 0], key=lambda g: (-contributions[g], g))
        residual = float(values[original] - values[rival])
        for k, g in enumerate(order, 1):
            residual -= contributions[g]
            if residual < 0 or (residual == 0 and rival < original):
                result = {"depth": k, "groups": order[:k], "rival": rival}
                if best is None or k < best["depth"]:
                    best = result
                break
    return best
