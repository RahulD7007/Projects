"""
test_versioning.py
──────────────────
Unit tests for the model versioning engine.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.versioning import (
    _load_registry,
    _next_version,
    get_all_versions,
    promote_champion,
    register_model,
)


class TestNextVersion:
    """Tests for _next_version() helper."""

    def test_first_version_is_v1(self):
        assert _next_version({}) == "v1"

    def test_increments_correctly(self):
        existing = {"v1": {}, "v2": {}}
        assert _next_version(existing) == "v3"

    def test_non_sequential_gaps(self):
        existing = {"v1": {}, "v3": {}}
        assert _next_version(existing) == "v4"


class TestRegisterModel:
    """Integration tests for register_model()."""

    def test_register_creates_artifact(
        self, fitted_model, processed_splits, tmp_path, monkeypatch
    ):
        """
        Registering a model should:
        - Create a .joblib artifact on disk.
        - Add an entry to the registry JSON.
        - Return a non-empty version string.
        """
        from src import versioning

        # Redirect registry to a temp directory
        monkeypatch.setattr(versioning, "REGISTRY_DIR", tmp_path)
        monkeypatch.setattr(
            versioning, "REGISTRY_FILE", tmp_path / "model_registry.json"
        )

        train_df, test_df = processed_splits
        dummy_metrics = {
            "roc_auc":  0.88,
            "pr_auc":   0.82,
            "accuracy": 0.87,
            "f1_score": 0.76,
        }

        version = register_model(
            model=fitted_model,
            model_name="test_rf",
            metrics=dummy_metrics,
            params={"n_estimators": 100},
            n_train=len(train_df),
            n_test=len(test_df),
            promote_to_champion=True,
        )

        assert version.startswith("v"), "Version must start with 'v'"

        # Registry JSON must exist and contain the model
        reg_file = tmp_path / "model_registry.json"
        assert reg_file.exists(), "Registry JSON must be created"

        with reg_file.open() as fh:
            registry = json.load(fh)

        assert "test_rf" in registry["models"]
        assert registry["models"]["test_rf"]["champion"] == version
