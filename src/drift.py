"""Drift-detection utilities for Adaptive Model Risk experiments."""

import numpy as np
import pandas as pd

from scipy.stats import (
    ks_2samp,
    wasserstein_distance,
)


def calculate_psi(
    reference,
    current,
    n_bins=10,
    epsilon=1e-6,
):
    """
    Calculate the Population Stability Index (PSI).

    Quantile-based bins are created from the reference
    distribution and then applied to both samples.

    Parameters
    ----------
    reference : array-like
        Baseline or reference observations.

    current : array-like
        Current or comparison observations.

    n_bins : int, default=10
        Number of reference quantile bins.

    epsilon : float, default=1e-6
        Small value used to avoid division by zero
        or log(0).

    Returns
    -------
    float
        Population Stability Index.
    """

    reference = np.asarray(
        reference,
        dtype=float,
    )

    current = np.asarray(
        current,
        dtype=float,
    )

    reference = reference[
        np.isfinite(reference)
    ]

    current = current[
        np.isfinite(current)
    ]

    if len(reference) == 0 or len(current) == 0:
        raise ValueError(
            "Reference and current samples must "
            "contain finite observations."
        )

    quantiles = np.linspace(
        0,
        1,
        n_bins + 1,
    )

    bin_edges = np.quantile(
        reference,
        quantiles,
    )

    bin_edges = np.unique(bin_edges)

    if len(bin_edges) < 2:
        raise ValueError(
            "PSI cannot be calculated for a "
            "constant reference variable."
        )

    bin_edges[0] = -np.inf
    bin_edges[-1] = np.inf

    reference_counts, _ = np.histogram(
        reference,
        bins=bin_edges,
    )

    current_counts, _ = np.histogram(
        current,
        bins=bin_edges,
    )

    reference_proportions = (
        reference_counts / reference_counts.sum()
    )

    current_proportions = (
        current_counts / current_counts.sum()
    )

    reference_proportions = np.clip(
        reference_proportions,
        epsilon,
        None,
    )

    current_proportions = np.clip(
        current_proportions,
        epsilon,
        None,
    )

    psi = np.sum(
        (
            current_proportions
            - reference_proportions
        )
        * np.log(
            current_proportions
            / reference_proportions
        )
    )

    return float(psi)


def summarize_feature_drift(
    reference_data,
    current_data,
    features,
    n_bins=10,
):
    """
    Compare feature distributions between two environments.

    Parameters
    ----------
    reference_data : pandas.DataFrame
        Reference environment.

    current_data : pandas.DataFrame
        Current environment.

    features : list of str
        Features to compare.

    n_bins : int, default=10
        Number of bins used for PSI.

    Returns
    -------
    pandas.DataFrame
        Feature-level drift statistics.
    """

    rows = []

    for feature in features:
        if feature not in reference_data.columns:
            raise ValueError(
                f"{feature} is missing from reference data."
            )

        if feature not in current_data.columns:
            raise ValueError(
                f"{feature} is missing from current data."
            )

        reference = reference_data[
            feature
        ].to_numpy()

        current = current_data[
            feature
        ].to_numpy()

        ks_result = ks_2samp(
            reference,
            current,
        )

        rows.append(
            {
                "feature": feature,
                "reference_mean": np.mean(reference),
                "current_mean": np.mean(current),
                "mean_shift": (
                    np.mean(current)
                    - np.mean(reference)
                ),
                "psi": calculate_psi(
                    reference,
                    current,
                    n_bins=n_bins,
                ),
                "ks_statistic": (
                    ks_result.statistic
                ),
                "wasserstein_distance": (
                    wasserstein_distance(
                        reference,
                        current,
                    )
                ),
            }
        )

    return pd.DataFrame(rows)
