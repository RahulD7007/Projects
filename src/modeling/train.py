"""
modeling/train.py
─────────────────
Model training, evaluation, and serialization engine.

Supports
────────
• Logistic Regression  (interpretable baseline)
• Random Forest        (ensemble baseline)
• XGBoost              (gradient-boosted trees)

All trained models are automatically registered in the versioning
registry via src/versioning.py.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    roc_auc_score,
)
from xgboost import XGBClassifier

from src.config import (
    LR_PARAMS,
    MODEL_NAME_LR,
    MODEL_NAME_RF,
    MODEL_NAME_XGB,
    RF_PARAMS,
    TARGET_COL,
    XGB_PARAMS,
)
from src.logger import get_logger
from src.versioning import register_model

logger = get_logger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# INTERNAL HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _split_xy(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Return (X, y) numpy arrays from a processed DataFrame."""
    X = df.drop(columns=[TARGET_COL]).values
    y = df[TARGET_COL].values
    return X, y


def _evaluate(
    model: object,
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> dict[str, float]:
    """
    Compute standard binary-classification metrics.

    Parameters
    ----------
    model : object
        Fitted classifier with ``predict_proba`` and ``predict``.
    X_test : np.ndarray
        Feature matrix.
    y_test : np.ndarray
        Ground-truth labels.

    Returns
    -------
    dict[str, float]
        Keys: ``roc_auc``, ``pr_auc``, ``accuracy``, ``f1_score``.
    """
    y_prob = model.predict_proba(X_test)[:, 1]
    y_pred = (y_prob >= 0.5).astype(int)

    metrics = {
        "roc_auc":  round(float(roc_auc_score(y_test, y_prob)), 4),
        "pr_auc":   round(float(average_precision_score(y_test, y_prob)), 4),
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "f1_score": round(float(f1_score(y_test, y_pred)), 4),
    }

    logger.debug("Evaluation metrics: %s", metrics)
    return metrics


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC TRAINING FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def train_logistic_regression(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    register: bool = True,
    promote_to_champion: bool = False,
) -> tuple[LogisticRegression, dict[str, float], str]:
    """
    Fit Logistic Regression and optionally register in the model registry.

    Parameters
    ----------
    train_df : pd.DataFrame
        Processed training DataFrame.
    test_df : pd.DataFrame
        Processed test DataFrame.
    register : bool
        Whether to register this run in the versioning registry.
    promote_to_champion : bool
        Whether to promote this version as champion.

    Returns
    -------
    tuple[LogisticRegression, dict, str]
        ``(fitted_model, metrics_dict, version_tag)``
    """
    logger.info("Training Logistic Regression | params=%s", LR_PARAMS)
    X_train, y_train = _split_xy(train_df)
    X_test, y_test = _split_xy(test_df)

    model = LogisticRegression(**LR_PARAMS)
    model.fit(X_train, y_train)
    logger.info("Logistic Regression training complete.")

    metrics = _evaluate(model, X_test, y_test)
    logger.info(
        "LR Results → ROC-AUC: %.4f | PR-AUC: %.4f | "
        "Accuracy: %.4f | F1: %.4f",
        metrics["roc_auc"], metrics["pr_auc"],
        metrics["accuracy"], metrics["f1_score"],
    )

    version = "not_registered"
    if register:
        version = register_model(
            model=model,
            model_name=MODEL_NAME_LR,
            metrics=metrics,
            params=LR_PARAMS,
            n_train=len(train_df),
            n_test=len(test_df),
            promote_to_champion=promote_to_champion,
        )

    return model, metrics, version


def train_random_forest(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    register: bool = True,
    promote_to_champion: bool = False,
) -> tuple[RandomForestClassifier, dict[str, float], str]:
    """
    Fit Random Forest and optionally register in the model registry.

    Parameters
    ----------
    train_df : pd.DataFrame
        Processed training DataFrame.
    test_df : pd.DataFrame
        Processed test DataFrame.
    register : bool
        Whether to register this run in the versioning registry.
    promote_to_champion : bool
        Whether to promote this version as champion.

    Returns
    -------
    tuple[RandomForestClassifier, dict, str]
        ``(fitted_model, metrics_dict, version_tag)``
    """
    logger.info("Training Random Forest | params=%s", RF_PARAMS)
    X_train, y_train = _split_xy(train_df)
    X_test, y_test = _split_xy(test_df)

    model = RandomForestClassifier(**RF_PARAMS)
    model.fit(X_train, y_train)
    logger.info("Random Forest training complete.")

    metrics = _evaluate(model, X_test, y_test)
    logger.info(
        "RF Results → ROC-AUC: %.4f | PR-AUC: %.4f | "
        "Accuracy: %.4f | F1: %.4f",
        metrics["roc_auc"], metrics["pr_auc"],
        metrics["accuracy"], metrics["f1_score"],
    )

    version = "not_registered"
    if register:
        version = register_model(
            model=model,
            model_name=MODEL_NAME_RF,
            metrics=metrics,
            params=RF_PARAMS,
            n_train=len(train_df),
            n_test=len(test_df),
            promote_to_champion=promote_to_champion,
        )

    return model, metrics, version


def train_xgboost(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    register: bool = True,
    promote_to_champion: bool = False,
) -> tuple[XGBClassifier, dict[str, float], str]:
    """
    Fit XGBoost and optionally register in the model registry.

    Parameters
    ----------
    train_df : pd.DataFrame
        Processed training DataFrame.
    test_df : pd.DataFrame
        Processed test DataFrame.
    register : bool
        Whether to register this run in the versioning registry.
    promote_to_champion : bool
        Whether to promote this version as champion.

    Returns
    -------
    tuple[XGBClassifier, dict, str]
        ``(fitted_model, metrics_dict, version_tag)``
    """
    logger.info("Training XGBoost | params=%s", XGB_PARAMS)
    X_train, y_train = _split_xy(train_df)
    X_test, y_test = _split_xy(test_df)

    # XGBoost handles missing values natively — no special treatment needed
    xgb_params = {k: v for k, v in XGB_PARAMS.items()
                  if k != "use_label_encoder"}
    model = XGBClassifier(**xgb_params, verbosity=0)
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False,
    )
    logger.info("XGBoost training complete.")

    metrics = _evaluate(model, X_test, y_test)
    logger.info(
        "XGB Results → ROC-AUC: %.4f | PR-AUC: %.4f | "
        "Accuracy: %.4f | F1: %.4f",
        metrics["roc_auc"], metrics["pr_auc"],
        metrics["accuracy"], metrics["f1_score"],
    )

    version = "not_registered"
    if register:
        version = register_model(
            model=model,
            model_name=MODEL_NAME_XGB,
            metrics=metrics,
            params=XGB_PARAMS,
            n_train=len(train_df),
            n_test=len(test_df),
            promote_to_champion=promote_to_champion,
        )

    return model, metrics, version


def serialize_model(model: object, path=None) -> None:
    """
    Persist a fitted model to disk via joblib (legacy compatibility).

    For new workflows, prefer ``register_model()`` via ``src.versioning``.

    Parameters
    ----------
    model : object
        Any scikit-learn / XGBoost compatible fitted estimator.
    path : Path | None
        Destination path. Defaults to ``MODEL_PATH`` from config.
    """
    import joblib
    from src.config import MODEL_PATH
    target = path or MODEL_PATH
    joblib.dump(model, target, compress=3)
    logger.info("Serialized model artifact → '%s'", target)
