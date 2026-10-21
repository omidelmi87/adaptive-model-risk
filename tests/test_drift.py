
import numpy as np
import pandas as pd
import pytest

from src.drift import calculate_psi, summarize_feature_drift


def test_psi_identical_distributions():
    """PSI should be zero for identical samples."""

    reference = np.array(
        [100, 200, 300, 400, 500, 600],
        dtype=float,
    )

    current = reference.copy()

    result = calculate_psi(
        reference,
        current,
        n_bins=3,
    )

    assert result == pytest.approx(0.0, abs=1e-12)


def test_psi_detects_distribution_shift():
    """PSI should be positive when a distribution shifts."""

    reference = np.arange(100, dtype=float)

    current = reference + 20.0

    result = calculate_psi(
        reference,
        current,
        n_bins=10,
    )

    assert np.isfinite(result)
    assert result > 0.0


def test_psi_constant_reference_raises_error():
    """PSI should reject a constant reference distribution."""

    reference = np.full(100, 5.0)

    current = np.arange(100, dtype=float)

    with pytest.raises(
        ValueError,
        match="constant reference variable",
    ):
        calculate_psi(
            reference,
            current,
            n_bins=10,
        )


def test_psi_ignores_nonfinite_observations():
    """Nonfinite values should be excluded before calculating PSI."""

    reference = np.array(
        [10, 20, 30, 40, 50, np.nan, np.inf],
        dtype=float,
    )

    current = np.array(
        [10, 20, 30, 40, 50, np.nan, -np.inf],
        dtype=float,
    )

    result = calculate_psi(
        reference,
        current,
        n_bins=5,
    )

    assert result == pytest.approx(0.0, abs=1e-12)


def test_psi_rejects_samples_without_finite_values():
    """PSI should reject a sample containing no finite values."""

    reference = np.array([10, 20, 30, 40, 50], dtype=float)
    current = np.array([np.nan, np.inf, -np.inf])

    with pytest.raises(
        ValueError,
        match="contain finite observations",
    ):
        calculate_psi(
            reference,
            current,
            n_bins=5,
        )


def test_feature_drift_known_shift():
    """Verify drift metrics for a known distribution shift."""

    reference = pd.DataFrame({
        "feature_a": np.arange(10, dtype=float)
    })

    current = pd.DataFrame({
        "feature_a": np.arange(10, dtype=float) + 2
    })

    result = summarize_feature_drift(
        reference_data=reference,
        current_data=current,
        features=["feature_a"],
        n_bins=5,
    )

    row = result.iloc[0]

    assert row["feature"] == "feature_a"
    assert row["mean_shift"] == pytest.approx(2.0)
    assert row["ks_statistic"] == pytest.approx(0.2)
    assert row["wasserstein_distance"] == pytest.approx(2.0)
    assert row["psi"] > 0.0


def test_feature_drift_multiple_features():
    """Verify independent drift calculations for multiple features."""

    reference = pd.DataFrame({
        "feature_a": np.arange(10, dtype=float),
        "feature_b": np.arange(10, dtype=float) * 2,
    })

    current = pd.DataFrame({
        "feature_a": np.arange(10, dtype=float) + 2,
        "feature_b": np.arange(10, dtype=float) * 2,
    })

    result = summarize_feature_drift(
        reference_data=reference,
        current_data=current,
        features=["feature_a", "feature_b"],
        n_bins=5,
    )

    result = result.set_index("feature")

    assert len(result) == 2

    # Feature A has shifted.
    assert result.loc["feature_a", "mean_shift"] == pytest.approx(2.0)
    assert result.loc["feature_a", "psi"] > 0.0

    # Feature B is unchanged.
    assert result.loc["feature_b", "mean_shift"] == pytest.approx(0.0)
    assert result.loc["feature_b", "psi"] == pytest.approx(0.0)
    assert result.loc["feature_b", "ks_statistic"] == pytest.approx(0.0)
    assert result.loc["feature_b", "wasserstein_distance"] == pytest.approx(0.0)


@pytest.mark.parametrize(
    "missing_from, expected_message",
    [
        ("reference", "feature_a is missing from reference data"),
        ("current", "feature_a is missing from current data"),
    ],
)
def test_feature_drift_missing_column(
    missing_from, expected_message
):
    """Missing requested features should raise clear errors."""

    reference = pd.DataFrame({
        "feature_a": np.arange(10, dtype=float)
    })

    current = reference.copy()

    if missing_from == "reference":
        reference = reference.drop(columns=["feature_a"])
    else:
        current = current.drop(columns=["feature_a"])

    with pytest.raises(ValueError, match=expected_message):
        summarize_feature_drift(
            reference_data=reference,
            current_data=current,
            features=["feature_a"],
            n_bins=5,
        )


def test_feature_drift_ignores_nonfinite_observations():
    """Identical finite values should produce zero drift."""

    values = np.arange(10, dtype=float)

    reference = pd.DataFrame({
        "feature_a": np.append(values, np.nan)
    })

    current = reference.copy()

    result = summarize_feature_drift(
        reference_data=reference,
        current_data=current,
        features=["feature_a"],
        n_bins=5,
    )

    row = result.iloc[0]

    assert row["mean_shift"] == pytest.approx(0.0)
    assert row["psi"] == pytest.approx(0.0)
    assert row["ks_statistic"] == pytest.approx(0.0)
    assert row["wasserstein_distance"] == pytest.approx(0.0)


def test_legacy_drift_imports():
    """Legacy and package imports must reference the same functions."""

    from src.drift import (
        calculate_psi as legacy_psi,
        summarize_feature_drift as legacy_summary,
    )

    from adaptive_model_risk.drift import (
        calculate_psi as package_psi,
        summarize_feature_drift as package_summary,
    )

    assert legacy_psi is package_psi
    assert legacy_summary is package_summary
