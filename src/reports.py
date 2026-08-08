"""
reports.py
──────────
Multi-model report and figure generation.

For each model (LR, RF, XGBoost):
    • reports/models/<model>/metrics.json
    • reports/models/<model>/figures/roc_curve.png
    • reports/models/<model>/figures/pr_curve.png
    • reports/models/<model>/figures/confusion_matrix.png
    • reports/models/<model>/figures/feature_importance.png  (tree models only)

Cross-model comparison:
    • reports/models/comparison/all_models_metrics.json
    • reports/models/comparison/figures/roc_curve_comparison.png
    • reports/models/comparison/figures/pr_curve_comparison.png
    • reports/models/comparison/figures/metrics_comparison_bar.png

Usage
─────
    python -m src.reports
    make reports
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    roc_auc_score,
)

from src.config import (
    ALL_METRICS_PATH,
    COMPARISON_REPORT_DIR,
    DECISION_THRESHOLD,
    LR_METRICS_PATH,
    LR_REPORT_DIR,
    MODEL_NAME_LR,
    MODEL_NAME_RF,
    MODEL_NAME_XGB,
    RF_METRICS_PATH,
    RF_REPORT_DIR,
    TARGET_COL,
    TEST_PROCESSED_PATH,
    XGB_METRICS_PATH,
    XGB_REPORT_DIR,
)
from src.logger import get_logger
from src.modeling.predict import predict_proba
from src.plots import (
    plot_confusion_matrix,
    plot_feature_importance,
    plot_metrics_comparison_bar,
    plot_pr_curve,
    plot_pr_curve_comparison,
    plot_roc_curve,
    plot_roc_curve_comparison,
)
from src.versioning import load_champion_model

logger = get_logger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _compute_metrics(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    y_pred: np.ndarray,
) -> dict:
    """Compute the full metrics dictionary for one model."""
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()

    return {
        "roc_auc":  round(float(roc_auc_score(y_true, y_prob)), 4),
        "pr_auc":   round(float(average_precision_score(y_true, y_prob)), 4),
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "f1_score": round(float(f1_score(y_true, y_pred)), 4),
        "confusion_matrix": {
            "true_negative":  int(tn),
            "false_positive": int(fp),
            "false_negative": int(fn),
            "true_positive":  int(tp),
        },
    }


def _save_metrics(metrics: dict, path: Path) -> None:
    """Persist a metrics dict as formatted JSON."""
    path.write_text(json.dumps(metrics, indent=2))
    logger.info("Metrics saved → '%s'", path)


def _generate_single_model_report(
    model_name: str,
    model: object,
    y_true: np.ndarray,
    test_df: pd.DataFrame,
    report_dir: Path,
    metrics_path: Path,
) -> dict:
    """
    Generate all per-model artefacts (metrics + figures).

    Parameters
    ----------
    model_name : str
        Human-readable model name for plot titles.
    model : object
        Fitted classifier.
    y_true : np.ndarray
        Ground-truth labels.
    test_df : pd.DataFrame
        Processed test DataFrame.
    report_dir : Path
        Root directory for this model's reports.
    metrics_path : Path
        Destination path for the metrics JSON.

    Returns
    -------
    dict
        Computed metrics dictionary.
    """
    figures_dir = report_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    # ── Inference ─────────────────────────────────────────────────────────────
    results = predict_proba(model, test_df, threshold=DECISION_THRESHOLD)
    y_prob = results["Predicted_Default_Prob"].values
    y_pred = results["Predicted_Status"].values

    # ── Metrics ───────────────────────────────────────────────────────────────
    metrics = _compute_metrics(y_true, y_prob, y_pred)
    _save_metrics(metrics, metrics_path)

    # ── Figures ───────────────────────────────────────────────────────────────
    plot_roc_curve(
        y_true, y_prob, metrics["roc_auc"],
        save_path=figures_dir / "roc_curve.png",
        model_name=model_name,
    )
    plot_pr_curve(
        y_true, y_prob, metrics["pr_auc"],
        save_path=figures_dir / "pr_curve.png",
        model_name=model_name,
    )
    plot_confusion_matrix(
        y_true, y_pred,
        save_path=figures_dir / "confusion_matrix.png",
        model_name=model_name,
    )

    # Feature importance (tree-based models only)
    if hasattr(model, "feature_importances_"):
        feature_names = test_df.drop(columns=[TARGET_COL]).columns.tolist()
        plot_feature_importance(
            feature_names=feature_names,
            importances=model.feature_importances_,
            top_n=20,
            save_path=figures_dir / "feature_importance.png",
            model_name=model_name,
        )

    logger.info(
        "[%s] ROC-AUC=%.4f | PR-AUC=%.4f | Accuracy=%.4f | F1=%.4f",
        model_name,
        metrics["roc_auc"], metrics["pr_auc"],
        metrics["accuracy"], metrics["f1_score"],
    )
    return metrics


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY-POINT
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    logger.info("Report generation pipeline started.")

    # ── Load test data ────────────────────────────────────────────────────────
    try:
        test_df = pd.read_csv(TEST_PROCESSED_PATH)
    except FileNotFoundError as exc:
        logger.critical("Test data not found: %s", exc)
        print(f"[ERROR] {exc}\nRun `make features` first.", file=sys.stderr)
        sys.exit(1)

    y_true = test_df[TARGET_COL].values

    # Model registry: (registry_key, display_name, report_dir, metrics_path)
    model_configs = [
        (MODEL_NAME_LR,  "Logistic Regression", LR_REPORT_DIR,  LR_METRICS_PATH),
        (MODEL_NAME_RF,  "Random Forest",        RF_REPORT_DIR,  RF_METRICS_PATH),
        (MODEL_NAME_XGB, "XGBoost",              XGB_REPORT_DIR, XGB_METRICS_PATH),
    ]

    all_metrics: dict = {}
    all_probs:   dict = {}    # for comparison plots
    models_loaded: dict = {}

    # ── Per-model reports ─────────────────────────────────────────────────────
    for reg_key, display_name, report_dir, metrics_path in model_configs:
        logger.info("Generating report for: %s", display_name)
        try:
            model = load_champion_model(reg_key)
        except (KeyError, FileNotFoundError) as exc:
            logger.warning(
                "Skipping '%s' — champion not found: %s", display_name, exc
            )
            print(f"  [SKIP] {display_name}: {exc}")
            continue

        metrics = _generate_single_model_report(
            model_name=display_name,
            model=model,
            y_true=y_true,
            test_df=test_df,
            report_dir=report_dir,
            metrics_path=metrics_path,
        )
        all_metrics[display_name] = metrics

        # Collect probabilities for comparison plots
        results = predict_proba(model, test_df, threshold=DECISION_THRESHOLD)
        all_probs[display_name] = results["Predicted_Default_Prob"].values
        models_loaded[display_name] = model

    # ── Cross-model comparison ────────────────────────────────────────────────
    if len(all_metrics) > 1:
        logger.info("Generating cross-model comparison figures...")
        comp_figures = COMPARISON_REPORT_DIR / "figures"
        comp_figures.mkdir(parents=True, exist_ok=True)

        # Consolidated metrics JSON
        _save_metrics(all_metrics, ALL_METRICS_PATH)

        # ROC comparison
        plot_roc_curve_comparison(
            y_true=y_true,
            model_probs=all_probs,
            save_path=comp_figures / "roc_curve_comparison.png",
        )

        # PR comparison
        plot_pr_curve_comparison(
            y_true=y_true,
            model_probs=all_probs,
            save_path=comp_figures / "pr_curve_comparison.png",
        )

        # Metrics bar chart
        plot_metrics_comparison_bar(
            all_metrics=all_metrics,
            save_path=comp_figures / "metrics_comparison_bar.png",
        )

    # ── Console summary ───────────────────────────────────────────────────────
    sep = "=" * 70
    print(sep)
    print("MULTI-MODEL EVALUATION REPORT SUMMARY")
    print(sep)
    header = f"{'Model':<22} {'ROC-AUC':>10} {'PR-AUC':>10} {'Accuracy':>10} {'F1':>8}"
    print(header)
    print("-" * 62)
    for m_name, m_metrics in all_metrics.items():
        print(
            f"{m_name:<22} "
            f"{m_metrics['roc_auc']:>10.4f} "
            f"{m_metrics['pr_auc']:>10.4f} "
            f"{m_metrics['accuracy']:>10.4f} "
            f"{m_metrics['f1_score']:>8.4f}"
        )
    print(sep)
    print(f"Per-model figures saved under: '{COMPARISON_REPORT_DIR.parent}'")
    print(
        f"Comparison figures saved to:   '{COMPARISON_REPORT_DIR / 'figures'}'")
    logger.info("Report generation complete.")


if __name__ == "__main__":
    main()
