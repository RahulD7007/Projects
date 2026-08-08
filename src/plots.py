"""
plots.py
────────
Reusable, side-effect-free plotting routines.

New additions
─────────────
• plot_roc_curve_comparison   – overlay ROC curves for multiple models
• plot_pr_curve_comparison    – overlay PR curves for multiple models
• plot_metrics_comparison_bar – grouped bar chart across all models & metrics
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    RocCurveDisplay,
    auc,
    confusion_matrix,
    precision_recall_curve,
    roc_curve,
)

from src.logger import get_logger

logger = get_logger(__name__)

_STYLE = "seaborn-v0_8-whitegrid"
_FIG_DPI = 150

# Consistent colour palette for multi-model plots
_PALETTE = {
    "Logistic Regression": "#2563EB",   # Blue
    "Random Forest":       "#16A34A",   # Green
    "XGBoost":             "#DC2626",   # Red
}
_DEFAULT_COLOUR = "#7C3AED"             # Purple fallback


def plot_roc_curve(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    roc_auc: float,
    save_path: Path,
    model_name: str = "Model",
) -> None:
    """
    Generate and save a single-model ROC curve.

    Parameters
    ----------
    y_true : np.ndarray
        Ground-truth binary labels.
    y_prob : np.ndarray
        Predicted positive-class probabilities.
    roc_auc : float
        Pre-computed ROC-AUC for annotation.
    save_path : Path
        Output file path.
    model_name : str
        Model label for legend.
    """
    colour = _PALETTE.get(model_name, _DEFAULT_COLOUR)
    with plt.style.context(_STYLE):
        fig, ax = plt.subplots(figsize=(7, 6), dpi=_FIG_DPI)
        RocCurveDisplay.from_predictions(
            y_true, y_prob,
            name=f"{model_name} (AUC = {roc_auc:.4f})",
            ax=ax, color=colour,
        )
        ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Random Classifier")
        ax.set_title(f"ROC Curve — {model_name}", fontweight="bold")
        ax.legend(loc="lower right")
        fig.tight_layout()
        fig.savefig(save_path, dpi=_FIG_DPI)
        plt.close(fig)
    logger.debug("Saved ROC curve → %s", save_path)


def plot_pr_curve(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    pr_auc: float,
    save_path: Path,
    model_name: str = "Model",
) -> None:
    """
    Generate and save a single-model Precision-Recall curve.

    Parameters
    ----------
    y_true : np.ndarray
        Ground-truth binary labels.
    y_prob : np.ndarray
        Predicted positive-class probabilities.
    pr_auc : float
        Pre-computed PR-AUC for annotation.
    save_path : Path
        Output file path.
    model_name : str
        Model label for legend.
    """
    colour = _PALETTE.get(model_name, _DEFAULT_COLOUR)
    with plt.style.context(_STYLE):
        fig, ax = plt.subplots(figsize=(7, 6), dpi=_FIG_DPI)
        PrecisionRecallDisplay.from_predictions(
            y_true, y_prob,
            name=f"{model_name} (AP = {pr_auc:.4f})",
            ax=ax, color=colour,
        )
        ax.set_title(
            f"Precision-Recall Curve — {model_name}", fontweight="bold")
        ax.legend(loc="upper right")
        fig.tight_layout()
        fig.savefig(save_path, dpi=_FIG_DPI)
        plt.close(fig)
    logger.debug("Saved PR curve → %s", save_path)


def plot_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    save_path: Path,
    model_name: str = "Model",
) -> None:
    """
    Generate and save a confusion matrix heatmap.

    Parameters
    ----------
    y_true : np.ndarray
        Ground-truth binary labels.
    y_pred : np.ndarray
        Binary predictions.
    save_path : Path
        Output file path.
    model_name : str
        Model label for the plot title.
    """
    with plt.style.context(_STYLE):
        fig, ax = plt.subplots(figsize=(6, 5), dpi=_FIG_DPI)
        cm = confusion_matrix(y_true, y_pred)
        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm,
            display_labels=["No Default (0)", "Default (1)"],
        )
        disp.plot(ax=ax, colorbar=False, cmap="Blues")
        ax.set_title(
            f"Confusion Matrix — {model_name}", fontweight="bold"
        )
        fig.tight_layout()
        fig.savefig(save_path, dpi=_FIG_DPI)
        plt.close(fig)
    logger.debug("Saved confusion matrix → %s", save_path)


def plot_feature_importance(
    feature_names: list[str],
    importances: np.ndarray,
    top_n: int = 20,
    save_path: Path | None = None,
    model_name: str = "Model",
) -> None:
    """
    Generate and save a horizontal bar chart of top-N feature importances.

    Parameters
    ----------
    feature_names : list[str]
        All feature names aligned with ``importances``.
    importances : np.ndarray
        Gini / MDI importance values.
    top_n : int
        Number of top features to display.
    save_path : Path | None
        If provided, saves the figure; otherwise displays it.
    model_name : str
        Model label for the plot title.
    """
    indices = np.argsort(importances)[::-1][:top_n]
    top_names = [feature_names[i] for i in indices]
    top_vals = importances[indices]
    colour = _PALETTE.get(model_name, _DEFAULT_COLOUR)

    with plt.style.context(_STYLE):
        fig, ax = plt.subplots(figsize=(9, 7), dpi=_FIG_DPI)
        y_pos = np.arange(len(top_names))
        ax.barh(y_pos, top_vals[::-1], color=colour, edgecolor="white")
        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_names[::-1], fontsize=9)
        ax.set_xlabel("Mean Decrease in Impurity (MDI)", fontsize=10)
        ax.set_title(
            f"Top {top_n} Feature Importances — {model_name}",
            fontweight="bold",
        )
        fig.tight_layout()

        if save_path is not None:
            fig.savefig(save_path, dpi=_FIG_DPI)
            plt.close(fig)
            logger.debug("Saved feature importance → %s", save_path)
        else:
            plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# MULTI-MODEL COMPARISON PLOTS
# ─────────────────────────────────────────────────────────────────────────────

def plot_roc_curve_comparison(
    y_true: np.ndarray,
    model_probs: dict[str, np.ndarray],
    save_path: Path,
) -> None:
    """
    Overlay ROC curves for multiple models on a single axes.

    Parameters
    ----------
    y_true : np.ndarray
        Ground-truth binary labels.
    model_probs : dict[str, np.ndarray]
        Mapping of ``{model_display_name: y_prob_array}``.
    save_path : Path
        Output file path.
    """
    with plt.style.context(_STYLE):
        fig, ax = plt.subplots(figsize=(8, 7), dpi=_FIG_DPI)

        for model_name, y_prob in model_probs.items():
            fpr, tpr, _ = roc_curve(y_true, y_prob)
            roc_auc_val = auc(fpr, tpr)
            colour = _PALETTE.get(model_name, _DEFAULT_COLOUR)
            ax.plot(
                fpr, tpr,
                label=f"{model_name} (AUC = {roc_auc_val:.4f})",
                color=colour, linewidth=2,
            )

        ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Random Classifier")
        ax.set_xlabel("False Positive Rate", fontsize=11)
        ax.set_ylabel("True Positive Rate", fontsize=11)
        ax.set_title("ROC Curve Comparison — All Models",
                     fontweight="bold", fontsize=13)
        ax.legend(loc="lower right", fontsize=10)
        fig.tight_layout()
        fig.savefig(save_path, dpi=_FIG_DPI)
        plt.close(fig)
    logger.debug("Saved ROC comparison → %s", save_path)


def plot_pr_curve_comparison(
    y_true: np.ndarray,
    model_probs: dict[str, np.ndarray],
    save_path: Path,
) -> None:
    """
    Overlay Precision-Recall curves for multiple models on a single axes.

    Parameters
    ----------
    y_true : np.ndarray
        Ground-truth binary labels.
    model_probs : dict[str, np.ndarray]
        Mapping of ``{model_display_name: y_prob_array}``.
    save_path : Path
        Output file path.
    """
    with plt.style.context(_STYLE):
        fig, ax = plt.subplots(figsize=(8, 7), dpi=_FIG_DPI)

        for model_name, y_prob in model_probs.items():
            precision, recall, _ = precision_recall_curve(y_true, y_prob)
            pr_auc_val = auc(recall, precision)
            colour = _PALETTE.get(model_name, _DEFAULT_COLOUR)
            ax.plot(
                recall, precision,
                label=f"{model_name} (AP = {pr_auc_val:.4f})",
                color=colour, linewidth=2,
            )

        ax.set_xlabel("Recall", fontsize=11)
        ax.set_ylabel("Precision", fontsize=11)
        ax.set_title(
            "Precision-Recall Curve Comparison — All Models",
            fontweight="bold", fontsize=13,
        )
        ax.legend(loc="upper right", fontsize=10)
        fig.tight_layout()
        fig.savefig(save_path, dpi=_FIG_DPI)
        plt.close(fig)
    logger.debug("Saved PR comparison → %s", save_path)


def plot_metrics_comparison_bar(
    all_metrics: dict[str, dict],
    save_path: Path,
) -> None:
    """
    Grouped bar chart comparing ROC-AUC, PR-AUC, Accuracy, and F1
    across all evaluated models.

    Parameters
    ----------
    all_metrics : dict[str, dict]
        Mapping of ``{model_display_name: metrics_dict}``.
    save_path : Path
        Output file path.
    """
    metric_keys = ["roc_auc", "pr_auc", "accuracy", "f1_score"]
    metric_labels = ["ROC-AUC", "PR-AUC", "Accuracy", "F1 Score"]
    model_names = list(all_metrics.keys())
    n_models = len(model_names)
    n_metrics = len(metric_keys)

    x = np.arange(n_metrics)
    bar_width = 0.25
    offsets = np.linspace(
        -(n_models - 1) * bar_width / 2,
        (n_models - 1) * bar_width / 2,
        n_models,
    )

    with plt.style.context(_STYLE):
        fig, ax = plt.subplots(figsize=(11, 7), dpi=_FIG_DPI)

        for idx, model_name in enumerate(model_names):
            values = [
                all_metrics[model_name].get(k, 0.0)
                for k in metric_keys
            ]
            colour = _PALETTE.get(model_name, _DEFAULT_COLOUR)
            bars = ax.bar(
                x + offsets[idx],
                values,
                width=bar_width,
                label=model_name,
                color=colour,
                edgecolor="white",
                alpha=0.88,
            )
            # Value annotation on top of each bar
            for bar, val in zip(bars, values):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.005,
                    f"{val:.3f}",
                    ha="center", va="bottom",
                    fontsize=8, fontweight="bold",
                )

        ax.set_xticks(x)
        ax.set_xticklabels(metric_labels, fontsize=11)
        ax.set_ylabel("Score", fontsize=11)
        ax.set_ylim(0, 1.12)
        ax.set_title(
            "Model Performance Comparison — All Metrics",
            fontweight="bold", fontsize=13,
        )
        ax.legend(loc="upper right", fontsize=10)
        fig.tight_layout()
        fig.savefig(save_path, dpi=_FIG_DPI)
        plt.close(fig)
    logger.debug("Saved metrics comparison bar chart → %s", save_path)
