# src/test_scripts/test_pipeline.py
import sys
import time
from src.dataset import generate_and_save_sessions
from src.features import split_and_save_data
from src.modeling.train import train_model
from src.modeling.predict import run_inference
from src.plots import generate_report

def run_full_pipeline():
    """
    Executes the entire DeepLog pipeline programmatically.
    Useful for CI/CD (Continuous Integration) pipelines (like GitHub Actions).
    """
    print("\n" + "="*50)
    print("🚀 STARTING END-TO-END DEEPLOG PIPELINE")
    print("="*50 + "\n")
    
    start_time = time.time()
    
    try:
        # Step 1: Raw Logs to Sessions
        print("[1/5] Running Log Parser & Session Generator...")
        generate_and_save_sessions(n_normal=200, n_anomaly=50) # Smaller numbers for fast testing
        
        # Step 2: Sessions to Sliding Windows
        print("\n[2/5] Running Feature Engineering (Sliding Windows)...")
        split_and_save_data()
        
        # Step 3: Train LSTM
        print("\n[3/5] Compiling and Training Stacked LSTM...")
        train_model()
        
        # Step 4: Top-K Anomaly Detection
        print("\n[4/5] Running Top-K Inference on Test Set...")
        run_inference()
        
        # Step 5: Metrics and Visuals
        print("\n[5/5] Generating Final Reports...")
        generate_report()
        
        elapsed = time.time() - start_time
        print("\n" + "="*50)
        print(f"✅ >>> Full end-to-end pipeline finished successfully in {elapsed:.2f} seconds!")
        print("="*50 + "\n")
        
    except Exception as e:
        print("\n" + "❌"*25)
        print(f"PIPELINE FAILED: {str(e)}")
        print("❌"*25 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    run_full_pipeline()