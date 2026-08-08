# ML_EDA_full_fledge: Loan Default EDA & Feature Selection Project

A production-grade, end-to-end Exploratory Data Analysis (EDA), Feature Engineering, and Feature Selection project structured according to the [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/) (CCDS) standard.

---

# ML_EDA_full_fledge: Loan Default EDA & Feature Selection Project

A production-grade, end-to-end Exploratory Data Analysis (EDA), Feature Engineering,
Feature Selection, Model Versioning, and REST API serving project structured according
to the [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/)
(CCDS) standard.

---

## Directory Structure

```text
.
├── .github
│   └── workflows
│       └── ci.yml                      <- CI/CD pipeline (GitHub Actions for linting, testing, and pipeline execution)
├── LICENSE                             <- Open-source MIT License
├── Makefile                            <- Automation commands (`make venv`, `make data`, `make features`, `make train`,
│                                          `make predict`, `make reports`, `make api`, `make flask`, `make test`, etc.)
├── README.md                           <- Top-level project documentation
├── pyproject.toml                      <- Project packaging, Ruff linter, and Pytest configuration
├── requirements.txt                    <- Dependencies for reproducing the environment
│
├── data
│   ├── raw                             <- Original, immutable raw dataset (data/raw/Loan_Default.csv)
│   ├── interim                         <- Intermediate data transformed during pipeline execution
│   └── processed                       <- Final canonical datasets for modeling (train_processed.csv, test_processed.csv)
│
├── docs                                <- Project documentation (docs/index.md)
│
├── logs                                <- NEW: Rotating structured log files directory
│   ├── pipeline.log                    <- All pipeline stage logs (DEBUG → CRITICAL)
│   └── flask_api.log                   <- Flask API request & response logs
│
├── models                              <- Trained and serialized model artifacts
│   ├── baseline_rf_model.joblib        <- Legacy best-model artifact (backward compatibility)
│   └── registry                        <- NEW: Versioned model store
│       ├── model_registry.json         <- NEW: Central JSON index of all registered models
│       ├── logistic_regression         <- Per-model versioned artifact directory
│       │   ├── logistic_regression_v1.joblib
│       │   └── logistic_regression_v2.joblib
│       ├── random_forest
│       │   ├── random_forest_v1.joblib
│       │   └── random_forest_v2.joblib
│       └── xgboost
│           ├── xgboost_v1.joblib
│           └── xgboost_v2.joblib
│
├── notebooks                           <- Jupyter notebooks (notebooks/1.0-eda-and-feature-selection.ipynb)
│
├── references                          <- Data dictionaries and explanatory materials (references/data_dictionary.md)
│
├── reports                             <- Generated analysis reports & metrics
│   ├── metrics.json                    <- Legacy top-level metrics (backward compatibility)
│   ├── figures                         <- Legacy top-level figures directory
│   └── models                          <- NEW: Per-model and cross-model comparison reports
│       ├── logistic_regression
│       │   ├── metrics.json            <- LR-specific metrics (ROC-AUC, PR-AUC, F1, Confusion Matrix)
│       │   └── figures
│       │       ├── roc_curve.png
│       │       ├── pr_curve.png
│       │       └── confusion_matrix.png
│       ├── random_forest
│       │   ├── metrics.json            <- RF-specific metrics (ROC-AUC, PR-AUC, F1, Confusion Matrix)
│       │   └── figures
│       │       ├── roc_curve.png
│       │       ├── pr_curve.png
│       │       ├── confusion_matrix.png
│       │       └── feature_importance.png
│       ├── xgboost
│       │   ├── metrics.json            <- XGBoost-specific metrics (ROC-AUC, PR-AUC, F1, Confusion Matrix)
│       │   └── figures
│       │       ├── roc_curve.png
│       │       ├── pr_curve.png
│       │       ├── confusion_matrix.png
│       │       └── feature_importance.png
│       └── comparison                  <- NEW: Cross-model comparison artifacts
│           ├── all_models_metrics.json <- Side-by-side metrics for all 3 models
│           └── figures
│               ├── roc_curve_comparison.png
│               ├── pr_curve_comparison.png
│               └── metrics_comparison_bar.png
│
├── src                                 <- Source code for execution in this project
│   ├── __init__.py                     <- Makes src a Python package
│   ├── config.py                       <- MODIFIED: versioning paths, XGBoost params, Flask config, logging constants
│   ├── dataset.py                      <- Data loading and dataset verification routines
│   ├── logger.py                       <- NEW: Centralized rotating-file + coloured-console logging setup
│   ├── versioning.py                   <- NEW: Model versioning engine (register, load champion, promote, delete)
│   ├── features.py                     <- MODIFIED: Feature engineering & scikit-learn ColumnTransformer pipeline + logging added
│   ├── train.py                        <- MODIFIED: Trains LR + RF + XGBoost, registers each in versioning registry
│   ├── predict.py                      <- MODIFIED: Batch inference entry point + logging added
│   ├── reports.py                      <- MODIFIED: Multi-model per-model & cross-model comparison reports
│   ├── api.py                          <- MODIFIED: Single application CLI scoring API + logging added
│   ├── plots.py                        <- MODIFIED: Reusable plotting routines + 3 new multi-model comparison plots
│   ├── flask_app.py                    <- NEW: Flask REST API (GET /health, POST /predict,
│   │                                      POST /predict/batch, GET /model/info)
│   └── modeling
│       ├── __init__.py
│       ├── train.py                    <- MODIFIED: train_xgboost() added, all trainers call register_model() + logging
│       └── predict.py                  <- MODIFIED: load_champion() added + logging added
│
└── tests                               <- Automated unit & integration test suite (Pytest)
    ├── __init__.py
    ├── conftest.py                     <- Pytest fixtures
    ├── test_dataset.py                 <- Data loading unit tests
    ├── test_features.py                <- Feature engineering & pipeline unit tests
    ├── test_modeling.py                <- Model prediction & probability bounds unit tests
    ├── test_versioning.py              <- NEW: Model versioning registry CRUD & version tests
    └── test_flask_app.py               <- NEW: 14 Flask API integration tests
                                           (health, predict, batch, model/info, error handlers)


---

## Quickstart & Environment Setup

### 1. Create Virtual Environment & Install Dependencies

```bash
# Create virtual environment (.venv) and install dependencies (includes XGBoost & Flask)
make venv

# Activate virtual environment

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

---

## Verify Installation

```bash
python -c "import sklearn, xgboost, flask; print('All dependencies OK')"
```

---

## Running the End-to-End Pipeline

You can run individual pipeline stages via `make` or direct module execution: All stages emit structured logs to logs/pipeline.log.

```bash
# 1. Verify Dataset Loading & Schema
make data

# 2. Feature Engineering & Preprocessing Pipeline
# Processes raw data, creates missingness flags, constructs financial ratios,
# fits ColumnTransformer (on training split only), and saves train/test CSVs
make features

# 3. Model Training & Evaluation
# Trains Logistic Regression, Random Forest, and XGBoost classifiers
# Registers each model in models/registry/ with auto-incremented version tags (v1, v2, ...)
# Prints consolidated results table and saves best model as legacy artifact
make train

# 4. Batch Prediction Inference
# Loads champion Random Forest, scores all 29,734 test rows,
# prints sample output with probabilities and binary labels
make predict

# 5. Generate Multi-Model Reports & Evaluation Figures
# Per-model:   metrics.json + roc_curve, pr_curve, confusion_matrix, feature_importance
# Comparison:  all_models_metrics.json + roc_curve_comparison, pr_curve_comparison,
#              metrics_comparison_bar
make reports

# 6. Sample Single Application CLI Inference
make api

# 7. Start Flask REST API (development server)
# Serves on http://0.0.0.0:5000
# Endpoints: GET /health | POST /predict | POST /predict/batch | GET /model/info
make flask


# 8. Start Flask REST API (production — gunicorn, Linux/macOS only)
make flask-prod

# 9. Run Automated Pytest Unit & Integration Tests
# Covers: dataset, features, modeling, versioning, Flask API (14 API tests)
make test

# 10. Run Tests with HTML Coverage Report
make test-cov

# 11. Lint Codebase with Ruff
make lint

# 12. Execute Full End-to-End Pipeline
make all
```

---

## Flask REST API

The Flask API exposes the champion Random Forest model for real-time single-application
and batch scoring. The model is loaded once at startup via @lru_cache — all
subsequent requests reuse the in-memory object with zero disk I/O overhead.
All requests and responses are logged to logs/flask_api.log.

### Starting the API

```bash
# Development server (auto-reload, single worker)
make flask
# → Listening on http://0.0.0.0:5000

# Production server — gunicorn (Linux / macOS only)
make flask-prod
# → 4 workers | access log → logs/gunicorn_access.log
```

---

## Endpoints

GET /health — Liveness Check

```bash
curl http://localhost:5000/health
```

---

```json
{
  "status":       "ok",
  "timestamp":    "2024-01-15T10:35:00",
  "model_name":   "random_forest",
  "model_status": "loaded",
  "service":      "Loan Default Scoring API"
}
```

---

## POST /predict — Score a Single Application

```bash
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{
           "loan_amount":               420000,
           "property_value":            null,
           "income":                    52000,
           "Credit_Score":              580,
           "LTV":                       97.0,
           "dtir1":                     null,
           "term":                      360,
           "loan_type":                 "type1",
           "loan_purpose":              "p1",
           "Credit_Worthiness":         "l1",
           "occupancy_type":            "pr",
           "Neg_ammortization":         "not_neg",
           "interest_only":             "not_int",
           "lump_sum_payment":          "not_lpsm",
           "construction_type":         "sb",
           "Secured_by":                "home",
           "total_units":               "1U",
           "co-applicant_credit_type":  "EXP",
           "submission_of_application": "to_inst",
           "Region":                    "south"
         }'
```

---

```json
{
  "default_probability":         0.8056,
  "underwriting_recommendation": "REJECT / HIGH RISK",
  "risk_score":                  165,
  "scored_at":                   "2024-01-15T10:35:01.234567"
}

```

---

## Underwriting Recommendation Logic

| Default Probability | Recommendation |
|---------------------|----------------|
|    < 0.30           | APPROVE / LOW RISK |
|  0.30 – 0.54       | REFER / MANUAL REVIEW |
|    ≥ 0.55           | REJECT / HIGH RISK |

---

## Risk Score Mapping

```text
risk_score = 100 + int(default_probability × 100)
Range: [100, 200]  →  100 = lowest risk, 200 = highest risk
```

---

## POST /predict/batch — Score Multiple Applications

```bash
curl -X POST http://localhost:5000/predict/batch \
     -H "Content-Type: application/json" \
     -d '[{ <application_1_fields> }, { <application_2_fields> }]'
```

---

```json
{
  "total":      2,
  "successful": 2,
  "failed":     0,
  "results": [
    {
      "index":                       0,
      "status":                      "scored",
      "default_probability":         0.1203,
      "underwriting_recommendation": "APPROVE / LOW RISK",
      "risk_score":                  112
    },
    {
      "index":                       1,
      "status":                      "scored",
      "default_probability":         0.8056,
      "underwriting_recommendation": "REJECT / HIGH RISK",
      "risk_score":                  165
    }
  ],
  "scored_at": "2024-01-15T10:35:02.567890"
}
```

---

## GET /model/info — Champion Model Metadata

```bash
curl http://localhost:5000/model/info
```

---

```json
{
  "model_name":         "random_forest",
  "champion_version":   "v1",
  "versions_available": ["v1"],
  "champion_metadata": {
    "version":    "v1",
    "model_name": "random_forest",
    "artifact":   "models/registry/random_forest/random_forest_v1.joblib",
    "roc_auc":    0.8851,
    "pr_auc":     0.8271,
    "accuracy":   0.8792,
    "f1_score":   0.7634,
    "trained_at": "2024-01-15T10:30:45",
    "n_train":    118936,
    "n_test":     29734,
    "params":     { "n_estimators": 300, "max_depth": 12 }
  }
}
```

## Model Versioning

Every make train run automatically registers all three models in a
local JSON registry under models/registry/. Version tags are
auto-incremented (v1, v2, …) on every run.

### model_registry.json Schema

```json
{
  "models": {
    "random_forest": {
      "champion": "v1",
      "versions": {
        "v1": {
          "version":    "v1",
          "model_name": "random_forest",
          "artifact":   "models/registry/random_forest/random_forest_v1.joblib",
          "roc_auc":    0.8851,
          "pr_auc":     0.8271,
          "accuracy":   0.8792,
          "f1_score":   0.7634,
          "trained_at": "2024-01-15T10:30:45",
          "n_train":    118936,
          "n_test":     29734,
          "params":     { "n_estimators": 300, "max_depth": 12 }
        }
      }
    }
  }
}

```

---

## Versioning API Usage

```python
from src.versioning import (
    register_model,       # Register a trained model → returns version tag
    load_champion_model,  # Load the current champion for a given model name
    load_model_version,   # Load any specific version (e.g. "v2")
    promote_champion,     # Manually promote a version to champion
    get_all_versions,     # List all versions + metadata for a model
    get_registry_summary, # Return the full registry dict
    delete_model_version, # Remove a non-champion version from disk + registry
)

# Promote v2 to champion after A/B test validation
from src.versioning import promote_champion
promote_champion("random_forest", "v2")

# Load a specific historical version for comparison
from src.versioning import load_model_version
old_model = load_model_version("xgboost", "v1")

```

## Logging

All pipeline stages and Flask API requests produce structured, levelled log output
to both the console and rotating log files.

### Log Files

| File  | Content | Max Size |
|-------|---------|----------|
| logs/pipeline.log | All pipeline stages (DEBUG → CRITICAL) | 10 MB × 5 |
| logs/flask_api.log | Flask API requests & scoring events |  10 MB × 5 |

---

## Obtaining a Logger in Any Module

```python
from src.logger import get_logger
logger = get_logger(__name__)

logger.debug("Processing %d rows", len(df))
logger.info("Feature engineering complete | shape=%s", df.shape)
logger.warning("Champion model not found, skipping '%s'", model_name)
logger.error("Scoring failed: %s", exc)
```

---

## Key Business & Technical Findings

1. **Target Leakage Remediation**: Post-decision interest rate attributes (`rate_of_interest`,
`Interest_rate_spread`, `Upfront_charges`) were identified as future leakage (missing in
100% of defaults) and removed from pre-underwriting decisioning.

2. **Missingness Indicator Flags**: Missing property appraisals (`property_value_isna`) and
debt ratios (`dtir1_isna`) carried a +0.4132 correlation with default, converting
missingness into high-precision binary predictors.

3. **Compound Risk Surfaces**: Debt-to-Income multiplied by Loan-to-Value (DTI_x_LTV)
captured non-linear layered risk undetectable by either ratio independently.

4. **Fit-on-Train-Only Discipline**: The ColumnTransformer (`imputation statistics`, `scaling
parameters`, `OHE category sets`) is fitted exclusively on X_train — preventing data
leakage from the test fold into preprocessing statistics.

5. **Class Imbalance Handling**: class_weight="balanced" (`LR & RF`) and
scale_pos_weight=3 (XGBoost) compensate for the 3:1 negative-to-positive class
ratio without resampling.

6. **Model Performance Comparison**: All three models evaluated on the same stratified
20% hold-out test set (29,734 applications):

| Model | ROC-AUC | PR-AUC | Accuracy | F1 Score |
| ------- | --------- | -------- | ---------- | ---------- |
| Logistic Regression | 0.8459 | 0.7731 | 82.34% | 0.7123 |
| Random Forest | 0.8851 | 0.8271 | 87.92% | 0.7634 |
| XGBoost | 0.8923 | 0.8354 | 88.61% | 0.7712 |

**Best Model**: `XGBoost` — highest ROC-AUC (0.8923) and PR-AUC (0.8354).
