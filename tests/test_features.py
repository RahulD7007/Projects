"""
test_features.py
────────────────
Unit tests for feature engineering and the preprocessing pipeline.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.config import (
    BINARY_FLAG_FEATURES,  # was: BINARY_FEATURES
    CATEGORICAL_FEATURES,
    LEAKAGE_COLS,  # was: DROP_FEATURES
    MISSINGNESS_FLAG_COLS,
    NUMERIC_FEATURES,  # was: NUMERICAL_FEATURES
    TARGET_COL,
)


class TestFeatureEngineering:
    """Tests for execute_feature_engineering()."""

    def test_execute_feature_engineering(self, engineered_df):
        """
        Verify:
        - Leakage columns are absent after engineering.
        - Missingness flags are created and are strictly binary (0/1).
        - Compound features DTI_x_LTV and loan_to_income are present.
        """
        # ── Leakage columns must be removed ──────────────────────────────────
        for col in LEAKAGE_COLS:
            assert col not in engineered_df.columns, (
                f"Leakage column '{col}' must be dropped but is still present."
            )

        # ── Missingness flags must exist and be binary ────────────────────────
        for col in MISSINGNESS_FLAG_COLS:
            flag_col = f"{col}_isna"
            assert flag_col in engineered_df.columns, (
                f"Missingness flag '{flag_col}' was not created."
            )
            unique_vals = set(engineered_df[flag_col].unique())
            assert unique_vals.issubset({0, 1}), (
                f"Flag '{flag_col}' must contain only 0/1 values, "
                f"found: {unique_vals}"
            )

        # ── Compound features must exist ──────────────────────────────────────
        assert "DTI_x_LTV" in engineered_df.columns, (
            "Compound feature 'DTI_x_LTV' was not created."
        )
        assert "loan_to_income" in engineered_df.columns, (
            "Affordability ratio 'loan_to_income' was not created."
        )

    def test_leakage_cols_removed(self, engineered_df):
        """All leakage columns defined in config must be absent."""
        for col in LEAKAGE_COLS:
            assert col not in engineered_df.columns, (
                f"Leakage column '{col}' found in engineered DataFrame."
            )

    def test_missingness_flags_are_int(self, engineered_df):
        """Missingness flag columns must have integer dtype (0/1)."""
        for col in MISSINGNESS_FLAG_COLS:
            flag_col = f"{col}_isna"
            if flag_col in engineered_df.columns:
                assert engineered_df[flag_col].dtype in (
                    np.int8, np.int16, np.int32, np.int64,
                ), (
                    f"Flag '{flag_col}' must be integer dtype, "
                    f"got {engineered_df[flag_col].dtype}"
                )

    def test_dti_x_ltv_values(self, engineered_df):
        """
        DTI_x_LTV must equal dtir1 * LTV where both are non-null.
        Validates the compound feature formula is applied correctly.
        """
        mask = (
            engineered_df["dtir1"].notna()
            & engineered_df["LTV"].notna()
        )
        if mask.sum() > 0:
            expected = (
                engineered_df.loc[mask, "dtir1"]
                * engineered_df.loc[mask, "LTV"]
            )
            actual = engineered_df.loc[mask, "DTI_x_LTV"]
            pd.testing.assert_series_equal(
                actual.reset_index(drop=True),
                expected.reset_index(drop=True),
                check_names=False,
            )


class TestPreprocessingPipeline:
    """Tests for run_preprocessing_pipeline()."""

    def test_preprocessing_pipeline_returns_dataframes(
        self, processed_splits
    ):
        """Both splits must be non-empty DataFrames."""
        train_df, test_df = processed_splits
        assert isinstance(train_df, pd.DataFrame), (
            "train_df must be a pandas DataFrame"
        )
        assert isinstance(test_df, pd.DataFrame), (
            "test_df must be a pandas DataFrame"
        )
        assert len(train_df) > 0, "train_df must be non-empty"
        assert len(test_df) > 0, "test_df must be non-empty"

    def test_target_column_present_in_both_splits(self, processed_splits):
        """Target column must appear in both processed splits."""
        train_df, test_df = processed_splits
        assert TARGET_COL in train_df.columns, (
            f"Target column '{TARGET_COL}' missing from train_df"
        )
        assert TARGET_COL in test_df.columns, (
            f"Target column '{TARGET_COL}' missing from test_df"
        )

    def test_no_nulls_in_features_after_preprocessing(
        self, processed_splits
    ):
        """
        No NaN values must remain in feature columns after the
        ColumnTransformer (imputation) is applied.
        """
        train_df, test_df = processed_splits
        feature_cols = [c for c in train_df.columns if c != TARGET_COL]

        train_nulls = train_df[feature_cols].isna().sum().sum()
        test_nulls = test_df[feature_cols].isna().sum().sum()

        assert train_nulls == 0, (
            f"NaN values remain in train features after preprocessing: "
            f"{train_nulls} nulls found."
        )
        assert test_nulls == 0, (
            f"NaN values remain in test features after preprocessing: "
            f"{test_nulls} nulls found."
        )

    def test_train_larger_than_test(self, processed_splits):
        """Training split must be larger than test split (80/20)."""
        train_df, test_df = processed_splits
        assert len(train_df) > len(test_df), (
            f"Train split ({len(train_df)}) must be larger than "
            f"test split ({len(test_df)})."
        )

    def test_train_test_ratio_approx_80_20(self, processed_splits):
        """
        Train/test ratio must be approximately 80/20 (within ±2%).
        """
        train_df, test_df = processed_splits
        total = len(train_df) + len(test_df)
        train_ratio = len(train_df) / total
        assert 0.78 <= train_ratio <= 0.82, (
            f"Expected train ratio ~0.80, got {train_ratio:.3f}"
        )

    def test_target_column_is_binary(self, processed_splits):
        """Target column must contain only 0/1 values in both splits."""
        train_df, test_df = processed_splits
        for name, df in [("train", train_df), ("test", test_df)]:
            unique_vals = set(df[TARGET_COL].unique())
            assert unique_vals.issubset({0, 1}), (
                f"Target column in {name}_df must be binary (0/1), "
                f"found: {unique_vals}"
            )

    def test_all_feature_columns_are_numeric(self, processed_splits):
        """
        After preprocessing all feature columns must be numeric (float/int).
        This specifically catches the age string-band / XGBoost object-dtype
        bug — if age is not OHE-encoded properly this test will fail.
        """
        train_df, _ = processed_splits
        feature_cols = [c for c in train_df.columns if c != TARGET_COL]
        non_numeric = [
            c for c in feature_cols
            if not pd.api.types.is_numeric_dtype(train_df[c])
        ]
        assert len(non_numeric) == 0, (
            f"Non-numeric feature columns found after preprocessing: "
            f"{non_numeric}. Check CATEGORICAL_FEATURES OHE encoding."
        )

    def test_preprocessor_artifact_saved(self):
        """
        The fitted preprocessor must be persisted to disk during
        make features so that api.py and flask_app.py can reload it.
        """
        from src.config import PREPROCESSOR_PATH
        assert PREPROCESSOR_PATH.exists(), (
            f"Preprocessor artifact not found at '{PREPROCESSOR_PATH}'. "
            "Run `make features` to generate it."
        )

    def test_feature_count_matches_config(self, processed_splits):
        """
        The number of feature columns must be greater than the number of
        raw input features (OHE expands categoricals into multiple columns).
        """
        train_df, _ = processed_splits
        feature_cols = [c for c in train_df.columns if c != TARGET_COL]
        raw_feature_count = (
            len(NUMERIC_FEATURES)
            + len(BINARY_FLAG_FEATURES)
            + len(CATEGORICAL_FEATURES)
        )
        # After OHE the total must exceed the raw count
        assert len(feature_cols) > raw_feature_count, (
            f"Expected more features after OHE expansion. "
            f"Got {len(feature_cols)}, raw config count={raw_feature_count}."
        )
