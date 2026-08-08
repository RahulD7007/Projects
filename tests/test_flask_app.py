"""
test_flask_app.py
─────────────────
Integration tests for the Flask prediction API.

Fix applied
───────────
Added 'age' field to valid_application and high_risk_application fixtures.
The preprocessor fitted during `make features` includes 'age' in
CATEGORICAL_FEATURES — omitting it causes:
    ValueError: columns are missing: {'age'}
"""
from __future__ import annotations

import json

import numpy as np
import pytest

# ─────────────────────────────────────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def flask_client():
    """
    Create a Flask test client with cached model and preprocessor.

    Module scope: Flask app created once per test module (not per test),
    matching how the production server behaves.
    """
    from src.flask_app import create_app
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def valid_application() -> dict:
    """
    A well-formed low-risk loan application payload.

    All required fields are present including 'age' (string band).
    property_value and dtir1 are provided (no missingness flags triggered).
    """
    return {
        "loan_amount":                 350_000,
        "property_value":              400_000,
        "income":                      85_000,
        "Credit_Score":                720,
        "LTV":                         87.5,
        "dtir1":                       35.0,
        "term":                        360,
        "age":                         "35-44",    # ← required: string band
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


@pytest.fixture
def high_risk_application() -> dict:
    """
    A high-risk application with missing appraisal and DTI.

    property_value=null and dtir1=null trigger both missingness flags
    (+0.41 correlation with default). High LTV (97.0) adds additional risk.
    """
    return {
        "loan_amount":                 420_000,
        "property_value":              None,       # → property_value_isna=1
        "income":                      52_000,
        "Credit_Score":                580,
        "LTV":                         97.0,
        "dtir1":                       None,       # → dtir1_isna=1
        "term":                        360,
        "age":                         "35-44",    # ← required: string band
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
# TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestHealthEndpoint:
    """GET /health"""

    def test_health_returns_200(self, flask_client):
        """Health endpoint must return HTTP 200."""
        response = flask_client.get("/health")
        assert response.status_code == 200

    def test_health_response_structure(self, flask_client):
        """Health response must contain status, timestamp, model_name."""
        response = flask_client.get("/health")
        data = response.get_json()
        assert "status" in data
        assert "timestamp" in data
        assert "model_name" in data
        assert data["status"] == "ok"

    def test_health_model_status_loaded(self, flask_client):
        """Health response must report model_status as 'loaded'."""
        response = flask_client.get("/health")
        data = response.get_json()
        assert data.get("model_status") == "loaded"


class TestPredictEndpoint:
    """POST /predict"""

    def test_predict_valid_application(
        self, flask_client, valid_application
    ):
        """Valid payload with all fields must return HTTP 200."""
        response = flask_client.post(
            "/predict",
            data=json.dumps(valid_application),
            content_type="application/json",
        )
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. "
            f"Body: {response.get_json()}"
        )

    def test_predict_response_structure(
        self, flask_client, valid_application
    ):
        """Response must contain all four expected fields."""
        response = flask_client.post(
            "/predict",
            data=json.dumps(valid_application),
            content_type="application/json",
        )
        data = response.get_json()
        assert "default_probability" in data
        assert "underwriting_recommendation" in data
        assert "risk_score" in data
        assert "scored_at" in data

    def test_predict_probability_bounds(
        self, flask_client, valid_application
    ):
        """Default probability must be within [0.0, 1.0]."""
        response = flask_client.post(
            "/predict",
            data=json.dumps(valid_application),
            content_type="application/json",
        )
        data = response.get_json()
        prob = data["default_probability"]
        assert 0.0 <= prob <= 1.0, (
            f"Probability {prob} is outside [0, 1]"
        )

    def test_predict_risk_score_bounds(
        self, flask_client, valid_application
    ):
        """Risk score must be within [100, 200]."""
        response = flask_client.post(
            "/predict",
            data=json.dumps(valid_application),
            content_type="application/json",
        )
        data = response.get_json()
        score = data["risk_score"]
        assert 100 <= score <= 200, (
            f"Risk score {score} is outside [100, 200]"
        )

    def test_predict_recommendation_values(
        self, flask_client, valid_application
    ):
        """Recommendation must be one of three valid strings."""
        valid_recs = {
            "APPROVE / LOW RISK",
            "REFER / MANUAL REVIEW",
            "REJECT / HIGH RISK",
        }
        response = flask_client.post(
            "/predict",
            data=json.dumps(valid_application),
            content_type="application/json",
        )
        data = response.get_json()
        assert data["underwriting_recommendation"] in valid_recs, (
            f"Unexpected recommendation: {data['underwriting_recommendation']}"
        )

    def test_predict_high_risk_application(
        self, flask_client, high_risk_application
    ):
        """
        High-risk application (missing appraisal + DTI, LTV=97) must
        return a default probability > 0.5.
        """
        response = flask_client.post(
            "/predict",
            data=json.dumps(high_risk_application),
            content_type="application/json",
        )
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. "
            f"Body: {response.get_json()}"
        )
        data = response.get_json()
        assert data["default_probability"] > 0.5, (
            f"High-risk application should yield prob > 0.5, "
            f"got {data['default_probability']}"
        )

    def test_predict_missing_required_field(self, flask_client):
        """Payload missing 'loan_amount' must return HTTP 422."""
        incomplete = {"income": 60_000, "Credit_Score": 700}
        response = flask_client.post(
            "/predict",
            data=json.dumps(incomplete),
            content_type="application/json",
        )
        assert response.status_code == 422
        data = response.get_json()
        assert "errors" in data

    def test_predict_wrong_content_type(
        self, flask_client, valid_application
    ):
        """Non-JSON Content-Type must return HTTP 415."""
        response = flask_client.post(
            "/predict",
            data=json.dumps(valid_application),
            content_type="text/plain",
        )
        assert response.status_code == 415

    def test_predict_empty_body(self, flask_client):
        """Empty request body must return HTTP 400."""
        response = flask_client.post(
            "/predict",
            data="",
            content_type="application/json",
        )
        assert response.status_code == 400


class TestBatchPredictEndpoint:
    """POST /predict/batch"""

    def test_batch_predict_valid(
        self, flask_client, valid_application, high_risk_application
    ):
        """Batch of 2 valid applications must return HTTP 200 with both scored."""
        batch = [valid_application, high_risk_application]
        response = flask_client.post(
            "/predict/batch",
            data=json.dumps(batch),
            content_type="application/json",
        )
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. "
            f"Body: {response.get_json()}"
        )
        data = response.get_json()
        assert data["total"] == 2
        assert data["successful"] == 2
        assert data["failed"] == 0
        assert len(data["results"]) == 2

    def test_batch_predict_empty_list(self, flask_client):
        """Empty JSON array must return HTTP 400."""
        response = flask_client.post(
            "/predict/batch",
            data=json.dumps([]),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_batch_predict_mixed_valid_invalid(
        self, flask_client, valid_application
    ):
        """
        Batch with one valid and one invalid application must return
        HTTP 207 Multi-Status with successful=1 and failed=1.
        """
        batch = [
            valid_application,
            {"income": 50_000},    # missing all required fields
        ]
        response = flask_client.post(
            "/predict/batch",
            data=json.dumps(batch),
            content_type="application/json",
        )
        assert response.status_code == 207
        data = response.get_json()
        assert data["failed"] == 1
        assert data["successful"] == 1

    def test_batch_predict_all_results_have_index(
        self, flask_client, valid_application, high_risk_application
    ):
        """Every result in the batch response must have an 'index' field."""
        batch = [valid_application, high_risk_application]
        response = flask_client.post(
            "/predict/batch",
            data=json.dumps(batch),
            content_type="application/json",
        )
        data = response.get_json()
        for result in data["results"]:
            assert "index" in result, (
                f"Result missing 'index' field: {result}"
            )

    def test_batch_predict_probability_bounds(
        self, flask_client, valid_application, high_risk_application
    ):
        """All batch probabilities must be within [0.0, 1.0]."""
        batch = [valid_application, high_risk_application]
        response = flask_client.post(
            "/predict/batch",
            data=json.dumps(batch),
            content_type="application/json",
        )
        data = response.get_json()
        for result in data["results"]:
            if result.get("status") == "scored":
                prob = result["default_probability"]
                assert 0.0 <= prob <= 1.0, (
                    f"Batch probability {prob} out of [0, 1] "
                    f"at index {result['index']}"
                )


class TestModelInfoEndpoint:
    """GET /model/info"""

    def test_model_info_returns_200(self, flask_client):
        """Model info endpoint must return HTTP 200."""
        response = flask_client.get("/model/info")
        assert response.status_code == 200

    def test_model_info_structure(self, flask_client):
        """Model info response must contain required registry fields."""
        response = flask_client.get("/model/info")
        data = response.get_json()
        assert "model_name" in data
        assert "champion_version" in data
        assert "versions_available" in data

    def test_model_info_champion_version_not_none(self, flask_client):
        """Champion version must be set (not null) after make train."""
        response = flask_client.get("/model/info")
        data = response.get_json()
        assert data["champion_version"] is not None, (
            "No champion version set. Run `make train` first."
        )


class TestErrorHandlers:
    """HTTP error handler tests."""

    def test_404_unknown_endpoint(self, flask_client):
        """Unknown endpoint must return HTTP 404 with error message."""
        response = flask_client.get("/nonexistent")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_405_wrong_method_on_predict(self, flask_client):
        """GET on a POST-only endpoint must return HTTP 405."""
        response = flask_client.get("/predict")
        assert response.status_code == 405
        data = response.get_json()
        assert "error" in data
