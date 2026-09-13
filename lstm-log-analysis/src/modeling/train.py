# src/modeling/train.py
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from src.config import (PROCESSED_DATA_DIR, MODELS_DIR, WINDOW_H, VOCAB_SIZE,
                        EMBED_DIM, LSTM_UNITS, BATCH_SIZE, EPOCHS)

def build_model():
    """Builds the DeepLog Stacked LSTM neural network."""
    # Define input layer expecting 'WINDOW_H' integers
    inp = keras.Input(shape=(WINDOW_H,), name='event_history')
    
    # Embedding layer: converts integer IDs into dense vectors of 'EMBED_DIM' length
    x = layers.Embedding(input_dim=VOCAB_SIZE, output_dim=EMBED_DIM, name='embed')(inp)
    
    # LSTM Layer 1: return_sequences=True passes the full sequence up to the next layer
    x = layers.LSTM(LSTM_UNITS, return_sequences=True, dropout=0.1, name='lstm_1')(x)
    
    # LSTM Layer 2: return_sequences=False compresses the sequence into one final state vector
    x = layers.LSTM(LSTM_UNITS, return_sequences=False, dropout=0.1, name='lstm_2')(x)
    
    # Output Layer: Softmax probabilities for every single possible next event ID in the vocab
    out = layers.Dense(VOCAB_SIZE, activation='softmax', name='output_probs')(x)
    
    # Compile model mapping inputs to outputs
    model = keras.Model(inp, out, name='DeepLog_LSTM')
    model.compile(optimizer='adam', 
                  loss='sparse_categorical_crossentropy', # Used when y is integer labels
                  metrics=['accuracy'])
    return model

def train_model():
    """Loads data, trains the model, and saves the best version."""
    print("Loading training data...")
    # Load arrays created by features.py
    data = np.load(PROCESSED_DATA_DIR / 'train_val_test.npz')
    X_train, y_train = data['X_train'], data['y_train']
    X_val, y_val = data['X_val'], data['y_val']

    model = build_model()
    model.summary()

    # Callbacks to save the best model and stop if it stops improving
    model_path = MODELS_DIR / 'lstm_log_anomaly_model.keras'
    callbacks = [
        keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        keras.callbacks.ModelCheckpoint(filepath=model_path, monitor='val_loss', save_best_only=True)
    ]

    print("Starting training...")
    # Fit the model to the data
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )

    # Save the training loss/accuracy history to JSON for plotting later
    history_dict = {k: [float(x) for x in v] for k, v in history.history.items()}
    with open(MODELS_DIR / 'model_metadata.json', 'w') as f:
        json.dump(history_dict, f, indent=4)
        
    print(f"Training complete. Model saved to {model_path}")

if __name__ == "__main__":
    train_model()