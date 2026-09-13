# tests/test_predict.py
import pytest
import numpy as np
from unittest.mock import MagicMock
from src.modeling.predict import predict_topk_flags

def test_topk_flag_logic_correctness():
    """
    Simulates a fake model to test if Top-K logic flags correctly.
    """
    # Create a Mock model that returns fixed probabilities
    mock_model = MagicMock()
    
    # Fake probabilities for 2 windows, vocab size 5
    # Window 1: highest probability is index 4
    # Window 2: highest probability is index 0
    fake_probs = np.array([
        [0.1, 0.1, 0.1, 0.1, 0.6],  # top event is 4
        [0.7, 0.1, 0.1, 0.05, 0.05]  # top event is 0
    ])
    mock_model.predict.return_value = fake_probs
    
    # Fake input windows (not actually used since predict is mocked)
    X_fake = np.zeros((2, 10))
    
    # Case 1: True labels match top predictions -> should NOT flag
    y_true = np.array([4, 0])
    flags = predict_topk_flags(mock_model, X_fake, y_true, k=1)
    assert not flags[0], "Should not flag when true event is #1 prediction"
    assert not flags[1], "Should not flag when true event is #1 prediction"

    # Case 2: True labels DON'T match top predictions -> should flag
    y_true = np.array([2, 3])  # Neither is the top-1 probability
    flags = predict_topk_flags(mock_model, X_fake, y_true, k=1)
    assert flags[0], "Should flag anomaly when true event not in top-K"
    assert flags[1], "Should flag anomaly when true event not in top-K"

def test_topk_with_higher_k():
    """Increasing K should reduce anomaly flags."""
    mock_model = MagicMock()
    fake_probs = np.array([[0.1, 0.2, 0.3, 0.15, 0.25]])  # Sorted: 2,4,1,3,0
    mock_model.predict.return_value = fake_probs
    
    X_fake = np.zeros((1, 10))
    y_true = np.array([3])  # Rank #4
    
    # K=2: True label (3) is NOT in top-2 (2, 4) -> flag anomaly
    flags_k2 = predict_topk_flags(mock_model, X_fake, y_true, k=2)
    assert flags_k2[0] == True
    
    # K=4: True label (3) IS in top-4 (2, 4, 1, 3) -> normal
    flags_k4 = predict_topk_flags(mock_model, X_fake, y_true, k=4)
    assert flags_k4[0] == False