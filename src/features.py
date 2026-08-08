"""
features.py
───────────
Feature engineering and scikit-learn preprocessing pipeline.
(Logging added via src.logger)
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import (
    BINARY_FLAG_FEATURES,
    CATEGORICAL_FEATURES,
    ID_COL,
    LEAKAGE_COLS,
    MISSINGNESS_FLAG_COLS,
    NUMERIC_FEATURES,
    RANDOM_STATE,
    RAW_DATA_PATH,
    TARGET_COL,
    TEST_PROCESSED_PATH,
    TEST_SIZE,
    TRAIN_PROCESSED_PATH,
)
from src.dataset import load_raw_data
from src.logger import get_logger

logger = get_logger(__name__)


def execute_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all deterministic feature-engineering transformations.

    Steps
    ─────
    1. Drop leakage + ID columns.
    2. Create binary missingness flags.
    3. Construct DTI_x_LTV compound feature.
    4. Construct loan_to_income affordability ratio.
    """
    logger.debug("Starting feature engineering | shape=%s", df.shape)
    df = df.copy()

    # ── 1. Drop leakage + identifier ─────────────────────────────────────────
    drop_cols = [c for c in LEAKAGE_COLS + [ID_COL] if c in df.columns]
    if drop_cols:
        df.drop(columns=drop_cols, inplace=True)
        logger.debug("Dropped columns: %s", drop_cols)

    # ── 2. Missingness flags ──────────────────────────────────────────────────
    for col in MISSINGNESS_FLAG_COLS:
        if col in df.columns:
            flag_col = f"{col}_isna"
            df[flag_col] = df[col].isna().astype(np.int8)
            n_missing = df[flag_col].sum()
            logger.debug(
                "Flag '%s' created | %d missing (%.1f%%)",
                flag_col, n_missing,
                100 * n_missing / len(df),
            )

    # ── 3. DTI × LTV compound feature ────────────────────────────────────────
    if "dtir1" in df.columns and "LTV" in df.columns:
        df["DTI_x_LTV"] = df["dtir1"] * df["LTV"]
        logger.debug("Feature 'DTI_x_LTV' created.")

    # ── 4. Loan-to-income ratio ───────────────────────────────────────────────
    if "loan_amount" in df.columns and "income" in df.columns:
        df["loan_to_income"] = df["loan_amount"] / \
            df["income"].replace(0, np.nan)
        logger.debug("Feature 'loan_to_income' created.")

    logger.info("Feature engineering complete | output shape=%s", df.shape)
    return df


def build_preprocessing_pipeline() -> ColumnTransformer:
    """
    Construct a scikit-learn ColumnTransformer with three sub-pipelines.

    Returns
    -------
    ColumnTransformer
        Unfitted transformer.
    """
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler",  StandardScaler()),
    ])
    binary_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value=0)),
    ])
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False,
                dtype=np.float32,
            ),
        ),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric",     numeric_pipeline,     NUMERIC_FEATURES),
            ("binary",      binary_pipeline,      BINARY_FLAG_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )
    logger.debug("Preprocessing pipeline constructed.")
    return preprocessor


def run_preprocessing_pipeline(
    df_engineered: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data, fit the ColumnTransformer on training fold only,
    transform both folds, and return labelled DataFrames.
    """
    X = df_engineered.drop(columns=[TARGET_COL])
    y = df_engineered[TARGET_COL]

    logger.debug(
        "Splitting data | test_size=%.2f | random_state=%d",
        TEST_SIZE, RANDOM_STATE,
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=RANDOM_STATE,
    )
    logger.info(
        "Train=%d samples | Test=%d samples", len(X_train), len(X_test)
    )

    preprocessor = build_preprocessing_pipeline()
    logger.debug("Fitting ColumnTransformer on training data only...")
    X_train_arr = preprocessor.fit_transform(X_train)
    X_test_arr = preprocessor.transform(X_test)

    feature_names: list[str] = preprocessor.get_feature_names_out().tolist()
    logger.info("Preprocessing complete | %d features generated.",
                len(feature_names))

    train_processed = pd.DataFrame(
        X_train_arr, columns=feature_names, index=y_train.index
    )
    train_processed[TARGET_COL] = y_train.values

    test_processed = pd.DataFrame(
        X_test_arr, columns=feature_names, index=y_test.index
    )
    test_processed[TARGET_COL] = y_test.values

    return train_processed, test_processed


def main() -> None:
    logger.info("Feature engineering pipeline started.")
    print("Loading raw dataset...")
    df_raw = load_raw_data()

    print("Executing feature engineering...")
    df_engineered = execute_feature_engineering(df_raw)

    print("Fitting preprocessing pipeline on training split...")
    train_df, test_df = run_preprocessing_pipeline(df_engineered)

    train_df.to_csv(TRAIN_PROCESSED_PATH, index=False)
    test_df.to_csv(TEST_PROCESSED_PATH, index=False)

    sep = "=" * 80
    print(sep)
    print("FEATURE ENGINEERING & PREPROCESSING COMPLETE")
    print(sep)
    print(
        f"Train Artifact: '{TRAIN_PROCESSED_PATH}' "
        f"({train_df.shape[0]:,} rows x {train_df.shape[1]} cols)"
    )
    print(
        f"Test Artifact:  '{TEST_PROCESSED_PATH}' "
        f"({test_df.shape[0]:,} rows x {test_df.shape[1]} cols)"
    )
    print(sep)
    logger.info("Feature engineering pipeline complete.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        logger.critical("Feature pipeline failed: %s", exc, exc_info=True)
        sys.exit(1)
