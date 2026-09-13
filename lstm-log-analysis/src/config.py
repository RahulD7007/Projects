# src/config.py
import os
import random
import numpy as np
import tensorflow as tf
from pathlib import Path

# ============================================================
# 1. DIRECTORY SETUP (Follows Cookiecutter Data Science v2)
# ============================================================
# Get the absolute path of the directory two levels up (the project root)
BASE_DIR = Path(__file__).resolve().parent.parent

# Define standard data folders
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"             # Raw log files go here
PROCESSED_DATA_DIR = DATA_DIR / "processed" # Numpy arrays go here

# Define model and output folders
MODELS_DIR = BASE_DIR / "models"            # Saved .keras models go here
REPORTS_DIR = BASE_DIR / "reports"          # Metrics JSON goes here
FIGURES_DIR = REPORTS_DIR / "figures"       # PNG plots go here

# Create directories if they don't exist yet
for d in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, REPORTS_DIR, FIGURES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ============================================================
# 2. HYPERPARAMETERS
# ============================================================
SEED = 42                # Standard seed for full reproducibility
WINDOW_H = 10            # History window: how many previous events to look at
TOP_K = 9                # Top-K threshold: if true event is in top 9 predictions, it's normal
VOCAB_SIZE = 25          # Maximum number of unique log event IDs (adjust for your logs)
EMBED_DIM = 64           # Dimensions for the embedding layer
LSTM_UNITS = 64          # Number of neurons in the LSTM layers
BATCH_SIZE = 64          # How many windows to train on at once
EPOCHS = 30              # Maximum training epochs (EarlyStopping will likely stop it sooner)
ANOMALY_THRESHOLD = 0.5  # If session anomaly score > 0.5, flag as anomaly

# ============================================================
# 3. REPRODUCIBILITY LOCK
# ============================================================
def set_seeds(seed=SEED):
    """Locks all random number generators to ensure identical results every run."""
    os.environ['PYTHONHASHSEED'] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)

set_seeds() # Execute immediately upon import