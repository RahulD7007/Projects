"""
api.py
──────
Single-application CLI scoring API wrapper.

Key change
──────────
Replaced run_preprocessing_pipeline() (which re-fits a ColumnTransformer
on just 1-2 rows) with load_preprocessor() which reloads the transformer
fitted on the full 118,936-row training split during ``make features``.
This guarantees that OHE categories, imputation medians, and scaler
statistics are always consistent with the training distribution, and
eliminates the XGBoost object-dtype error.
"""

from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

from src.config import (
    MODEL_NAME_RF,
    RISK_SCORE_CEILING,
    RISK_SCORE_FLOOR,
    TARGET_COL,
)
from src.features import execute_feature_engineering, load_preprocessor
from src.logger import get_logger
from src.modeling.predict import load_champion, predict_proba

logger = get_logger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# SAMPLE APPLICATION
# ─────────────────────────────────────────────────────────────────────────────
SAMPLE_APPLICATION: dict = {
    "ID":                          "APP-2024-001",
    "loan_amount":                 420_000,
    "property_value":              np.nan,        # Missing → high-risk flag
    "income":                      52_000,
    "Credit_Score":                580,
    "LTV":                         97.0,
    "dtir1":                       np.nan,        # Missing → high-risk flag
    "term":                        360,
    "age":                         "35-44",
    "loan_type":                   "type1",
    "loan_purpose":                "p1",
    "Credit_Worthiness":           "l1",
    "occupancy_type":              "pr",
    "Neg_ammortization":           "not_neg",
    "interest_only":               "not_int",
    "lump_sum_payment":            "not_lpsm",
    "construction_type":           "sb",
    "Secured_by":                  "home",
    "total_units":                 "1U",
    "co-applicant_credit_type":    "EXP",
    "submission_of_application":   "to_inst",
    "Region":                      "south",
}


# ─────────────────────────────────────────────────────────────────────────────
# SCORING HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _prob_to_risk_score(prob: float) -> int:
    """Map [0, 1] default probability → [100, 200] internal risk score."""
    score = RISK_SCORE_FLOOR + int(
        prob * (RISK_SCORE_CEILING - RISK_SCORE_FLOOR)
    )
    return int(np.clip(score, RISK_SCORE_FLOOR, RISK_SCORE_CEILING))


def _recommendation(prob: float) -> str:
    """Return underwriting recommendation string."""
    if prob < 0.30:
        return "APPROVE / LOW RISK"
    elif prob < 0.55:
        return "REFER / MANUAL REVIEW"
    return "REJECT / HIGH RISK"


def score_application(application: dict) -> dict:
    """
    Score a single raw loan application dictionary.

    Processing steps
    ────────────────
    1. Build a single-row DataFrame from the application dict.
    2. Apply deterministic feature engineering (flags, ratios).
    3. Load the persisted fitted ColumnTransformer.
    4. Transform the single row (no re-fitting — avoids object-dtype error).
    5. Load the champion model and run inference.

    Parameters
    ----------
    application : dict
        Raw application fields (mirrors CSV columns minus target).

    Returns
    -------
    dict
        Keys: default_probability, underwriting_recommendation, risk_score.
    """
    # ── 1. Build single-row DataFrame ────────────────────────────────────────
    df_raw = pd.DataFrame([application])

    # ── 2. Feature engineering ────────────────────────────────────────────────
    # Add dummy target so execute_feature_engineering works; stripped later.
    df_raw[TARGET_COL] = 0
    df_engineered = execute_feature_engineering(df_raw)

    # Drop the target column before transforming
    X_raw = df_engineered.drop(columns=[TARGET_COL])

    # ── 3. Load the persisted fitted preprocessor ─────────────────────────────
    # This transformer was fitted on 118,936 training rows during
    # `make features`. All OHE categories and scaler statistics match
    # the training distribution exactly.
    preprocessor = load_preprocessor()

    # ── 4. Transform single row (no fit — transform only) ────────────────────
    X_arr = preprocessor.transform(X_raw)
    feature_names = preprocessor.get_feature_names_out().tolist()
    X_df = pd.DataFrame(X_arr, columns=feature_names)

    # ── 5. Load champion model and score ─────────────────────────────────────
    model = load_champion(MODEL_NAME_RF)
    result = predict_proba(model, X_df)
    prob = float(result["Predicted_Default_Prob"].iloc[0])

    logger.info(
        "Application scored | prob=%.4f | recommendation=%s",
        prob,
        _recommendation(prob),
    )

    return {
        "default_probability":         round(prob, 4),
        "underwriting_recommendation": _recommendation(prob),
        "risk_score":                  _prob_to_risk_score(prob),
    }


# ─────────────────────────────────────────────────────────────────────────────
# STANDALONE ENTRY-POINT
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    logger.info("CLI API inference started.")
    try:
        response = score_application(SAMPLE_APPLICATION)
    except Exception as exc:
        logger.error("Scoring failed: %s", exc, exc_info=True)
        print(f"[ERROR] Scoring failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("SAMPLE API INFERENCE RESPONSE")
    print("=" * 60)
    print(json.dumps(response, indent=2))
    print("=" * 60)

    logger.info("CLI API inference complete.")


if __name__ == "__main__":
    main()
