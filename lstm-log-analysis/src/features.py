# src/features.py
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from src.config import PROCESSED_DATA_DIR, WINDOW_H, SEED

def create_sliding_windows(sessions, labels, h=WINDOW_H):
    """Converts whole sessions into sliding windows of length 'h'."""
    X, y, session_ids, window_labels = [], [], [], []
    
    # Loop through every session and its corresponding label
    for s_idx, (sess, lab) in enumerate(zip(sessions, labels)):
        if len(sess) <= h:
            continue # Skip sessions shorter than our history window
            
        # Slide a window of size 'h' across the session
        for i in range(len(sess) - h):
            X.append(sess[i : i+h])     # The 'h' previous events
            y.append(sess[i+h])         # The target next event
            session_ids.append(s_idx)   # Track which session this belongs to
            window_labels.append(lab)   # Inherit the session's overall label
            
    return np.array(X), np.array(y), np.array(session_ids), np.array(window_labels)

def split_and_save_data():
    """Splits data purely by session ID to avoid data leakage."""
    print("Loading raw sessions and applying sliding windows...")
    
    # Load the parsed sessions from dataset.py
    with open(PROCESSED_DATA_DIR / 'sessions.pkl', 'rb') as f:
        sessions, labels = pickle.load(f)

    # Convert to sliding windows
    X, y, sess_ids, win_labels = create_sliding_windows(sessions, labels)
    
    unique_sessions = np.unique(sess_ids)
    session_label_map = {s: labels[s] for s in unique_sessions}

    # DeepLog Rule: We ONLY train on perfectly NORMAL sessions
    normal_sessions = [s for s in unique_sessions if session_label_map[s] == 0]
    anomaly_sessions = [s for s in unique_sessions if session_label_map[s] == 1]

    # Split normal sessions: 70% Train, 15% Val, 15% Test
    train_sess, temp_sess = train_test_split(normal_sessions, test_size=0.3, random_state=SEED)
    val_sess, test_normal_sess = train_test_split(temp_sess, test_size=0.5, random_state=SEED)

    # Test set combines unseen normal sessions + ALL anomalous sessions
    test_sess = list(test_normal_sess) + anomaly_sessions

    # Helper function to grab windows belonging to specific sessions
    def mask_windows(session_list):
        mask = np.isin(sess_ids, session_list) # Find where sess_ids match the list
        return X[mask], y[mask], sess_ids[mask]

    X_train, y_train, _ = mask_windows(train_sess)
    X_val, y_val, _ = mask_windows(val_sess)
    X_test, y_test, sid_test = mask_windows(test_sess)

    # Save finalized splits to disk for training/prediction
    np.savez(PROCESSED_DATA_DIR / 'train_val_test.npz',
             X_train=X_train, y_train=y_train,
             X_val=X_val, y_val=y_val,
             X_test=X_test, y_test=y_test, sid_test=sid_test)
             
    print(f"Data split saved. Train windows: {len(X_train)} | Test windows: {len(X_test)}")

if __name__ == "__main__":
    split_and_save_data()