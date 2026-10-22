"""Model-monitoring utilities for Adaptive Model Risk experiments."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss, roc_auc_score


def calculate_calibration_error(
    y_true: ArrayLike,
    y_pred: ArrayLike,
    *,
    n_bins: int = 10,
    strategy: str = "quantile",
) -> float:
    """
    Calculate mean absolute calibration error across probability bins.

    Parameters
    ----------
    y_true
        Observed binary outcomes.
    y_pred
        Predicted probabilities for the positive class.
    n_bins
        Number of calibration bins.
    strategy
        Binning strategy passed to sklearn.calibration.calibration_curve.

    Returns
    -------
    float
        Mean absolute difference between observed and predicted event
        rates across calibration bins.
    """
    prob_true, prob_pred = calibration_curve(
        y_true,
        y_pred,
        n_bins=n_bins,
        strategy=strategy,
    )

    return float(np.mean(np.abs(prob_true - prob_pred)))


def calculate_performance_metrics(
    y_true: ArrayLike,
    y_pred: ArrayLike,
    *,
    n_bins: int = 10,
    strategy: str = "quantile",
) -> dict[str, float]:
    """
    Calculate outcome-dependent model-monitoring metrics.

    Parameters
    ----------
    y_true
        Observed binary outcomes.
    y_pred
        Predicted probabilities for the positive class.
    n_bins
        Number of bins used for calibration error.
    strategy
        Binning strategy used for calibration error.

    Returns
    -------
    dict[str, float]
        Dictionary containing ROC AUC, Brier score, calibration error,
        observed event rate, mean predicted probability, and the signed
        and absolute predicted-vs-observed probability gaps.
    """
    y_true_array = np.asarray(y_true)
    y_pred_array = np.asarray(y_pred)

    observed_rate = float(np.mean(y_true_array))
    mean_predicted_probability = float(np.mean(y_pred_array))

    signed_probability_gap = (
        observed_rate - mean_predicted_probability
    )

    # ROC AUC requires both binary outcome classes.
    # For single-class cohorts, report NaN without generating a warning.
    if np.unique(y_true_array).size < 2:
        roc_auc = float("nan")
    else:
        roc_auc = float(
            roc_auc_score(y_true_array, y_pred_array)
        )

    return {
        "roc_auc": roc_auc,
        "brier_score": float(
            brier_score_loss(y_true_array, y_pred_array)
        ),
        "calibration_error": calculate_calibration_error(
            y_true_array,
            y_pred_array,
            n_bins=n_bins,
            strategy=strategy,
        ),
        "observed_rate": observed_rate,
        "mean_predicted_probability": mean_predicted_probability,
        "signed_probability_gap": float(signed_probability_gap),
        "absolute_probability_gap": float(
            abs(signed_probability_gap)
        ),
    }
