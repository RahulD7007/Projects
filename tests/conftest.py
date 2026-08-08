"""
conftest.py
───────────
Shared Pytest fixtures available across all test modules.

Fixture hierarchy (session-scoped for performance)
───────────────────────────────────────────────────
raw_df
    └── engineered_df
            └── processed_splits
                    ├── fitted_model
                    └── test_processed
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.config import TARGET_COL

# ─────────────────────────────────────────────────────────────────────────────
# RAW DATA FIXTURE
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def raw_df() -> pd.DataFrame:
    """
    Load the raw dataset once per test session.

    Scope: session — loaded from disk exactly once; reused by all tests.
    """
    from src.dataset import load_raw_data
    return load_raw_data()
# ─────────────────────────────────────────────────────────────────────────────
# FEATURE ENGINEERING FIXTURE
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def engineered_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Return the feature-engineered DataFrame (pre-split, pre-preprocessing).

    Applies execute_feature_engineering() to the raw dataset:
    - Drops leakage columns
    - Creates missingness flags
    - Creates DTI_x_LTV and loan_to_income features

    Scope: session — computed once, shared across all test modules.
    """
    from src.features import execute_feature_engineering
    return execute_feature_engineering(raw_df)
# ─────────────────────────────────────────────────────────────────────────────
# PREPROCESSING PIPELINE FIXTURES
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def processed_splits(
    engineered_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Return (train_processed, test_processed) DataFrames.

    Applies the full ColumnTransformer pipeline:
    - Stratified 80/20 train/test split
    - Fits ColumnTransformer on training data only
    - Returns both processed DataFrames with target column

    Scope: session — fitted once, shared across all test modules.
    """
    from src.features import run_preprocessing_pipeline
    return run_preprocessing_pipeline(engineered_df)


@pytest.fixture(scope="session")
def train_processed(
    processed_splits: tuple[pd.DataFrame, pd.DataFrame],
) -> pd.DataFrame:
    """Return only the training processed DataFrame."""
    train_df, _ = processed_splits
    return train_df


@pytest.fixture(scope="session")
def test_processed(
    processed_splits: tuple[pd.DataFrame, pd.DataFrame],
) -> pd.DataFrame:
    """Return only the test processed DataFrame."""
    _, test_df = processed_splits
    return test_df


# ─────────────────────────────────────────────────────────────────────────────
# MODEL FIXTURES
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def fitted_model(
    processed_splits: tuple[pd.DataFrame, pd.DataFrame],
):
    """
    Train and return a fitted Random Forest model.

    Trains on the processed training split. Used by test_modeling.py
    and test_versioning.py.

    Scope: session — trained once, shared across all test modules.
    """
    from src.modeling.train import train_random_forest
    train_df, test_df = processed_splits
    model, _, _ = train_random_forest(
        train_df,
        test_df,
        register=False,           # do not pollute the registry during tests
        promote_to_champion=False,
    )
    return model


@pytest.fixture(scope="session")
def fitted_lr_model(
    processed_splits: tuple[pd.DataFrame, pd.DataFrame],
):
    """
    Train and return a fitted Logistic Regression model.

    Scope: session — trained once, shared across all test modules.
    """
    from src.modeling.train import train_logistic_regression
    train_df, test_df = processed_splits
    model, _, _ = train_logistic_regression(
        train_df,
        test_df,
        register=False,
        promote_to_champion=False,
    )
    return model


@pytest.fixture(scope="session")
def fitted_xgb_model(
    processed_splits: tuple[pd.DataFrame, pd.DataFrame],
):
    """
    Train and return a fitted XGBoost model.

    Scope: session — trained once, shared across all test modules.
    """
    from src.modeling.train import train_xgboost
    train_df, test_df = processed_splits
    model, _, _ = train_xgboost(
        train_df,
        test_df,
        register=False,
        promote_to_champion=False,
    )
    return model


# ─────────────────────────────────────────────────────────────────────────────
# SAMPLE DATA FIXTURES
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def sample_raw_dataframe() -> pd.DataFrame:
    """
    Return a small synthetic raw DataFrame for lightweight unit tests
    that do not need the full 148,670-row dataset.

    Contains all required raw columns including 'age' as string bands.
    """
    return pd.DataFrame({
        "ID":                          ["APP-001", "APP-002", "APP-003"],
        "loan_amount":                 [250_000,   420_000,   310_000],
        "property_value":              [320_000,   np.nan,    380_000],
        "income":                      [85_000,    52_000,    71_000],
        "Credit_Score":                [720,       580,       660],
        "LTV":                         [78.0,      97.0,      81.5],
        "dtir1":                       [28.5,      np.nan,    38.0],
        "term":                        [360,       360,       180],
        "age":                         ["35-44",   "45-54",   "55-64"],
        "loan_type":                   ["type1",   "type1",   "type2"],
        "loan_purpose":                ["p1",      "p1",      "p3"],
        "Credit_Worthiness":           ["l1",      "l1",      "l1"],
        "occupancy_type":              ["pr",      "pr",      "pr"],
        "Neg_ammortization":           ["not_neg", "not_neg", "not_neg"],
        "interest_only":               ["not_int", "not_int", "not_int"],
        "lump_sum_payment":            ["not_lpsm", "not_lpsm", "not_lpsm"],
        "construction_type":           ["sb",      "sb",      "sb"],
        "Secured_by":                  ["home",    "home",    "home"],
        "total_units":                 ["1U",      "1U",      "1U"],
        "co-applicant_credit_type":    ["EXP",     "EXP",     "EXP"],
        "submission_of_application":   ["to_inst", "to_inst", "to_inst"],
        "Region":                      ["south",   "south",   "north"],
        "rate_of_interest":            [3.5,       np.nan,    4.2],
        "Interest_rate_spread":        [1.2,       np.nan,    1.5],
        "Upfront_charges":             [1500,      np.nan,    1800],
        TARGET_COL:                    [0,         1,         0],
    })
