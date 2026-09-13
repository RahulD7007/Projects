# tests/test_dataset.py
import pytest
from src.dataset import generate_and_save_sessions

def test_session_generation_counts():
    """Verify the correct number of normal and anomaly sessions are created."""
    sessions, labels = generate_and_save_sessions(n_normal=100, n_anomaly=50)
    
    # Total should match input
    assert len(sessions) == 150, "Wrong total number of sessions"
    assert len(labels) == 150, "Labels mismatch"
    
    # Verify label distribution
    assert labels.count(0) == 100, "Normal count wrong"
    assert labels.count(1) == 50, "Anomaly count wrong"

def test_session_content_integrity():
    """Sessions must be non-empty lists of integers."""
    sessions, _ = generate_and_save_sessions(n_normal=10, n_anomaly=10)
    for sess in sessions:
        assert isinstance(sess, list), "Session must be a list"
        assert len(sess) > 0, "Session cannot be empty"
        assert all(isinstance(e, int) for e in sess), "All events must be integers"
        assert all(e >= 0 for e in sess), "Event IDs cannot be negative"