import numpy as np
from cfc_ref import compute_cfc_certificate


def predict(x):
    p = 1.0 / (1.0 + np.exp(-(2*x[0] - x[1])))
    return np.array([1-p, p])


def test_certificate_runs():
    cert = compute_cfc_certificate(predict, np.array([1.0, 0.2]), [[0], [1]], np.zeros(2), audit_depth=2)
    assert 0.0 <= cert.fds <= 1.0
    assert cert.flip_budget >= 1
    assert len(cert.margins) >= 1
