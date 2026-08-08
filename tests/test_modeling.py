"""
test_modeling.py
────────────────
Unit tests for model prediction output and probability bounds.
Covers: predict_proba(), load_model(), load_champion().
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.config import (
    DECISION_THRESHOLD,
    MODEL_NAME_LR,
    MODEL_NAME_RF,
    MODEL_NAME_XGB,
    TARGET_COL,
)


class TestPredictProba:
    """Tests for src.modeling.predict.predict_proba()."""

    def test_prediction_output_columns(self, fitted_model, test_processed):
        """
        Output DataFrame must contain exactly the two expected columns:
        Predicted_Default_Prob and Predicted_Status.
        """
        from src.modeling.predict import predict_proba

        results = predict_proba(fitted_model, test_processed)

        assert "Predicted_Default_Prob" in results.columns, (
            "Column 'Predicted_Default_Prob' missing from prediction output."
        )
        assert "Predicted_Status" in results.columns, (
            "Column 'Predicted_Status' missing from prediction output."
        )

    def test_probability_lower_bound(self, fitted_model, test_processed):
        """All predicted probabilities must be >= 0.0."""
        from src.modeling.predict import predict_proba

        results = predict_proba(fitted_model, test_processed)
        probs = results["Predicted_Default_Prob"].values
        assert np.all(probs >= 0.0), (
            f"Found probabilities below 0.0: min={probs.min():.6f}"
        )

    def test_probability_upper_bound(self, fitted_model, test_processed):
        """All predicted probabilities must be <= 1.0."""
        from src.modeling.predict import predict_proba

        results = predict_proba(fitted_model, test_processed)
        probs = results["Predicted_Default_Prob"].values
        assert np.all(probs <= 1.0), (
            f"Found probabilities above 1.0: max={probs.max():.6f}"
        )

    def test_binary_labels_only(self, fitted_model, test_processed):
        """Predicted_Status must contain only values in {0, 1}."""
        from src.modeling.predict import predict_proba

        results = predict_proba(fitted_model, test_processed)
        labels = set(results["Predicted_Status"].unique())
        assert labels.issubset({0, 1}), (
            f"Predicted labels must be binary (0 or 1), found: {labels}"
        )

    def test_output_row_count_matches_input(
        self, fitted_model, test_processed
    ):
        """Output row count must exactly match the input row count."""
        from src.modeling.predict import predict_proba

        results = predict_proba(fitted_model, test_processed)
        assert len(results) == len(test_processed), (
            f"Output rows ({len(results)}) != input rows ({len(test_processed)})"
        )

    def test_threshold_applied_correctly(self, fitted_model, test_processed):
        """
        Predicted_Status must be 1 when probability >= DECISION_THRESHOLD
        and 0 otherwise.
        """
        from src.modeling.predict import predict_proba

        results = predict_proba(
            fitted_model, test_processed, threshold=DECISION_THRESHOLD
        )
        probs = results["Predicted_Default_Prob"].values
        labels = results["Predicted_Status"].values

        expected = (probs >= DECISION_THRESHOLD).astype(int)
        np.testing.assert_array_equal(
            labels,
            expected,
            err_msg=(
                "Predicted_Status does not match the expected threshold "
                f"cutoff of {DECISION_THRESHOLD}."
            ),
        )

    def test_custom_threshold(self, fitted_model, test_processed):
        """
        A custom threshold of 0.30 should produce more positive predictions
        than the default 0.50 threshold.
        """
        from src.modeling.predict import predict_proba

        results_default = predict_proba(
            fitted_model, test_processed, threshold=0.50
        )
        results_low = predict_proba(
            fitted_model, test_processed, threshold=0.30
        )

        defaults_at_50 = results_default["Predicted_Status"].sum()
        defaults_at_30 = results_low["Predicted_Status"].sum()

        assert defaults_at_30 >= defaults_at_50, (
            "Lower threshold (0.30) should yield >= positive predictions "
            "compared to higher threshold (0.50)."
        )

    def test_predict_proba_ignores_target_column(
        self, fitted_model, test_processed
    ):
        """
        predict_proba must silently drop the target column if present
        and still return valid predictions.
        """
        from src.modeling.predict import predict_proba

        # test_processed already has TARGET_COL — should not raise
        results = predict_proba(fitted_model, test_processed)
        assert len(results) == len(test_processed)


class TestLoadModel:
    """Tests for load_model() and load_champion()."""

    def test_load_model_from_path(self):
        """
        load_model() must successfully load the legacy model artifact
        from the configured MODEL_PATH.
        """
        from src.config import MODEL_PATH
        from src.modeling.predict import load_model

        if not MODEL_PATH.exists():
            pytest.skip(
                f"Legacy model artifact not found at '{MODEL_PATH}'. "
                "Run `make train` first."
            )
        model = load_model(MODEL_PATH)
        assert model is not None
        assert hasattr(model, "predict_proba"), (
            "Loaded model must have a predict_proba method."
        )

    def test_load_model_raises_on_missing_file(self, tmp_path):
        """load_model() must raise FileNotFoundError for a missing path."""
        from src.modeling.predict import load_model

        missing_path = tmp_path / "nonexistent_model.joblib"
        with pytest.raises(FileNotFoundError):
            load_model(missing_path)

    def test_load_champion_random_forest(self):
        """
        load_champion() must return a fitted estimator for the
        random_forest champion registered in the model registry.
        """
        from src.modeling.predict import load_champion

        try:
            model = load_champion(MODEL_NAME_RF)
        except (KeyError, FileNotFoundError) as exc:
            pytest.skip(
                f"Champion RF model not found in registry: {exc}. "
                "Run `make train` first."
            )

        assert model is not None
        assert hasattr(model, "predict_proba"), (
            "Champion RF model must have a predict_proba method."
        )

    def test_load_champion_logistic_regression(self):
        """load_champion() must work for logistic_regression."""
        from src.modeling.predict import load_champion

        try:
            model = load_champion(MODEL_NAME_LR)
        except (KeyError, FileNotFoundError) as exc:
            pytest.skip(f"Champion LR not found: {exc}")

        assert hasattr(model, "predict_proba")

    def test_load_champion_xgboost(self):
        """load_champion() must work for xgboost."""
        from src.modeling.predict import load_champion

        try:
            model = load_champion(MODEL_NAME_XGB)
        except (KeyError, FileNotFoundError) as exc:
            pytest.skip(f"Champion XGB not found: {exc}")

        assert hasattr(model, "predict_proba")

    def test_load_champion_raises_on_unknown_model(self):
        """load_champion() must raise KeyError for an unknown model name."""
        from src.modeling.predict import load_champion

        with pytest.raises(KeyError):
            load_champion("nonexistent_model_xyz")


class TestModelMetrics:
    """Smoke tests verifying trained models meet minimum quality thresholds."""

    def test_random_forest_roc_auc_above_threshold(
        self, fitted_model, test_processed
    ):
        """
        Random Forest ROC-AUC on the test set must be > 0.80.
        Guards against catastrophic model degradation.
        """
        from sklearn.metrics import roc_auc_score

        from src.modeling.predict import predict_proba

        results = predict_proba(fitted_model, test_processed)
        y_true = test_processed[TARGET_COL].values
        y_prob = results["Predicted_Default_Prob"].values

        roc_auc = roc_auc_score(y_true, y_prob)
        assert roc_auc > 0.80, (
            f"Random Forest ROC-AUC ({roc_auc:.4f}) is below the "
            "minimum acceptable threshold of 0.80."
        )

    def test_predictions_not_all_same_class(
        self, fitted_model, test_processed
    ):
        """
        The model must not predict the same class for every observation
        (i.e. it must not degenerate into a constant classifier).
        """
        from src.modeling.predict import predict_proba

        results = predict_proba(fitted_model, test_processed)
        unique_labels = results["Predicted_Status"].nunique()
        assert unique_labels > 1, (
            "Model predicted only one class for all test samples — "
            "the model may have degenerated."
        )
