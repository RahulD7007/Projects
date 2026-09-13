# Makefile
# ==============================================================================
# AUTOMATION COMMANDS FOR DEEPLOG LSTM PIPELINE
# ==============================================================================

.PHONY: help env data train predict report all test clean

# Default command when you just type 'make'
help:
	@echo "Available commands:"
	@echo "  make data    - Generate synthetic logs and create sliding windows"
	@echo "  make train   - Train the Stacked LSTM model on normal data"
	@echo "  make predict - Run Top-K anomaly detection on test data"
	@echo "  make report  - Generate metrics and visualization plots"
	@echo "  make all     - Run the entire pipeline end-to-end"
	@echo "  make test    - Run pytest unit tests"
	@echo "  make clean   - Delete generated data and models (reset project)"

# 1. Data Pipeline
data:
	@echo ">>> 1. Generating Data & Splits..."
	python -m src.dataset
	python -m src.features

# 2. Model Training
train:
	@echo ">>> 2. Training LSTM Model..."
	python -m src.modeling.train

# 3. Inference
predict:
	@echo ">>> 3. Running Predictions..."
	python -m src.modeling.predict

# 4. Plots and Metrics
report:
	@echo ">>> 4. Generating Reports..."
	python -m src.plots

# Run everything from start to finish
all: data train predict report
	@echo ">>> Pipeline completely successfully!"

# Run unit tests
test:
	@echo ">>> Running Pytest Suite..."
	pytest tests/ -v

# Clean up directories to start fresh
clean:
	@echo ">>> Cleaning up generated files..."
	rm -rf data/processed/*.npz data/processed/*.pkl
	rm -rf models/*.keras models/*.json
	rm -rf reports/evaluation_metrics.json reports/figures/*.png