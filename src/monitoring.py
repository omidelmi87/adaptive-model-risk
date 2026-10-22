
"""Model-monitoring utilities for Adaptive Model Risk experiments."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike

# Backward-compatible imports for existing notebooks.
from adaptive_model_risk.performance import (
    calculate_calibration_error,
    calculate_performance_metrics,
)


def calculate_null_percentile(
    value: float,
    null_values: ArrayLike,
) -> float:
    """
    Calculate the empirical percentile of a value within a null distribution.

    Parameters
    ----------
    value
        Observed monitoring-metric value.
    null_values
        Metric values generated under healthy null simulations.

    Returns
    -------
    float
        Empirical percentile on the interval [0, 1]. Higher values indicate
        greater upper-tail extremeness relative to healthy operation.
    """
    null_array = np.asarray(null_values, dtype=float)

    if null_array.size == 0:
        raise ValueError("null_values must contain at least one value.")

    if np.isnan(value):
        raise ValueError("value must not be NaN.")

    if np.isnan(null_array).any():
        raise ValueError("null_values must not contain NaN values.")

    return float(np.mean(null_array <= value))


def calculate_ewma(
    values: ArrayLike,
    *,
    lambda_: float = 0.30,
) -> np.ndarray:
    """
    Calculate an exponentially weighted moving average (EWMA).

    Parameters
    ----------
    values
        Sequential numeric observations.
    lambda_
        Weight assigned to the current observation. Must be in (0, 1].

    Returns
    -------
    np.ndarray
        EWMA values with the same length as the input sequence.

    Notes
    -----
    The first EWMA value is initialized to the first observation:

        Z_0 = X_0

    Subsequent values follow:

        Z_t = lambda_ * X_t + (1 - lambda_) * Z_(t - 1)
    """
    values_array = np.asarray(values, dtype=float)

    if values_array.size == 0:
        raise ValueError("values must contain at least one observation.")

    if not 0 < lambda_ <= 1:
        raise ValueError("lambda_ must be in the interval (0, 1].")

    if np.isnan(values_array).any():
        raise ValueError("values must not contain NaN values.")

    ewma = np.empty_like(values_array, dtype=float)
    ewma[0] = values_array[0]

    for index in range(1, values_array.size):
        ewma[index] = (
            lambda_ * values_array[index]
            + (1 - lambda_) * ewma[index - 1]
        )

    return ewma


def apply_persistence_rule(
    flags: ArrayLike,
    *,
    window: int = 3,
    required: int = 2,
) -> np.ndarray:
    """
    Apply a rolling persistence rule to a sequence of raw monitoring flags.

    Parameters
    ----------
    flags
        Sequential binary or boolean raw flags.
    window
        Rolling window length.
    required
        Minimum number of raw flags within the rolling window needed to
        produce a confirmed alert.

    Returns
    -------
    np.ndarray
        Boolean array indicating whether the persistence rule is satisfied
        at each time point.

    Notes
    -----
    A confirmed alert can occur only once enough observations exist to fill
    the specified rolling window.
    """
    flags_array = np.asarray(flags, dtype=int)

    if flags_array.size == 0:
        raise ValueError("flags must contain at least one observation.")

    if window < 1:
        raise ValueError("window must be at least 1.")

    if required < 1:
        raise ValueError("required must be at least 1.")

    if required > window:
        raise ValueError("required cannot be greater than window.")

    if not np.isin(flags_array, [0, 1]).all():
        raise ValueError("flags must contain only binary values: 0/1 or False/True.")

    confirmed = np.zeros(flags_array.size, dtype=bool)

    for index in range(window - 1, flags_array.size):
        rolling_sum = np.sum(
            flags_array[index - window + 1 : index + 1]
        )

        confirmed[index] = rolling_sum >= required

    return confirmed


def calculate_detection_delay(
    confirmed_alerts: ArrayLike,
    periods: ArrayLike,
    *,
    onset_period: int,
) -> int | None:
    """
    Calculate detection delay from a known experimental change onset.

    Parameters
    ----------
    confirmed_alerts
        Sequential boolean or binary confirmed-alert indicators.
    periods
        Period identifiers corresponding to the alert sequence.
    onset_period
        First period in which the controlled change is present.

    Returns
    -------
    int | None
        Number of periods between the true change onset and the first
        confirmed alert at or after that onset. Returns None if no
        confirmed alert occurs after onset.

    Notes
    -----
    Confirmed alerts before the onset period are ignored for detection-delay
    calculation because they represent pre-change false alarms.
    """
    alerts_array = np.asarray(confirmed_alerts, dtype=bool)
    periods_array = np.asarray(periods)

    if alerts_array.size == 0:
        raise ValueError(
            "confirmed_alerts must contain at least one observation."
        )

    if alerts_array.size != periods_array.size:
        raise ValueError(
            "confirmed_alerts and periods must have the same length."
        )

    if periods_array.ndim != 1:
        raise ValueError("periods must be one-dimensional.")

    eligible = (
        alerts_array
        & (periods_array >= onset_period)
    )

    if not np.any(eligible):
        return None

    first_alert_period = periods_array[
        np.flatnonzero(eligible)[0]
    ]

    return int(first_alert_period - onset_period)


def calculate_system_score(
    component_percentiles: ArrayLike,
) -> float:
    """
    Aggregate component-level null percentiles into a system-level score.

    Parameters
    ----------
    component_percentiles
        Null-relative component scores on the interval [0, 1].

    Returns
    -------
    float
        Maximum component percentile. Higher values indicate stronger
        evidence of abnormal behavior relative to healthy operation.

    Notes
    -----
    This function does not itself determine whether an alert should occur.
    The distribution of the resulting system score must also be calibrated
    under healthy null simulations to account for multiple monitored signals.
    """
    percentiles = np.asarray(component_percentiles, dtype=float)

    if percentiles.size == 0:
        raise ValueError(
            "component_percentiles must contain at least one value."
        )

    if np.isnan(percentiles).any():
        raise ValueError(
            "component_percentiles must not contain NaN values."
        )

    if ((percentiles < 0) | (percentiles > 1)).any():
        raise ValueError(
            "component_percentiles must lie in the interval [0, 1]."
        )

    return float(np.max(percentiles))


def calculate_empirical_threshold(
    null_values: ArrayLike,
    *,
    quantile: float = 0.99,
) -> float:
    """
    Calculate an empirical upper-tail monitoring threshold.

    Parameters
    ----------
    null_values
        Metric or system-score values generated under healthy operation.
    quantile
        Quantile used as the monitoring boundary. Must lie strictly
        between 0 and 1.

    Returns
    -------
    float
        Empirical quantile of the healthy null distribution.

    Notes
    -----
    This function estimates a monitoring boundary from healthy simulated
    behavior rather than relying on a fixed conventional cutoff.
    """
    null_array = np.asarray(null_values, dtype=float)

    if null_array.size == 0:
        raise ValueError(
            "null_values must contain at least one value."
        )

    if np.isnan(null_array).any():
        raise ValueError(
            "null_values must not contain NaN values."
        )

    if not 0 < quantile < 1:
        raise ValueError(
            "quantile must lie strictly between 0 and 1."
        )

    return float(np.quantile(null_array, quantile))
