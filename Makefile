# ─────────────────────────────────────────────────────────────────────────────
# ML_EDA_full_fledge | Makefile
# ─────────────────────────────────────────────────────────────────────────────

PYTHON   := python
VENV_DIR := .venv
PIP      := $(VENV_DIR)/Scripts/pip

.PHONY: venv data features train predict reports api flask flask-prod \
        test test-cov lint clean all

# ── Environment ───────────────────────────────────────────────────────────────
venv:
	$(PYTHON) -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Virtual environment ready."

# ── Pipeline Stages ───────────────────────────────────────────────────────────
data:
	$(PYTHON) -u -m src.dataset

features:
	$(PYTHON) -u -m src.features

train:
	$(PYTHON) -u -m src.train

predict:
	$(PYTHON) -u -m src.predict

reports:
	$(PYTHON) -u -m src.reports

api:
	$(PYTHON) -u -m src.api

# ── Flask API — Development Server ───────────────────────────────────────────
# Single worker, auto-reloads on code changes.
# Not for production use.
flask:
	$(PYTHON) -u -m src.flask_app

# ── Flask API — Production Server (Windows) ───────────────────────────────────
# Waitress is a pure-Python WSGI server that works on Windows, Linux & macOS.
# Gunicorn does NOT support Windows (requires Unix fcntl module).
# 4 threads = handles 4 concurrent requests.
flask-prod:
	$(PYTHON) -u -m waitress \
		--host=0.0.0.0 \
		--port=5000 \
		--threads=4 \
		--call "src.flask_app:create_app"

# ── Flask API — Production Server (Linux / macOS only) ───────────────────────
# Uncomment this block and comment out flask-prod above when deploying
# to a Linux/macOS server or Docker container.
# flask-prod:
# 	gunicorn "src.flask_app:create_app()" \
# 		--bind 0.0.0.0:5000 \
# 		--workers 4 \
# 		--timeout 120 \
# 		--access-logfile logs/gunicorn_access.log \
# 		--error-logfile  logs/gunicorn_error.log

# ── Quality Assurance ─────────────────────────────────────────────────────────
test:
	$(PYTHON) -m pytest tests/ -v --tb=short

test-cov:
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=html --tb=short

lint:
	$(PYTHON) -m ruff check src/ tests/

# ── Full Pipeline ─────────────────────────────────────────────────────────────
all: data features train predict reports api

# ── Cleanup ───────────────────────────────────────────────────────────────────
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f data/processed/*.csv
	rm -f models/*.joblib
	rm -rf models/registry/
	rm -f reports/metrics.json
	rm -rf reports/models/
	rm -f reports/figures/*.png
	rm -f logs/*.log
	@echo "Build artifacts removed."