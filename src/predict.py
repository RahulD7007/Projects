"""
predict.py
──────────
Entry-point for batch prediction inference.

Loads the champion Random Forest model from the versioning registry,
scores all rows in the processed test set, and prints a sample of
the output to stdout.

Usage
─────
    python -m src.predict
    make predict
"""

from __future__ import annotations

import sys

import pandas as pd

from src.config import TARGET_COL, TEST_PROCESSED_PATH
from src.logger import get_logger
from src.modeling.predict import load_champion, predict_proba   # ← correct imports

logger = get_logger(__name__)


def main() -> None:
    logger.info("Batch prediction inference started.")

    # ── Load processed test data ──────────────────────────────────────────────
    logger.info("Loading test dataset from '%s'", TEST_PROCESSED_PATH)
    try:
        test_df = pd.read_csv(TEST_PROCESSED_PATH)
    except FileNotFoundError as exc:
        logger.critical("Test data not found: %s", exc)
        print(
            f"[ERROR] Test data not found: {exc}\n"
            "Run `make features` first.",
            file=sys.stderr,
        )
        sys.exit(1)

    logger.info("Test dataset loaded | %d rows", len(test_df))

    # ── Load champion model from registry ────────────────────────────────────
    logger.info("Loading champion model from versioning registry...")
    try:
        from src.config import MODEL_NAME_RF
        model = load_champion(MODEL_NAME_RF)
    except (FileNotFoundError, KeyError) as exc:
        logger.error("Champion model could not be loaded: %s", exc)
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)

    # ── Run batch inference ───────────────────────────────────────────────────
    logger.info("Running batch inference on %d samples...", len(test_df))
    results = predict_proba(model, test_df)
    logger.info(
        "Inference complete | predicted_defaults=%d / %d (%.2f%%)",
        results["Predicted_Status"].sum(),
        len(results),
        100 * results["Predicted_Status"].mean(),
    )

    # ── Console output ────────────────────────────────────────────────────────
    print("=" * 60)
    print("BATCH PREDICTION INFERENCE")
    print("=" * 60)
    print(f"Evaluated {len(results):,} sample applications.")
    print("Sample Prediction Output:")
    print(results.head(10).to_string(index=True))
    print("=" * 60)

    logger.info("Batch prediction inference complete.")


if __name__ == "__main__":
    main()
