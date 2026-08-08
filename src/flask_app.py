"""
flask_app.py
────────────
Flask REST API for single-application loan default scoring.

Endpoints
─────────
GET  /health
    Liveness check — returns service status and loaded model info.

POST /predict
    Score a single loan application.
    Accepts JSON body, returns default probability + recommendation.

POST /predict/batch
    Score multiple applications in one request.
    Accepts JSON array, returns array of scoring responses.

GET  /model/info
    Returns champion model metadata from the versioning registry.

Usage
─────
    # Development server
    python -m src.flask_app

    # Production (via gunicorn)
    gunicorn "src.flask_app:create_app()" --bind 0.0.0.0:5000 --workers 4

    # Make target
    make flask
"""

from __future__ import annotations

import time
import traceback
from datetime import datetime
from functools import lru_cache
from typing import Any

import numpy as np
import pandas as pd
from flask import Flask, Response, jsonify, request

from src.config import (
    FLASK_DEBUG,
    FLASK_HOST,
    FLASK_PORT,
    MODEL_NAME_RF,
    RISK_SCORE_CEILING,
    RISK_SCORE_FLOOR,
    TARGET_COL,
)
from src.features import execute_feature_engineering, run_preprocessing_pipeline
from src.logger import get_flask_logger
from src.modeling.predict import predict_proba
from src.versioning import get_registry_summary, load_champion_model

logger = get_flask_logger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# MODEL CACHE  (loaded once at startup; avoids per-request disk I/O)
# ─────────────────────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def _get_model() -> object:
    """
    Load the Random Forest champion model exactly once and cache it.

    The ``@lru_cache`` decorator ensures the model is loaded from disk
    only on the first call; subsequent requests reuse the in-memory object.

    Returns
    -------
    object
        Fitted champion Random Forest estimator.
    """
    logger.info("Loading champion model '%s' into memory cache...",
                MODEL_NAME_RF)
    model = load_champion_model(MODEL_NAME_RF)
    logger.info("Model loaded and cached successfully.")
    return model


# ─────────────────────────────────────────────────────────────────────────────
# SCORING HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _prob_to_risk_score(prob: float) -> int:
    """Map [0, 1] default probability → [100, 200] internal risk score."""
    score = RISK_SCORE_FLOOR + \
        int(prob * (RISK_SCORE_CEILING - RISK_SCORE_FLOOR))
    return int(np.clip(score, RISK_SCORE_FLOOR, RISK_SCORE_CEILING))


def _recommendation(prob: float) -> str:
    """Return underwriting recommendation string."""
    if prob < 0.30:
        return "APPROVE / LOW RISK"
    elif prob < 0.55:
        return "REFER / MANUAL REVIEW"
    return "REJECT / HIGH RISK"


def _score_single(application: dict[str, Any]) -> dict[str, Any]:
    """
    Core scoring logic for a single application dictionary.

    Applies the same feature engineering and preprocessing pipeline
    used during model training.

    Parameters
    ----------
    application : dict
        Raw loan application fields.

    Returns
    -------
    dict
        Scoring response:
        ``default_probability``, ``underwriting_recommendation``,
        ``risk_score``.
    """
    # Build single-row DataFrame with dummy target
    df_raw = pd.DataFrame([application])
    df_raw[TARGET_COL] = 0

    # Feature engineering
    df_engineered = execute_feature_engineering(df_raw)

    # Duplicate row so train/test split doesn't fail on a single sample
    df_doubled = pd.concat(
        [df_engineered, df_engineered], ignore_index=True
    )
    _, test_processed = run_preprocessing_pipeline(df_doubled)

    # Score with cached model
    model = _get_model()
    result = predict_proba(model, test_processed.iloc[[0]])
    prob = float(result["Predicted_Default_Prob"].iloc[0])

    return {
        "default_probability":       round(prob, 4),
        "underwriting_recommendation": _recommendation(prob),
        "risk_score":                _prob_to_risk_score(prob),
    }


def _validate_application(data: dict) -> list[str]:
    """
    Validate required fields in a loan application payload.

    Parameters
    ----------
    data : dict
        Raw JSON payload.

    Returns
    -------
    list[str]
        List of validation error messages (empty if valid).
    """
    required_fields = [
        "loan_amount", "income", "Credit_Score",
        "LTV", "term", "loan_type", "Region",
    ]
    errors = [
        f"Missing required field: '{field}'"
        for field in required_fields
        if field not in data
    ]
    # Type validation for numeric fields
    numeric_fields = ["loan_amount", "income", "Credit_Score", "LTV", "term"]
    for field in numeric_fields:
        if field in data and not isinstance(data[field], (int, float)):
            errors.append(
                f"Field '{field}' must be numeric, "
                f"got {type(data[field]).__name__}"
            )
    return errors


# ─────────────────────────────────────────────────────────────────────────────
# REQUEST / RESPONSE LOGGING MIDDLEWARE
# ─────────────────────────────────────────────────────────────────────────────

def _log_request_response(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
) -> None:
    """Log a structured summary of each API request."""
    logger.info(
        "REQUEST  | method=%-6s path=%-20s status=%d duration=%.1fms",
        method, path, status_code, duration_ms,
    )


# ─────────────────────────────────────────────────────────────────────────────
# APP FACTORY
# ─────────────────────────────────────────────────────────────────────────────

def create_app() -> Flask:
    """
    Flask application factory.

    Creating the app via a factory function (rather than at module level)
    ensures the model cache is populated lazily on the first request,
    and allows the test suite to create a fresh app instance per test.

    Returns
    -------
    Flask
        Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    # ── Pre-load model on startup ─────────────────────────────────────────────
    with app.app_context():
        try:
            _get_model()   # warm up the LRU cache
        except Exception as exc:
            logger.warning(
                "Could not pre-load model at startup: %s. "
                "Model will be loaded on first request.",
                exc,
            )

    # ─────────────────────────────────────────────────────────────────────────
    # ROUTES
    # ─────────────────────────────────────────────────────────────────────────

    @app.route("/health", methods=["GET"])
    def health() -> Response:
        """
        Liveness & readiness check.

        Returns
        -------
        JSON
            ``{"status": "ok", "timestamp": "...", "model": "..."}``
        """
        t0 = time.perf_counter()
        try:
            _get_model()
            model_status = "loaded"
        except Exception:
            model_status = "unavailable"

        payload = {
            "status":       "ok",
            "timestamp":    datetime.utcnow().isoformat(),
            "model_name":   MODEL_NAME_RF,
            "model_status": model_status,
            "service":      "Loan Default Scoring API",
        }
        duration = (time.perf_counter() - t0) * 1000
        _log_request_response("GET", "/health", 200, duration)
        return jsonify(payload), 200

    # ─────────────────────────────────────────────────────────────────────────

    @app.route("/predict", methods=["POST"])
    def predict() -> Response:
        """
        Score a single loan application.

        Request body (JSON)
        ───────────────────
        {
          "loan_amount":    420000,
          "property_value": null,        // null → missing appraisal flag
          "income":         52000,
          "Credit_Score":   580,
          "LTV":            97.0,
          "dtir1":          null,
          "term":           360,
          "loan_type":      "type1",
          "loan_purpose":   "p1",
          "Credit_Worthiness": "l1",
          "occupancy_type": "pr",
          "Neg_ammortization": "not_neg",
          "interest_only":  "not_int",
          "lump_sum_payment": "not_lpsm",
          "construction_type": "sb",
          "Secured_by":     "home",
          "total_units":    "1U",
          "co-applicant_credit_type": "EXP",
          "submission_of_application": "to_inst",
          "Region":         "south"
        }

        Response (JSON)
        ───────────────
        {
          "default_probability":        0.8056,
          "underwriting_recommendation": "REJECT / HIGH RISK",
          "risk_score":                  165,
          "scored_at":                  "2024-01-15T10:30:00.123456"
        }
        """
        t0 = time.perf_counter()

        if not request.is_json:
            return (
                jsonify({"error": "Content-Type must be application/json"}),
                415,
            )

        data = request.get_json(force=True)
        if data is None:
            return jsonify({"error": "Empty or malformed JSON body."}), 400

        # Validate payload
        validation_errors = _validate_application(data)
        if validation_errors:
            logger.warning("Validation failed: %s", validation_errors)
            return jsonify({"errors": validation_errors}), 422

        # Replace JSON null with numpy nan for pipeline compatibility
        data = {
            k: (np.nan if v is None else v)
            for k, v in data.items()
        }

        try:
            result = _score_single(data)
            result["scored_at"] = datetime.utcnow().isoformat()
            status_code = 200
            response = jsonify(result)
        except Exception as exc:
            logger.error(
                "Scoring failed for application: %s\n%s",
                data,
                traceback.format_exc(),
            )
            status_code = 500
            response = jsonify(
                {"error": "Internal scoring error.", "detail": str(exc)})

        duration = (time.perf_counter() - t0) * 1000
        _log_request_response("POST", "/predict", status_code, duration)
        return response, status_code

    # ─────────────────────────────────────────────────────────────────────────

    @app.route("/predict/batch", methods=["POST"])
    def predict_batch() -> Response:
        """
        Score multiple loan applications in a single request.

        Request body (JSON)
        ───────────────────
        [
          { <application_1_fields> },
          { <application_2_fields> },
          ...
        ]

        Response (JSON)
        ───────────────
        {
          "total":   2,
          "results": [
            { "index": 0, "default_probability": 0.12, ... },
            { "index": 1, "default_probability": 0.87, ... }
          ],
          "scored_at": "2024-01-15T10:30:00.123456"
        }
        """
        t0 = time.perf_counter()

        if not request.is_json:
            return (
                jsonify({"error": "Content-Type must be application/json"}),
                415,
            )

        data = request.get_json(force=True)
        if not isinstance(data, list) or len(data) == 0:
            return (
                jsonify({"error": "Request body must be a non-empty JSON array."}),
                400,
            )

        if len(data) > 500:
            return (
                jsonify(
                    {"error": "Batch size exceeds maximum of 500 applications."}),
                413,
            )

        results = []
        errors = []

        for idx, application in enumerate(data):
            # Replace JSON nulls
            cleaned = {
                k: (np.nan if v is None else v)
                for k, v in application.items()
            }
            # Per-item validation
            val_errors = _validate_application(cleaned)
            if val_errors:
                errors.append({"index": idx, "errors": val_errors})
                results.append({
                    "index":  idx,
                    "error":  val_errors,
                    "status": "failed",
                })
                continue

            try:
                score = _score_single(cleaned)
                results.append({"index": idx, "status": "scored", **score})
            except Exception as exc:
                logger.error(
                    "Batch scoring failed at index %d: %s", idx, exc
                )
                errors.append({"index": idx, "error": str(exc)})
                results.append({
                    "index":  idx,
                    "error":  str(exc),
                    "status": "failed",
                })

        status_code = 200 if not errors else 207  # 207 = Multi-Status
        response_payload = {
            "total":      len(data),
            "successful": len([r for r in results if r.get("status") == "scored"]),
            "failed":     len(errors),
            "results":    results,
            "scored_at":  datetime.utcnow().isoformat(),
        }

        duration = (time.perf_counter() - t0) * 1000
        logger.info(
            "Batch predict | total=%d | success=%d | failed=%d | %.1fms",
            len(data),
            response_payload["successful"],
            response_payload["failed"],
            duration,
        )
        _log_request_response("POST", "/predict/batch", status_code, duration)
        return jsonify(response_payload), status_code

    # ─────────────────────────────────────────────────────────────────────────

    @app.route("/model/info", methods=["GET"])
    def model_info() -> Response:
        """
        Return champion model metadata from the versioning registry.

        Response (JSON)
        ───────────────
        {
          "model_name": "random_forest",
          "champion_version": "v1",
          "versions_available": ["v1"],
          "champion_metadata": { ... }
        }
        """
        t0 = time.perf_counter()
        try:
            registry = get_registry_summary()
            model_entry = registry.get("models", {}).get(MODEL_NAME_RF, {})
            champion_ver = model_entry.get("champion")
            champion_meta = (
                model_entry.get("versions", {}).get(champion_ver, {})
                if champion_ver else {}
            )
            payload = {
                "model_name":         MODEL_NAME_RF,
                "champion_version":   champion_ver,
                "versions_available": list(model_entry.get("versions", {}).keys()),
                "champion_metadata":  champion_meta,
            }
            status_code = 200
        except Exception as exc:
            payload = {"error": str(exc)}
            status_code = 500

        duration = (time.perf_counter() - t0) * 1000
        _log_request_response("GET", "/model/info", status_code, duration)
        return jsonify(payload), status_code

    # ─────────────────────────────────────────────────────────────────────────

    @app.errorhandler(404)
    def not_found(exc) -> Response:
        return jsonify({"error": "Endpoint not found.", "path": request.path}), 404

    @app.errorhandler(405)
    def method_not_allowed(exc) -> Response:
        return (
            jsonify({
                "error":  "Method not allowed.",
                "method": request.method,
                "path":   request.path,
            }),
            405,
        )

    @app.errorhandler(500)
    def internal_error(exc) -> Response:
        logger.critical("Unhandled exception: %s", traceback.format_exc())
        return jsonify({"error": "Internal server error."}), 500

    return app


# ─────────────────────────────────────────────────────────────────────────────
# STANDALONE ENTRY-POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logger.info(
        "Starting Flask API on http://%s:%d (debug=%s)",
        FLASK_HOST, FLASK_PORT, FLASK_DEBUG,
    )
    app = create_app()
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
