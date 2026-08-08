"""
modeling/predict.py
───────────────────
Inference engine: loads a serialized or registered model and scores
new observations.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.config import DECISION_THRESHOLD, MODEL_PATH, TARGET_COL
from src.logger import get_logger

logger = get_logger(__name__)


def load_model(path: Path = MODEL_PATH) -> object:
    """
    Load a serialized model artifact from a direct file path.

    Parameters
    ----------
    path : Path
        Path to the ``.joblib`` file.

    Returns
    -------
    object
        Fitted scikit-learn / XGBoost estimator.

    Raises
    ------
    FileNotFoundError
        If the artifact is absent from disk.
    """
    import joblib

    if not path.exists():
        logger.error("Model artifact not found at '%s'", path)
        raise FileNotFoundError(
            f"Model artifact not found at '{path}'. "
            "Run `make train` to generate it."
        )
    logger.info("Loading model artifact from '%s'", path)
    return joblib.load(path)


def load_champion(model_name: str) -> object:
    """
    Load the current champion model from the versioning registry.

    Parameters
    ----------
    model_name : str
        Logical model name (e.g. ``"random_forest"``).

    Returns
    -------
    object
        Deserialized fitted estimator.
    """
    from src.versioning import load_champion_model
    logger.info("Loading champion model: '%s'", model_name)
    return load_champion_model(model_name)


def predict_proba(
    model: object,
    df: pd.DataFrame,
    threshold: float = DECISION_THRESHOLD,
) -> pd.DataFrame:
    """
    Generate default probabilities and binary predictions.

    Parameters
    ----------
    model : object
        Fitted classifier with ``predict_proba``.
    df : pd.DataFrame
        Processed feature DataFrame (target column dropped if present).
    threshold : float
        Classification cutoff (default 0.50).

    Returns
    -------
    pd.DataFrame
        Two-column frame: ``Predicted_Default_Prob``, ``Predicted_Status``.
    """
    X = df.drop(columns=[TARGET_COL], errors="ignore").values

    logger.debug(
        "Running inference on %d samples with threshold=%.2f",
        len(X), threshold,
    )

    proba: np.ndarray = model.predict_proba(X)[:, 1]
    labels = (proba >= threshold).astype(int)

    logger.debug(
        "Inference complete | mean_prob=%.4f | predicted_defaults=%d",
        proba.mean(),
        labels.sum(),
    )

    return pd.DataFrame(
        {
            "Predicted_Default_Prob": proba,
            "Predicted_Status": labels,
        }
    )
