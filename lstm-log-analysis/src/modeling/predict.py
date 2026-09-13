# src/modeling/predict.py
import json
import numpy as np
import pandas as pd
from tensorflow import keras
from src.config import (PROCESSED_DATA_DIR, MODELS_DIR, REPORTS_DIR, TOP_K)

def predict_topk_flags(model, X, y_true, k=TOP_K):
    """
    Vectorized logic:
    Predicts probabilities, gets indices of Top K highest probabilities,
    and checks if the TRUE event is inside that Top K list.
    """
    print(f"Running inference on {len(X)} windows...")
    # Get probability arrays for the whole test set at once
    probs = model.predict(X, batch_size=512, verbose=0) 
    
    # argpartition is a highly optimized numpy function to get top K indices fast
    topk_idx = np.argpartition(probs, -k, axis=1)[:, -k:] 
    
    # A window is flagged as anomalous (True) if y_true is NOT in the topk_idx
    flags = np.array([y_true[i] not in topk_idx[i] for i in range(len(y_true))])
    return flags

def run_inference():
    """End-to-end evaluation script generating final session scores."""
    print("Loading test data and model...")
    # Load test sets and original session labels
    data = np.load(PROCESSED_DATA_DIR / 'train_val_test.npz')
    X_test, y_test, sid_test = data['X_test'], data['y_test'], data['sid_test']
    
    # We also need the original labels to know which session was ACTUALLY anomalous
    import pickle
    with open(PROCESSED_DATA_DIR / 'sessions.pkl', 'rb') as f:
        _, original_labels = pickle.load(f)

    # Load the best model saved by train.py
    model = keras.models.load_model(MODELS_DIR / 'lstm_log_anomaly_model.keras')

    # Get True/False flags for every single window in the test set
    window_flags = predict_topk_flags(model, X_test, y_test, k=TOP_K)

    print("Aggregating window flags into session-level anomaly scores...")
    # Use Pandas to group by session ID and calculate the mean (fraction of True flags)
    df = pd.DataFrame({'sid': sid_test, 'flag': window_flags.astype(int)})
    sess_scores = df.groupby('sid')['flag'].mean().to_dict()

    # Compile the final operational metrics
    results = []
    unique_test_sessions = np.unique(sid_test)
    for s in unique_test_sessions:
        results.append({
            'session_id': int(s),
            'true_label': int(original_labels[int(s)]), # 1 if real anomaly, 0 if normal
            'anomaly_score': float(sess_scores[s])      # Fraction between 0.0 and 1.0
        })

    # Save results to a JSON file so plots.py can visualize it
    output_file = REPORTS_DIR / 'evaluation_metrics.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"Inference complete! Results saved to {output_file}")

if __name__ == "__main__":
    run_inference()