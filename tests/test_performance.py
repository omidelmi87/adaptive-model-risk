
import numpy as np
import pytest
import warnings

from sklearn.exceptions import UndefinedMetricWarning

from src.monitoring import (
    calculate_calibration_error,
    calculate_performance_metrics,
)


def test_perfect_binary_predictions():
    """Perfect predictions should produce ideal metrics."""

    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0.0, 0.0, 1.0, 1.0])

    result = calculate_performance_metrics(
        y_true,
        y_pred,
        n_bins=2,
    )

    assert result["roc_auc"] == pytest.approx(1.0)
    assert result["brier_score"] == pytest.approx(0.0)
    assert result["calibration_error"] == pytest.approx(0.0)

    assert result["observed_rate"] == pytest.approx(0.5)
    assert result["mean_predicted_probability"] == pytest.approx(0.5)

    assert result["signed_probability_gap"] == pytest.approx(0.0)
    assert result["absolute_probability_gap"] == pytest.approx(0.0)


def test_imperfect_probability_predictions():
    """Verify metrics for correctly ranked but imperfect predictions."""

    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0.1, 0.2, 0.7, 0.8])

    result = calculate_performance_metrics(
        y_true,
        y_pred,
        n_bins=2,
    )

    assert result["roc_auc"] == pytest.approx(1.0)
    assert result["brier_score"] == pytest.approx(0.045)
    assert result["calibration_error"] == pytest.approx(0.20)

    assert result["observed_rate"] == pytest.approx(0.5)
    assert result["mean_predicted_probability"] == pytest.approx(0.45)

    assert result["signed_probability_gap"] == pytest.approx(0.05)
    assert result["absolute_probability_gap"] == pytest.approx(0.05)


def test_single_class_outcomes():
    """Valid metrics should remain available with one outcome class."""

    y_true = np.array([0, 0, 0, 0])
    y_pred = np.array([0.1, 0.2, 0.3, 0.4])

    # Treat undefined-AUC warnings as errors.
    with warnings.catch_warnings():
        warnings.simplefilter("error", UndefinedMetricWarning)

        result = calculate_performance_metrics(
            y_true,
            y_pred,
            n_bins=2,
        )

    # ROC AUC is undefined for single-class outcomes.
    assert np.isnan(result["roc_auc"])

    # Other performance metrics remain meaningful.
    assert result["brier_score"] == pytest.approx(0.075)
    assert np.isfinite(result["calibration_error"])

    assert result["observed_rate"] == pytest.approx(0.0)
    assert result["mean_predicted_probability"] == pytest.approx(0.25)
    assert result["signed_probability_gap"] == pytest.approx(-0.25)
    assert result["absolute_probability_gap"] == pytest.approx(0.25)


@pytest.mark.parametrize(
    "invalid_probabilities",
    [
        [-0.1, 0.2, 0.7, 0.8],
        [0.1, 0.2, 0.7, 1.1],
        [0.1, 0.2, np.nan, 0.8],
    ],
)
def test_invalid_predicted_probabilities(invalid_probabilities):
    """Reject probabilities outside [0, 1] or containing NaN."""

    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array(invalid_probabilities)

    with pytest.raises(ValueError):
        calculate_performance_metrics(
            y_true,
            y_pred,
            n_bins=2,
        )


def test_mismatched_input_lengths():
    """Predictions and outcomes must have matching lengths."""

    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0.1, 0.2, 0.8])

    with pytest.raises(ValueError, match="inconsistent numbers of samples"):
        calculate_performance_metrics(
            y_true,
            y_pred,
            n_bins=2,
        )


def test_calibration_error_known_values():
    """Verify calibration error using two known probability bins."""

    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0.1, 0.3, 0.6, 0.8])

    result = calculate_calibration_error(
        y_true,
        y_pred,
        n_bins=2,
        strategy="quantile",
    )

    assert result == pytest.approx(0.25)


def test_calibration_error_unequal_bin_sizes():
    """Calibration error should average nonempty bins equally."""

    y_true = np.array([0, 0, 0, 1, 1])
    y_pred = np.array([0.2, 0.2, 0.2, 0.2, 0.8])

    result = calculate_calibration_error(
        y_true,
        y_pred,
        n_bins=2,
        strategy="uniform",
    )

    assert result == pytest.approx(0.125)


def test_calibration_error_with_empty_bins():
    """Empty probability bins should not affect calibration error."""

    y_true = np.array([0, 1, 1])
    y_pred = np.array([0.1, 0.1, 0.9])

    result = calculate_calibration_error(
        y_true,
        y_pred,
        n_bins=5,
        strategy="uniform",
    )

    assert result == pytest.approx(0.25)


def test_legacy_performance_imports():
    """Legacy and package imports must reference the same functions."""

    from src.monitoring import (
        calculate_calibration_error as legacy_calibration,
        calculate_performance_metrics as legacy_performance,
    )

    from adaptive_model_risk.performance import (
        calculate_calibration_error as package_calibration,
        calculate_performance_metrics as package_performance,
    )

    assert legacy_calibration is package_calibration
    assert legacy_performance is package_performance
