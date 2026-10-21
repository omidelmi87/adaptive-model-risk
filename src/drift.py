
"""
Backward-compatible imports for drift calculations.

The authoritative implementations now live in
adaptive_model_risk.drift.

This module is retained for compatibility with
existing research notebooks.
"""

from adaptive_model_risk.drift import (
    calculate_psi,
    summarize_feature_drift,
)

__all__ = [
    "calculate_psi",
    "summarize_feature_drift",
]
