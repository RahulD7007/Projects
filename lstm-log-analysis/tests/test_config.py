# tests/test_config.py
import pytest
from pathlib import Path
from src import config

def test_directories_exist():
    """Verify all required directories were auto-created by config.py"""
    assert config.RAW_DATA_DIR.exists(), "Raw data folder missing"
    assert config.PROCESSED_DATA_DIR.exists(), "Processed data folder missing"
    assert config.MODELS_DIR.exists(), "Models folder missing"
    assert config.REPORTS_DIR.exists(), "Reports folder missing"

def test_hyperparameter_sanity():
    """Ensure hyperparameters are logical (no zero windows, positive layers)."""
    assert config.WINDOW_H > 0, "History window must be positive"
    assert config.TOP_K > 0 and config.TOP_K < config.VOCAB_SIZE, "K must be smaller than vocab"
    assert config.EMBED_DIM > 0
    assert config.LSTM_UNITS > 0
    assert 0.0 <= config.ANOMALY_THRESHOLD <= 1.0, "Threshold must be between 0 and 1"

def test_seed_reproducibility():
    """Ensure random seeds are locked."""
    import numpy as np
    config.set_seeds(42)
    a = np.random.rand(3)
    config.set_seeds(42)
    b = np.random.rand(3)
    np.testing.assert_array_equal(a, b, "Random seed lock is broken!")