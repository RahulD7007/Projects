"""
train.py
────────
Entry-point for training all three models (LR, RF, XGBoost),
evaluating them, registering each in the versioning registry,
and persisting the best-performing model as the legacy artifact.

Usage
─────
    python -m src.train
    make train
"""

from __future__ import annotations

import sys

import pandas as pd

from src.config import (
    MODEL_NAME_LR,
    MODEL_NAME_RF,
    MODEL_NAME_XGB,
    MODEL_PATH,
    TARGET_COL,
    TEST_PROCESSED_PATH,
    TRAIN_PROCESSED_PATH,
)
from src.logger import get_logger
from src.modeling.train import (
    serialize_model,
    train_logistic_regression,
    train_random_forest,
    train_xgboost,
)

logger = get_logger(__name__)


def _best_model(results: dict) -> tuple[str, object]:
    """
    Select the model with the highest ROC-AUC.

    Parameters
    ----------
    results : dict
        Mapping of ``{model_name: (model_obj, metrics_dict, version_tag)}``.

    Returns
    -------
    tuple[str, object]
        ``(best_model_name, best_model_object)``
    """
    best_name = max(
        results,
        key=lambda k: results[k][1]["roc_auc"],
    )
    return best_name, results[best_name][0]


def main() -> None:
    logger.info("=" * 70)
    logger.info("MODEL TRAINING PIPELINE STARTED")
    logger.info("=" * 70)

    # ── Load processed artifacts ──────────────────────────────────────────────
    logger.info("Loading processed dataset artifacts...")
    try:
        train_df = pd.read_csv(TRAIN_PROCESSED_PATH)
        test_df = pd.read_csv(TEST_PROCESSED_PATH)
        logger.info(
            "Loaded train=%d rows | test=%d rows",
            len(train_df), len(test_df),
        )
    except FileNotFoundError as exc:
        logger.critical("Processed data not found: %s", exc)
        print(
            f"[ERROR] Processed data not found: {exc}\n"
            "Run `make features` first.",
            file=sys.stderr,
        )
        sys.exit(1)

    results: dict = {}

    # ── Train Logistic Regression ─────────────────────────────────────────────
    logger.info("─" * 50)
    print("Training Logistic Regression Classifier...")
    lr_model, lr_metrics, lr_ver = train_logistic_regression(
        train_df, test_df, register=True, promote_to_champion=True
    )
    results[MODEL_NAME_LR] = (lr_model, lr_metrics, lr_ver)

    # ── Train Random Forest ───────────────────────────────────────────────────
    logger.info("─" * 50)
    print("Training Random Forest Classifier...")
    rf_model, rf_metrics, rf_ver = train_random_forest(
        train_df, test_df, register=True, promote_to_champion=True
    )
    results[MODEL_NAME_RF] = (rf_model, rf_metrics, rf_ver)

    # ── Train XGBoost ─────────────────────────────────────────────────────────
    logger.info("─" * 50)
    print("Training XGBoost Classifier...")
    xgb_model, xgb_metrics, xgb_ver = train_xgboost(
        train_df, test_df, register=True, promote_to_champion=True
    )
    results[MODEL_NAME_XGB] = (xgb_model, xgb_metrics, xgb_ver)

    # ── Print consolidated results table ──────────────────────────────────────
    sep = "=" * 80
    print(sep)
    print("MODEL TRAINING & EVALUATION RESULTS")
    print(sep)

    header = f"{'Model':<22} {'Version':<8} {'ROC-AUC':>10} {'PR-AUC':>10} {'Accuracy':>10} {'F1':>8}"
    print(header)
    print("-" * 72)

    display_names = {
        MODEL_NAME_LR:  "Logistic Regression",
        MODEL_NAME_RF:  "Random Forest",
        MODEL_NAME_XGB: "XGBoost",
    }

    for name, (_, metrics, ver) in results.items():
        print(
            f"{display_names[name]:<22} {ver:<8} "
            f"{metrics['roc_auc']:>10.4f} {metrics['pr_auc']:>10.4f} "
            f"{metrics['accuracy']:>10.4f} {metrics['f1_score']:>8.4f}"
        )

    print(sep)

    # ── Serialize best model as legacy artifact ───────────────────────────────
    best_name, best_model = _best_model(results)
    serialize_model(best_model, path=MODEL_PATH)
    logger.info("Best model: '%s' serialized → '%s'", best_name, MODEL_PATH)
    print(f"\nBest Model : {display_names[best_name]}")
    print(f"Saved to   : '{MODEL_PATH}'")
    print(sep)

    logger.info("Training pipeline complete.")


if __name__ == "__main__":
    main()
