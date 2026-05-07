"""Anonymous review reference implementation for Counterfactual Fragility Certificates.

This package intentionally provides the compact, auditable core of CFC: probability standardization,
evidence-group removal, greedy stress trajectories, RCMA, degradation thresholds, and FDS.
The full training grid used in the paper is not included in this blinded artifact.
"""
from .certificate import CFCCertificate, compute_cfc_certificate
from .protocol import brittle_label, probability_to_pseudologits

__all__ = ["CFCCertificate", "compute_cfc_certificate", "brittle_label", "probability_to_pseudologits"]
