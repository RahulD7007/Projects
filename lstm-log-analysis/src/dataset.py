# src/dataset.py
import numpy as np
import pickle
from src.config import PROCESSED_DATA_DIR, VOCAB_SIZE

def generate_and_save_sessions(n_normal=500, n_anomaly=200):
    """
    Simulates parsing log lines into sessions of integer Event IDs.
    Normal logs follow a predictable sequence. Anomalies break the rules.
    """
    print("Generating synthetic log sessions...")
    sessions = [] # Will hold lists of event IDs
    labels = []   # 0 for normal, 1 for anomaly

    # The standard "healthy" sequence of our system
    normal_pattern = [1, 2, 3, 4, 5, 6, 7, 8]
    
    # 1. Generate Normal Sessions
    for _ in range(n_normal):
        # Random length between 15 and 50 lines
        length = np.random.randint(15, 50)
        # Repeat the normal pattern to fill the session
        sess = [normal_pattern[i % len(normal_pattern)] for i in range(length)]
        
        # Inject 5% random noise (normal operating jitter)
        for i in range(length):
            if np.random.rand() < 0.05:
                sess[i] = np.random.randint(1, VOCAB_SIZE - 5)
                
        sessions.append(sess)
        labels.append(0) # 0 = Normal

    # 2. Generate Anomalous Sessions
    for _ in range(n_anomaly):
        length = np.random.randint(15, 50)
        sess = [normal_pattern[i % len(normal_pattern)] for i in range(length)]
        
        # Inject a structural anomaly (simulating a crash or hack)
        fault_type = np.random.choice(['jump', 'burst', 'reverse'])
        pos = np.random.randint(5, length - 5) # Pick a random spot in the middle
        
        if fault_type == 'jump':
            sess[pos] = VOCAB_SIZE - 1 # Emit a very rare error ID
        elif fault_type == 'burst':
            sess[pos:pos+3] = [20, 20, 20] # Same error repeating fast
        else:
            sess[pos:pos+4] = list(reversed(sess[pos:pos+4])) # Execution out-of-order
            
        sessions.append(sess)
        labels.append(1) # 1 = Anomaly

    # 3. Save to disk so other scripts can use it (simulating a database/file save)
    with open(PROCESSED_DATA_DIR / 'sessions.pkl', 'wb') as f:
        pickle.dump((sessions, labels), f)
    
    print(f"Saved {len(sessions)} sessions to {PROCESSED_DATA_DIR / 'sessions.pkl'}")
    return sessions, labels

if __name__ == "__main__":
    # If we run `python -m src.dataset`, execute the function
    generate_and_save_sessions()