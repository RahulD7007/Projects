# tests/test_model.py
import pytest
import numpy as np
import tensorflow as tf
from src.config import WINDOW_H, VOCAB_SIZE
from src.modeling.train import build_model

def test_lstm_architecture_and_output_shape():
    """
    UNIT TEST: Verifies the neural network compiles correctly
    and outputs the expected Softmax probability shapes.
    """
    # 1. Build the model
    model = build_model()
    
    # Assert the model is a valid Keras Model
    assert isinstance(model, tf.keras.Model), "Model is not a valid Keras instance"
    
    # 2. Create dummy input data (Batch of 2, history window of WINDOW_H)
    # Filling it with random integer Event IDs within our VOCAB_SIZE
    dummy_batch_size = 2
    dummy_input = np.random.randint(1, VOCAB_SIZE, size=(dummy_batch_size, WINDOW_H))
    
    # 3. Pass dummy data through the model
    predictions = model.predict(dummy_input, verbose=0)
    
    # 4. Check Output Shape
    # Expected shape: (batch_size, vocab_size) because it outputs probabilities for every word
    expected_shape = (dummy_batch_size, VOCAB_SIZE)
    assert predictions.shape == expected_shape, f"Expected shape {expected_shape}, got {predictions.shape}"
    
    # 5. Check Softmax Validity
    # A valid softmax output must sum to exactly 1.0 across the vocab axis
    row_sums = np.sum(predictions, axis=1)
    
    # np.testing.assert_allclose is used for floats because 0.9999999 != 1.0 in standard python
    np.testing.assert_allclose(row_sums, 1.0, rtol=1e-5, err_msg="Softmax probabilities do not sum to 1")
    
    print("\n✅ test_lstm_architecture passed: Model architecture is mathematically sound.")