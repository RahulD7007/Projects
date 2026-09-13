# tests/test_features.py
import pytest
import numpy as np
from src.features import create_sliding_windows
from src.config import WINDOW_H

def test_sliding_window_shape():
    """Windows should have exactly WINDOW_H events and 1 target."""
    # Create mock data: 1 session of 20 events
    sessions = [[1, 2, 3, 4, 5, 6, 7, 8] * 3]  # 24 events
    labels = [0]
    
    X, y, sids, wlabels = create_sliding_windows(sessions, labels, h=WINDOW_H)
    
    # Each row of X must have exactly WINDOW_H columns
    assert X.shape[1] == WINDOW_H, f"X should have {WINDOW_H} columns"
    
    # For a session of length L, we should get (L - h) windows
    expected_windows = 24 - WINDOW_H
    assert X.shape[0] == expected_windows, f"Wrong number of windows"
    
    # y should be 1D (one target per window)
    assert y.ndim == 1

def test_short_sessions_are_skipped():
    """Sessions shorter than window size should be skipped."""
    short_session = [[1, 2, 3]]  # Only 3 events, less than WINDOW_H=10
    labels = [0]
    
    X, y, _, _ = create_sliding_windows(short_session, labels, h=WINDOW_H)
    
    assert len(X) == 0, "Short sessions should not produce windows"
    assert len(y) == 0