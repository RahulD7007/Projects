"""
test_flask_app.py
─────────────────
Integration tests for the Flask prediction API.
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
    Create a Flask test client with the champion RF model pre-loaded.

    Uses pytest's module scope so the Flask app and model are created
    once per test module (not per test function).
    """
    from src.flask_app import create_app
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def valid_application():
    """A well-formed loan application payload."""
    return {
        "loan_amount":              350_000,
        "property_value":           400_000,
        "income":                   85_000,
        "Credit_Score":             720,
        "LTV":                      87.5,
        "dtir1":                    35.0,
        "term":                     360,
        "loan_type":                "type1",
        "loan_purpose":             "p1",
        "Credit_Worthiness":        "l1",
        "occupancy_type":           "pr",
        "Neg_ammortization":        "not_neg",
        "interest_only":            "not_int",
        "lump_sum_payment":         "not_lpsm",
        "construction_type":        "sb",
        "Secured_by":               "home",
        "total_units":              "1U",
        "co-applicant_credit_type": "EXP",
        "submission_of_application": "to_inst",
        "Region":                   "south",
    }


@pytest.fixture
def high_risk_application():
    """A high-risk application with missing appraisal and DTI."""
    return {
        "loan_amount":              420_000,
        "property_value":           None,    # Missing → high-risk flag
        "income":                   52_000,
        "Credit_Score":             580,
        "LTV":                      97.0,
        "dtir1":                    None,    # Missing → high-risk flag
        "term":                     360,
        "loan_type":                "type1",
        "loan_purpose":             "p1",
        "Credit_Worthiness":        "l1",
        "occupancy_type":           "pr",
        "Neg_ammortization":        "not_neg",
        "interest_only":            "not_int",
        "lump_sum_payment":         "not_lpsm",
        "construction_type":        "sb",
        "Secured_by":               "home",
        "total_units":              "1U",
        "co-applicant_credit_type": "EXP",
        "submission_of_application": "to_inst",
        "Region":                   "south",
    }


# ─────────────────────────────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestHealthEndpoint:
    """GET /health"""

    def test_health_returns_200(self, flask_client):
        response = flask_client.get("/health")
        assert response.status_code == 200

    def test_health_response_structure(self, flask_client):
        response = flask_client.get("/health")
        data = response.get_json()
        assert "status" in data
        assert data["status"] == "ok"
        assert "timestamp" in data
        assert "model_name" in data


class TestPredictEndpoint:
    """POST /predict"""

    def test_predict_valid_application(self, flask_client, valid_application):
        """Valid payload must return 200 with correct response structure."""
        response = flask_client.post(
            "/predict",
            data=json.dumps(valid_application),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()

        assert "default_probability" in data
        assert "underwriting_recommendation" in data
        assert "risk_score" in data
        assert "scored_at" in data

    def test_predict_probability_bounds(self, flask_client, valid_application):
        """Default probability must be strictly within [0, 1]."""
        response = flask_client.post(
            "/predict",
            data=json.dumps(valid_application),
            content_type="application/json",
        )
        data = response.get_json()
        prob = data["default_probability"]
        assert 0.0 <= prob <= 1.0, f"Probability {prob} out of bounds"

    def test_predict_risk_score_bounds(self, flask_client, valid_application):
        """Risk score must be within [100, 200]."""
        response = flask_client.post(
            "/predict",
            data=json.dumps(valid_application),
            content_type="application/json",
        )
        data = response.get_json()
        score = data["risk_score"]
        assert 100 <= score <= 200, f"Risk score {score} out of [100, 200]"

    def test_predict_recommendation_values(self, flask_client, valid_application):
        """Recommendation must be one of three defined strings."""
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
        assert data["underwriting_recommendation"] in valid_recs

    def test_predict_high_risk_application(
        self, flask_client, high_risk_application
    ):
        """
        High-risk application (missing appraisal + DTI, high LTV)
        should return a probability > 0.5.
        """
        response = flask_client.post(
            "/predict",
            data=json.dumps(high_risk_application),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["default_probability"] > 0.5, (
            "High-risk application should yield prob > 0.5"
        )

    def test_predict_missing_required_field(self, flask_client):
        """Payload without 'loan_amount' must return 422."""
        incomplete = {"income": 60_000, "Credit_Score": 700}
        response = flask_client.post(
            "/predict",
            data=json.dumps(incomplete),
            content_type="application/json",
        )
        assert response.status_code == 422
        data = response.get_json()
        assert "errors" in data

    def test_predict_wrong_content_type(self, flask_client, valid_application):
        """Non-JSON Content-Type must return 415."""
        response = flask_client.post(
            "/predict",
            data=json.dumps(valid_application),
            content_type="text/plain",
        )
        assert response.status_code == 415

    def test_predict_empty_body(self, flask_client):
        """Empty body must return 400."""
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
        """Batch of 2 applications should return 200 with both scored."""
        batch = [valid_application, high_risk_application]
        response = flask_client.post(
            "/predict/batch",
            data=json.dumps(batch),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["total"] == 2
        assert data["successful"] == 2
        assert len(data["results"]) == 2

    def test_batch_predict_empty_list(self, flask_client):
        """Empty array must return 400."""
        response = flask_client.post(
            "/predict/batch",
            data=json.dumps([]),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_batch_predict_mixed_valid_invalid(
        self, flask_client, valid_application
    ):
        """Batch with one invalid app should return 207 Multi-Status."""
        batch = [
            valid_application,
            {"income": 50_000},  # missing required fields
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


class TestModelInfoEndpoint:
    """GET /model/info"""

    def test_model_info_returns_200(self, flask_client):
        response = flask_client.get("/model/info")
        assert response.status_code == 200

    def test_model_info_structure(self, flask_client):
        response = flask_client.get("/model/info")
        data = response.get_json()
        assert "model_name" in data
        assert "champion_version" in data
        assert "versions_available" in data


class TestErrorHandlers:
    """Error handler tests."""

    def test_404_unknown_endpoint(self, flask_client):
        response = flask_client.get("/nonexistent")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_405_wrong_method(self, flask_client):
        response = flask_client.get("/predict")   # GET on a POST-only route
        assert response.status_code == 405
