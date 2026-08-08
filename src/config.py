"""
config.py
─────────
Centralized configuration: project paths, feature lists, pipeline
hyper-parameters, logging settings, and versioning constants.
"""

from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# ROOT & DIRECTORY PATHS
# ─────────────────────────────────────────────────────────────────────────────
ROOT_DIR: Path = Path(__file__).resolve().parents[1]

DATA_RAW_DIR: Path = ROOT_DIR / "data" / "raw"
DATA_INTERIM_DIR: Path = ROOT_DIR / "data" / "interim"
DATA_PROCESSED_DIR: Path = ROOT_DIR / "data" / "processed"
MODELS_DIR: Path = ROOT_DIR / "models"
REPORTS_DIR: Path = ROOT_DIR / "reports"
FIGURES_DIR: Path = REPORTS_DIR / "figures"
LOGS_DIR: Path = ROOT_DIR / "logs"

# ── NEW: per-model report directories ────────────────────────────────────────
MODEL_REPORTS_DIR: Path = REPORTS_DIR / "models"
LR_REPORT_DIR: Path = MODEL_REPORTS_DIR / "logistic_regression"
RF_REPORT_DIR: Path = MODEL_REPORTS_DIR / "random_forest"
XGB_REPORT_DIR: Path = MODEL_REPORTS_DIR / "xgboost"
COMPARISON_REPORT_DIR: Path = MODEL_REPORTS_DIR / "comparison"

# Ensure all output directories exist
for _dir in (
    DATA_INTERIM_DIR,
    DATA_PROCESSED_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    FIGURES_DIR,
    LOGS_DIR,
    LR_REPORT_DIR / "figures",
    RF_REPORT_DIR / "figures",
    XGB_REPORT_DIR / "figures",
    COMPARISON_REPORT_DIR / "figures",
):
    _dir.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# FILE PATHS
# ─────────────────────────────────────────────────────────────────────────────
RAW_DATA_PATH: Path = DATA_RAW_DIR / "Loan_Default.csv"
TRAIN_PROCESSED_PATH: Path = DATA_PROCESSED_DIR / "train_processed.csv"
TEST_PROCESSED_PATH: Path = DATA_PROCESSED_DIR / "test_processed.csv"
MODEL_PATH: Path = MODELS_DIR / "baseline_rf_model.joblib"
METRICS_PATH: Path = REPORTS_DIR / "metrics.json"

# ── NEW: per-model metrics paths ──────────────────────────────────────────────
LR_METRICS_PATH: Path = LR_REPORT_DIR / "metrics.json"
RF_METRICS_PATH: Path = RF_REPORT_DIR / "metrics.json"
XGB_METRICS_PATH: Path = XGB_REPORT_DIR / "metrics.json"
ALL_METRICS_PATH: Path = COMPARISON_REPORT_DIR / "all_models_metrics.json"

# ─────────────────────────────────────────────────────────────────────────────
# TARGET & ID COLUMNS
# ─────────────────────────────────────────────────────────────────────────────
TARGET_COL: str = "Status"
ID_COL: str = "ID"

# ─────────────────────────────────────────────────────────────────────────────
# LEAKAGE / DROPPED COLUMNS
# ─────────────────────────────────────────────────────────────────────────────
LEAKAGE_COLS: list[str] = [
    "rate_of_interest",
    "Interest_rate_spread",
    "Upfront_charges",
]

# ─────────────────────────────────────────────────────────────────────────────
# FEATURE GROUPS
# ─────────────────────────────────────────────────────────────────────────────
MISSINGNESS_FLAG_COLS: list[str] = ["property_value", "dtir1"]

NUMERIC_FEATURES: list[str] = [
    "loan_amount", "property_value", "income", "Credit_Score",
    "LTV", "dtir1", "term", "age", "DTI_x_LTV", "loan_to_income",
]

BINARY_FLAG_FEATURES: list[str] = ["property_value_isna", "dtir1_isna"]

CATEGORICAL_FEATURES: list[str] = [
    "loan_type", "loan_purpose", "Credit_Worthiness", "occupancy_type",
    "Neg_ammortization", "interest_only", "lump_sum_payment",
    "construction_type", "Secured_by", "total_units",
    "co-applicant_credit_type", "submission_of_application", "Region",
]

# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE HYPER-PARAMETERS
# ─────────────────────────────────────────────────────────────────────────────
TEST_SIZE: float = 0.20
RANDOM_STATE: int = 42
DECISION_THRESHOLD: float = 0.50

# ── Model registry keys (canonical names) ─────────────────────────────────────
MODEL_NAME_LR:  str = "logistic_regression"
MODEL_NAME_RF:  str = "random_forest"
MODEL_NAME_XGB: str = "xgboost"

# ── Logistic Regression ───────────────────────────────────────────────────────
LR_PARAMS: dict = {
    "max_iter":     1_000,
    "class_weight": "balanced",
    "random_state": RANDOM_STATE,
    "solver":       "lbfgs",
    "C":            0.1,
}

# ── Random Forest ─────────────────────────────────────────────────────────────
RF_PARAMS: dict = {
    "n_estimators":   300,
    "max_depth":      12,
    "min_samples_leaf": 20,
    "max_features":   "sqrt",
    "class_weight":   "balanced",
    "random_state":   RANDOM_STATE,
    "n_jobs": -1,
}

# ── XGBoost ───────────────────────────────────────────────────────────────────
XGB_PARAMS: dict = {
    "n_estimators":     400,
    "max_depth":        6,
    "learning_rate":    0.05,
    "subsample":        0.8,
    "colsample_bytree": 0.8,
    "min_child_weight": 10,
    # ≈ (n_negative / n_positive) for class balance
    "scale_pos_weight": 3,
    "eval_metric":      "auc",
    "use_label_encoder": False,
    "random_state":     RANDOM_STATE,
    "n_jobs": -1,
    "tree_method":      "hist",  # fast histogram method
}

# ─────────────────────────────────────────────────────────────────────────────
# RISK SCORING CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
RISK_SCORE_FLOOR: int = 100
RISK_SCORE_CEILING: int = 200

# ─────────────────────────────────────────────────────────────────────────────
# FLASK API CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
FLASK_HOST: str = "0.0.0.0"
FLASK_PORT: int = 5000
FLASK_DEBUG: bool = False

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
LOG_LEVEL: str = "DEBUG"   # Root capture level
LOG_CONSOLE_LEVEL: str = "INFO"    # StreamHandler level
LOG_FILE_LEVEL: str = "DEBUG"   # RotatingFileHandler level
